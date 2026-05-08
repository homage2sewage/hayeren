# Frequency lists and core vocabulary — research base

How to construct an *N*-most-useful-words list for a learner: what the
literature says, what's available for Armenian, what choices to make
for our deck.

> **Scope note.** This document is the **research / theory** base. The
> *running build pipeline* (scripts, data layout, regenerate
> commands, validators) lives in [`frequency/README.md`](frequency/README.md)
> and the *Anki-importable outputs* live in
> [`cards/README.md`](cards/README.md). Read those if you want to
> rebuild the deck or understand how a card got there. Read this
> file for the *why* behind the choices the pipeline makes.

## Objectives

What the deck is meant to achieve, in priority order:

1. **High-leverage starter vocabulary for a Russian-speaking
   learner of Eastern Armenian** — Yerevan-colloquial-leaning, since
   the user's primary goal is understanding spoken Armenian.
2. **Citation-honest provenance** — every card traces to a source:
   sakayan textbook (vocab table or paradigm), ghamoyan colloquial
   study (filler / slang / register), hand-curated gap-additions
   from the Hermitdave OpenSubtitles diff, or the local Wiktionary
   dump. The card's `tags` field carries the source so the trail
   is auditable.
3. **Empirically validated heuristics** — every priority / sort /
   filter rule (POS-priority, language-name skip, MWU detection,
   …) confronts its input population *before* shipping. The
   golden-set in `frequency/golden_glosses.tsv` is the durable
   form of those audits. See `llm-workflow.md` and
   `.claude/skills/challenge-rule/` for the rationale.
4. **Russian-language gloss in addition to English** for words
   where the Russian formulation disambiguates faster than the
   English one (function words, particles, register-marked items,
   colloquial fillers).
5. **Phonetic respelling** on cards whose pronunciation deviates
   from spelling on a contrast-bearing consonant (voiced ↔
   unaspirated ↔ aspirated) — e.g. `ընդունել [ընթունել]`. Uses
   sakayan's transliteration as ground truth.
6. **Frequency-ranked top-1000** — Nation's first-tier coverage
   (~78% of running text) is the quantitative anchor. The deck
   matches Pinhok-deck-class size for external comparison.

The first three are the **non-negotiable** properties; 4–6 are the
present implementation choices and are revisitable as the corpus
or learner profile changes.

## What sources contribute

