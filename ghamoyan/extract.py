#!/usr/bin/env python3
"""Extract Armenian text from Ghamoyan, Sargsyan & Kartashyan,
*Yerevan's Colloquial Language* (Yerevan, 2014, 118 pp).

The PDF stores Armenian text in standard ARMSCII-8 encoding mapped
onto WinAnsi codepoints — `armscii.decode` reverses the mismapping.
Modern Unicode fonts in the same PDF (Calibri, Identity-H Sylfaen)
pass through unchanged.

Output:

    out/full.jsonl  — per-span records: page, font, size, bbox, text_raw, text
    out/full.md     — flat reading-order render

Usage:
    .venv/bin/python extract.py
    .venv/bin/python extract.py --pages 11
    .venv/bin/python extract.py --pages 1-5,11
    .venv/bin/python extract.py --show-unmapped
"""

import argparse
import collections
import json
import sys
from pathlib import Path

import fitz

import armscii


HERE = Path(__file__).resolve().parent
DEFAULT_PDF = HERE / "erewani_khosaktsakan_lezown.pdf"
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
                for span in line.get("spans", []):
                    yield {
                        "page": pn,
                        "font": span["font"],
                        "size": round(span["size"], 2),
                        "bbox": [round(x, 2) for x in span["bbox"]],
                        "text_raw": span["text"],
                        "text": armscii.remap(span["font"], span["text"]),
                    }


def render_md(spans: list[dict]) -> str:
    """Group spans into pages and lines using bbox y, emit flat markdown."""
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
    """Report glyphs in ARMSCII-8 fonts that have no entry in the table."""
    PASS = set(" \t\n0123456789()[]{}.,;:!?-–—'\"/&%*#@^+=<>~`|\\_")
    counts: collections.Counter = collections.Counter()
    for s in spans:
        if s["font"] not in armscii.ENCODED_FONTS:
            continue
        for ch in s["text_raw"]:
            cp = ord(ch)
            if cp >= 0x80 and cp not in armscii.ARMSCII8 and ch not in PASS:
                counts[(s["font"], ch)] += 1
    print(f"Unmapped non-ASCII glyphs in ARMSCII-8 fonts: {len(counts)} distinct")
    for (font, ch), n in counts.most_common(40):
        print(f"  {n:7d}  {font:25s}  {ch!r}  U+{ord(ch):04X}")


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


if __name__ == "__main__":
    main()
