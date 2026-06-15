# cards/ — change log

Dated record of substantive deck changes: what was fixed, **why**, the
grounding evidence, and where the guard lives. Companion to `README.md`
(layout) and `REQUIREMENTS.md` (intent). The deck itself is generated —
fixes live in `../frequency/build_deck.py` (`HAND_OVERRIDES`,
`SKIP_LEMMAS`, `PHONETIC_OVERRIDES`) and are guarded by
`../frequency/golden_glosses.tsv`; this file is the human-readable
narrative of *why each entry is there*.

Convention: newest entry on top. Every fix follows the two-step rule
(fix the case **and** add a guard). Record **walked-back** items too —
so a future pass doesn't "re-fix" a gloss that grounding already
vindicated.

---

## 2026-06-14 — new deck: `top_1000_ru.tsv` (Russian-only, ≤2-word)

A parallel **minimal** deck: same 1095 Armenian fronts (lemma + phonetic
respell reused verbatim from `top_1000.tsv`), but the back is a
**Russian-only gloss of at most 2 words** — the single most useful
sense. Follows the **Minimum Information Principle** (Wozniak, *20 Rules
of Formulating Knowledge*, Rule 4: atomic cards). Tag: `frequency
ru-minimal`. Russian is a prior/translation layer (not corpus-cited),
which the spec explicitly permits.

Built by a two-phase subagent fan-out (`ru-minimal-deck` workflow):

1. **Collapse** (15 batch subagents) — each pulls a lemma's multiple
   English/Russian senses and reduces to ≤2 Cyrillic words: dominant
   sense only, examples/grammar-labels/register-notes dropped; verbs →
   infinitive; cardinals → digit (`1`, `20`, `1000`); ordinals →
   Russian word (`первый`, `пятый`).
2. **Validate** (15 batch subagents) — checked Cyrillic-only, ≤2 tokens,
   non-empty, sense-correct; auto-fixed 12 (e.g. `չէիր` "ты не был" →
   "не был"; `նկատի ունենալ` "иметь в виду" → "подразумевать"; `առ`
   "грабить" → "возьми").

Post-assembly deterministic check: 0 empty / 0 Latin-leak / 0 Armenian-
leak / 0 over-2-words across 1095 rows. Then an **independent editorial
subagent** (native-Russian-learner framing) spot-checked ~55 cards; its
⚠ wrong-sense findings were applied:

| Lemma | was | → | note |
|-------|-----|---|------|
| `թերթ` | лепесток | газета | "petal" was the rare sense; dominant = newspaper/sheet |
| `այգի` | виноградник | сад | garden is primary; vineyard is the archaic sense |
| `ճանաչում` | распознавание | признание | recognition = acknowledgment, not pattern-recognition |
| `խորթ` | чужой | неродной | the salient sense is "step-/unrelated" |
| `կախվել` | висеть | повиснуть | intransitive change-of-state, not stative |
| `հոր` | отцовский | отца | genitive of `հայր` (noun), not an adjective |
| `թև` | рука | рука, крыло | arm + wing (бare "рука" collided with `ձեռք`) |
| `հեր` | волос | волосы | "hair" → plural, consistent with `մազ` → волосы |
| `խնդիր` | просьба | задача | corpus says problem/task; "request" is the EN deck's known-wrong lead |

**Known inheritance caveat.** The Russian deck mirrors `top_1000.tsv`,
so it inherits that deck's English sense choices. Several ⚠ above
(`թերթ`, `այգի`, `խնդիր`, `ճանաչում`) are *also* latent in the English
deck (kaikki rare-sense leads). Fixing them there (HAND_OVERRIDE) is the
proper two-step; not done this session — tracked as a follow-up.

---

## 2026-06-14 — agent-driven editorial review ("Anahit" critic) + grounding

A spec-aware critic persona ("Anahit": Eastern-Armenian tutor holding
the eight `REQUIREMENTS.md` gloss rules in mind) was fanned across the
whole deck in two framings (structural + editorial). Every sense /
phonology finding was then **grounded** before action — via
`frequency/query_kb.py` (corpus + topic graph) and, for the legal
idiom, the web (Wiktionary/nayiri). Structural/byte findings held at
100%; ~26% of the prior-based linguistic findings were wrong or
overstated and were walked back. This is the canonical demonstration of
the repo's grep-first discipline: the critic produces adversarial test
data, grounding decides.

Guards: 13 new `golden_glosses.tsv` anchors; 6 `SKIP_LEMMAS`; 13
`HAND_OVERRIDES` (12 added + 1 edited). Validator: **0 errors** at each
round. Deck size 1097 → 1095.

### Round 1 — confirmed sense/POS errors (kaikki shipped wrong homograph / dictionary-prose)

