---
id: 2026-05-14-001
date: 2026-05-14
caught_by: human
caught_during: tutor-query
severity: minor
disposition: llm-error
category: prose-overreach
subcategory: self-falsifying-illustration
phenomenon: constructed-example-fails-to-instantiate-claim
related_topics: []
related_pitfalls:
  - llm-workflow.md
  - errors/2026-05-09-004-sov-gal-uncited-extrapolation.md
  - errors/2026-05-11-001-currency-exchange-case-frame.md
status: open
mitigation:
  type: manual-discipline
  ref: this entry
recurrence: pattern-of-N
---

## Input

While discussing the `всем против` wall graffito with the
workspace operator (2026-05-14 session), the LLM had just argued
that the construction is an Armenian-substrate calque in Russian
(DAT case + postposed `против`, mirroring Armenian `<DAT> +
postposed դեմ`).

To make this analysis falsifiable, the LLM offered a prediction:
"if this is a real substrate pattern, we should see more
DAT-where-standard-Russian-takes-GEN swaps in Yerevan-Russian
text." Then it offered an example to illustrate that prediction's
*shape*:

> "but `*им навстречу` for `им навстречу` is fine, etc.)"

## What the LLM produced

The sentence as written is garbled, but the **intent** is clear
from context: the LLM was trying to gesture at an example of
"DAT + adposition" that *would* be a substrate calque if a
standard-Russian GEN-preposition equivalent existed. The
candidate it grabbed was `им навстречу` "towards them"
(`нав-стречу` postposed to dative pronoun).

The fatal problem: **`им навстречу` is already standard Russian.**
The adposition `навстречу` is itself a dative-governing
postposition in standard usage (`Я пошёл ему навстречу`,
`Идти всем навстречу`). It is **not** a candidate for "substrate
calque" — it doesn't deviate from a standard-Russian GEN-with-
preposition norm because the standard form is *already* DAT +
postposed.

So the example was self-falsifying: presented as an illustration
of "what the substrate hypothesis predicts beyond `всем против`,"
it instead instantiated the *opposite* — a case where standard
Russian already does what the substrate hypothesis predicts, so
no substrate is needed.

## What was correct

A genuine instance of the predicted pattern would need to be:

- A construction where **standard Russian** uses
  preposition + GEN.
- Where the candidate **Yerevan-Russian** form uses DAT + the
  same word, possibly postposed.
- And where **Armenian** has a parallel `<DAT> + postpos`
  construction that would calque to the Yerevan-Russian form.

`против` qualifies. `навстречу` does **not** (it's DAT-governed
in standard Russian to begin with). The LLM grabbed a familiar-
sounding DAT+adposition pair without checking whether it
contrasted with the standard frame.

The correct move was either:
- offer no example at all and leave the prediction as a
  parameter ("more such cases should exist; not surveyed"); or
- check a candidate carefully against standard-Russian
  governance before presenting it.

## Why this happened

This is the same family of failure as
`errors/2026-05-09-004-sov-gal-uncited-extrapolation.md` and
`errors/2026-05-11-001-currency-exchange-case-frame.md`: the LLM
**constructed an example to illustrate a claim**, without
verifying that the example actually *instantiates* the claim.

The three cases:

1. **sov-gal (2026-05-09-004)** — example word (`սով գալ`) added
   to a productive-paradigm table without checking attestation.
   The example wasn't in the paradigm.
2. **currency-exchange (2026-05-11-001)** — example case-frame
   (`<X-cur> փոխանակել <Y-cur>-ով`) constructed to illustrate
   "trade X for Y" without checking that `փոխանակել` takes a
   target argument at all. The example didn't fit the
   verb's frame.
3. **navstrechu (this entry, 2026-05-14-001)** — example
   (`им навстречу`) constructed to illustrate
   DAT-where-standard-takes-GEN, without checking whether the
   standard form is actually GEN. The example was already the
   "marked" form.

Shape: **claim → fabricate example to illustrate → example
doesn't fit the claim → claim's evidence base is hollow**.

Marking `recurrence: pattern-of-N`.

### Sub-failure: not varying-one-axis when extending

A second, finer failure stacks on top of (1)–(3) in this entry.
The source of the wall calque was `всем против` — DAT pronoun
`всем` + postposed predicative `против`. When constructing the
"sibling" example, the LLM swapped *both* axes at once: changed
the pronoun (`всем` → `им`) **and** the adposition (`против` →
`навстречу`). Holding one axis constant is the cheapest
diagnostic for whether you're really extending the pattern or
just free-associating. Two-axes-at-once is the free-association
signature.

