"""Detect spelling-vs-pronunciation deviations in Eastern Armenian using
Sakayan's phonetic transcription as ground truth.

Approach: walk the original Armenian word letter by letter, consuming
the matching token from the transcription. Where the transcription's
token at that position corresponds to a *different* Armenian letter,
we've found a deviation — the spelled letter is being pronounced as
the other one. Build a "phonetic spelling" reflecting actual sounds;
emit `original [phonetic]` if they differ.

Sakayan's transliteration scheme (relevant subset):
    Œ      = aspiration mark on preceding stop/affricate
    §      = schwa ə (Armenian ը — real letter at start, epenthetic mid-cluster)
    ¿      = digraph separator (keep the next char as part of a multi-char unit)
    ¤      = trill ռ (vs flap r → ր)
    ye     = ե at word start
    vo     = ո at word start
    yu     = ոու / mid-word ու after vowel
"""

import re

# Armenian letter → Sakayan token if pronounced as spelled.
LITERAL: dict[str, str] = {
    "ա": "a", "բ": "b", "գ": "g", "դ": "d", "ե": "e", "զ": "z",
    "է": "e", "ը": "§", "թ": "tŒ", "ժ": "z¿h", "ի": "i", "լ": "l",
    "խ": "k¿h", "ծ": "t¿s", "կ": "k", "հ": "h", "ձ": "d¿z", "ղ": "g¿h",
    "ճ": "t¿s¿h", "մ": "m", "յ": "y", "ն": "n", "շ": "s¿h", "ո": "o",
    "չ": "c¿hŒ", "պ": "p", "ջ": "j", "ռ": "¤", "ս": "s", "վ": "v",
    "տ": "t", "ր": "r", "ց": "t¿sŒ", "ւ": "u", "փ": "pŒ", "ք": "kŒ",
    "օ": "o", "ֆ": "f", "ու": "u",
    "և": "yev",  # ev-ligature, the conjunction "and"
}

# Sakayan token → Armenian letter (which letter would naturally produce this sound).
# Longer tokens listed first so greedy match works.
TOKEN_TO_LETTER: dict[str, str] = {
    "c¿hŒ": "չ", "t¿sŒ": "ց", "t¿s¿h": "ճ",
    "d¿z": "ձ", "z¿h": "ժ", "g¿h": "ղ", "k¿h": "խ", "s¿h": "շ", "t¿s": "ծ",
    "tŒ": "թ", "kŒ": "ք", "pŒ": "փ",
    "ye": "ե", "vo": "ո", "yu": "ու",
    "a": "ա", "b": "բ", "g": "գ", "d": "դ", "e": "ե", "z": "զ",
    "h": "հ", "§": "ը", "i": "ի", "l": "լ", "k": "կ", "m": "մ",
    "y": "յ", "n": "ն", "o": "ո", "p": "պ", "j": "ջ", "¤": "ռ",
    "s": "ս", "v": "վ", "t": "տ", "r": "ր", "u": "ու", "f": "ֆ",
    "yev": "և",
}
# Lowercase the comparison-side strings so case-folded translit (`.lower()`)
# can prefix-match. We keep Armenian letter values un-folded since output
# capitalization is fixed up at use-site.
LITERAL = {k: v.lower() for k, v in LITERAL.items()}
TOKEN_TO_LETTER = {k.lower(): v for k, v in TOKEN_TO_LETTER.items()}
TOKENS_BY_LEN = sorted(TOKEN_TO_LETTER.keys(), key=len, reverse=True)


# Pairs of (spelled letter, sounded letter) that we consider "deviations
# worth marking" — the voiced/voiceless/aspirated consonant alternations
# that English speakers find non-obvious. Anything else (vowel glides,
# epenthesis, junk in transcription) is ignored to keep cards clean.
DEVIATION_PAIRS: set[tuple[str, str]] = {
    ("դ", "թ"), ("դ", "տ"),
    ("բ", "փ"), ("բ", "պ"),
    ("գ", "ք"), ("գ", "կ"),
    ("ձ", "ց"), ("ձ", "ծ"),
    ("ջ", "չ"), ("ջ", "ճ"),
}


