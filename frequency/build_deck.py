#!/usr/bin/env python3
"""Build the unified top-1000 deck from the frequency list + existing
card translations.

Pipeline:
1. Read `out/our_top_1000.tsv` (rank | lemma | count | sources).
2. Index translations from existing card files in `../cards/`:
     ../cards/sakayan/unit*_vocab.tsv     (col 0 → col 1, lemma form)
     ../cards/ghamoyan/fillers.tsv        (col 0 → col 1 "en / ru" combined)
     ../cards/frequency/gap_additions.tsv (col 0 → col 1 "en / ru" combined)
     ../cards/sakayan/paradigms.tsv       (col 0 → col 1; tag has verb:LEMMA
                                           so the verb infinitive resolves
                                           via the tag rather than col 0)
3. For each top-1000 lemma, pick best translation:
     a) Direct vocab / filler / gap entry (with translation from card).
     b) Paradigm-tag verb-infinitive entry (typical English: "to X").
     c) Local Wiktionary-dump dictionary (kaikki.org) via
        `dictionary.py`. No live API calls — the dump is downloaded
        once, compacted by `build_dictionary.py`, queried offline.
4. Emit `../cards/top_1000.tsv`:
     Armenian \t English / Russian \t tags  (with rank in tags)

Russian translations come for free where the source card already has
combined "en / ru" (fillers + gap additions). For other sources the
field will be English-only.

Usage:  python3 build_deck.py [--limit 1000]
"""

import argparse
import csv
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CARDS = ROOT / "cards"
SAKAYAN_CARDS = CARDS / "sakayan"
GHAMOYAN_CARDS = CARDS / "ghamoyan"
FREQUENCY_CARDS = CARDS / "frequency"

# Same tokenizer / lemmatizer / known-lemma machinery as build_ours.py
import build_ours  # noqa: E402
import dictionary  # noqa: E402


# ---------- helpers ----------


_ANNOTATION = re.compile(r"\s*[\[\(].*?[\]\)]")
_INTRAWORD_PUNCT = re.compile(r"[՚-՟]")

# Pattern for phonetic-respelling annotations attached to Armenian
# headwords in already-built sakayan card files: "Արամ [phonetic]".
# The bracket contains an Armenian re-spelling using the actual
# pronounced consonants (e.g. ընդունել → ընթունել), produced by
# `sakayan/phonetics.py` against Sakayan's own transliteration column.
_PHONETIC_ANNOT = re.compile(r"([Ա-Ֆա-ֈ՚-՟]+)\s*\[([Ա-Ֆա-ֈ՚-՟]+)\]")


