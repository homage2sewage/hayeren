---
topic: verbal nouns and the -ում / -ք / -ած derivational system
domain: morphology
units: [sakayan:13, parnasyan:6, tioyan:8]
related: [aorist, participles, present-tense, irregular-verbs]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 207
    y_range: [275, 325]
    verbatim_quote:
      - "It functions as a verbal noun"
      - "indirectly refers to a person"
      - "complete sentences into nominal phrases"
    supports: supported
    note: |
      sakayan introduces the *infinitive-as-verbal-noun* construction
      (with possessive articles -ս, -դ, -ը/-ն). Personalised
      infinitives (e.g. "գրելս" = "my writing") that turn full
      sentences into nominal phrases. Distinct from the productive
      -ում / -ք / -ած derivations covered here, but it's the
      sakayan side of the verbal-noun phenomenon: every infinitive
      *can* function as a noun directly.
  - id: 2
    book: parnasyan
    page: 129
    y_range: [2800, 3220]
    verbatim_quote:
      - "образуются отглагольные существительные"
      - "կառուցել"
      - "կառուցում"
      - "строить"
      - "строительство"
    supports: supported
    note: |
      parnasyan's explicit section on verbal-noun formation. Worked
      example: կառուցել "to build" → կառուցում "construction /
      building" (the action-noun). Russian parallel:
      строить → строительство. This is the canonical -ում
      nominalization on the aorist stem.
  - id: 3
    book: parnasyan
    page: 48
    y_range: [700, 870]
    verbatim_quote:
      - "функции отглагольного существительного"
    supports: supported
    note: |
      parnasyan's earlier remark that the infinitive itself can
      perform "all the functions of a verbal noun" — which
      duplicates the sakayan p207 observation but in Russian.
      Triangulates the infinitive-as-noun reading.
  - id: 4
    book: tioyan
    page: 184
    y_range: [1830, 2000]
    verbatim_quote:
      - "существительные со значением действия"
      - "отглагольные"
      - "աղոթել"
      - "աղոթք"
      - "молитва"
      - "անիծել"
      - "անեծք"
    supports: supported
    note: |
      tioyan introduces the -ք suffix as a verbal-noun formant
      (collective / result-noun reading rather than process-noun).
      Worked pairs: աղոթել "to pray" → աղոթք "prayer";
      անիծել "to curse" → անեծք "curse". Russian glosses
      молитва / проклятие confirm the result-noun semantics.
  - id: 5
    book: tioyan
    page: 233
    y_range: [900, 990]
    verbatim_quote:
      - "образует отглагольные существительные"
    supports: partially-supported
    note: |
      tioyan documents an additional verbal-noun suffix in the
      same section. The exact suffix is OCR-mangled in our text
      (`-ш@р`, likely `-շար` or `-չար` / `-չում` depending on
      page bitmap). Confirms multiple suffixes in the system
      beyond -ում and -ք.
gaps:
  - "Productive vs non-productive: -ում is fully productive (any verb stem can take it); -ք and others are lexically restricted. We don't yet have a rule for *when* -ք is the right deriv vs -ում. Probably tracks animacy / aspect / register but isn't formalised in our sources."
  - "The participle vs verbal-noun overlap: -ում is also the imperfective participle suffix (`գրում եմ` 'I am writing'). For verbs whose present and aorist stems coincide, the two -ում forms are homophonous and disambiguated by syntactic position (auxiliary follows participle; standalone is noun)."
  - "Locative case in -ում: `քաղաքում` 'in the city' is yet another -ում that's neither participle nor verbal noun — case-marking on a noun. Three-way homophony (case / participle / nominalization) deserves a cross-reference but isn't covered by any single citable source."
  - "Tioyan p249 mentions a -յուն suffix for verbal nouns; not pulled into citations because the OCR'd context-window is small. Worth a follow-up read."
  - "Frequency / register data on which derivation a particular root takes — none of our sources quantify."
---

# Verbal nouns: -ում / -ք / -ած

