#!/usr/bin/env python3
"""Pull a dialogue out of the Sakayan PDF into Anki-importable TSV.

Dialogue page layout (sample: p27, dialogue 1):

    [x=43, Times-Roman]  speaker label, e.g. "A."
    [x=70, Barz-Italic]  Armenian utterance
    [x=261, Times-*]     English translation
    [x=70, Armtrans+]    transliteration on the next visual line

Each anchor (Barz-Italic Armenian span at x≈70) gets paired with the
speaker, English translation, and transliteration.

Dialogue boundaries are given by the user as a (page, y) start and end
since the section markers ("1.", "2.", "II  TEXT") sit at consistent
positions in Times-Bold at x=43 — easy to bookmark by page.

Usage:
    .venv/bin/python dialogues.py \\
        --start 27:92 --end 28:455 \\
        --tag "sakayan unit1 dialogue1" \\
        --out out/unit1_dialogue1.tsv
"""

import argparse
import csv
import re
import sys
from pathlib import Path

import fitz

import english_numbers
import fonts
import phonetics


HERE = Path(__file__).resolve().parent
DEFAULT_PDF = HERE / "dora_sahakyan.pdf"


def parse_pos(s: str) -> tuple[int, float]:
    page, y = s.split(":")
    return int(page), float(y)


def in_range(page: int, y: float,
             start: tuple[int, float], end: tuple[int, float]) -> bool:
    if page < start[0] or page > end[0]:
        return False
    if page == start[0] and y < start[1]:
        return False
    if page == end[0] and y >= end[1]:
        return False
    return True


def extract_spans(doc, page_num):
    spans = []
    for block in doc[page_num - 1].get_text("dict").get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for s in line.get("spans", []):
                spans.append({
                    "page": page_num,
                    "font": s["font"],
                    "x": s["bbox"][0],
                    "y": s["bbox"][1],
                    "text": fonts.remap(s["font"], s["text"]),
                })
    return spans


def collect_row(spans, anchor, x_lo, x_hi, dy_lo=-3, dy_hi=8):
    items = [s for s in spans
             if s["page"] == anchor["page"]
             and x_lo <= s["x"] < x_hi
             and anchor["y"] + dy_lo <= s["y"] <= anchor["y"] + dy_hi]
    items.sort(key=lambda s: s["x"])
    return fonts.normalize("".join(s["text"] for s in items)).strip()


def extract_dialogue(pdf_path, start, end):
    doc = fitz.open(pdf_path)
    rows = []
    for pn in range(start[0], end[0] + 1):
        spans = extract_spans(doc, pn)
        anchors = [s for s in spans
                   if s["font"] == "Barz-Italic"
                   and 50 <= s["x"] < 90
                   and in_range(s["page"], s["y"], start, end)]
        anchors.sort(key=lambda s: s["y"])
        for anchor in anchors:
            armenian = fonts.normalize(anchor["text"]).strip()
            if not armenian:
                continue
            # Speaker labels and English translation can sit *above* (-11)
            # or below (+5) the Armenian line depending on the unit. Use a
            # wide y-window in both directions; consecutive exchanges are
            # ≥30 px apart, so no risk of double-matching.
            raw_speaker = collect_row(spans, anchor, x_lo=30, x_hi=58,
                                      dy_lo=-15, dy_hi=10)
            # Speakers are single capital letters (A, B, C, …) but stray
            # punctuation/whitespace can leak in. Keep only the leading caps.
            m = re.match(r"^([A-Z]+)", raw_speaker)
            speaker = m.group(1) if m else ""
            english = collect_row(spans, anchor, x_lo=230, x_hi=600,
                                  dy_lo=-15, dy_hi=10)
            # Transliteration sits below the Armenian on both layouts.
            translit = collect_row(spans, anchor, x_lo=60, x_hi=600,
                                   dy_lo=8, dy_hi=22)
            translit = translit.strip("[]").strip()
            rows.append({
                "page": pn,
                "speaker": speaker,
                "armenian": armenian,
                "translit": translit,
                "english": english,
            })
    # Merge wrap-around continuations (speaker empty) into the prior turn.
    merged: list[dict] = []
    for r in rows:
        if not r["speaker"] and merged:
            for k in ("armenian", "translit", "english"):
                merged[-1][k] = (merged[-1][k] + " " + r[k]).strip()
        else:
            merged.append(r)
    return merged


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--start", required=True, type=parse_pos,
                    help='start position "page:y", e.g. "27:92"')
    ap.add_argument("--end", required=True, type=parse_pos,
                    help='end position (exclusive) "page:y", e.g. "28:455"')
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tag", type=str, default="sakayan dialogue")
    args = ap.parse_args()

    rows = extract_dialogue(args.pdf, args.start, args.end)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        # No header row — Anki's default TSV import treats row 1 as data.
        for r in rows:
            armenian = phonetics.annotate(r["armenian"], r["translit"])
            english = english_numbers.normalize(r["english"])
            w.writerow([r["speaker"], armenian, english, args.tag])
    print(f"Wrote {len(rows)} dialogue lines → {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
