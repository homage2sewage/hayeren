---
topic: verb conjugation classes in Eastern Armenian (-ել / -ալ)
domain: morphology
units: [sakayan:1]
related: [present-tense, negation, participles, irregular-verbs]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 35
    y_range: [195, 280]
    verbatim_quote:
      - "There are two infinitive endings and, correspondingly, two conjugation types in Armenian"
      - "1. The first conjugation:"
      - "2. The second conjugation:"
      - "-ել"
      - "-ալ"
    supports: supported
    note: |
      sakayan's canonical statement: Eastern Armenian has exactly two
      conjugation classes, distinguished by infinitive ending —
      first conjugation in `-ել`, second in `-ալ`. Set up with the
      header "1. The first conjugation: verb stem + -ել" and "2. The
      second conjugation: verb stem + -ալ". Foundational; everything
      downstream (present tense, participles, negation, etc.) keys
      off this binary.
  - id: 2
    book: parnasyan
    page: 47
    y_range: [3300, 3700]
    verbatim_quote:
      - "относятся к спряжению"
      - "Глаголы спряжения"
      - "к спряжению ш"
    supports: supported
    note: |
      parnasyan in Russian: verbs ending in `-ել` belong to "ե
      conjugation", in `-ալ` to "ш [a] conjugation" (Russian-language
      naming convention: classes named by the linking vowel). Same
      binary as sakayan; different naming. Russian L1 contrastive
      angle.
  - id: 3
    book: tioyan
    page: 31
    y_range: [1400, 1700]
    verbatim_quote:
      - "с суффиксом -ել"
      - "спряжение"
      - "с суффиксом -ալ"
      - "սիրել"
      - "ցոլալ"
      - "ապրել"
      - "զգալ"
    supports: supported
    note: |
      tioyan's parallel statement (more recent Russian-language
      pedagogy): "verbs with suffix -ել (1st conjugation), with
      suffix -ալ (2nd conjugation)", with example pairs (սիրել
      "to love" 1st-conj vs ցոլալ "to shine" 2nd-conj; ապրել "to
      live" 1st-conj vs զգալ "to feel" 2nd-conj). Triangulates
      with sakayan + parnasyan.
  - id: 4
    book: tioyan
    page: 31
    y_range: [1700, 1920]
    verbatim_quote:
      - "псевдосуффикс"
      - "սոսկածանց"
      - "-ան-"
      - "-են-"
    supports: supported
    note: |
      tioyan documents a wrinkle absent from the basic binary:
      between the root and the conjugation suffix, some 2nd-conj
      verbs have a *pseudo-suffix* (Armenian: սոսկածանց;
      "псевдосуффикс" lit. "pseudo-suffix") that has no lexical or
      grammatical meaning. Two are introduced here: `-ան-` and
      `-են-`. Important for parsing forms like մոտենալ
      (root մոտ- + -են- + -ալ) — the basic binary
      (root + -ալ) is incomplete for these verbs. Sakayan addresses
      this differently — see `gaps:`.
gaps:
  - "Pseudo-suffix verbs need their own treatment — tioyan flags `-ան-` and `-են-` here but doesn't fully enumerate. Sakayan (paradigms_data.py and unit-by-unit text) handles them implicitly via per-verb paradigms. Worth tracking which verbs in our corpus use which pseudo-suffix."
  - "Irregular verbs (տալ, գալ, լինել, ուտել, տեսնել, ունենալ, …) don't fit the simple class/sub-class scheme cleanly. Their citation form is `-ալ` or `-ել` but their stems and tense formations are irregular. Covered in `topics/morphology/irregular_verbs.md` (TODO) but the boundary between 'second-conjugation regular' and 'irregular' is not crisp."
  - "Class membership is mostly invariant but there are edge cases (a verb with a derivational suffix can change apparent class). Not addressed by any cited source."
  - "Frequency / corpus distribution: what fraction of high-frequency verbs are in each class? Useful for pedagogical sequencing. Not in the sources."
---

# Verb conjugation classes in Eastern Armenian

