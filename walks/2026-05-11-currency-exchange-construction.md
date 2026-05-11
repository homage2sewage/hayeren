# Topic walk: currency-exchange construction — `<X>-ի փոխանակում` / `<X> փոխանակել`

**Date**: 2026-05-11
**Operator**: Claude Code, manual walk
**Status**: walk executed; small enough to fold into the
service-encounter topic when one exists; not promoted on its own.

## Motivation

Follow-on from the `տոպրակ տա՞մ` / "100 dollars to drams" thread
(2026-05-11 session). The corpus has the relevant lexical items
(`փոխանակել`, `փոխանակում`, `արտարժույթ`, `դիմաց`) but no
service-encounter dialogue that combines them. A user observation
of a Yerevan street-sign formula (`տարադրամի փոխանակում`) supplied
the missing syntactic anchor and falsified an earlier
LLM-proposed case-frame (`<cur2>-ով` instrumental). This walk
captures the construction with corpus citations on the lexical
items and the user observation explicitly flagged as
observation-not-citation.

## User observation (not citation)

> Yerevan exchange-bureau / bank street signs say
> **`տարադրամի փոխանակում`** ("foreign-currency exchange").

This is **first-hand environmental Armenian**, not a corpus
citation. None of the four source books attests the compound
`տարադրամ`; it surfaces only via this user observation. Treat
as evidence of standard public-sphere usage; do not promote to
a `verbatim_quote` source until paired with a written attestation.

## Corpus attestations of the parts

### `փոխանակել` "to exchange" (verb)

- **Sakayan p426** y[142–153]
  > `խորհրդավոր հայացքներ փոխանակելով՝ փսփսում էին։`
  "Exchanging mysterious glances, they whispered."

  *Frame*: `<X-acc> փոխանակել` — single argument (the thing
  exchanged); subject is plural and the exchange is reciprocal /
  symmetric. Not a "trade X for Y" frame.

- **Sakayan p516, p525**: bare vocab listings of `փոխանակել` and
  `փոխանակում` — no syntactic context.

### `փոխանակում` "exchange" (deverbal noun)

- **Parnasyan p419** y[3979–4096] (OCR conf 66.4)
  > `փոխանակում [п'оханакум] сущ., -ман обмен`

  Glossary entry. Confirms the noun exists, declines as
  `-ման` (gen `փոխանակման`), Russian gloss `обмен`. No usage
  example.

### `փոխել` "to change, exchange" (verb)

- **Parnasyan p419** y[4258–4383] (OCR conf 82.9)
  > `փոխել [похэл] гл., -уй менять, поменять; обменивать, обменять`

  Glossary entry. Russian gloss list **explicitly includes
  `обменивать` / `обменять`** — so `փոխել` covers the
  currency-exchange sense too (in addition to "swap, change").

- **Tioyan p51** vocab: `փոխել менять` (single-word entry).

### `արտարժույթ` "foreign currency"

- **Tioyan p257** y[2298–2346] (OCR conf 87.6)
  > `… Արտարժույթի կուրսի կտրուկ …`
  "… [a] sharp [change in] the foreign-currency exchange rate …"

### `կուրս (դրամի)` "(exchange) rate (of the dram)"

- **Ghamoyan p109** y[266.82–275.73]
  > `կուրս (դրամի)`

  Vocab line that explicitly parenthesises `(դրամի)` to
  disambiguate from `կոնկուրս` "competition" on the line above.
  Establishes `կուրս` as the term for "(exchange) rate" in
  Yerevan colloquial.

### `<X>-ի դիմաց` "in exchange for X" (adjunct)

- **Sakayan p443** y[235.57–246.57]
  > `զավակներին՝ մի քանի արծաթ դրամի դիմաց`
  "(traded) the children for a few silver coins."

  The book-attested construction for "in exchange for X-currency."
  Transaction frame (verb of selling / trading); not specifically
  paired with `փոխանակել` in the corpus.

### `դրամական փոխանցումներ` "monetary transfers"

- **Tioyan p162** y[2069–2112]
  > `դրամական փոխանցումներ: денежные переводы`

  Banking-domain noun; related but distinct (transfers, not
  exchange).

## Derived construction

Combining the user observation with the corpus attestations:

**Nominal form** (mirrors the street sign):

> `<X>-ի փոխանակում`
> "exchange of X" — `X` is what's being exchanged, in the
> **genitive**.

Examples:
- `տարադրամի փոխանակում` "foreign-currency exchange" (sign)
- `հարյուր դոլարի փոխանակում` "exchange of 100 dollars"
  (reconstruction)

**Verbal form** (mirrors Sakayan p426):

