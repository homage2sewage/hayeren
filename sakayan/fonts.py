"""Glyph→Unicode mappings for the legacy Armenian fonts in the Sakayan
2007 PDF.

Derivation: vocab pages in the textbook print each Armenian word next to
its phonetic transliteration (Armtrans font, in brackets). Pairing the
two columns programmatically gives a direct decoding of every Barz-Italic
codepoint. See ../INDEX.md for the broader pattern.
"""


# Barz-Italic carries ~339K Armenian characters — virtually all body
# Armenian text in the book.
BARZ_ITALIC: dict[str, str] = {
    # lowercase Armenian letters (39)
    "a": "ա", "b": "բ", "g": "գ", "d": "դ",
    ";": "ե", "x": "զ", "h": "է", "e": "ը",
    "j": "թ", "v": "ժ", "i": "ի", "l": "լ",
    ".": "խ", "‘": "ծ", "k": "կ", "f": "հ",
    "]": "ձ", "[": "ղ", "y": "ճ", "m": "մ",
    "\\": "յ", "n": "ն", ",": "շ", "o": "ո",
    "c": "չ", "p": "պ", "=": "ջ", "®": "ռ",
    "s": "ս", "w": "վ", "t": "տ", "r": "ր",
    "z": "ց", "u": "ւ", "'": "փ", "q": "ք",
    "ø": "օ", "`": "ֆ",

    # uppercase Armenian letters
    "A": "Ա", "B": "Բ", "G": "Գ", "D": "Դ",
    ":": "Ե", "X": "Զ", "H": "Է", "E": "Ը",
    "J": "Թ", "V": "Ժ", "I": "Ի", "L": "Լ",
    ">": "Խ", "’": "Ծ", "K": "Կ", "F": "Հ",
    "}": "Ձ", "{": "Ղ", "Y": "Ճ", "M": "Մ",
    "|": "Յ", "N": "Ն", "<": "Շ", "O": "Ո",
    "C": "Չ", "P": "Պ", "+": "Ջ", "Â": "Ռ",
    "S": "Ս", "W": "Վ", "T": "Տ", "R": "Ր",
    "Z": "Ց", "U": "Ւ", '"': "Փ", "Q": "Ք",
    "Ø": "Օ", "~": "Ֆ",

    # ev-ligature
    "…": "և",

    # Armenian punctuation
    "!": "։",  # verjaket (full stop)
    "%": ",",  # storaket (comma — same Unicode as Latin comma)
    "#": "՞",  # hartsakan nshan (question mark — appears mid-word)
    "@": "՛",  # shesht (emphasis)
    "*": "՜",  # batsakanchakan (exclamation — appears mid-word)
    "&": "՝",  # mijaket (mid-stop, ~semicolon)
    "^": "՝",  # mijaket alt — clause separator in body text
    "ª": "«",  # left chakert (Armenian opening quote)
    "º": "»",  # right chakert (Armenian closing quote)
}


# DallakTimes / DallakTimeBold / Pedour-Regular / Pedour-Light carry the
# remaining ~17K Armenian chars (chapter titles, the all-caps decorative
# headings, and a handful of body excerpts like the UN Declaration on p18).
# Verified empirically that they share Barz-Italic's encoding — `:R:WAN`
# decodes to ԵՐԵՎԱՆ via the Barz table either way.
FONT_MAPS: dict[str, dict[str, str]] = {
    "Barz-Italic": BARZ_ITALIC,
    "DallakTimes": BARZ_ITALIC,
    "DallakTimeBold": BARZ_ITALIC,
    "Pedour-Regular": BARZ_ITALIC,
    "Pedour-Light": BARZ_ITALIC,
}


# Latin-with-diacritics font for the phonetic transliteration column.
# Already readable; no remap needed.
PASSTHROUGH_FONTS = {"Armtrans"}


def remap(font: str, text: str) -> str:
    table = FONT_MAPS.get(font)
    if table is None:
        return text
    return "".join(table.get(c, c) for c in text)


import re

_NORMALIZE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # 3+ mijakets collapse into a single ellipsis. The source PDF renders
    # ellipses by typing the ՝-key three times; runs of ՝ are essentially
    # never legitimate Armenian, so we treat any run ≥2 as ellipsis.
    (re.compile(r"՝{2,}"), "…"),
]


def normalize(text: str) -> str:
    """Apply multi-character substitutions that can't fit in the per-glyph map.

    Use on concatenated lines/runs — not individual spans, since legitimate
    multi-character sequences (e.g. ellipses) are usually split across spans.
    """
    for pat, sub in _NORMALIZE_PATTERNS:
        text = pat.sub(sub, text)
    return text
