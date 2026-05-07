---
topic: consonant reductions in Yerevan colloquial speech
domain: phonology
units: [ghamoyan:2]
related: [yerevan-vowel-reductions, voiced-aspirated-alternation, three-way-laryngeal-contrast]
status: draft
attestation: single-source
sources:
  - id: 1
    book: ghamoyan
    page: 37
    y_range: [60, 200]
    verbatim_quote:
      - "Խոսակցական լեզվում բաղաձայների անկումը"
      - "պաճառ, անպաճառ, պաճեն, մաչելի, Մկրչյան"
      - "շաշատ"
      - "երաշտական"
      - "բշկական"
    supports: supported
    note: |
      cluster reductions where adjacent consonants of similar
      articulation collapse — տ-elision in պատճառ→պաճառ,
      Մկրտչյան→Մկրչյան; ժ-elision in երաժշտական→երաշտական,
      բժշկական→բշկական. Ghamoyan attributes this to articulation-place
      similarity and fast speech rate.
  - id: 2
    book: ghamoyan
    page: 37
    y_range: [250, 300]
    verbatim_quote:
      - "հրամայական"
      - "գրի"
      - "խոսի"
      - "նստի"
      - "մաքրի"
    supports: supported
    note: |
      imperative-final ր-drop. Ghamoyan: "almost all 2sg imperatives
      are pronounced without ր" — գրի՛ր→գրի՛, խոսի՛ր→խոսի՛, also
      նստի՛, կանգնի՛, մաքրի՛. Note that the imperative stress mark
      ՛ lives on its own JSONL spans separately from the letter, so
      fragments here capture the verb stem only.
  - id: 3
    book: ghamoyan
    page: 37
    y_range: [375, 415]
    verbatim_quote:
      - "Երևանի լեզվին հատուկ է նաև"
      - "կողմ"
      - "(էստեղ//այստեղ)"
      - "ընդե"
    supports: supported
    note: |
      ղ-drop in pronominal/locative forms — a hallmark of Yerevan
      speech. էստեղ/այստեղ → ըստե, էնտեղ/այնտեղ → ընդե, կողմ → կոմ,
      թող → թո. Direct quote stitched: "Yerevan language is
      characterized by the elision of ղ" + literary forms (in
      parentheses) + colloquial forms.
  - id: 4
    book: ghamoyan
    page: 37
    y_range: [420, 475]
    verbatim_quote:
      - "բառավերջում"
      - "չեմ գալի"
      - "չես բերե"
      - "չի տվե"
      - "Այս երևույթը գրական նորմի տեսանկյունից ընդունելի չէ"
    supports: supported
    note: |
      word-final լ/ս-drop in negated verb forms: չեմ գալիս→չեմ գալի,
      չես բերել→չես բերե, չի տվել→չի տվե, չի ասել→չի ասե. Ghamoyan
      explicitly marks this as "not acceptable from the standpoint of
      the literary norm" (Այս երևույթը գրական նորմի տեսանկյունից
      ընդունելի չէ) — i.e., a stigmatised feature of pure colloquial.
  - id: 5
    book: ghamoyan
    page: 38
    y_range: [65, 100]
    verbatim_quote:
      - "Նկատելի է բառավերջի"
      - "ֆոկու"
      - "ավտոբու"
      - "Թիֆլի"
    supports: supported
    note: |
      word-final s-voicing in loanwords (the *opposite* of elision —
      a substitution): ֆոկուս→ֆոկու{զ}, սոուս→սոու{զ}, Թիֆլիս→Թիֆլի{զ},
      գլոբուս→գլոբու{զ}, ավտոբուս→ավտոբու{զ}. Included as a related
      consonant-reduction-adjacent phenomenon — the final voiceless
      consonant doesn't elide but does shift towards lenition.
gaps:
  - "Phonological conditioning vs lexical conditioning: ghamoyan attributes cluster reductions (#1) to articulation-place similarity but ղ-drop (#3) and final-consonant drop (#4) are listed as lexical/morphological. Whether the phonological vs lexical split is real or artefactual to ghamoyan's classification is open."
  - "Frequency / register stratification within colloquial: ghamoyan calls #4 (final լ/ս-drop) explicitly stigmatised but lists #3 (ղ-drop) as 'characteristic of Yerevan' without comparable judgement. Sociolinguistic ranking of the reductions on a literary↔casual continuum would help."
  - "Geographic / generational variation: are these features uniform across Yerevan, or correlated with neighbourhood / age? Untreated."
  - "Interaction with other reductions — when multiple sites are eligible in the same word, which apply? E.g., a verb like խոսում ես ('you are speaking') with ղ in a following word."
  - "Loanword s-voicing (#5): is it specific to Russian-source loans, or broader? Untreated; the example list is Russian-heavy but not exclusive."
---

# Consonant reductions in Yerevan colloquial speech

