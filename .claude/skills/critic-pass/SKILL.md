---
name: critic-pass
description: |
  Pre-merge gate for topic files. Combines mechanical structural lint
  (frontmatter schema, [#N] references, attestation consistency) with
  citation verification, plus an editorial rubric the agent applies
  qualitatively. Run before promoting a topic from `status: draft` to
  `reviewed`.
---

# critic-pass

Three-phase critic gate for topic files: mechanical structural lint,
mechanical citation verification, and an agent-side editorial rubric.

## When to invoke

- Before promoting a topic from `status: draft` to `reviewed`.
- After any non-trivial topic edit.
- Before merging a `walks/` plan-file's proposed changes into `topics/`.
- Periodically across the whole `topics/` tree to detect drift.

## Phase 1 — Structural lint (mechanical)

```sh
sakayan/.venv/bin/python .claude/skills/critic-pass/lint.py \
    topics/<domain>/<phenomenon>.md
```

Multiple files are accepted; pass `topics/**/*.md` to lint everything.
`--json` emits machine-readable output for chaining.

Checks performed:

- All required frontmatter fields are present (`topic`, `domain`,
  `status`, `attestation`, `sources`).
- Field values are in valid enums (`status` ∈ {draft, reviewed,
  stable}; `attestation` ∈ {single-source, multi-attested,
  conflicting}; `supports` ∈ {supported, partially-supported,
  unsupported, uncertain}).
- `domain` is a known linguistic domain (phonology, morphology,
  syntax, semantics, pragmatics, lexicon, pedagogy).
- Each source has all required fields (`id`, `book`, `page`,
  `y_range`, `verbatim_quote`, `supports`, `note`).
- Source `id`s are unique within the file.
- `y_range` is a `[lo, hi]` pair with `lo < hi`.
- Every body `[#N]` reference resolves to an existing source id.
- Sources referenced in the body (info-level if not).
- Attestation is consistent with source distribution
  (`multi-attested` requires ≥2 distinct books; `single-source`
  expects exactly 1).
- `gaps:` is non-empty (info-level if absent — every topic should
  have at least one open question).

Exit 0 iff no errors. Warnings and info-level findings don't fail.

## Phase 2 — Citation verification (mechanical)

```sh
sakayan/.venv/bin/python .claude/skills/citation-check/check.py \
    topics/<domain>/<phenomenon>.md
```

See `.claude/skills/citation-check/SKILL.md` for details.

## Phase 3 — Editorial rubric (agent applies)

After phases 1 and 2 pass, read the topic file and apply this
checklist:

1. **Body claim provenance.** Every substantive claim in the prose is
   either cited via `[#N]` or sits inside a clearly-labelled section
   ("Contrastive notes", "Pedagogical notes", "Open questions /
   gaps") that signals it's commentary, not a book-grounded claim.
2. **Examples carry script + translit + gloss.** Armenian examples
   in the prose are presented with at least the script and an English
   gloss. Transliteration is included where it disambiguates
   pronunciation (especially for words involving the
   voiced↔aspirated alternation).
3. **Gaps are specific and actionable.** Each gap names what's missing
   and, where possible, which source might fill it (e.g. "check
   `ghamoyan/` for colloquial register," "Dum-Tragut may treat this
   directly"). Avoid generic gaps like "more research needed."
4. **Cross-references resolve.** Any `topics/<domain>/<phenomenon>.md`
   reference should either exist on disk or be marked `(TODO)`.
5. **Attestation honestly stated.** If only one book is cited,
   `attestation: single-source` is required — don't pre-claim
   `multi-attested` for sources you mean to add later. `conflicting`
   means books actually disagree on the claim — that should be
   visible in the body, with the conflict explicit.
6. **No vibes-based claims.** Anything the LLM "knows" but isn't in
   the citation set is either flagged in `gaps:` for verification
   against a future source, or moved into a Pedagogical/Contrastive
   section that signals it isn't book-grounded.
7. **Contrastive notes match the L1 baselines.** Both English-L1 and
   Russian-L1 framings should be present (or one with a justified
   absence). Russian-L1 framings should align with `grammar-terms.md`'s
   Armenian/Russian mapping where relevant.
8. **Prose arc is consistent.** Topics roughly follow:
   *phenomenon → evidence → what it isn't (where applicable) →
   contrastive notes → gaps.* Deviations are fine but should be
   deliberate.

## Composition

Phases 1+2 are mechanical and idempotent — re-running them on the
same files is cheap. Phase 3 is the agent's editorial pass; record
findings either by extending `gaps:`, by fixing the prose, or by
opening a `walks/` plan file when the edit is large enough to want a
checkpoint. Re-run phases 1+2 if the edit touched frontmatter.

## Promotion gate

Before promoting `status: draft` → `reviewed`:

- Phase 1: 0 errors. Warnings reviewed and either fixed or justified.
- Phase 2: every fragment verifies (exit 0).
- Phase 3: rubric items 1–8 satisfied or explicitly waived in the
  topic's `gaps:`.

`reviewed` → `stable` is a higher bar: requires `attestation:
multi-attested` (at least one corroborating book) and explicit
sign-off in the change log of `kb-design.md`.
