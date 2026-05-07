# frequency — core vocabulary list construction

Builds a top-N lemma frequency list from our extracted Sakayan +
Ghamoyan material, and compares it against the public
Hermitdave/OpenSubtitles Armenian frequency list.

See `../frequency-lists.md` for the theoretical basis and methodology
choices.

## Status

- [x] Theory documented (`../frequency-lists.md`).
- [x] `build_ours.py` — aggregate + tokenize + lemmatize + rank.
- [x] `compare.py` — fetch + lemmatize Hermitdave list + diff report.
- [x] First run: 997 distinct lemmas in ours; 360 agree with
      Hermitdave's top-1000 (~36% agreement); 16+ genuine gaps
      identified for deck improvement (see `out/comparison_report.md`).

## Layout

```
frequency/
├── README.md                  this file
├── build_ours.py              builds out/our_top_1000.tsv
├── compare.py                 builds out/comparison_report.md
└── out/
    ├── our_top_1000.tsv       rank | lemma | count | sources
    ├── all_lemmas.tsv         every lemma we found, ranked
    ├── build_stats.txt        per-source token/lemma counts + Zipf check
    ├── hermitdave_hy_full.txt cached external reference (6874 entries)
    └── comparison_report.md   bucket diff + analysis
```

## How to run

No venv required — standard library only. Both scripts read TSV files
from `../sakayan/out/by-unit/` and `../ghamoyan/out/`.

```sh
# 1. build our list
python3 build_ours.py

# 2. fetch Hermitdave reference (one-time, cached)
curl -sL https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/hy/hy_full.txt \
     -o out/hermitdave_hy_full.txt

# 3. produce comparison report
python3 compare.py
```

## What's in the comparison report

Three buckets:

1. **Agreed** (in both top-1000s) — strong consensus, the core that
   any deck should have.
2. **We cover, frequency doesn't** — textbook-introductory vocab,
   register-marked items (fillers, slang), grammatical paradigm cells.
   Items in our deck that wouldn't surface from a frequency list.
3. **Frequency covers, we don't** — high-frequency Armenian missing
   from our deck. Most actionable for deck improvement.

Plus an analysis section noting:

- Subtitle-corpus bias in Hermitdave (proper nouns from Shakespeare
  translations dominate their head: `ռոմեո, ջուլիետ, մակբեթ`…).
- Tokenization-quirk artifacts (Armenian intra-word punctuation
  splitting words; both lists affected).
- Hand-curated "real gaps" list — ~16 high-frequency conversational
  Armenian words missing from our deck (`հա, մեզ, ամեն, գիշեր, կյանք,
  սեր, գործ, հենց, ողջ, ապա, մահ, ժամանակ`…).

## Limitations

- Our corpus is small (~3.3K tokens), heavily textbook-biased. The
  "top 1000" is essentially our entire deduplicated lemma set.
- Lemmatizer is rule-based suffix-strip + paradigm-cell inflection
  map. Accuracy ~85-90% at the head, degrades in the long tail.
  Edge cases visible in `out/comparison_report.md` analysis section.
- Hermitdave's source is OpenSubtitles 2018 — heavy on
  Shakespeare-translation movies, so proper-noun bias at the top.
- No cross-check against EANC (Eastern Armenian National Corpus) —
  would be the academic-quality reference but requires scraping.

## Next-step candidates (deferred)

- Add the 16 hand-curated gap entries to a new `out/deck_additions.tsv`
  with English + Russian glosses, ready for Anki import.
- Improve lemmatizer: extend SUFFIXES with `-ի` patterns missing for
  some forms (e.g. `քանզի, որքան, որտեղ` getting truncated).
- Add EANC as a second reference once scraping infrastructure exists.
- Extend our corpus by mining Ghamoyan Ch 3 (slang) and Hավելված 1-3
  appendices (likely conversation transcripts).
