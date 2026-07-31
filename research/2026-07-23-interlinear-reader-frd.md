# FRD: Interlinear reader — glossed re-typeset of a source book

Date: 2026-07-23. Status: **draft — awaiting sign-off**.
First target: ghamoyan (Երևանի խոսակցական լեզուն), generalizable to any
book with a `<book>/out/full.jsonl` extraction.

## Goal

Read a book from its extraction JSONL and produce an *almost identical*
typeset document (PDF) in which selected words carry a small translation
directly beneath them. A reading aid for a learner: the page looks like
the original book, but the hard words are pre-glossed.

## Original request (2026-07-23)

As stated, before design decisions:

1. Preserve the original's formatting: bold, cursive, tables.
2. Translations in dictionary form — the words must be lemmatized.
3. Translate only the load-bearing words, the ones crucial for
   understanding the sentence.
   3a. A **depth** setting — e.g. translate only less common words.
4. Never repeat the translation of the same word.
   4a. A setting for this too — e.g. repeat after 3 pages, or in the
   next chapter.
   4b. No tracking beyond chapters; books without chapters default to
   some number of pages.

Architectural constraints from the request:

- Separated parts: A read/chunk (full chapter or N pages, no hanging
  sentences) → B select words → C lemmatize/translate/context-check →
  D build output → optional E validate against input.
- **Each step's artifact is final input to the next; changing step N
  never re-executes or re-adjusts earlier outputs** — a consistency
  principle, not just performance: when looking back, look at the
  source, and if a step's results are bad, redesign the step.
- A produces readable markdown (bold, cursive, tables, footnotes).
- B/C annotations are non-destructive tags: "this word was selected,
  here's the dictionary form, here's the translation."
- C → D is mechanical, like an intermediate assembler — output format
  and page size changeable there.
- E is a human or unbiased-agent point of view.

## Existing assets (repo survey, 2026-07-23)

- **Extractions:** every book has `<book>/out/full.jsonl` with
  span-level records: `page, font, size, bbox, text_raw, text`.
  Bold/italic are recoverable from font names — ghamoyan carries
  `ArialArmenianBold` (609), `ArialArmenianItalic` (954),
  `ArialArmenianBoldItalic` (1358) spans; body text is 9pt (~10.2k
  spans), with ~2.1k spans at 8pt (presumably footnotes/examples —
  to verify). No structural markup: paragraphs, tables, footnote
  links must be reconstructed from bboxes.
- **Existing `ghamoyan/out/full.md`** is a plain-text render — no
  bold/tables/footnotes. Step A must be built; the `.md` is only a
  reference for text content.
- **Chapters:** `ghamoyan/manifest.yaml` `structure:` records chapter
  page ranges — R4's chapter scope comes from metadata for ghamoyan,
  no detection heuristic needed.
- **Lemmatizer:** `frequency/build_ours.py::lemmatize` —
  suffix-stripping heuristic with documented failure modes (inflected
  leaks, manufactured `-ում → -ել` lemmas, homograph trap).
- **Translation material:** kaikki dictionary
  (`frequency/data/armenian.jsonl`, ~21k entries, EN-primary);
  hand-vetted deck glosses + `HAND_OVERRIDES` +
  `frequency/golden_glosses.tsv`; Russian layer
  `cards/frequency/russian_glosses.tsv` (translation prior, not
  corpus-cited); `saqapetoyan` neologism KB (614 loanword↔coinage↔
  ru↔en entries).
- **Frequency signals:** `frequency/out/hermitdave_hy_50k.txt`
  (subtitle-derived — genre-mismatched for academic prose) and
  `frequency/out/our_top_1000.tsv` (textbook-corpus-derived; also the
  "reader already knows these" baseline).
- **Grounding/verification machinery:** `frequency/query_kb.py`
  (deterministic KB retrieval), citation-check squash conventions,
  critic-agent pattern, challenge protocol (`llm-workflow.md`) — all
  reused by steps B/C/E rather than reinvented.

## Requirements

- **R1 — formatting fidelity.** Bold, italic, tables, footnotes of the
  original survive into the output. (Extraction JSONL carries
  font-name + size + bbox per span; style is recoverable from font
  names — e.g. ghamoyan's `ArialArmenianBold/Italic/BoldItalic`,
  ~2.9k styled spans.)
