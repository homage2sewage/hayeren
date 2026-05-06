---
name: citation-check
description: |
  Verify every `verbatim_quote` in a topic file's `sources:` frontmatter
  actually appears at the cited (page, y_range) in the corresponding
  book's extracted JSONL. Use after writing or editing any topic file
  under `topics/`, or when a topic-walk proposes new sources.
---

# citation-check

Mechanically verifies the `sources:` block of a topic file by stitching
the relevant `full.jsonl` spans and substring-matching each declared
verbatim quote. Catches hallucinated citations, typo'd page numbers,
and y_range windows that miss their target.

The schema this skill enforces is defined in `kb-design.md` § "Topic
frontmatter schema."

## When to invoke

- Right after writing or editing `topics/<domain>/<phenomenon>.md`.
- After a `topic-walk` / `discovery-walk` proposes new sources.
- Before promoting a topic from `status: draft` to `reviewed`.
- As a critic gate during the `critic-pass` skill (when that lands).

## How to invoke

```sh
sakayan/.venv/bin/python .claude/skills/citation-check/check.py \
    topics/<domain>/<phenomenon>.md
```

Add `--json` for machine-readable output when chaining to other skills.

Exit code 0 iff every fragment verifies, else 1.

## What it does, step by step

1. Parses the YAML frontmatter of the topic file.
2. For each entry in `sources:`, resolves `book:` to a JSONL path —
   tries `books/<name>/out/full.jsonl` first (future layout), falls
   back to the legacy top-level `<name>/out/full.jsonl`.
3. Selects spans where `page == source.page` and `bbox[1]` falls in
   `source.y_range`.
4. Stitches the selected spans' `text` fields with single-space
   separators and NFC-normalises (Armenian script + Armtrans
   diacritics can be NFC/NFD-mixed).
5. For each fragment in `verbatim_quote` (treats a string as a
   single-element list), substring-matches against the stitched
   text.

## Reading the output

Pass example:

```
topics/phonology/voiced_aspirated_alternation.md: 11/11 verbatim fragments verified

  [OK  ] src#1 sakayan p18 y=[300, 320]  'The EA three-part consonant system...'
  ...
```

Fail example:

```
  [FAIL] src#3 sakayan p36 y=[110, 115]  'kart'
          region had 0 spans containing no match; widening y to ±30pt yields 8 spans
```

Reading the diagnostic:

- **"region had 0 spans"** — page exists but y_range is wrong or far
  off. Widen the y_range, or verify the page number.
- **"widening … yields N spans" (N > 0)** — the y_range is too narrow.
  Look at the wider region (e.g. via the JSONL directly) and pick a
  better range.
- **"region had K spans containing no match"** — the spans exist but
  the fragment isn't in the stitched text. Either the quote is wrong,
  or the fragment crosses a span boundary in a way that needs to be
  split (use the fragment-list form of `verbatim_quote`).

## Schema reminder

```yaml
sources:
  - id: 1
    book: sakayan
    page: 18
    y_range: [300, 320]
    verbatim_quote: "The EA three-part consonant system consists of one voiced stop"
    supports: supported
    note: prose statement of the three-way distinction.
  - id: 2
    book: sakayan
    page: 30
    y_range: [520, 540]
    verbatim_quote: ["ընդունել", "§nt", "unel]"]    # fragment list
    supports: partially-supported
    note: vocab line; nt^h transliteration witnesses դ→թ.
```

Use the **fragment-list** form whenever the cited text crosses span
boundaries that this script can't undo — most commonly Sakayan's
Armtrans transliterations where a diacritic on a consonant splits
the run (e.g. `[§ntʰunel]` lives as `[§nt` + `unel]`).

## Limitations

- **Whitespace-sensitive.** The stitched haystack uses single-space
  joins; quotes that include tab/newline structure may fail. Split
  into fragments to work around.
- **No fuzzy match.** The fragment must appear exactly (after NFC
  normalisation) in the haystack. Spelling drift between editions
  would need a different tool.
- **One book per source entry.** Multi-book composite citations need
  to be split into separate `sources:` entries.
- **Project-root resolution** walks up from the script's location
  looking for `kb-design.md` — moving the script outside this
  project will break it (intentional; it's project-local tooling).

## Dependencies

`pyyaml`, installed in `sakayan/.venv`. As `books/` grows, consider
hoisting a project-wide venv at the hayeren root and migrating this
skill to use it.
