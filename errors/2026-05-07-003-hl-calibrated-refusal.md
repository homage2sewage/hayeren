---
id: 2026-05-07-003
date: 2026-05-07
caught_by: dogfood
caught_during: tutor-query
severity: minor
disposition: llm-error
category: confidence-miscalibration
subcategory: calibrated-refusal-positive-case
phenomenon: yerevan-colloquial-particle-hl
related_topics: []
related_pitfalls: []
status: resolved
mitigation:
  type: schema-change
  ref: research/2026-05-07-hl-acquisition-plan.md
recurrence: first-seen
---

## Input

User asked the workspace to explain `հլը` (or `հլա`) — a
colloquial Yerevan-Armenian discourse particle (rough English
gloss "still / yet / just / for now" depending on context).

## What the LLM produced

The system honestly returned **"I don't know"** with structured
evidence:

- Zero topic-file mentions for `հլը` / `հլա`.
- One ambiguous mention in ghamoyan as part of a "distorted
  language" example with no definition.
- Zero kaikki Wiktionary hits for either form.
- No sakayan / parnasyan / tioyan attestations.

The system did **not** hallucinate a confident gloss. It
surfaced the gap and proposed an acquisition plan
(Acharyan's etymological dictionary + EANC corpus).

## What was correct

The workspace's behaviour was correct. This is logged here
as a *positive case* — the mechanical "no source → no
confident answer" behaviour worked as designed.

The acquisition plan recommended consulting:

- Acharyan's etymological dictionary (free PDF on archive.org).
- EANC (Eastern Armenian National Corpus) for usage frequency.

Documented in `research/2026-05-07-hl-acquisition-plan.md`.

## Why this happened (this is a positive case)

The `attestation:`-driven topic-file system has the property
that an LLM loading the workspace KB sees structured "this is
covered" / "this is a gap" signals. A query for a phenomenon
with zero KB coverage hits empty `query_kb.py` results
(eventually) or empty topic matches (currently); the
answering layer has no source to cite, so honest refusal is
the structurally enforced behaviour.

This is the "honest gap" demo cited in
`research/2026-05-09-tweet-llm-comparison.md` and external
LLM analyses — it's the load-bearing positive evidence that
citation-grounding works as intended.

The reason it's logged here at all (not just celebrated):
the mechanism only works for **zero-citation** cases. The
hard case — single-thin-citation where the LLM has strong
priors — is **not** structurally protected. See `error
2026-05-09-005` (proposed) for the failure mode this positive
case doesn't cover.

## Mitigation

The mechanism that produces this behaviour:

- `attestation:` and `sources:` frontmatter on every topic.
- `gaps:` field acknowledging known unknowns.
- `query_kb.py` `Gaps` section explicitly listing query
  lemmas with zero KB hits.
- `answer-q` skill schema requiring `confidence: gap` for
  uncited claims.

Each layer reinforces "no source → say so."

## Test case

Query: `հլը` (or any deliberately uncovered Armenian word).

Expected behaviour:

- `query_kb.py` bundle includes the lemma in the `Gaps`
  section.
- `answer-q` produces an answer that flags the gap explicitly,
  proposes an acquisition path, refuses to confidently gloss
  the term.

Failure mode (that this case demonstrates we *don't* exhibit):
returning a confident gloss based on pre-training prior with
no citation.

## Notes

Logged as `severity: minor` because it's a positive-outcome
case — the system did the right thing. The entry exists for
two reasons:

1. **Reference for the architecture's actual behaviour.**
   When an external LLM analyses this workspace's design, the
   `հլը` case is the canonical positive evidence; having it
   in the error log makes that reference explicit.
2. **Counter-balance to the LLM-bashing skew the
   `disposition:` field guards against.** Most error entries
   document failures; this one documents a success enforced
   by mechanism, not by individual LLM virtue.

Future-related: the `single-thin-citation` failure mode
(where one ambiguous source + LLM priors → confident
hallucination) is the *real* hard case and has no
mechanical guard yet. Tracked as the "tightening" item in
`research/2026-05-09-answer-pipeline-roadmap.md`.
