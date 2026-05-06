#!/usr/bin/env python3
"""Scan the extracted JSONL for Sakayan's section markers and build a
manifest of every unit's dialogue / vocab / grammar boundaries.

Section markers are Times-Bold spans at x≈43 with stable Roman-numeral
prefixes:

    I  DIALOGUES         start of a unit (each occurrence = new unit)
    II  TEXT             prose passage
    III NEW WORDS …      vocab table
    IV …                 thematic vocab (varies)
    V  GRAMMAR
    VI - XI              ARMENIAN-ENGLISH CONTRASTS, WORD FORMATION,
                         PRONUNCIATION, ORTHOGRAPHY, WRITING, EXERCISES
    1. 2. 3. …           individual dialogues inside DIALOGUES, exercises
                         inside EXERCISES, etc.

The output `units.json` lists for each unit:

    unit_n        — sequential unit number (1-based)
    page_start    — first page of the unit (where I DIALOGUES sits)
    page_end      — last page (the page before the next unit's I DIALOGUES)
    dialogues[]   — list of (start: page:y, end: page:y) for each numbered dialogue
    vocab_pages[] — pages containing III NEW WORDS table

This is the source of truth for `make_anki.py`.
"""

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
JSONL = HERE / "out" / "full.jsonl"
OUT = HERE / "units.json"


# Roman numerals 1-11 used for unit-section markers.
SECTION_RE = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X|XI)\b")
DIALOGUE_NUM_RE = re.compile(r"^(\d+)\.\s*$")


def load_markers() -> list[dict]:
    """Find all left-margin Times-Bold spans — these are the structural
    headers."""
    markers: list[dict] = []
    for line in JSONL.open():
        s = json.loads(line)
        if "Times-Bold" not in s["font"]:
            continue
        if not (40 <= s["bbox"][0] <= 50):
            continue
        t = s["text"].strip()
        if not t:
            continue
        markers.append({
            "page": s["page"],
            "y": s["bbox"][1],
            "text": t,
        })
    return markers


def classify(m: dict) -> tuple[str, str | int | None]:
    """Tag a marker with (section_type, value).

    section_type ∈ {dialogues, text, words, grammar, other_section,
                    dialogue_number, exercise_number, sub_grammar}
    """
    t = m["text"].strip()
    sec = SECTION_RE.match(t)
    if sec:
        roman = sec.group(1)
        rest = t[len(roman):].strip().upper()
        if "DIALOGUE" in rest:
            return ("dialogues", roman)
        if "TEXT" in rest:
            return ("text", roman)
        if "WORDS" in rest or "VOCABULAR" in rest:
            return ("words", roman)
        if "GRAMMAR" in rest:
            return ("grammar", roman)
        # Other unit sections (CONTRAST / WORD FORMATION / PRONUNCIATION /
        # ORTHOGRAPHY / WRITING / EXERCISES / THEMATIC) — recognize so we
        # don't misclassify lone-letter Romans in the glossary as sections.
        if any(k in rest for k in
               ("CONTRAST", "FORMATION", "PRONUN", "ORTHOGRAPHY",
                "WRITING", "EXERCIS", "THEMATIC", "READING")):
            return ("section", roman)
        return ("other_section", roman)
    num = DIALOGUE_NUM_RE.match(t)
    if num:
        return ("number", int(num.group(1)))
    if re.match(r"^\d+\.\s+\S", t):
        # Numbered exercise / grammar sub-point with text immediately after
        return ("number_with_text", t)
    return ("other", t)


