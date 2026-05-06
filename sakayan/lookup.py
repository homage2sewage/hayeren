#!/usr/bin/env python3
"""Look up an Armenian word on Wiktionary.

Uses the MediaWiki action API (no auth, no key) to fetch the wikitext
and rendered HTML of an entry, then surfaces the parts useful when
adding a word to your study deck:

    - English definitions
    - Pronunciation (IPA, where listed)
    - Inflection / declension / conjugation pointer
    - Derived terms (when you want to expand the family)
    - Direct link to the page (so you can jump to the rendered table)

Usage:
    .venv/bin/python lookup.py գիրք                  # default summary
    .venv/bin/python lookup.py գրել                  # any word
    .venv/bin/python lookup.py գրել --raw            # dump raw wikitext
    .venv/bin/python lookup.py գրել --html           # fetch rendered HTML
    .venv/bin/python lookup.py գրել --json           # machine-readable

Caches responses under .cache/lookup/ so repeat lookups are instant.
"""

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional


HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache" / "lookup"
WIKT = "https://en.wiktionary.org/w/api.php"
USER_AGENT = "hayeren-lookup/0.1 (personal study tool)"


def _fetch(url: str, cache_key: str, ttl_days: int = 30) -> str | None:
    """Cached HTTP GET as text. Returns None on 404/missing entry.
    Retries with exponential backoff on 429 (rate limit)."""
    import time
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / cache_key
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    delay = 1.0
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read().decode("utf-8")
            cache_path.write_text(body, encoding="utf-8")
            return body
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429 and attempt < 3:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    return None


def fetch_wikitext(word: str) -> Optional[str]:
    params = {
        "action": "parse", "page": word, "prop": "wikitext",
        "format": "json", "redirects": 1,
    }
    url = f"{WIKT}?{urllib.parse.urlencode(params)}"
    body = _fetch(url, f"wiki-{word}.json")
    if body is None:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    if "error" in data:
        return None
    return data["parse"]["wikitext"]["*"]


def fetch_html(word: str) -> Optional[str]:
    params = {
        "action": "parse", "page": word, "prop": "text",
        "format": "json", "redirects": 1, "disableeditsection": 1,
    }
    url = f"{WIKT}?{urllib.parse.urlencode(params)}"
    body = _fetch(url, f"wiki-html-{word}.json")
    if body is None:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    if "error" in data:
        return None
    return data["parse"]["text"]["*"]


# ----- wikitext parsing -----

def _section(wikitext: str, name: str) -> Optional[str]:
    """Extract the body of `==<name>==` ... up to next `==<other>==` (same level)."""
    pat = rf"==\s*{re.escape(name)}\s*==(.*?)(?=\n==[^=]|\Z)"
    m = re.search(pat, wikitext, re.DOTALL)
    return m.group(1) if m else None


def _subsection(armenian: str, name: str) -> Optional[str]:
    """Extract the body of `===<name>===` from the Armenian section."""
    pat = rf"===\s*{re.escape(name)}\s*===(.*?)(?=\n=={{2,4}}[^=]|\Z)"
    m = re.search(pat, armenian, re.DOTALL)
    return m.group(1) if m else None


