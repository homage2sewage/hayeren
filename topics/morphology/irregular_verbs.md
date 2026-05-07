---
topic: irregular verbs in Eastern Armenian
domain: morphology
units: [sakayan:1, sakayan:11]
related: [verb-classes, present-tense, participles, negation]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 37
    y_range: [55, 220]
    verbatim_quote:
      - "The present tense of some irregular verbs"
      - "Three monosyllabic verbs"
      - "տալ"
      - "գալ"
      - "լալ"
      - "-իս"
      - "տալիս եմ"
      - "գալիս եմ"
      - "լալիս եմ"
    supports: supported
    note: |
      sakayan's intro to irregular verbs: three high-frequency
      monosyllabic verbs (տալ "to give", գալ "to come", լալ "to cry")
      use the participle ending `-իս` instead of the regular `-ում`
      to form the present tense (`տալիս եմ` "I give", not the
      hypothetical `*տալում եմ`). This `-իս` participle is the
      "synchronic" non-finite form (free + bound; see
      `topics/morphology/participles.md`) — it's used as a regular
      converb on most verbs but as a *bound* present-tense element
      only on these three.
  - id: 2
    book: sakayan
    page: 37
    y_range: [280, 460]
    verbatim_quote:
      - "two parallel sets of present tense"
      - "one irregular pattern and one regular"
      - "լինել"
      - "ունենալ"
      - "ունեմ"
      - "ունենում եմ"
      - "լինում եմ"
    supports: supported
    note: |
      sakayan introduces the two-paradigm pattern for լինել "to be"
      and ունենալ "to have": each verb has *two* present-tense
      paradigms — a short irregular one (լինել → եմ ես է …;
      ունենալ → ունեմ ունես ունի …) and a regular continuative one
      (լինում եմ; ունենում եմ). The short irregular form expresses
      a current state ("I am now / have now"), the regular
      continuative form a habitual one ("I usually am / have").
  - id: 3
    book: sakayan
    page: 354
    y_range: [100, 400]
    verbatim_quote:
      - "անել"
      - "առնել"
      - "ասել"
      - "բանալ"
      - "բերել"
      - "գալիս եմ"
      - "եկա"
      - "դառնալ"
      - "դարձա"
      - "դնել"
      - "ելնել"
      - "ելա"
    supports: supported
    note: |
      sakayan's grammar-tables appendix (pp. 354-355) — irregular
      verb table giving each verb its present, imperfect, aorist,
      subjunctive, and imperative forms in tabular layout. The
      irregularity is often in the *aorist stem* (e.g. գալ →
      `եկ-` aorist, դառնալ → `դարձ-`, ելնել → `ել-` aorist different
      from `ելն-` other-tense stem) rather than in the present.
      Coverage: ~19 verbs. Used here as a citation that the table
      exists and is accurate; specific paradigms are encoded in
      `sakayan/paradigms_data.PARTICIPLES`.
  - id: 4
    book: parnasyan
    page: 64
    y_range: [2380, 2480]
    verbatim_quote:
      - "Заучите также спряжение неправильного глагола"
      - "տալ"
    supports: supported
    note: |
      parnasyan in Russian: "Memorize also the conjugation of the
      irregular verb տալ 'to give'." Direct Russian-language
      acknowledgement of the irregular class. Parnasyan p333 has a
      dedicated "НЕПРАВИЛЬНЫХ ГЛАГОЛОВ" appendix section worth
      citing in revision.
  - id: 5
    book: tioyan
    page: 16
    y_range: [880, 970]
    verbatim_quote:
      - "нестандартного глагола"
      - "գալ"
    supports: supported
    note: |
      tioyan corroborates with the term "нестандартный глагол"
      (non-standard verb — tioyan's preferred Russian term for
      irregular). On p16, գալ "to come" is treated explicitly;
      կամ (an obsolete/literary existential form) is also flagged
      as nestandartny. Triangulation: sakayan + parnasyan + tioyan
      all converge on the same set of high-frequency irregulars.
