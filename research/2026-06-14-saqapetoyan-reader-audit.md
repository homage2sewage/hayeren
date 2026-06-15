# Saqapetoyan parse — independent reader audit & the boldface fix (2026-06-14)

Context: after structurally parsing the Sakapetoyan neologism dictionary
(`saqapetoyan/parse_entries.py`, 614 entries), we ran an **independent,
page-parallel reader audit** to check the parse against the *rendered
book pages* (not the text layer the parser consumed — that would share
its blind spots).

## Method

- Rendered body pp. 9–76 to images (`pdftoppm -r 150`).
- 17 reader agents (4 pages each) via a Workflow. Each agent read the
  page **image** as a human would + the parsed records for those pages,
  and reported discrepancies through a structured schema. Framing:
  "do NOT assume the parser is right." Synthesis agent deduped/ranked.
- Page-overlap check: only 3 entries span a page boundary
  (`Արթրիտ` 14→15, `Էնդոսկոպ` 26→27, `Հոմոսեքսուալիզմ` 43→44); all fall
  inside a single agent's 4-page window, so no boundary entry was split
  across agents.

## Headline finding — the parser ignored the boldface layer

The audit flagged ~38/614 entries (~6%), dominated by **bold/regular
misclassification** (~28 entries) in both directions:

- bold coinage buried in `definition` (lost): `Ակցիոներ` (5 coinages → 2),
  `Աորտա`, `Բազա`, `Հիերարխիա`, `Սպիդոմետր`, `Սփիքեր`, …
- regular definition promoted to `native_coinages` (meaning lost):
  `Ֆուրգոն`, `Մոթել`, `Ֆեոդալ`, `Բուլյոն`, `Գերբ`, …

Root cause: the author distinguishes **coinage (bold)** from
**definition (regular)** by font weight, and the first parser instead
split on the `՝` mark / commas — which the book also uses *between*
coinages and as secondary commas. The delimiter heuristic was plausible
but wrong wherever weight and punctuation disagreed.

## Why the bold was invisible — and how we recovered it

The bold is **faux**: each bold glyph is drawn twice (fill + stroke
overprint). So:

- `get_text("dict")` / span `flags` report `Sylfaen flags=4` for the
  *entire* text — no bold bit anywhere. (This is why the original
  text-layer extraction, and the parser built on it, never saw it.)
- `page.get_texttrace()` exposes the stroke copy: a glyph is **bold iff
  a `type != 0` (stroked) render exists at its position**. We dedupe the
  doubled glyphs and emit a per-character bold mask aligned to clean text.

`parse_entries.py` was rewritten around this mask: bold Armenian runs →
`native_coinages`, regular Armenian runs → `definition`. Verified
directly against the rendered pages 9, 11, 17, 38, 42, 73, 76 — the mask
is ground truth.

## Other classes (verified)

- **Page-number contamination (64 entries):** the texttrace path let the
  page number (rendered as spaced digits, `"2 8"`) slip the `isdigit()`
  line filter and append to the last entry per page. Fixed (`[\d\s]+`).
- **Unbolded lone coinage (3):** `Կուլտուրա→Մշակույթ`, `Կապիտալիստ→Դրամատեր`
  — the typesetter genuinely did *not* bold these (the neighbouring entry
  IS bold). Reclassified with a `coinage-unbolded` flag.
- **Glyph-confusion findings (~7, e.g. շ/չ, բ/ք, պ/փ, dropped ու):**
  flagged by agents from the image; these need byte-vs-bitmap
  confirmation (could be agent vision misreads of confusable Armenian
  pairs) — tracked as a possible glyph-lint follow-up, not yet acted on.

## Outcome

After the rewrite: `coinage` 614/614, `definition` 313→327, **601/614
clean**, all residual warnings tied to genuine source quirks. Golden
anchors (`golden_entries.tsv`) extended with bold-signal cases
(`Ակցիոներ` all-bold, `Ֆուրգոն`, `Կոմիկ`, `Հիերարխիա`, `Ֆեոդալ`,
unbolded singles) so a regression that drops the bold extraction fails
`validate_entries.py`.

## Re-audit (same method, the 30 previously-flagged pages)

After the rewrite, 8 reader agents re-checked the 30 flagged pages.
**Findings dropped 38 → 16 (~58%)**, severity migrated from systematic to
incidental, verdict "coinage extraction is now reliable." Triage of the 16:

- **False positive (1):** `Ակցիոներ` — a re-audit agent claimed the first
  three coinages are regular-weight; checked the page bitmap directly and
  they are clearly **bold** (cf. neighbouring `Ամպլուա`, whose regular
  definition is visibly lighter). The mechanical texttrace mask was right.
  *Lesson: trust the texttrace stroke signal over vision for subtle bold.*
- **Real, fixed (1):** `Լահմաջուն` — `(արաբ. միս խմորի մեջ)` is an
  etymological note; `TAG_BLOCK_RE` had shredded it into domain tags. Now
  parenthetical tag-groups must be **abbreviation-only** (1 entry affected).
- **Known/flagged (2):** `Անտեննա`, `Ապրիորի` — per-sense Russian / the
  `/լատ./` tail; both already carry `interleaved-field`/`no-russian`.
- **Text-layer glyph artifacts (3):** `Բրոնխիտ` `բորբոքում→բորքոքում`
  (confirmed in the bytes — a real text-layer error, faithfully copied);
  `Հիդրոդինամիկա` `Ջրազորություն` (the agent's "correct" `Ջրագորություն`
  is a non-word — likely a vision misread, parsed value kept);
  `Ալտրուիստ` Cyrillic `а` in `altruist` (machine-detectable mixed script).
  These are source/extraction artifacts, NOT parser bugs.
- **Long-tail multi_sense glue (~6):** `Սկաուտ` gender tags, `Բյուջե`/
  `Բազա`/`Սպիդոմետր` per-sense fragment trimming — flagged `multi_sense`,
  `raw` preserved. Next fix target if needed.

Net: the dominant systematic class is gone; residual risk is concentrated
in multi-sense per-sense mapping and a handful of text-layer glyph typos.

## Reusable lesson

For a "clean Unicode text layer" PDF, **the text layer can still silently
drop typographic signal** (here, faux-bold via overprint). When a
distinction is carried by formatting, verify against the *rendered page*,
and reach for `get_texttrace()` (render mode / stroke) before concluding
the signal is unrecoverable. The independent image-based reader audit is
what surfaced it — a text-layer-only critic could not have.
