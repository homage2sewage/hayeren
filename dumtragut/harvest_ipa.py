#!/usr/bin/env python3
r"""Harvest word→IPA transcription pairs from out/full.jsonl.

Dum-Tragut's phonology chapter (and scattered later passages) gives
transcriptions in the fixed layout

    Armenian-word  translit  [IPA]  “gloss”
    ArialLatArm    It-font   mixed  Regular

The IPA glyphs are already decoded to real Unicode by phonetic.py at
extraction time; this script only *binds* each bracketed IPA to the
Armenian expression it transcribes, using fonts to tell the italic
transliteration apart from English prose:

- flatten each page's spans to one string (file order = reading order),
  remembering which span owns every character;
- for each `[...]` group containing an IPA-specific glyph
  (ɑɛɔəɾʃχʁʒŋɲʔʰ) and no uppercase/digit/#, walk backwards up to
  WINDOW chars to the nearest Armenian-script run;
- reject the binding if the gap contains a letter set in a Regular
  font (English prose, e.g. "reduced to schwa [ə]") or another
  bracket. Exception: a trailing "both:"/"both" — the reformed-vs-
  classical orthography pairs on p29, `սենյակ senyak < սենեակ seneak
  both: [sɛnjɑk]`; there the modern spelling (before the `<`) is
  bound and the classical one kept as a note.

Unbound IPA groups are alphabet-chart cells and in-prose phoneme
mentions — correctly not word transcriptions (spot-checked 2026-07-02).

Output: out/ipa_index.tsv, one row per *occurrence* so every row is
citation-ready (page + y-range):

    page  y0  y1  word  translit  ipa  gloss  note

Words are verbatim corpus bytes — including apparent book typos
(e.g. p36 ռարդիո for ռադիո); do not "fix" them here, the index must
stay byte-faithful so `citation-check` / the Stop-hook can verify
against it.

Run:  python3 harvest_ipa.py          (from dumtragut/)
"""

import collections
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
JSONL = HERE / "out" / "full.jsonl"
OUT_TSV = HERE / "out" / "ipa_index.tsv"

IPA_MARKER = set("ɑɛɔəɾʃχʁʒŋɲʔʋʰ")
ARM_RE = re.compile(r"[԰-֏]")
BRACKET = re.compile(r"\[([^\[\]]{1,80})\]")
# opener class includes the *closing* smart quote too: the book
# occasionally sets ”cold, freezy” (p52-area layout glitches)
GLOSS = re.compile(r'^\s*[“”"]([^”“"]{1,80})[”“"]')
BOTH_TAIL = re.compile(r"\bboth:?\s*$")
# connector between two IPA variants of the same word:
# `[əs-kəs-ɛts] or preferably [skə-sɛl] "to begin"`, `or even in
# colloquial [stɾuk]` (p52), also bare `or`, `Coll.`, `Standard`.
# Only consulted when normal binding failed AND the previous bracket
# on the page bound successfully, so prose like "reduced to schwa"
# never matches (it has no `or`-headed ≤3-word shape).
CONNECTOR = re.compile(r"^[\s,]*(?:or(?:\s+[a-z]+){0,3}|Coll\.?:?|Standard:?)\s*$")
WINDOW = 120

# fonts whose letters are allowed between the Armenian word and the
# '[' — the transliteration (italic) and the IPA/phonetic families.
def _gap_font_ok(font: str) -> bool:
    return ("It" in font or "Phonetic" in font
            or "Pht" in font or "Special" in font)


TRANSLIT_TOKEN = re.compile(r"[a-zžščǰŕṙēěōə’'ʼ`´°˚.!?-]{1,25}", re.I)


def _single_translit_token(gap: str) -> bool:
    toks = gap.split()
    return len(toks) == 1 and bool(TRANSLIT_TOKEN.fullmatch(toks[0]))


def looks_ipa(s: str) -> bool:
    return bool(set(s) & IPA_MARKER) and not re.search(r"[A-Z0-9#]", s)


def load_pages():
    pages = collections.defaultdict(list)
    with open(JSONL) as fh:
        for line in fh:
            r = json.loads(line)
            pages[r["page"]].append(r)
    return pages


