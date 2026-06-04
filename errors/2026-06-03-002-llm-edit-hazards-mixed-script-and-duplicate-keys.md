---
id: 2026-06-03-002
date: 2026-06-03
caught_by: user
caught_during: review
severity: minor
disposition: llm-error
category: script-and-source-hygiene
subcategory: cyrillic-armenian-mixing-and-silently-shadowed-dict-keys
phenomenon: llm-authored-gloss-and-override-edits-introduce-invisible-defects
related_pitfalls:
  - errors/2026-06-03-001-deck-homograph-trap-rare-sense-glosses.md
  - errors/2026-05-14-002-spurious-morpheme-decomposition-on-borrowed-toponym.md
status: mitigated
mitigation:
  type: rule-and-check
  ref: frequency/validate_deck.py
recurrence: pattern-of-N
---

## Input

While hand-editing `HAND_OVERRIDES` in `build_deck.py` to fix glosses,
the model (me) introduced two classes of defect that no existing check
caught. The user spotted the first ("էл error: mixing cyrillics and
armenian").

## What the LLM produced

1. **Mixed-script token.** The `ալ` gloss was written
   `… = էл) …` where the `լ` was **Cyrillic `л` (U+043B)**, not
   Armenian `լ` (U+056C) — a single token mixing scripts, visually
   identical, invisible in review. `check_script_purity` only scanned
   the *lemma* column, so a Cyrillic letter inside a *gloss* sailed
   through.
2. **Silently-shadowed duplicate keys.** Four `HAND_OVERRIDES` keys
   were duplicated across editing sessions (`դուր`, `հենց`, `ինչպես`,
   `կարող`). Python dict literals keep the **last** value, so the
   `դուր` card shipped the wrong (later) gloss
   `(in դուր գալ) to please …` instead of the curated one. No error,
   no warning — the earlier definition just vanished.

## What was correct

The intended glosses were fine; the defects were purely mechanical
(wrong codepoint, accidental duplicate). The deck validated 0-errors
the whole time — these are exactly the bugs a green structural pass
misses.

## Mitigation (two-step rule, applied)

**Fix.** Rewrote `ալ` with the correct Armenian `էլ` (built from
codepoints to avoid re-introducing the confusable); removed the three
shadowed duplicate-key lines and de-duplicated `դուր`.

**Guard.** Two new checks in `validate_deck.py`:
- `check_script_purity` extended to scan **gloss** tokens for any
  Armenian+Cyrillic / Armenian+Latin mix (`mixed-script-gloss`,
  error).
- `check_duplicate_override_keys` — an AST pass over `build_deck.py`
  that flags any string key duplicated within a dict literal
  (`duplicate-override-key`, error). Catches the shadowing class for
  every override dict, not just the ones we happened to notice.

## Lesson

LLM source edits introduce *invisible* defects — confusable codepoints
and duplicate keys read as correct. Visual review can't catch them;
only a machine check can. When the editing surface is code (an
override dict) rather than data, the guard belongs at the source/AST
level, not just the output level.
