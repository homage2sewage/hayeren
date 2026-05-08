# Lemma validation

Validated top-100 lemmas of `our_top_1000.tsv` via `sakayan/glosser.py` (Wiktionary lookup) + a small 'looks-suspicious' heuristic for short truncated stems.

## Summary

- **valid**: 72 (72%)
- **multi-meaning**: 9 (9%)
- **suspicious-but-found**: 19 (19%)
- **not-found**: 0 (0%)
- **suspicious**: 0 (0%)


## suspicious-but-found  (19)

| rank | lemma | count | notes |
|-----:|-------|------:|-------|
| 4 | ես | 66 | [very short (≤2 chars)] ego, the self; եմ (2 s pres) |
| 6 | եմ | 60 | [very short (≤2 chars)] I am |
| 7 | եք | 38 | [very short (≤2 chars)] եմ (2 p pres) |
| 8 | մի | 36 | [very short (≤2 chars)] one; don't! |
| 15 | են | 25 | [very short (≤2 chars)] եմ (3 p pres) |
| 18 | ոչ | 23 | [very short (≤2 chars)] no; not; no |
| 21 | էլ | 20 | [very short (≤2 chars)] also, too; any more |
| 24 | ու | 17 | [very short (≤2 chars)] and; The 34th letter of Armenian alphabet according to Reformed Orthography. Represents close ba |
| 31 | չէ | 15 | [very short (≤2 chars)] է (neg form); no |
| 32 | սա | 15 | [very short (≤2 chars)] this |
| 42 | էր | 11 | [very short (≤2 chars)] եմ (3 s impf) |
| 45 | օր | 10 | [very short (≤2 chars)] day |
| 46 | թե | 10 | [very short (≤2 chars)] that; or |
| 58 | կա | 9 | [very short (≤2 chars)] կամ (3 s pres indc) |
| 59 | եթե | 8 | [ends in bare vowel 'ե', likely truncated] if |
| 71 | րոպե | 8 | [ends in bare vowel 'ե', likely truncated] minute; unspecified short time, moment |
| 82 | էի | 7 | [very short (≤2 chars)] եմ (1 s impf) |
| 95 | հիմա | 6 | [ends in bare vowel 'ա', likely truncated] the present; now, at present, at this moment in time |
| 100 | ար | 6 | [very short (≤2 chars)] are |

## multi-meaning  (9)

| rank | lemma | count | notes |
|-----:|-------|------:|-------|
| 3 | ինչ | 68 | what? (interrogative pronoun); what (indefinite pronoun) |
| 22 | որ | 19 | [very short (≤2 chars)] who, which, that (relative pronoun); that |
| 39 | համար | 11 | number; size |
| 53 | քիչ | 9 | the little; few |
| 56 | տարեկան | 9 | rye; yearling piglet |
| 73 | նրան | 7 | dagger; dirk |
| 76 | դուր | 7 | chisel; flat, level |
| 77 | մեծ | 7 | leader, chief, elder; big, large |
| 97 | տաք | 6 | heat; warm weather, warm days |

## valid  (72)

| rank | lemma | count | notes |
|-----:|-------|------:|-------|
| 1 | կարդալ | 94 | to read; to recite from memory |
| 2 | գրել | 73 | to write |
| 5 | ունենալ | 63 | to have, to possess, to dispose; to own, to hold |
| 9 | նստել | 32 | to sit, to sit down, to take a seat; to sink, to subside |
| 10 | լինել | 31 | to be, to exist; to happen |
| 11 | իսկ | 30 | while, and, but; even |
| 12 | հոգնել | 30 | to become tired, exhausted |
| 13 | այո | 28 | yes |
| 14 | շատ | 26 | a lot of, many, much; very |
| 16 | բայց | 24 | but, yet; though, however |
| 17 | գալ | 23 | to come; to arrive |
| 19 | ձեր | 23 | դու (gen p) |
| 20 | գիտենալ | 22 | to know |
| 23 | սեր | 18 | love; affection, caring |
| 25 | ասել | 17 | to say; to tell |
| 26 | կարել | 17 | Karelian; to sew |
| 27 | ինձ | 16 | me |
| 28 | հայերեն | 15 | Armenian; Armenian |
| 29 | նոր | 15 | new; fresh; just, just now; not long ago, recently |
| 30 | անել | 15 | to do |
| 33 | ուզել | 14 | to want, wish, desire; to ask, ask for, request |
| 34 | այստեղ | 13 | here |
| 35 | գնալ | 13 | to go; to go away, to leave, to depart |
| 36 | այս | 12 | evil spirit; this |
| 37 | այսօր | 11 | today; today |
| 38 | տանել | 11 | to carry; to carry away or off, to take away; to lead; to tolerate, to endure, to stand, to brook |
| 40 | բարև | 11 | greeting, salute; salutation; hello!, hi! |
| 41 | խնդրեմ | 11 | please; you're welcome, don't mention it, no problem |
| 43 | քան | 10 | than |
| 44 | դառնալ | 10 | to become; to turn into; to return, to come back |
| 47 | բերել | 10 | to bring, to fetch |
| 48 | երբ | 10 | when; while |
| 49 | տեսնել | 10 | to see; to notice; to look at, to examine; to meet, to come across |
| 50 | ձեզ | 10 | you |
| 51 | ժամ | 10 | hour; time |
| 52 | լավ | 9 | good; good, fine, OK |
| 54 | հիանալ | 9 | to admire, to marvel at |
| 55 | ինչու | 9 | why |
| 57 | քեզ | 9 | you (objective form, singular, informal) |
| 60 | ամառ | 8 | summer |
| 61 | գեղեցիկ | 8 | beautiful; handsome; beautifully |
| 62 | տալ | 8 | sister-in-law; to give |
| 63 | դեռ | 8 | still, yet |
| 64 | ուր | 8 | where |
| 65 | առնել | 8 | to take; to buy, to purchase |
| 66 | ընկնել | 8 | to fall; to fall, to, drop, to decrease |
| 67 | դնել | 8 | to put, to lay; to impose, to inflict |
| 68 | շնորհակալ | 8 | grateful, thankful |
| 69 | այնտեղ | 8 | there |
| 70 | բան | 8 | thing; work, business |
| 72 | փոքր | 7 | small, little; younger, junior |
| 74 | հետ | 7 | back; with |
| 75 | մեկ | 7 | someone, somebody; one |
| 78 | բժիշկ | 7 | doctor, physician |
| 79 | ուրիշ | 7 | other, different; another |
| 80 | մեր | 7 | մենք (gen s) |
| 81 | հավանել | 7 | to agree, to accept; to like |
| 83 | ուտել | 7 | to eat; to corrode |
| 84 | բանալ | 7 | to open |
| 85 | ելնել | 7 | to go out (of); to leave; to exit; to mount, ascend, climb |

_… 12 more (see `lemma_validation.tsv` for the full list)_
