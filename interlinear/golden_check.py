"""Golden-anchor regression check for glosses.tsv.

Usage: python3 golden_check.py --book ghamoyan --chunk ch2
Reads interlinear/golden/glosses_<book>_<chunk>.tsv; every anchor
must match the current glosses.tsv (lemma equality + ru substring).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--chunk", required=True)
    ap.add_argument("--golden", default=None,
                    help="golden set name (default: the chunk; pass e.g. "
                         "ch2 to check a ch2-derived chunk like ch2v2)")
    args = ap.parse_args()

    name = args.golden or args.chunk
    golden = HERE / "golden" / f"glosses_{args.book}_{name}.tsv"
    current = HERE / args.book / args.chunk / "glosses.tsv"
    with current.open(encoding="utf-8") as f:
        cur = {(r["block_id"], r["surface"]): r
               for r in csv.DictReader(f, delimiter="\t")}
    with golden.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(
            (ln for ln in f if not ln.startswith("#")), delimiter="\t")]

    failures = 0
    for g in rows:
        key = (g["block_id"], g["surface"])
        c = cur.get(key)
        if c is None:
            print(f"FAIL: golden anchor {key} missing from glosses.tsv")
            failures += 1
            continue
        if c["lemma"] != g["lemma"]:
            print(f"FAIL: {key} lemma {c['lemma']!r} != {g['lemma']!r}")
            failures += 1
        if g["ru_contains"] not in c["ru"]:
            print(f"FAIL: {key} ru {c['ru']!r} lacks {g['ru_contains']!r}")
            failures += 1
    print(f"{len(rows)} golden anchors, {failures} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
