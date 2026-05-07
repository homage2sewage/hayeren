# Latin transliteration of Armenian — conventions and pitfalls

Top-level reference doc covering informal romanization of Armenian
(chat / SMS / social-media spelling) — what people *actually write*
when they don't have an Armenian keyboard or are writing
conversationally. Distinct from:

- The **phonetic transliteration** Sakayan uses in vocab tables
  (Armtrans column with diacritics). Linguistic, designed for L1=EN
  pronunciation guidance.
- The **Russian transliteration** Parnasyan and Tioyan use in their
  bracketed forms (`[на]` for `նա`). Linguistic, designed for L1=RU.
- Any standardised **scientific transliteration** (Hübschmann, ISO
  9985, etc.). None is in popular use for chat.

Informal Latin transliteration is none of these. It has **no
standard** — conventions are loose, register-driven, and pitfall-rich.
This doc collects what we know.

> Seed for this doc: notes originally in `ghamoyan/README.md` § "Topic 0:
> code-switching and informal romanization". Promoted here because the
> phenomenon is cross-cutting, not ghamoyan-specific.

## When does this matter

- The user pastes Armenian written in Latin script (chat, comment
  thread, social media post) and wants help reading or replying.
- The user writes in Latin script themselves and produces something
  grammatically broken — agreement mismatch, register collision,
  baked-in colloquialism that looks "wrong" only to the literary norm.
- The corpus contains transliterated Armenian (some social-media or
  chat data) that needs to be processed back into native script.
- AI Q&A: the question is asked with transliterated examples, and the
  AI needs to back-transliterate before it can use the topic graph.

## Common conventions — none of which are standard

Most informal romanizers pick from the following choices, often
inconsistently within a single message:

### High agreement (most writers do the same thing)

| Armenian | Latin | Notes |
|----------|-------|-------|
| ա | a | sometimes also for ը |
| բ | b | |
| գ | g | sometimes also for ղ |
| դ | d | |
| ե | e or ye | `ye` if word-initial, else `e` |
| զ | z | |
| է | e | conflated with ե |
| ի | i | |
| լ | l | |
| մ | m | |
| ն | n | |
| ո | o or vo | `vo` if word-initial |
| ս | s | |
| տ | t | conflated with թ |
| ր | r | conflated with ռ |
| ց | ts | |
| ու | u | digraph |
| և | ev or yev | |

### Conventions that vary by writer

| Armenian | Latin choice 1 | Latin choice 2 | Notes |
|----------|---------------|---------------|-------|
| ղ | gh | g | `gh` more careful, `g` more casual |
| շ | sh | ş | `sh` near-universal |
| չ | ch | č | almost always `ch` |
| ջ | j | dj | inconsistent |
| ռ | r | rr | usually conflated with ր |
| ք | k | q | `k` for Russian-influenced writers, `q` for Eastern-Armenian convention |
| թ | t | tʿ / t' | `t` collapses with տ |
| փ | p | pʿ | `p` collapses with պ |
| ձ | dz | ց | always `dz` |
| ճ | ch | č | conflicts with չ! |

The collisions in the second table are the source of ambiguity.
`ch` could be `չ` or `ճ`. `k` could be `կ` or `ք`. `t` could be `տ`
or `թ`. Disambiguation requires word knowledge.

## The five major pitfalls

### Pitfall 1: register baked into spelling

People write *as they say it*. A speaker who pronounces literary
`գրում է` as colloquial `գրում ա` (3sg copula `ա` for `է`, see
`topics/morphology/colloquial_copula_a.md`) will write `grum a`,
not `grum e`. Their input is *correct colloquial Yerevan*, *broken
literary*. Don't "correct" without checking which register was
intended.

Same for vowel reductions, consonant drops (see
`topics/phonology/yerevan_consonant_reductions.md`), and the
`-ություն → -ուցյուն` shift.

### Pitfall 2: agreement mismatch from naive back-transliteration

The canonical illustration of this pitfall, worked through fully:

A user writes `ches asem` intending "you won't say."

