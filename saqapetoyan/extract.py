#!/usr/bin/env python3
"""Extract text from Sakapetoyan's *Բառգրքույկ. Նոր և նորակազմ բառեր
հայերենում* (A Wordbook: New and Newly-coined Words in Armenian).

The PDF carries a clean embedded Unicode-Armenian text layer — no OCR
and no ARMSCII-8 decoding needed (contrast ghamoyan). We emit JSONL
with one entry per text-line, preserving page index and bounding box.
Schema mirrors gharagyulyan/parnasyan/tioyan:
  {page, bbox, text_raw, text, ocr_conf}

`ocr_conf: null` because there's no OCR involvement.

Also emits a flat reading-order Markdown render (out/full.md) for
eyeballing, matching the ghamoyan convention.

Usage:
    .venv/bin/python extract.py            # → out/full.jsonl + full.md
    .venv/bin/python extract.py --pages 9
    .venv/bin/python extract.py --pages 9-12
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF = HERE / "saqapetoyan_neologisms.pdf"
OUT = HERE / "out"


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="", help="e.g. 9 or 9-12 or 9,11,13")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("requires PyMuPDF: pip install pymupdf", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    pages = parse_pages(args.pages, doc.page_count)

    jsonl_path = OUT / "full.jsonl"
    md_path = OUT / "full.md"
    n_entries = 0

    with jsonl_path.open("w", encoding="utf-8") as jf, \
            md_path.open("w", encoding="utf-8") as mf:
        for pn in pages:
            page = doc[pn - 1]
            mf.write(f"\n\n## p. {pn}\n\n")
            blocks = page.get_text("dict")["blocks"]
            for blk in blocks:
                if blk.get("type", 0) != 0:
                    continue  # skip image blocks
                for line in blk.get("lines", []):
                    spans = line.get("spans", [])
                    if not spans:
                        continue
                    text = "".join(s.get("text", "") for s in spans)
                    if not text.strip():
                        continue
                    bbox = line.get("bbox", [0, 0, 0, 0])
                    entry = {
                        "page": pn,
                        "bbox": [round(x, 2) for x in bbox],
                        "text_raw": text,
                        "text": text,
                        "ocr_conf": None,
                    }
                    jf.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    mf.write(text + "\n")
                    n_entries += 1

    print(f"Extracted {n_entries} line entries from {len(pages)} "
          f"pages → {jsonl_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
