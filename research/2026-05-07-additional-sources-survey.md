# Additional Armenian-language sources — broader survey

**Date**: 2026-05-07 (follow-up to `2026-05-07-russian-language-sources.md`)
**Trigger**: user prompt to check `publishing.ysu.am` and Zangak's
catalog for additional candidates beyond Parnasyan / Tioyan.
**Status**: candidate-list; selective acquisition recommended below.

## What's now in hand

Two new books arrived at top level (`parnasyan.pdf`, `tioyan.pdf`),
both pure raster scans, no text layer. Confirmed via cover renders:

- `parnasyan.pdf` — Парнасян Н.А., Манукян Ж.К., *Самоучитель
  армянского языка*, Луйс, Ереван 1990, 215 image-pages
  (double-page-spread = ~430 book pages). Top recommendation from
  the prior research log.
- `tioyan.pdf` — Тиоян С., Григорян О., Урутян Р., *Самоучитель
  армянского языка / Հայերենի ինքնուսույց*, Зангак-97, Ереван
  2007, 393 pages, single-page scan. Newer Russian-language
  self-teacher; has a comprehensive 43+ lesson grammar coverage.

Both **need OCR** — tesseract is not installed; user decision pending.

## YSU publishing site — unreachable

The URL `http://publishing.ysu.am/hy/1372747165` (and the https
variant, and the related `https://monographs.ysu.am/index.php/ysuph/en`)
all returned `ECONNREFUSED` / `503` from this sandbox. May be a
transient outage, geo-block, or sandbox network restriction. **The
user should browse it directly** and paste the catalog or specific
titles back if useful.

What the search index *suggests* is on YSU publishing:
- **Աճառյան Հր., *Հայերեն լեզվի լիակատար քերականություն`
  համեմատությամբ 562 լեզուների*** (Acharyan, Full Grammar of
  Armenian Compared with 562 Languages) — recently published by YSU
  Press. Major typological / comparative work. Would be the
  scholarly equivalent in Armenian of what Dum-Tragut would be in
  English. Probably not free PDF.
- *Bulletin of Yerevan University. Philology* — peer-reviewed
  journal, Armenian linguistics articles. Open-access via
  `journals.ysu.am`.
- A "Self-teacher of Armenian Language" PDF on `lib.ysu.am`
  (institutional, instituional textbook). Worth checking if user
  reaches the site.

## Zangak publishing — no free PDFs

`zangak.am` is the Zangak Publishing House site. It identifies as a
leading textbook publisher (founded 1997, Mkrtchyan family) but
**does not host free PDF downloads** of its catalog. Visible
products through external listings:

- **Аybbenaran (Eastern-Armenian Alphabet Textbook)** — Gyulamiryan,
  Sevoyan. Children's alphabet primer. Probably not useful for our
  topic-walk pipeline.
- **Reader 2: A Textbook of Western Armenian** — Western Armenian.
  Different dialect; out of current scope.
- Various school textbooks and methodological guides for Armenian
  schools.

The Tioyan book (`tioyan.pdf`) is itself a Zangak-97 publication
(2007). The user already has the only Zangak title most relevant to
the project.

## learnarmenian.org — substantial free PDF catalogue

`https://www.learnarmenian.org/book-pdfs` aggregates 10+ free PDFs.
Authorship and editions are not always specified, so each candidate
needs verification before being treated as authoritative. Notable:

- **Arevelahayeren.pdf** — "Eastern Armenian for the English-Speaking
  World (Ultimate PDF)". Likely a digital re-edit of Sakayan or a
  similar work. **We already have Sakayan's PDF**; a duplicate is
  uninteresting unless it provides a cleaner extraction.
- **Eastern and Western Parallel Lessons.pdf** — comparative across
  dialects. Could underpin a future `topics/dialect-contrast/`
  axis once Western Armenian enters scope. Not priority now.
- **Spoken East Armenian.pdf** — possibly Greppin & Khachaturian
  *Spoken Eastern Armenian* (1980s, US Foreign Service) or similar.
  *Conversational* focus. Would make a second descriptive
  colloquial source alongside ghamoyan if it covers register
  similarly. **Worth investigating before any further book
  acquisition.**
- **Armenian Dictionary in Transliteration (Western pronunciation)**
  — lexical reference, Western dialect. Useful for cross-dialect
  lexicon work, not for current topics.
- **My First Book of Armenian Words** — beginner vocab. Not
  research-relevant.
- **Modern Western Armenian for the English-Speaking World** by Dora
  Sakayan (z-lib source). Western counterpart of the Eastern book
  we already cite. **Useful** if the project expands to Western
  Armenian — same author, same contrastive methodology, allows
  Eastern↔Western comparative topics with a single coherent voice.
- **Grammar: Armenian and English** by Aucher & Byron — 19th century,
  historical curiosity. Probably not useful for synchronic work.
- **Beginner's Western Armenian**, **A Textbook of Modern Western
  Armenian** — Western-only.

## Free academic / scholarly resources

