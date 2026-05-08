# LLM-comparison case study — Pashinyan-tweet slang gloss

A worked example of why citation-grounded answering matters for
this project. One slang-heavy Armenian tweet, four LLM answers
(three external + one Claude-Code in-conversation), four
*different* readings of the pivotal content word, all stated with
high confidence and no acknowledgment of uncertainty.

## The tweet

Reply to a positive video about Nikol Pashinyan:

```
հա լավ էսքան խոտ մարդ ըլնի

մի հատ էլ պալիտիկ 🤭😅
```

## What the four answers agreed on

- Register is colloquial Yerevan / internet-slang. All four flagged it.
- Tone is sarcastic, dismissive. All four.
- `պալիտիկ` is a Russian-loan colloquial spelling
  (Russian *политика*) used as a register marker — "I am being
  casual, possibly mocking." All four.
- Emojis as sarcastic-frame markers. All four.

The *grammar* and *register-marker layer* is well covered by
pre-training. Where the answers diverge is the lexicon —
specifically, what `խոտ` "grass" means as a slang noun.

## Where they diverged — the `խոտ` problem

| answer | gloss for `խոտ` | implied target | reading |
|--------|------------------|----------------|---------|
| my earlier (Claude Code in-session) | "weed / marijuana" (drug-slang calque) | speaker mocking the audience | "if a person smokes that much weed, of course they'd buy this take" |
| answ1 | "spineless / weak / wet blanket / vegetable" | Pashinyan (character) | "how can one person be this much of a wimp… and a politician on top of it" |
| answ2 | "passive / dumb / sheep-like / NPC / mindless masses" | Pashinyan's *supporters* | "with this many sheep around, of course you get another politician" |
| answ3 | "clueless / mindless / vegetable-brained" | Pashinyan (intellect) | "how can someone be this much of an idiot? And he calls himself a politician" |

Four readings, four targets, four confident commitments, no
citations.

## Which is grammatically supportable?

`էսքան խոտ մարդ ըլնի` — verb `ըլնի` is **3sg subjunctive**.

- The construction `էսքան + N + ըլնի` is a colloquial exclamation
  of incredulity about one referent: "[for] a person [to] be
  this much [of a] X." Predicative.
- answ1 and answ3 parse it correctly (singular subject;
  predicating about Pashinyan).
- **answ2 misreads it as plural** ("this many grass-people" →
  "this many sheep"). Plural would require 3pl `ըլնեն`. So
  answ2's structural frame is grammatically wrong, independent of
  the slang gloss.
