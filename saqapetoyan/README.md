# saqapetoyan — *Բառգրքույկ. Նոր և նորակազմ բառեր հայերենում*

Source: **Ռ.Կ. Սաքապետոյան — *Բառգրքույկ. Նոր և նորակազմ բառեր
հայերենում*** (A Wordbook: New and Newly-coined Words in Armenian)
(Yerevan: ԵՊՀ հրատարակչություն / Yerevan State University Press,
2014, 80 pp, ISBN 978-5-8084-1849-3). Editor prof. Y. Avetisyan;
English consultant Karapet Sakapetoyan.

A prescriptive glossary of **neologisms**: foreign loanwords paired
with proposed native-Armenian coinages, each with Russian and English
equivalents. Useful as a lexical resource (loanword ↔ native coinage ↔
ru ↔ en) and as a window on standard-language coinage debates (see the
preface, ԱՌԱՋԱԲԱՆ, pp. 3-6).

## Status

- [x] PDF identified; clean embedded **Unicode** text layer (no
      ARMSCII-8 decode, no OCR — contrast ghamoyan).
- [x] `extract.py` working end-to-end on all 79 pages
      (1622 line records → `out/full.jsonl` + `out/full.md`).
- [x] **Structured-entry parse** (`parse_entries.py` → `out/entries.jsonl`):
      **614 entries** from body pp. 9-76, one record per dictionary entry.
      Ran through the challenge protocol (`CLAUDE.md` § "Heuristic
      validation") incl. two adversarial critic-agent passes; guarded by
      `golden_entries.tsv` + `validate_entries.py`.

## Read this before USING the structured data

Four semantic caveats — the data is a *prescriptive coinage proposal*,
not a usage record:

1. **A native coinage is the author's PROPOSAL, not an attested word.**
   The book invents Armenian replacements for loanwords; many have
   ~zero real usage. Canonical case: `Մսադոնդող` (proposed for
   *холодец*/holodets) returns essentially nothing on the open web.
   Treat `native_coinages` as suggestions, and `definition` as the
   reliable meaning signal. Never present a coinage as "the Armenian
   word for X" without checking real usage (corpus/web).
2. **Many headwords are Russian-origin loanwords.** The headword +
   `ru` pair is therefore a useful signal for **colloquial / spoken
   Armenian**, where these russified forms are what people actually
   say (vs. the prescriptive coinage). Good raw material for the
   colloquial-register topics and the frequency deck's gap analysis.
3. **Russian translations are present for (almost) every entry**
   (`ru` 614/614). A parallel Armenian-loanword ↔ Russian layer.
4. **The inverse map (coinage → headword) is usable for
   synonyms/explanations.** Some coinages are *not* rare at all
   (`Ցեղասպանություն` "genocide", `Հանրակառք` "bus") — so a
   coinage→loanword lookup gives a native synonym / gloss for the
   loanword. 900 coinage tokens across the deck.

## Structured-entry schema (`out/entries.jsonl`)

One record per entry:

| field | meaning |
|-------|---------|
| `headword` | the loanword (Armenian script); homograph digit split off |
| `homograph` | `1`/`2`/… when the book numbers homographs (`Ավտոմատ1`) |
| `pos` | part-of-speech abbrev (`գ.`, `ած.`, `ած.գ.`, `ած. մ.`) or null |
| `domain` | `[]` of domain tags (`տեխն.`, `ախտ.`, `փիլ.`…) |
| `lang_origin` | `[]` of source-language tags (`արաբ.`, `գերմ.`, `ֆր.`) |
| `definition` | encyclopaedic gloss (the reliable meaning), or null |
| `native_coinages` | `[]` of proposed Armenian terms (see caveat 1) |
| `ru` / `en` | Russian / English equivalents |
| `multi_sense` | `true` for numbered-sense entries — consult `raw` |
| `stray` | non-Armenian fragment the right-anchor split couldn't place |
| `raw` | the de-hyphenated source line — ground truth, always present |
| `warnings` | per-entry review flags (see below) |

Parsing strategy (full rationale in `parse_entries.py` docstring): group
lines → de-hyphenate → split headword on the dash → parse POS/domain →
right of the last Armenian letter is `[ru][en]` (split by script) → the
Armenian region is split **definition (regular) vs coinage (bold) by FONT
WEIGHT**.

#### The boldface signal (why this is correct, not heuristic)

The author prints every native **coinage in bold** and the explanatory
definition in regular weight. This is the *only* reliable
definition↔coinage boundary — the `՝`/comma delimiters are used
inconsistently (also between coinages, also as secondary commas). The
first parser used `՝`-position and **disagreed with the visible bold on
~28 entries** (coinages buried in definitions and vice-versa), caught by
an independent page-parallel reader audit
(`research/2026-06-14-saqapetoyan-reader-audit.md`).

The bold is **faux** — drawn as a fill + stroke overprint (each glyph
twice), so it is *invisible* to `get_text()`/span `flags` (everything
reports `Sylfaen flags=4`). `parse_entries.py` recovers it from
`page.get_texttrace()`: a glyph is bold iff a stroke-render copy
(`type != 0`) exists at its position. Spaces inside a bold phrase are
bold too, so multi-word coinages (`Արժեթղթերի սեփականատեր`) stay intact.

### Coverage & quality

With 0 cross-script field leaks and the bold-verified def/coinage split:

- `ru` 613/614 · `en` 612/614 · `definition` 327/614 · `coinage(s)` 614/614
- **601/614 entries clean**; 13 flagged for review:
  `no-pos-tag` 5 (book genuinely omits POS), `coinage-unbolded` 3
  (typesetter forgot to bold a lone coinage — `Կուլտուրա→Մշակույթ`),
  `interleaved-field` 2 (`Անտեննա` per-sense Russian; `Ապրիորի` `/լատ./`
  edge), `no-english` 2 (`Էֆտանազիա` truncated; `Դեկադանս` missing comma),
  `no-russian` 1.
- 45 `multi_sense` entries: per-sense definition fragments are joined and
  flagged — coinages are bold-correct; `raw` holds the full structure.

Confirmed by a second, independent reader audit of the previously-flagged
pages (38 → 16 findings; details in the research note). Residual known
issues, all flagged or in `raw`: per-sense Russian on a couple of
multi-sense entries; a few **text-layer glyph artifacts** faithfully
copied from the source (`Բրոնխիտ` `բորբոքում→բորքոքում`; `Ալտրուիստ` has a
Cyrillic `а` in the English `altruist`) — these are source/extraction
quirks, not parser errors.

### Validate after any parser change

```sh
../ghamoyan/.venv/bin/python parse_entries.py --stats   # rebuild entries.jsonl
../ghamoyan/.venv/bin/python validate_entries.py        # golden + structural guard
```

`golden_entries.tsv` anchors one hand-verified entry per failure class
(hyphenated headword, homograph, grave separator, colon-coinage rescue,
definition-inferred, multi-sense, interleaved, genuine no-pos/no-english).
`validate_entries.py` also asserts the structural invariants that caught
the silent entry-boundary merges (no script leaks, no merged headwords).

## How to run

```sh
../ghamoyan/.venv/bin/python extract.py        # → out/full.jsonl + full.md
../ghamoyan/.venv/bin/python extract.py --pages 9     # one page (A-section head)
../ghamoyan/.venv/bin/python extract.py --pages 9-12  # a range
```

(No per-dir `.venv`; reuse `ghamoyan/.venv`, which carries PyMuPDF.)

## Entry structure

```
HEADWORD – POS. [(domain.)] [definition ՝] NATIVE-COINAGE, <ru>, <en>.
```

Examples (p. 9):

| Headword | POS | Native coinage | RU | EN |
|----------|-----|----------------|----|----|
| Աբստրակցիոնիզմ | գ. | Վերացապաշտություն | абстракционизм | abstractionism |
| Ագնոստիցիզմ | գ. (փիլ.) | …ուսմունք՝ Պատճառագիտություն | агностицизм | agnosticism |
| Ագրեսիվ | ած.գ. | Հարձակունակ | агрессивный | aggressive |

POS abbreviations and domain tags are defined in the
**Համառոտագրությունների ցանկ** (abbreviations list, pp. 7-8):
`գ.`=noun, `ած.`=adjective, `ած.գ.`=adj/noun, plus domain tags
`փիլ.`=philosophy, `տեխն.`=technical, `բժշկ.`=medical, etc.

## Layout map

| Section | pp. |
|---------|-----|
| Title + imprint | 1-2 |
| Preface (ԱՌԱՋԱԲԱՆ) | 3-6 |
| Abbreviations list (Համառոտագրությունների ցանկ) | 7-8 |
| Body glossary (Ա–Ֆ) | 9-76 |
| Alphabetical index (Բովանդակություն) | 77-78 |
| Colophon | 79-80 |

## Output

- `out/full.jsonl` — one record per text line:
  `{page, bbox, text_raw, text, ocr_conf}` (`ocr_conf: null`).
- `out/full.md` — flat reading-order render for eyeballing.
