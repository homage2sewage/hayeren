# cards/ — current Anki-importable card sets

Single source of truth for card output. Anything here is meant to be
imported into Anki; everything else (extraction artifacts, frequency
analysis, validation reports) stays in the per-project `out/`
directories.

## Layout

```
cards/
├── top_1000.tsv                ⭐ unified frequency-ranked deck
│                                ~1000 cards, lemmas ranked by occurrence
│                                in our combined corpus; translations
│                                pulled from sakayan vocab, ghamoyan
│                                fillers, frequency gap-additions, and
│                                Wiktionary fallback
├── sakayan/                     607 vocab + 290 dialogue + 354 paradigm + 202 chunk
│   ├── all.tsv                  combined sakayan deck (1453 cards)
│   ├── unit01_vocab.tsv         per-unit slices
│   ├── unit01_dialogue1.tsv
│   ├── …
│   ├── paradigms.tsv            verb/declension paradigms (354 cards)
│   └── chunks.tsv               short reusable phrases from dialogues (202)
├── ghamoyan/
│   └── fillers.tsv              colloquial filler / discourse markers (32)
└── frequency/
    └── gap_additions.tsv        16 high-frequency words missing from sakayan
                                 (identified via comparison with
                                  Hermitdave OpenSubtitles list)
```

## Which file should you import?

Two natural workflows:

1. **Frequency-first** — import `top_1000.tsv` and study highest-frequency
   words first. Each card has a `rank-NNNN` tag so you can order or
   filter by rank tier in Anki. This is the most efficient if you want
   broad-coverage recognition fast.
2. **Source-first** — import `sakayan/all.tsv` (textbook progression),
   `ghamoyan/fillers.tsv` (colloquial register), and
   `frequency/gap_additions.tsv` (curated supplements) as separate
   decks. Works better if you're following Sakayan unit-by-unit and
   want the textbook's pedagogical sequence.

## Caveats for `top_1000.tsv`

- The corpus is small and textbook-biased (~3.4K tokens from Sakayan +
  Ghamoyan), so the top-1000 lemmas reflect *what's in our books*, not
  the broad Armenian language. Compare against `frequency/out/comparison_report.md`
  for the diff against the OpenSubtitles-derived Hermitdave list — that
  shows what the textbook is missing.
- About 50% of cards have translations from existing card sources; the
  rest depend on Wiktionary fallback (English-only, definitions of
  varying length). Wiktionary entries for short particles often miss
  the colloquial sense (e.g., `ա` as 3sg copula) — see
  `armenian-grammar.md` for the linguistic context.
- Some entries will have empty translations where neither card-source
  nor Wiktionary covered them. These need manual fill.

## Schema for `top_1000.tsv`

```
Armenian \t  English / Russian (where available)  \t  tags
```

Tags include `frequency top-1000 rank-NNNN src-<origin>` where
`<origin>` is one of:

- `sakayan-vocab` — translation taken from a Sakayan vocab card
- `ghamoyan-filler` — taken from a Ghamoyan filler card (en + ru)
- `frequency-gap` — taken from a hand-curated gap-addition (en + ru)
- `sakayan-paradigm` — verb infinitive's English from `paradigms_data.py`
- `wiktionary` — first definition(s) from English Wiktionary
- `—` (em dash) — no translation found; needs manual fill

Cards from `ghamoyan-filler`, `frequency-gap`, and (some) hand-curated
sources have English/Russian combined; others are English-only.

## Card schemas (varies by source)

Single-language schema (most sakayan files):

```
Armenian \t  English  \t  Tags
```

3-column with speaker (sakayan dialogues):

```
Speaker \t  Armenian  \t  English  \t  Tags
```

3-column with combined translations (ghamoyan fillers, frequency gaps):

```
Armenian \t  English / Russian  \t  Tags
```

The combined-language schema for fillers and frequency gaps is
deliberate — see `../anki-design.md` for the rationale (English and
Russian translations for filler/discourse-marker words often
disambiguate each other faster than either alone).

## Anki import

AnkiDroid: File → Import → set delimiter to Tab → set Field 1 =
Armenian, then map remaining fields per schema, then map last column
to Tags. The Anki note type needs:

- 2 fields (Armenian / English) for plain sakayan cards
- 3 fields (Speaker / Armenian / English) for dialogue cards
- 2 fields (Armenian / Translations) for ghamoyan fillers and frequency gaps

`all.tsv` in the sakayan subfolder is a concatenated import — vocab,
dialogue (with speaker prefixed onto Armenian field), paradigms, and
chunks all in one file. Convenient for a one-shot deck setup.

## How these are regenerated

| File / set | Built by |
|------------|----------|
| `top_1000.tsv` | `../frequency/build_deck.py [--with-wiktionary]` |
| `sakayan/unit*_*.tsv`, `paradigms.tsv`, `chunks.tsv`, `all.tsv` | `../sakayan/make_anki.py` |
| `ghamoyan/fillers.tsv` | hand-curated; see `../ghamoyan/ch4-pleonasms.md` |
| `frequency/gap_additions.tsv` | hand-curated from `../frequency/out/comparison_report.md` |
