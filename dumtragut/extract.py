#!/usr/bin/env python3
"""Extract Armenian + interlinear text from Dum-Tragut, *Armenian:
Modern Eastern Armenian* (John Benjamins, 2009, 760 pp).

The PDF has a clean text layer; only the Armenian script (font
ArialLatArm) is stored at legacy WinAnsi codepoints and needs the
`armscii.remap` glyph→Unicode fix. MinionPro Latin (English prose,
transliteration, glosses) passes through unchanged.

Output (mirrors sakayan/ghamoyan):

    out/full[.<page-spec>].jsonl   — one record per text span
    out/full[.<page-spec>].md      — flat reading-order render

Run with a pymupdf-capable interpreter, e.g. the ghamoyan venv:

    ../ghamoyan/.venv/bin/python extract.py --pages 80
    ../ghamoyan/.venv/bin/python extract.py --pages 70-100
    ../ghamoyan/.venv/bin/python extract.py                 # all 760 pages
    ../ghamoyan/.venv/bin/python extract.py --show-unmapped
"""

import argparse
import collections
import json
import sys
from pathlib import Path

import fitz

import armscii
import phonetic


HERE = Path(__file__).resolve().parent
DEFAULT_PDF = HERE / "modern-eastern-armenian.pdf"
DEFAULT_OUT = HERE / "out"


