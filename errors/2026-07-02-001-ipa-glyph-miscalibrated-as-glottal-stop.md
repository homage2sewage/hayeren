---
id: 2026-07-02-001
date: 2026-07-02
caught_by: dogfood
caught_during: review
severity: major
disposition: llm-error
category: script-and-source-hygiene
subcategory: font-glyph-miscalibration
phenomenon: legacy-phonetic-font-decode-table-calibration
related_topics:
  - topics/phonology/dumtragut_ipa_transcriptions.md
  - topics/phonology/voiced_aspirated_alternation.md
related_pitfalls:
  - errors/2026-05-07-002-gloss-vs-bytes.md
status: mitigated
mitigation:
  type: pipeline-fix
  ref: dumtragut/phonetic.py
recurrence: novel
---

## Input

Building the full word→IPA harvest of the Dum-Tragut corpus
(`dumtragut/harvest_ipa.py`, 2026-07-02). The per-glyph decode
table in `dumtragut/phonetic.py` had been calibrated 2026-06-19
and was documented as "all glyphs verified against rendered
bitmaps; nothing tentative remains."

## What the LLM produced

The 2026-06-19 calibration mapped raw `‚` (MinionPhonetic) to the
glottal stop **ʔ**, glossed "glottal onset on initial ո/ա", anchored
on որբ `[‚fnph]` read as [ʔɔɾpʰ]. That reading was plausible-sounding
(glottal onsets before initial vowels do exist in Armenian phonetics
descriptions) but wrong — and it poisoned all 53 corpus occurrences:
և came out [jɛʔ], Երևան [jɛrɛʔɑn], որովհետև [ʔɔɾɔhɛtɛʔ].

## How it was caught

The 2026-07-02 harvest surfaced `և ew [jɛʔ] "and"` — phonologically
impossible (և is "yev"). Rendering the p37 line at 900dpi showed the
glyph is the **hooked script-v ʋ** (labiodental approximant): the
page prints [jɛʋ], [ʋɔɾdi], [ʋɔski], [jɛɾɛʋɑn] — the ordinary
word-initial ո = [ʋɔ] rule. որբ is "vorp": [ʋɔɾpʰ], which also fits
the original anchor. Every one of the 53 occurrences is consistent
with ʋ; none requires ʔ.

## Root cause

The anchor word որբ was interpreted through a *prior* ("glottal
onset on initial ո") instead of by looking at the rendered glyph
shape at sufficient resolution. ʔ and ʋ are both plausible-shaped
marks at 150dpi; only the 900dpi crop shows the hook. The
"bitmap-verified" claim was true for the *other* glyphs but this
slot's verification accepted a phonological story instead of a
pixel match — exactly the gloss-vs-bytes failure shape, one level
down (glyph-vs-story).

## Mitigation

- Fix: `dumtragut/phonetic.py` `‚`→ʋ (+ docstring correction note),
  corpus re-extracted, harvest + table regenerated; goldens
  (47 respellings.tsv IPA rows) still byte-match.
- Guard: `dumtragut/harvest_ipa.py` now exists — a full-book harvest
  makes systematic decode errors *visible in bulk* (53 weird ʔ rows
  in one table column is conspicuous; 1-2 scattered quotes were not).
  Its golden check against `cards/frequency/respellings.tsv` runs on
  every regeneration.
- `ʋ` added to `_IPA_MARKERS` in `armenian_self_check.py` and to
  the harvest's `IPA_MARKER` set.
- Stale-quote hazard: any pre-2026-07-02 dumtragut IPA quote
  containing ʔ no longer byte-verifies (correct behaviour — the
  bytes were wrong). Memory + phonetic.py docstring updated.

## Lesson

For legacy-font glyph calibration, "verified" must mean a
high-resolution pixel comparison per glyph slot, not "the decoded
word admits a phonological explanation." When a decode table claim
and a phonological impossibility collide (և = [jɛʔ]), render the
bitmap before trusting either.
