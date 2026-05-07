# Knowledge-base design — multi-book Armenian KB + agent workflow

Living design doc for the multi-book Armenian knowledge base and the
agent-driven research workflow over it. Updated after every design
iteration; **change log at the bottom**.

> **Publishing note.** This workspace may be made public in the future.
> Topic, walk, and skill files must not reference other
> `~/work/<project>` directories, personal repos, or private notes —
> cite only public sources and in-tree files.

## Goal

Move from "AI explains Armenian based on its training data" to
**answers grounded in cited textbook passages**. Support multiple books
(textbooks, dialect treatments, grammars), surface contradictions and
register differences across them, and detect what's missing so we know
what book to add next.

Driven entirely from Claude Code sessions — no separate CLI.

## Inputs as of 2026-05-07

- `sakayan/out/full.jsonl` + `full.md` — clean Unicode extraction of
  Dora Sakayan, *Eastern Armenian for the English-Speaking World*
  (2007). 558 pp, layout-preserving JSONL with `(page, font, size,
  x, y, text)` per span.
- `sakayan/units.json` — auto-detected manifest of all 11 units, with
  `page:y` bookmarks for each dialogue.
- `sakayan/lookup.py` — Wiktionary lookups, cached to `.cache/lookup/`.
  Returns IPA, definitions, inflection-template pointers.
- `armenian-grammar.md` — distilled linguistic notes with explicit
  citations into Sakayan (p18 phonology, p35–37 verbs, p354–355 +
  p359 paradigms). Already a topic-graph in embryonic form; being
  split into `topics/` (4 topics extracted as of 2026-05-07).
- `grammar-terms.md` — trilingual grammar-term glossary
  (English / Armenian / Russian). Confirms Russian as an L1 in scope
  for contrastive notes; the Armenian↔Russian case-mapping rows are
  particularly useful for `topics/morphology/case.md`-style topics.
- `anki-design.md` — card design decisions + request log.
- `armenian-vocab-research.md` — research base on flashcard methodology.

**Books extracted** (top-level book dirs; see Phase 0 of the ghamoyan
integration plan for the layout decision):

- `sakayan/` — Dora Sakayan, *Eastern Armenian for the English-Speaking
  World* (2007). 558 pp. Eastern-standard dialect, prescriptive
  pedagogy, contrastive with English.
- `ghamoyan/` — Ghamoyan, Sargsyan & Kartashyan, *Yerevan's Colloquial
  Language* (2014). 118 pp. Yerevan colloquial, descriptive
  linguistic study, contrastive with the literary norm. Integrated
  into `topics/` 2026-05-07.
