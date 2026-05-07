# Anki deck design — decisions and the reasoning behind them

A running log of why our cards look the way they do. Pairs with
`armenian-vocab-research.md` (the research base) and
`armenian-grammar.md` (the linguistic facts).

## Card structure

### Drop the transliteration column from displayed cards

**Why:** Sakayan's transliteration uses scholarly diacritics (`Œ`, `§`,
`¿`, `¤`) that are hard to read on a phone and don't help speaking — they
encode IPA-style detail beyond what learners need at vocab-card stage.
Forvo or deck-included audio is a better source for pronunciation
guidance.
**How applied:** transliteration is extracted as a *signal* — used by
`phonetics.py` to find pronunciation deviations and emit hints — but
never written to the TSV that goes to Anki.
**When this would change:** if/when we want to include audio cards or
support a learner who specifically wants romanized cues.

### Phonetic notes only on voiced↔voiceless/aspirated consonant pairs

**Why:** these are the unpredictable cases. English speakers can derive
voicing rules with practice, but lexical exceptions like
`ընդունել → ընթունել` (դ pronounced as թ in this specific word) have to
be memorized per-word. Vowel glides, epenthetic schwa, and ye/vo word-
initial allophony are *predictable* and don't need flagging.
**How applied:** `sakayan/phonetics.py` only substitutes from the set
`{(դ,թ), (դ,տ), (բ,փ), (բ,պ), (գ,ք), (գ,կ), (ձ,ց), (ձ,ծ), (ջ,չ), (ջ,ճ)}`.
Any other mismatch between spelling and Sakayan's transliteration is
silently ignored to keep cards clean.
**Format:** `բարդ [բարթ]` — phonetic spelling in lowercase brackets
after the original word, only when it differs.

### English number words → numerals

**Why:** scanning a card on a phone, `20 years old` is read instantly;
`Twenty years old` requires parsing. The user explicitly asked for this.
**How applied:** `sakayan/english_numbers.py` runs over the English
column. Handles single cardinals (one–nineteen, twenty–ninety),
hyphenated compounds (`twenty-one → 21`, `four-zero-zero → 4-0-0`), and
ordinals (`third → 3rd`, `twenty-first → 21st`). Quantity words
(`hundred`, `thousand`, `million`) deliberately stay as words because
they're often used non-numerically.

### Split equal-count comma pairs into separate cards

**Why:** Sakayan sometimes packs an infinitive plus its irregular
conjugated form on one row, e.g. `ունենալ, ունի ↔ to have, has`. For SRS
this is two concepts on one card — review intervals end up averaged
across them, and you can't tell if your "fail" was on the infinitive or
the conjugated form. Splitting gives each form its own SRS schedule.
**How applied:** in `sakayan/vocab.py`, when both Armenian and English
columns split into the same number of comma-separated parts, emit one
card per pair. Single-form rows pass through unchanged.
**Note:** sometimes the two halves are *synonyms* rather than verb
forms (e.g. `small, little`); splitting still works in that case — you
just learn both Armenian words for "small". The textbook doesn't have
many of those.

### One paradigm card per cell

