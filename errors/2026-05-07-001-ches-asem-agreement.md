---
id: 2026-05-07-001
date: 2026-05-07
caught_by: human
caught_during: drafting
severity: major
disposition: llm-error
category: language-understanding
subcategory: agreement-mismatch
phenomenon: armenian-verb-agreement-back-transliteration
related_topics:
  - topics/morphology/negation.md
related_pitfalls:
  - transliteration-notes.md#pitfall-2-agreement-mismatch-from-naive-back-transliteration
status: mitigated
mitigation:
  type: doc-update
  ref: transliteration-notes.md
recurrence: pattern-of-3
---

## Input

User wrote `ches asem`, intending "you won't say" (English / Latin
transliteration of intended Eastern Armenian).

## What the LLM produced

Naive segment-by-segment back-transliteration:

- `ches` → `չ` + `ես` = `չես` (2sg negative auxiliary "you aren't").
- `asem` → `ասեմ` (1sg subjunctive "let me say" / "(I) might say").
- Concatenation: `չես ասեմ`.

Then translated this as "you won't say" without flagging that
the auxiliary is 2sg but the lexical verb's ending is 1sg
subjunctive — broken agreement.

## What was correct

`չես ասի` (`ches asi`) — negative hypothetical 2sg of `ասել`
"to say."

Pattern: `չ` + auxiliary + **negative participle** in `-ի/-ա`.
- 2sg form: `չ` + `ես` + `ասի` = `չես ասի`.

## Why this happened

Token-level transliteration with no syntactic agreement check.
The LLM segments morphemes locally, finds plausible matches for
each, concatenates without verifying that the auxiliary's
person/number agrees with the lexical verb's ending. The `-եմ` /
`-ես` / `-ի` endings are person markers in some contexts and
subjunctive endings in others; disambiguating requires
sentence-level analysis the LLM isn't doing.

The diagnostic: when the auxiliary's person/number disagrees
with the lexical verb's ending, the agreement is broken — that's
the signal a different parse is needed.

## Mitigation

Documented as canonical pitfall in `transliteration-notes.md` §
"Pitfall 2: agreement mismatch from naive back-transliteration"
and § "The canonical example, end-to-end: `ches asem`."

Heuristic added: hypothetical-mood negation pattern is
`չ + auxiliary + negative participle in -ի/-ա`. Surface the
back-transliteration explicitly and check agreement before
returning.

The mitigation is doc-only; not yet skill-enforced. A future
back-transliterate skill should run agreement-check before
proposing a parse.

## Test case

Input: `ches asem`

Expected behaviour:
- Surface ambiguity, propose `չես ասի` as likely intent.
- Flag agreement mismatch on naive parse `չես ասեմ`.
- Ask user to confirm or note both possibilities.

Failure: returns `չես ասեմ` and translates to "you won't say"
without acknowledging the agreement break.
