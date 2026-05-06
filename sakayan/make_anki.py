#!/usr/bin/env python3
"""Walk units.json and produce Anki-importable TSV for every unit.

Outputs into out/by-unit/:

    unit{N}_vocab.tsv           — vocab table for unit N
    unit{N}_dialogue{i}.tsv     — each dialogue
    paradigms.tsv               — all hand-curated paradigm cards

Plus a combined `all.tsv` that concatenates every per-unit TSV.

Run after `build_units.py`. No PDF parsing here — the per-unit logic
delegates to `vocab.extract_rows` and `dialogues.extract_dialogue`.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

import chunks
import dialogues
import english_numbers
import phonetics
import paradigms_data
import vocab


HERE = Path(__file__).resolve().parent
DEFAULT_PDF = HERE / "dora_sahakyan.pdf"
UNITS_JSON = HERE / "units.json"
OUT_DIR = HERE / "out" / "by-unit"


def write_vocab(rows: list[dict], path: Path, tag: str) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for r in rows:
            for arm_part, tr_part, eng_part in vocab._split_pairs(
                    r["armenian"], r["translit"], r["english"]):
                armenian = phonetics.annotate(arm_part, tr_part)
                english = english_numbers.normalize(eng_part)
                w.writerow([armenian, english, tag])
                n += 1
    return n


def write_dialogue(rows: list[dict], path: Path, tag: str) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for r in rows:
            armenian = phonetics.annotate(r["armenian"], r["translit"])
            english = english_numbers.normalize(r["english"])
            w.writerow([r["speaker"], armenian, english, tag])
            n += 1
    return n


def run_unit(pdf_path: Path, unit: dict, out_dir: Path) -> dict:
    n = unit["unit_n"]
    counts = {"vocab": 0, "dialogues": 0, "dialogue_files": 0}

    if unit["vocab_pages"]:
        rows = vocab.extract_rows(pdf_path, unit["vocab_pages"])
        path = out_dir / f"unit{n:02d}_vocab.tsv"
        counts["vocab"] = write_vocab(rows, path, f"sakayan unit{n} vocab")

    for d in unit["dialogues"]:
        start = (d["start"]["page"], d["start"]["y"])
        end = (d["end"]["page"], d["end"]["y"])
        rows = dialogues.extract_dialogue(pdf_path, start, end)
        path = out_dir / f"unit{n:02d}_dialogue{d['n']}.tsv"
        added = write_dialogue(rows, path, f"sakayan unit{n} dialogue{d['n']}")
        counts["dialogues"] += added
        if added:
            counts["dialogue_files"] += 1

    return counts


def write_paradigms(out_dir: Path) -> int:
    path = out_dir / "paradigms.tsv"
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for e in paradigms_data.PARADIGMS:
            tags = (
                f"sakayan unit{e['unit']} paradigm "
                f"verb:{e['verb']} tense:{e['tense'].replace(' ', '_')}"
            )
            for arm, eng in e["forms"].values():
                w.writerow([arm, eng, tags])
                n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--units", type=Path, default=UNITS_JSON)
    ap.add_argument("--unit", type=int,
                    help="run only one unit (default: all)")
    args = ap.parse_args()

    units = json.loads(args.units.read_text())
    if args.unit is not None:
        units = [u for u in units if u["unit_n"] == args.unit]

    args.out.mkdir(parents=True, exist_ok=True)
    print(f"Writing TSVs into {args.out}", file=sys.stderr)

    grand = {"vocab": 0, "dialogues": 0, "dialogue_files": 0}
    for u in units:
        c = run_unit(args.pdf, u, args.out)
        for k in grand:
            grand[k] += c[k]
        print(f"  unit {u['unit_n']:2d}  vocab={c['vocab']:4d}  "
              f"dialogues={c['dialogues']:4d} ({c['dialogue_files']} files)",
              file=sys.stderr)

    if args.unit is None:
        para_count = write_paradigms(args.out)
        print(f"  paradigms={para_count}", file=sys.stderr)
        # Lexical chunks harvested from the just-written dialogue TSVs.
        chunks.main()

    print(f"\n  TOTAL  vocab={grand['vocab']}  dialogues={grand['dialogues']}",
          file=sys.stderr)

    # Combined deck — all per-unit TSVs concatenated. Note: vocab cards
    # have 3 columns, dialogue cards have 4 (extra Speaker col), so we
    # normalize dialogue rows by pulling the speaker into the Armenian
    # field as a prefix.
    if args.unit is None:
        all_path = args.out / "all.tsv"
        with all_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            for path in sorted(args.out.glob("*.tsv")):
                if path.name == "all.tsv":
                    continue
                with path.open(encoding="utf-8") as src:
                    for line in src:
                        cells = line.rstrip("\n").split("\t")
                        if len(cells) == 4:  # dialogue: speaker, arm, eng, tags
                            speaker, arm, eng, tags = cells
                            arm = f"{speaker}: {arm}" if speaker else arm
                            cells = [arm, eng, tags]
                        w.writerow(cells)
        print(f"  combined → {all_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
