#!/usr/bin/env python3
"""Build the project's top-1000 lemma frequency list from extracted
sakayan + ghamoyan material.

Inputs (all already-extracted Armenian, from cards/):

    ../cards/sakayan/unit*_vocab.tsv      (col 0: Armenian)
    ../cards/sakayan/unit*_dialogue*.tsv  (col 1: Armenian)
    ../cards/sakayan/paradigms.tsv        (col 0: Armenian)
    ../cards/sakayan/chunks.tsv           (col 0: Armenian)
    ../cards/ghamoyan/fillers.tsv         (col 0: Armenian)

Output:

    out/our_top_1000.tsv  rank \t lemma \t count \t sources
    out/all_lemmas.tsv    every lemma found, ranked
    out/build_stats.txt   token counts per source, lemmatization stats

Methodology (documented in ../frequency-lists.md):

- Tokenize on Armenian word boundaries; strip Armenian punctuation.
- Lemmatize via rule-based suffix stripping (definite article + case
  endings + common verb forms). Same suffix rules as sakayan/glosser.py.
- Strip phonetic-hint annotations like `[ընթունել]` and pronoun
  parentheticals before tokenizing.
- Count distinct lemmas across all sources; record provenance.
- Output top-1000 plus the full ranked list.
"""

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Anki-ready card TSVs are at workspace root in cards/<source>/
CARDS = ROOT / "cards"
SAKAYAN_CARDS = CARDS / "sakayan"
GHAMOYAN_CARDS = CARDS / "ghamoyan"
OUT = HERE / "out"


# ---------- tokenization ----------

# Armenian intra-word punctuation (mid-word emphasis/question marks).
# These split words for tokenization regexes if not stripped first:
# `Քանի՞` → `Քանի՞` (literally Քանի + ՞ + space) breaks across the ՞.
INTRAWORD_PUNCT = re.compile(r"[՚-՟]")

# Armenian letter range plus the ev-ligature U+0587. Also allow `_` so
# multi-word units (MWUs) merged into single tokens by the MWU pass
# survive the tokenizer.
ARMENIAN_TOKEN = re.compile(r"[Ա-Ֆա-ֆև_]+")

# Strip phonetic-hint annotations like ` [phonetic]` and parenthetical
# usage notes like ` (sg/informal)` from a cell before tokenizing.
ANNOTATION_RE = re.compile(r"\s*[\[\(].*?[\]\)]")


# Multi-word units that should NOT be split during tokenization. Each
# pair is treated as a single lemma in the frequency list. Joiner is
# `_` because it survives our regex character class.
#
# Sources for inclusion:
# - high-frequency phrasal idioms from Sakayan dialogues (`մի քիչ`,
#   `ոչ ոք`, `դուր գալ`)
# - discourse markers from Ghamoyan Ch 4 §1 (`ի դեպ`, `համենայն դեպս`,
#   `ի վերջո`, `ի միջի այլոց`, `մի խոսքով`, `կարճ ասած`,
#   `այսպես ասած`, `կարծես թե`, `մի տեսակ`, `ըստ էության`,
#   `տենց բաներ`, `օֆ եսիմ`, `պարզ ա`)
# - common greetings (`բարև ձեզ`, `բարի լույս`, `բարի երեկո`,
#   `բարի գիշեր`)
# - quantifiers / time (`մի անգամ`, `մի օր`, `մի շարք`, `ամեն ինչ`,
#   `ամեն մարդ`, `ամեն օր`)
MWUS: list[str] = [
    "մի քիչ",
    "ոչ ոք",
    "ոչ մի",
    "դուր գալ",
    "ի դեպ",
    "համենայն դեպս",
    "ի վերջո",
    "ի միջի այլոց",
    "մի խոսքով",
    "կարճ ասած",
    "այսպես ասած",
    "կարծես թե",
    "մի տեսակ",
    "ըստ էության",
    "տենց բաներ",
    "օֆ եսիմ",
    "պարզ ա",
    "բարև ձեզ",
    "բարի լույս",
    "բարի երեկո",
    "բարի գիշեր",
    "մի անգամ",
    "մի օր",
    "մի շարք",
    "ամեն ինչ",
    "ամեն մարդ",
    "ամեն օր",
    "շատ լավ",
    "շատ քիչ",
    "շնորհակալ եմ",
    "շնորհավոր տարի",
]