def _arm_run(text: str, end: int, spans=None, owner=None,
             phrase: bool = False) -> tuple[int, str]:
    """Collect the contiguous Armenian run ending at `end` (inclusive).
    Armenian block chars (letters + Armenian punctuation U+0530-058F),
    plus space/hyphen *between* Armenian chars, belong to the run.
    A Latin *letter* whose span is set in the Armenian font belongs to
    the run too — extraction artifacts like p55 `hագցնել` / p40
    `անդjադար` stay byte-faithful instead of truncating the word.

    In `phrase` mode (IPA transcribes several words) the run may also
    cross the ASCII punctuation this PDF stores inside Armenian text
    (`,` and `:`-for-`։` are ArialLatArm bytes — without them phrase
    entries like `Սա ի՞նչ է։ Վագ՞ր, թե՞ առյուծ։` break at the comma).
    Word mode must NOT cross those, or list separators between vocab
    items get swallowed (`..., ենք` regressions)."""
    k = end
    while k >= 0:
        c = text[k]
        arm_font = (spans is not None and "ArialLatArm" in
                    spans[owner[k]]["font"])
        ok = (ARM_RE.match(c) or c in " -’"
              or (arm_font and c.isalpha())
              or (phrase and arm_font and c in ",.:;!?"))
        if not ok:
            break
        k -= 1
    return k, text[k + 1:end + 1].strip(" -’,.:;!?")


def _squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def harvest(pages):
    rows, unbound = [], []
    for p in sorted(pages):
        spans = pages[p]
        parts, owner = [], []
        for i, s in enumerate(spans):
            t = s.get("text", "")
            parts.append(t)
            owner.extend([i] * len(t))
        text = "".join(parts)

        last_bound = None   # (bracket_end, row) of previous bound IPA
        for m in BRACKET.finditer(text):
            inner = m.group(1)
            if not looks_ipa(inner):
                continue
            phrase = " " in inner.strip() or "‿" in inner
            # walk back to nearest Armenian char
            j = m.start() - 1
            arm_end = None
            while j >= 0 and m.start() - j < WINDOW:
                if ARM_RE.match(text[j]):
                    arm_end = j
                    break
                j -= 1
            gap = text[arm_end + 1:m.start()] if arm_end is not None else ""
            note = ""
            if arm_end is not None:
                gap_wo_both = BOTH_TAIL.sub("", gap)
                bad = any(
                    (c.isalpha()
                     and not _gap_font_ok(spans[owner[arm_end + 1 + idx]]["font"]))
                    or c in "[]”“"
                    for idx, c in enumerate(gap_wo_both))
                if bad and _single_translit_token(gap_wo_both):
                    # the book occasionally sets a translit in Regular
                    # instead of italic (e.g. p42 "errord"); a lone
                    # translit-shaped token can't be English prose
                    bad = False
                if bad:
                    arm_end = None
            if arm_end is None:
                # second chance: an IPA *variant* of the previous bound
                # word — `[X] or preferably [Y] "gloss"` (p52). Without
                # this, the preferred variant and the gloss are silently
                # dropped and only the first (twice a book-typo) IPA
                # survives.
                if last_bound is not None:
                    prev_end, prev_row = last_bound
                    seg = text[prev_end:m.start()]
                    if len(seg) < 40 and CONNECTOR.match(seg):
                        gm = GLOSS.match(text[m.end():m.end() + 100])
                        gloss = _squash(gm.group(1)) if gm else ""
                        row = dict(prev_row, ipa=_squash(inner), gloss=gloss,
                                   note="preferably" in seg
                                        and "book-preferred variant"
                                        or "variant")
                        rows.append(row)
                        # the gloss printed after the last variant belongs
                        # to the word: backfill earlier variant rows
                        if gloss and not prev_row["gloss"]:
                            prev_row["gloss"] = gloss
                        last_bound = (m.end(), row)
                        continue
                unbound.append((p, inner, text[max(0, m.start() - 60):m.start()]))
                continue

            k, word = _arm_run(text, arm_end, spans, owner, phrase)
            if phrase:
                # interlinear liaison notes transcribe only part of a
                # sentence; if the captured run is far longer than the
                # IPA could cover, drop it rather than bind wrongly
                arm_letters = sum(c.isalpha() for c in word)
                ipa_letters = sum(c.isalpha() for c in inner)
                if arm_letters > 1.8 * ipa_letters + 2:
                    unbound.append((p, inner,
                                    text[max(0, m.start() - 60):m.start()]))
                    continue
            if BOTH_TAIL.search(gap):
                # reformed < classical pair: the run just found is the
                # classical spelling; the modern one sits before the `<`
                pre = text[:k + 1]
                classical = word
                lt = pre.rfind("<")
                if lt != -1 and k - lt < 60:
                    modern_end = _last_arm(pre, lt)
                    _, modern = _arm_run(pre, modern_end, spans, owner)
                    if modern:
                        word = modern
                        # italic between the modern word and '<' is its translit
                        gap = pre[modern_end + 1:lt]
                        note = (f"reformed spelling; classical {classical} "
                                f"pronounced the same")
            translit = _squash(re.sub(r"[<:]|\bboth\b", "", gap))
            gm = GLOSS.match(text[m.end():m.end() + 100])
            gloss = _squash(gm.group(1)) if gm else ""
            s0 = spans[owner[m.start()]]
            s1 = spans[owner[min(m.end() - 1, len(owner) - 1)]]
            rows.append(dict(page=p,
                             y0=round(min(s0["bbox"][1], s1["bbox"][1])),
                             y1=round(max(s0["bbox"][3], s1["bbox"][3])),
                             word=_squash(word), translit=translit,
                             ipa=_squash(inner), gloss=gloss, note=note))
            last_bound = (m.end(), rows[-1])

    # variant chains print the gloss once, after the last variant:
    # spread it across all glossless rows of the same (page, word)
    groups = collections.defaultdict(list)
    for r in rows:
        groups[(r["page"], r["word"], r["translit"])].append(r)
    for grp in groups.values():
        filled = next((r["gloss"] for r in grp if r["gloss"]), "")
        if filled:
            for r in grp:
                r["gloss"] = r["gloss"] or filled
    return rows, unbound