> `<X-acc> փոխանակել`
> "to exchange X" — `X` is what's being exchanged, in the
> **bare / accusative**.

Examples:
- `հայացքներ փոխանակել` "to exchange glances" (corpus)
- `հարյուր դոլար փոխանակել` "to exchange 100 dollars"
  (reconstruction)

**Optional "for Y" adjunct** (per Sakayan p443):

> `… <Y>-ի դիմաց`
> "for Y" — `Y` is what one gets back, in the genitive.

Examples:
- `դրամի դիմաց` "for drams/money" (corpus, in a selling context)
- `հարյուր դոլարի փոխանակում դրամի դիմաց` "exchange of 100
  dollars for drams" (reconstruction; both parts attested, the
  pairing is not)

## What was falsified

Earlier in the session the LLM (this assistant) proposed:

> `<sum> <cur1> փոխանակել <cur2>-ով`

The instrumental `-ով` on the target currency. **Not supported by
any corpus attestation, and not consistent with the street-sign
formula.** Logged separately as
`errors/2026-05-11-001-currency-exchange-case-frame.md`.

## Web corroboration — contemporary crypto-domain Armenian

A targeted web search on Armenian crypto-exchange usage (2026-05-11
session) independently confirmed the construction analysis derived
from the corpus + street-sign observation.

### Triple-attested: `<X-gen> + դիմաց` for "in exchange for X"

The construction surfaces across three independent registers:

1. **Literary / 19th-c flavour**: Sakayan p443, `դրամի դիմաց` (selling).
2. **Pedagogical**: Bayramyan 2009 phrasebook p63 (transcribed from
   photo, this session) — `Տարադրամի փոխանակում` as section heading,
   the `դիմաց` adjunct implicit in surrounding formulas.
3. **Contemporary financial journalism**: MediaFactory.am crypto
   article —

   > «**Կրիպտոյի դիմաց** ստանում է դոլար կամ դրամ»
   > "In exchange for crypto, [one] receives dollars or drams."

This is unusually strong cross-register agreement. The construction
is settled standard Armenian, not a register-bound formula.

### Verbs in contemporary crypto-domain usage

Web evidence (Bitcoin.org Armenian, Hetq.am, SkyLabs, MediaFactory)
confirms a verb hierarchy:

| verb | gloss | argument frame | example |
|---|---|---|---|
| `գնել` | "buy" | acc-target | `բիթքոին գնել` (Bitcoin.org) |
| `վաճառել` | "sell" | acc-source | `գնել կամ վաճառել այն` (Hetq) |
| `ձեռք բերել` | "acquire" (formal) | acc-target | `բիթքոինի ձեռք բերելու եղանակը` (Hetq) — gen on the verbal-noun complement |
| `փոխարկել` | "convert" | acc-source / **dat-target** | `գումարը… փոխարկել` (Hetq) |
| `վերածել` | "convert into" | acc-source / **dat-target** | `Վերածել բիթքոինի ներդրումի` (Hetq) |
| `փոխանակել` / `փոխանակում` | "exchange" | single-arg (gen on noun) | `արժույթների փոխանակում` (SkyLabs) |

Two observations:

- **Dative-target** for `փոխարկել` / `վերածել` is the productive
  "convert X into Y" frame in contemporary written Armenian. The
  instrumental `-ով` analysis the LLM proposed earlier this session
  is contradicted not only by the street-sign observation but by
  every web source surveyed. See
  `errors/2026-05-11-001-currency-exchange-case-frame.md`.
- **`փոխանակել`** remains single-argument in web usage too —
  `արժույթների փոխանակում` "exchange of currencies" (with the
  *plural* currencies as the single argument); the "exchange partner"
  isn't a verbal slot, consistent with the Sakayan p426 reciprocal
  frame.

### Crypto-domain vocabulary the four-book corpus lacks

The web search surfaced terminology entirely absent from
`{sakayan,ghamoyan,parnasyan,tioyan}/out/full.jsonl`:

- `կրիպտոարժույթ` — cryptocurrency (general)
- `կրիպտոակտիվ` — crypto-asset (legal-register term, used in
  *ՀՀ Օրենքը Կրիպտոակտիվների Մասին* / RA Law on Crypto-Assets)
- `բիթքոյն` / `բիթկոյն` / `բիթքոին` — Bitcoin (**three orthographic
  variants** in current use; not settled). `բիթքոյն` is the
  Bitcoin.org Armenian rendering; `բիթկոյն` appears on B24.am;
  `բիթքոին` in Hetq.am.