_MWU_RE = re.compile(
    "|".join(re.escape(m) for m in sorted(MWUS, key=len, reverse=True))
)


def _merge_mwus(text: str) -> str:
    return _MWU_RE.sub(lambda m: m.group(0).replace(" ", "_"), text)


def tokenize(text: str) -> list[str]:
    text = ANNOTATION_RE.sub("", text)
    text = INTRAWORD_PUNCT.sub("", text)
    text = _merge_mwus(text)
    tokens = ARMENIAN_TOKEN.findall(text)
    # Normalize the spelled-out conjunction `եվ`/`Եվ` → ligature `և`.
    # Both forms are correct Armenian orthography but should fold to
    # one lemma in the deck; modern usage prefers the ligature.
    return ["և" if t.lower() == "եվ" else t for t in tokens]


# ---------- lemmatization (suffix-strip, same as sakayan/glosser.py) ----------

# Suffixes that get *stripped* — case/article endings on nouns. We do
# NOT strip `-ել` or `-ալ` here: those are the infinitive endings, and
# the infinitive IS the dictionary lemma in Armenian. Stripping them
# would conflate `գրել` "to write" with the verb stem `գր-`.
SUFFIXES: list[str] = sorted(
    [
        # plural + case + article combinations
        "երից", "ներից", "ներով", "ներում", "ների", "ներ",
        # case + article (singular). Notes:
        #   `-ն`, `-ս`, `-դ` all removed — they're definite-article /
        #     possessive markers only after vowel-final stems (rare in
        #     modern colloquial), and far more often part of the lemma
        #     itself (հայերեն, հայկական, տարեկան, ամեն, այսպես, անուն,
        #     երիտասարդ…). Stripping them caused systematic
        #     over-stripping bugs in validation. Slight under-
        #     aggregation of possessive forms (`անունս` "my name" vs
        #     `անուն` "name") is the right tradeoff.
        #   `-ում` removed — see SUBSTITUTIONS for proper handling.
        "ից", "ով", "ին", "ի", "ը",
    ],
    key=len,
    reverse=True,
)

# Substitutions: ending swap rules. Applied *before* plain stripping;
# the first rule that matches wins.
#
# - Abstract-noun genitive: `-ություն` ↔ `-ության / -ությամբ / …`.
# - Verb forms back to infinitive: `-ում` (imperfective participle)
#   and `-ած` (resultative participle) → infinitive `-ել` / `-ալ`.
#   We default to `-ել` because it's the more common conjugation;
#   `-ալ` verbs need a known-lemma override to recover correctly
#   (handled later via the known-lemma set).
SUBSTITUTIONS: list[tuple[str, str]] = [
    # abstract-noun paradigm
    ("ությունից", "ություն"),
    ("ությունը", "ություն"),
    ("ությամբ", "ություն"),
    ("ության", "ություն"),
    # a-stem oblique (`Ամերիկա` → `Ամերիկայից`, `Ամերիկայի`):
    # the glide `յ` between vowel-final stem and case ending must be
    # dropped together with the case marker.
    ("այից", "ա"),
    ("այով", "ա"),
    ("այում", "ա"),
    ("այի", "ա"),
    # verb form → infinitive (default to `-ել` class)
    ("ում", "ել"),
    ("ած", "ել"),
    ("ող", "ել"),
    ("ելու", "ել"),
    ("ալու", "ալ"),
    ("ելիս", "ել"),
    ("ալիս", "ալ"),
]


