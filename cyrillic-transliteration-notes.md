# Russian-Cyrillic transliteration of Armenian — conventions, layers, pitfalls

Top-level reference doc covering the transliteration of Armenian
into Russian Cyrillic script. Sister doc to
`transliteration-notes.md` (which covers Latin / chat-style
romanization). Three distinct registers exist, with different
goals and conventions; this doc maps them and the
reader-strategies they imply.

> **Seed observation.** When Armenian is rendered in Cyrillic
> for a Russian-script audience, the *popular* convention is
> **glyph-by-glyph orthographic mapping** without sound
> substitutions or schwa insertion. *Вардавар* (Armenian
> `Վարդավառ`), *Фрунзик Мкртчян* (`Ֆրունզիկ Մկրտչյան`) — the
> Cyrillic preserves the consonant clusters and the
> orthographic letters even where the pronunciation differs
> sharply. Cafes, signs, news, Wikipedia titles, official
> documents all do this. Tourists and L2 learners are usually
> stuck applying the schwa rule and the consonant-row
> alternation themselves.
>
> Parnasyan and Tioyan break this convention: they're
> textbooks *for L1=Russian learners*, and their bracketed
> Cyrillic forms (`թշվառ [т‘эшвар]`, `Նա սովորում է [на
> соворум э]`) are **pronunciation-faithful** — schwas are
> filled in, aspirated stops marked, initial-glide forms
> made explicit. Different convention, different goal.

## Three registers

| register | goal | example |
|---|---|---|
| **Popular orthographic** | Reversibility, identity preservation. Maps each Armenian grapheme to a Cyrillic equivalent. | Wikipedia title, cafe menu, news byline, sign |
| **Textbook phonetic** | Pronunciation aid for an L1=Russian learner. Inserts schwas, marks aspiration. | parnasyan, tioyan |
| **Scholarly / linguistic** | Bibliographic precision, IPA-adjacent. ISO 9985, Hübschmann, library transliteration. | Academic linguistics; rarely seen outside |

The popular and textbook registers are the two you'll
encounter in real life. Scholarly is real but specialised; we
won't focus on it.

## Popular orthographic convention

### The rule

For each Armenian grapheme, emit the canonical Cyrillic
equivalent. Preserve the orthography, not the pronunciation.
Cluster-internal schwas, voiced→aspirated alternations, the
trilled-vs-flapped `ռ/ր` distinction, and initial-glide
realizations of `ե/ո` are **all dropped** because Cyrillic
doesn't distinguish them.

### Mapping table

| Armenian | popular Cyrillic | notes |
|---|---|---|
| ա | а | |
| բ | б | (literary [b]; sometimes [pʰ] in alternation — not reflected) |
| գ | г | (literary [g]; sometimes [kʰ] — not reflected) |
| դ | д | (literary [d]; sometimes [tʰ] — not reflected) |
| ե | е | initial `ե-` is `[ye-]` in pronunciation but Cyrillic uses bare `е` (Ереван not Йереван) |
| զ | з | |
| է | э | |
| ը | ы / ъ / often dropped | rarely written; sometimes elided in transliteration when initial |
| թ | т | aspirated; **collapses with `տ`** (both → т) |
| ժ | ж | |
| ի | и | |
| լ | л | |
| խ | х | |
| ծ | ц | unaspirated; collapses with `ց` |
| կ | к | unaspirated; collapses with `ք` |
| հ | х / silent / dropped | popular usage varies; `Հայաստան` → `Айастан` (silent) or `Хайастан` (rendered) |
| ձ | дз | |
| ղ | г / гх | usually `г`; sometimes `гх` for clarity |
| ճ | ч | unaspirated; collapses with `չ` |
| մ | м | |
| յ | й | |
| ն | н | |
| շ | ш | |
| ո | о | initial `ո-` is `[vo-]` in pronunciation but Cyrillic uses bare `о` |
| չ | ч | aspirated; collapses with `ճ` (both → ч) |
| պ | п | unaspirated; collapses with `փ` |
| ջ | дж | |
| ռ | р | trilled; **collapses with `ր`** (both → р) |
| ս | с | |
| վ | в | |
| տ | т | unaspirated; collapses with `թ` |
| ր | р | flap; collapses with `ռ` |
| ց | ц | aspirated; collapses with `ծ` |
| ու | у | digraph |
| փ | п | aspirated; collapses with `պ` (both → п) |
| ք | к | aspirated; collapses with `կ` (both → к) |
| օ | о | |
| ֆ | ф | |
| և | ев / эв | depends on writer |