Naive segment-by-segment back-transliteration:

- `ches` → `չ` + `ես` = `չես`. ✓ This is the 2sg negative auxiliary
  ("you aren't").
- `asem` → `ասեմ`. **But this is the 1sg subjunctive** of `ասել` "to
  say" — meaning "let me say" or "(I) might say." Not the desired
  form.
- Concatenation: `չես ասեմ` = "you-aren't [I-]should-say" — broken,
  because the auxiliary is 2sg but the lexical verb is 1sg
  subjunctive.

What the writer probably *meant*:

- "you won't say" = **negative hypothetical 2sg of `ասել`**.
- Hypothetical-mood negation pattern (see `armenian-grammar.md`):
  `չ` + auxiliary + **negative participle** in `-ի/-ա`.
- 2sg form: `չ` + `ես` + `ասի` = `չես ասի`.
- Romanized correctly: `ches asi`.

So `ches asem` → meant `չես ասի` / `ches asi`.

The trap is that `em`/`es`/`e` (`-եմ` / `-ես` / `-է`) are person
markers, but they're also part of subjunctive endings (`-եմ` 1sg
subj, `-ես` 2sg subj, `-ի` 3sg subj). When the auxiliary is one
person and the lexical verb's ending suggests a *different* person,
the agreement is broken — and that's the diagnostic.

### Pitfall 3: vowel reduction baked into spelling

Colloquial Yerevan elides unstressed vowels and the schwa `ը`
(`pəti` for `պիտի`, `əmi` for `հիմի`, etc.). Writers may bake
these reductions into the Latin form (`pti`, `mi`) and skip the
schwas, producing what looks like consonant clusters that don't
exist in the literary form.

Heuristic: when you see an "impossible" Latin consonant cluster, try
inserting a schwa.

### Pitfall 4: similar-looking glyphs and unicode confusables

- `ք` vs Latin `q`, but Latin `q` is rare in transliteration so this
  is usually OK
- `ե` vs Greek `ε` — rarely confused
- `ɡ`/`g` ambiguous between `գ` and `ղ` (the latter often as `gh`)

### Pitfall 5: code-switched tokens

Russian-origin words in Armenian-language text retain Russian
inflection or get adapted to Armenian morphology. They will not
back-transliterate to native Armenian roots. Examples documented in
ghamoyan p48 (`ghamoyan/README.md` Topic 0):

- `tochken` → `տոչկեն` = Russian *точка* "dot/spot" + Armenian definite
  `-ե + -ն`.
- `svarka` → `սվարկա` = Russian *сварка* "welding," undeclined.
- `razbirat` → `ռազբիրատ` = Russian *разбирать* "figure out."
- `lyuboy mament zhiznid` → `լյուբոյ մամենտ ժիզնիդ` = Russian *любой
  момент жизни* + Armenian 2sg possessive `-իդ`.

If a back-transliteration produces an Armenian root that doesn't
exist in any dictionary, suspect code-switching first.

## Back-transliteration heuristics

A useful sequence for handling transliterated Armenian input:

1. **Detect the script.** Mixed Cyrillic + Latin in one token suggests
   code-switched Russian + Armenian. Pure Latin: try standard
   back-transliteration. Pure Armenian: no work needed.
2. **Naive back-transliterate** segment-by-segment using the high-
   agreement table above.
3. **Check the result against grammar.**
   - Is the auxiliary's person/number consistent with the lexical
     verb's ending?
   - Is the case-marking consistent with the syntactic role?
   - Does each word exist as a real Armenian root + recognized
     inflection?
4. **If broken, try register alternatives.**
   - `ա` for `է` in 3sg → re-form as colloquial copula
     (`grum a` → `գրում ա`).
   - Vowel-reduced spellings → restore schwas where required.
   - Final-letter drops in negative verb forms (`chem gali`
     → `չեմ գալիս`, with restored `-ս`).
5. **If still broken, check for code-switching.** Is one of the
   tokens a Russian root with Armenian inflection?
