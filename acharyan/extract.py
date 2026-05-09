#!/usr/bin/env python3
"""Convert Acharyan etymological-dictionary OCR text into per-lemma
JSONL entries, with page tracking.

Input:  vol1.txt - vol4.txt (DJVU OCR text from archive.org)
Output: out/vol{N}.jsonl + out/full.jsonl

Entry shape:
  {volume, page, headword, headword_marker, body, line_start, line_end}

The OCR text format:
- Page numbers appear as bare-digit lines.
- Dictionary entries are introduced by an all-caps Armenian
  headword on its own line (or as the first word of a line),
  optionally prefixed with `*` (reconstructed) or `+` / `՛`
  (cross-reference / variant).
- Entry body continues until the next headword.

Heuristics — flagged here as such (per workspace `llm-workflow.md`).
Audit by spot-checking 20 random entries against the source PDF
before relying on extraction for citation.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"

# Page numbers in OCR are bare-digit lines (after stripping
# whitespace and stray punctuation). Range 1-2000 covers all volumes.
_PAGE_NUM = re.compile(r"^\s*([0-9]{1,4})\s*$")

# Headword: all-caps Armenian word at line start, optionally
# preceded by a marker. The OCR sometimes includes punctuation /
# OCR noise around the headword. Match on the first all-caps run
# of length >= 3; longer than 3 reduces noise from e.g. "Ա, Բ" list
# items in cross-reference sections.
_HEADWORD = re.compile(
    r"^([*+՛]?)\s*([Ա-Ֆ]{3,}(?:\s+[Ա-Ֆ]{3,})?)\s*[,.]?\s*"
)


def _is_armenian_caps(s: str) -> bool:
    return bool(s) and all("Ա" <= c <= "Ֆ" or c.isspace() for c in s)


def extract_volume(path: Path, volume: int) -> list[dict]:
    """Walk the OCR text linearly, collecting entries by headword
    boundary. Tracks the most-recently-seen page number."""
    entries: list[dict] = []
    current: dict | None = None
    page = 0
    line_no = 0

    with path.open(encoding="utf-8") as f:
        for raw in f:
            line_no += 1
            line = raw.rstrip("\n")
            stripped = line.strip()

            # Page-number line — update tracker, don't include in body.
            m_page = _PAGE_NUM.match(stripped)
            if m_page:
                num = int(m_page.group(1))
                # Sanity: page numbers monotonically increase by 1
                # (mostly). Reject obvious non-page-number digits
                # (e.g. years, page-line refs) by requiring 1 <= n <= 2000
                # AND no more than a 50-page jump from current.
                if 1 <= num <= 2000 and abs(num - page) <= 50:
                    page = num
                    continue

            # Headword candidate?
            m_hw = _HEADWORD.match(stripped)
            if m_hw and len(stripped) <= 80:  # cap to avoid run-on lines
                marker, hw = m_hw.group(1), m_hw.group(2).strip()
                # Heuristic: the headword is followed by a space and a
                # comma/abbreviation (e.g. "ԱԴԱՄԱՆԴ, ի" or "ԱՅՐ, ի դլ.").
                # If the line has further content beyond the headword,
                # treat it as an entry start.
                if current is not None:
                    current["line_end"] = line_no - 1
                    current["body"] = current["body"].strip()
                    if current["body"]:
                        entries.append(current)
                current = {
                    "volume": volume,
                    "page": page,
                    "headword": hw,
                    "headword_marker": marker,
                    "body": stripped[m_hw.end():].rstrip() + "\n",
                    "line_start": line_no,
                    "line_end": line_no,
                }
                continue

            # Body continuation
            if current is not None:
                current["body"] += line + "\n"

    if current is not None:
        current["line_end"] = line_no
        current["body"] = current["body"].strip()
        if current["body"]:
            entries.append(current)

    return entries


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    all_entries: list[dict] = []
    for vol in (1, 2, 3, 4):
        path = HERE / f"vol{vol}.txt"
        if not path.exists():
            print(f"missing: {path}", file=sys.stderr)
            continue
        entries = extract_volume(path, vol)
        out_path = OUT / f"vol{vol}.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"vol{vol}: {len(entries)} entries → {out_path}",
              file=sys.stderr)
        all_entries.extend(entries)

    full = OUT / "full.jsonl"
    with full.open("w", encoding="utf-8") as f:
        for e in all_entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"total: {len(all_entries)} entries → {full}", file=sys.stderr)

    # Quick stats
    by_vol: dict[int, int] = {}
    by_marker: dict[str, int] = {}
    for e in all_entries:
        by_vol[e["volume"]] = by_vol.get(e["volume"], 0) + 1
        m = e["headword_marker"] or "(plain)"
        by_marker[m] = by_marker.get(m, 0) + 1
    print(f"by volume: {by_vol}", file=sys.stderr)
    print(f"by marker: {by_marker}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
