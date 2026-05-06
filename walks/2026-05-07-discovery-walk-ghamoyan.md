# Discovery walk: phenomena in ghamoyan not yet in `topics/`

**Date**: 2026-05-07
**Operator**: Claude Code, manual.
**Status**: candidate-list only; no topic files written.

Source-mining was opportunistic — phenomena that surfaced while
reading Chapter 2 (phonology) and Chapter 4 (grammar) for the
topic-walk against existing topics. A more systematic discovery walk
would also cover Chapters 3 (lexicon) and 5 (style), and Appendices
1–3.

## High-priority new topics

These are dense, well-attested, and directly contrast literary vs
colloquial — the project's core use case.

### `topics/phonology/colloquial_copula_a.md`

The 3sg copula/auxiliary `ա` replacing literary `է` in Yerevan
colloquial. ghamoyan p73 documents both compound-predicate use
(`մեծ ա`) and simple-predicate use (`գրում ա`). Pattern is
ubiquitous in Yerevan speech and is the single most recognisable
marker of colloquial register.

Cross-references: present_tense.md, pro_drop.md.

### `topics/phonology/yerevan_vowel_reductions.md`

ghamoyan p35-36 catalogues a wide set of vowel elisions and
substitutions in fast colloquial speech: `ցտեսություն → ցըտեսցյուն`,
`շնորհակալություն → շնորակալցյուն`, `ի→ը` in pre-tonic syllables
(`պիտի→պըտի`, `ինչի→ընչի`), etc. Includes the `-ություն → -ուցյուն`
suffix change ("almost everyone speaks this way" — p40).

### `topics/phonology/yerevan_consonant_reductions.md`

ghamoyan p37-38: `ղ`-drop (`էստեղ → ըստե`), final `-ս/-լ` drop in
some inflected forms (`չեմ գալիս → չեմ գալի`), imperative final `ր`
drop (`գրի՛ր → գրի՛`). All highly characteristic of Yerevan
colloquial; none mentioned by Sakayan.

### `topics/phonology/diphthong_simplification.md`

ghamoyan p36, 39: `այ → է` in the pronominal series
(`այս/այդ/այն → էս/էդ/էն`), `ույ → ու` in `արյուն → արուն`,
`ձյուն → ձուն`, etc. Pronoun forms specifically are a register tell
— `էս` is colloquial, `այս` literary.

### `topics/syntax/sentence_member_elision.md`

A *generalisation* of pro-drop. ghamoyan p79-80: subject, predicate,
auxiliary, complements can all be elided when context permits.
Subject-only elision (`pro_drop.md`) is one case; sentence-fragment
"complete utterances" are a separate phenomenon worth its own topic
once we have more discourse-level material.

### `topics/morphology/post_pronominal_diminutives.md`

ghamoyan p72: `իմ քուրիկս` ("my sister-DIM-1SG.POSS"), `քո տատիկդ`
("your grandma-DIM-2SG.POSS"). Double marking of possessor —
pronoun + suffix — characteristic of colloquial register.
Pedagogical note: marked as "not recommended" by ghamoyan (հանձնարարելի չէ).

## Medium-priority

### `topics/lexicon/loanword_phonology.md`

ghamoyan p38-40: Russian loanwords arriving with Russian-flavoured
phonology (`Մոսկվա→Մասկվա`, `կոնֆետ→կանֆետ`); also `-տ → -ծ` and
`-դ → -ձ` in loanwords from Russian (`սանտիմետր → սանծիմետր`).

### `topics/syntax/pleonasm_with_da_dranq.md`

ghamoyan p89: pleonastic `դա/դրանք` after subject NPs
(`Հայրենիքը` …). Marked as a non-native construction.

### `topics/pragmatics/discourse_particles.md`

ghamoyan p77 lists colloquial particles: `հա, չէ՛, օֆ, ըհը, հըմ,
էհ`, etc. Affirmation, hesitation, exclamation registers.

### `topics/pragmatics/diminutive_personal_names.md`

ghamoyan p70-71: -իկ, -չիկ, -չո (Russian-borrowed). Anush→Անուշիկ.

### `topics/morphology/case_drift_in_locatives.md`

ghamoyan p89 (mentioned, not deeply explored): `Ես Երևան եմ
ապրում` instead of literary `Ես Երևանում եմ ապրում` — accusative-
shape locative replacing the locative case ending. Symptomatic of
the case system simplifying in colloquial.

## Low-priority / requires Chapter 3 read

- Lexical doublets (Chapter 3, pp. 41-69) — wholesale colloquial
  vocabulary distinct from literary. Doublet-by-doublet treatment is
  Phase-3 lexicon work; a single overview topic would be premature.
- Stylistic markers (Chapter 5, pp. 92-96) — likely overlaps with
  the discourse-particles topic.

## Ordering rationale

The high-priority list is dominated by phonology because (a)
ghamoyan's Chapter 2 was read first and most carefully, and (b)
phonology has the most binary literary-vs-colloquial contrasts
that are easy to surface from a few page-spans. Grammar
(Chapter 4) discoveries are more diffuse.

A re-pass over Chapters 3 and 5 would round out the picture —
particularly for `lexicon/` and `pragmatics/`.

## What this walk did *not* do

- Read the appendices (pp. 100-115) — likely sample-data tables
  worth mining for examples once topic files are populated.
- Cross-reference ghamoyan's claims with Sakayan's vocab pages to
  identify literary↔colloquial doublets that show up in both
  books.
- Check ghamoyan's bibliography (p116) — could reveal candidate
  next sources.

## Suggested next moves

1. Pick 2 high-priority topics from this list and write them. Good
   first-cut choices: `colloquial_copula_a.md` (highest-utility, most
   recognisable register marker) and `yerevan_consonant_reductions.md`
   (large concrete catalogue, easy to cite).
2. Use those two as the second pressure-test of the schema (after
   the four existing topics) — at scale ~6 topics, structural drift
   becomes more visible.
3. Then tackle Chapter 3 (lexicon) for the lexical-doublet pass.
