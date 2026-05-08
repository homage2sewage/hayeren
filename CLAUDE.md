# Working in this repo with Claude

Workspace-wide habits and constraints. Read `INDEX.md` for layout
and `llm-workflow.md` for the rationale behind the heuristic-
validation rules below.

## Heuristic validation — non-negotiable

This repo has a documented failure mode: plausible-sounding rules
ship, fail on edge cases, surface as user-found bugs. Every fix
costs a session round-trip. The remedy is a workflow rule:

> Before adding any *priority / sort-key / fallback / filter / re-
> ranking* heuristic ANYWHERE in the repo (deck builder, OCR
> pipeline, topic-graph schema, lemmatiser, glossary lookup,
> frequency rule, transliteration converter, ANYTHING), run the
> challenge protocol from `llm-workflow.md` § "When introducing a
> new heuristic" — or invoke the `challenge-rule` skill.

Six steps, mandatory:

1. **Inputs.** Enumerate or sample the population the rule will act
   on.
2. **Outputs.** Generate the rule's outputs across that sample.
3. **Counterexamples.** Find cases where the rule chose poorly.
4. **Golden anchors.** Convert step-3 cases into golden-set
   entries (`frequency/golden_glosses.tsv` for deck-domain;
   parallel files for other domains).
5. **Baseline diff.** Compare against the trivial baseline (no
   priority, identity, source-natural-order). If the proposed
   rule isn't strictly better, drop it.
6. **Land.** Commit only after 1–5.

Skipping these is the failure mode. Don't.

## Critic-agent pattern

When implementing any non-trivial heuristic, pipeline rule, or
schema decision, after writing it:

- Spawn a separate Agent (e.g. `general-purpose`) with the
  framing **"find weaknesses in this rule / where would it pick
  the wrong answer / produce the wrong output"** — different
  prompt frame from the implementer agent.
- Feed it the rule + a sample of inputs + the desired outputs.
- Treat its output as adversarial test data: each plausible
  failure case becomes either a HAND_OVERRIDES entry / golden-
  set anchor / extension to the runtime validator.

**Two framings, two passes.** Run the critic agent (or a manual
review) in both:

1. *Structural* — "does the rule pick the right answer? are the
   bytes correct? does it round-trip?" Catches content bugs.
2. *Editorial* — "read this as the end user (a learner, not a
   pipeline). Does the output read naturally? Does it look like
   a flashcard / a paragraph / a citation? What would you flag?"
   Catches shape bugs that structural checks systematically miss.

The 2026-05-09 deck cleanup is the canonical case: 0 structural
errors but six classes of editorial bugs (dictionary-prose
glosses, kaikki sense-stacks, underscore-MWUs, redundant
`(language)`, inflected leaks). The fix loop is in
`llm-workflow.md` §§ 9–10 and `frequency/validate_deck.py` §
`check_prose_gloss / check_verbose_gloss /
check_redundant_language_parenthetical`.

This generalises beyond `frequency/`: same pattern for OCR
pipelines (`sakayan/extract.py`, `parnasyan/extract.py`,
`tioyan/extract.py`), citation-checking heuristics
(`.claude/skills/citation-check/check.py`), schema rules in
`kb-design.md`, transliteration logic in
`transliteration-notes.md`, etc.

## Before answering an Armenian-language question

Default reflex when the user asks about a specific Armenian word,
phrase, or grammar phenomenon: **grep the KB before answering**.
The pre-training prior is the *fallback*, not the first move.

The fast path — automated retrieval:

```sh
python3 frequency/query_kb.py "<armenian text>"
```

`query_kb.py` is the deterministic KB-grounding layer: it
tokenises + lemmatises the input, greps `topics/`, the four book
JSONLs, and the project notes, and emits a Markdown bundle with
matched-topic excerpts, book passages with page+y-range, and an
explicit *Gaps* section listing query-lemmas with no coverage.
That's the bundle you ground an answer in — anything outside it
is pre-training prior, not citation. Run this *first* on any
question targeting a specific Armenian word/phrase.

Manual fallback (if the script can't help — e.g. lemma is too
short, or you want to check inflected forms directly):

