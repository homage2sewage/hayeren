# 2026-06-13 — Answer-verification architectures vs. this repo's failure modes

Driven by the `2026-06-13` "1960s manual" incident
(`errors/2026-06-13-001`) and the broader question: the
characteristic LLM failure here is *ungrounded answer-time prose*;
is there a known architecture that catches it, and which fits?

Method: web survey of verify-over-output architectures → summary →
**adversarial fact-check agent over the summary** (which corrected
three of my claims — logged inline below, because the correction is
the point) → map against the error-log failure families
(`research/2026-06-13-errors-log-overview.md`, agent re-summary) →
synthesize with the repo's own enhancement plan
(`research/2026-06-11-repo-review.md` § "Enhancement plan").

## The architectures (corrected after the fact-check pass)

Common spine: **decompose output → retrieve evidence → verify each
claim.** They differ on where the verify sits, whether it edits or
only scores, and whether it needs training or a corpus.

| method | when | edits or scores | training? | corpus? | targets |
|---|---|---|---|---|---|
| **CoVe** | prompt-time self-critique | **edits** (revised final) | no | default no¹ | factual hallucination via self-deliberation |
| **Self-RAG** | in-model, decode-time | shapes generation (soft re-rank²) | **yes**³ | yes | groundedness baked into generation; `IsUse` adds a utility signal⁴ |
| **RARR** | post-hoc | **edits** + attribution report | no | yes | making output attributable to evidence |
| **SAFE / FActScore** | post-hoc | **score only** | no | yes | factual-precision score over atomic claims |
| **VeriFastScore** | post-hoc | score only | **yes (fine-tuned)**⁵ | yes | same, ~6× faster |
| **FacTool / Factcheck-GPT** | post-hoc | score + explanation | no | yes | true/false per claim (FacTool fast; Factcheck-GPT slow) |

Fact-check corrections (agent over this summary):
1. CoVe answers verification questions from the model's **own
   knowledge** by default; the paper notes retrieval/tool variants
   are compatible. Not definitionally self-contained.
2. Self-RAG's inference is **soft re-ranking** in segment beam
   search (weighted critique-token probabilities), with optional
   thresholds — *not* "hard constraints dropping spans."
3. Self-RAG's critic runs **offline at training time** to insert
   reflection tokens; at inference a single generator emits them.
4. `IsUse` scores **response utility to the query** (1–5),
   independent of passage support — adjacent to "was this needed,"
   so "none targets necessity" is overstated. The real residual:
   none does **sentence-level pruning of true-but-unnecessary
   content** of the *final* text.
5. VeriFastScore is **distilled/fine-tuned** (Llama-3.1-8B); SAFE
   and FActScore are training-free.
6. (Also flagged) atomic-claim **decomposition is itself LLM-hard**
   in general — not a pure grep step. It's lighter *here* only
   because our verifiable units are narrow (Armenian-script spans +
   their adjacent glosses/characterizations).

## The problem they'd face (error-log re-summary)

Dominant failure family **F1**: confident structural/linguistic
assertion built on pre-training prior **without the cheapest
available baseline check — even when the disconfirming citation is
already on screen.** 6 instances; every mitigation is
doc/discipline; 4 still `open`; the restated discipline-rule
demonstrably failed to prevent same-session recurrence
(`05-14-002`, `06-07-001`). The "1960s manual" case is the same
family in chat: unfounded characterization, no citation, caught
only by the operator.

Critical nuance from `06-07-001` and the autoground hooks: the
**evidence-delivery** gap is already closed — `armenian_autoground`
injects the bundle, `armenian_self_check` re-greps the draft and
blocks. The open gap is **evidence-consumption**: the model asserts
past a bundle it was handed. So the need is not more retrieval; it
is a *verify-and-block on the specific claims*, grounded in the
corpus, that the current "block any uncited Armenian draft" nag
cannot do (it gates on *presence of a citation*, not on whether the
claims — cited or not — are *supported*).

## Fit

- **Self-RAG** — best *concept* (groundedness as a first-class
  generation signal, plus `IsUse` for utility) but **requires
  training a model.** This repo consumes a hosted model; ruled out.
  Reference only.
- **CoVe** — adoptable (prompt-time, cheap) but its **self-answer
  step is the wrong grounding for domain facts.** The model
  verifying "is it a manual?" from the same prior that hallucinated
  "manual" re-confirms it. Its *structure* (extract checkable
  claims from the draft, answer them as separate tasks) is
  valuable; its *self-answer grounding* is not — replace with
  corpus grounding.