def _last_arm(text: str, before: int) -> int:
    j = before - 1
    while j >= 0 and not ARM_RE.match(text[j]):
        j -= 1
    return j


# ---------------------------------------------------------------------------
# Deviation filter (2026-07-03): the human table keeps only rows whose
# attested IPA differs from the *regular* reading of the spelling.
# Regular phenomena — canonicalized away before comparison — are:
# schwa epenthesis (ə ignored on both sides), initial/medial glide
# readings of ե/ո/և, generic intervocalic j-glide, nasal place
# assimilation (ŋ ɲ = n), ɾ/r and ʋ/v mergers, ʰ/h aspiration spelling,
# liaison/stress/intonation marks, morpheme hyphens and syllable dots.
# What survives is a genuine spelling↔pronunciation mismatch (mostly
# the voiced-stop devoicing/aspiration classes, ղ→χ clusters, հ-loss,
# վ→f). Validated 2026-07-03: all 47 golden respellings.tsv rows
# survive; 404 regular rows drop (incl. the whole schwa-epenthesis
# and reading-rules classes); per-variant calls verified (որդի keeps
# devoiced [ʋɔɾtʰi], drops spelling-pronunciation [ʋɔɾdi]).

_LETTER_IPA = {
    'ա': 'ɑ', 'բ': 'b', 'գ': 'g', 'դ': 'd', 'ե': '(j)ɛ', 'զ': 'z',
    'է': 'ɛ', 'ը': '', 'թ': 'th', 'ժ': 'ʒ', 'ի': 'i', 'լ': 'l',
    'խ': 'χ', 'ծ': 'ts', 'կ': 'k', 'հ': 'h', 'ձ': 'dz', 'ղ': 'ʁ',
    'ճ': 'tʃ', 'մ': 'm', 'յ': 'j', 'ն': 'n', 'շ': 'ʃ', 'ո': '(v)ɔ',
    'չ': 'tʃh', 'պ': 'p', 'ջ': 'dʒ', 'ռ': 'r', 'ս': 's', 'վ': 'v',
    'տ': 't', 'ր': 'r', 'ց': 'tsh', 'ւ': 'v', 'փ': 'ph', 'ք': 'kh',
    'և': '(j)ɛʋ', 'օ': 'ɔ', 'ֆ': 'f',
}
_VOWELS = 'ɑɛɔiu'
_COMBINING = re.compile(r'[̀-ͯ‿ˈˌ]')


def _canon_ipa(s: str, strip_parens: bool = True) -> str:
    import unicodedata
    s = unicodedata.normalize('NFD', s)
    if strip_parens:
        s = re.sub(r'\(.*?\)', '', s)   # optional segments like (j)
    s = _COMBINING.sub('', s)           # stress/intonation marks, ties
    s = (s.replace('ʰ', 'h').replace('ɾ', 'r').replace('ʋ', 'v')
          .replace('ŋ', 'n').replace('ɲ', 'n')
          .replace('ә', 'ə').replace('∫', 'ʃ').replace('a', 'ɑ'))
    s = re.sub(r'[ə\-.\s\[\]]', '', s)
    return unicodedata.normalize('NFC', s)


