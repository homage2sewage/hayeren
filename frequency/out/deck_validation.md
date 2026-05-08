# Deck validation report

- Deck: `cards/top_1000.tsv` (993 rows)
- Findings: **237** (0 errors, 180 warnings)

## By category

| category | severity | count |
| --- | --- | --- |
| `ambiguous-sense` | info | 57 |
| `duplicate-translation` | warning | 18 |
| `empty-translation` | warning | 154 |
| `golden-missing` | warning | 2 |
| `mwu-leak` | warning | 6 |

## `ambiguous-sense`

- **#  37** `համար` → `number` — 2 POS senses; competing: [noun] number / [postp] for
- **#  48** `թե` → `that` — 2 POS senses; competing: [conj] that / [particle] serves as an interrogative particle
- **#  68** `հետ` → `back` — 2 POS senses; competing: [adv] back / [postp] with
- **#  87** `մեկ` → `one` — 2 POS senses; competing: [num] one / [pron] someone, somebody
- **# 141** `դժվար` → `hard, difficult, challenging` — 2 POS senses; competing: [adj] hard, difficult, challenging / [adv] with difficulty
- **# 150** `պետք` → `needed, required` — 2 POS senses; competing: [adj] needed, required / [noun] need, requirement
- **# 157** `վատ` → `bad` — 2 POS senses; competing: [adj] bad / [adv] badly
- **# 160** `սպիտակ` → `white` — 2 POS senses; competing: [adj] white / [noun] white
- **# 191** `առաջին` → `first, earliest` — 2 POS senses; competing: [adj] first, earliest / [num] first
- **# 207** `վաղը` → `tomorrow` — 2 POS senses; competing: [adv] tomorrow / [noun] tomorrow, the day after today
- **# 210** `կարոտ` → `in want of something, needing, wanting` — 2 POS senses; competing: [adj] in want of something, needing, wanting / [noun] longing (for), yearning (for); nostalgia
- **# 213** `շնորհակալություն` → `gratefulness, thankfulness` — 2 POS senses; competing: [noun] gratefulness, thankfulness / [particle] thank you, thanks
- **# 214** `ապրես` → `attaboy!, well done!` — 2 POS senses; competing: [intj] attaboy!, well done! / [verb] second-person singular future subjunctive/optative
- **# 223** `մասին` → `definite dative singular of մաս` — 2 POS senses; competing: [noun] definite dative singular of մաս (mas) / [postp] about; regarding
- **# 225** `ուղիղ` → `straight, direct` — 3 POS senses; competing: [adj] straight, direct / [adv] straight, directly / [noun] straight line
- **# 249** `առաջ [առաչ]` → `forward` — 3 POS senses; competing: [adv] forward / [noun] front part; front, anterior / [postp] before
- **# 276** `կամաց` → `slow` — 2 POS senses; competing: [adj] slow / [adv] slowly
- **# 287** `ռուսերեն` → `Russian` — 3 POS senses; competing: [adj] Russian (of or pertaining to the language) / [adv] in Russian / [noun] Russian (language)
- **# 305** `հայ` → `Armenian` — 2 POS senses; competing: [adj] Armenian / [noun] Armenian
- **# 323** `հաշվիչ` → `counting` — 2 POS senses; competing: [adj] counting / [noun] counter; meter; register
- **# 337** `կենացդ` → `cheers!` — 2 POS senses; competing: [noun] nominative singular second-person possessive of կե / [particle] cheers!
- **# 340** `ամսական` → `monthly` — 3 POS senses; competing: [adj] monthly / [adv] monthly / [noun] menstruation, period
- **# 347** `նման` → `similar, like, resembling` — 2 POS senses; competing: [adj] similar, like, resembling / [postp] like, as, such as
- **# 353** `ծանոթ` → `familiar, known` — 2 POS senses; competing: [adj] familiar, known / [noun] acquaintance; friend
- **# 369** `էժան` → `cheap, inexpensive; low` — 2 POS senses; competing: [adj] cheap, inexpensive; low (of price) / [adv] cheaply, inexpensively
- **# 370** `հազար` → `lettuce, Lactuca` — 2 POS senses; competing: [noun] lettuce, Lactuca / [num] thousand
- **# 374** `անց` → `passage, pass, passageway` — 2 POS senses; competing: [noun] passage, pass, passageway / [postp] after; past
- **# 380** `բաց` → `open, not closed` — 2 POS senses; competing: [adj] open, not closed / [noun] Bats (language)
- **# 383** `ձախ` → `left; left-hand` — 3 POS senses; competing: [adj] left; left-hand / [adv] to the left (of) / [noun] left, the left side; the left hand
- **# 406** `առատ` → `abundant, abounding, plentiful, copious` — 2 POS senses; competing: [adj] abundant, abounding, plentiful, copious / [adv] abundantly, aboundingly, plentifully, copiously
- … and 27 more

## `duplicate-translation`

