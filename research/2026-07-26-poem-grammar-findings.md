# Poem-grammar session findings (2026-07-24 → 2026-07-26)

Conversation-driven walk: the operator is writing an Armenian poem
(converb-heavy, `-ով` end-rhymes, colloquial register touches) and
asked a chain of grammar questions. Each answer was KB-grounded per
`CLAUDE.md` § "Before answering an Armenian-language question"; the
non-obvious findings and where they were captured are recorded here.
Song lines quoted below (Ladaniva «Jako», Lav Eli «Արևին, արևին»)
are transcription-level — prompts for the questions, not corpus
evidence.

## 1. `-ելով` converb is subject-oriented — CAPTURED IN TOPIC

The instrumental-infinitive converb's implicit agent is the matrix
subject; a non-coreferent logical agent must surface in the dative
(dumtragut p535, rule + example (576); examples (570) p533, (585)
p537 all conform). Practical consequence: `*թողիր նրան քեզ
չգտնելով` cannot mean "leave him in a state where he didn't find
you" — the non-finder parses as the addressee of թողիր. Fix by
making the intended agent the matrix subject («մնա՝ քեզ չգտնելով»,
«թող նա մնա՝ …») or using a finite clause («թողիր, որ նա քեզ
չգտնի» — constructed).

→ `topics/morphology/participles.md` source [#18] + § "Orientation:
the implicit agent is the matrix subject" (added 2026-07-24; closed
the topic's own same-subject gap for the `-ով` half; `-իս` half
still open).

## 2. "Stay unfound": active `չգտնելով` vs passive `չգտնված`

`մնա չգտնելով` = "may he stay, *not finding*" (he is the failed
seeker). "Stay unfound" (not being found) needs the passive stem
`գտնվ-`:

- գտնվել "be found/discovered" attested: «Այն գտնվեց միայն 20-րդ
  դարի սկզբում» (sakayan p390).
- `գտնված` + locative in the discovery sense: «փողոցում գտնված
  երեխաներն» "children found in the street" (dumtragut p518).
- The "stay X-ed" complement slot `մնալ + -ած/adj` is productive:
  «Ավելի լավ սոված մնամ» (dumtragut p537), «մի վայրկյան մնաց
  անխոս», «մնացին սևեռած» (sakayan p423).

So «(օտար հողերում) չգտնված մնա» — constructed from cited parts.
Caveat (prior): գտնվել's dominant corpus sense is "be located", so
«օտար հողերում չգտնված» can flicker toward "never having been in
foreign lands"; «կորած մնա» sidesteps it. NOT yet a topic — the
resultative-complement (`մնալ + -ած`) pattern deserves one if it
recurs.

## 3. `ինքս/ինքդ` person agreement

The `-ս/-դ` suffix on `ինք-` encodes the person of the antecedent:
«ինքս я сам / ինքդ ты сам» (parnasyan p104, OCR), «Ես ինքս
կպատասխանեմ նրան», «դու ինքդ» (dumtragut p143), «Դու ինքդ գիտես»
(tioyan p96, OCR). Reflexive combos: «Ինքս ինձ համար մի ամբողջ
տիեզերք եմ» (sakayan p429), optional-intensifier «Ես մի գիրք
ուղարկեցի (ինքս) ինձ» (dumtragut p144). The 2sg combo «ինքդ քեզ»
is the regular analogue but has no corpus line (per the
no-pattern-extension rule, graded prior). Leaner alternative for
"freeing yourself": reflexive ազատվել, attested «Փորձելով ազատվել
դատավորի ձեռքից» (dumtragut p537). No topic — paradigm-table
material, candidate for a reflexives topic if it recurs.

## 4. Rhyming `-ով`; stress phonology

Stress "lies on the last syllable with a full vowel-nucleus"
(dumtragut p64) → line-final `-ով` is stressed and carries rhyme
alone (unlike English "-ing"). `-ով`/`-ով` pairs are grammatical
rhyme — abundant; Armenian verse practice runs suffix mono-rhyme
openly (`songs/dav-vnas-myus-angam.md` documents `-ական`/`-ան` and
`-երը`/`-ները` schemes). Stronger moves (prior — no KB source on
versification, a standing gap): rhyme deeper than the suffix;
cross category (converb vs noun-instr `սիրով/ցավով/սրտով`); rhyme
against lexical [ov] roots (ծով, հով, կով, ով).

## 5. Manner instrumental `սրտով`

Noun-in-instrumental is a standard manner adjunct (dumtragut p404
inventory). `սրտով` attested with modifiers: «ալեկոծ սրտով»
(sakayan p443), «թեթևացած սրտով …» (tioyan p125, OCR). Bare manner
«պարիր սրտով» — no corpus line; colloquially normal (`սրտովս է`
— prior). Fixed idiom «ի սրտե//սրտանց» (ghamoyan p102; usage
example parnasyan p204, OCR) — bookish register.

