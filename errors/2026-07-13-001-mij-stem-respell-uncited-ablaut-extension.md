---
id: 2026-07-13-001
date: 2026-07-13
caught_by: human
caught_during: tutor-query
severity: critical
disposition: llm-error
category: citation-fabrication
subcategory: provenance-laundered-extrapolation
phenomenon: ja-devoicing-mij-stem
related_topics:
  - topics/phonology/voiced_aspirated_alternation.md
  - topics/phonology/known_transcriptions.md
related_pitfalls:
  - research/2026-06-10-transcription-coverage-and-system.md
status: mitigated
mitigation:
  type: doc-update
  ref: topics/phonology/voiced_aspirated_alternation.md
recurrence: recurrence
---

# միջ- stem respells: uncited extension across an ablaut boundary, provenance-laundered as `sakayan`

Second instance of the `errors/2026-05-09-004` pattern (սով գալ:
uncited member added to a cited family), now in phonology and
with an aggravating factor — the fabricated provenance label.

## Input

The 2026-06 respell-curation passes (root-propagation strategy
per `research/2026-06-10-transcription-coverage-and-system.md`):
extend deck phonetic respells from attested forms to
same-root deck lemmas.

## What the LLM produced

Five rows in `cards/frequency/respellings.tsv` (later also
surfaced in `topics/phonology/known_transcriptions.md` as
"hand-curated" and shipped on live top-1000 cards):

```
միջոց	միչոց		sakayan	միջ- stem (extension of մեջ-)
միջև	միչև		sakayan	միջ- stem
միջին	միչին		sakayan	միջ- stem
միջազգային	միչազգային		sakayan	միջ- stem
անմիջապես	անմիչապես		sakayan	միջ- stem
```

Plus a sixth propagated row `մեջտեղ → [մեչտեղ]` (from sister
մեջք). The **source column says `sakayan`** — but sakayan attests
no միջ- word at all; only the note field admits these are
extensions. Extrapolation wearing an attestation's clothes: any
downstream check that trusts the source column is defeated.

## What was correct

The միջ- stem keeps voiced [dʒ]. Dum-Tragut p43 (book p26) gives
the post-vocalic ջ→[tʃʰ] devoicing as a closed list (աջ, առաջ,
առաջին, մեջ, ոջիլ, քաջք "and their derivations and compounds"),
then: "In all other words it is written as ջ j pronounced as
[dʒ]" — with **միջին [midʒin]** and **միջատ [midʒɑt]** as
explicit examples. Wiktionary's audio for միջոց and running
YouTube speech agree (operator-verified 2026-07-13). For մեջտեղ,
Dum-Tragut p57 transcribes the exact lemma voiced: [mɛdʒtɛʁ].

Counter-evidence exists (parnasyan p398 միջին [мичин],
միջոցառում [мичоцар’ум] — contrastive transliteration, so a
deliberate claim) and is recorded as a doublet, but the modern
reference grammar + audio outrank it. Full matrix:
`research/2026-07-13-mij-stem-devoicing-doublet.md`.

## Why this happened

1. **Pattern completion across a morpheme-shape boundary.** The
   մեջ/մեջք/վերջ-/առաջ- devoicings are real and well-attested;
   the LLM treated "same root" as the propagation unit, but the
   ե→ի ablaut in միջ- is precisely where the lexicalized
   devoicing stops. The rule was lexical-*shape*-level, not
   etymological-root-level — an unvalidated assumption about the
   propagation unit's granularity.
2. **Provenance laundering.** The rows inherited the family's
   source label (`sakayan`) instead of naming their actual basis
   (`sister-propagation from մեջ`). This made the extrapolation
   invisible to every check keyed on the source column, and let
   `known_transcriptions.md` render them alongside genuinely
   attested rows.
3. The 2026-06-14 tier-1 propagation pass *did* test
   counterexamples (rejected այդպես/այդպիսի) — but only within
   tioyan's transliteration coverage. No source covering միջ-
   transliterations was consulted; absence of counter-evidence
   was read as license.

## Mitigation

- **Data fix:** five միջ- rows + մեջտեղ removed from
  `respellings.tsv`; deck rebuilt + validated (2026-07-13).
- **Doc guard:** `voiced_aspirated_alternation.md` § "2026-07-13
  correction" with byte-verified sources [#14]–[#19] (the
  միջին/միջատ counter-anchors make the retraction re-checkable);
  retraction sections in `known_transcriptions.md`.
- **Rule:** a respell needs per-lexeme attestation or propagation
  within an identical surface shape — **an ablaut boundary breaks
  the license**. Provenance columns must name the actual basis,
  never the family's source.
- Not yet mechanical (`status: mitigated`, not `resolved`): no
  validator checks that `respellings.tsv` source labels
  correspond to real attestations. A `validate_deck.py` check
  cross-referencing respell rows against
  `dumtragut/out/ipa_index.tsv` + sakayan TSV annotations would
  upgrade this to `resolved`.

## Test case

Query: "does միջոց devoice (ջ→չ)?" — expected answer: **no**,
voiced [dʒ] per dumtragut p43 (միջին [midʒin], միջատ [midʒɑt] in
the "all other words" class); parnasyan p398 [мнчои]/[мичоцар'ум]
noted as a conflicting older-norm doublet, not followed. A deck
card for միջոց/միջև/միջազգային/անմիջապես must carry **no**
bracket respell. Regression signal: any future propagation pass
re-adding a միջ- respell without new per-lexeme evidence.

*(Amended 2026-07-15: միջին acquired exactly such per-lexeme
evidence — operator audio, devoiced — and was restored with
honest provenance; see `errors/2026-07-15-001`. The regression
signal stands for the remaining four lemmas.)*
