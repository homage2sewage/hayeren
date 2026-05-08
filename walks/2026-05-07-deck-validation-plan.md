# Plan: top-1000 deck validator

**Status**: in progress (mechanical lint pass implemented today).
**Author**: drafted with Claude Code 2026-05-07.

## Context

The `cards/top_1000.tsv` deck is now built end-to-end from
`build_ours.py` (corpus + lemmas) and `build_deck.py` (translation
join). Coverage is currently 77.1% — the remaining 22.9% are
"`—`-translation" rows, but a coverage number alone hides the
*kinds* of errors that creep in. The user has hit several distinct
classes (paraphrased from past sessions):

- **Ghost translations.** `կարող` → "Karelian" (Wiktionary returned
  an ethnonym sense). `մի` → "a little" (multi-word vocab card leak).
- **Truncated lemmas.** `ուսուցչուհ` (should be `ուսուցչուհի`),
  `դեպս` (leaked tail of `ի դեպ`), `ըստ_էություն` (genitive `-ի`
  stripped from a fixed phrase).
- **Inflection that wasn't normalized.** `մորս`, `կոկորդս` (1sg
  possessive), `կգայինք` (irrealis), `պատրաստվենք` (subjunctive),
  `ճաշեր` (plural), `եվ` (spelled-out `և` ligature).
- **Proper nouns that aren't first-and-foremost Armenian words.**
  `մալյան` (surname). Policy: keep `Հայաստան`, `Եվրոպա` etc; filter
  personal names.
- **Multi-word units split into single tokens.** Now mitigated in
  `build_ours.py` via the `MWUS` list and `_`-joining, but the
  validator should detect any future leak.
- **Noise glosses.** Morphological-only entries from kaikki
  (`եմ (2 s pres)`), alphabet-letter descriptions. `dictionary.py`
  filters most; the validator should flag any that survive.
- **Duplicate translations.** Two distinct lemmas mapped to the same
  English gloss usually means the lemmatizer collapsed them
  inconsistently — worth surfacing.

The user asked specifically: "take all known errors into account,
plan and implement a validator for it, mb an agent or agentic
pattern or whatever, see the docs."

## Design

Two-phase, per the **mechanical-lint + agent-rubric** pattern from
`kb-design.md` §"Phase 1 / Phase 2 split":

### Phase 1 — `validate_deck.py` (mechanical lint)

Pure-stdlib checks against `cards/top_1000.tsv`. Fast (<1 s). Each
finding is a row of:

    severity \t rank \t lemma \t translation \t category \t hint

Where `severity ∈ {error, warning}` and `category` is one of the
classes listed in the table below.

| category               | severity | rule                                                                                                                |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------------- |
| `empty-translation`    | warning  | translation column is blank                                                                                         |
| `noise-translation`    | error    | matches `\b(letter of (?:the )?(?:Armenian )?alphabet|inflection of)\b` or `^[Ա-Ֆա-ֆև]+\s*\(.+?\)$`                  |
| `false-friend`         | error    | translation contains `Karelian` (the canonical example), or other ethnic-adjective ghosts we collect over time      |
| `truncated-lemma`      | error    | lemma length < 4 *or* lemma not present in dictionary AND lemma+`ի` / lemma+`ի` / lemma+`ություն` is present        |
| `inflected-leak`       | error    | lemma ends in `-ս`, `-դ`, `-ն` AND a vowel-shorter form exists in the dictionary (1sg/2sg/def-art possessive leak)  |
| `paradigm-leak`        | error    | lemma ends in `-ենք`, `-եք`, `-ինք`, `-ին`, `-ի`, `-ուց`, `-ում`, `-ել`, `-ալ` AND a known infinitive subsumes it    |
| `proper-noun-foreign`  | error    | lemma's only dictionary entry is `pos=name` AND not in a `KEEP_NAMES` allow-list (`Հայաստան`, `Եվրոպա`, `Երևան` …)   |
| `mwu-leak`             | warning  | both halves of a known `MWUS` member appear in the deck independently (suggests merging missed an occurrence)       |
| `duplicate-translation`| warning  | two or more distinct lemmas share the exact same translation string                                                 |
| `eu-ligature`          | error    | lemma is exactly `եվ` (should be merged into `և`)                                                                   |

Output goes to:

- `frequency/out/deck_validation.tsv` — every finding
- `frequency/out/deck_validation.md` — human-readable summary,
  grouped by category, with counts

### Phase 2 — agent rubric (deferred)

A `critic-pass` skill that, given a slice of low-confidence cards
(e.g. the `empty-translation` and `truncated-lemma` rows), asks an
LLM critic to:

1. Confirm whether the lemma is plausibly Armenian.
2. Propose a corrected lemma (with reasoning).
3. Propose a candidate translation if the dictionary missed it.

This is genuinely *new* judgment — we'd be paying for it — so it
sits behind Phase 1's filter. We don't build it until Phase 1's
mechanical pass settles.

## Implementation order

1. Write `frequency/validate_deck.py` with the rules above.
2. Run it on the current `cards/top_1000.tsv`; record the
   distribution of categories.
3. For each category with N > 5 findings, decide: fix the upstream
   builder, or accept the findings as a known-issue list.
4. Defer Phase 2.

## What this plan does *not* cover

- **English/Russian back-of-card quality.** That's an Anki concern,
  not a lemma-list concern.
- **Frequency-rank accuracy.** Comparison against Hermitdave already
  exists in `compare.py`.
- **Card formatting / TSV escaping.** Out of scope; the deck is
  built by `build_deck.py` which controls writing.
