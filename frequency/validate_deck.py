#!/usr/bin/env python3
"""Phase 1 mechanical-lint validator for `cards/top_1000.tsv`.

Run after `build_deck.py`. Surfaces every category of error the
user has already hit (see `walks/2026-05-07-deck-validation-plan.md`),
so we can fix them upstream or accept them as a known-issue list.

No network calls; uses only the local Wiktionary-dump dictionary
(`dictionary.py`). Pure stdlib.

Output:

    out/deck_validation.tsv   one finding per row
    out/deck_validation.md    grouped human summary

Exit code: 0 on success regardless of findings (validation is
diagnostic, not gate-blocking). Use `--strict` to exit 1 if any
`error`-severity findings exist.
"""

from __future__ import annotations

import argparse
import csv
import html as _html
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

# We import dictionary lazily-ish; placement matches build_deck.
import dictionary  # noqa: E402

HERE = Path(__file__).resolve().parent
DECK_PATH = HERE.parent / "cards" / "top_1000.tsv"
OUT_DIR = HERE / "out"
TSV_OUT = OUT_DIR / "deck_validation.tsv"
MD_OUT = OUT_DIR / "deck_validation.md"


# ---- known shapes & allow-lists -------------------------------------------

# Proper nouns that are first-and-foremost Armenian words and belong
# in any Armenian top-1000. Anything else flagged as `pos=name` only
# in the dictionary gets surfaced.
KEEP_NAMES = {
    # Armenia & its core geography (first-and-foremost Armenian words).
    "հայաստան", "հայ", "հայերեն", "հայկական",
    "երևան", "արարատ", "սևան", "կոտայք", "շիրակ",
    "գեղարքունիք", "լոռի", "սյունիք", "տավուշ", "վայոց",
    # Other countries / regions Armenian dialogues commonly mention —
    # these are normal Armenian-language nouns when used in Armenian
    # text, not foreign loanwords.
    "եվրոպա", "ռուսաստան", "ամերիկա", "մոսկվա",
    "գերմանիա", "հունաստան", "ֆրանսիա", "իտալիա",
    "չինաստան", "ճապոնիա", "թուրքիա", "վրաստան",
    "ադրբեջան", "իրան",
}

# Ethnonyms / nationality adjectives we've seen leak from Wiktionary
# senses — `կարող → "Karelian"` was the canonical bug.
FALSE_FRIEND_PATTERNS = [
    re.compile(r"\bKarelian\b", re.IGNORECASE),
    re.compile(r"\bGagauz\b", re.IGNORECASE),
    re.compile(r"\bChuvash\b", re.IGNORECASE),
]

# `dictionary.lookup` already filters most noise but the Wiktionary
# fallback historically shipped some through. Re-check at the deck
# layer so we catch any future regression.
NOISE_PATTERNS = [
    re.compile(r"^[Ա-Ֆա-ֆև]+\s*\([^)]+\)$"),
    re.compile(r"\bletter of (?:the )?(?:Armenian )?alphabet", re.IGNORECASE),
    re.compile(r"^The \d+(?:st|nd|rd|th) letter", re.IGNORECASE),
    re.compile(r"^inflection of "),
    # kaikki uses prose like "dative singular of X" / "nominative
    # plural of Y" for paradigm-cell entries that shouldn't show up
    # as deck translations.
    re.compile(
        r"^(?:nominative|accusative|dative|genitive|ablative|"
        r"instrumental|locative|vocative)\s+(?:singular|plural)\s+of\s+",
        re.IGNORECASE,
    ),
    re.compile(
        r"^(?:nominative|accusative|dative|genitive|ablative|"
        r"instrumental|locative|vocative)\s+singular\s+second-person",
        re.IGNORECASE,
    ),
    re.compile(r"^[a-z]+\s+(?:singular|plural)\s+of\s+", re.IGNORECASE),
]

# Possessive / definite-article inflection markers. If the lemma
# ends in one of these AND the stripped form is in the dictionary,
# that's an inflected leak the lemmatizer should have normalized.
POSSESSIVE_TAILS = ("ս", "դ", "ն")

# Verb paradigm-cell markers that should have folded back to an
# infinitive (-ել / -ալ).
PARADIGM_TAILS = (
    "ենք", "եք", "ինք", "ին",
    "վենք", "վեք", "վեցինք", "վեցին",
    "ուց", "ում",
)

