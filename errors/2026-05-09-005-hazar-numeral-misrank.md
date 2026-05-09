---
id: 2026-05-09-005
date: 2026-05-09
caught_by: human
caught_during: review
severity: major
disposition: tooling-bug
category: tooling
subcategory: dictionary-pos-misrank
phenomenon: kaikki-natural-order-misranks-numeral-vs-noun
related_topics: []
related_pitfalls:
  - llm-workflow.md#11-the-validator-is-itself-a-heuristic-audit-it-recursively
status: mitigated
mitigation:
  type: schema-change
  ref: frequency/build_deck.py#HAND_OVERRIDES
recurrence: pattern-of-N
---

## Input

User reviewing `cards/top_1000.tsv` rank 150:

```
հազար	lettuce, Lactuca	frequency top-1000 rank-0150 src-dictionary
```

User reaction: "հազար says lettuce, Lactuca, this doesn't make
sense as it's 1000 in the first place, though lettuce is
correct."

## What the LLM produced

`հազար` glossed as `lettuce, Lactuca`. The lemma's primary
modern meaning — the numeral **1000** — was missing from the
card.

## What was correct

`հազար` = "thousand" (numeral, primary sense). The lettuce
gloss is a real but obscure botanical sense (Wiktionary
catalogues `հազար` as also denoting *Lactuca* the lettuce
genus); however, this is the *secondary* sense for a
high-frequency lemma whose top-1000 frequency is entirely
driven by numeral usage.

kaikki entries for `հազար`:

```
noun: lettuce, Lactuca
num:  thousand
```

## Why this happened

Recurrence of the `2026-05-09-001-pos-priority-misranks`
pattern, but with a twist: the previous fix (switch from
`verb=0, noun=1, adj=2` priority to *kaikki natural order*)
assumed kaikki's first listed sense is the dominant one.
For `հազար`, kaikki's natural order *itself* puts the rare
noun before the dominant numeral, so the fix didn't catch
this case.

`check_dictionary_ambiguity` *did* surface this card as an
info-level finding (2 POS senses; the card picked one), but
info-level findings aren't actively reviewed — they're a
log to skim, not a gate. The user found it via dogfooding,
not via the validator.

The general lesson, restated for the third time in this log:
**any heuristic for picking among multiple kaikki senses is
brittle** — sense-rank in Wiktionary doesn't track modern
usage frequency, especially for numerals (often listed *after*
homophone nouns/adjectives on the same page) and for
high-frequency function words.

## Mitigation

Immediate: HAND_OVERRIDE in `frequency/build_deck.py` —
`"հազար": "thousand / тысяча"`. Plus golden-set entry in
`frequency/golden_glosses.tsv` so the regression can't come
back via a kaikki refresh.

Structural: review `info`-level `ambiguous-sense` rows for
the **top 50 lemmas** as a build-time gate, not a passive log.
A 2-POS sense conflict at rank ≤ 50 is high-risk by
construction — those slots are *all* either function words
(unambiguous: hand-override) or content words where the
primary sense matters disproportionately. Promoting top-50
ambiguous-sense from info → warning would have caught this.

Open question: where else does kaikki order misrank?
A targeted audit script that lists every `ambiguous-sense`
card with its competing POSes is a small ask and would
surface other latent landmines before they surface during
review.

## Test case

```python
import sys; sys.path.insert(0, 'frequency')
import dictionary
# Without HAND_OVERRIDE the bug returns:
assert dictionary.lookup('հազար') == 'lettuce, Lactuca'  # bug
# With HAND_OVERRIDE applied, deck row should match:
import csv
for row in csv.reader(open('cards/top_1000.tsv'), delimiter='\t'):
    if row[0] == 'հազար':
        assert 'thousand' in row[1].lower(), \
            f'հազար gloss must include "thousand"; got {row[1]!r}'
        break
```

## Cross-references

- Original entry: `2026-05-09-001-pos-priority-misranks.md`
  (the `տարեկան → rye`, `բաց → Bats` bug class).
- Validator that *should* catch this:
  `frequency/validate_deck.py § check_dictionary_ambiguity`.
- Golden-set anchor:
  `frequency/golden_glosses.tsv` line for `հազար`.
