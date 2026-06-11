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

# Armenian intra-word punctuation that the source text may carry in
# the *spelled* form but not in the lemma key — `՞` (question stress
# mark) is the common one (`Առաջի՞ն` for `Առաջին`). Strip these
# before storing the index key so dictionary-form lemma lookups
# match. The respelled form on the right side of `[…]` doesn't
# normally carry these.
_INTRAWORD_PUNCT_STRIP = re.compile(r"[՚-՟]")


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
                        a = _INTRAWORD_PUNCT_STRIP.sub(
                            "", m.group(1)).lower()
                        b = _INTRAWORD_PUNCT_STRIP.sub(
                            "", m.group(2)).lower()
                        if a and a != b:
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
    # ջ → չ — sakayan transliterations attest this devoicing
    # systematically within specific lexicalized roots
    # (վերջ-, առաջ-, մեջ-, առողջ-). Bare-root and additional
    # derivatives below are inferred from the same root pattern.
    # Counterexample on record: հաջորդ [հաջորթ] keeps ջ voiced
    # — so this is *lexical-root regularity*, not a phonological
    # rule. See topics/phonology/voiced_aspirated_alternation.md
    # and errors/2026-05-09-005 lineage.
    "մեջ":     "մեչ",
    "վերջ":    "վերչ",         # bare root; derivatives all attest չ
    "միջոց":   "միչոց",         # միջ- stem (extension of մեջ-)
    "միջև":    "միչև",
    "միջին":   "միչին",
    "միջազգային": "միչազգային",
    "անմիջապես":  "անմիչապես",
    # ղջ cluster — both consonants devoice (ղ → χ, ջ → չ).
    # Parnasyan p346 attests `աղջիկ [ахчик]`, `ամբողջ [амбохч]`.
    # Different mechanism from the lexical-root regularity above:
    # this is cluster devoicing, applies wherever the ղջ cluster
    # appears. We mark only the ჯ → չ change in the respell
    # (matching sakayan's convention in `առողջություն →
    # առողչություն`); the ղ surface devoicing is documented in
    # the topic file but not encoded here.
    "աղջիկ":   "աղչիկ",
    "ողջ":     "ողչ",
    "ամբողջ":  "ամբողչ",
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
    # Oblique personal pronouns — case indication in the gloss
    # (item 7). Forms are dat/acc; for plural դա/նա the same form
    # also serves the genitive (gen=dat syncretism).
    "ինձ":    "me (dat/acc of ես) / меня, мне",
    "քեզ":    "you (dat/acc of դու) / тебя, тебе",
    "նրան":   "him, her (dat/acc of նա) / его, ему",
    "մեզ":    "us (dat/acc of մենք) / нас, нам",
    "ձեզ":    "you, pl/formal (dat/acc of դուք) / вас, вам",
    "նրանց":  "them; their (gen/dat of նրանք) / их, им",
    "իմ":     "my / мой",
    "քո":     "your (sg) / твой",
    "նրա":    "his, her / его, её",
    "մեր":    "our / наш",
    "ձեր":    "your (pl/formal) / ваш",
    "բա":     "well, what about / ну, а как же",
    "դե":     "well, come on / ну, давай",
    "ուրեմն": "so, then / значит, итак",
    "իսկ":    "but, and (contrast) / а, же",
    "բայց":   "but / но",
    "կամ":    "or / или",
    "շատ":    "very, much, many / очень, много",
    "քիչ":    "little, few / мало",
    "շնորհակալ": "thankful / благодарный",
    "խնդրեմ": "please; you're welcome / пожалуйста",
    "բարև":   "hello / привет",
    "դուրս":  "out, outside / снаружи, наружу",
    "շուտ":   "soon, quickly, early / скоро, быстро, рано",
    "իր":     "his/her own (reflexive); thing, item / его/её (свой); вещь",
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
    # `դուր` ranks top-1000 because the lemmatiser counts the first
    # half of the verbal idiom `դուր գալ` as a separate token —
    # auxiliaries (եմ, ես, է, …) interpolate between the two halves
    # so the MWU regex doesn't catch inflected forms (`դուր է գալիս`,
    # `դուր եկավ`, `դուր է եկել`). The bare lemma is treated here
    # as a stand-in for the full idiomatic verb-phrase. See
    # DISPLAY_OVERRIDES below: the Armenian column is rewritten to
    # show `դուր գալ` so the learner sees the whole phrase.
    "դուր":   "to please, to be liked (ինձ դուր է գալիս — I like it) / нравиться",
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
    # Inflected forms with idiomatic standalone meaning — translate
    # the actual sense, not the grammatical description.
    "մասին":    "about, concerning (քո մասին — about you) / о, про",
    "չկա":      "(there) isn't, doesn't exist / нет, не имеется",
    "չէր":      "wasn't (3sg) / не был(-а)",
    "նշանված":  "engaged (to be married); marked / помолвленный; отмеченный",
    "սկսվել":   "to begin, start (intr.) / начинаться",
    "զարմացնել": "to amaze, surprise (someone) / удивить, поразить",
    "հագել":    "to put on, wear (var. of հագնել) / надеть, одеть",
    # Negative copula forms (չ + էի/էիր/էր/էինք/էիք/էին) — distinct
    # high-frequency forms each carrying person/number, idiomatic
    # in spoken Armenian.
    "չէի":      "wasn't (1sg) / не был(-а)",
    "չէիր":     "weren't (2sg) / ты не был(-а)",
    "չէին":     "weren't (3pl) / не были",
    "չէիք":     "weren't (2pl/formal) / вы не были",
    "չէինք":    "weren't (1pl) / мы не были",
    # Mediopassive verbs — distinct from their active counterparts.
    "կոչվել":   "to be called, be named / называться",
    "կիրառվել": "to be applied, used / применяться",
    "գտնվել":   "to be located, be found / находиться",
    "ծնվել":    "to be born / родиться",
    "կառուցվել": "to be built / строиться",
    # Causative — also distinct from base verb.
    "դարձնել":   "to make, turn (sth) into / превратить, делать",
    "ներկայացնել": "to present, introduce / представить, представлять",
    # Resultative participle used as adjective.
    "կապված":    "tied, connected; related to / связанный, привязанный",
    # Diminutive — distinct lexical item.
    "թիթեռնիկ":  "little butterfly / бабочка (уменьш.)",
    # Adverb derived from adjective (locative form).
    "հիմնականում": "mainly, basically / в основном, главным образом",
    # Colloquial / dialectal — high-frequency variants.
    "էն":        "that (colloq dialectal of այն) / то (разг.)",
    "տուր":      "give! (imp. of տալ) / дай!",
    # Fixed expression — at-home reading is idiomatic.
    "տանը":      "at home (def. dat. of տուն) / дома",
    # Trim verbose dictionary gloss.
    "ուսումնական": "academic, school (related) / учебный, школьный",
    "պարզել":     "to clarify, clean, purify / прояснить, очистить",
    # Postposition is the dominant sense; "the inside" is rare.
    "մեջ":        "in, inside (տան մեջ — in the house); among / в, внутри; среди",
    # Both senses: noun "example" + adverbial "for example".
    "օրինակ":     "example; for example (also: օրինակի համար) / пример; например",
    # Numeral, not the rare "lettuce" noun sense kaikki listed first.
    "հազար":      "thousand / тысяча",
    # Postposition senses are dominant for high-frequency
    # function-word lemmas; kaikki lists noun first.
    "համար":      "for (ինձ համար — for me); number / для (послелог); номер",
    "հետ":        "with (ընկերոջ հետ — with a friend); back (noun) / с; назад",
    # Vocabulary that the source frequency list has in top-1000 but
    # which the offline kaikki dictionary doesn't cover. Without
    # these, the build_deck.py "skipped-empty" filter would silently
    # drop them. Glosses vetted by sub-agent (2026-05-14 session).
    "առօրյա":     "everyday, daily routine / повседневный, будни",
    "արտահայտել": "to express / выражать",
    "կիրառություն": "use, application / применение",
    "գործածություն": "use, usage / употребление",
    "ոճական":     "stylistic / стилистический",
    # NB: `դուր` is overridden above (dative-experiencer idiom
    # `դուր գալ`); no duplicate key here — dict literals keep the
    # last value, which silently shadowed the curated gloss.
    "պայմանավորված": "conditioned by, due to / обусловленный",
    "միավոր":     "unit / единица",
    "այլև":       "also, moreover / также, к тому же",
    "հուզված":    "agitated, moved, emotional / взволнованный",
    "ժողովրդախոսակցական": "vernacular, colloquial / народно-разговорный",
    "նշանակություն": "meaning, significance / значение",
    "միջնակարգ":  "secondary (school) / средний (о школе)",
    "հանրակրթական": "general-education, public-school / общеобразовательный",
    "հանրույթ":   "community / сообщество",
    "հասկացություն": "concept, notion / понятие",
    "շարահյուսական": "syntactic / синтаксический",
    "գործառական": "functional / функциональный",
    "իրադրություն": "situation / ситуация, обстановка",
    "արտահայտչական": "expressive / выразительный",
    "հուզական":   "emotional / эмоциональный",
    "միևնույն":   "the very same / тот же самый",
    "նորմ":       "norm / норма",
    "հաճախականություն": "frequency / частотность",
    "դժվարություն": "difficulty / трудность",
    "առանձնահատկություն": "peculiarity, distinctive feature / особенность",
    "վերաբերմունք": "attitude / отношение",
    "զբաղմունք":  "occupation, pastime / занятие",
    # Discourse particle (more frequent than the verbal 2sg of
    # `կարծել` "to think"); pedagogically "as if/seemingly" wins.
    "կարծես":     "as if, seemingly / как будто, кажется",
    "երանգավորել": "to tint, shade, give a tone / оттенять, придавать оттенок",
    # Disambiguation: `թվել` = "to seem" (most common) vs. rare
    # "to number/enumerate" homonym; default to the high-frequency
    # sense.
    "թվել":       "to seem / казаться",
    # ⚠ blocker fixes from 2026-05-14 editorial pass — sub-agent
    # flagged " / " misused as comma-separator (deck schema reserves
    # " / " for English-Russian pairs).
    "առնել":      "to take, to buy / брать, покупать",
    "զարկել":     "to hit, to strike / ударить, бить",
    "ենթակա":     "subject (grammatical); subordinate / подлежащее; подчинённый",
    # ⚙ suggestion fixes — sense-priority + gloss-naturalness.
    "առաջ":       "before, ago; forward / до, тому назад; вперёд",
    "նպաստել":    "to contribute, to foster / способствовать, содействовать",
    "փնտրել":     "to look for, to search / искать",
    "անծանոթ":    "unfamiliar; stranger / незнакомый; незнакомец",
    "վերաբերել":  "to concern, to relate to / касаться, относиться",
    "հան":        "grandma, granny (colloq.) / бабушка (разг.)",
    "նշանակել":   "to mean / значить, обозначать",
    # MWUs (multi-word units): the build_ours.py pipeline merges
    # high-frequency phrases into single underscored "lemmas".
    # `best_translation` rejects multi-word card-source entries to
    # prevent phrase-meaning leaking onto bare first tokens, so
    # MWUs need to land via HAND_OVERRIDES. `annotated_lemma`
    # converts the underscore to a space for the card display
    # (`մի_քիչ` → `մի քիչ`), but the lookup key here stays
    # underscored — that's the canonical pipeline identity.
    "մի_քիչ":     "a little, a bit / немного, чуть-чуть",
    "ոչ_միայն":   "not only / не только",
    "մի_շարք":    "a series, a number of / ряд, несколько",
    "ամեն_ինչ":   "everything / всё",
    "մի_օր":      "one day, someday / однажды, как-то раз",
    # ⚠ blocker fixes from 2026-06-01 editorial pass — kaikki's
    # natural sense order picked a marked/wrong sense over the
    # learner-useful one. Each fix has a golden_glosses.tsv anchor.
    # `գոյական` is a grammar term ("noun" the word-class) — kaikki
    # led with the adjective "existing".
    "գոյական":    "noun (grammatical term) / существительное",
    # Ordinal, not the adverb "fifthly" that kaikki led with.
    "հինգերորդ":  "fifth / пятый",
    # kaikki's "outer member, limb" is an odd lead; the everyday
    # senses are member (of a group/body) and limb.
    "անդամ":      "member; limb / член; конечность",
    # Jussive particle — see topics/morphology/jussive_thogh_subjunctive.md.
    # Russian пусть. "let (him/it…)" is the core sense; sakayan gave
    # the bare "may, let".
    "թող":        "let (him/it/them); may / пусть",
    # ⚙ suggestion fixes — sense-priority over kaikki's lead sense.
    # տեսություն's dominant sense is "theory"; kaikki led "survey;
    # roundup".
    "տեսություն": "theory; survey / теория; обзор",
    # հարցում's modern dominant sense is "survey, poll"; kaikki's
    # "formal address" is odd.
    "հարցում":    "survey, poll; inquiry / опрос; запрос",
    # Contrastive conjunction "whereas" dominates the temporal
    # "meanwhile" kaikki led with.
    "մինչդեռ":    "whereas, while / тогда как, в то время как",
    # Reorder: core sense is "until/till", not "as far as".
    "մինչև":      "until, till; up to / до, вплоть до",
    # Trim kaikki's 4-synonym stacks to the learner-useful lead.
    "սովորաբար":  "usually / обычно",
    "ձգտում":     "aspiration, striving / стремление",
    # ── 2026-06-03 user card-review pass ──────────────────────────
    # Homograph-trap sense fixes, pronoun citation forms, Russian
    # added, short embedded examples for function words. kaikki's
    # lead (or only) sense was the rare/wrong one for these high-
    # frequency tokens. Each has a golden_glosses.tsv anchor.
    "թե":         "that; whether; or / что; ли; или",
    "խոսք":       "word; speech, talk / слово; речь",
    "տարբեր":     "different, various / разный, различный",
    "իրենք":      "they (themselves) / они (сами)",
    # Genitive/dative of իրենք — citation note like նրա/նրան.
    "իրենց":      "their; them (gen/dat of իրենք) / их, им",
    "կողմ":       "side, direction; party / сторона; направление",
    "սեփական":    "own, one's own; private / собственный; частный",
    # Syncretic gen/dat/acc of ով (animate): "whose / to whom / whom".
    "ում":       "whom; whose; to whom (gen/dat/acc of ով) / кому, чей, кого",
    # kaikki picked the rare adj "scarlet"; corpus + kaikki's own adv
    # sense show this is the Western-Armenian/dialectal form of էл.
    "ալ":         "also, too (W. Arm., dialectal, = էլ) / тоже, и",
    "իմաստ":      "sense, meaning / смысл, значение",
    "սակայն":     "however, but, yet / однако, но",
    "դրանք":      "those; they (inanimate) / те; они",
    "երևույթ":    "phenomenon; appearance (բնական երևույթ) / явление",
    "տվյալ":      "given, this; data (pl. տվյալներ) / данный; данные",
    # kaikki led the adj "more than"; core sense is the adverb "up".
    "վեր":        "up, upward; upper part / вверх; верх",
    "անվանի":     "famous, renowned / знаменитый, именитый",
    "փոխարեն":    "instead of (իմ փոխարեն — instead of me) / вместо",
    # Second wave — homograph traps surfaced by the Russian-
    # augmentation sweep: postpositions glossed as bare nouns, plus
    # the ` / `-as-comma bug. Each has a golden anchor.
    "դեմ":        "against (պատերազմի դեմ — against war); opposite / против",
    "տակ":        "under (սեղանի տակ — under the table); bottom / под; низ",
    # Postpositions whose dictionary gloss carried no usage example
    # (item 3 — every pre-/postposition gets one).
    "վրա":        "on, upon (սեղանի վրա — on the table) / на, поверх",
    "ըստ":        "according to (ըստ օրենքի — according to the law) / согласно, по",
    "առանց":      "without (առանց քեզ — without you) / без",
    "պես":        "like, as (քո պես — like you) / как, подобно",
    "դեպի":       "towards (դեպի տուն — towards home) / к, по направлению к",
    "շուրջ":      "around (սեղանի շուրջ — around the table) / вокруг",
    "ներս":       "in, inside (ներս մտնել — to enter) / внутрь, внутри",
    "հավանել":    "to like, to approve; to agree / нравиться, одобрять",
    "լսել":       "to hear, to listen; to obey / слышать, слушать; слушаться",
    # ` / ` was misused as an English comma-separator (the deck
    # reserves ` / ` strictly for the English/Russian boundary).
    "լալ":        "to cry, to weep / плакать, рыдать",
    "ելնել":      "to go out, to rise / выходить, подниматься",
    # 2026-06-03 deck-vs-requirements review fixes.
    # `/` was misused as an English sense-separator + no Russian.
    "միթե":       "really?, is it so? (interrogative particle) / разве, неужели",
    # Comparative conjunction — function word, needs Russian (req §3).
    "քան":        "than (comparative) / чем",
    # Postposition — needs Russian + an example (req §3, §6).
    "ընթացքում":  "during, in the course of (դասի ընթացքում — during the class) / в течение",
    # W.-Armenian / colloquial pronoun; Eastern standard is նա (also
    # on deck). Labelled to avoid presenting a dialectal form as neutral.
    "ան":         "he, she (W. Arm. / colloq.; Eastern: նա) / он, она",
    # ── 2026-06-11 adversarial review ─────────────────────────────
    # Homograph traps: kaikki's lead (or only) sense is a rare/wrong
    # homograph for these high-frequency tokens. Corpus-confirmed;
    # each has a golden_glosses.tsv anchor.
    # Existential past dominates the corpus (~10/14 hits: sakayan
    # p223 `Տերևախիտ մի ծառ կար անտառի մեջ`, p404, ghamoyan p95);
    # kaikki led the noun "seam | sewing" (1 hit, ghamoyan p86
    # `կար էր անում`). Keep sewing as a labelled secondary sense.
    "կար":       "there was (past of կա); sewing (կար ու ձև — tailoring) / было; шитьё",
    # kaikki led "knowing, having the knowledge" (rare literary
    # homograph); the everyday word is the river.
    "գետ":       "river / река",
    # kaikki led "more, more than"; corpus usage is additive
    # (`Երևանում ևս` — "in Yerevan too").
    "ևս":        "also, too, as well / тоже, также",
    # kaikki led "paron, baron" (the Cilician feudal title); the
    # living sense is the address term (corpus: `պարոն Սարյան`).
    "պարոն":     "mister, sir (պարոն Սարյան — Mr. Saryan) / господин",
    # kaikki led "wherefrom, whence" (archaic); the living sense is
    # the conjunction (corpus: `ուստի ուզում եմ գալ`).
    "ուստի":     "therefore, hence / поэтому",
    # kaikki led the noun "passage, pass"; the high-frequency use is
    # clock-time "past" (corpus: `Ութն անց կես է`, `անց քառորդ`).
    "անց":       "past (ութն անց կես — half past eight; անց կենալ — to pass) / после (о времени)",
}


