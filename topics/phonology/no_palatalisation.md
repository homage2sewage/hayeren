---
topic: absence of palatalisation contrast in Eastern Armenian
domain: phonology
units: [sakayan:1]
related: [three-way-laryngeal-contrast, voiced-aspirated-alternation]
status: draft
attestation: single-source
sources:
  - id: 1
    book: parnasyan
    page: 21
    y_range: [5080, 5500]
    verbatim_quote:
      - "отсутствием противопоставления согласных по твердости"
      - "Армянские согласные произносятся твердо"
      - "смягчаются"
    supports: supported
    note: |
      parnasyan's explicit Russian-language statement: "[the
      Armenian consonant system is characterized by] the absence of
      a hard/soft (palatalisation) contrast. Armenian consonants are
      pronounced hard and barely soften." This is the *fifth point*
      in parnasyan's enumeration of differences from Russian (cited
      from `topics/phonology/three_way_laryngeal_contrast.md` for
      the parent contrast); promoted here as a standalone topic
      because the no-palatalisation point is structurally distinct
      and is *the* sharpest Russian-L1 phonological gotcha.
gaps:
  - "Russian-L1 specific. Sakayan, ghamoyan, and tioyan don't make this point explicitly because their target audiences (English speakers, Armenian-internal, Russian speakers but in tioyan more concise) don't need it spelled out — only parnasyan's older Russian-pedagogy tradition does. So `attestation: single-source` is structural, not a gap; ghamoyan / tioyan would *not* address this if asked."
  - "Phonetic detail: Armenian consonants are described as 'hard' but are they truly *velarised* (like Russian's 'hard'), or just *unpalatalised* (default articulation)? Sakayan's transcription doesn't distinguish; parnasyan's claim is broad."
  - "Edge cases: are there any Armenian consonants that *do* soften in some environments (e.g., before front vowels, in loanwords)? Untreated."
  - "Loanword phonology: Russian loans into Armenian (`տրակտոր` 'tractor' from Russian *трактор*) — does the loan retain Russian-style palatalisation, or get re-articulated in Armenian style? Untreated."
---

# Absence of palatalisation contrast in Eastern Armenian

Eastern Armenian has **no hard/soft (palatalisation) contrast** in
its consonants. [#1] All consonants are articulated "hard" — without
the secondary palatalisation that distinguishes Russian's `мягкие`
(soft) from `твёрдые` (hard) consonants.

This is **the** classical Russian-L1 phonological gotcha — Russian's
hard/soft contrast is so pervasive (every consonant has both
versions, distinguished orthographically by following ь / vowel
choice) that Russian L1 speakers *automatically* palatalise before
front vowels (и, е) and need to *resist* this to sound natively
Armenian.

## Source

> **Parnasyan [#1]**: *"отсутствием противопоставления согласных по
> твердости—мягкости. Армянские согласные произносятся твердо и
> почти не смягчаются."*
>
> "[The Armenian consonant system is characterised by] the absence
> of a hard/soft contrast among consonants. Armenian consonants are
> pronounced hard and barely soften."

Single Russian-language source — the only one in our corpus that
makes this point explicitly. Sakayan (English-pedagogy) and ghamoyan
(Armenian-internal) don't address it because their target audiences
don't have the Russian palatalisation system as a baseline that
needs explicit unlearning.

## What it means in practice

In Russian:

- `н` /n/ is hard (твёрдый): `нос` /nos/ "nose"
- `нь` /nʲ/ is soft (мягкий): `день` /dʲenʲ/ "day"
- The hard/soft distinction is *phonemic*: changing it changes the
  word.

In Armenian:

- `ն` /n/ is just /n/. There's no `ն` vs `նյ` phonemic contrast.
- Before front vowels (`ի, ե`), `ն` does *not* palatalise:
  `նիստ` /nist/ "session" — not /nʲist/.
- Loanwords from Russian get *de-palatalised*: Russian `тётя` /tʲotʲa/
  "aunt" → Armenian `տյոտյա` (orthographically marked with `յ` to
  approximate the palatalisation, but typically articulated less
  palatalised than the Russian source).

## Pedagogical implication for Russian L1

When learning Armenian:

1. **Pronounce consonants flat / hard** before all vowels, including
   front vowels `ի, ե`. Resist the Russian instinct to soften.
2. **Don't insert `ь`-style softness** in word-final consonants —
   Armenian doesn't have it.
3. **Don't read written `յ` as Russian `ь`** — `յ` in Armenian is
   the consonant /j/, not a softening marker.

The mirror-image trap: when speaking Russian after speaking
Armenian, *miss* palatalisation cues and sound foreign.

## What this topic is *not*

- **Yerevan colloquial register** may have *some* palatalisation
  patterns under Russian contact influence — not addressed by
  parnasyan (1990); ghamoyan documents code-switching and
  Russian-loan integration but doesn't isolate palatalisation.
  See `topics/lexicon/code_switching_with_russian.md`.
- **Phonotactic constraints** (which consonant clusters are
  allowed) are a separate phenomenon.
- **The `յ` letter** appears in many Armenian words but represents
  /j/ (English "y") not Russian palatalisation softness.

## Contrastive notes

**For an English L1**: English doesn't have palatalisation as a
phonemic feature either, so this point isn't a "gotcha" — you'll
naturally produce hard Armenian consonants without effort. Skip
this topic; it's Russian-L1-specific.

**For a Russian L1**: this is **a daily-practice item**. Every time
you pronounce an Armenian word with a front vowel (`ի, ե`), check
whether you instinctively palatalised the preceding consonant.
Armenian `սիրել` /siɾɛl/ "to love" should be /si.ɾel/, not
/sʲi.ɾɛl/. The harder you concentrate on individual sounds, the
more naturally the de-palatalisation comes.

A useful diagnostic: have a native speaker say a word and listen for
the *absence* of the soft-consonant glide. If you can't hear it,
you'll struggle to produce it. Repeated exposure to Armenian audio
calibrates the ear faster than any rule explanation.

## Cross-references

- `topics/phonology/three_way_laryngeal_contrast.md` — the parent
  consonant-system topic, where this point appears as the fifth
  enumerated contrast with Russian.
- `topics/lexicon/code_switching_with_russian.md` — borrowed Russian
  items may retain or lose palatalisation depending on speaker;
  not yet investigated.
- `armenian-grammar.md` — original notes; doesn't currently mention
  palatalisation explicitly.
