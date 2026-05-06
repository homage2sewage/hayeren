# Eastern Armenian — grammar & phonology notes

Living notes on the Armenian linguistic facts I keep encountering as I
work through Sakayan. Not a tutorial — just the points that matter for
deck-building, transcription, and avoiding traps.

## Phonology

### Three-way consonant distinction

Armenian distinguishes voiced / voiceless-unaspirated / voiceless-aspirated
across stops and affricates — six triples. Spelled distinctly:

| voiced | voiceless | aspirated |
|--------|-----------|-----------|
| բ /b/  | պ /p/     | փ /pʰ/    |
| դ /d/  | տ /t/     | թ /tʰ/    |
| գ /g/  | կ /k/     | ք /kʰ/    |
| ձ /dz/ | ծ /ts/    | ց /tsʰ/   |
| ջ /dʒ/ | ճ /tʃ/    | չ /tʃʰ/   |

English speakers default to the *aspirated* category for /p t k tʃ/,
which means the unaspirated letters (պ տ կ ճ) are the ones that need
deliberate practice. The *voiced* row (բ դ գ ձ ջ) is also unstable
in modern speech — see next note.

### Voiced consonants pronounced as aspirated

In *some* words, written voiced stops are pronounced as their aspirated
or voiceless counterparts. Sakayan's transcription is the ground truth.
After extracting all 11 units we have evidence the alternation is:

- broad — affects every voiced stop/affricate (բ/գ/դ/ձ/ջ);
- lexically irregular — different words substitute different counterparts:
  - `դ → թ`: `ընդունել → ընթունել` (to accept), `կարդում → կարթում`
    (reading), `արդեն → արթեն` (already);
  - `դ → տ`: `Այդ → այտ` (that), `դուրդ → դուրտ` (your, post-cl.);
  - `բ → փ`: `շաբաթ → շափաթ` (week);
  - `գ → ք`: `օգնական → օքնական` (assistant), `հագուստ → հաքուստ`
    (clothing), `անգամ → անքամ` (time/instance), `հոգնում →
    հոքնում` (getting tired);
  - `ձ → ց`: `փորձարկում → փորցարկում` (experiment), `բարձր → բարցր`
    (high);
  - `ջ → չ`: `վերջապես → վերչապես` (finally), `առողջություն →
    առողչություն` (health).

Only this voiced↔voiceless/aspirated swap counts as a pronunciation
deviation. Vowel glides (`ի` becoming /j/ before another vowel,
`միլիոն` → /milyon/) and epenthetic schwas (`փոքր` → [pŒokŒ§r] with
inserted ə) are predictable allophonic processes, not deviations from
spelling. See `sakayan/phonetics.py` for the detection logic.

Pedagogical takeaway: there's no shortcut. Every word that has a voiced
stop needs to be checked against its actual pronunciation. The phonetic
hints on the cards make this practical.

### Pro-drop

Armenian routinely omits subject pronouns: the verb ending alone marks
person and number. `Ունեմ։` (one word) is a complete sentence "I have."
Pronouns appear when emphasized or contrasted:
`Ես ունեմ, դու չունես։` "*I* have, *you* don't."

This is why paradigm cards (`ունեմ → I have`) are useful in isolation —
each form really is a complete utterance.

### `ոու` is a digraph

The two characters `ո` (vo) + `ւ` (vyun) together render as the single
sound /u/, written `ու`. **Don't split them in annotations** — it's
analogous to splitting "th" in English. `ընդունել` segments as
`ը-ն-դ-ո+ւ-ն-ե-լ`, not `ը-ն-դ-ո-ւ-ն-ե-լ`.

### Punctuation marks

Armenian punctuation differs from Latin:

| mark | name (Armenian / English) | role | usage |
|------|--------------------------|------|-------|
| `։`  | վերջակետ / verjaket       | full stop | end of sentence (= Latin `.`) |
| `,`  | ստորակետ / storaket       | comma | same as Latin |
| `՝`  | միջակետ / mijaket         | mid-stop | clause separator (≈ semicolon) |
| `՞`  | հարցական / hartsakan      | question mark | placed *above* the stressed syllable, mid-word |
| `՜`  | բացականչական / batsakanchakan | exclamation | placed mid-word, like ՞ |
| `՛`  | շեշտ / shesht             | emphasis mark | mid-word, marks stress |

