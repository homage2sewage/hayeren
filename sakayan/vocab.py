#!/usr/bin/env python3
"""Pull a vocab table (the "III NEW WORDS AND EXPRESSIONS" pages) into
Anki-importable TSV.

Each vocab row in the source PDF has three visually-aligned columns:
Armenian (Barz-Italic, x≈71), transliteration (Armtrans, x≈196),
English (Times-Italic, x≈332). We anchor on each Armenian span and
collect transliteration / English spans by x-column and y-proximity.

Usage:
    .venv/bin/python vocab.py --pages 30 --tag "sakayan unit1"
"""

import argparse
import csv
import sys
from pathlib import Path

import fitz

import english_numbers
import fonts
import phonetics


HERE = Path(__file__).resolve().parent
DEFAULT_PDF = HERE / "dora_sahakyan.pdf"

# Sakayan uses two table layouts across the book:
#   single-column — Armenian | Translit | English  (units 1, 2, 4, 7, 8, 10, 11)
#   two-column   — left-half {Arm | Tr | Eng} side-by-side with right-half (units 3, 5, 6, 9)
# Plus the English column is sometimes ABOVE its row (Layout B, p52) instead of
# beside it (Layout A, p30). All x ranges below are empirical.
SINGLE_COLUMN = {
    "armenian": (40, 95),
    "translit": (170, 290),
    "english": (290, 600),
}
TWO_COLUMN = {
    "left":  {"armenian": (40, 80),   "translit": (95, 165),  "english": (165, 235)},
    "right": {"armenian": (235, 280), "translit": (290, 365), "english": (365, 460)},
}


def extract_spans(doc, page_num):
    spans = []
    for block in doc[page_num - 1].get_text("dict").get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for s in line.get("spans", []):
                spans.append({
                    "font": s["font"],
                    "x": s["bbox"][0],
                    "y": s["bbox"][1],
                    "text": fonts.remap(s["font"], s["text"]),
                })
    return spans


def _split_pairs(armenian: str, translit: str, english: str):
    """Sakayan sometimes packs verb infinitive + irregular conjugated form
    onto one row, e.g. `ունենալ, ունի` ↔ `to have, has`. When both the
    Armenian and English columns split into the same number of comma-
    separated parts, emit one card per pair so each form can be drilled
    independently. Otherwise pass through unchanged."""
    arm = [p.strip() for p in armenian.split(",")]
    eng = [p.strip() for p in english.split(",")]
    if len(arm) > 1 and len(arm) == len(eng):
        tr = [p.strip() for p in translit.split(",")]
        if len(tr) != len(arm):
            tr = [translit] * len(arm)
        return list(zip(arm, tr, eng))
    return [(armenian, translit, english)]


def collect_row(spans, anchor_y, x_lo, x_hi, dy_lo: float = -2, dy_hi: float = 5):
    """Pick spans on the anchor's visual line, in the given column.
    Sort by x only — y wobbles up to ~3 px between Barz / Armtrans / F26
    / Times baselines on the same line, so (y, x) sort interleaves F26
    diacritics wrong. dy bounds are relative to anchor_y."""
    items = [s for s in spans
             if x_lo <= s["x"] < x_hi
             and anchor_y + dy_lo <= s["y"] <= anchor_y + dy_hi]
    items.sort(key=lambda s: s["x"])
    return fonts.normalize("".join(s["text"] for s in items)).strip()


def detect_english_layout(anchors, english_spans) -> tuple[float, float]:
    """Decide whether the English column is laid out *below* its Armenian
    row (Layout A — pages 30, 96, …) or *above* (Layout B — page 52).
    Heuristic: compare the first Armenian's y with the first English's y."""
    if not anchors or not english_spans:
        return (-2, 5)
    first_arm = min(anchors, key=lambda s: s["y"])
    first_eng = min(english_spans, key=lambda s: s["y"])
    if first_eng["y"] < first_arm["y"] - 3:
        # English starts above first Armenian → "above" layout.
        return (-15, -2)
    return (-2, 8)


def _extract_one_column(spans, pn, cols, rows):
    """Pull rows from a single Armenian/translit/english column triple.
    `cols` is a dict with 'armenian'/'translit'/'english' (lo, hi) ranges."""
    anchors = sorted(
        [s for s in spans if s["font"] == "Barz-Italic"
         and cols["armenian"][0] <= s["x"] < cols["armenian"][1]],
        key=lambda s: s["y"],
    )
    english_spans = [s for s in spans if "Times-Italic" in s["font"]
                     and cols["english"][0] <= s["x"] < cols["english"][1]]
    eng_dy = detect_english_layout(anchors, english_spans)
    for anchor in anchors:
        armenian = fonts.normalize(anchor["text"]).strip()
        translit = collect_row(spans, anchor["y"], *cols["translit"]).strip("[]").strip()
        english = collect_row(spans, anchor["y"], *cols["english"],
                              dy_lo=eng_dy[0], dy_hi=eng_dy[1])
        if armenian and english:
            rows.append({
                "armenian": armenian,
                "translit": translit,
                "english": english,
                "page": pn,
            })


def extract_rows(pdf_path, pages):
    doc = fitz.open(pdf_path)
    rows = []
    for pn in pages:
        spans = extract_spans(doc, pn)
        # Two-column heuristic: a substantial cluster of Barz-Italic at
        # x≈246 means we're in a two-column vocab table.
        right_anchors = [s for s in spans if s["font"] == "Barz-Italic"
                         and TWO_COLUMN["right"]["armenian"][0] <= s["x"]
                                < TWO_COLUMN["right"]["armenian"][1]]
        if len(right_anchors) >= 4:
            _extract_one_column(spans, pn, TWO_COLUMN["left"], rows)
            _extract_one_column(spans, pn, TWO_COLUMN["right"], rows)
        else:
            _extract_one_column(spans, pn, SINGLE_COLUMN, rows)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--pages", required=True, type=str,
                    help='vocab page(s), e.g. "30" or "30,46"')
    ap.add_argument("--out", type=Path, default=HERE / "out" / "vocab.tsv")
    ap.add_argument("--tag", type=str, default="sakayan",
                    help='Anki tag(s), space-separated')
    args = ap.parse_args()

    pages: list[int] = []
    for part in args.pages.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))

    rows = extract_rows(args.pdf, pages)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        # No header row — Anki's default TSV import treats row 1 as data.
        for r in rows:
            for arm_part, tr_part, eng_part in _split_pairs(
                    r["armenian"], r["translit"], r["english"]):
                armenian = phonetics.annotate(arm_part, tr_part)
                english = english_numbers.normalize(eng_part)
                w.writerow([armenian, english, args.tag])
    print(f"Wrote {len(rows)} vocab rows → {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
