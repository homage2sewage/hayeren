#!/usr/bin/env python3
"""Generate Anki paradigm cards from `paradigms_data.PARADIGMS`.

Each cell of a verb paradigm becomes its own Anki card. This follows
SRS conventions for grammar drilling:

- one card per form (so every conjugation is reviewed independently)
- bidirectional via Anki's note-type templates (we just write the data;
  the reverse direction is configured in Anki itself)
- tagged by unit, verb, and tense — easy to filter or suspend by tag

Phonetic deviations (e.g. դ→թ) are not annotated for paradigm cards
because the textbook's transliteration column doesn't accompany them.
If specific forms have deviations, edit `paradigms_data.py` to embed
the `[phonetic]` form directly in the Armenian field.

Usage:
    .venv/bin/python paradigms.py --unit 1 --out out/unit1_paradigms.tsv
    .venv/bin/python paradigms.py                  # all units → out/paradigms.tsv
"""

import argparse
import csv
import sys
from pathlib import Path

import paradigms_data


HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "out" / "paradigms.tsv"


def emit_cards(entries: list[dict], tag_prefix: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for e in entries:
        tags = (
            f"{tag_prefix} unit{e['unit']} paradigm "
            f"verb:{e['verb']} tense:{e['tense'].replace(' ', '_')}"
        )
        for person, (arm, eng) in e["forms"].items():
            rows.append((arm, eng, tags))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unit", type=int,
                    help="filter to one unit (default: all)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--tag", type=str, default="sakayan",
                    help="prefix for Anki tags")
    args = ap.parse_args()

    entries = paradigms_data.PARADIGMS
    if args.unit is not None:
        entries = [e for e in entries if e["unit"] == args.unit]

    cards = emit_cards(entries, args.tag)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for c in cards:
            w.writerow(c)
    print(f"Wrote {len(cards)} paradigm cards "
          f"({len(entries)} paradigms) → {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
