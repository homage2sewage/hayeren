#!/usr/bin/env python3
"""OCR tioyan textbook → out/full.jsonl + out/full.md

Single-page scan, 393 pages. Pipeline:

    1. Render PDF page N to PNG via pdftoppm (cached).
    2. OCR with tesseract -l rus+hye, page-segmentation mode 4.
    3. Group words into lines via tesseract's block/par/line indices.
    4. Emit one JSONL record per line with bbox in image coords.

Differs from parnasyan/extract.py in that there is no double-page
split — each PDF page is one book page.

Usage:
    .venv/bin/python extract.py                 # all 393 pages
    .venv/bin/python extract.py --pages 50      # one page (probe)
    .venv/bin/python extract.py --pages 92-108  # one chapter
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
PDF = HERE / "tioyan.pdf"
OUT = HERE / "out"
CACHE = HERE / ".cache"
LANG = "rus+hye"
PSM = 4   # single column of variable text size


def render_page_to_png(page_num: int, dpi: int = 300) -> Path:
    dest = CACHE / f"page-{page_num:03d}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest
    with tempfile.TemporaryDirectory() as td:
        prefix = Path(td) / "p"
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi),
             "-f", str(page_num), "-l", str(page_num),
             str(PDF), str(prefix)],
            check=True,
        )
        candidates = list(Path(td).glob("p-*.png"))
        if not candidates:
            raise FileNotFoundError(f"pdftoppm produced no output for page {page_num}")
        shutil.copy(candidates[0], dest)
    return dest


def ocr_to_lines(img: Image.Image, page: int, lang: str = LANG) -> list[dict]:
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
            "page": page,
            "font": f"tess-{lang}",
            "size": 0,
            "bbox": [x0, y0, x1, y1],
            "text_raw": text,
            "text": text,
            "ocr_conf": round(sum(confs) / len(confs), 1) if confs else 0,
        })
    return out


def parse_pages(spec: str) -> list[int]:
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
    ap.add_argument("--pages", default="1-393")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--lang", default=LANG)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.out / "full.jsonl"
    md_path = args.out / "full.md"

    pages = parse_pages(args.pages)
    print(f"OCR'ing {len(pages)} page(s)", file=sys.stderr)

    with jsonl_path.open("w") as fjson, md_path.open("w") as fmd:
        for page in pages:
            png = render_page_to_png(page, dpi=args.dpi)
            img = Image.open(png)
            print(f"page {page}: OCR'ing...", file=sys.stderr)
            records = ocr_to_lines(img, page, lang=args.lang)
            for rec in records:
                fjson.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fmd.write(f"\n## p. {page}\n\n")
            for rec in records:
                fmd.write(rec["text"] + "\n")

    print(f"wrote {jsonl_path}", file=sys.stderr)
    print(f"wrote {md_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
