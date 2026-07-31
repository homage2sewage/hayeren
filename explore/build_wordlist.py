#!/usr/bin/env python3
"""Build the top-N exploration wordlist skeleton.

Reuses the deck pipeline's *validated* lemma filters (personal-name
skip, SKIP_LEMMAS, empty-gloss skip, HAND_OVERRIDES / card-source /
kaikki gloss resolution) from `frequency/build_deck.py` — no new
ranking heuristics are introduced here; the input pool is
`frequency/out/all_lemmas.tsv` (full corpus ranking), drained until
N rows survive the filters.

Output: `explore/words.tsv` with columns

    rank  word  en  ru  ex1  ex2

`en` comes from the deck's gloss resolution (corpus-derived card
sources, kaikki fallback). `ru` is pre-filled from the deck's
Russian layer (`frequency/out/ru_minimal_source.tsv` +
`cards/frequency/russian_glosses.tsv`) where known, else empty.
`ex1`/`ex2` are left empty — they are filled by the generation
pass (a *prior* translation layer, see README.md).

Re-running this script REGENERATES the skeleton and would drop the
filled ru/ex columns; it therefore refuses to overwrite `words.tsv`
unless --force is given, and with --merge it preserves already-
filled ru/ex1/ex2 cells for words that keep their place.
"""

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "frequency"))

import build_deck as bd  # noqa: E402

ALL_LEMMAS = ROOT / "frequency" / "out" / "all_lemmas.tsv"
RU_MINIMAL = ROOT / "frequency" / "out" / "ru_minimal_source.tsv"
OUT = HERE / "words.tsv"

HEADER = ["rank", "word", "en", "ru", "ex1", "ex2"]


def load_ru_layer() -> dict[str, str]:
    """lemma -> russian gloss, from the deck's two Russian sources."""
    ru: dict[str, str] = {}
    if RU_MINIMAL.exists():
        with RU_MINIMAL.open(encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) >= 3 and row[0] and not row[0].startswith("#"):
                    ru.setdefault(row[0].strip(), row[2].strip())
    # curated layer wins over the minimal export
    ru.update(bd.load_russian_glosses())
    return ru


def build(limit: int) -> list[list[str]]:
    index = bd.index_card_translations()
    ru_layer = load_ru_layer()

    with ALL_LEMMAS.open(encoding="utf-8") as f:
        pool = [r for r in csv.reader(f, delimiter="\t") if len(r) >= 4]

    rows: list[list[str]] = []
    for _rank, lemma, _count, _src in pool:
        if len(rows) >= limit:
            break
        if bd._is_personal_name(lemma):
            continue
        if lemma in bd.SKIP_LEMMAS:
            continue

        if lemma in bd.HAND_OVERRIDES:
            en = bd.HAND_OVERRIDES[lemma]
        else:
            entry = bd.best_translation(lemma, index)
            en = entry["translation"] if entry else bd.dictionary_lookup(lemma)
        if not en.strip():
            continue

        # Hand-override glosses follow the deck authoring schema
        # "English / Russian" (` / ` reserved for that boundary,
        # split on the LAST occurrence — mirrors render_gloss).
        en = en.strip()
        ru = ru_layer.get(lemma, "").strip()
        if " / " in en:
            left, right = en.rsplit(" / ", 1)
            if bd._HAS_CYRILLIC.search(right):
                en = left.strip()
                if not ru:
                    ru = right.strip()

        word = " ".join(lemma.split("_"))
        rows.append([str(len(rows) + 1), word, en, ru, "", ""])
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing words.tsv")
    ap.add_argument("--merge", action="store_true",
                    help="preserve filled ru/ex cells from existing words.tsv")
    args = ap.parse_args()

    if OUT.exists() and not (args.force or args.merge):
        print(f"{OUT} exists — pass --force to regenerate or --merge "
              f"to regenerate while keeping filled cells", file=sys.stderr)
        return 1

    old: dict[str, list[str]] = {}
    if args.merge and OUT.exists():
        with OUT.open(encoding="utf-8") as f:
            rdr = csv.reader(f, delimiter="\t")
            next(rdr, None)
            for r in rdr:
                if len(r) >= 6:
                    old[r[1]] = r

    rows = build(args.limit)
    filled = 0
    for r in rows:
        prev = old.get(r[1])
        if prev:
            for i in (3, 4, 5):
                if prev[i].strip() and not r[i].strip():
                    r[i] = prev[i]
            filled += 1

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(rows)

    n_ru = sum(1 for r in rows if r[3].strip())
    print(f"wrote {len(rows)} rows to {OUT} "
          f"(ru filled: {n_ru}, merged from old: {filled})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