def lemmatize(
    token: str,
    known_lemmas: set[str] | None = None,
    inflected_to_lemma: dict[str, str] | None = None,
) -> str:
    """Return the candidate lemma. Order of resolution:

    1. Direct inflected→lemma lookup (paradigm forms — most reliable).
    2. Substitution rules (abstract noun, verb participles).
    3. Plain suffix stripping (case/article endings).
    4. `-ել ↔ -ալ` swap if known_lemmas suggests it.

    `-ն` and `-ս` are gated: only stripped when the preceding letter
    is a vowel (i.e. they're really a definite article on a
    vowel-final stem, not part of the lemma)."""
    # Inflected→lemma lookup runs first because short paradigm cells
    # (`եմ`, `ես`, `է`, `եք`) are 2-char and the length check below
    # would otherwise return them unchanged, skipping the mapping.
    if inflected_to_lemma and token in inflected_to_lemma:
        return inflected_to_lemma[token]
    # Multi-word units already merged via `_` are atomic; do not strip
    # suffixes (they're case-marked phrases like `ի դեպ`, `ըստ էության`
    # that survive as fixed expressions).
    if "_" in token:
        return token
    if len(token) < 3:
        return token

    # If the token itself is a dictionary headword, it's already a
    # lemma — don't strip. This catches `ինչպիսի`, `ուսուցչուհի`,
    # `միասին`, etc. that the suffix list would otherwise truncate
    # to non-words. Skip when no dictionary is available (graceful
    # degradation to plain rule-based stripping).
    try:
        d = _dict_headwords()
    except Exception:
        d = None
    if d and token.lower() in d:
        return token

    candidate = None
    matched_substitution = None
    for old, new in SUBSTITUTIONS:
        if token.endswith(old):
            candidate = token[: -len(old)] + new
            matched_substitution = old
            break
    if candidate is None:
        # Dictionary-aware suffix strip: prefer the strip that yields a
        # known headword. Falls back to the first match (longest, due
        # to SUFFIXES sort) if no strip is dictionary-confirmed. This
        # rescues cases like `ինչպիսին → ինչպիսի` (-ն, in dict) over
        # `ինչպիս` (-ին, not in dict).
        first_match = None
        for suf in SUFFIXES:
            if token.endswith(suf) and len(token) - len(suf) >= 2:
                cand = token[: -len(suf)]
                if d and cand.lower() in d:
                    candidate = cand
                    break
                if first_match is None:
                    first_match = cand
        if candidate is None:
            candidate = first_match
    if candidate is None:
        candidate = token

    # Gate the -ող and -ած substitutions: they're correct for verbal
    # participles (`գրող`/`գրած` → `գրել`) but wrong for adjectives or
    # agent nouns that share the suffix without being -ել verbs
    # (`կարող` "able" → would give `կարել` "Karelian / to sew", a
    # false match). Only accept the substitution if `candidate` is a
    # known lemma (lives in vocab/paradigm/filler/gap sources) — else
    # fall back to the original token.
    if known_lemmas and matched_substitution in ("ող", "ած"):
        if candidate not in known_lemmas:
            candidate = token

    if known_lemmas and candidate not in known_lemmas:
        if candidate.endswith("ել"):
            alt = candidate[:-2] + "ալ"
            if alt in known_lemmas:
                return alt
        elif candidate.endswith("ալ"):
            alt = candidate[:-2] + "ել"
            if alt in known_lemmas:
                return alt

    # Dictionary-aware possessive / definite-article strip. If the
    # candidate isn't itself a dictionary headword but candidate[:-1]
    # *is* (and the dropped char is `-ս/-դ/-ն`), the trailing letter
    # is almost certainly possessive (`անունս` "my name") or
    # definite-article (`տղան` "the boy"), and the lemma should fold
    # to the bare form. We do this AFTER the suffix-strip pass so
    # `երիտասարդ` (5+ chars, dictionary headword) isn't touched.
    if len(candidate) >= 4 and candidate[-1] in ("ս", "դ", "ն"):
        if d is not None and candidate.lower() not in d:
            stripped = candidate[:-1]
            if stripped.lower() in d:
                return stripped

    # Rescue under-strip: if the candidate is a non-headword but
    # `candidate + 'ի'` is a headword, the suffix-strip overshot a
    # genitive marker we should have kept. This rescues cases like
    # `ինչպիսին → ինչպիս → ինչպիսի` and `այսպիսին → այսպիս →
    # այսպիսի` where `-ին` strip was tried before noticing the
    # underlying lemma already ends in `-ի`.
    if d is not None and candidate.lower() not in d:
        cand_i = candidate.lower() + "ի"
        if cand_i in d:
            return candidate + "ի"

    # Generic paradigm-cell fallback. If the candidate isn't a known
    # headword but ends in a verb-paradigm tail (`-ենք` 1pl present /
    # subjunctive, `-եք` 2pl imperative / present, `-ինք` 1pl past)
    # AND the stem + `-ել` / `-ալ` / `-նել` / `-վել` is a dict
    # headword, fold to the infinitive. Catches `սկսենք → սկսել`,
    # `տեսեք → տեսնել`, `բերեք → բերել`, etc.
    if d is not None and candidate.lower() not in d:
        for tail in ("վենք", "վեք", "ենք", "եք", "ինք"):
            if candidate.endswith(tail) and len(candidate) - len(tail) >= 2:
                stem = candidate[: -len(tail)]
                for inf_tail in ("ել", "ալ", "նել", "վել"):
                    cand_inf = stem.lower() + inf_tail
                    if cand_inf in d:
                        return stem + inf_tail
                break
    return candidate


