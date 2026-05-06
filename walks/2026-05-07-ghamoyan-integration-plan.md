# Plan: integrate `ghamoyan/` as second book

**Status**: proposal, not yet executed.
**Author**: drafted with Claude Code 2026-05-07.

## Context

- `ghamoyan/` was added 2026-05-07 with PDF, ARMSCII-8 decoder, and a
  full extraction (`out/full.jsonl`, ~13.3k spans, `out/full.md`).
- Source: Ghamoyan, Sargsyan & Kartashyan, *Yerevan's Colloquial
  Language* (2014, 118 pp). A linguistic study of spoken Yerevan
  Armenian vs the literary norm — phonology, lexicon, morphology,
  syntax, style.
- Existing topics under `topics/` (4): voiced_aspirated_alternation,
  three_way_laryngeal_contrast (phonology); present_tense
  (morphology); pro_drop (syntax). All currently
  `attestation: single-source` (sakayan only).
- This plan replaces the prior "next book = Dum-Tragut" recommendation:
  ghamoyan is now the natural Phase-1 second source because it's
  already extracted *and* it occupies a register slot Sakayan doesn't
  cover (descriptive colloquial vs prescriptive literary).

## Goals

1. Make `book: ghamoyan` citable from topic files (as `book: sakayan`
   already is).
2. Convert as many existing topics as possible from `single-source`
   to `multi-attested` (or `conflicting`, where the two books
   genuinely disagree — that's the *interesting* case for this
   project).
3. Discover phenomena ghamoyan covers that aren't in `topics/` yet —
   especially register, sociolinguistic, and dialect-specific
   phenomena that Sakayan deliberately omits.

## Phases

### Phase 0 — Convention + manifests

- **Layout decision**: book directories currently live at top level
  (`sakayan/`, `ghamoyan/`); `kb-design.md` sketches `books/<name>/`.
  The citation-check script already handles both. Recommendation:
  **accept reality** — keep top-level book dirs, update kb-design.md
  to match. Migrating to `books/` would touch every extract.py
  internal path, every venv reference, and the user's habits, for no
  data benefit. The `books/` wrapper was an aesthetic preference, not
  a structural need.
- **Write `<book>/manifest.yaml`** for both books. Schema:
  ```yaml
  title: "Eastern Armenian for the English-Speaking World"
  authors: ["Sakayan, Dora"]
  year: 2007
  pages: 558
  dialect: eastern-standard         # eastern-standard | yerevan-colloquial | ...
  register: prescriptive-pedagogy   # prescriptive-pedagogy | descriptive-linguistic-study | reference-grammar | conversational-handbook
  audience: english-speakers        # english-speakers | linguists | russian-speakers | general-armenian-learners
  contrastive-with: [english]       # languages explicitly contrasted in the source
  extraction:
    jsonl: out/full.jsonl
    md: out/full.md
    pages-extracted: 558
  ```
- **Sakayan**: `dialect: eastern-standard, register:
  prescriptive-pedagogy, audience: english-speakers, contrastive-with:
  [english]`.
- **Ghamoyan**: `dialect: yerevan-colloquial, register:
  descriptive-linguistic-study, audience: linguists, contrastive-with:
  [eastern-standard]` (the literary norm is the foil).

The manifest is purely metadata for now — citation-check ignores it.
But `topic-walk` (when written) and any future register-aware Q&A
needs these tags to weight or label sources.

### Phase 1 — Topic walks (manual first, then skill)

For each existing topic, scan `ghamoyan/out/full.jsonl` for relevant
content. Output goes to a walk plan file:

```
walks/2026-05-07-topic-walk-ghamoyan-<phenomenon>.md
```

Each plan file proposes:

- new source entries to add to the topic's `sources:` block
  (`book: ghamoyan`, page, y_range, verbatim_quote, supports, note);
- proposed `attestation` change (`single-source` → `multi-attested`
  or `conflicting`);
- prose deltas to the body — especially when ghamoyan disagrees with
  sakayan, an explicit "literary vs colloquial" contrast paragraph;
- new `gaps:` items uncovered.

Human reviews, accepts/rejects, merges into the topic file. Run
`citation-check` and `critic-pass` against the merged result.

**Recommended order** (rationale: phonology likely has the most
genuine prescriptive-vs-descriptive disagreement):

1. **voiced_aspirated_alternation** — does ghamoyan describe the
   alternation phonologically (rule-based) where Sakayan only
   exemplifies? Does Yerevan colloquial extend the alternation
   further?
2. **three_way_laryngeal_contrast** — does ghamoyan document
   collapse, neutralisation, or any shift in colloquial speech?
   This is the highest-value question for the whole phonology arc.