def main() -> None:
    raw = load_markers()
    classified = [(m, classify(m)) for m in raw]

    # Each "I DIALOGUES" marker starts a unit.
    unit_anchors = [
        (i, m) for i, (m, c) in enumerate(classified)
        if c[0] == "dialogues" and c[1] == "I"
    ]

    units = []
    for n, (start_idx, anchor) in enumerate(unit_anchors, 1):
        # End at the next anchor's start, or end of book.
        end_idx = unit_anchors[n][0] if n < len(unit_anchors) else len(classified)
        unit_markers = classified[start_idx:end_idx]

        # Locate per-section anchors.
        sections: dict[str, list[dict]] = {}
        for m, c in unit_markers:
            if c[0] in ("dialogues", "text", "words", "grammar", "other_section"):
                sections.setdefault(c[0], []).append({
                    "page": m["page"], "y": m["y"], "roman": c[1]
                })

        # Build dialogue ranges: each top-level "n." marker inside the
        # DIALOGUES section starts a dialogue; ends at the next "n." or
        # at the start of "II  TEXT".
        dlg_section_start = sections.get("dialogues", [{}])[0]
        text_section = sections.get("text", [{}])[0] if "text" in sections else {}

        dlg_numbers = []
        in_dialogues = False
        for m, c in unit_markers:
            if (m["page"], m["y"]) == (dlg_section_start.get("page"),
                                       dlg_section_start.get("y")):
                in_dialogues = True
                continue
            if c[0] == "text":
                in_dialogues = False
            if not in_dialogues:
                continue
            # Accept both "1." (alone) and "1. A has invited B..." (number + descriptor).
            if c[0] == "number":
                dlg_numbers.append({"page": m["page"], "y": m["y"], "n": c[1]})
            elif c[0] == "number_with_text":
                m_num = re.match(r"^(\d+)\.", c[1])
                if m_num:
                    dlg_numbers.append({"page": m["page"], "y": m["y"], "n": int(m_num.group(1))})

        dialogues = []
        # If there are no numbered markers, treat the whole DIALOGUES → TEXT
        # span as a single un-numbered dialogue. Some units have only one
        # dialogue and Sakayan skips the "1." marker.
        if not dlg_numbers and text_section:
            dialogues.append({
                "n": 1,
                "start": {"page": dlg_section_start["page"],
                          "y": dlg_section_start["y"] + 1},
                "end": {"page": text_section["page"], "y": text_section["y"]},
            })
        for i, dlg in enumerate(dlg_numbers):
            if i + 1 < len(dlg_numbers):
                end_page, end_y = dlg_numbers[i + 1]["page"], dlg_numbers[i + 1]["y"]
            elif text_section:
                end_page, end_y = text_section["page"], text_section["y"]
            else:
                end_page, end_y = anchor["page"] + 50, 0
            dialogues.append({
                "n": dlg["n"],
                "start": {"page": dlg["page"], "y": dlg["y"] + 1},
                "end": {"page": end_page, "y": end_y},
            })

        # Vocab pages: walk from "III NEW WORDS" until the next section marker.
        vocab_pages: list[int] = []
        if "words" in sections:
            wstart = sections["words"][0]
            # Pick the next section marker (any kind) after the words anchor.
            next_marker_page = anchor["page"] + 50
            for m, c in unit_markers:
                if c[0] in ("dialogues", "text", "words", "grammar", "other_section"):
                    if (m["page"], m["y"]) > (wstart["page"], wstart["y"]):
                        next_marker_page = m["page"]
                        break
            vocab_pages = list(range(wstart["page"], next_marker_page))

        # page_end: page just before next unit, OR for the last unit, the
        # last *unit-content* marker page. Appendix material (verb tables,
        # alphabetical glossary) has Times-Bold left-margin headers too,
        # so we exclude classify="other" pages to keep the cap tight.
        if n < len(unit_anchors):
            page_end = unit_anchors[n][1]["page"] - 1
        else:
            unit_content_pages = [
                m["page"] for m, c in unit_markers
                if c[0] in ("dialogues", "text", "words", "grammar",
                            "section", "number", "number_with_text")
            ]
            page_end = max(unit_content_pages) + 2 if unit_content_pages else anchor["page"]

        units.append({
            "unit_n": n,
            "page_start": anchor["page"],
            "page_end": page_end,
            "dialogues": dialogues,
            "vocab_pages": vocab_pages,
        })

    OUT.write_text(json.dumps(units, ensure_ascii=False, indent=2))
    print(f"Wrote {len(units)} units → {OUT}")
    for u in units:
        dlg_summary = ", ".join(
            f"{d['n']}@p{d['start']['page']}–{d['end']['page']}"
            for d in u["dialogues"]
        )
        print(f"  Unit {u['unit_n']:2d}  pages {u['page_start']:3d}–{u['page_end']:3d}  "
              f"vocab=p{u['vocab_pages']!r}  dialogues=[{dlg_summary}]")


if __name__ == "__main__":
    main()