def _expected_ipa(word: str) -> tuple[str, bool]:
    """Regular reading of an Armenian spelling. Returns (ipa, unknown)
    where unknown=True if the word carries non-Armenian glyphs (the
    byte-faithful artifacts — can't compute an expectation for those)."""
    out, unknown = [], False
    w = word.lower()
    i = 0
    while i < len(w):
        c = w[i]
        if c == 'ո' and i + 1 < len(w) and w[i + 1] == 'ւ':
            out.append('u')
            i += 2
            continue
        if c in _LETTER_IPA:
            out.append(_LETTER_IPA[c])
        elif c not in ' -՛՜՞’,։:;.!?«»':
            unknown = True
        i += 1
    return ''.join(out), unknown


def _regular_re(exp: str):
    """Regex over canonicalized attested IPA: (j)/(v) become optional,
    plus an optional intervocalic glide between adjacent vowels."""
    pat = re.escape(_canon_ipa(exp, strip_parens=False))
    pat = pat.replace(r'\(j\)', 'j?').replace(r'\(v\)', 'v?')
    out = []
    for i, ch in enumerate(pat):
        out.append(ch)
        if ch in _VOWELS and i + 1 < len(pat) and pat[i + 1] in _VOWELS:
            out.append('j?')
    return re.compile('^' + ''.join(out) + '$')


def classify_deviation(word: str, ipa: str) -> str:
    """'deviant' | 'regular' | 'artifact' (non-Armenian glyphs in word)."""
    exp, unknown = _expected_ipa(word)
    if unknown:
        return 'artifact'
    if _regular_re(exp).match(_canon_ipa(ipa)):
        return 'regular'
    return 'deviant'


OUT_MD = HERE.parent / "topics" / "phonology" / "dumtragut_ipa_transcriptions.md"

MD_HEADER = """\
# Dum-Tragut IPA transcriptions — spelling↔pronunciation deviations

Words whose attested IPA in Dum-Tragut, *Armenian: Modern Eastern
Armenian* (Benjamins 2009) **differs from the regular reading of
their spelling**. Harvested from the extracted text layer (nearly all
from Chapter 1, Phonology, corpus pages 29–75), then filtered: rows
whose IPA is fully predicted by ordinary reading rules are excluded.

*Not* counted as deviations (canonicalized away by the filter):
schwa epenthesis (never written), initial/medial glide readings of
ե/ո/և and intervocalic glides, nasal place assimilation, ɾ/r and ʋ/v
notation, liaison/stress/intonation marks, morpheme hyphens. What
remains is the real divergence inventory: voiced-stop
devoicing/aspiration (մարդ [mɑɾtʰ]), ղ→[χ] clusters (աղջիկ
[ɑχtʃʰik]), հ-loss (աշխարհ [ɑʃχɑɾ]), վ→[f] (հարավ [hɑɾɑf]), etc.

**Regenerate:** `python3 dumtragut/harvest_ipa.py` (rewrites this file
and `dumtragut/out/ipa_index.tsv`). The TSV keeps **all** bound rows —
regular ones included — occurrence-level with citation-ready y-ranges
and a `deviant` column (`deviant` / `regular` / `artifact`); this file
is the deduplicated deviations-only human view.

Reading notes:

- **Pages are corpus pages** (PDF pages, as cited everywhere in this
  workspace: `dumtragut pN`). Book-print page = corpus page − 17
  (corpus p40 = book p23).
- **Byte-faithful.** Words are verbatim corpus bytes, including
  apparent book typos (p36 `ռարդիո` for ռադիո), stray Latin glyphs
  inside Armenian-font spans (p55 `hագցնել`, p40 `անդjադար`), and the
  1922–40 reformed-orthography demonstration spellings on p29
  (`վորակ`, `յերկիր`, …). Don't "fix" entries here — the Stop-hook /
  `citation-check` verify against these bytes.
- **Aspiration** is normally superscript `ʰ`; a few pages set a plain
  `h` (e.g. p71 `[kaɾthatsh]`) — kept as printed.
- **Appendix codepoint quirks** (pp52, 694, 698–699): the PDF text
  layer encodes schwa as Cyrillic `ә` (U+04D9, not ə U+0259) and ʃ as
  `∫` (U+222B) in a few Regular-font IPA spans (`[mәkәɾtit∫h]`).
  Rendered glyphs look right; the codepoints differ. Kept byte-faithful
  — mind this when substring-searching IPA across those rows.
- **Prosody marks** (per `dumtragut/phonetic.py`): ◌́ acute = primary
  stress, ◌̂ circumflex = interrogative intonation, `‿` = enclitic
  liaison.
- A word may carry **several IPA variants** — the book itself prints
  different realisations in different sections. The filter judges each
  variant separately: որդի keeps its devoiced [ʋɔɾtʰi] here while its
  spelling-pronunciation [ʋɔɾdi] (p37) stays TSV-only as `regular`.
- `ʋ` (hooked script-v, labiodental approximant) is the corrected
  decode of the glyph earlier read as ʔ — see the 2026-07-02 note in
  `dumtragut/phonetic.py`.
- **`variant` / `book-preferred variant` notes**: where the book gives
  several IPA for one word (`[əs-kəs-ɛts] or preferably [skə-sɛl]`,
  p52 schwa-epenthesis section), each variant is its own row; the
  first-printed one is *not* always the recommended one — trust the
  note. Occasionally the first-printed variant is itself a book typo
  (p52 սկսել `[əs-kəs-ɛts]`, շտկել `[əʃ-kət-ɛl]`).
- **Headwords are whatever the book transcribed** — mostly citation
  forms, but also inflected/negated/derived demo forms (կորոշեմ
  "I shall decide", Աննայի "Anna's") and one hypocoristic from the
  name-formation appendix (Մակո p699). An occasional Armenian glyph
  appears *inside* an IPA (p54 `[հəɾ-məʃ-tə-kɛl]`) — same
  byte-faithful policy.
"""


