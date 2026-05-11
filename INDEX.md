# hayeren / Հայերեն — Armenian learning workspace

Personal workspace for studying Armenian. Mix of source-text extraction,
vocabulary tooling, and study notes. Sibling projects live in their own
subdirectories — keep top level limited to this index and shared assets.

> **Publishing note.** This workspace may be made public in the future.
> Files in this tree must not reference other `~/work/<project>`
> directories, personal repos, or private notes; cite only public sources.
> Applies to all docs, topics, walks, and skill files.

## Layout convention

```
~/work/hayeren/
├── INDEX.md                       # this file
├── kb-design.md                   # multi-book KB + agent-workflow design (living)
├── armenian-vocab-research.md     # research base: SRS, chunks, frequency
├── armenian-grammar.md            # linguistic notes: phonology, pronouns, verbs (to be split into topics/)
├── grammar-terms.md               # English/Armenian/Russian grammar-term glossary
├── transliteration-notes.md       # Latin transliteration of Armenian: conventions + pitfalls (incl. the `ches asem` trap)
├── cyrillic-transliteration-notes.md  # Russian-Cyrillic transliteration: popular orthographic vs textbook phonetic conventions
├── frequency-lists.md             # core-vocabulary theory + Armenian sources + methodology
├── anki-design.md                 # card design decisions + request log
├── llm-workflow.md                # LLM-assisted-coding hygiene: how to catch bad heuristics before they ship
├── errors/                        # structured LLM-failure log (append-only, indexed)
│   ├── README.md                  # schema + tiered logging rule + categories
│   ├── INDEX.md                   # auto-generated chronological index
│   ├── BY-CATEGORY.md             # auto-generated grouped index
│   └── YYYY-MM-DD-NNN-*.md        # one error per file
├── sakayan/                       # extract Eastern-Armenian textbook (Sakayan 2007)
│   ├── README.md
│   ├── dora_sahakyan.pdf
│   ├── extract.py / fonts.py
│   ├── vocab.py / dialogues.py / paradigms.py
│   ├── phonetics.py / english_numbers.py
│   ├── paradigms_data.py
│   ├── lookup.py / glosser.py     # Wiktionary lookup; per-word verifier
│   ├── .venv/
│   └── out/
├── ghamoyan/                      # Ghamoyan et al., *Yerevan's Colloquial Language* (2014)
│   ├── README.md
│   ├── erewani_khosaktsakan_lezown.pdf
│   ├── armscii.py                 # standard ARMSCII-8 decoder + 2 PDF-specific overrides
│   ├── extract.py
│   ├── .venv/
│   └── out/
├── frequency/                     # core-vocabulary list construction + Hermitdave compare
│   ├── README.md
│   ├── build_ours.py / compare.py
│   └── out/                       # our_top_1000.tsv, comparison_report.md, …
├── cards/                         # ⭐ Anki-importable TSVs — current variants live here
│   ├── README.md
│   ├── top_1000.tsv               # unified frequency-ranked top-1000 deck
│   ├── sakayan/                   # vocab / dialogue / paradigm / chunk TSVs + all.tsv
│   ├── ghamoyan/fillers.tsv
│   └── frequency/gap_additions.tsv
├── topics/                        # synthesis layer — one MD per linguistic phenomenon
│   ├── phonology/                 # voiced-aspirated alternation, schwa, laryngeal contrast, …
│   ├── morphology/                # verb classes, aorist, perfect, articles, negation, …
│   ├── syntax/                    # pro-drop, dative-experiencer, …
│   ├── lexicon/                   # code-switching, slang, idioms, expressives
│   └── pragmatics/                # intimate register
├── walks/                         # dated "walk through book X for phenomenon Y" notes
├── research/                      # dated investigation notes
│   └── 2026-05-09-answer-pipeline-roadmap.md   # ⭐ current status of the citation-grounded answer pipeline (Phases 1-5+)
└── (future siblings: anki/, dictionary/, lexicon/, ...)
```

Four reading paths into this workspace:

- **Linguistic facts** — `armenian-grammar.md`. Phonology, pronouns,
  verb classes, irregular paradigms. The "why" behind the cards. Will
  be split into per-phenomenon files under `topics/` (see `kb-design.md`).
- **Card design** — `anki-design.md`. What every choice in the TSV
  output reflects, with research citations. Includes a request log so
  past decisions are traceable.
- **Multi-book KB + agent workflow** — `kb-design.md`. Living design
  doc: storage shape, topic-frontmatter schema with verbatim-quote
  citations, walk skills (topic / discovery / gap), CitationAgent +
  critic verifier passes. Read before any work that touches `topics/`,
  `walks/`, `research/`, or `.claude/skills/`.
- **Tooling** — `sakayan/README.md` plus this file's "cross-project
  facts" below.

Each subdirectory owns its own venv, data, and notes. The top-level INDEX
points at them and records cross-cutting facts (fonts, encoding, transliteration
schemes) that are likely to be reused.

## Active projects