gaps:
  - "Per-irregular-verb full paradigm tables not enumerated in this topic — partly because the Sakayan p354 table is tabular and citation-checking each cell would explode the source list. The data lives in `sakayan/paradigms_data.PARTICIPLES` (8 verbs covered) + the Sakayan appendix tables (19 verbs)."
  - "Why these specific verbs are irregular (etymological / historical reason — most are very ancient native Armenian roots that didn't undergo regular morphological levelling) is not addressed in any pedagogical source. Acharyan's etymological dictionary would help."
  - "Distinction between true irregular paradigms (entire stems differ) and minor irregularities (one form deviates) — sakayan's appendix mixes both. The full 'irregular' label can mean different things across the verbs."
  - "Tioyan's term `կամ` (existential) vs Sakayan's standard `եմ` paradigm — `կամ` appears in some classical/literary contexts but is largely obsolete. The relationship between `կամ` and `եմ` is a register/historical question untreated by the cited sources."
  - "Aorist stems for irregular verbs are often unpredictable (գալ → եկ-, ուտել → կեր-, լինել → եղ-). No general rule; must be memorised. Sakayan p354 gives them but doesn't explain *why*."
---

# Irregular verbs in Eastern Armenian

A small set of high-frequency verbs deviate from the regular -ել /
-ալ conjugation pattern. They fall into three loose groups:

