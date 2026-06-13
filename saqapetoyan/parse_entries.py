#!/usr/bin/env python3
"""Parse the saqapetoyan neologism glossary (body pp. 9-76) from the
line-level `out/full.jsonl` into one structured record per dictionary
entry.

Entry shape in the book:

    HEADWORD – POS[.(domain.)] [definition ՝] COINAGE[, COINAGE2 …], <ru>, <en>.

Parsing strategy
----------------
1. Take body lines only (pp. BODY_START..BODY_END); drop page-number
   lines and single-letter alphabet section headers.
2. Group lines into entries: a line *starts* a new entry iff it begins
   with a capital Armenian letter and contains the ' – ' (en-dash)
   headword separator. Everything up to the next such line is one entry.
3. Reconstruct entry text by de-hyphenating line-final splits
   (`word-`\n`rest` → `wordrest`; otherwise join with a space).
4. Split the headword off on the first ' – '.
5. Parse leading POS / domain / language-of-origin tags off the body.
6. **Right-anchored, script-based field split** of the remainder:
   the trailing Latin run = `en`, the Cyrillic run before it = `ru`,
   everything before = the Armenian gloss (definition + coinages).
   This is robust to entries carrying several comma-separated native
   synonyms, numbered senses, etc.
7. Split the Armenian gloss on '՝' into (definition, coinage-list) when
   present; otherwise the whole gloss is the coinage-list.

IMPORTANT editorial note (per user direction): a native COINAGE is the
book's *proposed* Armenian replacement — its existence here does **not**
mean it is actually used (e.g. մսադոնդող for Russian холодец/holodets
returns ~nothing on the open web). Treat `native_coinages` as
prescriptive suggestions, `definition` as the reliable meaning signal,
and the `ru`/headword pair as the colloquial-usage signal. The inverse
map (coinage → headword) is still useful as a synonym/explanation index
because some coinages are common words.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSONL = HERE / "out" / "full.jsonl"

BODY_START, BODY_END = 9, 76  # Ա … Ֆ glossary body

ARM_UPPER = "Ա-Ֆ"          # Ա..Ֆ
ARM_LOWER = "ա-ֆև"    # ա..ֆ plus և (ligature)
EN_DASH = "–"              # – EN DASH (headword separator)
# The definition↔coinage boundary is printed inconsistently as the
# ARMENIAN COMMA ՝ (U+055D) or a GRAVE ACCENT ` (U+0060) standing in for it.
# Treat both as the same mark; the LAST one in the Armenian region is the
# boundary (earlier ones are intra-definition, like a secondary comma).
DEF_MARKS = ("՝", "`")

# A headword line: an Armenian word (upper- OR lowercase initial — the
# book occasionally lowercases, e.g. p25 'էլեկտրաթերապիա'), optionally with
# a parenthetical, then the headword separator, then Armenian/digit content.
# The separator is en-dash OR hyphen-minus (p37 'Կենգուրու - գ.') with
# flexible spacing (p68 'Տեխնիկ –գ.' has none after the dash). Pre-dash is
# Armenian-script only, so this never fires on a Cyrillic/Latin or mid-word
# continuation line.
# Headword separator: a dash with at least one ADJACENT space. This is what
# distinguishes the field separator (' – ', ' –', '- ') from an intra-headword
# hyphen in a compound loanword (Ուիք-էնդ, Աուդիո–վիդեո — no flanking spaces).
SEP_RE = re.compile(r"\s+[–-]\s*|[–-]\s+")
HEADWORD_RE = re.compile(
    # pre-dash: Armenian word(s), allowing a homograph digit (Ավտոմատ1),
    # a parenthetical (Ռակետ (թենիսի)), and internal spaces (Հարդ դիսկ).
    rf"^[{ARM_UPPER}{ARM_LOWER}][{ARM_UPPER}{ARM_LOWER}0-9()\s]{{0,25}}?"
    # then the dash separator, then POS/domain/sense content — Armenian,
    # a digit (numbered sense), or '(' (domain-first, Հիպոֆիզ – (կենս.)).
    rf"\s*[–-]\s*(?=[{ARM_UPPER}{ARM_LOWER}0-9(])"
)

# Leading tag block right after ' – ': a run of `abbr.` tokens and
# parenthetical `(domain.)` groups, e.g. "գ.", "ած.գ.", "գ.(ախտ.)",
# "ած. (փիլ.)". Captured greedily, then sub-split below.
TAG_BLOCK_RE = re.compile(
    rf"^((?:[{ARM_UPPER}{ARM_LOWER}]+\.|\([^)]*\))[\s]*)+"
)
# Domain / language tags live inside parens; POS tags are the bare
# `xxx.` tokens. We don't hard-code the tag set — we record what's there.
PAREN_RE = re.compile(r"\(([^)]*)\)")

CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]")
LATIN_RE = re.compile(r"[A-Za-z]")
ARM_LETTER_RE = re.compile(rf"[{ARM_UPPER}{ARM_LOWER}]")
TRAIL_LATIN_RE = re.compile(r"([A-Za-z][A-Za-z'\- ]*[A-Za-z]|[A-Za-z])\s*$")
# trailing Cyrillic run, optionally preceded by a ':'-class field separator
TRAIL_CYR_RE = re.compile(r"[:;։፡]?\s*([Ѐ-ӿ][Ѐ-ӿ'\- ]*[Ѐ-ӿ]|[Ѐ-ӿ])\s*$")


def squash(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip()


def arm_word_count(s: str) -> int:
    return sum(1 for w in s.split() if ARM_LETTER_RE.search(w))


def dominant_script(s: str) -> str:
    """Majority letter-script of a field chunk: 'latin' / 'cyrillic' /
    'armenian' / 'other'. Majority (not 'any') so a single homoglyph —
    e.g. the Cyrillic 'а' in the mistyped English 'аltruist' — doesn't
    flip an English field to Russian."""
    lat = len(LATIN_RE.findall(s))
    cyr = len(CYRILLIC_RE.findall(s))
    arm = len(ARM_LETTER_RE.findall(s))
    best = max(lat, cyr, arm)
    if best == 0:
        return "other"
    if best == arm:
        return "armenian"
    if best == cyr:
        return "cyrillic"
    return "latin"


def load_body_lines() -> list[dict]:
    lines = []
    for ln in JSONL.open(encoding="utf-8"):
        e = json.loads(ln)
        if not (BODY_START <= e["page"] <= BODY_END):
            continue
        t = e["text"].rstrip()
        s = t.strip()
        if not s:
            continue
        if s.isdigit():            # page number
            continue
        if len(s) <= 2 and re.fullmatch(rf"[{ARM_UPPER}]Ւ?", s):
            continue               # single-letter section header (incl. ՈՒ)
        lines.append({"page": e["page"], "text": t})
    return lines


def group_entries(lines: list[dict]) -> list[dict]:
    """Group consecutive lines into entries, de-hyphenating splits."""
    entries: list[dict] = []
    cur_lines: list[str] = []
    cur_page = None

    def flush():
        if not cur_lines:
            return
        buf = cur_lines[0].strip()
        for nxt in cur_lines[1:]:
            nxt = nxt.strip()
            if buf.endswith("-") or buf.endswith("‐"):
                buf = buf[:-1] + nxt          # de-hyphenate, no space
            else:
                buf = buf + " " + nxt
        entries.append({"page": cur_page, "raw": squash(buf)})

    for ln in lines:
        if HEADWORD_RE.match(ln["text"].strip()):
            flush()
            cur_lines = [ln["text"]]
            cur_page = ln["page"]
        else:
            if not cur_lines:
                # stray line before first headword (shouldn't happen in body)
                continue
            cur_lines.append(ln["text"])
    flush()
    return entries


def parse_entry(raw: str, page: int) -> dict:
    rec: dict = {
        "page": page, "headword": None, "homograph": None, "pos": None,
        "domain": [], "lang_origin": [], "definition": None,
        "native_coinages": [], "ru": None, "en": None, "raw": raw,
        "warnings": [],
    }

    # 1. headword | rest  (first dash separator)
    m = SEP_RE.search(raw)
    if not m:
        rec["warnings"].append("no-headword-sep")
        return rec
    headword = squash(raw[: m.start()])
    # trailing homograph index (Ավտոմատ1, Ավտոմատ2) → split into field
    hm = re.match(r"^(.*?)(\d+)$", headword)
    if hm:
        headword, rec["homograph"] = hm.group(1), int(hm.group(2))
    rec["headword"] = headword
    rest = raw[m.end():].strip()
    # POS-terminator typo: a short leading abbrev closed by ',' not '.'
    # (e.g. "գ, Մասնակի…" on p31) — normalise so the tag block matches.
    rest = re.sub(rf"^([{ARM_UPPER}{ARM_LOWER}]{{1,3}}),(\s)", r"\1.\2", rest)

    # 2. leading tag block → pos + parenthetical (domain / lang)
    tm = TAG_BLOCK_RE.match(rest)
    if tm:
        tag_block = tm.group(0)
        rest = rest[tm.end():].strip()
        parens = PAREN_RE.findall(tag_block)
        # POS = tag block minus the parenthetical groups, trimmed
        pos = PAREN_RE.sub("", tag_block).strip()
        rec["pos"] = pos or None
        for p in parens:
            for tok in re.split(r"[,\s]+", p.strip()):
                tok = tok.strip()
                if not tok:
                    continue
                # language-of-origin tags (per abbrev list pp.7-8)
                if tok in ("արաբ.", "գերմ.", "ֆր.", "Արաբ.", "Գերմ.", "Ֆր."):
                    rec["lang_origin"].append(tok)
                else:
                    rec["domain"].append(tok)
    else:
        rec["warnings"].append("no-pos-tag")

    # 3. right-anchored, majority-script field split. Pop ALL trailing
    #    Latin-dominant chunks as the English run, then ALL Cyrillic-
    #    dominant chunks as the Russian run; the rest is Armenian.
    body = rest.rstrip(". ").strip()
    arm_parts = [p.strip() for p in body.split(",") if p.strip()]
    en_chunks, ru_chunks = [], []
    strip_sense = lambda s: re.sub(r"^\d+\.\s*", "", s.strip(". "))
    while arm_parts and dominant_script(arm_parts[-1]) == "latin":
        en_chunks.insert(0, strip_sense(arm_parts.pop()))
    while arm_parts and dominant_script(arm_parts[-1]) == "cyrillic":
        chunk = arm_parts.pop().strip(". ")
        # rescue a coinage glued to ru by a ':' inside one chunk, e.g.
        # "Ծինական: генетический" — the chunk is Cyrillic-dominant so it
        # popped whole, but its leading Armenian part is a lost coinage.
        cm = re.match(rf"^([{ARM_UPPER}{ARM_LOWER}][{ARM_UPPER}{ARM_LOWER} ]*?)\s*[:։]\s*(.+)$", chunk)
        if cm:
            arm_parts.append(cm.group(1).strip())   # push coinage back → loop stops
            chunk = cm.group(2).strip()
        ru_chunks.insert(0, strip_sense(chunk))
    # salvage a ':'-/space-separated or missing-comma source typo where
    # ru got stranded inside the last Armenian-dominant chunk, e.g.
    # "Վերանցական: априори", "Ծծըմբատ сульфат". Only fires when no ru
    # was popped, so it can't eat a legitimate all-Armenian coinage.
    if not ru_chunks and arm_parts:
        ctail = TRAIL_CYR_RE.search(arm_parts[-1])
        if ctail:
            ru_chunks.append(ctail.group(1).strip())
            arm_parts[-1] = arm_parts[-1][: ctail.start()].strip(". :;։").strip()
            if not arm_parts[-1]:
                arm_parts.pop()
    # symmetric salvage for a missing-comma English tail:
    # "…декадентство decadence" (Cyrillic chunk ending in an English word).
    if not en_chunks and ru_chunks:
        tail = TRAIL_LATIN_RE.search(ru_chunks[-1])
        if tail and len(tail.group(1).replace(" ", "")) >= 3:
            en_chunks.append(tail.group(1).strip())
            ru_chunks[-1] = ru_chunks[-1][: tail.start()].strip(". ").strip()
    rec["en"] = ", ".join(en_chunks) or None
    rec["ru"] = ", ".join(c for c in ru_chunks if c) or None
    if not en_chunks:
        rec["warnings"].append("no-english")
    if not rec["ru"]:
        rec["warnings"].append("no-russian")

    arm = ", ".join(arm_parts).strip()

    # 4. definition <mark> coinage-list. Split on the LAST def-mark (՝ or `).
    cut = max(arm.rfind(mk) for mk in DEF_MARKS)
    if cut >= 0:
        rec["definition"] = squash(arm[:cut]) or None
        coin_src = arm[cut + 1:]
    else:
        coin_src = arm
    # Numbered-sense entries ("1. … 2. …") carry sense markers into the
    # coinage region (and sometimes the definition — Սենատոր). Flag on the
    # whole Armenian region. Senses are delimited by comma OR a colon-class
    # terminator (':' '։'); split on both, then strip the leading "N." so
    # the coinage token is clean. Full structure stays in `raw`.
    if re.search(r"(?:^|[,:։])\s*\d+\.\s", " " + arm):
        rec["multi_sense"] = True
    coinages = []
    for c in re.split(r"[,:։]", coin_src):
        c = re.sub(r"^\s*\d+\.\s*", "", squash(c))   # drop leading "N. "
        if c:
            coinages.append(c)
    # Keep native_coinages pure-Armenian. A non-Armenian chunk here means a
    # ru/en got interleaved between numbered senses (p13 'Անтеннա':
    # "1. Ալեհավաք, принимающая антенна, 2. …") and the right-anchor split
    # couldn't reach it. Pull it out rather than fabricate a clean coinage;
    # flag for human review. raw is preserved for ground truth.
    clean, stray = [], []
    for c in coinages:
        if dominant_script(c) in ("armenian", "other"):
            clean.append(c)
        else:
            stray.append(c)
    rec["native_coinages"] = clean
    if stray:
        rec["stray"] = stray
        rec["warnings"].append("interleaved-field")

    # Class-2 reclassification: with no explicit def-mark, an entry may still
    # lead with a definitional PHRASE before its coinages, e.g. Հերմաֆրոդիտ
    # "Միաժ…ունեցող, Արուէգ, Որձևէգ". A ≥3-Armenian-word first coinage is a
    # definition, not a coinage — move it to `definition` (the reliable
    # field). If the phrase ends in a Capitalised word right after a
    # lowercase one (Բրենդ "…հատուկ Ապրանքանիշ"), recover that coinage.
    # Skip multi_sense: its sense structure must stay intact in `raw`.
    if rec["definition"] is None and not rec.get("multi_sense") and clean \
            and arm_word_count(clean[0]) >= 3:
        toks = clean[0].split()
        recovered = None
        if len(toks) >= 3 and toks[-1][:1].isupper() and toks[-2][:1].islower():
            recovered, toks = toks[-1], toks[:-1]
        rec["definition"] = squash(" ".join(toks))
        rec["native_coinages"] = ([recovered] if recovered else []) + clean[1:]
        rec["warnings"].append("definition-inferred")

    # Cosmetic: a grave accent surviving inside a definition is a secondary
    # comma in the source — render it as one.
    if rec["definition"] and "`" in rec["definition"]:
        rec["definition"] = squash(re.sub(r"\s*`\s*", ", ", rec["definition"]))
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--out", default=str(HERE / "out" / "entries.jsonl"))
    args = ap.parse_args()

    lines = load_body_lines()
    entries = group_entries(lines)
    parsed = [parse_entry(e["raw"], e["page"]) for e in entries]

    with open(args.out, "w", encoding="utf-8") as f:
        for r in parsed:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if args.stats:
        from collections import Counter
        n = len(parsed)
        warn = Counter()
        for r in parsed:
            for w in r["warnings"]:
                warn[w] += 1
        print(f"entries: {n}", file=sys.stderr)
        print(f"with russian: {sum(bool(r['ru']) for r in parsed)}", file=sys.stderr)
        print(f"with english: {sum(bool(r['en']) for r in parsed)}", file=sys.stderr)
        print(f"with definition: {sum(bool(r['definition']) for r in parsed)}", file=sys.stderr)
        print(f"with lang_origin: {sum(bool(r['lang_origin']) for r in parsed)}", file=sys.stderr)
        print(f"warnings: {dict(warn)}", file=sys.stderr)
    print(f"wrote {len(parsed)} entries → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