- **SAFE / FacTool** — the right *detection* shape
  (decompose → retrieve → label supported/unsupported) and
  prompt-time. Score-only, so they detect-and-flag, not revise.
- **RARR** — SAFE + revision + attribution report. Higher power,
  higher risk (auto-editing Armenian the operator can't check).

The repo already owns ~80% of the SAFE/RARR substrate:
`query_kb.py` (retrieve), `citation-check` byte-grep (verify a
fragment against a page), and the repaired Stop hook (read draft
from transcript, block). And the enhancement plan **already names
the missing glue** — the deferred *"Stop hook tier-1 redesign:
parse (citation, fragment) pairs from the draft and byte-verify via
citation-check logic; block on specific failures."* That deferred
item **is** a domain-specialized SAFE-over-draft.

## Best-fitting enhancement

**Implement the deferred "Stop hook tier-1 redesign" as a
SAFE-shaped verify pass over the draft — with two scope
corrections the architecture comparison forces:**

1. **Verify uncited characterizations, not only attached
   citations.** The planned "(citation, fragment) byte-verify"
   only checks claims that *carry* a citation. But the F1/"manual"
   failure is the inverse: confident source/Armenian
   characterizations with **no** citation that should have been
   cut. So the pass needs a second arm — flag *characterizing
   assertions about Armenian or source-facts that carry no citation
   and have no support in the bundle.* That arm is exactly what
   would have caught "manual," "1960s," and the F1 family; the
   citation-checking arm catches the song-style fabrications (F2).

2. **Ground in the corpus; never self-answer (CoVe's trap).** Each
   extracted claim is verified against `query_kb`/`citation-check`
   bytes — support, not token-presence — not against the model's
   prior. This is the SAFE/RARR grounding, not CoVe's.

Staging (mirrors the repo's own caution and the cost reality that
keeps verify-passes opt-in everywhere):
- **v1 — detect & block** (SAFE-style, score-only). Reuse the Stop
  hook's existing scope gate (substantive Armenian; the hook
  already counts Armenian chars) so it fires only where it pays.
  Extract Armenian-script spans + their adjacent EN/RU
  characterizations (light, regex-able *here*), verify each, block
  with the *specific* unsupported items. Do **not** auto-revise.
- **v2 — revise** (RARR-style) only after v1's block-rate and
  false-positive rate are observed, because auto-editing Armenian
  the operator can't independently check is the riskier mode.

Why this and not the alternatives:
- It targets **F1**, the dominant, least-guarded, most
  human-dependent failure — not the already-solved write-time
  classes (F6 heuristic-audit, F7 byte-purity).
- It is **adaptation, not greenfield**: query_kb + citation-check +
  the Stop hook already exist; this is the verify-and-extract glue.
- It is **hosted-model-compatible** (rules out Self-RAG) and
  **corpus-grounded** (fixes CoVe's self-answer trap).
- It converts the existing *"block uncited Armenian"* nag into
  *per-claim verification* — the evidence-consumption gap, not the
  evidence-delivery gap.

What this deliberately does **not** chase: a **necessity** pruner
for true-but-unnecessary prose. Per the fact-check (#4) no
architecture does sentence-level necessity pruning, and per the
operator's own correction the "1960s manual" paragraph was not
true-but-unnecessary — it was *unfounded*, which a groundedness
verifier catches. Necessity stays an output-contract / prompt
concern (terse schema: answer + citation + named gaps), not an
architecture.

## Two orthogonal process fixes (cheap, from the incident)

Independent of the verifier, from `errors/2026-06-13-001`:

- **Remediation routing.** When operator feedback lands, default to
  an `errors/` entry (the guard-building system), not only a
  `memory/` note (the private aside). The memory mechanism is
  harness-primed; `errors/` is not — so the lighter path wins by
  default and routes around the durability system. A one-line
  CLAUDE.md / hook nudge.
- **Remediation propagation (the §11 sibling-sweep).** When a
  correction names one error, sweep the *same sentence* for
  same-class siblings before declaring the lesson captured. "1960s"
  was patched; "manual," beside it, was not. Mechanizable as a step
  in the verify pass (re-scan the corrected sentence for other
  uncited characterizations), zero affect required.