1. **Three monosyllabic verbs** with a `-իս` (not `-ում`) present
   participle: տալ "to give", գալ "to come", լալ "to cry". [#1]
2. **Two existential / possessive verbs** with two parallel present
   paradigms (short irregular + regular continuative): լինել "to be"
   and ունենալ "to have". [#2]
3. **A wider class of ~19 verbs** with irregular *aorist stems*
   (different from the present stem) — listed in sakayan's
   grammar-tables appendix. [#3]

All four cited sources (sakayan, ghamoyan, parnasyan, tioyan) treat
these as a special class. [#1] [#3] [#4] [#5]

## Group 1: monosyllabic `-իս` trio

> **Sakayan [#1]**: "Three monosyllabic verbs, տալ to give, գալ to
> come, and լալ to cry deviate from the regular pattern: they form
> their indicative present tense with a participle ending in `-իս`,
> rather than the regular present participle ending in `-ում`."

Paradigm:

|  | տալ "to give" | գալ "to come" | լալ "to cry" |
|--|---------------|---------------|--------------|
| ես | տալիս եմ | գալիս եմ | լալիս եմ |
| դու | տալիս ես | գալիս ես | լալիս ես |
| նա | տալիս է | գալիս է | լալիս է |

… and so on through the persons. The auxiliary set is the same
(`եմ ես է ենք եք են`); only the participle suffix changes.

The `-իս` ending is the *synchronic / converb* participle (Armenian:
համակատար, "while-Ving"). For most verbs it functions as a free
converb (`գրելիս` "while writing"); for these three monosyllabic
verbs it does double duty as the bound present-tense participle.
See `topics/morphology/participles.md` for the wider system.

## Group 2: existential / possessive — two paradigms each

> **Sakayan [#2]**: "The verbs լինել to be and ունենալ to have have
> two parallel sets of present tense, one irregular pattern and one
> regular."

The split:

|  | irregular short | regular continuative |
|--|----------------|---------------------|
| լինել "to be" | եմ ես է ենք եք են | լինում եմ, լինում ես, … |
| ունենալ "to have" | ունեմ ունես ունի ունենք ունեք ունեն | ունենում եմ, ունենում ես, … |

The semantic distinction is **state vs habit**:

- *Short irregular* expresses **current state**:
  - `Ուսանող եմ։` "I am a student (now)."
  - `Մի հարց ունեմ։` "I have a question (now)."
- *Regular continuative* expresses **habitual state**:
  - `Հաճախ տանն եմ լինում։` "I'm often at home."
  - `Հաճախ ենք հանդիպում ունենում։` "We often have meetings."

Don't conflate them — picking the wrong paradigm misses the aspectual
nuance.

The "short irregular" forms of լինել double as the **auxiliary verb**
that drives all analytic tenses (present, perfect, future, etc.) —
see `topics/morphology/present_tense.md`. So the auxiliary system
itself is built from one of the language's irregular verbs.

## Group 3: aorist-stem irregularities (the wider table)

Sakayan p354-355 lists ~19 verbs with their full irregular paradigms.
Most of these have *regular* present (`-ում եմ`) but irregular
*aorist* stems. Selected examples [#3]:

| infinitive | present (regular) | aorist (irregular) | gloss |
|-----------|-------------------|--------------------|-------|
| անել | անում եմ | արեցի / արի | "to do" |
| առնել | առնում եմ | առա | "to take" |
| ասել | ասում եմ | ասացի | "to say" |
| գալ | գալիս եմ ⚡ | եկա | "to come" — also Group 1 |
| դառնալ | դառնում եմ | դարձա | "to become" |
| դնել | դնում եմ | դր(եց)ի | "to put" |
| ելնել | ելնում եմ | ելա | "to go up" |
| բերել | բերում եմ | բերեցի / բերի | "to bring" |
| բանալ | բացում եմ | բացեցի / բացի | "to open" |
| (more in sakayan p354-355) | | | |

The pattern: the *aorist stem* differs from the *infinitive stem* in
ways that have to be memorised per verb. There's no general rule.

Other tenses built off the aorist stem (perfect, pluperfect,
past participles) inherit the irregularity. So "irregular in aorist"
propagates through ~half the tense system.

For the eight high-frequency irregulars covered in
`sakayan/paradigms_data.PARTICIPLES` — `գրել, կարդալ, ունենալ,
լինել, գալ, տեսնել, ուտել, տալ` — the full participle tables are
encoded in code; the irregularity-in-stem propagates into each
non-finite form.

Notable per-verb stems from the participles topic:

- `գալ` (aorist `եկ-`): past participle `եկած`, active `եկող`.
- `ուտել` (aorist `կեր-`): past participle `կերած` (not `*ուտած`).
- `տեսնել` (aorist `տես-`): past participle `տեսած`.
- `լինել` (aorist `եղ-`): past participle `եղած`.

## Russian-side acknowledgement

Both Russian-language pedagogical sources name the class:

- **Parnasyan [#4]** uses *неправильный глагол* "irregular verb"
  (`Заучите также спряжение неправильного глагола տալ`).
- **Tioyan [#5]** uses *нестандартный глагол* "non-standard verb"
  (`спряжение нестандартного глагола գալ`).

Both terms cover the same set in practice. Tioyan's *нестандартный*
arguably has less of a "broken / wrong" connotation than Parnasyan's
*неправильный*, which matters pedagogically — these aren't broken,
they're just historically older.

## What this topic is *not*

- **Pseudo-suffix verbs** (2nd-conjugation verbs with intervening
  `-ան-`/`-են-`, e.g. ուշանալ, մոտենալ) are *regular* — see
  `topics/morphology/verb_classes.md`. The pseudo-suffix is
  predictable per-verb but not "irregular" in the sense used here.
- **Derivational variation** (a verb taking a different ending in a
  derived form, e.g. ընդունել "to accept" vs ընդունվել "to be
  accepted") is regular morphology, not irregularity.

## Contrastive notes

**For an English L1**: the three monosyllabic `-իս` verbs (տալ /
գալ / լալ) are the closest Armenian analogue to English's
"highest-frequency irregulars" (be, have, go, do). The two-paradigm
λinel/ouenal pattern has no English parallel — English doesn't
distinguish "I am (now)" from "I am (habitually)" with different
forms.

**For a Russian L1**: Russian also has irregular verbs (быть, идти,
ехать, etc.) and the mental model "memorise irregulars one at a time"
maps directly. The two-paradigm split for լինել / ունենալ is
*structurally similar* to Russian's habitual/continuous pair like
ходить vs идти (both translate "to go" but with different
aspectual nuance). That mental model is the right starting point.

The Russian-language sources [#4] [#5] make this explicit by using
the standard Russian linguistic terms.

## Open questions / gaps

(Mirrored from frontmatter.)

- Per-verb full paradigms not enumerated here; live in
  `sakayan/paradigms_data.PARTICIPLES` and Sakayan p354-355 table.
- Why these specific verbs are irregular (etymology) — Acharyan's
  dictionary would address.
- Aorist-stem unpredictability has no general rule.
- Tioyan's *կամ* (literary existential) vs *եմ* (Eastern Armenian
  standard) needs a register/historical clarification.

## Cross-references

- `topics/morphology/verb_classes.md` — the regular `-ել/-ալ` binary
  these verbs *deviate from*.
- `topics/morphology/present_tense.md` — the regular paradigm with
  imperfective participle + auxiliary.
- `topics/morphology/participles.md` — the eight non-finite forms,
  several of which are built from the aorist stem in irregulars.
- `topics/morphology/negation.md` — the negation pattern is the same
  for irregulars (just `չ-` prefix on the existing forms).
- `armenian-grammar.md` § "Irregular verbs" — original seed notes.
- `sakayan/paradigms_data.PARTICIPLES` — code-side per-verb data.
