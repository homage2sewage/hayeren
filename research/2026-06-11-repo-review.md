# 2026-06-11 — Full-repo critical review (agent-conducted)

Five parallel review agents swept the workspace (interaction
machinery, deck pipeline, KB/citation layer, extraction pipelines,
process/meta layer), followed by operator Q&A that corrected two
framings. This file stores the findings and the enhancement plan.
Implementation status of the "immediate" items is tracked at the
bottom.

## What this workspace is

Two entangled projects, deliberately:

1. **Learning Eastern Armenian** (Yerevan-colloquial orientation):
   the deck (~1100 cards), the topic graph (34 topics), song
   translations, six OCR'd source books.
2. **A methodology for reliable LLM-assisted knowledge work**, with
   Armenian as the testbed — chosen partly because the LLM prior is
   confidently wrong there often enough to generate failure data.
   The comparative-medium book choice (sakayan = English-medium,
   parnasyan/tioyan = Russian-medium) is itself methodology: the
   LLM's EN/RU priors are strong, its Armenian prior weak, so the
   same lemma glossed independently in two strong-prior languages
   permits triangulation.

The interaction architecture is a pincer around every
Armenian-content exchange: pre-emit grounding
(`armenian_autoground.py` injects a `query_kb.py` bundle) and
post-emit verification (`armenian_self_check.py` Stop hook), with
skills as on-demand verifiers and `CLAUDE.md` doctrine as prose
backstop.

## Headline finding

**The post-emit Stop hook had a 0% effective activation rate from
installation (2026-05-26) to this review.** It guessed at payload
keys (`response`, `message`, …) that Claude Code's Stop event does
not carry; the response lives in the transcript file at
`transcript_path`, which the hook never read. Every production
firing extracted an empty string and skipped. The lone logged
`block` was an install-day smoke test against a hand-invented
payload. The measurement log (`.claude/logs/armenian_self_check.jsonl`)
flat-lined at `response_chars: 0` for 38 consecutive real events and
was committed unexamined for 16 days.

This is the repo's own canonical failure mode — plausible rule ships
without confronting its real input population — applied to the
machinery built to prevent it. The challenge protocol was enforced
for linguistic heuristics and exempted for infrastructure.

## Findings by layer

### Corpus / extraction

- `sakayan/out/full.jsonl` stale vs. `fonts.py`: re-running the
  current font table changes 1,442 records (undecoded spans in the
  corpus); ~13.5k further spans sit in Barz-encoded fonts absent
  from `FONT_MAPS` (`F2–F41`, `Nork-*`), invisible to
  `--show-unmapped` (it only audits fonts already mapped).
- `ghamoyan/armscii.py` mis-decoded both guillemets: empirically
  0xA7=«, 0xA6=» (516/515, perfectly paired), table had `-`/`,`.
  Every quoted term decoded as `-Մունետիկ,` for «Մունետիկ».
  Backtick 0x60 (641×) is the բութ `՝`; 0xB0/0xB1 (5×) are `՛`/`՞`.
- `acharyan/extract.py`: page tracker jams permanently at vol3 p406
  (latter half of vol3 mis-cited); headword regex splits on
  bibliographic abbreviations (ՆՀԲ ×2,228 …) — ~38% of "entries"
  are fragments.
- Schema fragmentation: `query_kb.py` hard-codes four books;
  acharyan/gharagyulyan are invisible to the grounding layer.

### KB / citation layer

- 32/34 topics pass `citation-check` at 100% (542/542 fragments);
  2 files crash the tools (`dialectal_lnel.md` on `y_range: null`,
  `known_transcriptions.md` no frontmatter).
- The byte-presence check is gameable: no window-width cap (real
  topics already cite near-whole-page windows), no minimum fragment
  length (33/139 sources have fragments ≤4 chars), no word
  boundaries (demonstrated: `ցրել` "verifies" inside
  `ներկայացրել` on the wrong page).
