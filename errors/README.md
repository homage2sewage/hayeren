# errors/ — structured LLM-failure log

Append-only inventory of LLM errors encountered during this
project's operation. Converts pattern-of-N anecdotes into
structured, indexable, loadable infrastructure — the same
move that took linguistic phenomena out of `armenian-grammar.md`
prose into citation-checked `topics/`.

Source of the design:
`/home/alexey/work/hayeren_claude_log_err` (LLM-authored design
doc, May 2026). This README is the operationalised version.

## Why this exists

Three goals, in order of cost:

1. **Be a record.** Preserve enough context to understand what
   went wrong, after the moment passes.
2. **Be a teacher.** Get loaded into context for future LLM
   sessions so the same error doesn't recur.
3. **Be a test.** Convert into regression cases that can be
   re-run to verify a fix held.

(1) is cheap (just write the file). (2) requires shaping the
file so a future LLM reading it as context produces correct
behaviour. (3) is real engineering and is deferred — see
`research/2026-05-09-answer-pipeline-roadmap.md`-style staged
roadmap below.

## What gets logged — the tiered rule

Logging fatigue kills any error-log system. The tiered rule:

- **Always log.**
  - Anything that survived to a verifier or human review and
    was caught there.
  - Any *novel* failure mode — never seen before in this
    workspace.
  - Any error whose mitigation requires changing schema, a
    doc, or a skill.
