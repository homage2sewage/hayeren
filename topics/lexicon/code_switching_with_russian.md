---
topic: code-switching with Russian in Yerevan colloquial speech
domain: lexicon
units: [ghamoyan:3]
related: [yerevan-slang, latin-transliteration]
status: draft
attestation: single-source
sources:
  - id: 1
    book: ghamoyan
    page: 48
    y_range: [340, 400]
    verbatim_quote:
      - "Երևանյան պատանիների խոսքից են սղագրված"
      - "տոչկեն"
      - "սվարկա"
      - "Լյուբոյ մամենտ ժիզնիդ"
      - "Ռազբիրատ"
      - "լիշնի"
    supports: supported
    note: |
      ghamoyan documents teen-Yerevan speech with Russian lexical
      items embedded in Armenian morphological frames. Examples
      transcribed from real recordings: the Russian noun *точка*
      "spot/dot" appears as `տոչկեն` (root + Armenian definite
      `-ե/-ն`), *сварка* "welding" as `սվարկա` (undeclined),
      *разбирать* "to figure out" as `Ռազբիրատ` (verbal noun?),
      *лишний* "extra" as `լիշնի`, and the full phrase *любой
      момент жизни* "any moment of life" with Russian-genitive
      `жизни` followed by the Armenian 2sg possessive `-իդ`.
  - id: 2
    book: ghamoyan
    page: 48
    y_range: [480, 525]
    verbatim_quote:
      - "օտար բառեր գործածելը"
      - "կառոչի"
      - "չերեզ"
      - "վաժնի"
      - "վռոձի"
      - "ուժե"
      - "տուտժե"
      - "դավայ"
      - "կանկռետնի"
      - "ժալետչիկ"
    supports: supported
    note: |
      ghamoyan's catalogue of Russian lexical insertions
      ("foreign-word usage" — *օտար բառեր գործածելը*): adverbials
      and discourse particles directly transliterated from Russian
      — *короче* "shortly/in short" → կառոչի, *через* "through" →
      չերեզ, *важно* "important" → վաժնի, *вроде* "like, sort of"
      → վռոձի, *уже* "already" → ուժե, *тоже* "also" → տուտժե,
      *давай* "come on" → դավայ, *конкретно* "specifically" →
      կանկռետնի, *жалейчик* "complainer" → ժալետչիկ. These usually
      stay undeclined in Armenian text.
  - id: 3
    book: ghamoyan
    page: 105
    y_range: [45, 175]
    verbatim_quote:
      - "պադվալ"
      - "նկուղ"
      - "սամավառ"
      - "ինքնաեռ"
      - "տաբուրետկա"
      - "աթոռակ"
      - "ֆոլգա"
      - "փայլաթիթեղ"
    supports: supported
    note: |
      ghamoyan's Appendix 2 — a dictionary-style word-list of
      common Russian-loan colloquialisms with their Armenian-native
      equivalents. Each line: loan on the left, native on the right.
      Sample: պադվալ (RU *подвал*) → նկուղ "basement"; սամավառ (RU
      *самовар*) → ինքնաեռ; տաբուրետկա (RU *табуретка*) → աթոռակ
      "stool"; ֆոլգա (RU *фольга*) → փայլաթիթեղ "foil"; etc. The
      appendix lists ~100+ such pairs across multiple semantic
      categories (household items, plants, body, etc.). High-utility
      reference for register-aware translation: when reading
      colloquial text with `պադվալ`, the literary equivalent is
      `նկուղ`; in formal writing, swap.
gaps:
  - "Sociolinguistic conditions: ghamoyan flags this as 'youth speech' but doesn't quantify across age/social class. The real distribution (Yerevan-only? all of Armenia? diaspora?) is open."
  - "Code-switching grammar: when the Russian item gets Armenian morphology (տոչկեն takes the definite article) vs when it stays bare (սվարկա). What governs this? Untreated."
  - "Direction of borrowing for adverbials/discourse particles — ghamoyan documents Russian → Armenian; reverse cases (Armenian items in Russian Yerevan speech) untreated."
  - "Auto-translators (Google, DeepL, etc.) typically fail on code-switched text: they pick one language and silently drop or mistranslate the other. Documented in `ghamoyan/README.md` Topic 0."
  - "Detection: programmatically distinguishing 'Russian root with Armenian inflection' (`տոչկեն`) from native Armenian morphology requires a Russian root lexicon + a fuzzy matcher. Out of current scope."
---

# Code-switching with Russian in Yerevan colloquial speech

