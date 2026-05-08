---
topic: future and future-imperfect tenses in Eastern Armenian
domain: morphology
units: [sakayan:6]
related: [aorist, perfect-tenses, present-tense, participles, auxiliary-e, hypothetical-mood]
status: draft
attestation: single-source
sources:
  - id: 1
    book: sakayan
    page: 149
    y_range: [105, 230]
    verbatim_quote:
      - "FUTURE"
      - "FUTURE"
      - "IMPERFECT"
      - "Armenian has two future tenses in the indicative"
      - "future and future imperfect"
      - "Both are compound tenses"
      - "future participle ending in"
      - "-ելու"
      - "-ալու"
      - "գրելու եմ"
    supports: supported
    note: |
      sakayan's introduction of Armenian's two indicative future
      tenses: simple future (`գրելու եմ` "I will write / am going to
      write") and future imperfect (`գրելու էի`). Both are compound
      tenses combining the *future participle* (`-ելու` for 1st conj,
      `-ալու` for 2nd conj) with the auxiliary in present or past
      form respectively.
  - id: 2
    book: sakayan
    page: 150
    y_range: [60, 350]
    verbatim_quote:
      - "Formation of the future imperfect tense"
      - "The future imperfect"
    supports: supported
    note: |
      sakayan's section on the second future tense — future
      imperfect (also called "future in the past"). Built from the
      same future participle but with past-tense auxiliary
      (`գրելու էի, գրելու էիր, ...`). Used for actions that *were
      going to happen* from a past reference point.
gaps:
  - "Russian-side citations not pulled in this v1; would triangulate. Russian's *буду писать* (analytic future) is structurally similar (auxiliary + lexical verb), making this an easy Russian-L1 topic."
  - "Negation: pattern 1 from `topics/morphology/negation.md` for these compound tenses (`չեմ գրելու` 'I won't write'); cited there but not duplicated here."
  - "Hypothetical future I (`կգրեմ`) is a *different* future construction — it expresses speaker's strong belief or determination rather than a plain future. Covered in `armenian-grammar.md` (full system table) and would benefit from its own topic alongside the conditional/mandative complex."
  - "Aspectual difference between simple future and future imperfect: not crisply formalised here. Sakayan's p150-151 'Uses' subsections would clarify; not yet cited."
---

# Future tenses (indicative)

Eastern Armenian has **two indicative future tenses**: simple
future and future imperfect. [#1] Both are compound (analytic)
constructions: future participle + auxiliary `եմ` in present or
past form respectively.

A *third* future-like construction — the **hypothetical future**
(`կգրեմ` "I'd write / I will write [with conviction]") — uses a
different mood and a different formation; it's covered separately
(see `gaps:` below).

## Simple future

> **Sakayan [#1]**: "The future tense is formed by combining the
> future participle ending in `-ելու` or `-ալու` … and the
> conjugated forms of the auxiliary verb `եմ`."

| infinitive | future participle | future 1sg | gloss |
|-----------|-------------------|-----------|-------|
| գրել | գրելու | գրելու եմ | "I will write / am going to write" |
| կարդալ | կարդալու | կարդալու եմ | "I will read" |
| սիրել | սիրելու | սիրելու եմ | "I will love" |
| մնալ | մնալու | մնալու եմ | "I will stay" |

The class binary determines the future-participle suffix:
1st conj `-ել` → `-ելու`; 2nd conj `-ալ` → `-ալու`.

Full paradigm of `գրել`:

| | sg | pl |
|--|----|----|
| 1st | գրելու եմ | գրելու ենք |
| 2nd | գրելու ես | գրելու եք |
| 3rd | գրելու է | գրելու են |

## Future imperfect

> **Sakayan [#2]**: "Formation of the future imperfect tense …"

Same future participle, but the auxiliary is in the past tense.
Expresses "was going to V" — an action expected from a past
reference point that may or may not have actualised.

| | future | future imperfect |
|--|--------|------------------|
| 1sg | գրելու եմ | գրելու էի |
| 2sg | գրելու ես | գրելու էիր |
| 3sg | գրելու է | գրելու էր |

Use:
- `Վաղը գնալու եմ Մոսկվա:` "I'm going to Moscow tomorrow."
- `Երեկ գնալու էի, բայց ձյուն եկավ:` "Yesterday I was going to go,
  but it snowed."

The future imperfect is the natural future-in-the-past for narrative
contexts.

## Negation

Pattern 1 from `topics/morphology/negation.md`: `չ-` prefixes the
auxiliary, which moves before the participle.

| affirmative | negative |
|-------------|----------|
| գրելու եմ | չեմ գրելու |
| գրելու էի | չէի գրելու |

## Future vs hypothetical future

Armenian has *another* construction expressing future — the
**hypothetical future I** (`կգրեմ` "I would/will write [with
determination]"). It uses a different mood (hypothetical, a sub-mood
of indicative in some treatments) and prefixes `կ-` to the
subjunctive future form.

| construction | example | meaning |
|--------------|---------|---------|
| future indicative | գրելու եմ | "I will write" (neutral fact) |
| hypothetical future I | կգրեմ | "I'd write / I'll definitely write" (determination) |

Both translate to English "will write" but carry different shades.
See `gaps:` — hypothetical-mood topic deferred.

## Contrastive notes

**For an English L1**: future indicative = `will / am going to`;
future imperfect = `was going to`. The two-way distinction is
familiar. Hypothetical future is closer to "will surely" or
emphatic-determination "I'll write that letter [you can count on
it]." Memorise the future-participle suffix (`-ելու/-ալու`) per
verb; the rest is mechanical.

**For a Russian L1**: Russian's *аналитическое будущее* "buducheye"
(`буду писать` "I will write") is structurally identical to
Armenian's: auxiliary (`буду / գրելու եմ`) + lexical content.
Russian's analytic future uses `быть` + imperfective infinitive;
Armenian uses `եմ` + future participle. The mental model maps
cleanly. The future imperfect (`գրելու էի`) corresponds to Russian's
"я собирался писать" (analytic past intention) — periphrastic
rather than a single tense.

## Cross-references

- `topics/morphology/aorist.md`, `topics/morphology/perfect_tenses.md`
  — past system; future stands as the temporal mirror.
- `topics/morphology/participles.md` — the future participle is one
  of the four bound-and-free participles.
- `topics/morphology/auxiliary_e.md` — the auxiliary that combines
  with the future participle.
- `topics/morphology/negation.md` — `չ-` prefix and word-order
  change.
- `topics/morphology/subjunctive_mood.md` — subjunctive future is
  the input to hypothetical future I.