- **R2 — dictionary-form glosses.** Translations are attached to the
  *lemma*, shown under the surface form.
- **R3 — load-bearing words only**, with a **depth** setting.
  Decision: selection is **LLM judgement per sentence** (not a bare
  frequency threshold). Depth is a profile passed to the selector
  (see § Settings) plus a known-words baseline (deck top-1000).
- **R4 — no repeated glosses** within a scope window.
  Decision: dedup is keyed by **lemma** (not surface form), the window
  is measured in **source pages** (stable; output pagination differs),
  default reset at **chapter boundaries** when the book declares them
  (ghamoyan: `manifest.yaml` `structure:`), else every N source pages
  (default N=5). Both knobs are settings.
- **Gloss language: Russian primary, English fallback** when no Russian
  gloss is available at acceptable confidence.
- **Gap policy:** a selected word with no dictionary/deck entry is
  **LLM-translated and marked `prior`** in the sidecar; the render
  styles prior glosses distinctly (dashed underline). Honest-provenance
  discipline, reader stays unblocked.

## Architecture

Five steps, each producing a **durable artifact** consumed by the next.
Re-running step N never rewrites the artifact of step N−1; if a step's
results are bad, the step is redesigned, its predecessors untouched.
Downstream annotation is **standoff** (sidecar files keyed to step-A
ids), never in-place edits — this is what makes the no-reexecution
principle actually hold: changing B's selection cannot perturb the text
C was checked against.

```
full.jsonl ──A──▶ book.md + blocks.tsv          (structure + provenance)
              ─B─▶ selection.tsv                 (standoff: what to gloss)
              ─C─▶ glosses.tsv                   (standoff: lemma + translation)
              ─D─▶ book.typ ──typst──▶ book.pdf  (mechanical merge + render)
              ─E─▶ validation report             (bytes + editorial)
```

### A — structure recovery (JSONL → markdown + provenance)

Input: `<book>/out/full.jsonl` (span records: page, font, size, bbox,
text). Output:

- `book.md` — readable markdown: paragraphs, `**bold**`, `*italic*`,
  tables, footnotes, headings. Human-checkable rendition of the book.
- `blocks.tsv` — provenance sidecar: `block_id → page, y-range, kind
  (para/heading/table-cell/footnote)`. Every markdown block carries a
  stable `block_id` (HTML comment anchor). Token addressing downstream
  is `(block_id, token_index)`.

Chunking: emit per chapter (from `manifest.yaml` when present) or per
N pages, extending to the next sentence boundary (`։`) so no chunk ends
mid-sentence ("no hanging sentences").

**This is the highest-risk step.** The PDF has no structural markup:
tables are aligned text boxes, footnotes are 8pt spans at page bottom
(body is 9pt — verify), hyphenation splits words across lines. Every
layout heuristic (paragraph merge, table detection, footnote linking,
hyphen repair) falls under the challenge protocol (`llm-workflow.md`);
each gets golden anchors. Acceptance gate: **golden page set** — 5–10
hand-checked pages (incl. at least one table page and one footnote
page) diffed against the rendered PDF before A is trusted.

Text invariant: concatenated block text, whitespace-squashed
(`_squash` convention), must equal the page's JSONL bytes. This
invariant is what step E re-checks end-to-end.

### B — selection (LLM per sentence → standoff)

Input: A's artifacts. Output `selection.tsv`:
`block_id, token_start, token_end, surface, reason, confidence`.

- LLM reads sentence-in-context and selects words **crucial for
  understanding**, honoring the depth profile and the known-set
  (deck top-1000 lemmas = "reader already knows these").
- Frequency data (hermitdave 50k, our corpus counts) is supplied to the
  selector as a *signal*, not a rule — the LLM decides.
- `token_start..token_end` spans allow **multiword expressions**
  (light-verb constructions, idioms — the `դուր գալ` class) to be
  selected as one unit; glossing their parts separately is misleading.
- Cost/resume: selection runs per chunk, cached keyed by
  `(chunk content hash, depth profile, prompt version)` — re-running B
  after a prompt tweak recomputes only affected chunks.