**Why:** each conjugated form is a separately-retrievable unit. Putting
all six forms on one "table card" tests recognition (you see the table)
not recall. The research file's emphasis on *retrieval practice* and
*frequency-ordered learning* both argue for individual cards: high-
frequency forms (1sg, 3sg, 1pl) get reinforced naturally; rare forms
(2pl-formal) end up in the hard pile and reviewed more.
**How applied:** `sakayan/paradigms_data.py` stores hand-curated
paradigm tables (because PDF auto-extraction of the paradigm columns is
fragile — they're space-less concatenations in the source). Each table
is 6 cells (3 persons × 2 numbers); `paradigms.py` emits one card per
cell, tagged with verb and tense.
**Pro-drop note:** Armenian's pro-drop nature means each form on its
own (`ունեմ`) is a complete utterance, not a fragment. So the card
makes pedagogic sense without requiring a sentence wrapper.
**Open question:** should we also build *chunked* paradigm cards
(`ժամանակ ունեմ → I have time`) per the research file's "lexical chunks
transfer to speech better" recommendation? Probably yes, but only after
collecting good chunk candidates from the dialogues. Deferred.

## Workflow

1. `extract.py` parses the whole PDF into JSONL + Markdown (~6s for all
   558 pages).
2. `build_units.py` scans the JSONL for left-margin Times-Bold section
   headers and emits `units.json` — the manifest of every unit's vocab
   pages and dialogue (page, y) bookmarks.
3. `make_anki.py` reads `units.json` and produces:
   - `out/by-unit/unit{NN}_vocab.tsv` (one per unit)
   - `out/by-unit/unit{NN}_dialogue{i}.tsv` (one per dialogue)
   - `out/by-unit/paradigms.tsv` (curated from `paradigms_data.py`)
   - `out/by-unit/all.tsv` (concatenated; speaker prefixed onto the
     Armenian field for dialogues so all rows have the same shape)
4. `phonetics.annotate` and `english_numbers.normalize` post-process the
   Armenian and English fields respectively, transparently.
5. TSVs go to AnkiDroid via File → Import. No header row.

End-to-end coverage on Sakayan (11 units, 558 pages):

- 606 vocab cards
- 290 dialogue cards
- 18 paradigm cards (Unit 1 only — extend `paradigms_data.py` as you go)

## Layout quirks discovered during extraction

Sakayan's typesetting is not uniform across the book; the extractor has
to handle several variants:

### Vocab table layouts

- **Single-column** (units 1, 2, 4, 7, 8, 10, 11) — one Armenian / one
  translit / one English column. Anchor x sometimes 43, sometimes 71,
  always within (40, 95).
- **Two-column** (units 3, 5, 6, 9) — two side-by-side `Arm | Tr | Eng`
  triples on each visual row. `vocab.py` detects this by looking for a
  cluster of Barz-Italic anchors at x≈246; if found it extracts both
  halves with separate column ranges.

### English position

- **Layout A** (most pages) — English sits to the right of Armenian, on
  the same y-row, offset +2 to +5 px.
- **Layout B** (page 52 and similar) — English is on the line *above*
  its Armenian by ≈10 px. Detected by comparing the y of the first
  Armenian and the first English on the page.

### Dialogue speaker/translation position

- Same A/B split applies to dialogue pages. The Armenian utterance can
  have its speaker label and English translation either +5 below it
  (Unit 1) or -11 above it (Unit 2). `dialogues.py` uses a wide
  `dy_lo=-15, dy_hi=10` window for both speaker and English; consecutive
  exchanges are ≥30 px apart so this doesn't cause double-matching.

### Sub-section detection in `build_units.py`

The book has 11 numbered units. After each unit's `XI EXERCISES`,
appendix material follows (verb tables, alphabetical glossary). Lone
Roman-numeral letters (`I`, `V`) appear in the glossary and would
mis-classify as new section markers. `build_units.classify` requires a
descriptive word after the Roman ("DIALOGUE", "TEXT", …, "EXERCISES")
to count as a unit section.

### Single un-numbered dialogues

Some units have only one dialogue and skip the `1.` marker. When no
numbered dialogue starts are found between `I DIALOGUES` and `II TEXT`,
`build_units.py` treats the whole region as a single un-numbered
dialogue (this is the case for Unit 2).

## Coverage gaps and follow-ups

- **Paradigms beyond Unit 1.** `paradigms_data.py` is a manual ledger;
  new units' paradigms (other irregular verbs in Unit 5+, the negative
  paradigm in Unit 2, etc.) need to be added by hand as the user
  progresses.
- **Two-column dialogue rows** — only single-column dialogues are
  observed so far. If later units use two-column dialogues, the
  detection logic from vocab.py would need to be ported.
- **Lexical chunks from dialogues.** The research file argues for
  multi-word chunk cards (`Ժամանակ ունեմ → I have time`). Now that we
  have 290 dialogue exchanges, harvesting reusable chunks is feasible
  but not yet implemented.

## Request log

Notable design decisions made interactively. Helps future sessions
understand why specific behaviors are in place.

### 2026-05-06 — "indicate when դ is pronounced as թ"

User asked for spelling-vs-pronunciation hints inline with the Armenian
word, format `բարդ [բարթ]`. Implementation in `sakayan/phonetics.py`,
restricted to the voiced↔voiceless/aspirated consonant pairs (see
above). Vowel glides, epenthetic ə, and ye/vo allophony are silently
ignored. Brackets always lowercase, even if the original word starts
with a capital.

