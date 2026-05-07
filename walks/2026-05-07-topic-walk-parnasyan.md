# Topic walk: parnasyan against existing 6 topics

**Date**: 2026-05-07
**Operator**: Claude Code, manual walk (no `topic-walk` skill yet).
**Source**: `parnasyan/out/full.jsonl` (430 OCR'd book pages, avg
confidence 80.1).

## Summary

Read the parnasyan extraction's grammar chapters (pp. 21-50) and
spot-checked the rest. Three topics get new Parnasyan sources; three
do not. The pattern is asymmetric: Parnasyan is a Russian-L1
prescriptive textbook of the literary norm, so it directly addresses
phonology, present tense, and pro-drop with explicit Russian
contrasts — but it does not discuss the colloquial / dialectal
phenomena (voiced↔aspirated lexical alternation, Yerevan reductions,
copula `ա`).

The biggest win: the **Russian-L1 contrastive notes** that currently
appear as agent-paraphrased prose in three topic files become
**book-cited**. Parnasyan repeats "В отличие от русского..." across
multiple chapters, with passages directly answering the project's
existing contrastive framings.

## Per-topic proposals

### topics/phonology/three_way_laryngeal_contrast.md

**Add source #5**: parnasyan p21, y_range [4140, 5300].

Verbatim quotes (Russian):

> "Система согласных армянского языка отличается от русского
> наличием:
> 1) аффрикат…
> 2) глухих придыхательных…
> 3) заднеязычного звонкого согласного գ…
> 4) гортанного придыхательного հ…
> 5) отсутствием противопоставления согласных по
> твердости—мягкости. Армянские согласные произносятся твердо и
> почти не смягчаются."

Significance: explicit Russian-contrastive enumeration of how the
Armenian consonant system differs from Russian's. Specifically
flags:
- Three-way affricate distinction (Russian has only ц/ч)
- **Aspirated voiceless row** — Russian has no aspiration distinction
- Voiced velar գ — different from Russian
- **No palatalisation contrast** — Armenian doesn't have hard/soft

This converts the Russian-L1 contrastive section in the topic from
agent-paraphrased to directly book-cited.

**Body delta**: append `[#5]` references in the "For a Russian L1"
paragraph; no other prose changes.

**Attestation**: stays `multi-attested` (still multi-source; just
goes from 2 books to 3).

### topics/morphology/present_tense.md

**Add source #6**: parnasyan p30 y_range [2830, 6010] — the
"ВСПОМОГАТЕЛЬНЫЙ ГЛАГОЛ" section header and the full auxiliary
paradigm.

**Add source #7**: parnasyan p31 y_range [460, 1100] — three explicit
Russian contrasts about the auxiliary, including "армянский
вспомогательный глагол է имеет формы настоящего времени" (Armenian
aux *has* present-tense forms — Russian's зеро-copula doesn't) and
"не имеет родового различия" (past tense aux doesn't distinguish
gender).

**Add source #8**: parnasyan p32 y_range [100, 600] —
"в армянском языке, в отличие от русского, связка всегда
присутствует" (in Armenian, unlike Russian, the copula is always
present). The literary-norm baseline against which Yerevan
colloquial's zero-copula deviation (already cited from ghamoyan)
becomes a sharp register tell.

Significance: corroborates Sakayan's literary-norm paradigm with
two independent Russian-language sources, and converts the existing
Russian-L1 contrastive note to book-cited. Also makes the literary
vs colloquial copula contrast attestable from both sides — sakayan
+ parnasyan (literary, copula required) vs ghamoyan (colloquial,
copula often dropped).

**Body delta**: append `[#6 #7 #8]` references in the Russian-L1
contrastive paragraph; nothing else.

**Attestation**: stays `multi-attested`.

### topics/syntax/pro_drop.md

**Add source #5**: parnasyan p49 y_range [800, 1600] — the explicit
pro-drop claim in Russian:

> "Так как в армянском языке глагол-сказуемое всегда указывает на
> действующее лицо (как в настоящем, будущем, так и прошедшем
> времени), то подлежащее при глаголе в первом и втором лицах
> может быть опущено и в прошедшем времени (в отличие от русского
> языка)."

Translation: "Since the predicate-verb in Armenian always indicates
the doer (in present, future, and past tense), the subject with the
verb in 1st and 2nd person can be omitted **even in the past tense**
(unlike Russian)."

