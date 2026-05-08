# Take-verbs cluster: առնել / տանել / բերել / վերցնել

Status: **to explore further** — promising candidate for a
`topics/lexicon/take_verbs.md` topic file.

## Why this matters

English "take" and Russian *брать/взять* both collapse what Armenian
splits across multiple verbs. Russian L1 learners hit this constantly:
*взять детей на работу* (motion-along) and *взять новый телефон по
скидке* (acquisition) take one verb in Russian but require two
different verbs in Armenian.

| Russian | English | Armenian | sense |
|---------|---------|----------|-------|
| взять (с собой) куда-то | take (somewhere) | **տանել** | motion-with, motion-to-place |
| взять (приобрести) | take, buy | **առնել** | acquire, get; (colloq) buy |
| взять, поднять | pick up | **վերցնել** | pick up, take in hand |
| принести | bring (here) | **բերել** | motion-toward speaker |

So Russian *взять* and English *take* are lossy: both force a commit
to motion-vs-acquisition that Armenian makes you specify in the verb
choice itself.

## Diagnostic

When translating *to take* / *взять* into Armenian:

1. Is the action moving the object **to a place** or **with you**?
   → **տանել**.
2. Is the action **acquiring**, **buying**, **receiving**?
   → **առնել**.
3. Is the action **picking up** / **lifting** / **grasping**?
   → **վերցնել** (overlaps slightly with առնել but doesn't carry the
   "buy" reading).
4. Is the motion **toward the speaker**?
   → **բերել** (= "bring," not "take").

## Examples

- *Я взял детей на работу* "I took the kids to work" →
  **Երեխեքին գործ տարա** (տանել, aorist).
- *Я взял новый телефон по скидке* "I bought a new phone on discount" →
  **Նոր հեռախոս առա զեղչով** (առնել, aorist).
- *Возьми книгу со стола* "Pick up the book from the table" →
  **Վերցրու գիրքը սեղանից** (վերցնել, imperative).
- *Принеси воды* "Bring some water" →
  **Ջուր բեր** (բերել, imperative).

## What's open

- **Frequency split**. In modern Yerevan colloquial, is վերցնել
  encroaching on առնել's "pick up" sense (with առնել specialising
  more strongly toward "buy")? Anecdotally yes, but not citation-
  checked.
- **Aspectual / paradigm pairings**. Russian's *брать/взять* are
  aspectual partners (impf/pf). Armenian doesn't have grammatical
  aspect in this Russian sense, so the pairing doesn't survive
  translation. What replaces it? Probably the perfective vs
  imperfective distinction in Armenian falls on tense
  (aorist vs perfect/imperfect), not lexical pairs.
- **Idiomatic collocations**. e.g. `ձեռ առնել` (lit. "take a hand")
  = "to mock"; `ձև առնել` = "to put on airs". These are idioms that
  don't follow the "acquire" reading. Cross-reference with
  `topics/lexicon/idioms_phrasal.md`.
- **Russian-side citations**. Parnasyan p? and Tioyan p? likely
  contrast Russian *брать/взять* with Armenian verbs explicitly —
  worth grepping for in the next research turn.

## Source candidates for a future topic file

- `sakayan/cards/paradigms.tsv` — already has առնել / տանել /
  բերել / վերցնել glossed with "to buy / to take", "to take (away)
  / to lead", "to bring", "to pick up".
- `sakayan/dora_sahakyan.pdf` Unit 12 paradigms include all four
  verbs as complete tense paradigms.
- Parnasyan / Tioyan — TBD (need to grep).

## Spawned by

Conversation 2026-05-09 — user asked "տանել 'to take' but it's not
exactly to take... what's the difference with առնել" and observed
that Russian *взять* covers both motion-along and acquisition,
collapsing what Armenian splits.

## Cross-references

- `topics/lexicon/idioms_phrasal.md` — idiomatic V+N collocations
  using these verbs.
- `armenian-grammar.md` — verb-class system (1st vs 2nd
  conjugation; relevant here because the four verbs split across
  classes: առնել 1st, տանել 1st, բերել 1st, վերցնել 1st — uniform).