Yerevan colloquial speech embeds Russian lexical items into Armenian
sentence frames at high frequency, especially among younger speakers.
[#1] [#2] The result is **neither pure Armenian nor pure Russian** —
discourse units that depend on understanding both substrates. Many
of the embedded items have Armenian-native equivalents that exist in
the literary norm but are absent from casual speech; ghamoyan's
Appendix 2 [#3] lists ~100+ such pairs across household, plant,
mechanical, and abstract semantic fields.

## What it looks like

Two patterns:

**1. Russian roots adapted to Armenian morphology**: the borrowed
word gets Armenian definite, possessive, or case marking. [#1]

| input (in Yerevan speech) | breakdown | meaning |
|---------------------------|-----------|---------|
| **տոչկեն** | RU *точка* "dot" + AM def. `-ե/-ն` | "the spot" |
| **լյուբոյ մամենտ ժիզնիդ** | RU *любой момент жизни* + AM 2sg poss. `-իդ` | "any moment of your life" |

**2. Russian items inserted bare** (no Armenian inflection,
sometimes with Armenian phonology). [#1] [#2]

| input | RU origin | meaning |
|-------|-----------|---------|
| սվարկա | *сварка* | "welding" |
| ռազբիրատ | *разбирать* (inf.) | "to figure out" |
| լիշնի | *лишний* | "extra" |
| կառոչի | *короче* | "in short" |
| չերեզ | *через* | "through" |
| վաժնի | *важно* | "important(ly)" |
| վռոձի | *вроде* | "like, sort of" |
| ուժե | *уже* | "already" |
| տուտժե | *тоже* | "also" |
| դավայ | *давай* | "come on" |
| կանկռետնի | *конкретно* | "specifically" |

The bare-insertion pattern is especially common for **adverbials and
discourse particles** (`կառոչի, ուժե, դավայ, կանկռետնի`) — short
high-frequency items that don't need to inflect.

## Project-attested examples beyond the ghamoyan corpus

Real-world Yerevan internet usage (Twitter / social media reply,
2026-05; reproduced in `research/2026-05-09-tweet-llm-
comparison.md`):

> *հա լավ էսքան խոտ մարդ ըլնի մի հատ էլ պալիտիկ 🤭😅*

`պալիտիկ` here is a Russian-loan colloquial spelling of
*политика* "politics," used as a register-marker (a
mockingly-casual stand-in for the literary
**քաղաքականություն**). Pattern-conformant with the lexemes
documented from ghamoyan p48 below — bare-insertion, no Armenian
inflection. Not book-attested as a specific lexeme; included
here as the canonical real-world test case the topic should be
able to gloss.

## Documented examples (ghamoyan p48)

Real teen-speech transcriptions: [#1]

> *Արա, էդ տոչկեն ով ա, խի ա թթվել վրներս?*
> "Hey, who's that spot/guy, why is he glaring at us?"
>
> *Չափալախեմ, պատին սվարկա կըլնես.*
> "I'll smack you, you'll be welded to the wall."
>
> *Լյուբոյ մամենտ ժիզնիդ տռոսը կկտրեմ.*
> "Any moment of your life I'll cut your rope."
>
> *Ռազբիրատ կանենք, լիշնի կհանենք.*
> "We'll figure it out, take out the extras."

## Detection ideas

Programmatic detection of Armenian-Russian code-switching is
non-trivial. Notes from `ghamoyan/README.md` Topic 0:

- **Cyrillic in Armenian-script text**: trivial via Unicode
  block-check (script transition mid-token).
- **Russian roots with Armenian inflection**: would need a Russian
  root lexicon plus a fuzzy matcher to recognise stems like *точк-*
  inside `տոչկեն`. Out of current scope.
- **Latin-transliterated Armenian** mixed with Latin-transliterated
  Russian: most painful case. See `transliteration-notes.md`.

## What this topic is *not*

- **Russian-language pedagogical examples in textbooks** (parnasyan,
  tioyan): those use Russian to *explain* Armenian, not as
  embedded lexical items. Different phenomenon.
- **Loanword integration over time**: words like `սաբունը` (soap, ←
  Arabic via Turkish, naturalised centuries ago) aren't
  code-switching — they're integrated loans. Code-switching here
  means *currently-foreign* items recognised as such by speakers.
- **Pure Russian speech** with Armenian items embedded — the
  reverse direction. Untreated.

## Contrastive notes

**For an English L1**: the closest English analogue is bilingual
Spanish-English speakers' "I'm gonna *agarrar* the keys" pattern —
Spanglish. The grammatical-frame question (which language provides
the morphology) is the same. Yerevan code-switching, like Spanglish,
has Armenian as the matrix language and Russian as the embedded
language; the Armenian inflectional system handles items from both
substrates.

**For a Russian L1**: this is the easiest pattern to recognise —
you can see the Russian roots immediately. The harder direction
(reading the Armenian frame around the Russian item) is the
learnable skill. A Russian L1 looking at `էդ տոչկեն ով ա` should
read "this *точка* who is" → "who's that guy/spot." The frame is
3 Armenian function words; the lexical content is Russian.

## Cross-references

- `topics/lexicon/yerevan_slang.md` — code-switching overlaps with
  jargon; some of the "slang" items are technically Russian
  borrowings.
- `transliteration-notes.md` — when Yerevan code-switched text gets
  romanised, both languages' tokens enter the Latin form.
- `ghamoyan/README.md` Topic 0 — original seed notes with
  detection-idea sketches.