- **#  65** `փոքր (#65), փոքրիկ (#789)` → `small` — 2 lemmas map to identical gloss
- **#  68** `հետ (#68), մեջք [մեչք] (#599)` → `back` — 2 lemmas map to identical gloss
- **#  76** `բանալ (#76), բացել (#780)` → `to open` — 2 lemmas map to identical gloss
- **# 119** `հին (#119), ծեր (#720)` → `old` — 2 lemmas map to identical gloss
- **# 131** `ուժեղ (#131), ամուր (#538)` → `strong` — 2 lemmas map to identical gloss
- **# 174** `նորից (#174), կրկին (#582)` → `again` — 2 lemmas map to identical gloss
- **# 187** `մյուս (#187), այլ (#479)` → `other` — 2 lemmas map to identical gloss
- **# 198** `վերջապես [վերչապես] (#198), ի_վերջո (#281)` → `finally` — 2 lemmas map to identical gloss
- **# 208** `ցանկանալ (#208), ուզենալ (#555)` → `to wish` — 2 lemmas map to identical gloss
- **# 233** `երեկո (#233), երեկոյան (#443)` → `evening` — 2 lemmas map to identical gloss
- **# 248** `կլինի (#248), հեշտ (#543)` → `it will be easy` — 2 lemmas map to identical gloss
- **# 430** `կարճ (#430), կարճահասակ (#734)` → `short` — 2 lemmas map to identical gloss
- **# 507** `միրգ [միրք] (#507), պտուղ (#770)` → `fruit` — 2 lemmas map to identical gloss
- **# 547** `վառ (#547), պայծառ (#777)` → `bright` — 2 lemmas map to identical gloss
- **# 568** `մեջ (#568), ներս (#799)` → `the inside` — 2 lemmas map to identical gloss
- **# 683** `ինժեներ (#683), ճարտարագետ (#684)` → `engineer` — 2 lemmas map to identical gloss
- **# 761** `հով (#761), քամի (#929)` → `wind` — 2 lemmas map to identical gloss
- **# 900** `ելույթ (#900), խոսք (#992)` → `speech` — 2 lemmas map to identical gloss

## `empty-translation`

- **#  34** `գիտել` → `` — no card source or local dict entry covered this lemma
- **#  98** `գնանք` → `` — no card source or local dict entry covered this lemma
- **# 117** `կարոյ` → `` — no card source or local dict entry covered this lemma
- **# 135** `որն` → `` — no card source or local dict entry covered this lemma
- **# 145** `քննեմ` → `` — no card source or local dict entry covered this lemma
- **# 151** `պալյան` → `` — no card source or local dict entry covered this lemma
- **# 154** `ծանոթացնեմ` → `` — no card source or local dict entry covered this lemma
- **# 182** `մի_օր` → `` — no card source or local dict entry covered this lemma
- **# 211** `սարյան` → `` — no card source or local dict entry covered this lemma
- **# 227** `գրվել` → `` — no card source or local dict entry covered this lemma
- **# 238** `քաղաքել` → `` — no card source or local dict entry covered this lemma
- **# 251** `իրավաց` → `` — no card source or local dict entry covered this lemma
- **# 258** `երկր` → `` — no card source or local dict entry covered this lemma
- **# 291** `պարոնյան` → `` — no card source or local dict entry covered this lemma
- **# 293** `հիսունութ` → `` — no card source or local dict entry covered this lemma
- **# 298** `մալյան` → `` — no card source or local dict entry covered this lemma
- **# 300** `կոմիտաս` → `` — no card source or local dict entry covered this lemma
- **# 301** `քսանութ` → `` — no card source or local dict entry covered this lemma
- **# 302** `հիսունմեկ` → `` — no card source or local dict entry covered this lemma
- **# 309** `տառեր` → `` — no card source or local dict entry covered this lemma
- **# 313** `գրքեր` → `` — no card source or local dict entry covered this lemma
- **# 314** `տետրեր` → `` — no card source or local dict entry covered this lemma
- **# 317** `ուսանողներն` → `` — no card source or local dict entry covered this lemma
- **# 324** `կտաք` → `` — no card source or local dict entry covered this lemma
- **# 328** `չարժե` → `` — no card source or local dict entry covered this lemma
- **# 335** `կլցնես` → `` — no card source or local dict entry covered this lemma
- **# 342** `նշանածն` → `` — no card source or local dict entry covered this lemma
- **# 343** `կողքիններ` → `` — no card source or local dict entry covered this lemma
- **# 345** `ծնողներիդ [ծնողներիտ]` → `` — no card source or local dict entry covered this lemma
- **# 349** `կարծեմ` → `` — no card source or local dict entry covered this lemma
- … and 124 more

## `golden-missing`

- **#  -1** `ես` → `` — in golden set but absent from deck; expected one of: i, я
- **#  -1** `վերցնել` → `` — in golden set but absent from deck; expected one of: pick up, take, брать

## `mwu-leak`

- **#  -1** `մի_քիչ` → `` — both `մի_քիչ` and components ['մի', 'քիչ'] appear — review whether all occurrences merged
- **#  -1** `դուր_գալ` → `` — both `դուր_գալ` and components ['դուր', 'գալ'] appear — review whether all occurrences merged
- **#  -1** `կարծես_թե` → `` — both `կարծես_թե` and components ['կարծես', 'թե'] appear — review whether all occurrences merged
- **#  -1** `մի_տեսակ` → `` — both `մի_տեսակ` and components ['մի', 'տեսակ'] appear — review whether all occurrences merged
- **#  -1** `մի_օր` → `` — both `մի_օր` and components ['մի', 'օր'] appear — review whether all occurrences merged
- **#  -1** `ամեն_ինչ` → `` — both `ամեն_ինչ` and components ['ամեն', 'ինչ'] appear — review whether all occurrences merged
