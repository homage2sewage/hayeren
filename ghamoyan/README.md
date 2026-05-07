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

### 2. Youth slang — TODO, future dive

Ch 3 (p48) lists Yerevan-youth jargon: `լոքշ` (idleness/lame),
`թույն` (cool, lit. "poison"), `բոց` (cool/wild, lit. "flame"),
`քյառթու` (vulgar/loutish), `փոստ ա` (entertaining), `ֆազոտ`
(unstable person), `ֆռցնել` (to deceive), `դուխով` (brave / with
spirit), `բքել` (to chain-smoke), and many more. Plus the
Russian-Armenian code-switching examples on p48 lines 2344-2348:
*Արա՛, էդ տոչկեն ո՞վ ա, խի՞ ա թթվել վրներս,* etc.

This is a *high-density* register slice — would make a `slang_yerevan`
deck tag distinct from the standard fillers. **Don't forget to dive
into this.** The book material on p48 plus its surrounding pages is
likely a single afternoon's mining work.

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