| source | role | volume | format |
|--------|------|--------|--------|
| **sakayan** (Sahakyan 2007, *Eastern Armenian for the English-Speaking World*) | textbook lemmas + paradigm cells + dialogue Armenian | ~1450 cards | sakayan/unit*_vocab.tsv, dialogue, paradigms |
| **ghamoyan** (Ghamoyan et al. 2014, *Yerevan's Colloquial Language*) | conversational fillers + slang + colloquial register markers; corpus contribution to the frequency list | ~32 fillers + ~3K tokens of mined examples | `cards/ghamoyan/fillers.tsv`, `topics/lexicon/yerevan_slang.md`, `topics/pragmatics/intimate_register.md` |
| **frequency-gap** (Hermitdave-derived) | high-frequency conversational items missing from sakayan | ~16 hand-curated entries | `cards/frequency/gap_additions.tsv` |
| **kaikki.org Wiktionary** | offline dictionary fallback for lemmas without a card-level translation | ~22K dictionary entries | `frequency/data/armenian_dict.tsv` |
| **HAND_OVERRIDES** | safety valve for high-frequency particles / pronouns / function words where Wiktionary's first gloss is misleading | ~75 entries | inline in `frequency/build_deck.py` |

Ghamoyan plays a larger role than its filler-card count suggests —
it's the **only colloquial-register source** in the corpus.
Without it, the deck would be 100% literary-Sakayan and miss the
register the user wants to understand. Specifically:

- Filler set (`բա, դե, հենց, ուրեմն, …`) lifts colloquial discourse
  markers into the deck that Sakayan's textbook prose doesn't
  isolate.
- Register-marked vocab and slang feed both the deck and the
  topic-graph (`topics/lexicon/yerevan_slang.md`,
  `topics/lexicon/code_switching_with_russian.md`,
  `topics/pragmatics/intimate_register.md`).
- Phonological / morphological observations from ghamoyan
  (`ա` for `է`, ղ-drop, voiced↔aspirated bidirectional shifts)
  feed into the phonetic-respelling heuristic and the topic
  graph rather than the cards directly.

When a future *spoken-Yerevan* corpus becomes available (EANC
colloquial sub-corpus, transcribed YouTube/podcast data, etc.),
ghamoyan's role here will narrow back to its slang/register
specialty; for now it's load-bearing for everything register-
related.

## The theoretical question

When you build a flashcard deck for a language learner, which words
should be in it? Frequency is the obvious answer; the literature
refines it.

### Lexical coverage and the size-of-vocabulary question

The canonical work is Paul Nation's series of papers, especially
**Nation (2006)**, *How large a vocabulary is needed for reading and
listening?* (*Canadian Modern Language Review* 63, 59–82).

Using the British National Corpus and matching American spoken
corpora, Nation derived these coverage curves (English; comparable
shapes in other languages):

| Top-N word families | Text coverage |
|--------------------:|--------------:|
| 1 000               | ~78 %         |
| 2 000               | ~85 %         |
| 4 000               | ~93 %         |
| 9 000               | ~98 %         |

98% is a commonly-cited threshold for *functional* unassisted reading
of general text — fewer than 2 unknown words per 100 means the reader
can usually infer meaning from context.

For *spoken* conversation the curve is shifted: spoken language
re-uses fewer high-frequency words at higher rates, so 1 000–2 000
families covers more of casual conversation than of written text.
This is why frequency lists derived from subtitle corpora (heavy
spoken-register weight) make particular sense for an Armenian learner
whose primary goal is *understanding what people say in Yerevan*.

### Zipf's law

Word-frequency distributions follow Zipf's law: the *k*-th most
frequent word occurs ~ 1/k as often as the most-frequent word. The
practical consequences:

- The top 100 words cover ~50 % of any text.
- The first ~1 000 do most of the work; gains drop sharply afterwards.
- The long tail is dominated by content-specific items (proper nouns,
  technical terms, hapax legomena — words appearing exactly once).

This is *why* a curated 1 000-word deck is high-leverage: you're at
the steep part of the curve.

### Counting units: token / type / lemma / word family

Frequency lists differ wildly depending on what they count:

- **Token** — every occurrence. "Go" appearing 5 times = 5 tokens.
- **Type** — unique word form. "Go", "goes", "went", "going" = 4 types.
- **Lemma** — base/dictionary form. The 4 forms above collapse to one
  lemma: `go`. **Most public frequency lists use lemmas.**
- **Word family** — lemma plus derivations. `go, goer, going (n.),
  goings-on`, etc. = one family. Nation's 1 000-family count is
  closer to ~3 000 lemmas.

For Armenian this matters a lot because of rich inflection. A noun
like `գիրք` "book" appears in running text as `գիրքը, գիրքը, գրքի,
գրքից, գրքերի, գրքերը, գրքերում…` — roughly 20+ forms once you
count case × number × article. Lemmatization is the difference between
"the deck has 100 noun cards" and "the deck has 100 noun forms ≈ 5
nouns".

### How frequency lists are built — 4-step recipe

1. **Choose a corpus.** Genre-balanced (e.g. BNC, COCA) for general
   learners; spoken-only for conversation goals; news for reading
   modern media; literature for narrative reading. Genre selection
   determines what the resulting list privileges.
2. **Tokenize and lemmatize.** Tokenize on word boundaries; apply a
   lemmatizer to collapse inflected forms. Lemmatizer accuracy
   determines the long-tail quality.
3. **Count + rank by lemma frequency.**
4. **Filter.** Drop proper nouns, hapaxes, language-mix artifacts,
   sometimes orthographic variants.

### Caveats

Pure frequency lists have known limitations:

- **Register** — a "fork" might rank ~3 000 in a balanced corpus but
  you need it daily. A filler like `բա` ranks high but isn't
  traditionally taught.
- **Collocational dependencies** — some words are useful only as
  parts of fixed phrases (`ի դեպ` "by the way"). Frequency-list
  inclusion at lemma level can miss the real unit.
- **Genre bias** — subtitle corpora over-represent first/second
  person and emotional vocabulary; news under-represents emotion;
  academic texts over-represent abstract nouns.
- **Dialect/variant skew** — Eastern vs. Western Armenian; standard
  vs. colloquial. A list built from one register doesn't transfer.

These caveats are why **comparing two lists** (ours vs. an external
reference) is more informative than treating any single list as
gospel.

## What's available for Armenian

Surveyed for Eastern Armenian; Western Armenian resources are
separate.

### Hermitdave/FrequencyWords (GitHub) — recommended primary reference

Repository: `github.com/hermitdave/FrequencyWords` (2018 corpus
release).

Built from **OpenSubtitles 2018** — movie/TV subtitle corpus
aggregated across many films. Spoken-register weighted, which suits
our colloquial-leaning goal. Per-language, the Armenian list at
`content/2018/hy/hy_full.txt` is ~50 K entries, lemma-aggregated,
plain text format `lemma frequency`. Free, no auth, no rate limit.

Limitations: subtitle text can be unrepresentative of natural
conversation (over-edited, plot-driven), and dubbed films skew
toward source-language usage patterns. But for a *first comparison
reference*, it's the right choice.

### Pinhok Armenian Frequency Dictionary

Commercial product (~$15 ebook); ~1 000 words. Available as a
shared Anki deck. Already noted in `armenian-vocab-research.md`.
Quality varies by language across Pinhok's catalogue; haven't
verified Armenian specifically. Useful as a *secondary*
comparison if the primary surfaces gaps.

### EANC — Eastern Armenian National Corpus

`eanc.net` — academic corpus, ~110 M tokens, includes a colloquial
sub-corpus (TV/radio transcripts, online forums). Highest quality
data for Armenian generally. Drawback: web interface only, no API
and no bulk download — would need scraping. Defer.

### Wiktionary's Frequency lists / Armenian

Community-maintained at `en.wiktionary.org/wiki/Wiktionary:Frequency_
lists/Armenian`. ~5 000 words. Variable curation quality (volunteer
work; corpus source is sometimes opaque). Useful for spot-checking
but not as a primary reference.

## Methodology choices for our list

These are the decisions made for this specific build; revisit as we
learn more.

### Reference list: **Hermitdave OpenSubtitles**

Free, lemma-form, spoken-register weighted, easy to fetch. EANC would
be cleaner academic data but requires scraping that we've deferred.
Pinhok matches our *output* size (1 000) so it's not a corpus; could
later cross-check if we feel the need.

### Lemmatization: **rule-based suffix stripping**

Reuse the suffix list from `sakayan/glosser.py` (definite article,
case endings, common verb endings) plus a few abstract-noun
substitution rules. Expected accuracy: ~85–90 % at the head of the
list (function words and high-frequency content words), degrading in
the long tail.

The cheap approach is right for a *first cut* because:

- Frequency lists tolerate ~10 % noise at the head.
- Building a proper lemmatizer (UDPipe, etc.) is roughly 10× the
  effort for ~5–10 percentage points of accuracy gain.
- We can detect lemmatization failures via the comparison phase: if
  our top-1 000 has weird inflected forms missing from Hermitdave's
  top-1 000, that's a lemmatization bug surfacing.

### Output size: **top 1 000**

Aligns with Nation's first-tier coverage (~78 % of running text in
general, more for conversation). Also matches the size of Pinhok's
deck and most Anki "core 1 000" decks for other languages —
makes external comparison meaningful. We can extend to 2 000 later.