### Worked examples

| Armenian | Cyrillic | losses |
|---|---|---|
| Վարդավառ | Вардавар | `ռ` (trilled) → `р` (collapses); `դ` could be [t] in pronunciation → `д` (orthographic) |
| Մկրտչյան | Мкртчян | hidden schwas in `Մ-կ-ր-տ-չ-յ-ա-ն`: pronounced [mə-kərt-čʰyan]; Cyrillic gives no schwa hint |
| Ֆրունզիկ | Фрунзик | clean (no clusters, no alternations) |
| Հայաստան | Айастан / Хайастан | `հ` ambiguous; both spellings exist; usually depends on whether the writer learned the convention from old-Soviet sources (Хайастан) or post-Soviet (Айастан) |
| Երևան | Ереван | initial `Ե-` → `Е-`, dropping the `[ye-]` glide; `և` → `ев` digraph |
| Շուշի | Шуши | clean |
| Մոսկվա | Москва | borrowed Russian word in Armenian; the Cyrillic restoration is trivial |
| Թումանյան | Туманян | aspirated `թ` → `т`, indistinguishable from `Տուման-` (with unaspirated) if such a name existed |
| Քրիստոս | Кристос / Христос | aspirated `ք` → `к`; some religious-context conventions use `Х-` (Христос) — hybrid spelling |
| Ղազարոս | Газарос / Гхазарос | `ղ` → `г` (popular) or `гх` (more careful) |

### Information losses (systematic)

