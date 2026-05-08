# LLM workflow hygiene — catching wrong heuristics before they ship

Working notes on a recurring failure mode in LLM-assisted code: the
LLM (or the human, prompted by the LLM's prose) commits a
plausible-sounding rule that wasn't empirically validated, and the
bug surfaces only via downstream user feedback. Captured here because
the lesson generalises beyond this workspace.

## Where this came from

A real instance from this project, 2026-05-09:
`frequency/dictionary.py` had a POS-priority rule that promoted
`verb > noun > adj > adv …` when picking a translation gloss for a
top-1000 lemma. The rule's stated rationale was the implicit
"translation glosses are usually nouns." It was true on average and
wrong exactly where it mattered — adjective-primary words like
`տարեկան` surfaced their rare noun sense ("rye"), `բաց` surfaced
"Bats (language)", and so on.

The rule should have been confronted with its own input population
*before* shipping. The audit, when finally done, was one batch of
~50 multi-POS lemmas; the failure mode was obvious within seconds.
The cost of skipping that audit: multiple rounds of user-found
errors over several sessions.

## Principles

The trap is asymmetric: LLMs (and humans) eagerly write
plausible-sounding heuristics — priorities, sort keys, fallbacks —
and we accept them on prose justification rather than data
confrontation. The remedy isn't more rules; it's a workflow that
forces empirical confrontation at the moment of rule introduction.

### 1. Adversarial-case prompts on every heuristic

When a rule is proposed, the next move is *not* "implement it" — it
is "name 10 inputs where this rule produces the wrong output." If
the LLM (or you) can't produce 10, that's also signal.

### 2. Output-first, rule-last

Sketch desired outputs *before* writing the rule. "For these 30
lemmas, here are the glosses we want." The rule is whatever
produces that table — and the table doubles as a test.

### 3. Baseline comparison is mandatory

Every proposed re-ranking competes against the trivial baseline
(do nothing, trust the source's order, return identity). If the
rule can't beat the baseline on the audit set, drop it. The
noun-promotion rule lost to "kaikki order" — we just hadn't
compared.

### 4. Golden tests are the persistent form of the audit

Every wrong output the user (or dogfooding) catches becomes a
permanent golden-set entry. Future LLM-assisted edits run against
it; the regression is caught at PR-time, not session N+5. See
`frequency/golden_glosses.tsv` and `frequency/validate_deck.py`'s
`check_golden_glosses` for the realisation in this codebase.

### 5. Critic-agent / second-pass review

When an LLM writes a heuristic, run a second pass with explicit
"find weaknesses in this rule" framing — different agent, different
prompt. Often surfaces what the implementer agent rationalised
past. This generalises what runtime validators
(`validate_deck.py`'s `check_dictionary_ambiguity`) do — it's an
automated critic for the lookup.

### 6. Distrust LLM rationale that names no examples

"It's standard to prioritise verbs and nouns" is an LLM-style
explanation that sounds authoritative but cites nothing. Demand a
concrete witness: a published source, a reference dataset, a worked
example. If only the LLM's prior says it, treat as a hypothesis.

### 7. Dogfood early, label discoveries as process signals

"User found a wrong gloss" is the cheapest validation signal in
the system. Treat each one as a *workflow audit signal*, not just
"fix this card": ask "what process failed to catch this?" The
answer becomes a permanent guard (a check, a golden entry, a
prompt habit).

### 8. Constrain LLM output to data, not prose

Wherever possible, prompt the LLM to produce a table / TSV / JSON
(concrete, comparable) rather than rules-in-code. Tables are easy
to spot-check; rules embed assumptions that compound silently.

### Unifying principle

Shift validation from *"does the rule sound right"* to *"does the
rule's empirical output set match what we want."* LLMs are
excellent at the former and unreliable at the latter — the
workflow has to compensate by routing every proposed heuristic
through a confrontation with data before it gets committed.

## Workflow integration in this repo

Concrete touchpoints — things that already exist or are cheap to
add — that operationalise the principles above.

### When introducing a new heuristic

A "challenge protocol" to run before merging any priority / sort /
fallback / filter rule:

1. **Inputs.** Enumerate or sample the population the rule will
   act on. For dictionary heuristics: every multi-POS lemma in
   the kaikki dump that matters for top-N. For tokenisers: a
   randomly sampled paragraph set.
2. **Outputs.** Generate the rule's outputs across that sample.
   Write them to a file you can scan.
3. **Counterexamples.** Manually (or with an LLM critic) identify
   cases where the rule chose poorly. If any are common-frequency
   inputs, the rule is broken — redesign or fall back to baseline.
4. **Golden anchors.** Convert at least the cases discovered in
   step 3 into golden-set entries (`golden_glosses.tsv` or the
   nearest equivalent for that domain). The audit becomes a
   durable test.
5. **Baseline diff.** Run the same outputs under the baseline rule
   (no priority, identity, source-natural-order) and compare. If
   the proposed rule isn't strictly better, drop it.
6. **Land.** Commit only after steps 1–5.

The key is that steps 1–5 are *mandatory*, not optional. Skipping
them is the failure mode this whole document is trying to prevent.

### When a wrong output surfaces

Treat every user-found wrong card / wrong gloss / wrong fact as a
two-step job, not one:

- **Fix the immediate case.** Add a HAND_OVERRIDE / amend the
  rule / patch the data.
- **Capture as a guard.** Add a golden-set entry, extend a noise
  pattern, or add a runtime check. The same shape of bug must
  cost less to catch next time.

If the wrong output is genuinely outside the existing checks'
ability to detect, that's a signal to extend the validator —
not just patch the data and move on.

### Standing checks

The `frequency/` validator suite is the running embodiment of
this:

- `validate_deck.py` — mechanical lints (noise patterns,
  inflected-leak detection, etc.) — Layer 1 / 2 / 3 of the
  validation strategy in `frequency/validate_deck.py`'s docstring.
- `golden_glosses.tsv` — the durable audit for dictionary lookups.
- `validate_lemmas.py` — separate sanity pass for lemma quality.

For other domains (topics/, cards/sakayan/), parallel infra:

- `.claude/skills/citation-check/check.py` — verifies every
  `verbatim_quote` fragment in topic files against the source
  JSONL. This is the citation-equivalent of golden glosses:
  a mechanical truth check at audit time.
- `.claude/skills/critic-pass/lint.py` — schema validation
  (frontmatter consistency, [#N] reference resolution, attestation
  rules). The schema-equivalent of the noise-pattern filter.

### Prompt-time habits

When working with the LLM (Claude Code, here) on heuristics-heavy
edits:

- "Before you write the rule, list 10 inputs where it might fail."
- "Show me the output of this rule across the existing dataset."
- "What's the simplest baseline this rule should beat?"
- After implementation: "Critique this rule. Where would it pick
  the wrong answer?" — best run as a separate critic agent so the
  framing isn't anchored on the original implementation.

### When NOT to apply this

The protocol scales with the *blast radius* of the heuristic, not
with line count. Use judgment:

- **Heuristic that affects every output** (POS priority, sort key
  for the deck, lemmatiser rule): full protocol, golden anchors,
  baseline diff. These are exactly the rules that ship subtle bugs.
- **One-off filter for a known-bad pattern** (skip alphabet-letter
  prose): no audit needed; the pattern is named, the population is
  small.
- **Pure mechanical refactor** (rename, type cleanup, extract
  function): no audit needed; behaviour-preserving.

If a change blends a refactor and a heuristic, treat the heuristic
as the gating part.

## Worked examples

Real cases that illustrate the failure mode in action and what
citation-grounded answering would have looked like instead:

- `research/2026-05-09-tweet-llm-comparison.md` — four LLM
  answers to a slang-heavy Pashinyan-tweet, four different
  glosses for the pivotal word `խոտ`, all stated with high
  confidence and no acknowledgment of uncertainty. The grammar
  + register-marker layers converged across all four; the
  lexicon layer diverged wildly. Argues for the topic-graph
  direction: pre-training has the structural side covered; the
  citation-grounded value is concentrated in slang / dialectal /
  domain-specific lexicon entries.

## Cross-references

- `frequency/validate_deck.py` — Layer 1/2/3 implementation of
  ambiguity flagging + golden-set check.
- `frequency/golden_glosses.tsv` — current golden set (seeded
  during the 2026-05-09 audit; growing).
- `frequency/dictionary.py` — the lookup whose POS-priority bug
  motivated this doc.
- `kb-design.md` — agent-workflow design for the topic graph;
  the citation-check / critic-pass infra there is the
  topic-domain analogue of the validator suite here.
- `anki-design.md` — card-design decisions and the request log
  that surfaced the wrong-gloss reports in the first place.