- `հարթակ` "platform" / `տերմինալ` "terminal" / `հավելված` "app"
- `կանխիկ` / `անկանխիկ` "cash / non-cash" (the law restricts crypto
  exchange to non-cash transactions for most cases)
- `փոխանակման կետ` "exchange point" (service-encounter physical term)

### Operational phrasings (web-attested or web-derivable)

Service-encounter sentences a learner could actually use:

| English | Armenian |
|---|---|
| "I want to buy USDT" | `Ուզում եմ USDT գնել։` |
| "I want to buy USDT with drams" | `Ուզում եմ USDT գնել դրամով։` (instrumental = means) |
| "Convert 100,000 drams to USDT" | `100 000 դրամ USDT-ի փոխարկել։` (dative target) |
| "Exchange drams for USDT" | `Դրամի փոխանակում USDT-ի դիմաց։` (nominal + adjunct) |
| "Sell BTC for drams" | `BTC վաճառել դրամի դիմաց։` |
| "How much can I get for 1000 USDT?" | `1000 USDT-ի դիմաց որքա՞ն կստանամ։` |

### Web sources surveyed (2026-05-11)

- Կրիպտոարժույթ — hy.wikipedia.org/wiki/Կրիպտոարժույթ
- Ինչպե՞ս գնել Բիթքոին — hetq.am/hy/article/127019
- Հայ պաշտոնյաների կրիպտո ակտիվները — mediafactory.am/our-products/crypto
- Գնեք Բիթքոյն — bitcoin.org/hy/buy
- SkyLabs — skylabs.world (Armenian-language crypto exchange platform)
- ՀՀ Օրենքը Կրիպտոակտիվների Մասին — arlis.am/hy/acts/208599
- Haykakan Crypto Dprots — haykakancryptodprots.com/hy/

## Implications for `topics/`

No topic file exists for the service-encounter register. This
walk is now one of three pieces of evidence (with the
`տոպրակ տա՞մ` cashier observation and the Bayramyan p62-63
phrasebook transcription from earlier in the same session) that
together establish a clear KB gap:

> `topics/pragmatics/service-encounter.md` (or
> `topics/lexicon/currency-and-commerce.md`) — does not exist;
> would house exchange formulas, price-asking
> (`Ի՞նչ է վերջնական գինը` Sakayan p117), payment
> (`Քանիակա՞ն դոլար ստացաք` Sakayan p158/164), bag-offer
> (`Տոպրակ տա՞մ` reconstruction), and the currency-exchange
> formulas above.

A second topic candidate now in scope:

> `topics/lexicon/cryptocurrency.md` — would catalogue
> orthographic variants of `Bitcoin` (`բիթքոյն` / `բիթկոյն` /
> `բիթքոին`), the formal/casual register split
> (`կրիպտոակտիվ` legal vs. `կրիպտոարժույթ` general), and the
> verb hierarchy (`գնել` / `վաճառել` / `փոխարկել` / `փոխանակել` /
> `վերածել`) with their argument frames as web-attested. All
> sources are written and citable (Bitcoin.org Armenian, Hetq,
> SkyLabs, MediaFactory, Wikipedia, ՀՀ law).

Defer creation until at least one more service-encounter
construction is grounded — single-construction topics tend to
read as glossary entries rather than syntheses. The
crypto-lexicon topic, by contrast, is already viable on its own
(multiple orthographic variants + register split + verb-frame
table = enough body to stand alone).

## Implications for `cards/`

Two chunk-card candidates if/when a service-encounter set is
built:

- `Հարյուր դոլարի փոխանակում, խնդրեմ։` / `100 dollars' exchange,
  please.` — borrows the street-sign genitive formula.
- `Կարո՞ղ եք հարյուր դոլար փոխանակել։` / `Can you exchange 100
  dollars?` — uses the corpus-attested verbal frame.

Both flagged as "reconstructed from corpus parts + user
observation, not corpus-attested as a unit" until paired with a
witness.

## Process notes

- The walk was triggered by the user-supplied environmental
  datum `տարադրամի փոխանակում`, which falsified the LLM's prior
  `<cur2>-ով` analysis. Recording this so the audit trail is
  intact: the case-frame the LLM produced was internally
  plausible and would not have been caught by the existing
  `verify_citations.py` (no `topics/` file in scope, no
  `verbatim_quote` to check).
- The corpus genuinely lacks service-encounter material;
  multiple consecutive questions in this session
  (`տոպրակ տա՞մ`, currency exchange) hit the same gap. The gap
  should be promoted from "noticed in passing" to a recorded
  research priority — candidate for an entry in
  `research/2026-05-09-answer-pipeline-roadmap.md` or a new
  `research/2026-05-11-service-encounter-corpus-gap.md`.
