---
id: 2026-06-07-001
date: 2026-06-07
caught_by: human
caught_during: tutor-query
severity: major
disposition: llm-error
category: language-understanding
subcategory: spurious-morpheme-decomposition
phenomenon: colloquial-copula-a-misanalysed-as-distributive-morpheme
related_topics:
  - topics/morphology/present_tense.md
  - topics/morphology/numeral_forms.md
related_pitfalls:
  - errors/2026-05-14-002-spurious-morpheme-decomposition-on-borrowed-toponym.md
  - errors/2026-05-11-001-currency-exchange-case-frame.md
  - errors/2026-05-09-004-sov-gal-uncited-extrapolation.md
  - errors/2026-05-14-001-self-falsifying-illustrative-example.md
status: mitigated
mitigation:
  type: doc-update
  ref: research/2026-06-06-vote-buying-tweets.md
recurrence: pattern-of-N
---

## Input

While reading a single colloquial-Yerevan tweet (2026-06-06
session, logged in `research/2026-06-06-vote-buying-tweets.md`),
the LLM glossed the token `մարդա` in the clause:

> `... 100000 հայ ... ուղարկելու համար, մարդա 500$`
> "to send 100,000 Armenians..., $500 a head."

## What the LLM produced

Unprompted, in the first-pass answer and the research log, the LLM
analysed `մարդա` as:

> "colloquial distributive `մարդ`+`ա`" / "reading is from
> arithmetic + distributive `-ա`"

i.e. it posited a **distributive morpheme `-ա`** ("per / each")
attaching to `մարդ` "person." The user then adopted this framing
in a follow-up ("also explain distributive ա"), so the invented
category propagated into the user's mental model before being
caught.

## What was correct

The `ա` is the **colloquial 3sg copula `ա` (= literary `է`)**, the
single most-cited Yerevan register marker, documented in
`topics/morphology/present_tense.md` § "Yerevan colloquial: 3sg
auxiliary `ա` for `է`" (ghamoyan):

> "In folk-colloquial language, `ա` is used as a linker [copula]…
> In simple predicates, `ա` replaces the auxiliary `է`."

So `մարդա 500$` = `մարդ ա 500 դոլար`, the copula cliticised to
`մարդ`: "(per) person **is** $500." The **"per / distributive"
sense is constructional** — a bare unit-noun + copula + price
frame ("$500 a head," cf. `հատը 100 դրամ ա` "100 dram apiece") —
not a dedicated morpheme.

There is no distributive suffix `-ա` in Armenian. The genuine
numeral distributive is **`-ական`** (`մեկ → մեկական` "one each",
`երկու → երկուական` "two each").

## Why this happened

Same failure family as `2026-05-14-002` (Քոբուլեթի): **spurious
morpheme decomposition** — a familiar-looking word-final shape
(`-ա`) was assigned a morpheme label without checking (a) the
inventory of real Armenian morphemes with that shape, or (b)
whether a simpler, already-cited analysis covered the form.

Two cheap checks, both skipped:

1. **"Is there a distributive morpheme `-ա` in Armenian?"** —
   the answer (no; the distributive is `-ական`) was a single
   grep / prior-recall away.
2. **"What is the well-attested function of word-final colloquial
   `ա`?"** — the copula. And this is the aggravating factor: the
   present_tense.md `ա`-for-`է` section **was already in the
   auto-grounding bundle** for the original tweet turn (it matched
   on `հայ`, header visible at line 183 of that bundle). The
   corrective citation was on-screen and went unused — the exact
   shape of the canonical `խոտ` case (`2026-05-09-002`): the
   answer was in the bundle, nobody looked.

So this is both a `spurious-morpheme-decomposition` recurrence and
a `confidence-miscalibration` / bundle-ignored instance: a novel
morpheme was *invented* (not merely mis-attached) with no hedge,
while the grounded analysis sat in context.

## Pattern membership

Adds to the workspace's "structural analysis without the cheapest
baseline check" family (see `2026-05-14-002`'s roll-up):

1. `2026-05-09-004` — paradigm extended to uncited member.
2. `2026-05-11-001` — verb case-frame asserted without checking
   argument structure.
3. `2026-05-14-001` — illustrative example that didn't instantiate
   its own claim.
4. `2026-05-14-002` — morpheme boundary asserted without checking
   the stem inventory; + author-gender default (same session).
5. **This entry** — a morpheme *invented* (distributive `-ա`)
   without checking the morpheme inventory or the already-cited
   copula analysis.

The restated discipline-rule from `2026-05-14-002` applies
verbatim and would have caught it:

> **Before asserting a structural analysis, run the cheapest
> possible check on the baseline assumption the analysis rests on
> — even if (especially if) the assumption feels obvious.**

Sharper morphology-specific corollary, now twice-earned: when you
label a word-final string a morpheme, **first confirm that
morpheme exists in the language's inventory with that function**;
a near-identical surface string with a *different*, better-attested
function (here: copula `ա`) is the default trap.

## Mitigation

Immediate:

- `research/2026-06-06-vote-buying-tweets.md` `մարդա` row rewritten
  to the copula analysis + constructional "per" reading, with the
  `-ա`-is-not-a-distributive note and `-ական` as the real
  distributive.

Durable:

- This entry. `recurrence: pattern-of-N` (fifth in the family).
- No new doc needed beyond the existing present_tense.md copula
  section — the failure was not consulting it, not a gap in it.

## Test case

Future LLM prompt:

> "Explain `մարդա` in `մարդա 500$` (Yerevan colloquial)."

Expected behaviour:

- Parse `ա` as the colloquial 3sg copula (= `է`), citing
  `topics/morphology/present_tense.md`.
- Attribute the "per person / a head" sense to the bare-unit-noun
  pricing construction, not to a suffix.
- If tempted to call `-ա` a "distributive," check the morpheme
  inventory first and recall the real distributive is `-ական`.

Failure mode: inventing a distributive morpheme `-ա` and/or
ignoring the copula analysis already present in the grounding
bundle.

## Notes

- Caught by user follow-up ("so ա as distributive should be logged
  as error i guess"). Reached the user's answer and a research log
  (hence `major`), but not a topic/card; corrected same session.
- Re-run `.claude/skills/error-log/build_index.py` once committed
  so `errors/INDEX.md` and `errors/BY-CATEGORY.md` regenerate.
