# explore/ — top-2000 wordlist for manual exploration

A browsing companion to the Anki deck (`cards/top_1000.tsv`): the
top-2000 corpus-frequency words as a flat table

    rank  word  en  ru  ex1  ex2

meant to be sampled at random and read on an e-reader, not drilled.

## Files

- `words.tsv` — the raw table (2000 rows + header).
- `build_wordlist.py` — regenerates the skeleton (rank/word/en and
  the pre-existing ru layer) from `frequency/out/all_lemmas.tsv`,
  reusing `frequency/build_deck.py`'s validated filters
  (personal-name skip, `SKIP_LEMMAS`, empty-gloss skip,
  `HAND_OVERRIDES` → card sources → kaikki gloss resolution). Use
  `--merge` to regenerate without losing filled ru/ex cells.
- `validate_wordlist.py` — structural lint (column shape, script
  membership, the reserved ` — ` separator, headword-presence
  warning) plus the golden-anchor check. Run after any edit to
  `words.tsv`; must be 0 errors.
- `golden.tsv` — golden gloss anchors, domain-parallel to
  `frequency/golden_glosses.tsv`: every caught-and-fixed wrong
  gloss gets a row so a regeneration can't resurrect it.
- `make_pdf.py` — randomized sample → PDF sized 1:1 for a ~10"
  e-reader (157×209 mm), 1 or 2 columns.
- `out/` — rendered PDFs (artifacts, not sources).

## Usage

```sh
# 100 random entries, 2 columns
python3 explore/make_pdf.py -n 100

# 60 entries from the rank-1000..2000 tail, 1 column, reproducible
python3 explore/make_pdf.py -n 60 --ranks 1000-2000 --columns 1 --seed 7

# validate after editing words.tsv
python3 explore/validate_wordlist.py
```

Entries print in draw order (shuffled); `--sort-rank` re-sorts the
sample by frequency rank.

## Provenance / trust levels

- **rank, word** — corpus-derived (`frequency/out/all_lemmas.tsv`,
  the four-book frequency count), filtered by the deck pipeline's
  rules. Same trust level as the deck.
- **en** — the deck's gloss resolution: corpus-derived card sources
  where available, kaikki (Wiktionary) fallback otherwise.
- **ru, ex1, ex2** — a *translation/prior layer*, same status as
  `cards/frequency/russian_glosses.tsv`: for the top-1000 the ru
  glosses come from the deck's Russian layer where it had them; the
  rest of the ru column and all example phrases were LLM-generated
  (2026-07-26, batch generation + structural validation + sampled
  critic pass). They are **not corpus-cited** — do not quote them as
  evidence for how a word is used; for citation-grade usage go
  through `frequency/query_kb.py` / the topic graph.

Example-cell format: `Armenian phrase — русский перевод`; the
` — ` (spaced em dash) is reserved for that boundary, one per cell.

## Fixing a bad row

Deck two-step rule applies: fix the cell in `words.tsv` **and** make
the same bug cheaper to catch next time (extend
`validate_wordlist.py` if the bug shape was structurally catchable;
note editorial bug classes here). `build_wordlist.py --merge`
preserves hand-fixed ru/ex cells across skeleton regeneration as
long as the word keeps its slot.
