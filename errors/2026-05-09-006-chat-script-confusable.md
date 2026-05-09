---
id: 2026-05-09-006
date: 2026-05-09
caught_by: human
caught_during: review
severity: minor
disposition: llm-error
category: representation-bias
subcategory: chat-output-script-confusable
phenomenon: unicode-confusable-substitution-in-mixed-script-output
related_topics:
  - topics/phonology/voiced_aspirated_alternation.md
related_pitfalls:
  - llm-workflow.md#9-two-validation-axes-structural-and-editorial
status: open
mitigation:
  type: none-yet
  ref: null
recurrence: pattern-of-N
---

## Input

User reviewing assistant chat output describing the ղջ
cluster behaviour. The assistant's text contained:

> the վերջ-/առաջ-/մեջ- root regularity though — this is
> ղջ cluster devoicing (both consonants of the cluster
> shift: ղ → /χ/, **ჯ** → /tʃʰ/)

User reaction: "i see ჯ → չ, is this a bug or an ipa item?"

## What the LLM produced

The character `ჯ` (U+10EF GEORGIAN LETTER JIL) instead of
the intended Armenian `ջ` (U+057B ARMENIAN SMALL LETTER JE)
in mixed-script chat output. The two glyphs are visually
near-identical and render the same in many monospace fonts,
but they're different codepoints from different unicode
blocks (Georgian vs Armenian).

## What was correct

`ջ` (U+057B). Same character that appears correctly in the
neighbouring `վերջ-/առաջ-/մեջ-` cluster of the same sentence.
The substitution was inconsistent within the same paragraph,
which is the diagnostic signal for the LLM-decoding-drift
mechanism (different position → different sampling, lands on
a confusable codepoint).

## Why this happened

Pattern-of-N recurrence — third documented instance in this
project of LLM unicode-confusable substitution in mixed-script
output. Prior cases (logged contextually in conversation, not
as their own files because they were caught & fixed in-session):

1. `մыть` (intended Russian) written with Armenian `մ`
   (U+0574 instead of Cyrillic м U+043C).
2. `λվանալ` (intended Armenian) written with Greek `λ`
   (U+03BB instead of Armenian լ U+056C).
3. `ჯ` (this case) — Georgian `ჯ` for Armenian `ջ`.

Underlying mechanism: when LLM output switches scripts
mid-paragraph (Russian↔Armenian, Greek↔Armenian, Georgian
↔Armenian), the conditional probability over the next token
includes visual-cousin codepoints from neighbouring scripts.
At sampling time the wrong-script codepoint is occasionally
picked, producing output that *looks* correct but fails byte-
level verification. The pattern is asymmetric across positions:
the same character can be correct in one occurrence and wrong
in the next within the same paragraph.

This is structurally the same trap as the prose-gloss bug:
output looks right, passes casual inspection, fails byte-level
check.

## Mitigation

**Existing guards (file-write side):**
- `frequency/validate_deck.py § check_script_purity` — flags
  confusables in the deck's lemma column. Catches them when
  the bug lands in `cards/top_1000.tsv`.
- `.claude/skills/critic-pass/lint.py § _check_script_purity`
  — flags confusables in any topic-file Armenian word
  (word-dominance rule). Catches them when the bug lands in
  `topics/`.

**Coverage gap (chat side):**
Chat output isn't gated by any validator. The user is the
last line of defense.

**Possible mitigation paths** (none implemented yet):

1. **Self-check protocol** — before ending a turn that
   includes Armenian text, scan the output for confusables
   in Armenian-context words and correct in place. Cheap
   for the LLM at the cost of another tool/instruction.

2. **Force-LaTeX-style markers** for high-stakes Armenian
   tokens (e.g. `^[am]ջ` to indicate "Armenian script: ջ").
   Verbose; impacts readability.

3. **Explicit prompt-level reminder** in the project
   `CLAUDE.md`: "When writing Armenian in chat, distrust
   single-character glyphs that could be confusables; spell
   out via Armenian-script unicode names if uncertain."
   Low-cost; relies on prompt adherence.

4. **Dogfood-only acceptance**: treat chat confusables as
   minor and trust user to flag (the current state). Cost:
   user pays attention.

Recommendation: try (3) — add a CLAUDE.md note. The fully
mechanical solution (1) is implementable but adds friction;
(3) is cheap and might be sufficient given the bug's low
severity (immediately recognised by the user, no downstream
impact since chat doesn't write to files without validation).

## Test case

```python
# Can't easily replay LLM sampling, but the diagnostic for
# any future occurrence:
import unicodedata
def find_confusables_in_armenian(text: str) -> list:
    """Find non-Armenian alphabetic chars whose word context
    is dominantly Armenian. Mirrors validate_deck check."""
    # implementation in `.claude/skills/critic-pass/lint.py
    # § _check_script_purity` and `frequency/validate_deck.py
    # § check_script_purity`.
    pass

# Reproduction context:
# - Mixed-script output (Russian + Armenian, or
#   Greek + Armenian, or Georgian + Armenian).
# - The confusable codepoint appears once or twice in a
#   paragraph where the same intended character appears
#   correctly elsewhere.
```

## Cross-references

- File-write validators that catch this when it lands in
  files: `frequency/validate_deck.py § check_script_purity`,
  `.claude/skills/critic-pass/lint.py § _check_script_purity`.
- Prior in-session occurrences (not separately filed):
  `մыть` / `λվանալ` mentioned in the 2026-05-09 conversation.
- Workflow context: `llm-workflow.md` §9 (structural vs
  editorial axes — this falls in the *structural* axis but
  for chat output specifically, which has no validator).
