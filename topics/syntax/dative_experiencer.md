---
topic: dative-experiencer construction (`դուր գալ` and family) and the `դուր / դուրս / դուռ` near-homograph trap
domain: syntax
units: [parnasyan, tioyan, ghamoyan]
related: [idioms-phrasal, irregular-verbs, present-tense, case-system]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: tioyan
    page: 121
    y_range: [2210, 2250]
    verbatim_quote:
      - "դուր գալ нравиться"
    supports: supported
    note: |
      tioyan's bilingual gloss for the verb `դուր գալ`: Russian
      *нравиться* "to be pleasing to (someone), to be liked by".
      The pairing is exact — Russian's *нравиться* uses the same
      dative-experiencer construction (subject = thing liked,
      experiencer in dative), and the gloss assumes the L1=Russian
      reader will recognise the syntactic shape directly.
  - id: 2
    book: tioyan
    page: 121
    y_range: [2155, 2200]
    verbatim_quote:
      - "դուրս գալ ВЫХОДИТЬ"
    supports: supported
    note: |
      tioyan's bilingual gloss for the *different* verb `դուրս գալ`
      "to come out / exit", appearing one line above [#1] on the
      same page. Russian *выходить* is a regular intransitive motion
      verb; the structure is straightforwardly subject + verb +
      ablative (*ВЫЙТИ ИЗ X* = `X-ից դուրս գալ`). The minimal-pair
      attestation on a single tioyan page is the clean evidence
      that these are two different verbs, not variants of one.
  - id: 3
    book: parnasyan
    page: 181
    y_range: [2010, 2170]
    verbatim_quote:
      - "ինձ դուր է գալիս"
      - "мне нравится"
    supports: supported
    note: |
      parnasyan's full-sentence example showing the dative-
      experiencer construction in present-tense indicative.
      The Armenian: *Աբամի մեջ ինձ դուր է գալիս* "in Aram, to-me
      pleasing comes (about something)" → "I like (something)
      about Aram." Russian: *В Араме мне нравится добро-* "(In
      Aram I like (his) goodness)" — same dative experiencer
      structure. The OCR'd `Աբամի` is an OCR error for `Արամի`
      (ր ↔ բ are voiced-stop confusions per the parnasyan OCR-
      caveats); the *grammatical* attestation is unaffected.
  - id: 4
    book: parnasyan
    page: 101
    y_range: [2055, 2200]
    verbatim_quote:
      - "շատ դուր եկավ"
      - "очень понравился"
    supports: supported
    note: |
      parnasyan's aorist-tense example: *շատ դուր եկավ* "(s)he/it
      pleased very much / I/you/they liked it very much (perf.
      aorist)" with Russian *очень понравился* (perfective past).
      The aorist of `դուր գալ` inflects only `գալ` → `եկավ` (3sg
      aorist of irregular `գալ`), and `դուր` stays invariant.
      Confirms the conjugation pattern with a citation in a tense
      other than the present.
  - id: 5
    book: tioyan
    page: 165
    y_range: [775, 930]
    verbatim_quote:
      - "ես դուրս եկա սենյակից"
    supports: supported
    note: |
      tioyan's full-sentence example using `դուրս գալ` in aorist:
      "I came out of the room" — *ես դուրս եկա սենյակից*. Subject
      `ես` (nom.), verb `դուրս եկա` (1sg aorist of `գալ` + `դուրս`),
      ablative complement `սենյակից` "from the room." Confirms
      the *motion-verb* structure of `դուրս գալ` in contrast to
      [#3]'s dative-experiencer structure for `դուր գալ`.
  - id: 6
    book: ghamoyan
    page: 63
    y_range: [108, 122]
    verbatim_quote:
      - "ջրի երես դուրս գալ"
    supports: partially-supported
    note: |
      ghamoyan idiom-catalogue entry illustrating `դուրս գալ` in a
      figurative phrasal idiom: *ջրի երես դուրս գալ* "to come out
      onto the surface of the water" → "to be revealed / surface /
      come to light." Confirms `դուրս գալ` extends into
      metaphorical idioms where the directional `out` reading
      stays compositional. Listed as `partially-supported` because
      the idiom-list is a catalogue without per-item glosses;
      the meaning is inferred from form + pattern, not explicit.
gaps:
  - "Etymology of `դուրս` (← `դուռ` 'door' + fossilised directional ending?) is not addressed by any of the cited books — pre-training prior only. Acharyan's etymological dictionary would close this; tagged as research follow-up."
  - "Other psych-verbs in the same dative-experiencer construction — `քուն գալ` 'to feel sleepy' (lit. 'sleep comes'), `սով գալ` 'to feel hungry', `ցավ գալ` 'to feel pain' — are not cited here. The construction generalises beyond `դուր գալ` but the cross-verb generalisation isn't book-attested in our extracted corpus."
  - "Argument-order variation. Examples cited use `Y-ին X դուր է գալիս` and `X-ին դուր է գալիս Y`; the discourse / register / focus correlates of word order aren't formalised."
  - "Negation paradigm: tioyan p353 has *դուր չգալ* 'to not like'; the negation pattern follows pattern 1 from `topics/morphology/negation.md` (`չ-` prefix on auxiliary, which moves before `դուր`: *չի դուր գալիս*) but the full negative paradigm isn't enumerated."
  - "Comparison with the transitive `հավանել` 'to like (deliberately/approvingly)' — tioyan p197 attests *(նա) հավանեց ему понравилось* 'he/she liked-PFV / to-him liked-PFV', showing both the Armenian transitive and Russian dative-experiencer construction together, suggesting the lexical-aspect / register split between `դուր գալ` and `հավանել` deserves its own treatment. Out of scope here."
---

# Dative-experiencer construction: `դուր գալ` and the `դուր / դուրս / դուռ` trap

Eastern Armenian uses a **dative-experiencer construction** to
express liking. The thing liked is the grammatical subject
(nominative); the person who likes is in the dative. The verb
is the idiom `դուր գալ` (lit. "to come (as) pleasing"), where
`դուր` is invariant and `գալ` carries all the morphology. [#1]
[#3] [#4]

```
Y                ինձ                    դուր է գալիս
[Y nominative]   [me dative-experiencer] [is-pleasing-coming]

  ↑ subject       ↑ experiencer            ↑ predicate
   = thing liked   = person who likes
```

This is the same shape as Russian *нравиться*, Spanish *gustar*,
Italian *piacere*, French *plaire à*. English flips: the
experiencer becomes subject, the thing-liked becomes object.

> **Parnasyan [#3]**: *Աբամի մեջ ինձ դուր է գալիս* — В Араме
> мне нравится…
> "In Aram, I like (his)..." (lit. "in Aram, to-me pleasing
> comes...")

The dative experiencer can never be the subject. *Ես դուր եմ
գալիս* would mean "I am pleasing (to someone)" — which is
grammatical, but inverts the roles.

## Conjugation

`դուր` stays put; `գալ` (irregular verb of motion) inflects:

| reading | form | example |
|---|---|---|
| present | `դուր է գալիս` | *Ինձ դուր է գալիս ֆիլմը* "I like the film" [#3] |
| aorist | `դուր եկավ` | *Շատ դուր եկավ* "(I) liked it very much" [#4] |
| perfect | `դուր է եկել` | "(I) have come to like" |
| imperfect | `դուր էր գալիս` | "(I) used to like" |
| future | `դուր կգա` | "(I) will like" |
| subjunctive | `դուր գա` | "(that I) would like" |
| infinitive | `դուր գալ` | "to like" [#1] |
| negative pres | `դուր չի գալիս` | "(I) don't like it" |

Negation follows pattern 1 from
`topics/morphology/negation.md`: prefix `չ-` to the auxiliary,
which moves before `դուր`. So *չի դուր գալիս* "is-not pleasing
to (someone)" — `դուր` keeps its slot, the negated auxiliary
hops in front of it.

## Russian / Spanish / Italian parallel

| Armenian | Russian | Spanish | English |
|---|---|---|---|
| Ինձ դուր է գալիս գիրքը | Мне нравится книга | A mí me gusta el libro | "I like the book" |
| Ինձ դուր եկավ ֆիլմը | Мне понравился фильм | A mí me gustó la película | "I liked the film" |
| Քեզ դուր կգա | Тебе понравится | A ti te va a gustar | "You'll like it" |

For a **Russian L1 learner**, the construction is one-to-one:
the experiencer is in the same case (dative), the thing liked
is in the same case (nominative), the auxiliary verb behaves
analogously. Almost no syntactic learning required — only the
lexical pair `դուր գալ` ↔ *нравиться* needs memorising.

For an **English L1 learner**, the trap is the **subject-object
flip**. The instinct "I" + "like" + "the book" produces *Ես
սիրում/հավանում եմ գիրքը* with a transitive verb — grammatically
valid but with `հավանել` not `դուր գալ`. The natural everyday
"liking" verb in Armenian is `դուր գալ`, and to use it correctly
the learner has to consciously invert the argument structure.

## Other psych-verbs in the same construction

The dative-experiencer pattern extends to several other Armenian
verbs that express bodily / psychological states. The
generalisation is *book-uncited* in our corpus (see `gaps:`); the
list below is project-internal:

| construction | meaning | structure |
|---|---|---|
| `քուն գալ` | "to feel sleepy" (lit. "sleep comes") | `Ինձ քուն է գալիս` "I'm getting sleepy" |
| `սով գալ` | "to feel hungry" (lit. "hunger comes") | `Ինձ սով է գալիս` "I'm getting hungry" |
| `ցավ գալ` | "to be in pain" | `Ինձ ցավ է գալիս` "I'm in pain" |

Each follows the same shape: experiencer in dative, sensation as
nominal subject, verb `գալ` carrying tense/agreement. The pattern
is productive — when a state "happens to" the experiencer rather
than being chosen by them, this construction is the natural
choice.

## The near-homograph trap: `դուր / դուրս / դուռ`

Three words look almost identical in script and have *no
relationship in modern Armenian usage*:

| word | POS | meaning | role |
|---|---|---|---|
| **`դուր`** | predicative noun | "pleasing" — only in `դուր գալ` | psych-verb root |
| **`դուրս`** | adverb / postposition / noun | "out, outside" | motion / location |
| **`դուռ`** | noun | "door, gate, exit" | ordinary noun |

The verb `դուրս գալ` "to come out, exit" exists, is common, and
is *not* `դուր գալ`. tioyan p121 attests both on adjacent lines
[#1] [#2] — the same source treats them as separate lexical
items, not variants.

| `դուր գալ` (psych-verb) | `դուրս գալ` (motion-verb) |
|---|---|
| *Գիրքը ինձ **դուր է գալիս*** [#3] | *Ես **դուրս եկա** սենյակից* [#5] |
| dat. experiencer + nom. thing | nom. subject + abl. source |
| "I like the book" | "I'm going out of the house" |
| ↔ Russian *нравиться* | ↔ Russian *выходить* |

### Diagnostic for L2 learners

The case of the human participant tells you which verb you're in:

- **dative `-ին`** (or implicit dative pronoun like `ինձ`, `քեզ`)
  → it's `դուր գալ` (psych).
- **nominative subject + ablative source `-ից`** → it's
  `դուրս գալ` (motion).

If the sentence has *both* a dative argument and an ablative
argument, you're probably looking at one of `դուրս գալ`'s
metaphorical extensions (e.g. *ջրի երես դուրս գալ* "to surface
/ come to light", lit. "to come out onto the water's face"
[#6]; or *հունից դուրս գալ* "to lose composure", lit. "to come
out of one's groove" — ghamoyan p49 area), where the
experiential reading layers on top of the motion structure.
Check whether the dative argument is human-experiencer or part
of a body-of-water / channel metaphor — if metaphor, motion-verb
wins.

### Etymology — flagged as workspace gap

It is *plausible* that historically `դուրս` derives from `դուռ`
"door" via an old directional/ablative ending — same shape as
many Armenian directional adverbs (e.g. `ներս` "in" ← `ներ`
"interior", `վար` "down" ← old locational). **None of our four
books cites this etymology.** Tagged as a research follow-up;
Acharyan's etymological dictionary would close it. Until then,
synchronically `դուր / դուրս / դուռ` are three separate lemmas
that happen to look similar.

## Comparison with `հավանել`

Armenian has a *transitive* "to like" verb — `հավանել` —
attested at tioyan p197 as *(նա) հավանեց ему понравилось* and
p363 as *հավանել понравиться*. The transitive structure mirrors
English: subject = experiencer, object = thing liked.

| feature | `դուր գալ` | `հավանել` |
|---|---|---|
| structure | dative experiencer (Y → X) | transitive (X → Y) |
| nuance | spontaneous, instinctive liking | considered, evaluative liking |
| frequency | dominant in everyday speech | secondary; more deliberate register |
| Russian gloss | нравиться | одобрять / нравиться (одобрительно) |

For most "I like X" everyday cases, `դուր գալ` is the unmarked
default. `հավանել` carries an evaluative flavor: "I find X
acceptable / approve of X." Cross-pattern cited in tioyan;
deserves a dedicated topic eventually, but the contrast is
sketched here for completeness.

## Cross-references

- `topics/morphology/irregular_verbs.md` — `գալ` is irregular;
  the conjugation in this construction follows that paradigm.
- `topics/morphology/aorist.md` — `դուր եկավ` example.
- `topics/morphology/present_tense.md` — `դուր է գալիս` example.
- `topics/morphology/negation.md` — `չ-` prefix and movement
  for `դուր չի գալիս`.
- `topics/lexicon/idioms_phrasal.md` — `դուրս գալ`-based
  idioms (`հունից դուրս գալ`, `ջրի երես դուրս գալ`).
- `topics/morphology/case_system.md` — dative function as
  experiencer, ablative as source.
- `cards/top_1000.tsv` — `դուր գալ` card with the dative-
  experiencer gloss (rank 313).
- `transliteration-notes.md` — the L2 confusion *դորս գալ* /
  *դուր գալ* in informal Latin transliteration belongs here.
