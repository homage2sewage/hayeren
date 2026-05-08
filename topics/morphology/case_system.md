---
topic: the seven-case nominal system in Eastern Armenian
domain: morphology
units: [sakayan:4]
related: [determinate-article, accusative-of-direction]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 102
    y_range: [225, 280]
    verbatim_quote:
      - "Armenian has seven cases"
      - "nominative, accusative, genitive, dative, ablative, instrumen"
      - "and locative"
      - "first four cases, nominative and accusative, genitive and dative"
      - "two pairs that may correspond in form but differ in syntactic function"
    supports: supported
    note: |
      sakayan's canonical statement: Armenian has seven cases —
      nominative, accusative, genitive, dative, ablative,
      instrumental, locative. Notes structurally that nom+acc form
      one pair (often syncretic in form) and gen+dat form another.
      So while there are *seven* case-functions, there are typically
      five distinct word-forms (nom=acc, gen=dat for animates).
  - id: 2
    book: sakayan
    page: 102
    y_range: [330, 480]
    verbatim_quote:
      - "Nominative:"
      - "ո՞վ"
      - "ի՞նչ"
      - "Accusative"
      - "ո՞ւմ"
      - "Genitive:"
      - "Dative"
      - "Ablative"
      - "ումի՞ց"
    supports: supported
    note: |
      sakayan's case-by-case question table. Question words
      diagnose case function: nom = `ո՞վ` "who?" / `ի՞նչ(ը)` "what?";
      acc = `ո՞ւմ` "whom?" / `ի՞նչ(ը)` "what?"; gen = `ո՞ւմ` "whose?"
      / `ինչի՞` "of what?"; dat = `ո՞ւմ` "to whom?" / `ինչի՞(ն)` "to
      what?"; abl = `ումի՞ց` "from whom?". The animate (`ո՞վ`) /
      inanimate (`ի՞նչ`) split is parallel to many languages including
      Russian.
  - id: 3
    book: parnasyan
    page: 101
    y_range: [3200, 3300]
    verbatim_quote:
      - "семь падежей"
      - "именительный, родительный"
    supports: supported
    note: |
      parnasyan corroborates the seven-case count in Russian:
      *"семь падежей: именительный, родительный, да-..."* — "seven
      cases: nominative, genitive, da[tive]...". Russian-language
      naming for direct comparison with the Russian case system,
      which has six.
gaps:
  - "Tioyan covers individual cases across multiple lessons (p41 genitive, p86 'Падежи.' header, p87 genitive declension etc.) but doesn't have a single overview comparable to sakayan p102 — so tioyan triangulation per-case rather than at the overview level."
  - "Per-case topic files are deferred — this overview names the seven and gives diagnostic questions, but doesn't give the full inflectional paradigms. The follow-on topics: `topics/morphology/genitive_case.md`, `topics/morphology/dative_case.md`, etc."
  - "Declension types — Armenian has multiple declension classes (see sakayan p125-126 'Declension types') determined by the genitive ending (-ի, -ու, -ա, -ոջ, etc.). Class membership is mostly per-noun and must be memorised. Out of scope here."
  - "Case syncretism: sakayan notes nom=acc and gen=dat 'may correspond in form' but doesn't formalise *when*. The full rule: animate nouns distinguish nom/acc; inanimate nouns syncretise them. Gen/dat for definite/possessed nouns also syncretise."
  - "Case + definite article interaction: when a noun has a case ending and the definite article, both attach. E.g. գիրք-ի-ն 'to the book' (gen + def `-ն`). Pattern not detailed here."
---

# The seven-case nominal system

