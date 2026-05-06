# Grammar terminology — English / Armenian / Russian

Trilingual glossary for Armenian-language grammar discussions. Covers
the terms that show up in Sakayan, Wiktionary's `--table` output, the
verb-conjugation paradigms in `sakayan/paradigms_data.py`, and standard
Russian linguistics references.

When Russian and Armenian don't map cleanly (cases especially —
Armenian has 7, Russian 6), the cell notes the closest equivalent and
the mismatch.

## Parts of speech / Մասերի խոսքի / Части речи

| English | Armenian | Russian |
|---------|----------|---------|
| noun | գոյական | существительное |
| verb | բայ | глагол |
| adjective | ածական | прилагательное |
| adverb | մակբայ | наречие |
| pronoun | դերանուն | местоимение |
| numeral | թվական | числительное |
| preposition | նախդիր | предлог |
| postposition | (post-position) | послелог |
| conjunction | շաղկապ | союз |
| interjection | ձայնարկություն | междометие |
| particle | մասնիկ / եղանակավորող | частица |
| article | հոդ | артикль (Armenian has them, Russian doesn't) |
| determiner | որոշիչ | определитель / детерминатив |

## Grammatical case / Հոլով / Падеж

Armenian has 7 cases. Russian has 6. The mapping isn't 1:1 — see
notes per row.

| English | Armenian | Russian | Notes |
|---------|----------|---------|-------|
| nominative | ուղղական (հոլով) | именительный | matches |
| genitive | սեռական | родительный | matches |
| dative | տրական | дательный | matches |
| accusative | հայցական | винительный | matches; Armenian merges accusative with nominative for inanimate nouns |
| ablative | բացառական | (no exact case; *исходный* descriptively) | Russian uses prepositions (*из / от / с*) where Armenian uses ablative case ending |
| instrumental | գործիական | творительный | matches |
| locative | ներգոյական | (closest: предложный) | Russian's prepositional is preposition+noun; Armenian's locative is a true case ending |

## Number / Թիվ / Число

| English | Armenian | Russian |
|---------|----------|---------|
| singular | եզակի | единственное число |
| plural | հոգնակի | множественное число |
| dual (historical) | երկակի | двойственное (древнерусское) |

## Person / Դեմք / Лицо

| English | Armenian | Russian |
|---------|----------|---------|
| 1st person | առաջին դեմք | первое лицо |
| 2nd person | երկրորդ դեմք | второе лицо |
| 3rd person | երրորդ դեմք | третье лицо |

## Mood / Եղանակ / Наклонение

| English | Armenian | Russian | Notes |
|---------|----------|---------|-------|
| indicative | սահմանական | изъявительное | factual statements |
| subjunctive | ստորադասական | сослагательное | wishes, conditions, subordinate clauses |
| conditional / hypothetical | պայմանական (Sakayan: hypothetical) | условное | with `կ-` prefix in Armenian |
| imperative | հրամայական | повелительное | direct commands |
| prohibitive | արգելական | (отрицательное повелительное) | the `մի՛` + verb form |
| mandative | հարկադրական | долженствовательное (no native Russian term — usually translated as "значение долженствования") | `պիտի / պետք է` + verb |
| resultative | հարակատար | результативное | `-ած` + auxiliary; describes resulting state |

## Tense / Ժամանակ / Время

Aspects are baked into Armenian tenses; the table notes which.

| English | Armenian | Russian | Notes |
|---------|----------|---------|-------|
| present | ներկա | настоящее | Eastern Armenian's only present covers both English present simple and continuous |
| imperfect | անցյալ անկատար | прошедшее несовершенное / имперфект | `-ում էի` |
| aorist (simple past) | անցյալ կատարյալ / պարզ անցյալ | прошедшее совершенное / аорист | `-եց-/-աց-` + endings |
| present perfect | վաղակատար ներկա | настоящее перфектное / перфект | `-ել եմ` |
| pluperfect | վաղակատար անցյալ | давнопрошедшее / плюсквамперфект | `-ել էի` |
| future | ապառնի | будущее | `-ելու եմ` |
| future imperfect | ապառնի անկատար | будущее несовершенное | `-ելու էի` |

## Aspect / Կերպ / Вид

| English | Armenian | Russian |
|---------|----------|---------|
| perfective | կատարյալ կերպ | совершенный вид |
| imperfective | անկատար կերպ | несовершенный вид |
| iterative / habitual | բազմակատար / սովորութային | многократный вид (rare) |
| resultative | հարակատար | результативное |

## Voice / Սեռ / Залог

| English | Armenian | Russian |
|---------|----------|---------|
| active | ներգործական | действительный залог |
| passive | կրավորական | страдательный залог |
| causative | պատճառական | каузатив (понудительный залог) |
| middle / reflexive | միջանկյալ (rare term) | возвратный |

## Non-finite verb forms / Դերբայներ / Неличные формы глагола

Armenian groups all non-finite verb forms under "դերբայ" (literally
"non-personal"). Russian distinguishes "причастие" (participle —
adjectival) from "деепричастие" (converb — adverbial). The same
Armenian form can act as either depending on context, so the mapping
is contextual.

| English (Wiktionary terminology) | Armenian (Sakayan terminology) | Russian | Form |
|----------------------------------|--------------------------------|---------|------|
| infinitive | անորոշ դերբայ | инфинитив / неопределённая форма | `գրել`, `կարդալ` |
| subject participle (active, "the one who Vs") | ենթակայական դերբայ | действительное причастие настоящего времени | `գրող` |
| resultative participle ("having Ved") | հարակատար դերբայ | результативное причастие | `գրած` |
| simultaneous / synchronic converb ("while Ving") | համընթաց դերբայ | деепричастие одновременности | `գրելիս` |
| imperfective converb (bound, "Ving" — used in present) | անկատար դերբայ | имперфективное причастие | `գրում` |
| perfective converb (bound, "Ved" — used in perfect) | վաղակատար դերբայ | перфективное причастие | `գրել` (= infinitive form for I conj.) |
| future converb / future participle ("going to V") | ապառնի դերբայ | причастие будущего времени | `գրելու` |
| connegative / negative participle (used in `չեմ V-ի`) | ժխտական դերբայ | отрицательное причастие | `գրի` |
| instrumental converb ("by Ving") | (no Sakayan term — `-ելով` form) | деепричастие способа / образа действия | `գրելով` |

Note: Sakayan's `-իք` form (`գրելիք` "what is to be written") is also a
future participle but with a slightly different sense — closer to a
gerundive ("what should be written"). Wiktionary calls it "future
converb II".

## Conjugation / Խոնարհում / Спряжение

| English | Armenian | Russian |
|---------|----------|---------|
| conjugation | խոնարհում | спряжение |
| declension | հոլովում | склонение |
| inflection | թեքում | словоизменение / флексия |
| stem | հիմք | основа |
| root | արմատ | корень |
| ending | վերջավորություն | окончание |
| suffix | վերջածանց | суффикс |
| prefix | նախածանց | приставка |
| infix | միջածանց | инфикс |
| affix | ածանց | аффикс |

## Sentence elements / Նախադասության անդամներ / Члены предложения

| English | Armenian | Russian |
|---------|----------|---------|
| sentence | նախադասություն | предложение |
| clause | երկրորդական (subordinate) / գլխավոր (main) | придаточное / главное |
| subject | ենթակա | подлежащее |
| predicate | ստորոգյալ | сказуемое |
| direct object | ուղիղ խնդիր | прямое дополнение |
| indirect object | անուղղակի խնդիր | косвенное дополнение |
| modifier / attribute | որոշիչ | определение |
| adverbial | պարագա | обстоятельство |
| copula | հանգույց / օժանդակ բայ | связка |

## Other / Ուրիշ / Прочее

| English | Armenian | Russian |
|---------|----------|---------|
| gender | սեռ (grammatical) | род | Armenian has no grammatical gender |
| animacy | շնչավորություն | одушевлённость | Armenian uses different declension for human nouns |
| definiteness | որոշյալություն | определённость / неопределённость |
| article (definite) | որոշյալ հոդ | определённый артикль | Armenian: `-ը / -ն` |
| article (indefinite) | անորոշ հոդ | неопределённый артикль | Armenian: `մի` |
| definite article (possessive) | -ս / -դ | (no equivalent — Russian uses possessive pronouns) |
| pronominal possessive | ստացական դերանուն | притяжательное местоимение |
| transitive | ներգործական (verb) | переходный |
| intransitive | չեզոք | непереходный |
| pro-drop | ենթական բացակայ (descriptive) | (язык) с опущением подлежащего | Armenian, like Russian, allows omission of pronoun subjects |
| auxiliary verb | օժանդակ բայ | вспомогательный глагол | `եմ` "to be" is the main aux |
| modal verb | եղանակավորող բայ | модальный глагол |
| epenthesis (schwa insertion) | ձայնավորի ներդրում | эпентеза | `փոքր → /pŏkŏr/` with epenthetic ə |
| converb | դերբայի մակբայական ձև (descriptive) | деепричастие |
| participle | դերբայի ածականական ձև (descriptive) / դերբայ (broad) | причастие |

## Eastern Armenian–specific quirks

A few terms that are easier to learn together with their Russian
analogue, since the *concept* exists in Russian but with different
grammar:

| Phenomenon | Armenian | Russian analogue / explanation |
|-----------|----------|--------------------------------|
| voiced→aspirated alternation in some words (`ընդունել → ընթունել`) | (no canonical name; "բարբառային ձև") | оглушение согласных перед глухими — comparable but not identical (Russian devoices clusters; Armenian alternation is lexical, not phonological) |
| pro-drop (verb ending alone signals subject) | ենթական բացակայել | ясно из формы глагола; в русском так же |
| post-positional definite article (`գիրքը`) | որոշյալ -ը հոդ | (нет аналога — русский использует артикля нет, определённость передаётся контекстом / порядком слов) |
| three-way stop contrast (voiced / voiceless / aspirated: բ պ փ) | (no specific term) | в русском двухчастная система — звонкий/глухой; армянский добавляет придыхательные |
| ev-ligature `և` | (one letter) | одна буква-лигатура `и` (грубая аналогия — но `й` ближе по звучанию к `ев`) |