| Lemma | Was | Fixed to | Grounding |
|-------|-----|----------|-----------|
| `վախ` | "an exclamation of pain or grief" | fear / страх | `topics/morphology/verbal_nouns.md` (վախենալ→վախ "fear") |
| `հոլով` | "much, plenty, numerous" | grammatical case, declension / падеж | `grammar-terms.md` "Հոլով / Падеж"; `accusative_for_locative.md` |
| `անկաշկանդ` | "unfastened, unsealed, untied" | uninhibited, free, at ease / непринуждённый, свободный | ghamoyan (paired with ազատ/անկախ) |
| `ափսոս` | "pitiable" | what a pity!, too bad / жаль, как жаль | parnasyan p76 glosses it «(выражение …» (an exclamation) |
| `փակ` | "close" (verb) | closed, shut / закрытый | `topics/lexicon/idioms_phrasal.md` «ձեռքը փակ» |
| `քար` | "hard, strong, solid" | stone, rock / камень | sakayan p91 proverb «Սոված մարդը քարից փափուկը կուտի» |
| `հաստատություն` | "firmness, sturdiness, hardness" | institution, establishment / учреждение | ghamoyan «ուսումնական հաստատություններ» |
| `անհատ` | "singular, unique" | individual / личность, индивид | sakayan p448 «մեծ անհատները» |
| `անցնել` | "to surpass" | to pass, cross, go by / проходить, переходить | sakayan p400 «սահմանն անցնելիս»; "surpass" unattested |
| `կինո` | "cinematography, filmmaking" | cinema, the movies; film / кино, кинотеатр | sakayan p131 «կինոնկար» (film) |
| `ոսկի` | "gold *(en)*" | gold / золото | stray `(en)` annotation leak |
| `հայրիկ` | "diminutive of հայր : dad, daddy" | dad, daddy / папа, папочка | dictionary-prose (REQUIREMENTS §3 bans it) |
| `ուսումնական` | "academic, school *(related)*" | academic, school / учебный, школьный | stray `(related)` in an existing override |

Removed as noise / inflected-of-deck-lemma (`SKIP_LEMMAS`):

| Lemma | Why | Grounding |
|-------|-----|-----------|
| `մեկին` | dat/acc of `մեկ` "one" (on deck); kaikki's "clear, explained" is the wrong homograph | sakayan p147 «մեկին, երկուսին» |
| `յան` | the patronymic surname suffix `-յան`, not a word ("side") | corpus has only Սարյան/Ազարյան |
| `ար` | tokenizer noise; kaikki glossed the English fragment "are" | 0 standalone corpus hits |
| `յա` | tokenizer noise / colloquial tag particle; kaikki glossed "or" (=կամ) | 0 standalone corpus hits |

### Round 1 — WALKED BACK (do NOT "re-fix" — grounding vindicated the original)

| Item | Critic claim | Why left as-is |
|------|--------------|----------------|
| `անգամ [անքամ]` | "wrong respell — post-nasal գ isn't devoiced" | **Correct respell** — it's Sakayan's own transliteration; `topics/phonology/known_transcriptions.md` documents `անգամ \| [անքամ] \| գ→ք`. EArm devoicing is *lexical*, not environment-conditioned. |
| `մեծանալ` "to grow older" | "wrong → should be grow up" | This is **Sakayan's own vocab gloss** (`cards/sakayan/unit5_vocab`). Not an error. |
| `ինչպիսի` "what a…!" | "wrong primary sense" | The exclamative is **corpus-frequent** (sakayan p73/p89 «Ինչպիսի՛ գեղեցկություն»). Not wrong. |
| `պատմություն` "story" | "missing history" | "story" is **corpus-attested** (p223, p241). Adding "history" is optional, not a blocker. |
| `ալ` / `ան` | "homograph-trap noise, skip" | Intentionally **labeled W. Armenian/dialectal** on the card. Not unflagged noise. |

### Round 2 — latent items surfaced by the verification pass, then grounded

| Lemma | Action | Grounding |
|-------|--------|-----------|
| `կեր` | sense fix → "(animal) feed, fodder; eat! (imperative of ուտել) / корм; ешь!" (was the too-generic "food, nourishment" that also hid the imperative homograph) | ghamoyan dict «կեր … сущ. пища, корм»; sakayan imperative «կեր/կերե՛ք» |
| `բերում` | removed (`SKIP_LEMMAS`) | present converb of `բերել` "to bring" (on deck); `irregular_verbs.md` «բերել → բերում եմ», sakayan p354 — same class as the documented `գնում` trap |
| `հան` | removed (`SKIP_LEMMAS`) | kaikki's "grandma" gloss has **zero corpus support**; the token is the imperative of `հանել` (on deck) + the name fragment Հանս |

Rebuild after the skips pulled 4 legitimate words into the cutoff
(`թեյ`, `հարսանիք`, `հոգի`, `շարժում`) — all clean.

### Round 3 — `դատ բանալ` "to sue" (web-grounded; corrected my own earlier proposal)

The phrasal `դատ բանալ` "to file a lawsuit" was not the everyday form,
but the round-1 *proposed* fix `դատ տալ` turned out to mean something
else. Web/dictionary grounding resolved it:

- `դատի տալ` (gen. `դատի` + `տալ`) = **"to sue"** — Wiktionary modern entry. ✅ applied.
- `դատ տալ` = "to condemn **oneself**, be condemned" — would have been a *new* error.
- `դատ բանալ` = "open/initiate a case" — literary, attested but not the learner form.

Fix: `cards/frequency/phrasal_verbs.tsv` `դատ բանալ` → `դատի տալ`
"to sue, to take to court / подать в суд"; golden anchor swapped
(`դատ բանալ` anchor removed, `դատի տալ` added). Sources: Wiktionary
`դատ`, bararan.am, nayiri.com.

### Still parked

- `հանել` "take off" — known, separately-tracked narrowness (corpus
  also supports "take out, remove, subtract"); not changed this session.
