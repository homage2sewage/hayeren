---
name: answer-q
description: |
  Citation-grounded answering for Armenian-language questions
  about specific words, phrases, grammar phenomena, or short
  texts. Composes `frequency/query_kb.py` (KB retrieval) with a
  constrained answering protocol and `verify_citations.py`
  (post-answer validation). Use whenever the user asks "what
  does X mean / how does Y work / translate Z" — anywhere a
  pre-training-prior answer could plausibly be wrong about
  Armenian-specific content.
---

# answer-q

The Phase-2 wrapper that operationalises
`CLAUDE.md` § "Before answering an Armenian-language question."
Three steps: retrieve, answer, verify. Each step has a separate
artefact. The protocol is what's enforced; the LLM filling in
the answer step is whatever's running the conversation.

## When to invoke

Trigger on any Armenian-language question, especially:

- "What does <word> mean?" / "translate <text>" / "what's
  the difference between X and Y?"
- "Why does Y use <form> here?" / "is this colloquial /
  literary / dialectal?"
- "Is <expression> idiomatic? where does it come from?"
- Inputs that mix scripts (Latin transliteration, Cyrillic
  code-switching) and need register / register-marker analysis.

Skip if the question is purely conversational ("how's the
project going") or about workspace tooling (these don't need
KB grounding).

## Protocol

### Step 1 — retrieve

```sh
python3 frequency/query_kb.py "<armenian text>" > /tmp/kb-bundle.md
```

Or, for a longer source text:

```sh
python3 frequency/query_kb.py --file path/to/text.md > /tmp/kb-bundle.md
```

The bundle has four sections:

- **Lemmas extracted** — what was tokenised + lemmatised from
  the input.
- **Matched topic files** — citation-checked syntheses, with
  excerpts around each lemma hit.
- **Matched project notes** — `armenian-grammar.md`,
  `transliteration-notes.md`, `grammar-terms.md` excerpts.
- **Matched book passages** — page + y-range + raw text from
  the four extracted books.
- **Gaps** — query-lemmas with zero KB coverage. Anything
  about these terms in the answer must be flagged
  `gap: pre-training prior, no KB source`.

### Step 2 — answer

Produce a structured Markdown response using **only** the
bundle as evidence. Schema:

```markdown
# Answer

## Reading

<one-paragraph plain-prose translation / explanation. Each
substantive claim ends with an inline citation marker like
`[topics/lexicon/yerevan_slang.md]` or `[ghamoyan p48]`. No
uncited substantive claims.>

## Claims

- **<short claim text>** — citation: `<path or book-page>` —
  confidence: `cited` / `single-source` / `gap`
- **<another claim>** — citation: `…` — confidence: `…`

## Gaps

<list of bundle's "Gaps" lemmas plus any claim-level gaps
encountered. Each line: `<token> — <one-sentence reason it
matters / what would close the gap>`. If no gaps, say so.>
```

Hard rules:

- **Every substantive claim has a citation** to a path/page in
  the bundle.
- **Every gap is named explicitly.** No confident pre-training
  prose for things the bundle doesn't cover.
- **Confidence grading is honest.** "cited" only if the bundle
  has a verbatim or near-verbatim source for the claim;
  "single-source" if exactly one source backs it;
  "gap" if it's not in the bundle.
- **No reasoning that bypasses the bundle.** If the bundle
  doesn't have it and pre-training does, that's a gap, not a
  claim.

### Step 3 — verify

```sh
python3 .claude/skills/answer-q/verify_citations.py \
    --bundle /tmp/kb-bundle.md \
    --answer /tmp/answer.md
```

Fails if:

- A citation in the answer points to a source not in the bundle.
- A citation's quoted text doesn't appear at the cited location.
- A "gap" claim is in fact covered by the bundle (you missed
  a citation that was there).

Exit code 0 = all citations check out. Non-zero = rewrite
the answer's offending parts.

## Worked example — the Pashinyan tweet

Input:

```
հա լավ էսքան խոտ մարդ ըլնի մի հատ էլ պալիտիկ 🤭😅
```

Step 1 — `python3 frequency/query_kb.py "հա լավ էսքան…"`
produces a bundle that surfaces (among others):

- `topics/lexicon/yerevan_slang.md` — `խոտ` "naive / clueless
  person" (ghamoyan p48).
- `topics/morphology/dialectal_lnel.md` — `ըլնել` as
  `(գավառական)` copula per bararan.am.
- `topics/lexicon/code_switching_with_russian.md` —
  Russian-loan pattern; `պալիտիկ` documented on the page.
- ghamoyan p48 raw passage attesting `խոտ`.

Step 2 — Answer:

```markdown
# Answer

## Reading

`խոտ` here is colloquial Yerevan slang for **"naive / clueless
person"**, a metaphor from literal "grass" [topics/lexicon/yerevan_slang.md]
[ghamoyan p48]. The 3sg subjunctive `ըլնի` is a regular form of the
**dialectal verb ըլնել** "to be" (literary `լինել`)
[topics/morphology/dialectal_lnel.md]. `պալիտիկ` is a Russian-loan
colloquial spelling of *политика*, register-marked as casual /
mocking [topics/lexicon/code_switching_with_russian.md].

Reading: "*how can a person be this clueless — and a politician
on top of that 🤭😅*." Sarcastic dunk on Pashinyan as personally
clueless.

## Claims

- **`խոտ` = naive/clueless person** — citation:
  `topics/lexicon/yerevan_slang.md` + `ghamoyan p48` —
  confidence: `cited`
- **`ըլնի` = 3sg subj of dialectal `ըլնել`** — citation:
  `topics/morphology/dialectal_lnel.md` — confidence:
  `single-source` (bararan.am only)
- **`պալիտիկ` = Russian-loan, register-marked** — citation:
  `topics/lexicon/code_switching_with_russian.md` —
  confidence: `cited`
- **Overall reading: sarcastic dunk on Pashinyan** —
  citation: `[interpretive synthesis]` — confidence:
  `synthesis` (no single source, but each component is cited)

## Gaps

- `մի հատ էլ` — idiomatic "and on top of that"; flagged as
  topic gap in `topics/lexicon/idioms_phrasal.md` § gaps.
  My reading is consistent with general Armenian usage but
  unverified at the corpus level.
```

Step 3 — `verify_citations.py` confirms every cited path/page
is in the bundle; flags `[interpretive synthesis]` as a
non-bundle citation (acceptable but logged).

## Why this exists

The 2026-05-09 Pashinyan-tweet comparison
(`research/2026-05-09-tweet-llm-comparison.md`) had four LLMs
(three external + one workspace-aware) confidently produce four
different glosses for `խոտ`. The correct citation was sitting
in the topic graph; nobody looked. This skill makes "look
first" a mechanical step instead of a habit, and verifies that
every claim in the output traces back to the bundle.

## Cross-references

- `frequency/query_kb.py` — the retrieval layer this skill wraps.
- `.claude/skills/answer-q/verify_citations.py` — the citation
  validator.
- `CLAUDE.md` § "Before answering an Armenian-language question"
  — the human-driven version of this protocol.
- `llm-workflow.md` — the rationale for citation-grounded
  answering.
- `kb-design.md` — the broader agent-flow architecture this
  skill is one Phase of.
