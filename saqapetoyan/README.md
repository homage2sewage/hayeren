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
- [ ] **Structured-entry parse** — split each entry into
      `{headword, pos, domain, definition, native_coinage, ru, en}`,
      de-hyphenate line-final splits, and emit one record per entry.
      Deferred: this is a parsing *heuristic* and must go through the
      challenge protocol (`CLAUDE.md` § "Heuristic validation") with a
      golden-anchor sample before it ships.

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
