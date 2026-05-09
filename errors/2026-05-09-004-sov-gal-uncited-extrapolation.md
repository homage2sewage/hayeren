---
id: 2026-05-09-004
date: 2026-05-09
caught_by: human
caught_during: tutor-query
severity: major
disposition: llm-error
category: prose-overreach
subcategory: uncited-extrapolation
phenomenon: dative-experiencer-construction-productivity
related_topics:
  - topics/syntax/dative_experiencer.md
related_pitfalls:
  - llm-workflow.md
status: open
mitigation:
  type: doc-update
  ref: topics/syntax/dative_experiencer.md
recurrence: first-seen
---

## Input

In writing `topics/syntax/dative_experiencer.md` (the topic file
covering `դուր գալ` and related psych-verbs), the LLM listed a
table of "other psych-verbs in the same construction":

```markdown
| construction | meaning | structure |
|---|---|---|
| `քուն գալ` | "to feel sleepy" | `Ինձ քուն է գալիս` |
| `սով գալ` | "to feel hungry" | `Ինձ սով է գալիս` |
| `ցավ գալ` | "to be in pain" | `Ինձ ցավ է գալիս` |
```

The `gaps:` field flagged that "the cross-verb generalisation
isn't book-attested," but the body still presented the table
as if all three constructions were equivalent in usage.

User pushback shortly after the topic was written:

> "what's the difference between սոված եմ and սով եմ գալիս"

## What the LLM produced

The topic file's table treated `սով գալ` as a productive
member of the dative-experiencer psych-verb family. In a card
gloss elsewhere it noted "Russian-parallel: 'Y нравится X-у'."

Implication taken from the table: a learner could form `Ինձ
սով է գալիս` "I'm getting hungry" by analogy with `Ինձ քուն է
գալիս` "I'm getting sleepy" and have it be standard.

## What was correct

`Սոված եմ` (adjective + copula, "I am hungry") is the
ubiquitous, dominant form for "I'm hungry" in Eastern Armenian.
The dative-experiencer with `սով` is **not standard** and is
not book-attested in any of our four corpora. Native speakers
seem to say `սոված եմ դառնում` "I'm becoming hungry" or
`քաղց եմ զգում` "I'm feeling hunger" rather than `Ինձ սով է
գալիս`.

The construction *is* productive for some psych-state nouns
(`քուն գալ` is real and very common; `ցավ գալ` exists) but
not uniformly across the lexicon. Hunger specifically
prefers the participial-adjective `սոված` route.

## Why this happened

The LLM extrapolated from one robustly-attested pattern
(`դուր գալ`, `քուն գալ`) to a broader class without
verification. Each individual entry "felt right" by
syntactic analogy, but lexical productivity in psych-verb
constructions doesn't follow simple analogy — it's idiomatic
per-noun.

Specifically:

1. The `gaps:` field correctly named the lack of book
   attestation but the body presentation made the
   constructions look equivalent anyway.
2. No KB grep was run for `սով գալ` / `սով է գալիս` before
   adding the row to the table — would have shown zero
   corpus hits.
3. The LLM's pre-training prior on "Armenian psych-verbs use
   gen/dat experiencer + come" overrode the duty to verify
   per-lexeme.

This is exactly the failure mode `llm-workflow.md` § 6
("Distrust LLM rationale that names no examples") describes:
"It's standard to use X-construction with Y" is the
LLM-typical claim that needs adversarial confrontation.

## Mitigation

(`status: open` — mitigation pending)

Proposed two-part fix:

1. **Update `topics/syntax/dative_experiencer.md`** to remove
   `սով գալ` from the affirmative table. Demote to "uncertain
   — possibly used by analogy with `քուն գալ`, but not
   attested and natively likely replaced by `սոված եմ
   դառնում`." Similarly hedge `ցավ գալ` until corpus-verified.
   Update `gaps:` field to record this audit.

2. **Update `topics/syntax/dative_experiencer.md` `gaps:`**:
   add an entry naming this audit explicitly, so future
   readers see the construction's productivity as an open
   question rather than a settled generalisation.

Durable: lemma-by-lemma, the construction's productivity
should be verified against the four-book corpus before a
psych-verb row gets added to the topic table. The lookup is
cheap (one grep per candidate); skipping it is the failure
mode.

## Test case

User question:

> "What's the difference between `սոված եմ` and `սով եմ
> գալիս`?"

Expected behaviour:

- `Սոված եմ` — confirm as standard, ubiquitous "I am hungry."
- `Սով եմ գալիս` — flag as ungrammatical (1sg auxiliary
  doesn't fit dative-experiencer; that would be 3sg `Ինձ սով
  է գալիս`).
- The dative-experiencer form for hunger is not standard;
  native form is `սոված եմ դառնում` or `քաղց եմ զգում`.
- Acknowledge this reveals a workspace audit signal: the
  topic file's psych-verb table over-generalised.

Failure mode: confidently confirming `սով գալ` as a regular
member of the dative-experiencer family without flagging the
audit gap.

## Notes

Logged with `status: open` because the mitigation (the topic-
file edit) hasn't been committed yet. Will flip to
`mitigated` once the edit lands. Recurrence is `first-seen`
in this exact form — though the underlying pattern (LLM
extrapolating from a small attested set to a broader claim)
is the structural failure mode behind several earlier
errors on this project.
