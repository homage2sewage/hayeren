# Answer-q pipeline — state, roadmap, decision triggers

Engineering roadmap for the citation-grounded Armenian-language
Q&A pipeline. Snapshot taken 2026-05-09. Use this file to resume
the work after a break, hand it off, or check whether a proposed
extension is in or out of scope.

## What this is

A local pipeline that takes an Armenian text (a question, tweet,
excerpt) and produces a citation-grounded answer where every
substantive claim resolves to a workspace-attested source —
topic file, project note, or book passage — and any uncovered
material is named as a gap.

Originated in response to the 2026-05-09 Pashinyan-tweet
comparison (`research/2026-05-09-tweet-llm-comparison.md`):
four LLMs (three external + one workspace-aware) confidently
produced four different glosses for `խոտ`; the correct citation
was sitting in the topic graph; nobody looked. The answer-q
pipeline makes "look first" mechanical instead of habitual.

## Pipeline at a glance

```
                ┌─────────────────────┐
   query text → │   query_kb.py       │  → bundle.md  (topic excerpts +
                │   (Phase 1)         │                 book passages +
                └─────────────────────┘                 declared gaps)
                          │
                          ▼
                ┌─────────────────────┐
   bundle.md → │   LLM, prompted     │  → answer.md  (structured schema:
                │   per SKILL.md      │                 reading + claims +
                │   (Phase 2)         │                 gaps + inline cites)
                └─────────────────────┘
                          │
                          ▼
                ┌─────────────────────┐
   answer.md → │  verify_citations.py│  → exit 0   (all cites resolve)
   bundle.md → │   (Phase 3)         │  | exit 1   (per-claim findings)
                └─────────────────────┘
```

## Status — 2026-05-09

| phase | what | status |
|-------|------|--------|
| 1 | `frequency/query_kb.py` — KB retrieval (grep-based) | **landed** |
| 2 | `.claude/skills/answer-q/SKILL.md` — answer protocol + schema | **landed** |
| 3 | `.claude/skills/answer-q/verify_citations.py` — target validation | **landed** |
| 4 | wiring (slash command / MCP) | open |
| 5 | embeddings retrieval | deferred |
| 5a | lemma-expansion via dictionary synonyms | deferred (mid option) |
| – | tightening: citation-content validation | deferred |

End-to-end demo verified on the Pashinyan tweet: bundle surfaces
6 topic-paths + 468 book-pages, structured answer cites 4 paths
+ 1 book-page, verifier resolves all and exits 0. Deliberately-
broken answer (`topics/lexicon/cutlery.md` + `ghamoyan p999`)
correctly emits 2 errors and exits 1.

## File map

| file | role |
|------|------|
| `frequency/query_kb.py` | retrieval (Phase 1) — input → bundle |
| `.claude/skills/answer-q/SKILL.md` | protocol + answer schema (Phase 2) |
| `.claude/skills/answer-q/verify_citations.py` | citation-target validator (Phase 3) |
| `CLAUDE.md` § "Before answering an Armenian-language question" | human-driven version of the protocol |
| `llm-workflow.md` | rationale for citation-grounded answering |
| `research/2026-05-09-tweet-llm-comparison.md` | the case study that motivated this pipeline |

## Phase 4 — wiring into Claude Code

Today's pipeline requires three shell commands:

```sh
python3 frequency/query_kb.py "<text>" > /tmp/kb-bundle.md
# (LLM produces /tmp/answer.md by reading the bundle)
python3 .claude/skills/answer-q/verify_citations.py \
    --bundle /tmp/kb-bundle.md --answer /tmp/answer.md
```

Phase 4 makes it one trigger.

### 4A — slash command

The `answer-q` skill already exists. Missing piece: registering
`/answer-q "<text>"` as a slash trigger. When fired, Claude reads
SKILL.md, runs query_kb via Bash, ingests the bundle, produces
the structured answer following the schema, runs verify_citations,
reports findings.

Pros: no new code; gives a conversational trigger immediately;
makes each pipeline step visible and challengeable in the
transcript. Cons: only works inside Claude Code sessions.

**Lowest-friction next step. Recommended first move.**

### 4B — MCP server

Stand up an MCP server exposing two tools:

- `query_kb(text: str) -> bundle: str`
- `verify_citations(bundle: str, answer: str) -> findings: list`

Pros: any Claude session in the workspace gets these as native
tools (inline, no shell-out); a non-Claude-Code consumer
(Anthropic SDK script, automation, web wrapper) can use the same
retrieval. Cons: needs MCP-server scaffold (Python or TypeScript),
lifecycle config in `settings.json`, refresh handling for the
underlying scripts when KB content changes.

**Do only after 4A proves the pipeline gets used.**

### 4 — decision trigger

Land 4A immediately if the slash command would actually be typed
in chat. Land 4B only when a non-Claude-Code consumer needs the
pipeline.

## Phase 5 — embeddings (deferred)

Today's retrieval is **substring-grep on lemmatised query
tokens**: broad-recall, high-precision when query content-words
exactly appear in topic bodies. Three under-recall patterns:

1. **Synonyms / paraphrase.** Query has `դանակ` "knife"; topic
   body uses `սուր առարկա` "sharp object" — grep misses.
2. **Concept-level questions.** "How do you form commands in
   Armenian?" has no Armenian content-word; nothing to grep.
3. **Cross-language queries.** Question typed in Russian /
   English about an Armenian phenomenon — no Armenian tokens.

Phase 5 adds a parallel retrieval path:

- Build sentence-level embeddings for each topic-file paragraph,
  each book-passage chunk, and each project-note section, via
  a multilingual embedding model (Anthropic-compatible API or
  local `sentence-transformers` multilingual).
