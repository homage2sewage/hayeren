#!/usr/bin/env python3
"""Structural validator for `explore/words.tsv`.

Mirrors the deck's validate-after-build discipline
(`frequency/validate_deck.py`): run after any regeneration or merge
of the wordlist. Checks are structural (column shape, script
membership, separator discipline); editorial quality of the
generated ru/example layer is covered by the critic pass documented
in README.md.

Severities: `error` (must fix before use) and `warn` (inspect —
may be legitimate, e.g. suppletive verb forms failing the
headword-presence heuristic).
"""

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = HERE / "words.tsv"
GOLDEN = HERE / "golden.tsv"

ARM = re.compile(r"[԰-֏]")
CYR = re.compile(r"[А-Яа-яЁё]")
LAT = re.compile(r"[A-Za-z]")

# " — " is reserved: exactly one per example, splitting the Armenian
# phrase from its Russian translation.
DASH = " — "

# Armenian intonation/punctuation marks that sit INSIDE the word
# (Ի՞նչ, Արի՛) — strip before headword matching.
INTRAWORD = re.compile(r"[՚-՟]")


def headword_stem(word: str) -> list[str]:
    """Crude prefix stems for the headword-presence warning.
    Strips the infinitive ending of verbs; takes the first 4 chars
    otherwise. Warning-severity only — suppletive forms (գալ→եկավ)
    legitimately fail this."""
    stems = []
    for tok in word.split():
        t = tok.lower()
        if len(t) > 3 and t.endswith(("ալ", "ել")):
            t = t[:-2]
        stems.append(t[:4] if len(t) >= 4 else t)
    return stems


def check_example(ex: str, word: str, col: str, rank: str,
                  problems: list[tuple[str, str]]) -> None:
    n_dash = ex.count(DASH)
    if n_dash == 0:
        problems.append(("error", f"rank {rank} {word}: {col} has no "
                         f"'{DASH.strip()}' phrase/translation boundary"))
        return
    if n_dash > 1:
        problems.append(("warn", f"rank {rank} {word}: {col} has "
                         f"{n_dash} em-dash separators (reserved for the "
                         f"phrase/translation boundary)"))
    phrase, translation = ex.split(DASH, 1)
    if not ARM.search(phrase):
        problems.append(("error", f"rank {rank} {word}: {col} phrase part "
                         f"has no Armenian: {phrase!r}"))
    if not CYR.search(translation):
        problems.append(("error", f"rank {rank} {word}: {col} translation "
                         f"part has no Cyrillic: {translation!r}"))
    if CYR.search(phrase):
        problems.append(("error", f"rank {rank} {word}: {col} Armenian part "
                         f"contains Cyrillic (mixed-script): {phrase!r}"))
    if ARM.search(translation):
        problems.append(("warn", f"rank {rank} {word}: {col} translation "
                         f"contains Armenian: {translation!r}"))
    if LAT.search(ex):
        problems.append(("warn", f"rank {rank} {word}: {col} contains Latin "
                         f"characters: {ex!r}"))
    if len(ex) > 100:
        problems.append(("warn", f"rank {rank} {word}: {col} is long "
                         f"({len(ex)} chars) for a one-line entry"))
    stems = headword_stem(word)
    phrase_l = INTRAWORD.sub("", phrase.lower())
    if stems and not any(s and s in phrase_l for s in stems):
        problems.append(("warn", f"rank {rank} {word}: {col} may not "
                         f"contain the headword: {phrase!r}"))


def load_golden() -> dict[str, list[str]]:
    """`explore/golden.tsv`: word -> alternative expected substrings.
    Same format/semantics as `frequency/golden_glosses.tsv`."""
    golden: dict[str, list[str]] = {}
    if not GOLDEN.exists():
        return golden
    with GOLDEN.open(encoding="utf-8") as f:
        for raw in f:
            raw = raw.rstrip("\n")
            if not raw or raw.startswith("#"):
                continue
            parts = raw.split("\t")
            word = parts[0].strip()
            alts = [p.strip().lower() for p in parts[1:] if p.strip()]
            if word and alts:
                golden[word] = alts
    return golden


def check_golden(rows: list[list[str]],
                 problems: list[tuple[str, str]]) -> None:
    table = {r[1]: (r[2] + " " + r[3]).lower() for r in rows if len(r) >= 4}
    for word, alts in load_golden().items():
        gloss = table.get(word)
        if gloss is None:
            problems.append(("warn", f"golden: {word!r} absent from "
                             f"wordlist"))
        elif not any(a in gloss for a in alts):
            problems.append(("error", f"golden: {word} gloss lacks all of "
                             f"{alts}: {gloss!r}"))


def main() -> int:
    problems: list[tuple[str, str]] = []
    with WORDS.open(encoding="utf-8") as f:
        rdr = csv.reader(f, delimiter="\t")
        header = next(rdr, None)
        if header != ["rank", "word", "en", "ru", "ex1", "ex2"]:
            problems.append(("error", f"unexpected header: {header}"))
        rows = list(rdr)

    seen: dict[str, str] = {}
    for i, row in enumerate(rows, start=2):
        if len(row) != 6:
            problems.append(("error", f"line {i}: {len(row)} columns"))
            continue
        rank, word, en, ru, ex1, ex2 = row
        if rank != str(i - 1):
            problems.append(("error", f"line {i}: rank {rank!r} not "
                            f"sequential"))
        if not ARM.search(word):
            problems.append(("error", f"rank {rank}: word {word!r} has no "
                            f"Armenian"))
        if word in seen:
            problems.append(("error", f"rank {rank}: duplicate word "
                            f"{word!r} (also rank {seen[word]})"))
        seen[word] = rank
        if not ru.strip():
            problems.append(("error", f"rank {rank} {word}: empty ru gloss"))
        elif not CYR.search(ru):
            problems.append(("error", f"rank {rank} {word}: ru gloss has no "
                            f"Cyrillic: {ru!r}"))
        if ARM.search(ru):
            problems.append(("warn", f"rank {rank} {word}: ru gloss contains "
                            f"Armenian: {ru!r}"))
        if not ex1.strip():
            problems.append(("error", f"rank {rank} {word}: empty ex1"))
        else:
            check_example(ex1, word, "ex1", rank, problems)
        if ex2.strip():
            check_example(ex2, word, "ex2", rank, problems)

    check_golden(rows, problems)

    errors = [m for s, m in problems if s == "error"]
    warns = [m for s, m in problems if s == "warn"]
    for m in errors:
        print(f"ERROR {m}")
    for m in warns:
        print(f"warn  {m}")
    print(f"\n{len(rows)} rows checked: {len(errors)} errors, "
          f"{len(warns)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
