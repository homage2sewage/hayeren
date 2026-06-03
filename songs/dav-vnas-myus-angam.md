---
title: Մյուս անգամ / Myus Angam ("Next Time")
artists: [Dav, Vnas]
genre: hip-hop / rap (Armenian)
lyrics_source:
  - "Musixmatch (crowd-sourced transcription) — primary text"
  - "https://www.youtube.com/watch?v=NV2t6JHqx_8 (official lyric video — meaning cross-check)"
date_processed: 2026-06-01
status: reviewed  # all sections translated + adversarially verified; residual low-confidence lines flagged in Open questions
---

# Dav feat. Vnas — Մյուս անգամ (Myus Angam)

## What the song is about

The title `Մյուս անգամ` "next time / another time" **is** the hook,
and the whole track is built on recontextualizing it. The refrain
`Թող մնա մյուս անգամ` "let it wait for next time" is the spine — a
gesture of deferral that the verses keep reframing.

- **Dav raps V1 and V3; Vnas raps V2.**
- **V1 (Dav)** — legacy and maturity: leaving bars behind, having
  outgrown the old roads, a manifesto thread (don't get
  complacent, build your home, live for your name, bleed for
  family).
- **V2 (Vnas)** — art vs. fakeness: wait for the *muse* or defer;
  hollow "deep" lyrics, the streets, and *genuine* brotherhood as
  "supernatural" strength.
