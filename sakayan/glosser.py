#!/usr/bin/env python3
"""Word-by-word Armenian text glosser via Wiktionary.

Tokenize Armenian text, look up each token (and its likely lemma after
stripping definite-article / case suffixes) on Wiktionary using the
existing `lookup.py` machinery, and emit a Markdown table with verbatim
form, candidate lemma, English gloss(es), and a status flag.

Purpose: a *verification tier* for translations and analyses I produce
when summarizing Armenian text. Every token is paired with an
independent dictionary entry, so a hallucinated translation is visible
at a glance — `not-found` and `multi-meaning` rows flag where my prose
goes beyond what the dictionary alone confirms.

Usage:
    .venv/bin/python glosser.py "ա-ն փոխարինում է է օժանդակ բային"
    echo "Բարև ձեզ։" | .venv/bin/python glosser.py
    .venv/bin/python glosser.py --json "գրում ա, գալիս ա"
    .venv/bin/python glosser.py --file ../ghamoyan/some_passage.txt
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import lookup


# Common Eastern Armenian noun/verb suffixes that may attach to the
# bare lemma. Stripped longest-first so multi-char suffixes win.
# Suffixes intentionally limited to high-frequency ones — over-stripping
# produces wrong lemmas.
SUFFIXES: list[str] = sorted(
    [
        # noun: definite article, case endings (genitive, dative, ablative,
        # instrumental, accusative)
        "երից", "ներից", "ներով", "ներում", "ների", "ներ",
        "ից", "ով", "ում", "ին", "ի", "ն", "ը", "ս", "դ",
        # verb: extremely common conjugated/participle endings — only
        # patterns where the bare stem is a real lemma (infinitive)
        "ելու", "ալու", "ելիք", "ալիք", "ելիս", "ալիս",
        "ում", "ած", "ել", "ալ", "ող",
    ],
    key=len,
    reverse=True,
)


# Suffix → suffix substitutions for cases where lemma differs from a
# simple truncation. Most common: abstract-noun `-ություն` whose genitive
# replaces final `-ն` with `-ան` (e.g. էություն → էության).
SUBSTITUTIONS: list[tuple[str, str]] = [
    ("ության", "ություն"),
    ("ությամբ", "ություն"),
    ("ությունում", "ություն"),
    ("ությունից", "ություն"),
    ("ությունները", "ություն"),
]

# Match runs of Armenian letters (skip punctuation, digits, Latin words).
ARMENIAN_TOKEN = re.compile(r"[Ա-Ֆա-ֈ]+")


def lemma_candidates(token: str) -> list[str]:
    """Return the token followed by article-/case-stripped variants,
    preserving order. Always tries the original form first."""
    out = [token]
    # Suffix substitutions (handle paradigms like -ություն ↔ -ության).
    for old, new in SUBSTITUTIONS:
        if token.endswith(old):
            candidate = token[: -len(old)] + new
            if candidate not in out:
                out.append(candidate)
    # Plain suffix stripping for case/article endings.
    for suf in SUFFIXES:
        if token.endswith(suf) and len(token) - len(suf) >= 2:
            stem = token[: -len(suf)]
            if stem not in out:
                out.append(stem)
    return out


def gloss_token(token: str, max_defs: int = 3) -> dict:
    """Return {form, lemma, parts, definitions, status}.

    status ∈ {found, multi-meaning, not-found}.
    `parts` is the list of (POS, [definitions]) — useful when the token
    is genuinely ambiguous between e.g. noun and verb."""
    for i, lemma in enumerate(lemma_candidates(token)):
        # Throttle Wiktionary requests. Cache hits don't go to network so
        # only sleep when we're actually about to fetch.
        cache_path = lookup.CACHE / f"wiki-{lemma}.json"
        if not cache_path.exists():
            time.sleep(0.5)
        wikitext = lookup.fetch_wikitext(lemma)
        if not wikitext:
            continue
        parsed = lookup.parse_armenian(wikitext)
        if not parsed.get("found") or not parsed.get("pos"):
            continue
        all_defs: list[str] = []
        parts: list[tuple[str, list[str]]] = []
        for entry in parsed["pos"]:
            entry_defs = entry["definitions"][:max_defs]
            parts.append((entry["part_of_speech"], entry_defs))
            all_defs.extend(entry_defs)
        status = "multi-meaning" if len(all_defs) >= 4 else "found"
        return {
            "form": token,
            "lemma": lemma,
            "parts": parts,
            "definitions": all_defs[:max_defs],
            "status": status,
        }
    return {
        "form": token, "lemma": token,
        "parts": [], "definitions": [],
        "status": "not-found",
    }


def render_markdown(results: list[dict]) -> str:
    out = ["| token | lemma | POS — gloss | status |",
           "|-------|-------|-------------|--------|"]
    for r in results:
        if r["parts"]:
            cells = []
            for pos, defs in r["parts"]:
                cells.append(f"*{pos}*: " + "; ".join(defs))
            gloss = " <br>".join(cells)
        else:
            gloss = "—"
        same = (r["form"] == r["lemma"])
        lemma_cell = "—" if same else r["lemma"]
        flag = {"found": "✓", "multi-meaning": "?", "not-found": "✗"}[r["status"]]
        out.append(f"| {r['form']} | {lemma_cell} | {gloss[:200]} | {flag} {r['status']} |")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="?",
                    help="Armenian text to gloss (omit to read stdin)")
    ap.add_argument("--file", type=Path,
                    help="read text from a file instead")
    ap.add_argument("--json", action="store_true",
                    help="emit JSON instead of Markdown table")
    ap.add_argument("--unique", action="store_true",
                    help="dedupe tokens (case-sensitive)")
    args = ap.parse_args()

    if args.file:
        text = args.file.read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    tokens = ARMENIAN_TOKEN.findall(text)
    if args.unique:
        seen = set()
        tokens = [t for t in tokens if not (t in seen or seen.add(t))]

    results = [gloss_token(t) for t in tokens]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(results))
        # Summary
        by_status = {"found": 0, "multi-meaning": 0, "not-found": 0}
        for r in results:
            by_status[r["status"]] += 1
        print(f"\n_{len(results)} tokens · "
              f"{by_status['found']} found · "
              f"{by_status['multi-meaning']} multi-meaning · "
              f"{by_status['not-found']} not-found_")


if __name__ == "__main__":
    main()
