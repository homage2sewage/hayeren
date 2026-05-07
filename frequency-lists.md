# Frequency lists and core vocabulary — research base

How to construct an *N*-most-useful-words list for a learner: what the
literature says, what's available for Armenian, what choices to make
for our deck.

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
