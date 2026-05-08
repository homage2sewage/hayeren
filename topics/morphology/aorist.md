---
topic: aorist (simple past) tense in Eastern Armenian
domain: morphology
units: [sakayan:4]
related: [verb-classes, present-tense, negation, perfect-tenses, irregular-verbs]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 99
    y_range: [100, 250]
    verbatim_quote:
      - "The aorist (simple past) tense"
      - "the only simple tense in the conjugation paradigm"
      - "completed action in the past"
      - "գրեցի"
      - "կարդացի"
      - "գրել"
      - "կարդալ"
    supports: supported
    note: |
      sakayan's canonical statement: the aorist is *the only simple
      (synthetic) tense* in the Armenian indicative mood — all other
      tenses are analytic (participle + auxiliary). Expresses a
      completed past action without duration/progression. Examples:
      գրեցի "I wrote / I have written" (from գրել), կարդացի "I read /
      I have read" (from կարդալ). Pattern differs by conjugation
      class (-ել → `-եց-`; -ալ → `-աց-`).
  - id: 2
    book: sakayan
    page: 100
    y_range: [60, 400]
    verbatim_quote:
      - "Knowledge of the aorist forms is important"
      - "other verbal forms are derived"
      - "infinitive or the aorist stem"
      - "irregular aorist forms"
    supports: supported
    note: |
      sakayan emphasises the aorist's structural centrality: many
      non-finite forms (past participle, perfect-driver, resultative)
      are built from the *aorist stem*, which differs from the
      infinitive stem in irregular verbs. The aorist isn't just one
      tense — it's the source of half the analytic-tense system. This
      is why irregular verbs are classified by their aorist stem
      (see `topics/morphology/irregular_verbs.md`).
  - id: 3
    book: sakayan
    page: 100
    y_range: [490, 580]
    verbatim_quote:
      - "negative forms of the aorist"
      - "prefixing the negative marker"
    supports: supported
    note: |
      negation of the aorist follows pattern 1 from
      `topics/morphology/negation.md` — `չ-` prefix on the verb form
      (no auxiliary involved since aorist is simple/synthetic).
      Examples: գրեցի → չգրեցի "I didn't write."
gaps:
  - "Per-verb aorist-stem irregularities (`գալ → եկա`, `անել → արեցի/արի`, `տեսնել → տեսա`, etc.) need explicit cataloguing — partly in `paradigms_data.PARTICIPLES` and sakayan p354-355 table, cited from `topics/morphology/irregular_verbs.md` but not duplicated here."
  - "Russian/parnasyan/tioyan don't have direct citations on this page yet — would strengthen `attestation` to triangulated. Russian-language treatments use term *прошедшее совершенное* (literally 'past perfective'), which maps onto Armenian aorist."
  - "Aspectual semantics: aorist is described by sakayan as 'completed without duration', but its precise relationship to perfect (`գրել եմ`) and to imperfect (`գրում էի`) — when does Armenian use which? — is undertreated."
  - "Phonological alternations in stems (e.g. -ել vs -իլ shifts) when -եց- attaches: not addressed at the topic-level here."
---

# Aorist (simple past) in Eastern Armenian

The aorist — Armenian's simple past — is the **only synthetic tense**
in the indicative mood. [#1] All other tenses (present, imperfect,
perfect, future) are analytic combinations of *participle + auxiliary*.
The aorist stands alone with a single verb form carrying tense, person,
and number.

## Formation