- The meaning layer is never checked: `supports:` is self-graded
  (130 supported / 8 partial / 0 unsupported — the signature of
  self-assessment); `attestation: multi-attested` is hand-declared
  and `aorist.md` carries it falsely (cites only sakayan).
- Confabulation next to verified anchors: `yerevan_slang.md` `բոց ա`
  glossed "cool/amazing" where ghamoyan says "unusual, strange,
  original"; `aorist.md` asserts Russian past tense has person
  endings (it doesn't).

### Deck pipeline

- Seven live wrong-sense cards, all in the documented homograph-trap
  shape, all `info`-severity or structurally invisible: `կար`
  ("seam" → should lead "there was"), `գետ` ("knowing" → "river"),
  `ևս` (sense 2 "also" is correct), `պարոն` ("baron" → "mister"),
  `ուստի` ("whence" → "therefore"), `անց` ("passage" → clock-time
  "past"), `ակ` (morpheme/hyphenation noise, e.g. `մի-ակ`
  line-splits → skip).
- `golden_glosses.tsv` corrupted: 5 Russian alternates orphaned onto
  their own lines, 3 duplicate keys silently shadowing; `load_golden`
  is the one loader with no malformed-input guard.
- `query_kb.py` produces false Gaps: `lemmatize(…, None, …)`
  disables the known-lemma check, so e.g. `կարդում → կարդել`
  (non-word), grep misses, bundle declares a Gap while sakayan has
  288 `կարդա*` hits. It also never greps the surface token. This
  bundle is hook-injected as ground truth.
- `_fmt_english` rejoin inserts a stray space before punctuation
  after parentheticals (10 rows).
- The `info`-severity review fodder was never reviewed: nothing
  enforces it, the rows have no triage delta, and the severity
  gradient promotes only rank ≤50 while dictionary-sourced cards
  live at ranks 297–604.

### Skills / docs (staleness is systemic)

- `answer-q/verify_citations.py` verifies path/page name-dropping,
  not quoted text; `missed-citation` documented but unimplemented.
- `deck-editorial-pass` stale vs. the 2026-06-03 HTML deck format
  (`rank-NNNN` tag extraction, unproducible output schema, broken
  documented invocation).
- Stale counts everywhere (README "9 errors"/16, "27 topics"/34);
  `kb-design.md` references nonexistent `topics/INDEX.md`;
  `songs/README.md` says "Six steps:" then lists seven; error
  2026-05-11-001 still `open` though its artifact exists.
- `#nogrep`/`#nocheck` were substring checks, not the documented
  prefix; the block message advertised its own bypass token.

### What is genuinely good

`citation-check` does real byte-level verification; the autoground
hook works; the error log functions as a teacher (pattern-family
roll-ups); songs provenance discipline is real (the 2026-06-01
whole-song audit caught six fabricated citations); deferred-phase
roadmaps carry explicit decision triggers. Every guard that exists
traces to a logged failure.

## Operator corrections from the review Q&A

1. **Observability, not perception.** The guillemet corruption was
   not a human miss: the decoded corpus has no human-facing surface;
   its only readers are LLMs, who normalize punctuation noise. The
   blame is on the pipeline, and the fix must be mechanical
   (flanking-pair statistics in extractor self-checks), because no
   reader will ever be in the frame where punctuation is the object
   of attention.
2. **The pattern was inferable without the bitmap.** Paired flanking
   marks (516/515, opener-before / closer-after) are obviously
   quotes to anyone inspecting the output *as an artifact*. The
   editorial-frame pass (`llm-workflow.md` §10) was applied to decks
   and topics but never to the extraction layer.
3. **`կար` mechanism** (worked example of two sound rules composing
   wrong): kaikki has both entries; the verb entry is a form-of
   gloss ("3sg imperfect of կամ") which the inflected-leak hygiene
   rightly suppresses elsewhere; that left the noun entry, where
   kaikki-natural-order took sense 1 "seam" — "sewing" was sense 2,
   one slot away. English Wiktionary orders senses
   concrete/etymological-first, not by Armenian frequency.
   Operator field knowledge: `կար ու ձև` = tailoring (not
   corpus-attested; user-supplied, deck-gloss eligible).
4. **Cross-language triangulation is intended methodology** but the
   pipeline's Russian layer (`russian_glosses.tsv`) is a translation
   of the English gloss — zero independence; it would confirm
   "seam" as «шов». The independent Russian anchors are the
   RU-medium corpora (parnasyan/tioyan vocab glosses). A
   cross-language sense-consistency check is the mechanizable form.

## Enhancement plan

### Immediate (this session — implemented, see status below)

1. **Stop hook repair**: read the response from `transcript_path`;
   skip when the draft already carries citations (topic path or
   `book pNN`), block once otherwise; stop advertising `#nocheck`;
   `#nogrep` becomes a true prefix check; autoground gets its own
   log (`.claude/logs/armenian_autoground.jsonl`); fixture-replay
   test with a real-shaped payload.
2. **ghamoyan decoder fix + re-extraction**: 0xA7→«, 0xA6→»,
   0x60→՝, 0xB0→՛, 0xB1→՞; guillemet-pairing self-check; re-run
   `citation-check` across all topics and repair any
   `verbatim_quote` fragments that embedded the old artifacts.
3. **Deck fixes**: HAND_OVERRIDES for կար/գետ/ևս/պարոն/ուստի/անց,
   SKIP for ակ, golden anchors for each (two-step rule); repair
   `golden_glosses.tsv` orphans/duplicates; add `load_golden`
   malformed-row + duplicate-key guards; fix `_fmt_english`
   spacing; rebuild + validate.
4. **query_kb fixes**: pass real known-lemma set to `lemmatize`,
   grep surface token in addition to lemma; verify the `կարդում`
   false-Gap case is fixed.
5. **citation-check hardening**: graceful handling of
   `y_range: null`; warnings for short fragments and
   page-spanning windows.

### Deferred (next waves, with triggers)

- **sakayan re-extraction** after deriving maps for the unmapped
  Barz fonts (F2–F41, Nork-*, DallakTimeItalic) — hours of
  empirical mapping work; do before the next topic wave that cites
  sakayan beyond the textbook body.
- **acharyan rework** (page-tracker forward resync, abbreviation-
  aware headword regex) — before acharyan joins `query_kb.py`'s
  book list.
- **Stop hook tier-1 redesign** — **SHIPPED 2026-06-13.** Cited
  drafts are no longer trusted: each `<book> pN` cite + same-line
  quoted Armenian fragment is byte-verified (whitespace-insensitive
  NFC) against sakayan/ghamoyan, blocking on the specific
  unsupported `fragment@book pN`. Rationale in
  `research/2026-06-13-answer-verification-architecture-fit.md`;
  CLAUDE.md § "same check on the response side" documents behaviour.
  *Still deferred:* the uncited-characterization arm (flag
  confident source/Armenian characterizations with no citation —
  the F1/"manual" class) — judged LLM-hard/false-positive-prone,
  wants a design pass not a regex.
- **Cross-language sense-consistency check**: for each
  `src-dictionary` card, compare the kaikki-EN sense against the
  RU-medium corpus gloss where present; disagreement promotes
  `info` → flag. Extends the homograph drill.
- **Ambiguity triage gate**: persist acknowledged
  `ambiguous-sense` rows (`ambiguous_triage.tsv`); validator fails
  on unacknowledged *new* rows. Converts "inspect" into
  "acknowledge or fix".
- **Staleness lint** (`doc-sync`): generated stats blocks in
  README/kb-design; lint that every path mentioned in `*.md`
  exists and every documented CLI line parses; error `status:`
  cross-checked against named artifacts; wire into `push.sh`
  emitting `STALENESS.md`. Principle: generated > checked > prose.
- **`verify_citations.py` rewrite** to check quoted text, not
  path name-dropping; implement `missed-citation`.
- **`deck-editorial-pass` refresh** for the HTML deck format
  (rank from `deck_meta.tsv` sidecar).
- **`our_top_1000.tsv` artifact lemmas**: the rank list itself was
  generated with the same `known_lemmas=None` lemmatiser bug and
  contains manufactured lemmas (`կարդել` rank 210, `խաղել`,
  `զգել`, …). `query_kb.py` now guards against them (poison-guard
  in `load_known_lemmas`), but the list should be regenerated on
  the next deliberate rank rebuild — not casually (rank churn
  touches every card).

## Implementation status (2026-06-11) — all five immediate items landed

All changes in working tree only (nothing committed). Each item
verified after implementation; final cross-workstream integration
pass re-ran the hook tests, deck validator, citation-check, and
the false-Gap query together.

1. **Hooks** (`.claude/hooks/`): `armenian_self_check.py` now reads
   the draft from `transcript_path` (groups transcript lines by
   `message.id`, last assistant message, sidechain-aware); cited
   drafts pass through as `skip-cited`; `#nocheck` no longer
   advertised in the block message; all skip reasons logged
   distinctly. `armenian_autoground.py`: `#nogrep` is prefix-only,
   cap raised to 8000 chars, full JSONL logging to
   `armenian_autoground.jsonl`. New fixture-replay suite
   `.claude/hooks/test_hooks.py` (47 checks, built against the
   real transcript schema; runs with a log-dir env override so it
   never pollutes the real logs) — all green. Live smoke test
   against a real transcript: extraction now sees real text
   (was 0 chars on all 38 production firings). CLAUDE.md hook
   paragraphs updated to match.
2. **ghamoyan decoder** (`armscii.py`, `extract.py`): 0xA7→«,
   0xA6→», 0x60→՝, 0xB0→՛, 0xB1→՞; re-extracted (1,175 records
   changed; char-level diff is exactly the five expected classes:
   ՝×639, «×516, »×515, ՛×3, ՞×2; zero other changes). New
   `self_check()` in extract.py: guillemet-pairing balance
   (517/516 ✓) + undecoded-codepoint census. Citation re-audit
   across all topics: 542/542 fragments still verify against the
   new corpus (no topic had embedded the old artifacts); zero
   `,,` sequences remain.
3. **Deck** (`build_deck.py`, `validate_deck.py`,
   `golden_glosses.tsv`, `cards/top_1000.tsv`): six HAND_OVERRIDES
   (կար "there was…; sewing (կար ու ձև — tailoring)", գետ, ևս,
   պարոն, ուստի, անց) + ակ → SKIP_LEMMAS with `MORPHEME_NOISE`
   absence guard; `_fmt_english` no longer inserts a space before
   punctuation (10 rows fixed); golden file repaired (5 orphaned
   Russian alternates rejoined, 3 duplicate keys merged) + 6 new
   anchors; new `check_golden_file` validator check (errors on
   non-Armenian keys / duplicates / empty rows — fired 8 on the
   pre-fix file, 0 after). Validator: 1097 rows, 0 errors;
   `բրինձ` "rice" drained in to replace ակ.
4. **query_kb.py**: real known-lemma set passed to `lemmatize`
   (dict headwords + top-1000 lemmas, with a poison-guard against
   the artifact lemmas the old bug wrote into `our_top_1000.tsv`);
   greps surface token AND lemma, Gaps only when both miss.
   `"Նա կարդում էր գիրքը"` now lemmatizes կարդում→կարդալ and
   reports zero gaps (was: false Gap on the manufactured `կարդել`
   while sakayan held 288 hits). Runtime ~0.8s.
5. **citation-check/check.py**: `y_range: null` → page-wide check
   with WARN instead of traceback; missing frontmatter → clean
   error, exit 2; WARNs for short fragments (<4 Armenian letters
   and <8 total) and windows covering >60% of a page's span
   y-extent (unit-agnostic); missing-book sources (web cites) →
   SKIP rows. yerevan_slang 25/25 OK; dialectal_lnel no longer
   crashes.
