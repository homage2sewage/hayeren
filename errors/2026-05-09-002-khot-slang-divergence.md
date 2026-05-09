---
id: 2026-05-09-002
date: 2026-05-09
caught_by: external-llm
caught_during: tutor-query
severity: critical
disposition: llm-error
category: confidence-miscalibration
subcategory: slang-gloss-without-citation
phenomenon: yerevan-slang-khot
related_topics:
  - topics/lexicon/yerevan_slang.md
  - topics/lexicon/code_switching_with_russian.md
  - topics/morphology/dialectal_lnel.md
related_pitfalls:
  - CLAUDE.md#before-answering-an-armenian-language-question
  - llm-workflow.md
status: mitigated
mitigation:
  type: skill-update
  ref: .claude/skills/answer-q/SKILL.md
recurrence: pattern-of-4
---

## Input

The Pashinyan-tweet test case — Armenian Twitter reply to a
positive video about Nikol Pashinyan:

```
հա լավ էսքան խոտ մարդ ըլնի մի հատ էլ պալիտիկ 🤭😅
```

Same prompt given to four LLMs (three external, one
workspace-aware Claude Code session) asking for translation +
explanation.

## What the LLM produced

Four different glosses for the pivotal slang word `խոտ`,
each stated with high confidence and **no citation**:

| answer | gloss for `խոտ` | implied target | reading |
|---|---|---|---|
| my-first-pass (Claude Code, in-session) | "weed / marijuana" (drug-slang calque) | speaker mocking the audience | "if a person smokes that much weed, of course…" |
| answ1 | "spineless / weak / wet blanket / vegetable" | Pashinyan's character | "how can one person be this much of a wimp" |
| answ2 | "passive / dumb / sheep-like / NPC / mindless masses" | Pashinyan's *supporters* (also misread grammar as plural) | "with this many sheep around…" |
| answ3 | "clueless / mindless / vegetable-brained" | Pashinyan's intellect | "how can someone be this much of an idiot" |

## What was correct

`khot` (խոտ) as a colloquial Yerevan-slang insult means
**"naive / clueless person"** — a metaphor from literal "grass."

This is **already attested in the workspace KB**:

- `topics/lexicon/yerevan_slang.md` line 114:
  `| խոտ | "grass" | "naive / clueless person" |`
- citing **ghamoyan p48**:
  *"խոտ (անհասկացող, չափազանց միամիտ)"*
  = "khot (clueless, excessively naive)"

`answ3`'s gloss is closest to the cited reading;
`my-first-pass`'s "weed" reading also fails the predicative
construction (`էսքան X մարդ ըլնի` means "for a person to *be*
X," not "for a person to *consume* X").

## Why this happened

Two distinct failure modes:

1. **External LLMs** ran in empty conversations with no
   workspace access. They couldn't have grepped the KB; they
   had to guess from pre-training. Architectural failure: no
   retrieval layer connects external LLMs to citation-checked
   workspace content.

2. **Workspace-aware in-session Claude** had access to the KB
   but didn't `grep` `topics/`. Treated the prompt as
   "translate and explain" rather than "look up in our KB."
   Habitual failure: pre-training prior was the first move,
   not the fallback.

The `խոտ` case is the canonical evidence for `llm-workflow.md`
principles #1 (adversarial-case prompts), #4 (golden tests),
#6 (distrust LLM rationale that names no examples), #7
(dogfood early). Every claim about a slang gloss was vibes;
the correct citation was sitting indexed and unread.

## Mitigation

Three layers:

1. **Habitual** — `CLAUDE.md` § "Before answering an Armenian-
   language question" now codifies the grep-first reflex.
   Every Armenian content-word question routes through KB
   lookup before pre-training prior gets consulted.

2. **Architectural (in-session)** — `frequency/query_kb.py`
   retrieves KB matches deterministically; `.claude/skills/
   answer-q/SKILL.md` codifies the answering protocol;
   `.claude/skills/answer-q/verify_citations.py` validates
   that each cited claim resolves to the bundle. End-to-end
   pipeline demoed on this exact tweet — the citation-grounded
   answer surfaces ghamoyan p48 and gets `խոտ` correct.

3. **Architectural (external LLMs)** — Phase 4B (MCP server)
   in `research/2026-05-09-answer-pipeline-roadmap.md` is the
   path to giving external consumers the same retrieval
   layer. Not yet built; tracked.

## Test case

Input:

```
հա լավ էսքան խոտ մարդ ըլնի մի հատ էլ պալիտիկ 🤭😅
```

Expected behaviour:

- Run `query_kb.py` on the tweet.
- Bundle surfaces `topics/lexicon/yerevan_slang.md` and
  `topics/morphology/dialectal_lnel.md` and ghamoyan p48.
- Answer cites `topics/lexicon/yerevan_slang.md` for `խոտ →
  "naive / clueless person"`, `topics/morphology/dialectal_
  lnel.md` for `ըլնի = 3sg subj of dialectal ըլնել`, and
  `topics/lexicon/code_switching_with_russian.md` for
  `պալիտիկ = Russian-loan colloquial`.
- Confidence-graded; gaps named (`մի հատ էլ` flagged as topic
  gap).
- `verify_citations.py` resolves all cites against bundle;
  exit 0.

Failure modes still possible:

- Bare-prior gloss for `խոտ` ("weed" / "spineless" / "sheep")
  — would indicate the KB-grep step was skipped.
- Confident gloss without citation marker — would indicate
  the answer schema was bypassed.

## Notes

Backfilled to `errors/` because the case is now the canonical
worked example for the `answer-q` pipeline AND for the
broader `llm-workflow.md` principles. Living document:
`research/2026-05-09-tweet-llm-comparison.md` carries the full
analysis and is kept in sync.

Recurrence flag `pattern-of-4` reflects four distinct LLM
runs on the same prompt all failing in the same architectural
shape (no citation, no source) even when they happened to land
near the right gloss.