## 6. Colloquial imperative `-իր → -ի`

"In colloquial Armenian the imperative 2nd person SG ending -իր is
usually reduced to -ի" (dumtragut p290, example «Անուշ, ինձ նամակ
գրի»); Dum-Tragut annotates a verse quotation with exactly this
form (p706). Hence Ladaniva's «նայի'», and the doublet
պարիր ~ պարի available for meter. Candidate topic (colloquial
verb-form reductions) — ties in with p291 (colloquial 2pl from
present stem) and ghamoyan p37's final-consonant drops (թո, կո).

## 7. `էլ` scoping — TOPIC EXTENDED

`էլ` marks the constituent it follows (topic
`topics/syntax/el_particle_position.md`, status reviewed). New
this session: (a) «դու էլ պարիր» ≠ «պարիր էլ» — the second scopes
the verb ("also dance"), affirmative-imperative host is an uncited
slot; (b) Ladaniva's «Ես կպարեմ, դու էլ նայի'» shows the
paired-clause subject-switch shade («а ты», different predicates).
→ both added to that topic's gap list (2026-07-26).

## 8. One-syllable particles for the V___N slot

- `հենց` "just/precisely" — prepositive focus particle, attested
  postverbally before an oblique: «հենց գետնի վրա» (dumtragut
  p590); in an imperative clause: «հենց տնօրենի ճակատին ասա ամեն
  ինչ» (p466, colloquial); identity focus «նա հենց իրենց փնտրած
  անձնավորությունն է» (p474). «պարիր հենց սրտով» = "with the very
  heart."
- `լոկ` "only" — literary/poetic modal particle (dumtragut p185
  particle inventory; sakayan p494 glossary "only, just").
  «պարիր լոկ սրտով» = restrictive "with heart alone."
- `միշտ` "always" — plain adverb option. `դե` is clause-initial
  only (prior). `էլ` fits metrically but changes meaning (§7).

## 9. `էս` + plural

`էս/էդ/էն` are the այ>է colloquial variants of the demonstrative
series — ghamoyan states it metalinguistically (p36; series listed
again p44, p73). Demonstrative + plural is normal: «Կարո՞ղ եմ այս
գրքերը վերցնել գրադարանից» (dumtragut p188), «Սեմական այս
լեզուները» (sakayan p387). `էս` near plural: «էս ինչ էրեխեք են»
(ghamoyan p68); determiner use «էս մեր տան եղած-չեղածը» (sakayan
p411). Exact «էս + N-pl-ը» determiner shape unattested — safe
inference (pronunciation variant shares base syntax), residual gap.

## 10. Negative concord + bare-`մի` — NEW TOPIC

Obligatory double negation with negative indefinites (dumtragut
p546 rule; corpus uniform, zero counterexamples), `ոչ մի` = "the
negated indefinite article" (p160), and the force paradigm
bare-noun / `մի N` / `ոչ մի N` / `ո՜չ մի N` (all + negated verb;
`մի N չկա` = scalar "not a single N", not a weaker negation).
→ `topics/syntax/negative_concord.md` (new, 2026-07-26; 12/12
citations verified, lint clean).

## 11. Postposition `հետ` prosody

No source says `հետ` is never stressed: Dum-Tragut's never-stressed
inventory (p66) is proclitics only (պիտի/պետք, թող, prepositions ի,
առ, մինչ(և)) — postpositions absent from it, and no parallel
statement found (pp. 64–67 read directly; no IPA of pronoun+հետ in
corpus — gap). Phrase-level: clash deletion (p67) yields one beat
on neutral «քո հետ» (default on the pronoun — prior); emphasis/
contrast legitimately shifts stress (p66 deviations; p67 focus;
p706 any-stressable-syllable). Register note: «քո հետ» genitive is
the colloquial variant of normative dative «քեզ հետ»
(`topics/syntax/postposition_pronoun_case.md`).

## Process notes

- The Stop-hook's cited-arm fired four times this session — every
  time because a *constructed example* or cross-cited fragment
  shared a line with a book cite (never an actually-wrong page).
  Working rule reaffirmed: one cited fragment per line, its own
  cite only; constructed examples on cite-free lines, labelled.
- The auto-grounding hook's bundle surfaced the decisive evidence
  unprompted twice (tioyan p206 «Ուրիշ ելք չկար» for §10, ghamoyan
  p36/44/73 for §9) — the grep-first reflex paying for itself.

## Captured artifacts

- `topics/morphology/participles.md` — [#18] + Orientation section
  (2026-07-24).
- `topics/syntax/negative_concord.md` — new (2026-07-26).
- `topics/syntax/el_particle_position.md` — two gap entries
  (2026-07-26).
- This file.
