# Phonetic-transcription coverage & the system behind it

2026-06-10. Investigation prompted by the observation that the deck's
pronunciation respells (`կարդալ [կարտալ]`) come **only from sakayan**,
and the question of how to expand them without per-word external
lookup (Wiktionary). Pairs with
[`topics/phonology/voiced_aspirated_alternation.md`](../topics/phonology/voiced_aspirated_alternation.md)
(the linguistic synthesis) and
[`topics/phonology/known_transcriptions.md`](../topics/phonology/known_transcriptions.md)
(the harvested data table).

## Current state

- **Deck coverage: 52 / 1097 cards** carry a `[respell]` (was 45; +7 from
  the 2026-06-14 tier-1 propagation pass below).
- **Total known transcriptions in the corpus: 105** — 87 sakayan-attested
  (harvested from `cards/sakayan/*.tsv`) + 18 hand-curated
  (`PHONETIC_OVERRIDES`). Deviation tally: `ջ→չ` ×25, `դ→թ` ×23,
  `գ→ք` ×19, `ձ→ց` ×14, `դ→տ` ×11, `բ→փ` ×10, `բ→պ` ×2, `գ→կ` ×2.

### 2026-06-14 update — tier-1 prototyped and partially landed

The tier-1 root-propagation strategy below was executed against the
deck's 1097 lemmas. Prefix-matching deck lemmas to attested respell
roots surfaced **11 candidates**; each was vetted against the book
transliteration columns. **7 landed** (3 corpus-confirmed in tioyan:
`երբեմն [ерп'эмэн]`, `վարդագույն [варт'агуйн]`, `ողջույն [вохчуйн]`;
4 sister-attested: `երբեք`, `բարձրագույն`, `բարձրացնել`, `մեջտեղ`).
**2 rejected as counterexamples** (`այդպես [айдпэс]`, `այդպիսի
[айдписи]` — դ stays voiced word-internally, the predicted failure of
extending word-final devoicing). 2 were phrase cards needing a code
change (`խորհուրդ տալ`, `ողջույն տալ`). Details + provenance table in
`topics/phonology/known_transcriptions.md` § "Tier-1 root-propagation
additions". The 87 sakayan-attested respells served as the gold set;
0 of the 7 landed forms disagree with any attested form.

## Why coverage is stuck on sakayan

`sakayan/phonetics.py` does **not** generate respells from spelling. It
walks each Armenian word against **Sakayan's transliteration column**
token-by-token and flags letters where the transcription disagrees with
the spelling (`DEVIATION_PAIRS`). So a respell exists only for words
Sakayan transliterated. This is why `երբ→[երփ]` is marked but its own
derivatives `երբեմն`, `երբեք` are bare — same `երբ-` root, no
transliteration data for the derivatives. It's a per-word-**data** gap,
not a rule gap.

## Is there a system? Three layers (from the topic file)

1. **Lexically idiosyncratic** (literary default, *no* rule). Sakayan
   treats which words devoice as memorize-per-word.
2. **Lexical-root regularity** (a sub-system). Devoicing is *consistent
   within a root across all its derivatives* (`վերջ-`, `առաջ-`, `մեջ-`,
   `քույր`-genitive) — but **which** roots devoice isn't predictable.
   Counterexample: `հաջորդ→[հաջորթ]` keeps `ջ` voiced.
3. **Genuine phonological rule** (real system). `ղ → /χ/ (=խ)` adjacent
   to a voiceless consonant — environment-conditioned, attested across
   books (`զեղչ→[զէխչ]` tioyan p38; `աղջիկ→[ахчик]`, `ամբողջ→[амбохч]`
   parnasyan p346). `պղպեղ` proves it's positional, not lexical (one
   `ղ` devoices, the other doesn't).

Ghamoyan (p39) adds that in **Yerevan colloquial** the shift is
**bidirectional** (voicing too: `ընկեր→ընգեր`) and dialect-driven.

## Expansion strategy (no external lookup)

Ranked by safety, anchored to which layer each relies on:

- **Tier 1 — root/morpheme propagation** *(recommended first)*. Build a
  `(root, position) → substitution` table from the 87 attested respells
  and apply to unattested lemmas sharing the root. Fixes `երբեմն→[երփեմն]`
  etc. for free. Relies on **layer 2** (root-regularity), which the repo
  already leans on by hand in `PHONETIC_OVERRIDES`. Lowest risk.
- **Tier 2 — encode the `ղ`-cluster rule**. `ղ→խ` before a voiceless
  consonant is **layer 3** (a real rule), safe to rule-generate.
- **Tier 3 — blanket spelling rule for `բ դ գ ձ ջ`** *(not recommended)*.
  Would guess into **layer 1**, an open question; the conditioning
  environment for stop devoicing is unknown from our sources, and the
  target isn't even uniform (`բ→փ` vs `բ→պ`). Overgenerates.

**The lucky break for validation:** the 87 sakayan-attested respells are
a ready-made **gold set**. Any generated rule's output can be diffed
against them; disagreements are counterexamples → exceptions list +
golden anchors. So the challenge protocol (mandatory per `CLAUDE.md`
before any such heuristic ships) is cheap here — we can measure
precision/recall before emitting a single new respell.

**Rejected — harvesting other books.** parnasyan/tioyan/ghamoyan *do*
carry transcription brackets, but extraction OCR-garbles them
(`թագավոր [ририщоп]`, `դեղձ [199]`). Mining them would be heavier and
dirtier than the alternatives; only the hand-verified, page-cited forms
in the topic file are usable.

## How the table was harvested (regeneration recipe)

`topics/phonology/known_transcriptions.md` was generated by:

1. Regex `([Ա-Ֆ…]+)\s*\[([Ա-Ֆ…]+)\]` over every `cards/sakayan/*.tsv`
   (skipping `all.tsv`), stripping intra-word punctuation `[՚-՟]`,
   recording word → respell + which unit file(s) it appears in.
2. Merging `build_deck.PHONETIC_OVERRIDES` (sakayan-attested wins on
   provenance collisions).
3. Per-letter diff of word vs respell to label the deviation(s);
   grouping by primary deviation.
4. Appending the cross-book attestations from the topic-file frontmatter
   (exact page + verbatim quote provenance).

## Open gaps (carried from the topic file)

- **Conditioning environment for stop/affricate devoicing is unknown**
  from our corpus — the single biggest blocker to a tier-3 rule.
- No **frequency** data (how often voiced stops alternate in running
  text).
- **Etymology** (native vs Iranian/Turkish/Russian loan stratum)
  unaddressed; might predict which roots devoice.
- Dum-Tragut (2009) descriptive grammar would likely close these but
  isn't in the corpus.

## Next action (if pursued)

Prototype tier 1: emit propagated respells, report (a) new-coverage
count and (b) every disagreement with a sakayan-attested form, before
committing anything to the deck.
