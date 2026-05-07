#!/usr/bin/env python3
"""Build the project's top-1000 lemma frequency list from extracted
sakayan + ghamoyan material.

Inputs (all already-extracted Armenian):

    ../sakayan/out/by-unit/unit*_vocab.tsv      (col 0: Armenian)
    ../sakayan/out/by-unit/unit*_dialogue*.tsv  (col 1: Armenian)
    ../sakayan/out/by-unit/paradigms.tsv        (col 0: Armenian)
    ../sakayan/out/by-unit/chunks.tsv           (col 0: Armenian)
    ../ghamoyan/out/fillers.tsv                 (col 0: Armenian)

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
SAKAYAN_OUT = ROOT / "sakayan" / "out" / "by-unit"
GHAMOYAN_OUT = ROOT / "ghamoyan" / "out"
OUT = HERE / "out"


# ---------- tokenization ----------

# Armenian intra-word punctuation (mid-word emphasis/question marks).
# These split words for tokenization regexes if not stripped first:
# `Քանի՞` → `Քանի՞` (literally Քանի + ՞ + space) breaks across the ՞.
INTRAWORD_PUNCT = re.compile(r"[՚-՟]")

# Armenian letter range plus the ev-ligature U+0587.
ARMENIAN_TOKEN = re.compile(r"[Ա-Ֆա-ֆև]+")

# Strip phonetic-hint annotations like ` [phonetic]` and parenthetical
# usage notes like ` (sg/informal)` from a cell before tokenizing.
ANNOTATION_RE = re.compile(r"\s*[\[\(].*?[\]\)]")


def tokenize(text: str) -> list[str]:
    text = ANNOTATION_RE.sub("", text)
    text = INTRAWORD_PUNCT.sub("", text)
    return ARMENIAN_TOKEN.findall(text)


# ---------- lemmatization (suffix-strip, same as sakayan/glosser.py) ----------

# Suffixes that get *stripped* — case/article endings on nouns. We do
# NOT strip `-ել` or `-ալ` here: those are the infinitive endings, and
# the infinitive IS the dictionary lemma in Armenian. Stripping them
# would conflate `գրել` "to write" with the verb stem `գր-`.
SUFFIXES: list[str] = sorted(
    [
        # plural + case + article combinations
        "երից", "ներից", "ներով", "ներում", "ների", "ներ",
        # case + article (singular)
        "ից", "ով", "ին", "ի", "ն", "ը", "ս", "դ",
        # NB: `-ում` removed from the strip list — see SUBSTITUTIONS,
        # where it gets remapped back to the verb's `-ել/-ալ` infinitive
        # form rather than chopped to a bare stem.
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
    """
    if len(token) < 3:
        return token

    if inflected_to_lemma and token in inflected_to_lemma:
        return inflected_to_lemma[token]

    candidate = None
    for old, new in SUBSTITUTIONS:
        if token.endswith(old):
            candidate = token[: -len(old)] + new
            break
    if candidate is None:
        for suf in SUFFIXES:
            if token.endswith(suf) and len(token) - len(suf) >= 2:
                candidate = token[: -len(suf)]
                break
    if candidate is None:
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
    return candidate


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
    paradigms = SAKAYAN_OUT / "paradigms.tsv"
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
            # The cell may be multi-word (e.g. "պիտի գրեմ"); each
            # constituent token gets mapped to the verb's lemma so a
            # later occurrence of `պիտի` or `գրեմ` resolves correctly.
            armenian = ANNOTATION_RE.sub("", armenian)
            armenian = INTRAWORD_PUNCT.sub("", armenian)
            for tok in ARMENIAN_TOKEN.findall(armenian):
                mapping[tok.lower()] = lemma
    # A few hand-pinned mappings for tokens that suffix-stripping
    # mauls but that aren't in any paradigm row:
    mapping.setdefault("պիտի", "պիտի")  # modal particle, treat as own lemma
    mapping.setdefault("պետք", "պետք")  # noun + modal
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


def collect_sources() -> dict[str, list[str]]:
    """Return {source_name: [armenian_text_strings]}."""
    sources: dict[str, list[str]] = {}

    vocab_files = sorted(SAKAYAN_OUT.glob("unit*_vocab.tsv"))
    sources["sakayan_vocab"] = [
        cell for f in vocab_files for cell in read_tsv_column(f, 0)
    ]

    dialogue_files = sorted(SAKAYAN_OUT.glob("unit*_dialogue*.tsv"))
    sources["sakayan_dialogue"] = [
        cell for f in dialogue_files for cell in read_tsv_column(f, 1)
    ]

    sources["sakayan_paradigms"] = read_tsv_column(
        SAKAYAN_OUT / "paradigms.tsv", 0
    )
    sources["sakayan_chunks"] = read_tsv_column(
        SAKAYAN_OUT / "chunks.tsv", 0
    )
    sources["ghamoyan_fillers"] = read_tsv_column(
        GHAMOYAN_OUT / "fillers.tsv", 0
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
    # punctuation residues.
    counts = Counter({
        lemma: n for lemma, n in counts.items()
        if len(lemma) >= 2 and ARMENIAN_TOKEN.fullmatch(lemma)
    })

    ranked = counts.most_common()
    top_1000 = ranked[:1000]

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