def _strip_templates(s: str) -> str:
    """Best-effort: replace common Wiktionary templates with their content,
    then strip the rest. Handles the templates that show up in Armenian
    etymologies and definitions:
        {{m|hy|word|gloss}}     — link to a word, optional gloss
        {{l|hy|word}}           — same kind of link
        {{uder|hy|xcl|word}}    — universal derivation: 'from <word>'
        {{inh+|hy|xcl|word}}    — inherited form: 'inherited from <word>'
        {{cog|xcl|word}}        — cognate: '(cognate <word>)'
    """
    # Inheritance / derivation prefixes — preserve the source word.
    s = re.sub(r"\{\{inh\+?\|[^|}]+\|[^|}]+\|([^|}]+)[^}]*\}\}",
               r"inherited from \1", s)
    s = re.sub(r"\{\{u?der\+?\|[^|}]+\|[^|}]+\|([^|}]+)[^}]*\}\}",
               r"from \1", s)
    s = re.sub(r"\{\{cog\|[^|}]+\|([^|}]+)[^}]*\}\}",
               r"(cognate \1)", s)
    # Plain link templates — keep just the linked word.
    s = re.sub(r"\{\{[ml]\|[a-z\-]+\|([^|}]+)[^}]*\}\}", r"\1", s)
    # Inflection-of templates: pull the lemma + form description.
    s = re.sub(r"\{\{inflection of\|[a-z\-]+\|([^|}]+)\|\|([^}]*)\}\}",
               lambda m: f"{m.group(1)} ({m.group(2).replace('|', ' ')})", s)
    # Drop everything else (nested may need two passes).
    for _ in range(3):
        s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"\[\[([^\[\]\|]+)\|([^\[\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\[\]]+)\]\]", r"\1", s)
    s = re.sub(r"'{2,3}([^']+)'{2,3}", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# Sections that introduce parts of speech and may carry "# definition" lines.
POS_SECTIONS = ["Noun", "Verb", "Adjective", "Adverb", "Pronoun",
                "Numeral", "Preposition", "Postposition", "Conjunction",
                "Interjection", "Particle", "Determiner", "Article",
                "Letter", "Symbol", "Phrase", "Proper noun"]


def parse_armenian(wikitext: str) -> dict:
    """Walk the ==Armenian== section, return a structured dict."""
    arm = _section(wikitext, "Armenian")
    if arm is None:
        return {"found": False}

    out: dict = {"found": True, "pos": []}

    # Pronunciation — capture template names, useful as a pointer.
    pron_section = _subsection(arm, "Pronunciation")
    if pron_section:
        ipas = re.findall(r"\{\{IPA\|hy\|/([^/]+)/", pron_section)
        out["ipa"] = ipas
        out["pronunciation_raw"] = pron_section.strip().split("\n")[:8]

    # Etymology — first sentence.
    ety = _subsection(arm, "Etymology")
    if ety:
        out["etymology"] = _strip_templates(ety).split("\n")[0][:300]

    # Each part of speech: definitions are "# ..." lines under that section.
    for pos in POS_SECTIONS:
        body = _subsection(arm, pos)
        if not body:
            continue
        defs = []
        for line in body.split("\n"):
            line = line.rstrip()
            if line.startswith("# ") and not line.startswith("#:") and not line.startswith("#*"):
                cleaned = _strip_templates(line[2:])
                if cleaned:
                    defs.append(cleaned)
        if defs:
            out["pos"].append({"part_of_speech": pos, "definitions": defs})

    # Inflection / Declension / Conjugation — point to the template.
    for sect in ["Inflection", "Conjugation", "Declension"]:
        body = _subsection(arm, sect)
        if body:
            tmpls = re.findall(r"\{\{(hy[^|}]*|hyw[^|}]*)", body)
            out[sect.lower()] = tmpls

    # Derived terms — list of links inside {{col|hy|...}}.
    derived = _subsection(arm, "Derived terms")
    if derived:
        m = re.search(r"\{\{col\|hy\|([^}]+)\}\}", derived)
        if m:
            out["derived_terms"] = [t.strip() for t in m.group(1).split("|") if t.strip()]

    return out


# ----- HTML parsing for tables -----

def extract_inflection_table(rendered_html: str) -> Optional[str]:
    """Pull the inflection/declension/conjugation table HTML block."""
    m = re.search(
        r'<table[^>]*class="[^"]*(?:inflection-table|hy-conjugation|hy-declension)[^"]*".*?</table>',
        rendered_html, re.DOTALL,
    )
    return m.group(0) if m else None


def _strip_html_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def render_table_text(table_html: str) -> str:
    """Convert the Wiktionary inflection-table HTML into plain-text rows.
    Each <tr> becomes one line; cells are joined with `  |  `."""
    rows: list[list[str]] = []
    caption = ""
    cap_m = re.search(r"<caption[^>]*>(.*?)</caption>", table_html, re.DOTALL)
    if cap_m:
        caption = _strip_html_tags(cap_m.group(1))
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.DOTALL)
        if cells:
            rows.append([_strip_html_tags(c) for c in cells])
    out = []
    if caption:
        out.append(caption)
        out.append("")
    # Compute column widths.
    if rows:
        cols = max(len(r) for r in rows)
        widths = [0] * cols
        for r in rows:
            for i, cell in enumerate(r):
                widths[i] = max(widths[i], min(len(cell), 28))
        for r in rows:
            padded = [
                (r[i] if i < len(r) else "").ljust(widths[i] if i < len(widths) else 0)
                for i in range(cols)
            ]
            out.append("  ".join(padded).rstrip())
    return "\n".join(out)


# ----- Output -----

def print_summary(word: str, parsed: dict) -> None:
    qword = urllib.parse.quote(word)
    if not parsed.get("found"):
        print(f"  No Armenian section on Wiktionary for {word!r}.")
        print(f"  Try bararan.am: https://bararan.am/search/{qword}")
        return
    print(f"  Wiktionary:   https://en.wiktionary.org/wiki/{qword}#Armenian")
    print(f"  bararan.am:   https://bararan.am/search/{qword}")
    if parsed.get("ipa"):
        print(f"  IPA: " + " / ".join(f"/{ipa}/" for ipa in parsed["ipa"]))
    if parsed.get("etymology"):
        print(f"  Etymology: {parsed['etymology']}")
    for entry in parsed["pos"]:
        print(f"\n  {entry['part_of_speech']}:")
        for d in entry["definitions"]:
            print(f"    • {d}")
    for tag in ("inflection", "conjugation", "declension"):
        if parsed.get(tag):
            print(f"\n  {tag.title()}: {', '.join(parsed[tag])}")
    if parsed.get("derived_terms"):
        terms = parsed["derived_terms"]
        print(f"\n  Derived terms ({len(terms)}): " + ", ".join(terms[:12]))
        if len(terms) > 12:
            print(f"    … and {len(terms) - 12} more.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("word", help="Armenian word to look up")
    ap.add_argument("--raw", action="store_true",
                    help="dump raw wikitext")
    ap.add_argument("--html", action="store_true",
                    help="dump raw HTML of the inflection/declension table")
    ap.add_argument("--table", action="store_true",
                    help="pretty-print the inflection/declension table as text")
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON")
    args = ap.parse_args()

    word = args.word.strip()
    wikitext = fetch_wikitext(word)

    if args.raw:
        print(wikitext or f"# no entry for {word!r}", end="")
        return

    if not wikitext:
        print(f"  No Wiktionary entry for {word!r}.")
        sys.exit(1)

    parsed = parse_armenian(wikitext)

    if args.html or args.table:
        rendered = fetch_html(word)
        table = extract_inflection_table(rendered) if rendered else None
        if not table:
            print(f"  No inflection table found in HTML for {word!r}.")
            return
        print(render_table_text(table) if args.table else table)
        return

    if args.json:
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        return

    print_summary(word, parsed)


if __name__ == "__main__":
    main()