`՞ ՛ ՜` go *inside* the word at the stressed syllable (so `Քանի՞`
"how many?" not `Քանի?`). When transliterating, they tend to migrate
to word-final position — keep that in mind for alignment work.

## Pronouns

| singular | plural |
|----------|--------|
| ես (1sg, "I") | մենք (1pl, "we") |
| դու (2sg informal, "you") | դուք (2pl OR 2sg formal, "you") |
| նա (3sg, "he/she") | նրանք (3pl, "they") |

There's no grammatical gender — `նա` covers both "he" and "she". The
formal/informal distinction in the second person works like French
*tu*/*vous*: `դու` for friends/family/children, `դուք` for strangers
or anyone you'd treat with deference.

## Verbs

### Two infinitive endings → two regular conjugation classes

- I conjugation: stem + `-ել` (e.g. `գրել` "to write", `խոսել` "to speak")
- II conjugation: stem + `-ալ` (e.g. `կարդալ` "to read", `մնալ` "to stay")

### Present tense of regular verbs

Built from the *present participle* (`stem + -ում`) plus the auxiliary
form of `լինել` "to be":

| pronoun | participle + aux |
|---------|------------------|
| ես      | գր**ում եմ**     |
| դու     | գր**ում ես**     |
| նա      | գր**ում է**      |
| մենք    | գր**ում ենք**    |
| դուք    | գր**ում եք**     |
| նրանք   | գր**ում են**     |

Eastern Armenian has *one* present tense covering both English present
indefinite ("I write") and present continuous ("I am writing").

### Irregular verbs

Five high-frequency verbs deviate. See Sakayan p37, encoded in
`sakayan/paradigms_data.py`.

- `տալ` "to give", `գալ` "to come", `լալ` "to cry" — use `-իս` participle
  instead of `-ում` (`տալիս եմ` "I give", not `*տալում եմ`).
- `լինել` "to be" — has both an irregular *short* present (the
  auxiliary forms `եմ ես է ենք եք են`) and a regular continuative
  (`լինում եմ`...).
- `ունենալ` "to have" — same pattern: short irregular `ունեմ ունես ունի
  ունենք ունեք ունեն` plus regular `ունենում եմ`...

The short forms express *current* state ("I have now"); the regular
forms express *habitual* state ("I usually have"). Don't conflate them.

The full irregular-verb table (Sakayan grammar appendix, p354–355) lists
~19 verbs with all their irregular stems and forms: `անել, առնել, ասել,
բանալ, բերել, գալ, դառնալ, դնել, ելնել, զարկել, ընկնել, թողնել, լալ,
լինել, լվանալ, տալ, տանել, տեսնել, ուտել`. For each, the table gives
the aorist stem (irregular), then the participles and finite tenses
follow predictable patterns from that stem.

### The full tense system

After working through Sakayan, Eastern Armenian's indicative + modal
inventory comes out roughly as:

| Mood | Tense | Construction |
|------|-------|--------------|
| Indicative | Present | imperfective participle (`-ում`) + aux |
|            | Imperfect | imperfective participle (`-ում`) + imperfect aux |
|            | Aorist | bare verb stem + `-եց-/-աց-/-` + personal endings |
|            | Perfect | past participle (`-ել/-ացել`) + aux |
|            | Pluperfect | past participle (`-ել/-ացել`) + imperfect aux |
|            | Future | future participle (`-ելու/-ալու`) + aux |
|            | Future imperfect | future participle (`-ելու/-ալու`) + imperfect aux |
| Subjunctive | Future | bare stem + `-եմ/-ամ` endings |
|             | Past | bare stem + `-եի/-այի` endings |
| Mandative | Future I | `պիտի` / `պետք է` + subjunctive future |
|           | Past I | `պիտի` / `պետք է` + subjunctive past |
|           | Future/Past II | past participle + `պիտի + լինել` |
| Resultative | Present | past participle (`-ած`) + aux |
|             | Past | past participle (`-ած`) + imperfect aux |
| Hypothetical | Future I | `կ-` + subjunctive future |
|              | Past I | `կ-` + subjunctive past |
|              | Future/Past II | past participle + `կ + լինել` |
| Imperative | Singular | `-ի՛ր / -ա՛`, irregular for some verbs |
|            | Plural | `-ե՛ք / -ա՛ք` |
| Prohibitive | sg / pl | `մի՛ + ` imperative form |

Negation in finite tenses works two ways:

- **Most tenses** prefix `չ-` to the auxiliary: `գրում եմ → չեմ գրում`
  (and the auxiliary moves before the participle).
- **Hypothetical** uses `չեմ + negative-participle (-ի/-ա)`:
  `կգրեմ → չեմ գրի`, `կկարդամ → չեմ կարդա`. The negative participle
  is its own form — listed in `sakayan/paradigms_data.PARTICIPLES`.

## Դերբայ — non-finite forms (participles)

Sakayan's grammar appendix (p359, "THE INFINITIVE AND THE PARTICIPLES")
classifies non-finite forms as **free** (independent use as nouns,
adjectives, adverbs) or **bound** (only inside conjugation paradigms).
Each verb has up to eight non-finite forms:

| Form | Suffix | Free/Bound | Use | Example (`գրել`) |
|------|--------|-----------|-----|------------------|
| Infinitive | `-ել / -ալ` | free | citation form, also a noun | `գրել` to write |
| Active participle | `-ող / -ացող` | free | "the one who Vs" — agent noun, also adjective | `գրող` writer |
| Past participle | `-ած / -ացած` | free | "having Ved", "Ved" (passive sense) — adjective, perfect/resultative tenses | `գրած` written |
| Synchronic | `-ելիս / -ալիս` | free + bound | "while Ving" — temporal converb; also irregular present (`գալիս եմ`) | `գրելիս` while writing |
| Imperfective | `-ում` | bound only | the present-tense participle, takes auxiliary | `գրում (եմ)` |
| Perfective | `-ել / -ացել` | bound only | the perfect-tense participle (-ել identical to infinitive for first-conjugation verbs!) | `գրել (եմ)` have written |
| Future | `-ելու / -ալու` | free + bound | "going to V" — future tense + standalone purpose phrases | `գրելու` going to write |
| Negative | `-ի / -ա` | bound only | combines with negated auxiliary in hypothetical: `չեմ V-ի` | `գրի` (in `չեմ գրի`) |

There's also one form Sakayan doesn't list separately but which is
common in real speech:

- **Instrumental converb** `-ելով / -ալով` (the infinitive in instrumental
  case): `գրելով` "by writing", `կարդալով` "by reading". Used for manner
  / means adverbials.

For irregular verbs, the participles are built off the *aorist stem*
rather than the infinitive stem:

- `գալ` (aorist `եկ-`): active `եկող`, past `եկած`, future `գալու`,
  synchronic `գալիս`, instrumental `գալով`, negative `գա`.
- `ուտել` (aorist `կեր-`): past `կերած` (not `*ուտած`!), the rest from
  `ուտ-`.
- `տեսնել` (aorist `տես-`): past `տեսած`, the rest from `տեսն-`.
- `լինել` (aorist `եղ-`): active `եղող`, past `եղած`, future `լինելու`.

These eight verbs' full participle tables are encoded in
`sakayan/paradigms_data.PARTICIPLES`.

## References

- Sakayan, *Eastern Armenian for the English-Speaking World* (2007),
  pp. 35–37 for verbs/conjugation; pp. 26 onwards for the Unit 1
  treatment.
- `sakayan/phonetics.py` for the deviation detector backed by these
  facts.
- `sakayan/paradigms_data.py` for hand-curated conjugation tables.