- **Three-way laryngeal contrast collapses to two-way.** Aspirated /
  unaspirated / voiced (Armenian's three rows) → voiced / voiceless
  (Russian's two). So `Թումանյան` (aspirated `թ`), `Տիգրան`
  (unaspirated `տ`), and a hypothetical `*Դիգրան` (voiced `դ`)
  would be `Туманян`, `Тигран`, `Дигран` — but the first two share
  `т` and the contrast between them vanishes.
- **Hidden schwas vanish.** `Մկրտչյան`, `փոքր`, `տժվժիկ`,
  `սպասել`, `մկրատ` all give Cyrillic readers bare consonant
  clusters with no insertion hint. See
  `topics/phonology/epenthetic_schwa.md` for the rule the
  reader has to apply.
- **Trilled/flap `ռ/ր` collapse** to single `р`. `Վարդավառ`
  vs. a hypothetical `*Վարդավար` would both be `Вардавар`.
- **Initial glides drop.** `Երևան` → `Ереван` (no `Йэ-`);
  `Որոտ` → `Орот` or `Ворот` depending on writer. The
  pronunciation-faithful Latin form `Yerevan` preserves what
  the Cyrillic form drops.
- **Voiced→aspirated alternation isn't reflected.** `Վարդան`
  is `Вардан` even though the literary pronunciation is
  closer to [vartan] (with voiceless / aspirated [t] for `դ`
  in this position).

### Why the convention is this way

Reversibility. Glyph-mapping is invertible: `Вардан` always
maps back to `Վարդան`, never `Վարտան` or `Վարթան`. A
pronunciation-faithful version would lose orthographic
information (you couldn't tell whether the Russian `т` came
from `տ` or `թ` or `դ`). For identification — which is what
names, place names, and signs need — reversibility wins.

The information losses don't matter to the assumed reader:
either someone who already knows Armenian (and reads the
Cyrillic as a script aid), or someone who doesn't and just
needs to identify a name. Tourists / L2 learners trying to
*pronounce* the Cyrillic form are a tertiary audience.

## Textbook phonetic convention (parnasyan, tioyan)

Different audience, different goal. Parnasyan and tioyan are
Armenian textbooks **for Russian L1 learners**. Their
bracketed transliterations are pronunciation aids, not
identity preservation.

### What changes

- **Schwas are inserted.** `թշվառ` "miserable" becomes
  `[т‘эшвар]` — the `э` between `т‘` and `ш` is the
  epenthetic schwa, filled in so a Russian reader can
  pronounce it.
- **Aspiration is marked.** Aspirated stops carry a `‘`
  (sometimes typeset as `'` or `’`): `թ` → `т‘`, `ք` → `к‘`,
  `փ` → `п‘`, `չ` → `ч‘`, `ց` → `ц‘`. The collapse with
  unaspirated is *avoided* by the diacritic.
- **Initial glides are sometimes preserved.** `որոշված`
  "decided" becomes `[ворошвац‘]` — `во-` for initial `ո`,
  not bare `о`. (Pattern is inconsistent; varies by book and
  even within a book.)
- **`ռ/ր` distinction.** Some textbooks mark the trill
  (`р’`) vs. flap (`р`); usage varies.

### Examples from parnasyan / tioyan

> **Parnasyan p29**: `նա [на] он, она, оно. մեկ [мэк] ОДИН.`

> **Parnasyan p33**: `[на соворум э дэпроцум]` for `Նա
> սովորում է դպրոցում` "He studies at school." Note `դ` →
> `д`, `ց` → `ц`, schwas not added in this case (no clusters
> needing one).

> **Parnasyan p370**: `թշվառ [т‘эшвар] прил. несчастный,
> отверженный` — schwa inserted (`т‘ə-ш-в-а-р`) plus
> aspiration mark.

> **Parnasyan p405**: `որոշված [ворошвац‘] прич. решенный` —
> initial `ո-` rendered as `во-`; aspirated `ց` rendered as
> `ц‘`.

### Reader convention from tioyan

> **Tioyan p10**: "В армянском языке написание и
> произношение..." — opens the orthography-pronunciation
> mapping section.

> **Tioyan p11**: "Усвоить возможные отклонения нетрудно. р
> может произноситься..." — frames the deviations as a small
> learnable rule-set. Includes treatment of `դ → [տ]` in
> demonstratives (`այդ → [այտ]`), `հ` silencing in some
> words, and schwa insertion.

> **Tioyan p19**: `Местоимение այդ произносится |այտ|.` —
> explicit orthographic-vs-phonetic divergence example for
> the demonstrative.

So tioyan and parnasyan both teach the *rule-set* that lets
a Russian L1 learner read Armenian script aloud, and use
their bracketed Cyrillic as the pronunciation reference for
each entry. They don't use the popular orthographic
convention.

## Reader-side strategy

If you encounter Armenian-in-Cyrillic, the first move is
**identify the register**:

1. **Source-context check.** Is this a Wikipedia title,
   a sign, a cafe menu, a news byline, an official document?
   → popular orthographic. Apply schwa rule + aspirated/
   unaspirated knowledge to get pronunciation.
2. **Is it a textbook entry, a learner-facing dictionary, a
   pronunciation guide?** → textbook phonetic. The
   transliteration is already pronunciation-faithful;
   trust it.

### Strategy for popular orthographic input

Three steps:

- **Back-transliterate via the table above.** `Вардан` →
  `Վարդան`. Use orthographic mapping; don't second-guess.
- **Apply the schwa rule** (`topics/phonology/epenthetic_
  schwa.md`) to fill in cluster-internal vowels. `Мкртчян`
  → consonant cluster `М-к-р-т-ч-я-н` → pronounced
  [mə-kərt-čʰyan].
- **Apply the consonant-row knowledge** (`topics/phonology/
  three_way_laryngeal_contrast.md` and `voiced_aspirated_
  alternation.md`) to refine pronunciation. `Вардан` written
  with `д` is in literary practice often pronounced [vartan]
  with [t]; whether to apply this is a judgment based on
  word and register.

### Strategy for textbook phonetic input

The bracketed Cyrillic in parnasyan / tioyan is intended to
be readable as Russian. Just read it aloud. Trust the schwa
insertions and aspiration marks. Don't try to back-derive
Armenian orthography from the bracketed form — use the
unbracketed Armenian-script form for that.

## Common pitfalls

### Pitfall 1: assuming popular = textbook convention

Reading `Вардан` and trying to pronounce it letter-for-letter
in Russian. The Russian `д` is voiced [d]; the Armenian word
in literary register has voiceless [t]. Without knowing the
voiced-aspirated alternation, you'll produce a non-native
[vardan] instead of [vartan].

### Pitfall 2: the cafe-menu trap

Encountering `тжвжик` on a menu. Russian phonotactics doesn't
allow `тж-` initial cluster either — but the convention
expects you to know the schwa rule and read it as
[təʒvəʒik]. Most foreign tourists pronounce it haltingly or
ask the waiter.

### Pitfall 3: hybrid forms in informal writing

People mix conventions. You'll see `Хайастан` (Soviet-era
convention with `Х`) next to `Айастан` (modern, `հ` silent)
in the same paragraph. Don't try to be consistent for them;
just back-transliterate each token.

### Pitfall 4: name-borrowing into Russian

Some Armenian proper nouns have *separately-conventionalised*
Russian forms that aren't transliterations at all. The country
itself — `Հայաստան` — is `Армения` in Russian (a Russian
exonym, not a transliteration of Hayastan). Similarly,
`Արարատ` is `Арарат` (just transliteration), but
`Կարմիր Բերդ` (a place) might be either transliterated or
calque-translated to `Красная Крепость` "Red Fortress."
Context tells you which.

### Pitfall 5: `հ` ambiguity in the popular convention

`հ` has three popular Cyrillic outcomes:

- `х` (most common: `Հայ` → `Хай`, `Հովհաննես` → `Хованнес`).
- silent: `Հայաստան` → `Айастан`.
- omitted entirely (`Հովհաննես` → `Ованнес` — Soviet-era
  Russian-Armenian convention).

You'll see all three. The post-Soviet trend favours `х`.

## Cross-references

- `transliteration-notes.md` — Latin / chat-style
  transliteration. Sister doc; same problems, different script.
- `topics/phonology/epenthetic_schwa.md` — the rule that
  Russian Cyrillic readers have to apply themselves.
- `topics/phonology/three_way_laryngeal_contrast.md` — the
  three-way distinction that collapses to Russian's two-way.
- `topics/phonology/voiced_aspirated_alternation.md` — the
  literary-pronunciation deviations not reflected in popular
  Cyrillic.
- `parnasyan/manifest.yaml` and `tioyan/manifest.yaml` —
  the two L1=Russian textbooks whose internal convention is
  the **textbook-phonetic** register documented above.
- `errors/2026-05-09-002-khot-slang-divergence.md` and
  `research/2026-05-09-tweet-llm-comparison.md` — adjacent
  scenarios where transliteration ambiguity bit hard.

## Open questions / gaps

- **No corpus of popular Cyrillic transliterations** of Armenian
  proper nouns to validate the convention table empirically.
  Real-world frequencies (when does `հ` get `х` vs. dropped?)
  would need a chat / news / Wikipedia-titles dataset.
- **No automated transliterator.** The popular convention is
  mechanical enough to script; the textbook one needs phonetic
  rules. Worth building when there's a reason.
- **Hybrid Armenian-Russian text detection.** When a paragraph
  mixes Armenian script and Cyrillic-Armenian transliterations,
  identifying which is which programmatically is non-trivial.
  Not a current need but worth noting.
- **Stress placement in Cyrillic transliteration.** Russian
  often marks stress with diacritics in pedagogical contexts;
  Armenian stress is lexically contrastive; whether the textbook
  convention preserves stress is undocumented in our corpus.
