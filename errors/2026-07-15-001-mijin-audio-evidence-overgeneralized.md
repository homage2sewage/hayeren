---
id: 2026-07-15-001
date: 2026-07-15
caught_by: human
caught_during: tutor-query
severity: major
disposition: llm-error
category: confidence-miscalibration
subcategory: evidence-scope-overgeneralization
phenomenon: ja-devoicing-mij-stem
related_topics:
  - topics/phonology/voiced_aspirated_alternation.md
  - topics/phonology/known_transcriptions.md
related_pitfalls:
  - errors/2026-07-13-001-mij-stem-respell-uncited-ablaut-extension.md
status: mitigated
mitigation:
  type: doc-update
  ref: research/2026-07-13-mij-stem-devoicing-doublet.md
recurrence: recurrence
---

# միջին kept voiced on միջոց's audio evidence: verification generalized across lemmas

Follow-on to `errors/2026-07-13-001`, one level up: that entry
fixed respell rows extended beyond their citations; this one is
the *retraction itself* extending **verification evidence**
beyond the lemma it covered.

## Input

The 2026-07-13 retraction pass. Operator audio evidence existed
for **միջոց only** (Wiktionary audio, YouTube shorts). The
evidence matrix in
`research/2026-07-13-mij-stem-devoicing-doublet.md` recorded that
audio row without a lemma qualifier.

## What the LLM produced

The deck stance "no bracket on **any** միջ- lemma" and topic
prose ("Real-speech evidence agrees with Dum-Tragut") that read
as family-wide, though the audio covered one lemma. For միջին the
voiced claim actually rested on Dum-Tragut's text alone — against
parnasyan's contrastive [мичин] and Wiktionary's text IPA, i.e. a
2-vs-1 matrix presented as audio-settled.

## What was correct

Operator re-checked միջին specifically (2026-07-15, YouTube +
TikTok running speech; unambiguous adjective uses — coffee sizes,
math averages): consistently devoiced [tʃʰ]. The doublet splits
per-lexeme — միջոց voiced, միջին devoiced — matching Dum-Tragut's
own "often doublets" framing. Homograph control applied: միջին as
inflected մեջ (ձորի միջին type) would devoice unremarkably and
proves nothing; the checked clips were the adjective.

## Why this happened

The retraction corrected a per-lexeme failure with a family-level
conclusion. Once "միջ- does not devoice" became the headline, the
one-lemma scope of the audio evidence disappeared from the deck
decision. Absence of per-lexeme audio was read as agreement with
the reference grammar — the same absence-as-license move as
`2026-07-13-001` § "Why" point 3.

## Mitigation

- **Data fix:** `միջին [միչին]` restored to
  `cards/frequency/respellings.tsv` with honest provenance
  (`operator audio 2026-07-15; parnasyan p398 [мичин]`) — a
  per-lexeme attestation, not propagation; the ablaut guard
  stands and the row licenses no other միջ- lemma. Deck rebuilt +
  validated.
- **Doc guard:** § "2026-07-15 refinement" in
  `voiced_aspirated_alternation.md`, reversal note in
  `known_transcriptions.md`, dated addendum in the doublet
  research file.
- **Rule:** *audio verification is per-lexeme too — an empty
  audio cell is a gap, not agreement.* Evidence-matrix rows must
  name the exact lemma the evidence covers.

## Test case

Query: "does միջին devoice (ջ→չ)?" — expected answer: **yes**,
[tʃʰ] per operator audio 2026-07-15 + parnasyan p398 [мичин],
explicitly against dumtragut p43 [midʒin] (recorded doublet). The
միջին card carries [միչին]; միջոց/միջև/միջազգային/անմիջապես
still carry no bracket. Regression signal: any pass that flips
միջին back citing dumtragut p43 without engaging the audio
evidence, or that extends միջին's row to another միջ- lemma.
