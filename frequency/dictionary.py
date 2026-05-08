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


# A frequency-ranked Armenian word can't be high-frequency *because*
# of an obscure-language sense — words like `բաց` are top-1000
# because they mean "open," not because the same string happens to
# be wiktionary's name for a Caucasian minority language. So if a
# noun gloss matches the `X (language)` shape AND the word has any
# non-language sense in another POS section, skip the language
# gloss and fall through. Words whose only senses are language-
# names (հայերեն, անգլերեն) keep them.
_LANGUAGE_GLOSS = re.compile(
    r"^(?:[A-Z][a-z\-]+(?:\s[A-Z][a-z\-]+)?\s*\(language\)|"
    r"[A-Z][a-z\-]+,\s+a\s+(?:minority|regional|extinct)?\s*language\b)",
)


def _looks_like_language_name(gloss: str) -> bool:
    return bool(_LANGUAGE_GLOSS.match(gloss))


def _has_non_language_sense(entries: list[tuple[str, str]]) -> bool:
    for _pos, glosses_str in entries:
        for g in glosses_str.split(" | "):
            g = g.strip()
            if g and not _is_noise(g) and not _looks_like_language_name(g):
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
    # Preserve kaikki's natural POS order — Wiktionary lists the
    # primary sense first, and an arbitrary verb>noun>adj priority
    # mistranslates words whose primary sense is non-noun (e.g.
    # `տարեկան` whose three POS entries are adj "annual" / adv
    # "yearly" / noun "rye"; with noun-priority we'd surface "rye").
    # Only deprioritize entries that are rarely the useful gloss:
    # personal/place `name` and alphabet-`letter` descriptions.
    # Python's `sorted` is stable, so equal-priority entries keep
    # their kaikki order.
    pos_priority = {"name": 90, "letter": 99}

    def sort_key(e: tuple[str, str]) -> int:
        return pos_priority.get(e[0].lower(), 50)

    skip_language = _has_non_language_sense(entries)
    for pos, glosses_str in sorted(entries, key=sort_key):
        for g in glosses_str.split(" | "):
            g = g.strip()
            if not g or _is_noise(g):
                continue
            if skip_language and _looks_like_language_name(g):
                continue
            # Trim parenthetical clutter to keep the gloss short.
            # Keep main meaning before any "(disambiguation)" tail.
            short = re.sub(r"\s*\([^)]*\)\s*", " ", g).strip()
            if short:
                return short[:80]
    return ""


def lookup_full(word: str) -> list[tuple[str, str]]:
    """All (pos, glosses_pipe_joined) tuples for the word."""
    return load_dict().get(word.lower(), [])
