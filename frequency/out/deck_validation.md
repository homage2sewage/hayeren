# Deck validation report

- Deck: `cards/top_1000.tsv` (1074 rows)
- Findings: **141** (2 errors, 21 warnings)

## By category

| category | severity | count |
| --- | --- | --- |
| `ambiguous-sense` | warning | 121 |
| `duplicate-translation` | warning | 18 |
| `truncated-lemma` | error | 2 |

## `ambiguous-sense`

- **#  26** `թե` → `that` — 2 POS senses; competing: [conj] that / [particle] serves as an interrogative particle
- **#  33** `պետք` → `needed, required` — 2 POS senses; competing: [adj] needed, required / [noun] need, requirement
- **#  42** `մեկ` → `one` — 2 POS senses; competing: [num] one / [pron] someone, somebody
- **#  88** `հայ` → `Armenian` — 2 POS senses; competing: [adj] Armenian / [noun] Armenian
- **#  91** `կողմ` → `around, at about` — 2 POS senses; competing: [adv] around, at about / [noun] side; direction
- **# 103** `առաջին [առաչին]` → `first, earliest` — 2 POS senses; competing: [adj] first, earliest / [num] first
- **# 111** `նման` → `similar, like, resembling` — 2 POS senses; competing: [adj] similar, like, resembling / [postp] like, as, such as
- **# 115** `գնում` → `purchase` — 2 POS senses; competing: [noun] purchase (act) / [verb] imperfective converb of գնել (gnel)
- **# 117** `սխալ` → `wrong, incorrect` — 2 POS senses; competing: [adj] wrong, incorrect / [noun] mistake, error
- **# 121** `ալ` → `scarlet, bright red` — 2 POS senses; competing: [adj] scarlet, bright red / [adv] Western Armenian form of էլ (ēl)
- **# 150** `տվյալ` → `given, present, this` — 2 POS senses; competing: [adj] given, present, this / [noun] that which is given
- **# 154** `վեր` → `more than` — 4 POS senses; competing: [adj] more than / [adv] up / [noun] upside, upper part / [postp] higher than
- **# 168** `ճիշտ` → `right, correct` — 2 POS senses; competing: [adj] right, correct / [noun] truth
- **# 208** `ռուսերեն` → `Russian` — 3 POS senses; competing: [adj] Russian (of or pertaining to the language) / [adv] in Russian / [noun] Russian (language)
- **# 214** `բանավոր` → `oral, verbal` — 2 POS senses; competing: [adj] oral, verbal / [adv] orally, verbally
- **# 221** `վատ` → `bad` — 2 POS senses; competing: [adj] bad / [adv] badly
- **# 222** `դեմ` → `the front part` — 2 POS senses; competing: [noun] the front part / [postp] against
- **# 239** `տակ` → `bottom, lower part` — 2 POS senses; competing: [noun] bottom, lower part / [postp] under, beneath, below
- **# 240** `ընդհանուր` → `general, universal, common` — 2 POS senses; competing: [adj] general, universal, common / [adv] generally, in general
- **# 251** `մեկն` → `correctly, right, upright` — 2 POS senses; competing: [adv] correctly, right, upright (referring e.g. to the w / [pron] definite nominative singular of մեկ (mek)
- **# 261** `վերջին [վերչին]` → `last, final` — 2 POS senses; competing: [adj] last, final / [noun] definite dative singular of վերջ (verǰ)
- **# 273** `դժվար` → `hard, difficult, challenging` — 2 POS senses; competing: [adj] hard, difficult, challenging / [adv] with difficulty
- **# 275** `հիվանդ` → `sick, ill, diseased` — 2 POS senses; competing: [adj] sick, ill, diseased / [noun] patient, person who receives treatment
- **# 278** `նկատմամբ` → `towards, regarding, concerning` — 2 POS senses; competing: [noun] instrumental singular of նկատում (nkatum) / [postp] towards, regarding, concerning
- **# 297** `ներս` → `the inside` — 2 POS senses; competing: [noun] the inside / [postp] in, inside
- **# 301** `անց` → `passage, pass, passageway` — 2 POS senses; competing: [noun] passage, pass, passageway / [postp] after; past
- **# 302** `բաց` → `open, not closed` — 2 POS senses; competing: [adj] open, not closed / [noun] Bats (language)
- **# 305** `ընթացքում` → `during` — 2 POS senses; competing: [adv] during / [noun] locative singular of ընթացք (əntʻacʻkʻ)
- **# 309** `հեռու` → `far, distant, remote` — 3 POS senses; competing: [adj] far, distant, remote / [adv] far / [noun] distance
- **# 315** `որոշակի` → `certain, clear` — 2 POS senses; competing: [adj] certain, clear / [adv] certainly, clearly
- … and 91 more

## `duplicate-translation`

- **#   9** `այլ (#9), մյուս (#93)` → `other` — 2 lemmas map to identical gloss
- **#  86** `հայոց (#86), հայ (#88)` → `armenian` — 2 lemmas map to identical gloss
- **#  97** `գիտենալ (#97), իմանալ (#893)` → `to know` — 2 lemmas map to identical gloss
- **# 139** `փոքր (#139), փոքրիկ (#450)` → `small` — 2 lemmas map to identical gloss
- **# 169** `նամակ (#169), գիր (#990)` → `letter` — 2 lemmas map to identical gloss
- **# 175** `տանել (#175), վերցնել (#1012)` → `to take` — 2 lemmas map to identical gloss
- **# 185** `կարելի (#185), հնարավոր (#543)` → `possible` — 2 lemmas map to identical gloss
- **# 205** `դեմք (#205), երես (#416)` → `face` — 2 lemmas map to identical gloss
- **# 208** `ռուսերեն (#208), ռուս (#561)` → `russian` — 2 lemmas map to identical gloss
- **# 226** `հին (#226), ծեր (#522)` → `old` — 2 lemmas map to identical gloss
- **# 234** `հատկապես (#234), մանավանդ (#851)` → `especially` — 2 lemmas map to identical gloss
- **# 294** `նորից (#294), կրկին (#494), էլի (#832)` → `again` — 3 lemmas map to identical gloss
- **# 398** `տեղի (#398), վայր (#941)` → `place` — 2 lemmas map to identical gloss
- **# 466** `հնչյուն (#466), ձայն (#508)` → `sound` — 2 lemmas map to identical gloss
- **# 564** `ակ (#564), աղբյուր (#644)` → `spring, fountain, source of water` — 2 lemmas map to identical gloss
- **# 584** `ուժեղ (#584), ամուր (#1048)` → `strong` — 2 lemmas map to identical gloss
- **# 661** `բացել (#661), բանալ (#666)` → `to open` — 2 lemmas map to identical gloss
- **#1045** `միրգ [միրք] (#1045), պտուղ (#1058)` → `fruit` — 2 lemmas map to identical gloss

## `truncated-lemma`

- **# 328** `պայմանավորված` → `conditioned by, due to / обусловленный` — dictionary has `պայմանավորվածություն` — `ություն` was stripped
- **# 341** `միավոր` → `unit / единица` — dictionary has `միավորություն` — `ություն` was stripped
