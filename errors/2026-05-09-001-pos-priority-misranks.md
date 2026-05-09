---
id: 2026-05-09-001
date: 2026-05-09
caught_by: human
caught_during: review
severity: major
disposition: llm-error
category: tooling
subcategory: heuristic-without-audit
phenomenon: dictionary-pos-priority
related_topics: []
related_pitfalls:
  - llm-workflow.md
  - CLAUDE.md#heuristic-validation
status: resolved
mitigation:
  type: validator-update
  ref: frequency/dictionary.py
recurrence: first-seen
---

## Input

Build the `cards/top_1000.tsv` deck from the kaikki Wiktionary
dump. For multi-POS lemmas, pick the best gloss.

## What the LLM produced

Earlier `frequency/dictionary.py` had the implicit rule
"translation glosses are usually nouns," implemented as a
`pos_priority = {"verb": 0, "noun": 1, "adj": 2, "adv": 3, …}`
sort key. For each multi-POS lemma, this picked the noun gloss
when present, falling through to adj only if no noun existed.

Concrete misranks introduced:

- `տարեկան` → "rye" (noun, 3rd POS section in kaikki) instead
  of "annual, yearly" (adj, primary sense).
- `բաց` → "Bats (language)" (noun, marginal Caucasian-language
  sense flagged in kaikki as "incorrect language header")
  instead of "open, not closed" (adj, primary sense).
- `ուղիղ` → "straight line" (noun) instead of "straight,
  direct" (adj).
- `ամսական` → "menstruation, period" (noun) instead of
  "monthly" (adj).
- `արի` → "valiant, brave, manly" (adj, archaic) instead of
  "come!" (verb, imperative — modern dominant sense).

Several others.

## What was correct

For adjective-primary words, the adjective gloss is the right
one. For words where kaikki's natural ordering is non-obvious,
the right rule is to **trust the source's natural order**
(kaikki preserves Wiktionary's editor-curated primary-first
ordering), only deprioritising entries that are rarely the
useful gloss (`name`, `letter`).

Post-fix: `pos_priority = {"name": 90, "letter": 99}`; everything
else equal at 50; Python's stable sort preserves kaikki's
natural order.

## Why this happened

The original priority rule sounded reasonable ("nouns are usually
the right gloss") and was committed without an audit pass over
its actual outputs. The audit, when finally done, was one batch
of ~50 multi-POS lemmas; the failure mode was obvious within
seconds.

Cost of skipping the audit: multiple rounds of user-found
"this card says rye?" / "this card says Bats?" / "this card
says valiant?" over multiple sessions.

This is the canonical case study for `llm-workflow.md` § "Where
this came from" — a heuristic shipped without confronting its
input population, then surfacing as user-found bugs.

## Mitigation

Two layers:

1. **Code fix** in `frequency/dictionary.py`: drop verb/noun/
   adj priorities, preserve kaikki natural order.
2. **Process fix** in `llm-workflow.md` § "Principles" + the
   `challenge-rule` skill: any new priority/sort/filter rule
   must run the 6-step challenge protocol (sample population,
   generate outputs, find counterexamples, golden anchors,
   baseline diff, land) BEFORE shipping. Codified in
   `CLAUDE.md` § "Heuristic validation — non-negotiable."

Plus durable layer: `frequency/golden_glosses.tsv` seeded with
the misranked cases (`տարեկան → annual`, `բաց → open`, `արի →
come`, `ապրես → well done`, etc.). `validate_deck.py`'s
`check_golden_glosses` enforces these — future kaikki refresh
or priority-rule change can no longer silently regress them.

## Test case

```sh
python3 -c "
import sys; sys.path.insert(0,'frequency')
import dictionary
for w in ['տարեկան', 'բաց', 'ուղիղ', 'ամսական']:
    print(f'{w}: {dictionary.lookup(w)!r}')
"
```

Expected output:

```
տարեկան: 'annual, yearly'
բաց: 'open, not closed'
ուղիղ: 'straight, direct'
ամսական: 'monthly'
```

Failure mode: any of these returning the noun-promoted gloss
(`'rye'`, `'Bats (language)'`, `'straight line'`,
`'menstruation, period'`).

Regression test runs as part of `validate_deck.py` via
`check_golden_glosses`.
