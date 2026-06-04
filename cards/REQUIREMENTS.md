# Deck requirements — `cards/top_1000.tsv`

The spec the frequency-ranked Armenian study deck must satisfy.
Compiled 2026-06-03 from the operator's stated requirements across
the build sessions. Each item is meant to be testable. Source of
truth for *intent*; `frequency/build_deck.py` + `validate_deck.py`
are the implementation and the automated guards.

## 1. Purpose & scope

- A frequency-ranked deck of the most common Armenian (Eastern,
  Yerevan-leaning) words for a learner, built from a textbook +
  colloquial corpus (sakayan, ghamoyan, parnasyan, tioyan).
- Rows ordered by corpus frequency. Size ~1000+ cards; **may grow**
  when a requirement calls for it (e.g. phrasal verbs, missing
  inflected forms) — size is not a hard cap.

## 2. Card schema

- Three tab-separated columns: **Armenian** · **gloss** · **tags**.
- **Armenian column**: the lemma (citation form), rendered as Anki
  **HTML** — lemma **bold**, the optional `[phonetic-respell]` small
  and muted gray on the same line. The respell is Armenian script and
  appears only when pronunciation deviates from spelling
  (`կարդալ [կարտալ]`). No bracket if no deviation. The plain lemma
  remains the internal key (sidecar, validator) — HTML is emit-time
  only.
- **Gloss column**: rendered as **Anki HTML** — English **bold**,
  Russian muted gray, on separate lines (`<br>`); embedded examples
  italic. Import with "Allow HTML in fields" enabled. Authoring is
  plain `English / Russian`; HTML is produced at build time.