_DICT_HEADWORDS_CACHE: set[str] | None = None


def _dict_headwords() -> set[str]:
    """Real-lemma view onto `dictionary.load_dict()`. Filters out
    entries whose ONLY senses are paradigm-cell prose (e.g. kaikki
    stores `Հայաստանի` as its own entry with sense "dative singular
    of Հայաստան" — that's not a lemma we want lemmatization to
    short-circuit on)."""
    global _DICT_HEADWORDS_CACHE
    if _DICT_HEADWORDS_CACHE is not None:
        return _DICT_HEADWORDS_CACHE
    try:
        import dictionary
        d = dictionary.load_dict()
        real: set[str] = set()
        for word, entries in d.items():
            for _pos, glosses_str in entries:
                # If any sense survives the noise filter, treat as
                # a real lemma. Reuse `dictionary._is_noise` so the
                # filter rules stay in one place.
                for g in glosses_str.split(" | "):
                    g = g.strip()
                    if g and not dictionary._is_noise(g):
                        real.add(word)
                        break
                if word in real:
                    break
        _DICT_HEADWORDS_CACHE = real
    except Exception:
        _DICT_HEADWORDS_CACHE = set()
    return _DICT_HEADWORDS_CACHE


def collect_known_lemmas(sources: dict[str, list[str]]) -> set[str]:
    """Build a set of lemmas treated as canonical: vocab entries (already
    in dictionary form) and the verb infinitives from paradigm tags."""
    known: set[str] = set()
    for cell in sources.get("sakayan_vocab", []):
        cell = ANNOTATION_RE.sub("", cell)
        cell = INTRAWORD_PUNCT.sub("", cell)
        toks = ARMENIAN_TOKEN.findall(cell)
        if toks:
            known.add(toks[0].lower())
            if len(toks) > 1 and len(toks[0]) <= 2:
                known.add(toks[1].lower())
    for cell in sources.get("ghamoyan_fillers", []):
        cell = INTRAWORD_PUNCT.sub("", cell)
        toks = ARMENIAN_TOKEN.findall(cell)
        for t in toks:
            known.add(t.lower())
    return known


