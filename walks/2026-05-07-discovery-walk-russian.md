# Discovery walk: phenomena in parnasyan / tioyan not yet in `topics/`

**Date**: 2026-05-07
**Operator**: Claude Code, manual.
**Status**: candidate-list. New topics not yet written; the highest-
priority candidate (`determinate_article`) is recommended for the
next session.

Source-mining was driven by the parnasyan + tioyan walks against
existing topics (see `walks/2026-05-07-topic-walk-parnasyan.md` and
the inline citations in negation/verb_classes/participles/
irregular_verbs/three_way_laryngeal_contrast/pro_drop). This file
catalogues phenomena addressed by parnasyan and/or tioyan that have
*no* corresponding topic file yet.

## High-priority new topics (from parnasyan + tioyan)

### `topics/morphology/determinate_article.md`

**Sources**: parnasyan p45 (canonical Russian-language statement),
sakayan units 1-2 (definiteness suffixes, also visible in basic
vocab examples), tioyan likely covers in early lessons.

**parnasyan p45**: *"В отличие от русского, в армянском языке
определенность—неопределенность имен существительных выражается
специальными грамматическими показателями."* — "Unlike Russian, in
Armenian definiteness/indefiniteness is expressed by specialized
grammatical markers."

**Topic content**: the suffixes `-ը` and `-ն` (definite article),
their distribution (`-ը` after consonants; `-ն` after vowels and
sometimes before vowel-initial words). Possessive suffixes (`-ս`,
`-դ`) replace the definite when the noun is also possessed.
Indefiniteness via the indefinite-article-like marker `մի` (ա one /
some, plus zero-marking).

**Why high priority**: directly addresses a major Russian-L1 gap
(Russian has no articles); also relevant for English-L1 since
Armenian's article system isn't 1:1 with English's. Foundational
topic that propagates through every noun phrase.

### `topics/phonology/no_palatalisation.md`

**Sources**: parnasyan p21 (already cited in three_way_laryngeal
_contrast.md for the consonant-system enumeration; the no-
palatalisation point is one of the five enumerated differences).

**parnasyan p21**: *"отсутствием противопоставления согласных по
твердости—мягкости. Армянские согласные произносятся твердо и почти
не смягчаются."* — "absence of the consonant hard/soft contrast.
Armenian consonants are pronounced hard and barely soften."

**Topic content**: Russian has palatalised consonants (мягкие)
contrasting with non-palatalised (твёрдые) — for Russian L1
learners, the *absence* of this contrast in Armenian is a learning
challenge in itself (resisting the urge to palatalise before front
vowels). Affects pronunciation across the board.

**Why high priority**: classical Russian-L1 phonological gotcha,
independently citable, single-source clean.

### `topics/morphology/auxiliary_e.md`

**Sources**: parnasyan p30-32 (already cited in present_tense.md;
could be hoisted to its own topic since `է` is structurally central).

**Topic content**: the auxiliary verb `է` "to be" — its dual role as
copula in compound predicates (`տուն է` "is a house") and as
auxiliary in analytic tenses (`գրում է` "is writing"); its
person/number paradigm (եմ ես է ենք եք են present, էի էիր էր էինք
էիք էին past); its relationship to the irregular verb `լինել` "to
be" (the regular continuative); historical roots in proto-Armenian.

**Why useful**: the auxiliary is referenced from present_tense,
pro_drop, negation, irregular_verbs, colloquial_copula_a. A
dedicated topic would consolidate.

### `topics/syntax/accusative_of_direction.md`

**Sources**: parnasyan p41 footnote (*"обстоятельство места,
показывающее направление, ставится в вин. п."* — "adverbial of place
showing direction is in the accusative"). Sakayan probably has
matching content.

**Topic content**: for inanimate destinations (cities, places),
Armenian uses the accusative (which coincides with the nominative
for inanimates) rather than a preposition + locative — `գնում եմ
Մոսկվա` "I go to Moscow" not `*գնում եմ Մոսկվայում`. Russian uses
prepositions (в, на + acc) for the same function; English uses
prepositions (to + obj). Armenian's case-only marking is leaner.

**Why useful**: a structural difference often missed by Russian-L1
learners (who try to insert a preposition).

## Medium-priority

### `topics/morphology/case_system_overview.md`

**Sources**: tioyan (multiple lessons cover individual cases),
parnasyan, sakayan p23+, `grammar-terms.md` already has the case
table.

**Why deferred**: case is a *system* topic; doing it justice means
either (a) writing one big topic with all 7 cases, or (b) per-case
topics (gen, dat, abl, ins, loc each as standalone). Scope decision
needed.

### `topics/morphology/numerals.md`

**Sources**: tioyan Lesson 16 (cardinal/ordinal/distributive
numerals). Parnasyan covers numbers in early lessons.

**Why useful**: numbers are basic vocabulary + have some grammatical
quirks (declension in some forms, the `-ից` for "out of",
distributive `-ական`).

### `topics/syntax/word_order.md`

**Sources**: parnasyan p49+ (general sentence characterization),
ghamoyan ch 4 syntax section (already partly mined).

**Why deferred**: word-order topic is large and overlaps with
existing pro_drop. Could be a follow-up consolidation topic.

## Low-priority / quick-mention

- **Reflexive pronouns** (`ինքը` etc.): parnasyan p104+ (visible).
  Small standalone topic.
- **Punctuation marks** (`՞ ՛ ՜`): tioyan Lesson 22, sakayan
  has a list. Already informally covered in
  `armenian-grammar.md`; could be promoted.
- **Cardinal direction adverbs** and other small lexical paradigms:
  not high-leverage but easy single-source topics.

## Decision matrix

For each candidate, the considerations:

| topic | parnasyan cite | tioyan cite | Russian-L1 impact | scope |
|-------|---------------|-------------|-------------------|-------|
| determinate_article | strong | (likely strong) | high | small |
| no_palatalisation | strong | (small mention) | high | small |
| auxiliary_e | strong | strong | medium | medium |
| accusative_of_direction | strong | TBD | medium | small |
| case_system_overview | medium | strong | high | large |
| numerals | medium | strong | low | medium |
| reflexive_pronouns | small | medium | low | small |

**Recommended next-action set** (by yield/effort):

1. `determinate_article.md` — high impact, small scope, strong
   citations already available.
2. `no_palatalisation.md` — quick win, single-source.
3. `auxiliary_e.md` — consolidation; hoists existing citations
   into a dedicated topic.

## Out of scope for this discovery walk

- Lexicon-side discoveries from parnasyan / tioyan — neither book
  covers slang or colloquial vocabulary (they're prescriptive),
  so the lexicon discovery walk is fully covered by ghamoyan.
- Per-case topics — pending the case-system-vs-per-case decision.
- Topics touching on phenomena ghamoyan hasn't documented (Western
  Armenian, Classical, etc.) — out of corpus scope.

## Suggested next move

Pick one of the three high-priority candidates and write the topic.
`determinate_article` is the recommended first because the Russian-
L1 contrast is sharpest (Russian has *no* articles) and the
parnasyan citation is already located.
