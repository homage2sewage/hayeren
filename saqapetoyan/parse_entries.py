#!/usr/bin/env python3
"""Parse the saqapetoyan neologism glossary (body pp. 9-76) into one
structured record per dictionary entry.

Entry shape in the book:

    HEADWORD – POS[.(domain.)] [definition] COINAGE[, COINAGE2 …], <ru>, <en>.

The DEFINITION vs COINAGE distinction is carried by FONT WEIGHT, not by
any delimiter: the author prints coinages in **bold** and the explanatory
definition in regular weight. The bold is *faux* (drawn as a fill + a
stroke overprint, so each bold glyph appears twice in the content stream)
and is invisible to `get_text()` / span `flags` — every span reports
`Sylfaen flags=4`. We recover it from `page.get_texttrace()`: a glyph is
bold iff a stroke-render copy (`type != 0`) exists at its position. See
`research`/README for why the earlier `՝`-delimiter heuristic was wrong
(it disagreed with the visible bold on ~28 entries — the page-parallel
reader audit, 2026-06-14).

Parsing strategy
----------------
1. `extract_bold_lines` — per body line, the clean (deduplicated) text
   PLUS an aligned bold mask ('B'/'.').
2. Group lines into entries; de-hyphenate text and mask in lockstep.
3. Split the headword off on the dash separator; parse POS/domain/lang.
4. Right of the last Armenian letter is `[ru][en]` (regular Cyrillic then
   Latin) — split by script.
5. The Armenian region left of it is segmented by the bold mask:
   **bold runs → native_coinages, regular runs → definition.** Spaces
   inside a bold phrase are bold (so multi-word coinages stay intact);
   the comma before `ru` is regular.

IMPORTANT editorial note (per user direction): a native COINAGE is the
book's *proposed* Armenian replacement — its existence here does **not**
mean it is actually used (e.g. մսադոնդող for Russian холодец/holodets
returns ~nothing on the open web). Treat `native_coinages` as
prescriptive suggestions, `definition` as the reliable meaning signal,
and the `ru`/headword pair as the colloquial-usage signal.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF = HERE / "saqapetoyan_neologisms.pdf"

BODY_START, BODY_END = 9, 76  # Ա … Ֆ glossary body

ARM_UPPER = "Ա-Ֆ"
ARM_LOWER = "ա-ֆև"
ARM_LETTER_RE = re.compile(rf"[{ARM_UPPER}{ARM_LOWER}]")
CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]")
LATIN_RE = re.compile(r"[A-Za-z]")

# Headword separator: a dash with at least one ADJACENT space — distinguishes
# the field separator (' – ', ' –', '- ') from an intra-headword hyphen in a
# compound loanword (Ուիք-էնդ, Աուդիո–վիդեո, no flanking spaces).
SEP_RE = re.compile(r"\s+[–-]\s*|[–-]\s+")
HEADWORD_RE = re.compile(
    rf"^[{ARM_UPPER}{ARM_LOWER}][{ARM_UPPER}{ARM_LOWER}0-9()\s]{{0,25}}?"
    rf"\s*[–-]\s*(?=[{ARM_UPPER}{ARM_LOWER}0-9(])"
)
# Leading POS/domain tag block after the dash: runs of `abbr.` tokens and
# parenthetical groups, e.g. "գ.", "ած.գ.", "գ.(ախտ.)". A parenthetical
# counts as a tag group ONLY if it contains nothing but abbreviations — so
# an etymological NOTE like "(արաբ. միս խմորի մեջ)" (Լահմաջուն) is NOT eaten
# as domain tags; it stays in the body and lands in the definition.
TAG_BLOCK_RE = re.compile(
    rf"^((?:[{ARM_UPPER}{ARM_LOWER}]+\.|\((?:[{ARM_UPPER}{ARM_LOWER}]+\.\s*)+\))[\s]*)+"
)
PAREN_RE = re.compile(r"\(([^)]*)\)")
LANG_TAGS = {"արաբ.", "գերմ.", "ֆր.", "Արաբ.", "Գերմ.", "Ֆր.", "լատ."}


def squash(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip()


def dominant_script(s: str) -> str:
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


def strip_both(t: str, m: str) -> tuple[str, str]:
    a, b = 0, len(t)
    while a < b and t[a].isspace():
        a += 1
    while b > a and t[b - 1].isspace():
        b -= 1
    return t[a:b], m[a:b]


# ── extraction: clean text + aligned bold mask ───────────────────────────

def extract_bold_lines(pages: list[int]) -> list[tuple[int, str, str]]:
    import fitz
    doc = fitz.open(PDF)
    out: list[tuple[int, str, str]] = []
    for pn in pages:
        glyphs = []  # (oy, ox, char, is_stroke)
        for span in doc[pn - 1].get_texttrace():
            stroke = span.get("type") != 0  # mode 0 = fill (regular); else bold
            for c in span.get("chars", []):
                ox, oy = c[2]
                glyphs.append((oy, ox, chr(c[0]), stroke))
        glyphs.sort(key=lambda g: (g[0], g[1]))
        # cluster into visual lines by baseline y
        lines: list[list] = []
        cur: list = []
        cy = None
        for oy, ox, ch, st in glyphs:
            if cy is not None and abs(oy - cy) > 3:
                lines.append(cur)
                cur = []
            cur.append((ox, ch, st))
            cy = oy
        if cur:
            lines.append(cur)
        for row in lines:
            row.sort()
            merged: list[list] = []  # [ox, char, bold]
            for ox, ch, st in row:
                # faux-bold draws each glyph twice at ~the same origin → merge
                if merged and abs(ox - merged[-1][0]) < 1.2 and merged[-1][1] == ch:
                    merged[-1][2] = merged[-1][2] or st
                else:
                    merged.append([ox, ch, st])
            text = "".join(c for _, c, _ in merged)
            mask = "".join("B" if b else "." for _, _, b in merged)
            out.append((pn, text, mask))
    return out


def load_body_lines() -> list[dict]:
    lines = []
    for pn, text, mask in extract_bold_lines(list(range(BODY_START, BODY_END + 1))):
        s = text.strip()
        if not s or re.fullmatch(r"[\d\s]+", s):
            continue  # blank / page number (renders with spaced digits, e.g. "2 8")
        if len(s) <= 2 and re.fullmatch(rf"[{ARM_UPPER}]Ւ?", s):
            continue  # single-letter section header (incl. ՈՒ)
        lines.append({"page": pn, "text": text, "mask": mask})
    return lines


def group_entries(lines: list[dict]) -> list[dict]:
    entries: list[dict] = []
    cur: list[dict] = []
    cur_page = None

    def flush():
        if not cur:
            return
        bt, bm = strip_both(cur[0]["text"], cur[0]["mask"])
        for ln in cur[1:]:
            nt, nm = strip_both(ln["text"], ln["mask"])
            if bt.endswith("-") or bt.endswith("‐"):
                bt, bm = bt[:-1] + nt, bm[:-1] + nm        # de-hyphenate
            else:
                bt, bm = bt + " " + nt, bm + "." + nm       # join (space=regular)
        entries.append({"page": cur_page, "text": bt, "mask": bm})

    for ln in lines:
        if HEADWORD_RE.match(ln["text"].strip()):
            flush()
            cur = [ln]
            cur_page = ln["page"]
        elif cur:
            cur.append(ln)
    flush()
    return entries


# ── per-entry parse ──────────────────────────────────────────────────────

def _bold_runs(text: str, mask: str):
    """Yield (segment_text, is_bold) for maximal same-weight runs."""
    if not text:
        return
    start = 0
    for i in range(1, len(text) + 1):
        if i == len(text) or mask[i] != mask[start]:
            yield text[start:i], mask[start] == "B"
            start = i


def parse_entry(text: str, mask: str, page: int) -> dict:
    rec: dict = {
        "page": page, "headword": None, "homograph": None, "pos": None,
        "domain": [], "lang_origin": [], "definition": None,
        "native_coinages": [], "ru": None, "en": None, "multi_sense": False,
        "stray": [], "raw": squash(text), "warnings": [],
    }

    m = SEP_RE.search(text)
    if not m:
        rec["warnings"].append("no-headword-sep")
        return rec
    headword = text[:m.start()].strip()
    hm = re.match(r"^(.*?)(\d+)$", headword)
    if hm:
        headword, rec["homograph"] = hm.group(1), int(hm.group(2))
    rec["headword"] = squash(headword)

    rest_t, rest_m = strip_both(text[m.end():], mask[m.end():])
    # POS-terminator typo: a short leading abbrev closed by ',' not '.' (p31).
    # Same length → mask stays aligned.
    rest_t = re.sub(rf"^([{ARM_UPPER}{ARM_LOWER}]{{1,3}}),(\s)", r"\1.\2", rest_t)

    tm = TAG_BLOCK_RE.match(rest_t)
    if tm:
        tag_block = tm.group(0)
        rest_t, rest_m = strip_both(rest_t[tm.end():], rest_m[tm.end():])
        rec["pos"] = PAREN_RE.sub("", tag_block).strip() or None
        for p in PAREN_RE.findall(tag_block):
            for tok in re.split(r"[,\s]+", p.strip()):
                if not tok:
                    continue
                (rec["lang_origin"] if tok in LANG_TAGS else rec["domain"]).append(tok)
    else:
        rec["warnings"].append("no-pos-tag")

    # [Armenian def+coinage] | [ru][en]: everything right of the last Armenian
    # letter is the regular Cyrillic-then-Latin tail.
    arm_idx = [i for i, ch in enumerate(rest_t) if ARM_LETTER_RE.match(ch)]
    if arm_idx:
        cut = arm_idx[-1] + 1
        arm_t, arm_m, tail = rest_t[:cut], rest_m[:cut], rest_t[cut:]
    else:
        arm_t, arm_m, tail = "", "", rest_t

    # ru / en from the tail
    en_chunks, ru_chunks = [], []
    for p in re.split(r"[,]", tail):
        p = p.strip(" .,:;՝`–-")
        if not p:
            continue
        ds = dominant_script(p)
        if ds == "latin":
            en_chunks.append(re.sub(r"^\d+\.\s*", "", p))
        elif ds == "cyrillic":
            ru_chunks.append(re.sub(r"^\d+\.\s*", "", p))
    rec["en"] = ", ".join(en_chunks) or None
    rec["ru"] = ", ".join(ru_chunks) or None

    # definition (regular) vs coinages (bold) from the Armenian region
    defrag, coin = [], []
    for seg, is_bold in _bold_runs(arm_t, arm_m):
        if is_bold:
            for tok in re.split(r"[,:՝`]", seg):       # coinage separators
                tok = squash(re.sub(r"^\d+\.\s*", "", tok.strip(" .՝`:")))
                if not tok:
                    continue
                if ARM_LETTER_RE.search(tok):
                    coin.append(tok)
                elif re.search(r"[A-Za-zЀ-ӿ]", tok):
                    rec["stray"].append(tok)            # bold non-Armenian (rare)
                # else: letterless (a stray sense number) → drop
        else:
            s = seg.strip(" ,:;՝`")
            if not s:
                continue
            ds = dominant_script(s)
            if ds in ("armenian", "other"):
                defrag.append(s)
            else:                                        # interleaved per-sense ru/en
                rec["stray"].append(s)
    definition = squash(re.sub(r"\s{2,}", " ", " ".join(defrag)))
    definition = definition.replace("`", ",")          # grave = secondary comma
    definition = re.sub(r"[\s,]*\b\d+\.?\s*$", "", definition).strip(" ,")
    if re.fullmatch(r"\d+\.?", definition) or re.fullmatch(r"\([^)]*\)", definition):
        definition = ""                                # lone sense number / leftover tag-paren
    # Source inconsistency: the typesetter occasionally forgets to bold a
    # lone coinage (Կուլտուրա→Մշակույթ, Կապիտալիստ→Դրամատեր — verified
    # un-bolded against the page while the neighbouring entry IS bold). If no
    # bold coinage was found but the whole regular gloss is a short Armenian
    # phrase (≤2 words, no sense number), it IS the coinage, not a definition.
    if not coin and definition and not re.search(r"\d", definition) \
            and len([w for w in definition.split() if ARM_LETTER_RE.search(w)]) <= 2 \
            and dominant_script(definition) == "armenian":
        coin = [definition]
        definition = None
        rec["warnings"].append("coinage-unbolded")

    rec["native_coinages"] = coin
    rec["definition"] = definition or None

    if re.search(r"\d+\.", arm_t):
        rec["multi_sense"] = True
    if not coin:
        rec["warnings"].append("no-coinage")
    if not rec["ru"]:
        rec["warnings"].append("no-russian")
    if not en_chunks:
        rec["warnings"].append("no-english")
    if rec["stray"]:
        rec["warnings"].append("interleaved-field")
    if not rec["stray"]:
        del rec["stray"]
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--out", default=str(HERE / "out" / "entries.jsonl"))
    args = ap.parse_args()

    entries = group_entries(load_body_lines())
    parsed = [parse_entry(e["text"], e["mask"], e["page"]) for e in entries]

    with open(args.out, "w", encoding="utf-8") as f:
        for r in parsed:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if args.stats:
        from collections import Counter
        n = len(parsed)
        warn = Counter(w for r in parsed for w in r["warnings"])
        print(f"entries: {n}", file=sys.stderr)
        print(f"  with russian: {sum(bool(r['ru']) for r in parsed)}", file=sys.stderr)
        print(f"  with english: {sum(bool(r['en']) for r in parsed)}", file=sys.stderr)
        print(f"  with definition: {sum(bool(r['definition']) for r in parsed)}", file=sys.stderr)
        print(f"  with coinage: {sum(bool(r['native_coinages']) for r in parsed)}", file=sys.stderr)
        print(f"  multi_sense: {sum(r['multi_sense'] for r in parsed)}", file=sys.stderr)
        print(f"  warnings: {dict(warn)}", file=sys.stderr)
    print(f"wrote {len(parsed)} entries → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
