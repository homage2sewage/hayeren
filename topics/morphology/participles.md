---
topic: non-finite verb forms (participles, դերբայներ) in Eastern Armenian
domain: morphology
units: [sakayan:6, sakayan:10]
related: [verb-classes, present-tense, negation, irregular-verbs]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 259
    y_range: [60, 240]
    verbatim_quote:
      - "WORD FORMATION"
      - "Formation of participles"
      - "Armenian has two sets of participles."
      - "first set consists of four participles that are bound"
      - "The present participle ending in"
      - "-ում"
    supports: supported
    note: |
      sakayan's framing: "Armenian has two sets of participles" —
      bound (used only with the auxiliary in conjugation paradigms)
      vs free (independent use). Page introduces the first set; the
      first member is the imperfective/present participle in -ում
      that drives the present and imperfect tenses.
  - id: 2
    book: sakayan
    page: 259
    y_range: [240, 620]
    verbatim_quote:
      - "The past participle ending in"
      - "-ել/-ացել"
      - "The future participle ending in"
      - "second set consists of four free participles"
    supports: supported
    note: |
      sakayan's enumeration of the remaining bound participles (past
      `-ել/-ացել`, future) and the introduction of the second set
      (free participles, "function independently in sentences").
  - id: 3
    book: tioyan
    page: 157
    y_range: [375, 1100]
    verbatim_quote:
      - "Безличные формы глагола"
      - "դերբայ"
      - "անկախ"
      - "դերբայներ"
    supports: supported
    note: |
      tioyan's canonical Armenian-language classification: non-finite
      forms (անդեմ ձևեր) are termed *դերբայ* (lit. "non-finite-form"
      / "infinite verb form"). They split into *անկախ* (independent /
      free) and *կախյալ* / *ձևակազմիչ* (dependent / form-building).
      This is the project's first source for the systematic Armenian
      terminology — sakayan uses English-only names; tioyan gives the
      formal Armenian terms which are useful for cross-referencing
      with Armenian-language linguistic literature.
  - id: 4
    book: tioyan
    page: 157
    y_range: [1450, 2050]
    verbatim_quote:
      - "Зависимые дербаи"
      - "անկատար"
      - "վաղակատար"
      - "ապառնի"
      - "ժխտական"
      - "Независимые дербаи"
      - "անորոշ"
      - "համակատար"
      - "ենթակայական"
      - "հարակատար"
    supports: supported
    note: |
      tioyan's enumeration of all eight (or nine, with հարակատար
      bridging both sets) non-finite forms by their Armenian names:
      Dependent — անկատար (imperfective, drives present/imperfect),
      վաղակատար (perfect/pluperfect-driving), ապառնի I (future I,
      drives future tense), ժխտական (negative, drives hypothetical
      negation). Independent — անորոշ (infinitive), համակատար
      (synchronic / "while-Ving" converb), ենթակայական
      (active/subject participle, "the one who Vs"), հարակատար
      (resultative, drives resultative tenses + standalone use),
      ապառնի II (future II, used standalone).
  - id: 5
    book: parnasyan
    page: 60
    y_range: [2150, 4700]
    verbatim_quote:
      - "несовершенное причастие"
      - "образуется прибавлением"
      - "Таблица образования инфинитива и несовершенного причастия"
    supports: supported
    note: |
      parnasyan in Russian: "Imperfective participle is formed by
      adding -ум to..." with a tabular formation rule. The classical
      Russian-pedagogical treatment of the participle that drives the
      present/imperfect tense, with separate sub-tables for 1st and
      2nd conjugation. Russian-L1 framing, OCR'd at 90%+ confidence.
gaps:
  - "Per-form formation rules (suffix tables for each of the eight forms × two conjugations) not yet enumerated here. The basic parent file `armenian-grammar.md` has them; can be folded in when the topic gets revised."
  - "Per-irregular-verb participle tables (cf. paradigms_data.PARTICIPLES which has 8 verbs covered: գրել, կարդալ, ունենալ, լինել, գալ, տեսնել, ուտել, տալ + the universal anel/ar`nel) are not directly cited from a single book passage — Sakayan p354-355 has the table; needs a citation source on its own."
  - "Discrepancy: sakayan says 'two sets of four' (= 8 forms), tioyan lists 5 independent + 4 dependent (= 9, with հարակատար bridging). The accounting depends on whether հարակատար is counted once or twice. Worth resolving by reading both sources more carefully."
  - "Sociolinguistic / register data on participle usage: which forms are colloquial-only vs literary-only? E.g. is համակատար (synchronic converb in -ելիս) used in colloquial speech or only in writing? Untreated by the cited sources."
  - "Aspectual semantics of each form: vague labels like 'imperfective' vs 'perfect' don't fully capture the system. A typological grammar (Dum-Tragut 2009) would help — TODO."