def split_letters(word: str) -> list[str]:
    """Tokenize an Armenian word into letters, treating ո+ւ (and Ո+ւ) as
    the digraph ու / Ու."""
    out: list[str] = []
    i = 0
    while i < len(word):
        if word[i] in ("ո", "Ո") and i + 1 < len(word) and word[i + 1] == "ւ":
            out.append(word[i] + "ւ")  # preserve case via the original ո/Ո
            i += 2
        else:
            out.append(word[i])
            i += 1
    return out


def _consume_token(translit: str, j: int) -> tuple[str, int]:
    """Greedy longest-match: return (token, length consumed)."""
    for tok in TOKENS_BY_LEN:
        if translit.startswith(tok, j):
            return tok, len(tok)
    return translit[j], 1


def phonetic_word(word: str, translit: str) -> str:
    """Return the spelling that would correspond to the actual pronunciation.
    Equal to `word` if pronounced as spelled. Case-insensitive on translit."""
    letters = split_letters(word)
    translit = translit.lower()  # Sakayan capitalizes sentence-initial; we don't care.
    out: list[str] = []
    j = 0
    n = len(translit)
    at_start = True
    for letter in letters:
        # Skip pure punctuation / spacing in translit.
        while j < n and translit[j] in " ,;:":
            j += 1
        # Epenthetic § not in spelling — skip unless the current Armenian letter is ը.
        while j < n and translit[j] == "§" and letter != "ը":
            j += 1
        if j >= n:
            out.append(letter)
            continue
        # Look up by case-folded letter, preserve original case in output.
        expected = LITERAL.get(letter.lower(), letter.lower())
        initial_alt = None
        if at_start:
            if letter.lower() == "ե":
                initial_alt = "ye"
            elif letter.lower() == "ո":
                initial_alt = "vo"
        # և is "yev" word-initial / after vowel, but "ev" after consonant.
        # Accept both as same-as-spelled.
        if letter.lower() == "և" and translit.startswith("ev", j):
            out.append(letter)
            j += 2
            at_start = False
            continue
        if translit.startswith(expected, j):
            out.append(letter)
            j += len(expected)
        elif initial_alt and translit.startswith(initial_alt, j):
            out.append(letter)
            j += len(initial_alt)
        else:
            tok, consumed = _consume_token(translit, j)
            alt = TOKEN_TO_LETTER.get(tok)
            # Only substitute if (original, alternate) is a recognized
            # voiced↔voiceless/aspirated deviation. Otherwise pass the
            # original through (translit junk, vowel glides, epenthesis
            # mismatch — none of which are "real" pronunciation deviations
            # the user wants flagged).
            if alt and (letter.lower(), alt) in DEVIATION_PAIRS:
                replacement = alt
                if letter[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                out.append(replacement)
            else:
                out.append(letter)
            j += consumed
        at_start = False
    return "".join(out)


# Treat punctuation, brackets, digit, whitespace as word boundaries.
_WORD_RE = re.compile(r"[Ա-Ֆա-ֈ՚-՟]+")


def annotate(armenian_text: str, translit: str) -> str:
    """For a phrase (one-or-more words) and its full transliteration,
    return the same phrase with `[phonetic]` appended after any word
    whose pronunciation differs from spelling."""
    if not translit.strip():
        return armenian_text

    # Tokenize translit into words (whitespace separated, lowercased preserved).
    tr_words = translit.strip().split()
    arm_words = _WORD_RE.findall(armenian_text)
    # If counts don't align, fall back: don't annotate (avoid misleading pairs).
    if len(arm_words) != len(tr_words):
        return armenian_text

    annotations: dict[str, str] = {}
    for aw, tw in zip(arm_words, tr_words):
        tw_stripped = tw.strip(".,;:!?()[]\"'")
        aw_clean = re.sub(r"[՚-՟]", "", aw)
        ph = phonetic_word(aw_clean, tw_stripped)
        # Compare case-insensitively — capitalization differences aren't deviations.
        if ph and ph.lower() != aw_clean.lower() and ph.lower() != aw.lower():
            annotations[aw] = ph

    if not annotations:
        return armenian_text

    out = armenian_text
    for aw, ph in annotations.items():
        out = out.replace(aw, f"{aw} [{ph.lower()}]", 1)
    return out