- **Tags column**: `frequency <category>` only, where category is
  `top-1000` / `core-inject` / `phrasal-verb`. **No `rank-NNNN`, no
  `src-…`, no POS (`verb`/`noun`/…) tags on the card.** Rank was
  dropped from the card because it isn't needed for study; it is
  *retained* in the `frequency/out/deck_meta.tsv` sidecar because the
  validator/ordering tooling needs it (this is the "unless necessary"
  resolution of req #1). `core-inject` is an internal implementation
  tier (force-injected essential/function vocab behind the §3 Russian
  coverage and §5 person/number asks), not a separate operator
  request.

## 3. The `English / Russian` gloss

- ` / ` is **reserved** strictly for the English↔Russian boundary.
  Multiple English (or Russian) senses are separated by commas or
  `;` — never by ` / `.
- **Russian coverage target**: all of the top-300, plus all function
  words / pronouns / conjunctions / postpositions. Rarer content
  nouns below that may stay English-only. (Russian is a translation
  layer — prior, not corpus-cited.) The EN/RU pairing also serves to
  **disambiguate**: each language narrows the other's sense (the
  operator's stated rationale for bilingual backs).
- Glosses are terse and learner-natural (contemporary, not archaic /
  dictionary-prose); lead with the most useful/frequent sense.
- **No script mixing**: a single token must not mix Armenian with
  Cyrillic letters (the operator's reported `էл`-with-Cyrillic-`л`
  bug). The implemented guard generalizes this to Latin as well — a
  deliberate broadening beyond the literal report.

## 4. Sense correctness (the homograph trap)

- A gloss must reflect a real, primary/high-frequency sense of the
  lemma, confirmed in the **corpus**, not just whatever the kaikki
  dictionary returns.
- High-frequency grammatical/colloquial tokens that collide with a
  rare literary headword must NOT ship the rare sense (`մերի` ≠
  "woods", `ալ` ≠ "scarlet", `դեմ` ≠ "front part"). If the token is
  a form of a word already on the deck or tokenizer noise, drop it;
  if it's a real word with the wrong sense, fix the sense.

## 5. Grammatical annotation

- **Person**: copula/verb person-forms carry a person tag —
  `չէր` "wasn't (3sg)", `չէի` "wasn't (1sg)", etc. The negative-past
  copula paradigm is present (1sg…3pl).
- **Case**: an oblique/case form used as a card carries an explicit
  case label tying it to its citation form — `նրանց` "them; their
  (gen/dat of նրանք)", `ինձ` "me (dat/acc of ես)", etc.
- **Numbers**: numeral cards show the **digit** — `մեկ`→`1`,
  `հազար`→`1000`. *Exception (documented):* ordinals carry the
  English ordinal suffix on the digit (`հինգերորդ`→`5th`), since a
  bare digit can't express ordinality; this is the agreed reading of
  "digit only," not strictly digits-with-no-letters.

## 6. Pre-/postpositions

- **Every** pre-/postposition card carries a short, grammatically
  correct, corpus-plausible usage example embedded in the gloss
  (`վրա` → "on, upon (սեղանի վրա — on the table)").
- The current postposition inventory is the closed checklist:
  `հետ`, `մասին`, `դեմ`, `տակ`, `վրա`, `ըստ`, `առանց`, `պես`, `դեպի`,
  `շուրջ`, `համար`, `ընթացքում` (+ any newly surfaced). "Every" is decidable
  against this list; if a check is wanted, it should iterate a
  `POSTPOSITIONS` set rather than guess.
- When a card must hold an embedded example **and** EN **and** RU,
  the `verbose-gloss` length cap (90 chars for an en/ru pair) takes
  precedence: trim the example before exceeding it.

## 7. Phrasal / light-verb verbs

- Common Armenian phrasal / light-verb constructions
  (`[noun/adj] + անել/տալ/գալ/լինել/ունենալ/…`) are first-class cards:
  `դուր գալ`, `հարց տալ`, `տեղի ունենալ`, `կանգ առնել`, `դատ բանալ`, …
- When a base word has a common phrasal (e.g. `դատ` → `դատ բանալ`),
  the phrasal is provided.
- The phrasal set is **mined from the textbook corpora** (currently
  parnasyan + tioyan, which are bilingual ARM–RUS) and corpus-
  grounded; it lives in `cards/frequency/phrasal_verbs.tsv`, tagged
  `frequency phrasal-verb`, and may grow (sakayan/ghamoyan are
  candidate future sources).

## 8. Filtering

- Personal given names excluded (geography/landmarks kept).
- Inflected forms whose lemma is already on the deck excluded
  (converbs, definite forms, etc.).
- Bare grammatical morphemes / tokenizer spill excluded
  (`-ներ` plural suffix, possessive-genitive artifacts).
- Lemmas stay literary; colloquial variants are mentioned **inside
  the gloss**, not by swapping the lemma.
- **No duplicate lemma** across the merged sources (top_1000 +
  core_inject + phrasal_verbs). A phrasal `X + verb` is a distinct
  card from the bare `X` and the two may coexist; but the same bare
  lemma must not appear twice. (`check_duplicate_translation` guards
  identical *glosses*; lemma-identity dedup is done at inject time.)

## 9. Quality & process

- `frequency/validate_deck.py` must pass **0 errors** (`--strict`
  exit 0) on every build.
- **Enforcement honesty.** Not every requirement here is population-
  enforced. *Population-enforced by a `check_*`*: reserved-slash,
  script-purity / mixed-script, prose/verbose gloss, missing-Russian
  (top-300), morpheme-noise, duplicate-override-key, golden anchors.
  *Spot-anchored only* (golden entries on specific lemmas, not a
  population sweep): person tags (§5), case labels (§5), number→digit
  (§5), postposition examples (§6). Closing these into population
  checks (iterating a `POSTPOSITIONS` / `NUMBER_DIGITS` / copula-form
  set) is a known follow-up.
- Every wrong-output fix is two-step: **fix the case AND add a
  guard** (golden anchor in `golden_glosses.tsv`, a new `check_*`, or
  a `SKIP_LEMMAS` + check).
- New heuristics run the challenge protocol (`llm-workflow.md`).
- After the structural validator is green, an editorial / unbiased
  agent pass reviews gloss quality; findings feed back via the
  two-step rule.
- Glossing claims about Armenian are corpus-grounded; uncited
  translation (e.g. Russian) is labelled as such, not presented as
  citation.
