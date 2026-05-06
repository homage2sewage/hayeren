"""Convert English number words to numerals in translation text.

Anki cards are easier to scan when '20' replaces 'Twenty'. Handles:

- single cardinals: ``one`` → ``1``, ``twenty`` → ``20``
- hyphenated tens-units: ``twenty-one`` → ``21``
- digit sequences (phone-number-style): ``four-zero-zero`` → ``4-0-0``
- ordinals: ``third`` → ``3rd``, ``twenty-first`` → ``21st``

Quantity words (``hundred``, ``thousand``, ``million``) are deliberately
left alone — they're often used non-numerically ("a million reasons")
and grammatically attach to context we don't want to fight.
"""

import re

CARDINALS: dict[str, int] = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}

_DIGITS_ONLY = {k: v for k, v in CARDINALS.items() if v < 10}
_TENS = {k: v for k, v in CARDINALS.items() if v >= 20 and v % 10 == 0}

ORDINAL_TO_CARDINAL: dict[str, str] = {
    "first": "one", "second": "two", "third": "three",
    "fourth": "four", "fifth": "five", "sixth": "six",
    "seventh": "seven", "eighth": "eight", "ninth": "nine",
    "tenth": "ten", "eleventh": "eleven", "twelfth": "twelve",
    "thirteenth": "thirteen", "fourteenth": "fourteen",
    "fifteenth": "fifteen", "sixteenth": "sixteen",
    "seventeenth": "seventeen", "eighteenth": "eighteen",
    "nineteenth": "nineteen", "twentieth": "twenty",
    "thirtieth": "thirty", "fortieth": "forty", "fiftieth": "fifty",
    "sixtieth": "sixty", "seventieth": "seventy",
    "eightieth": "eighty", "ninetieth": "ninety",
}


def _ord_suffix(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _hyphen_replace(m: re.Match) -> str:
    raw = m.group(0)
    parts = raw.lower().split("-")

    # Digit sequence: "four-zero-zero" → "4-0-0"
    if all(p in _DIGITS_ONLY for p in parts):
        return "-".join(str(_DIGITS_ONLY[p]) for p in parts)

    # Tens + cardinal digit: "twenty-one" → "21"
    if len(parts) == 2 and parts[0] in _TENS and parts[1] in _DIGITS_ONLY:
        return str(_TENS[parts[0]] + _DIGITS_ONLY[parts[1]])

    # Tens + ordinal digit: "twenty-first" → "21st"
    if len(parts) == 2 and parts[0] in _TENS and parts[1] in ORDINAL_TO_CARDINAL:
        cardinal = ORDINAL_TO_CARDINAL[parts[1]]
        if cardinal in _DIGITS_ONLY:
            n = _TENS[parts[0]] + _DIGITS_ONLY[cardinal]
            return f"{n}{_ord_suffix(n)}"

    return raw


def _word_replace(m: re.Match) -> str:
    raw = m.group(0)
    w = raw.lower()
    if w in CARDINALS:
        return str(CARDINALS[w])
    if w in ORDINAL_TO_CARDINAL:
        cardinal = ORDINAL_TO_CARDINAL[w]
        if cardinal in CARDINALS:
            n = CARDINALS[cardinal]
            return f"{n}{_ord_suffix(n)}"
    return raw


_HYPHEN_RE = re.compile(r"\b[A-Za-z]+(?:-[A-Za-z]+)+\b")
_WORD_RE = re.compile(r"\b[A-Za-z]+\b")


def normalize(text: str) -> str:
    """Replace English number words with numerals."""
    text = _HYPHEN_RE.sub(_hyphen_replace, text)
    text = _WORD_RE.sub(_word_replace, text)
    return text