---

# Non-finite verb forms (participles, դերբայներ) in Eastern Armenian

Eastern Armenian has **two parallel verb-form systems**: finite forms
(տիմավոր ձևեր; carry person, number, mood, tense) and non-finite
forms (անդեմ ձևեր), the latter called **դերբայներ** (singular դերբայ)
— literally "non-finite-form." [#3] The finite forms are
*built from* the non-finite ones — every analytic tense in the
language is `participle + auxiliary` — so the participles are the
engine of the entire verbal system.

## Two sets / two functional roles

Both sakayan and tioyan agree on a binary classification, with
slightly different terminology:

| sakayan ("[#1] two sets") | tioyan ("[#3] անկախ vs կախյալ") | role |
|---------------------------|---------------------------------|------|
| bound (set I) | կախյալ / ձևակազմիչ (dependent / form-building) | only used with auxiliary in conjugation paradigms |
| free (set II) | անկախ (independent) | function independently in sentences (as adjectives, nouns, adverbs) |

> **Sakayan [#1] [#2]**: "Armenian has two sets of participles. I.
> The first set consists of four participles that are bound for use
> in conjugation paradigms… II. The second set consists of four
> free participles that function independently in sentences."

> **Tioyan [#3]**: "Non-finite forms — անդեմ ձևեր — are designated
> by the term դերբայ. … Դերբայներ are subdivided into two groups:
> անկախ (independent) and կախյալ or ձևակազմիչ դերբայներ (dependent,
> or form-building dərbays)."

## Inventory

**Dependent / bound** (used with auxiliary to form analytic tenses)
[#4]:

| Armenian name | English / function | suffix | drives |
|---------------|-------------------|--------|--------|
| **անկատար** (imperfective) | "is doing / was doing" | `-ում` | present, imperfect → see `topics/morphology/present_tense.md` |
| **վաղակատար** (perfect-driver) | "has done" | `-ել/-ացել` | perfect, pluperfect |
| **ապառնի I** (future I) | "will do / going to" | `-ելու/-ալու` | future, future imperfect |
| **ժխտական** (negative) | (no standalone gloss) | `-ի/-ա` | hypothetical-mood negation → see `topics/morphology/negation.md` |

**Independent / free** (also usable in their own right) [#4]:

| Armenian name | English / function | suffix |
|---------------|-------------------|--------|
| **անորոշ** (infinitive) | "to do" — citation form, also a noun | `-ել/-ալ` |
| **համակատար** (synchronic converb) | "while doing" — temporal converb | `-ելիս/-ալիս` |
| **ենթակայական** (active / subject participle) | "the one who does" — agent noun, also adjective | `-ող/-ացող` |
| **հարակատար** (resultative) | "having done" — adjective, drives resultative tenses | `-ած/-ացած` |
| **ապառնի II** (future II) | parallel free version of future | `-ելու` |

The accounting differs between sources (sakayan's "two sets of four"
implies 8; tioyan's listing has 5 independent + 4 dependent = 9 with
հարակատար effectively in both groups). Resolution: հարակատար is
*both* — it has a bound use in the resultative tenses *and* a free
use as an adjective. Counting it once gives 8.

## Per-form formation: an example (անկատար / imperfective)

The most-encountered participle: imperfective in `-ում`, the engine
of the present and imperfect tenses. [#1] [#5]

> **Parnasyan [#5]**: "Несовершенное причастие образуется
> прибавлением `-ум` к [stem]" — the imperfective participle is
> formed by adding `-ում` to the verb stem.

Class-conditioned: stem-extraction depends on conjugation class
(see `topics/morphology/verb_classes.md`).

| infinitive | class | stem | imperfective participle |
|-----------|-------|------|------------------------|
| գրել "to write" | 1st | գր- | գր**ում** |
| կարդալ "to read" | 2nd | կարդ- | կարդ**ում** |
| մոտենալ "to approach" | 2nd (pseudo-suffix) | մոտեն- | մոտեն**ում** |

## Per-form formation: the rest (sketch)

Detailed suffix-by-suffix tables for the remaining 7 participles
× 2 conjugations exist in `armenian-grammar.md` (parent file) and
sakayan's appendix tables (pp. 345-355). Citation-quality coverage
of those tables is queued; for now this topic captures the
**framework** (two sets, eight forms with terminology) and individual
form formations live in or are cross-referenced from related topic
files:

- Imperfective `-ում` → see `topics/morphology/present_tense.md`
  for the form in use.
- Negative `-ի/-ա` → see `topics/morphology/negation.md` for the
  hypothetical-mood pattern that uses it.
- Perfect-driver `-ել/-ացել`, future `-ելու/-ալու`, infinitive,
  active, synchronic, resultative — TODO.

## Irregular-verb participles

Eight high-frequency irregular verbs (`գրել`, `կարդալ`, `ունենալ`,
`լինել`, `գալ`, `տեսնել`, `ուտել`, `տալ`) have their full participle
tables encoded in `sakayan/paradigms_data.PARTICIPLES`. The pattern
is the same eight forms above, but the *stems* used to build them
deviate from the citation infinitive — typically the participle uses
the **aorist stem** rather than the infinitive stem:

- `գալ` (aorist `եկ-`): active `եկող`, past `եկած`, future `գալու`,
  synchronic `գալիս`, instrumental `գալով`, negative `գա`.
- `ուտել` (aorist `կեր-`): past `կերած` (not `*ուտած`!), the rest
  from `ուտ-`.
- `տեսնել` (aorist `տես-`): past `տեսած`, the rest from `տեսն-`.
- `լինել` (aorist `եղ-`): active `եղող`, past `եղած`, future
  `լինելու`.

See `topics/morphology/irregular_verbs.md` (TODO) for the full
treatment.

## Contrastive notes

**For an English L1**: English has present participle (`writing`),
past participle (`written`), gerund (`writing`-as-noun), and
infinitive (`to write`). Armenian's eight is wider but the function
overlap is significant:

- *imperfective* `գրում` ≈ progressive `writing` (always with aux)
- *perfect-driver* `գրել` ≈ perfect `written` (with aux)
- *future* `գրելու` ≈ "going to write"
- *active* `գրող` ≈ "the writing-one" / "the writer"
- *resultative* `գրած` ≈ "having been written" (passive-ish)
- *infinitive* `գրել` = "to write" (also acts as a noun)
- *synchronic* `գրելիս` ≈ "while writing" (no English single word)
- *negative* `գրի` — no English analogue (only appears in negation)

The free/bound distinction has no clean English parallel — English
participles are pretty freely usable. Treat Armenian's bound set as
"only seen with `եմ` / `էի` etc." and learn them as a *unit* with
the auxiliary.

**For a Russian L1**: Russian has причастия (participles) and
деепричастия (converbs / "verbal adverbs") — and tioyan and parnasyan
*use these terms* explicitly to translate the Armenian forms:

- *անկատար* = "несовершенное причастие" (imperfective participle)
- *հարակատար* = "результативное причастие" (resultative participle)
- *համակատար* = "деепричастие сопутствующего действия"
  (concomitant-action converb)
- *ապառնի* = "причастие последующего действия" (subsequent-action
  participle)
- *ենթակայական* = "субъектное причастие" / "действительное
  причастие" (active/subject participle)

The Russian deepričаstije / pričаstije split (~adverbial vs
adjectival uses of non-finite forms) maps roughly onto Armenian's
free vs bound, but not perfectly — Armenian's *infinitive*, for
instance, can act as a *noun* (with case marking and articles), which
Russian infinitives only do in limited constructions.

The biggest Russian-L1 leverage: free participles like *ենթակայական*
(`գրող` "the one who writes," substantive) translate cleanly to the
Russian active participle (`пишущий`). Bound participles need to be
learned as the participle+auxiliary unit.

## Cross-references

- `topics/morphology/verb_classes.md` — the class binary that
  determines participle suffix shapes.
- `topics/morphology/present_tense.md` — the imperfective participle
  in use.
- `topics/morphology/negation.md` — the negative participle that
  drives hypothetical-mood negation.
- `topics/morphology/irregular_verbs.md` (TODO) — the eight
  high-frequency verbs whose participle stems deviate from the
  citation infinitive.
- `armenian-grammar.md` § "Դերբայ" — original seed notes (will be
  updated when fully split).
- `sakayan/paradigms_data.PARTICIPLES` — code-side data for 8 high-
  frequency verbs' full participle tables.
