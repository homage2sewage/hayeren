# frequency — core vocabulary list construction

Builds a top-N lemma frequency list from our extracted Sakayan +
Ghamoyan material, and compares it against the public
Hermitdave/OpenSubtitles Armenian frequency list.

See `../frequency-lists.md` for the theoretical basis and methodology
choices.

## Status

- [x] Theory documented (`../frequency-lists.md`).
- [x] `build_ours.py` — aggregate + tokenize + lemmatize + rank, with
      MWU merging (`մի քիչ` → `մի_քիչ`) and dictionary-aware suffix
      stripping that prefers the strip yielding a known headword.
- [x] `compare.py` — fetch + lemmatize Hermitdave list + diff report.
- [x] `validate_lemmas.py` — Wiktionary-based per-lemma sanity check.
- [x] `build_dictionary.py` + `data/armenian_dict.tsv` — one-time
      compaction of the kaikki.org Armenian Wiktionary dump
      (~22K entries → 1.3 MB TSV). Replaces live Wiktionary API
      calls (which got rate-limited).
- [x] `dictionary.py` — offline lookup module with noise-gloss
      filtering (alphabet-letter descriptions, paradigm-cell prose
      like "dative singular of X").
- [x] `build_deck.py` — emit unified top-1000 deck at
      `../cards/top_1000.tsv` with translations pulled from existing
      card sources, then the local dictionary as fallback. No
      network calls.
- [x] `validate_deck.py` — Phase 1 mechanical-lint pass. Categories:
      `empty-translation`, `noise-translation`, `false-friend`,
      `truncated-lemma`, `inflected-leak`, `paradigm-leak`,
      `proper-noun-foreign`, `mwu-leak`, `duplicate-translation`,
      `eu-ligature`. See `walks/2026-05-07-deck-validation-plan.md`.
- [x] 360 of our top-1000 agree with Hermitdave's top-1000; 16 high-
      frequency gap-words written to `../cards/frequency/gap_additions.tsv`.

## Lemmatization rules — what we fixed

The lemmatizer is rule-based suffix-stripping plus a paradigm-cell
inflected→infinitive map. Two kinds of bugs caught by the validation
pass and fixed:

- **`-ն` and `-ս` over-stripped.** They're a definite-article
  suffix only on vowel-final stems and rarely correct in casual
  writing — far more often part of the lemma itself (`հայերեն,
  հայկական, ամեն, այսպես, անուն`). Removed from the strip list.
  Slight under-aggregation of 1sg-possessive forms (`անունս` "my
  name" vs `անուն` "name") is the right tradeoff.
- **Stem-change nouns** (`սեր` → `սիր-` in oblique cases): hand-pinned
  `սիրով → սեր`, etc. in `collect_inflected_to_lemma`.

## Layout

```
frequency/
├── README.md                  this file
├── build_ours.py              builds out/our_top_1000.tsv
├── compare.py                 builds out/comparison_report.md
├── validate_lemmas.py         Wiktionary sanity-check on top-N lemmas
├── build_deck.py              builds ../cards/top_1000.tsv (unified deck)
├── build_dictionary.py        compacts data/armenian.jsonl → TSV
├── dictionary.py              offline lookup module (kaikki.org dump)
├── validate_deck.py           mechanical-lint pass on cards/top_1000.tsv
├── data/
│   ├── armenian.jsonl         kaikki.org dump (212 MB, gitignored)
│   └── armenian_dict.tsv      compacted lookup TSV (~1.3 MB)
└── out/
    ├── our_top_1000.tsv       rank | lemma | count | sources
    ├── all_lemmas.tsv         every lemma we found, ranked
    ├── build_stats.txt        per-source token/lemma counts + Zipf check
    ├── hermitdave_hy_full.txt cached external reference (6874 entries)
    ├── comparison_report.md   bucket diff + analysis
    ├── lemma_validation.tsv   per-lemma Wiktionary status (top-N)
    ├── lemma_validation.md    summary breakdown: valid / not-found / suspicious
    ├── deck_validation.tsv    one row per finding (severity, rank, …)
    └── deck_validation.md     grouped human summary
```

## How to run

No venv required — standard library only. Scripts read TSV files
from `../cards/sakayan/` and `../cards/ghamoyan/`.

```sh
# 0. one-time: download + compact the Wiktionary dump
curl -sL https://kaikki.org/dictionary/Armenian/kaikki.org-dictionary-Armenian.jsonl \
     -o data/armenian.jsonl
python3 build_dictionary.py

# 1. build our list
python3 build_ours.py

# 2. fetch Hermitdave reference (one-time, cached)
curl -sL https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/hy/hy_full.txt \
     -o out/hermitdave_hy_full.txt

# 3. produce comparison report
python3 compare.py

# 4. build the unified deck and validate it
python3 build_deck.py
python3 validate_deck.py
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