def index_phonetic_respellings() -> dict[str, str]:
    """Scan all already-built sakayan TSVs and harvest the
    `lemma → respelling` map. Sakayan unit-vocab + dialogue files
    have the annotations baked in by `sakayan/make_anki.py` (which
    runs `phonetics.annotate` against Sakayan's transliteration).
    Each annotation we surface here is therefore book-cited.

    Skips `all.tsv` (concat of the per-unit files — would
    double-count) and `paradigms.tsv` (no transliteration column;
    no annotations present anyway).

    Returns lowercased lemma → lowercased respelling. Caller
    preserves original case from the input lemma.
    """
    hits: dict[str, str] = {}
    for path in sorted(SAKAYAN_CARDS.glob("*.tsv")):
        if path.name == "all.tsv":
            continue
        with path.open(encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                for cell in row:
                    for m in _PHONETIC_ANNOT.finditer(cell):
                        a, b = m.group(1).lower(), m.group(2).lower()
                        if a != b:
                            # First-seen wins — vocab files come first
                            # in sorted order.
                            hits.setdefault(a, b)
    return hits


# Hand-curated additions for documented voiced↔aspirated alternations
# that don't show up in sakayan TSVs (because the lemma is paradigm-
# only or hand-override only, with no transliteration column to
# annotate). Sources: armenian-grammar.md § "After extracting all 11
# units we have evidence the alternation is" + topics/phonology/
# voiced_aspirated_alternation.md. Keep this list narrow — only add
# entries that are textually attested in those notes.
PHONETIC_OVERRIDES: dict[str, str] = {
    "շաբաթ":   "շափաթ",
    "հոգնում": "հոքնում",
    "հոգնել":  "հոքնել",
}


def armenian_tokens(cell: str) -> list[str]:
    """All Armenian tokens in a card cell, with annotations stripped.
    Length tells you whether it's a single word or a phrase."""
    cleaned = _ANNOTATION.sub("", cell)
    cleaned = _INTRAWORD_PUNCT.sub("", cleaned)
    return [t.lower() for t in build_ours.ARMENIAN_TOKEN.findall(cleaned)]


def first_armenian_token(cell: str) -> str:
    toks = armenian_tokens(cell)
    return toks[0] if toks else ""


# ---------- translation indexing ----------


def index_card_translations() -> dict[str, list[dict]]:
    """Return {lemma_lower: [{translation, source, raw_armenian, single_word}, …]}.

    Multi-word entries are still indexed under their first token, but
    flagged single_word=False so single-word matches are preferred at
    pick time (e.g. `մի` from filler "մի խոսքով" doesn't override the
    real single-word meaning of `մի`)."""
    index: dict[str, list[dict]] = {}

    def add(lemma: str, translation: str, source: str, raw: str,
            single_word: bool) -> None:
        if not lemma or not translation.strip():
            return
        index.setdefault(lemma, []).append({
            "translation": translation,
            "source": source,
            "raw_armenian": raw,
            "single_word": single_word,
        })

    def index_simple_tsv(path: Path, source: str) -> None:
        if not path.exists():
            return
        with path.open(encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) < 2:
                    continue
                toks = armenian_tokens(row[0])
                if not toks:
                    continue
                add(toks[0], row[1].strip(), source, row[0],
                    single_word=(len(toks) == 1))

    for path in sorted(SAKAYAN_CARDS.glob("unit*_vocab.tsv")):
        index_simple_tsv(path, "sakayan-vocab")
    index_simple_tsv(GHAMOYAN_CARDS / "fillers.tsv", "ghamoyan-filler")
    index_simple_tsv(FREQUENCY_CARDS / "gap_additions.tsv", "frequency-gap")

    # Paradigms: pull the verb's clean English infinitive directly from
    # paradigms_data.py (each paradigm dict has `english_infinitive`).
    # This gives us "to have" instead of trying to mangle "I have" or
    # "I read (past)" into infinitive form.
    sys.path.insert(0, str(ROOT / "sakayan"))
    import paradigms_data  # noqa: E402
    for entry in paradigms_data.PARADIGMS:
        verb = entry.get("verb", "").lower()
        eng = entry.get("english_infinitive", "")
        if verb and eng and verb != "—":
            add(verb, eng, "sakayan-paradigm", verb, single_word=True)

    return index


# ---------- main ----------


# Hand-curated overrides for high-frequency particles where Wiktionary's
# first POS section gives a misleading or overly-narrow translation
# (e.g. Wiktionary returns "nobody" for ոչ, "a little" for մի — both
# correct as collocational phrase-translations but wrong for the bare
# lemma). These take priority over any source.
HAND_OVERRIDES: dict[str, str] = {
    "ոչ":     "no, not / нет, не",
    "մի":     "one, a; don't! / один, а; не (запрет)",
    "ու":     "and / и",
    "որ":     "that, which, who / что, который",
    "ինչ":    "what / что",
    "ինչու":  "why / почему",
    "որտեղ":  "where / где",
    "երբ":    "when / когда",
    "հա":     "yeah, yes / да, ага",
    "չէ":     "no, isn't (it?) / нет, не так ли",
    "այո":    "yes / да",
    "այստեղ": "here / здесь, тут",
    "այնտեղ": "there / там",
    "այս":    "this / этот",
    "այն":    "that / тот",
    "այդ":    "that / этот, тот",
    "սա":     "this (one) / это",
    "դա":     "that (one) / то",
    "նա":     "he, she / он, она",
    "ես":     "I / я",
    "դու":    "you (sg) / ты",
    "մենք":   "we / мы",
    "դուք":   "you (pl/formal) / вы",
    "նրանք":  "they / они",
    "ինձ":    "me / меня, мне",
    "քեզ":    "you (sg, obj) / тебя, тебе",
    "նրան":   "him, her / его, ему",
    "մեզ":    "us / нас, нам",
    "ձեզ":    "you (pl/formal, obj) / вас, вам",
    "նրանց":  "them / их, им",
    "իմ":     "my / мой",
    "քո":     "your (sg) / твой",
    "նրա":    "his, her / его, её",
    "մեր":    "our / наш",
    "ձեր":    "your (pl/formal) / ваш",
    "բա":     "well, what about / ну, а как же",
    "դե":     "well, come on / ну, давай",
    "հենց":   "exactly, just / именно, как раз",
    "ուրեմն": "so, then / значит, итак",
    "իսկ":    "but, and (contrast) / а, же",
    "բայց":   "but / но",
    "կամ":    "or / или",
    "ինչպես": "how, as / как",
    "շատ":    "very, much, many / очень, много",
    "քիչ":    "little, few / мало",
    "շնորհակալ": "thankful / благодарный",
    "խնդրեմ": "please; you're welcome / пожалуйста",
    "բարև":   "hello / привет",
    "կարող":  "able, can / способный, может",
    "դուրս":  "out, outside / снаружи, наружу",
    "շուտ":   "soon, quickly, early / скоро, быстро, рано",
    "իր":     "his/her (own, reflexive) / его/её (свой)",
    "ինքն":   "he/she himself / он/она сам(а)",
    "ինքը":   "he/she (emphatic) / он/она (сам)",
    "դրա":    "of that / того",
    "և":      "and / и",
    "նաև":    "also / также",
    "անգամ":  "time, instance; even / раз; даже",
    "հենց":   "exactly, just / именно, как раз",
    "բոլոր":  "all, every / все",
    "որպես":  "as, like / как, в качестве",
    "միայն":  "only / только",
    "հիմա":   "now / сейчас",
    "այսպես": "thus, like this / так, вот так",
    "այդպես": "thus, like that / так, вот так",
    "ինչպես": "how, as / как",
    "հայաստան": "Armenia / Армения",
    "եվրոպա": "Europe / Европа",
    "ամերիկա": "America / Америка",
    "ռուսաստան": "Russia / Россия",
    "դեպ":    "[fragment of դեպք 'case']",
    "շաբաթ":  "week; Saturday / неделя; суббота",
    "տուն":   "house, home / дом",
    "ընկեր":  "friend / друг",
    "տարի":   "year / год",
    "ամեն":   "every / каждый",
    "որոշ":   "some, certain / некоторый",
    "ուրիշ":  "other, different / другой",
    "ով":     "who / кто",
    "արի":    "come! (imp. of գալ) / иди!",
    "արա":    "hey, dude (voc.); do! (imp. of անել; մի՛ արա = don't) / эй, чувак; делай!",
    "դուր":   "liking (only in 'դուր է գալիս' = it pleases / нравится)",
    "տարեկան": "annual; -years-old / годовой; -летний",
    "թողնել":  "to leave, allow (colloq: թողել) / оставить, разрешать",
    # `(language)` parenthetical is kaikki/sakayan scaffolding; the
    # -երեն suffix already encodes "language" in Armenian.
    "հայերեն":   "Armenian / армянский",
    "անգլերեն":  "English / английский",
    "ֆրանսերեն": "French / французский",
    "գերմաներեն": "German / немецкий",
    # Replace dictionary-prose glosses ("Nth-person singular ...") with
    # actual card-usable translations.
    "կա":      "(there) is, exists / есть, имеется",
    "կարդում": "(am/is) reading (pres. ptcp of կարդալ) / читаю(-ет) (наст.)",
    "գնա":     "go! (imp. of գնալ) / иди!",
    "ասա":     "say! (imp. of ասել) / скажи!",
    "բեր":     "bring! (imp. of բերել) / принеси!",
    "ի_միջի_այլոց": "by the way / кстати",
    "տվեց":    "gave (3sg aor of տալ) / дал(-а)",
    # Verbose kaikki-prose glosses pruned to 2-3 senses.
    "զբաղվել":   "to be busy with, occupy oneself / заниматься",
    "ահա":       "here, behold / вот, гляди",
    "ներկայանալ": "to appear, present oneself / появиться, представиться",
    "գրասեղան":  "writing desk, desk / письменный стол",
    "անշուշտ":   "certainly, undoubtedly / конечно, безусловно",
    "աշխատել":   "to work / работать",
    "կարող":     "able, can; capable / способный, может",
    "հեռախոս":   "telephone, phone / телефон",
    "ազգանուն":  "surname / фамилия",
    # "alternative form of X" — replace with the actual meaning.
    "տաս":     "ten (var. of տասը) / десять",
    "սառը":    "cold (var. of սառն, before consonants) / холодный",
    "չափս":    "size, measure (var. of չափ) / размер",
    "քցել":    "to throw, drop (colloq var. of գցել) / бросить, ронять",
}


def best_translation(lemma: str, index: dict[str, list[dict]]) -> dict | None:
    """Pick best translation entry — but only from single-word card
    sources. Multi-word entries (`մի քիչ` "a little", `ոչ ոք`
    "nobody", `ստեղծել է` "has created") would otherwise leak their
    phrase-level meaning onto the bare first token (`մի, ոչ, ստեղծել`).
    Returns None if no single-word match — caller falls through to
    Wiktionary.
    """
    entries = [e for e in index.get(lemma, []) if e["single_word"]]
    if not entries:
        return None
    source_priority = {
        "sakayan-vocab": 0,
        "frequency-gap": 1,
        "ghamoyan-filler": 2,
        "sakayan-paradigm": 3,
    }

    def sort_key(e: dict) -> tuple:
        return (
            0 if e["raw_armenian"].strip().lower() == lemma else 1,
            source_priority.get(e["source"], 99),
        )

    return min(entries, key=sort_key)


def dictionary_lookup(lemma: str) -> str:
    """Best English gloss from the local Wiktionary dump (kaikki.org).
    No network calls. Returns "" if not in the dump.

    Replaces the live-API path that previously got us rate-limited.
    The dump is built one-time by `build_dictionary.py` from the
    `data/armenian.jsonl` download; re-run that script to refresh."""
    return dictionary.lookup(lemma)


# Proper nouns kept on the deck (first-and-foremost Armenian words):
# countries, regions, landmarks, ethnonyms — i.e. concepts an Armenian
# learner needs to be able to read and write. Personal given names
# don't qualify: someone called `Արամ` is a person, not a vocabulary
# concept.  Mirrors `validate_deck.KEEP_NAMES` — keep them in sync.
KEEP_NAMES = {
    "հայաստան", "հայ", "հայերեն", "հայկական",
    "երևան", "արարատ", "սևան", "կոտայք", "շիրակ",
    "գեղարքունիք", "լոռի", "սյունիք", "տավուշ", "վայոց",
    "եվրոպա", "ռուսաստան", "ամերիկա", "մոսկվա",
    "գերմանիա", "հունաստան", "ֆրանսիա", "իտալիա",
    "չինաստան", "ճապոնիա", "թուրքիա", "վրաստան",
    "ադրբեջան", "իրան",
}


def _is_personal_name(lemma: str) -> bool:
    """True if the dictionary classifies this lemma as a name only AND
    it isn't on the geography/landmark allow-list."""
    if "_" in lemma:
        return False
    if lemma.lower() in KEEP_NAMES:
        return False
    entries = dictionary.lookup_full(lemma)
    if not entries:
        return False
    return all(pos.lower() == "name" for pos, _ in entries)


def annotated_lemma(lemma: str, phonetic: dict[str, str]) -> str:
    """Return `lemma [phonetic]` when the pronounced form differs
    from the spelling, else just `lemma`. The respelling uses
    Armenian script — same convention as `sakayan/phonetics.py`.

    Multi-word units carry an underscore as the build-pipeline
    joiner (`մի_քիչ`); converted to a regular space here so the
    Anki card displays naturally as `մի քիչ`. HAND_OVERRIDES /
    phonetic-respelling lookups still key on the underscored form
    (that's the canonical pipeline identity), so the conversion
    is strictly a presentation step.
    """
    key = lemma.lower()
    respell = phonetic.get(key)
    display = lemma.replace("_", " ")
    if not respell or respell == key:
        return display
    return f"{display} [{respell}]"


def build(limit: int = 1000, with_dictionary: bool = True) -> None:
    top_path = HERE / "out" / "our_top_1000.tsv"
    out_path = CARDS / "top_1000.tsv"

    index = index_card_translations()
    print(f"Indexed {len(index)} unique-lemma translation sources",
          file=sys.stderr, flush=True)

    phonetic = index_phonetic_respellings()
    phonetic.update(PHONETIC_OVERRIDES)
    print(f"Indexed {len(phonetic)} phonetic respellings "
          f"({len(PHONETIC_OVERRIDES)} hand-curated)",
          file=sys.stderr, flush=True)

    rows_out: list[list[str]] = []
    stats = {"vocab": 0, "filler": 0, "gap": 0, "paradigm": 0,
             "dictionary": 0, "no-translation": 0}
    skipped_names = 0

    with top_path.open(encoding="utf-8") as f:
        all_input_rows = [r for r in csv.reader(f, delimiter="\t") if len(r) >= 4]

    rank_n = 0
    for row in all_input_rows:
        _orig_rank, lemma, count, _src = row
        if rank_n >= limit:
            break

        # Filter personal names. Per user policy: keep proper nouns
        # only when they're "first and foremost an Armenian word"
        # (countries, regions, landmarks). Personal given names
        # don't qualify and shouldn't take a slot in the top-1000.
        if _is_personal_name(lemma):
            skipped_names += 1
            continue

        rank_n += 1

        translation = ""
        source = ""
        # Hand-curated override has priority — high-frequency
        # particles where Wiktionary's first-gloss is misleading.
        if lemma in HAND_OVERRIDES:
            translation = HAND_OVERRIDES[lemma]
            source = "hand-override"
            stats.setdefault("hand-override", 0)
            stats["hand-override"] += 1
            tags = f"frequency top-1000 rank-{rank_n:04d} src-{source}"
            rows_out.append([annotated_lemma(lemma, phonetic), translation, tags])
            if rank_n <= 10 or rank_n % 50 == 0:
                print(f"  rank {rank_n:4d}  {lemma:25s}  [{source}]  "
                      f"{translation[:60]}", file=sys.stderr, flush=True)
            continue

        entry = best_translation(lemma, index)
        if entry:
            translation = entry["translation"]
            source = entry["source"]
            if source == "sakayan-vocab":
                stats["vocab"] += 1
            elif source == "ghamoyan-filler":
                stats["filler"] += 1
            elif source == "frequency-gap":
                stats["gap"] += 1
            elif source == "sakayan-paradigm":
                stats["paradigm"] += 1
        elif with_dictionary:
            translation = dictionary_lookup(lemma)
            if translation:
                source = "dictionary"
                stats["dictionary"] += 1
            else:
                source = "—"
                stats["no-translation"] += 1
        else:
            source = "—"
            stats["no-translation"] += 1

        if not translation.strip():
            # Skip empty-gloss rows entirely — they're either
            # lemmatizer leaks (ուսանողներն, գրքեր), unfiltered
            # surnames (պալյան, սարյան), spelled-out numerals
            # (հիսունութ), or stems no source covers. Keeping
            # them makes the deck noisy without educational value.
            # The original rank is preserved on emitted rows so
            # rank-NNNN still reflects frequency-list position.
            stats.setdefault("skipped-empty", 0)
            stats["skipped-empty"] += 1
            continue

        tags = f"frequency top-1000 rank-{rank_n:04d} src-{source}"
        rows_out.append([annotated_lemma(lemma, phonetic), translation, tags])

        if rank_n <= 10 or rank_n % 50 == 0:
            print(f"  rank {rank_n:4d}  {lemma:25s}  [{source}]  "
                  f"{translation[:60]}", file=sys.stderr, flush=True)

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for r in rows_out:
            w.writerow(r)

    print(f"\nWrote {len(rows_out)} cards → {out_path}", file=sys.stderr)
    if skipped_names:
        print(f"Filtered {skipped_names} personal-name lemma(s) "
              f"(see KEEP_NAMES allow-list)", file=sys.stderr)
    print("Translation sources:", file=sys.stderr)
    for src, n in stats.items():
        pct = 100 * n / len(rows_out) if rows_out else 0
        print(f"  {src:18s}  {n:4d}  ({pct:.1f}%)", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--no-dictionary", action="store_true",
                    help="skip the local Wiktionary-dump dictionary fallback")
    args = ap.parse_args()
    build(args.limit, with_dictionary=not args.no_dictionary)


if __name__ == "__main__":
    main()