Yerevan colloquial speech features a substantial set of consonant
reductions absent from the literary norm. Ghamoyan groups them into
three loose classes, each with distinct conditioning. [#1] [#2] [#3]
[#4] These reductions, taken together with the vowel reductions
catalogued separately (TODO: `yerevan_vowel_reductions.md`), account
for much of what makes spontaneous Yerevan speech sound compressed
and "fast" relative to the literary register.

## 1. Cluster reductions (articulation-place collapse)

When adjacent consonants share or nearly share place of articulation,
the preceding one is weakened or dropped — especially in fast speech.
[#1]

| literary | colloquial | what dropped |
|----------|------------|--------------|
| պատճառ "reason" | պաճառ | տ |
| անպատճառ "without fail" | անպաճառ | տ |
| Մկրտչյան (surname) | Մկրչյան | տ |
| երաժշտական "musical" | երաշտական | ժ |
| բժշկական "medical" | բշկական | ժ |
| շատ-շատ "very-very" | շաշատ | տ |

Ghamoyan attributes these to fast speech rate and articulatory
similarity ("articulation place is the same or close"). [#1]

## 2. Imperative-final ր-drop

Ghamoyan notes that "almost all 2sg imperatives are pronounced
without ր" [#2]:

| literary | colloquial |
|----------|------------|
| գրի՛ր "write!" | գրի՛ |
| խոսի՛ր "speak!" | խոսի՛ |
| նստի՛ "sit!" | (no ր to drop) |
| կանգնի՛ "stand!" | (no ր to drop) |
| մաքրի՛ "clean!" | (no ր to drop) |

The pattern is uniform across 1st-conjugation 2sg imperatives whose
literary form ends in `-իր`.

## 3. ղ-drop in pronominal and locative forms

A hallmark of Yerevan speech. [#3] Affects high-frequency pronominal
and locative items:

| literary | colloquial | gloss |
|----------|------------|-------|
| էստեղ / այստեղ | ըստե | "here" |
| էդտեղ / այդտեղ | ըտե | "there (medial)" |
| էնտեղ / այնտեղ | ընդե | "there (distal)" |
| կողմ | կոմ | "side" |
| թող | թո | "let, allow" |

Ghamoyan: *"Երևանի լեզվին հատուկ է նաև ղ բաղաձայնի անկումը"*
("ղ-elision is also characteristic of Yerevan language").

## 4. Word-final լ/ս-drop in negated verb forms (stigmatised)

Negated verb forms in colloquial speech often drop their final `լ` or
`ս`. [#4]

| literary | colloquial | gloss |
|----------|------------|-------|
| չեմ գալիս | չեմ գալի | "I'm not coming" |
| չես բերել | չես բերե | "you didn't bring" |
| չի տվել | չի տվե | "s/he didn't give" |
| չի ասել | չի ասե | "s/he didn't say" |
| չի տալիս | չի տալի | "s/he doesn't give" |

Ghamoyan flags this explicitly as **not acceptable from the
standpoint of the literary norm** (գրական նորմի տեսանկյունից
ընդունելի չէ) — i.e., stigmatised, more colloquial than the
ղ-drop of class #3.

## 5. Word-final s-voicing in loanwords (related, not strictly elision)

Ghamoyan documents a related but distinct phenomenon: word-final `ս`
in loanwords gets voiced to `զ`. [#5]

| literary | colloquial |
|----------|------------|
| ֆոկուս "focus" | ֆոկու{զ} |
| սոուս "sauce" | սոու{զ} |
| Թիֆլիս (toponym) | Թիֆլի{զ} |
| գլոբուս "globe" | գլոբու{զ} |
| ավտոբուս "bus" | ավտոբու{զ} |

This isn't elision — the `ս` doesn't drop, it lenites to `զ`. Worth
treating alongside the elision phenomena because it follows the same
"weakening of word-final consonants" gradient: drop in some cases
(class #4), voice in others.

## Cross-class observations

A loose lenition gradient runs across all five classes:

> *full articulation* (literary) → *weakening* (#5: voicing) →
> *cluster collapse* (#1) → *segment drop* (#2, #3, #4)

But ghamoyan doesn't formalise it this way; the gradient is the
present author's synthesis from the catalogued examples, and is
flagged in `gaps:` as a hypothesis to test against more data.

## Contrastive notes

**For an English L1**: English has comparable phenomena —
`going to → gonna`, final-t-glottalisation in `cat`, schwa-deletion
in `family /ˈfæm.li/`. The Yerevan reductions feel similar in
register: they're the kind of thing that marks a non-careful,
unmonitored speech mode. Don't try to imitate them in early study;
reproduce the literary forms first, recognise the colloquial reductions
second.

**For a Russian L1**: Russian has rich consonant reductions of
exactly the same flavour — `что /ʂto/`, `сегодня /sʲɪˈvodʲnʲə/`,
final-consonant devoicing in `дуб /dup/`. The Yerevan ղ-drop in
locative pronominals (`ըստե` for `էստեղ`) parallels Russian's
abbreviated pronoun forms in informal speech (`щас` for `сейчас`,
`ваще` for `вообще`). The cognitive template is "literary form X
is what schools teach; colloquial form Y is what you actually hear,
and educated speakers freely shift between them depending on register
and audience" — this is more familiar to a Russian L1 than to an
English L1, where written-spoken divergence is shallower.

The final-s-voicing in loanwords (#5) is the one feature with no
clean Russian parallel — Russian's word-final devoicing rule goes
the *opposite* direction (final voiced → voiceless), so an instinct
to apply Russian's rule will *over-voicelessen* and miss the
Armenian colloquial pattern.

## Open questions / gaps

(Mirrored from frontmatter.)

- Phonological vs lexical conditioning split.
- Frequency / register stratification *within* colloquial.
- Geographic / generational variation.
- Interaction when multiple reduction sites are eligible.
- Loanword s-voicing scope.

## Cross-references

- `topics/phonology/yerevan_vowel_reductions.md` (TODO) — companion
  catalogue for vowel-side reductions.
- `topics/phonology/voiced_aspirated_alternation.md` — bidirectional
  shifts among the three laryngeal series; partly overlaps with
  the loanword voicing in #5.
- `topics/phonology/three_way_laryngeal_contrast.md` — the system
  these reductions perturb.
- `topics/morphology/colloquial_copula_a.md` — companion register
  marker, also single-source from ghamoyan.
