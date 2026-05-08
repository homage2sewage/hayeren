---
topic: dialectal copula ըլնել as alternate to literary լինել
domain: morphology
units: []
related: [auxiliary-e, colloquial-copula-a, intimate-register]
status: draft
attestation: external-only
schema-deviation: |
  This topic's primary source is bararan.am (the standard
  Armenian-dictionary portal), not one of the four book corpora
  that the topic schema was designed around. citation-check will
  be unable to verify the verbatim_quote against a `<book>/out/
  full.jsonl` since no such file exists for this source. Flagged
  here so the topic can stand without breaking the
  book-attested-only invariant for everything else. Promote to
  `attestation: multi-attested` (or `single-source` cited from a
  book) when a textbook treatment of dialectal `ըլնել` is found
  in sakayan / ghamoyan / parnasyan / tioyan.
sources:
  - id: 1
    book: bararan.am
    url: https://bararan.am
    page: null
    y_range: null
    verbatim_quote:
      - "ըլնել [չեզոք բայ] (գավառական) Լինել:"
    note: |
      bararan.am dictionary entry for ըլնել. The square-bracket
      tag `[չեզոք բայ]` is the standard grammar abbreviation for
      *intransitive verb* (lit. "neutral verb"); `(գավառական)`
      is the dialectal/provincial register flag. The definition
      is the literary copula `Լինել:` "to be."
gaps:
  - "No book-corpus citation. Need to grep sakayan / ghamoyan / parnasyan / tioyan for explicit treatment of ըլնել; if found, promote attestation tier."
  - "Full inflection paradigm not given. The 3sg subjunctive `ըլնի` is real-world attested (see `research/2026-05-09-tweet-llm-comparison.md`); other paradigm cells (`ըլնեմ, ըլնես, ըլնենք, ըլնեք, ըլնեն` for subjunctive future; aorist; participle; etc.) are predicted by analogy with `լինել` but not enumerated by the bararan.am entry."
  - "Geographic dialect distribution (`գավառական` is a generic flag, not a specific region) is not given. Yerevan colloquial uses `ըլնել` forms; whether other dialect zones (Karabakh, Ararat-valley, diaspora) prefer it equally is unknown from this entry alone."
  - "Etymology / historical morphology — why the schwa-prosthesis `ը-` precedes `լնել` in dialect — is not addressed."
  - "Relation to the colloquial 3sg copula `ա` (covered in `topics/morphology/colloquial_copula_a.md`) is not formalised. `ա` replaces literary `է` in 3sg present indicative; `ըլնի` replaces literary `լինի` in 3sg subjunctive. Likely a parallel dialectal phenomenon affecting the same lexeme family but at different paradigm cells."
---

# Dialectal copula ըլնել

