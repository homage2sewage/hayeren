#!/usr/bin/env python3
"""Render a randomized sample of `explore/words.tsv` to a PDF sized
for a ~10-inch e-reader.

Examples:

    # 100 random entries, 2 columns
    python3 explore/make_pdf.py -n 100

    # 60 entries from the 1000–2000 rank tail, 1 column, fixed seed
    python3 explore/make_pdf.py -n 60 --ranks 1000-2000 --columns 1 --seed 7

Output goes to `explore/out/` (git-ignored artifacts) unless -o is
given. Entries are printed in the random draw order — shuffled, not
rank-sorted — since the point is exploration; pass --sort-rank to
re-sort the sample by frequency rank.
"""

import argparse
import csv
import random
import sys
from pathlib import Path

from fpdf import FPDF

HERE = Path(__file__).resolve().parent
WORDS = HERE / "words.tsv"
OUT_DIR = HERE / "out"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

# ~10" e-reader screen (e.g. Kindle Scribe / Onyx Note): 157×209 mm
# usable panel. Rendering 1:1 to that size means no reflow/zoom on
# the device.
PAGE_W, PAGE_H = 157, 209


def load_rows(ranks: str | None) -> list[dict]:
    with WORDS.open(encoding="utf-8") as f:
        rdr = csv.DictReader(f, delimiter="\t")
        rows = [r for r in rdr if r.get("word")]
    if ranks:
        lo, hi = (int(x) for x in ranks.split("-", 1))
        rows = [r for r in rows if lo <= int(r["rank"]) <= hi]
    return rows


def render(rows: list[dict], out: Path, columns: int) -> None:
    pdf = FPDF(unit="mm", format=(PAGE_W, PAGE_H))
    pdf.set_margins(9, 9, 9)
    pdf.set_auto_page_break(True, margin=9)
    pdf.add_font("dejavu", "", FONT_DIR / "DejaVuSans.ttf")
    pdf.add_font("dejavu", "B", FONT_DIR / "DejaVuSans-Bold.ttf")
    pdf.add_font("dejavu", "I", FONT_DIR / "DejaVuSans-Oblique.ttf")
    pdf.add_page()

    with pdf.text_columns(ncols=columns, gutter=7, text_align="LEFT") as cols:
        for r in rows:
            with cols.paragraph(bottom_margin=3.2, wrapmode="WORD") as par:
                pdf.set_text_color(150)
                pdf.set_font("dejavu", "", 7)
                par.write(f"{r['rank']} ")
                pdf.set_text_color(0)
                pdf.set_font("dejavu", "B", 11.5)
                par.write(r["word"])
                pdf.set_font("dejavu", "", 10)
                par.write(f" — {r['ru']}" if r["ru"] else "")
                for ex in (r["ex1"], r["ex2"]):
                    if not ex.strip():
                        continue
                    par.ln()
                    pdf.set_font("dejavu", "I", 9)
                    if " — " in ex:
                        phrase, translation = ex.split(" — ", 1)
                        par.write("· " + phrase)
                        pdf.set_text_color(110)
                        par.write(" — " + translation)
                        pdf.set_text_color(0)
                    else:
                        par.write("· " + ex)

    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="randomized wordlist sample -> e-reader PDF")
    ap.add_argument("-n", type=int, default=100,
                    help="number of entries to sample (default 100)")
    ap.add_argument("--columns", type=int, choices=(1, 2), default=2)
    ap.add_argument("--seed", type=int, default=None,
                    help="random seed (default: nondeterministic)")
    ap.add_argument("--ranks", default=None, metavar="A-B",
                    help="restrict to frequency ranks A..B, e.g. 1000-2000")
    ap.add_argument("--sort-rank", action="store_true",
                    help="sort the sample by rank instead of draw order")
    ap.add_argument("-o", "--out", default=None, help="output PDF path")
    args = ap.parse_args()

    rows = load_rows(args.ranks)
    if not rows:
        print("no rows match", file=sys.stderr)
        return 1
    rng = random.Random(args.seed)
    n = min(args.n, len(rows))
    sample = rng.sample(rows, n)
    if args.sort_rank:
        sample.sort(key=lambda r: int(r["rank"]))

    if args.out:
        out = Path(args.out)
    else:
        tag = f"_r{args.ranks}" if args.ranks else ""
        seed = f"_s{args.seed}" if args.seed is not None else ""
        out = OUT_DIR / f"sample_n{n}{tag}{seed}_{args.columns}col.pdf"

    render(sample, out, args.columns)
    print(f"wrote {n} entries to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
