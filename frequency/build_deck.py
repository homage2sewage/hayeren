#!/usr/bin/env python3
"""Build the unified top-1000 deck from the frequency list + existing
card translations.

Pipeline:
1. Read `out/our_top_1000.tsv` (rank | lemma | count | sources).
2. Index translations from existing card files in `../cards/`:
     ../cards/sakayan/unit*_vocab.tsv     (col 0 → col 1, lemma form)
     ../cards/ghamoyan/fillers.tsv        (col 0 → col 1 "en / ru" combined)
     ../cards/frequency/gap_additions.tsv (col 0 → col 1 "en / ru" combined)
     ../cards/sakayan/paradigms.tsv       (col 0 → col 1; tag has verb:LEMMA
                                           so the verb infinitive resolves
                                           via the tag rather than col 0)
3. For each top-1000 lemma, pick best translation:
     a) Direct vocab / filler / gap entry (with translation from card).
     b) Paradigm-tag verb-infinitive entry (typical English: "to X").
     c) Wiktionary fallback via `sakayan/glosser.py`.
4. Emit `../cards/top_1000.tsv`:
     Armenian \t English / Russian \t tags  (with rank in tags)

Russian translations come for free where the source card already has
combined "en / ru" (fillers + gap additions). For other sources the
field will be English-only.

Usage:  python3 build_deck.py [--limit 1000]
"""

import argparse
import csv
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CARDS = ROOT / "cards"
SAKAYAN_CARDS = CARDS / "sakayan"
GHAMOYAN_CARDS = CARDS / "ghamoyan"
FREQUENCY_CARDS = CARDS / "frequency"

# Same tokenizer / lemmatizer / known-lemma machinery as build_ours.py
import build_ours  # noqa: E402


# ---------- helpers ----------


_ANNOTATION = re.compile(r"\s*[\[\(].*?[\]\)]")
_INTRAWORD_PUNCT = re.compile(r"[՚-՟]")


def armenian_tokens(cell: str) -> list[str]:
    """All Armenian tokens in a card cell, with annotations stripped.
    Length tells you whether it's a single word or a phrase."""
    cleaned = _ANNOTATION.sub("", cell)
    cleaned = _INTRAWORD_PUNCT.sub("", cleaned)
    return [t.lower() for t in build_ours.ARMENIAN_TOKEN.findall(cleaned)]


def first_armenian_token(cell: str) -> str:
    toks = armenian_tokens(cell)
    return toks[0] if toks else ""


# ---------- translation indexing ----------


def index_card_translations() -> dict[str, list[dict]]:
    """Return {lemma_lower: [{translation, source, raw_armenian, single_word}, …]}.

    Multi-word entries are still indexed under their first token, but
    flagged single_word=False so single-word matches are preferred at
    pick time (e.g. `մի` from filler "մի խոսքով" doesn't override the
    real single-word meaning of `մի`)."""
    index: dict[str, list[dict]] = {}

    def add(lemma: str, translation: str, source: str, raw: str,
            single_word: bool) -> None:
        if not lemma or not translation.strip():
            return
        index.setdefault(lemma, []).append({
            "translation": translation,
            "source": source,
            "raw_armenian": raw,
            "single_word": single_word,
        })

    def index_simple_tsv(path: Path, source: str) -> None:
        if not path.exists():
            return
        with path.open(encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) < 2:
                    continue
                toks = armenian_tokens(row[0])
                if not toks:
                    continue
                add(toks[0], row[1].strip(), source, row[0],
                    single_word=(len(toks) == 1))

    for path in sorted(SAKAYAN_CARDS.glob("unit*_vocab.tsv")):
        index_simple_tsv(path, "sakayan-vocab")
    index_simple_tsv(GHAMOYAN_CARDS / "fillers.tsv", "ghamoyan-filler")
    index_simple_tsv(FREQUENCY_CARDS / "gap_additions.tsv", "frequency-gap")

    # Paradigms: pull the verb's clean English infinitive directly from
    # paradigms_data.py (each paradigm dict has `english_infinitive`).
    # This gives us "to have" instead of trying to mangle "I have" or
    # "I read (past)" into infinitive form.
    sys.path.insert(0, str(ROOT / "sakayan"))
    import paradigms_data  # noqa: E402
    for entry in paradigms_data.PARADIGMS:
        verb = entry.get("verb", "").lower()
        eng = entry.get("english_infinitive", "")
        if verb and eng and verb != "—":
            add(verb, eng, "sakayan-paradigm", verb, single_word=True)

    return index


