# interlinear/ — glossed re-typeset of a source book

Reads a book's extraction JSONL and produces a typeset PDF that
mirrors the original, with Russian (English-fallback) translations
under the load-bearing words. Design and decisions:
`research/2026-07-23-interlinear-reader-frd.md`.

## Pipeline (A→E, checkpointed artifacts)

Each step's output is a durable artifact and the *final* input of the
next step; downstream annotation is standoff (sidecar TSVs keyed to
block ids), never edits to an upstream artifact. Feedback from checks
flows back as golden anchors / rule changes, then the step re-runs.

```
A  structure.py    <book>/out/full.jsonl → <book>/<chunk>/book.md
                   + blocks.tsv (provenance) + drops.tsv
B  select_prep.py  book.md → candidates.tsv (tokens+lemma+rank+known)
   <LLM authors selection.tsv>   select_check.py validates
C  gloss_prep.py   selection.tsv → gloss_prep.tsv (dictionary hits)
   <LLM authors glosses.tsv>     critic agent (Opus) reviews;
                                 golden_check.py regression-checks
D  render.py       book.md + glosses.tsv → book.typ → book.pdf
E  validate.py     byte-check book.md vs source JSONL (squash-equal,
                   body and footnote streams separately)
   + editorial agent (Opus) reads the PDF as a learner
```

Worked chunks (both over pages 35–40, ԳԼՈՒԽ 2):

- `ghamoyan/ch2/` (2026-07-23) — v1: learner-1k depth (deck-known
  pruned), chapter-scope dedup, 114 glosses.
- `ghamoyan/ch2v2/` (2026-07-24) — v2 dense profile: deck pruning
  off, **every highlighted (bold/bold-italic) example word glossed
  with its literary form's meaning** (kind=hl; where the standard
  form isn't shown nearby, the gloss carries it as `<std>: перевод`),
  and per-source-page repeat window via `expand_anchors.py`
  (334 authored + 51 auto page-repeat anchors). hl skip policy:
  proper names, Russian-transparent loanwords (Москва/конфета class),
  bare numbers, affix mentions, and inflected forms of top-frequency
  verbs whose standard spelling sits in the adjacent parenthetical.
  v2 authors `glosses.tsv` directly (selection and glossing merged —
  the B artifact is the row set, C the lemma/ru columns); render
  consumes `glosses_expanded.tsv` via `--glosses`.

## Commands (ghamoyan ch2)

```sh
python3 structure.py    --book ghamoyan --pages 35-40 --chunk ch2
python3 validate.py     --book ghamoyan --pages 35-40 --chunk ch2
python3 select_prep.py  --book ghamoyan --chunk ch2
python3 select_check.py --book ghamoyan --chunk ch2
python3 gloss_prep.py   --book ghamoyan --chunk ch2
python3 golden_check.py --book ghamoyan --chunk ch2
python3 render.py       --book ghamoyan --chunk ch2 [--paper a5 --size 10]
```

## Conventions

- **selection.tsv** is lemma-level with a first-occurrence anchor
  (`block_id`, `surface`). Chapter-scope dedup means the gloss renders
  only at the anchor; smaller repeat windows would locate further
  occurrences mechanically via candidates.tsv (not yet implemented).
- **learner-1k depth**: deck-known lemmas (`cards/top_1000.tsv`) are
  pruned by select_check; the deck was partly built FROM ghamoyan's
  corpus, so this book's own meta-language is disproportionately
  "known" — revisit per book.
- **glosses.tsv `source`**: `kaikki` / `terms` (grammar-terms.md) /
  `prior` (LLM, no dictionary backing). Prior rows render with a
  dashed underline. A gloss is `prior` unless the *meaning* was
  verified against a source with the corrected lemma (gloss_prep +
  the targeted recheck); RU wording is authored either way.
- **Gloss wording**: keep interlinear-short (≲ 2 words + qualifier);
  long synonym stacks make ruby boxes balloon.
- **Golden anchors** (`golden/glosses_<book>_<chunk>.tsv`): every
  critic/review finding lands here (two-step rule). `golden_check.py`
  must pass before a rebuilt glosses.tsv ships.

## Review log

- 2026-07-23 Opus gloss critic: 0 wrong rows, 5 refinements
  (→ `golden/glosses_ghamoyan_ch2.tsv`).
- 2026-07-23 Opus editorial pass: real findings = prior-underline too
  faint (fixed: luma 35%, 0.6pt, offset), gloss-label overhang
  causing crowding/visual drift (fixed: ±0.4em), and uneven vertical
  rhythm (glossed lines taller than plain ones).
- 2026-07-23 constant line spacing (user request): the gloss box is
  clamped to one text line (`height: 1em, baseline: 0.25em`) so it
  never grows its line; labels overflow into the interline gap, and a
  single global `leading: 0.8em` — the slimmest that clears hanging
  labels — applies to every line. Tune `leading` together with the
  label size (0.58em) and stack spacing (0.24em) if either changes. **Caveat for future
  editorial passes**: the agent reads page bitmaps, and at 5.8pt it
  *misread* several Russian glosses as typos ("прызнак",
  "орфонический") and hallucinated stray text — verify any claimed
  typo against `pdftotext` output before "fixing" it.
- Open editorial question: gloss under a display-heading word
  (ՀԱՏԿԱՆԻՇՆԵՐԸ, p1) — kept for now (the word occurs nowhere else),
  flagged by the editorial pass as looking artifact-ish.
- 2026-07-24 Opus critic on v2 hl mappings: 0 wrong across 171 hl
  rows; 14 style fixes (redundant `= std:` prefix where the book
  shows the standard form adjacently); ալանի/անալի homonym clash and
  the մեր→մայր hl homograph became golden anchors (now 9).
- v2 layout note: adjacent glossed words in example-pair lists
  (blocks 0021/0029/0047/0051) have labels that nearly touch — the
  known cost of the dense profile at ±0.4em overhang; reduce label
  wording, not the overhang, if it bothers on paper.

## Known limitations / TODO

- **Tables**: ch2 has none; table reconstruction in structure.py is
  unimplemented — other chapters will need it (build_blocks currently
  has no table branch; a table-like page will come out as paragraphs).
- **Footnote numbering**: typst renumbers (book's ²⁵ → ¹); text and
  placement preserved.
- **Squash byte-check blind spot**: a space wrongly inserted inside a
  word is invisible to it (whitespace-insensitive); covered only by
  the golden-page eyeball and the editorial pass.
- **MWE anchors** must be contiguous in one style run; a styled or
  discontinuous phrase glosses its first part only (WARN at render).
- **Cross-page block y-ranges** in blocks.tsv are first-line-y0 →
  last-line-y1 (reading-order semantics, not a bounding box).
- **Page-window dedup** (`repeat_scope: pages`) not implemented; the
  chapter scope covers the current use.
