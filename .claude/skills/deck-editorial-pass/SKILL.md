---
name: deck-editorial-pass
description: |
  Agent-driven editorial review of a card deck. Samples N rows,
  spawns a sub-agent with a learner-pov critic prompt, returns
  structured findings. Complements `frequency/validate_deck.py`
  (structural lint) by catching the editorial bugs that structural
  checks systematically miss. See `CLAUDE.md` § "Critic-agent
  pattern" and the canonical 2026-05-09 deck cleanup case.
---

# deck-editorial-pass

Stage 3 of the deck-review pipeline: agent-driven editorial critic.
The first two stages are mechanical (`frequency/validate_deck.py`
for structural lint + `frequency/golden_glosses.tsv` for regression
anchors). This stage catches the **judgement-required residue** —
the bugs a human reader spots in 30 seconds but no rule-based
validator can detect cleanly.

## Motivation

CLAUDE.md documents the canonical case: the 2026-05-09 deck cleanup
found six classes of editorial bugs that the structural validator
passed cleanly. The fix-loop pattern is general:

> "When implementing any non-trivial heuristic [...] after writing
> it: Spawn a separate Agent with the framing **'find weaknesses in
> this rule / where would it pick the wrong answer / produce the
> wrong output'** — different prompt frame from the implementer
> agent."

This skill packages that pattern for card decks.

The structural validator at `frequency/validate_deck.py` already
covers a lot of the editorial-bug surface (`check_prose_gloss`,
`check_verbose_gloss`, `check_inflected_leak`,
`check_redundant_language_parenthetical`, etc.). This skill's value
lies **strictly in what's left after those checks**:

- Sense-priority misorder (basic sense buried after secondary ones)
- Gloss naturalness (stilted, archaic, unidiomatic for a learner)
- Register mismatches (colloquial lemma with formal gloss or vice versa)
- Ambiguous sense-stacks that pass the length cap but still mislead
- Anything else that breaks the "this is a flashcard" frame

## When to invoke

- After running `frequency/validate_deck.py` and getting a clean
  structural pass.
- Before shipping a deck build.
- Periodically (e.g. weekly, or on every `build_deck.py` rebuild) on
  a fresh sample to detect drift.
- When the user refreshes deck source data (kaikki dump, dictionary
  source, etc.).

## Protocol

1. **Run structural validator first.** Stage 3 is only meaningful
   after stage 1 (structural) is green:

   ```sh
   sakayan/.venv/bin/python frequency/validate_deck.py cards/top_1000.tsv
   ```

2. **Sample rows for review.** Default 30 rows, deterministic seed:

   ```sh
   python3 .claude/skills/deck-editorial-pass/sample.py \
       cards/top_1000.tsv -n 30 --seed 42
   ```

   Use `--stratified` for proportional sampling across rank buckets
   (top-100 / 101-500 / 501-1000 / 1000+). Use `--seed <new>` to get
   a fresh sample for drift detection.

3. **Spawn the editorial critic.** Spawn a `general-purpose` Agent
   with:
   - The prompt template at `PROMPT.md` (in this skill's directory),
   - The sampled rows pasted in as input,
   - Instructions to return structured findings in the schema
     described in `PROMPT.md`.

4. **Triage findings.**
   - **⚠ blockers**: add the row + the fix to `HAND_OVERRIDES` in
     `frequency/build_deck.py`. Re-run `build_deck.py`. Re-validate.
   - **⚙ suggestions**: review case-by-case. If accepted, add the
     "correct" gloss to `frequency/golden_glosses.tsv` as a
     regression anchor. Per CLAUDE.md two-step rule: a fix + a
     guard, never one without the other.
   - **ℹ notes**: log to `frequency/golden_glosses.tsv` as drift
     signals (with severity 'info') without blocking the ship.

5. **Re-sample and re-run** with a different `--seed` until the
   ⚠ count is zero across multiple samples. Single-sample zero is
   not enough — the bug class might just have been absent from the
   first sample.

## Composition

| stage | what it covers | tool |
|---|---|---|
| 1. Structural lint | columns, lemma-form match, prose, length, language-parenthetical, MWU, EU-ligature, script purity, etc. | `frequency/validate_deck.py` |
| 2. Regression anchors | per-row "known good" glosses | `frequency/golden_glosses.tsv` |
| 3. **Editorial critic** | sense-priority, naturalness, register, ambiguity, learner-pov flow | **this skill** |

Stage-3 findings flow back into stages 1 and 2: a recurring class
of bug becomes a new check in `validate_deck.py`; per-row
corrections become anchors in `golden_glosses.tsv`. The agent stage
is the discovery channel for new check classes; the structural
stage is where the checks live once they've been articulated.

## What this skill is NOT

- Not a replacement for `frequency/validate_deck.py`. The
  structural validator stays primary; this is a complement.
- Not a per-row review of the entire deck. The sample is N=30
  typically; full-deck review would be a build-promotion gate, not
  a routine check.
- Not where new heuristics are introduced — those go through
  `challenge-rule` per CLAUDE.md § "Heuristic validation —
  non-negotiable." This skill's findings can *inform* new
  heuristics, but introducing them is a separate workflow.

## Files in this skill

- `SKILL.md` (this file)
- `sample.py` — deterministic row sampler
- `PROMPT.md` — canonical editorial-critic prompt for the sub-agent
