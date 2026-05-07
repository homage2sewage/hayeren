#!/usr/bin/env python3
"""Quality probe: OCR a single image-page and print the result.

Run after installing tesseract + rus + hye language packs to verify
output quality before committing to the full extract.

Usage:
    .venv/bin/python probe.py                 # default image-page 50
    .venv/bin/python probe.py --page 1
"""

import argparse
import sys
from pathlib import Path

from PIL import Image
import pytesseract

import extract


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--page", type=int, default=50,
                    help="image-page number to probe")
    ap.add_argument("--lang", default=extract.LANG)
    ap.add_argument("--show-conf", action="store_true",
                    help="show per-line OCR confidence")
    args = ap.parse_args()

    print(f"=== Probing parnasyan image-page {args.page} (lang={args.lang}) ===",
          file=sys.stderr)
    png = extract.render_page_to_png(args.page)
    img = Image.open(png)
    left, right = extract.split_double_page(img)

    for half_name, half in [("LEFT", left), ("RIGHT", right)]:
        book_page = (args.page - 1) * 2 + 1 + (0 if half_name == "LEFT" else 1)
        print(f"\n--- {half_name} (book page {book_page}) ---")
        records = extract.ocr_to_lines(half, book_page, lang=args.lang)
        for rec in records:
            conf = f"  [{rec['ocr_conf']}]" if args.show_conf else ""
            print(f"{rec['text']}{conf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
