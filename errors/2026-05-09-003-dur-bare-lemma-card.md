---
id: 2026-05-09-003
date: 2026-05-09
caught_by: human
caught_during: review
severity: minor
disposition: tooling-bug
category: tooling
subcategory: mwu-detection-miss
phenomenon: armenian-multi-word-units-with-aux-interpolation
related_topics:
  - topics/syntax/dative_experiencer.md
related_pitfalls: []
status: mitigated
mitigation:
  type: schema-change
  ref: frequency/build_deck.py
recurrence: first-seen
---

## Input

User reviewing `cards/top_1000.tsv` rank 319:

```
դուր	liking (only in 'դուր է գալիս' = it pleases / нравится)
```

User reaction: "the whole phrase should be there."

## What the LLM produced

Card with bare-lemma `դուր` as the headword and a parenthetical
"(only in X)" hint as the gloss. The lemma alone is a poor
card unit because:

- `դուր` outside the phrase has rare dictionary senses
  ("flat," "chisel" per kaikki) that don't reflect why it
  ranks top-1000.
- The frequency rank comes entirely from the verbal idiom
  `դուր գալ` "to please / be liked"; a learner studying
  bare `դուր` learns nothing useful.

## What was correct

The card should display the full phrase as the headword:

```
դուր գալ	to please, be liked — dative-experiencer construction:
'X-ին դուր է գալիս Y' = 'X likes Y' (lit. 'pleasing comes to X
about Y'). Conjugate գալ; դուր is invariant. Aor: դուր եկավ.
```

## Why this happened

The MWU regex in `build_ours.py` matches literal
`դուր գալ` (adjacent tokens) but auxiliaries always
interpolate between the two halves in inflected forms (`դուր
է գալիս`, `դուր եմ գալիս`, `դուր եկավ`, `դուր է եկել`). So
real-text occurrences are never adjacent; the MWU never gets
detected; only the bare first half (`դուր`) accumulates token
counts, which then ranks high in the frequency list.

This is a pure tooling limitation — the lemmatiser counts
half of an idiom as a unit. Likely affects other Armenian
psych-verbs in the same `noun + գալ/տալ/անել` pattern (`քուն
գալ`, `սով գալ` if it's a real construction, `ցավ գալ`).

## Mitigation

Two-part fix in `frequency/build_deck.py`:

1. **DISPLAY_OVERRIDES** dict added — for cases where the
   frequency-list lemma is misleading as a card headword,
   map the lemma to a corrected display string. Currently:
   ```python
   DISPLAY_OVERRIDES = {"դուր": "դուր գալ"}
   ```
   `annotated_lemma()` now consults this when emitting the
   Armenian column. The HAND_OVERRIDES key stays as `դուր`
   (matching the frequency-list rank), so the lookup keeps
   working; only the *displayed* surface changes.

2. **HAND_OVERRIDES gloss** for `դուր` rewritten as a proper
   verbal-idiom card explanation (dative-experiencer
   construction, conjugation pattern, Russian parallel) —
   not a "(only in X)" parenthetical hint.

Plus durable layer: `topics/syntax/dative_experiencer.md`
(written same day) covers the construction with multi-source
attestation (parnasyan + tioyan + ghamoyan).

## Test case

```sh
python3 frequency/build_deck.py
grep -E "^(դուր	|դուր գալ	)" cards/top_1000.tsv
```

Expected output:

```
դուր գալ	to please, be liked — dative-experiencer construction…
```

Failure mode (pre-mitigation): bare-lemma `դուր` headword
with awkward `(only in X)` gloss form.

## Notes

Worth a sweep over `cards/top_1000.tsv` for other
`bare-noun-half-of-MWU` cases. Candidates from the
`MWUS` list in `build_ours.py` and from the dative-experiencer
psych-verb family:

- `քուն գալ` ("to feel sleepy") — if `քուն` ranks bare,
  same pattern.
- `ցավ գալ` ("to be in pain") — same.
- Other Armenian compound verbs with auxiliary interpolation.

Sweep deferred until another instance surfaces; this entry
documents the *shape* of the bug for future reference.