`ըլնել` is the dialectal alternate to the literary copula
`լինել` "to be." Per bararan.am [#1], it is a separately-listed
intransitive verb in the standard reference dictionary,
flagged `(գավառական)` (provincial / dialectal register).

This is the verb whose 3sg subjunctive form `ըլնի` appears
constantly in Yerevan colloquial speech and internet writing —
including the 2026-05-09 Pashinyan-tweet test case
(`research/2026-05-09-tweet-llm-comparison.md`), where four
external LLMs treated `ըլնի` as merely a phonetic deformation of
literary `լինի` rather than recognising it as a regular form of
a separately-attested dialectal lexeme.

## What bararan.am says

> **ըլնել** [չեզոք բայ] (գավառական) Լինել: [#1]

Reading:

- **`[չեզոք բայ]`** — *intransitive verb*. Standard Armenian
  grammar-term abbreviation; "չեզոք" literally "neutral" but in
  this metalinguistic context it's the conventional name for
  unaccusative / intransitive verbs.
- **`(գավառական)`** — dialectal / provincial register flag.
- **`Լինել:`** — definitional gloss: equivalent to the literary
  copula. The colon-terminus is bararan.am's standard format.

## Predicted paradigm (by analogy with լինել)

The bararan.am entry doesn't enumerate paradigm cells, but the
verb is regular and follows the standard `-ել` 1st-conjugation
pattern. By analogy with `լինել`'s irregular paradigm
(`լինեմ / եմ` etc.), the dialectal `ըլնել` should fill:

| | sg | pl |
|---|----|----|
| **subjunctive future 1** | ըլնեմ | ըլնենք |
| **subjunctive future 2** | ըլնես | ըլնեք |
| **subjunctive future 3** | **ըլնի** | ըլնեն |

The 3sg form `ըլնի` is the one with confirmed real-world
attestation (the Pashinyan tweet); other cells are predicted but
not corpus-verified. **Caveat**: this is paradigm extrapolation,
not citation — flag accordingly when surfacing.

The dialectal verb may also have its own irregular forms
parallel to `լինել`'s suppletive auxiliary (`եմ, ես, է, ենք,
եք, են`); whether `ըլնել` shares that suppletion or has a
regular paradigm throughout is unknown from this single source.

## Pragmatic distribution

Where literary Armenian uses 3sg subjunctive `լինի`, Yerevan
colloquial speakers freely use `ըլնի` — especially in:

- Exclamatory predicative constructions: *էսքան X մարդ ըլնի*
  "for a person to be this much (of an) X" (the Pashinyan-tweet
  shape).
- Conditional clauses: *եթե ըլնի* for *եթե լինի* "if there is."
- Subordinate `որ`-clauses introducing potentiality: *ուզում եմ
  որ ըլնի* for *ուզում եմ որ լինի* "I want there to be."

In each context, the dialectal form sounds *casual / Yerevantsi
/ in-group*; the literary form sounds *bookish / formal*.
Choosing `ըլնի` over `լինի` is itself a register marker.

## Relation to other colloquial-copula phenomena

This topic is one piece of a larger dialectal-copula complex
that also includes:

- **`ա` for `է` in 3sg present indicative**
  (`topics/morphology/colloquial_copula_a.md`) — `գնում ա`
  vs. literary `գնում է`.
- **The free auxiliary system** (`topics/morphology/
  auxiliary_e.md`) — present-tense `եմ, ես, է, ենք, եք, են`
  paradigm.

What's missing: a synthetic topic that documents the *whole*
dialectal-copula system across present indicative + subjunctive
+ aorist + participle, showing where literary and dialect agree
and where they diverge. `ըլնել` would be the dialectal infinitive
anchor; `ա` for `է` would be the 3sg-present substitution; etc.

## Contrastive notes

**For an English L1**: this is morphological complexity that
*looks* like Armenian "having two verbs for 'to be'" but is
actually one verb with a literary form and a dialect form. The
practical learner-rule: when reading Yerevan-flavored text
(internet, dialogue, casual register), expect `ըլն-` stems
where a textbook would have `լին-`.

**For a Russian L1**: somewhat parallel to Russian's literary /
colloquial alternation in copula-like constructions (e.g.
*является* vs ∅), though the Armenian case is straightforwardly
two cognate verb-forms rather than a presence/absence
alternation. The dialectal flag `(գավառական)` is roughly
equivalent in tone to Russian `прост.` / `разг.` markers.

## Cross-references

- `topics/morphology/colloquial_copula_a.md` — sister topic
  (3sg present `ա`).
- `topics/morphology/auxiliary_e.md` — auxiliary paradigm of
  literary `լինել` for contrast.
- `topics/pragmatics/intimate_register.md` — the broader register
  framework that motivates picking dialectal over literary
  forms.
- `transliteration-notes.md` § "register baked into spelling" —
  the same register signal in Latin-transliterated Armenian
  (`grum a` vs `grum e`).
- `research/2026-05-09-tweet-llm-comparison.md` — the canonical
  real-world test case where this topic should resolve `ըլնի`
  for the answering system.