# Common derivational endings that, if missing the final -ի or -ություն,
# point to a truncated stem (e.g. ուսուցչուհ → ուսուցչուհի).
TRUNCATION_RE_TAIL_CANDIDATES = ("ի", "ություն", "ություն")


# ---- I/O ------------------------------------------------------------------

Row = tuple[str, str, str]  # (lemma, translation, tags_field)


_TAG_RE = re.compile(r"<[^>]+>")


def plain_gloss(s: str) -> str:
    """Strip the Anki HTML rendering back to the plain
    `English / Russian` form the content checks expect. `<br>` is the
    EN/RU boundary → ` / `."""
    s = re.sub(r"<br\s*/?>", " / ", s)
    s = _TAG_RE.sub("", s)
    return _html.unescape(s).strip()


def load_deck_meta() -> dict[str, tuple[str, str]]:
    """lemma → (rank, src) from build_deck's sidecar. Lets the
    validator recover rank/source even though the card's tag column
    is now just `frequency top-1000` (rank/src dropped per 2026-06-03)."""
    path = HERE / "out" / "deck_meta.tsv"
    meta: dict[str, tuple[str, str]] = {}
    if path.exists():
        with path.open(encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            next(reader, None)  # header
            for row in reader:
                if len(row) >= 3:
                    meta[row[0]] = (row[1], row[2])
    return meta


def read_deck(path: Path = DECK_PATH) -> list[Row]:
    meta = load_deck_meta()
    rows: list[Row] = []
    with path.open(encoding="utf-8") as f:
        for r in csv.reader(f, delimiter="\t"):
            if len(r) < 3:
                continue
            lemma, gloss, tags = r[0], plain_gloss(r[1]), r[2]
            # Reconstruct rank/src into the tags string so the existing
            # rank_of()/`src-…` checks keep working unchanged.
            if lemma in meta:
                rank, src = meta[lemma]
                tags = (f"frequency top-1000 rank-{rank} src-{src}"
                        if rank else f"frequency core-inject src-{src}")
            rows.append((lemma, gloss, tags))
    return rows


def rank_of(tags_field: str) -> int:
    m = re.search(r"rank-(\d+)", tags_field)
    return int(m.group(1)) if m else -1


# ---- per-category checks --------------------------------------------------

Finding = dict  # {severity, rank, lemma, translation, category, hint}


def _emit(findings: list[Finding], severity: str, rank: int, lemma: str,
          translation: str, category: str, hint: str = "") -> None:
    findings.append({
        "severity": severity,
        "rank": rank,
        "lemma": lemma,
        "translation": translation,
        "category": category,
        "hint": hint,
    })


def check_empty(rows: list[Row], findings: list[Finding]) -> None:
    for lemma, tr, tags in rows:
        if not tr.strip():
            _emit(findings, "warning", rank_of(tags), lemma, tr,
                  "empty-translation",
                  "no card source or local dict entry covered this lemma")


def check_noise(rows: list[Row], findings: list[Finding]) -> None:
    for lemma, tr, tags in rows:
        if not tr:
            continue
        for pat in NOISE_PATTERNS:
            if pat.search(tr):
                _emit(findings, "error", rank_of(tags), lemma, tr,
                      "noise-translation",
                      f"matches noise pattern: {pat.pattern}")
                break


def check_false_friend(rows: list[Row], findings: list[Finding]) -> None:
    for lemma, tr, tags in rows:
        if not tr:
            continue
        for pat in FALSE_FRIEND_PATTERNS:
            if pat.search(tr):
                _emit(findings, "error", rank_of(tags), lemma, tr,
                      "false-friend",
                      f"ethnonym sense leaked: {pat.pattern}")
                break


def check_truncated(rows: list[Row], findings: list[Finding]) -> None:
    """Lemma not in dict, but dict has lemma+`ի`, suggesting we cut
    off an inflectional suffix from a word whose citation form ends
    in `-ի` (e.g. `ուղի`, `գինի`, `բանալի`).

    NOTE: we deliberately do NOT test the `-ություն` tail. The
    lemmatizer (build_ours.py:169-172) only *normalizes* inflected
    `-ություն` forms back to `-ություն`; it never strips `-ություն`
    down to a bare stem. So a deck lemma can never be a `-ություն`
    truncation artifact. Adding the tail only produces false
    positives on legitimate base/abstract-noun derivational pairs
    (`միավոր`/`միավորություն`, `պայմանավորված`/`պայմանավորվածություն`)
    where the base happens to be absent from the kaikki dump."""
    d = dictionary.load_dict()
    for lemma, tr, tags in rows:
        if "_" in lemma or len(lemma) < 3:
            continue
        if lemma.lower() in d:
            continue
        # Don't double-count proper-noun cases (handled separately).
        for tail in ("ի",):
            cand = lemma.lower() + tail
            if cand in d:
                _emit(findings, "error", rank_of(tags), lemma, tr,
                      "truncated-lemma",
                      f"dictionary has `{cand}` — `{tail}` was stripped")
                break


def check_inflected_leak(rows: list[Row], findings: list[Finding]) -> None:
    """Lemma ends in possessive or definite-article suffix AND the
    stripped form exists in the dictionary AND the original lemma is
    NOT itself a dictionary entry. The last clause is the key
    de-noising step: `մարդ`, `չորս`, `դուրս`, `ինքն` all look like
    they end in `-ս/-դ/-ն` but are valid lemmas in their own right."""
    d = dictionary.load_dict()
    for lemma, tr, tags in rows:
        if "_" in lemma or len(lemma) < 4:
            continue
        if lemma.lower() in d:
            # The lemma is a dictionary headword — the suffix lookalike
            # is part of the word itself, not an inflection.
            continue
        for tail in POSSESSIVE_TAILS:
            if lemma.endswith(tail):
                stripped = lemma[: -len(tail)]
                if stripped.lower() in d:
                    _emit(findings, "error", rank_of(tags), lemma, tr,
                          "inflected-leak",
                          f"`{stripped}` in dict — `{tail}` is "
                          f"possessive/article")
                    break


def check_paradigm_leak(rows: list[Row], findings: list[Finding]) -> None:
    """Verb-form tail that should have collapsed to an infinitive."""
    d = dictionary.load_dict()
    for lemma, tr, tags in rows:
        if "_" in lemma or len(lemma) < 4:
            continue
        # If we already have a translation it might be valid (some
        # paradigm-cells were pinned manually). Only flag if neither
        # the lemma nor a plausible -ել / -ալ infinitive is in dict.
        if lemma.lower() in d:
            continue
        for tail in PARADIGM_TAILS:
            if lemma.endswith(tail):
                # Try common infinitive recoveries.
                stem = lemma[: -len(tail)]
                for inf_tail in ("ել", "ալ", "նել", "վել"):
                    cand = stem + inf_tail
                    if cand.lower() in d:
                        _emit(findings, "error", rank_of(tags), lemma, tr,
                              "paradigm-leak",
                              f"`{cand}` in dict — `{lemma}` looks like "
                              f"a paradigm cell")
                        break
                else:
                    continue
                break


def check_proper_noun(rows: list[Row], findings: list[Finding]) -> None:
    d = dictionary.load_dict()
    for lemma, tr, tags in rows:
        if "_" in lemma:
            continue
        if lemma.lower() in KEEP_NAMES:
            continue
        entries = d.get(lemma.lower(), [])
        if not entries:
            continue
        if all(pos.lower() == "name" for pos, _ in entries):
            _emit(findings, "error", rank_of(tags), lemma, tr,
                  "proper-noun-foreign",
                  "dictionary classifies as `name` only — surname/place "
                  "not in KEEP_NAMES")


def check_mwu_leak(rows: list[Row], findings: list[Finding],
                   mwus: Iterable[str]) -> None:
    """If a MWU and both its component words show up at high frequency,
    the merging missed cases. We don't reject — just warn."""
    deck_lemmas = {r[0] for r in rows}
    for mwu in mwus:
        joined = mwu.replace(" ", "_")
        parts = mwu.split()
        if joined in deck_lemmas and all(p in deck_lemmas for p in parts):
            # Note: some component words (`մի`, `ոչ`) are independently
            # high-frequency and legitimately appear on their own, so
            # this is a soft warning — we surface it for review only
            # when the joined form's *count* might be incomplete.
            _emit(findings, "warning", -1, joined, "",
                  "mwu-leak",
                  f"both `{joined}` and components {parts} appear — "
                  "review whether all occurrences merged")


def check_duplicate_translation(rows: list[Row], findings: list[Finding]) -> None:
    by_tr: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for lemma, tr, tags in rows:
        if not tr.strip():
            continue
        # Strip language-divider for comparison: "X / Y" vs "X" etc.
        key = tr.strip().lower()
        by_tr[key].append((rank_of(tags), lemma))
    for tr, occurrences in by_tr.items():
        if len(occurrences) > 1:
            lemmas = ", ".join(f"{l} (#{r})" for r, l in
                               sorted(occurrences))
            _emit(findings, "warning", min(r for r, _ in occurrences),
                  lemmas, tr, "duplicate-translation",
                  f"{len(occurrences)} lemmas map to identical gloss")


def check_eu_ligature(rows: list[Row], findings: list[Finding]) -> None:
    for lemma, tr, tags in rows:
        if lemma == "եվ":
            _emit(findings, "error", rank_of(tags), lemma, tr,
                  "eu-ligature",
                  "should be merged into `և` (single ligature character)")


# Lemma cells in cards/top_1000.tsv may carry a phonetic-respelling
# annotation: `արդեն [արթեն]`. Strip it before dictionary lookup —
# the dictionary keys on the orthographic lemma alone.
_ANNOT_RE = re.compile(r"\s*\[[^\]]*\]\s*$")


def _strip_annot(lemma: str) -> str:
    return _ANNOT_RE.sub("", lemma).strip()


# Visual-confusable codepoints we've actually hit in LLM output. Each
# entry maps a wrong codepoint to the Armenian letter it visually
# matches. Extend when a new confusable surfaces.
_ARMENIAN_CONFUSABLES = {
    "м": ("մ", "Cyrillic em U+043C ↔ Armenian men U+0574"),
    "о": ("ո", "Cyrillic o U+043E ↔ Armenian vo U+0578"),
    "λ": ("լ", "Greek lambda U+03BB ↔ Armenian liwn U+056C"),
    "a": ("ա", "Latin a U+0061 ↔ Armenian ayb U+0561"),
    "o": ("ո", "Latin o U+006F ↔ Armenian vo U+0578"),
    "p": ("ք",  "Latin p U+0070 looks like Armenian քե (no exact match)"),
    "n": ("ո", "Latin n U+006E ↔ Armenian vo (visual; rare)"),
    "h": ("հ", "Latin h U+0068 ↔ Armenian ho U+0570"),
    "y": ("ց", "Latin y U+0079 ↔ Armenian tso (visual)"),
    "u": ("ս", "Latin u U+0075 ↔ Armenian se (visual)"),
}

# Allowed non-Armenian characters in the lemma column: spaces (MWUs),
# bracket-pair for the phonetic-respelling annotation, underscore
# (build-pipeline MWU joiner), hyphen (compound markers), apostrophe
# variants (Armenian intra-word punctuation U+055A-U+055F is in the
# Armenian block already and passes naturally).
_ALLOWED_NON_ARMENIAN = set(" -[]_")


def _is_armenian(ch: str) -> bool:
    cp = ord(ch)
    return 0x0530 <= cp <= 0x058F or 0xFB13 <= cp <= 0xFB17


# Editorial-quality: glosses that *describe* an inflected form
# instead of *translating* it. Earlier version was a whitelist of
# specific descriptor words (Nth-person, imperative of, …) and
# missed every shape not on the list (imperfective converb,
# definite dative plural, negative form, resultative participle).
# Replaced with a structural detector that catches the underlying
# shape: any prose ending with `… of <Armenian word>`. That's the
# kaikki-style "X form/sense of Y" template, regardless of which
# X is used.
#
# Backstop list of explicit shapes, in case kaikki produces prose
# that doesn't end with the Armenian-word reference (e.g. "in
# combination with numerals").
_PROSE_OF_ARMENIAN = re.compile(
    # Optional `(romanization)` after the Armenian word; kaikki cross-
    # references look like `… of լինել (linel)`. Without the
    # optional group, the structural detector misses every prose
    # gloss with a romanization suffix.
    r"\bof\s+[Ա-Ֆա-ֆ]+\s*(?:\([^)]+\))?\s*[.,;:!?]?\s*$"
)
_PROSE_FALLBACK_PATTERNS = [
    re.compile(r"\balternative\s+(?:form|spelling)\s+of\b", re.IGNORECASE),
    re.compile(r"\bin\s+combination\s+with\s+numerals\b", re.IGNORECASE),
    re.compile(r"\bused\s+(?:to\s+)?(?:before|after|in)\s+(?:vowels|consonants|words)\b",
               re.IGNORECASE),
]


def check_prose_gloss(rows: list[Row], findings: list[Finding]) -> None:
    """Flag glosses that describe a word's grammatical role rather
    than translate it. Two layers:
    1. Structural: gloss ends with `of <Armenian word>` — the
       canonical "X form of Y" template.
    2. Backstop: a small list of explicit phrasings that don't
       reference an Armenian word but are still descriptive prose.
    Each finding suggests a HAND_OVERRIDE.
    """
    for lemma, tr, tags in rows:
        if _PROSE_OF_ARMENIAN.search(tr):
            _emit(findings, "warning", rank_of(tags), lemma, tr,
                  "prose-gloss",
                  "gloss describes the form ('… of <lemma>') rather than "
                  "translates it — add a HAND_OVERRIDE")
            continue
        for pat in _PROSE_FALLBACK_PATTERNS:
            if pat.search(tr):
                _emit(findings, "warning", rank_of(tags), lemma, tr,
                      "prose-gloss",
                      f"reads as dictionary prose (matches /{pat.pattern}/) "
                      f"— add a HAND_OVERRIDE")
                break


def check_verbose_gloss(rows: list[Row], findings: list[Finding]) -> None:
    """Glosses longer than 60 chars (single-language) or 90 chars
    (en/ru pair) tend to be kaikki sense-stacks ('to do, be busy
    with; be occupied with, be engaged in; …') rather than card
    answers. Flag for trim.
    """
    for lemma, tr, tags in rows:
        cap = 90 if " / " in tr else 60
        if len(tr) > cap:
            _emit(findings, "info", rank_of(tags), lemma, tr,
                  "verbose-gloss",
                  f"gloss is {len(tr)} chars (cap {cap}); consider "
                  f"trimming to 1-3 senses")


def check_redundant_language_parenthetical(
        rows: list[Row], findings: list[Finding]) -> None:
    """For lemmas ending in -երեն (the 'language' suffix), a trailing
    `(language)` in the gloss is redundant scaffolding. Flag so it
    can be trimmed."""
    for lemma, tr, tags in rows:
        if lemma.endswith("երեն") and "(language)" in tr.lower():
            _emit(findings, "warning", rank_of(tags), lemma, tr,
                  "redundant-language-parenthetical",
                  "lemma ends in -երեն (= 'language'); '(language)' in gloss is redundant")


def check_script_purity(rows: list[Row], findings: list[Finding]) -> None:
    """Lemma column must be pure Armenian (plus the allowed
    non-Armenian punctuation set). Flag any character outside that
    set, with extra prominence for known visual-confusables —
    the LLM-generation bug where Cyrillic `м` or Greek `λ` substitutes
    for the visually-identical Armenian letter.

    The check sits at the cards layer, but the same idea extends
    naturally to topic-file Armenian text. citation-check already
    catches confusables in `verbatim_quote` (byte-level); this
    check covers card lemmas which aren't byte-anchored to a
    source.
    """
    for lemma, tr, tags in rows:
        for ch in lemma:
            if _is_armenian(ch) or ch in _ALLOWED_NON_ARMENIAN:
                continue
            if ch in _ARMENIAN_CONFUSABLES:
                expected, hint = _ARMENIAN_CONFUSABLES[ch]
                _emit(findings, "error", rank_of(tags), lemma, tr,
                      "script-confusable",
                      f"{ch!r} → expected {expected!r}; {hint}")
            else:
                _emit(findings, "warning", rank_of(tags), lemma, tr,
                      "non-armenian-in-lemma",
                      f"unexpected char {ch!r} (U+{ord(ch):04X})")
            break  # one finding per lemma is enough
        # Gloss-side guard: a single token mixing Armenian with
        # Cyrillic/Latin letters is the `էл`-with-Cyrillic-л bug
        # (2026-06-03). The lemma loop above can't see it — embedded
        # Armenian examples live in the gloss. One finding per row.
        for tok in tr.split():
            arm = any(_is_armenian(c) for c in tok)
            other = any((0x0400 <= ord(c) <= 0x04FF)  # Cyrillic
                        or (0x0041 <= ord(c) <= 0x007A and c.isalpha())  # Latin
                        for c in tok)
            if arm and other:
                _emit(findings, "error", rank_of(tags), lemma, tr,
                      "mixed-script-gloss",
                      f"token {tok!r} mixes Armenian with Cyrillic/Latin "
                      f"letters")
                break


def check_dictionary_ambiguity(rows: list[Row], findings: list[Finding]) -> None:
    """For dictionary-sourced cards where kaikki lists 2+ POS
    senses, surface a one-line review item showing the picked gloss
    alongside competing senses. Catches "rye" / "valiant" / "Bats" /
    "lettuce vs thousand"-type misranks where another sense is the
    actually-frequent one.

    Severity gradient: top-50 ranks are `warning` (very likely a
    misrank if 2+ senses; the `հազար → "lettuce"` recurrence in
    `errors/2026-05-09-005-hazar-numeral-misrank.md` motivated
    promoting these). Lower ranks remain `info` — review fodder
    rather than a gate.
    """
    for lemma, tr, tags in rows:
        if "src-dictionary" not in tags:
            continue
        key = _strip_annot(lemma).lower()
        entries = dictionary.lookup_full(key)
        if len(entries) < 2:
            continue
        # Skip entries where the only "competition" is name/letter,
        # which we already deprioritize structurally.
        real_entries = [e for e in entries
                        if e[0].lower() not in ("name", "letter")]
        if len(real_entries) < 2:
            continue
        competing = []
        for pos, glosses_str in real_entries:
            first = glosses_str.split(" | ")[0].strip()
            competing.append(f"[{pos}] {first[:50]}")
        rank = rank_of(tags)
        severity = "warning" if 0 < rank <= 50 else "info"
        _emit(findings, severity, rank, lemma, tr,
              "ambiguous-sense",
              f"{len(real_entries)} POS senses; "
              f"competing: {' / '.join(competing)}")


# ---- golden-glosses test ---------------------------------------------------

GOLDEN_PATH = HERE / "golden_glosses.tsv"


def load_golden() -> dict[str, list[str]]:
    """Read `golden_glosses.tsv` if present.

    Format (tab-separated):
        lemma <TAB> expected_substring [<TAB> expected_substring …]

    A row passes if at least one expected substring is contained
    (case-insensitive) in the deck's gloss for that lemma. Multiple
    substrings on a row are alternatives, not all-required."""
    golden: dict[str, list[str]] = {}
    if not GOLDEN_PATH.exists():
        return golden
    with GOLDEN_PATH.open(encoding="utf-8") as f:
        for raw in f:
            raw = raw.rstrip("\n")
            if not raw or raw.startswith("#"):
                continue
            parts = raw.split("\t")
            if len(parts) < 2:
                continue
            lemma = parts[0].strip().lower()
            alts = [p.strip().lower() for p in parts[1:] if p.strip()]
            if lemma and alts:
                golden[lemma] = alts
    return golden


def check_golden_glosses(rows: list[Row], findings: list[Finding]) -> None:
    """For each lemma listed in `golden_glosses.tsv`, confirm the
    deck's gloss contains at least one expected substring. Catches
    regressions when kaikki re-orders senses on a wiktionary refresh
    or when a HAND_OVERRIDES entry is removed."""
    golden = load_golden()
    if not golden:
        return
    deck: dict[str, tuple[str, str]] = {}
    for lemma, tr, tags in rows:
        deck[_strip_annot(lemma).lower()] = (tr, tags)
    for lemma, alts in golden.items():
        if lemma not in deck:
            _emit(findings, "warning", -1, lemma, "",
                  "golden-missing",
                  f"in golden set but absent from deck; expected one of: "
                  f"{', '.join(alts)}")
            continue
        tr, tags = deck[lemma]
        tr_lower = tr.lower()
        if not any(alt in tr_lower for alt in alts):
            _emit(findings, "error", rank_of(tags), lemma, tr,
                  "golden-mismatch",
                  f"gloss does not contain any expected substring: "
                  f"{', '.join(alts)}")


_CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")

# Grammatical morphemes / suffix tokens that must NEVER appear as
# standalone cards. They reach the frequency list as tokenizer spill
# or metalinguistic mentions in the grammar books (e.g. the plural
# `-ներ` discussed as "-ներ հոգնակերտ մասնիկ"), and kaikki happily
# glosses them as rare literary homographs. build_deck.SKIP_LEMMAS
# drops them; this check is the regression guard — if a SKIP is ever
# removed, the noise card resurfaces and this fires. Extend together
# with SKIP_LEMMAS.
MORPHEME_NOISE = {
    "ներ",   # plural suffix -ներ (kaikki: "sister-in-law")
    "երի",   # gen of plural -եր
    "ին",    # dative/definite tail
    "ություն",  # bare abstract-noun suffix
    "մերի",  # gen of substantivized possessive մերը (kaikki: "woods")
    "մեկն",  # definite nom. sg. of մեկ (kaikki: rare adv "upright")
}

# How deep the "every card should ideally carry a Russian gloss"
# expectation runs. Per the 2026-06-03 review the committed coverage
# target is the top-300 plus function words; below that, English-only
# is acceptable, so we don't want to drown the report in info rows.
RUSSIAN_COVERAGE_RANK = 300


def check_missing_russian(rows: list[Row], findings: list[Finding]) -> None:
    """Coverage tracker (info): a top-RUSSIAN_COVERAGE_RANK card whose
    gloss has no Cyrillic. The deck schema is `English / Russian`; the
    Russian half disambiguates senses (esp. for function words) and is
    a committed coverage target for the high-frequency core. Populate
    via cards/frequency/russian_glosses.tsv. Info-severity by design —
    it measures a gap, it doesn't block."""
    for lemma, tr, tags in rows:
        rank = rank_of(tags)
        if rank == -1 or rank > RUSSIAN_COVERAGE_RANK:
            continue
        # Digit-only glosses (number cards) need no Russian — the
        # numeral is language-neutral.
        if re.fullmatch(r"\d+(?:st|nd|rd|th)?", tr.strip()):
            continue
        if not _CYRILLIC_RE.search(tr):
            _emit(findings, "info", rank, _strip_annot(lemma), tr,
                  "missing-russian",
                  "top-300 card has no Russian gloss; add a row to "
                  "russian_glosses.tsv")


def check_reserved_slash(rows: list[Row], findings: list[Finding]) -> None:
    """The deck reserves ` / ` strictly for the English/Russian
    boundary. A gloss that contains a `/` but NO Cyrillic anywhere is
    misusing the slash as an English comma-separator (`to cry / to
    weep`; also the un-spaced `Don't you think?/Isn't it?` case, which
    the old space-padded pattern missed). The no-Cyrillic guard
    exempts legit within-word alternatives like `his/her`, `pl/formal`
    — those always carry a Russian half, so Cyrillic is present."""
    for lemma, tr, tags in rows:
        if "/" in tr and not _CYRILLIC_RE.search(tr):
            _emit(findings, "warning", rank_of(tags), _strip_annot(lemma),
                  tr, "reserved-slash",
                  "` / ` is reserved for the EN/RU boundary; use a comma "
                  "between English senses")


def check_duplicate_override_keys(rows: list[Row],
                                  findings: list[Finding]) -> None:
    """Source-level guard: a duplicate string key in any dict literal
    in build_deck.py (HAND_OVERRIDES, DISPLAY_OVERRIDES, …) silently
    shadows the earlier value — Python keeps the last. This caused the
    `դուր` gloss to ship as `(in դուր գալ) …` (2026-06-03). `rows` is
    ignored; the check parses build_deck.py directly."""
    import ast
    src_path = HERE / "build_deck.py"
    if not src_path.exists():
        return
    try:
        tree = ast.parse(src_path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        _emit(findings, "error", -1, "build_deck.py", "",
              "build-deck-syntax", f"could not parse: {e}")
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: dict[str, int] = {}
        for k in node.keys:
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                if k.value in seen:
                    _emit(findings, "error", -1, k.value, "",
                          "duplicate-override-key",
                          f"key {k.value!r} duplicated in a build_deck.py "
                          f"dict (line {k.lineno}, first {seen[k.value]}) "
                          f"— the later value silently shadows the earlier")
                seen[k.value] = k.lineno


def check_morpheme_noise(rows: list[Row], findings: list[Finding]) -> None:
    """Regression guard: a bare grammatical morpheme surfaced as a
    card (see MORPHEME_NOISE). Means a SKIP_LEMMAS entry was dropped."""
    for lemma, tr, tags in rows:
        if _strip_annot(lemma) in MORPHEME_NOISE:
            _emit(findings, "error", rank_of(tags), _strip_annot(lemma),
                  tr, "morpheme-noise",
                  "bare grammatical morpheme / tokenizer spill — should "
                  "be in build_deck.SKIP_LEMMAS, not a card")


# ---- driver ---------------------------------------------------------------

CHECKS = [
    check_empty,
    check_noise,
    check_false_friend,
    check_truncated,
    check_inflected_leak,
    check_paradigm_leak,
    check_proper_noun,
    check_duplicate_translation,
    check_eu_ligature,
    check_dictionary_ambiguity,
    check_golden_glosses,
    check_script_purity,
    check_prose_gloss,
    check_verbose_gloss,
    check_redundant_language_parenthetical,
    check_missing_russian,
    check_reserved_slash,
    check_morpheme_noise,
    check_duplicate_override_keys,
]


def load_mwus() -> list[str]:
    """Pull MWUS list from build_ours so the validator stays in sync."""
    try:
        import build_ours  # noqa: E402
        return list(build_ours.MWUS)
    except Exception:
        return []


def write_tsv(findings: list[Finding], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["severity", "rank", "lemma", "translation",
                    "category", "hint"])
        for fnd in sorted(findings,
                          key=lambda x: (x["category"], x["rank"])):
            w.writerow([fnd["severity"], fnd["rank"], fnd["lemma"],
                        fnd["translation"], fnd["category"], fnd["hint"]])


def write_md(findings: list[Finding], path: Path,
             total_rows: int) -> None:
    by_cat: dict[str, list[Finding]] = defaultdict(list)
    for fnd in findings:
        by_cat[fnd["category"]].append(fnd)
    severity_count = Counter(f["severity"] for f in findings)

    lines: list[str] = []
    lines.append("# Deck validation report\n")
    lines.append(f"- Deck: `cards/top_1000.tsv` ({total_rows} rows)")
    lines.append(f"- Findings: **{len(findings)}** "
                 f"({severity_count.get('error', 0)} errors, "
                 f"{severity_count.get('warning', 0)} warnings)")
    lines.append("")
    lines.append("## By category\n")
    lines.append("| category | severity | count |")
    lines.append("| --- | --- | --- |")
    for cat in sorted(by_cat):
        sev = by_cat[cat][0]["severity"]
        lines.append(f"| `{cat}` | {sev} | {len(by_cat[cat])} |")
    lines.append("")
    for cat in sorted(by_cat):
        lines.append(f"## `{cat}`\n")
        # Show up to 30 per category to keep the report readable.
        rows = sorted(by_cat[cat], key=lambda x: x["rank"])
        for fnd in rows[:30]:
            lines.append(
                f"- **#{fnd['rank']:>4}** `{fnd['lemma']}` → "
                f"`{fnd['translation']}` — {fnd['hint']}"
            )
        if len(rows) > 30:
            lines.append(f"- … and {len(rows) - 30} more")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", type=Path, default=DECK_PATH)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any error-severity findings exist")
    args = ap.parse_args()

    rows = read_deck(args.deck)
    findings: list[Finding] = []
    for check in CHECKS:
        check(rows, findings)
    check_mwu_leak(rows, findings, load_mwus())

    write_tsv(findings, TSV_OUT)
    write_md(findings, MD_OUT, total_rows=len(rows))

    by_cat = Counter(f["category"] for f in findings)
    sev = Counter(f["severity"] for f in findings)
    print(f"Validated {len(rows)} rows.")
    print(f"Findings: {len(findings)} "
          f"({sev.get('error', 0)} errors, "
          f"{sev.get('warning', 0)} warnings).")
    for cat in sorted(by_cat):
        print(f"  {cat:24s} {by_cat[cat]:>4d}")
    print(f"Wrote {TSV_OUT}")
    print(f"Wrote {MD_OUT}")
    if args.strict and sev.get("error", 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
