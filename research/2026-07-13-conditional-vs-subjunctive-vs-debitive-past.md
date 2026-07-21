# Conditional past vs subjunctive past vs debitive past (պիտի)

Q&A note produced via the `answer-q` protocol (KB bundle +
`verify_citations.py`, all citations green). Candidate seed for the
missing hypothetical/conditional-mood and debitive-mood topic files —
see `topics/morphology/subjunctive_mood.md` § gaps ("derived moods
need their own topic eventually").

## The three forms share one core

All three are built on the **same synthetic form** — the subjunctive
past: bare stem + `-եի -եիր -եր -եինք -եիք -եին` (1st conj) /
`-այի -այիր -ար…` (2nd conj), so `գրեի`, `կարդայի`
(`topics/morphology/subjunctive_mood.md`, single-source sakayan). The
other two moods are *derived* from it (`armenian-grammar.md`, full
tense-system table):

| form | construction | rough English |
|---|---|---|
| subjunctive past | `կարդայի` | "(if) I read / were reading" — irrealis building block |
| conditional past | `կ-` + subj. past → `կկարդայի` | "I would have read" |
| debitive past | `պիտի` + subj. past → `պիտի կարդայի` | "I had to / was supposed to read" |

The choice between them is not about the *form* of the verb — it's
about which marker (none / `կ-` / `պիտի`) you attach, and each marker
picks a different modal meaning.

## 1. Subjunctive past — the subordinate/irrealis workhorse

The bare form mostly lives in **subordinate clauses**: the
`եթե`-protasis of counterfactuals, clauses after `որ`/`որպեսզի`,
wishes, and polite past requests (`Կարո՞ղ էի խնդրել` "Could I
ask…?") — per `topics/morphology/subjunctive_mood.md`. It's the "if I
had known" half of a counterfactual, never the "I would have" half.

## 2. Conditional past (`կկարդայի`) — the counterfactual main clause

Dum-Tragut: the conditional past expresses "an action which should
have been performed in past, but which was not performed due to
certain conditions and circumstances" [dumtragut p277]. The canonical
pairing with the subjunctive past in one sentence:
«Նրան նամակ կգրեի, եթե իմանայի նրա հասցեն» "I would have written to
him, if I had known his address" [dumtragut p278] — `կգրեի`
conditional in the main clause, `իմանայի` bare subjunctive in the
if-clause.

Second, less obvious use: **past-habitual narrative** ("used to"),
with plain indicative meaning — the village's oldest woman
«կպատմեր զանազան հետաքրքիր պատմություններ ու հեքիաթներ» "used to tell
various interesting stories and fairy tales" [dumtragut p279].

Terminology trap: Sakayan calls this mood "hypothetical", Dum-Tragut
"conditional"; Armenian school term `պայմանական`, Russian `условное`
(`grammar-terms.md`).

## 3. Debitive past (`պիտի կարդայի`) — past obligation

The debitive mood is marked by `պիտի` (more common **spoken**) or
`պետք է` (more common **written**) + the subjunctive form; `պիտի`
can't be used on its own [dumtragut p281]. Future vs past:
«Վաղը պիտի գնամ համալսարան» "Tomorrow I have to go to the university"
[dumtragut p283] vs the past «Դուռը պիտի բացեր այս բանալիով» "He
should have opened the door with this key" [dumtragut p287].

The debitive past covers three readings [dumtragut p287]:

- **unfulfilled obligation** — "should have opened" (as above);
- **future-in-the-past obligation** — "was to / was supposed to",
  when the reference point is in the past;
- **averted imminent event** — "one more minute and the bomb would
  have exploded" (often with `մի րոպե ևս` "one more minute and…").

That third reading is where debitive past and conditional past can
both come out as English "would have" — the debitive adds
inevitability/predetermination, the conditional pure hypothesis.
**Gap:** no source contrasts these two side by side; that line is a
synthesis of each mood's separate description.

Attested paradigm in the Russian-language textbooks too:
`պիտի գրեի / պիտի կարդայի` labeled прошедшее время
долженствовательного наклонения [tioyan p240], and
«ես պիտի նամակ գրեմ» = "Я должен написать письмо" [parnasyan p284].
Sakayan's term is "mandative", Armenian `հարկադրական`
(`grammar-terms.md`).

## Negation — three different patterns

- **Subjunctive past**: plain `չ-` on the verb — `չգրեի`
  (`topics/morphology/subjunctive_mood.md`).
- **Conditional**: `կ-` doesn't survive negation; the pattern switches
  to negated auxiliary + negative participle — `կգրեմ → չեմ գրի`,
  past `չէի գրի` (`topics/morphology/negation.md`).
- **Debitive**: the *particle* is negated — `չպիտի`:
  «Բայց չպիտի հանձնվեմ, պիտի պայքարեմ» "But I should not give up, I
  should fight" [dumtragut p284; rule at dumtragut p282].

Both derived moods also have stative/processual/prospective aspectual
sub-forms with `լինել` — e.g. stative conditional past
«եթե դա հեշտ լիներ, ապա խնդիրը վաղուց լուծված կլիներ» "If that had
been easy, the problem would have been solved long ago"
[dumtragut p279].

## Confidence & gaps

- Conditional/debitive semantics: **well-cited** (Dum-Tragut ch.
  2.5.7.3, corpus pp. 274–288, + tioyan/parnasyan paradigms).
- Subjunctive-past morphology: **single-source** (sakayan p174–175 via
  `topics/morphology/subjunctive_mood.md`).
- The hypothetical/conditional mood and the debitive mood have **no
  dedicated topic files** yet (flagged in `subjunctive_mood.md` gaps);
  this note leans on `armenian-grammar.md` + Dum-Tragut directly.
- The debitive-past vs conditional-past boundary in "averted event"
  readings is **synthesis**, not citation.
- Colloquial reduction of `պիտի` to `pəti/pti`:
  `transliteration-notes.md` § Pitfall 3.

## Provenance

- Retrieval: `frequency/query_kb.py` bundle on
  `պիտի կկարդայի կարդայի պիտի կարդայի եթե`, extended by manual pulls
  of `dumtragut/out/full.jsonl` pp. 274–288 (conditional + debitive
  chapters).
- Verification: `.claude/skills/answer-q/verify_citations.py` — green,
  including dumtragut cites (the script's book-regexes were extended
  with `dumtragut` on 2026-07-12 as part of this session).
