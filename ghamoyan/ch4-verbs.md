# Ch 4 — ԲԱՅ section (verb morphology in colloquial Yerevan)

Source: Ghamoyan/Sargsyan/Kartashyan, *Yerevan's Colloquial Language*
(2014), pp 73-75. Section heading on line 3587 of `out/full.md`.

Notes from a first read-through, organized by claim. Verification
applied: every Armenian quote is verbatim from the book; grammar
terms are cross-referenced to `../grammar-terms.md`; key lemmas
checked via `../sakayan/lookup.py`.

## High-impact patterns (recommended for cards)

### 1. ⭐ `ա` ⇄ `է` — colloquial 3sg copula / present auxiliary

The single most pervasive Yerevan-vs-literary divergence. Where the
literary norm uses `է` (3sg "is" / present aux), spoken Yerevan
uses `ա`.

| Literary | Colloquial | Gloss |
|----------|-----------|-------|
| մեծ է | մեծ ա | (it) is big |
| լավն է | լավն ա | (it) is good (with def. art.) |
| գրում է | գրում ա | (he/she) is writing |
| գալիս է | գալիս ա | (he/she) is coming |
| ուտում է | ուտում ա | (he/she) is eating |

Source quote: «ա-ն փոխարինում է է օժանդակ բային, ինչպես՝ գրում ա,
գալիս ա, ուտում ա» (p73, line 3603).

**Card design suggestion.** Don't make these "wrong" cards. Instead:
add a new tag `colloquial` and emit pair-cards where each literary
form has its colloquial counterpart on the back, so the learner can
*recognize* both in input.

### 2. `չի` ⇄ `չէ` — negative copula in nominal predicates

| Literary | Colloquial | Gloss |
|----------|-----------|-------|
| ցուրտ չէ | ցուրտ չի | (it) is not cold |
| վատը չէ | վատը չի | (it) is not bad |
| քնած չէ | քնած չի | (he/she) is not asleep |
| տուն չէ | տուն չի | (he/she) is not home |

Source quote: «ցուրտ չի, վատը չի, քնած չի, տուն չի և այլն, գրականում
հանձնարարելի են ցուրտ չէ, վատը չէ, քնած չէ, տուն չէ և այլ ձևերը»
(p74).

Pairs with the `ա/է` swap: same `է → ա` shift, just with the
negation prefix `չ-`.

### 3. Imperative singular without final `-ր`

| Literary | Colloquial | Gloss |
|----------|-----------|-------|
| խոսի՛ր | խոսի՛ | speak! |
| գրի՛ր | գրի՛ | write! |
| թռի՛ր | թռի՛ | fly! / jump! |
| բարձրացի՛ր | բարձրացի՛ | rise!, get up! |
| մի՛ երգիր | մի՛ երգի | don't sing! |
| մի՛ կանգնիր | մի՛ կանգնի | don't stop! |

Source quote: «խոսակցական լեզվում հիմնականում գործածվում է
առանց ր-ի ձևը» (p74).

Note: only the `-իր` imperative loses `-ր`. The `-ա` imperative
(from `-ալ` verbs) doesn't have this issue.

### 4. Imperative plural shortened (`-եցեք` / `-ացեք` → `-եք` / `-աք`)

| Literary | Colloquial |
|----------|-----------|
| գրեցե՛ք | գրե՛ք (write! pl) |
| նստեցե՛ք | նստե՛ք (sit! pl) |
| ասացե՛ք | ասե՛ք (say! pl) |
| մի՛ նստեք (already short) | մի՛ նստեք |

Source: «գրեցե՛ք-գրե՛ք, նստեցե՛ք-նստե՛ք, ասացե՛ք-ասե՛ք» (p74).

### 5. Compound predicate: subjunctive instead of infinitive after modal

| Literary | Colloquial | Gloss |
|----------|-----------|-------|
| ուզում եմ կանչել | ուզում եմ կանչեմ | I want to call |
| վախենում եմ ասել | վախենում եմ ասեմ | I'm afraid to say |

Source: «խոսակցական լեզվում այն հաճախ կազմվում է խոնարհված
բայ + ըղձական եղանակի բայաձև կառույցով» (p75).

The colloquial version repeats the subject across both verbs:
literally "I-want I-call" instead of "I-want to-call". Russian
parallel: «*хочу позвонить*» (literary) vs. «*хочу я позвоню*»
(stylistically marked) — actually this is closer to South-Slavic
syntactic patterns than Russian.

### 6. Short aorist forms (drop `-եց-`)

Literary 1sg aorist with `-եց-` marker → colloquial without it:

| Literary | Colloquial | Gloss |
|----------|-----------|-------|
| հանձնեցի | հանձնի | I handed in |
| բերեցի | բերի | I brought |

Source: «կարճ ձևերին նախապատվություն տալը, ինչպես՝ հանձնի,
բերի (փոխ.՝ հանձնեցի, բերեցի)» (p73).

Note: this overlaps with #4 — both are "drop the cuneiform `-եց-`"
patterns.

## Medium / lower impact (documentation, not cards)

### 7. Inserted `-ն-` in some verbs (nonstandard)

Literary `թռչել` "fly" → colloquial `թռնել`. Literary `փախչել`
"flee" → colloquial `փախնել`. Book frames as deviation.

### 8. Causative `-եցն-` ↔ `-ացն-` confusion

Correct: հիշեցնել, ցավեցնել, քնեցնել, իջեցնել, խոսեցնել, մոտեցնել.
Wrong: հիշացնել, ցավացնել, քնացնել, իջացնել, խոսացնել, մոտացնել.

Documented as error.

### 9. The substandard `-իմ` aorist (vulgarism)

Forms like `գրիմ` for `գրեցի` "I wrote", `տեսամ` for `տեսա` "I saw",
`էկամ` for `եկա` "I came". Book labels *հասարակաբանական* —
"vulgarisms / lower-register".

Recognition value only.

### 10. -ել / -ալ infinitive confusion

Some speakers say `խոսալ` for `խոսել`. Documented as error.

### 11. Person-shifting (1pl for 2sg, 2sg for impersonal)

Pragmatic device, not a morphological pattern. Not card material.

### 12. Pleonastic `չ-` in perfect tense

Wrong: թռչել եմ (for թռել եմ), կպչել եմ (for կպել եմ).
Correct: թռել եմ "I have flown", կպել եմ "I have stuck".

Recognition only.

### 13. Causative aorist over-application of `-եց-`

Wrong: խոսեցրեցի, խոսեցրեցիր (double `-եց-`).
Correct: խոսեցրի, խոսեցրիր.

Pure error pattern; don't internalize.

## Card design follow-ups (decision pending)

If we mine this, the natural addition to the deck is a `colloquial`
tag layer. Two card-type ideas:

1. **Colloquial-recognition cards.** Front: colloquial form; Back:
   literary form + meaning. e.g. `գրում ա` → `գրում է / "(he/she) is
   writing"`. The literary form already exists in the deck via
   paradigms; the colloquial form is the new card.

2. **Doubled paradigms.** For each verb already in `paradigms_data.py`,
   add a colloquial alternate row where it diverges: 3sg present
   becomes `գրում է / գրում ա`. This reads in Anki as either form
   accepted.

(1) is more SRS-honest because each form gets its own retrieval
schedule. (2) reduces card count but conflates the registers.

I'd lean (1) for items 1-6 above, plus a `colloquial` deck tag so
they can be hidden/shown as a group.