- **sakayan/** — extract clean Unicode Armenian from Dora Sakayan,
  *Eastern Armenian for the English-Speaking World* (Yerevan State University
  Press, 2007, 558 pp), produce per-unit Anki TSVs (vocab + dialogues +
  paradigms). See `sakayan/README.md`.
- **ghamoyan/** — Ghamoyan, Sargsyan & Kartashyan, *Yerevan's Colloquial
  Language* (2014, 118 pp). Linguistic study of spoken Yerevan Armenian
  vs literary norm — phonology, lexicon, morphology, syntax, style.
  Tools verified; content-mining deferred. See `ghamoyan/README.md`.
- **frequency/** — core-vocabulary frequency list built from Sakayan
  + Ghamoyan extraction, compared against Hermitdave's
  OpenSubtitles-derived public list. Theory in `frequency-lists.md`,
  build/compare scripts and outputs in `frequency/`.

## Cross-project facts

### The legacy-font Armenian encoding problem

Most pre-Unicode Armenian publications (and many post-2000 ones from
QuarkXPress workflows) ship Armenian text as Latin/symbol codepoints
rendered through a custom-encoded font. `pdftotext` returns the raw
codepoints — readable as gibberish like `Fa\astane` for Հայաստան. To
recover Unicode you need a per-font glyph→Armenian mapping table.

Reusable knowledge:

- **Identify Armenian fonts via `pdffonts <file>`** — they show
  `encoding: Custom` and `uni: no`. Names typical of legacy Armenian
  fonts: *Arasan*, *Aramian*, *Sylfaen* variants, *Barz*, *DallakTimes*,
  *Pedour*, *Nork*, *Armtrans*, *Mashtots*, *Mariam*. (Note: *Armtrans*
  is for **transliteration** — Latin glyphs with diacritics — not Armenian.)
- **Different fonts in the same document often share a base mapping**
  (the keyboard-layout-to-Armenian convention) but disagree on a handful
  of punctuation/decorative codes. Build one base map, then patch outliers.
- **Vocab pages with phonetic transliteration are a free oracle** — auto-
  transliterate the script's Unicode output and diff against the bracketed
  column to validate the mapping.
- **Tooling**: prefer `pymupdf` (`fitz`) over `pdfplumber` for per-character
  font info; `page.get_text("dict")` returns spans grouped by font and
  reading order. Fallback path is OCR with `tesseract -l hye` (apt:
  `tesseract-ocr-hye`) — slow, format-lossy, but bypasses the encoding.

### ARMSCII-8 — standard, widespread, easy to decode

A second class of legacy Armenian PDFs (notably the 2014
Ghamoyan/Sargsyan/Kartashyan book) uses **ARMSCII-8** (Armenian
Standard Code for Information Interchange, 8-bit) — a real, documented
single-byte encoding. The PDF declares the font as WinAnsi; the bytes
0xA1-0xFE are then mis-extracted as Latin-1 glyphs (`0xB3` displays as
`³` instead of `ա`).

Decoding is one Unicode lookup table — see `ghamoyan/armscii.py` for
the standard mapping. PDFs may add 1-3 file-specific overrides where
the embedded font's ToUnicode CMap is quirky (this PDF maps Greek `μ`
to Armenian `բ`, and `¨` to the ev-ligature `և`).

Compared to Sakayan-style custom fonts:

|                        | Sakayan (Barz-Italic etc.) | ARMSCII-8 (this book) |
|------------------------|----------------------------|-----------------------|
| Encoding standard?     | Custom per-document        | Documented standard   |
| Mapping derivation     | Empirical (vocab+translit) | Lookup table          |
| Decoding effort        | Hours per font family      | Minutes               |

When you encounter a new Armenian PDF, **try ARMSCII-8 decoding first**
— a 5-line script test on a Latin-1-misencoded sample will tell you in
seconds whether it's ARMSCII-8 or a custom font scheme.

### Code-switching and Latin-transliterated Armenian

Two phenomena that pervade real Armenian usage and break naive tooling
(machine translation, PDF extraction heuristics, search heuristics):

- **Armenian–Russian code-switching** at high rate in casual Yerevan
  speech: Russian lexical items embedded inside Armenian morphology
  (`տոչկեն`, `սվարկա`, `ռազբիրատ`, `լիշնի`). These are neither pure
  Armenian nor pure Russian. Auto-translators usually pick one side
  and silently drop or misinterpret the other.
- **Informal Latin transliteration** of Armenian (in chat / SMS /
  social media). No standard scheme; common conventions are loose
  and often phonetic-not-orthographic, so colloquial register gets
  baked into the spelling. Auto-translators usually fail to recognize
  it as Armenian at all. **Common trap**: even careful manual
  transliteration can produce grammatically broken Armenian if the
  back-mapping isn't checked.

See `ghamoyan/README.md` (topic 0) for examples and the worked-through
illustration of how this trips up casual writing.

### Key tools to keep in mind

- `pdffonts`, `pdftotext`, `pdftoppm` (poppler) — system tools, no install.
- `pymupdf` — Python library, per-char font/size/position. Per-project venv.
- `tesseract-ocr-hye` — OCR fallback, not yet installed.

