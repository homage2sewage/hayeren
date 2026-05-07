---
topic: three-way laryngeal contrast in Eastern Armenian
domain: phonology
units: [sakayan:1]
related: [voiced-aspirated-alternation, armenian-alphabet-phonology]
status: draft
attestation: multi-attested   # sakayan + ghamoyan + parnasyan
sources:
  - id: 1
    book: sakayan
    page: 18
    y_range: [295, 320]
    verbatim_quote: "The EA three-part consonant system consists of one voiced stop (line 1) and two types of voiceless stops, one unaspirated (line 2) and one aspirated (line 3):"
    supports: supported
    note: prose statement of the contrast in the literary standard.
  - id: 2
    book: sakayan
    page: 18
    y_range: [330, 370]
    verbatim_quote:
      - "(1)  voiced stops"
      - "բ"
      - "[b]"
      - "(2)  unaspirated stops"
      - "պ"
      - "[p]"
      - "(3)  aspirated stops"
      - "փ"
    supports: supported
    note: |
      the three-row table immediately below the prose statement.
      Each row lists 5 segments (labial / velar / dental stops + two
      affricate places). Verifies all three rows are present.
  - id: 3
    book: sakayan
    page: 18
    y_range: [215, 240]
    verbatim_quote:
      - "A similar two-part system can be found in other Indo-European languages."
      - "Compare"
      - "the one in English"
      - "b / p"
      - "g / k"
      - "d / t"
    supports: supported
    note: contrastive paragraph showing English's two-way pattern as a foil.
  - id: 4
    book: ghamoyan
    page: 39
    y_range: [215, 260]
    verbatim_quote:
      - "ձայնեղների շնչեղացում, խլացում"
      - "ընկեր-ընգեր"
      - "գդալ-քթալ"
    supports: supported
    note: |
      ghamoyan describes Yerevan-colloquial articulatory shifts among
      the three series ("aspiration of voiced, devoicing, and the
      reverse") under dialect/idiom influence. The system of three
      series is preserved; individual lexemes shift between them.
  - id: 5
    book: parnasyan
    page: 21
    y_range: [4140, 5300]
    verbatim_quote:
      - "Система согласных армянского языка отличается от русско"
      - "глухих придыхательных"
      - "отсутствием противопоставления согласных по твердости"
    supports: supported
    note: |
      Russian-language enumeration of how Armenian's consonant
      system differs from Russian's: presence of affricates with
      three-way contrast, presence of aspirated voiceless row
      (Russian has no aspiration distinction), voiced velar գ,
      glottal aspirated հ, and absence of the palatalisation contrast
      (Russian's hard/soft distinction). This passage book-grounds
      the Russian-L1 contrastive note in the body of this topic.
      OCR'd at avg confidence 87 across the 3 fragments.
  - id: 6
    book: tioyan
    page: 50
    y_range: [1100, 1330]
    verbatim_quote:
      - "трехчленных рядов"
      - "звонкий — глухой — глухой придыхательный"
      - "русском языке"
      - "звонкий — глухой"
      - "немецком"
    supports: supported
    note: |
      tioyan's explicit Russian-language statement of the three-way
      contrast — "the Armenian consonant system has several
      three-member rows: voiced — voiceless — voiceless aspirated"
      — and a comparative typology: Russian has only the
      voiced-voiceless pair (б-п, в-ф); English and German pair
      voiced-aspirated (b-p^h, d-t^h). This is the *cleanest single
      cross-linguistic typological statement* in our corpus on the
      three-way contrast — more explicit than parnasyan's
      enumeration. Triangulates sakayan + ghamoyan + parnasyan with
      a fourth source.
gaps:
  - "Phonetic implementation (VOT values, aspiration duration, voicing onset) is not measured by either source."
  - "Sakayan presents the contrast for stops + 2 affricate places (5 articulations × 3 phonations); whether the alveolar (ձ/ծ/ց) and palatal (ջ/ճ/չ) affricates form a unitary class or two distinct series is not discussed."
  - "Historical depth — Sakayan asserts EA matches Classical Armenian phonetically (p18); the historical claim is not itself argued in the surrounding pages."
  - "Quantitative dialect data — ghamoyan attributes lexical drift to dialect/idiom but doesn't quantify; what fraction of items shift, and along which axes, is open."
---

# Three-way laryngeal contrast in Eastern Armenian

Eastern Armenian distinguishes **three laryngeal series** across stops
and affricates: voiced, voiceless-unaspirated, and voiceless-aspirated.
[#1] [#2] This is unusual for Indo-European; most IE languages
(including English) have a two-way voicing contrast. [#3]

## The three rows

| voiced | unaspirated | aspirated |
|--------|-------------|-----------|
| բ /b/  | պ /p/       | փ /pʰ/    |
| գ /g/  | կ /k/       | ք /kʰ/    |
| դ /d/  | տ /t/       | թ /tʰ/    |
| ձ /dz/ | ծ /ts/      | ց /tsʰ/   |
| ջ /dʒ/ | ճ /tʃ/      | չ /tʃʰ/   |

The IPA superscript ʰ above is a linguistic gloss; Sakayan's
typesetting renders aspiration as a small `Œ`+`h` glyph cluster
(font F19) that does not appear as a Unicode codepoint in the JSONL.

## Comparison with English

English has a two-way contrast — voiced vs voiceless: `b/p`, `g/k`,
`d/t`. [#3] Sakayan uses this directly as the contrastive foil,
calling the EA system "unusual for Indo-European."

## Western Armenian collapse

Western Armenian has shifted to a two-part system under a sound shift,
described in the same passage at [#1]. Documenting that shift is
outside this topic's scope; see
`topics/phonology/eastern_vs_western_shift.md` (TODO) when written.

## Cross-dialectal status: Yerevan colloquial

Ghamoyan documents that Yerevan colloquial speech preserves the
**three-series system** but exhibits **lexical drift** between the
series under dialect / idiom influence. [#4] Specifically:
"aspiration of voiced consonants, devoicing, and the reverse"
(ձայնեղների շնչեղացում, խլացում և հակառակը).

This is the answer to "does Yerevan colloquial preserve the three-way
contrast?" — the *system* persists; the *membership* of specific
lexemes shifts. Examples include:

- ընկեր → ընգեր (voiceless k → voiced g)
- հանկարծ → հանգարծ (voiceless k → voiced g)
- գդալ → քթալ (voiced g → aspirated kʰ; voiced d → aspirated tʰ)

The coexistence of bidirectional shifts argues against the system
being on a path to collapse — both directions are documented, so the
contrast itself is robust. See
`topics/phonology/voiced_aspirated_alternation.md` for the full
treatment of the alternation phenomenon, which Sakayan also documents
within the literary standard but only in the voiced→aspirated
direction.

## Contrastive notes

**For an English L1**: the *unaspirated* row (պ կ տ ծ ճ) is the
unfamiliar category. English voiceless stops are aspirated word-
initially, so an English speaker reflexively maps /p t k/ onto
Armenian aspirated (փ թ ք) and undercounts the unaspirated set.
Practice on minimal pairs `պ/փ`, `տ/թ`, `կ/ք`.

**For a Russian L1**: Russian has the *aspirated* row missing — all
voiceless stops are unaspirated by default. So the Armenian
voiced/voiceless distinction (բ/պ, դ/տ, գ/կ) maps cleanly onto
Russian (б/п, д/т, г/к); the aspirated row (փ թ ք չ ց) is the
unfamiliar category. Practice on the same minimal pairs as above —
coming from the opposite side of the contrast. Parnasyan [#5]
makes this contrast explicit, listing four ways Armenian's
consonant system differs from Russian's: three-way affricates,
aspirated voiceless row, voiced velar գ, glottal aspirated հ, and
the absence of the palatalisation contrast (Russian's hard/soft
distinction). The aspirated-row gap and the no-palatalisation
point are the two that hit Russian L1 learners hardest.

## Sister phenomenon: alternation

In some words, the *voiced* row is pronounced as the corresponding
*aspirated* (or unaspirated) consonant despite the spelling. This is
the **voiced↔aspirated alternation** —
`topics/phonology/voiced_aspirated_alternation.md`. In the literary
standard (Sakayan) it's lexically irregular and one-directional; in
Yerevan colloquial (ghamoyan) it's part of a broader bidirectional
zone of dialect-driven drift.
