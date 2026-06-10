# Known phonetic transcriptions from the corpus

Harvested respellings (spelled → pronounced) attested in this
workspace's corpus. These are the voiced→voiceless/aspirated
alternations of the three-way laryngeal contrast — see
[`voiced_aspirated_alternation.md`](voiced_aspirated_alternation.md)
for the analysis (what's a rule vs. lexical vs. root-regular).

**How this was built** (regenerate by re-running the harvest in
`research/2026-06-10-transcription-coverage-and-system.md`):

- **sakayan rows** — `[respell]` annotations baked into
  `cards/sakayan/*.tsv`, themselves derived by `sakayan/phonetics.py`
  from Sakayan's transliteration column. Source cites the unit
  file(s) the form appears in (`u07v` = `unit07_vocab.tsv`,
  `u01d1` = `unit01_dialogue1.tsv`, `chunks` = `chunks.tsv`).
- **hand-curated rows** — `PHONETIC_OVERRIDES` in
  `frequency/build_deck.py`; rationale + book pages in the topic file.

**98 entries** (87 sakayan-attested, 11 hand-curated). Deviation tally: ջ→չ ×23, դ→թ ×22, գ→ք ×19, ձ→ց ×12, դ→տ ×11, բ→փ ×8, բ→պ ×2, գ→կ ×2.

## դ → թ (d → tʰ, aspirated) — 21

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| անարդար | [անարթար] | դ→թ | sakayan u07v |
| արդեն | [արթեն] | դ→թ | sakayan u02v, u11d3 |
| երիտասարդ | [երիտասարթ] | դ→թ | sakayan chunks, u04d1, u08v |
| երրորդ | [երրորթ] | դ→թ | sakayan u11d3 |
| ընդունակ | [ընթունակ] | դ→թ | sakayan u08v |
| ընդունել | [ընթունել] | դ→թ | sakayan u01v, u08v |
| խնդրեմ | [խնթրեմ] | դ→թ | sakayan chunks, u03d4, u05d3, u06d3 |
| խորհուրդ | [խորհուրթ] | դ→թ | sakayan u04v |
| կարդա | [կարթա] | դ→թ | sakayan chunks, u06d1 |
| կարդում | [կարթում] | դ→թ | sakayan chunks, u01d1 |
| կենդանի | [կենթանի] | դ→թ | sakayan u06v, u07v |
| կոկորդս | [կոկորթս] | դ→թ | sakayan chunks, u07d2 |
| հաջորդ | [հաջորթ] | դ→թ | sakayan chunks, u11d2 |
| մարդ | [մարթ] | դ→թ | sakayan u07v, u08d1 |
| նախորդին | [նախորթին] | դ→թ | sakayan chunks, u08d1 |
| որդի | [որթի] | դ→թ | sakayan u04v |
| վարդ | [վարթ] | դ→թ | sakayan u09v |
| վարորդ | [վարորթ] | դ→թ | sakayan u08v |
| օդ | [օթ] | դ→թ | sakayan u06v, u11v |
| օդաչու | [օթաչու] | դ→թ | sakayan u08v |
| օդն | [օթն] | դ→թ | sakayan chunks, u09d2 |

## դ → տ (d → t, unaspirated) — 11

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| ազգանունդ | [ազգանունտ] | դ→տ | sakayan chunks, u01d2 |
| այդ | [այտ] | դ→տ | sakayan chunks, u01d1 |
| այդքան | [այտքան] | դ→տ | sakayan chunks, u10d1 |
| անունդ | [անունտ] | դ→տ | sakayan chunks, u01d2 |
| դուրդ | [դուրտ] | դ→տ | sakayan chunks, u05d1, u05d2, u08d1, u08d2 |
| ծնողներիդ | [ծնողներիտ] | դ→տ | sakayan chunks, u04d1 |
| կահույքդ | [կահույքտ] | դ→տ | sakayan u05d1 |
| կարդալ | [կարտալ] | դ→տ | sakayan u02d1 |
| կենացդ | [կենացտ] | դ→տ | sakayan chunks, u03d4 |
| հետդ | [հետտ] | դ→տ | sakayan u10d1 |
| մորդ | [մորտ] | դ→տ | sakayan chunks, u04d1 |

## բ → փ (b → pʰ) — 8

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| անհամբեր | [անհամփեր] | բ→փ | sakayan u11v |
| դարբին | [դարփին] | բ→փ | sakayan u08v |
| երբ | [երփ] | բ→փ | sakayan chunks, u05v, u06d2, u06v, u07d2, u08d2 |
| համբուրել | [համփուրել] | բ→փ | sakayan u09v, u11v |
| նրբանկատ | [նրփանկատ] | բ→փ | sakayan u08v |
| շաբաթ | [շափաթ] | բ→փ | sakayan chunks, u11d2 |
| շաբաթը | [շափաթը] | բ→փ | sakayan chunks, u02d1 |
| ուրբաթ | [ուրփաթ] | բ→փ | sakayan u10d1 |

## բ → պ (b → p) — 2

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| եղբայրն | [եղպայրն] | բ→պ | sakayan u04d2 |
| եղբորս | [եղպորս] | բ→պ | sakayan chunks, u04d1, u04d2 |

## գ → ք (g → kʰ) — 19

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| անգամ | [անքամ] | գ→ք | sakayan chunks, u02d1, u11d3 |
| անգամն | [անքամն] | գ→ք | sakayan u11d3 |
| ծագել | [ծաքել] | գ→ք | sakayan u09v |
| հագել | [հաքել] | գ→ք | sakayan chunks, u08d2 |
| հագնել | [հաքնել] | գ→ք | sakayan u05v |
| հագուստ | [հաքուստ] | գ→ք | sakayan u05v |
| հագուստը | [հաքուստը] | գ→ք | sakayan u05d3 |
| հագուստս | [հաքուստս] | գ→ք | sakayan u05d2 |
| համակարգիչ | [համակարքիչ] | գ→ք | sakayan chunks, u06d3 |
| հոգնել | [հոքնել] | գ→ք | hand-curated |
| հոգնում | [հոքնում] | գ→ք | sakayan u05d2 |
| հոգու | [հոքու] | գ→ք | sakayan chunks, u10d1 |
| միրգ | [միրք] | գ→ք | sakayan u03v |
| շոգն | [շոքն] | գ→ք | sakayan chunks, u09d1 |
| օգնական | [օքնական] | գ→ք | sakayan u08v, u10d1 |
| օգնել | [օքնել] | գ→ք | sakayan chunks, u10d1 |
| օգնեցեք | [օքնեցեք] | գ→ք | sakayan chunks, u07d2 |
| օգնիր | [օքնիր] | գ→ք | sakayan chunks, u06d1 |
| օգտակար | [օքտակար] | գ→ք | sakayan u06v, u07v |

## գ → կ (g → k) — 2

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| երգող | [երկող] | գ→կ | sakayan u09v |
| հագիր | [հակիր] | գ→կ | sakayan u09d3 |

## ձ → ց (dz → tsʰ) — 12

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| ատաղձագործ | [ատաղցագործ] | ձ→ց | sakayan u08v |
| արձակուրդ | [արցակուրթ] | ձ→ց,դ→թ | sakayan u11v |
| բարձր | [բարցր] | ձ→ց | sakayan u05d2, u06v, u07v |
| բարձրահասակ | [բարցրահասակ] | ձ→ց | sakayan u08d2, u08v |
| դեղձ | [դեղց] | ձ→ց | sakayan u03v |
| դերձակ | [դերցակ] | ձ→ց | sakayan u08v |
| տարեդարձն | [տարեդարցն] | ձ→ց | sakayan u10d1 |
| փորձ | [փորց] | ձ→ց | sakayan u08v |
| փորձարկում | [փորցարկում] | ձ→ց | sakayan u08v |
| փորձել | [փորցել] | ձ→ց | sakayan u04v, u05d3 |
| օձ | [օց] | ձ→ց | sakayan u06v |
| օձերը | [օցերը] | ձ→ց | sakayan u06v |

## ջ → չ (dʒ → tʃʰ) — 23

| word | respell | all deviations | source |
|------|---------|----------------|--------|
| աղջիկ | [աղչիկ] | ջ→չ | hand-curated |
| ամբողջ | [ամբողչ] | ջ→չ | hand-curated |
| անմիջապես | [անմիչապես] | ջ→չ | hand-curated |
| առաջ | [առաչ] | ջ→չ | sakayan u07d2 |
| առաջարկել | [առաչարկել] | ջ→չ | sakayan u04v, u08v |
| առաջը | [առաչը] | ջ→չ | sakayan u05v |
| առաջին | [առաչին] | ջ→չ | sakayan chunks, u11d3 |
| առողջություն | [առողչություն] | ջ→չ | sakayan u11v |
| մեջ | [մեչ] | ջ→չ | hand-curated |
| մեջք | [մեչք] | ջ→չ | sakayan u07v |
| միջազգային | [միչազգային] | ջ→չ | hand-curated |
| միջին | [միչին] | ջ→չ | hand-curated |
| միջոց | [միչոց] | ջ→չ | hand-curated |
| միջև | [միչև] | ջ→չ | hand-curated |
| ողջ | [ողչ] | ջ→չ | hand-curated |
| վերջ | [վերչ] | ջ→չ | hand-curated |
| վերջանալ | [վերչանալ] | ջ→չ | sakayan u09v |
| վերջապես | [վերչապես] | ջ→չ | sakayan u04d3, u08v |
| վերջերս | [վերչերս] | ջ→չ | sakayan u05d1 |
| վերջին | [վերչին] | ջ→չ | sakayan u08d1 |
| վերջնական | [վերչնական] | ջ→չ | sakayan chunks, u05d3 |
| վերջո | [վերչո] | ջ→չ | sakayan u09v |
| քրոջս | [քրոչս] | ջ→չ | sakayan chunks, u04d1 |

## Cross-book attestations (exact page citations)

From the citation-checked topic file frontmatter — these carry
verbatim-quote + page + y-range provenance:

| form | spelled → pronounced | book | page | note |
|------|----------------------|------|------|------|
| ընդունել [ընթունել] | դ → թ | sakayan | 30 | translit `[§nt…unel]` shows /nt/ for spelled /nd/ |
| կարդում [կարթում] | դ → թ | sakayan | 36 | paradigm header `[kart-um]` |
| բարձր [բարցր] | ձ → ց | sakayan | 42 | vocab `[bart…r]`, /ts/ for spelled /dz/ |
| զեղչ [զէխչ] | ղ → խ /χ/ (before չ) | tioyan | 38 | "discount" / скидка — cluster devoicing |
| աղջիկ [ахчик] | ղջ → խչ | parnasyan | 346 | both cluster members devoice |
| ամբողջ [амбохч] | ղջ → խչ | parnasyan | 346 | "whole/entire" |
| ընկեր → ընգեր | կ → գ (voicing, *reverse* direction) | ghamoyan | 39 | colloquial; dialect-driven |
| գդալ → քթալ | voiced → aspirated | ghamoyan | 39 | "spoon", colloquial |

> The ghamoyan rows show the alternation runs **both directions** in
> Yerevan colloquial speech (voicing *and* devoicing), attributed to
> dialect/idiom influence — not just the literary devoicing the
> sakayan rows above capture.

## Caveats

- The ghamoyan/tioyan/parnasyan **transcription columns are largely
  OCR-garbled** in extraction (`թագավոր [ририщоп]`, `դեղձ [199]`), so
  only the hand-verified, topic-file-cited forms above are usable —
  bulk-harvesting those books is not currently viable.
- sakayan respells mark only the **single contrast-consonant** change;
  schwa epenthesis and the ղ→խ surface shift inside clusters are
  documented in the topic file but not in the bracket.

