# Acquisition plan: closing the `հլը` gap (and similar colloquial particles)

**Date**: 2026-05-07
**Trigger**: explicit user Q&A test — "explain `հլը` and which forms
it takes." The corpus came up empty; the system honestly reported
"I don't know."
**Status**: gap identified, no acquisition yet started. This doc is
the plan.

## What the gap is

`հլը` /hələ/ is a high-frequency colloquial Yerevan particle meaning
roughly "still / yet / wait / first / let me first." Its variants
include `հլա`, `հըլը`, `հըլա`. It's not in our four-book corpus
(except as one undefined occurrence in ghamoyan p49's "distorted
TV-language" example list, where it appears as `հլա`). Wiktionary
also has no entry. The literary equivalent is `դեռ` "still / yet,"
but `հլը` carries colloquial-register signal *and* a wider pragmatic
range that `դեռ` doesn't fully capture.

This is the **first concrete lexicon-side gap** the project has
encountered. It exposes:

- Our prescriptive textbooks (sakayan, parnasyan, tioyan) deliberately
  omit colloquial particles.
- Our descriptive-colloquial source (ghamoyan) is research-oriented
  and surveys phenomena in classes (jargon, code-switching, etc.)
  rather than per-lexeme.
- Wiktionary's coverage of Armenian is patchy for non-literary items.

## Why fix this gap

1. **AI Q&A quality**: a user asking "what does հլը mean?" gets a
   correct but unsatisfying "I don't know." Filling this gap turns
   that into a citation-grounded answer.
2. **Pattern-validation**: `հլը` is *typical* of a class of
   colloquial particles (`թե`, `դե`, `բա`, `էլի`, `հենց`) that
   pervade real spoken Armenian. The acquisition method we develop
   for `հլը` will scale to ~30-50 such items.
3. **Lexicon-layer kickoff**: the current `topics/` tree is
   phenomenon-oriented; particles like `հլը` are lexeme-oriented
   and want a `lexicon/<lemma>.md` home. This is the trigger to
   start building that.

## Acquisition options, ranked

### Option 1 (recommended): Acharyan's *Armenian Etymological Dictionary*

`Հայերեն արմատական բառարան` by Հր. Աճառյան (Hr. Acharyan), 6 volumes
(1926-1935). Free PDF on Internet Archive, Pan-Armenian Digital
Library, and Academia.edu. Each volume covers a letter-range:

| volume | range | likely contains `հլը` |
|--------|-------|----------------------|
| Ա (Ա-Դ) | A-D | no |
| Բ (Ե-Կ) | Ye-K | no |
| Գ (Հ-Չ) | H-Ch | **yes** (հ-, հլ-) |
| Դ (Պ-Ֆ) | P-F | no |

**Action**: download volume Գ from archive.org (likely
archive.org/details/Hrarm3 by analogy with Hrarm1, Hrarm2, Hrarm4).
Search for the lemma. Acharyan typically gives:
- The headword + dialectal variants
- Etymology (with reconstructed PIE / Iranian / Turkic source)
- Cognates in related languages
- Sample attestations from Classical and Modern Armenian texts

**Pros**: free; canonical; etymology + cognates that make sense of
Turkic-loan particles like հլը.
**Cons**: dense scholarly Armenian; OCR may be imperfect on a 1930s
print; no usage examples from contemporary Yerevan speech.

### Option 2: EANC (Eastern Armenian National Corpus)

`eanc.net` — academic corpus, ~110M tokens, includes a colloquial
sub-corpus with TV/radio transcripts and online forum posts.

**Action**: web interface only (no API). Manually search for `հլը` /
`հլա` / variants. Produce a frequency count + a sample of
context-windows. Convert to a `lexicon/hələ.md` entry citing N
real-world usages.

**Pros**: contemporary; quantitative; shows actual usage patterns
across syntactic positions and registers.
**Cons**: scraping required (no API); the colloquial subcorpus may
be smaller; results need human filtering.

### Option 3: native-speaker query

Ask a native Armenian speaker (ideally Yerevan-resident, native
colloquial) to define `հլը` and provide example sentences in 2-3
distinct uses. Document with permission.

**Pros**: fastest; gives exactly the modern colloquial coverage no
book has; can probe specific contexts.
**Cons**: not reproducible; needs ethical handling
(permission/anonymisation if quoted in a public-bound workspace);
single-source (one informant).

### Option 4: Wiktionary's `հենց` / `դեռ` discussion pages + community wikis

Some Armenian-learner communities maintain dictionaries with
colloquial coverage (e.g., bararan.am, hayoclezvi.com). Could provide
quick pointers but won't be citation-grade for this project's
schema.

**Pros**: free, contemporary.
**Cons**: not stable enough as a citation source; quality varies.

## Recommended approach

**Combine 1 + 2** for the lexicon-layer kickoff:

1. **Acharyan (Option 1)** for the etymology and historical attestation.
2. **EANC (Option 2)** for current usage frequency and contemporary
   examples.
3. Resort to **Option 3 (native speaker)** only if 1+2 leave
   ambiguity on a specific usage.

## What the lexicon entry would look like

The first lexicon entry kicks off `lexicon/` as a new artefact type.
Schema sketch (extending the current topic frontmatter):

```yaml
---
lemma: հլը
ipa: /hələ/
variants: [հլա, հըլը, հըլա]
register: yerevan-colloquial
literary-equivalents: [դեռ "still", առաջ "first"]
loan-stratum: turkic           # if Acharyan confirms
pos: particle / adverb
domain: discourse-particle
attestation: multi-attested    # once 2+ sources cited
sources:
  - id: 1
    book: acharyan-vol-3
    page: ...
    verbatim_quote: [...]
    supports: supported
    note: etymology + cognates
  - id: 2
    book: ghamoyan
    page: 49
    y_range: [355, 380]
    verbatim_quote: ["հլա"]
    supports: partially-supported
    note: undefined mention in TV-language list
  - id: 3
    book: eanc-search
    query: հլը
    date-fetched: 2026-XX-XX
    sample-frequency: ~N hits in colloquial subcorpus
    representative-examples: [...]
    supports: supported
    note: usage examples
gaps: [...]
---

# հլը /hələ/ — colloquial particle "still / yet / wait"

[body: definition, forms, syntactic positions, examples in context,
contrast with literary դեռ, register notes...]
```

The schema additions for lexicon (vs topic):

- `lemma`, `ipa`, `variants`, `pos`, `loan-stratum`,
  `literary-equivalents` — lexeme-specific fields.
- `book: acharyan-vol-3` — needs the book itself extracted; would
  follow same pipeline as parnasyan/tioyan (OCR if scan,
  text-extract if PDF).
- `book: eanc-search` — a *non-book* citation source. Schema
  extension: allow citation sources that are search-result
  snapshots rather than book-page+y_range.

## Schema decisions to make

1. **`lexicon/` directory layout**: flat (`lexicon/hələ.md`) or
   nested by domain (`lexicon/discourse-particles/hələ.md`)?
   Recommend flat — most lemmas are searched by name, not by
   category.
2. **Naming**: `lexicon/հլը.md` (Armenian script) or `lexicon/hl.md`
   (transliterated)? Recommend Armenian-script for fidelity, even
   though some filesystems are awkward with non-ASCII.
3. **Citation source for EANC**: the script extension to support
   `book: eanc-search` requires a different `citation-check`
   verification path (fetch the search result, compare). Out of
   scope for v1; for now, `attestation: partially-supported` with
   a plain URL note.
4. **Acharyan extraction**: yes/no? Given 6 volumes × ~700pp = ~4200
   pp of dense scholarly Armenian, an extraction would be
   substantial work. **Recommend**: don't extract the whole
   dictionary; manually look up specific lemmas as needed,
   capturing the relevant page snippet per lookup. Iterate.
5. **Plan-mode walks**: the lexicon entry workflow can mirror the
   topic walks but with a per-lemma cadence rather than per-topic.

## Out of scope for this acquisition plan

- Full EANC scraping infrastructure (web interface only; no API
  forces manual or semi-manual flow).
- Acquiring the full Acharyan dictionary as a fifth corpus book
  (deferred; per-lookup is sufficient for now).
- Per-particle lexicon entries beyond `հլը` (the next 5-10 will
  follow the same pattern: `դե`, `բա`, `էլի`, `թե` etc.).
- Schema extension to formally support `book: <external-source>`
  with non-page-y_range citations — defer until 2-3 lexicon entries
  shake out the requirements.

## Suggested next move

Pick one of:

**A. Quick demo path** (~30 min): hit archive.org for Acharyan
volume Գ; manually find `հլը` / related; capture page image; write
`lexicon/հլը.md` v1 citing Acharyan + ghamoyan p49. This validates
the lexicon flow with one lemma. Schema extensions (EANC etc.)
deferred until lemma #2 or #3 needs them.

**B. Defer until next session**: keep `հլը` as a documented gap;
move on to the other queued discovery-walk topics
(`auxiliary_e` already done, but the case-system question still
open).

Recommended: **A** for end-to-end validation that the lexicon layer
is feasible. The first lexicon entry is the high-uncertainty step;
subsequent ones become routine.

## Sources

- Acharyan vol Ա: https://archive.org/details/Hrarm1
- Acharyan vol Բ: https://archive.org/details/Hrarm2
- Acharyan vol Դ: https://archive.org/details/Hrarm4
- (vol Գ — the relevant one for հ — same pattern, search archive.org)
- Pan-Armenian Digital Library: https://arar.sci.am/
- EANC: https://eanc.net
- Earlier discussion in `transliteration-notes.md`,
  `ghamoyan/README.md` Topic 0.
