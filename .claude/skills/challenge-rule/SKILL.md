---
name: challenge-rule
description: |
  Run the heuristic-validation protocol before adding any
  priority/sort/filter/fallback/re-ranking rule anywhere in the
  workspace (deck builder, OCR pipeline, topic-graph schema,
  lemmatiser, glossary lookup, transliteration, ...). Forces
  empirical confrontation with the rule's input population
  *before* it ships, instead of via slow downstream user
  feedback. See `llm-workflow.md` for the underlying rationale.
---

# challenge-rule

Mandatory pre-flight for any heuristic that picks one option
from a candidate set. Generalises across domains: dictionary
POS-priority, OCR column-split rules, lemma-folding rules,
topic-graph attestation thresholds, etc.

## When to invoke

Trigger this skill BEFORE you write the rule, not after. If you
notice you're about to introduce one of:

- A priority / preference / sort key
- A "prefer X over Y when both apply" branch
- A filter / noise-pattern / blocklist
- A fallback chain
- A threshold (e.g. "attest as `multi-attested` when ≥2 books")
- A re-ranking step

…run the protocol. Skipping it is the documented failure mode this
skill exists to prevent (`llm-workflow.md` § "Where this came from").

Do NOT invoke for:

- Pure mechanical refactors (rename, extract function, type
  cleanup).
- One-off filters for a *named* known-bad pattern (e.g. "skip
  alphabet-letter prose") — the population is small and the
  pattern is explicit.
- Bug fixes that revert a previously-bad rule to a known-good
  baseline.

The protocol scales with the *blast radius* of the heuristic, not
with line count.

## How to invoke

```
/challenge-rule <one-line description of the proposed rule>
```

or, when interacting conversationally with Claude:

> "Run the challenge protocol on <proposed rule>."

There's no executable script — the skill is a *workflow protocol*
that Claude (or you) walks through interactively.

## The protocol

Six steps, mandatory in order:

### 1. Inputs

Enumerate or sample the population the rule will act on. Be
specific about the size and the source.

- Dictionary heuristics → "every multi-POS lemma in
  `frequency/data/armenian.jsonl`" (~6500 entries) or "every
  lemma at rank ≤1000 in `cards/top_1000.tsv`."
- OCR heuristics → "10 randomly sampled pages from
  `<book>/<book>.pdf`."
- Topic-graph heuristics → "every topic file currently under
  `topics/`."
- Lemma-folding heuristics → "every word-form pair in the
  generated `out/our_top_1000.tsv`."

The point: name the actual file or query that produces the input
set. "Average usage" is not an input population.

### 2. Outputs

Run (or hand-execute) the rule across the sample and write outputs
to a file you can scan. Format: one input per line, with the
rule's chosen output, plus enough context to judge correctness
(e.g. the alternative options the rule rejected).

For dictionary POS-priority, the sample table looks like:

```
lemma         picked-pos  picked-gloss     other-glosses
տարեկան       noun        rye              adj:annual,yearly | adv:yearly
բաց           noun        Bats (language)  adj:open
արի           verb        imp. of գալ      adj:valiant | noun:Aryan
…
```

Tables are reviewable; rules-in-prose are not.

### 3. Counterexamples

Scan the output and identify cases where the rule chose poorly.
Be specific:

- Is the picked output rare / specialist / archaic, while a more
  common sense was rejected?
- Is the picked output a proper noun / language name / ethnonym
  when the rejected sense is a common-noun translation?
- Does the picked output contain noise markers ("inflection of",
  "letter of alphabet", "(language)")?

If the misranked cases include any common-frequency input, the
rule is broken — go to step 5 baseline before considering
step 4 patches.

You can run a critic-agent here (separate prompt: "find words
where this rule produces the wrong gloss") to surface cases the
implementer missed.

### 4. Golden anchors

Convert at least the cases discovered in step 3 into permanent
golden-set entries. Audit becomes a durable test.

- Deck domain → `frequency/golden_glosses.tsv`
- Topic-graph domain → entries in
  `.claude/skills/citation-check/`-tracked example files
- Other → create the analogous TSV at the appropriate
  location and add a corresponding `check_*` to the relevant
  validator.

Adding the golden anchor is the step that makes the audit
*durable*: future LLM-assisted edits and source-data refreshes
can no longer silently regress these cases.

### 5. Baseline diff

Run the same outputs under the trivial baseline:

- For sort/priority rules → no priority, source-natural-order.
- For filters → no filter, full pass-through.
- For fallback chains → just the highest-priority leg.
- For thresholds → the universal answer (always-true /
  always-false).

Compare. If the proposed rule isn't strictly better than the
baseline on the audit set, **drop the rule** — the baseline is
simpler and equally correct.

The noun-promotion rule that motivated this skill failed exactly
here: kaikki's natural order produced better outputs than verb=0,
noun=1, adj=2, … on every common-frequency word in the audit set.
Had we done the baseline diff, we'd never have shipped the rule.

### 6. Land

Commit the rule only after 1–5. Include in the commit message:

- The audit-set size.
- The baseline-diff result.
- The golden-set entries added.

If a future maintainer (or future-you) wants to revisit the rule,
they have the audit data and the test anchors to do so.

## Output

If the protocol passes (rule beats baseline, golden anchors
added), you have:

- The audit table (saveable as
  `research/YYYY-MM-DD-<rule-name>-audit.md`).
- New golden-set entries.
- A defensible commit.

If the protocol fails (rule loses to baseline or has too many
counterexamples), you have:

- A clear "drop the rule" outcome.
- The audit table as evidence for why.
- Optionally, a HAND_OVERRIDES list of the cases where the
  baseline itself misranks — the targeted fix that doesn't
  require a global rule.

## Cross-references

- `llm-workflow.md` — full rationale, principles, and the
  POS-priority case study that motivated this skill.
- `frequency/validate_deck.py` — runtime validators (Layer 1/2/3)
  for the deck domain. Each check there embodies the durable form
  of an audit done at rule-introduction time.
- `frequency/golden_glosses.tsv` — current golden set; the
  living result of past audits.
- `.claude/skills/citation-check/` and
  `.claude/skills/critic-pass/` — the topic-domain analogues:
  runtime validators that gate every topic file's commit.

## When this skill itself needs revision

When you discover a class of heuristic this protocol doesn't cover
(e.g. probabilistic rules, ML-trained classifiers, multi-stage
pipelines where step-3 counterexamples cascade), extend the
protocol. The skill is itself a heuristic; it needs the same
empirical-confrontation discipline.
