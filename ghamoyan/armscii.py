"""ARMSCII-8 → Unicode decoder for Armenian text mis-extracted as
WinAnsi.

ARMSCII-8 (Armenian Standard Code for Information Interchange, 8-bit)
is a single-byte Armenian encoding common in Armenian PDFs from the
late-1990s through 2010s. When a PDF stores Armenian text in
ARMSCII-8 but declares its font's encoding as WinAnsi, every text
extractor (pdftotext, pymupdf, etc.) mis-interprets each ARMSCII-8
byte as the matching Latin-1 glyph: 0xB3 displays as `³` instead of
`ա`, 0xC9 as `É` instead of `լ`, and so on.

This module reverses that: given the mis-extracted text, look up each
character's codepoint in the ARMSCII-8 → Unicode table and substitute
the real Armenian letter.

The table here is the standard ARMSCII-8 mapping (Wikipedia: ArmSCII).
Per-PDF overrides handle fonts that deviate from the standard for a
handful of glyphs (this PDF uses Greek μ U+03BC for `բ` and ¨ U+00A8
for the ev-ligature `և`).
"""


ARMSCII8: dict[int, str] = {
    # Punctuation 0xA1-0xAF
    0xA1: "։",   # verjaket (full stop)
    0xA2: "՚",   # apostrophe / breath mark
    0xA3: "՛",   # shesht (emphasis)
    0xA4: "․",   # mid-dot (Armenian period equivalent in some standards)
    0xA5: "՝",   # mijaket (mid-stop / clause separator)
    0xA6: ",",   # storaket (comma)
    0xA7: "-",   # hyphen
    0xA8: "և",   # ev-ligature (this PDF; standard ARMSCII-8 has ֊ here)
    0xA9: "՞",   # hartsakan (question)
    0xAA: "՟",   # patʿiv / abbreviation
    0xAB: "«",
    0xAC: "»",
    0xAE: "…",
    0xAF: "՜",   # batsakanchakan (exclamation)
    # Letter pairs (uppercase, lowercase) from 0xB2
    0xB2: "Ա", 0xB3: "ա", 0xB4: "Բ", 0xB5: "բ",
    0xB6: "Գ", 0xB7: "գ", 0xB8: "Դ", 0xB9: "դ",
    0xBA: "Ե", 0xBB: "ե", 0xBC: "Զ", 0xBD: "զ",
    0xBE: "Է", 0xBF: "է", 0xC0: "Ը", 0xC1: "ը",
    0xC2: "Թ", 0xC3: "թ", 0xC4: "Ժ", 0xC5: "ժ",
    0xC6: "Ի", 0xC7: "ի", 0xC8: "Լ", 0xC9: "լ",
    0xCA: "Խ", 0xCB: "խ", 0xCC: "Ծ", 0xCD: "ծ",
    0xCE: "Կ", 0xCF: "կ", 0xD0: "Հ", 0xD1: "հ",
    0xD2: "Ձ", 0xD3: "ձ", 0xD4: "Ղ", 0xD5: "ղ",
    0xD6: "Ճ", 0xD7: "ճ", 0xD8: "Մ", 0xD9: "մ",
    0xDA: "Յ", 0xDB: "յ", 0xDC: "Ն", 0xDD: "ն",
    0xDE: "Շ", 0xDF: "շ", 0xE0: "Ո", 0xE1: "ո",
    0xE2: "Չ", 0xE3: "չ", 0xE4: "Պ", 0xE5: "պ",
    0xE6: "Ջ", 0xE7: "ջ", 0xE8: "Ռ", 0xE9: "ռ",
    0xEA: "Ս", 0xEB: "ս", 0xEC: "Վ", 0xED: "վ",
    0xEE: "Տ", 0xEF: "տ", 0xF0: "Ր", 0xF1: "ր",
    0xF2: "Ց", 0xF3: "ց", 0xF4: "Ւ", 0xF5: "ւ",
    0xF6: "Փ", 0xF7: "փ", 0xF8: "Ք", 0xF9: "ք",
    0xFA: "Օ", 0xFB: "օ", 0xFC: "Ֆ", 0xFD: "ֆ",
    0xFE: "և",
    # Per-PDF overrides — pdftotext mis-extracts these to non-WinAnsi
    # codepoints because the embedded font's ToUnicode CMap is quirky:
    0x03BC: "բ",  # Greek small μ → Armenian բ
}


# Fonts in this PDF that need decoding. Modern Identity-H Unicode fonts
# (Calibri, plain Sylfaen with uni:yes) extract directly and need no
# decoding — they're not in this set.
ENCODED_FONTS: set[str] = {
    "ArialArmenian",
    "ArialArmenianBold",
    "ArialArmenianItalic",
    "ArialArmenianBoldItalic",
    "TimesNewRoman",
    "ArianAMU-Italic",
}


def decode(text: str) -> str:
    """Substitute every ARMSCII-8-encoded character with its Armenian
    Unicode counterpart. Characters not in the table pass through."""
    return "".join(ARMSCII8.get(ord(c), c) for c in text)


def remap(font: str, text: str) -> str:
    """Decode `text` if the font is one of the ARMSCII-8 ones; otherwise
    return unchanged. Mirrors the shape of `sakayan/fonts.remap`."""
    if font in ENCODED_FONTS:
        return decode(text)
    return text
