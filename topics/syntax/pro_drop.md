---
topic: pro-drop in Eastern Armenian
domain: syntax
units: [sakayan:1, sakayan:2]
related: [present-tense, irregular-verbs, sentence-member-elision]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 36
    y_range: [590, 615]
    verbatim_quote:
      - "Normally, Armenian finite forms do not necessarily require personal pronouns"
      - "as"
      - "the expressive personal forms of the conjugated verb"
      - "make them redundant"
      - "ես, դու,"
      - "եմ, ես,"
    supports: supported
    note: |
      footnote at the bottom of p36 stating pro-drop directly. The
      pronouns ես, դու are listed as examples of redundant subject
      pronouns; եմ, ես, է are listed as examples of "expressive
      personal forms" (the auxiliary).
  - id: 2
    book: sakayan
    page: 71
    y_range: [165, 185]
    verbatim_quote:
      - "Ունեմ, ահա՜։"
      - "[Unem, aha]"
    supports: supported
    note: |
      one-word pro-drop sentence in dialogue context: "I have, here you
      are!" The verb form ունեմ "I have" alone identifies the subject
      as 1sg; no Ես. Demonstrates the rule from [#1] in use.
  - id: 3
    book: ghamoyan
    page: 79
    y_range: [305, 380]
    verbatim_quote:
      - "զեղչման բոլոր տիպերը"
      - "ենթական, և"
      - "Առավոտը"
      - "Ես հիմար եմ, դու խելացի ես"
    supports: supported
    note: |
      direct claim that Yerevan colloquial generalises elision (զեղչում)
      to "all types of sentence members — subject, predicate, and other
      complements." Examples include subject+predicate elision
      (Ես առավոտյան էլի գործի եմ գնալու → Առավոտը էլի գործի) and
      auxiliary elision (Ես հիմար եմ, դու խելացի ես → Ես՝ հիմար, դու՝ խելացի).
      Quote stitched across multiple ghamoyan p79 spans.
  - id: 4
    book: ghamoyan
    page: 80
    y_range: [40, 80]
    verbatim_quote:
      - "անհանգույց"
      - "խենթ ու խելառ"
    supports: supported
    note: |
      zero-copula example in colloquial: "Դու` խենթ ու խելառ" ("You
      [are] crazy and silly"). Quote captures the technical term
      անհանգույց "unlinked / without copula" + the example.
gaps:
  - "Empty-pronoun typology: is Armenian a 'consistent' null-subject language (like Spanish, Italian) or 'partial' (like Russian)? Untreated by both sources."
  - "Topicalisation / dislocation patterns surrounding pro-drop: untreated."
  - "Object pro-drop or other null arguments: untreated by sakayan; ghamoyan's broad elision claim implies object-drop is permitted but doesn't formalise."
  - "Quantitative data on pronoun expression — what fraction of finite clauses have an overt subject in colloquial vs literary text?"
  - "Discourse-newness conditions on overt pronouns: when is an explicit pronoun obligatory vs optional? Sakayan's 'emphasis or contrast' is partial; ghamoyan doesn't extend it."
---

# Pro-drop in Eastern Armenian

Eastern Armenian routinely **omits subject pronouns**: the verb's
person/number marking (in the auxiliary, for analytic tenses) is
sufficient to identify the subject. [#1] In Yerevan colloquial speech,
this generalises to the elision of *any* sentence member —
predicate, complements, and even the auxiliary itself can be dropped
when context permits. [#3] [#4]

## Source of the rule (literary norm)

Sakayan states the rule directly in a footnote on p36: [#1]

> Normally, Armenian finite forms do not necessarily require personal
> pronouns (ես, դու, etc.) as the expressive personal forms of the
> conjugated verb (եմ, ես, է, etc.) make them redundant.

The footnote frames the auxiliary forms (`եմ, ես, է, …`) as
"expressive personal forms" — they carry person/number unambiguously,
so the subject pronoun adds nothing in the unmarked case.

## Example: a one-word complete sentence

[#2] *Ունեմ, ահա՜։* — "I have, here you are!" The verb form `ունեմ`
"I have" by itself is the predicate; no `Ես`. This generalises: any
conjugated verb form whose suffix unambiguously identifies the
subject can stand alone as a sentence.

## Yerevan colloquial: elision beyond the subject (Ghamoyan)

Ghamoyan documents a much broader elision pattern in colloquial
Yerevan speech. [#3] The framing is direct:

> "Colloquial language is characterised by **all types of
> sentence-member elision** — subject, predicate, and other
> complements" (զեղչման բոլոր տիպերը` և՛ ենթական, և՛ ստորոգյալը,
> և՛ մյուս լրացումները).

Examples ghamoyan gives:

- **Subject + predicate elision**: *Ես առավոտյան էլի գործի եմ
  գնալու* ("I'm going to work again tomorrow morning") →
  *Առավոտը էլի գործի* ("morning, again to work").
- **Auxiliary elision**: *Ես հիմար եմ, դու խելացի ես* ("I am
  stupid, you are smart") → *Ես՝ հիմար, դու՝ խելացի* ("I — stupid,
  you — smart").

Ghamoyan also documents **zero-copula constructions** [#4]:

> "Colloquial language features sentences with **unlinked predicates**
> (անհանգույց ստորոգյալով). Example: *Դու` խենթ ու խելառ* ('You
> [are] crazy and silly')."

So in Yerevan colloquial, the pro-drop pattern is one corner of a
broader licensing of contextual elision: anything recoverable from
context can be dropped.

## When subject pronouns *do* appear

Two motivations carry over from Sakayan's prose (paraphrased; not
single-passage quoted):

1. **Emphasis** — `Ես ունեմ։` "*I* have."
2. **Contrast** — `Ես ունեմ, դու չունես։` "*I* have, *you* don't."

A third, less explicit case is **discourse newness**: when a subject
referent is introduced for the first time, an explicit pronoun (or
full NP) is normal even without contrast. Neither Sakayan nor
ghamoyan formalises this — it's an open gap.

## Implication for paradigm cards

A single conjugated form like `ունեմ` *is* a complete utterance ("I
have"). This validates the per-form card design in `anki-design.md` —
each paradigm cell can be presented in isolation without an
artificial subject pronoun. For colloquial-register cards, the
auxiliary itself can also be dropped (`Ես՝ հիմար`) without loss of
meaning — though that's a separate card-design question.

## Contrastive notes

**For an English L1**: English requires explicit subjects (`*Have`
is not a sentence; `I have` is). Treat `ունեմ` as already including
"I" — the auxiliary suffix `-մ` is the "I." For colloquial register,
add: even a copula-less sentence like `Դու` խենթ ու խելառ` (literally
"You — crazy and silly") works the way English headlinese drops "is"
(*"Mayor: corrupt"*).

**For a Russian L1**: Russian is *partial* pro-drop — colloquially,
present-tense forms can drop the subject (`Иду` for "I'm going"), but
past-tense forms (which don't carry person marking) need a pronoun.
Armenian is *consistent* pro-drop across all tenses, because the
auxiliary carries person/number even where the participle doesn't. In
colloquial Yerevan, Russian's "drop the copula in present-tense
predicative sentences" pattern (`он умный` "he-smart" — no copula)
matches ghamoyan's *անհանգույց ստորոգյալ* exactly. So a Russian L1
already has the cognitive template for the colloquial Armenian
pattern; what's new is its extension to verb auxiliaries
(`Ես հիմար, դու խելացի` — auxiliary `եմ`/`ես` dropped).

## Open questions / gaps

Mirrored from frontmatter:

- Empty-pronoun typology classification (consistent vs partial NSL).
- Object pro-drop / null arguments more generally — ghamoyan's broad
  elision claim implies it's permitted but doesn't formalise.
- Quantitative pronoun-expression data.
- Discourse-newness conditions on overt pronouns.