Significance: the *exact* claim that's been agent-paraphrased in the
topic's Russian-L1 contrastive note. The 1st/2nd-person past-tense
asymmetry is the precise wedge between Armenian (consistent
pro-drop) and Russian (partial pro-drop) — Russian past tense
doesn't carry person, so it can't drop the subject; Armenian past
tense *does* carry person, so it can.

**Add source #6** (optional): parnasyan p46 y_range [3880, 4200] —
"`նա` не различается по родам и соответствует русским местоимениям
он, она, оно" — the gender-neutral 3sg pronoun. Indirectly
relevant to pro-drop because it shows that 3sg doesn't gain the
disambiguation Russian gets from gender. Skip for now if we want to
keep the topic focused.

**Body delta**: convert the Russian-L1 section from
agent-paraphrased to book-cited via `[#5]` references.

**Attestation**: stays `multi-attested`.

## Topics with no Parnasyan additions

### topics/phonology/voiced_aspirated_alternation.md

Parnasyan describes the literary-norm three-way contrast (cited from
the same p21 passage above for `three_way_laryngeal_contrast`) but
**does not discuss the lexical alternation** Sakayan documents.
Adding the same p21 source here would be redundant with the parent
topic; the alternation is the pedagogically *abnormal* phenomenon
that prescriptive textbooks like Parnasyan don't dwell on.

No change. `attestation` stays `multi-attested` (sakayan + ghamoyan).

### topics/morphology/colloquial_copula_a.md

Pure colloquial phenomenon. Parnasyan teaches strict literary `է`;
the substitution `ա` is precisely what a prescriptive textbook
treats as a deviation, so it isn't covered.

No change. `attestation` stays `single-source` (ghamoyan).

But: Parnasyan's p32 "связка всегда присутствует" claim (now cited
from `present_tense.md`) is the *literary-norm baseline* against
which `ա`-substitution is the colloquial deviation. The
`present_tense.md` body section already makes this contrast
explicit; no need to duplicate here.

### topics/phonology/yerevan_consonant_reductions.md

Pure colloquial phenomenon. Parnasyan teaches the literary norm
without the consonant elisions ghamoyan catalogues.

No change. `attestation` stays `single-source` (ghamoyan).

## Side-discoveries (queue for discovery walk)

While reading parnasyan's chapters, multiple Russian-L1-relevant
phenomena surfaced that would be worth their own topics:

- **No palatalisation contrast** in Armenian (Parnasyan p21, point
  5). Direct Russian contrast — Russian L1 must learn that Armenian
  consonants don't palatalise before front vowels. Single-source
  parnasyan, very citable.
- **Auxiliary verb `է` always carries person** even in past tense
  (Parnasyan p31, point 1) — the structural reason for consistent
  pro-drop. Could be folded into `topics/morphology/auxiliary_e.md`.
- **The accusative-of-direction** for inanimate destinations:
  "обстоятельство места, показывающее направление, ставится в вин.
  п." (Parnasyan p41 footnote). Russian uses prepositions for this;
  Armenian uses the case ending. Worth a topic if/when case is
  added.
- **Determinate article `-ը/-ն` distribution**: Parnasyan p45
  "В отличие от русского, в армянском языке определенность—
  неопределенность выражается артиклем". Russian has no articles;
  Armenian has them. Already partly in `armenian-grammar.md` but
  not yet a topic file.
- **3sg gender-neutral pronoun `նա`** (Parnasyan p46) — direct
  Russian contrast, already covered as a "skip for now" option in
  pro_drop.md.

These are queued for the discovery-walk pass when more parnasyan
content is mined. Output: extend
`walks/2026-05-07-discovery-walk-ghamoyan.md` or write a sibling
discovery-walk-russian-sources.md.

## Verification protocol

After merging sources into the three topic files:

1. `citation-check` on each updated topic — confirms verbatim
   quotes verify against parnasyan/out/full.jsonl.
2. `critic-pass/lint.py` on all 6 topics — confirms structural
   integrity.
3. Spot-check OCR quality on cited spans by rendering the page PNG
   and visually confirming the Russian text matches what the OCR
   produced.

## OCR caveats

- Russian-language fragments OCR cleanly (90%+ confidence on the
  spans cited above).
- Armenian-script fragments in parnasyan show typical
  voiced-stop confusions (գ↔դ, etc.) — the same OCR errors visible
  in the dictionary section. Avoid citing Armenian-script fragments
  from parnasyan when a Russian-language paraphrase is available.
- The book has many "В отличие от русского..." passages (5+ found
  in spot-grep across the book). These are easy to harvest because
  they all start with the same recognisable prefix.
