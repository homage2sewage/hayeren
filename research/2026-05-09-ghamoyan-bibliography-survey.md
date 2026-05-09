# Ghamoyan bibliography — survey for colloquial-language source expansion

Survey of the 63-entry "Օգտագործված գրականության ցանկ"
(used-literature list) at ghamoyan p116-117, scored for
relevance to expanding our colloquial-Armenian knowledge.

## Method

Extracted from `ghamoyan/out/full.jsonl` p116-117. Russian-script
entries were extracted as Latin1-mojibake (cp1251 roundtrip
from the ARMSCII-decoded JSONL); recovered via
`s.encode("latin1").decode("cp1251")`. Bibliography organisation:
1-52 are Armenian-language sources (sorted alphabetically by
author); 53-58 are Russian sociolinguistics sources; 58-63 are
web URLs and statistical sources.

## Top-priority acquisition candidates

### Tier 1 — directly on colloquial / spoken / dialect Armenian

**#34 Ղուկասյան Ս., *Առօրյա բառարան* (Everyday Dictionary), Երևան, 2013.**
Single highest-value entry. A whole dictionary of everyday
Armenian — likely contains the slang, fillers, idioms, and
register-marked vocabulary that our `topics/lexicon/`
sub-tree is trying to cover from a single source (ghamoyan
itself). 2013 publication, contemporaneous with the ghamoyan
study. Acquisition: published in Yerevan; check for a digital
copy via Armenian academic repositories or Nayiri.com-style
public-domain wikis.

**#24 *Ժամանակակից հայերեն խոսակցական լեզուն* (Modern Armenian
Colloquial Language), Երևան, 1981.** Anonymous / collective
work — title is a direct match for our concern. Older (1981)
so any phenomena discussed are pre-modern-Yerevan-Russian
contact-era; reference value rather than living-corpus value.

**#16 Բաղդասարյան-Թափալցյան, *Արարատյան բարբառի խոսվածքները
հոկտեմբերյանի շրջանում* (Spoken forms of the Ararat dialect in
the Hoktemberian district), ՀՍՍՀ ԳԱ հրատ., 1973.** Ararat
dialect study. Yerevan colloquial sits close to the Ararat
dialect family; the localised spoken-form documentation here
likely overlaps with phonological / morphological patterns in
our existing `topics/phonology/` and
`topics/lexicon/yerevan_slang.md`.

**#49 Սարգսյան Ն., *Առօրյա խոսքի կառուցման
առանձնահատկություններ* (Features of everyday-speech
construction), Լեզվի և ոճի հարցեր 10, 1987, էջ 231-287.**
Article (~57 pages) on syntactic / structural features of
everyday speech. Older but specifically syntax-focused.

**#50 Սարգսյան Ն., *Խոսքի մասերի գործածության
առանձնահատկությունները խոսակցական լեզվում* (Part-of-speech
usage features in colloquial language), 2012, էջ 291-294.**
Same author, modern paper — focuses on POS distribution in
colloquial speech (likely the kind of "fillers + discourse
markers + register-marked function words" register we already
mine ghamoyan for).

### Tier 2 — phraseology / idioms

**#13 Բադիկյան Խ., *Ժամանակակից հայերենի դարձվածային միավորները*
(Phraseological units of Modern Armenian), 1986.**

**#18 Բեդիրյան Պ., *Ժամանակակից հայերենի դարձվածաբանություն*
(Modern Armenian phraseology), Երևան, "Լույս" 1978.**

Both directly feed `topics/lexicon/idioms_phrasal.md`. Bedirian's
1978 vol. is the older standard reference; Badikyan's 1986 vol.
likely supplements with later attestations. Either or both would
be primary citation sources for an idiom-topics sub-tree.

### Tier 3 — phonology / orthoepy

**#33 Ղարագուլյան Թ., *Ժամանակակից հայերենի ուղղախոսությունը*
(Modern Armenian orthoepy), 1974.** This is the orthoepy
(prescribed-pronunciation) reference for Modern Eastern
Armenian. Would directly settle questions like "is պղպեղ →
պխպեղ?" — orthoepy books document exactly this kind of
spelling-vs-pronunciation alternation across the lexicon.
Companion / authority for `topics/phonology/voiced_aspirated_alternation.md`.

### Tier 4 — etymology / lexicon

**#7 Աճառյան Հր., *Հայերեն արմատական բառարան* (Armenian
Etymological Dictionary), 4 vols, 1971-1979.** Aлready on the
acquisition wishlist (`research/2026-05-07-hl-acquisition-plan.md`
mentions Acharyan as the canonical source for tracing colloquial
particles like `հլը` to their pre-modern roots). Public-domain
status; should be available on Nayiri.com or similar.

