---
topic: perfect and pluperfect tenses in Eastern Armenian
domain: morphology
units: [sakayan:5]
related: [aorist, present-tense, participles, auxiliary-e, irregular-verbs]
status: draft
attestation: single-source
sources:
  - id: 1
    book: sakayan
    page: 121
    y_range: [100, 250]
    verbatim_quote:
      - "perfect and pluperfect tenses"
      - "Armenian uses the perfect and pluperfect"
      - "actions that"
      - "took place in the past"
      - "compound tenses formed by combining the auxiliary verb"
      - "in the present and imperfect tense respectively"
      - "past participle"
      - "-ել /-ացել"
      - "գրել եմ, գրել էի"
      - "կարդացել եմ, կարդացել էի"
    supports: supported
    note: |
      sakayan's canonical introduction: perfect and pluperfect are
      *compound* (analytic) tenses combining the auxiliary `եմ` (in
      present or imperfect form respectively) with the *past
      participle* of the lexical verb. Past participle ends in
      `-ել` (1st conjugation) or `-ացել` (2nd conjugation). Examples:
      գրել եմ "I have written" / գրել էի "I had written" (1st conj);
      կարդացել եմ "I have read" / կարդացել էի "I had read" (2nd
      conj).
  - id: 2
    book: sakayan
    page: 121
    y_range: [195, 280]
    verbatim_quote:
      - "past participle of the base verb is built as follows"
      - "first-conjugation verbs"
      - "-ել"
      - "infinitive and the past participle coincide"
      - "սիրել"
    supports: supported
    note: |
      sakayan's note that for **first-conjugation verbs** (ending
      in `-ել`), the **past participle is identical to the
      infinitive form** (`սիրել` "to love" = past participle "loved").
      This is a useful pedagogical anchor — the participle isn't
      "another form to memorise" but the same word with different
      function. Second-conjugation past participles add `-ացել` to
      the stem (`կարդալ → կարդացել`).
gaps:
  - "Russian-side citations not yet added — parnasyan and tioyan both treat perfect tenses but not pulled in this v1. Adding would triangulate to multi-attested."
  - "Negation not directly cited here — pattern is straightforward (չ-prefix on the auxiliary, with movement: `չեմ գրել, չէի գրել`). Cited from `topics/morphology/negation.md` Pattern 1."
  - "Aorist vs perfect aspectual distinction — this topic mentions both but doesn't fully formalise when to use which. See `topics/morphology/aorist.md` § 'Aorist vs perfect.'"
  - "For irregular verbs the past participle is built off the *aorist stem*, not the infinitive (e.g. ուտել → կերած, գալ → եկած). Cross-referenced from `topics/morphology/irregular_verbs.md` and `topics/morphology/participles.md`."
  - "Resultative tenses (using -ած/-ացած, e.g. `գրած եմ` 'I have it written / it stands written') are a parallel system; not covered here. Worth its own topic."
---

# Perfect and pluperfect tenses

Armenian's perfect tenses (perfect + pluperfect) are **analytic
constructions**: past participle of the lexical verb +
auxiliary `եմ` (in present form for perfect, past form for
pluperfect). [#1] They sit alongside the aorist and imperfect to
form a four-way past-tense system in the indicative mood.

## Formation

> **Sakayan [#1]**: "Armenian uses the perfect and pluperfect to
> express actions that took place in the past. They are compound
> tenses formed by combining the auxiliary verb `եմ`, in the
> present and imperfect tense respectively, with the past
> participle (ending either in `-ել /-ացել`) of the base verb."

### Past participle

> **Sakayan [#2]**: "For first-conjugation verbs (ending in `-ել`),
> the infinitive and the past participle coincide."

| infinitive | class | past participle |
|-----------|-------|----------------|
| գրել "to write" | 1st | գրել "[having] written" |
| սիրել "to love" | 1st | սիրել "[having] loved" |
| կարդալ "to read" | 2nd | կարդացել |
| մնալ "to stay" | 2nd | մնացել |

The class binary (`-ել` vs `-ալ`) determines the participle suffix:
1st conj keeps `-ել` (no change), 2nd conj adds `-ացել` (replacing
`-ալ`). For irregular verbs, the past participle is built off the
*aorist stem* (see `topics/morphology/irregular_verbs.md`):
ուտել → կեր**ած** (and կերել in some uses), գալ → եկ**ել**.

### The two compound tenses

| tense | structure | gloss | example |
|-------|-----------|-------|---------|
| **perfect** | past participle + present aux | "have V-ed" | գրել **եմ** "I have written" |
| **pluperfect** | past participle + past aux | "had V-ed" | գրել **էի** "I had written" |

Both work for both conjugation classes:

| | 1st conj (գրել) | 2nd conj (կարդալ) |
|--|---|---|
| perfect | գրել եմ "I have written" | կարդացել եմ "I have read" |
| pluperfect | գրել էի "I had written" | կարդացել էի "I had read" |

## Aspectual / temporal use

Perfect: past action with present relevance, or experience reading.
- `Արամը նամակ գրել է:` "Aram has written a letter [now there
  exists a letter]."
- `Նա ֆրանսիայում եղել է:` "He has been to France [as
  experience]."

Pluperfect: past action prior to another past reference point.
- `Մինչև գալս նա արդեն գրել էր:` "Before I came, he had
  already written."

## Negation

Pattern 1 from `topics/morphology/negation.md`: `չ-` prefixes the
auxiliary, which then moves before the participle.

| affirmative | negative |
|-------------|----------|
| գրել եմ "I have written" | չեմ գրել "I haven't written" |
| գրել էի "I had written" | չէի գրել "I hadn't written" |
| կարդացել եմ | չեմ կարդացել |

## Contrastive notes

**For an English L1**: perfect (`գրել եմ`) and pluperfect
(`գրել էի`) map closely onto English `have written` and `had
written`. The structural template is the same: auxiliary +
participle. Memorise the participle form per verb (especially the
1st-conj coincidence with infinitive — that's a free pedagogy win)
and the rest is mechanical.

**For a Russian L1**: Russian doesn't have separate perfect /
pluperfect tenses — the *прошедшее совершенное* (perfective past)
covers both readings via context. So Armenian's distinction is
*more* fine-grained than Russian. Russian L1 learners need to
*notice* when present-relevance is being signalled and use the
perfect (`գրել եմ`) over the aorist (`գրեցի`). The pluperfect
particularly has no Russian counterpart — Russian uses *уже было*
or temporal adverbs to convey the same.

## Cross-references

- `topics/morphology/aorist.md` — Armenian's other major past tense;
  aspectual contrast.
- `topics/morphology/participles.md` — the past participle is one
  of the four "bound" participles.
- `topics/morphology/auxiliary_e.md` — the `եմ` paradigm that
  drives compound tenses.
- `topics/morphology/irregular_verbs.md` — past participles built
  off aorist stems.
- `topics/morphology/negation.md` — how `չ-` prefixes and moves.