6. **If the result is grammatical but ambiguous**, surface the
   alternative parses to the user — they can disambiguate.

## The canonical example, end-to-end: `ches asem`

User input: `ches asem`

Step 1 — naive back-transliteration:
- `ches` → `չես` (high agreement: `ch` = `չ`, `e` = `ե`, `s` = `ս`).
- `asem` → `ասեմ`.

Step 2 — grammar check:
- `չես` = 2sg negative copula/auxiliary ("you aren't").
- `ասեմ` = 1sg subjunctive ("let me say" / "(I) might say").
- Combined: 2sg subject + 1sg verb → **agreement mismatch**.

Step 3 — register alternatives:
- Could `ches` be a register variant of `chem` (`չեմ`)? In some
  speakers' colloquial speech the auxiliary might shift, but `չեմ`
  vs `չես` are different persons, not register variants. So no.
- Could `asem` be a register variant of `asi`? Possibly — some
  speakers in fast speech might pronounce a closed vowel approaching
  `e` instead of `i`, especially before `m`-final morphology. But
  more likely this is a writer error.

Step 4 — alternative parse: did the writer mean negative
hypothetical 2sg?
- "you won't say" = `չ` + `ես` + `ասի` = `չես ասի`.
- Romanization of `չես ասի` = `ches asi`.
- Pattern: hypothetical-mood negation = `չ` + auxiliary + negative
  participle (-ի for first conjugation, -ա for second).

Step 5 — propose to user: "Did you mean `չես ասի` (you won't say,
2sg negative hypothetical)?" Show the literary form alongside the
input. If yes, fix; if no, ask for clarification.

## For AI Q&A

When answering Armenian questions where the user has supplied
transliterated input:

1. **Always run the heuristic sequence above** before treating the
   input as authoritative.
2. **Surface the back-transliteration explicitly** in the answer —
   "I read this as `չես ասի` (negative hypothetical 2sg of ասել)";
   the user can confirm or correct.
3. **Cite the relevant topic file** for the underlying grammar:
   `topics/morphology/negation.md` (TODO), the negation paradigm
   from `armenian-grammar.md`, etc.
4. **Acknowledge ambiguity** — if both `չես ասի` and `չես ասում` are
   plausible parses, list both with the difference explained.
5. **Flag register** — if the Latin form bakes a colloquialism
   (`grum a`, `chem gali`), point this out and show the literary
   alternative.

## Related docs

- `armenian-grammar.md` — negation grammar (the `չ + aux +
  neg-participle` rule that makes `չես ասի` correct).
- `grammar-terms.md` — trilingual grammar-term glossary
  (English / Armenian / Russian).
- `topics/morphology/colloquial_copula_a.md` — the `ա/է` swap that
  changes what writers spell.
- `topics/phonology/yerevan_consonant_reductions.md` — vowel/
  consonant elisions baked into colloquial spellings.
- `ghamoyan/README.md` § "Topic 0" — original seed notes (kept in
  place as historical record; this doc is now the primary
  reference).

## Open questions / gaps

- **No corpus of transliterated Armenian** to validate the convention
  table empirically. Real-world frequencies (does `gh` or `g` win for
  `ղ`?) would need a chat/social-media corpus.
- **No automated back-transliteration tool** — the heuristic sequence
  above is for a human or LLM to follow; not yet codified into a
  script.
- **Detection-side scripts** (Cyrillic-in-Armenian-text, Russian-
  root-with-Armenian-inflection) flagged in ghamoyan/README.md
  Topic 0 are still TODO.
- **Standardisation.** It's worth investigating whether any Armenian
  online communities have informal *de-facto* standards (a popular
  forum's transliteration FAQ, a community style guide). If so, this
  doc should align with it.
- **A topic-graph entry** — should this become
  `topics/pragmatics/latin_transliteration.md` for AI-Q&A topic
  loading? Constraint: the topic schema requires book-cited sources;
  this doc is partly project synthesis. Decide whether to extend
  the schema for `attestation: project-knowledge` topics, or keep
  this as a top-level doc only.
