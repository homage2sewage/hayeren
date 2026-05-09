# acharyan/ — Hrachya Acharyan, *Armenian Etymological Dictionary*

Hrachya Acharyan, *Հայերեն Արմատական Բառարան* (Armenian
Etymological Dictionary), 4 vols, Yerevan State University Press,
1971-1979. Public-domain by publication year + Soviet-era
academic publication.

The canonical etymological reference for Armenian. Tracks every
classical / literary Armenian root back through documented
attestations to Indo-European, Iranian, Greek, Aramaic, Turkish,
and other source languages.

## Source

Internet Archive scans, ABBYY-OCR'd text layer:

- Vol I (Ա): https://archive.org/details/Hrarm1
- Vol II (Բ-Թ): https://archive.org/details/Hrarm2
- Vol III (Ժ-Ղ): https://archive.org/details/Hrarm3
- Vol IV (Մ-Ֆ): https://archive.org/details/Hrarm4

Downloaded `vol{1,2,3,4}.txt` (≈3.7 MB each) — the DJVU OCR
text. Searchable PDFs are also available on Internet Archive
(~190 MB each) but the text layer is the same OCR.

## OCR quality

ABBYY at 600 DPI on the original 1971-1979 print. Quality
varies — generally readable Armenian script but with these
artifacts:

- Headword detection is the main signal: dictionary entries
  start with an all-caps Armenian word, sometimes prefixed
  with `*` (reconstructed) or `+` (cross-reference / variant).
- Embedded foreign-script characters (Greek, Arabic, cuneiform
  etymons) are mostly mis-recognised as ASCII / random
  Unicode. Tolerable since etymons aren't our primary
  search target — Armenian-side info is.
- Page numbers preserved as bare-digit lines in the OCR
  output. Useful for citation.
- Pre-dictionary front-matter (preface, source list, abbreviation
  key) takes the first ~30 pages of vol I; not relevant for
  per-lemma lookup.

## Coverage caveat

Acharyan's scope is **classical / literary** Armenian. Modern
*colloquial* particles like `հլը` (the original acquisition-plan
target — see `research/2026-05-07-hl-acquisition-plan.md`) may
NOT have entries if they lack classical attestation. Vol III
search for `ՀԼԸ` returns no bare-headword match; ՀԼ-prefixed
entries that do exist are mostly Greek/Aramaic-loanword roots
(`ՀԱԼԻԼԱ կամ ՀԼԷԼԻՃ` "myrobalan", `ՀԼՈԵ` "aloe", etc.).

So Acharyan closes the *etymological* coverage gap for
classical Armenian, but the colloquial-particle gap may need
EANC corpus or Sukiasyan/Galstyan phraseology.

## Extraction

`extract.py` converts each volume's text to `out/vol{N}.jsonl`
with one entry per dictionary lemma. Schema:

```json
{
  "volume": 1,
  "page": 47,
  "headword": "ԱԴԱՄԱՆԴ",
  "headword_marker": "",
  "body": "...etymology prose with attestations...",
  "line_start": 4823,
  "line_end": 4892
}
```

`headword_marker` is `*` for reconstructed forms or `+` for
cross-reference shells; empty for standard entries.

## Usage

```sh
# One-time extraction (idempotent)
python3 extract.py

# Search for a specific lemma's entry
python3 -c "
import json
for line in open('out/vol1.jsonl'):
    e = json.loads(line)
    if e['headword'] == 'ԱԴԱՄԱՆԴ':
        print(e['body'][:500]); break
"
```

## Layout

```
acharyan/
├── README.md
├── manifest.yaml             # bibliographic metadata for citation-check
├── vol1.txt - vol4.txt       # raw OCR text from Internet Archive (~15 MB total)
├── extract.py                # text → JSONL
└── out/
    ├── vol1.jsonl - vol4.jsonl
    └── full.jsonl            # concatenation for `topics/`-style citation
```
