# songs/ — lyric translation & analysis

Worked translations of Armenian songs (esp. hip-hop / rap, where
slang density and wordplay defeat naive machine translation). Each
song gets one dated-or-slugged Markdown file holding **both** the
final translation **and** the provenance of every meaning — so a
later reader (human or LLM) can see *how* each gloss was obtained,
not just the result.

## Why a separate folder

Songs aren't textbook prose. They carry:
- heavy **Yerevan slang** and Russian code-switching,
- **colloquial phonetic spelling** (`թո` for `թող`, `շատէ` for
  `շատ ենք`, `ճամփեք` for `ճամփաներ`),
- **wordplay / double meaning** that only resolves with cultural
  context,
- **transcription uncertainty** (lyrics often come from a lyric
  video or a crowd-sourced site like Musixmatch, not an
  authoritative print source).

This means a song file is a *provenance document*, not just a
gloss table. The grounding discipline from `CLAUDE.md` § "Before
answering an Armenian-language question" applies in full, but the
output shape is different — hence this folder + routine.

## The routine (per song)

Same discipline as the topic graph: ground first, grade
confidence, name gaps. Six steps:

1. **Acquire & attribute the text.** Record where the lyrics came
   from (lyric video URL, Musixmatch, etc.) and flag that it's a
   *transcription* — not authoritative. Note any lines you're
   unsure are transcribed correctly.
2. **Normalize the colloquial spelling.** For each section, give
   the as-sung line and a bracketed standard-Armenian
   normalization so the grammar is visible (`Թո` → `թող`, `անցե`
   → `անցել`, elided copulas restored: `Շանսերը շատ [են]`).
3. **KB-ground the lexicon.** Run
   `python3 frequency/query_kb.py "<armenian line>"`, then
   targeted `grep` of `ghamoyan/out/full.jsonl` and
   `topics/lexicon/*` for each slang item. Attach a citation
   (book + page) to every slang gloss you can; mark the rest as
   **prior** (pre-training guess), never as fact.
4. **Translate per line, graded.** Two renderings per section: a
   **literal** line-by-line table with a **confidence** column
   (high / med / low), and a **register-aware** rendering that
   keeps the flow. Flag wordplay / double meanings explicitly.
5. **Verify at granularity.** Spawn separate critic agents (per
   verse, or per low-confidence line) framed *"is this meaning
   correct? where would this gloss be wrong?"* — the critic-agent
   pattern from `CLAUDE.md`, applied to meaning rather than to a
   heuristic. Reconcile their findings into the file.
6. **Record provenance.** Every non-obvious gloss carries a note:
   cited (book+page) / prior / disputed-and-resolved. The
   "Methodology & provenance" section of the song file states how
   the meaning was obtained overall.
7. **Whole-song pass (over the assembled file).** Section-by-
   section review cannot catch whole-file problems. After the file
   is assembled, run a pass over the *whole document* — ideally
   multi-agent with three framings:
   - **citation re-audit** — `grep` every cited page against the
     corpus and confirm it says what the file claims. This is the
     song-domain analogue of the `citation-check` skill and is
     **mandatory**: drafting agents reliably fabricate
     plausible-but-wrong citations (the repo's canonical failure
     mode). The 2026-06-01 *Myus Angam* pass caught six.
   - **structural/consistency** — recurring forms glossed the same
     way everywhere; reconciliation edits applied in *all* the
     places they touch (table cell, wordplay note, register
     rendering); no stale notes contradicting an applied fix.
   - **editorial (learner POV)** — coherent meaning arc, a
     synopsis up top, consistent register across renderings,
     low-confidence honestly surfaced in the blockquotes a
     skim-reader will actually read.

## File format

Frontmatter (artists, title, source URLs, date, status) + then:

- **Methodology & provenance** — how the text + meanings were
  obtained; transcription caveats; what's cited vs. prior.
- **Per section** (chorus / verse N): as-sung text, normalized
  text, line-by-line graded table, slang glossary with citations,
  wordplay notes, register-aware rendering.
- **Open questions / gaps** — unresolved lines, low-confidence
  glosses, things needing audio or a native check.
- **Verification log** — what the critic agents checked and
  changed.

## Confidence vocabulary

- **high** — grammar/lexicon corpus-grounded or transparent
  standard Armenian.
- **med** — gist stable, exact phrasing or one lexeme uncertain.
- **low** — meaning is a reconstruction; flag the specific
  unknown (untranscribable form, un-attested slang, ambiguous
  segmentation).

## Index

- `dav-vnas-myus-angam.md` — Dav feat. Vnas, *Մյուս անգամ /
  Myus Angam*.
- `brunette-8-sutasan.md` — Brunette, *8 SUTASAN / Սուտասան*
  (chorus only; `status: partial` — verses not yet acquired).
