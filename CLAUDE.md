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

### Automation: this rule is hook-enforced

`.claude/hooks/armenian_autoground.py` runs on every
`UserPromptSubmit` event. When the user's prompt contains any
Armenian character (U+0530–U+058F), it invokes
`frequency/query_kb.py` automatically and injects the resulting
bundle as a system-reminder *before* the model sees the prompt.
You'll see a `<system-reminder>` block titled "Armenian content
detected" — that's the bundle. Ground the answer in it.

To skip the auto-grounding for a specific prompt (e.g. while
editing a topic file that contains Armenian fragments), prefix
the prompt with `#nogrep` (prefix only — mentioning the token
mid-prompt does not suppress). Prompts over 8000 chars are
skipped as likely file pastes. Every invocation (fired or
skipped, with reason) is logged to
`.claude/logs/armenian_autoground.jsonl`. The hook is registered
in `.claude/settings.json` (committed) and survives reinstall.

### Automation: same check on the response side (Stop hook)

`.claude/hooks/armenian_self_check.py` runs on every `Stop`
event (i.e. when the model finishes a draft response). It
reads the draft from the session transcript (the Stop payload
carries `transcript_path`, not the response text; the hook
parses the JSONL and takes the last assistant message's text
blocks). It mirrors the auto-grounding hook in the opposite
direction and has **two arms** keyed on whether the draft
carries a citation marker (a `topics/<...>.md` path or a
book-page cite like `ghamoyan p48`):

- **Uncited arm** (the original behaviour). If the draft has
  substantive Armenian content (≥ 20 Armenian characters) and
  **no** citation marker, it runs `frequency/query_kb.py` on
  the Armenian-bearing lines and, if the bundle has substantive
  corpus matches, **blocks** with the bundle as feedback. The
  model re-emits with the bundle in context and reconciles any
  claims that disagree. This gates on *presence of a citation*.

- **Cited arm** (added 2026-06-13). A citation is no longer
  trusted on sight — a *fabricated* page cite used to be the
  one thing that waved a draft straight through. Now each
  `<book> pN` cite is **byte-verified against the corpus**: for
  every line, quoted Armenian fragments (`` `…` ``, `«…»`,
  straight/smart quotes) are bound to the `<book> pN` cite **on
  that same line** and checked against that page's bytes. A
  mismatch **blocks**, naming the specific unsupported
  `fragment@book pN`. This gates on whether the cited claim is
  *supported* — the evidence-*consumption* gap, vs. the uncited
  arm's evidence-*delivery* gap.

  Verification details: **sakayan**, **ghamoyan** and
  **dumtragut** are verifiable (clean text layer). parnasyan/
  tioyan are OCR/Cyrillic-garbled and acharyan/gharagyulyan lack
  a text field, so their cites log `skip-cited-unverifiable`
  rather than false-block. Matching is **whitespace-insensitive
  NFC** (`_squash`) because the corpus stores text at token/box
  granularity — a multiword phrase the model quotes with a
  single space (`word1 word2`) is `word1\nword2` on the page;
  squashing whitespace on both sides avoids false-blocking
  correct multiword citations (test (g) is the guard). The same
  squash makes **IPA respellings citable**: dumtragut stores IPA
  one glyph per span (`[mɑɾtʰ]` = `[ m ɑ ɾ tʰ ]`), so the
  cited-arm also extracts IPA `[…]` brackets (carrying an
  IPA-specific glyph) and byte-verifies them — a wrong respell
  (`[mɑɾt]` for page's `[mɑɾtʰ]`) blocks at emit time (tests (h)/
  (i)). `citation-check` squashes identically, so topic
  `verbatim_quote`s may be IPA brackets too (give the y-window
  ~3pt of headroom to include the raised superscript ʰ span).
  Log actions: `pass-citations-verified` /
  `block-citation-unverified` / `skip-cited-unverifiable`.

This closes the gap that motivated 7+ failure-log entries over
the 2026-05-09 → 2026-05-26 stretch (see
`errors/INDEX.md`): the model would assert structurally-
plausible-sounding Armenian analysis without checking the
corpus, and the operator had to manually push back. The
self-check hook automates the push-back. The cited arm
additionally catches the citation-fabrication class
(`errors/2026-06-01-001`): a plausible `«word»` attached to a
page that doesn't contain it now blocks at emit time.

To skip the self-check for a specific response, include the
literal token `#nocheck` in the response prose. The hook also
has an anti-loop guard via the payload's `stop_hook_active`
field — it fires at most once per turn. Activations are logged
to `.claude/logs/armenian_self_check.jsonl` for measurement.

See `research/2026-05-26-pre-emit-verification-automation.md`
for the original design rationale (options A-D considered; this
is A), and
`research/2026-06-13-answer-verification-architecture-fit.md`
for the cited-arm rationale (the SAFE-shaped verify-over-draft
that motivated byte-verifying cited claims rather than trusting
them).

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
- **Homograph trap.** The most insidious deck bug: a high-
  frequency grammatical/colloquial token spelled like a rare
  literary headword, so kaikki returns the rare sense (often the
  *only* sense → invisible to ambiguity flagging). `մերի`
  "woods" (gen of `մերը`), `ներ` "sister-in-law" (the `-ներ`
  plural suffix), `գնում` "purchase" (converb of `գնալ`), `դեմ`
  "front part" (postp "against"). Confirm in the **corpus**, not
  the dictionary; then `SKIP_LEMMAS` if it's a form of a deck
  lemma / noise, or `HAND_OVERRIDES` if it's the wrong sense.
  Full drill + case list: `llm-workflow.md` § "The homograph
  trap".
