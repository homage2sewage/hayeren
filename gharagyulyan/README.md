# gharagyulyan/ — Tereza Gharagyulyan, *Modern Armenian Orthoepy*

Թերեզա Ղարագյուլյան, *Ժամանակակից հայերենի ուղղախոսությունը*
(Modern Armenian Orthoepy), Armenian SSR Academy of Sciences,
Acharyan Institute of Language, 1974. Public-domain by
publication year + Soviet-era academic publication.

The standard prescriptive reference for spelling-vs-pronunciation
relationships in literary Eastern Armenian — the authoritative
source for questions like "is `պղպեղ` pronounced `պխպեղ`?",
"does `մեջ` devoice to `մեչ`?", and the broader patterns of
voiced↔aspirated, ղ↔խ, vowel-reduction, and cluster-assimilation
alternations.

## Source

Pan-Armenian Digital Library:
https://arar.sci.am/Content/362355/GHARAGYULYAN_TEREZA_Jamanakakic_hajereni_ughghaxosutjuny.pdf

`gharagyulyan_orthoepy.pdf` — 14 MB. Contains an embedded text
layer (good news: extraction is cleaner than the Acharyan DJVU
OCR), with some encoding noise on title-page Russian/Armenian
mixed text.

## Why this acquisition

Identified as #33 in the ghamoyan-bibliography survey
(`research/2026-05-09-ghamoyan-bibliography-survey.md`). It's the
authoritative orthoepy reference companion to
`topics/phonology/voiced_aspirated_alternation.md` — settles
exactly the kind of "lexicalized vs phonologically-conditioned"
questions our existing topic file leaves open.

Specific anticipated value:

- Documents the literary-pronunciation norms across the lexicon —
  more comprehensive than sakayan's per-vocab transliterations.
- Pre-dates ghamoyan (1974 vs 2014) and explicitly addresses
  "deviations from literary pronunciation" in a 50-year window
  that includes the Yerevan-colloquial drift ghamoyan documents.
- Tier-3 priority on the bibliography survey, but acquired
  ahead of Tier-2 Bediryan because the orthoepy fits more
  directly into existing topic-graph gaps.

## Extraction

`extract.py` walks pages with PyMuPDF and emits per-line JSONL
entries to `out/full.jsonl`, mirroring the parnasyan/tioyan
schema:

```json
{"page": 7, "bbox": [...], "text_raw": "...", "text": "...", "ocr_conf": null}
```

`text_layer` not OCR — confidence is null. Page numbers come
from PDF page index (1-indexed); the printed page number may
differ for the Soviet-style front-matter.

## Usage

```sh
python3 extract.py
# Search for orthoepy notes on a specific cluster:
python3 -c "
import json
for line in open('out/full.jsonl'):
    e = json.loads(line)
    if 'ղջ' in e.get('text', ''):
        print(f'p{e[\"page\"]}: {e[\"text\"][:120]}')
"
```

## Layout

```
gharagyulyan/
├── README.md
├── manifest.yaml
├── gharagyulyan_orthoepy.pdf       # raw PDF from arar.sci.am
├── extract.py                       # PDF text → JSONL
└── out/
    └── full.jsonl
```