# Inflected forms whose lemma is already on the deck (or whose
# standalone sense is just "the X" / "(to) the Xs" with no
# pedagogical value beyond what the lemma carries). Skip these so
# the slot goes to a lemma that contributes new content.
SKIP_LEMMAS: set[str] = {
    # Lemma already on deck — these are redundant inflected forms.
    "հասկանում",   # imperfective converb of հասկանալ (rank 523)
    "խոսում",      # simultaneous converb of խոսել (rank 475)
    "մեկը",        # def. nom. sg. of մեկ (rank 87)
    "ծաղիկները",   # def. nom. pl. of ծաղիկ (rank 767)
    "ձմռանը",      # def. dat. sg. of ձմեռ (rank 109)
    "շաբաթը",      # def. nom. sg. of շաբաթ (rank 460)
    # Lemma not on deck but the inflected form has no standalone
    # value — would just clutter ("the book", "to the clouds").
    "գիրքը",       # def. nom. sg. of գիրք
    "ամպերին",     # def. dat. pl. of ամպ
    # New skips after the corpus expansion (sakayan + ghamoyan
    # JSONL added) surfaced more inflected duplicates.
    "լինում",      # imperfective participle of լինել
    "եղել",        # past participle of լինել
    "ուտում",      # imperfective participle of ուտել
    "կերել",       # past participle of ուտել
    "գործում",     # imperfective converb of գործել
    "գնում",       # imperfective converb of գնալ (rank 132) /
                   # գնել (rank 959), both in deck; kaikki glossed it
                   # the rare noun "purchase" (homograph trap, rank 114)
    "լինեի",       # 1sg subj/optative of լինել
    "խոսքը",       # def. nom. sg. of խոսք
    "խոսքն",       # def. variant of խոսք
    "խոսքին",      # def. dat. sg. of խոսք
    "գլուխը",      # def. nom. sg. of գլուխ
    "միտքը",       # def. nom. sg. of միտք
    # 2026-06-03 homograph-trap / corpus-noise removals (user card
    # review). High-frequency tokens whose ONLY kaikki sense is a
    # rare literary noun — the token is actually a grammatical form
    # or tokenizer spill, NEVER the dictionary headword. See
    # llm-workflow.md § "Homograph trap" and check_morpheme_noise.
    "մերի",        # gen of substantivized possessive մերը ("ours")
                   # + tokenizer spill from Ամերիկա; kaikki glossed
                   # it the rare noun "woods, forest" at rank ~39.
    "ներ",         # the plural suffix -ներ, mis-tokenized from the
                   # ghamoyan grammar book (ԴՄ-ներ); kaikki: the
                   # rare noun "sister-in-law".
    "մեկն",        # definite nom. sg. of մեկ (rank 42, in deck);
                   # kaikki's rare adverb "upright" is the wrong sense.
    "տաս",         # colloquial reduction of literary տասը "10" (on
                   # deck); variant-of-deck-lemma, per the literary-
                   # lemma rule (req §5/§8).
    "ինք",         # W. Arm. / colloq variant of ինքը
    "ել",          # rare, ambiguous (could be ելք or "and-too")
    # 2026-05-14 additions: vetted by sub-agent. Three buckets:
    #
    # (a) inflected forms / variants of lemmas already in deck.
    "բառեր",       # pl of բառ
    "բառերն",      # def pl of բառ
    "դրանց",       # gen-dat pl of դա/դրանք
    "դրան",        # dat sg of դա
    "սրան",        # dat sg of սա
    "ասաց",        # 3sg aor of ասել
    "ձևեր",        # pl of ձև
    "մարդկանց",    # gen-dat pl of մարդ
    "մարդիկ",      # nom pl of մարդ
    "մարդու",      # gen-dat sg of մարդ
    "մարդուն",     # dat-def sg of մարդ
    "իրեն",        # dat/acc reflexive of ինքը
    "գործածվել",   # passive infinitive of գործածել
    "գործածվող",   # present participle of գործածել
    "կարդել",      # variant/inflected of կարդալ
    "տան",         # gen-dat sg of տուն
    "որն",         # def form of որը
    "եկել",        # perfect participle of գալ
    "եկան",        # 3pl aor of գալ
    "եկեք",        # 2pl imp of գալ
    "գնաց",        # 3sg aor of գնալ
    "գնանք",       # 1pl subj of գնալ
    "գնացել",      # perfect participle of գնալ
    "հայեր",       # pl of հայ
    "տեսել",       # perfect participle of տեսնել
    "տեսա",        # 1sg aor of տեսնել
    "խաղել",       # variant/inflected of խաղալ
    "խաղա",        # 2sg imp of խաղալ
    "խաղացել",     # perfect participle of խաղալ
    "աչքեր",       # pl of աչք
    "սկսեց",       # 3sg aor of սկսել
    "որդիներ",     # pl of որդի
    "դրել",        # perfect/variant of դնել
    "դրվել",       # passive infinitive of դնել
    "հյուրեր",     # pl of հյուր
    "հարցեր",      # pl of հարց
    "հարցրեց",     # 3sg aor of հարցնել
    "հարցումներ",  # pl of հարցում
    "շատեր",       # substantivized pl of շատ
    "մասեր",       # pl of մաս
    "կապեր",       # pl of կապ
    "արտահայտվել", # passive infinitive of արտահայտել
    "առանձնահատկություններ", # pl of առանձնահատկություն
    "զգել",        # variant/inflected of զգալ
    "գրվել",       # passive infinitive of գրել
    "երեխաներ",    # pl of երեխա
    "օրեր",        # pl of օր
    "ծրագրեր",     # pl of ծրագիր
    "գործեր",      # pl of գործ
    "դարեր",       # pl of դար
    "համարվել",    # passive infinitive of համարել
    "նախադասություններ", # pl of նախադասություն
    "գրքեր",       # pl of գիրք
    "ծառեր",       # pl of ծառ
    "կանայք",      # suppletive nom pl of կին
    "կանանց",      # gen-dat pl of կին
    "արեց",        # 3sg aor of անել
    "արել",        # perfect participle of անել
    "սիրո",        # gen sg of սեր
    "տարբերվել",   # passive infinitive of տարբերել
    "ունեցել",     # perfect participle of ունենալ
    "ինն",         # def form of ինը
    "գիտել",       # present-stem variant of գիտենալ
    "զարգացման",   # gen of զարգացում
    "հաղորդակցման", # gen of հաղորդակցում
    # (b) OCR / lemmatizer noise — bare suffixes, truncated stems,
    # spurious `-ել` appended to nouns.
    "լեզվել",      # spurious -ել on լեզու
    "խոսքել",      # spurious -ել on խոսք
    "դեպքել",      # spurious -ել on դեպք
    "երևանել",     # spurious -ել on Երևան
    "հայաստանել",  # spurious -ել on Հայաստան
    "քաղաքել",     # spurious -ել on քաղաք
    "դպրոցներել",  # spurious -ել on դպրոցներ
    "շրջանել",     # spurious -ել on շրջան
    "ոլորտել",     # spurious -ել on ոլորտ
    "ացած",        # bare participle suffix
    "բառայ",       # truncation of բառային
    "ժարգոնայ",    # truncation of ժարգոնային
    "իմաստայ",     # truncation of իմաստային
    "ություն",     # bare noun suffix
    "թյուն",       # bare noun suffix fragment
    "խմբ",         # truncated stem of խումբ
    "ձեռ",         # truncated stem of ձեռք
    "սրտ",         # truncated stem of սիրտ
    "նկատ",        # truncated stem of նկատել
    "խոս",         # truncated stem of խոսել/խոսք
    "լինե",        # truncated stem of լինել
    "կլին",        # truncated future stem of լինել
    "գրք",         # truncated stem of գիրք
    "անհարկ",      # truncation of անհարկի
    # (c) Surnames / proper-noun fragments not caught by
    # `_is_personal_name` (which targets given names).
    "սաքայան",     # Sakayan (surname)
    "սարյան",      # Saryan (surname)
    "մաշտոց",      # Mashtots (historical figure)
    "երեվան",      # misspelled Երևան without ՛
    # 2026-06-11 adversarial review: tokenizer / morpheme noise.
    "ակ",          # corpus hits are suffix citations (`-ակ`) and
                   # hyphenation splits across line breaks
                   # (`մի-ակ` = միակ) — never a standalone word;
                   # kaikki glossed it the rare noun "spring,
                   # fountain". Same bucket as the bare suffixes
                   # above (-իկ/-ուկ-style metalinguistic mentions).
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


_HAS_CYRILLIC = re.compile(r"[А-Яа-яЁё]")


def load_russian_glosses() -> dict[str, str]:
    """Lemma → Russian gloss, from cards/frequency/russian_glosses.tsv.

    This is a *translation* layer, NOT a corpus-cited one: the Russian
    is human/LLM prior (translation of the English gloss), so it lives
    in its own file with a clear header rather than mixing into
    HAND_OVERRIDES. build_deck appends ` / <ru>` to a card only when
    its English gloss has no Cyrillic yet, so a hand-override that
    already carries Russian is never double-glossed. Keys are bare /
    underscored lemmas (MWUs use `_`). `#` lines are comments."""
    path = FREQUENCY_CARDS / "russian_glosses.tsv"
    out: dict[str, str] = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            key, ru = parts[0].strip(), parts[1].strip()
            if key and ru:
                out[key] = ru
    return out


# Display-form overrides for cases where the frequency-list lemma
# is NOT the right surface to show on the card. The MWU regex in
# `build_ours.py` doesn't catch inflected verbal phrases where an
# auxiliary interpolates (`դուր է գալիս`, `քուն ա գալիս`), so
# their bare-noun first half ranks top-1000 separately. We display
# the full phrase to the learner; HAND_OVERRIDES still keys on the
# bare-noun lemma for lookup. Add an entry only when the lemma
# alone is *misleading* as a card headword.
DISPLAY_OVERRIDES: dict[str, str] = {
    "դուր":   "դուր գալ",
}


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

    DISPLAY_OVERRIDES (above) rewrites the Armenian surface for
    misleading-bare-lemma cases like `դուր → դուր գալ`.
    """
    key = lemma.lower()
    respell = phonetic.get(key)
    display = DISPLAY_OVERRIDES.get(key, lemma).replace("_", " ")
    if not respell or respell == key:
        return display
    return f"{display} [{respell}]"


# Number lemmas → digit-only glosses (item 8: "number translations
# should be numerical"). Keyed by bare lemma. Cardinals → digit;
# ordinals → digit + ordinal suffix.
NUMBER_DIGITS: dict[str, str] = {
    "մեկ": "1", "երկու": "2", "երեք": "3", "չորս": "4", "հինգ": "5",
    "վեց": "6", "յոթ": "7", "ութ": "8", "ինը": "9", "տասը": "10",
    "տասն": "10", "տասնմեկ": "11", "տասներկու": "12",
    "քսան": "20", "երեսուն": "30", "քառասուն": "40", "հիսուն": "50",
    "վաթսուն": "60", "յոթանասուն": "70", "ութսուն": "80",
    "իննսուն": "90", "հարյուր": "100", "հազար": "1000",
    "միլիոն": "1000000",
    "առաջին": "1st", "երկրորդ": "2nd", "երրորդ": "3rd",
    "չորրորդ": "4th", "հինգերորդ": "5th", "վեցերորդ": "6th",
    "յոթերորդ": "7th", "ութերորդ": "8th", "իններորդ": "9th",
    "տասներորդ": "10th",
}


def _esc(s: str) -> str:
    """Minimal HTML escaping for gloss text."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _fmt_english(en: str) -> str:
    """Bold the English senses, italicise parenthetical examples
    (`(ներս մտնել — to enter)`). Single-quoted attrs only — the CSV
    writer would otherwise quote-escape double quotes and break the
    Anki import."""
    html = ""
    for seg in re.split(r"(\([^)]*\))", en):
        seg = seg.strip()
        if not seg:
            continue
        if seg.startswith("(") and seg.endswith(")"):
            rendered = f"<i>{_esc(seg)}</i>"
        else:
            rendered = f"<b>{_esc(seg)}</b>"
        # Rejoin with a space EXCEPT before punctuation — stripping
        # the segments would otherwise turn `…house); among` into
        # `…house)</i> <b>; among</b>` (a space before the `;`).
        if html and not seg.startswith((";", ",", ".", ":", ")", "!", "?")):
            html += " "
        html += rendered
    return html


def render_lemma(annotated: str) -> str:
    """Render the Armenian front column to Anki HTML: the lemma bold,
    the optional `[phonetic-respell]` small and muted gray on the same
    line (`կարդալ [կարտալ]` → bold `կարդալ`, gray `[կարտալ]`). Mirrors
    `render_gloss`; authoring/keys stay plain, this runs at emit time.
    The validator strips it back via `plain_gloss`."""
    m = re.match(r"^(.*?)\s*(\[[^\]]*\])$", annotated)
    if m:
        base, resp = m.group(1), m.group(2)
        return (f"<b>{_esc(base)}</b> "
                f"<span style='color:#888;font-size:0.8em'>{_esc(resp)}"
                f"</span>")
    return f"<b>{_esc(annotated)}</b>"


def render_gloss(plain: str) -> str:
    """Render a plain `English / Russian` gloss to tasteful Anki HTML:
    English bold, Russian in muted gray on a new line, examples italic.
    Authoring stays plain text (HAND_OVERRIDES, russian_glosses.tsv);
    this is applied once at emit time. Import with 'Allow HTML in
    fields' enabled. The validator strips this back to plain text."""
    parts = plain.rsplit(" / ", 1)
    en = parts[0].strip()
    ru = parts[1].strip() if len(parts) > 1 else ""
    html = _fmt_english(en)
    if ru:
        html += f"<br><span style='color:#888'>{_esc(ru)}</span>"
    return html


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
        # `limit` is the cap on *emitted* cards, not on ranks
        # processed. Break when we've already written that many
        # rows; pre-filter skips and skipped-empty entries don't
        # count against it. Lets a top-1500 input pool drain to
        # exactly --limit successful cards.
        if len(rows_out) >= limit:
            break

        # Filter personal names. Per user policy: keep proper nouns
        # only when they're "first and foremost an Armenian word"
        # (countries, regions, landmarks). Personal given names
        # don't qualify and shouldn't take a slot in the top-1000.
        if _is_personal_name(lemma):
            skipped_names += 1
            continue

        # Filter inflected forms whose lemma is already on deck or
        # whose standalone sense is purely grammatical ("the X").
        # See SKIP_LEMMAS above.
        if lemma in SKIP_LEMMAS:
            stats.setdefault("skipped-inflected", 0)
            stats["skipped-inflected"] += 1
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

    # Force-inject pass: add pedagogically-essential basic
    # vocabulary that the corpus-driven frequency list misses or
    # under-ranks. See `cards/frequency/core_inject.tsv`.
    #
    # Dedup key is the underscore-joined token list, so MWUs like
    # `դուր_գալ` (file form) match the deck's displayed `դուր գալ`
    # (space-separated after `annotated_lemma`).
    def _lemma_key(cell: str) -> str:
        return "_".join(armenian_tokens(cell))

    inject_path = FREQUENCY_CARDS / "core_inject.tsv"
    existing_lemmas = {_lemma_key(r[0]) for r in rows_out}
    injected = 0
    if inject_path.exists():
        with inject_path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 2:
                    continue
                # Use the raw column (preserves underscores for
                # MWUs) as the canonical lemma identity.
                lemma = parts[0].strip()
                if not lemma:
                    continue
                key = _lemma_key(lemma) or lemma
                gloss = parts[1].strip()
                if not gloss:
                    continue
                if key in existing_lemmas:
                    # Already organically in the deck — inject is
                    # only for ones that didn't make the rank-based
                    # cut.
                    continue
                tags = "frequency core-inject src-core-inject"
                rows_out.append([annotated_lemma(lemma, phonetic),
                                 gloss, tags])
                existing_lemmas.add(key)
                injected += 1
        if injected:
            stats.setdefault("core-inject", 0)
            stats["core-inject"] = injected
            print(f"  injected {injected} core-vocab rows from "
                  f"{inject_path.name}", file=sys.stderr, flush=True)

    # Phrasal / light-verb enrichment (items 4,5): inject common
    # multi-word verb constructions mined from the textbook corpora.
    # Same dedup as core-inject; tagged `frequency phrasal-verb` so
    # they're filterable in Anki.
    phrasal_path = FREQUENCY_CARDS / "phrasal_verbs.tsv"
    phrasal_n = 0
    if phrasal_path.exists():
        with phrasal_path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 2:
                    continue
                lemma = parts[0].strip()
                gloss = parts[1].strip()
                if not lemma or not gloss:
                    continue
                key = _lemma_key(lemma) or lemma
                if key in existing_lemmas:
                    continue
                tags = "frequency phrasal-verb src-phrasal"
                rows_out.append([annotated_lemma(lemma, phonetic),
                                 gloss, tags])
                existing_lemmas.add(key)
                phrasal_n += 1
        if phrasal_n:
            stats["phrasal-verb"] = phrasal_n
            print(f"  injected {phrasal_n} phrasal-verb rows from "
                  f"{phrasal_path.name}", file=sys.stderr, flush=True)

    # Russian-augmentation layer: append ` / <ru>` to any card whose
    # English gloss still lacks Cyrillic and whose lemma has an entry
    # in russian_glosses.tsv. Runs last so core-injected cards are
    # covered too. Translation layer (prior) — see load_russian_glosses.
    ru_map = load_russian_glosses()
    if ru_map:
        ru_added = 0
        for r in rows_out:
            key = _lemma_key(r[0]) or r[0]
            # Skip if Russian already present, or if the gloss already
            # contains the reserved ` / ` separator (a malformed EN/EN
            # gloss — appending would make a 3-part gloss; let the
            # validator flag those instead of compounding them).
            if (key in ru_map and not _HAS_CYRILLIC.search(r[1])
                    and " / " not in r[1]):
                r[1] = f"{r[1]} / {ru_map[key]}"
                ru_added += 1
        if ru_added:
            stats["russian-augmented"] = ru_added
            print(f"  augmented {ru_added} cards with Russian glosses "
                  f"from russian_glosses.tsv", file=sys.stderr, flush=True)

    # Number cards → digit-only glosses (item 8).
    num_fixed = 0
    for r in rows_out:
        key = _lemma_key(r[0]) or r[0]
        if key in NUMBER_DIGITS:
            r[1] = NUMBER_DIGITS[key]
            num_fixed += 1
    if num_fixed:
        print(f"  rewrote {num_fixed} number cards as digits",
              file=sys.stderr, flush=True)

    # Write the user-facing deck — clean tags (`frequency top-1000`,
    # rank/src dropped per the 2026-06-03 review) and HTML-rendered
    # glosses — plus a sidecar `out/deck_meta.tsv` carrying rank +
    # source. The validator loads the sidecar so its rank/src-aware
    # checks keep working without cluttering the card.
    meta_path = HERE / "out" / "deck_meta.tsv"
    with out_path.open("w", encoding="utf-8", newline="") as f, \
            meta_path.open("w", encoding="utf-8", newline="") as mf:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        mw = csv.writer(mf, delimiter="\t", lineterminator="\n")
        mw.writerow(["lemma", "rank", "src"])
        for lemma, plain, tags in rows_out:
            rm = re.search(r"rank-(\d+)", tags)
            sm = re.search(r"src-([a-z-]+)", tags)
            rank = rm.group(1) if rm else ""
            src = sm.group(1) if sm else ""
            mw.writerow([lemma, rank, src])
            # Display tag = first two internal tokens: `frequency
            # <category>` (top-1000 / core-inject / phrasal-verb).
            display_tag = " ".join(tags.split()[:2])
            # Sidecar keeps the PLAIN lemma as key; the card gets HTML.
            w.writerow([render_lemma(lemma), render_gloss(plain),
                        display_tag])

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