### 2026-05-06 — drop transliteration column entirely

User: "we don't need transliteration at all". Confirmed by the previous
request — once we have phonetic deviation hints, the bulky scholarly
transliteration adds noise without value. The transliteration is still
extracted (we need it for the deviation detector) but isn't written to
the Anki TSV.

### 2026-05-06 — number words → numerals

User: "we don't want to type numbers in english i guess, better put em
numerically with -th/-rd if required". Implemented in
`sakayan/english_numbers.py`. Phone-number-style digit-spelling
(`Four-zero-zero`) preserves the hyphen structure (`4-0-0`) since the
textbook deliberately uses digit-by-digit reading there.

### 2026-05-06 — paradigm cards for conjugation

User: "ունեմ is different from ունենք" — concerned that bundling
`ունենալ, ունի` in a single vocab card doesn't actually teach the full
paradigm. Implemented `paradigms_data.py` + `paradigms.py` with one
card per cell, plus retroactive comma-split on the vocab side so
`ունենալ, ունի` becomes two separate cards naturally.

### 2026-05-06 — extract the whole book

User: "let's extract the whole book, expand knowledge along the way".
Implemented `build_units.py` + `make_anki.py` for one-step bulk
extraction of all 11 units. Output is 914 cards in
`out/by-unit/all.tsv`. Layout quirks discovered along the way (two-
column tables, Layout A/B for English position, single un-numbered
dialogues, lone-Roman-letter false positives in the glossary) are
documented above. Knowledge files updated with all newly-found
voiced↔aspirated examples (now ≈12 documented words).

### 2026-05-06 — paradigm coverage extended to units 2-6

`paradigms_data.PARADIGMS` now includes:

- **Unit 2** — present negative for `լինել` / `ունենալ` / `գիտենալ`
  (the auxiliary `չեմ`, plus the irregular `չունեմ` and `չգիտեմ`).
- **Unit 3** — imperfect for `լինել` / `ունենալ` / `գիտենալ`, plus
  the possessive-adjective table (`իմ / քո / իր / նրա / մեր / ձեր
  / իրենց / նրանց`).
- **Unit 4** — aorist for the prototypical regular verbs `գրել`
  (-ել class) and `կարդալ` (-ալ class).
- **Unit 6** — future indicative for the same two prototypes.

Total: 14 paradigms × 6 cells (+8 possessive forms) = 86 cards. Units
5, 7, 8, 9, 10 (perfect, subjunctive, mandative, resultative,
hypothetical) are still TODO — they're more complex compound forms
and the user can read them and extend `paradigms_data.py` as needed.

### 2026-05-06 — chunk cards from dialogues

User: "yes, do it" (build lexical-chunk cards). Implemented `chunks.py`
which walks every dialogue TSV, filters for short (≤7 words, single-
sentence) Armenian utterances, dedupes by Armenian text, and emits
`out/by-unit/chunks.tsv` (202 cards). Wired into `make_anki.py` so
the chunks regenerate alongside vocab/dialogue/paradigm output.

Format: dialogue exchange minus the speaker label. So
`Բարև ձեզ։ → Hello!` becomes a chunk card without the `A:` prefix —
turning each useful phrase into a standalone vocab-style item.

### 2026-05-06 — DallakTimes / Pedour fonts

User: "show examples". Inspected the four un-mapped Armenian fonts;
verified empirically (`fonts.remap("Barz-Italic", text)` produces
correct Armenian for sample strings from each) that all four use the
*same encoding scheme* as Barz-Italic. Added them to `FONT_MAPS` as
aliases. Now decorative chapter headings, the alphabet table on p20,
and the UN-Declaration excerpt on p18 also extract cleanly. No quality
impact on previous vocab/dialogue output (those fonts don't appear in
vocab table cells), but the full-book MD is now Unicode-clean
throughout.

### 2026-05-07 — Pass 1: finite tenses for units 5, 7, 8, 9, 10

Read each unit's grammar pages (p121-123, p174-175, p201-203, p228,
p247-249) and added paradigms for:

