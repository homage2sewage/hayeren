"""Local Armenian dictionary lookup, built from kaikki.org's Wiktionary
dump (`data/armenian.jsonl`, compacted to `data/armenian_dict.tsv` by
`build_dictionary.py`). 22 000 entries; loads in <1 s.

Used as the primary backup translation source after textbook vocab,
*replacing* live Wiktionary API calls (which got us rate-limited).
The trade-off: slightly older Wiktionary snapshot; updated by
re-downloading the JSONL and re-running `build_dictionary.py`.

Public surface:

    load_dict() → dict[str, list[(pos, glosses_str)]]
    lookup(word) → str    # best single English gloss (filtered)
    lookup_full(word) → list[(pos, gloss_str)]
"""

import csv
import re
import threading
from pathlib import Path
from typing import Optional


HERE = Path(__file__).resolve().parent
DICT_PATH = HERE / "data" / "armenian_dict.tsv"


_DICT: Optional[dict[str, list[tuple[str, str]]]] = None
_LOAD_LOCK = threading.Lock()


def load_dict() -> dict[str, list[tuple[str, str]]]:
    """Lazy-load the compact TSV into memory. Returns
    {lemma_lower: [(pos, glosses_pipe_joined), …]}."""
    global _DICT
    if _DICT is not None:
        return _DICT
    with _LOAD_LOCK:
        if _DICT is not None:
            return _DICT
        d: dict[str, list[tuple[str, str]]] = {}
        if not DICT_PATH.exists():
            _DICT = d
            return d
        with DICT_PATH.open(encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) != 3:
                    continue
                word, pos, glosses = row
                d.setdefault(word.lower(), []).append((pos, glosses))
        _DICT = d
        return d


# Patterns that suggest a gloss isn't a useful translation:
#   morphology-only entries: "եմ (2 s pres)", "դու (gen p)"
#   alphabet-letter descriptions: "The 11th letter of Armenian alphabet…"
#   pure inflection-of references with no semantic content
_NOISE_PATTERNS = [
    re.compile(r"^[Ա-Ֆա-ֆև]+\s*\([^)]+\)$"),  # `եմ (2 s pres)`
    re.compile(r"letter of (Armenian|the) alphabet", re.IGNORECASE),
    re.compile(r"^The \d+(st|nd|rd|th) letter", re.IGNORECASE),
    re.compile(r"^inflection of "),
    # kaikki paradigm-cell prose that isn't a real translation:
    #   "dative singular of Հայաստան", "nominative plural of …",
    #   "genitive singular second-person possessive of …", etc.
    re.compile(
        r"^(?:nominative|accusative|dative|genitive|ablative|"
        r"instrumental|locative|vocative)\b",
        re.IGNORECASE,
    ),
]


def _is_noise(gloss: str) -> bool:
    for pat in _NOISE_PATTERNS:
        if pat.search(gloss):
            return True
    return False


def lookup(word: str) -> str:
    """Best single English gloss. Picks the first non-noise gloss from
    the first non-name part-of-speech entry. Returns "" on miss.

    For multi-word units glued with `_` (the build pipeline's MWU
    convention), tries the dictionary with the underscore replaced by
    a space — kaikki.org stores phrasal entries with literal spaces."""
    key = word.lower()
    d = load_dict()
    entries = d.get(key, [])
    if not entries and "_" in key:
        entries = d.get(key.replace("_", " "), [])
    if not entries:
        return ""
    # Prefer Verb / Noun / Adjective / Adverb / Pronoun / Particle /
    # Conjunction / Interjection / Determiner over `name`.
    pos_priority = {
        "verb": 0, "noun": 1, "adj": 2, "adv": 3, "pron": 4,
        "particle": 5, "conj": 6, "intj": 7, "det": 8, "prep": 9,
        "phrase": 10, "name": 90, "letter": 99,
    }

    def sort_key(e: tuple[str, str]) -> int:
        return pos_priority.get(e[0].lower(), 50)

    for pos, glosses_str in sorted(entries, key=sort_key):
        for g in glosses_str.split(" | "):
            g = g.strip()
            if g and not _is_noise(g):
                # Trim parenthetical clutter to keep the gloss short.
                # Keep main meaning before any "(disambiguation)" tail.
                short = re.sub(r"\s*\([^)]*\)\s*", " ", g).strip()
                if short:
                    return short[:80]
    return ""


def lookup_full(word: str) -> list[tuple[str, str]]:
    """All (pos, glosses_pipe_joined) tuples for the word."""
    return load_dict().get(word.lower(), [])
