---
id: 2026-06-03-001
date: 2026-06-03
caught_by: user
caught_during: review
severity: major
disposition: tooling-gap
category: gloss-sense-selection
subcategory: high-frequency-token-glossed-with-rare-homograph-sense
phenomenon: deck-builder-picks-kaikki-rare-headword-for-grammatical-token
related_topics:
  - topics/morphology/case_system.md
  - topics/phonology/voiced_aspirated_alternation.md
related_pitfalls:
  - errors/2026-05-09-002-khot-slang-divergence.md
  - errors/2026-05-14-002-spurious-morpheme-decomposition-on-borrowed-toponym.md
status: mitigated
mitigation:
  type: rule-and-check
  ref: llm-workflow.md
recurrence: pattern-of-N
---

## Input

User manually reviewed `cards/top_1000.tsv` and reported ~20 wrong or
incomplete cards — among them `մերի` "woods, forest", `ներ`
"sister-in-law", `ալ` "scarlet", `կողմ` "around, at about", `վեր`
"more than", `դեմ` "the front part", `տակ` "bottom", and a cluster of
high-frequency cards lacking a Russian gloss.

## What the LLM (pipeline) produced

`build_deck.py` ranks frequency by **surface token** but glosses by
**kaikki headword**. When a high-frequency grammatical or colloquial
token is spelled like a rare literary headword, kaikki returns the
rare sense — frequently as the *only* sense — and the builder shipped
it:

| card | shipped gloss | reality (corpus-confirmed) |
|---|---|---|
| `մերի` (rank ~39) | "woods, forest" | gen. of substantivized `մերը` ("ours") + `Ամերիկա` tokenizer spill |
| `ներ` (rank ~191) | "sister-in-law" | the plural suffix `-ներ`, metalinguistic mention in the grammar book |
| `գնում` (rank ~114) | "purchase" (noun) | imperfective converb of `գնալ`/`գնել` ("going/buying") |
| `ալ` (rank ~120) | "scarlet, bright red" | W.-Armenian/dialectal form of `էл` ("also") |
| `կողմ` | "around, at about" | noun "side, direction" |
| `վեր` | "more than" | adverb "up" |
| `դեմ` | "the front part" | postposition "against" |
| `տակ` | "bottom, lower part" | postposition "under" |
| `ներս` | "the inside" | postposition "in, inside" |
| `մեկն` | "correctly, upright" | definite nom. sg. of `մեկ` ("one") |
| `հավանել` | "to agree, to accept" | "to like, to approve" |

Plus two schema bugs found in passing: `լալ` "to cry / to weep" and
`ելնել` "to go out / to rise" misused ` / ` (reserved for the
English↔Russian boundary) as an English comma.

## What was correct

The structural validator was **green** the whole time — every wrong
gloss is a real, well-formed kaikki entry that round-trips and cites.
The lower-frequency cards and all hand-overrides were fine. As with
the 2026-06-01 song case, the errors hid in a mostly-correct deck.

## Why the existing checks missed it

`check_dictionary_ambiguity` only fires when a lemma has **≥2** real
senses to compare. A single-sense kaikki entry that happens to be the
*wrong* (rare) sense has nothing to flag against — it is structurally
invisible. The trap is a corpus-grounding gap, not a structural one.

## Mitigation (two-step rule, applied)

**Fix.** `SKIP_LEMMAS` for tokens that are a form of a deck lemma or
noise (`մերի`, `ներ`, `գնում`, `մեկն`); `HAND_OVERRIDES` (with Russian
+ short examples) for wrong-sense real words (`կողմ`, `վեր`, `դեմ`,
`տակ`, `ներս`, `հավանել`, `ալ`, `թե`, `խոսք`, …); `ум` re-labelled
gen/dat/acc per `topics/morphology/case_system.md`.

**Guard.** (1) Golden anchor in `golden_glosses.tsv` for every
re-gloss (75 rows now). (2) New `check_morpheme_noise` regression
guard on `SKIP_LEMMAS` removals. (3) New `check_reserved_slash` for
the ` / ` misuse. (4) New `check_missing_russian` coverage tracker.
(5) Named and documented the class as the **homograph trap** in
`llm-workflow.md` with the corpus-confirm drill, cross-linked from
`CLAUDE.md` § "Card decks". (6) The Russian-augmentation sweep doubles
as a homograph sweep — translating each gloss forces reading it, which
is how the second wave (`դեմ`, `տակ`, `հավանել`, …) and `գնում` (via
the independent auditor) were caught.

## Lesson

For frequency-ranked decks, **high rank + concrete-rare-noun gloss is
itself a smell.** Confirm sense in the corpus, never in the dictionary
that produced the gloss. A single-sense dictionary entry is *more*
dangerous than an ambiguous one, because the ambiguity check sleeps
through it.