- Validation: LLM selection is still a heuristic → challenge protocol
  applies. Golden selection set: sample pages hand-annotated
  ("must-select" / "must-not-select" lemmas), regression-checked on
  every prompt change. Baseline diff (protocol step 5): compare against
  the trivial frequency-threshold selector; the LLM must be strictly
  better on the golden set to earn its cost.

### C — lemmatize + translate + context check (standoff)

Input: A + B. Output `glosses.tsv`:
`block_id, token_start, token_end, surface, lemma, gloss_ru, gloss_en,
source, confidence`.

- **Lemmatization:** `build_ours.lemmatize` proposes, LLM confirms
  in context. Wrong-lemma → wrong-translation is *silent* — the
  dictionary happily glosses the wrong headword. The homograph trap
  (`գնում`, `դեմ` class: frequent form spelled like a rare headword
  whose only sense hides the ambiguity) is the documented worst case;
  the context check must gate on "does this lemma's sense fit this
  sentence", not on lookup success.
- **Translation lookup order:** deck `HAND_OVERRIDES` / golden glosses
  → `russian_glosses.tsv` → kaikki (`frequency/data/armenian.jsonl`,
  EN-primary → feeds the EN fallback) → **LLM, marked `source=prior`**.
  Every row records its source; nothing is unattributed.
- **Context-sense critic pass** (separate agent, adversarial framing
  per CLAUDE.md § critic-agent): "does this gloss fit this sentence?
  where would it be wrong?" Findings → corrections + golden anchors
  (two-step rule).
- Dedup is **not** C's job (see D) — C glosses every selected
  occurrence, so the repeat window can be changed without re-running C.

### D — merge + typeset (mechanical)

Input: A + C + settings. Output: `book.typ` → `typst compile` →
`book.pdf`.

- Pure function, no judgement: apply the repeat-window filter (first
  occurrence per lemma per scope keeps its gloss; later ones drop it),
  map markdown structure to typst (bold/italic/tables/footnotes/
  headings), wrap glossed spans in a `#gloss(word, ru)[...]` typst
  function that stacks the translation beneath in small gray type;
  `source=prior` glosses get a dashed underline.
- Page geometry, fonts, gloss styling, EN-fallback rendering are all
  config — changing them re-runs D only ("intermediate assembler").
- The `.typ` source is itself a durable, inspectable artifact.
- Prerequisite: typst — installed 2026-07-23.

### E — validation

1. **Mechanical (bytes):** strip gloss markup from D's input model,
   squash whitespace, compare per source page against `full.jsonl`
   text. Any drift = a bug in A or D. Same discipline as the citation
   hooks.
2. **Gloss audit:** sample glossed tokens, verify lemma+sense against
   KB (`query_kb.py`) — the song-domain "mandatory citation re-audit"
   analogue; drafting LLMs fabricate plausible glosses.
3. **Editorial (unbiased-reader pass):** agent (or human) reads the
   PDF as a learner: gloss density right? glosses readable at size?
   tables intact? line breaks sane? Structural checks systematically
   miss shape bugs (2026-05-09 deck-cleanup lesson) — this pass is
   mandatory, not optional.

## Iteration model (where loops live)

- **Within a step:** verification loops until dry — C's context critic
  and E's gloss audit repeat until K consecutive rounds find nothing
  new (single-pass review demonstrably misses; cf. the Myus Angam
  whole-song audit). A's layout heuristics iterate against the golden
  pages the same way.
- **Across steps:** feedback carries **rules, not artifacts**. An E
  finding never patches `glosses.tsv`; it becomes a golden anchor /
  override / prompt change, and the step reruns from its upstream
  inputs. Loop state = golden sets + rulesets; artifacts are always
  regenerated. (Two-step rule; preserves the no-readjust principle.)
- **Settings tuning** loops over D only (seconds) — dedup and render
  were pushed to D precisely so density/layout iteration is free.
- **No execution loops:** the long LLM run is chunk-hashed and
  resumable; a single rerun recomputes only uncached chunks.

## Model policy

- **Armenian-semantics judgement stays top-tier** (session model,
  Fable): B selection, C lemma/sense-in-context, `prior` translations,
  E editorial. Armenian is low-resource — capability degrades faster
  down the tiers than English tasks suggest; and the volume (~a few
  hundred calls/book at per-page batching) is too small for downgrades
  to pay for their risk.
