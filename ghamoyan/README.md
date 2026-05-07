# ghamoyan — *Yerevan's Colloquial Language*

Source: **Լուսինե Ղամոյան, Մերի Սարգսյան, Անահիտ Քարտաշյան —
*Երևանի խոսակցական լեզուն*** (Yerevan: «Մունետիկ», 2014, 118 pp,
ISBN 978-9939-9010-8-4).

A linguistic study of the spoken/colloquial register of Yerevan
Armenian, contrasting it against the literary norm. Written for
linguists and language teachers; not a textbook.

## Status

- [x] PDF identified, fonts surveyed.
- [x] Encoding determined: standard ARMSCII-8 mapped onto WinAnsi
      codepoints, with two file-specific quirks (`U+03BC → բ`,
      `U+00A8 → և`).
- [x] `armscii.py` decoder + `extract.py` working end-to-end on all
      118 pages (~13 K spans, runs in <1s).
- [ ] Mining the book's content for cards / knowledge entries —
      deferred per user direction (we just want to make sure we can
      *read* it for now).

## How to run

```sh
.venv/bin/python extract.py                # → out/full.jsonl + full.md
.venv/bin/python extract.py --pages 35     # one page (Chapter 2 head)
.venv/bin/python extract.py --pages 35-40  # range
.venv/bin/python extract.py --show-unmapped
```

## What's in the book

Table of contents:

| Section | p. |
|---------|----|
| Ներածություն (Introduction) | 4 |
| Գլուխ 1: Երևանի արդի լեզվավիճակը և նրա վրա ազդող գործոնները | 10 |
| Գլուխ 2: Երևանի խոսակցական լեզվի հնչյունական հատկանիշները | 35 |
| Գլուխ 3: Բառային իրողությունները Երևանի խոսակցական լեզվում | 41 |
| Գլուխ 4: Քերականական իրողությունները Երևանի խոսակցական լեզվում | 70 |
| Գլուխ 5: Երևանի խոսակցական լեզվի ոճական առանձնահատկությունները | 92 |
| Որպես վերջաբան (Epilogue) | 97 |
| Եզրակացություններ (Conclusions) | 98 |
| Հավելված 1, 2, 3 (Appendices) | 100, 104, 114 |
| Օգտագործված գրականության ցանկ (References) | 116 |

## Topics of interest (in priority order)

### 0. Code-switching and informal romanization — major cross-cutting topic

Two phenomena that pervade real Armenian usage and break naive
tooling:

**Armenian–Russian code-switching.** Yerevan everyday speech mixes
Russian lexical items into Armenian sentence frames at a high rate.
The book documents examples on p48: *Արա՛, էդ տոչկեն ո՞վ ա,
խի՞ ա թթվել վրներս* — uses Russian *точка* "spot/dot" inside an
Armenian morphological frame (`տոչկեն` = `տոչկ` + `-ե` connecting +
`-ն` definite). Similarly *սվարկա* (Russian *сварка* "welding"),
*ռազբիրատ* (*разбирать* "to figure out"), *լիշնի* (*лишний* "extra"),
*լյուբոյ մամենտ ժիզնիդ* (*любой момент жизни* "any moment of [your]
life"). These are not translatable as Armenian or Russian — they're
discourse units that depend on understanding both substrates.

**Informal Latin transliteration of Armenian** (chat, SMS, social
media, sometimes "Armenglish"). No standard transliteration scheme —
common conventions are loose: `չ → ch`, `ղ → gh`, `շ → sh`,
`ց → ts`, `ք → k/q`, `թ → t`, `ա/ը → a` (often conflated). Common
problems:

- People often write *as they say it* (colloquial register, including
  the `ա/է` swap), which doesn't match the literary spelling.
- Vowel reductions get baked into the spelling (`ches asum` for
  `չեմ ասում`, with the literary `չեմ` written as `ches`/`chem` per
  whatever the speaker pronounced).
- Letters that look similar in some scripts get conflated.
- **Even careful transliteration can produce grammatically broken
  Armenian** — the writer may not be checking the back-transliteration.

Concrete trap (illustrated by a mistake I made earlier in this
project): I wrote `ches asem` as if it transliterated to
`չես ասի`. It doesn't:

- `ches` → `չես` (2sg neg copula, "you aren't") ✓
- `asem` → `ասեմ` (**1sg subjunctive**, "let-me-say"), not `ասի`
- `չես ասեմ` is grammatically broken — 2sg subject + 1sg verb.
- The actual transliteration of `չես ասի` ("you won't say") is
  `ches asi`.

Auto-translators (Google, DeepL, etc.) typically fail on:

1. Code-switched text — they pick one language and try to translate
   the foreign tokens phonetically or skip them.
2. Latin-transliterated Armenian — most don't recognize it as
   Armenian and treat it as gibberish or random Latin.
3. Colloquial-register Armenian (with `ա` for `է`, dropped letters,
   etc.) — they handle the literary form well but miss the spoken.

**Detection ideas (no implementation yet):**

- Cyrillic characters in an Armenian-script text — trivial to flag
  via Unicode block check (script transition mid-token).
- Russian-origin lexical roots adapted to Armenian morphology
  (`տոչկեն`, `ռազբիրատ`) — would need a Russian root lexicon and a
  fuzzy matcher.
- Latin-transliterated Armenian — could attempt back-transliteration
  via the common conventions and check if the result is real Armenian.

These are bigger projects than current scope. Mention here so we
remember the topic exists and matters.

### 1. Filler words and discourse markers — *first card slice done*

Phrases like `ըստ էության` (essentially), `ի դեպ` (by the way),
`համենայն դեպս` (in any case), and the colloquial register's
`եսիմ`, `տենց`, `բա`, `դե` are extremely high-frequency in real
Armenian conversation but often skipped in textbook learning. They
unlock the ability to *follow* spoken Armenian — without them you
spend bandwidth wondering whether a discourse marker carries content.

First slice extracted from Ch 4 §1 ("parasitic words") into
`out/fillers.tsv` — 32 entries, three registers (standard / casual /
slang). See `ch4-pleonasms.md` for the source mapping with
verification status (Wiktionary cross-check via `../sakayan/glosser.py`
on every word that has a Wiktionary entry).

### 2. Colloquialisms broadly — fillers + slang + idioms

Goal: mine **all** colloquialisms from the book, not just fillers.
Filler-words slice is done (`out/fillers.tsv`). Remaining categories,
in rough order of card-utility:

- **Yerevan youth slang** (book Ch 3, p48). Jargon entries: `լոքշ`
  (idleness/lame), `թույն` (cool, lit. "poison"), `բոց` (cool/wild,
  lit. "flame"), `քյառթու` (vulgar/loutish), `փոստ ա` (entertaining),
  `ֆազոտ` (unstable person), `ֆռցնել` (to deceive), `դուխով`
  (brave / with spirit), `բքել` (to chain-smoke), and ~20 more.
- **Russian-Armenian code-switched phrases** from p48 (see topic 0
  above): *տոչկա, սվարկա, ռազբիրատ, լիշնի, լյուբոյ մամենտ ժիզնիդ*…
  These should probably get a `codeswitch` tag rather than a slang
  tag — they're a different category.
- **Phrasal/idiomatic verbs** from p49+ (`կուտ տալ` "to deceive",
  `յուղ վառել` "to talk nonsense", `ձև բռնել` "to put on airs",
  `արյուն վերցնել` "to annoy", `գծերից ընկնել` "to lose face",
  `կոշկվել` "to get into a bad situation"). High idiomatic density.
- **Proverbial / fixed expressions** from various sections.

This is a *high-density* register slice — should produce a
`slang_yerevan` tag for jargon, plus separate tags for code-switched
items and idioms. **Don't forget to dive into this.** A single
afternoon's mining for Ch 3, plus another for the appendices
(Hավելված 1-3 on pp 100-115) which are likely conversation
transcripts.

### 2.5 Future tools / corpus sources to consider

When/if we want real-usage examples for cards (e.g. seeing `լոքշ ա`
in actual sentences from native speakers), the most realistic sources
to scrape — not built yet:

- **EANC (Eastern Armenian National Corpus)** at `eanc.net` — academic
  corpus, ~110M tokens, includes a colloquial sub-corpus with TV/radio
  transcripts and online forum posts. Web interface only (no API), so
  scraping required. Highest quality if we commit to maintenance.
- **YouTube subtitles** via `yt-dlp`. Free. Channels in colloquial
  Armenian (street interviews, podcasts, vlogs) yield spoken-register
  text with timestamps. Auto-generated Armenian subs are imperfect
  but searchable.
- **OpenSubtitles** (`opensubtitles.org`). Armenian subtitles for
  Armenian and dubbed films. Dialogue-heavy by definition. Free API
  with daily quota.
- **Reddit `r/armenia`** via free API. Mixed quality — many threads
  in English/Russian, but Armenian threads exist. Lower signal density.

**Twitter/X is no longer viable** — paid API since 2023, and
Armenian Twitter has high code-switching rate that makes filtering
expensive.

Defer until needed. For the current ~32-entry filler deck, manual
glosses are sufficient. The need becomes real when we mine the
slang tier — `լոքշ ա` doesn't carry meaning without a real-usage
context.

### 3. Phonology of colloquial speech

See INDEX-level `armenian-grammar.md` voiced-aspirated section. Ch 2
of this book extends with vowel reductions (ցտեսություն → ցտեսցյուն)
and other patterns. Lower priority because phonology is best
absorbed through audio, not flashcards.

### 4. Grammar / morphology divergences

See `ch4-verbs.md` for the verb-section findings. The colloquial
copula `ա` (replacing literary `է`) is the biggest single divergence
and the most card-worthy.

## Why this book is potentially useful for the deck

Likely productive lifts from the book if/when we choose to mine it:

- **Phonology (Ch 2)** — vowel reductions, ի→ը shifts, syncope and
  consonant drops in colloquial speech. Concrete examples like
  `ցտեսություն → ցտեսցյուն`, `ուսուցիչ → ուսցիչ`, `բարի լույս → բար
  լուս`. Would expand `armenian-grammar.md`'s phonology section
  substantially.
- **Vocabulary (Ch 3)** — colloquial register: slang, foreign
  borrowings, register-marked words. Useful as a sociolinguistic
  reference.
- **Stylistic (Ch 5)** — *intimate/affectionate* register with the
  high-frequency endearments (`կյանք`, `ջան`, `ազիզ`, `մռութ`,
  `արև`) and their use with the `-ս` possessive suffix
  (`կյանքս`, `ջանս`). Productive diminutive suffixes (`-իկ`, `-ուկ`,
  `-ակ`, `-չիկ`, `-չո`) — these are essential for natural-sounding
  conversational Armenian.
- **Morphology (Ch 4)** — colloquial-only grammatical forms,
  contrasted against the literary paradigms we already have from
  Sakayan. Would *not* go into paradigm cards directly (they're
  non-standard) but valuable as a "what real speakers do" companion
  layer.
- **Appendices 1-3** — likely real-conversation transcripts; could
  feed chunk cards.

Decision deferred: per the user's direction we have the tools to read
the book, but aren't yet committing to a study workflow on it.