def collect_inflected_to_lemma() -> dict[str, str]:
    """Parse paradigms.tsv to build a direct inflected-form → infinitive
    mapping. Each paradigm row has a tag like `... verb:ունենալ tense:…`,
    and the Armenian cell (col 0) is the inflected form. So `ունեմ` →
    `ունենալ`, `ունենք` → `ունենալ`, etc. This catches conjugated forms
    that suffix-stripping alone can't lemmatize."""
    mapping: dict[str, str] = {}
    paradigms = SAKAYAN_CARDS / "paradigms.tsv"
    if not paradigms.exists():
        return mapping
    verb_re = re.compile(r"verb:([Ա-Ֆա-ֆև]+)")
    with paradigms.open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 3:
                continue
            armenian, _, tags = row[0], row[1], row[2]
            m = verb_re.search(tags)
            if not m:
                continue
            lemma = m.group(1)
            # The cell may be multi-word ("գրել եմ" perfect, "պիտի
            # գրեմ" mandative, "հոգնած եմ" resultative). For compound
            # forms only the *head* token (the participle / lexical
            # verb form) belongs to this verb's lemma; auxiliaries
            # like `եմ, ես, է` belong to `լինել`, modal `պիտի` is its
            # own lemma. Index only token[0] to avoid auxiliaries
            # leaking into the lexical-verb count.
            armenian = ANNOTATION_RE.sub("", armenian)
            armenian = INTRAWORD_PUNCT.sub("", armenian)
            tokens = ARMENIAN_TOKEN.findall(armenian)
            if tokens:
                mapping[tokens[0].lower()] = lemma
    # A few hand-pinned mappings for tokens that suffix-stripping
    # mauls but that aren't in any paradigm row:
    mapping.setdefault("պիտի", "պիտի")  # modal particle, treat as own lemma
    mapping.setdefault("պետք", "պետք")  # noun + modal
    # Stem-change nouns where suffix-stripping the inflected form
    # produces a non-lemma stem (`սեր` → `սիր-` in oblique cases):
    mapping.setdefault("սիրով", "սեր")
    mapping.setdefault("սիրուց", "սեր")
    mapping.setdefault("սիրում", "սեր")
    mapping.setdefault("սիրեր", "սեր")  # plural
    # Kinship-term oblique stems. These have radical stem changes in
    # the genitive that no rule-based stripper can recover from
    # (`եղբայր → եղբոր`, `քույր → քրոջ`, `հայր → հոր`, `մայր → մոր`,
    # `դուստր → դստեր`). Hand-pin every common case and possessive
    # form. Note: kaikki stores the oblique stem as its own entry
    # (`եղբոր (genitive of եղբայր)`), but it's not the lemma we
    # want for deck purposes.
    for inflected, lemma in [
        ("եղբայր", "եղբայր"),
        ("եղբոր", "եղբայր"),
        ("եղբորս", "եղբայր"),
        ("եղբորդ", "եղբայր"),
        ("եղբորից", "եղբայր"),
        ("եղբորով", "եղբայր"),
        ("քույր", "քույր"),
        ("քրոջ", "քույր"),
        ("քրոջս", "քույր"),
        ("քրոջդ", "քույր"),
        ("քրոջն", "քույր"),
        ("քրոջից", "քույր"),
        ("քրոջով", "քույր"),
        ("հայր", "հայր"),
        ("հոր", "հայր"),
        ("հորս", "հայր"),
        ("հորդ", "հայր"),
        ("մայր", "մայր"),
        ("մոր", "մայր"),
        ("մորս", "մայր"),
        ("մորդ", "մայր"),
        # vowel-syncope nouns (`բժիշկ → բժշկ-` in oblique cases)
        ("բժիշկ", "բժիշկ"),
        ("բժշկի", "բժիշկ"),
        ("բժշկից", "բժիշկ"),
        ("բժշկով", "բժիշկ"),
        # ով → "who" oblique stem `ում`
        ("ումից", "ով"),
        ("ումով", "ով"),
        # `կողքիս` "by my side" — locative + 1sg-poss, lemma `կողք`.
        # kaikki mistakenly glosses this as "Colchis"; hand-pin
        # to override.
        ("կողքիս", "կողք"),
        ("կողքից", "կողք"),
        ("կողքին", "կողք"),
        # `տես` 2sg-imperative of `տեսնել`; kaikki has neither.
        ("տես", "տեսնել"),
        ("տեսեք", "տեսնել"),
        ("տեսնենք", "տեսնել"),
        # `գիտել` paradigm cells that lack their own dict entries
        ("գիտեմ", "գիտել"),
        ("գիտես", "գիտել"),
        ("գիտի", "գիտել"),
        ("գիտենք", "գիտել"),
        ("գիտեք", "գիտել"),
        ("գիտեն", "գիտել"),
    ]:
        mapping.setdefault(inflected, lemma)
    return mapping


