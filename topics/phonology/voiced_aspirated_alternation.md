---
topic: voiced↔aspirated alternation in Eastern Armenian
domain: phonology
units: [sakayan:1, sakayan:2, sakayan:3]
related: [three-way-laryngeal-contrast, armenian-alphabet-phonology]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 18
    y_range: [300, 320]
    verbatim_quote: "The EA three-part consonant system consists of one voiced stop (line 1) and two types of voiceless stops, one unaspirated (line 2) and one aspirated (line 3):"
    supports: supported
    note: prose statement of the three-way distinction itself.
  - id: 2
    book: sakayan
    page: 30
    y_range: [520, 540]
    verbatim_quote: ["ընդունել", "§nt", "unel]"]
    supports: partially-supported
    note: |
      vocab-page line. Stitched across one Barz-Italic span (Armenian
      script "ընդունել") and two Armtrans spans ("[§nt" + "unel]").
      Aspiration in Sakayan's Armtrans is encoded by glyph layout, not
      a Unicode codepoint — the JSONL has no IPA "ʰ". The
      transliteration shows /nt/ where spelling has դ /nd/, witnessing
      the դ→թ alternation; Sakayan does not state the rule in prose.
  - id: 3
    book: sakayan
    page: 36
    y_range: [110, 120]
    verbatim_quote: ["կարդ-ում", "kart", "-um]"]
    supports: partially-supported
    note: |
      paradigm header. Armenian "կարդ-ում" + Armtrans "[kart" + "-um]"
      across separate spans. դ→թ alternation visible (kart vs spelled
      kard).
  - id: 4
    book: sakayan
    page: 42
    y_range: [365, 375]
    verbatim_quote: ["բարձր", "bart", "r]"]
    supports: partially-supported
    note: |
      vocab line. Armenian "բարձր" + Armtrans "[bart" + "r]" across
      separate spans (intervening "s" glyph and a baseline "§"
      diacritic on its own span). ձ→ց alternation: spelled /dz/,
      transliterated /ts/.
  - id: 5
    book: ghamoyan
    page: 39
    y_range: [215, 260]
    verbatim_quote:
      - "ձայնեղների շնչեղացում, խլացում"
      - "ընկեր-ընգեր"
      - "գդալ-քթալ"
    supports: supported
    note: |
      ghamoyan describes the same phenomenon class but with a wider
      typological framing: "aspiration of voiced consonants, devoicing,
      and the reverse" (ձայնեղների շնչեղացում, խլացում և հակառակը),
      attributed to the influence of individual dialects and idioms.
      The example list is bidirectional — ընկեր-ընգեր (voiceless→voiced,
      opposite of Sakayan's direction); գդալ-քթալ (voiced→aspirated,
      Sakayan's direction). Quote stitched across ghamoyan p39 spans.
gaps:
  - "Sakayan does not state the alternation as a rule. Ghamoyan attributes the broader class of shifts to dialect/idiom influence but doesn't characterize the conditioning environment phonetically. Whether any of the shifts are environment-sensitive (vs purely lexical) remains open."
  - "No frequency data — what proportion of voiced-stop tokens actually alternate in running text?"
  - "Etymological correlation unaddressed — does the alternation track native vs loan stratum (Iranian, Turkish, Russian)?"
  - "Many further examples in `armenian-grammar.md` (արդեն, շաբաթ, օգնական, հոգնում, վերջապես, …) are not yet citation-checked against the JSONL."
---

# Voiced↔aspirated alternation in Eastern Armenian

In some words, written voiced stops and affricates (բ, գ, դ, ձ, ջ) are
pronounced as their aspirated or voiceless counterparts. Sakayan
treats this as **lexically irregular** within the literary standard —
no rule predicting which words alternate, observable only via the
transliteration column. [#2] [#3] [#4] Ghamoyan reframes the same
phenomenon as part of a broader **dialect-influenced bidirectional
shift** characteristic of Yerevan colloquial speech. [#5]

## The three-way contrast it deviates from

Eastern Armenian distinguishes three laryngeal series across stops and
affricates: **voiced / voiceless-unaspirated / voiceless-aspirated**.
[#1]

| voiced | voiceless | aspirated |
|--------|-----------|-----------|
| բ /b/  | պ /p/     | փ /pʰ/    |
| դ /d/  | տ /t/     | թ /tʰ/    |
| գ /g/  | կ /k/     | ք /kʰ/    |
| ձ /dz/ | ծ /ts/    | ց /tsʰ/   |
| ջ /dʒ/ | ճ /tʃ/    | չ /tʃʰ/   |

(Western Armenian has collapsed this — outside this topic's scope.)

## Sakayan's lexical-irregularity account

| pair | spelled | pronounced | source |
|------|---------|------------|--------|
| դ → թ | ընդունել "to accept" | [ընթունել] | [#2] |
| դ → թ | կարդում "reading"   | [կարթում]   | [#3] |
| ձ → ց | բարձր "high"        | [բարցր]    | [#4] |

Further examples carried over from `armenian-grammar.md` but **not
yet citation-checked**:

- **դ → թ**: արդեն → [արթեն]
- **դ → տ**: Այդ → [այտ], դուրդ → [դուրտ]
- **բ → փ**: շաբաթ → [շափաթ]
- **գ → ք**: օգնական → [օքնական], հագուստ → [հաքուստ], անգամ → [անքամ], հոգնում → [հոքնում]
- **ձ → ց**: փորձարկում → [փորցարկում]
- **ջ → չ**: վերջապես → [վերչապես], առողջություն → [առողչություն]

## Wider scope in colloquial speech (Ghamoyan)

Ghamoyan documents a *broader* phenomenon in Yerevan colloquial: [#5]

> "Yerevan colloquial language is characterized by certain
> articulatory shifts of consonants, especially under the influence of
> individual dialects and idioms — **aspiration of voiced consonants,
> devoicing, and the reverse**."

The shifts go in **both directions**:

| direction | example | comment |
|-----------|---------|---------|
| voiced → aspirated | գդալ → քթալ ("spoon") | Sakayan's direction |
| voiceless → voiced | ընկեր → ընգեր ("friend") | opposite |
| voiceless → voiced | ընկնել → ընգնել ("to fall") | opposite |
| voiceless → voiced | հանկարծ → հանգարծ ("suddenly") | opposite |

Ghamoyan attributes this to **dialect / idiom influence** (առանձին
բարբառների և խոսվածքների ազդեցության հետևանքով) — a typological
framing Sakayan doesn't offer. The two accounts together suggest the
phenomenon Sakayan presents as lexical idiosyncrasy in the literary
norm is, in colloquial Yerevan, a much wider zone of dialect-driven
phonological drift around the three-way contrast.

## What the alternation is *not*

Two phenomena that look like alternation but are predictable
allophonic processes, not lexical:

- **Vowel glide**: `ի` between vowels surfaces as /j/ — `միլիոն` →
  /milyon/.
- **Epenthetic schwa**: `ə` inserted into consonant clusters —
  `փոքր` → [pʰokʰər].

Both are suppressed by `sakayan/phonetics.py`'s deviation detector
and are *not* deviations from spelling in the sense relevant here.

## Contrastive notes

**For an English L1**: the actual trap is *the unaspirated row*
(պ տ կ ճ ծ), not the alternation. English voiceless stops are
aspirated word-initially, so learners reflexively map English /p t k/
onto Armenian aspirated (փ թ ք) and undercount the unaspirated
category. The aspirated row is "free" for English speakers; the
unaspirated row needs deliberate practice.

**For a Russian L1**: Russian has *no* aspiration distinction — all
voiceless stops are unaspirated by default. So the Armenian aspirated
row (փ թ ք չ ց) is the unfamiliar one and needs deliberate practice;
the voiced/voiceless contrast (բ/պ, դ/տ, գ/կ) maps cleanly onto
Russian (б/п, д/т, г/к). The alternation phenomenon documented here
is *more disorienting* for Russian L1 learners than for English L1:
Russian spelling-pronunciation is largely transparent for stops, so a
written voiced consonant pronounced as something other than voiced
has no obvious Russian analogue.

## Open questions / gaps

Mirrored from frontmatter:

- Sakayan exemplifies but does not state the alternation as a rule;
  ghamoyan attributes the broader class of shifts to dialect/idiom
  influence but doesn't characterize the *conditioning environment*
  phonetically. Whether any of the shifts are environment-sensitive
  (vs purely lexical) remains open.
- Frequency / token-count: how often does the alternation actually
  occur in running text?
- Etymological correlation (native vs Iranian/Turkish/Russian loan
  stratum) is unaddressed by both books.
- A descriptive grammar — Dum-Tragut (2009) — would likely close the
  remaining gaps; but with ghamoyan now citable, the most pressing
  open question shifts from "what is the rule" to "what's the
  conditioning environment".

## Cross-references

- `topics/phonology/three_way_laryngeal_contrast.md` — the underlying
  contrast that the alternation deviates from.
- `sakayan/phonetics.py` — implementation of the deviation detector
  used to surface alternations on flashcards.
- `armenian-grammar.md` (parent file, pending split) — the original
  notes that seeded this topic.
