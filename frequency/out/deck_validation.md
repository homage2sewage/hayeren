# Deck validation report

- Deck: `cards/top_1000.tsv` (1000 rows)
- Findings: **149** (0 errors, 25 warnings)

## By category

| category | severity | count |
| --- | --- | --- |
| `ambiguous-sense` | warning | 127 |
| `duplicate-translation` | warning | 20 |
| `golden-missing` | warning | 2 |

## `ambiguous-sense`

- **#  26** `թե` → `that` — 2 POS senses; competing: [conj] that / [particle] serves as an interrogative particle
- **#  34** `պետք` → `needed, required` — 2 POS senses; competing: [adj] needed, required / [noun] need, requirement
- **#  43** `մեկ` → `one` — 2 POS senses; competing: [num] one / [pron] someone, somebody
- **#  79** `առաջ [առաչ]` → `forward` — 3 POS senses; competing: [adv] forward / [noun] front part; front, anterior / [postp] before
- **#  91** `հայ` → `Armenian` — 2 POS senses; competing: [adj] Armenian / [noun] Armenian
- **#  94** `կողմ` → `around, at about` — 2 POS senses; competing: [adv] around, at about / [noun] side; direction
- **# 106** `առաջին [առաչին]` → `first, earliest` — 2 POS senses; competing: [adj] first, earliest / [num] first
- **# 114** `նման` → `similar, like, resembling` — 2 POS senses; competing: [adj] similar, like, resembling / [postp] like, as, such as
- **# 118** `գնում` → `purchase` — 2 POS senses; competing: [noun] purchase (act) / [verb] imperfective converb of գնել (gnel)
- **# 120** `սխալ` → `wrong, incorrect` — 2 POS senses; competing: [adj] wrong, incorrect / [noun] mistake, error
- **# 124** `ալ` → `scarlet, bright red` — 2 POS senses; competing: [adj] scarlet, bright red / [adv] Western Armenian form of էլ (ēl)
- **# 155** `տվյալ` → `given, present, this` — 2 POS senses; competing: [adj] given, present, this / [noun] that which is given
- **# 159** `վեր` → `more than` — 4 POS senses; competing: [adj] more than / [adv] up / [noun] upside, upper part / [postp] higher than
- **# 175** `ճիշտ` → `right, correct` — 2 POS senses; competing: [adj] right, correct / [noun] truth
- **# 218** `ռուսերեն` → `Russian` — 3 POS senses; competing: [adj] Russian (of or pertaining to the language) / [adv] in Russian / [noun] Russian (language)
- **# 225** `բանավոր` → `oral, verbal` — 2 POS senses; competing: [adj] oral, verbal / [adv] orally, verbally
- **# 233** `վատ` → `bad` — 2 POS senses; competing: [adj] bad / [adv] badly
- **# 234** `դեմ` → `the front part` — 2 POS senses; competing: [noun] the front part / [postp] against
- **# 254** `տակ` → `bottom, lower part` — 2 POS senses; competing: [noun] bottom, lower part / [postp] under, beneath, below
- **# 255** `ընդհանուր` → `general, universal, common` — 2 POS senses; competing: [adj] general, universal, common / [adv] generally, in general
- **# 266** `մեկն` → `correctly, right, upright` — 2 POS senses; competing: [adv] correctly, right, upright (referring e.g. to the w / [pron] definite nominative singular of մեկ (mek)
- **# 276** `վերջին [վերչին]` → `last, final` — 2 POS senses; competing: [adj] last, final / [noun] definite dative singular of վերջ (verǰ)
- **# 288** `դժվար` → `hard, difficult, challenging` — 2 POS senses; competing: [adj] hard, difficult, challenging / [adv] with difficulty
- **# 290** `հիվանդ` → `sick, ill, diseased` — 2 POS senses; competing: [adj] sick, ill, diseased / [noun] patient, person who receives treatment
- **# 293** `նկատմամբ` → `towards, regarding, concerning` — 2 POS senses; competing: [noun] instrumental singular of նկատում (nkatum) / [postp] towards, regarding, concerning
- **# 312** `ներս` → `the inside` — 2 POS senses; competing: [noun] the inside / [postp] in, inside
- **# 316** `անց` → `passage, pass, passageway` — 2 POS senses; competing: [noun] passage, pass, passageway / [postp] after; past
- **# 317** `բաց` → `open, not closed` — 2 POS senses; competing: [adj] open, not closed / [noun] Bats (language)
- **# 320** `ընթացքում` → `during` — 2 POS senses; competing: [adv] during / [noun] locative singular of ընթացք (əntʻacʻkʻ)
- **# 324** `հեռու` → `far, distant, remote` — 3 POS senses; competing: [adj] far, distant, remote / [adv] far / [noun] distance
- … and 97 more

## `duplicate-translation`

- **#   9** `այլ (#9), մյուս (#96)` → `other` — 2 lemmas map to identical gloss
- **#  89** `հայոց (#89), հայ (#91)` → `armenian` — 2 lemmas map to identical gloss
- **# 100** `գիտենալ (#100), իմանալ (#986)` → `to know` — 2 lemmas map to identical gloss
- **# 144** `փոքր (#144), փոքրիկ (#474)` → `small` — 2 lemmas map to identical gloss
- **# 176** `նամակ (#176), գիր (#1083)` → `letter` — 2 lemmas map to identical gloss
- **# 182** `տանել (#182), վերցնել (#1105)` → `to take` — 2 lemmas map to identical gloss
- **# 194** `կարելի (#194), հնարավոր (#573)` → `possible` — 2 lemmas map to identical gloss
- **# 215** `դեմք (#215), երես (#439)` → `face` — 2 lemmas map to identical gloss
- **# 218** `ռուսերեն (#218), ռուս (#593)` → `russian` — 2 lemmas map to identical gloss
- **# 240** `հին (#240), ծեր (#551)` → `old` — 2 lemmas map to identical gloss
- **# 249** `հատկապես (#249), մանավանդ (#937)` → `especially` — 2 lemmas map to identical gloss
- **# 262** `լույս (#262), թեթև (#1182)` → `light` — 2 lemmas map to identical gloss
- **# 309** `նորից (#309), կրկին (#521), էլի (#910)` → `again` — 3 lemmas map to identical gloss
- **# 421** `տեղի (#421), վայր (#1034)` → `place` — 2 lemmas map to identical gloss
- **# 490** `հնչյուն (#490), ձայն (#535)` → `sound` — 2 lemmas map to identical gloss
- **# 596** `ակ (#596), աղբյուր (#689)` → `spring, fountain, source of water` — 2 lemmas map to identical gloss
- **# 621** `ուժեղ (#621), ամուր (#1141)` → `strong` — 2 lemmas map to identical gloss
- **# 711** `բացել (#711), բանալ (#716)` → `to open` — 2 lemmas map to identical gloss
- **# 961** `հունարեն (#961), հունական (#1169)` → `greek` — 2 lemmas map to identical gloss
- **#1138** `միրգ [միրք] (#1138), պտուղ (#1151)` → `fruit` — 2 lemmas map to identical gloss

## `golden-missing`

- **#  -1** `ապրես` → `` — in golden set but absent from deck; expected one of: well done, attaboy, молод
- **#  -1** `ես` → `` — in golden set but absent from deck; expected one of: i, я