Eastern Armenian has a productive system for turning verbs into
nouns. The most common nominalising suffix is **-ում** (action noun:
"the act of V-ing") attached to the **aorist stem**; alongside it,
**-ք** forms result/collective nouns and other suffixes (-ած, -ուստ,
-յուն) cover narrower senses. [#2] [#4]

## Why this matters

The user's car-wash example: `ավտոլվացում` "car wash" uses
`լվացում` — the verbal noun of `լվանալ` "to wash" — not the
infinitive itself. Russian and English collapse this distinction
silently (English has bare nominalization "wash, build, run"; Russian
sometimes adds a derivational suffix as in строительство / стройка).
Armenian forces an explicit deriv every time you want the noun.

## The main suffix: -ում on the aorist stem

> **Parnasyan [#2]**: *"которого образуются отглагольные
> существительные: կառուցել — կառուցում, строить —
> строительство…"*

The verbal-noun -ում attaches to the **aorist stem**. For verbs
where the present stem and aorist stem coincide (most regular -ել
verbs), the noun coincides in form with the imperfective participle:

| verb | pres stem | aor stem | -ում noun | gloss |
|------|-----------|----------|-----------|-------|
| գրել | գր- | գր- | գրում | "writing" (process) |
| կառուցել | կառուց- | կառուց- | կառուցում | "construction" |
| վճարել | վճար- | վճար- | վճարում | "payment" |
| հանդիպել | հանդիպ- | հանդիպ- | հանդիպում | "meeting" |

For irregular verbs and -ալ class verbs where the two stems
**differ**, the verbal noun visibly tracks the *aorist* stem, not
the present stem:

| verb | pres stem | aor stem | -ում noun | gloss |
|------|-----------|----------|-----------|-------|
| լվանալ | լվան- | լվաց- | **լվացում** | "wash" (e.g. ավտոլվացում) |
| ստանալ | ստան- | ստաց- | **ստացում** | "receipt, reception" |
| մնալ | մն- | մնաց- | **մնացում** | "remainder, balance" |
| դառնալ | դառն- | դարձ- | **դարձում** | "turn, conversion, U-turn" |
| տեսնել | տեսն- | տես- | **տեսում** | "view, sight, scene" |

The aorist-stem dependency is the *signature* of this nominalisation:
a learner reading `դարձում` "turn" should be able to recover the
aorist stem `դարձ-` (`դարձա` "I turned") and from there the
infinitive `դառնալ` "to become / turn." The participle form
`դառնում` (in `դառնում եմ` "I'm becoming") doesn't help — it
uses the present stem.

## The result-noun suffix: -ք

> **Tioyan [#4]**: *"существительные со значением действия
> (отглагольные существительные), …: աղոթել → աղոթք (молитва),
> անիծել → անեծք (проклятие)."*

Where -ում yields a *process* noun ("the act of V-ing"), -ք
yields a *result* or *collective* noun ("the V-ing as a thing"):

| verb | -ք noun | gloss |
|------|---------|-------|
| աղոթել | աղոթք | "prayer" (the spoken thing, not the act) |
| անիծել | անեծք | "curse" |
| լվանալ | լվացք | "laundry" (the things washed) |
| մտածել | մտածք | (rare; usually մտքեր) |
| վախենալ | վախ | "fear" (suffix lost — this one's irregular) |

The -ք set is **lexically restricted**, not productive — you can't
freely apply -ք to any verb. The pairs above are inherited from
older Armenian. For a modern productive nominalization, default to
-ում.

## Other suffixes (smaller productive set)

| suffix | sense | example |
|--------|-------|---------|
| -ած | past-participle / result-state | գրած "written (thing)"; can be nominalised |
| -ող | agent | գրող "writer"; one who Vs |
| -արան | locative | լվացարան "washbasin"; place where V happens |
| -ույթ | abstract event | ելույթ "speech, performance" (built off ելնել) |

The -ած suffix is more often used as the past participle in
compound tenses (see `topics/morphology/perfect_tenses.md`) than
as a free noun, but it does appear nominalised in fixed
expressions: `գրածներ` "(the) writings", `տեսածներ` "(the) things
seen."

## Three -ում homophones — keep them apart

A single Armenian word can be all three depending on context:

1. **Imperfective participle** — `գրում` in `գրում եմ` "I am
   writing." Built from *present* stem + -ում. Always paired with
   an auxiliary.
2. **Verbal noun (action)** — `գրում` "(act of) writing" as a
   standalone noun. Same form for regular verbs; differs for
   irregulars (the noun uses the aorist stem).
3. **Locative case ending** — `քաղաքում` "in the city," `տանը` /
   `տանում` "in the house." Marks position on any common noun.

Disambiguation is syntactic. A bare `-ում` form with an auxiliary
following → participle. A bare `-ում` form acting as the head of
a noun phrase (taking case endings, articles, modifiers) → verbal
noun. A bare `-ում` form attached to a noun stem (not a verb stem)
→ locative. The three layers don't compete at the same surface
position, so context resolves them — but learners who aren't
prepared can mis-parse `դասը հաշվում է` ("the lesson counts" —
where հաշվում is the participle, not noun) as "the lesson's
counting [noun]."

## Contrastive notes

**For an English L1**: English nominalises verbs by zero-derivation
(`a wash, a turn, a build-up`), `-ing` (`washing, building`), or
`-tion`/`-ment` (`construction, payment`). Armenian's -ում sits
closest to English `-ing` (process reading) and English `-tion`
(action-noun reading) at once. The trap: English `-ing` is also
the present participle, so the homophony with Armenian's -ում
participle / -ում noun is a familiar shape — but Armenian's
disambiguation is positional (auxiliary or no), not morphological.

**For a Russian L1**: Russian's отглагольное существительное
("verbal noun") is exactly the same construct, formed by suffixes
like *-ние* (написание "writing, the process"), *-тельство*
(строительство "construction"), *-ка* (стирка "wash, laundry"),
*-ость* (бледность "paleness"). Armenian's -ում maps onto Russian
*-ние / -тельство*; Armenian's -ք maps onto *-ка* and *-ность*
in different cases. The semantic split (process vs result) is
parallel; the suffix selection is per-lexeme in both languages
and just has to be memorised.

## Cross-references

- `topics/morphology/aorist.md` — aorist stem (the input to the
  -ում nominalization for irregulars).
- `topics/morphology/participles.md` — imperfective -ում participle
  vs the noun -ում (homophony).
- `topics/morphology/case_system.md` — locative case in -ում
  (third homophone).
- `topics/morphology/irregular_verbs.md` — verbs whose present /
  aorist stems differ (and thus whose verbal noun visibly differs
  from the participle).
- `armenian-grammar.md` — original notes (will gain a pointer
  here when the parent file is next refreshed).
- `cards/top_1000.tsv` — currently has the verbs but not their
  derived nouns; candidate for hand-curated deck additions.
