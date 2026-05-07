---
topic: present tense of regular verbs in Eastern Armenian
domain: morphology
units: [sakayan:1]
related: [verb-classes, irregular-verbs, pro-drop, participles, negation, colloquial-copula-a]
status: draft
attestation: multi-attested
sources:
  - id: 1
    book: sakayan
    page: 36
    y_range: [80, 105]
    verbatim_quote:
      - "գր-ել"
      - "գր-ում"
      - "գրում եմ"
      - "I write"
      - "I am writing"
    supports: supported
    note: |
      schematic header for first-conjugation verbs (`-ել`). Shows the
      chain infinitive → imperfective participle → finite form, with
      gloss "I write or I am writing" — direct evidence that one
      tense covers both English readings.
  - id: 2
    book: sakayan
    page: 36
    y_range: [105, 140]
    verbatim_quote:
      - "կարդ-ալ"
      - "կարդ-ում"
      - "կարդում եմ"
      - "I read"
      - "I am reading"
    supports: supported
    note: same chain for second-conjugation verbs (`-ալ`).
  - id: 3
    book: sakayan
    page: 36
    y_range: [370, 500]
    verbatim_quote:
      - "Present tense (affirmative)"
      - "ես"
      - "գրում եմ"
      - "դու"
      - "գրում ես"
      - "նա"
      - "գրում է"
      - "մենք"
      - "գրում ենք"
      - "դուք"
      - "գրում եք"
      - "նրանք"
      - "գրում են"
    supports: supported
    note: full 6-row paradigm for գրել "to write" in the literary norm.
  - id: 4
    book: sakayan
    page: 36
    y_range: [535, 575]
    verbatim_quote:
      - "Ջոնը սովորում է հայերեն"
      - "Նա արդեն կարդում է"
      - "John is learning Armenian"
      - "He is already reading"
    supports: supported
    note: example sentences with English glosses.
  - id: 5
    book: ghamoyan
    page: 73
    y_range: [290, 340]
    verbatim_quote:
      - "Ժողովրդախոսակցական լեզվում բաղադրյալ ստորոգյալի երրորդ"
      - "մեծ ա, լավն ա,"
      - "գրում ա, գալիս ա, ուտում ա"
    supports: supported
    note: |
      direct statement that in Yerevan colloquial, 3sg `ա` replaces
      literary `է` — both as a copula in compound predicates
      (մեծ ա "is big") and as an auxiliary in simple/analytic
      predicates (գրում ա "[s/he] writes"). This is the single most
      recognisable register marker of Yerevan colloquial speech.
  - id: 6
    book: parnasyan
    page: 30
    y_range: [2820, 6010]
    verbatim_quote:
      - "ВСПОМОГАТЕЛЬНЫЙ ГЛАГОЛ"
      - "быть (есть)"
      - "выражают значение лица и в прошед"
    supports: supported
    note: |
      parnasyan's auxiliary-verb section header + paradigm + first
      Russian contrast. Establishes that the auxiliary "expresses
      person even in the past tense, in contrast to Russian" — the
      structural reason for consistent pro-drop documented in
      pro_drop.md. OCR'd at avg confidence 90 across fragments.
  - id: 7
    book: parnasyan
    page: 31
    y_range: [460, 1100]
    verbatim_quote:
      - "армянский вспомогательны"
      - "не имеет родового различия"
    supports: supported
    note: |
      parnasyan's two further Russian contrasts about the auxiliary:
      (a) Armenian aux *has* present-tense forms (Russian's null
      copula doesn't), (b) past-tense aux doesn't distinguish gender
      (Russian's был/была/было does). Both are Russian-L1 contrastive
      notes converted from agent-paraphrased to book-cited.
  - id: 8
    book: parnasyan
    page: 32
    y_range: [100, 600]
    verbatim_quote:
      - "в армянском языке, в отличие от русского, связка"
      - "всегда присутствует"
      - "характерная особенность"
    supports: supported
    note: |
      parnasyan's literary-norm baseline: "in Armenian, unlike
      Russian, the copula is always present. This is a characteristic
      feature of Armenian compound predicates." Sets the literary
      norm against which ghamoyan's colloquial copula-elision (cited
      from pro_drop.md and yerevan_consonant_reductions.md) is the
      register deviation.
gaps:
  - "Negation construction is handled in a separate Sakayan section (Unit 1's negation paradigms) — should become its own topic."
  - "Stress / prosody on the participle+auxiliary unit: not addressed by either source."
  - "Aspect disambiguation — Sakayan says the same form covers indefinite and continuous; how the contrast is expressed when context is insufficient is not discussed."
  - "Auxiliary contraction patterns in colloquial speech (e.g. clitic merge `գրումեմ`) — ghamoyan doesn't address; may live in chapter 5 or in actual recordings cited in the appendices."
---

# Present tense of regular verbs

Built from the **imperfective participle** (verb stem + `-ում`) plus
the **auxiliary form of `լինել`** "to be" inflected for person and
number. [#1] [#2] In Yerevan colloquial speech, the 3sg auxiliary
`է` is replaced by `ա`. [#5]

## Construction

For a regular verb, the present tense is formed in two steps:

1. Strip the infinitive ending (`-ել` for first-conjugation, `-ալ`
   for second-conjugation) and append `-ում` — the imperfective
   participle.
2. Follow with the auxiliary inflected for person/number:
   `եմ ես է ենք եք են`.

| infinitive | participle | finite (1sg) |
|------------|------------|--------------|
| գրել "write" | գրում | գրում եմ "I write" |
| կարդալ "read" | կարդում | կարդում եմ "I read" |

[#1] [#2]

## The full paradigm (literary norm)

For `գրել` "to write": [#3]

|     | singular        | plural             |
|-----|-----------------|--------------------|
| 1st | ես գրում եմ     | մենք գրում ենք     |
| 2nd | դու գրում ես    | դուք գրում եք      |
| 3rd | նա գրում է      | նրանք գրում են     |

The auxiliary forms `եմ ես է ենք եք են` are the same set used as the
present tense of `լինել` "to be" itself.

## One tense, two English readings

Eastern Armenian has **one** present tense covering both English
present indefinite ("I write") and present continuous ("I am
writing"). [#1] [#2] Disambiguation, when needed, is contextual.

Examples in context: [#4]

- *Ջոնը սովորում է հայերեն։* — "John is learning Armenian."
- *Նա արդեն կարդում է։* — "He is already reading."

## Yerevan colloquial: 3sg auxiliary `ա` for `է`

Ghamoyan documents the most recognisable colloquial-register marker
of Yerevan speech [#5]:

> "In folk-colloquial language, **`ա` is used as a linker [copula]**
> in the third person of compound predicates: `մեծ ա` ('is big'),
> `լավն ա` ('is good'), `կանաչ ա` ('is green'). **In simple
> predicates, `ա` replaces the auxiliary `է`**: `գրում ա`,
> `գալիս ա`, `ուտում ա`..."

So 3rd-singular present tense in colloquial Yerevan is:

| form | literary | colloquial |
|------|----------|------------|
| s/he writes | գրում **է** | գրում **ա** |
| s/he comes | գալիս **է** | գալիս **ա** |
| s/he eats | ուտում **է** | ուտում **ա** |
| she/he/it is big | մեծ **է** | մեծ **ա** |

Other persons (1sg `եմ`, 2sg `ես`, plurals) are not affected — the
substitution is specifically 3sg `է → ա`.

The same colloquial copula appears in many other ghamoyan examples
elsewhere in the book (e.g. p77 *"Թունդ կռիվ ա գնում դուրսը"* —
"there's a fierce fight going on outside") — the pattern is
ubiquitous in spontaneous Yerevan speech.

## Pro-drop and elision

Subject pronouns are routinely omitted; the auxiliary's
person/number ending is sufficient. See `topics/syntax/pro_drop.md`
for the full treatment, including ghamoyan's broader account of
auxiliary and copula elision in colloquial speech.

## Contrastive notes

**For an English L1**: the auxiliary attaches *after* the participle
(`գրում եմ` not `*եմ գրում`). The absence of a separate progressive
construction is the conceptual win — don't try to translate "I am
writing" with a different construction; it's the same form. Once you
add Yerevan colloquial: `գրում ա` for "s/he writes" instead of
`գրում է` is the single most useful register tell.

**For a Russian L1**: Russian present indicative carries person/number
on the verb itself (пишу, пишешь, пишет, …). Armenian splits the
work — the lexical content sits in the participle (`գրում`), the
person/number inflection in the auxiliary (`եմ ես է`). [#6] [#7]
Russian doesn't grammaticalise the indefinite/continuous split (unlike
English), so no extra mental work to map "I write" / "I am writing"
both onto `գրում եմ`. Yerevan-colloquial `ա` for `է` has no Russian
analogue — Russian's present-tense copula is null, not substituted —
but the phenomenon of register-specific 3rd-person forms (Russian's
"уважительное Вы" with 3pl agreement, formal vs informal) is a
familiar enough mental model for "different verb forms in different
registers."

Three explicit contrasts from Parnasyan worth internalising:

1. The Armenian auxiliary *has* present-tense forms; Russian's
   present-tense copula is null (`он студент`, no copula). [#7]
2. The Armenian past-tense auxiliary doesn't distinguish gender
   (`էր` for all of был/была/было). [#7]
3. **The copula is always present** in Armenian compound predicates
   — *"в армянском языке, в отличие от русского, связка всегда
   присутствует. Это характерная особенность армянского составного
   сказуемого."* [#8] This is the literary-norm baseline. In Yerevan
   colloquial that baseline gets relaxed (zero-copula sentences, see
   `topics/syntax/pro_drop.md`), so the literary↔colloquial contrast
   becomes a sharp register marker.

## Open questions / gaps

Mirrored from frontmatter:

- Negation construction → separate topic.
- Stress / prosody on the participle+auxiliary unit.
- Aspect disambiguation strategies.
- Auxiliary contraction patterns (clitic merge, `գրումեմ`) in
  colloquial speech — ghamoyan doesn't address directly; may live in
  appendix data.
