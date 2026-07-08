r"""Font-glyph → Unicode decoder for Dum-Tragut, *Armenian: Modern
Eastern Armenian* (London Oriental and African Language Library 14,
John Benjamins, 2009).

The book is an InDesign CS3 PDF with a clean text layer. Latin text
(English prose, the interlinear transliteration, glosses) is set in
MinionPro / MinionExp and extracts as correct Unicode. The Armenian
script, however, is set in a single legacy 8-bit font, **ArialLatArm**,
whose glyphs sit at WinAnsi/Latin-1 codepoints. Every extractor
(pdftotext, pymupdf) therefore reads Armenian as Latin-1 garbage:
raw `î»ë³ ÙÇ Ù³ñ¹áõ` is really `Տեսա մի մարդու` ("I saw a person").

The LETTER block (0xB2–0xFE) is standard ARMSCII-8 and decodes
cleanly. The PUNCTUATION block, however, is **font-specific and
differs sharply from standard ARMSCII-8** (and from the ghamoyan PDF's
ARMSCII-8 layout). Every punctuation slot below was verified glyph-by-
glyph against the rendered page bitmaps on 2026-06-18, e.g.:

    0xAB  raw `«`  ->  `,`   (comma)     p298 `դառձա, դարձար, դարձավ`
    0xA3  raw `£`  ->  `։`   (full stop) p37  `մեծ սերն է։`
    0xA5  raw `¥`  ->  `(`                p423 `Ես կվճարեմ (դրա համար)։`
    0xA4  raw `¤`  ->  `)`                p423      ″
    0xAA  raw `ª`  ->  `՝`   (mijaket)   p107 `իսկ Յուրիին՝`
    0xA9  raw `©`  ->  `.`   (period)    p286 `կամուրջով. ինչ որ մեկը`
    0x60  raw `` ` `` -> `՝`  (bowt)      p92  `կղզիներ՝ արձակուրդի`

Do NOT port punctuation slots back to/from ghamoyan/armscii.py — the
two PDFs disagree on nearly every one. Letters are shared.
"""


# ArialLatArm raw-codepoint -> Armenian Unicode.
#
# Punctuation (verified against rendered bitmaps, see module docstring).
DECODE: dict[int, str] = {
    0x60: "՝",   # bowt / mijaket (clause separator)         p92
    0xA0: " ",   # no-break space -> plain space
    0xA3: "։",   # verjaket (Armenian full stop, glyph ‹:›)  p37
    0xA4: ")",   # close paren                               p423
    0xA6: "»",   # closing guillemet (rare)                  p50
    0xA5: "(",   # open paren                                p423
    0xA8: "և",   # ev-ligature                               p31 (Երևան)
    0xA9: ".",   # period: abbrev/initials dot, entry-final  p286, p742 bibl.
    0xAA: "՝",   # bowt / mijaket                            p107
    0xAB: ",",   # comma                                     p298
    0xAC: "»",   # closing guillemet (rare, ~1/250pp)        p423
    0xAD: "",    # soft hyphen (discretionary) -> drop
    0xAF: "՜",   # yerkaratsman nshan (exclamation)          p98 (Վահա՜ն)
    0xB0: "՛",   # shesht (emphasis)                         p70 (գի՛րքը)
    0xB1: "՞",   # hartsakan (question)                      p73 (ե՞ք)
    0xFF: "՝",   # bowt (rare, ~3/250pp)                     p271  [TENTATIVE]

    # Letters 0xB2–0xFE: standard ARMSCII-8 (uppercase, lowercase pairs).
    0xB2: "Ա", 0xB3: "ա", 0xB4: "Բ", 0xB5: "բ",
    0xB6: "Գ", 0xB7: "գ", 0xB8: "Դ", 0xB9: "դ",
    0xBA: "Ե", 0xBB: "ե", 0xBC: "Զ", 0xBD: "զ",
    0xBE: "Է", 0xBF: "է", 0xC0: "Ը", 0xC1: "ը",
    0xC2: "Թ", 0xC3: "թ", 0xC4: "ժ", 0xC5: "ժ",  # 0xC4: font draws lowercase
    # ž (verified: արժենալ/ժամանակ/գիտաժողով render at x-height, p202/210/267);
    # standard ARMSCII-8 puts uppercase Ժ here. This font has no distinct
    # uppercase-Ž glyph, so a sentence-initial Ժ extracts as ժ — rare, accepted.
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
}


# Fonts whose bytes need decoding. Only ArialLatArm is a legacy 8-bit
# Armenian font here; everything else (MinionPro family) is real Unicode.
ENCODED_FONTS: set[str] = {"ArialLatArm"}

# MinionPro "Expert" cuts (Minion-SemiboldExpert, MinionExp-Regular, …)
# store glyphs in the Private Use Area, per Adobe's expert layout:
#   U+F730+d  = oldstyle/lining digit d   (folios, dates, cross-refs;
#               p267 header F732 F735 F730 = "250", p401 = "384")
#   U+F761+n  = small-cap letter a+n      (front-matter roman folios:
#               F776 F769 = "vi", F778 = "x"; and small-cap text)
# Left unmapped these extract as PUA boxes (the "dropped page number"
# in the calibration).
EXPERT_PUA: dict[int, str] = {
    **{0xF730 + d: str(d) for d in range(10)},
    **{0xF761 + n: chr(ord("a") + n) for n in range(26)},
}

# Slots flagged TENTATIVE in DECODE — low-frequency, single-bitmap
# evidence. self_check reports their live counts so a future page can
# disconfirm them. (0xA9→. was promoted to confirmed after p742.)
TENTATIVE: dict[int, str] = {0xFF: "՝"}


def decode(text: str) -> str:
    """Substitute every ArialLatArm-encoded character with its Armenian
    Unicode counterpart. Characters absent from the table pass through
    (true Unicode already: spaces, digits, curly quotes, …)."""
    return "".join(DECODE.get(ord(c), c) for c in text)


def remap(font: str, text: str) -> str:
    """Decode `text` for the encoded Armenian font; map PUA figures for
    the Expert Latin cuts; otherwise return unchanged. Mirrors
    sakayan/fonts.remap & ghamoyan/armscii.remap."""
    if font in ENCODED_FONTS:
        return decode(text)
    if "Exp" in font:  # MinionExp-Regular, Minion-SemiboldExpert
        return "".join(EXPERT_PUA.get(ord(c), c) for c in text)
    return text
