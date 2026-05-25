---
id: 2026-05-14-002
date: 2026-05-14
caught_by: human
caught_during: drafting
severity: minor
disposition: llm-error
category: language-understanding
subcategory: spurious-morpheme-decomposition
phenomenon: armenian-borrowed-toponym-stem-ending
related_topics:
  - topics/morphology/accusative_for_locative.md
related_pitfalls:
  - errors/2026-05-14-001-self-falsifying-illustrative-example.md
  - errors/2026-05-11-001-currency-exchange-case-frame.md
  - errors/2026-05-09-004-sov-gal-uncited-extrapolation.md
status: mitigated
mitigation:
  type: doc-update
  ref: topics/morphology/accusative_for_locative.md
recurrence: pattern-of-N
---

## Input

While drafting `topics/morphology/accusative_for_locative.md`
(2026-05-14 session), the LLM analysed ghamoyan p87's two examples
of accusative-for-locative case substitution:

1. `Ես Երևան եմ ապրում` "I live in Yerevan" (bare `Երևան`).
2. `Էս տարի Քոբուլեթի հանգստացա` "This year I vacationed in
   Kobuleti" (`Քոբուլեթի` with apparent `-ի` ending).

Ghamoyan grouped both under "հայցական ներգոյականի փոխարեն" —
"accusative used in place of the locative."

## What the LLM produced

The LLM analysed the morphology of `Քոբուլեթի` as:

> stem `Քոբուլեթ` + suffix `-ի` (gen/dat ending)

And concluded: "this doesn't match Ghamoyan's 'accusative' label,
since the formal accusative of `Քոբուլեթ` would be bare `Քոբուլեթ`
(for inanimate nouns, ACC = NOM = bare stem)." The LLM flagged the
mismatch as a *puzzle* in the topic file's frontmatter and gaps,
listing three speculative readings:

1. Ghamoyan uses "accusative" loosely as a cover term.
2. Georgian place names licence a different reduction pattern.
3. OCR error.

This puzzle was surfaced in the body of the topic file and
documented in the gaps list.

## What was correct

Kobuleti is a Georgian seaside town — Georgian `ქობულეთი`. The
final `-ი` in Georgian is the **nominative suffix** that attaches
to most Georgian common and proper nouns. When Georgian toponyms
are borrowed into Armenian, the final `-ი` is preserved as
Armenian `-ի`:

| Georgian | Armenian | English |
|---|---|---|
| თბილისი | Թբիլիսի | Tbilisi |
| ბათუმი | Բաթումի | Batumi |
| ქუთაისი | Քութայիսի | Kutaisi |
| ქობულეթი | Քոբուլեթի | Kobuleti |

So the **bare / nominative form** of the Armenian-borrowed toponym
*is* `Քոբուլեթի`. The `-ի` is **stem-final**, not a case ending.
For inanimate nouns, accusative = nominative, so the accusative is
also `Քոբուլեթի`.

Ghamoyan's "accusative" label is therefore **correct**. Both his
examples instantiate the same reduction:

| | colloquial | literary | gloss |
|---|---|---|---|
| Yerevan | `Երևան եմ ապրում` | `Երևանում եմ ապրում` | "I live in Yerevan" |
| Kobuleti | `Քոբուլեթի հանգստացա` | `Քոբուլեթիում հանգստացա` | "I vacationed in Kobuleti" |

Both drop the locative `-ում`. The only difference is whether the
bare stem ends in a consonant (`Երևան`) or a vowel (`Քոբուլեթի`).
No puzzle, no mismatch.

## Why this happened

The failure is **spurious morpheme decomposition**: the LLM saw a
familiar-looking suffix shape at the end of a word
(`-ի` = Armenian gen/dat) and assumed a morpheme boundary
without checking the stem inventory.

The decomposition `Քոբուլեթ + ի` was treated as if it were the
only reading. The alternative — that `Քոբուլեթի` is itself the
stem, inherited intact from Georgian — was not considered.

The one-line check that would have caught the error:
**"what is the Armenian nominative form of Kobuleti?"** A quick
mental check against the parallel `Թբիլիսի` (well-known Armenian
form of Tbilisi, with `-ի`) would have flagged the assumption
immediately.

The LLM also had access to corpus passages that would have
disambiguated. Quick grep for `Թբիլիսի` or `Բաթումի` in the
corpus would have shown vowel-final stems on Georgian-borrowed
toponyms. But the check wasn't run.

## Pattern membership

This is the **fourth recurrence in this workspace** of the broader
"structural assumption made without verification" failure family:

1. **2026-05-09-004 (sov-gal)**: paradigm extended to uncited
   member without checking attestation.
2. **2026-05-11-001 (currency-exchange)**: case-frame asserted
   without checking the verb's argument structure.
3. **2026-05-14-001 (self-falsifying example)**: illustrative
   example produced without checking it instantiates the claim
   (and the case-shift it should have shown).
4. **This entry (2026-05-14-002)**: morpheme boundary asserted
   without checking the stem inventory.

### Fifth recurrence, same session: author-gender assumption

