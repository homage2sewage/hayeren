# Topic walk: Armenian predicative grammar in Russian wall text

**Date**: 2026-05-14
**Operator**: Claude Code, manual walk
**Status**: walk executed; topic proposal at bottom; not yet promoted to `topics/`.

## Motivation

A wall photograph from Yerevan (`photo_5199905489704129439_y.jpg`,
shared by the workspace operator) carries this graffiti tag, in a
boxed frame:

```
BRATVA
[ KRIVO NAR-DOS ]
ВСЕМ ПРОТИВ :)
```

The first two lines are Latin-transliterated Russian (`братва`,
`Кривой Нар-Дос`); the third is Cyrillic Russian — but the Russian is
**non-standard**:

- Standard Russian "against everyone" = `против всех`
  (preposition `против` + genitive `всех`).
- The wall has `всем против` — **dative `всем` + postposed `против`**.

Both deviations point the same direction: Armenian syntactic substrate
calquing into Russian lexicon. This walk gathers the corpus,
web-attestation, and morphological evidence required to call it a
calque rather than a Russian-internal coinage / blend.

## The diagnostic

Two non-standard moves stack:

| feature | standard Russian | wall Russian | Armenian (calque source) |
|---|---|---|---|
| case on "all" | `всех` (GEN pl) | `всем` (DAT pl) | `բոլոր-ին` (DAT) |
| order | `против` + N (prep) | N + `против` (postpos) | N + `դեմ` (postpos) |
| copula | absent (`я против`) | absent | absent (`եմ` ellipsable, here named-phrase reading) |

Either deviation alone would be weakly diagnostic — case-without-order
would just be a Russian-internal coinage on the `всем назло` (DAT +
adv-predicate) template; order-without-case would be elliptical
re-ordering of `против всех`. **The combination** is exactly the
morpheme-for-morpheme image of the Armenian predicative `<DAT> դեմ
[եմ/է/էր/...]` "(be) against <X>" frame.

