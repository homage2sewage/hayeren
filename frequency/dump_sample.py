#!/usr/bin/env python3
"""Dump a human-eyeball sample of `cards/top_1000.tsv` to
`out/deck_sample.md` — top-25, bottom-25, and 50 random rows in a
markdown table easy to scan as a learner.

Run after `validate_deck.py` to catch editorial-quality issues that
the structural checks don't anticipate. Each new "this looks weird"
finding from a sample read should turn into a `check_*` function in
`validate_deck.py` (see `llm-workflow.md` § 9).

Usage:  python3 dump_sample.py [--n-random 50] [--seed 0]
"""
from __future__ import annotations

import argparse
import csv
import random
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
DECK_PATH = HERE.parent / "cards" / "top_1000.tsv"
OUT_PATH = HERE / "out" / "deck_sample.md"


def rank_of(tags: str) -> int:
    m = re.search(r"rank-(\d+)", tags)
    return int(m.group(1)) if m else -1


def src_of(tags: str) -> str:
    m = re.search(r"src-(\S+)", tags)
    return m.group(1) if m else "?"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-random", type=int, default=50)
    ap.add_argument("--n-edge", type=int, default=25,
                    help="rows to take from each end (top + bottom)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    rows: list[tuple[int, str, str, str]] = []
    with DECK_PATH.open(encoding="utf-8") as f:
        for r in csv.reader(f, delimiter="\t"):
            if len(r) < 3:
                continue
            rows.append((rank_of(r[2]), r[0], r[1], src_of(r[2])))
    rows.sort(key=lambda x: x[0])

    head = rows[:args.n_edge]
    tail = rows[-args.n_edge:]
    random.seed(args.seed)
    middle = random.sample(rows[args.n_edge:-args.n_edge],
                           min(args.n_random,
                               max(0, len(rows) - 2 * args.n_edge)))
    middle.sort(key=lambda x: x[0])

    lines: list[str] = []
    lines.append("# Deck sample for human-eye review\n")
    lines.append(f"Source: `cards/top_1000.tsv` ({len(rows)} rows)")
    lines.append(f"Sampling: top-{args.n_edge}, bottom-{args.n_edge}, "
                 f"{len(middle)} random middle (seed={args.seed})")
    lines.append("")
    lines.append("**How to read.** Scan as a learner would, not as a "
                 "pipeline reviewer. For each row ask: *would this be "
                 "useful as a flashcard front/back?* Anything off — "
                 "verbose gloss, dictionary prose, awkward phrasing, "
                 "register mismatch, missing context — is a candidate "
                 "for a new `check_*` in `validate_deck.py` or a "
                 "`HAND_OVERRIDE` in `build_deck.py`.\n")

    def render_section(title: str, sec_rows: list) -> None:
        lines.append(f"## {title}\n")
        lines.append("| rank | lemma | gloss | src |")
        lines.append("|---:|---|---|---|")
        for rk, lemma, tr, src in sec_rows:
            tr_clean = tr.replace("|", "\\|")
            lines.append(f"| {rk} | `{lemma}` | {tr_clean} | {src} |")
        lines.append("")

    render_section(f"Top {args.n_edge}", head)
    render_section(f"Random middle ({len(middle)})", middle)
    render_section(f"Bottom {args.n_edge}", tail)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