Eastern Armenian has **exactly two conjugation classes**, distinguished
by the infinitive ending: [#1] [#2] [#3]

| class | infinitive ending | example | gloss |
|-------|-------------------|---------|-------|
| 1st | `-ել` | գրել | "to write" |
| 1st | `-ել` | խոսել | "to speak" |
| 1st | `-ել` | սիրել | "to love" |
| 2nd | `-ալ` | կարդալ | "to read" |
| 2nd | `-ալ` | մնալ | "to stay" |
| 2nd | `-ալ` | զգալ | "to feel" |

> **Sakayan [#1]**: "There are two infinitive endings and,
> correspondingly, two conjugation types in Armenian: 1. The first
> conjugation: verb stem + `-ել`; 2. The second conjugation: verb
> stem + `-ալ`."

Class membership is the *first* fact every learner needs about a new
verb. It determines:

- Imperfective participle: `stem + -ում` (same suffix for both
  classes, but stem extraction differs — see below).
- Subjunctive: `-եմ/-ես/-ի…` (1st) vs `-ամ/-ես/-ա…` (2nd).
- Aorist (simple past): `-եց-` (1st) vs `-աց-` (2nd) before personal
  endings.
- Negative participle: `-ի` (1st) vs `-ա` (2nd) — the form that
  drives hypothetical-mood negation, see `topics/morphology/negation.md`.
- Past participle: `-ել/-ացել` (1st/2nd) — drives perfect tenses.

So the `-ել/-ալ` distinction propagates through every analytic tense.
Memorising a verb means memorising its class.

## Naming conventions across sources

The binary is uncontroversial; the *names* differ:

- **Sakayan (English)**: "first conjugation" / "second conjugation."
- **Parnasyan (Russian, 1990) [#2]**: "ե conjugation" / "ш [a]
  conjugation" — names the class by the linking vowel (`ե` for `-ել`,
  `ш` is one Russian-side notation for `-ա-` from `-ալ`).
- **Tioyan (Russian, 2007) [#3]**: "I спряжение" (1st conj.) and
  "II спряжение" (2nd conj.) — Roman numerals, parallel to
  sakayan's English.
- **Armenian-internal**: classes are sometimes called *e-ka* and
  *a-ka* (after the linking vowel), or just by the infinitive
  ending. Sakayan's terminology has won out in English-language
  pedagogy.

Whichever name you use, refer to the same binary.

## The pseudo-suffix wrinkle

Not all verbs are bare-root + class-suffix. Some 2nd-conjugation
verbs have a **pseudo-suffix** between the root and the `-ալ`
ending. [#4]

> **Tioyan [#4]**: "Between the root and the [class] suffix, in
> verbs there can be a pseudo-suffix (Armenian: *սոսկածանց*) which
> has neither lexical nor grammatical meaning. Two pseudo-suffixes
> appearing in a number of 2nd-conjugation verbs: `-ան-` and `-են-`."

Examples:

| verb | parse | gloss |
|------|-------|-------|
| մոտենալ | մոտ- + -են- + -ալ | "to approach" |
| ուշանալ | ուշ- + -ան- + -ալ | "to be late" |
| մնալ | մն- + -ալ | "to stay" (no pseudo-suffix; bare root) |

In aorist and other forms, the pseudo-suffix surfaces or doesn't,
depending on the verb. This is part of why second-conjugation verbs
behave less uniformly than first-conjugation. For learning, the
practical rule: when memorising a 2nd-conjugation verb, also
memorise its aorist stem (which makes the pseudo-suffix presence/
absence visible).

Sakayan addresses pseudo-suffixes implicitly through per-verb
paradigms in `paradigms_data.py` rather than as a named phenomenon.
Tioyan's explicit naming is useful for parsing.

## Irregular verbs sit *outside* this binary

A handful of high-frequency verbs deviate from both classes' regular
patterns despite having an `-ել` or `-ալ` infinitive: `տալ`, `գալ`,
`լալ` (use `-իս` participle instead of `-ում`), `լինել` (has a
short irregular present), `ունենալ` (same), `տեսնել`, `ուտել`, etc.
See `topics/morphology/irregular_verbs.md` (TODO). For class-
membership purposes, the irregulars are "neither" — their citation
form fits one ending, but their conjugation is sui generis.

## Contrastive notes

**For an English L1**: English doesn't have conjugation classes in
this sense. The closest analogue is the regular/irregular split
("walk → walked" vs "go → went"), but Armenian's binary applies to
*regular* verbs — the regulars themselves come in two flavours, and
the difference is structural (different participles, different tense
formations), not just lexical.

Practical tip: when learning a verb, write the class symbol next to
it (e.g., "գրել [1]" or "կարդալ [2]"). The class determines
everything downstream; spending five seconds to label it pays off
for every later tense.

**For a Russian L1**: Russian also has conjugation classes (1st and
2nd), and the parallel is closer than for English. Russian's classes
are determined by the present-tense theme vowel (`е` vs `и`);
Armenian's by the infinitive ending (`-ել` vs `-ալ`). The mental
model "memorise the class along with the verb" carries over directly.

But: Russian's classes don't propagate through the *whole* tense
system the way Armenian's do. Russian past tense is regular for
both classes (just the `-л` suffix). Armenian's past forms differ
by class (`-եց-` vs `-աց-`). So expect more class-conditioned
variation downstream than Russian intuition predicts.

## Cross-references

- `topics/morphology/present_tense.md` — uses class to extract the
  participle stem (`գրել → գր- + -ում`, `կարդալ → կարդ- + -ում`).
- `topics/morphology/negation.md` — class determines the negative
  participle ending (`-ի` for 1st, `-ա` for 2nd) used in the
  hypothetical pattern.
- `topics/morphology/participles.md` (TODO) — the eight non-finite
  forms; each has a class-specific shape.
- `topics/morphology/irregular_verbs.md` (TODO) — the verbs that
  evade the binary.
- `armenian-grammar.md` — the parent file; will be updated when
  fully split.