# ---------- main ----------


def best_translation(lemma: str, index: dict[str, list[dict]]) -> dict | None:
    """Pick best translation entry. Sort key — lower is better:

    1. single-word entries before multi-word entries (so `մի` doesn't
       inherit `մի խոսքով`'s "in a word" gloss)
    2. exact-match raw_armenian == lemma before non-exact
    3. source priority — vocab and gap/filler give the cleanest
       glosses, paradigms are last-resort because we lose nuance
    """
    entries = index.get(lemma, [])
    if not entries:
        return None
    source_priority = {
        "sakayan-vocab": 0,
        "frequency-gap": 1,
        "ghamoyan-filler": 2,
        "sakayan-paradigm": 3,
    }

    def sort_key(e: dict) -> tuple:
        return (
            0 if e["single_word"] else 1,
            0 if e["raw_armenian"].strip().lower() == lemma else 1,
            source_priority.get(e["source"], 99),
        )

    return min(entries, key=sort_key)


def wiktionary_lookup(lemma: str) -> str:
    """Fetch first 1-3 definitions from Wiktionary via glosser.
    Returns empty string on cache miss + rate limit."""
    sys.path.insert(0, str(ROOT / "sakayan"))
    import glosser  # noqa: E402
    try:
        result = glosser.gloss_token(lemma)
    except Exception:
        return ""
    defs = result.get("definitions", [])
    if not defs:
        return ""
    # Take up to 2 definitions, semicolon-joined, capped length.
    short = "; ".join(defs[:2])
    return short[:120]


def build(limit: int = 1000, with_wiktionary: bool = False) -> None:
    top_path = HERE / "out" / "our_top_1000.tsv"
    out_path = CARDS / "top_1000.tsv"

    index = index_card_translations()
    print(f"Indexed {len(index)} unique-lemma translation sources",
          file=sys.stderr, flush=True)

    rows_out: list[list[str]] = []
    stats = {"vocab": 0, "filler": 0, "gap": 0, "paradigm": 0,
             "wiktionary": 0, "no-translation": 0}

    with top_path.open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 4:
                continue
            rank, lemma, count, _src = row
            rank_n = int(rank)
            if rank_n > limit:
                break

            translation = ""
            source = ""
            entry = best_translation(lemma, index)
            if entry:
                translation = entry["translation"]
                source = entry["source"]
                if source == "sakayan-vocab":
                    stats["vocab"] += 1
                elif source == "ghamoyan-filler":
                    stats["filler"] += 1
                elif source == "frequency-gap":
                    stats["gap"] += 1
                elif source == "sakayan-paradigm":
                    stats["paradigm"] += 1
            elif with_wiktionary:
                translation = wiktionary_lookup(lemma)
                if translation:
                    source = "wiktionary"
                    stats["wiktionary"] += 1
                else:
                    source = "—"
                    stats["no-translation"] += 1
            else:
                source = "—"
                stats["no-translation"] += 1

            tags = f"frequency top-1000 rank-{rank_n:04d} src-{source}"
            rows_out.append([lemma, translation, tags])

            if rank_n <= 10 or rank_n % 50 == 0:
                print(f"  rank {rank_n:4d}  {lemma:25s}  [{source}]  "
                      f"{translation[:60]}", file=sys.stderr, flush=True)

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for r in rows_out:
            w.writerow(r)

    print(f"\nWrote {len(rows_out)} cards → {out_path}", file=sys.stderr)
    print("Translation sources:", file=sys.stderr)
    for src, n in stats.items():
        pct = 100 * n / len(rows_out) if rows_out else 0
        print(f"  {src:18s}  {n:4d}  ({pct:.1f}%)", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--with-wiktionary", action="store_true",
                    help="fall back to Wiktionary for lemmas without a card "
                         "translation (slow, rate-limited; cached afterwards)")
    args = ap.parse_args()
    build(args.limit, with_wiktionary=args.with_wiktionary)


if __name__ == "__main__":
    main()