### Corpus for "ours": book-derived

Aggregate all extracted Armenian from:

- `cards/sakayan/unit*_vocab.tsv` — vocab cards (lemma-form
  by construction; ~600 entries).
- `cards/sakayan/unit*_dialogue*.tsv` — dialogue Armenian
  text (running prose; needs tokenization + lemmatization;
  ~290 exchanges, ~3 000 tokens).
- `cards/sakayan/paradigms.tsv` — verb paradigm cells
  (already lemma-form for our purposes; ~350 entries).
- `cards/ghamoyan/fillers.tsv` — colloquial fillers (~32 entries).

Note: the Sakayan textbook is a deliberately *learner-oriented*
corpus, not a balanced one — it over-represents introductory vocab
(family, body parts, basic verbs, greetings) and under-represents
specialized domains. So "our top-1 000" is best read as *the
high-frequency words in this learner's first textbook plus
colloquial fillers* — not a frequency list of Armenian as a whole.
The comparison phase is where we'll see what that bias costs us.

## What "comparison" produces

Three buckets:

1. **Agreed** — words in both our top-1 000 and Hermitdave's
   top-1 000. The core that any deck should have.
2. **We cover, frequency doesn't** — items in our deck that don't
   crack Hermitdave's top-1 000. Expect: textbook-introductory
   nouns (`այբուբեն` "alphabet", `քրիստոնեություն` "Christianity"),
   register-marked items (`բա, եսիմ, տենց`), grammatical paradigm
   cells (`ունեցել եմ`), irregular verb forms.
3. **Frequency covers, we don't** — high-frequency Armenian words
   missing from our deck. Expect: function words Sakayan didn't
   isolate as vocab (pronouns, demonstratives, common conjunctions),
   common modal verbs, time expressions, conversational fillers we
   haven't yet mined from Ghamoyan.

Bucket 3 is the most actionable — it tells us what to add.

## Sources

1. **Nation, I. S. P. (2006).** *How large a vocabulary is needed
   for reading and listening?* Canadian Modern Language Review,
   63(1), 59–82.
2. **Nation, I. S. P. (2013).** *Learning Vocabulary in Another
   Language* (2nd ed.), Cambridge University Press. The textbook
   summary of decades of vocabulary-acquisition research.
3. **Zipf, G. K. (1949).** *Human Behavior and the Principle of
   Least Effort.* Addison-Wesley. Original statement of the
   frequency–rank power law.
4. **Schmitt, N., Cobb, T., Horst, M., & Schmitt, D. (2017).**
   *How much vocabulary is needed to use English?* Language
   Teaching, 50(2), 212–226. Updated coverage targets.
5. **OpenSubtitles 2018 corpus** —
   `opus.nlpl.eu/OpenSubtitles2018.php`. The source for
   Hermitdave's frequency derivations.
6. **Hermitdave/FrequencyWords** —
   `github.com/hermitdave/FrequencyWords`. Per-language frequency
   lists derived from OpenSubtitles.
