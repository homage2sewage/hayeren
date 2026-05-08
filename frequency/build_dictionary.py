#!/usr/bin/env python3
"""One-time compaction of `data/armenian.jsonl` (kaikki.org Armenian
Wiktionary dump, ~22K entries, 200 MB) into a small lookup-friendly
TSV at `data/armenian_dict.tsv`.

The full JSONL has ~30 fields per entry (etymology, pronunciations,
inflection templates, etc.). For deck-building we only need:

    word  \\t  pos  \\t  english_glosses_joined_with_pipes

After compaction the file is ~3 MB and loads as a dict in <1 second.

Run once after downloading the JSONL. `dictionary.py` reads the
compact TSV at runtime.
"""

import csv
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SRC = DATA / "armenian.jsonl"
DST = DATA / "armenian_dict.tsv"


def gloss_for(entry: dict) -> str:
    """Return all English glosses for an entry, separated by ` | `.
    Empty if the entry has no senses (rare)."""
    glosses: list[str] = []
    for s in entry.get("senses", []):
        for g in s.get("glosses", []):
            g = g.strip()
            if g and g not in glosses:
                glosses.append(g)
    return " | ".join(glosses)


def main() -> None:
    if not SRC.exists():
        print(f"Source missing: {SRC}", file=sys.stderr)
        sys.exit(1)
    rows: dict[tuple[str, str], list[str]] = {}
    seen = 0
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            seen += 1
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("lang") != "Armenian":
                continue
            word = (d.get("word") or "").strip()
            pos = (d.get("pos") or "").strip()
            if not word:
                continue
            gloss = gloss_for(d)
            if not gloss:
                continue
            key = (word, pos)
            # Some words have multiple entries (different etymologies).
            # Concatenate their glosses.
            if key in rows:
                rows[key].append(gloss)
            else:
                rows[key] = [gloss]
    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for (word, pos), glosses_list in sorted(rows.items()):
            joined = " | ".join(glosses_list)
            w.writerow([word, pos, joined])
    print(f"Read {seen} entries; wrote {len(rows)} rows → {DST}",
          file=sys.stderr)
    print(f"File size: {DST.stat().st_size / 1024:.1f} KB", file=sys.stderr)


if __name__ == "__main__":
    main()
