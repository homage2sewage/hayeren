# Deck validation report

- Deck: `cards/top_1000.tsv` (1097 rows)
- Findings: **116** (0 errors, 12 warnings)

## By category

| category | severity | count |
| --- | --- | --- |
| `ambiguous-sense` | warning | 106 |
| `duplicate-translation` | warning | 10 |

## `ambiguous-sense`

- **#  33** `պետք` → `needed, required / нужный, необходимый` — 2 POS senses; competing: [adj] needed, required / [noun] need, requirement
- **#  41** `մեկ` → `1` — 2 POS senses; competing: [num] one / [pron] someone, somebody
- **#  87** `հայ` → `Armenian / армянин, армянский` — 2 POS senses; competing: [adj] Armenian / [noun] Armenian
- **# 102** `առաջին [առաչին]` → `1st` — 2 POS senses; competing: [adj] first, earliest / [num] first
- **# 110** `նման` → `similar, like, resembling / похожий, подобный` — 2 POS senses; competing: [adj] similar, like, resembling / [postp] like, as, such as
- **# 115** `սխալ` → `wrong, incorrect / неправильный, ошибочный` — 2 POS senses; competing: [adj] wrong, incorrect / [noun] mistake, error
- **# 166** `ճիշտ` → `right, correct / правильный, верный` — 2 POS senses; competing: [adj] right, correct / [noun] truth
- **# 205** `ռուսերեն` → `Russian / русский (язык)` — 3 POS senses; competing: [adj] Russian (of or pertaining to the language) / [adv] in Russian / [noun] Russian (language)
- **# 211** `բանավոր` → `oral, verbal / устный` — 2 POS senses; competing: [adj] oral, verbal / [adv] orally, verbally
- **# 218** `վատ` → `bad / плохой` — 2 POS senses; competing: [adj] bad / [adv] badly
- **# 237** `ընդհանուր` → `general, universal, common / общий, всеобщий` — 2 POS senses; competing: [adj] general, universal, common / [adv] generally, in general
- **# 257** `վերջին [վերչին]` → `last, final / последний` — 2 POS senses; competing: [adj] last, final / [noun] definite dative singular of վերջ (verǰ)
- **# 269** `դժվար` → `hard, difficult, challenging / трудный, тяжёлый` — 2 POS senses; competing: [adj] hard, difficult, challenging / [adv] with difficulty
- **# 271** `հիվանդ` → `sick, ill, diseased / больной` — 2 POS senses; competing: [adj] sick, ill, diseased / [noun] patient, person who receives treatment
- **# 274** `նկատմամբ` → `towards, regarding, concerning / по отношению к, относительно` — 2 POS senses; competing: [noun] instrumental singular of նկատում (nkatum) / [postp] towards, regarding, concerning
- **# 297** `անց` → `passage, pass, passageway / проход, переход` — 2 POS senses; competing: [noun] passage, pass, passageway / [postp] after; past
- **# 298** `բաց` → `open, not closed / открытый` — 2 POS senses; competing: [adj] open, not closed / [noun] Bats (language)
- **# 305** `հեռու` → `far, distant, remote` — 3 POS senses; competing: [adj] far, distant, remote / [adv] far / [noun] distance
- **# 311** `որոշակի` → `certain, clear` — 2 POS senses; competing: [adj] certain, clear / [adv] certainly, clearly
- **# 320** `պատճառով` → `by reason of, because of` — 2 POS senses; competing: [noun] instrumental singular of պատճառ (patčaṙ) / [postp] by reason of, because of
- **# 339** `գրավոր` → `written` — 2 POS senses; competing: [adj] written / [noun] written homework
- **# 353** `ուստի` → `wherefrom, whence` — 2 POS senses; competing: [adv] wherefrom, whence / [conj] therefore, so, hence, consequently
- **# 364** `կար` → `seam` — 2 POS senses; competing: [noun] seam (where two pieces of fabric are sewn together / [verb] third-person singular imperfect indicative of կամ 
- **# 371** `հարուստ` → `rich` — 2 POS senses; competing: [adj] rich / [noun] rich man
- **# 373** `ազգային` → `national` — 2 POS senses; competing: [adj] national / [noun] compatriot, someone of the same ethnicity regardle
- **# 377** `երեկ` → `yesterday` — 2 POS senses; competing: [adv] yesterday / [noun] yesterday, the day before today
- **# 380** `գետ` → `knowing, having the knowledge` — 2 POS senses; competing: [adj] knowing, having the knowledge / [noun] river
- **# 381** `կանաչ` → `green` — 2 POS senses; competing: [adj] green / [noun] green (color)
- **# 383** `հաճախակի` → `frequent` — 2 POS senses; competing: [adj] frequent / [adv] often, frequently, repeatedly, constantly
- **# 384** `տարածված` → `common, widespread` — 2 POS senses; competing: [adj] common, widespread / [verb] resultative participle of տարածվել (taracvel)
- … and 76 more

## `duplicate-translation`

- **#   9** `այլ (#9), մյուս (#92)` → `other / другой` — 2 lemmas map to identical gloss
- **#  28** `հայերեն (#28), հայոց (#85)` → `armenian / армянский` — 2 lemmas map to identical gloss
- **# 394** `տեղի (#394), վայր (#936)` → `place` — 2 lemmas map to identical gloss
- **# 462** `հնչյուն (#462), ձայն (#504)` → `sound` — 2 lemmas map to identical gloss
- **# 490** `կրկին (#490), էլի (#827)` → `again` — 2 lemmas map to identical gloss
- **# 560** `ակ (#560), աղբյուր (#640)` → `spring, fountain, source of water` — 2 lemmas map to identical gloss
- **# 580** `ուժեղ (#580), ամուր (#1043)` → `strong` — 2 lemmas map to identical gloss
- **# 657** `բացել (#657), բանալ (#662)` → `to open` — 2 lemmas map to identical gloss
- **# 866** `հունարեն (#866), հունական (#1071)` → `greek` — 2 lemmas map to identical gloss
- **#1040** `միրգ [միրք] (#1040), պտուղ (#1053)` → `fruit` — 2 lemmas map to identical gloss
