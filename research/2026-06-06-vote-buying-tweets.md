# Tweet read-through — "vote-buying" political rant (2026-06-06)

A **single** Armenian tweet (one author's voice throughout — a
factual-style claim followed immediately by the author's own moral
condemnation, not a quote + reply) parsed with `query_kb.py`
auto-grounding. Heavy Yerevan colloquial register; the rhetorical
pivot is a slang double-meaning that **is** in the corpus. Logged
per the user request and the precedent of
`research/2026-05-09-tweet-llm-comparison.md`.

## The text

```
Ռուսները պատրաստվում են 50 միլիոն $ ծախսեն 100000 հայ հայաստան
քվեարկելու ուղարկելու համար, մարդա 500$

անհայրենիք շուն բառը, որ ուզեք մեկին բացատրեք էս դեպքը հիշեք, ոնց
կարելիա հայրենիքդ 500 $ ով ուրիշ պետության ծախել
```

## Working translation

One continuous utterance (the `,` after `մարդա 500$` joins the two
halves — no speaker change):

> "The Russians are preparing to spend \$50 million to send
> 100,000 Armenians to Armenia to vote — \$500 a head. The phrase
> 'homeland-less dog' — if you ever want to explain it to someone,
> remember this case: how can you sell your homeland to another
> state for \$500?"

Content is a political / disinformation-style claim (an alleged
Russian-funded scheme to fly diaspora Armenians in to vote, costed
at \$50M ÷ 100,000 = \$500/person — the arithmetic is internally
consistent) plus a moral condemnation. Nothing here is
linguistically *hard*; the value of the pass is the register +
the one slang pivot.

## Token-by-token (graded)