Eastern Armenian declines nouns and pronouns through **seven cases**:
nominative, accusative, genitive, dative, ablative, instrumental,
and locative. [#1] [#3] Every common noun has a case form for each
of these — though several pairs are typically *syncretic* (same
form, different function), reducing the distinct word-form count
to ~5 per noun for most lexemes.

This is the **single biggest grammatical-system addition** for an
English L1 learner (English has effectively no case marking) and
the **biggest cross-system difference** for a Russian L1 learner
(Russian has six cases, with some functional overlap and some
mismatches).

## The seven cases

> **Sakayan [#1]**: "Armenian has seven cases: nominative,
> accusative, genitive, dative, ablative, instrumental, and
> locative."
>
> **Parnasyan [#3]**: *"семь падежей: именительный, родительный..."*

| # | Armenian | Russian equiv. | function | English fn |
|---|----------|---------------|----------|------------|
| 1 | ուղղական | именительный | subject | "Aram comes" |
| 2 | հայցական | винительный | direct object | "I see Aram" |
| 3 | սեռական | родительный | possession, of-relation | "Aram's book" / "the book of Aram" |
| 4 | տրական | дательный | indirect object, recipient | "give to Aram" |
| 5 | բացառական | (no exact equiv; *из/от/с +*) | source, "from" | "from Aram" |
| 6 | գործիական | творительный | instrument, "with" | "with a pencil" |
| 7 | ներգոյական | (no equiv; *в/на + prep*) | location, "in/at" | "in the city" |

(Trilingual mapping in `grammar-terms.md`.)

## Diagnostic questions

> **Sakayan [#2]**: case-by-case question words used to diagnose
> case function.

Each case is associated with characteristic interrogative pronouns
("who?" "to whom?" etc.). The question word *agrees* in case with
the answer:

| case | animate question | inanimate question | English |
|------|-----------------|---------------------|---------|
| nom | ո՞վ | ի՞նչ(ը) | who? / what? |
| acc | ո՞ւմ | ի՞նչ(ը) | whom? / what? |
| gen | ո՞ւմ | ինչի՞ | whose? / of what? |
| dat | ո՞ւմ | ինչի՞(ն) | to whom? / to what? |
| abl | ումի՞ց | ինչի՞ց | from whom? / from what? |
| ins | ումո՞վ | ինչո՞վ | with whom? / with what? |
| loc | ումո՞ւմ | ինչո՞ւմ | in whom? / in what? |

(loc and ins are spotty for animates — typically only used for
inanimates.)

## Syncretism: 7 cases, ~5 forms

> **Sakayan [#1]**: "The first four cases, nominative and
> accusative, genitive and dative, form two pairs that may
> correspond in form but differ in syntactic function."

For most nouns the system collapses:

- **nom = acc** for inanimate nouns: `գիրք` "book" is both
  "[the] book is on the table" (nom) and "I see [the] book" (acc).
- **gen = dat** in many contexts: `Արամի` is both "of Aram" (gen)
  and "to Aram" (dat) — distinguished only by syntax/preposition.

Animate nouns *do* distinguish acc from nom (`Արամ` nom vs `Արամին`
acc with definite -ին), so the syncretism is conditional. This
requires lexical-level animacy judgment; pedagogically: "people →
distinguish, things → don't."

## Suffix sketch (per regular declension class)

For a typical -ի-class noun (`գիրք` "book"):

| case | sg | gloss |
|------|----|-------|
| nom | գիրք | "book" |
| acc | գիրք | (= nom for inanimates) |
| gen | գրքի | "of book" |
| dat | գրքի(ն) | "to book" |
| abl | գրքից | "from book" |
| ins | գրքով | "with book" |
| loc | գրքում | "in book" |

(Plural and definite forms add their respective suffixes; see
deferred per-case topics + sakayan p125-126 for declension
classes.)

## Definiteness + case

When a noun is definite (with `-ը`/`-ն`), the article attaches
*after* the case suffix in some forms, *replaces* it in others.
E.g. `գրքին` "to the book" (dat + def `-ն`) — see
`topics/morphology/determinate_article.md` for the article system.

## Contrastive notes

**For an English L1**: the entire concept of grammatical case
might be foreign — English has only a vestige (he/him, who/whom).
Armenian's seven cases require a major mental-model addition. Start
with the four most-used (nom, acc, gen, dat) and add abl/ins/loc
as needed. Memorise per noun: its nominative form + its genitive
form (which encodes the declension class). The other cases derive
mostly mechanically.

**For a Russian L1**: the Armenian system *almost* matches Russian's
six-case system, with two key shifts:

1. **Armenian has a locative** (ներգոյական, "in/at" + suffix) where
   Russian uses *prepositional* (preposition + noun in a special
   form). The Armenian locative is a *true* case ending; no
   preposition needed for "in the house" — just `տանը` (house +
   loc). Russian L1 learners initially try to insert a preposition;
   resist.
2. **Armenian's ablative** (բացառական, "from" + suffix) similarly
   doesn't need a preposition — `քաղաքից` "from the city" alone,
   no `из/от` prefix. Russian has no exact equivalent case;
   *from* is expressed by `из/от/с + genitive`.

Otherwise the case-function correspondence is direct and usable as
mental scaffold.

## Cross-references

- `topics/morphology/determinate_article.md` — article + case
  interaction.
- `grammar-terms.md` — trilingual case glossary
  (English/Armenian/Russian) with detailed function notes.
- `armenian-grammar.md` — the original notes (will be updated when
  per-case topic files land).
- TODO: `topics/morphology/genitive_case.md`,
  `topics/morphology/dative_case.md`,
  `topics/morphology/ablative_case.md`,
  `topics/morphology/instrumental_case.md`,
  `topics/morphology/locative_case.md` — each case deserves a
  dedicated topic for full inflectional paradigms.
- `topics/syntax/accusative_of_direction.md` (TODO from
  `walks/2026-05-07-discovery-walk-russian.md`) — special
  accusative-of-destination use.
