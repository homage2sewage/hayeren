# hayeren — Armenian-language study workspace

A personal but reproducible workspace for learning Eastern Armenian
(հայերեն) from primary sources: source-text extraction, a
frequency-ranked vocabulary deck, and a citation-grounded synthesis
layer that answers questions about Armenian *with quotations
attached*, not from a model's prior.

The artefacts here come from three commitments:

1. **Read the books.** Four Armenian textbooks/grammars are extracted
   page-by-page into machine-readable JSONL with page+y-coordinates
   so every claim downstream can cite back.
2. **Card the words.** A unified top-1000-lemma Anki deck is built
   from the extracted corpus, ranked by attested frequency, with
   hand-vetted glosses for the words that matter most.
3. **Cite every claim.** A `topics/` directory holds one-Markdown-
   per-phenomenon synthesis files; every statement is anchored to a
   *literal byte string* from one of the extracted books, mechanically
   verifiable.

---

## What's in here

### Source-book extractions

Four Armenian-language books extracted to clean Unicode JSONL with
position metadata, one directory per book:

| dir          | book                                                            | pages | encoding                |
|--------------|-----------------------------------------------------------------|-------|-------------------------|
| `sakayan/`   | Sakayan, *Eastern Armenian for the English-Speaking World* (2007) | 558   | custom Barz-Italic font |
| `ghamoyan/`  | Ghamoyan et al., *Yerevan's Colloquial Language* (2014)         | 118   | ARMSCII-8               |
| `parnasyan/` | Parnasyan, Armenian-Russian textbook                            | -     | Unicode                 |
| `tioyan/`    | Tioyan, Armenian-for-Russian-speakers reference                 | -     | Unicode                 |

Each book's `extract.py` produces `out/full.jsonl` — one line per
text fragment with page number, y-range, text content, and font info.
This is the primary citation surface for everything downstream.

### Frequency deck (cards/)

- **`cards/top_1000.tsv`** — 1000 lemmas, frequency-ranked across the
  combined corpus, Anki-importable (TAB-separated, lemma + gloss +
  tags). Some lemmas carry phonetic-respelling annotations:
  `կարդալ [կարտալ]` flags lexically-conditioned voiced↔aspirated
  consonant alternation.
- **`cards/sakayan/`** — per-unit vocab/dialogue/paradigm/chunk
  slices from the textbook (~1450 cards).
- **`cards/ghamoyan/`** — colloquial fillers and discourse markers.

### Synthesis: the topic graph (topics/)

27 Markdown files (and growing), each covering one linguistic
phenomenon: phonology, morphology, syntax, lexicon, pragmatics.
Every file has YAML frontmatter listing its sources with
`verbatim_quote` arrays that must match the cited JSONL byte-for-byte
(verified by `.claude/skills/citation-check/`).

Browse-worthy starting points:

- `topics/phonology/three_way_laryngeal_contrast.md` — the voiced /
  voiceless-unaspirated / voiceless-aspirated system (Eastern
  Armenian's signature feature).
- `topics/phonology/epenthetic_schwa.md` — why `Մկրտչյան` is
  pronounceable even though it looks like four consonants.
- `topics/syntax/dative_experiencer.md` — psych-verb construction
  (`դուր է գալիս` "it pleases me"), including the
  `դուր/դուրս/դուռ` near-homograph trap.
- `topics/lexicon/code_switching_with_russian.md` — Yerevan-colloquial
  Russian borrowing patterns (`տոչկեն`, `սվարկա`, `կառոչի`).
- `topics/lexicon/yerevan_slang.md` — informal vocabulary.

### Reference / theory docs (top level)

| file                                | content                                                                   |
|-------------------------------------|---------------------------------------------------------------------------|
| `INDEX.md`                          | full directory layout + cross-project facts (font encodings, OCR caveats) |
| `armenian-grammar.md`               | phonology, pronouns, verb classes, paradigms                              |
| `grammar-terms.md`                  | English/Armenian/Russian grammar-term glossary                            |
| `transliteration-notes.md`          | Latin transliteration: conventions + the `ches asem` trap                 |
| `cyrillic-transliteration-notes.md` | Russian-Cyrillic conventions (popular vs textbook-phonetic)               |
| `frequency-lists.md`                | core-vocabulary theory + Armenian sources + methodology                   |
| `anki-design.md`                    | card-design decisions with research citations + request log               |
| `kb-design.md`                      | KB schema + topic-graph design (living doc)                               |

### Operational layer

- `frequency/` — frequency-list construction, Hermitdave comparison,
  the dictionary lookup that powers gloss selection.
- `errors/` — append-only structured log of LLM-failure cases caught
  during the workspace's construction (each one explains what went
  wrong, the root cause, and the mitigation that landed).
- `research/` — dated investigation notes, including the
  citation-pipeline roadmap.