# ---------- source readers ----------


def read_tsv_column(path: Path, col: int) -> list[str]:
    if not path.exists():
        return []
    out: list[str] = []
    with path.open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) > col:
                out.append(row[col])
    return out


def _is_armenian_text(text: str, thresh: float = 0.5) -> bool:
    """True when at least `thresh` of the alphabetic characters in
    `text` are in the Armenian unicode block. Used to filter raw
    JSONL extractions: sakayan's PDF carries large stretches of
    English prose alongside the Armenian content; we want only
    the Armenian cells in the frequency corpus.
    """
    if not text or not text.strip():
        return False
    arm = sum(1 for c in text if 0x0530 <= ord(c) <= 0x058F)
    letters = sum(1 for c in text if c.isalpha())
    return letters > 0 and arm / letters >= thresh


def _load_jsonl_armenian(path) -> list[str]:
    """Return Armenian-text cells from a `<book>/out/full.jsonl`.
    Each cell is one JSONL entry's text. Skips cells whose alpha
    characters are <50% Armenian (so English instructional prose
    in sakayan and Russian explanatory prose in parnasyan/tioyan
    don't pollute the frequency counts).
    """
    import json
    out: list[str] = []
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = e.get("text", "")
            if _is_armenian_text(t):
                out.append(t)
    return out


def collect_sources() -> dict[str, list[str]]:
    """Return {source_name: [armenian_text_strings]}."""
    sources: dict[str, list[str]] = {}

    vocab_files = sorted(SAKAYAN_CARDS.glob("unit*_vocab.tsv"))
    sources["sakayan_vocab"] = [
        cell for f in vocab_files for cell in read_tsv_column(f, 0)
    ]

    dialogue_files = sorted(SAKAYAN_CARDS.glob("unit*_dialogue*.tsv"))
    sources["sakayan_dialogue"] = [
        cell for f in dialogue_files for cell in read_tsv_column(f, 1)
    ]

    sources["sakayan_paradigms"] = read_tsv_column(
        SAKAYAN_CARDS / "paradigms.tsv", 0
    )
    sources["sakayan_chunks"] = read_tsv_column(
        SAKAYAN_CARDS / "chunks.tsv", 0
    )
    sources["ghamoyan_fillers"] = read_tsv_column(
        GHAMOYAN_CARDS / "fillers.tsv", 0
    )

    # Raw JSONL extractions — the underlying corpus, not just the
    # already-curated card content. Vastly expands the lemma pool
    # (sakayan unit prose, exercises; ghamoyan five chapters).
    # The Armenian-text filter drops English/Russian prose cells.
    sources["sakayan_jsonl"] = _load_jsonl_armenian(
        ROOT / "sakayan" / "out" / "full.jsonl"
    )
    sources["ghamoyan_jsonl"] = _load_jsonl_armenian(
        ROOT / "ghamoyan" / "out" / "full.jsonl"
    )
    return sources


