#!/usr/bin/env python3
"""Extract Armenian text from Sakayan, *Eastern Armenian for the
English-Speaking World* (2007 PDF).

Walks the PDF span-by-span, applies a font-aware glyph→Unicode remap
(see fonts.py), and emits two artefacts under out/:

    out/full[.<page-spec>].jsonl   — one record per text span
    out/full[.<page-spec>].md      — flat reading-order render

Usage:
    .venv/bin/python extract.py
    .venv/bin/python extract.py --pages 30
    .venv/bin/python extract.py --pages 30-45,80
    .venv/bin/python extract.py --show-unmapped
"""

import argparse
import collections
import json
import sys
from pathlib import Path

import fitz

import fonts


HERE = Path(__file__).resolve().parent
DEFAULT_PDF = HERE / "dora_sahakyan.pdf"
DEFAULT_OUT = HERE / "out"


def parse_pages(spec: str, total: int) -> list[int]:
    """Parse "30" / "30-45" / "1,5,7" / "30-45,80" → list of 1-indexed pages."""
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
        d = page.get_text("dict")
        for block in d.get("blocks", []):
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
                        "text": fonts.remap(span["font"], span["text"]),
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
            out.append(fonts.normalize("".join(line_buf)).rstrip())
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
    """Report glyphs in mapped fonts that have no entry in the mapping."""
    PASS = set(" \t\n0123456789()[]{}.,;:!?-–—'\"/&%*#@^+=<>~`|\\_")
    counts: collections.Counter = collections.Counter()
    for s in spans:
        m = fonts.FONT_MAPS.get(s["font"])
        if m is None:
            continue
        for ch in s["text_raw"]:
            if ch not in m:
                counts[(s["font"], ch)] += 1
    print(f"Unmapped glyphs in mapped fonts: {len(counts)} distinct")
    for (font, ch), n in counts.most_common(50):
        marker = "" if ch in PASS else "  ← unexpected"
        print(f"  {n:7d}  {font:20s}  {ch!r}  U+{ord(ch):04X}{marker}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--pages", type=str, default="",
                    help='page spec like "30", "30-45", "1,5,7"')
    ap.add_argument("--show-unmapped", action="store_true",
                    help="report unmapped glyphs and exit")
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
