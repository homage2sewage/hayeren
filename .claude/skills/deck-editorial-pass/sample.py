#!/usr/bin/env python3
"""Sample rows from a card deck TSV for editorial review.

Used by the `deck-editorial-pass` skill (stage 3 of the deck-review
pipeline) to produce a deterministic, reproducible sample for an
agent-driven editorial critic.

Usage:
    python3 sample.py <deck.tsv> [-n N] [--seed S] [--stratified]

The sample is written to stdout in the original TSV format
(lemma\tgloss\ttags). Rows are sorted by rank for readability.
"""

import argparse
import csv
import random
import re
import sys
from pathlib import Path


RANK_RE = re.compile(r"rank-(\d+)")


def rank_of(row: list[str]) -> int:
    """Extract the numeric rank from the tags column."""
    if len(row) < 3:
        return 0
    m = RANK_RE.search(row[2])
    return int(m.group(1)) if m else 0


def load_deck(path: Path) -> list[list[str]]:
    """Load TSV rows. Skips empty lines."""
    rows = []
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if not row or not row[0].strip():
                continue
            rows.append(row)
    return rows


def stratified_sample(rows: list[list[str]], n: int) -> list[list[str]]:
    """Sample proportionally across rank buckets.

    Buckets:
      top-100      (ranks 1-100, the most learner-facing)
      101-500      (mid-frequency core)
      501-1000     (low-frequency core)
      1000+        (tail; out-of-top-1000 source rows)

    Each bucket gets max(1, n//4) rows, up to bucket size.
    """
    buckets: dict[str, list[list[str]]] = {
        "top-100": [],
        "101-500": [],
        "501-1000": [],
        "1000+": [],
    }
    for r in rows:
        rk = rank_of(r)
        if 1 <= rk <= 100:
            buckets["top-100"].append(r)
        elif 101 <= rk <= 500:
            buckets["101-500"].append(r)
        elif 501 <= rk <= 1000:
            buckets["501-1000"].append(r)
        else:
            buckets["1000+"].append(r)

    per_bucket = max(1, n // 4)
    sample: list[list[str]] = []
    for name, br in buckets.items():
        if br:
            sample.extend(random.sample(br, min(per_bucket, len(br))))
    return sample


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Sample rows from a card deck TSV for editorial review."
    )
    ap.add_argument("deck", type=Path, help="Path to deck TSV")
    ap.add_argument("-n", type=int, default=30,
                    help="Sample size (default: 30)")
    ap.add_argument("--seed", type=int, default=42,
                    help="Random seed (default: 42; vary to get fresh samples)")
    ap.add_argument("--stratified", action="store_true",
                    help="Stratified sample across rank buckets")
    ap.add_argument("--header", action="store_true",
                    help="Emit a header comment line at the top")
    args = ap.parse_args()

    if not args.deck.exists():
        print(f"FATAL: deck not found: {args.deck}", file=sys.stderr)
        return 2

    rows = load_deck(args.deck)
    if not rows:
        print(f"FATAL: no rows loaded from {args.deck}", file=sys.stderr)
        return 2

    random.seed(args.seed)

    if args.stratified:
        sample = stratified_sample(rows, args.n)
    else:
        sample = random.sample(rows, min(args.n, len(rows)))

    sample.sort(key=rank_of)

    if args.header:
        print(f"# deck-editorial-pass sample")
        print(f"# source: {args.deck}")
        print(f"# n={len(sample)} seed={args.seed} "
              f"stratified={args.stratified}")
        print(f"# columns: lemma<TAB>gloss<TAB>tags")
        print()

    for r in sample:
        print("\t".join(r))

    return 0


if __name__ == "__main__":
    sys.exit(main())
