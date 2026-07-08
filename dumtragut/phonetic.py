r"""IPA decoder for Dum-Tragut's phonetic-transcription fonts.

The bracketed IPA in this book (`[mɑɾtʰ]` for մարդ) is set in a family
of legacy fonts that place IPA-specific glyphs at Latin/WinAnsi
codepoints — so pymupdf reads `[mɑɾtʰ]` as the garbage `[mcnth]`.
Crucially the IPA is **split across fonts**: plain-Latin-looking IPA
(m, b, d, t, p, k, h, s, l, i, u, n-nasal, …) stays in MinionPro and
extracts correctly, while the IPA-specific glyphs live in these
phonetic fonts. So a `t` in MinionPhonetic is the voiced uvular [ʁ],
but a `t` in MinionPro is plain [t] — the decode must be font-scoped.

Glyph→IPA verified against anchor words whose pronunciation is known
and against the book's own sound charts (2026-06-19), e.g. the chart
on p17 states the two uvular fricatives are "voiced [t] and voiceless
[ó]" — i.e. raw `t` = [ʁ], raw `ó` = [χ]:

    մարդ   [mcnth]   = [mɑɾtʰ]   c→ɑ  n→ɾ
    որբ    [‚fnph]   = [ʋɔɾpʰ]   ‚→ʋ  f→ɔ
    սրբել  [s6nph7l] = [səɾpʰɛl]  6→ə  7→ɛ
    ապշել  [cphw7l]  = [ɑpʰʃɛl]   w→ʃ
    խարդախ [ócndcó]  = [χɑɾdɑχ]   ó→χ
    բուրջ  [bundŠ]   = [buɾdʒ]    Š→ʒ
    անգամ  [c]khcm]  = [ɑŋkʰɑm]   ]→ŋ
    վոչինչ [‚ftwhi\twh] = [ʋɔtʃʰiɲtʃʰ]  \→ɲ

2026-07-02 correction: `‚` was originally decoded as glottal stop ʔ
("glottal onset on initial ո/ա"). The 900dpi bitmap of p37 shows the
glyph is the *hooked script-v* ʋ (labiodental approximant): the page
prints և ew [jɛʋ] "and", որդի ordi [ʋɔɾdi], ոսկի oski [ʋɔski],
Երևան [jɛɾɛʋɑn] — the regular word-initial ո = [ʋɔ] rule and the
[ʋ]-realisation of և, where a glottal stop makes no phonological
sense (որբ is "vorp"). All 53 corpus occurrences of the raw glyph
are consistent with ʋ; none require ʔ.
"""


import re


# char -> IPA, applied only to spans in PHONETIC_FONTS. Glyph repertoires
# don't collide across these fonts (e.g. `c` only occurs in Pht-Medium),
# so a single char-keyed table is unambiguous. Chars absent here pass
# through unchanged — that covers the plain glide `j` (Special-Italic)
# and spaces. (`æ` and `>` were long documented as "literal one-off"
# pass-throughs; 2026-07-03 bitmap checks showed both are glyph slots —
# undertie and ɣ — now mapped below.)
DECODE: dict[str, str] = {
    # vowels
    "c": "ɑ",    # open back        (ա)
    "7": "ɛ",    # open-mid front   (ե / է)
    "f": "ɔ",    # open-mid back    (ո / օ)
    "6": "ə",    # schwa            (ը, epenthetic)
    # consonants
    "n": "ɾ",    # alveolar flap    (ր)
    "w": "ʃ",    # postalveolar fric (շ; + t/d → affricate tʃ/dʒ)
    "ó": "χ",    # voiceless uvular fric (խ; devoiced ղ)
    "t": "ʁ",    # voiced uvular fric    (ղ)  ← NOT plain [t]
    "Š": "ʒ",    # voiced postalveolar fric (ժ; + d → dʒ)
    "]": "ŋ",    # velar nasal      (ն before k/g)
    "\\": "ɲ",   # palatal nasal    (ն before tʃ/dʒ)
    "‚": "ʋ",    # labiodental approximant (initial ո- [ʋɔ], glide of և);
                 # wrongly ʔ until 2026-07-02 — see docstring correction
    # juncture / prosody (verified against the rendered bitmaps p65/p74).
    # The two prosody marks are *combining* diacritics that sit on the
    # preceding vowel; placed after the vowel byte they attach correctly
    # (ɑ + U+0301 → ɑ́). The book draws stress as an acute and
    # interrogative intonation as a circumflex, mirroring the romanisation
    # (káysr → kɑ́jsəɾ; vá՞յ → vɑ̂j).
    "ç": "‿",   # undertie ‿ (enclitic liaison: ergúm‿em)
    "æ": "‿",   # undertie again — second slot, single occurrence p31
                 # գնալու‿եմ (500dpi bitmap check 2026-07-03; was a
                 # documented "literal one-off" pass-through, wrongly)
    ">": "ɣ",    # voiced velar fricative — single occurrence p34, the
                 # "[x] [ɣ]" older-grammar notation discussion (500dpi
                 # bitmap check 2026-07-03; same wrong pass-through)
    "¢": "́",   # ◌́ combining acute — primary stress
    "¥": "̂",   # ◌̂ combining circumflex — interrogative intonation
}

