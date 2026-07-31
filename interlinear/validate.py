"""Step E (mechanical): verify book.md against the source JSONL.

Two invariants:

1. blocks.tsv text == book.md blocks stripped of markup (artifact
   self-consistency).
2. squash(blocks in reading order) == squash(source lines in reading
   order, minus drops.tsv) — the whitespace-insensitive byte-check,
   same discipline as the citation hooks. Reading order for blocks is
   (first page, y0), which re-inserts the footnote at its true page
   position.

Known limitation (documented in the FRD): squash() cannot catch a
space wrongly inserted *inside* a word — that class is covered by the
golden-page eyeball and the editorial pass.

Usage: python3 validate.py --book ghamoyan --pages 35-40 --chunk ch2
"""
from __future__ import annotations

import argparse
import csv
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (PROFILES, cluster_lines, load_spans, parse_book_md,  # noqa: E402
                    squash)


def norm(text: str) -> str:
    """squash + drop footnote-marker punctuation (kept as digits)."""
    return squash(text).replace("[^", "").replace("]:", "").replace("]", "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=sorted(PROFILES))
    ap.add_argument("--pages", required=True)
    ap.add_argument("--chunk", required=True)
    args = ap.parse_args()

    profile = PROFILES[args.book]
    a, b = args.pages.split("-")
    pages = range(int(a), int(b) + 1)
    out_dir = Path(__file__).resolve().parent / args.book / args.chunk

    blocks = parse_book_md(out_dir / "book.md")
    failures = 0

    # -- invariant 1: book.md vs blocks.tsv
    with (out_dir / "blocks.tsv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != len(blocks):
        print(f"FAIL: {len(rows)} tsv rows vs {len(blocks)} md blocks")
        failures += 1
    for row, blk in zip(rows, blocks):
        if squash(row["text"]) != squash(blk.plain):
            print(f"FAIL: block {row['block_id']} text drift md<->tsv")
            failures += 1

    # -- invariant 2: reading-order byte equality vs source.
    # Body and footnotes are compared as SEPARATE streams: a footnote
    # sits mid-page in the source but is a trailing block in book.md,
    # and can even interleave inside a cross-page paragraph — a
    # block-level sort cannot reproduce that, a stream split can.
    # Same classification code path as the builder (shared import).
    from structure import classify_lines, mark_footnote_refs
    spans = load_spans(profile, pages)
    mark_footnote_refs(spans, profile)
    lines = cluster_lines(spans, profile)
    body_lines, foot_lines, _, _ = classify_lines(lines, profile)

    def compare(name: str, src: str, got: str) -> int:
        src_n, got_n = norm(src), norm(got)
        if src_n == got_n:
            print(f"OK: {name} byte-check passed "
                  f"({len(src_n)} chars squashed)")
            return 0
        print(f"FAIL: {name} byte-check "
              f"({len(src_n)} vs {len(got_n)} chars)")
        sm = difflib.SequenceMatcher(a=src_n, b=got_n, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal":
                print(f"  {tag}: src[{i1}:{i2}]={src_n[i1:i2]!r} "
                      f"got[{j1}:{j2}]={got_n[j1:j2]!r}")
        return 1

    failures += compare(
        "body",
        "".join(ln.text for ln in body_lines),
        "".join(b.plain for b in blocks if b.kind != "footnote"))
    failures += compare(
        "footnotes",
        "".join(ln.text for ln in foot_lines),
        "".join(b.plain for b in blocks if b.kind == "footnote"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