def _md_escape(s: str) -> str:
    return s.replace("|", "\\|")


def write_md(rows):
    # deviations only (artifacts kept: can't compute an expectation
    # for words carrying stray non-Armenian glyphs, and they are
    # near-certain deviants anyway)
    rows = [r for r in rows if r["deviant"] != "regular"]
    # dedupe by (word, ipa), aggregating pages and glosses
    uniq: dict[tuple, dict] = {}
    for r in rows:
        e = uniq.setdefault((r["word"], r["ipa"]),
                            dict(pages=[], glosses=[], translit=r["translit"],
                                 note=r["note"]))
        if r["page"] not in e["pages"]:
            e["pages"].append(r["page"])
        if r["gloss"] and r["gloss"] not in e["glosses"]:
            e["glosses"].append(r["gloss"])
        if not e["translit"] and r["translit"]:
            e["translit"] = r["translit"]
        if not e["note"] and r["note"]:
            e["note"] = r["note"]

    words, phrases = [], []
    for (word, ipa), e in uniq.items():
        row = (word, e["translit"], ipa, "; ".join(e["glosses"]),
               ", ".join(f"p{p}" for p in e["pages"]), e["note"])
        if " " in ipa:
            phrases.append(row)
        else:
            words.append(row)
    key = lambda r: r[0].lower()
    words.sort(key=key)
    phrases.sort(key=key)

    def table(fh, rows, with_note):
        cols = "| word | translit | IPA | gloss | pages |"
        dash = "|------|----------|-----|-------|-------|"
        if with_note:
            cols += " note |"
            dash += "------|"
        fh.write(cols + "\n" + dash + "\n")
        for w, tr, ipa, gl, pg, note in rows:
            cells = [w, tr, f"[{ipa}]", gl, pg] + ([note] if with_note else [])
            fh.write("| " + " | ".join(_md_escape(c) for c in cells) + " |\n")
        fh.write("\n")

    with open(OUT_MD, "w") as fh:
        fh.write(MD_HEADER + "\n")
        any_note = any(r[5] for r in words)
        fh.write(f"## Words — {len(words)} entries\n\n")
        table(fh, words, any_note)
        fh.write(f"## Phrases with a deviating word — {len(phrases)} "
                 "entries\n\n"
                 "Multi-word examples kept because at least one word in "
                 "them deviates from its spelling (e.g. դուրս → [dus], "
                 "կարդաց → [kaɾtʰatsʰ]).\n\n")
        table(fh, phrases, False)
    return len(words), len(phrases)


def main():
    pages = load_pages()
    rows, unbound = harvest(pages)
    for r in rows:
        r["deviant"] = classify_deviation(r["word"], r["ipa"])
    with open(OUT_TSV, "w") as fh:
        fh.write("page\ty0\ty1\tword\ttranslit\tipa\tgloss\tnote\tdeviant\n")
        for r in rows:
            fh.write("{page}\t{y0}\t{y1}\t{word}\t{translit}\t{ipa}"
                     "\t{gloss}\t{note}\t{deviant}\n".format(**r))
    nw, np = write_md(rows)
    tally = collections.Counter(r["deviant"] for r in rows)
    print(f"{len(rows)} bound occurrences -> {OUT_TSV} "
          f"({tally['deviant']} deviant / {tally['regular']} regular / "
          f"{tally['artifact']} artifact)")
    print(f"{nw} deviating words + {np} phrases -> {OUT_MD}")
    print(f"{len(unbound)} unbound IPA groups (chart cells / in-prose phonemes)")


if __name__ == "__main__":
    main()