# Fonts whose bytes carry IPA glyphs at Latin codepoints.
PHONETIC_FONTS: set[str] = {
    "MinionPhonetic",
    "Minion-Pht-Medium",
    "Minion-Pht-SemiBold",
    "Minion-Special-Italic",
    "Minion-Special-Regular",
}

# All glyphs verified against rendered bitmaps; nothing tentative remains.
TENTATIVE: dict[str, str] = {}


def decode(text: str) -> str:
    """Substitute phonetic-font glyphs with their IPA. Unmapped chars
    (j-glide, space, æ, >) pass through unchanged."""
    return "".join(DECODE.get(c, c) for c in text)


def remap(font: str, text: str) -> str:
    """Decode `text` iff the font is a phonetic one; else return it
    unchanged. Composes after armscii.remap in the extractor."""
    if font in PHONETIC_FONTS:
        return decode(text)
    return text


def fix_diacritics(text: str) -> str:
    """Make the spacing caron ˇ (U+02C7) a *combining* caron (U+030C) so
    the reduced/short-vowel mark sits on the preceding vowel (`iˇ` → `ǐ`).
    Context-free, applied per span."""
    return text.replace("ˇ", "̌")


# Aspiration ʰ is stored in the text layer as a baseline/superscript `h`
# (indistinguishable by font/geometry from the phoneme [h]). It is
# recovered by *position*, validated against the corpus with zero
# counterexamples: an IPA `h` is the aspiration of a voiceless stop or
# affricate iff it immediately follows p/t/k or the affricates ts/tʃ;
# the phoneme [h] (Armenian հ, always a syllable onset) only follows
# vowels, [, space, or a sonorant. Restricted to inside [...] so English
# prose ("the", "photo") and bracketed citations are untouched.
_ASP_STOP = re.compile(r"(?<=[ptk])h")
_ASP_AFFR = re.compile(r"(?<=t[sʃ])h")
_BRACKET = re.compile(r"\[[^\]]*\]")


def fix_aspiration(line: str) -> str:
    """Within each `[...]` span on a rendered line, raise aspiration
    `h`→`ʰ` after a voiceless stop/affricate. Scoped to brackets so
    English prose ("the", "photo") is never touched; bracketed content in
    this book is IPA (source citations are parenthetical, not bracketed),
    so a census over all 760 pages finds zero English-word hits. (An
    English gloss can occasionally interleave into an IPA bracket via
    reading order, but none carries a stop+h digraph in practice.)
    Length-preserving (1 codepoint per substitution), so callers may
    slice the result back onto spans."""
    def repl(m: "re.Match") -> str:
        return _ASP_AFFR.sub("ʰ", _ASP_STOP.sub("ʰ", m.group(0)))
    return _BRACKET.sub(repl, line)
