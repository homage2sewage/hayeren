---
id: 2026-06-13-001
date: 2026-06-13
caught_by: human
caught_during: tutor-query
severity: minor
disposition: llm-error
category: prose-overreach
subcategory: unfounded-characterization-and-mis-scoped-remediation
phenomenon: genre-and-date-attribution-from-prior; remediation-misrouted-and-narrow
related_topics: []
related_pitfalls:
  - llm-workflow.md#11-the-validator-is-itself-a-heuristic-audit-it-recursively
  - errors/2026-06-07-001-distributive-a-spurious-morpheme.md
  - errors/2026-05-14-001-self-falsifying-illustrative-example.md
status: open
mitigation:
  type: manual-discipline
  ref: memory/feedback_no_decorative_flourishes.md
recurrence: pattern-of-N
---

## Input

In a chat about what ghamoyan says regarding `մտապահել`, the model
(Fable 5) reported that the word appears inside a quotation ghamoyan
takes from another work (footnote 39, p61). Asked "what kind of
manual is that?", it retrieved the footnote — *Ա. Սարգսյան,
Ս. Համբարձումյան, Հայոց լեզուն և խոսքի մշակույթ, Ե., 2012, էջ 51* —
and characterised the source.

## What the LLM produced

Three layered claims, none in the cited bytes:

1. **"1960s-style usage-manual prose"** — an invented date. The
   source is a 2012 textbook.
2. **"manual"** — an invented genre. The bytes give a *title*
   (`Հայոց լեզուն և խոսքի մշակույթ`); "manual" was supplied from
   prior. It is a course textbook (учебник), not a reference
   handbook. The word then propagated: the operator adopted it
   ("what kind of *manual*…"), so the unsupported term seeded the
   shared vocabulary.
3. **A whole paragraph** ("this paronym advice is the repo's entire
   methodology…") spun out of a two-line paronym admonition —
   manufactured significance, not a found observation.

When corrected ("you called a textbook a '1960 manual'…"), the
model produced multiple paragraphs *defending* the guess as "safe
genre inference" rather than conceding.

## What was correct

The bytes support only: authors, title, city, year, page (footnote
39, ghamoyan p61 y504-511). Everything past that — date, genre,
significance — was prior. Footnote 40 (p61 y518-522) does correctly
point to ghamoyan's own Appendix 3, which the corpus locates at
**ghamoyan p114-115** ("ՀԱՎԵԼՎԱԾ 3. ԲԱՌԵՐԻ ՃԻՇՏ ԸՆՏՐՈՒԹՅՈՒՆ",
opening on the `պահպանել`/`պաշտպանել` pair) — note the model's
in-passing "around pp. 107+" estimate for that appendix was also
wrong and also self-corrected.

## Why this happened

Surface: `prose-overreach` (F8 / the `feedback_no_decorative_flourishes`
class) — characterising words supplied from prior read as analysis.
This is the same shape as `2026-05-14-001` (self-falsifying example):
fluent continuation emits the attractive ornament; there is no
gate that asks "is this in the bytes? is it load-bearing?"

But the **novel, schema-relevant** content is two failures of the
*remediation itself*:

1. **Mis-routed.** The model logged the lesson to a `memory/`
   feedback note, not to `errors/`. The memory mechanism is
   foregrounded in the harness with a literal "after feedback,
   save it" trigger; `errors/` is a less-salient project
   convention requiring more ceremony (schema, test case, index
   regen). The model took the primed/cheaper artifact, which is
   precisely the *lighter* path that routes **around** the system
   built to make a fix durable (`errors/` is where a user-found
   failure becomes a guard; a memory note is a private aside).

2. **Mis-scoped — the recursive-narrowness failure of
   `llm-workflow.md` §11.** The captured lesson named "1960s"
   (the flashy modifier) and the entry headline treated *that* as
   the error, while **"manual"** — the load-bearing wrong noun the
   user had put in quotes in the very same correction — was folded
   under "decorative flourishes" and never addressed until a
   *second* operator prompt ("was 'manual' a good word choice?").
   The chosen frame ("decorative flourishes") is shaped to miss
   "manual": a flat, plausible genre noun is not decorative, so a
   future read of that note would re-emit it. The guard caught only
   the case that motivated it — exactly the §11 whitelist-rot the
   repo already documents.

Meta (not separately logged): the same failure reproduced one level
up. When a second model explained *why* the remediation mis-routed,
it asserted a motivational story ("entering the errors/ log is
self-incrimination as a deliberate act") that it had no access to —
confabulation produced while explaining confabulation.

## Mitigation

Immediate: this entry (the durable capture the memory note should
have been); the memory note retained as the prompt-time discipline.
The "manual"/"1960s"/significance claims were conceded in-session.

Durable (open): no mechanical guard exists for answer-time
ungrounded prose. The correct structural rule — broader than the
memory note's "flourishes" — is: **any characterising word supplied
that is not in the cited bytes (genre, date, significance) is an
uncited claim, gated identically to a slang gloss.** The fit
analysis for what catches this lives in
`research/2026-06-13-answer-verification-architecture-fit.md`.

## Lesson

Three compounding layers, each its own guard:

1. **The claim.** Characterising nouns/dates/significance are
   citations-or-cut, same as glosses — not exempt for being prose.
2. **The remediation routing.** A user-found failure belongs in
   `errors/` (the guard-building system), not only in `memory/`
   (the private aside). Logging to the lighter artifact is itself
   a failure mode.
3. **The remediation scope.** When a correction names one error,
   sweep the *same sentence* for siblings of the same class before
   declaring the lesson captured — the §11 rule applies to the
   error-capture step, not only to producers. "1960s" was patched;
   "manual," sitting beside it, was not. The fix is a *propagation*
   step, mechanizable with zero affect.