- **Unit 5** (perfect / pluperfect): `գրել եմ`, `կարդացել եմ`,
  `գրել էի`, `կարդացել էի` for both verbs.
- **Unit 7** (subjunctive): future and past for `գրել` / `կարդալ`.
- **Unit 8** (mandative): future I and past I with `պիտի` for
  `գրել` / `կարդալ`. Mandative II skipped — it's a compound (past
  participle + `պիտի լինել`) that's better assembled from primitives
  than memorized as 6-cell cards.
- **Unit 9** (resultative): present and past for `նստել` "to sit down"
  and present for `հոգնել` "to get tired" — the prototype stative verbs.
- **Unit 10** (hypothetical): future I and past I with `կ-` for
  `գրել` / `կարդալ`.

Total Pass 1 addition: 14 paradigms × 6 cells = 84 cards.

### 2026-05-07 — Pass 2: participle (դերբայ) tables

Source: Sakayan's grammar appendix, p359 ("THE INFINITIVE AND THE
PARTICIPLES") for regular verbs, p354-355 ("TABLE OF IRREGULAR VERBS")
for the 19 high-frequency irregulars.

Encoded 8 verbs' full participle tables in `paradigms_data.PARTICIPLES`:

- regular -ել: `գրել`
- regular -ալ with -աց- insertion: `կարդալ`
- common irregulars: `ունենալ`, `լինել`, `գալ`, `տեսնել`, `ուտել`, `տալ`

Each verb gets 7 participle cards: infinitive, active (-ող), past
(-ած), synchronic (-ելիս), future (-ելու), negative (-ի/-ա),
instrumental (-ելով). Total: 56 cards.

**What's emitted vs skipped:**

- **Free** participles (independent use as nouns/adjectives/adverbs)
  → emitted: active, past, synchronic, future, instrumental.
- **Bound** participles (only used inside finite tenses) → mostly
  skipped because they don't have standalone meaning. Exception:
  the `negative` participle (`գրի`, `կարդա`) is included because it's
  needed to produce hypothetical negatives (`չեմ գրի`).
- The `-ելով` instrumental converb isn't in Sakayan's appendix table
  but is widely productive — added as the 7th card per verb.

For irregular verbs, the participles are built off the aorist stem
(`գալ → եկած`, `ուտել → կերած`), not the infinitive stem. The
appendix table lists these explicitly. Encoded verbatim from there.

Final tally after both passes: **256 paradigm cards** (33 finite-tense
paradigms + 8 participle tables + the possessive-adjective table) and
1354 cards total in `out/by-unit/all.tsv`.

**Still TODO (deferred — diminishing returns):**