1. **Topic graph.** `grep -rE "<content-word>" topics/` — every
   topic is a citation-checked synthesis. If a topic covers the
   phenomenon, ground the answer in it.
2. **Source corpus.** `grep -nE "<content-word>" \
   {sakayan,ghamoyan,parnasyan,tioyan}/out/full.jsonl` — the raw
   extractions. Even if no topic exists, the books may have a
   primary citation usable as evidence.
3. **Project notes.** `armenian-grammar.md`, `transliteration-
   notes.md`, `grammar-terms.md` — broader synthesis docs.
4. **Cards.** `cards/top_1000.tsv`, `cards/sakayan/*.tsv` — for
   high-frequency lemmas, the deck has hand-vetted glosses.

Then answer with:

- **Citations attached** to each glossed claim (`per
  topics/lexicon/yerevan_slang.md, ghamoyan p48 [#3]`).
- **Confidence graded**, not uniform-high. Distinguish "well-
  cited" / "single-source" / "no topic entry — guess from prior."
- **Gaps named explicitly.** If no source covers a claim, say so;
  don't paper over with confident pre-training prose.
- **Topic-file links** so the user can follow up.

Why: the canonical case is the 2026-05-09 Pashinyan-tweet
comparison (`research/2026-05-09-tweet-llm-comparison.md`) where
four LLMs (including me) confidently produced four different
glosses for `խոտ` while the correct citation
("naive / clueless person," ghamoyan p48) was sitting in
`topics/lexicon/yerevan_slang.md` line 114. Nobody looked. The
habitual fix is in this rule. Reach for grep, not for prior.

## When the user reports a wrong output

Always two-step, never one:

1. **Fix the immediate case.** Patch the data, add a HAND_OVERRIDE,
   amend the rule.
2. **Capture as a guard.** Add a golden-set entry / extend a noise
   pattern / add a runtime check. The same shape of bug must cost
   less to catch next time.

If the existing checks couldn't structurally have caught the bug,
that's a signal to extend the validator, not just patch the data.

## Domain-specific reminders

### Topic graph (`topics/`)

- Every `verbatim_quote` fragment MUST be literal JSONL bytes,
  not glosses. Use `.claude/skills/citation-check/check.py` to
  verify.
- Schema validation lives in `.claude/skills/critic-pass/lint.py`.
- Topics that survive both checks AND have ≥2 source-book
  citations → `attestation: multi-attested`.

### Card decks (`cards/`)

- Lemma column may carry `[phonetic-respell]` annotations (Armenian
  script). Generated by `sakayan/phonetics.py` for sakayan
  sources; hand-curated `PHONETIC_OVERRIDES` in
  `frequency/build_deck.py` for others. Empty bracket → no
  deviation; if respell == lemma, no bracket emitted.
- HAND_OVERRIDES are the safety valve when kaikki's natural
  order misranks a sense (`արի`, `արա`, `դուր`, …). Add an
  override AND a golden-set entry — never just one or the other.
- Run `frequency/validate_deck.py` after every
  `frequency/build_deck.py`. Inspect `info`-severity
  `ambiguous-sense` rows for fresh misranks.

### OCR / extraction pipelines

- Each book has `<book>/extract.py` writing JSONL to
  `<book>/out/full.jsonl`. The pipeline's parsing heuristics
  (column splits, character maps, font handling) qualify as
  rules requiring the challenge protocol. New pipeline change →
  spot-check 5–10 random pages against the rendered PDF.
- ARMSCII-8 decoder (ghamoyan): never trust the auto-decoded
  output without comparing against the source page bitmap.

### Transliteration

- The `ches asem` trap is the canonical failure of naive
  back-transliteration. Always run the heuristic sequence in
  `transliteration-notes.md` § "Back-transliteration heuristics"
  before treating Latin-script Armenian as authoritative.

## Style / convention reminders

- Prefer editing existing files to creating new ones. Workspace
  is meant to be made public eventually — no references to
  sibling `~/work/<other>` directories or private notes.
- Topic / research / walk filenames are dated:
  `YYYY-MM-DD-<slug>.md`.
- Memory file paths are private (under `~/.claude/...`); the
  workspace itself is the published surface. Don't link from
  workspace files into memory paths.