- `parnasyan/` — Parnasyan & Manukyan, *Самоучитель армянского
  языка* (Russian-language self-teacher of Armenian, Луйс, Yerevan
  1990). 431 book pages, scanned as 215 double-page-spread images.
  Eastern-standard, prescriptive-pedagogy, Russian-L1 contrastive.
  OCR-extracted via tesseract (`-l rus+hye`); avg confidence 80.1.
  Integrated into 3 topics 2026-05-07 (the 3 prescriptive-norm
  topics — yerevan_consonant_reductions and colloquial_copula_a are
  pure colloquial and parnasyan doesn't address them).
- `tioyan/` — Tioyan, Grigoryan & Urutyan, *Самоучитель армянского
  языка / Հայերենի ինքնուսույց* (Zangak-97, Yerevan 2007). 393 pp.
  Eastern-standard, prescriptive-pedagogy, Russian-L1 contrastive.
  More recent than parnasyan; comprehensive 43+ lesson coverage.
  Manifest written; OCR pipeline ready (`tioyan/extract.py`); not
  yet run.

## Storage shape

Six kinds of artefacts, each with different mutability rules:

| Kind | Where | Edited by | Citation role |
|------|-------|-----------|---------------|
| Raw extraction | `books/<name>/out/full.jsonl` | extractor only | atomic citation target: `book + page + y_range` |
| Book metadata | `books/<name>/manifest.yaml` | human, rarely | `dialect`, `register`, `audience`, `year` — drives source weighting |
| Topics | `topics/<domain>/<phenomenon>.md` | human + agent | the synthesis layer; the thing answers cite |
| Lexicon | `lexicon/<lemma>.md` | agent, human reviews | per-word artefact (definitions, paradigm, source occurrences) |
| Walks | `walks/YYYY-MM-DD-<kind>-<book>.md` | agent, append-only | plan files for any change to `topics/` or `lexicon/` |
| External research | `research/YYYY-MM-DD-<slug>.md` | session-level | book candidates, papers, web sources → cited from topics |

```
hayeren/
├── INDEX.md
├── kb-design.md                    # this file
├── armenian-grammar.md             # to be split into topics/
├── anki-design.md
├── armenian-vocab-research.md
├── books/
│   └── sakayan/                    # current top-level sakayan/ moves here
│       ├── manifest.yaml
│       ├── out/full.jsonl
│       └── ...
├── topics/
│   ├── INDEX.md
│   ├── phonology/
│   ├── morphology/
│   ├── syntax/
│   └── pragmatics/
├── lexicon/<lemma>.md
├── walks/
├── research/
└── .claude/skills/
    ├── topic-walk.md
    ├── discovery-walk.md
    ├── gap-walk.md
    ├── citation-check.md
    └── critic-pass.md
```

### Decisions

- **Linguistic-domain organisation** for `topics/` (chosen 2026-05-07,
  over pedagogy/unit organisation). Pedagogy is captured via topic
  frontmatter `units: [sakayan:1, sakayan:2]` so unit-driven study
  still works.
- **Atomicity**: each topic file ~300 lines max — agent can rewrite
  atomically without re-reasoning the whole grammar.
- **Provenance is mechanical**: every claim points to a JSONL span.
  `verbatim_quote` is load-bearing — a verifier agent re-greps
  `out/full.jsonl` and asserts the quote exists at the cited locus.
  Hallucinated citations get caught mechanically.
- **No vector DB / RAG.** Markdown + grep + frontmatter outperforms
  retrieval at this scale (<10k docs). Revisit only if grep+frontmatter
  measurably fails.

### Topic frontmatter schema

```yaml
---
topic: voiced↔aspirated alternation
domain: phonology
units: [sakayan:1, sakayan:2]
related: [three-way-laryngeal-contrast, digraph-ou]
status: draft                      # draft | reviewed | stable
attestation: single-source         # single-source | multi-attested | conflicting
sources:
  - id: 1
    book: sakayan
    page: 18
    y_range: [300, 320]
    verbatim_quote: "The EA three-part consonant system consists of one voiced stop"
    supports: supported            # supported | partially-supported | unsupported | uncertain
    note: prose statement of the three-way distinction.
  - id: 2
    book: sakayan
    page: 30
    y_range: [520, 540]
    verbatim_quote: ["ընդունել", "§nt", "unel]"]   # fragment list — stitched across span boundaries
    supports: partially-supported
    note: vocab line; nt^h transliteration witnesses դ→թ. Sakayan does not state the rule.
gaps:
  - "Sakayan doesn't characterise the alternation phonologically..."
---
```

Field reference:

- **`id:`** — integer used for `[#N]` references in the body prose.
- **`verbatim_quote:`** — either a string (single substring to find in
  the y_range) **or a list of fragments** (each must appear in the
  stitched text of the y_range). The fragment list is needed because
  Sakayan's transliteration glyphs with diacritics get split across
  multiple JSONL spans — `[§ntʰunel]` lives as `[§nt` + `unel]` in
  two `Armtrans` spans. **The fragments must be the literal bytes
  in the JSONL** — not a linguistic gloss, not an IPA rendering. If
  the JSONL has `[§nt` (with the aspiration encoded as a glyph layout
  and no Unicode `ʰ` codepoint), the fragment must be `§nt`. Glosses
  and IPA renderings belong in `note:` or in the body prose, not in
  `verbatim_quote`.
- **`y_range: [lo, hi]`** — bounding box bottom-y range covering the
  cited region. Lines in Sakayan are ~14pt apart; a 10–20pt window
  per source is typical, wider for multi-line prose.
- **`supports:`** — per-source verification axis (SemanticCite four-class).
- **`note:`** — *why* this source supports the claim and any stitching
  / interpretation caveats.

Topic-level:

- **`attestation:`** — cross-source agreement axis. `conflicting` is
  the interesting case (standard-vs-colloquial, prescriptive-vs-
  descriptive contrasts).

Two orthogonal confidence dimensions:

- **`supports:` (per-source)** — does the verbatim quote actually support
  the claim it's attached to? Uses the SemanticCite taxonomy
  (`supported` / `partially-supported` / `unsupported` / `uncertain`).
  This is what the CitationAgent verifies mechanically.
- **`attestation:` (topic-level)** — how many independent sources agree?
  `single-source` (only one book treats this), `multi-attested`
  (multiple books agree), `conflicting` (books disagree — usually
  signals a register/dialect difference worth flagging in the body).

Conflicting attestation is the *interesting* case — it surfaces exactly
the standard-vs-colloquial / prescriptive-vs-descriptive contrasts the
multi-book setup is designed to expose.

## Workflow patterns

Mapped from modern agent practice (see References). The patterns
adopted, in priority order:

**1. Plan-then-act.** Every walk writes a plan file in `walks/` before
touching `topics/`. Plan files are markdown with proposed diffs; human
accepts/rejects; a second pass commits. Audit trail + checkpoint, no
silent edits.

**2. Orchestrator-worker.** Walks decompose into per-book / per-chapter
subagents:
- *Topic walk*: orchestrator reads `topics/INDEX.md`, spawns one
  subagent per book to scan for that phenomenon, merges into the
  topic MD.
- *Discovery walk*: one subagent per chapter of a new book, surfacing
  content not yet covered by any topic.
- *Gap walk*: one subagent per topic to score completeness against a
  rubric and propose additions to `gaps:`.

**3. CitationAgent (strongest single pattern for this project).** A
*separate* agent re-attaches every claim to a verbatim source span
post-hoc. Schema borrowed from Anthropic's multi-agent research
write-up: `{claim, source_id, locator, verbatim_quote, confidence}`.
The verbatim quote is what makes verification mechanical.

**4. Evaluator-optimizer.** Critic pass before merge. Rubric: every
claim has `book:page`; examples carry script+translit+gloss; no
contradictions with sibling topics; dialect tag matches manifest.

**5. Agentic engineering (Karpathy, Sequoia AI Ascent 2026).** "Vibe
coding" is obsolete; the programmer is now an *orchestrator of agents*.
Dec 2025 was the inflection point where chunks got coherent enough that
trust shifts from line-by-line review to plan-and-spec review. Loops
stay small — agent proposes a topic diff, human accepts in ~10 seconds.

**6. Harness engineering / context engineering (Karpathy + Anthropic).**
The substrate is the harness's *configuration points* — what files load
into context, what tools are available, what skills the agent
discovers. `topics/INDEX.md` + per-topic frontmatter is the curated
context for each walk; `.claude/skills/` is the procedural layer; the
union of those two is the harness for this project.

**7. External-research handoff (deep-research pattern).** Long-horizon
"what book do I need next" runs as a *separate* task with a strict
output schema (`{resource, type, target_topics, license, why_relevant}`);
a second pass merges accepted entries into `research/`. Don't
interleave discovery and curation.

### Skipped (overhyped at this scale)

- Vector embeddings / RAG — see decision above.
- GraphRAG, LangGraph state machines, agent frameworks.

## References

Verified URLs as of 2026-05-07 (web search was blocked from the
agent-flow research subagent on the first pass; second pass run from
parent context with WebSearch enabled).

**Anthropic engineering blog**:
- "Building Effective Agents" (Dec 2024) — workflow vs. agent patterns;
  orchestrator-worker, evaluator-optimizer, prompt chaining.
  https://www.anthropic.com/engineering/building-effective-agents
- "How we built our multi-agent research system" (Jun 2025) —
  orchestrator → parallel subagents → CitationAgent. The claim schema
  is from here.
  https://www.anthropic.com/engineering/multi-agent-research-system
- "Effective harnesses for long-running agents" (late 2025) —
  configuration points, context-window management, working across
  multiple context windows.
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- "Harness design for long-running application development" (early 2026)
  — multi-agent harness, frontend + long-running autonomous SE.
  https://www.anthropic.com/engineering/harness-design-long-running-apps
- "Equipping agents for the real world with Agent Skills" — Skills are
  now an **open standard** (Claude Code, Codex, OpenCode, Gemini CLI,
  Cursor). Authoritative reference for `.claude/skills/<name>.md`.
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- *Agentic Coding Trends Report 2026* (Anthropic PDF).
  https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf

**Karpathy**:
- "Software Is Changing (Again)" — YC AI Startup School keynote
  (Jun 2025). Software 3.0, context window as RAM.
  https://www.youtube.com/watch?v=LCEmiRjPEtQ
- *Sequoia AI Ascent 2026 keynote* — "Agentic Engineering" supersedes
  vibe coding. Dec 2025 = inflection point for agentic coding;
  programmer as orchestrator. (Bearblog summary written by Karpathy:
  https://karpathy.bearblog.dev/sequoia-ascent-2026/)

**Citation verification**:
- *SemanticCite* (arXiv 2511.16198, Nov 2025) — four-class
  classification (Supported / Partially Supported / Unsupported /
  Uncertain) for claim-source relationships. Source for the
  `supports:` field taxonomy in the topic schema.
  https://arxiv.org/html/2511.16198v1
- Deep-research citation conventions (industry standard in 2026):
  `[HIGH CONFIDENCE]` (≥3 independent sources agree),
  `[CONFLICTING - INVESTIGATE]` (sources disagree),
  `[UNVERIFIED - NEEDS CONFIRMATION]` (single source). Source for the
  `attestation:` field.

**Direct precedents for this project**:
- Karpathy's *LLM Wiki* — turn raw documents into a structured
  markdown KB Claude can query. The clearest one-shot precedent for
  what we're building. (MindStudio writeup:
  https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code)

**External research**:
- OpenAI Deep Research (Feb 2025) — external-research handoff pattern.
  https://openai.com/index/introducing-deep-research/

## Open / next steps

**Topics under `topics/` as of 2026-05-07 (post-parnasyan walk):**

| topic | domain | sources | status | attestation |
|-------|--------|---------|--------|-------------|
| voiced_aspirated_alternation | phonology | sakayan p18,30,36,42 + ghamoyan p39 | draft | multi-attested |
| three_way_laryngeal_contrast | phonology | sakayan p18 + ghamoyan p39 + **parnasyan p21** | draft | multi-attested |
| yerevan_consonant_reductions | phonology | ghamoyan p37,38 | draft | single-source |
| present_tense | morphology | sakayan p36 + ghamoyan p73 + **parnasyan p30,31,32** | draft | multi-attested |
| colloquial_copula_a | morphology | ghamoyan p73 | draft | single-source |
| pro_drop | syntax | sakayan p36,71 + ghamoyan p79,80 + **parnasyan p49** | draft | multi-attested |

All six pass `citation-check` (**117/117 fragments verified** — 15
new from parnasyan) and `critic-pass` phase-1 lint
(0 errors / 0 warnings).

**Next moves:**

- ~~**Active plan**: ghamoyan integration~~ — **executed 2026-05-07.**
  All three documented phases (manifests + topic walk + discovery
  walk) complete; lexicon phase deferred. The two highest-priority
  discovery-walk candidates have been written:
  `topics/morphology/colloquial_copula_a.md` (the `ա↔է` register
  marker, ghamoyan p73) and `topics/phonology/yerevan_consonant_reductions.md`
  (cluster reductions, imperative ր-drop, ղ-drop, final լ/ս-drop,
  loanword s-voicing — ghamoyan p37–38). Both single-source
  (ghamoyan only); both pass citation-check and lint.

- **Russian-language source acquisition**: candidate list at
  `research/2026-05-07-russian-language-sources.md`. Top
  recommendation: **Parnasyan & Manukyan (1990), *Самоучитель
  армянского языка*** — explicitly Armenian-Russian contrastive.
  Backup: Markosyan (2003/2013), *Крунк Айастани*. Acquisition
  decision pending.
- **Continue splitting `armenian-grammar.md`** in parallel where
  cheap. Remaining candidates:
  `topics/phonology/punctuation.md`,
  `topics/morphology/verb_classes.md` (Sakayan p35–36),
  `topics/morphology/irregular_verbs.md` (Sakayan p37),
  `topics/morphology/participles.md` (Sakayan p359),
  `topics/morphology/negation.md`.
- **Walk skills** (still to write): `topic-walk`, `discovery-walk`,
  `gap-walk`. Per the ghamoyan plan, do 1–2 walks manually before
  skill-ifying so the scaffolding reflects what actually worked.
- **Subagent web access**: WebSearch / WebFetch blocked from
  `general-purpose` subagents; works in parent. Either run web
  research from parent or investigate `~/.claude/settings*.json` to
  enable subagent web tools.

**Done:**

- `citation-check` — `.claude/skills/citation-check/{SKILL.md, check.py}`.
  Verified across 4 topics, 60/60 fragments. Caught a real
  author-side bug on first run (gloss-vs-bytes).
- `critic-pass` (mechanical phase + agent rubric) —
  `.claude/skills/critic-pass/{SKILL.md, lint.py}`. Validates
  frontmatter schema, source consistency, body `[#N]` references,
  attestation/source-count consistency. SKILL.md carries the
  agent-side editorial rubric (8 items) for the Phase-3 review pass.

## Change log

- **2026-05-07** — initial design after first conversation. Decisions:
  topic schema with verbatim-quote citations, plan-then-act + walks/,
  orchestrator-worker for walks, CitationAgent + critic verifier
  passes, linguistic-domain organisation for `topics/`, no
  vector-DB/RAG. WebSearch was blocked from the agent-flow research
  fork — sources below are from internal knowledge, pending
  verification + Dec 2025+ updates.
- **2026-05-07 (later)** — re-ran agent-flow research with WebSearch
  enabled from parent context (subagent web tools are still blocked).
  Updates: (a) citation taxonomy refined to two orthogonal axes —
  per-source `supports:` (SemanticCite four-class) + topic-level
  `attestation:` (single-source / multi-attested / conflicting);
  (b) Karpathy reference updated from Software 3.0 / "Software Is
  Changing" to Sequoia AI Ascent 2026 "Agentic Engineering" framing
  (Dec 2025 = inflection point); (c) References section verified
  with live URLs and expanded with late-2025/2026 Anthropic harness
  posts, Agent Skills (now an open standard), SemanticCite, and
  Karpathy's LLM Wiki as direct precedent; (d) workflow pattern #6
  reframed as "harness engineering" — `topics/INDEX.md` + frontmatter
  + `.claude/skills/` *is* this project's harness.

- **2026-05-07 (schema test)** — first topic file written:
  `topics/phonology/voiced_aspirated_alternation.md`, 4 cited Sakayan
  sources (p18 prose + p30/p36/p42 examples). Manual citation check
  passed all 11 fragments. Schema refinements adopted:
  (a) **`id:`** field on each source for `[#N]` body references;
  (b) **`verbatim_quote:` may be a list of fragments**, not just a
  string — needed because Armtrans transliteration glyphs split across
  JSONL spans (e.g. `[§ntʰunel]` lives as `[§nt` + `unel]`); citation
  check stitches spans within `y_range` then substring-matches each
  fragment;
  (c) **`note:`** field on each source captures interpretation caveats
  (especially "claim is implicit, witnessed by transliteration column");
  (d) added Russian-L1 contrastive notes (per `grammar-terms.md`)
  alongside English-L1 — the `contrastive_notes:` content stays in
  body prose for now, not yet a structured frontmatter field.

- **2026-05-07 (citation-check packaged)** — first walk skill landed
  at `.claude/skills/citation-check/{SKILL.md, check.py}`. The script
  resolves `book:` slugs via `find_project_root()` (walks up looking
  for `kb-design.md`), tries `books/<name>/out/full.jsonl` then the
  legacy top-level path, NFC-normalises before matching, supports both
  string and fragment-list `verbatim_quote`, and emits human or
  `--json` output. Dependency: `pyyaml` 6.0.3 added to `sakayan/.venv`
  (will hoist to a project-wide venv once a second book lands).
  **Schema rule clarified by first run**: `verbatim_quote` fragments
  must be the literal bytes in the JSONL, not linguistic glosses or
  IPA renderings. The first run caught my own gloss-vs-bytes confusion
  on the alternation topic — proof that the skill earns its keep on
  the very first invocation. After fix: 10/10 fragments verified,
  exit 0.

- **2026-05-07 (width pass)** — three more topics split from
  `armenian-grammar.md`:
  `topics/phonology/three_way_laryngeal_contrast.md` (Sakayan p18,
  3 sources, 15 fragments — the parent of the alternation topic);
  `topics/morphology/present_tense.md` (Sakayan p36, 4 sources,
  27 fragments — schematic chain + full paradigm + example
  sentences); `topics/syntax/pro_drop.md` (Sakayan p36 footnote +
  p71 example, 2 sources, 8 fragments). Discovered: Sakayan's p36
  footnote is a *direct* statement of pro-drop, which we'd have
  considered uncited otherwise. All three pass citation-check
  cleanly. Schema scales unchanged across phonology / morphology /
  syntax.

- **2026-05-07 (critic-pass packaged)** — second skill landed at
  `.claude/skills/critic-pass/{SKILL.md, lint.py}`. Three-phase
  design: phase 1 mechanical lint (frontmatter schema, [#N] refs,
  attestation/source-count consistency) via lint.py; phase 2
  delegates to citation-check; phase 3 is an agent-side editorial
  rubric (8 items: provenance, examples format, gap specificity,
  cross-ref resolution, attestation honesty, vibes vigilance, L1
  contrastive coverage, prose arc). All 4 existing topics pass
  phase-1 lint clean (0/0/0).

- **2026-05-07 (ghamoyan landed)** — second book extracted by user
  while design work was in progress: `ghamoyan/` (Ghamoyan,
  Sargsyan, Kartashyan, *Yerevan's Colloquial Language*, 2014, 118
  pp). ARMSCII-8 encoding (cleaner than Sakayan's custom-font
  scheme); decoder at `ghamoyan/armscii.py`. This *replaces*
  Dum-Tragut as the recommended next source — ghamoyan occupies the
  colloquial-register slot Sakayan deliberately omits, which is a
  higher-value contrast than a typological reference grammar would
  be at this stage. Integration plan drafted at
  `walks/2026-05-07-ghamoyan-integration-plan.md`. Layout decision
  made: book directories live at top level (drop the `books/<name>/`
  wrapper from earlier sketches; citation-check already accepts
  both, so no code change needed).

- **2026-05-07 (parnasyan OCR + topic walk)** — OCR'd parnasyan
  end-to-end (430 book pages from a 215-image double-page-spread
  scan; tesseract `-l rus+hye --psm 4`; avg confidence 80.1; runtime
  ~50 min). Output at `parnasyan/out/{full.jsonl, full.md}`,
  16,886 line records. Topic-walked against the 6 existing topics —
  walk plan at `walks/2026-05-07-topic-walk-parnasyan.md`. Three
  topics gained parnasyan sources: three_way_laryngeal_contrast (p21
  — Russian-contrastive enumeration of consonant-system differences),
  present_tense (p30,31,32 — auxiliary paradigm + 3 explicit Russian
  contrasts including "связка всегда присутствует" literary baseline),
  pro_drop (p49 — explicit Russian-L1 contrastive claim that
  1st/2nd-person subjects can be dropped *even in the past tense*,
  unlike Russian). Three colloquial-only topics correctly didn't
  gain parnasyan sources. After: 117/117 fragments verify, lint
  clean across all 6 topics. The Russian-L1 contrastive notes in
  the affected topics moved from agent-paraphrased to book-cited.

  **OCR quality observations**: Russian-language fragments OCR at
  90%+ confidence — citable as-is. Armenian-script fragments show
  voiced-stop confusions (գ↔դ, etc.) typical of tesseract's
  Armenian model, around 70-80% accuracy. Strategy: prefer
  Russian-language quotes when available; for Armenian-script
  citations from parnasyan, use shorter fragments and visual
  verification.

  **Layout caveat**: parnasyan.pdf is double-page-spread; each
  PDF image-page covers two book pages side-by-side. extract.py
  splits at the centerline before OCR. tioyan.pdf is single-page;
  its extract.py omits the split.

- **2026-05-07 (two new colloquial topics + Russian source research)**
  — wrote the two highest-priority discovery-walk candidates as
  topic files: `topics/morphology/colloquial_copula_a.md` (4
  fragments verify, single-source ghamoyan) and
  `topics/phonology/yerevan_consonant_reductions.md` (23 fragments,
  five sub-phenomena: cluster reduction, imperative ր-drop, ղ-drop,
  final լ/ս-drop, loanword s-voicing). Total topics: 6; total
  citation-check fragments: 102/102 verified; lint clean (0/0/0)
  across all 6 files.

  Separately, ran web research for a Russian-language source —
  output at `research/2026-05-07-russian-language-sources.md`. Top
  candidate: **Parnasyan & Manukyan (1990), *Самоучитель армянского
  языка*** (Луйс, Yerevan, 431 pp), explicitly Armenian-Russian
  contrastive, with phonological + grammatical comparison built in.
  Acquiring this would convert most current Russian-L1 contrastive
  notes from agent-paraphrased to book-grounded, and would give the
  project a third pillar (English-contrastive / Armenian-descriptive /
  Russian-contrastive). Acquisition pending user decision.

- **2026-05-07 (ghamoyan integration executed)** — full-pass
  integration of ghamoyan into the existing `topics/` tree.
  Manifests written: `sakayan/manifest.yaml`,
  `ghamoyan/manifest.yaml`, schema-fields `dialect`, `register`,
  `audience`, `contrastive-with`, `extraction.{jsonl,md,encoding}`,
  `structure`. Topic walk: read ghamoyan Chapter 2 (phonology, pp.
  35-40) and Chapter 4 (grammar, pp. 70-91) in full; identified one
  ghamoyan source per topic (two for pro_drop). Walk plan at
  `walks/2026-05-07-topic-walk-ghamoyan.md`; merged into all 4
  topic files. All four flipped from `single-source` to
  `multi-attested`. Verification: 75/75 verbatim fragments verify
  via citation-check (up from 60); 0/0/0 lint findings. Discovery
  walk: ~10 candidate new topics catalogued at
  `walks/2026-05-07-discovery-walk-ghamoyan.md` — high-priority
  picks `colloquial_copula_a`, `yerevan_consonant_reductions`,
  `yerevan_vowel_reductions`, `sentence_member_elision`,
  `diphthong_simplification`. Substantive findings folded into
  topics: (a) ghamoyan reframes Sakayan's lexically-irregular
  voiced↔aspirated alternation as part of a broader bidirectional
  dialect-influenced shift among the three series; (b) the three-way
  contrast as a *system* persists in Yerevan colloquial — only
  lexeme membership shifts; (c) Yerevan colloquial generalises
  pro-drop to "all sentence members" — subject, predicate,
  complements, auxiliary, copula; (d) the single most recognisable
  colloquial register marker is 3sg `ա` replacing literary `է` in
  both copular and auxiliary uses (`գրում ա` for `գրում է`). Schema
  unchanged — survived the second pressure test cleanly.
