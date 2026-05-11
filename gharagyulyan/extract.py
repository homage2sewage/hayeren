#!/usr/bin/env python3
"""Extract text from Gharagyulyan's *Modern Armenian Orthoepy* PDF.

The PDF (from arar.sci.am) carries an embedded text layer — no OCR
needed. We emit JSONL with one entry per text-block, preserving
page index and bounding box. Schema mirrors parnasyan/tioyan:
  {page, bbox, text_raw, text, ocr_conf}

`ocr_conf: null` because there's no OCR involvement.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF = HERE / "gharagyulyan_orthoepy.pdf"
OUT = HERE / "out"


def main() -> int:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("requires PyMuPDF: pip install pymupdf", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    out_path = OUT / "full.jsonl"

    doc = fitz.open(PDF)
    n_pages = doc.page_count
    n_entries = 0

    with out_path.open("w", encoding="utf-8") as f:
        for i in range(n_pages):
            page = doc[i]
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
                        "page": i + 1,
                        "bbox": [round(x, 2) for x in bbox],
                        "text_raw": text,
                        "text": text,
                        "ocr_conf": None,
                    }
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    n_entries += 1

    print(f"Extracted {n_entries} text-block entries from {n_pages} "
          f"pages → {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