Found via search (not on the user's listed sites):

- **Hrachya Acharyan, *Armenian Etymological Dictionary***
  (Հայերեն արմատական բառարան), 6 volumes (1926-1935), free PDFs:
  - Volume Ա (Ա-Դ) — academia.edu, archive.org
  - Volume Բ (Ե-Կ) — academia.edu, archive.org
  - Volume Գ (Հ-Չ) — academia.edu
  - Volume Դ (Պ-Ֆ) — academia.edu, archive.org
  - Pan-Armenian Digital Library (`arar.sci.am`) hosts the full set.

  ~11,000 root words with grammar and etymology. **The canonical
  reference for Armenian etymology.** Major value for `lexicon/`
  work — every lemma entry could trace its etymology + cognates via
  Acharyan citations. Out of scope for the current topic-walk
  pipeline (it's a dictionary, not a grammar) but worth noting for
  the later lexicon phase.

- **Pan-Armenian Digital Library (ARAR)**, `arar.sci.am` —
  digitised Armenian academic library. Open access. Has the
  Acharyan dictionary and many other scholarly works. Worth
  bookmarking; full catalogue not yet surveyed.

- **Internet Archive** — has scanned versions of older Armenian
  scholarly works, free download.

- **Academia.edu** — many uploaded copies of Armenian linguistics
  papers and books, free with login.

## Open-access journals

- **Bulletin of Yerevan University. Philology** — `journals.ysu.am`,
  open-access, Armenian-language linguistics articles. Likely useful
  for filling specific topic gaps once we know what we're missing.
- **Armenian Studies Journal** at `aaj.ysu.am` — possibly relevant
  but not investigated.

## What's *missing* from the survey

- **Dum-Tragut, *Armenian: Modern Eastern Armenian*** (Benjamins,
  2009) — descriptive grammar in the typological tradition. Not
  free; would be a paid academic acquisition. Still the
  highest-quality typological reference.
- **Vaux, *The Phonology of Armenian*** (Oxford, 1998) — same.
- **Khachaturian, *Spoken Eastern Armenian*** — possibly the same
  as the learnarmenian.org "Spoken East Armenian" PDF. Worth
  identifying.

## Recommendation

**Stop acquiring sources for now.** Four books in hand
(sakayan + ghamoyan + parnasyan + tioyan) is already a strong
pillar set:

| pillar | book | dialect | register | L1 framing |
|--------|------|---------|----------|------------|
| English-contrastive pedagogy | sakayan | eastern-standard | prescriptive-pedagogy | English |
| Armenian-internal descriptive | ghamoyan | yerevan-colloquial | descriptive-linguistic | (Armenian-only) |
| Russian-contrastive pedagogy (older) | parnasyan | eastern-standard | prescriptive-pedagogy | Russian |
| Russian-contrastive pedagogy (newer) | tioyan | eastern-standard | prescriptive-pedagogy | Russian |

The next decision-relevant question is **OCR**: how to extract
parnasyan and tioyan into queryable form. After that pipeline is
working and a topic-walk against the new books has run, the
*output* will tell us what's actually missing — whether to invest
in a typological grammar (Dum-Tragut), a Western Armenian source
(Sakayan-WA), a colloquial second source (Spoken East Armenian),
or the Acharyan dictionary (lexicon work).

If, after running the parnasyan + tioyan walks, gaps still cluster
around:

- **Etymology / loanword stratum** → Acharyan dictionary (free).
- **Typological depth** → Dum-Tragut 2009 (paid).
- **Cross-dialect** → Sakayan's Modern Western Armenian (free PDF).
- **More colloquial / register data** → "Spoken East Armenian" PDF
  identified above.

## OCR — pending decision

Both new PDFs are scans. Tesseract is not installed. Three options
spelled out in task #1 of the current task list:

1. **Install tesseract** + Russian + Armenian language packs;
   build an `extract.py` per book; produce `out/full.jsonl` /
   `out/full.md` like sakayan/ghamoyan. Same pipeline downstream.
   `sudo apt install tesseract-ocr tesseract-ocr-rus tesseract-ocr-hye`.
2. **Vision-based on-demand OCR.** Render specific pages to PNG
   as needed for topic-walks; read via Claude vision; build
   citations directly from image content. No JSONL in the same
   sense; citation-check would need a parallel "image-verifier"
   path. Cheaper for targeted reads, expensive for full-corpus.
3. **Hybrid.** Vision to OCR the TOC and chapter starts (bounded
   work, ~10-30 page reads per book). Tesseract for the bulk-text
   extraction once installed. Vision as the verifier when
   tesseract output is suspect.

**Recommendation**: option 1 is cleanest for matching the existing
pipeline, but requires the user to run an `apt install`. If that's
inconvenient, option 3 still works — start with vision-based TOC
mapping (which I've already done partially), and choose
extraction approach later.

## Sources

- [zangak.am about](https://zangak.am/about_us.php?language=en)
- [learnarmenian.org/book-pdfs](https://www.learnarmenian.org/book-pdfs)
- [easternarmeniantextbook.com](https://easternarmeniantextbook.com/)
- [Acharyan vol Ա — academia.edu](https://www.academia.edu/4358000/)
- [Acharyan vol Բ — academia.edu](https://www.academia.edu/8255197/)
- [Acharyan vol Բ — archive.org](https://archive.org/details/Hrarm2)
- [Pan-Armenian Digital Library](https://arar.sci.am/)
- [YSU monographs (503 from sandbox)](https://monographs.ysu.am/index.php/ysuph/en)
- [YSU library](http://lib.ysu.am/index.html?lg=1)
- [YSU journals](https://journals.ysu.am/)
