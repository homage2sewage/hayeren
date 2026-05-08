# Deck sample for human-eye review

Source: `cards/top_1000.tsv` (839 rows)
Sampling: top-25, bottom-25, 50 random middle (seed=0)

**How to read.** Scan as a learner would, not as a pipeline reviewer. For each row ask: *would this be useful as a flashcard front/back?* Anything off — verbose gloss, dictionary prose, awkward phrasing, register mismatch, missing context — is a candidate for a new `check_*` in `validate_deck.py` or a `HAND_OVERRIDE` in `build_deck.py`.

## Top 25

| rank | lemma | gloss | src |
|---:|---|---|---|
| 1 | `լինել` | to be | sakayan-paradigm |
| 2 | `կարդալ [կարտալ]` | to read | sakayan-paradigm |
| 3 | `գրել` | to write | sakayan-paradigm |
| 4 | `ինչ` | what / что | hand-override |
| 5 | `ունենալ` | to have | sakayan-vocab |
| 6 | `իսկ` | but, and (contrast) / а, же | hand-override |
| 7 | `այո` | yes / да | hand-override |
| 8 | `շատ` | very, much, many / очень, много | hand-override |
| 9 | `գալ` | to come | sakayan-vocab |
| 10 | `մի` | one, a; don't! / один, а; не (запрет) | hand-override |
| 11 | `բայց` | but / но | hand-override |
| 12 | `ոչ` | no, not / нет, не | hand-override |
| 13 | `ձեր` | your (pl/formal) / ваш | hand-override |
| 14 | `գիտենալ` | to know | sakayan-vocab |
| 15 | `էլ` | too, also | sakayan-vocab |
| 16 | `որ` | that, which, who / что, который | hand-override |
| 17 | `սեր` | love (noun) / любовь | frequency-gap |
| 18 | `ու` | and / и | hand-override |
| 19 | `ասել` | to say | sakayan-vocab |
| 20 | `ինձ` | me / меня, мне | hand-override |
| 21 | `նստել` | to sit down | sakayan-paradigm |
| 22 | `հայերեն` | Armenian / армянский | hand-override |
| 23 | `անել` | to do | sakayan-vocab |
| 24 | `տեսնել` | to see | sakayan-vocab |
| 25 | `չէ` | no, isn't (it?) / нет, не так ли | hand-override |

## Random middle (50)