- My earlier "weed" reading fails the construction too —
  consumption-of-X would be `էսքան խոտ քաշի մարդ` ("person
  smokes this much weed"); the actual sentence is X *being* the
  predicate, not *taking* the predicate.

So on structure, the field narrows to answ1 and answ3 — both read
`մարդ` as "[a] person being this much [of a] grass." The
remaining difference is the connotation of `խոտ` (weak vs dumb).

## On the dialectal verb `ըլնել` itself

bararan.am (the standard Armenian-dictionary portal) confirms
**ըլնել** as a separately-attested dialectal lexeme:

> **ըլնել** [չեզոք բայ] (գավառական) — Լինել:

i.e. *intransitive verb, dialectal/provincial register, defined
as "to be" (the literary լինել)*.

So the form `ըլնի` in the tweet is the regular 3sg subjunctive of
the **dialectal verb ըլնել**, not merely a casual phonetic
deformation of `լինի`. This matters: the LLMs all treated it as a
sound-variant, but it is in fact a recognized dictionary entry —
exactly the kind of thing the topic graph should attest with a
citation rather than infer with vibes. Worth a follow-up topic
file under `topics/morphology/` (or absorbed into an existing
page on dialectal copula/auxiliary forms) citing the bararan.am
entry.

## Which LLM is which (best guesses, not certainties)

Stylistic fingerprints across the three external answers:

- **answ3 → GPT (OpenAI, likely 4o/5).** Heavy structural
  scaffolding: `###` headers, **bolded inline labels:**,
  horizontal `---` rules, literal-vs-idiomatic translation pair,
  enumerated contextual-analysis list, a closing **Summary:**
  italic line. House-style fingerprint is strong. Confidence: 70%.
- **answ1 → Claude (Anthropic).** Inline transliterations in
  parens for every Armenian word (`(ha lav)`, `(esqan khot mard
  ëlni)`) — a Claude pedagogical reflex with non-Latin scripts.
  Hedging present ("dominant sense is …, Some users also use
  …"). Politically-situated final paragraph (opposition camp /
  Artsakh framing). Confidence: 60%.
- **answ2 → Grok (xAI), possibly Gemini Flash or a smaller
  faster model.** Shortest answer, internet-native vocabulary
  ("NPCs," "bots," "sheep-like"), three-bullet near-synonym
  enumeration as a stylistic tic, the structural misread.
  Confidence: 40%.

The fact that *none* of the four (including my own first pass)
produced an uncertainty-acknowledging answer is itself the
diagnostic signal.

## What the right LLM behavior would have been

> "`խոտ` here is a colloquial insult; the most common readings in
> Yerevan slang are (a) 'spineless / weak' or (b) 'clueless /
> vegetable-brained.' Both fit grammatically. The drug-slang
> reading is also possible but disfavored by the predicative
> construction. I don't have a citable source to disambiguate —
> flag for verification against ghamoyan, EANC, or
> bararan.am."

That's citation-grounded answering. Without
`topics/lexicon/yerevan_slang.md` actually covering `խոտ` as a
personal insult — which it currently doesn't — even a "good"
model is just guessing with vibes.

## Action items spawned

1. **Add `խոտ` as a slang-insult entry** to
   `topics/lexicon/yerevan_slang.md`, with citations from
   ghamoyan or Acharyan if available; flag as
   `attestation: single-source` until triangulated.
2. **Add `ըլնել` (dialectal copula)** as a topic or supplement
   under `topics/morphology/`, citing bararan.am's
   `(գավառական)` entry as a primary source. The 3sg subj `ըլնի`
   was the form the LLMs all stumbled on.
3. **Add this tweet as the canonical test case** for the slang +
   dialectal-copula topics. The topic-graph answering system is
   "working" only when it produces a structured answer like the
   "right LLM behavior" sketch above for this exact tweet.
4. **Add `խոտ` and `պալիտիկ`** as `golden_glosses.tsv`-style
   anchors at the right level (probably a future
   `topics/lexicon/golden_phrases.tsv` or in-topic example list).

## How this connects to `llm-workflow.md`

This case study is a real-world instance of the general failure
mode `llm-workflow.md` describes: confident heuristic outputs
that look authoritative but were never confronted with their
input population. Each LLM committed to a slang gloss without
producing alternatives or citing a source. The fix at the
project level is the same: surface the hypothesis, name the
sources, accept "I don't know without citation" as the correct
answer when it is.

Worked-example status: this file should remain stable as
documentation of *what good citation-grounded answering would
look like for a hard real input*, used to evaluate future
versions of the topic graph.

## Cross-references

- `llm-workflow.md` — general principles; this file is a
  concrete instance.
- `topics/lexicon/yerevan_slang.md` — needs `խոտ` entry.
- `topics/lexicon/code_switching_with_russian.md` — `պալիտիկ`
  as Russian-loan register marker fits here.
- `topics/morphology/colloquial_copula_a.md` — adjacent
  phenomenon (3sg `ա` for `է`); the `ըլնի` finding suggests a
  parallel topic on dialectal-copula full-paradigm forms is
  needed.
- `transliteration-notes.md` — register-baked spelling
  pitfalls; `պալիտիկ` and `էսքան` are textbook examples.