**#52 Օհանյան Հ., *Ժամանակակից հայոց լեզվի բառապաշարը և նրա
հարստացման միջոցները* (Modern Armenian vocabulary and means of
enrichment), 1982.** Lexicology — would inform the
borrowing/code-switching coverage in
`topics/lexicon/code_switching_with_russian.md`.

### Tier 5 — Russian sociolinguistics theory

| # | Author | Title | Year |
|---|--------|-------|------|
| 53 | Алпатов В. | Языковая ситуация в регионах современной России | 2005 |
| 54 | Гамперц Дж. (Gumperz, translated) | Типы языковых обществ | 1975 |
| 55 | Ларин Б. | К лингвистической характеристике города | 1977 |
| 56 | Серебренников Б. | Территориальная и социальная дифференциация языка | 1970 |
| 57 | Степанов Г. | Типология языковых состояний и ситуаций | 1976 |
| 58 | Швейцер А. | К проблеме социальной дифференциации языка | 1982 |

Foundational Russian-language sociolinguistics — relevant for
*framing* (urban linguistics, social differentiation, language-
contact theory) but not Armenian-specific. Useful as background
reading; not direct primary sources for our colloquial-Armenian
content. Larin (1977) on urban linguistic characterisation is
the closest in subject to what ghamoyan models its own approach
on.

## Lower priority — general grammar / stylistics

Entries 1-6 (Aбегян, Aбрахамян, Aлгайан×4): general modern-Armenian
grammar / linguistic theory; useful as authority but doesn't add
register-specific content.

Entries 8-12, 14, 17, 19-23, 27-32, 35-48, 51-52: stylistics,
language correctness, education-domain, syntactic analysis,
diachronic. Each is a single-volume scholarly Armenian
publication; selectable case-by-case if a specific topic-graph
gap calls for one of them.

## Web sources (58-63)

Mostly broken links by 2026 (the publications are from 2013-2014
research); Armenian Statistical Service URLs may still resolve.
Not relevant for linguistic content.

## Acquisition plan

If the goal is **maximum colloquial-language signal per unit of
work**, the pick order:

1. **#34 Ղուկասյան Առօրյա բառարան** (2013) — directly a
   colloquial dictionary; if obtained, becomes a primary lexicon
   citation source rivalling ghamoyan itself in coverage.
2. **#33 Ղարագուլյան ուղղախոսություն** (1974) — orthoepy reference
   for the spelling↔pronunciation alternation work.
3. **#7 Աճառյան etymological dictionary** (1971-1979) — already
   wished-for; would close several outstanding gaps including
   `հլը` and other colloquial particles' diachronic background.
4. **#13 Բադիկյան OR #18 Բեդիրյան phraseology** — pick one to
   anchor an idioms-and-phraseology citation source.

Together these would expand the topic graph's primary-source
coverage from `{sakayan, ghamoyan, parnasyan, tioyan}` to a 7-8
book pillar set with strong colloquial-side weight.

The deferred path (lower priority but worth noting): the Russian
sociolinguistics entries (53-58) might be worth a single
background-reading pass to better frame *how* we model
register/dialect/contact — they're the theoretical lens
ghamoyan herself uses.

## Availability findings (2026-05-09 web search)

Searches across National Library of Armenia (haygirk.nla.am),
Pan-Armenian Digital Library (arar.sci.am), Nayiri.com, Google
Books, WorldCat, ASPIRANTUM's standard-references list:

### #34 Ղուկասյան *Առօրյա բառարան* (2013) — NOT FOUND online

The originally-prioritised target. Searches for the title +
author in Armenian script, transliterated form, and combined
with year produced no hits in any major Armenian or international
catalogue. Notable absences:

- Not on Pan-Armenian Digital Library (arar.sci.am).
- Not on Nayiri.com's dictionary collection.
- Not on Google Books.
- Not on ASPIRANTUM's curated "most popular Armenian
  dictionaries" list.
- The National Library catalogue's `koha` interface returns
  403 to `WebFetch` (likely User-Agent gating).

This is consistent with a **small-print / institute /
self-published** edition: the bibliography entry "Երևան, 2013"
without a publisher name is the diagnostic signal. Acquisition
path likely requires either:

1. In-person visit to NLA Yerevan, or
2. Inter-library loan via a major academic library that
   already holds it, or
3. Direct contact with the author or with ghamoyan herself
   (who cited it).

