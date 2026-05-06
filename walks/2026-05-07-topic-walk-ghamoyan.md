# Topic walk: ghamoyan against existing topics

**Date**: 2026-05-07
**Operator**: Claude Code, manual walk (no `topic-walk` skill yet)
**Status**: executed; merge into `topics/` follows in the same session.

## Summary

Read ghamoyan's Chapter 2 (phonology, pp. 35-40) and Chapter 4 (grammar,
pp. 70-91). Each existing topic gets at least one new ghamoyan source.
All four topics flip from `single-source` → `multi-attested`.

The framing for each: ghamoyan is *descriptive of colloquial*, Sakayan
is *prescriptive of literary*. Where ghamoyan addresses the same
phenomenon Sakayan does, it almost always extends the picture rather
than contradicting it. Hence `multi-attested` rather than `conflicting`
for all four — but each topic gains a body section explicitly framed
around the literary-vs-colloquial contrast that the multi-book setup is
*for*.

## Per-topic proposals

### topics/phonology/voiced_aspirated_alternation.md

**Add source #5**: ghamoyan p39, y_range [215, 260].

> "Երևանի խոսակցական լեզվին հատուկ են նաև բաղաձայնների արտասանական
> որոշ տեղաշարժերը, հատկապես առանձին բարբառների և խոսվածքների
> ազդեցության հետևանքով (**ձայնեղների շնչեղացում, խլացում և
> հակառակը**)."

Translation: "Yerevan colloquial language also features certain
articulatory shifts of consonants, especially under the influence of
individual dialects and idioms (**aspiration of voiced consonants,
devoicing, and the reverse**)."

Examples ghamoyan gives (literary–colloquial pairs):
`ընկեր-ընգեր, ընկնել-ընգնել, հանկարծ-հանգարծ, գդալ-քթալ, գտնել-քթնել,
գցել-քցել, ...`

**Significance for the topic**:

- ghamoyan's phenomenon is *bidirectional* and *dialect-attributed*,
  whereas Sakayan presents only the voiced→aspirated direction as
  lexically irregular.
- Examples like `ընկեր→ընգեր` (k→g, voiceless→voiced) are *opposite*
  direction from Sakayan's `ընդունել→ընթունել` (d→tʰ,
  voiced→aspirated).
- ghamoyan attributes the shifts to "individual dialects and idioms"
  — a typological framing Sakayan doesn't offer.

**Body delta**: add a section "## Wider scope in colloquial speech
(Ghamoyan)" between the existing "## Observed alternation pairs" and
"## What the alternation is *not*", explaining the bidirectional /
dialect-attributed framing.

**Attestation**: `single-source` → `multi-attested`.

