"""Step B prep: deterministic candidate table for word selection.

Tokenizes every block of book.md and attaches, per token:
  lemma       via frequency/build_ours.lemmatize (heuristic — the
              LLM selection pass must sanity-check it in context)
  rank        corpus frequency rank from frequency/out/our_top_1000.tsv
  known       lemma is in the learner's deck (cards/top_1000.tsv)

Output: candidates.tsv — a *signal* for the LLM selector, not a rule
(FRD § B). The frequency-threshold baseline for the challenge
protocol is derived from the same table.

Usage: python3 select_prep.py --book ghamoyan --chunk ch2
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "frequency"))
from common import ROOT, parse_book_md  # noqa: E402
import build_ours  # noqa: E402
from query_kb import load_known_lemmas  # noqa: E402


def load_ranks() -> dict[str, int]:
    ranks: dict[str, int] = {}
    with (ROOT / "frequency" / "out" / "our_top_1000.tsv").open(
            encoding="utf-8") as f:
        for line in f:
            cols = line.rstrip("\n").split("\t")
            if len(cols) >= 2 and cols[0].strip().isdigit():
                ranks.setdefault(cols[1].strip().lower(), int(cols[0]))
    return ranks


def load_deck_lemmas() -> set[str]:
    deck: set[str] = set()
    path = ROOT / "cards" / "top_1000.tsv"
    with path.open(encoding="utf-8") as f:
        for line in f:
            m = re.match(r"<b>([^<[]+)", line)
            if m:
                deck.add(m.group(1).strip().lower())
    return deck


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--chunk", required=True)
    args = ap.parse_args()
    out_dir = HERE / args.book / args.chunk

    blocks = parse_book_md(out_dir / "book.md")
    ranks = load_ranks()
    deck = load_deck_lemmas()
    known = load_known_lemmas()
    inflected = build_ours.collect_inflected_to_lemma()

    rows = []
    for blk in blocks:
        tokens = build_ours.tokenize(blk.plain)
        for i, tok in enumerate(tokens):
            low = tok.lower()
            lemma = build_ours.lemmatize(low, known, inflected)
            rows.append((
                f"{blk.id:04d}", i, tok, lemma,
                ranks.get(lemma, ""),
                "y" if lemma in deck else "",
            ))

    with (out_dir / "candidates.tsv").open("w", encoding="utf-8",
                                           newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["block_id", "tok", "surface", "lemma", "rank", "known"])
        w.writerows(rows)
    n_unknown = sum(1 for r in rows if not r[5])
    uniq = {r[3] for r in rows}
    uniq_unknown = {r[3] for r in rows if not r[5]}
    print(f"{len(rows)} tokens, {len(uniq)} unique lemmas, "
          f"{n_unknown} tokens / {len(uniq_unknown)} lemmas outside deck "
          f"-> {out_dir/'candidates.tsv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
