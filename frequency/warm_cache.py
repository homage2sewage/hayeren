#!/usr/bin/env python3
"""Politely populate the Wiktionary cache for top-1000 lemmas missing
translations.

Wiktionary rate-limits aggressive lookups (HTTP 429). This script
fetches *one* uncached lemma per second for as long as it's running,
which Wiktionary tolerates indefinitely. Stop with Ctrl-C; the cache
persists. Run again later to continue from where you left off — it
skips already-cached entries.

Once cached, run `build_deck.py --with-wiktionary --cache-only` to
regenerate `cards/top_1000.tsv` with the new translations folded in.

Usage:
    .venv/bin/python warm_cache.py            # warm all uncovered
    .venv/bin/python warm_cache.py --top 200  # only top-200 lemmas
"""

import argparse
import csv
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

sys.path.insert(0, str(ROOT / "sakayan"))
import lookup  # noqa: E402
import glosser  # noqa: E402

import build_deck  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=1000)
    ap.add_argument("--delay", type=float, default=1.0,
                    help="seconds between fresh API calls (default 1.0)")
    args = ap.parse_args()

    # Build the index of already-translated lemmas (sakayan/ghamoyan/freq).
    card_index = build_deck.index_card_translations()

    top_path = HERE / "out" / "our_top_1000.tsv"

    todo: list[tuple[int, str]] = []
    with top_path.open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 4:
                continue
            rank = int(row[0])
            lemma = row[1]
            if rank > args.top:
                break
            # Skip if already covered by a card source.
            if build_deck.best_translation(lemma, card_index):
                continue
            # Skip if already cached.
            cache_path = lookup.CACHE / f"wiki-{lemma}.json"
            if cache_path.exists():
                continue
            todo.append((rank, lemma))

    print(f"{len(todo)} uncached lemmas to warm "
          f"(of top-{args.top}).", file=sys.stderr, flush=True)

    successes = 0
    failures = 0
    for rank, lemma in todo:
        time.sleep(args.delay)
        try:
            wikitext = lookup.fetch_wikitext(lemma)
            if wikitext:
                successes += 1
                status = "✓"
            else:
                # 404 from API — Wiktionary doesn't have an entry
                successes += 1  # cached as None, no need to retry
                status = "∅"
        except Exception as e:
            failures += 1
            status = f"✗ {type(e).__name__}"
        print(f"  rank {rank:4d}  {lemma:25s}  {status}",
              file=sys.stderr, flush=True)

    print(f"\nDone: {successes} cached / {failures} failed",
          file=sys.stderr)


if __name__ == "__main__":
    main()