def parse_pages(spec: str, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return sorted(p for p in pages if 1 <= p <= total)


def iter_spans(doc: fitz.Document, pages: list[int]):
    for pn in pages:
        page = doc[pn - 1]
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                # Decode each span (Armenian / IPA glyphs + per-span breve).
                decoded = [
                    phonetic.fix_diacritics(
                        phonetic.remap(
                            s["font"], armscii.remap(s["font"], s["text"])
                        )
                    )
                    for s in spans
                ]
                # Aspiration (h→ʰ) needs cross-span context within the line,
                # so fix the joined line and slice it back onto spans
                # (length-preserving, 1 codepoint per substitution).
                fixed = phonetic.fix_aspiration("".join(decoded))
                pos = 0
                for s, d in zip(spans, decoded):
                    seg = fixed[pos:pos + len(d)]
                    pos += len(d)
                    yield {
                        "page": pn,
                        "font": s["font"],
                        "size": round(s["size"], 2),
                        "bbox": [round(x, 2) for x in s["bbox"]],
                        "text_raw": s["text"],
                        "text": seg,
                    }


def render_md(spans: list[dict]) -> str:
    """Group spans into pages and lines using bbox y, emit flat markdown.

    Spans within ~2pt of vertical agreement are one visual line — this
    keeps an Armenian span and the italic transliteration that follows
    it on the same line, while the interlinear gloss line below stays
    separate."""
    out: list[str] = []
    cur_page: int | None = None
    line_buf: list[str] = []
    last_y: float | None = None

    def flush_line() -> None:
        nonlocal line_buf
        if line_buf:
            out.append("".join(line_buf).rstrip())
            line_buf = []

    for s in spans:
        if s["page"] != cur_page:
            flush_line()
            if cur_page is not None:
                out.append("")
            out.append(f"## p. {s['page']}")
            out.append("")
            cur_page = s["page"]
            last_y = None
        y = s["bbox"][1]
        if last_y is None or abs(y - last_y) > 2:
            flush_line()
            last_y = y
        line_buf.append(s["text"])
    flush_line()
    return "\n".join(out) + "\n"


def show_unmapped(spans: list[dict]) -> None:
    """Report raw codepoints in ArialLatArm with no DECODE entry."""
    PASS = {chr(c) for c in (
        0x2013, 0x2014, 0x2012, 0x2026,          # dashes, ellipsis
        0x201C, 0x201D, 0x2018, 0x2019,          # smart quotes
        0x2002, 0x2003, 0x2009, 0x00A0,          # en/em/thin/nbsp
        0x02C9, 0x00A7,                          # macron, section sign
    )}
    counts: collections.Counter = collections.Counter()
    for s in spans:
        if s["font"] not in armscii.ENCODED_FONTS:
            continue
        for ch in s["text_raw"]:
            if ord(ch) not in armscii.DECODE and ch not in PASS:
                counts[ch] += 1
    print(f"Unmapped non-pass glyphs in encoded fonts: {len(counts)} distinct")
    for ch, n in counts.most_common(40):
        print(f"  {n:7d}  {ch!r}  U+{ord(ch):04X}")


def self_check(spans: list[dict]) -> bool:
    """Post-decode sanity checks. Returns True iff all pass.

    1. Census of raw ≥0x80 codepoints in ArialLatArm the table does not
       cover (passed through undecoded → likely a missing slot).
    2. Live counts for the TENTATIVE punctuation slots, so a fresh page
       can disconfirm a single-bitmap guess.
    """
    ok = True

    # Real Unicode that legitimately rides inside ArialLatArm spans
    # (dashes, ellipsis, smart quotes, em/en/thin spaces, length macron,
    # section sign) — present in the text layer as proper Unicode, needs
    # no decoding. Anything outside this set that stays undecoded is a
    # candidate missing slot and fails the check.
    PASS = set("–—‒…“”‘’"
               "     ˉ§")
    undecoded: collections.Counter = collections.Counter()
    for s in spans:
        if s["font"] not in armscii.ENCODED_FONTS:
            continue
        for ch in s["text_raw"]:
            cp = ord(ch)
            if cp >= 0x80 and cp not in armscii.DECODE and ch not in PASS:
                undecoded[ch] += 1
    if undecoded:
        print(f"self-check: {len(undecoded)} distinct undecoded ≥0x80 "
              f"codepoints in ArialLatArm (candidate missing slots):",
              file=sys.stderr)
        for ch, n in undecoded.most_common():
            print(f"  {n:7d}  {ch!r}  U+{ord(ch):04X}", file=sys.stderr)
        ok = False
    else:
        print("self-check: no unexpected undecoded ≥0x80 codepoints in "
              "ArialLatArm", file=sys.stderr)

    for cp, glyph in armscii.TENTATIVE.items():
        n = sum(s["text_raw"].count(chr(cp)) for s in spans
                if s["font"] in armscii.ENCODED_FONTS)
        print(f"self-check: TENTATIVE 0x{cp:02X} -> {glyph!r}  ×{n}",
              file=sys.stderr)

    # Phonetic (IPA) fonts: any glyph the table doesn't cover, plus live
    # counts for the low-confidence prosody glyphs.
    phon_undecoded: collections.Counter = collections.Counter()
    for s in spans:
        if s["font"] not in phonetic.PHONETIC_FONTS:
            continue
        for ch in s["text_raw"]:
            if ch not in phonetic.DECODE and ch not in " j æ>":
                phon_undecoded[ch] += 1
    if phon_undecoded:
        print(f"self-check: {len(phon_undecoded)} undecoded glyphs in "
              f"phonetic fonts:", file=sys.stderr)
        for ch, n in phon_undecoded.most_common():
            print(f"  {n:7d}  {ch!r}  U+{ord(ch):04X}", file=sys.stderr)
        ok = False
    else:
        print("self-check: no undecoded glyphs in phonetic fonts",
              file=sys.stderr)
    for glyph, ipa in phonetic.TENTATIVE.items():
        n = sum(s["text_raw"].count(glyph) for s in spans
                if s["font"] in phonetic.PHONETIC_FONTS)
        print(f"self-check: TENTATIVE phon {glyph!r} -> {ipa!r}  ×{n}",
              file=sys.stderr)

    # No Private-Use-Area glyphs should survive into the decoded text
    # (Expert figures must have been mapped to digits).
    pua = collections.Counter(
        ch for s in spans for ch in s["text"] if 0xE000 <= ord(ch) <= 0xF8FF
    )
    if pua:
        print(f"self-check: {len(pua)} distinct PUA codepoints survived "
              f"into decoded text:", file=sys.stderr)
        for ch, n in pua.most_common(20):
            print(f"  {n:7d}  U+{ord(ch):04X}", file=sys.stderr)
        ok = False
    else:
        print("self-check: no PUA codepoints in decoded text", file=sys.stderr)
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--pages", type=str, default="")
    ap.add_argument("--show-unmapped", action="store_true")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    pages = parse_pages(args.pages, doc.page_count)
    print(f"Processing {len(pages)} of {doc.page_count} pages from {args.pdf.name}",
          file=sys.stderr)

    spans = list(iter_spans(doc, pages))

    if args.show_unmapped:
        show_unmapped(spans)
        return

    args.out.mkdir(parents=True, exist_ok=True)
    suffix = "" if not args.pages else f".{args.pages.replace(',', '_').replace('-', 'to')}"
    jsonl_path = args.out / f"full{suffix}.jsonl"
    md_path = args.out / f"full{suffix}.md"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for s in spans:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    md_path.write_text(render_md(spans), encoding="utf-8")
    print(f"Wrote {len(spans)} spans → {jsonl_path}", file=sys.stderr)
    print(f"Wrote markdown → {md_path}", file=sys.stderr)
    if not self_check(spans):
        sys.exit(1)


if __name__ == "__main__":
    main()