Not a "download tomorrow" target. Parking.

### #7 Աճառյան *Etymological Dictionary* (4 vols, 1971-1979) — FREELY AVAILABLE

Internet Archive hosts all 4 volumes with full ABBYY-OCR
searchable text:

- Vol I: https://archive.org/details/Hrarm1
- Vol II: https://archive.org/details/Hrarm2
- Vol III: https://archive.org/details/Hrarm3
- Vol IV: https://archive.org/details/Hrarm4

Each available as PDF (~140 MB), searchable PDF (~192 MB),
plain text (~3.7 MB), and other formats. Public domain by
publication year.

**This is the highest-leverage immediate acquisition** — would
close the long-standing `հլը`/colloquial-particle etymology
gap (per `research/2026-05-07-hl-acquisition-plan.md`) and
provide diachronic backing for many other entries in our
existing topic graph.

### #18 Բեդիրյան phraseology — NAYIRI HOSTING

Bediryan's phraseological dictionary work is on
[nayiri.com](http://nayiri.com/) (specifically
*Հայերեն դարձվածքների ընդարձակ բացատրական բառարան*, 2011 —
later edition than the 1978 ghamoyan-cited one, but same
author / lineage). Free image-based access; OCR availability
to be checked.

### Other ghamoyan-cited works on Nayiri.com

A broader nayiri inventory pass would surface several other
items from this bibliography. Confirmed already on nayiri:

- Sukiasyan/Galstyan *Phraseological Dictionary*
- Aghayan *Modern Armenian Explanatory Dictionary*
- Acharyan *Comprehensive Grammar of Armenian* (#8)
- Malkhasyants *Explanatory Dictionary*
- Acharyan *Etymological* — same as Internet Archive above.

So the *technical-acquisition* path for several wishlist items
is "scrape nayiri.com" — a tooling task. The harder
acquisitions are the post-2010 small-print Yerevan publications
(Ղուկասյան, Բադիկյան-2012, Միրզոյան-2013, etc.).

## Recommended acquisition pivot

Original priority: #34 first → #33 → #7 → #13/#18.

Updated priority (based on availability):

1. **#7 Acharyan Etymological** — direct download from
   Internet Archive. **Start here.** Run a one-off OCR-text
   pull (the ABBYY layer is already there) and write
   `acharyan/extract.py` modelled on the parnasyan/tioyan
   pipelines. Becomes a primary diachronic-etymology source
   for the topic graph.
2. **#18 Bediryan phraseology** — scrape from Nayiri.
   Becomes the citation source for `topics/lexicon/idioms_phrasal.md`.
3. **#33 Ղարագուլյան orthoepy** (1974) — search Nayiri / Pan-
   Armenian; if not findable, check NLA. Less urgent now that
   #7 is in the pipeline.
4. **#34 Ղուկասյան Առօրյա բառարան** — defer until a
   Yerevan-based contact path exists. The colloquial-vocab
   gap can be partly filled by Bediryan + ghamoyan in the
   meantime.

## Open questions

- **Availability**: see above.
- **Nayiri scraping ethics / scale**: Nayiri.com publishes
  these dictionaries on a community basis with image-based
  rendering (no bulk download API). A respectful scrape
  (rate-limited, headword-by-headword for relevant lemmas)
  is technically feasible but not zero-cost. Worth doing
  only after Acharyan-from-Internet-Archive is integrated.
- **Schema fit**: would books that aren't directly extractable
  to JSONL fit our citation-checked topic-file model? The
  citation-check skill assumes
  `<book>/out/full.jsonl`-shaped extractions. New sources would
  need OCR / extraction work first — comparable to the
  parnasyan/tioyan work we did earlier.
- **Coverage overlap**: how much of #34 (Ղուկասյան Առօրյա) overlaps
  with what's already in ghamoyan Ch3 (slang)? If high overlap,
  diminishing returns; if low, prime expansion target.

## Cross-references

- `research/2026-05-07-russian-language-sources.md` — the prior
  Russian-language acquisition survey (Parnasyan & Markosyan).
- `research/2026-05-07-hl-acquisition-plan.md` — the Acharyan
  acquisition plan for the `հլը` particle.
- `kb-design.md` — multi-book pillar strategy. Adding any of
  these would extend the corpus-pillar set defined there.
- `topics/lexicon/yerevan_slang.md`,
  `topics/lexicon/idioms_phrasal.md`,
  `topics/pragmatics/intimate_register.md` — topic files that
  would directly benefit from #34, #13/#18.