Crucially, the Armenian case-frame and the wall's case-frame agree on
**dative**, not genitive — and Armenian distinguishes the two ("fight
*against* X" takes GEN, "be against X" takes DAT, see below).

## Corpus evidence

`grep -nE " դեմ\b" {sakayan,ghamoyan,parnasyan,tioyan}/out/full.jsonl`
(excluding the homonymous `դեմք` "face") returns ~25 uses of `դեմ` as a
postposition or predicative. The split is sharp:

### Pattern A — `<GEN> + դեմ + verb (պայքարել / կռվել / գնալ / բացել-դատ ...)`

Verbal-prepositional. Maps to **standard Russian `против <GEN>`**.

- ghamoyan p102, y[168-177]:
  > `կռվել թշնամու դեմ`
  "to fight against the enemy" (GEN `թշնամու`)

- ghamoyan p86, y[83-94]:
  > `թշնամու դեմ`
  (lexical entry headword)

- ghamoyan p97, y[77-87]:
  > `մեր լեզվի դեմ`
  "against our language" (GEN `մեր լեզվի`)

- ghamoyan p59, y[197-207]:
  > `դրա դեմ պետք է շարունակական պայքար տարվի`
  "a continued struggle must be waged against this" (GEN `դրա`)

- tioyan p225, y[1775-1820]:
  > `Հայության բոլոր ոսոխների դեմ կռվեի աճդուլ`
  "I'd fight against all the foes of Armenian-kind" (GEN
  `բոլոր ոսոխների`)

- **tioyan p226, y[269-313]** (the smoking-gun translation entry):
  > `բոլոր ոսոխների դեմ` — `против всех противников (врагов)`
  Tioyan's own Russian gloss. `GEN + դեմ` ↔ `против + GEN`.
  Standard Russian; no calque needed.

- sakayan p398, y[340-351]:
  > `Այս հարձակումն, ի դեմս Հրանտ Դինքի, կատարվել է մեր բոլորի
  > դեմ, ուղղված է մեր միասնության և կայունության դեմ»`
  "This attack, in the person of Hrant Dink, was carried out
  against all of us, directed against our unity and stability."
  (GEN `մեր բոլորի`, GEN `մեր միասնության և կայունության`)

- sakayan p394, y[103-114]:
  > `Քաբաթեքի՝ «Նյու Յորք Լայֆ» ապահովագրական ընկերության դեմ
  > բացված դատով`
  "by the lawsuit filed by Kabateki against the New York Life
  insurance company" (GEN)

- sakayan p424, y[389-400]:
  > `դատ բանալու եղբոր դեմ`
  "filing a lawsuit against the brother" (GEN `եղբոր`)

### Pattern B — `<DAT> + դեմ + լինել` (predicative)

The predicative-be construction. Maps to **`быть против <DAT>`** —
which Russian standardly inverts to `<NOM> против <GEN>` (with `быть`
elided in present), but Armenian preserves DAT throughout.

- **tioyan p319, y[1365-1408]** (the load-bearing single witness):
  > `Հայրը դեմ էր նրանց`
  "Father was against them" / *Отец был против них*.
  `Հայրը` (NOM) + `դեմ էր` (predicate-cop) + `նրանց` (DAT pl, the
  argument of `դեմ`).

- tioyan p285, y[778-822] (pedagogical anchor):
  > `վճռականապես դեմ լինել` — `быть решительно против`
  Tioyan explicitly maps `դեմ լինել` ↔ `быть против`. The argument
  case is left implicit in this entry but the structural pairing is
  locked.

- tioyan p279, y[833-877]:
  > `Նրան հարցրին, թե ում դեմ է ելույթ ունենալու: Его спросили,
  > против [кого он будет выступать]`
  `ում դեմ` — interrogative `ում` is GEN/DAT-syncretic, but the
  Russian gloss `против кого` makes the verbal-prepositional Pattern
  A reading available. Borderline; not load-bearing.

Pattern A produces standard Russian (`против всех противников`).
Pattern B is the one that calques into `всем против`.

## Web evidence

Armenian web search `"բոլորին դեմ եմ" OR "բոլորին դեմ է"` returns the
exact construction as the **name of a current Armenian political
movement / political party** — `Բոլորին դեմ եմ` "(I am) against
everyone."

- Movement homepage: https://bolorindem.am/
- Coverage: Azatutyun (RFE/RL Armenian), Aravot, Hetq, A1+,
  irates.am; YouTube channel; party founded February 2026 to
  contest the 2026 parliamentary elections on an electoral-reform
  platform.
- The Armenian phrase has **`բոլորին`** (DAT) — not the GEN
  `բոլորի` — confirming that the predicative `դեմ լինել` /
  `դեմ եմ` construction takes a dative argument and that the
  dative-form quantifier is the productive (not exceptional) shape.
- Movement's Russian-language self-presentation uses standard
  `против всех` (the electoral-ballot concept inherited from
  post-Soviet electoral systems). So the standard-Russian and
  Armenian-grammar forms **coexist** in the public discourse — the
  political-discourse register has the *standard* Russian; the
  wall-tag register has the *calqued* Russian.

This is the strongest possible "phrase is real, current, idiomatic"
evidence: it's the name of a registered political party.

## Why the case match is the smoking gun

The Russian template `всем + ADV-predicate` already exists — `всем
назло` "to spite everyone," `всем понятно` "everyone gets it," `всем
нравится` "everyone likes (it)" — so the wall's DAT case-marking
*could* in principle have arisen Russian-internally by analogy to that
template, with `против` reanalysed as adverbial-predicative on the
`назло` model.

But the analogy-from-`всем назло` analysis predicts:
- DAT case ✓ (matches)
- but **no specific reason for `против`** rather than another
  adverb-predicate — the template doesn't prefer `против` over
  `назло` / `понятно` / etc.

The substrate analysis predicts:
- DAT case ✓ (matches Armenian DAT-argument of `դեմ լինել`)
- AND the lexical choice of **`против`** specifically — because
  Tioyan's own pedagogical entry locks `դեմ լինել` ↔ `быть против`.

Substrate has lexical predictive power that template-by-analogy
lacks. The wall is more likely calqued from Armenian than coined from
Russian-internal templates.

(That said, the Russian template provides the *landing zone* — it's
why the calque parses at all to a Russian speaker, rather than being
read as broken Russian. The two analyses reinforce; they don't
compete.)

## What the wall does *not* show

- The construction `<DAT> + postposed-`против`` is *not* documented (so
  far in this walk) as an established feature of "Yerevan Russian" or
  "Armenian-Russian" contact variety — the targeted web searches
  ("ереванский русский", "армянский русский") returned no linguistic
  literature.
- A single graffito + one corpus minimal pair + one political slogan
  is structurally diagnostic but **frequency-unattested** as a
  *productive* L2 calque. Whether Armenian L1 speakers regularly
  produce `всем против` in spoken Russian remains an open question.

## Productive vs. confined: scope of the substrate signal

A natural question once `всем против` is analysed as a calque: does
the substrate signal extend to other constructions, or is it
lexically confined to this case? Honest answer: **likely the latter,
to a small set.**

Most Armenian DAT-governed predicates map to **Russian DAT-experiencer
predicates that already exist** (`մեզ պետք է` ↔ `нам нужно`, `քեզ
ծանոթ է` ↔ `тебе знакомо`, `ինձ ցավ է գալիս` ↔ `мне больно`). No
calque-divergence to detect; Russian's DAT-experiencer slot absorbs
them invisibly. The wall case is salient because Russian's `против`
diverges in two governance modes:

| | Russian `против` | Armenian `դեմ` |
|---|---|---|
| verbal-prepositional ("fight against") | prep + **GEN** | postpos + **GEN** |
| predicative ("be against") | indeclinable, **no complement** (`я против`) | postpos + **DAT** + copula |

The wall calques the *predicative* construction. Russian's
predicative `против` doesn't normally license a complement at all;
Armenian's `դեմ լինել` requires DAT. So the calque imports both **the
DAT case** AND **a complement position that Russian's predicative
doesn't independently license** — dual non-standardness that makes
the substrate signal visible.

Candidate siblings (same predicative-postposition dual-divergence):

- **`<DAT> + կողմ + լինել`** "to be in favor of <DAT>" → calque
  `всем за` "for everyone[DAT]." `կողմ` more naturally takes a
  possessive `<GEN> + կողմ` ("<X's> side"), so the DAT-frame may be
  marked rather than default — needs verification.
- **`<DAT> + հակառակ + լինել`** "to be opposed to <DAT>" → calque
  again `<DAT> против` (synonymous with `դեմ`). Same wall pattern, no
  new construction.

Beyond the **oppositional / aligned attitudinal-predicate** family
(`դեմ`, `կողմ`, `հակառակ`), candidate slots run dry. The substrate
analysis is real for the wall case; whether it generalises is an
empirical question with **probably a small positive answer**.

The disciplined way to extend a substrate prediction is to **vary one
axis at a time** from the source. Hold `против`, vary the noun
(`этим решениям против`, `Հայաստանին դեմ → Армении против`) — that
tests construction productivity within the lexical frame. Hold
`всем`, vary the adposition — that tests whether the substrate
extends to other Russian preps. Varying both at once (as the
2026-05-14-001 error entry catches) doesn't extend the pattern; it
free-associates.

### Falsifiable predictions, narrowed

- If we see `всем за` or `этому решению против` on another Yerevan
  wall / overheard / corpus, that's productivity-within-frame
  confirmed.
- If we see DAT-where-GEN-is-expected with a prep *outside* the
  oppositional-predicate family (e.g. `всем для`, `этому без`), the
  substrate generalises beyond the predictions above. Unlikely on
  the analysis here.
- If we never see another instance, the wall is an isolated calque
  rather than a register feature, and the topic-grade promotion is
  premature.

## Refining the substrate mechanism: preservation vs. underspecification vs. frame-transfer

Armenian's pronoun case system has multiple syncretisms Russian
keeps distinct. The corpus is explicit about this:

- **DAT = ACC** in the personal pronouns. Tioyan p95
  [y 2043-2204] declension paradigm:
  > `Дат. ինձ մեզ քեզ ձեզ`
  > `Вин. ինձ մեզ քեզ ձեզ`
  The DAT and ACC slots are formally identical for all four
  persons of the personal pronoun.
- **GEN ≠ DAT** strictly, but the GEN form is a different
  pronoun: `ձեր` "ваш" (genitive/possessive), distinct from
  `ձեզ` "вам / вас" (DAT/ACC). Parnasyan p96 [y 400-562]:
  > `ձեր — форма Род. (ед.), а ձեզ — дат. п. личного
  > местоимения դուք`
- **GEN/DAT on quantifiers** like `բոլոր` distinguish in form
  (`բոլորի` GEN, `բոլորին` DAT), but the DAT marker `-ին` is
  the oblique-stem + the definite article `-ն`, so the
  morphological boundary between "marked-GEN" and "marked-DAT"
  is a single suffix difference rather than separate paradigm
  slots. In colloquial use the line can blur in some
  constructions.

This refines the substrate analysis for the wall calque
`всем против`:

| model | mechanism | prediction |
|---|---|---|
| **Preservation** | Armenian `բոլորին` (DAT) is preserved as Russian `всем` (DAT) in calque | Armenian source-case maps one-to-one onto Russian target-case |
| **Underspecification** | Armenian source-case is itself underspecified for the L1 speaker (or absorbed into a syncretism); the Russian-L2 speaker picks whichever case the *Russian* construction template reaches for | Calque-target case is determined by Russian-internal templates, not by Armenian source-case |

The wall datum doesn't distinguish the two — both predict DAT
for `всем против` (preservation: Armenian DAT `բոլորին`
preserved; underspecification: Russian's `всем + adv-predicate`
template, cf. `всем назло`, reaches for DAT independently).
**Distinguishing prediction**: find a case where Armenian's
source-case-marking is unambiguously GEN (or another case) but
the Russian-L2 form goes to DAT (or another case) anyway. That
would favour the underspecification model.

Practical consequence: when looking for sibling Yerevan-Russian
substrate examples, the right test isn't "does Russian DAT
match Armenian DAT" — it's "does the Russian-L2 case-marking
follow a Russian construction template *more* tightly than it
follows the Armenian source case." If yes, the substrate
mechanism is underspecification-plus-template-pull, not
case-preservation.

### Third model: subcategorisation-frame transfer

A separate concern: the "two non-standard moves" framing
(case-shift + order-shift) initially treated those as
independent diagnostics. On closer reading they aren't — and
this points to a third, sharper model.

Russian natively has DAT-first order for the **`DAT + state-
predicate`** template:

- `Им смешно.` "they find it funny" — DAT-experiencer + indecl.
  state-pred.
- `Всем понятно.` "everyone gets it" — same.
- `Всем назло.` "to spite everyone" — same.
- `Мне всё равно.` "I don't care" — same.

So once a noun lands in DAT case in a state-predicate
construction, DAT-first order is **the natively-licensed
Russian order**. The wall's `всем против` isn't an inversion
relative to `всем смешно` / `всем назло` — it's the same
order. The "inversion" feeling came from comparing it to
`против всех` (prepositional frame), which is a *different*
template altogether.

Re-stated:

| feature | `против всех` (prep frame) | `всем смешно` (state-pred frame) | wall `всем против` |
|---|---|---|---|
| construction-type | prepositional | DAT-experiencer + state-pred | DAT-experiencer + state-pred |
| case on N | GEN | DAT | DAT (✓ for the state-pred template) |
| order | prep + N | N(DAT) + pred | N(DAT) + pred (✓ for the state-pred template) |
| lexical choice | `против` natively allowed | `смешно`/`понятно`/`назло` natively allowed | `против` **not natively allowed** as a DAT-experiencer state-pred |

So the wall's non-standardness collapses to **one** thing,
not two: `против` is being used as a DAT-experiencer state-
predicate, a frame Russian doesn't natively license for this
lexeme. Once that reanalysis is made, the DAT case and the
DAT-first order both fall out of Russian's existing
`DAT + state-pred` template.

This is **subcategorisation-frame transfer** — a recognised
contact-linguistics mechanism distinct from both
case-preservation and case-underspecification:

| model | what transfers from Armenian | what Russian supplies |
|---|---|---|
| Preservation | case-marking | nothing |
| Underspecification | absence of source-case | template-pulled case + order |
| **Frame-transfer** | lexical-syntactic subcategorisation frame: `դեմ լինել` takes DAT-experiencer + state-pred | DAT case, DAT-first order, all surface morphology |

Frame-transfer puts the substrate effect at the lexical level
(the choice of `против` as a state-predicate-with-complement),
where the wall's actual non-standardness sits. The
case-marking and order are *consequences* of that lexical
choice, not independent substrate signals.

The intuition "the inversion is due to Armenian postpositions"
is then partially right but at the wrong level: the L1
doesn't push word-order directly — it pushes the **lexical-
frame** ("be in opposition" takes a DAT-experiencer). The
order is supplied downstream by Russian's existing template,
which happens to be DAT-first.

### Sharpened falsifiable prediction

Under frame-transfer, the substrate generalisation isn't
"DAT-where-GEN-is-expected" — it's **Russian lexemes used in
DAT-experiencer-state-pred frames they don't natively license,
where their Armenian counterpart does**. Candidate slots
(probably small set, but worth scanning future wall photos /
overheard text for):

- `<DAT> + за` — calque of `<DAT> + կողմ + լինել`. Russian
  predicative `за` doesn't license a DAT-experiencer; Armenian
  `կողմ լինել` does.
- `<DAT> + не против` — same frame, negated. Predicts
  `всем не против` for "no one minds."
- Other state-pred adverbials whose Armenian counterparts take
  DAT-experiencer arguments: candidates would need to be
  enumerated from Armenian's predicative-postposition list.

The case-shift and order-shift become diagnostic *only* once
the lexeme-and-frame is verified — they're not independent
witnesses.

## Implications for `topics/`

A topic-grade entry is warranted:

- **`topics/contact-linguistics/`** (new domain folder) — for the
  general phenomenon of Armenian L1 grammar surfacing in Russian
  text. First entry: `armenian_predicative_calque_in_russian.md`.
- The first entry would cite:
  - tioyan p319 (DAT pronoun + `դեմ էր`)
  - tioyan p285 (`դեմ լինել` ↔ `быть против` pedagogical anchor)
  - tioyan p226 (`<GEN> դեմ` ↔ `против <GEN>` — the *non*-calqued
    Pattern A for contrast)
  - the `Բոլորին դեմ եմ` party as web-attested current usage
  - the wall photo as the surface evidence of the calque

Whether to land the topic now or wait for a second wall / spoken
example: judgment call. The corpus + party-name attestations are
structurally sufficient; a second surface example would harden the
frequency claim.

## Adjacent observation: toponym register

The wall's `KRIVO NAR-DOS` is a second linguistic datum — a colloquial
Yerevan district nickname (`Krivo`) juxtaposed with the official
street name (`Nar-Dos`). The operator notes that Yerevan district
naming has a three-way register typology: current admin / inherited
admin (often translated, e.g. *Monument*) / transformed nicknames
(e.g. *Силачи*, *Krivo*). Captured separately in
`research/2026-05-14-yerevan-district-naming.md` since the theme is
likely to recur on other wall photos / overheard speech.

## Related artifacts

- Photo: `photo_5199905489704129439_y.jpg` (workspace root).
- Wall-writings register note:
  `research/2026-05-14-yerevan-wall-writings.md` — frames the
  photo within the broader register and catalogues its four
  distinct writing layers.
- Toponym typology: `research/2026-05-14-yerevan-district-naming.md`.
- Adjacent code-switching note:
  `topics/lexicon/code_switching_with_russian.md`.
- Error captured during this walk:
  `errors/2026-05-14-001-self-falsifying-illustrative-example.md`.