3. **pro_drop** — discourse-pragmatic conditions on pronoun
   expression in spontaneous speech. Sakayan's "emphasis or
   contrast" framing is from textbook examples; colloquial data may
   be richer.
4. **present_tense** — auxiliary clitic positioning, register
   variation, contraction phenomena. Common in colloquial Armenian
   (e.g. `գրումեմ` clitic merges) but absent from Sakayan's canonical
   forms.

For the first walk, do it **manually**: read the relevant ghamoyan
chapters by hand (118 pp is tractable), write the plan file, merge.
Use that experience to draft the `topic-walk` skill. Don't skill-ify
prematurely.

### Phase 2 — Discovery walk

Read ghamoyan's table of contents and chapter headings to find
phenomena it treats that aren't in `topics/`:

- Likely candidates from the back-cover description (phonology /
  lexicon / morphology / syntax / style):
  - **Lexical doublets / register-specific vocabulary** — colloquial
    forms vs literary forms. Probably becomes
    `topics/lexicon/register_doublets.md`.
  - **Style register markers** — discourse particles, hedges,
    intensifiers. New file in `topics/pragmatics/`.
  - **Phonological reductions** — vowel drops, cluster
    simplification beyond Sakayan's epenthetic-schwa rule.
  - **Morphological colloquialisms** — non-standard inflections,
    contracted auxiliaries.
  - **Syntax** — word order variation, ellipsis, dialogue-specific
    structures.

Output: `walks/2026-05-07-discovery-walk-ghamoyan.md` with one
proposed topic file per discovered phenomenon (skeletons only).
Human picks which to flesh out and in what order.

### Phase 3 — Lexicon layer

The first time we have register-specific lexical doublets is when
`lexicon/<lemma>.md` starts to earn its keep. Each entry shows:

- the literary form (sakayan citation)
- the colloquial form (ghamoyan citation)
- wiktionary lookup (already cached via `lookup.py`)
- usage notes / register

Defer until at least one Phase-1 walk and the Phase-2 discovery walk
have run.

## Specific deliverables (in order)

1. `sakayan/manifest.yaml`, `ghamoyan/manifest.yaml`.
2. Update `kb-design.md`: layout decision (top-level book dirs is
   official), reflect ghamoyan presence in Inputs section.
3. Manual topic-walk on `voiced_aspirated_alternation` against
   ghamoyan → `walks/2026-05-07-topic-walk-ghamoyan-voiced_aspirated_alternation.md`.
4. Merge accepted proposals into the topic; re-run
   citation-check + critic-pass; update topic's `attestation`.
5. Lessons learned → first cut of `topic-walk` skill at
   `.claude/skills/topic-walk/`.
6. Run topic-walk on the remaining 3 existing topics.
7. Discovery walk on ghamoyan.

## Risks / open questions

- **Ghamoyan is descriptive, Sakayan is prescriptive.** Most topics
  will end up `conflicting` rather than `multi-attested`. The body
  prose convention for that case isn't yet exercised — will need to
  evolve it during the first walk.
- **Register-tagging propagation.** Once topics start having
  conflicting sources, every claim probably needs a register tag
  (`literary` / `colloquial` / `both`). May force a schema extension
  to per-claim register, not just per-source.
- **Cross-book example matching.** Ghamoyan's transliteration scheme
  (if any) may differ from Sakayan's Armtrans; matching the *same
  word* across books for a single phenomenon needs a normalisation
  step.
- **Linguistic terminology drift.** Ghamoyan likely uses Armenian
  linguistic vocabulary not in `grammar-terms.md`. Plan to extend the
  glossary on first encounter.
- **Validity of the manifest's `register:` enum.** Two books isn't
  enough to prove the four-value enum is right. Expect to revise.

## Explicitly out of scope

- **Dum-Tragut acquisition / extraction**. Re-evaluate after the
  ghamoyan integration is complete: the gap-walk output will tell us
  whether a typological reference grammar is the highest-value next
  source, or whether something else (a Western Armenian source,
  a Classical Armenian historical, a children's reader) takes
  priority.
- **Walk-skill formalisation before manual experience**. The
  `topic-walk` skill should be built *after* doing 1–2 walks
  manually, so its scaffolding reflects what actually worked.
- **Layout migration to `books/`**. Decided against (see Phase 0).

## Smallest concrete next move

Write `sakayan/manifest.yaml` and `ghamoyan/manifest.yaml`, then read
ghamoyan's first ~30 pages (or the phonology chapter) to draft the
voiced↔aspirated alternation topic-walk plan file by hand.