- `walks/` — dated "walk through book X looking for phenomenon Y"
  notes.
- `llm-workflow.md` — methodology for catching bad heuristics before
  they ship (the workspace's accumulated lessons about working with
  LLMs).

---

## Using it as a human

### Look something up

The fastest path from "I have an Armenian word" to "here are the
citations":

```sh
python3 frequency/query_kb.py "<armenian text or phrase>"
```

This tokenizes + lemmatizes the input, greps `topics/`, the four book
JSONLs, and the project notes, then emits a Markdown bundle with
matched-topic excerpts, book passages (with page + y-range), and an
explicit *Gaps* section listing query-lemmas with no coverage.

### Use the deck

`cards/top_1000.tsv` imports into Anki directly: **File → Import →**
select the TSV → **Fields separated by: Tab** → field 1 is Front,
field 2 is Back, field 3 is Tags. Bracketed phonetic respellings
(`կարդալ [կարտալ]`) stay in the Front field so you see them while
reviewing.

### Search the source corpus directly

```sh
grep -nE "<armenian-word>" {sakayan,ghamoyan,parnasyan,tioyan}/out/full.jsonl
```

Every match gives you book + page + y-range, which is exactly what
the topic-graph citations encode.

### Browse the topic graph

`topics/` is organized by linguistic domain (`phonology/`,
`morphology/`, `syntax/`, `lexicon/`, `pragmatics/`). Each file is
self-contained and cross-references siblings. If you don't know
where to start, `INDEX.md` has a curated reading-path section.

---

## Rebuilding from scratch

Each source-book directory and the `frequency/` and `sakayan/`
directories carry their own Python venv and `README.md`. Typical
flow:

```sh
# extract a book
cd sakayan && .venv/bin/python extract.py        # → out/full.jsonl

# build the deck
cd frequency && .venv/bin/python build_deck.py   # → ../cards/top_1000.tsv

# verify a topic file's citations
.claude/skills/citation-check/check.py topics/phonology/epenthetic_schwa.md
```

System dependencies: `poppler-utils` (pdftotext, pdffonts, pdftoppm),
Python 3.10+. `tesseract-ocr-hye` is a fallback for the few cases the
embedded-font extraction can't handle.

---

## AI-collaboration angle

This workspace was built in conversation with Claude. Two pieces of
that collaboration are durable and committed:

1. **`.claude/skills/`** — five reusable skills the assistant invokes:
   - `citation-check` — verifies `verbatim_quote` strings appear in
     the cited JSONL byte-for-byte
   - `critic-pass` — schema-lint + editorial review of topic files
   - `challenge-rule` — protocol for validating any new
     heuristic/priority/filter rule against its input population
     before it ships
   - `answer-q` — citation-grounded answering for Armenian questions
   - `error-log` — index-builder for the `errors/` directory

2. **Workflow documentation** — `CLAUDE.md` (project-root rules),
   `llm-workflow.md` (the doctrine: heuristic validation, critic-
   agent pattern, two-framings review), `errors/` (concrete cases
   where the doctrine was earned through failure).

3. **Hook-enforced KB grounding** — `.claude/hooks/armenian_autoground.py`
   is a `UserPromptSubmit` hook (registered in `.claude/settings.json`)
   that detects Armenian in the user's prompt and auto-runs
   `query_kb.py`, injecting the bundle into context *before* the
   model answers. Turns the "grep KB first" rule from suggestion
   into invariant. Prefix any prompt with `#nogrep` to suppress.

The same skills + docs work for any LLM that can read Markdown and
run Python — they're not Claude-specific in implementation. The hook
mechanism is specific to Claude Code's hook protocol, but the
underlying `query_kb.py` is a plain CLI script invokable from
anywhere.

---

## Status

- **Source extraction**: 4 books extracted, full JSONL committed.
- **Topic graph**: 27 topics across 5 domains, all citation-verified.
- **Deck**: top-1000 deck stable; sakayan per-unit slices complete;
  ghamoyan + frequency-gap supplements landed.
- **Errors log**: 9 entries documenting LLM failure modes
  (POS-priority misranks, hallucinated extrapolations, slang
  divergence, bare-lemma cards) with their structural mitigations.
- **Citation-grounded answer pipeline**: Phase 1-3 landed
  (`query_kb.py` + `answer-q` skill + post-answer verifier). Phases
  4-5 (slash-command wiring, MCP server, embedding retrieval) are
  scoped in `research/2026-05-09-answer-pipeline-roadmap.md`.

---

## Licence + sources

Source PDFs are excluded from the repo (see `.gitignore`). The four
books are cited as primary sources; extracted text quotes are short
and used for linguistic analysis. Project code, topic files, and
notes: see repository licence (if added; ask before redistributing
extracted text in bulk).
