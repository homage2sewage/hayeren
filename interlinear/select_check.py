"""Step B check: validate selection.tsv against book.md + candidates.

- anchor check: the surface string literally occurs in its block
- depth check: warn when the (heuristic) lemma is deck-known —
  learner-1k profile should not gloss known words
- dedup check: same heuristic lemma selected more than once
- density report per block

Usage: python3 select_check.py --book ghamoyan --chunk ch2
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "frequency"))
from common import parse_book_md  # noqa: E402
from select_prep import load_deck_lemmas  # noqa: E402
import build_ours  # noqa: E402
from query_kb import load_known_lemmas  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--chunk", required=True)
    args = ap.parse_args()
    out_dir = HERE / args.book / args.chunk

    blocks = {f"{b.id:04d}": b for b in parse_book_md(out_dir / "book.md")}
    deck = load_deck_lemmas()
    known = load_known_lemmas()
    inflected = build_ours.collect_inflected_to_lemma()

    with (out_dir / "selection.tsv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    errors = warnings = 0
    lemma_of: dict[str, str] = {}
    for r in rows:
        blk = blocks.get(r["block_id"])
        if blk is None:
            print(f"ERROR: {r['surface']}: no block {r['block_id']}")
            errors += 1
            continue
        if r["surface"] not in blk.plain:
            print(f"ERROR: {r['surface']!r} not found in block "
                  f"{r['block_id']}")
            errors += 1
            continue
        if r["kind"] in ("mwe", "abbr"):
            continue
        head = r["surface"].split()[0].lower()
        lemma_of[r["surface"]] = build_ours.lemmatize(head, known, inflected)

    for surface, lemma in lemma_of.items():
        if lemma in deck:
            print(f"WARN: {surface} -> lemma {lemma!r} is deck-known "
                  f"(learner-1k should skip)")
            warnings += 1
    dupes = Counter(lemma_of.values())
    for lemma, n in dupes.items():
        if n > 1:
            surfs = [s for s, l in lemma_of.items() if l == lemma]
            print(f"WARN: lemma {lemma!r} selected {n}x: {surfs}")
            warnings += 1

    per_block = Counter(r["block_id"] for r in rows)
    dense = [f"{b}:{n}" for b, n in per_block.most_common(5)]
    print(f"{len(rows)} selections over {len(per_block)} blocks "
          f"({len(blocks)} total); densest: {', '.join(dense)}")
    print(f"{errors} errors, {warnings} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
