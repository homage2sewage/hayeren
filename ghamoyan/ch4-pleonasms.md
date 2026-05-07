# Ch 4 — ԱՎԵԼՈՐԴԱԲԱՆՈՒԹՅՈՒՆՆԵՐ (Pleonasms)

Source: Ghamoyan/Sargsyan/Kartashyan, *Yerevan's Colloquial Language*
(2014), pp 87–90. Section heading at line 4277 of `out/full.md`.

The book groups pleonasms into 4 categories. Card-relevance ranking:

## 1. Filler words (*մակաբույծ բառեր*) — **HIGH recognition value**

Verbatim list (p87–88):

> Ըմ-ըմ, է-է, ա-ա, այսպիսով, լավ, բայց, սակայն, ուրեմն, ահա,
> ի միջի այլոց, կարծում եմ, իմ կարծիքով, հասկանում ենք, ասենք,
> ենթադրենք, համենայն դեպս, մի տեսակ, օֆ եսիմ, եսիմ, պարզ ա,
> տենց, տենց բաներ, բանը, բա

Plus slang fillers (p88): «խոսքի, քցենք, լսի».

Most useful for learner recognition:

| Form | Reading | Meaning |
|------|---------|---------|
| օֆ եսիմ | "ugh I-don't-know" | "ugh, whatever / dunno" |
| եսիմ | reduced "I don't know" (`ես իմ`) | "dunno" |
| տենց | reduced "այդպես" | "like that" |
| տենց բաներ | | "stuff like that" / "and so on" |
| պարզ ա | "(it's) clear" | "obviously / yeah" (with colloquial ա) |
| բա | particle | multipurpose: "well, so, but, eh?" |
| ի միջի այլոց | "in the middle of others" | "by the way" |
| համենայն դեպս | | "in any case" |
| մի տեսակ | "a sort" | "kind of, sort of" |

These are not in our deck yet — natural addition as a `colloquial filler`
tag. Without learning them you spend conversational bandwidth wondering
whether you're missing content.

## 2. Meaning-duplication pleonasms — low card value

Examples where two words convey the same thing (don't memorize, just be
aware):

- *նորից եմ կրկնում* — `կրկնել` already means "repeat"
- *նորից վերհիշեցի* — `վեր-` prefix already means "re-"
- *Քեզ հետ միասին* — `հետ` already means "together with"
- *մինչև առ այսօր* — `առ` already means "until"
- *միմյանց փոխադարձաբար* — `միմյանց` already means "reciprocally"
- *Անվճար նվեր* — gifts are free by definition (book blames advertising)

## 3. Self-evident-noun pleonasms — low card value

Don't say the obvious nominal class after a name:

- *Երևան քաղաքը* → *Երևանը* (Yerevan IS a city)
- *երկուշաբթի օրը* → *երկուշաբթի* (Monday IS a day)
- *հայերեն լեզուն* → *հայերենը* / *հայոց լեզուն*
- *դեղին գույնը* → *դեղինը* (yellow IS a color)
- *մարտ ամսին* → *մարտին* (March IS a month)

Plus a long list of "redundant adjective + noun" pairs (p89): *հանդիպել
միասին, լրացուցիչ բոնուս, ուրիշ այլընտրանք, տեղացի աբորիգեն,
ժողովրդական բանահյուսություն, անսպասելի անակնկալ, խառնել իրար,
փոխադարձ համագործակցություն* — all the same kind of redundancy English
speakers also commit.

## 4. ⭐ Russian-calque pleonasms — MEDIUM (linguistic awareness)

The book singles out a class of "non-Armenian" constructions that are
prevalent due to Russian substrate. These are *not* card material per
se, but learners with Russian background should be explicitly aware of
them — the constructions feel natural but aren't idiomatic Armenian:

| Calque (avoid) | Armenian native | Source / gloss |
|----------------|-----------------|----------------|
| գտնվում է լավ վիճակում | լավ վիճակում է | "is in a good condition" — Russian *находится* |
| հանդիսանում է ներկայացուցիչը | ներկայացուցիչ է | "is/serves as a representative" |
| համարվում է | է | "is considered to be" |
| բանը կայանում է նրանում, որ… | բանն այն է, որ… | "the thing is that..." — Russian *дело состоит в том, что* |
| Հայրենիքը՝ դա…  երազանքները՝ դրանք… | Հայրենիքը… | Russian *это*-appositive |
| IT տեխնոլոգիաներ | IT (already includes "technology") | abbreviation + redundant noun |
| CD դիսկ, LCD էկրան, GPS համակարգ | CD, LCD-ը, GPS-ը | same |

The book frames these as *սխալ* (errors) but acknowledges they're
deeply entrenched in spoken Armenian.

## On the slang word `լոքշ` (p48 — separate Ch 3 section)

Listed in the youth-jargon catalogue:

> *…քյառթու (գռեհիկ), փոստ ա (զվարճալի), **լոքշ ա (պարապություն)**,
> ֆազոտ (անկայուն մարդ)…* (p48)

- **Book gloss:** `պարապություն` — "idleness, vacancy, void"
- **Wiktionary:** noun "boredom, idleness"; adj "boring" (verified via glosser)
- **Idiomatic English:** "(it's) lame / nothing / a waste of time"
- **Origin:** Russian gambler's argot `локш` ("rubbish, dud") via the same
  Russian-substrate slang corridor that gave Yerevan speech `քյառթու`,
  `բոց`, `թույն` etc.

Construction is `<noun-as-predicate> + ա` (the colloquial copula we
documented in `ch4-verbs.md` §2): «լոքշ ա» = "it is loksh".

## Card-design suggestion (deferred)

Two new tags worth considering when/if we mine more of this book:

- `colloquial_filler` — items from §1 above (the *մակաբույծ բառեր*).
- `slang_yerevan` — items from p48's youth-jargon list (`լոքշ, թույն,
  բոց, քյառթու, փոստ, ֆազոտ` etc.).

Both should ride the `colloquial` umbrella tag from the verb section so
the user can suspend/show the whole register at once.

## Filler deck — first slice done

`../cards/ghamoyan/fillers.tsv` (32 entries). Per-row format:

```
Armenian \t  English (2-3 words) / Russian (2-3 words)  \t  tags
```

**Single back-of-card field** containing both languages, separated by
` / `. The two-language gestalt is intentional: for filler/discourse
markers especially, the English and Russian equivalents often
disambiguate each other (English "well" vs. Russian "ну" vs. "ладно"
vs. "давай"; the pair tells you which sense of "well" the Armenian
filler is doing). Seeing both at once is faster to internalize than
holding one and looking up the other.

Concise on purpose — no etymology, no Wiktionary citations in the cells
(those live in this file's verification record below).

Three sub-tags so registers can be enabled/suspended independently:

- `ghamoyan colloquial filler standard` — 21 entries. Literary
  discourse markers (ուրեմն, ի դեպ, համենայն դեպս, ըստ էության,
  իհարկե, ուղղակի…). Heard in formal speech and writing too.
- `ghamoyan colloquial filler casual` — 8 entries. Hesitation/
  intensifier fillers (եսիմ, օֆ եսիմ, տենց, բա, դե, պարզ ա…).
- `ghamoyan colloquial filler slang` — 3 entries. Yerevan jargon
  fillers from book p88 (լսի, խոսքի, քցենք).

### Anki import note

Anki note type for these cards needs **2 fields**: Armenian /
Translations. Tags column maps to Anki's tag field. With AnkiDroid:
File → Import → set delimiter to Tab → map Field 1=Armenian,
Field 2=Translations, Field 3=Tags.

The Translations field holds both English and Russian, separated by
` / `. The Anki card template will show both together — that's
intentional (see "Two-language gestalt" rationale above).

### Verification record (Tier 1)

Each Armenian token in the TSV was passed through `sakayan/glosser.py`
(Wiktionary lookup). Outcomes:

| Status | Count | Notes |
|--------|-------|-------|
| ✓ found on Wiktionary, agrees with my translation | ~22 | strong evidence |
| ✗ not in Wiktionary as a standalone entry | ~10 | mostly verb forms (կարծես, ասենք, ենթադրենք), reduced colloquials (տենց, քցենք), multi-word idioms whose components are findable but the whole isn't (համենայն դեպս, մի խոսքով) |

Sample of the strong-agreement findings (verbatim from glosser):

- `եսիմ` → Wiktionary "I don't know; who knows? how should I know?"
- `բա` → Wiktionary "what about (something not considered); exclamation
  of approval/surprise; of course"
- `դե` → Wiktionary "well"
- `իհարկե` → Wiktionary "of course, certainly, sure"
- `ուղղակի` → Wiktionary "directly, simply, plainly, just"
- `ըստ` + `էություն` → "according to" + "essence" → idiomatic
  "essentially / in essence"

For colloquial reductions and multi-word idioms not on Wiktionary
(`տենց` = `այդպես`, `քցենք` = `գցել` 1pl subj), the gloss is from the
book's context plus the literal reading — author judgment, not a
two-source claim. Russian translations are my own; not Wiktionary-
verified.

## Open follow-ups

- **Youth slang deep dive** (book Ch 3, p48). Listed in this file above;
  should produce a `slang_yerevan` tag with maybe 30-40 entries
  (`լոքշ, թույն, բոց, քյառթու, փոստ ա, ֆազոտ, ֆռցնել, դուխով, բքել…`
  plus the Russian-Armenian code-switch examples). **Don't forget.**
- Russian-calque pleonasms (§4 above) → could become a separate
  `colloquial_calque` tag if user finds it useful for *avoiding* these
  rather than producing them.
