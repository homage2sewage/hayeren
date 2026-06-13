# Deck validation report

- Deck: `cards/top_1000.tsv` (1095 rows)
- Findings: **103** (0 errors, 11 warnings)

## By category

| category | severity | count |
| --- | --- | --- |
| `ambiguous-sense` | warning | 94 |
| `duplicate-translation` | warning | 9 |

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
- **# 298** `բաց` → `open, not closed / открытый` — 2 POS senses; competing: [adj] open, not closed / [noun] Bats (language)
- **# 305** `հեռու` → `far, distant, remote` — 3 POS senses; competing: [adj] far, distant, remote / [adv] far / [noun] distance
- **# 311** `որոշակի` → `certain, clear` — 2 POS senses; competing: [adj] certain, clear / [adv] certainly, clearly
- **# 320** `պատճառով` → `by reason of, because of` — 2 POS senses; competing: [noun] instrumental singular of պատճառ (patčaṙ) / [postp] by reason of, because of
- **# 339** `գրավոր` → `written` — 2 POS senses; competing: [adj] written / [noun] written homework
- **# 371** `հարուստ` → `rich` — 2 POS senses; competing: [adj] rich / [noun] rich man
- **# 373** `ազգային` → `national` — 2 POS senses; competing: [adj] national / [noun] compatriot, someone of the same ethnicity regardle
- **# 377** `երեկ` → `yesterday` — 2 POS senses; competing: [adv] yesterday / [noun] yesterday, the day before today
- **# 381** `կանաչ` → `green` — 2 POS senses; competing: [adj] green / [noun] green (color)
- **# 383** `հաճախակի` → `frequent` — 2 POS senses; competing: [adj] frequent / [adv] often, frequently, repeatedly, constantly
- **# 384** `տարածված` → `common, widespread` — 2 POS senses; competing: [adj] common, widespread / [verb] resultative participle of տարածվել (taracvel)
- **# 400** `հատկանիշ` → `characteristic, distinctive, peculiar, idiosyncratic` — 2 POS senses; competing: [adj] characteristic, distinctive, peculiar, idiosyncrat / [noun] characteristic, feature, property, attribute
- **# 409** `սուրբ` → `holy, sacred` — 2 POS senses; competing: [adj] holy, sacred / [noun] saint
- **# 414** `անցյալ` → `past, last` — 2 POS senses; competing: [adj] past, last / [noun] the past
- **# 417** `առավել` → `more, much, far` — 2 POS senses; competing: [adv] more, much, far / [noun] the untilled land left at the edges of the field
- … and 64 more

## `duplicate-translation`

- **#   9** `այլ (#9), մյուս (#92)` → `other / другой` — 2 lemmas map to identical gloss
- **#  28** `հայերեն (#28), հայոց (#85)` → `armenian / армянский` — 2 lemmas map to identical gloss
- **# 394** `տեղի (#394), վայր (#933)` → `place` — 2 lemmas map to identical gloss
- **# 462** `հնչյուն (#462), ձայն (#503)` → `sound` — 2 lemmas map to identical gloss
- **# 489** `կրկին (#489), էլի (#825)` → `again` — 2 lemmas map to identical gloss
- **# 578** `ուժեղ (#578), ամուր (#1037)` → `strong` — 2 lemmas map to identical gloss
- **# 655** `բացել (#655), բանալ (#660)` → `to open` — 2 lemmas map to identical gloss
- **# 864** `հունարեն (#864), հունական (#1065)` → `greek` — 2 lemmas map to identical gloss
- **#1034** `միրգ [միրք] (#1034), պտուղ (#1047)` → `fruit` — 2 lemmas map to identical gloss