Within ~10 minutes of logging this entry, a fifth instance of the
same family surfaced. The LLM had been referring to the ghamoyan
authors with masculine singular pronouns ("Ghamoyan himself uses
the literary form...") throughout the session, including in the
topic file produced just before this error was logged.

User prompted: *"also is ghamoyan a man?"*

Check: `ghamoyan/manifest.yaml` lists three authors —
**Լուսինե Ղամոյան** (Lusine Ghamoyan), **Մերի Սարգսյան** (Meri
Sargsyan), **Անահիտ Քարտաշյան** (Anahit Kartashyan). All three
given names are feminine Armenian names. The work is a collective
authored by three women, not a single male author.

The structural assumption was: "Armenian surname `Ghamoyan` →
default to masculine singular pronoun." Cross-linguistically, this
imports a habit from gender-marking surname systems (Russian
`-ов / -ова`) onto a non-gender-marking one (Armenian `-յան`
applies to both men and women). The given name `Լուսինե` was
sitting in the manifest file the LLM had read; the check was
trivial.

The fix-framing also has to be sharper than "Armenian doesn't
gender-mark." Armenian has *no grammatical gender* (no agreement
on adjectives, verbs, pronouns) but **does have lexical /
derivational gender** on human-referent nouns and names:
- `-ուհի` suffix derives feminine agent nouns: `ուսուցչուհի`
  "female teacher", `հայուհի` "Armenian woman", `Արմենուհի`
  (F given name from M `Արմեն`).
- Given names are gender-marked: `Լուսինե`, `Մերի`, `Անահիտ` are
  all feminine; `Արմեն`, `Հովհաննես` are masculine.
- Inherent-gender pairs: `տղամարդ / կին`, `հայր / մայր`,
  `պարոն / տիկին`.

So the check that would have caught the error wasn't "do
Armenian surnames carry gender" (no) — it was "does the **given
name** carry gender" (yes). The information was sitting in the
manifest's `authors:` field; the LLM read the surname and skipped
the given name.

Fix: topic file updated to use "the Ghamoyan authors themselves"
in place of "Ghamoyan himself" — both correcting the gender
default and acknowledging the three-author nature of the work.

Updates the pattern-of-N count to **five within the workspace,
two within today's session**. The recurring shape stays the same:
running a structural inference without the cheapest possible
baseline check. The cross-domain spread now spans paradigm
extension, verb argument-structure, example-construction,
morpheme decomposition, and author identification.

Each instance has its own surface shape, but the core failure is
identical: **proposing a structural analysis without running the
cheapest possible verification of its baseline assumption.**

That this is the *second* such error logged within the same
session is itself notable — the discipline-rule named in
2026-05-14-001 ("vary one axis at a time and verify the baseline
before extending") didn't generalise to a different decomposition
task that called for the same kind of baseline check. The
abstraction has to be re-stated in language that catches all four
cases:

> **Before asserting a structural analysis, run the cheapest
> possible check on the baseline assumption the analysis rests on
> — even if (especially if) the assumption feels obvious.**

For morphological parsing specifically: when decomposing a word
into stem + ending, **verify the bare nominative form of the stem**
before treating the apparent ending as a case marker.

## Mitigation

Immediate:

- The topic file `topics/morphology/accusative_for_locative.md` was
  rewritten to incorporate the resolved reading. The body's
  inline caveat now explains the Georgian-stem origin of `-ի` and
  concludes that ghamoyan's "accusative" label is correct.
- The gaps list entry that flagged the puzzle was replaced with a
  sharper open question about phonological-shape coverage (do
  other vowel-final stems show the same productive reduction?).

Durable:

- This entry. Marking `recurrence: pattern-of-N` (fourth instance
  of the broader family).
- The discipline-rule restated above ("cheapest baseline check
  before structural assertion") is now stated as a generalisation
  across morphology / verb-frame / case-marking / example-
  construction.

## Test case

Future LLM prompt:

> "Analyse the Armenian word `<vowel-final borrowed toponym>` for
> its morphological structure."

Expected behaviour:

- Identify the source language and check whether the final vowel
  is stem-final (inherited from the source) or a case ending.
- For Georgian-borrowed toponyms ending in `-ի`: recognise that
  Georgian nominative `-ი → -ի` is preserved as stem-final.
- For Armenian-native nouns ending in `-ի`: recognise that `-ի`
  may be gen/dat, in which case the stem is the consonant-final
  preceding form.

Failure mode: assuming the apparent suffix is a case marker
without checking the source-language morphology or the bare
nominative.

## Notes

- The error was caught at drafting time by user prompt ("this is
  a georgian town"). Topic file was updated within the same
  session; no propagation downstream. Severity: minor.
- The resolution actually *improved* the topic file: a flagged
  "puzzle" became a clean second example, and the gaps list now
  contains a sharper falsifiable question (phonological-shape
  coverage of the reduction) rather than a speculative
  three-way alternative.
- Re-run `.claude/skills/error-log/` once committed so
  `errors/INDEX.md` and `errors/BY-CATEGORY.md` regenerate.
