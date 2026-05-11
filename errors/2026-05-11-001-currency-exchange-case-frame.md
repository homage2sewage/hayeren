---
id: 2026-05-11-001
date: 2026-05-11
caught_by: human
caught_during: tutor-query
severity: major
disposition: llm-error
category: prose-overreach
subcategory: uncited-case-frame
phenomenon: service-encounter-construction-fabrication
related_topics: []
related_pitfalls:
  - llm-workflow.md
  - errors/2026-05-09-004-sov-gal-uncited-extrapolation.md
status: open
mitigation:
  type: doc-update
  ref: walks/2026-05-11-currency-exchange-construction.md
recurrence: pattern-of-N
---

## Input

User asked, in a 2026-05-11 session, two related questions:

1. "Is there any source on how to convey 'change 100 dollars to drams'?"
2. (after the LLM's response) "Can we say that the correct
   structure is `<sum> <cur1> փոխանակել <cur2>-ով`?"

Auto-grounding bundles for each prompt surfaced:

- `փոխանակել` attested only once in a contextualised use:
  Sakayan p426, "exchanging glances" (reciprocal frame, single
  argument, no target).
- `փոխանակում` as a noun in Parnasyan p419 (glossary, no usage).
- `փոխել` as glossed `менять / обменивать` in Parnasyan p419.
- `<X-gen> դիմաց` "in exchange for X" attested at Sakayan p443
  (selling context, not specifically with `փոխանակել`).
- No service-encounter dialogue in any of the four books.

## What the LLM produced

In the response to question (1), the LLM offered four candidate
phrasings for "exchange 100 dollars to drams." All four assumed
that `փոխանակել` takes a **two-argument frame** (source-currency
+ target-currency) and disagreed only on how to mark the target:

- `հարյուր դոլար փոխանակել դրամով` (instrumental)
- `հարյուր դոլար փոխանակել դրամի` (dative)
- `հարյուր դոլարը դրամով փոխել` (alternative verb, instrumental)
- `Կարո՞ղ եք հարյուր դոլար փոխանակել դրամի։` (presented as
  most-likely-correct)

The instrumental-on-target reading was specifically packaged as
the LLM's best-guess case-frame.

The LLM did acknowledge in prose that "the case marking is my
best guess — none of the four books witnesses currency exchange
specifically." That hedge was correct but **understated the
problem**: the case-frame itself (two-argument transitive
`exchange X for Y`) was not the issue. The deeper problem was
that the corpus does not witness `փոխանակել` *having* a target
argument at all.

## What was correct

User-supplied environmental datum (Yerevan street signs):

> `տարադրամի փոխանակում` "foreign-currency exchange"

This shows the actually-used Armenian construction:

1. The deverbal-noun form `<X-gen> + փոխանակում` is the standard
   public-sphere formula. The thing exchanged is in the
   **genitive**, modifying the action noun.
2. The verb `փոխանակել` / noun `փոխանակում` takes a **single
   primary argument** (the thing exchanged). This is consistent
   with Sakayan p426's `հայացքներ փոխանակել` "exchange glances"
   — same single-argument, reciprocal frame.
3. The "target" / "in exchange for what" — if named explicitly —
   comes via an **adjunct**, not via case-marking on a second
   verbal argument. The book-attested adjunct shape is
   `<Y-gen> դիմաց` (Sakayan p443).

So `<sum> <cur1> փոխանակել <cur2>-ով` is wrong on two counts:

- The instrumental `-ով` has no corpus or environmental witness.
- The two-argument transitive frame the construction presupposes
  does not exist for `փոխանակել` in the corpus — the verb is
  single-argument; the target is adjunct, not argument.

The natural phrasings, derived from the street-sign genitive
formula + the corpus single-argument verb frame:

- Nominal: `հարյուր դոլարի փոխանակում [դրամի դիմաց]`
- Verbal: `հարյուր դոլար փոխանակել [դրամի դիմաց]`

## Why this happened

Three contributing failures:

1. **The LLM extrapolated a case-frame from pre-training prior
   rather than from corpus evidence.** The instrumental-target
   reading is plausible cross-linguistically (Russian uses
   instrumental in some exchange contexts), and `փոխանակել` *looks
   like* it should be transitive-with-target by analogy with
   English "exchange X for Y." Neither warrants asserting the
   case-frame for Armenian.

2. **The grounding bundle's silence was not treated as a stop
   signal.** The auto-grounding bundle for the first prompt
   correctly returned only the Sakayan p426 reciprocal-frame
   attestation. The LLM noted this in prose but proceeded to
   construct candidate phrasings anyway, smuggling pre-training
   prior past the citation-grounding workflow.

3. **The failure mode is structurally identical to
   `errors/2026-05-09-004-sov-gal-uncited-extrapolation.md`**
   (extrapolating a productive case-frame from limited
   attestations). That entry already named the pattern. This
   instance is its third recurrence in the workspace; marking
   `recurrence: pattern-of-N` (see
   `errors/README.md` § "What gets logged — the tiered rule").

This is exactly the failure mode `llm-workflow.md` § 6
("Distrust LLM rationale that names no examples") describes:
"the case-marking is X" stated without a citation, presented as
"my best guess" but functionally as analysis.

## Mitigation

(`status: open` — durable mitigation pending the service-encounter
topic file)

Immediate:

1. **`walks/2026-05-11-currency-exchange-construction.md`** —
   captures the user observation, the corpus attestations, the
   re-derived single-argument frame, and explicitly names this
   error as a falsified analysis. Provides the durable artifact
   future sessions can ground a service-encounter answer in.

Durable:

2. **A `topics/pragmatics/service-encounter.md` (or equivalent)
   topic file** — does not yet exist. The currency-exchange,
   bag-offer (`Տոպրակ տա՞մ`), and price-asking constructions all
   hit the same uncovered register. Until that topic exists,
   service-encounter questions will keep producing LLM
   pre-training-prior answers with the same shape of error.
   Tracked as a research priority in
   `walks/2026-05-11-currency-exchange-construction.md` §
   "Implications for `topics/`".

3. **Prompt-time habit**: when the auto-grounding bundle returns
   *no contextualised attestation* of the requested verb's
   argument frame, declining to specify the case-marking is the
   correct move. Producing "best-guess" case-frames in this
   condition is the structural error.

## Test case

User question:

> "How do I say 'change 100 dollars to drams' in Armenian? What
> case does the target currency take?"

Expected behaviour:

- Surface corpus attestations of `փոխանակել` / `փոխանակում` and
  flag that the verb's only contextualised use is single-argument
  / reciprocal (Sakayan p426).
- State clearly: the case-marking of a "target currency" argument
  cannot be determined from the corpus, because the corpus does
  not witness `փոխանակել` taking a target argument.
- Cite `walks/2026-05-11-currency-exchange-construction.md` for
  the street-sign-derived nominal formula `<X-gen> փոխանակում` and
  the `<Y-gen> դիմաց` adjunct.
- Recommend the genitive-nominalised formula or defer to native
  speaker / parallel corpus; do *not* propose an instrumental,
  dative, or accusative case-frame for the target as if grounded.

Failure mode: producing a "best-guess" candidate phrasing with a
specific case marker on the target currency, presented as
analysis even when hedged.

## Notes

- The pattern this entry indexes — fabricating case-frames for
  service-encounter constructions the corpus doesn't cover — is
  the third recurrence of the broader uncited-extrapolation
  failure (see `errors/2026-05-09-004-sov-gal-uncited-extrapolation.md`).
  Earlier instances were psych-verb productivity and POS
  priority; this instance is verbal argument structure. The
  structural fix is the topic-file gap closure, not per-instance
  patching.
- Re-run `.claude/skills/error-log/` once committed so the
  `INDEX.md` and `BY-CATEGORY.md` indices regenerate.

## Update — web corroboration (2026-05-11, same session)

A web search on Armenian crypto-exchange usage (Bitcoin.org
Armenian, Hetq, SkyLabs, MediaFactory.am, Wikipedia, ՀՀ Law on
Crypto-Assets) returned **zero instances** of instrumental
`-ով` marking a target currency in an exchange frame. The
positive evidence for the alternative analysis is now:

- **`X-gen դիմաց`** "in exchange for X" attested in three
  independent registers: literary (Sakayan p443), pedagogical
  (Bayramyan 2009 p63), and contemporary financial journalism
  (MediaFactory.am, verbatim: `Կրիպտոյի դիմաց ստանում է դոլար
  կամ դրամ` "in exchange for crypto [one] receives dollar or
  dram").
- **Dative-target on `փոխարկել` / `վերածել`** ("convert into
  Y") attested on Hetq: `Վերածել բիթքոինի ներդրումի` "to
  convert into bitcoin investment" (dative `բիթքոինի`).
- **`փոխանակել`** remains single-argument in web usage too:
  `արժույթների փոխանակում` "exchange of currencies" (gen
  modifier), with no second verbal argument. Confirms the
  corpus analysis (Sakayan p426 reciprocal frame).

The falsification is thus not single-witness (user observation)
but multi-register cross-corroborated. The earlier `-ով`
proposal is conclusively wrong, not merely uncited.

The web findings have been folded into
`walks/2026-05-11-currency-exchange-construction.md` § "Web
corroboration." This entry stays `status: open` until a
durable `topics/` artifact (service-encounter or
cryptocurrency-lexicon) lands; the walk is the interim
reference.