- Store in a small vector index (FAISS or just a numpy array;
  the corpus is ~5K chunks, brute-force cosine works).
- At query time: embed the question, retrieve top-K, fold into
  the bundle alongside the grep hits.

Cost: model dependency (network call or local weights),
re-embed-on-change refresh script, cache-invalidation logic.

### Phase 5a — lemma-expansion (cheap middle ground)

For each query lemma, expand to its top-3 synonyms via the
existing kaikki dictionary; grep those too. Stays inside the
current architectural style — no embeddings, no model
dependency — and addresses the synonym/paraphrase problem
partially.

### 5 — decision trigger

Track a counter: every time the bundle comes back missing a
relevant topic *that exists in the workspace* (i.e. a
false-negative against the KB itself, not against the world).
At ≥5 instances → consider 5a; ≥10 instances → consider full 5.
Until then, today's grep is overshooting (broad recall) not
undershooting; both phases are speculative protection.

## Tightening — citation-content validation

`verify_citations.py` today does **target validation**: does the
cited path / page exist in the bundle? It does **not** do
**content validation**: does the cited file actually contain
what the answer claims?

Failure shape it can't catch today:

> Answer: "`խոտ` means 'agriculture' [topics/lexicon/yerevan_slang.md] [ghamoyan p48]"
> Verifier: ✓ path in bundle, ✓ page in bundle. Exit 0.

But the cited file says "naive / clueless person," not
"agriculture." Citation target is real; citation claim is
fabricated. Same shape as wiktionary's "Bats (language)" gloss
— confident wrong content under valid-looking surface form.

Implementation sketch:

1. Extend answer schema so each claim carries an explicit
   `quoted_text:` field (or extract claim predicates with NLP;
   former is more reliable).
2. For each claim, look up the citation target in the bundle.
3. Substring-match (or fuzzy-match) the claim's predicate
   against the cited target's content.
4. No match → `unsupported-content` finding.

This mirrors `citation-check`'s topic-frontmatter verifier
(verbatim-quote fragments must appear in the source JSONL) —
same machinery, different direction.

### Decision trigger

Do only after observing real content-hallucination cases in Q&A
use. The answer pipeline already reduces hallucination
substantially because the LLM sees the bundle and can read what
each cited target actually says. Most claims correctly mirror
their cited content. The silent-failure shape (correct target,
wrong predicate) is rare relative to old-school no-bundle
hallucination — but not zero. Until ≥3 real instances are
logged, target validation is sufficient.

## Anti-scope

Things explicitly out of scope for this pipeline:

- **Generative authoring.** answer-q is for Q&A on existing KB
  content. Topic-file authoring uses the topic-walk workflow
  (`walks/`), not this skill.
- **Multi-turn conversation memory.** Each invocation is
  stateless; each question gets its own bundle. If a follow-up
  needs context from a previous turn, the user re-asks with
  enough text for query_kb to extract lemmas.
- **Translation as a primary task.** answer-q can answer "how
  do we translate this?" but the value is in *grounding the
  translation in cited evidence*, not in producing translations
  themselves. For pure translation without grounding, just
  prompt directly.
- **Russian / English Q&A about Armenian.** Phase 5 (embeddings)
  is the path to handling cross-language queries; until then,
  query_kb only retrieves on Armenian content-words.

## Open questions parked for later

- **Bundle size.** Today's bundle for a 9-token query is ~3500
  lines. Mostly fine inside an LLM context window (1M tokens
  available) but wasteful. A "compact" mode that drops
  low-relevance topic excerpts is easy to add when the
  context-bloat actually starts mattering.
- **Multi-script input.** A query mixing Latin-transliterated
  Armenian + native script doesn't cleanly tokenise.
  `transliteration-notes.md` defines the back-trans heuristic;
  wiring it as a query_kb pre-pass is doable.
- **Bundle hash / caching.** Re-running `query_kb.py` on the
  same text re-greps everything. Caching by text-hash would
  help iteration; not a priority while the corpus is small.
- **Multi-question / multi-turn evaluation.** No corpus of
  realistic Q&A inputs exists yet; once we accumulate ~30
  real questions answered through the pipeline, that becomes
  the regression set.

## How to resume this work

1. **Read this file first.** It's the snapshot.
2. **Read `.claude/skills/answer-q/SKILL.md`** for the protocol +
   answer schema. The SKILL.md is what's actually executed.
3. **Run a sanity check:** `python3 frequency/query_kb.py "հա
   լավ էսքան խոտ մարդ ըլնի մի հատ էլ պալիտիկ" | head -50`.
   The bundle should surface `topics/lexicon/yerevan_slang.md`
   and `topics/morphology/dialectal_lnel.md`. If not, something
   regressed in retrieval — start there.
4. **Pick a phase off the table above.** Each is independent;
   Phase 4A is the natural next move.
5. **Update this file** when a phase lands or a new failure mode
   becomes visible. Keep the status table accurate; that's the
   first thing future-you will look at.

## Cross-references

- `kb-design.md` — broader agent-flow design; this pipeline is
  one Phase of the agent-workflow plan there.
- `llm-workflow.md` — citation-grounded-answering rationale,
  worked-example list (this pipeline is the durable response
  to the Pashinyan-tweet failure).
- `CLAUDE.md` — the human-driven version of the protocol;
  Phase 4A automates the slash-command form of it.
- `research/2026-05-09-tweet-llm-comparison.md` — the case study
  that motivated this pipeline; future regression-test fodder
  ("can the answer-q pipeline answer this tweet correctly?").
