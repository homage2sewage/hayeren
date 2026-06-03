---
id: 2026-06-01-001
date: 2026-06-01
caught_by: dogfood
caught_during: review
severity: major
disposition: llm-error
category: citation-fabrication
subcategory: subagent-fabricated-and-mislabeled-citations
phenomenon: song-lyric-slang-glossing-via-delegated-subagents
related_topics:
  - topics/lexicon/yerevan_slang.md
related_pitfalls:
  - errors/2026-05-09-004-sov-gal-uncited-extrapolation.md
  - errors/2026-05-09-002-khot-slang-divergence.md
  - errors/2026-05-14-002-spurious-morpheme-decomposition-on-borrowed-toponym.md
status: mitigated
mitigation:
  type: doc-update
  ref: songs/README.md
recurrence: pattern-of-N
---

## Input

Processing the song Dav feat. Vnas — *Մյուս անգամ / Myus Angam*
into `songs/dav-vnas-myus-angam.md`. Verses 2 and 3 were translated
by two delegated `general-purpose` subagents, each instructed to
ground slang glosses in the corpus (`grep ghamoyan/out/full.jsonl`,
`query_kb.py`) and attach a citation (book + page) to every gloss
it could, marking the rest `prior`. The orchestrator then
integrated the returned sections into the song file.

## What the LLM produced

The subagents returned slang/lexicon glosses with corpus citations
that *looked* grounded and were integrated verbatim. Six were
wrong. A later whole-song **citation re-audit** agent (and a manual
`grep` re-check) found:

| item | citation as written | reality |
|---|---|---|
| `զսպել` "restrain" | parnasyan p354, **Cited** | not in corpus at all (p354 is a dict page `արեմուտք…բալ`) |
| `աչք ծակել` "be conspicuous" | parnasyan p440 / idiom list p63, **Cited** | not in corpus; the real attested idiom is `աչքի ընկնել` (parnasyan p183–184, `бросается в глаза`) |
| `կուսական` "virginal" | sakayan dict p383 | right page, **wrong book** — it is parnasyan p383 (absent from all of sakayan) |
| `լուսնկա` "moonlit" | parnasyan p438–440 | right page, **wrong book** — it is sakayan p438–439 (absent from parnasyan) |
| `սաղ` "all" (V2) | ghamoyan p44–46 | only p45 / p46 / p83; p44 has no `սաղ` |
| `բուսական` "herbal" | sakayan p357 + p486 | only p486; p357 is a grammar-tables page |

Two were pure fabrication (`զսպել`, `աչք ծակել` — no such entry
anywhere), two were right-page/wrong-book swaps (`կուսական`,
`լուսնկա`), two were page-range overstatements (`սաղ`, `բուսական`).
All six carried the **Cited** tag, indistinguishable in the file
from the dozen citations that *were* real.

## What was correct

The genuinely attested items (verified by grep): `ջոգել` ghamoyan
p48, `հավայի` p49, `քցել` p39, `ախպեր` p44, `տրաքած` p50, `մթոմ`
p60, `կրակ երեխա` p94, `սուս` p45/p96, `շուբ` p106, `ընգ`=`ընկ`
p39, `կոմ`=`կողմ` p37, `կոկոն` sakayan p498, `անցնել փողոցով`
parnasyan p179. The corpus does support a large fraction of the
glossing — which is exactly what made the six fabrications easy to
miss: they sat in a list that was mostly correct.

## Why this happened

Two compounding failures:

1. **The subagent failure is the workspace's recurring "assert
   without the cheapest verification" pattern** (cf.
   2026-05-09-004, 2026-05-14-002), here in its
   `citation-fabrication` surface: a slang word is glossed
   correctly from pre-training prior, then a *plausible* page
   number is attached to make it look grounded — sometimes the
   right page in the wrong book (the model "knew" the word was in a
   dictionary and guessed which one), sometimes a number with no
   basis. The gloss being *right* (e.g. `կուսական` does mean
   "virginal") masks that the *citation* is invented.

2. **The novel, delegation-specific failure: the orchestrator did
   not audit what the subagents returned.** The integration step
   trusted the subagents' `Cited` tags. A citation written by a
   subagent is no more trustworthy than one written inline — but
   the act of delegation created a false sense that grounding "had
   been done." The corpus citations were never re-grepped at
   integration time; they were only caught when a *dedicated*
   citation-audit agent was spawned in a later whole-song pass.

The cheapest check that would have caught all six:
`grep "<word>" <book>/out/full.jsonl` on each cited item — the same
one-line check the subagents were *told* to run and (for these six)
either skipped or hallucinated the result of. The topic-graph layer
already enforces this mechanically (`.claude/skills/citation-check`
greps every `verbatim_quote` against the cited page); the song
layer had no equivalent gate until this incident.

## Pattern membership

This extends the "structural assertion without baseline
verification" family (2026-05-09-004, 2026-05-11-001,
2026-05-14-001/002) into two new dimensions:

- **First `citation-fabrication`-category instance** logged in the
  workspace (prior entries were uncited *extrapolation* or
  prose-overreach; this is invented page numbers on a **Cited**
  tag).
- **First instance amplified by subagent delegation.** The lesson
  is not just "verify citations" but "**a delegated subagent's
  citations must be re-audited by the orchestrator** — delegation
  does not transfer trust." This is the load-bearing new rule.

## Mitigation

Immediate (all six fixed in `songs/dav-vnas-myus-angam.md`):
- `զսպել`, `աչք ծակել` → relabeled `prior` / transparent-standard;
  `աչք ծակել`'s meaning re-anchored to the attested synonym
  `աչքի ընկնել` (parnasyan p183–184).
- `կուսական`, `լուսնկա` → book corrected.
- `սաղ`, `բուսական` → page ranges corrected.
- The file's "Methodology" cited/prior summary and a new
  "Whole-song review (pass 2)" log section record the corrections.

Durable:
- `songs/README.md` step 7 now makes a **citation re-audit**
  (grep every cited page against the corpus — the song-domain
  analogue of `citation-check`) a **mandatory** part of the song
  routine, explicitly called out as the guard against this failure.
- `CLAUDE.md` § "Song / lyric processing" records the rule:
  *drafting subagents reliably fabricate plausible citations; the
  orchestrator must re-audit, delegation does not transfer trust.*
- This entry. `recurrence: pattern-of-N`.

## Test case

Future scenario:

> Orchestrate N subagents to gloss/translate Armenian content;
> each returns glosses tagged `Cited (book pN)`. Integrate the
> results.

Expected behaviour:

- Before treating any subagent-supplied citation as grounded,
  re-run `grep "<quote/word>" <book>/out/full.jsonl` (or the
  domain's `citation-check` analogue) on a sample — minimally on
  every `Cited` item that will be published.
- Flag any citation whose page does not contain the claimed
  word/sense; downgrade to `prior`.
- Treat right-word/wrong-book and page-range-overstatement as the
  *most likely* fabrication shapes (the gloss is correct, the
  locator is invented), not just whole-cloth invented sources.

Failure mode: integrating subagent output and trusting its `Cited`
tags without re-grepping, because "the subagent was told to ground
it."

## Notes

- Caught at review (a deliberately adversarial whole-song citation
  re-audit agent), before any human consumed the citations as
  fact, but after they were written into a published-surface file
  — hence `major`, not `minor`.
- The incident is a clean argument for the
  errors/-design goal (2): the same delegation pattern will be used
  for every future song, so the guard has to live in the routine,
  not in this conversation.
- Re-run `.claude/skills/error-log/` so `errors/INDEX.md` and
  `errors/BY-CATEGORY.md` regenerate.
