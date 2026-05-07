---
topic: negation in Eastern Armenian (finite-verb forms)
domain: morphology
units: [sakayan:2, sakayan:6]
related: [present-tense, pro-drop, hypothetical-mood, participles, yerevan-consonant-reductions]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 55
    y_range: [85, 250]
    verbatim_quote:
      - "Formation of the negative forms of verbs"
      - "by prefixing it to the verb"
      - "չ-"
      - "չգրել"
      - "չկարդալ"
      - "Լինել թե՞ չլինել"
    supports: supported
    note: |
      sakayan's canonical negation section, opening with the rule
      "Armenian uses the negative … by prefixing it to the verb" and
      working through infinitive examples (չգրել "not to write",
      չկարդալ "not to read", չլինել "not to be", չունենալ "not to
      have"), with the *Hamlet* example "Լինել թե՞ չլինել" as the
      cultural reference example.
  - id: 2
    book: sakayan
    page: 55
    y_range: [260, 440]
    verbatim_quote:
      - "չեմ"
      - "չես"
      - "չի/չէ"
      - "չենք"
      - "չեք"
      - "չեն"
      - "չունեմ"
      - "չգիտեմ"
    supports: supported
    note: |
      sakayan's full negative auxiliary paradigm — single-letter
      prefix `չ-` on each form of the present auxiliary
      (եմ ես է ենք եք են → չեմ չես չի/չէ չենք չեք չեն), plus
      irregular-auxiliary negatives (ունեմ → չունեմ "I don't have",
      գիտեմ → չգիտեմ "I don't know"). This is the *first* of the
      two negation patterns; covers all analytic tenses where the
      auxiliary negation is the whole story.
  - id: 3
    book: sakayan
    page: 247
    y_range: [415, 555]
    verbatim_quote:
      - "negative paradigm of the hypothetical future I"
      - "negative participle"
      - "չեմ գրի"
      - "չեմ կարդա"
    supports: supported
    note: |
      sakayan's introduction of the *second* negation pattern: in
      hypothetical (and future) tenses, the negation is `չ` +
      auxiliary + a special **negative participle** ending in
      `-ի` (1st conjugation) or `-ա` (2nd conjugation). Examples:
      գրել → չեմ գրի "I won't write"; կարդալ → չեմ կարդա "I won't
      read". The negative participle is a non-finite form distinct
      from the imperfective participle and is documented in
      sakayan/paradigms_data.PARTICIPLES.
  - id: 4
    book: parnasyan
    page: 62
    y_range: [750, 1500]
    verbatim_quote:
      - "Запомните, что отрицательные формы глагола образуются"
      - "при помощи отрицательной частицы"
      - "перемещается вперед"
    supports: supported
    note: |
      parnasyan's Russian-language statement of the same rule, with
      a structural note sakayan doesn't make explicit: in analytic
      forms, the negative auxiliary "moves forward" (перемещается
      вперед) — i.e., word order changes. `գրում եմ` (I write) → 
      `չեմ գրում` (I don't write), with the auxiliary preceding the
      participle. OCR'd at avg confidence 89.
  - id: 5
    book: tioyan
    page: 25
    y_range: [1990, 2055]
    verbatim_quote:
      - "Отрицательные формы образуются добавлением частицы"
      - "к глаголу"
    supports: supported
    note: |
      tioyan corroborates the basic rule from a more recent (2007)
      Russian-pedagogy source. Direct: "negative forms are formed by
      adding the particle [չ] to the verb." Used here to triangulate
      sakayan + parnasyan with a third source on the most
      fundamental claim. OCR'd from the modern Russian textbook.
  - id: 6
    book: ghamoyan
    page: 37
    y_range: [420, 475]
    verbatim_quote:
      - "չեմ գալի"
      - "չես բերե"
      - "չի տվե"
      - "Այս երևույթը գրական նորմի տեսանկյունից ընդունելի չէ"
    supports: supported
    note: |
      ghamoyan documents a colloquial Yerevan deviation: in negated
      verb forms, the word-final լ or ս drops (չեմ գալիս → չեմ գալի
      "I'm not coming", չես բերել → չես բերե "you didn't bring",
      չի տվել → չի տվե "s/he didn't give"). Explicitly flagged as
      "not acceptable from the standpoint of the literary norm" —
      stigmatised colloquialism. Same span is also cited from
      `topics/phonology/yerevan_consonant_reductions.md` (#4 there).
gaps:
  - "Imperative negation (`մի՛` prohibitive particle) not yet cited here — Sakayan p152, p349; Parnasyan p110, p254; Tioyan p53, p67, p142. Worth a separate sub-section once the topic gets to revision."
  - "Past-tense negation (negation of imperfect/aorist/perfect) follows the same pattern as basic auxiliary negation but with past-tense auxiliary forms (չէի, չէիր, չէր, …) — should be added explicitly with examples."
  - "Subjunctive negation (չ + bare-stem subjunctive forms like չգրեմ) not yet cited."
  - "Word-formation negation prefixes (`ան-` 'un-' on nominals, `չ` as a derivational prefix in nouns like `չինացի` 'Chinese') is a different phenomenon — could become a separate `topics/morphology/derivational_negation.md` topic."
  - "Sociolinguistic data on the colloquial letter-drop in negation: ghamoyan flags it as stigmatised but doesn't quantify by age/class/neighbourhood."
---

# Negation in Eastern Armenian (finite-verb forms)

Eastern Armenian uses **two different negation patterns** for finite
verbs, depending on tense:

1. **Most analytic tenses** (present, imperfect, perfect, future
   indicative): the negative particle `չ-` prefixes the auxiliary,
   and the auxiliary moves before the participle. [#1] [#2] [#4] [#5]
2. **Hypothetical mood** (hypothetical future / past): `չ` +
   auxiliary + a special **negative participle** ending in `-ի` or
   `-ա`. [#3]

Imperative is a third pattern (prohibitive particle `մի՛`); see
`gaps:` — not cited from this topic file yet.

## Pattern 1: prefix `չ-` to the auxiliary

The default negation rule. Take the affirmative form, prefix `չ-`
to the auxiliary, and (for analytic tenses) move the auxiliary before
the participle.

> **Sakayan [#1]**: "To create negative counterparts of affirmative
> forms, Armenian uses the negative `չ-` by prefixing it to the
> verb."
>
> **Parnasyan [#4]**: "Запомните, что отрицательные формы глагола
> образуются при помощи отрицательной частицы `չ` … отрицательный
> вспомогательный глагол перемещается вперед."

For the infinitive: just prefix `չ-`. [#1]

| affirmative | negative | gloss |
|-------------|----------|-------|
| գրել | չգրել | "to write" / "not to write" |
| կարդալ | չկարդալ | "to read" / "not to read" |
| լինել | չլինել | "to be" / "not to be" |
| ունենալ | չունենալ | "to have" / "not to have" |

The Hamlet example: *Լինել թե՞ չլինել* = "To be, or not to be?" [#1]

For finite forms, the auxiliary takes the prefix and reorders:

| affirmative | negative |
|-------------|----------|
| գրում **եմ** "I write" | **չեմ** գրում "I don't write" |
| գրում **ես** "you write" | **չես** գրում "you don't write" |
| գրում **է** "s/he writes" | **չի** գրում "s/he doesn't write" |
| գրում **ենք** "we write" | **չենք** գրում "we don't write" |
| գրում **եք** "you-pl write" | **չեք** գրում "you-pl don't write" |
| գրում **են** "they write" | **չեն** գրում "they don't write" |

[#2]

The same paradigm pattern applies to copular `է`: 3sg negative is
*chi* / *che*, often written `չի` in the literary norm and `չէ` as
an alternative spelling. Sakayan documents both. [#2]

### Irregular-auxiliary negatives

The two short irregular auxiliaries `ունեմ` "I have" and `գիտեմ` "I
know" take the same `չ-` prefix on each person/number form: [#2]

| have | not-have | know | not-know |
|------|----------|------|----------|
| ունեմ | չունեմ | գիտեմ | չգիտեմ |
| ունես | չունես | գիտես | չգիտես |
| ունի | չունի | գիտի | չգիտի |
| ունենք | չունենք | գիտենք | չգիտենք |
| ունեք | չունեք | գիտեք | չգիտեք |
| ունեն | չունեն | գիտեն | չգիտեն |

## Pattern 2: hypothetical / future negation uses the negative participle

The hypothetical mood (and the future, in some analyses) doesn't
follow Pattern 1. Instead, it uses a special **negative participle**
form of the lexical verb plus a negated auxiliary. [#3]

> **Sakayan [#3]**: "The negative paradigm of the hypothetical
> future I is formed by combining the negated [auxiliary] with the
> **negative participle** of the [main] verb."

The negative participle ends in `-ի` (first conjugation, `-ել` verbs)
or `-ա` (second conjugation, `-ալ` verbs). It's a distinct non-finite
form, listed in `sakayan/paradigms_data.PARTICIPLES`. Examples:

| affirmative (positive hypothetical) | negative |
|-------------------------------------|----------|
| **կ**գրեմ "I'd write" | **չեմ գրի** "I wouldn't write" |
| **կ**կարդամ "I'd read" | **չեմ կարդա** "I wouldn't read" |

Pattern: literary positive hypothetical = `կ-` prefix on the
subjunctive form; negative = `չ-` + auxiliary + negative-participle.

The negative-participle forms for high-frequency verbs (from
sakayan/paradigms_data.PARTICIPLES):

- `գրել → գրի` ("not to write" 1sg → `չեմ գրի`)
- `կարդալ → կարդա`
- `ասել → ասի` (so 2sg negative hypothetical = `չես ասի`)
- `տեսնել → տեսնի`
- `գալ → գա`
- `տալ → տա`
- `ուտել → ուտի`
- `անել → անի`

### Worked example: `չես ասի` "you won't say"

This is the canonical example for the project's
`transliteration-notes.md` (the `ches asem` trap). The grammar
behind why `չես ասի` is correct and `չես ասեմ` is broken:

- `չ` — negative prefix on the auxiliary
- `ես` — 2sg present auxiliary ("you are")
- `ասի` — *negative participle* of `ասել` "to say"

So `չ` + `ես` + `ասի` = `չես ասի` = "you won't say." [#3] (negative
hypothetical 2sg).

Compare the broken parse `չես ասեմ`: the `ասեմ` form is *1sg
subjunctive future* of `ասել`, not the negative participle. The
auxiliary `ես` is 2sg, but `ասեմ` is 1sg — agreement mismatch. The
form has no grammatical reading.

## Word-final letter-drop in colloquial negation (Yerevan)

In Yerevan colloquial speech, negated verb forms often drop their
final `լ` or `ս`. [#6] Examples (literary → colloquial):

- չեմ գալի**ս** → չեմ գալի "I'm not coming"
- չես բերե**լ** → չես բերե "you didn't bring"
- չի տվե**լ** → չի տվե "s/he didn't give"
- չի ասե**լ** → չի ասե "s/he didn't say"
- չի տալի**ս** → չի տալի "s/he doesn't give"

Ghamoyan flags this explicitly as **stigmatised** in the literary
register: *"Այս երևույթը գրական նորմի տեսանկյունից ընդունելի չէ"*
("This phenomenon is not acceptable from the standpoint of the
literary norm"). [#6]

When reading transliterated colloquial Yerevan text, expect this drop
— see `topics/phonology/yerevan_consonant_reductions.md` for the
broader catalogue and `transliteration-notes.md` for how to recover
the literary form.

## Imperative negation (prohibitive)

Brief: imperatives use the prohibitive particle `մի՛` before the
imperative form, not `չ-` (e.g. `մի՛ գրիր` "don't write!", `մի՛
խաղաք` "don't play!"). Sakayan p152 and p349, Parnasyan p110 and
p254, Tioyan p53 / p67 / p142 cover this. Citing this from a future
revision; see `gaps:` — not yet integrated.

## What this topic is *not*

- **Word-formation negation** (the prefix `ան-` on nominals, e.g.
  `հնարավոր` "possible" → `անհնարավոր` "impossible") is a different
  phenomenon, derivational rather than inflectional. Worth a
  separate topic eventually (Parnasyan p26 has the rule).
- **Pseudonegation** (rhetorical negation, double negation) and
  scope/quantifier interactions with negation are not addressed in
  any of the four current sources at the level needed for a
  topic; a typological grammar like Dum-Tragut would be the
  natural source if/when this becomes scope.

## Contrastive notes

**For an English L1**: pattern 1 (`չ-` prefix on auxiliary) is the
analogue of English's "do-support" — `I don't write` ≈ `չեմ գրում`,
in both cases the auxiliary takes the negation. But Armenian has no
`do`-equivalent: the existing auxiliary just gets prefixed. The
auxiliary movement (post→pre-participle) has no English parallel,
since English already has fixed Aux-V order.

Pattern 2 (negative participle) is foreign to English — there's
no English construction where the negation requires a different form
of the lexical verb. Memorise the negative-participle forms of
high-frequency verbs alongside the affirmative paradigm.

**For a Russian L1**: Russian negation is just `не` before the verb
(or another constituent). Pattern 1 (`չ-` prefix on auxiliary) is
*structurally simpler* than Russian's: instead of inserting a
particle, you change the auxiliary's first consonant. Easy.

The Russian `не` particle stays put; the Armenian negated auxiliary
*moves*. This is sometimes overlooked: word order is part of the
rule, not just the prefix. [#4]

Pattern 2 has no Russian analogue — Russian doesn't have a separate
"negative participle" form. The negative-participle endings (`-ի`,
`-ա`) need to be memorised as part of each verb's paradigm. The
upside: this pattern only fires in hypothetical/future, so for
present/past indicative the simpler Pattern 1 covers most usage.

## Cross-references

- `topics/morphology/present_tense.md` — affirmative paradigm that
  Pattern 1 negates.
- `topics/morphology/colloquial_copula_a.md` — the 3sg `ա↔է` swap
  also affects negation: in colloquial Yerevan, `չի` is used in 3sg
  for analytic forms; the copular substitution affects affirmative
  copula but not the negation prefix.
- `topics/morphology/participles.md` (TODO) — the eight non-finite
  forms, including the negative participle that drives Pattern 2.
- `topics/phonology/yerevan_consonant_reductions.md` — the
  word-final letter-drop in colloquial negated forms.
- `topics/syntax/pro_drop.md` — negation interacts with pro-drop:
  `չեմ ասի` (no overt subject) is fine for "I won't say" because
  the negated auxiliary still carries person/number.
- `transliteration-notes.md` — uses `չես ասի` as the canonical
  back-transliteration example; this topic is what makes the
  grammar of that form correct.
- `armenian-grammar.md` — original seed notes (will be updated when
  fully split into topic files).