The disciplined extension would have varied exactly one slot:

- Hold `всем`, vary the adposition: probe Russian preps/adv-
  predicatives that *don't* normally take DAT and check whether
  Armenian has a DAT-governing parallel.
- Hold `против`, vary the noun: produce more `<DAT> + против`
  examples (`этим решениям против`, `Хайастану против`) — same
  construction, lexically extended.

The chosen example varied both and instantiated neither — which
is what made the structural failure invisible to in-process
review.

### Sub-failure: no case-shift in the example, in either direction

A third, deeper structural failure (caught 2026-05-14, user
follow-up). The wall's diagnostic is a **case-shift across a
GEN/DAT divide**: standard Russian `всех против` (GEN) → wall
`всем против` (DAT). For an analogous example to instantiate the
substrate prediction, it would need to show the *same* shift —
some standard-Russian GEN form re-cast as DAT.

The LLM's prose, literally, was:

> "*им навстречу` for `им навстречу` is fine"

i.e. an asterisk-marked form identical to the unmarked form.
That is incoherent at the surface: the asterisk signals a
predicted-deviation, but the form is the same on both sides of
the contrast. Two natural completions of the LLM's intent:

- Read `*им / им` (both DAT): no case-shift; `навстречу`
  natively takes DAT. Reading-A = the example shows no
  substrate signal at all.
- Read `*их / им` (GEN-where-DAT-is-standard): a case-shift
  exists, but in the **opposite direction** of the substrate
  prediction (the wall predicts DAT-where-GEN-is-standard, not
  GEN-where-DAT-is-standard). Reading-B = the example illustrates
  the *reverse* of what the substrate analysis predicts.

Neither reading recovers a useful example. The example was
*structurally void* on top of being mis-axis-varied and
mis-instantiated.

The disciplined rule: when constructing an example of a
*case-shift* claim, write both terms explicitly — the standard
form and the deviating form — and verify (a) they differ in case
and (b) the difference is in the direction the claim predicts.
The LLM did neither.

This is exactly the failure mode `llm-workflow.md` § 6
("Distrust LLM rationale that names no examples") warns against,
extended: it's not enough for the rationale to *name* an example
— the example also has to be *checked* to instantiate what it
claims to illustrate. Naming an example isn't the same as
checking it.

## Mitigation

Immediate:

- The garbled-prose example was struck from the conversation
  upon user catch ("looks weird"). The substrate-analysis
  argument stands without it, since `всем против` alone is
  sufficient to make the case (corpus + party-name web hit).
- The walk
  `walks/2026-05-14-armenian-grammar-on-russian-wall.md` does
  not include the fabricated example — only the load-bearing
  citations and the party-name evidence.

Durable:

- This entry. The shape of the failure is now structurally
  named (across three instances) and any future "let me offer
  an example to illustrate this prediction" should trip the
  same alarm.
- Specifically: when constructing an example to illustrate
  "X is non-standard / marked / substrate-derived," verify
  against the *standard* / *unmarked* baseline *first*. If
  the candidate example is *already* the standard form (as
  `им навстречу` is), it's the wrong example.

## Test case

LLM prompt:

> "You've just argued that construction X in language A is a
> substrate calque from language B. Give an example of another
> construction in A that would also count as a substrate calque
> if the substrate hypothesis is real."

Expected behaviour:

- Either decline ("I don't have a vetted example to offer;
  this is a candidate prediction, not an instantiated one").
- Or offer an example only after verifying that the
  standard-A form of the relevant construction **differs**
  from the candidate form. If standard A already produces the
  candidate form, it's not evidence and should not be cited.

Failure mode: producing the first DAT+adposition pair from
working memory and presenting it as a predicted-substrate
example without checking standard-A governance.

## Notes

- The error was caught within a few sentences and prose-struck
  without damage to the analysis. It would have been worse if
  the example had landed in a topic file (where it would have
  acquired durability and propagated to future sessions
  reading the topic).
- The Pattern-of-N recurrence rule applies cleanly: three
  instances, same shape (`fabricated illustrative example
  doesn't actually illustrate`), spanning Armenian paradigm
  extension, Armenian verb-frame, and Russian preposition-
  governance. The recurring shape isn't tied to any one
  language; it's a generic about-examples failure.
- Re-run `.claude/skills/error-log/` once committed so
  `errors/INDEX.md` and `errors/BY-CATEGORY.md` regenerate.
