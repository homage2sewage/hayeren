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
  - id: 6
    book: tioyan
    page: 38
    y_range: [200, 260]
    verbatim_quote:
      - "զեղչ"
      - "զէխչ"
      - "скидка"
    supports: supported
    note: |
      tioyan attests `զեղչ [զէխչ]` "discount" — direct evidence
      of ղ → /χ/ (= խ) before voiceless չ. Same cluster-devoicing
      mechanism that drives the ղջ cluster cases (parnasyan p346
      [ахчик], [амбохч]) — supports the broader-than-lexical-root
      reading of ղ devoicing. The Russian gloss is "скидка."
  - id: 7
    book: dumtragut
    page: 39
    y_range: [371, 397]
    verbatim_quote:
      - "(c) fricative voice assimilation given below are NOT strict and general rules in SMEA: "
      - "they are only applied to one part of the lexicon (see below), whereas the other part is still "
    supports: supported
    note: |
      Dum-Tragut (§1.2.1 "Writing and pronunciation of SMEA
      consonants", book p22 = JSONL p39) explicitly frames devoicing,
      aspiration, s-aspiration and fricative voice assimilation as
      *lexically restricted* — applying to only part of the lexicon,
      with the rest pronounced as spelled, "often doublets." Directly
      corroborates Sakayan's lexical-irregularity account [#2][#3][#4].
  - id: 8
    book: dumtragut
    page: 39
    y_range: [444, 458]
    verbatim_quote: "In SMEA there is, in principle, no terminal devoicing: voiced consonants in general remain "
    supports: supported
    note: |
      Important nuance the textbook sources don't state: word-final
      devoicing is NOT a blanket rule in SMEA (book p22). Devoicing is
      conditioned (see [#9][#10]), not a general terminal-position
      process — so a deck respell must be per-lexeme, never a blanket
      "final voiced stop → voiceless."
  - id: 9
    book: dumtragut
    page: 40
    y_range: [385, 399]
    verbatim_quote: "If the medial or final voiced consonant follows a nasal, it may undergo devoicing and "
    supports: supported
    note: |
      States one of Dum-Tragut's three conditioning environments — the
      one our sources never characterised. Nasal environment: m+b
      (համբույր), n+d (անդամ, խնդիր, կենդանի), ŋ+g (անգամ). The other
      two environments are r-devoicing (after flap [r]/[ɾ]: մարդ, բարդ,
      արջ; attested [#11]) and intervocalic/post-vocalic (օդ, էգ, հոգի).
      The bracketed IPA is itself citable — see [#11]–[#13].
  - id: 10
    book: dumtragut
    page: 41
    y_range: [428, 441]
    verbatim_quote:
      - "it follows the voiced uvular fricative ["
      - "], [b] is only pronounced voiceless but not aspi-"
    supports: supported
    note: |
      The ղ exception (book p24): after the voiced uvular fricative ղ
      [ʁ], a following voiced stop devoices to *plain voiceless, not
      aspirated* ([p], not [pʰ]) — աղբ, աղբյուր, եղբայր, ողբալ.
      Attested IPA [#12] եղբայր [jɛχpɑjɾ]: ղ→[χ] and բ→[p]. This
      refines our existing "ղ→խ in voiceless clusters" note [#6] and the
      ղջ-cluster cases: ղ conditions both its own devoicing and the
      (un)aspiration of the following stop.
  - id: 11
    book: dumtragut
    page: 42
    y_range: [109, 124]
    verbatim_quote: ["մարդ", "[mɑɾtʰ]", "նյարդ", "[njɑɾtʰ]"]
    supports: supported
    note: |
      r-devoicing + aspiration, IPA byte-verified: մարդ "man" [mɑɾtʰ]
      (դ→[tʰ] after flap [ɾ]), նյարդ "nerve" [njɑɾtʰ]. The [tʰ] (vs the
      [t] of the unaspirated row, or the spelled voiced [d]) is the
      whole point — and it now verifies against the corpus, so an IPA
      respelling claim like մարդ → [mɑɾtʰ] can be checked, not just
      asserted. (y-window starts ~3pt above the baseline to include the
      raised superscript ʰ span.)
  - id: 12
    book: dumtragut
    page: 41
    y_range: [452, 466]
    verbatim_quote: ["աղբյուր", "[ɑχpjuɾ]", "եղբայր", "[jɛχpɑjɾ]"]
    supports: supported
    note: |
      The ղ exception, IPA byte-verified: աղբյուր "spring" [ɑχpjuɾ],
      եղբայր "brother" [jɛχpɑjɾ] — ղ→[χ] and the following բ→[p]
      *unaspirated* (contrast the aspirated [pʰ] of the r/nasal/vowel
      environments, e.g. [#11]). Direct evidence for [#10].
  - id: 13
    book: dumtragut
    page: 41
    y_range: [125, 139]
    verbatim_quote: ["դեղձ", "[dɛχtsʰ]", "աղջիկ", "[ɑχtʃʰik]"]
    supports: supported
    note: |
      Fricative voice assimilation / ղ-cluster devoicing, IPA
      byte-verified: դեղձ "peach" [dɛχtsʰ] (ղ→[χ], ձ→[tsʰ]), աղջիկ
      "girl" [ɑχtʃʰik] (ղ→[χ], ջ→[tʃʰ]). The ղջ→[χtʃʰ] form is exactly
      the cluster our deck respells (`աղջիկ → [աղչիկ]`) approximate in
      Armenian script; here the full IPA is attested.
gaps:
  - "ADDRESSED by Dum-Tragut [#7][#9][#10]: the conditioning environment is now characterised — devoicing/aspiration applies after a flap [r], after a nasal, or intervocalically, with a ղ-exception (plain voiceless after uvular ʁ), but only across part of the lexicon (lexically restricted within those environments). The earlier open question (Sakayan exemplifies but states no rule; Ghamoyan attributes to dialect) is resolved: it is environment-conditioned AND lexically selective, not one or the other."
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

Dum-Tragut's reference grammar [#7]–[#10] reconciles the two: the
shifts are **environment-conditioned _and_ lexically selective**. They
occur in three phonological environments — after a flap [r], after a
nasal, or intervocalically — but only across *part* of the lexicon
within those environments, "often doublets." [#7] So neither account
is wrong: Sakayan sees the lexical selectivity (no rule predicts *which*
word), Dum-Tragut adds the conditioning that bounds *where* it can
happen at all. See "Dum-Tragut's conditioning environments" below.

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

### Note on **ջ → չ** specifically — root-level lexicalization

A 2026-05-09 audit of sakayan's own transliterations across
`cards/sakayan/*.tsv` found **systematic ջ → չ devoicing within
specific roots**, not just the two examples above. Every
`վերջ-`-stem derivative (վերջապես, վերջերս, վերջնական, վերջին),
every `առաջ-`-stem derivative (առաջ, առաջը, առաջին,
առաջարկել), the `մեջ-`-stem (մեջք), and the `քույր`-genitive
form (քրոջս) all surface with չ in sakayan's IPA-style
transliteration column.

Counterexample on record: **հաջորդ → [հաջորթ]** — the
`հաջ-`-stem keeps ջ voiced; only դ devoices.

Conclusion: ջ → չ is a **lexical-root regularity** (the
devoicing is consistent *within* the relevant roots and across
all their derivatives) but **not a phonological rule** —
synchronic environment doesn't predict whether a given root's
ջ devoices. The split is per-root and must be memorised.

Practical effect on the deck: `frequency/build_deck.py`'s
`PHONETIC_OVERRIDES` carries the bare roots and sakayan-
unattested derivatives of these four families that don't have
their own annotation in the source TSVs.

### Note on the **ղջ** cluster — broader cluster devoicing

A separate mechanism applies wherever the cluster ղջ appears:
**both consonants devoice**, ղ → /χ/ and ջ → /tʃʰ/. Parnasyan
p346 transliterates `աղջիկ` "girl" as **[ахчик]** and `ամբողջ`
"whole/entire" as **[амбохч]** — both members of the cluster
shifted to voiceless. Sakayan's own convention is to mark only
the ჯ → չ part in the respell (`առողջություն → առողչություն`,
unit-11 vocab); the ղ shift is real but isn't separately
notated in the Armenian-script respell column.

Coverage in the deck (`frequency/build_deck.py
PHONETIC_OVERRIDES`): աղջիկ → [աղչիկ], ողջ → [ողչ], ամբողջ →
[ամբողչ]. Same root family `առողջ-` is sakayan-attested via
`առողջություն`. Unlike the lexical-root regularity for մեջ-,
վերջ-, առաջ-, this cluster-devoicing mechanism is more general
(phonologically conditioned by the cluster), and adding new
ղջ-containing lemmas in the future is safe to extrapolate.

### Note on ղ → խ in voiceless clusters generally

The ղջ → խչ pattern above is one instance of a wider rule:
**ղ devoices to /χ/ (= խ) when adjacent to a voiceless
consonant**. Direct attestation from tioyan p38 [#6]:
*զեղչ [զէխչ]* "discount" — ղ before չ surfaces as խ. The
same phenomenon drives the ղջ-cluster cases (ղ + ջ → χ + č).

In Armenian script the surface of devoiced /ղ/ is /χ/, the
sound spelled խ. Sakayan's convention does not separately
notate this in respells (e.g. `առողջություն → առողչություն`
keeps the ղ in the bracket); we follow that convention to
keep respells one-character-at-a-time on the contrast-
affricate row. The ղ → խ shift is real but encoded in this
documentation rather than in the bracketed deck respell.

**`պղպեղ` "pepper"** — cluster `պղպ` not directly in our
corpus, but Wiktionary's pronunciation `/pəχpéʁ/`
([en.wiktionary.org/wiki/պղպեղ](https://en.wiktionary.org/wiki/%D5%BA%D5%B2%D5%BA%D5%A5%D5%B2))
confirms the same cluster-devoicing rule: the *first* ղ
(between two voiceless պ's) surfaces as `/χ/` (= խ); the
*second* ղ (word-final after stressed vowel) stays voiced
`/ʁ/`. Armenian-script respell would be `պխպեղ` — only the
first ղ shifts. Wiktionary is *not* a citation-checked source
in this workspace's sense (we ground citations in book JSONLs,
not external lookups), so this is recorded as an external
data-point pending a book-source attestation.

The bidirectional ղ behaviour in `պղպեղ` (one position
devoices, the other doesn't) is a clean illustration that
ղ-devoicing is **environment-conditioned**, not lexicalized
per-root: same ղ in same word, different position, different
outcome.

## Dum-Tragut's conditioning environments

Dum-Tragut's §1.2.1 (book pp22–26) is the first source in this
workspace to state the phonological conditioning. Up front it stresses
the rules are **"NOT strict and general… only applied to one part of
the lexicon"** [#7] — and that, **"in principle, no terminal
devoicing"** applies: a word-final voiced stop is not automatically
devoiced. [#8] Within that lexically-restricted scope, three
environments license devoicing-and-aspiration of voiced plosives/
affricates:

| environment | trigger | examples (IPA render-verified) |
|-------------|---------|-------------------------------|
| **r-devoicing** | after flap [r]/[ɾ] | մարդ [mɑɾtʰ], նյարդ [njɑɾtʰ] [#11]; բարդ [bɑɾtʰ], արջ [ɑɾtʃʰ] |
| **post-vocalic** | after / between vowels | օդ [ɔtʰ], էգ [ɛkʰ], հոգի [hɔkʰi] |
| **nasal** | m+b, n+d, ŋ+g | համբույր [hɑmpʰujɾ], անդամ [ɑntʰɑm], անգամ [ɑŋkʰɑm] [#9] |

(IPA byte-verified against the corpus — [#11] r-devoicing, [#12] the ղ
exception, [#13] ղ-cluster — now that the bracketed phonetics are
citable.)

Two refinements our textbook sources didn't have:

- **The ղ exception.** After the voiced uvular fricative ղ [ʁ], a
  following voiced stop devoices to **plain voiceless, *not* aspirated**
  — [p] not [pʰ]: աղբ [ɑχp], եղբայր [jɛχpɑjɾ], ողբալ [ɔχbɑl]. [#10]
  This is the same ղ-devoicing our [#6] / ղջ-cluster notes describe,
  now with the extra fact that ղ also *suppresses aspiration* on the
  stop it precedes.
- **Voiced stays voiced after [r] in specific strata** — dialectal
  loans (դարդ [dɑɾd], նարդի [nɑɾdi], բուրջ [buɾdʒ]), new loans, and
  reduplications (գրգիռ, բարբառ). So the [r] environment *enables*
  devoicing but the lexical/etymological layer still decides.

Dum-Tragut also separates two further processes from the voiced-stop
devoicing above: **(b) s-aspiration** of voiceless plosives before
sibilants (ապստամբել [ɑpʰstɑmbel]) and **(c) fricative voice
assimilation** in clusters (եղբայր, աղջիկ [ɑχtʃʰik], դեղձ [dɛχtsʰ]) —
the mechanism behind our ղջ-cluster respells.

**Practical effect on the deck.** The conditioning explains *why* the
respell families cluster the way they do (most attested respells sit in
an r/nasal/post-vocalic environment), but it does **not** license a
blanket "devoice every voiced stop after [r]" rule — [#7] and the
dialectal-loan counterexamples (դարդ stays [dɑɾd]) show the lexical
gate is real. Any new `PHONETIC_OVERRIDES` entry still needs per-lexeme
attestation (corpus IPA / transliteration), not extrapolation from the
environment alone.

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

- ~~Whether the shifts are environment-sensitive vs purely lexical~~
  **CLOSED by Dum-Tragut [#7][#9][#10]** (2026-06-19): both — they are
  environment-conditioned (flap [r] / nasal / post-vocalic, with a ղ
  exception) *and* lexically selective within those environments. See
  "Dum-Tragut's conditioning environments."
- Frequency / token-count: how often does the alternation actually
  occur in running text? **Still open** — Dum-Tragut gives word-lists,
  not corpus frequencies.
- Etymological correlation (native vs Iranian/Turkish/Russian loan
  stratum): **partially addressed** — Dum-Tragut notes that voiced
  stops *stay voiced* after [r] in dialectal/new loans (դարդ, նարդի)
  and reduplications, tying the lexical gate to stratum, but gives no
  systematic native-vs-loan breakdown.
- Many further examples in `armenian-grammar.md` (արդեն, շաբաթ,
  օգնական, …) are still not citation-checked against the JSONL.

## Cross-references

- `topics/phonology/known_transcriptions.md` — harvested table of all
  98 attested respells from the corpus (sakayan + hand-curated), with
  sources and a per-deviation tally.
- `research/2026-06-10-transcription-coverage-and-system.md` — deck
  coverage (45/1097) and the no-lookup expansion strategy
  (root-propagation / cluster-rule / why a blanket stop-rule is unsafe).
- `topics/phonology/three_way_laryngeal_contrast.md` — the underlying
  contrast that the alternation deviates from.
- `sakayan/phonetics.py` — implementation of the deviation detector
  used to surface alternations on flashcards.
- `armenian-grammar.md` (parent file, pending split) — the original
  notes that seeded this topic.
- `dumtragut/out/full.md` §1.2.1 "Writing and pronunciation of SMEA
  consonants" (book pp22–26) — the reference-grammar account of the
  conditioning environments [#7]–[#10]; `dumtragut/README.md` documents
  the IPA decode (the bracketed phonetics are now usable).