**Gap update**: resolve the third gap ("Cross-dialectal status —
whether Yerevan colloquial preserves the three-way contrast or has
begun shifting…") — partially answered: the contrast is preserved as
a system, but lexeme membership shifts.

---

### topics/phonology/three_way_laryngeal_contrast.md

**Add source #4**: ghamoyan p39, y_range [215, 260] (same passage).

**Significance for the topic**:

- Directly addresses the third frontmatter gap: "Cross-dialectal
  status — does Yerevan colloquial preserve the three-way contrast,
  or has it shifted?"
- Answer (per ghamoyan): the *system* of three series persists; the
  *membership* of specific lexemes shifts under dialect influence
  (both voiced↔aspirated and voiced↔voiceless directions).

**Body delta**: add a section "## Cross-dialectal status: Yerevan
colloquial (Ghamoyan)" replacing the placeholder gap, noting that
ghamoyan documents preservation-of-system + lexical drift.

**Attestation**: `single-source` → `multi-attested`.

---

### topics/syntax/pro_drop.md

**Add source #3**: ghamoyan p79, y_range [305, 380].

> "Խոսակցական լեզվին բնորոշ են նախադասության անդամների **զեղչման
> բոլոր տիպերը**` և՛ ենթական, և՛ ստորոգյալը, և՛ մյուս լրացումները:"

Translation: "Colloquial language features **all types of
sentence-member elision**: subject, predicate, and other complements."

Examples:

- `Ես առավոտյան էլի գործի եմ գնալու` (I'm going to work again
  tomorrow morning) → `Առավոտը էլի գործի` (subject + predicate
  elided).
- `Ես հիմար եմ, դու խելացի ես` (I'm stupid, you're smart) →
  `Ես՝ հիմար, դու՝ խելացի` (auxiliary elided).

**Add source #4**: ghamoyan p80, y_range [40, 80].

> "Խոսակցական լեզվին բնորոշ են **անհանգույց ստորոգյալով**
> նախադասությունները: Օրինակ՝ Դու` խենթ ու խելառ:"

Translation: "Colloquial language features sentences with
**unlinked predicates [zero-copula]**. Example: Դու` խենթ ու խելառ
('You [are] crazy and silly')."

**Significance for the topic**:

- ghamoyan extends pro-drop *generalised to all sentence members*.
- Sakayan: subject pronouns are redundant *because the auxiliary
  carries person/number*.
- Ghamoyan: predicate, complements, **and the auxiliary itself** can
  also be dropped in Yerevan colloquial.
- Plus zero-copula in Yerevan colloquial — directly addresses the
  topic's first gap ("Information-structural conditions").

**Body delta**: add section "## Yerevan colloquial: elision beyond
the subject (Ghamoyan)" explaining the broader picture.

**Attestation**: `single-source` → `multi-attested`.

**Gap update**: partially resolve gap 1 (information-structural
conditions on overt pronouns).

---

### topics/morphology/present_tense.md

**Add source #5**: ghamoyan p73, y_range [290, 340].

> "Ժողովրդախոսակցական լեզվում բաղադրյալ ստորոգյալի երրորդ դեմքի
> հետ իբրև հանգույց կիրառվում է **ա-ն**, ինչպես` մեծ ա, լավն ա,
> կանաչ ա, **պարզ ստորոգյալում ա-ն փոխարինում է է օժանդակ բային**,
> ինչպես` գրում ա, գալիս ա, ուտում ա..."

Translation: "In folk-colloquial language, **`ա` is used as a linker
[copula]** in the third person of compound predicates: `մեծ ա` ('is
big'), `լավն ա` ('is good'), `կանաչ ա` ('is green'). **In simple
predicates, `ա` replaces the auxiliary `է`**: `գրում ա`, `գալիս ա`,
`ուտում ա`."

**Significance for the topic**:

- Direct answer to the topic's first gap: "Auxiliary positioning in
  colloquial speech — ghamoyan may document where the auxiliary
  attaches differently from Sakayan's canonical postposed form."
- ghamoyan's answer: not a positioning shift, but a **morphological
  substitution** — 3sg `է` → `ա` in colloquial Yerevan, applies both
  to copular `է` (compound predicates) and to auxiliary `է`
  (analytic verb forms like `գրում է`).
- Pattern is ubiquitous (`գրում ա`, `գալիս ա`, `ուտում ա`) — should
  be common in any natural Yerevan-Armenian dialogue.

**Body delta**: add a section "## Yerevan colloquial: 3sg auxiliary
`ա` for `է` (Ghamoyan)" with examples.

**Attestation**: `single-source` → `multi-attested`.

**Gap update**: resolve gap 1 (auxiliary positioning) with the
substitution finding.

---

## Side-discoveries (for the discovery-walk plan)

While reading the chapters above, multiple unrelated phenomena
surfaced that aren't yet in `topics/`. These are queued for the
discovery walk — see `walks/2026-05-07-discovery-walk-ghamoyan.md`.

## What this walk did *not* address

- Discovery of phenomena not in `topics/` — separate walk.
- Lexical-doublet harvesting — Phase 3 of the integration plan.
- Cross-checking ghamoyan's examples against Sakayan's vocab list to
  see which words have a literary↔colloquial doublet attested in
  both books — also Phase 3.

## Verification protocol after merge

1. `citation-check` on each of the four updated topic files.
2. `critic-pass/lint.py` on each of the four.
3. Manual review of body deltas for clarity / arc consistency.