- Mandative II / Hypothetical II compound paradigms — formed by
  combining a past participle with `պիտի լինել` / `կ-լինել`. Once you
  know the primitives (past participle + `լինել`'s tense paradigms),
  the compound is mechanical. Could be auto-generated from existing
  data instead of hand-curated.
- Imperative paradigms — singular/plural pairs per verb. Not yet
  encoded as cards; the irregular forms are documented in
  `armenian-grammar.md` and visible in the Wiktionary `--table` output.

### 2026-05-07 — extend irregular participles to all 22 verbs

User asked to extend with the remaining irregulars. Added the 14
remaining verbs from Sakayan's appendix-p354/355 table:

`անել, առնել, ասել, բանալ, բերել, դառնալ, դնել, ելնել, զարկել,
ընկնել, թողնել, լալ, լվանալ, տանել`

Each entry inherits the standard 7-form schema (infinitive, active,
past, synchronic, future, negative, instrumental). Where the
participle's stem differs from the infinitive's stem (most cases —
e.g. `անել → արած`, `ուտել → կերած`), the gloss notes the aorist
stem so the user can derive other forms.

`paradigms_data.PARTICIPLES` is now 22 verbs × 7 forms = 154 cards.
Combined with the finite-tense paradigms and possessive-adjective
table, paradigm cards total **354** — the deck-wide all.tsv now
contains 1452 cards.

### 2026-05-07 — Filler-word deck slice from Ghamoyan Ch 4

Added a new card category — colloquial filler words and discourse
markers — at user request. These are high-frequency in real Armenian
conversation but absent from textbook learning, so they fill a real
gap.

Source: Ghamoyan Ch 4 §1 (*մակաբույծ բառեր* "parasitic words", p87-88)
plus a few discourse markers grepped from elsewhere in the book
(notably `ըստ էության` from the appendix of common errors).

Output: `ghamoyan/out/fillers.tsv` — 32 cards in three sub-tags:

- `ghamoyan colloquial filler standard` (21) — discourse markers
  used in any register: ուրեմն, ի դեպ, ի միջի այլոց, համենայն դեպս,
  ըստ էության, իհարկե, ուղղակի, պարզապես, իսկապես, կարծես թե, մի
  խոսքով, կարճ ասած, այսպես ասած, կարծում եմ, իմ կարծիքով, ասենք,
  ենթադրենք, մի տեսակ, ի վերջո, այսպիսով, իրականում.
- `ghamoyan colloquial filler casual` (8) — hesitation/intensifier
  fillers: եսիմ, օֆ եսիմ, տենց, տենց բաներ, բա, դե, բանը, պարզ ա.
- `ghamoyan colloquial filler slang` (3) — Yerevan-youth jargon
  attention markers: լսի, խոսքի, քցենք.

**Card schema: 3 columns** — `Armenian \t English / Russian \t Tags`.
The two languages are joined into a single back-of-card field with
` / ` as separator. Each side holds 2-3 quick equivalents (no
etymology, no Wiktionary annotations).

**Why combined-language back, not separate fields:** the user's
intuition (which lines up with how cross-language semantic
triangulation is supposed to work) — for fillers/discourse markers
the English and Russian equivalents often *disambiguate each other*
faster than either alone. English "well" is overloaded (greeting,
hesitation, OK-then…); seeing it next to Russian "ну, давай" tells
you which sense the Armenian particle is doing. Holding one
translation and mentally fetching the other is slower than seeing
both at once.

Anki import: AnkiDroid → File → Import → tab delimiter → Field 1
= Armenian, Field 2 = Translations (en/ru combined), Field 3 = Tags.
Note type needs two text fields.

Verification: every Armenian token passed through
`sakayan/glosser.py` (Wiktionary cross-check). ~22 of 32 entries got
strong two-source agreement (Wiktionary + book context); the other
~10 are colloquial reductions or multi-word idioms whose composing
words are findable on Wiktionary but whose idiomatic meaning isn't —
the verification record is in `ghamoyan/ch4-pleonasms.md`, not in
the TSV cells (kept terse for card-display purposes). Russian
translations are author-supplied; not independently verified.

### 2026-05-07 — Wiktionary lookup tool

User: "having a tool to lookup wiktionary + probably browse related
terms + definitely check conjugation tables would be quite useful, is
there a good way to do this through api or something". Built
`sakayan/lookup.py`:

- Uses the MediaWiki action API (`/w/api.php?action=parse`) with no
  auth or key. The `prop=wikitext` request returns parseable wiki
  source for the Armenian section; `prop=text` returns rendered HTML
  (where the conjugation table lives).
- Caches every response under `.cache/lookup/` so repeated calls are
  instant.
- Output modes: default summary (definitions + pronunciation +
  derived terms), `--table` (text-rendered conjugation/declension
  table), `--html` (raw table HTML), `--raw` (full wikitext),
  `--json` (machine-readable).
- Surfaces both the Wiktionary URL and the bararan.am search URL —
  the latter as a clickable fallback because bararan.am is a SPA
  that doesn't expose a stable scraping endpoint.

Wiktionary's Armenian conjugation tables (rendered from the
`{{hy-conj-ել}}` / `{{hy-conj-ալ}}` templates) are unusually
comprehensive: in one table they cover infinitive, all 8 participles
(naming them with both the English term and a link to the Armenian
դերբայ category), all 7 finite indicative tenses, subjunctive,
conditional (= our hypothetical), and imperative. So the tool gives
us a reference table on demand for any verb in the deck.

**On bararan.am:** they run a JavaScript SPA whose word data is
fetched from internal API endpoints (`/api/search` etc., which return
HTTP 400 on plain GET — they expect specific headers/POST payloads).
Reverse-engineering that without browser dev-tools is fragile, so
`lookup.py` just emits the search URL for click-through. If a stable
JSON endpoint is found later, plugging it in is straightforward.
