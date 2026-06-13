# 2026-06-13 — Overview of the LLM-error log (`errors/`)

Synthesis of all 16 entries, read end-to-end (2026-05-07 →
2026-06-07). Companion to `research/2026-06-11-repo-review.md`
(the full-repo review).

## Topline

16 entries. Severity: 1 critical, 9 major, 6 minor. Status: 10
mitigated, 4 open, 2 resolved. **Caught by a human in 13 of 16
cases**; the mechanical layer (citation-check) caught one,
dogfooding two. The log is honest in both directions: one entry
is a *positive* case (correct refusal to gloss `հլը` with zero
sources, 2026-05-07-003), one is filed
`human-error-with-llm-confirmation` (2026-05-07-002).

## Four families

### 1. Structural assertion without the cheapest baseline check
(6 instances — the dominant family, rolled up inside the log
itself at 2026-05-14-002 and 2026-06-07-001)

- `սով գալ` added to the psych-verb paradigm by analogy, zero
  corpus hits, never grepped (2026-05-09-004, open).
- Case-frame invented for `փոխանակել` (`X փոխանակել Y-ով`); the
  corpus attests only a single-argument frame; falsified by the
  operator's street-sign datum `տարադրամի փոխանակում`, then
  web-corroborated (2026-05-11-001, open).
- Self-falsifying illustrative example (`им навстречу` offered
  as a predicted deviation when it is standard Russian; two axes
  varied at once) (2026-05-14-001, open).
- `Քոբուլեթի` decomposed as stem + `-ի` case ending; the `-ի` is
  the Georgian nominative inside the borrowed stem (cf.
  `Թբիլիսի`). Same session: "Ghamoyan himself" for three female
  authors whose given names were in the manifest
  (2026-05-14-002).
- Distributive morpheme `-ա` invented for `մարդա 500$`; the `ա`
  is the colloquial 3sg copula, and the corrective citation was
  **already in the auto-grounding bundle on screen**
  (2026-06-07-001).

Distilled rule (stated twice in the log): *before asserting a
structural analysis, run the cheapest possible check on its
baseline assumption — especially when it feels obvious.*

### 2. Dictionary sense-selection / deck tooling (4 entries)

POS-priority misranks (`տարեկան`→"rye", `բաց`→"Bats (language)";
2026-05-09-001, the founding case for the challenge protocol);
kaikki natural order itself misranking (`հազար`→"lettuce" before
"thousand"; 2026-05-09-005); bare-lemma `դուր` missing its idiom
(2026-05-09-003); the homograph-trap harvest from the operator's
manual deck review (`մերի`, `ներ`, `գնում`, `ալ`, postpositions;
2026-06-03-001). Lesson: *a single-sense dictionary entry is more
dangerous than an ambiguous one — the ambiguity check sleeps
through it.* Best-guarded family: every entry produced golden
anchors plus a named validator check.

### 3. Citation discipline (3 entries, incl. the two worst)

- `խոտ` (critical, 2026-05-09-002): four LLMs, four confident
  uncited glosses; correct citation sat in
  `topics/lexicon/yerevan_slang.md` (ghamoyan p48).
- Song subagents (2026-06-01-001): six fabricated/mislabeled
  citations under `Cited` tags (two whole-cloth, two
  right-page/wrong-book, two page-range overstatements),
  integrated on trust. Load-bearing rule: **delegation does not
  transfer trust — the orchestrator re-audits subagent
  citations.**
- Verbatim-bytes violation (`[§ntʰunel]` gloss vs. actual JSONL
  spans; 2026-05-07-002) — the one error the mechanical layer
  caught itself.

### 4. Script / edit hygiene (2 entries)

Unicode confusables in chat output (Georgian `ჯ` for Armenian
`ջ`; third in-project instance after `մыть`, `λվանալ`;
2026-05-09-006, open — chat output has no validator). Invisible
source edits: Cyrillic `л` inside an Armenian gloss token +
four silently-shadowed duplicate dict keys (2026-06-03-002) →
`mixed-script-gloss` and the AST `duplicate-override-key` check.

## Trajectory

May 9 cluster = tooling bugs; May 14 onward = in-chat linguistic
analysis errors. That is the guards working: the deck/topic
classes got mechanized, so the residue lives in the one layer
nothing gates — live analysis in conversation. Starkest datum:
2026-06-07-001 happened with the corrective citation already
injected by the autoground hook. Retrieval is solved; attention
is not. (Caveat recorded 2026-06-11: that response was English
prose around one short Armenian token — below the self-check
hook's ≥20-Armenian-chars threshold, so even the repaired hook
would not have fired. The threshold is this family's next test.)

## Bookkeeping

- Stale status: 2026-05-11-001 remains `open` pending "a durable
  `topics/` artifact" while `topics/lexicon/currency_exchange.md`
  exists with `status: reviewed` — the bit was never flipped.
  The other three opens (sov-gal table demotion, chat-confusable
  mitigation, self-falsifying-example discipline) are genuinely
  pending.
- Category drift: `gloss-sense-selection` and
  `script-and-source-hygiene` (both 2026-06-03) are not in
  `errors/README.md`'s seven-category enum; `citation-real-but-
  wrong` has zero entries; disposition `tooling-gap` is not in
  the README enum either.
- Two-step compliance is real in the `mitigated` entries — each
  names fix + guard, and the guards verifiably exist in code.
