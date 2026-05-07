#!/usr/bin/env python3
"""OCR parnasyan textbook → out/full.jsonl + out/full.md

The PDF is a 215-image double-page-spread scan: each image-page covers
two book pages side-by-side. The pipeline:

    1. Render image-page N to PNG via pdftoppm (cached at .cache/).
    2. Split the wide image into left + right halves.
    3. OCR each half with tesseract -l rus+hye, page-segmentation mode 4
       (single column of variable text size).
    4. Group words into lines using tesseract's block/paragraph/line
       indices. Emit one JSONL record per line with a bbox in image
       coordinates.
    5. Book-page numbering: image-page N → book pages 2N-1 (left) and
       2N (right).

Usage:
    .venv/bin/python extract.py                 # all 215 image-pages
    .venv/bin/python extract.py --pages 50      # one image-page (a probe)
    .venv/bin/python extract.py --pages 1-10    # range
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
import pytesseract

HERE = Path(__file__).resolve().parent
PDF = HERE / "parnasyan.pdf"
OUT = HERE / "out"
CACHE = HERE / ".cache"
LANG = "rus+hye"
PSM = 4   # single column of variable text size — fits a textbook page


def render_page_to_png(image_page_num: int, dpi: int = 300) -> Path:
    """Render PDF image-page #N (1-based) to a PNG, cached under .cache/."""
    dest = CACHE / f"page-{image_page_num:03d}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest
    with tempfile.TemporaryDirectory() as td:
        prefix = Path(td) / "p"
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi),
             "-f", str(image_page_num), "-l", str(image_page_num),
             str(PDF), str(prefix)],
            check=True,
        )
        candidates = list(Path(td).glob("p-*.png"))
        if not candidates:
            raise FileNotFoundError(f"pdftoppm produced no output for page {image_page_num}")
        shutil.copy(candidates[0], dest)
    return dest


def split_double_page(img: Image.Image) -> tuple[Image.Image, Image.Image]:
    """Split a wide double-page-spread image at the centerline."""
    w, h = img.size
    return img.crop((0, 0, w // 2, h)), img.crop((w // 2, 0, w, h))


def ocr_to_lines(img: Image.Image, book_page: int, lang: str = LANG) -> list[dict]:
    """Run tesseract; group words into lines; return JSONL records.

    Each record matches the schema used by sakayan/ghamoyan extractions
    (page, font, size, bbox, text_raw, text) plus an `ocr_conf` field.
    """
    data = pytesseract.image_to_data(
        img, lang=lang, output_type=pytesseract.Output.DICT,
        config=f"--psm {PSM}",
    )

    lines: dict = {}
    n = len(data["text"])
    for i in range(n):
        if not data["text"][i].strip():
            continue
        key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
        lines.setdefault(key, []).append(i)

    out = []
    for idxs in lines.values():
        text = " ".join(data["text"][i] for i in idxs)
        confs = [int(data["conf"][i]) for i in idxs
                 if int(data["conf"][i]) >= 0]
        x0 = min(data["left"][i] for i in idxs)
        y0 = min(data["top"][i] for i in idxs)
        x1 = max(data["left"][i] + data["width"][i] for i in idxs)
        y1 = max(data["top"][i] + data["height"][i] for i in idxs)
        out.append({
            "page": book_page,
            "font": f"tess-{lang}",
            "size": 0,
            "bbox": [x0, y0, x1, y1],
            "text_raw": text,
            "text": text,
            "ocr_conf": round(sum(confs) / len(confs), 1) if confs else 0,
        })
    return out


def parse_pages(spec: str) -> list[int]:
    """Parse '1,3,5-7' style page specs into a list of ints."""
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(chunk))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--pages", default="1-215",
                    help="image-page range (default: all)")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--lang", default=LANG)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.out / "full.jsonl"
    md_path = args.out / "full.md"

    image_pages = parse_pages(args.pages)
    print(f"OCR'ing {len(image_pages)} image-page(s) → {len(image_pages)*2} book pages",
          file=sys.stderr)

    with jsonl_path.open("w") as fjson, md_path.open("w") as fmd:
        for image_page in image_pages:
            png = render_page_to_png(image_page, dpi=args.dpi)
            img = Image.open(png)
            left, right = split_double_page(img)
            for half_idx, half in enumerate([left, right]):
                book_page = (image_page - 1) * 2 + 1 + half_idx
                print(f"image-page {image_page} -> book page {book_page}: OCR'ing...",
                      file=sys.stderr)
                records = ocr_to_lines(half, book_page, lang=args.lang)
                for rec in records:
                    fjson.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fmd.write(f"\n## p. {book_page}\n\n")
                for rec in records:
                    fmd.write(rec["text"] + "\n")

    print(f"wrote {jsonl_path}", file=sys.stderr)
    print(f"wrote {md_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