- **Don't log.**
  - Routine in-session corrections during drafting ("no, try
    again" → second pass succeeds). That's collaboration, not
    a recordable failure.
- **Log on third recurrence.**
  - Mistakes seen before but not yet structural — the third
    instance triggers a writeup even if no individual case was
    severe. The `recurrence: pattern-of-N` frontmatter field
    captures this.

The third-recurrence rule is what converts pattern recognition
into *structured* pattern recognition: the author thinking
"the LLM keeps doing X" becomes a file future sessions can load.

## File schema

One markdown file per error: `errors/YYYY-MM-DD-NNN.md`. Three
digits for within-day serial. Append-only.

### Frontmatter

```yaml
---
id: 2026-05-09-001                     # date + serial within day
date: 2026-05-09
caught_by: human                       # who/what caught it
caught_during: drafting                # context of the catch
severity: minor                        # critical | major | minor
disposition: llm-error                 # what kind of error
category: language-understanding       # primary category
subcategory: agreement-mismatch        # finer grain
phenomenon: armenian-verb-agreement    # linguistic / system thing
related_topics:                        # topic files touching this
  - topics/morphology/negation.md
related_pitfalls:                      # docs that already note the pattern
  - transliteration-notes.md#pitfall-2
status: mitigated                      # open | mitigated | resolved
mitigation:                            # null if open
  type: doc-update                     # schema-change | doc-update | skill-update | manual-discipline
  ref: transliteration-notes.md
recurrence: first-seen                 # first-seen | recurrence | pattern-of-N
---
```

### Field semantics

| field | values | notes |
|---|---|---|
| `caught_by` | `human` / `citation-check` / `critic-pass` / `verify_citations` / `validate_deck` / `external-llm` / `dogfood` | Who or what surfaced it. `external-llm` covers the case where another LLM (e.g. on a different chat) flagged something. |
| `caught_during` | `drafting` / `walk` / `review` / `tutor-query` / `extraction` / `validation` | What activity was running when the catch happened. |
| `severity` | `critical` / `major` / `minor` | `critical` = wrong info reached or would-reach a topic / card / answer to user. `major` = caught at review but plausible enough to slip. `minor` = obvious-on-second-glance, included for completeness. |
| `disposition` | `llm-error` / `prompt-ambiguity` / `source-ambiguity` / `human-error-with-llm-confirmation` / `verifier-bug` / `tooling-bug` | The honest classification. The last one — human error the LLM didn't catch — is critical to keep separate from LLM errors so the inventory doesn't skew toward LLM-bashing. |
| `category` | one of the seven below | Primary categorisation. |
| `subcategory` | free string | Finer-grain pattern. |
| `phenomenon` | free string | What linguistic / system thing this involved. Used for `errors/BY-CATEGORY.md` aggregation. |
| `related_topics` | list of paths | Topic files that touch this. Bidirectional — those topics should backlink. |
| `related_pitfalls` | list of paths + section anchors | Existing docs documenting the pattern. |
| `status` | `open` / `mitigated` / `resolved` | `mitigated` = doc update / discipline note exists. `resolved` = mechanical guard catches recurrences. |
| `mitigation.type` | `schema-change` / `doc-update` / `skill-update` / `validator-update` / `manual-discipline` / `none-yet` | Where the fix lives. |
| `mitigation.ref` | path | The fix's location. |
| `recurrence` | `first-seen` / `recurrence` / `pattern-of-N` | Whether this is novel. Trips the third-recurrence logging rule. |

### Body structure

Fixed five-section structure (skip a section by leaving it
empty if not applicable):

```markdown
## Input

<the prompt or task that produced the failure>

## What the LLM produced

<verbatim, with context. quote actual output.>

## What was correct

<verbatim, with citation if available.>

## Why this happened

<diagnosis of the underlying failure pattern.>

## Mitigation

<either link to existing fix, or propose one. include type and ref.>

## Test case

<minimal input that reproduces the failure. used by future
regression-replay skill.>
```

The Test-case section is what turns logging into infrastructure.
Every error file is a potential regression test.

## Categories

Seven top-level categories, sized to span the failure-mode
landscape without proliferating:

| category | covers |
|---|---|
| `language-understanding` | Agreement mismatch, register confusion, code-switching, calibrated-refusal failures, dative-experiencer construction errors. |
| `citation-fabrication` | Invented sources; real source but wrong page; real page but quote doesn't exist there. |
| `citation-real-but-wrong` | Verbatim quote exists at the cited location but doesn't support the claim attached to it. (The "tightening" gap from `research/2026-05-09-answer-pipeline-roadmap.md`.) |
| `prose-overreach` | Body prose making claims beyond what cited sources support. |
| `representation-bias` | Canonical-form normalisation: gloss-vs-bytes, Unicode normalisation, IPA-instead-of-bytes, OCR confidence by script. |
| `confidence-miscalibration` | Confident output where uncertainty was warranted. The Pashinyan-tweet four-LLM case is the canonical example. |
| `tooling` | Verifier bugs, schema drift, harness limitations, MWU-detection misses, lemmatiser overstrip. |

If a new error doesn't fit any of these, log it under `tooling`
provisionally and let pattern emerge before adding a category.
Five-or-six categories is the right size; more becomes
categorisation-as-work.

## Indices (auto-generated)

Run `.claude/skills/error-log/build_index.py` to (re)generate:

- `errors/INDEX.md` — chronological, with id / date / category /
  severity / status / one-line summary.
- `errors/BY-CATEGORY.md` — grouped by category, then
  subcategory.

The script walks `errors/`, parses frontmatter, emits both
files. Run after adding a new error file. Eventually hookable
to a pre-commit or critic-pass.

## Bidirectional links to topics

Each error's `related_topics:` entries should be backlinked
from the topic file's frontmatter:

```yaml
known_failure_modes:
  - errors/2026-05-09-001.md
```

Mechanical bidirectional-link enforcement is a planned
critic-pass extension — until then, maintain by hand. The
bidirectional link is what makes the error log useful at
*query time*: when an LLM loads a topic file, it also sees
"errors X, Y involve this topic; consult before answering."

## Loading errors into LLM context

Three integration points worth designing for:

1. **At walk time.** `walk` skills (when authoring a topic) grep
   `errors/` by phenomenon/category, load matches into the
   subagent's briefing context. The drafting LLM sees prior
   failures before producing its first output.
2. **At critic-pass time.** Phase 4 (proposed): for each topic
   touched by a walk, check error log for related entries;
   verify the topic doesn't reproduce any failure pattern.
3. **At tutor-query time** (the `answer-q` skill, see
   `.claude/skills/answer-q/SKILL.md`). Future enhancement:
   `query_kb.py` already greps `topics/` and the four book
   JSONLs; extend it to also grep `errors/` and surface matched
   error files in the bundle. The error file teaches the
   answering LLM "this failure mode applies; calibrate
   accordingly."

(3) is the highest-leverage integration; tracked under the
"answer-q phase 5+" portion of the pipeline roadmap.

## Implementation order

Per the design doc's six-step plan:

1. ✅ **Directory + schema.** `errors/` exists; this README +
   schema present.
2. ✅ **Backfill known cases.** ~6 errors backfilled from
   conversation history and prior-session pitfalls.
3. ✅ **Index generator.** `.claude/skills/error-log/
   build_index.py`.
4. ⬜ **Bidirectional-link enforcement** in `critic-pass`. When
   a topic lists an error in `known_failure_modes:`, the error
   file must list the topic in `related_topics:`. Mechanical
   check, fits existing critic-pass phase-1 lint.
5. ⬜ **Wire errors into walk briefings.** Modify topic-walk
   skill to grep `errors/` by phenomenon, load matches into
   subagent context.
6. ⬜ **Regression replay.** Each error's Test-case section
   becomes a runnable input. `replay-errors` skill takes test
   cases, re-runs against current system, reports
   pass/fail-deltas. Real engineering — only build at 30+
   logged errors.

Don't build all six at once. The 1–3 jump is the biggest
single leap in usefulness; everything after multiplies on top.

## What to watch out for

**Logging fatigue.** Too-liberal rule → author gives up. The
third-recurrence rule prevents this; honour it.

**Confirmation bias in categorisation.** "LLM was wrong" as
default framing → log becomes LLM-bashing artifact. The
`disposition:` field is the discipline against this; in
particular `human-error-with-llm-confirmation` keeps the
inventory honest about cases where the LLM was a *check on*
human error and just wasn't strong enough.

## Cross-references

- `/home/alexey/work/hayeren_claude_log_err` — the design doc
  this README implements. Kept for historical reference.
- `llm-workflow.md` — broader LLM-hygiene principles. Error log
  is the durable inventory of what the principles are
  defending against.
- `research/2026-05-09-answer-pipeline-roadmap.md` — the Q&A
  pipeline that should eventually consume the error log
  (integration point 3 above).
- `kb-design.md` — agent-flow design; error log fits next to
  walks and topics in the artifact-types map.
- `CLAUDE.md` § "When the user reports a wrong output" — the
  two-step rule (fix + capture-as-guard) of which error
  logging is the durable form.