- **Russian-augmentation layer.** Authoring schema is
  `English / Russian` (` / ` is *reserved* for that boundary —
  never an English comma). Russian for English-only cards lives
  in `cards/frequency/russian_glosses.tsv` (a *translation*
  layer, prior not corpus-cited); `build_deck.py` appends
  ` / <ru>` only when the gloss has no Cyrillic yet, so
  hand-overrides that already carry Russian are untouched.
  Coverage target = top-300 + function words/pronouns, tracked by
  `check_missing_russian`. Embed short examples for function
  words inside the gloss (`ներս` → "in, inside (ներս մտնել — to
  enter)").
- **Output is HTML (2026-06-03).** Both columns are Anki HTML.
  Authoring stays plain; `render_gloss` + `render_lemma` emit it at
  write time. Gloss: English bold, Russian gray
  (`<span style='color:#888'>`), examples italic, EN/RU split on
  `<br>`. Front: lemma bold, `[respell]` small gray on the same line.
  Import with **"Allow HTML in fields" enabled**. Single-quoted attrs
  only (the CSV writer would quote-escape `"`). `render_gloss` splits
  on the *last* ` / ` (English may contain a parenthetical slash).
  The validator strips HTML from *both* columns via `plain_gloss()`
  before its checks; the `deck_meta.tsv` sidecar is keyed by the
  plain lemma.
- **Tags are `frequency top-1000` / `core-inject` /
  `phrasal-verb`** — rank and src dropped from the card per user
  request. They live in the `frequency/out/deck_meta.tsv` sidecar,
  which the validator loads so its rank/`src-`-aware checks still
  work. Don't put `rank-NNNN` back on the card.
- **Numbers are digits** (`մեկ`→`1`, `հինգերորդ`→`5th`) via
  `NUMBER_DIGITS`; digit-only glosses are exempt from
  `check_missing_russian`.
- **Phrasal / light-verb cards** live in
  `cards/frequency/phrasal_verbs.tsv` (mined from the textbook
  corpora, corpus-grounded), injected with tag
  `frequency phrasal-verb`. The list may grow.
- Run `frequency/validate_deck.py` after every
  `frequency/build_deck.py`. Inspect `info`-severity
  `ambiguous-sense` rows for fresh misranks. Checks added across
  the 2026-06-03 reviews: `missing-russian`, `reserved-slash`,
  `morpheme-noise`, `mixed-script-gloss` (Armenian+Cyrillic in one
  gloss token — the `էл`-with-Cyrillic-`л` bug), and
  `duplicate-override-key` (a dict key duplicated in build_deck.py
  silently shadows — caught the `դուր` regression).
- **Editorial pass**: after the structural validator is
  green, run the `deck-editorial-pass` skill
  (`.claude/skills/deck-editorial-pass/`) for the
  agent-side critic that catches the residue structural
  checks miss (sense-priority misorder, gloss naturalness,
  register mismatch, ambiguous sense-stacks that pass the
  length cap). Pattern: sample N rows → spawn
  `general-purpose` Agent with `PROMPT.md` → triage
  findings. **Two-step rule applies to findings**:
  ⚠ blocker → add `HAND_OVERRIDES` entry **and**
  `frequency/golden_glosses.tsv` anchor (the fix + the
  guard); ⚙ suggestion → at least the golden-set anchor
  if accepted. The 2026-05-09 deck-cleanup case is the
  canonical motivation; this skill packages the loop.

### OCR / extraction pipelines

- Each book has `<book>/extract.py` writing JSONL to
  `<book>/out/full.jsonl`. The pipeline's parsing heuristics
  (column splits, character maps, font handling) qualify as
  rules requiring the challenge protocol. New pipeline change →
  spot-check 5–10 random pages against the rendered PDF.
- ARMSCII-8 decoder (ghamoyan): never trust the auto-decoded
  output without comparing against the source page bitmap.

### Song / lyric processing (`songs/`)

- Armenian songs (esp. hip-hop / rap) are processed under
  `songs/` — one Markdown file per song. **Read
  `songs/README.md` first** for the routine; it is the
  song-domain analogue of the topic-graph workflow.
- A song file is a **provenance document**, not just a gloss
  table: it records the latest final translation **and** how
  each meaning was obtained (cited vs. prior), the
  transcription source + its caveats, confidence per line, and
  a verification log.
- The seven-step routine (acquire+attribute text → normalize
  colloquial spelling → KB-ground the lexicon via
  `query_kb.py` + `grep ghamoyan` → translate per-line graded →
  verify at granularity with critic agents → record provenance →
  **whole-song pass over the assembled file**) mirrors the
  grounding discipline in § "Before answering an Armenian-language
  question." Lyrics from a lyric video / Musixmatch are a
  **transcription**, never authoritative — flag uncertain lines
  `low`.
- **Mandatory citation re-audit (step 7).** Drafting subagents
  reliably fabricate plausible-but-wrong citations — the repo's
  canonical failure mode. After assembling the file, `grep` every
  cited page against the corpus (the song-domain analogue of
  `citation-check`). The 2026-06-01 *Myus Angam* whole-song pass
  caught six wrong citations that section-by-section review missed.
  This is the two-step rule applied to songs: the fix is the
  audit, the guard is making it a routine step.
- The **critic-agent pattern** applies to *meaning*: spawn
  separate agents per verse (or per low-confidence line) framed
  "is this gloss correct? where would it be wrong?" and
  reconcile findings into the file's Verification log.
- Slang glosses get a citation (`ghamoyan` p-N,
  `topics/lexicon/yerevan_slang.md`) where attested; Russian-
  origin slang and idioms not in corpus are marked **prior**.
- Canonical worked example: `songs/dav-vnas-myus-angam.md`.

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