| rank | lemma | gloss | src |
|---:|---|---|---|
| 41 | `դառնալ` | to become, to turn | sakayan-vocab |
| 68 | `հետ` | back | dictionary |
| 90 | `տաք` | warm | sakayan-vocab |
| 103 | `լեզու` | language | sakayan-vocab |
| 124 | `բարձր [բարցր]` | high | sakayan-vocab |
| 126 | `իր` | his/her (own, reflexive) / его/её (свой) | hand-override |
| 130 | `հաճելի` | pleasant | sakayan-vocab |
| 132 | `ձյուն` | snow | sakayan-vocab |
| 175 | `տարի` | year / год | hand-override |
| 176 | `գույն` | color | sakayan-vocab |
| 184 | `նաև` | also / также | hand-override |
| 246 | `փորձել [փորցել]` | to try | sakayan-vocab |
| 262 | `թռչուն` | bird | sakayan-vocab |
| 297 | `գրականություն` | literature | dictionary |
| 311 | `գրասեղան` | writing desk, desk / письменный стол | hand-override |
| 312 | `աթոռ` | chair | dictionary |
| 340 | `ամսական` | monthly | dictionary |
| 375 | `պատրաստ` | prepared, ready | dictionary |
| 387 | `ջերմություն` | heat, warmth | dictionary |
| 396 | `ցավ` | pain, ache | dictionary |
| 420 | `գոնե` | at least | dictionary |
| 454 | `անպայման` | absolute, unconditional | dictionary |
| 462 | `հեռու` | far, distant, remote | dictionary |
| 497 | `կդառնա` | will become, will turn into | sakayan-vocab |
| 513 | `ձմերուկ` | watermelon | sakayan-vocab |
| 519 | `հայրենիք` | fatherland | sakayan-vocab |
| 535 | `տվեց` | gave (3sg aor of տալ) / дал(-а) | hand-override |
| 550 | `կանգնած` | standing | sakayan-vocab |
| 559 | `հուսահատ` | desperate | sakayan-vocab |
| 596 | `գրեթե` | almost | sakayan-vocab |
| 601 | `տձև` | deformed | sakayan-vocab |
| 610 | `կնճիթ` | trunk | sakayan-vocab |
| 630 | `լավագույն` | best | sakayan-vocab |
| 637 | `բնութագիր` | recommendation | sakayan-vocab |
| 647 | `նրբանկատ [նրփանկատ]` | considerate | sakayan-vocab |
| 659 | `հատկություն` | quality | sakayan-vocab |
| 676 | `գանձապահ` | cashier | sakayan-vocab |
| 680 | `դիվանագետ` | diplomat | sakayan-vocab |
| 688 | `վարսահարդար` | hairdresser | sakayan-vocab |
| 712 | `կոշկակար` | shoemaker | sakayan-vocab |
| 731 | `կոկիկ` | neat | sakayan-vocab |
| 740 | `թույլ` | weak | sakayan-vocab |
| 748 | `տերևախիտ` | full of leaves | sakayan-vocab |
| 770 | `պտուղ` | fruit | sakayan-vocab |
| 817 | `թոռնիկ` | grandson | sakayan-vocab |
| 849 | `իննսուն` | ninety | dictionary |
| 873 | `միայն` | only / только | hand-override |
| 890 | `թեքել` | to tilt, incline, bend | dictionary |
| 938 | `մենք` | we / мы | hand-override |
| 941 | `ֆրանսիա` | France | dictionary |

## Bottom 25

| rank | lemma | gloss | src |
|---:|---|---|---|
| 959 | `կողմ` | around, at about | dictionary |
| 960 | `լեռ` | mountain, mount | dictionary |
| 961 | `գերմանիա` | Germany | dictionary |
| 962 | `ամուսին` | husband | dictionary |
| 963 | `հունաստան` | Greece | dictionary |
| 964 | `երրորդ [երրորթ]` | thirdly | dictionary |
| 965 | `որոշել` | to decide | dictionary |
| 967 | `ռուսաստան` | Russia / Россия | hand-override |
| 968 | `քո` | your (sg) / твой | hand-override |
| 969 | `այսպիսի` | such; such a; of this kind; like this | dictionary |
| 970 | `ի դեպ` | by the way | dictionary |
| 971 | `ի միջի այլոց` | by the way / кстати | hand-override |
| 973 | `ըստ էության` | in essence, essentially, basically | dictionary |
| 974 | `իրականում` | actually, in reality / на самом деле | ghamoyan-filler |
| 975 | `ուղղակի` | just, simply / просто, прямо | ghamoyan-filler |
| 976 | `պարզապես` | simply, just / просто | ghamoyan-filler |
| 979 | `կարճ ասած` | long story short | dictionary |
| 981 | `ենթադրել` | to suppose, assume, presume | dictionary |
| 983 | `եսիմ` | dunno, who knows / не знаю, фиг знает | ghamoyan-filler |
| 985 | `տենց` | like that / так, вот так | ghamoyan-filler |
| 987 | `բա` | well, what about / ну, а как же | hand-override |
| 988 | `դե` | well, come on / ну, давай | hand-override |
| 989 | `բանը` | the thing is / дело в том, штука в том | ghamoyan-filler |
| 992 | `խոսք` | speech | dictionary |
| 993 | `քցել` | to throw, drop (colloq var. of գցել) / бросить, ронять | hand-override |