# ---------- pipeline ----------


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = collect_sources()
    known = collect_known_lemmas(sources)
    inflected_map = collect_inflected_to_lemma()

    counts: Counter[str] = Counter()
    provenance: dict[str, set[str]] = defaultdict(set)
    stats: dict[str, dict] = {}

    for source_name, cells in sources.items():
        tokens: list[str] = []
        for cell in cells:
            tokens.extend(tokenize(cell))
        lemmas = [lemmatize(t.lower(), known, inflected_map) for t in tokens]
        counts.update(lemmas)
        for lemma in lemmas:
            provenance[lemma].add(source_name)
        stats[source_name] = {
            "cells": len(cells),
            "tokens": len(tokens),
            "unique_lemmas": len(set(lemmas)),
        }

    # Filter — minimum-sane lemma length, and drop pure-digit / pure-
    # punctuation residues. Also skip-list known extraction artifacts
    # — `իկ`, `ուկ` are diminutive-suffix fragments where unit09_vocab
    # rows got truncated (`քամիկ → իկ`, `տաքուկ → ուկ`); they ended
    # up as deck rows with wrong "wind" / "warm" translations. The
    # underlying TSV needs an upstream fix; until then, suppress.
    EXTRACTION_BUG_FRAGMENTS = {"իկ", "ուկ"}
    counts = Counter({
        lemma: n for lemma, n in counts.items()
        if len(lemma) >= 2
        and ARMENIAN_TOKEN.fullmatch(lemma)
        and lemma not in EXTRACTION_BUG_FRAGMENTS
    })

    ranked = counts.most_common()
    # Buffer beyond 1000: deck-build skips ~17% of these (no
    # translation source / inflected duplicates / personal names).
    # Emitting top-1500 lets `build_deck.py --limit 1000` actually
    # reach 1000 emitted cards. Lemmas at ranks 1001-1500 still
    # have count ≥ 8 in the current corpus — well above hapax
    # noise.
    top_1000 = ranked[:1500]

    # Write top-1000 with provenance and rank.
    top_path = OUT / "our_top_1000.tsv"
    with top_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for rank, (lemma, count) in enumerate(top_1000, 1):
            srcs = ",".join(sorted(provenance[lemma]))
            w.writerow([rank, lemma, count, srcs])

    # Full ranked list for reference / future filtering.
    full_path = OUT / "all_lemmas.tsv"
    with full_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for rank, (lemma, count) in enumerate(ranked, 1):
            srcs = ",".join(sorted(provenance[lemma]))
            w.writerow([rank, lemma, count, srcs])

    # Build stats.
    stats_path = OUT / "build_stats.txt"
    with stats_path.open("w", encoding="utf-8") as f:
        f.write("Per-source token / lemma counts\n")
        f.write("=" * 60 + "\n")
        for name, s in stats.items():
            f.write(f"  {name:25s}  cells={s['cells']:6d}  "
                    f"tokens={s['tokens']:7d}  "
                    f"unique_lemmas={s['unique_lemmas']:6d}\n")
        total_tokens = sum(s["tokens"] for s in stats.values())
        total_lemmas = len(counts)
        f.write("\n")
        f.write(f"Total tokens (all sources): {total_tokens}\n")
        f.write(f"Total distinct lemmas:      {total_lemmas}\n")
        f.write(f"Top-1000 covers ranks 1..1000 of {total_lemmas}\n")
        # Rough Zipf check: top-N coverage of total tokens.
        for n in [10, 50, 100, 500, 1000]:
            cover = sum(c for _, c in ranked[:n])
            pct = 100.0 * cover / total_tokens if total_tokens else 0
            f.write(f"  top-{n:4d} covers {cover:7d} tokens "
                    f"({pct:5.1f}% of corpus)\n")

    print(f"Wrote {top_path.name} ({len(top_1000)} entries)", file=sys.stderr)
    print(f"Wrote {full_path.name} ({len(ranked)} entries)", file=sys.stderr)
    print(f"Wrote {stats_path.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
