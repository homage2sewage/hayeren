# sakayan — extracting Sakayan's Eastern Armenian textbook

Source: **Dora Sakayan, *Eastern Armenian for the English-Speaking World:
A Contrastive Approach*, Yerevan State University Press (2007).** 558 pages,
QuarkXPress 6.5 output, version 1.6 PDF.

## What this folder does

Convert the legacy-font Armenian text in the PDF into clean Unicode and
emit two artefacts under `out/`:

- `out/full.jsonl` — one record per text span: `(page, font, size, x, y,
  text_unicode, text_raw)`. Layout-preserving, font-tagged. Use for
  programmatic queries like "give me all dialogue spans" (filter by font
  + style).
- `out/full.md` — flat reading-order render (chapter headers, vocab tables,
  prose, dialogues all merged in document order).

## How to run

The simple path — generate everything in one shot:

```sh
.venv/bin/python extract.py                # JSONL + MD for all 558 pages
.venv/bin/python build_units.py            # → units.json (11 units detected)
.venv/bin/python make_anki.py              # → out/by-unit/*.tsv + all.tsv
```

Word lookup (Wiktionary):

```sh
.venv/bin/python lookup.py գիրք            # definitions, IPA, related terms
.venv/bin/python lookup.py գրել --table    # full conjugation table (text)
.venv/bin/python lookup.py գիրք --table    # noun declension table
.venv/bin/python lookup.py գրել --json     # machine-readable
```

Per-word verifier (gloss every Armenian token in a passage, used to
sanity-check translations against Wiktionary):

```sh
.venv/bin/python glosser.py --unique "ա-ն փոխարինում է է օժանդակ բային"
echo "Բարև ձեզ։" | .venv/bin/python glosser.py
.venv/bin/python glosser.py --file ../ghamoyan/some_passage.txt
.venv/bin/python glosser.py "գրում ա" --json
```

Output is a Markdown table with each token, its lemma (after stripping
common case/article suffixes), Wiktionary gloss, and a status flag
(`✓ found`, `? multi-meaning`, `✗ not-found`). Inflected forms whose
lemma isn't easily derivable show as `not-found` — that's a feature,
not a bug: it tells you when the dictionary alone can't confirm a
translation.

Per-unit and individual scripts (for iterative work):

```sh
.venv/bin/python make_anki.py --unit 5
.venv/bin/python vocab.py --pages 30 --tag "sakayan unit1 vocab"
.venv/bin/python dialogues.py \
    --start 27:92 --end 28:455 \
    --tag "sakayan unit1 dialogue1" \
    --out out/unit1_dialogue1.tsv
.venv/bin/python paradigms.py --unit 1 --out out/unit1_paradigms.tsv
.venv/bin/python extract.py --pages 30-45,80      # ad-hoc page range
.venv/bin/python extract.py --show-unmapped       # diagnose font gaps
```

The `--start` / `--end` positions in `dialogues.py` are `page:y`
bookmarks. `units.json` carries them for every dialogue in the book.

## How the encoding works

Armenian text is rendered through `Barz-Italic` (≈339 000 chars, the
overwhelming majority), with minor amounts in `DallakTimes`, `DallakTimeBold`,
`Pedour-Regular`, `Pedour-Light`. Each font stores Armenian glyphs at
Latin/symbol codepoints — e.g. the byte `F` renders as `Հ`, `\` as `յ`, `;`
as `ե`. The mapping is in `fonts.py`.

`Armtrans` (≈124 000 chars) renders the **phonetic transliteration column**
in vocab/dialogue pages — Latin letters with combining diacritics. This is
already readable and we pass it through unchanged; the only post-processing
worth doing is normalizing precomposed forms.

## Verifying the mapping & deriving pronunciation hints

Vocab pages have a three-column structure:

```
Armenian (Barz-Italic)   Transliteration (Armtrans)   English (Times)
Fa\astane                [Hayastan]                   Armenia
'oqr                     [pŒokŒ§r]                    small
```

`phonetics.py` consumes the transliteration column for two purposes:

1. **Verification** — it reverse-maps each Sakayan token back to the
   Armenian letter that would naturally produce that sound, and aligns
   against the actual spelling. Misalignments surface mapping bugs.
2. **Pronunciation hints** — where the actual transcription substitutes
   one consonant for another from a known voiced↔voiceless/aspirated
   pair (`դ↔թ/տ`, `բ↔փ/պ`, `գ↔ք/կ`, `ձ↔ց/ծ`, `ջ↔չ/ճ`), the script
   appends `[phonetic spelling]` after the word, e.g.
   `ընդունել [ընթունել]` (the դ is pronounced as թ). Vowel glides,
   epenthetic schwas, and noise in the transcription are ignored to
   keep cards clean.

The transliteration itself is **not** included in the Anki output — it
serves only as the oracle for the two checks above.

## Status

- [x] PDF imported, fonts identified, full Barz-Italic glyph map.
- [x] `extract.py` — full book → JSONL + Markdown.
- [x] `vocab.py` — vocab tables → Anki TSV with phonetic hints, handles
      both single-column and two-column layouts plus Layout A/B (English
      below vs above).
- [x] `dialogues.py` — speaker-aware dialogue → Anki TSV.
- [x] `phonetics.py` — voiced↔aspirated deviation detector.
- [x] `english_numbers.py` — number-word → numeral normalizer.
- [x] `build_units.py` — auto-detected manifest of all 11 units.
- [x] `paradigms.py` + `paradigms_data.py` — one card per paradigm cell.
- [x] `make_anki.py` — one-step bulk extraction; **1184 cards** in
      `out/by-unit/all.tsv` (606 vocab + 290 dialogues + 86 paradigms
      + 202 chunks).
- [x] `chunks.py` — short single-sentence utterances harvested from
      dialogues, deduped, written to `out/by-unit/chunks.tsv`.
- [x] `DallakTimes` / `DallakTimeBold` / `Pedour-Regular` /
      `Pedour-Light` mapped (they share Barz-Italic's encoding).
- [x] `paradigms_data.py` covers all 10 grammar units (1-10):
      negation, imperfect, aorist, perfect/pluperfect, future,
      subjunctive, mandative I, resultative, hypothetical I, plus
      possessive adjectives.
- [x] `paradigms_data.PARTICIPLES` — non-finite forms (դերբայ) for
      8 verbs: prototypes `գրել` / `կարդալ` and irregulars
      `ունենալ`, `լինել`, `գալ`, `տեսնել`, `ուտել`, `տալ`.
- [ ] Mandative II / Hypothetical II compound paradigms (could be
      auto-generated from existing primitives).
- [ ] More irregular verbs' participle tables (անել, ասել, դնել, etc.).
