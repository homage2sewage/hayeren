---
title: 8 SUTASAN (Սուտասան, "Liar")
artists: [Brunette, Nare Manukyan, Arthur Armeni, Fred Irie]
genre: pop / R&B (Armenian)
album: LOVE REVERSED (2025-11-05)
lyrics_source:
  - "User-provided chorus excerpt (5 lines) — primary text processed here"
  - "Web search confirmed title/artist: matchlyric.com, shazam.com (full verse text NOT cleanly acquired — see Gaps)"
date_processed: 2026-06-10
status: partial  # only the chorus/hook is processed; verses are an open gap
---

# Brunette — 8 SUTASAN (Սուտասան)

## What the song is about

`Սուտասան` "liar" is the hook word. The chorus is **three parallel
refusals** (`Չեմ ... Չեմ էլ ... Չեմ էլ ...` — "I won't... nor
will I... nor will I...") aimed at an ex, built on an extended
metaphor: the addressee is figured as an **old car gone cold** —
something the speaker refuses to steal, endure, or come to own,
because it's a *trap*. Lines 4–5 retroactively re-gender the
metaphor's referent toward a person (`ինքն էլ ... սուտասան` "she
too is a liar"), so the "car" is a vehicle (pun acknowledged) for
the deceptive lover.

*Learner's analysis, not an authoritative reading — see
Methodology for how meanings were obtained and where they're
uncertain.*

## Methodology & provenance

**Text.** Only the **chorus/hook** (5 lines) is processed here —
supplied by the operator, clean. Title/artist confirmed by web
search (Brunette feat. Nare Manukyan, Arthur Armeni, Fred Irie,
on *LOVE REVERSED*, 2025-11-05). The **full verse text was not
acquired**: the lyric aggregators (matchlyric, shazam) returned
403/no-text. Treat even the chorus as a **transcription** —
line splits and colloquial forms (`դե`, `ա` for `է`) are
transcription-confidence `medium`, not corpus-verified.

**Meaning.** Processed by the `songs/README.md` routine:
KB-grounded the lexicon via `frequency/query_kb.py` + `grep` of
the four-book corpus; translated line-by-line graded; verified by
a separate meaning-critic agent; **every cited page re-audited
against the corpus** (the mandatory step-7 citation audit — it
caught one fabricated attribution, see Verification log).

**What is cited vs. prior.** All content verbs/nouns are
**corpus-grounded** (citations below). The grammar (the `չեմ V-ա`
negative future, the `կ-` hypothetical future, `տիրանալ`+dative,
colloquial copula `ա`) is corpus/transparent-standard. The
**"car = deceptive lover" metaphor** and the "dead/lifeless" shade
of `սառած` are **interpretive** (prior), flagged `med`.

**Related KB.** `topics/morphology/negation.md` (the `չեմ V-ա`
paradigm), `topics/morphology/future_tenses.md` (the `կ-`
conviction future), `topics/syntax/el_particle_position.md`
(`Չեմ էլ` = additive / emphatic "not even").

---

## Chorus (hook)

**As sung:**

```
Չեմ գողանա ես քո հին սառած մեքենան
Չեմ էլ դիմանա կխեղդի հետ նստած սատանան
Չեմ էլ տիրանա նրան դե քո սարքած ծուղակն ա
Աչքերիս առաջ ինքն ա
Ինքն էլ քո նման սուտասան
```

**Normalized (copulas/clause breaks made visible):**

```
Չեմ գողանա ես քո հին սառած մեքենան։
Չեմ էլ դիմանա — կխեղդի հետ նստած սատանան։
Չեմ էլ տիրանա նրան — դե քո սարքած ծուղակն [է]։
Աչքերիս առաջ ինքն [է]։
Ինքն էլ քո նման սուտասան [է]։
```

**Line-by-line, graded:**

| # | Armenian | Literal | Conf. |
|---|---|---|---|
| 1 | Չեմ գողանա ես քո հին սառած մեքենան | I won't steal your old car gone cold | high (grammar/lexicon); metaphor med |
| 2 | Չեմ էլ դիմանա, կխեղդի հետ նստած սատանան | Nor will I hold out — the devil seated beside me will choke me | high |
| 3 | Չեմ էլ տիրանա նրան, դե քո սարքած ծուղակն ա | Nor will I come to own her/it — well, it's the trap you set | high; referent of նրան ambiguous |
| 4 | Աչքերիս առաջ ինքն ա | There she/it is, right before my eyes | high |
| 5 | Ինքն էլ քո նման սուտասան | And she/it too is a liar, just like you | high |

**Lexicon (all corpus-cited):**

- **գողանալ** "to steal" (воровать) — tioyan p38, p351. `Չեմ
  գողանա` = `չեմ` + negative participle = negative future **1sg**
  ("I won't steal"); overt `ես` confirms 1sg (a 3sg would be `չի
  գողանա`). Per `topics/morphology/negation.md`.
- **սառած** "cooled, gone cold" (остывший) — parnasyan p216
  (`սառչել → սառած`). Literal sense is "cold"; **"frozen/dead"
  overshoots** — keep it as an interpretive shade, not a gloss.
- **դիմանալ** "to endure, withstand, hold out" (выдерживать,
  терпеть, вынести) — parnasyan p362. Intransitive/absolute here
  ("I can't take it / won't last"); it does **not** take `կխեղդի`
  as a complement — line 2 is two clauses.
- **խեղդել** "to choke, strangle, drown" (душить, задушить,
  топить, утопить) — parnasyan p376. `կխեղդի` = `կ-` hypothetical
  future **3sg transitive**; subject = `հետ նստած սատանան` (the
  devil seated beside me), object = implied "me." (1sg would be
  `կխեղդեմ` — so "I'll choke the devil" is excluded.)
- **տիրանալ** "to gain ownership / come to own" — sakayan p514
  (`տիրանալ [tiranal] to gain ownership`). Inchoative + dative
  (`նրան`). Not "inherit" (that's `ժառանգել`).
- **սարքել** "to make, build, set (up)" — sakayan p511 (headword),
  p406/p137 (examples). `քո սարքած ծուղակն ա` = "it's the trap you
  set."
- **ծուղակ** "trap" — sakayan p496 (headword; transparent-standard).
- **սուտասան** "liar; also adj." (лжец, врун; тж прил.) — **tioyan
  p287, p288, p376** (`սուտ ասել` "to tell a lie" → `սուտասան`).
  The adjectival use fits the predicate slot: `... քո նման
  սուտասան [է]` = "is a liar, like you."
- **ա** = colloquial `է` "is"; **դե** = colloquial discourse
  particle "well"; **ինքը** = colloquial 3rd-person pronoun
  ("he/she/it"). Transparent-standard colloquial.

**Wordplay / notes:**

- `Չեմ էլ` (×2): per `el_particle_position.md`, post-copula `էլ`
  is additive ("also/either") or emphatic ("not even") — **not**
  the preverbal "anymore" reading (that needs `Էլ չեմ...`). So
  "nor will I" / "I won't even" both license; "anymore" does not.
- **Referent ambiguity** (`նրան`, `ինքն`): deliberately
  unresolved between the car and the person. Preserve "her/it" —
  lines 4–5 tip it toward a person but never name one.

**Register-aware rendering:**

> I won't steal your old car gone cold —
> and I won't hold out either: the devil riding shotgun will choke me.
> I won't come to own her, either — well, she's the trap you set.
> There she is, right before my eyes —
> and she, too, is a liar, just like you.

---

## Open questions / gaps

- **Full lyrics not acquired.** Only the chorus is processed.
  Verses need a clean transcription source (lyric video / official
  source), then the same routine. Until then `status: partial`.
- **`սառած` "dead/lifeless"** — interpretive, not lexical
  (corpus gives only "cooled/cold").
- **Referent of `նրան`/`ինքն`** — car vs. person; left ambiguous
  by design.
- **Colloquial transcription** (`դե`, `ա`) — `med` confidence on
  the exact text; meaning is unaffected.

## Verification log

- **Meaning-critic agent** (adversarial, different framing):
  confirmed the grammar reading on every contested point —
  `գողանա` is 1sg not 3sg; line 2 is two clauses (`դիմանալ` doesn't
  take `կխեղդի`); the devil is the choker not the chokee;
  `տիրանալ` = "come to own" not "inherit". Corrected the prose:
  `դիմանալ` is absolute (dropped spurious "endure **it**"),
  `սառած` = "gone cold" not "frozen", `(dead)` demoted to
  interpretive.
- **Citation re-audit (mandatory step 7):** re-grepped every
  cited page against the corpus. **Caught one fabrication** — the
  critic attributed `սուտասան` to *parnasyan p376*; it is actually
  **tioyan p287/288/376** (page 376 collided with `խեղդել`@parnasyan
  p376). Corrected here. All other citations (`գողանալ` tioyan
  p38/351, `սառած` parnasyan p216, `դիմանալ` parnasyan p362,
  `խեղդել` parnasyan p376, `տիրանալ` sakayan p514, `սարքել` sakayan
  p511/406/137, `ծուղակ` sakayan p496) verified present and
  correct.
