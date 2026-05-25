# Pre-emit verification automation — design options A-D

Date: 2026-05-26
Status: design note. Option A is the chosen starting point.

## Motivation

This conversation has logged 7+ instances over 17 days of the same
failure family: **structural assumption made by the LLM without
the cheapest baseline check**. Each instance was caught by the
human operator pushing back on smooth-sounding answers and forcing
the LLM to re-verify against corpus. Concretely the same shape
across:

- `errors/2026-05-09-004` — sov-gal paradigm extension without
  attestation
- `errors/2026-05-11-001` — currency-exchange case-frame without
  verb argument-structure check
- `errors/2026-05-14-001` — self-falsifying illustrative example
  without instantiation check
- `errors/2026-05-14-002` — Քոբուլեթի morpheme decomposition
  without stem-inventory check
- 2026-05-14-002 follow-up — Ghamoyan author-gender assumption
  without given-name check
- 2026-05-26 — Kotayk copula-drop misanalysis (twice: first
  application to a non-clause; then "Pattern 2" fabrication to
  bridge the slogan question)

The operator-as-verification-layer works but shouldn't have to.
Several existing pieces of infrastructure already do this kind of
check — they just don't fire on the LLM's output.

## What exists

| layer | runs on | extends to LLM output? |
|---|---|---|
| `armenian_autoground.py` hook (greps KB via `query_kb.py`) | `UserPromptSubmit` | ✗ |
| `query_kb.py` (lemmatize + grep corpus + emit bundle) | callable from anywhere | n/a |
| `answer-q` skill (forces grounding protocol) | when LLM explicitly invokes | ✗ |
| `citation-check` skill (byte-verifies verbatim quotes) | topic files | ✗ — only `verbatim_quote` frontmatter |
| `critic-pass` skill (structural + editorial lint) | topic files | ✗ |

Every failure logged this session would have been caught by
something already in this list if it fired on the LLM's
in-progress response.

## Options, lightest to heaviest

### (A) Pre-emit self-grep — chosen as starting point

A hook that intercepts the LLM's draft response before emission,
scans for substantive grammar/usage claims about specific Armenian
lemmas, runs `query_kb.py` on those lemmas, and either:

- injects the bundle back into the LLM's context as a
  system-reminder (forcing reconciliation before emission), or
- refuses to emit unsupported claims (forcing a redraft)

Minimal viable version: always inject the bundle for any Armenian-
content draft, even if the user's prompt had no Armenian. Forces
the LLM to look at corpus evidence before asserting anything.

**Pros**: reuses existing `query_kb.py` and `armenian_autoground`
hook patterns. Smallest delta. Catches roughly 70-80% of the
logged failure family.

**Cons**: doesn't fix register-claims that the corpus has no
evidence on either way (e.g. contemporary spoken / advertising
register — out of corpus scope). Can be ignored if the model
asserts anyway.

### (B) Auto-invoke `answer-q` skill on Armenian-content prompts

The `answer-q` skill exists and defines the right protocol for
Armenian-content questions (composes `query_kb.py` retrieval with
a constrained answering protocol plus `verify_citations.py`
post-answer validation). The skill is rarely invoked. A hook that
detects "Armenian-content question" in the user's prompt and
forces the response to route through `answer-q` would close most
of the gap with zero new code — just enforce existing
infrastructure.

**Pros**: zero new code. Skill is already designed for exactly
this case.

**Cons**: makes responses slower / more verbose for short
questions where the protocol is overkill. Triggering rules need
calibration.

### (C) Critic-agent on the LLM's draft

For multi-paragraph linguistic analyses: spawn a `general-purpose`
sub-agent with the prompt "find the structural-assumption-without-
baseline-check failures in this draft" and either auto-apply the
findings before emission or surface them as a system-reminder
forcing a re-draft. Same pattern as the `deck-editorial-pass` and
`critic-pass` skills, applied to conversational output.

**Pros**: catches subtle inference-overreach that structural greps
can't see. Best for topic-promotion-grade answers.

**Cons**: slow (~30-60s per spawn). Overkill for one-liners.
Token-expensive.

### (D) Confidence-tagging output schema

Constrain the LLM's output format so every linguistic claim is
tagged `[CORPUS: ref]`, `[PRIOR]`, or `[PREDICTION]`. Reaching
beyond citation becomes visible in the surface form. Makes the
failure mode auditable at the prose level.

**Pros**: catches the exact failure ("plausible-sounding inference
without citation") at the level the failure happens. Visible to
the operator without verification machinery.

**Cons**: invasive on response format. Hard to enforce
mechanically — the tags themselves can be wrong.

## Recommended path

1. **Start with A**, specifically the simplest variant: a hook
   that always runs `query_kb.py` on Armenian content in the
   LLM's draft response and injects the bundle back as a
   system-reminder before emission.

2. **Measure**: log every time the hook fires, what bundle gets
   injected, whether the LLM revises its draft. Run for a week,
   count failures-prevented.

3. **If A catches 5/7 of the logged failure family**, ship it as
   default. If it catches 7/7, no need for B-D yet. If only 3-4,
   add B as a secondary trigger.

4. **Reserve C** for topic-promotion-grade answers (already in
   place via the editorial-pass pattern).

5. **D** is exploratory — only justified if A+B+C don't close the
   gap.

## Implementation sketch for A

```
.claude/hooks/armenian_self_check.py
  - reads LLM draft (from hook payload)
  - extracts Armenian lemmas from substantive claims
  - calls frequency/query_kb.py
  - returns system-reminder with bundle + instruction to
    reconcile claims with corpus
```

Hook event: whatever pre-emit / Stop-with-feedback event the
Claude Code harness exposes. The hook should be able to block-and-
feedback (similar to how `UserPromptSubmit` hooks inject context
before model sees prompt — same mechanism, reversed direction).

Register in `.claude/settings.json` alongside the existing
`armenian_autoground` hook entry.

## What this WON'T fix

Even with A running, the model can still:

1. **Ignore the injected bundle** and assert anyway. Rare but
   possible.
2. **Make register-claims the corpus has no evidence on either
   way** (the gap that's not closable without a contemporary-
   spoken / contemporary-media Armenian corpus).
3. **Fabricate quasi-corpus citations that look right.**
   `citation-check` catches these on topic files; would need to
   extend to conversational claims.

So A closes ~70-80% of the recurring failure family but not 100%.
The remaining 20-30% needs C, D, or domain-side scaffolding (a
contemporary corpus).

## Cross-references

- `.claude/hooks/armenian_autoground.py` — pattern to follow for
  the new hook
- `frequency/query_kb.py` — the retrieval call site
- `.claude/skills/answer-q/` — the skill that already enforces
  the grounding protocol when invoked
- `errors/INDEX.md` and the 7+ logged instances of the failure
  family — the empirical basis for this work
