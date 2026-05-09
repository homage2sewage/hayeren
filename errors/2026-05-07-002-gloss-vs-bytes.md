---
id: 2026-05-07-002
date: 2026-05-07
caught_by: citation-check
caught_during: validation
severity: major
disposition: human-error-with-llm-confirmation
category: representation-bias
subcategory: gloss-vs-extracted-bytes
phenomenon: sakayan-armtrans-aspiration-mark
related_topics:
  - topics/phonology/voiced_aspirated_alternation.md
related_pitfalls:
  - kb-design.md
status: mitigated
mitigation:
  type: doc-update
  ref: kb-design.md
recurrence: pattern-of-3
---

## Input

Author writing the first topic file (`voiced_aspirated_alternation.md`)
populated `verbatim_quote:` fields with the linguistic-IPA gloss
form `[§ntʰunel]` for sakayan's transliteration of `ընդունել`.

## What the LLM produced

Topic frontmatter:

```yaml
verbatim_quote: "[§ntʰunel]"
```

Author (and LLM-as-collaborator) believed this was the literal
content of the cited transliteration — the way it would appear
in the JSONL extraction.

## What was correct

The actual JSONL bytes for the same span are split across two
separate Armtrans spans, with the aspiration rendered as glyph
layout (font F19 stacking `Œ` and `h`) rather than as a Unicode
codepoint:

```yaml
verbatim_quote:
  - "[§nt"
  - "unel]"
```

There is no `ʰ` (Unicode U+02B0 modifier-letter-small-h) in the
JSONL. The aspiration mark is positional / font-rendered, not
encoded.

## Why this happened

LLMs default to writing transliterations in their canonical
linguistic form (with proper IPA modifiers and joined tokens)
because that's what training corpora overwhelmingly contain.
The actual extraction artefact has different invariants: span
boundaries from the PDF's text-fragment layout, no IPA
codepoints, font-rendering implicit.

The author and the drafting LLM both assumed "verbatim quote =
gloss as I'd write it" rather than "verbatim quote = bytes
present in the JSONL." Same invariant violation either way.

`citation-check`'s grep-against-JSONL refused both fragments on
first invocation. The verifier had a more rigid model of "what
verbatim means" than the human or the LLM did.

## Mitigation

Documented in `kb-design.md` § "Topic frontmatter schema" as
the cardinal rule: **verbatim_quote fragments must be literal
JSONL bytes, not linguistic glosses**. The fragment-list form
of `verbatim_quote` (multiple shorter strings) was added to
the schema specifically to handle span-boundary cases like
this.

`citation-check` itself enforces the rule mechanically —
nothing can land in `topics/` without grep-matching the JSONL.

## Test case

Input: a verbatim_quote that uses canonical linguistic form
(IPA, joined tokens) for a span that's actually split across
multiple JSONL records with non-Unicode aspiration / diacritics.

Expected behaviour: `citation-check` exits non-zero with a
`fragment not found` finding pointing to the JSONL location.

Failure mode (before mitigation): topic file lands with
unverifiable quotes; subsequent LLM passes treat the gloss
form as authoritative; downstream regenerations propagate the
error.

## Notes

This is classified as `human-error-with-llm-confirmation`, not
pure `llm-error`. The human author chose the gloss form; the
collaborating LLM agreed without challenging. Logged here
because the failure mode is identical from a process standpoint
(verbatim invariant violated; mechanical verifier was the
catch) regardless of which agent introduced the gloss.
