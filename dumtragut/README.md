# dumtragut — *Armenian: Modern Eastern Armenian* (Dum-Tragut 2009)

Extraction of Jasmine Dum-Tragut, **Armenian: Modern Eastern
Armenian** (London Oriental and African Language Library 14, John
Benjamins, 2009, 760 pp) — a comprehensive reference grammar with
interlinear-glossed examples (Armenian → transliteration → morpheme
gloss → free translation).

## Pipeline

`extract.py` walks the PDF span-by-span with pymupdf and applies the
font-aware glyph→Unicode remap in `armscii.py`, emitting:

    out/full[.<page-spec>].jsonl   — one record per text span
    out/full[.<page-spec>].md      — flat reading-order render

Run with any pymupdf-capable interpreter (the ghamoyan venv has it):

    ../ghamoyan/.venv/bin/python extract.py --pages 80
    ../ghamoyan/.venv/bin/python extract.py --pages 70-100
    ../ghamoyan/.venv/bin/python extract.py                 # all 760 pages
    ../ghamoyan/.venv/bin/python extract.py --show-unmapped

## The encoding problem (and why the ghamoyan table was NOT reused)

The PDF has a clean InDesign text layer. **Latin** text (English prose,
the italic transliteration, glosses) is MinionPro/MinionExp and
extracts as correct Unicode. The **Armenian** script is set in one
legacy 8-bit font, `ArialLatArm`, whose glyphs sit at WinAnsi
codepoints — every extractor reads it as Latin-1 garbage
(`î»ë³ ÙÇ Ù³ñ¹áõ` = `Տեսա մի մարդու`, "I saw a person").

`ArialLatArm`'s **letter** block (0xB2–0xFE) is standard ARMSCII-8.
Its **punctuation** block is font-specific and differs sharply from
both standard ARMSCII-8 and the ghamoyan PDF — so the ghamoyan
`armscii.py` table is wrong here on nearly every punctuation slot.
Each slot below was verified glyph-by-glyph against the rendered page
bitmaps (calibration, 2026-06-18):

| raw | ghamoyan said | this PDF | evidence |
|----:|:-------------:|:--------:|:---------|
| 0xAB | `«` | **`,`** comma | p298 `դառձա, դարձար, դարձավ` |
| 0xA3 | `՛` | **`։`** full stop | p37 `մեծ սերն է։` |
| 0xA5 | `՝` | **`(`** | p423 `(դրա համար)` |
| 0xA4 | `․` | **`)`** | p423 `(դրա համար)` |
| 0xAA | `՟` | **`՝`** mijaket | p107 `Յուրիին՝` |
| 0xA9 | `՞` | **`.`** period | p286 `կամուրջով.` |
| 0xB1 | `՞` | `՞` ✓ | p73 `ե՞ք` |
| 0xB0 | `՛` | `՛` ✓ | p70 `գի՛րքը` |
| 0xAF | `՜` | `՜` ✓ | p98 `Վահա՜ն` |
| 0x60 | `՝` | `՝` ✓ | p92 `կղզիներ՝` |

Two further font quirks, also verified and handled:

- **`0xC4` draws lowercase `ժ`**, not uppercase `Ժ` (standard ARMSCII).
  `արժենալ`, `ժամանակ`, `գիտաժողով` all render at x-height. The font
  has no distinct uppercase-Ž glyph, so a sentence-initial `Ժ` extracts
  as `ժ` (rare, accepted).
- **Expert Latin cuts** (`Minion-SemiboldExpert`, `MinionExp-Regular`)
  store glyphs in the Private Use Area: `U+F730+d` = digit `d`,
  `U+F761+n` = small-cap letter `a+n`. These carry running-head folios
  (arabic in the body, roman in the front matter), dates and
  cross-references; `remap` maps them back. (`p267` folio
  `F732 F735 F730` = `250`; front-matter `F776 F769` = `vi`.)

`self_check` (run after every extraction) reports: undecoded ≥0x80
codepoints in ArialLatArm, live counts for the TENTATIVE slots
(`0xA9→.`, `0xFF→՝` — low-frequency single-bitmap guesses), and any PUA
glyph that survived into the decoded text.

## Phonetic transcription (IPA)

The bracketed IPA (`[mɑɾtʰ]` for մարդ) is set in a family of legacy
fonts that place IPA glyphs at Latin codepoints, so pymupdf reads it as
garbage (`[mcnth]`). `phonetic.py` decodes them. Two subtleties:

- **The IPA is split across fonts.** Plain-Latin-looking IPA (m, b, d,
  t, p, k, s, l, i, u, n-nasal, …) stays in MinionPro and extracts
  correctly; only IPA-specific glyphs live in the phonetic fonts. The
  decode is therefore **font-scoped**: a `t` in `MinionPhonetic` is the
  voiced uvular **[ʁ]**, but a `t` in MinionPro is plain **[t]**. (The
  book's own chart, p17, names the two uvulars "voiced [t], voiceless
  [ó]" — i.e. raw `t`=ʁ, raw `ó`=χ.)
- Glyph→IPA verified against the rendered bitmaps (p41 segments, p65/p74
  prosody). Covers vowels ɑ ɛ ɔ ə, the uvulars χ/ʁ, ʃ ʒ ɾ ɲ ŋ ʔ, the
  combining stress acute / interrogative circumflex, and the enclitic
  undertie ‿.

Two diacritics that the text layer stores as baseline/spacing glyphs
(in the **MinionPro** layer, recovered in `phonetic.py`):

- **Aspiration ʰ.** Stored as a `h` indistinguishable by font/geometry
  from the phoneme [h]. Recovered by **position**, not font: inside an
  IPA `[...]` bracket, an `h` after a voiceless stop/affricate (p, t, k,
  ts, tʃ) is aspiration → ʰ; the phoneme [h] (Armenian հ, always a
  syllable onset) only follows vowels/sonorants/space and is left alone.
  A census over all 760 pages confirms the split has **zero
  counterexamples** and never touches English prose (`fix_aspiration`).
- A short-vowel **breve** ĭ (spacing caron U+02C7) → combining caron
  U+030C so it sits on the vowel (`iˇ` → `ǐ`).

## Known source conventions (NOT bugs, left byte-faithful)

- **Armenian full stop encoded as ASCII `:`** in the *Latin* MinionPro
  runs (e.g. `…մարդու:`). It is *not* in ArialLatArm, and the same `:`
  is a real English colon elsewhere (`Comparative:`), so it is left as
  `:` rather than risk corrupting English with a `:`→`։` rewrite. Grep
  for Armenian sentence-final `։` accordingly.
- **Transliteration ring**: the romanisation of `ռ` (ṙ) decomposes in
  the Latin layer to `r` + a spacing ring (`r°`/`r˚`). Cosmetic, in the
  transliteration tier only; the Armenian `ռ` itself is correct.

## Calibration

`calib/` holds the page bitmaps + per-page extracts used to validate
the remap, plus the tight glyph crops behind each punctuation decision.
Five human-pov review agents (pages 80/134/267/401/523) verified the
letter remap letter-for-letter; their findings drove the `ž`, PUA-figure
and punctuation fixes above.