| token | reading | grounding |
|-------|---------|-----------|
| `ծախսեն` | "(to) spend" — colloquial bare subjunctive where literary wants `ծախսել` after `պատրաստվում են` | prior (transparent); not in corpus (Gaps) |
| `հայաստան քվեարկելու ուղարկելու համար` | "to send to Armenia to vote" — **bare `հայաստան`** = accusative-for-directional/locative | **cited**: `topics/morphology/accusative_for_locative.md` (ghamoyan p87, `Ես Երևան եմ ապրում`) |
| `քվեարկել` | "to vote" | attested in corpus (modern term); transparent |
| `մարդա 500$` | "\$500 a head" = `մարդ` + colloquial copula `ա` (=`է`), cliticized: "person-is \$500." The "per" sense is **constructional** (bare unit-noun + copula + price), NOT a distributive morpheme | copula `ա`=`է` **cited**: `present_tense.md` [#5]. The per-unit pricing construction is a **gap** (prior). NB: the real numeral distributive is `-ական`, not `-ա` |
| `անհայրենիք` | "homeland-less, stateless" = privative `ան-` + `հայրենիք` | **prior** (Gaps); but morphologically transparent. `հայրենիք` itself is corpus-attested (sakayan p74, p183 `հանուն հայրենիքի`) |
| `շուն` | "dog" — here a free term of abuse, not a fixed idiom | register **cited**: `topics/lexicon/idioms_phrasal.md` documents the `շուն` insult/idiom family (`շան թուլա`, `շան լակոտ` carry vulgar/reproachful register) |
| `որ ուզեք ... բացատրեք` | "if/when you want to explain" — colloquial `որ` conditional + 2pl subjunctive | prior (transparent) |
| `էս` | "this" = colloquial `այս` | **cited**: `topics/morphology/determinate_article.md`, `accusative_for_locative.md` |
| `ոնց` | "how" = colloquial `ինչպես` | corpus-attested: `ոնց որ` (sakayan p279) |
| `կարելիա` | "is possible / can one" = `կարելի` + colloquial copula `-ա` for `է` | **cited** for the `ա`-for-`է` shift: `topics/morphology/present_tense.md` § "Yerevan colloquial 3sg `ա` for `է`" |
| `հայրենիքդ` | "your homeland" — 2sg possessive `-դ` | corpus-attested possessive pattern |
| `500$ով` | "for \$500" — instrumental `-ով` (price/means) | prior (transparent) |
| `ուրիշ պետության ծախել` | "sell to another state" — note `պետության` is genitive where dative `պետությանը` would be cleaner | prior; mild case slip |
| **`ծախել`** | **the pivot**: literally "to sell," but Yerevan slang **"to betray, to snitch"** | **cited**: `topics/lexicon/yerevan_slang.md` [#2] (ghamoyan p48): `ծախել` "to sell" → "to betray"; also `ծախվել` "to be sold" → "to be betrayed/to give in" |

## The pivot worth flagging

`ծախել` carries a deliberate double meaning here. The surface
clause is "sell your homeland for \$500," but `ծախել` in Yerevan
slang is the verb for **betraying / selling someone out**
(`topics/lexicon/yerevan_slang.md`, ghamoyan p48). So the line
isn't only "sell" in a commercial sense — it reads as "**betray**
your homeland for \$500," which is exactly the `անհայրենիք շուն`
("homeland-less dog") accusation made one clause earlier. The
literal-betrayal pun is the rhetorical engine of the second tweet.
This is the same `ծախել` whose slang sense was the corpus anchor
in the 2026-05-09 `խոտ` case — already in the KB, no need to guess.

## Register summary

Dense Yerevan colloquial: `էս`, `ոնց`, the `-ա` copula
(`կարելիա`), bare subjunctive (`ծախսեն`), accusative-for-
directional (`հայաստան ... ուղարկելու`), distributive `մարդա`.
All the *grammar/register* markers are corpus-grounded; the only
genuinely uncited lexemes (`մարդա`, `անհայրենիք`, `կարելիա`) are
morphologically transparent compounds, not opaque slang.

## Gaps (named, per `query_kb.py`)

`ծախսեն`, `անհայրենիք`, `կարելիա` — absent from topic graph,
notes, and all four books. Glossed above from prior + morphology,
not citation. `մարդա` distributive likewise prior-only.

## Not assessed

The factual/political claim itself (Russian funding, 100k voters,
\$500/head) is a content claim, not a language one — flagged as a
propaganda-style assertion, not verified.

---

# Tweet 2 — "index finger" lament (same session, election theme)

A second election-period tweet read in the same session. Unlike
Tweet 1 this is essentially **standard written Armenian** with only
a light colloquial dusting — no slang pivot.

## The text

```
Էս ընտրությունների ամենացավոտ պահերից մեկը իմ համար էն
բացահայտումն էր թե քանի մարդ չգիտի թե ցուցամատը որն ա
```

## Working translation

> "One of the most painful moments of these elections, for me, was
> the discovery of how many people don't know which finger the
> index finger is."

A lament about observed general ignorance during the elections — a
social/content observation, not a linguistic claim, not assessed.

## Token-by-token (graded)

| token | reading | grounding |
|-------|---------|-----------|
| `Էս` / `էն` | "these" / "that" = colloquial `այս` / `այն` | **cited**: `determinate_article.md`, `accusative_for_locative.md` |
| `ընտրությունների` | "of the elections" (gen.pl, `ընտրություն`) | **cited**: ghamoyan p19 `ընտրությունը`; tioyan p61 `ընտրական ցուցակ`, `ընտրել`, `ընտրող` |
| `ամենացավոտ` | "most painful" = `ամենա-` (superl.) + `ցավոտ` (`ցավ`+`-ոտ`) | **prior/gap** (transparent); not in corpus |
| `պահերից մեկը` | "one of the moments" — abl.pl + substantive `մեկը` (partitive) | **cited**: `topics/morphology/numeral_forms.md` (substantive `մեկը`) |
| `իմ համար` | "for me" — colloquial; literary `ինձ համար` (dative, not possessive) | **prior** (gap) |
| `բացահայտումն էր` | "was the discovery" — `բացահայտում` + pre-copula `-ն` + `էր` | prior (transparent) |
| `թե … թե` | two stacked complementizers → embedded questions | **cited**: `negation.md`, `subjunctive_mood.md`, `el_particle_position.md` |
| `չգիտի` | "doesn't know" = `չ-` + `գիտի` (`գիտենալ`) | **cited**: `topics/morphology/negation.md` |
| `ցուցամատը` | "the index finger" = `ցուց-` "point" + `մատ` "finger" | **cited**: tioyan p105 & p379 `ցուցամատ указательный палец`; sakayan p172, p515 |
| `որն ա` | "which one it is" = `որ`+`-ն` + colloquial copula `ա` (=`է`) | copula **cited**: `present_tense.md` |

## Register summary

Standard written Armenian + three colloquial tells: `Էս`/`էն` for
`այս`/`այն`, the `ա`-copula in `որն ա`, and `իմ համար` for `ինձ
համար`. No slang lexicon; `ցուցամատ` is the neutral literary word.

## Gaps

`ամենացավոտ` (and the `իմ համար`-for-`ինձ համար` colloquialism) —
not in corpus; glossed from morphology/prior, not citation.
