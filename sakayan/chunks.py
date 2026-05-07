#!/usr/bin/env python3
"""Harvest reusable lexical chunks from dialogue TSVs.

Per the research file (`armenian-vocab-research.md`), multi-word
phrases transfer to speech better than isolated words. The dialogue
TSVs already pair short utterances with their English translations —
this script just filters them to produce a chunk-card deck.

Heuristics:
- Word count ≤ 7 (most utterances are 2–6 words; longer ones tend to
  be multi-clause and don't make good chunk cards).
- One Armenian sentence (single ։ at end), one English clause.
- Dedup by Armenian text — a phrase like "Բարև" appears in many
  dialogues but should give one chunk card.

The Speaker column from the dialogue TSVs is dropped; chunks are
context-free phrases. Tags carry the unit and dialogue origin so you
can suspend specific groups in Anki if needed.

Usage:
    .venv/bin/python chunks.py
"""

import csv
import glob
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CARDS = HERE.parent / "cards" / "sakayan"
DEFAULT_OUT = CARDS / "chunks.tsv"
DIALOGUE_GLOB = str(CARDS / "unit*_dialogue*.tsv")

MAX_WORDS = 7


def is_chunk_candidate(armenian: str) -> bool:
    """Strip phonetic hints, then check word count and sentence count."""
    plain = re.sub(r"\s*\[[^\]]+\]", "", armenian).strip()
    if not plain:
        return False
    if len(plain.split()) > MAX_WORDS:
        return False
    # Reject multi-sentence Armenian: more than one ։ usually means a
    # complex exchange that shouldn't be a single chunk card.
    if plain.count("։") > 1:
        return False
    return True


def main() -> None:
    seen_armenian: set[str] = set()
    chunks: list[tuple[str, str, str]] = []

    for path in sorted(glob.glob(DIALOGUE_GLOB)):
        path_obj = Path(path)
        m = re.search(r"unit(\d+)", path_obj.name)
        unit_n = int(m.group(1)) if m else 0
        for row in csv.reader(path_obj.open(encoding="utf-8"), delimiter="\t"):
            if len(row) < 4:
                continue
            _speaker, armenian, english, _src_tags = row
            armenian = armenian.strip()
            english = english.strip()
            if not armenian or not english:
                continue
            if not is_chunk_candidate(armenian):
                continue
            # Dedup key strips the phonetic hint so spelling-only
            # duplicates collapse.
            key = re.sub(r"\s*\[[^\]]+\]", "", armenian).strip()
            if key in seen_armenian:
                continue
            seen_armenian.add(key)
            chunks.append((armenian, english, f"sakayan unit{unit_n} chunk"))

    DEFAULT_OUT.parent.mkdir(parents=True, exist_ok=True)
    with DEFAULT_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for c in chunks:
            w.writerow(c)
    print(f"Wrote {len(chunks)} chunk cards → {DEFAULT_OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