- **V3 (Dav)** — fake-flash vanity: a pun-chain mocking gaudy
  Coco-Chanel "cuckoos," ending on a turn toward silence ("better
  they stay quiet").
- The refrain shifts meaning across the song: **resigned
  deferral** in the hook → **deferred *hope*** in V3 (`հույս
  կճարենք մյուս անգամ` "we'll find hope next time") and even `մյուս
  կյանքում` "in the next life" (V2).

*This is a learner's analysis, not an authoritative reading — see
Methodology for how meanings were obtained and where they're
uncertain.*

## Methodology & provenance

How the text and the meanings in this file were obtained — read
this before trusting any single gloss.

**Text.** The Armenian text is a **crowd-sourced transcription**
from Musixmatch, spot-cross-checked against the official lyric
video. It is *not* an authoritative print source. Several lines
carry colloquial phonetic spellings that the transcriber rendered
ad hoc (`թո` = `թող`, `շատէ` = `շատ ենք`, `գիդեն` = `գիտեն`). One
line uses a **marked plural**: `ճամփեքը` "the roads" appears to
carry the archaic `-ք` plural (the operator hears `ք`, not `ր`, in
the audio) — non-standard and stylized; standard is `ճամփաները`
(see Chorus L4). Where transcription itself is in doubt, the
line is flagged **low** confidence.

**Meaning.** Each section was processed by the routine in
`songs/README.md`:
1. colloquial spelling normalized to standard Armenian (grammar
   made visible);
2. lexicon KB-grounded via `frequency/query_kb.py` + targeted
   `grep` of `ghamoyan/out/full.jsonl` and `topics/lexicon/*`;
3. translated line-by-line with a **confidence grade**, plus a
   register-aware rendering;
4. slang glosses carry a **citation** (book + page) where the
   corpus attests them, and are marked **prior** (pre-training
   guess) where it doesn't;
5. low-confidence lines verified by separate critic agents (see
   Verification log).

**What is cited vs. prior.** Grammar (the `թող`+subjunctive
jussive, `անցնել` argument frame, adverbial `անգամ`) and several
slang items (`ջոգել`, `հավայի`, `սաղ`, `նենց`, `գիդ-`, `քցել`,
`ախպեր`, `շուբ`, `ընգ`=`ընկ`) are corpus-grounded. Russian-origin
slang (`սումմա`, `գոնկ`, `բես`, `քեշ`), the idiom `վիզ դնել`, and
words that are standard but absent from our four-book corpus
(`զսպել`, the lyric idiom `աչք ծակել`) are **prior /
transparent-standard** — flagged inline. Confidence is graded per
line, never uniform-high. **Note:** a whole-song citation audit
(pass 2) corrected six citation errors made during drafting — see
the Verification log.

**Related KB.** `topics/morphology/jussive_thogh_subjunctive.md`
(the chorus hook), `topics/lexicon/yerevan_slang.md` (slang
glosses).

---

## Chorus (hook)

**As sung:**
```
Թո մնա մյուս անգամ
Շանսերը շատ, բայց շատէ մեծցել ենք
Թո մնա մյուս անգամ
Ճամփեքը նույն անցե ու գնացել ենք
```

**Normalized:**
```
Թող մնա մյուս անգամ
Շանսերը շատ [են], բայց շատ ենք մեծացել
Թող մնա մյուս անգամ
Ճամփեքը նույն [են], անցել ու գնացել ենք
```

| # | line | translation | conf. |
|---|---|---|---|
| 1 | `Թող մնա մյուս անգամ` | "Let it wait for next time" (3sg jussive, subj = unstated *it*) | high |
| 2 | `Շանսերը շատ [են], բայց շատ ենք մեծացել` | "Plenty of chances — but we've grown up a lot" | med |
| 3 | (repeat of 1) | "Let it wait for next time" | high |
| 4 | `Ճամփեքը նույն [են], անցել ու գնացել ենք` | "Same roads — we've been through it and moved on" | high |

**Grammar grounded:**
- L1/L3 `Թող մնա` — `թող` + 3sg subjunctive jussive ("let X …");
  `մնա` is the 3sg subjunctive of `մնալ`, **not** the 2sg
  imperative "stay!". See `topics/morphology/jussive_thogh_subjunctive.md`
  (parnasyan p260–263 `пусть` paradigm; tioyan p217 `Թող գա`;
  ghamoyan p67 colloquial `թող անի`/`թող գնա`).
- `մյուս անգամ` "next time" = bare adverbial NP, no adposition
  (cf. `այս անգամ` sakayan p398, `մի անգամ`↔`один раз` tioyan
  p160). English "next time" matches; Russian needs `в … раз`.
- L4 `անցել` is **intransitive** ("passed through / moved on").
  `ճամփեքը նույն [են]` is a copular clause parallel to
  `Շանսերը շատ [են]`, not the object of `անցել`. Corpus: `անցնել`
  takes instrumental paths (`անցնել փողոցով`↔`по улице`,
  parnasyan p179), not accusative.
- **`ճամփեքը` — a marked `-ք` plural (`ք`, not `ր`).** Standard
  modern plural of `ճամփա` is `ճամփաներ` (corpus 8×); the
  productive colloquial would be `ճամփերը` (`-եր`). But the
  operator hears `ք` in the audio, and `-ք` **is** a real Armenian
  plural — the archaic/Classical nominative plural, surviving in
  frozen modern forms: `կանայք` "women" (corpus 29×), `տիկնայք`
  "ladies" (7×), `պարոնայք` (4×), `որդիք` "sons," `ծնողք`
  "parents." It is **not productive** in standard speech, so
  `ճամփեք` (= colloquial plural stem `ճամփե-` + archaic `-ք`) is a
  **stylized / archaic-flavored** plural, not a standard one — the
  kind of marked form rap deploys. Meaning ("the roads") is
  unchanged; standard equivalent `ճամփաները`. (`ճամփեք` itself is
  a nonce form, not corpus-attested.) Flagged by the operator,
  2026-06-01.

**Open:** L2 `շատէ` segmentation — (A) `շատ ենք մեծացել` "grown up
*a lot*" or (B) `շատ ա, մեծացել ենք` "it's a lot — we've grown
up." Both converge on *much opportunity, but we've matured*;
audio would disambiguate.

**Register-aware rendering:**
> Leave it for next time —
> plenty of shots, but we done grown up
> Leave it for next time —
> same roads, we walked 'em and moved on

*(Renderings are styled for flow and smooth over the low-confidence
lines — trust the table's confidence column, not the blockquote.)*

---

## Verse 1 (Dav)

**As sung:**
```
Գնացել եմ առաջ ու դժվար էլ հետ գամ
Թողում տողեր հետևիցս կարան պետք գան
Ես ունեմ թեմա խոսալու, քանի դեռ կամ
Ապագան, որը գծում էս պահին ներկան (Յե)
Մյուս անգամ չքցես հանկարծ
Լավ արածդ մեկին չի ըլնի անվերադարձ
Չծախսենք ժամանակ հավայի, ի՞նչ աշխատավարձ
Նենց ստացվե օրվա մեջ լուծում հազար հատ հարց
Բարդ արարած սաղս սաղս ջոգում էդ
Հայտարարած սաղս կապված ենք ու՞մ հետ
Մի տէ պարզ, մի տէ պարզ էր թվում էդ
Մի տէ քէշ ծախում քեզ գիդեն սումմեդ
Ուշ զարթնի, թե քաղցրա քունդ
Հասցրա, բայց դու շենացրա տունդ
Ապրի նենց, որ բարձր անունդ
Ու տանդ համար միշտ եռա արունդ
Ով վիզա դնում իմ հարգանքը քեզ
Գոնկեքի մեջ քեզ չկորցնես
Հոգեպես պատրաստ առյուծի պես
Ժամանակները բարդ, մեջս չունեմ բես բայց
```

| # | line | translation | conf. |
|---|---|---|---|
| 1 | `Գնացել եմ առաջ ու դժվար էլ հետ գամ` | "I've gone on ahead — and I'll hardly come back" | high |
| 2 | `Թողում [եմ] տողեր հետևիցս, կարան պետք գան` | "I leave lines behind me — they might be needed" | high |
| 3 | `Ես ունեմ թեմա խոսալու, քանի դեռ կամ` | "I've got something to say, long as I'm still here" | high |
| 4 | `Ապագան, որը գծում [է] էս պահին ներկան` | "The future — which the present is sketching right now" | high |
| 5 | `Մյուս անգամ չքցես հանկարծ` | "(careful) you don't go losing it next time" | med-high |
| 6 | `Լավ արածդ մեկին չի ըլնի անվերադարձ` | "The good you do for someone won't go unreturned" | high |
| 7 | `Չծախսենք ժամանակ հավայի, ի՞նչ աշխատավարձ` | "Let's not waste time for nothing — what's the pay?" | high |
| 8 | `Նենց ստացվե[ց] օրվա մեջ լուծում հազար հատ հարց` | "It just works out — I solve a thousand problems a day" | med-high |
| 9 | `Բարդ արարած, սաղս սաղս ջոգում [ենք] էդ` | "Complex creatures — all of us, all of us get that" | med-high |
| 10 | `Հայտարարած, սաղս կապված ենք ու՞մ հետ` | "Declared: we're all tied — to whom?" | med |
| 11 | `Մի տէ պարզ, մի տէ պարզ էր թվում էդ` | "One second it's clear, next it just *seemed* clear" | low |
| 12 | `Մի տէ քէշ ծախում, քեզ գիդեն սումմեդ` | "One second flashing cash — they know your worth (your money)" | low |
| 13 | `Ուշ զարթնի, թե քաղցրա քունդ` | "You'll wake up late if your sleep's too sweet" | high |
| 14 | `Հասցրա, բայց դու շենացրա տունդ` | "I made it in time — but you, build up your home" | med-high |
| 15 | `Ապրի նենց, որ բարձր [լինի] անունդ` | "Live so your name stands high" | high |
| 16 | `Ու տանդ համար միշտ եռա արունդ` | "And let your blood always boil for your home" | high |
| 17 | `Ով վիզ[ա] դնում — իմ հարգանքը քեզ` | "Whoever puts their neck out (grinds) — my respect to you" | med |
| 18 | `Գոնկեքի մեջ քեզ չկորցնես` | "Don't lose yourself in the race/rush" | med-low |
| 19 | `Հոգեպես պատրաստ, առյուծի պես` | "Spiritually ready, like a lion" | high |
| 20 | `Ժամանակները բարդ, մեջս չունեմ բես, բայց` | "Times are hard — but I've got no devil in me" | low |

**Slang & lexicon grounded:**
- `ջոգել` "to get / understand" — ghamoyan jargon list p48; in
  use `ջոգած ա` p50. **Cited.**
- `հավայի` "pointless / for nothing" — ghamoyan p49 (`հավայի
  բազար`). **Cited.**
- `սաղ(ս)` "all / all of us" — ghamoyan slang lists p45, p46.
  **Cited.**
- `նենց` = `այնպես` "so / like that" — colloquial, frequent in
  ghamoyan. **Cited.**
- `գիդեն` = `գիտեն` "they know" — ghamoyan p112. **Cited.** (The
  spelling `գիդեն` is the transcriber's ad-hoc colloquial form; the
  *lexeme* `գիտ-`/`գիդ-` is the cited one.)
- `քցել` (in `չքցես` = `չ`+`քցես`) = colloquial variant of `գցել`
  "throw / drop / let slip / lose" — ghamoyan p39 (`գցել-քցել`
  dialectal-variants list). Lemma is `քցել`; the `չ` is negation.
  **Cited** (was prior — now grounded).

**Wordplay:**
- L2 `տող` = a *line of verse* → "leaving lines behind me" is a
  legacy boast (his bars outlive him).
- L4 `ներկա` "the present (time)" ↔ `ներկ` "paint" + `գծել`
  "draw": the present *sketches* the future.
- L13–16 — manifesto mode (don't get complacent; build your home;
  live for your name; bleed for family). **Correction (critic):**
  `հասցրա` (L14) is colloquial **1sg aorist** ("I made it"), not
  an imperative — the imperative of `հասցնել` is `հասցրու`/
  `հասցրեք`, never `հասցրա`. So L14 = "I made it in time, but
  *you*, build up your home" (`շենացրա` imperative-to-addressee
  after explicit `դու`). `զարթնի / ապրի / եռա` remain the
  jussive/imperative thread.

**Prior (not cited) — flagged:**
- L11–12 `մի տէ` — read as "one moment … one moment"; not pinnable
  to corpus (could be `մի տես`). Gist stable, framing uncertain.
- L12 `սումմեդ` = Russ. `сумма` + 2sg poss "your total (worth)."
- L17 `վիզ դնել` "put one's neck out / grind" — corpus has the
  *opposite* idiom `վիզ(ը) ծռել` "submit/beg," not `վիզ դնել`.
- L18 `գոնկ` = Russ. `гонка` "race / rush."
- L20 `բես` = Russ. `бес` "demon" → "no devil in me." Genuinely
  unsure.

**Register-aware rendering:**
> I'm out ahead — ain't coming back, that's hard /
> leaving these bars behind me, you might need 'em /
> got something to say long as I'm still breathing /
> the future? the present's sketching it right now /
> don't go slipping up next time /
> the good you do for somebody comes back around /
> let's not waste time for free — where's the pay? /
> it just works out — I crack a thousand problems a day /
> complex creatures, every one of us knows it /
> it's stated: we're all tied — but tied to who? /
> one second it's clear, next it only looked clear /
> one second flashing cash — they clock your number /
> you'll sleep right through it if the sleep's too sweet /
> I made it in time — but you, build your house up /
> live so your name rides high /
> and for your home, let your blood stay boiling /
> whoever puts their neck out — respect to you /
> don't lose yourself inside the race /
> ready in spirit, like a lion /
> times are hard — but there's no devil in me.

*(Low-confidence lines — L11–12 `մի տէ`, L20 `բես` — read as
confident punchlines here but are guesses; see the table.)*

---

## Verse 2 (Vnas)

**As sung:**
```
Սպասենք, որ մուսան գա, թե՞ թողենք մյուս անգամ
Ութ անգամ շատացելա մուտքը ռուսական
Էլ չկա կրոնը կուսական
Դուսն էլ գիշերը լուսավորում ա լուսնկան
Թղթի մեջէ բուսական
Տեքստերը ձեր դատարկ մթոմ հուզական
Կլսենք մյուս անգամ կամ մյուս կյանքում
Շատ զսպեցին ու տրաքան
Եթե փողոցում ես մութ կրակ հան
Էս գրվածք չի զուտ գրական
Բայց ստե էդ սաղ դրանք կան ու սաղ դրական
Դիմավորենք թո սաղ վրա գան
Գիտենք ուժը մեր ախպերական, գերբնական
Հետ գնա գամ
Մի ասա ինձ ախպեր ախպերական (Դու)
```

| # | line (normalized, copulas restored) | translation | conf. |
|---|---|---|---|
| 1 | `Սպասենք, որ մուսան գա, թե՞ թողենք մյուս անգամ` | "Should we wait for the muse to come — or leave it for next time?" | med |
| 2 | `Ութ անգամ շատացել [է] մուտքը ռուսական` | "The Russian inflow/entry has gone up eightfold" | med |
| 3 | `Էլ չկա կրոնը կուսական` | "The virgin/pure faith is gone" | med |
| 4 | `Դուսն էլ գիշերը լուսավորում ա լուսնկան` | "And outside, the moon lights up the night" | high |
| 5 | `Թղթի մեջ է բուսական` | "There's herb [rolled] in the paper" | med |
| 6 | `Տեքստերը ձեր դատարկ [են], մթոմ հուզական` | "Your lyrics are empty — supposedly emotional" | med-high |
| 7 | `Կլսենք մյուս անգամ կամ մյուս կյանքում` | "We'll listen next time — or in the next life" | high |
| 8 | `Շատ զսպեցին, ու տրաքան` | "They held it in too long — and went off" | low |
| 9 | `Եթե փողոցում ես, մութ կրակ հան` | "If you're in the streets, bring out [your] dark fire" | med |
| 10 | `Էս գրվածք չի զուտ գրական` | "This writing isn't purely literary" | high |
| 11 | `Բայց ստե էդ սաղ դրանք կան, ու սաղ դրական` | "But here all of that exists — and all of it positive" | med |
| 12 | `Դիմավորենք, թող սաղ վրա գան` | "Let's face it — let them all come at [us]" | med |
| 13 | `Գիտենք ուժը մեր ախպերական, գերբնական` | "We know our brotherly strength — supernatural" | high |
| 14 | `Հետ գնա, գամ` | "Step back, [so] I can come [through]" | low |
| 15 | `Մի ասա ինձ ախպեր ախպերական (Դու)` | "Don't call me 'bro' just for show (You)" | med |

**Slang & lexicon grounded:**
- `սաղ` "all / everyone" — ghamoyan slang lists p45, p46 (also
  p83). **Cited.**
- `ախպեր` "brother / bro" (vocative address) — ghamoyan core
  Yerevan-slang vocab list p44 (`ախպեր, ախչի, արա`); derivational
  `ախպերնյակ` p49; in-use p83 (`ախպերս, ես դրա ջանին մեռնեմ…`).
  `ախպերական` "brotherly / of brotherhood" is the transparent
  `-ական` adjective off it. **Cited.**
- `տրաքած` glossed `հարբած` "drunk / wasted" — ghamoyan jargon
  list p50 (alongside `եզոտ`, `ղժժալ`, `խզարել`). The verb here
  is `տրաքել` "to burst / blow up / go off"; the *adjective*
  sense in the corpus is specifically "drunk." **Cited (related
  form);** the "blow up / lash out" verb reading is **prior**.
- `մթոմ` / `մթամ` "supposedly / as if" (= `իբր`, Russ. `якобы`)
  — ghamoyan p60 `յանի-մթամ թե` (paired with `յանի` "i.e."),
  in the colloquial-discourse section. **Cited.**
- `էդ` = `այդ`, `ստե` = `այստեղ`, `դուս(ն)` = `դուրս(ը)` "outside,"
  `թո` = `թող`, `-ա` 3sg copula `է` — the standing colloquial
  reductions from the chorus + verse 1. **Cited (convention).**
- `բուսական` "vegetal / herbal" — sakayan p486. Here a cannabis
  euphemism. **Cited (literal sense);** drug reading is **prior**
  (see Wordplay).
- `կրակ` "fire" — attested as a person-intensity epithet
  (`կրակ երեխա` "a fiery/spirited kid," ghamoyan p94; also idiom
  section p64–68: `Աստծու կրակ`, `կրակի կտոր`, `Թանկ ու կրակ`).
  `մութ կրակ հան` = "bring out [your] dark/raw fire"
  (intensity/aggression), **not** the English-rap "spit fire."
  **Cited (lexeme + epithet sense).**
- `կուսական` "virgin / virginal" — parnasyan dict p383
  (`կուսական [кусакан] прил. девственный`); in use p215. **Cited**
  (was mislabeled "sakayan" — corrected to parnasyan).
- `զսպել` "restrain / hold back" — standard Armenian but **not in
  our four-book corpus**; the earlier "parnasyan p354" cite was
  fabricated (no such entry). Treat as transparent-standard, not
  corpus-cited.
- `դատարկ` "empty" — standard; ghamoyan figurative `դատարկ գլուխ`
  "empty head" p94. **Cited.**
- `դրական` "positive," `գրական` "literary," `գերբնական`
  "supernatural," `լուսնկա` "moon / moonlit" (`Օգոստոսյան լուսնկա
  գիշեր` sakayan p438–439 — was mislabeled "parnasyan") —
  transparent standard Armenian. **Cited / transparent.**

**Wordplay:**
- **The `մուսա` / `մյուս` pun (L1).** `Սպասենք որ **մուսան** գա`
  "wait for the **muse**" vs. the chorus hook `**մյուս** անգամ`
  "**next** time" — `մուսան գա` and `մյուս անգամ` are near-
  homophones, so the line literally asks "wait for the *muse*" while
  echoing "wait for *next time*." Sets up the verse against the hook.
  **Caveat:** the pun rests on the transcription `մուսան` being
  right — it could be `մյուսը գա` "the next one comes," in which
  case there's no muse at all. Hence the line is `med`, not `high`.
- **Relentless `-ական` / `-ան` end-rhyme.** Almost every line
  closes on it: `ռուսական, կուսական, լուսնկան, բուսական, հուզական,
  տրաքան, հան, գրական, դրական, գան, ախպերական, գերբնական, գամ,
  ախպերական`. The rhyme is the verse's organizing constraint;
  several word choices (`բուսական`, `կուսական`) are partly rhyme-
  driven.
- **Drug references.** L5 `Թղթի մեջ է բուսական` — `թուղթ` "paper"
  = rolling paper, `բուսական` "herbal/vegetal" = cannabis: "there's
  herb in the paper" (a rolled joint). L8 `տրաքան` and L9 `մութ
  կրակ հան` keep the smoke/fire register going. (drug reading:
  **prior**, from imagery; the lexemes are cited.)
- **L9 `մութ կրակ հան`** — "bring out [your] dark/raw fire," i.e.
  show your intensity/aggression. `կրակ` is corpus-attested as a
  person-intensity epithet (`կրակ երեխա`, ghamoyan p94); the
  English-rap "spit fire = deliver bars" reading was rejected by
  the critic as an import. `մութ` "dark" intensifies.
- **L7 `մյուս անգամ կամ մյուս կյանքում`** — folds the hook (`մյուս
  անգամ`) into `մյուս կյանքում` "in the next life," extending the
  deferral motif from "next time" to "next lifetime."
- **L13/L15 `ախպերական` repeated** — earnest in L13 (real
  brotherhood = "supernatural" strength), then in L15 (`Մի ասա ինձ
  ախպեր ախպերական`) "don't call me 'bro' just for show":
  rejecting the *performative/empty* use of the word, in contrast
  to the genuine brotherhood of L13 — a refinement, not a flat dis.

**Prior (not cited) — flagged:**
- L2 `Ութ անգամ շատացել [է] մուտքը ռուսական` — literal
  "the Russian entry/inflow has increased eightfold." `մուտք`
  "entrance / entry / inflow," `ռուսական` "Russian." The
  *referent* is unclear: Russian influence, Russian-speaker influx,
  Russian-money/import inflow? Gist (a sharp rise in something
  "Russian") is med-confidence; the specific target is **prior /
  unresolved**. Possibly a topical jab.
- L8 `Շատ զսպեցին ու տրաքան` — segmentation/agency uncertain.
  Read as "they held [it] back so long, then went off/burst"
  (suppression → explosion). `տրաքան` = `տրաքեցին` 3pl colloquial.
  The corpus only attests `տրաքած` = "drunk"; the "explode/blow
  up/lash out" verb sense is **prior**. **low.**
- L12 `Դիմավորենք, թող սաղ վրա գան` — `վրա գալ` "come at / come
  upon / attack." Read "let's meet it head-on, let them all come at
  us." `վրա գալ` as "attack/come at" is **prior** (not corpus-
  confirmed here); `դիմավորել` "to meet/greet" is standard.
- L14 `Հետ գնա, գամ` — terse and ambiguous. Possible readings:
  (a) "step back so I can come [through]"; (b) "go back, [let me]
  come"; (c) a `հետ գնալ` "go backward / regress" beat-flip. Too
  short to pin. **low.**
- L6 `մթոմ հուզական` — `մթոմ` is cited (p60), but the sarcasm
  ("*supposedly* emotional," i.e. fake-deep) is an **interpretive**
  reading of an attested word.

**Register-aware rendering:**
> Wait for the muse to hit — or leave it for next time? /
> Russian inflow's up eightfold, eight times over /
> the virgin faith is gone /
> and outside, the moon's lighting up the night /
> there's green rolled in the paper /
> your lyrics empty — "deep," supposedly /
> we'll hear it next time, or the next life /
> held it in too long, then they popped off /
> if you're in these streets, pull out that dark fire /
> this ain't just literary writing /
> but it's all here, and it's all positive /
> let's meet it — let 'em all come at us /
> we know our brother-strength, it's supernatural /
> step back, let me come through /
> don't "bro" me just for show (You)

*(Low-confidence — L8 "popped off," L14 "step back," and the whole
muse premise depend on uncertain transcription/sense; see table.)*

---

## Verse 3 (Dav)

**As sung:**
```
Ու՞ր պիտի փախնես, փակ են եթե 4 կոմերը
240 նստավ վրեդ էդ 4 մոմերը
Էս քաղաքում իրար ժպտում են ոչէ տոն օրերը
Էս քաղաքում անգիր են արե ստի կոմբոները
Էս քաղաքում աչք են ծակում ռոկոկոները
Նկատվում են սերնդում չար աճող կոկոնները
Coco chanel ցանած կուկուները
Մյուս կյանքում ըլնելու են իրանց հագի վրի շուբերը
Մյուս անգամ, սաղ կհասցնենք մյուս անգամ
Եթե չկա հույս անգամ, հույս կճարենք մյուս անգամ
Գիշերը լուսավորումա լուսնկան, դուս ընգածները դուս ընգան
Սաղ մնացին սուս էնքան
Որ էլ ի՞նչ խոսան, լավա սուս էթան
```

| # | line (normalized, copulas restored) | translation | conf. |
|---|---|---|---|
| 1 | `Ու՞ր պիտի փախնես, եթե փակ են 4 կողմերը` | "Where are you gonna run, if all 4 sides are closed?" | high |
| 2 | `240 նստավ վրեդ էդ 4 մոմերը` | "240 came down on you — those 4 candles" | low |
| 3 | `Էս քաղաքում իրար ժպտում են ոչ թե տոն օրերը` | "In this city they smile at each other — and not just on holidays" | med |
| 4 | `Էս քաղաքում անգիր են արել ստի կոմբոները` | "In this city they've memorized the lying combos / scams" | med |
| 5 | `Էս քաղաքում աչք են ծակում ռոկոկոները` | "In this city the Rococo (gaudy ones) stick out / catch the eye" | med |
| 6 | `Նկատվում են սերնդում չար աճող կոկոնները` | "You notice them in this generation — the evil, growing buds" | med |
| 7 | `Coco Chanel ցանած կուկուները` | "The cuckoos (fakes) decked / sown in Coco Chanel" | low |
| 8 | `Մյուս կյանքում ըլնելու են իրանց հագի վրի շուբերը` | "In the next life all they'll have is the fur coats on their backs" | high |
| 9 | `Մյուս անգամ, սաղ կհասցնենք մյուս անգամ` | "Next time — we'll make it all in time, next time" | high |
| 10 | `Եթե չկա հույս անգամ, հույս կճարենք մյուս անգամ` | "Even if there's no hope, we'll find hope next time" | high |
| 11 | `Գիշերը լուսավորում է լուսնկան, դուս ընգածները դուս ընգան` | "At night the moon lights it up — the cast-out ones fell away" | med |
| 12 | `Սաղ մնացին սուս էնքան` | "Everyone stayed so silent" | high |
| 13 | `Որ էլ ի՞նչ խոսան, լավ է սուս էթան` | "That — what's left to say? — better they stay quiet" | med |

**Slang & lexicon grounded:**
- `կոմ` = `կողմ` "side / direction" — colloquial consonant drop;
  **cited** ghamoyan p37 (`կոմ (կողմ)`, `արի էն կոմով`). So
  `4 կոմերը` = "the 4 sides/walls," not "rooms."
- `սաղ` "all / everyone" — **cited** ghamoyan slang lists p45/p46
  (consistent with verses 1–2).
- `սուս` "silent / quiet" — **cited** ghamoyan p45 (`սուսիկ-
  փուսիկ`), p96 (`սուսուփուս նստել`); `սուս կենալ` in
  sakayan/parnasyan. `սուս էթան` = colloquial "go/stay quiet."
- `աչք ծակել` "be conspicuous / stick out / catch the eye" — the
  lyric's exact idiom is **not in our corpus** (the earlier
  "parnasyan p440 / p63" cite was fabricated). The synonymous
  attested idiom is `աչքի ընկնել` "stand out / catch the eye"
  (parnasyan p183–184, `бросается в глаза`); the gloss is
  supported by that synonym, but `աչք ծակել` itself is **prior**.
- `անգիր անել` "to memorize / learn by heart" — **cited**
  (sakayan/tioyan vocab). `անգիր են արել` = "they've memorized."
- `տոն օր` "holiday / праздничный день" — **cited** tioyan.
- `շուբ` = Russ. `шуба` "fur coat" — **cited** ghamoyan p106
  (glossed `մուշտակ`).
- `լուսնկա` "moon / moonlight," `ժպտալ` "smile," `կոկոն` "bud (of
  a flower)" — **cited** standard vocab (`լուսնկա` sakayan
  p438–439; `կոկոն` sakayan p498), used metaphorically here for
  young people.
- Colloquial reductions consistent with the song's convention:
  `վրեդ`=`վրադ`, `արե`=`արել`, `վրի`=`վրա`, `ըլնելու`=`լինելու`,
  `ընգ-`=`ընկ-`, `դուս`=`դուրս`, `ոչէ`=`ոչ թե`, `էթան`=`գնան`.

**Wordplay:**
- **The fake-flash pun chain** (the verse's centerpiece, dense
  `-ները` mono-rhyme): `ռոկոկո` (Rococo — ornate/overdecorated →
  "gaudy show-offs") → `կոկոն` ("bud," echoing ROCO-KO and "Coco")
  → `Coco Chanel` (luxury-brand drop) → `կուկու` ("cuckoo" — the
  bird that fakes its nest; here "fakes / impostors"). Four near-
  homophones (ko-ko / ro-ko-ko / ku-ku / Co-co) stacked to mock
  conspicuous fake-luxury people. **The pun chain *is* the
  meaning;** the literal glosses are scaffolding.
- **L2 `240` / `4 մոմերը` — unresolved (critic overturned the
  funeral reading).** `մոմ` is just "candle" (no funereal sense in
  corpus); there is no support for `նստել`=prison-time or
  `240`=Criminal-Code article. `240` is most likely a number pun
  off the preceding `4` (4 sides → 4 candles → 240). Do **not**
  assert a funeral image — genuinely open.
- **L11 `դուս ընգած`** — `ընգ`=`ընկ` is documented Yerevan
  voicing (ghamoyan p39 `ընկնել-ընգնել`), so `դուս ընգած` =
  `դուրս ընկած` "cast out / dropped out" (possible secondary play
  on `դուխից ընկնել` "lose nerve," ghamoyan p49). Was prior — now
  grounded.
- **L10 `անգամ` pun** — here `անգամ` = "even" (`եթե չկա հույս
  անգամ` "even if there's no hope"), a homophone of the song's
  refrain `անգամ` "time / occasion." Deliberate.
- **Rhyme scheme:** relentless `-երը`/`-ները` mono-rhyme
  (`կոմերը · մոմերը · օրերը · կոմբոները · ռոկոկոները · կոկոնները ·
  կուկուները · շուբերը`), then the hook-echo `անգամ · անգամ` and
  the `-ան` cluster `ընգան · էնքան · էթան`.
- **Brand / vanity motif:** `Coco Chanel` + `шуба`/fur coats; the
  moral turn (L8) — in the next life the show-offs keep only the
  coats on their backs.
- **L11 figura etymologica:** `դուս ընգածները դուս ընգան` ("the
  fallen-out fell out") — deliberate repetition for flow.

**Prior (not cited) — flagged:**
- L2 `240` — unidentified (a price/sum? date? penal-code article?
  or literally "240 candles"?). The candle/funeral reading of
  `4 մոմերը` is **prior** (image-inference, not an attested idiom).
  **low.**
- L5 `ռոկոկո` "Rococo → gaudy people" — **prior** (cultural
  inference; not in corpus).
- L7 `Coco Chanel` (brand) and `կուկու` "cuckoo = fake/impostor" —
  **prior**; `ցանած` read as "sown / strewn / decked out (in)" is
  the weak link (could be `ցանկ-` "wish/list"). **low.**
- L4 `կոմբո` = Eng./gaming "combo" → "scams / routines" —
  **prior** loanword; `ստի` read as "of lying / fake." **med→low.**

**Register-aware rendering:**
> Where you gonna run when all four walls are closed? /
> 240 came down on you — those four candles /
> in this city they smile at each other, and not just on holidays /
> in this city they got the lying combos memorized /
> in this city the Rococo crowd stick out a mile /
> you spot 'em in this generation — the rotten little buds /
> the cuckoos all decked out in Coco Chanel /
> next life all they keep is the fur coat on their back /
> next time — we'll make it all, next time /
> even if there's no hope, we'll find hope next time /
> the moon lights up the night, the cast-outs all fell off /
> everybody went so quiet — /
> so what's left to say? better they stay silent.

*(Low-confidence — L2 `240`/candles and the `ռոկոկո/Coco/կուկու`
pun chain are cultural inference, not corpus-cited; see table.)*

---

## Open questions / gaps

- Verse-1 L11–12, L20: `մի տէ`, `բես` — see prior flags above.
- L2 chorus `շատէ` segmentation — needs audio.
- Chorus L4 `ճամփեքը`: operator hears `ք` (not `ր`) in the audio.
  Read as a marked/archaic `-ք` plural "the roads" (standard
  `ճամփաները`; productive-colloquial `ճամփերը`). `ճամփեք` is a
  nonce form — not corpus-attested; open whether it's a stylized
  `-ք` plural, a dialectal form, or take-to-take variation.
- Verse-2 L2 `մուտքը ռուսական` — referent unclear (Russian
  influence / influx / inflow?); a topical jab whose target isn't
  recoverable from text alone.
- Verse-2 L8 `զսպեցին ու տրաքան` — suppression→explosion reading;
  corpus attests `տրաքած` only as "drunk," not the verb "blow up."
- Verse-2 L14 `Հետ գնա, գամ` — too terse to disambiguate; three
  candidate readings, all low-confidence.
- Verse-3 L2 `240` — unidentified referent; `4 մոմերը` candle/
  funeral image is prior, not an attested idiom.
- Verse-3 L7 `ցանած` segmentation (`ցան-` "sow/strew" vs `ցանկ-`
  "wish") unresolved.
- Verse-3 L11 `դուս ընգած` "thrown out / off the rails" — street
  idiom not attested in the books.
- Verse-3 pun chain `ռոկոկո / Coco Chanel / կուկու` — meaning is
  prior (cultural inference), not corpus-cited.

## Verification log

Three adversarial critic agents (skeptical-native-speaker frame,
corpus + web tools) verified meaning at line granularity — one per
section group (chorus+V1, V2, V3). Each was told *not* to agree but
to find where glosses are wrong. Findings reconciled into the file
above; key outcomes:

### Corrections applied
- **V1 L14 — grammar error fixed (high).** `հասցրա` is colloquial
  **1sg aorist** ("I made it"), not an imperative (imperative =
  `հասցրու`/`հասցրեք`). Re-glossed "I made it in time — but you,
  build up your home." Wordplay note + rendering updated.
- **V2 L9 — over-translation fixed (med).** "spit fire" imported
  the English-rap idiom; `կրակ` is corpus-attested as a *person*-
  intensity epithet (`կրակ երեխա`, ghamoyan p94), not "rap bars."
  Re-glossed "bring out [your] dark fire."
- **V2 L15 — reframed (med).** From "dis on fake brotherhood" to
  "don't call me 'bro' just for show" — the contrast with the
  *genuine* `ախպերական` of L13.
- **V3 L2 — invented image removed (med-high).** Funeral/candle
  reading overturned: `մոմ` carries no funereal sense in corpus;
  no support for `նստել`=prison or `240`=Criminal-Code article.
  `240` marked genuinely unresolved (likely a number pun off `4`).
- **V1 L12 — refined.** `սումմեդ` = Russ. `сумма` + 2sg poss "your
  worth (money)," better than "number."

### Glosses upgraded from *prior* → *cited*
- **V1 L5 `քցել`** (=`գցել` "drop/lose") — ghamoyan p39.
- **V3 L8 `շուբ`** (=`մուշտակ` "fur coat," Russ. `шуба`) —
  ghamoyan p106. Confidence med→high.
- **V3 L11 `դուս ընգած`** (=`դուրս ընկած`; `ընգ`=`ընկ` voicing) —
  ghamoyan p39. Confidence low→med.
- **V3 L5 `աչք ծակել`** ("be conspicuous/garish") — confirmed
  ghamoyan p63 (already cited; confidence reaffirmed high).

### Grammar claims pressure-tested and upheld (high)
- Chorus `Թող մնա` jussive (`թող`+3sg subjunctive, not imperative).
- Chorus L4 `անցել` intransitive; `ճամփեքը նույն [են]` copular.
- V1 L17 `վիզ դնել` ("put one's neck out") correctly kept apart
  from the corpus's opposite idiom `վիզ ծռել` ("submit/yield") —
  a deliberate false-friend trap avoided.

### Left flagged (critics agree: genuinely uncertain)
- Chorus L2 `շատէ` segmentation (needs audio).
- V1 L11 `մի տէ`, L20 `բես` (бес) — Russian-loan slang, plausible
  but not corpus-pinnable.
- V2 L1 `մուսա`/`մյուս` pun (transcription itself unverified —
  could be `մյուսը գա` "the next one comes"); L2 `մուտքը ռուսական`
  referent; L5 `բուսական` cannabis-vs-"empty words"; L12 `վրա գալ`
  attack-vs-welcome directional ambiguity; L14 `Հետ գնա, գամ`.
- V3 L7 `ցանած` segmentation; the `ռոկոկո/Coco/կուկու` pun chain
  (meaning is cultural inference — no listener-consensus source
  found online).

### Method caveat
All three critics independently confirmed **no web-accessible
transcription or analysis** of this song exists (YouTube/Shazam
expose no text; no Genius page). Every line therefore rests on the
Musixmatch transcription, which could not be independently
verified — reinforcing the `low` flags on the hardest lines.

## Whole-song review (pass 2)

The pass above verified meaning section-by-section but never
reviewed the *assembled* file. A second multi-agent pass did:
three reviewers over the whole document — **structural/
consistency**, **editorial (learner POV)**, and **citation
re-audit** (grep every cited page against the corpus).

### Citation errors caught & fixed (the headline finding)
The citation re-audit found **six citations that were wrong** —
introduced when the verse subagents drafted from pre-training
prior. This is the repo's canonical failure mode (plausible-
sounding citation, never checked). All fixed:

| item | claimed | actual | fix |
|---|---|---|---|
| `զսպել` | parnasyan p354 "Cited" | not in corpus | → transparent-standard (not cited) |
| `աչք ծակել` | parnasyan p440 / p63 "Cited" | not in corpus | → `prior`; real synonym `աչքի ընկնել` parnasyan p183–184 |
| `կուսական` | sakayan p383 | **parnasyan** p383 (right page, wrong book) | → book corrected |
| `լուսնկա` | parnasyan p438–440 | **sakayan** p438–439 (right page, wrong book) | → book corrected |
| `սաղ` (V2) | ghamoyan p44–46 | only p45/p46/p83 | → range corrected |
| `բուսական` | sakayan p357+p486 | only p486 | → p357 dropped |

Lesson for the routine: **song-file citations need the same
grep-against-corpus discipline as topic files** (`citation-check`).
This audit is now step 7 of `songs/README.md`.

### Structural fixes (stale notes from reconciliation)
- **V2 L9** — "spit fire" survived in the Wordplay note, the
  `կրակ` slang bullet, and a Prior flag *after* the gloss was
  changed; all three updated to the intensity-epithet reading
  (`կրակ երեխա`, ghamoyan p94).
- **V3 L2** — the register rendering still said "four candles
  *burning*," silently re-committing to the funeral image the
  pass-1 critic overturned; "burning" removed.
- **V2 L15** — Wordplay still framed it as a "dis turn / fake
  brotherhood"; softened to match the reconciled "just for show."

### Editorial fixes (learner POV)
- Added a **"What the song is about"** synopsis above Methodology
  (who raps what; the refrain's arc) — the biggest reader gap.
- Added **low-confidence notes under each register rendering** —
  skim-readers read the blockquotes, which present guesses
  (`բես`, `240`/candles, "popped off") as confident punchlines.
- **V2 L1** muse-pun confidence dropped `high`→`med` — it rests on
  the unverified transcription `մուսան` (could be `մյուսը գա`).
- Standardized "Slang & lexicon grounded" headers; fixed chorus
  rendering "bounced"→"moved on"; clarified `գիդեն`
  spelling-vs-lexeme.

### Net
Pass 2 changed no *meanings* beyond what pass-1 critics already
flagged, but caught fabricated citations and internal
contradictions that section-by-section review structurally could
not. The file is now internally consistent.