> **Sakayan [#1]**: "The aorist or the simple past is the only simple
> tense in the conjugation paradigm of the [Armenian] indicative
> mood. It expresses a completed action in the past without any
> implication of duration or progression."

For regular verbs, the aorist is formed by:

1. Strip the infinitive ending (`-ել` for 1st conj, `-ալ` for 2nd
   conj).
2. Add the class-conditioned **aorist linking suffix**:
   - 1st conjugation (`-ել` verbs): `-եց-`
   - 2nd conjugation (`-ալ` verbs): `-աց-`
3. Add personal endings (different from present-tense endings):
   `-ի, -իր, ø, -ինք, -իք, -ին`.

Examples [#1]:

| infinitive | class | aorist 1sg | gloss |
|-----------|-------|-----------|-------|
| գրել | 1st | գր**եց**ի | "I wrote / have written" |
| կարդալ | 2nd | կարդ**աց**ի | "I read / have read" |
| խոսել | 1st | խոս**եց**ի | "I spoke" |
| մնալ | 2nd | մնա**ց**ի | "I stayed" |

Full paradigm of `գրել` (1st conjugation):

| | sg | pl |
|--|----|----|
| 1st | գրեցի | գրեցինք |
| 2nd | գրեցիր | գրեցիք |
| 3rd | գրեց | գրեցին |

## Why the aorist matters beyond simple-past

> **Sakayan [#2]**: "Knowledge of the aorist forms is important as
> other verbal forms are derived [from] the infinitive or the aorist
> stem."

The aorist *stem* (the part before the personal ending — for `գրեցի`
that's `գր-`, for `կարդացի` that's `կարդ-`) is the root from which
several non-finite forms are built:

- **Past participle** (`-ել/-ացել`) → drives perfect tenses (`գրել եմ`,
  `կարդացել եմ`).
- **Resultative participle** (`-ած/-ացած`) → drives resultative
  tenses (`գրած եմ`).
- **Imperative** in some forms.

For irregular verbs, the aorist stem deviates from the infinitive
stem (e.g. `գալ → եկ-`, `ուտել → կեր-`, `տեսնել → տես-`). Knowing
the aorist of a verb means knowing how to form half of its
analytic tenses too. See `topics/morphology/irregular_verbs.md`.

## Negation

> **Sakayan [#3]**: "The negative forms of the aorist are constructed
> by prefixing the negative marker [`չ-`]."

Pattern 1 from `topics/morphology/negation.md`: `չ-` prefix directly
on the verb form. No auxiliary movement (since aorist is synthetic).

| affirmative | negative |
|-------------|----------|
| գրեցի "I wrote" | չգրեցի "I didn't write" |
| կարդացի "I read" | չկարդացի "I didn't read" |
| եկա "I came" | չեկա "I didn't come" |

## Aorist vs perfect: aspectual choice

Armenian has both aorist (`գրեցի` "I wrote") and perfect
(`գրել եմ` "I have written"). When does each apply?

- **Aorist**: completed action at a specific past moment.
  *Երեկ նամակ գրեցի* "I wrote a letter yesterday."
- **Perfect**: action completed but with current relevance / as
  experience. *Երբևէ հայերեն գրել ե՞ս* "Have you ever written
  Armenian?"

This is broadly parallel to English's `wrote` vs `have written`
distinction — but Armenian is somewhat looser. In practice the
aorist is the default for past narration; perfect is reserved for
"experience / state" readings.

## Contrastive notes

**For an English L1**: Armenian's aorist + perfect distinction is
*close to but not identical* with English's simple past + present
perfect. Use aorist for narrative past (`I went, I saw, I conquered`);
use perfect for experience/state (`I have been to France`). When in
doubt, aorist is safer.

**For a Russian L1**: Russian's *прошедшее совершенное* (perfective
past) maps roughly onto Armenian's aorist. The Russian/Armenian
similarity is strong because both are synthetic, marked by stem +
suffix + person endings (Russian: `я написал`, Armenian: `գրեցի`).
Russian's *прошедшее несовершенное* (imperfective past)
corresponds more to Armenian's *imperfect* (`գրում էի` "I was
writing"), not to the aorist. Don't conflate.

## Cross-references

- `topics/morphology/verb_classes.md` — the `-ել/-ալ` binary
  determines the aorist linking suffix.
- `topics/morphology/irregular_verbs.md` — the high-frequency
  verbs whose aorist stems deviate.
- `topics/morphology/perfect_tenses.md` (TODO) — aorist's analytic
  cousin built from the aorist stem.
- `topics/morphology/negation.md` — `չ-` prefix on synthetic forms.
- `armenian-grammar.md` — original seed notes.
