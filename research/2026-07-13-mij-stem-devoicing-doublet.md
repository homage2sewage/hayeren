# The միջ- stem does not devoice: retracting five respells, mapping a doublet zone

**Date:** 2026-07-13
**Trigger:** operator's ear. The deck carried hand-curated ջ→չ
respells `միջոց [միչոց]`, `միջին [միչին]`, `միջև [միչև]`,
`միջազգային [միչազգային]`, `անմիջապես [անմիչապես]`; the operator
reported that Wiktionary's *audio* for միջոց and running speech in
YouTube clips (e.g. «միջոցը հազի դեմ» shorts) have plainly voiced
[dʒ], even though Wiktionary's *text* transcription gives
/mit͡ʃʰot͡sʰ/ for both Eastern and Western Armenian.

**Outcome:** the operator was right. All five միջ- respells (plus
the propagated `մեջտեղ [մեչտեղ]`) retracted from
`cards/frequency/respellings.tsv` and the deck rebuilt. The
underlying rule corrected in
`topics/phonology/voiced_aspirated_alternation.md`
§ "2026-07-13 correction" (new byte-verified sources [#14]–[#19])
and `topics/phonology/known_transcriptions.md` (retraction
sections in the ջ→չ table and the tier-1 propagation table).

## The decisive evidence

Dum-Tragut states the post-vocalic ջ→[tʃʰ] devoicing as a
**closed word-list**, not an open environment (dumtragut p43,
book p26):

> "it occurs between two vowels, or follows a vowel in the
> following words (and their derivations and compounds)":
> աջ [ɑtʃʰ], առաջ [ɑrɑtʃʰ], առաջին [ɑrɑtʃʰin], մեջ [mɛtʃʰ],
> ոջիլ [ʋɔtʃʰil], քաջք [kʰɑtʃʰkʰ]

followed by the complement rule:

> "In all other words it is written as ջ j pronounced as [dʒ] as
> in հաջորդ hajord [hɑdʒɔɾtʰ] 'next', իջնել ijnel [idʒnɛl] 'to
> descend', **միջին mijin [midʒin]** 'middle', **միջատ mijat
> [midʒɑt]** 'insect', քրոջ k'roj [kʰəɾɔdʒ]…"

միջին and միջատ — the ablauted միջ- stem — are *explicitly on the
voiced side*, despite being historical derivations of մեջ. The
ե→ի vowel alternation boundary is where the devoicing license
stops.

## The evidence matrix

| source | claim for միջ- | form |
|--------|----------------|------|
| dumtragut p43 | **voiced** | միջին [midʒin], միջատ [midʒɑt], rule text |
| Wiktionary audio (միջոց), YouTube speech | **voiced** | operator-verified 2026-07-13 |
| Wiktionary text IPA | devoiced | /mit͡ʃʰot͡sʰ/ (EA & WA) |
| parnasyan p398 | devoiced | միջին [мичин], միջոցառում [мичоцар’ум], միջամտել [мичамэтэл] |
| parnasyan p110 | devoiced | միջակետ [мичакэт] |
| tioyan p77 | devoiced | միջև rendered ~[միչէվ] (OCR-garbled) |

The split is not noise. **parnasyan's transliteration is
contrastive** — this was the load-bearing check, because Russian
has no single letter for [dʒ] and a lazy system would write ч
everywhere:

- voiced kept voiced: ջուր [джур] (p98), ջերմ [джерм] (p97),
  անջնջելի [анджэнджэли] (p350)
- devoiced where uncontroversial: վերջանալ [вэрчанал] (p413)

So parnasyan's ч in the միջ- rows is a deliberate pronunciation
claim, in head-on conflict with Dum-Tragut on the same lexeme
(միջին). Reading: a Soviet-era prescriptive/broader devoicing
norm vs. a 2009 descriptive reference grammar — or genuine
speaker variation. Dum-Tragut itself frames these alternations as
lexically restricted, "often doublets" (p39). Where a reference
grammar and live audio point the same way, they outrank a
50-year-old textbook transliteration; the doublet is *recorded*
(topic source [#19]) rather than silently overruled.

## Edges of the doublet zone (kept on file, unresolved)

- **մեջ-compounds:** sakayan attests մեջք [мэчк'-style] (u07v)
  devoiced; Dum-Tragut's own practice gives մեջքակապ
  [mɛdʒkʰɑkɑp], մեջտեղ [mɛdʒtɛʁ], մեջընդմեջ [mɛdʒəntʰmɛdʒ]
  voiced (p57) — contradicting its own p43 "and their derivations
  and compounds". `մեջտեղ`'s deck bracket rested on
  sister-propagation from մեջք; a direct attestation for the
  exact lemma beats propagation → retracted.
- **-ոջ genitives:** sakayan քրոջս [քրոչս] (u04d1) vs Dum-Tragut
  քրոջ [kʰəɾɔdʒ], ընկերոջ [əŋkɛɾɔdʒ] (p43–44). Marked disputed in
  `known_transcriptions.md`; քրոջս is a sakayan card annotation,
  not a deck respell, so no deck action.
- **Where everyone agrees** (brackets stay): bare մեջ [mɛtʃʰ],
  the առաջ- family (առաջին [ɑrɑtʃʰin] in both sources), the
  վերջ- family (dumtragut p39 վերջին [vɛɾtʃʰin] = sakayan
  վերջ- rows), and հաջորդ keeping voiced ջ (both sources, only
  the դ devoices).

## What failed, and the guard

The five respells entered `respellings.tsv` as root-propagations
from attested մեջ/մեջք across the ե→ի ablaut boundary — **never
attested anywhere** — and, worse, with `sakayan` in the source
column and only the note admitting "միջ- stem (extension of
մեջ-)". Extrapolation laundered as attestation: the exact failure
mode of `errors/2026-05-09-004` (սով գալ), now with a
morphological refinement.

Guards landed:

1. **Rule, stated in the topic:** a respell needs per-lexeme
   attestation, or propagation within an *identical surface
   shape*; **an ablaut boundary (մեջ→միջ) breaks the license.**
   (`voiced_aspirated_alternation.md`, end of the ջ→չ section.)
2. **Counter-anchors recorded** so the propagation can't be
   re-added: միջին/միջատ in the topic's source [#16], the
   retraction tables in `known_transcriptions.md`.
3. **Provenance honesty:** source columns must name the actual
   basis (`sister-propagation from X`), never the family's
   source. (Also folded into the private feedback memory on
   pattern extension.)
4. Deck rebuilt (`build_deck.py` + `validate_deck.py`, 0 errors);
   `citation-check` green on the edited topic.

## 2026-07-15 addendum: միջին flips to devoiced — the doublet splits per-lexeme

**Trigger:** operator's ear again. Re-checked միջին specifically
in YouTube + TikTok running speech (adjective uses only: coffee
sizes — «միջին» as a size, and math-average contexts) and heard
consistently devoiced [tʃʰ].

**What the 2026-07-13 pass got wrong:** its audio evidence
covered միջոց only — the միջին row of the evidence matrix above
has an *empty* audio cell — yet the deck decision ("no bracket on
միջ- lemmas") generalised միջոց's audio to the sibling. That is
the same extension-beyond-evidence shape this file was written to
correct, applied one level up (to verification evidence instead
of respell rows). The matrix row for "Wiktionary audio / YouTube
speech" should be read as **միջոց only**.

**Updated matrix for միջին:** devoiced side now holds parnasyan
p398 [мичин] + Wiktionary text IPA + operator audio 2026-07-15;
voiced side holds Dum-Tragut's text [midʒin] alone. By this
file's own decision principle (live audio + a concurring source
outrank a lone text claim), միջին flips. միջոց stays voiced
(audio-verified 2026-07-13); միջև, միջազգային, անմիջապես, միջատ
remain audio-unverified and unbracketed.

**Homograph control:** the adjective միջին "middle/average" was
distinguished from միջին as inflected մեջ (ձորի միջին "in the
gorge", tioyan p129/p219), which sits inside մեջ's closed-list
devoicing family and would prove nothing. The verified clips were
unambiguous adjective uses.

**Actions:** `միջին [միչին]` restored to
`cards/frequency/respellings.tsv` with per-lexeme provenance
(operator audio + parnasyan p398 — attestation, not propagation;
the ablaut guard stands and the row licenses nothing else);
retraction sections amended in both phonology topics
(`voiced_aspirated_alternation.md` § "2026-07-15 refinement",
`known_transcriptions.md`); deck rebuilt + validated.

**Guard:** the workflow rule gains a clause — *audio verification
is per-lexeme too; an empty audio cell is a gap, not agreement.*
Logged as `errors/2026-07-15-001`.

## Cross-references

- `topics/phonology/voiced_aspirated_alternation.md` — the
  corrected analysis; sources [#14]–[#19] byte-verified.
- `topics/phonology/known_transcriptions.md` — retraction
  sections (ջ→չ table, tier-1 table).
- `cards/frequency/respellings.tsv` — the live respell base after
  retraction.
- `dumtragut/out/ipa_index.tsv` — the harvest rows that supplied
  citation-ready y-ranges (p43 միջին/միջատ, p57 մեջտեղ, p44
  ընկերոջ).
- `research/2026-06-10-transcription-coverage-and-system.md` —
  the propagation strategy this corrects (tier-1 root
  propagation is now bounded by the ablaut rule).
- `errors/2026-05-09-004-sov-gal-uncited-extrapolation.md` — the
  same failure shape in the syntax domain.