- **Critics run on a different model (Opus)** to decorrelate from the
  drafter: a same-model critic shares the drafter's priors and finds
  drafts plausible for the same reasons. Applies to C's context critic,
  E's gloss audit, and E's "unbiased agent" pass — *unbiased relative
  to the drafter* ≈ different model + adversarial frame.
- Model ID is part of the B/C chunk-cache key (with prompt version):
  switching models invalidates the cache; never mix models silently
  within one artifact.
- Any tier downgrade proposal is a heuristic change → challenge
  protocol: golden-set diff against the current baseline first.
- Grounding outranks model choice (the խոտ four-LLM case): dictionary/
  KB-backed glosses are model-independent by construction; model tier
  only decides the quality of what's left.

## Settings

| setting | meaning | default |
|---|---|---|
| `depth` | selection profile given to B (e.g. `learner-1k`: assume top-1000 known; `shallow`: only rare/technical) | `learner-1k` |
| `repeat_scope` | `chapter` \| `pages` | `chapter` if manifest declares structure, else `pages` |
| `repeat_pages` | window in *source* pages when scope=`pages` | 5 |
| `gloss_lang` | priority list | `ru,en` |
| `page` | typst page geometry, base font size | A5, 10pt |

## Known risks (ranked)

1. **A's layout reconstruction** — most effort, most heuristics, gates
   everything. Mitigation: golden page set before anything else runs.
2. **Silent wrong lemma / homograph trap** — mitigation: context-gated
   lemma check in C + golden anchors; corpus (not dictionary) is the
   arbiter of which sense is live.
3. **LLM cost & drift in B** — per-sentence judgement over a 118-page
   book is slow and rerun-hostile. Mitigation: chunk-hash caching,
   prompt-versioned golden regression, baseline diff vs frequency
   threshold.
4. **Coverage gaps** — ghamoyan's body is academic linguistic prose;
   kaikki coverage of terminology is poor and Russian coverage poorer.
   Mitigation: `prior`-marked LLM glosses (decided); recurring gap
   lemmas graduate into a hand-curated overrides TSV (two-step rule).
5. **Dedup traps** — lemmatizer mapping two inflections of one word to
   different lemmas silently defeats dedup; homographs must *not*
   dedup across senses (key is lemma+sense-source, not bare surface).
   Golden anchors for both.
6. **ARMSCII decode** (ghamoyan-specific) — decoded text must be
   spot-checked against page bitmaps per the standing rule; A's golden
   pages double as this check.

## Layout

New top-level `interlinear/` (cross-book tool, like `frequency/`):
`interlinear/{structure.py,select.py,gloss.py,render.py,validate.py}`,
per-book artifacts in `interlinear/out/<book>/`. Golden sets in
`interlinear/golden/`.

## Milestones

1. ✅ (2026-07-23) A for ghamoyan chapter 2 (pp. 35–40) — byte-check
   green (11,576 squashed chars), golden-page visual diff vs the
   rendered PDF pages passed. Implementation deviations from this
   FRD, all documented in `interlinear/README.md`: selection is
   lemma-level with a first-occurrence anchor (windows smaller than
   chapter not yet needed); byte-check compares body and footnote
   streams separately (a footnote can interleave inside a cross-page
   paragraph, which a block-level sort cannot express).
2. ✅ B+C: 114 selections (learner-1k pruned 45 deck-known),
   glosses 49 kaikki / 7 grammar-terms / 58 prior; Opus critic pass:
   0 wrong, 5 refinements applied; golden anchors in
   `interlinear/golden/glosses_ghamoyan_ch2.tsv`.
3. ✅ D+E: 8-page A5 PDF (`interlinear/ghamoyan/ch2/book.pdf`),
   ruby glosses with word-width boxes, prior rows dash-underlined,
   footnote placed by typst (renumbered); editorial pass run.
4. E mechanical byte-check wired — done as part of 1; remaining:
   full ghamoyan run (needs table support in structure.py).
5. Generalize: second book (sakayan or dumtragut) to flush
   ghamoyan-specific assumptions.
