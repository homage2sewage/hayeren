#!/usr/bin/env python3
"""Validator + regression guard for the saqapetoyan structured parse.

Two layers, per the repo's two-step rule (fix the case + capture a guard):

1. GOLDEN anchors (`golden_entries.tsv`) — one hand-verified entry per
   failure class found during the challenge protocol (hyphenated headword,
   homograph, grave separator, colon-coinage rescue, definition-inferred,
   multi-sense, interleaved, genuine no-pos/no-english, …). A regression
   that reintroduces any class fails here.

2. STRUCTURAL invariants over the whole `out/entries.jsonl` — the audits
   that caught the silent merges and field leaks:
     - no Cyrillic/Latin leaked into native_coinages or definition
     - no Armenian leaked into ru
     - no headword carries an embedded ' – POS' (entry-boundary merge)
     - entry count within an expected band

Run after every `parse_entries.py` change:
    ../ghamoyan/.venv/bin/python validate_entries.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRIES = HERE / "out" / "entries.jsonl"
GOLDEN = HERE / "golden_entries.tsv"

CYR = re.compile(r"[Ѐ-ӿ]")
LAT = re.compile(r"[A-Za-z]")
ARM = re.compile(r"[Ա-֊ա-ֆև]")
MERGE = re.compile(r"[–-]\s*(?:գ|ած|մ|բ|կ)\.")  # embedded 'word – POS'
EXPECT_MIN, EXPECT_MAX = 600, 630


def load_entries() -> dict:
    idx = {}
    for ln in ENTRIES.open(encoding="utf-8"):
        r = json.loads(ln)
        idx[(r["headword"], r["homograph"])] = r
    return idx


def check_golden(idx: dict) -> list[str]:
    fails = []
    for row in csv.DictReader(GOLDEN.open(encoding="utf-8"), delimiter="\t"):
        hw = row["headword"]
        hg = int(row["homograph"]) if row["homograph"] else None
        r = idx.get((hw, hg))
        tag = f"{row['class_note']}::{hw}"
        if r is None:
            fails.append(f"GOLDEN {tag}: entry not found (merge/boundary regression?)")
            continue
        got = {
            "pos": r["pos"] or "",
            "domain": "|".join(r["domain"]),
            "definition": r["definition"] or "",
            "coinages": "|".join(r["native_coinages"]),
            "ru": r["ru"] or "",
            "en": r["en"] or "",
            "multi_sense": "1" if r.get("multi_sense") else "",
        }
        for field, want in (
            ("pos", row["pos"]), ("domain", row["domain"]),
            ("definition", row["definition"]), ("coinages", row["coinages"]),
            ("ru", row["ru"]), ("en", row["en"]),
            ("multi_sense", row["multi_sense"]),
        ):
            if got[field] != want:
                fails.append(f"GOLDEN {tag}: {field}\n    want={want!r}\n    got ={got[field]!r}")
    return fails


def check_structural(idx: dict) -> list[str]:
    fails = []
    rows = list(idx.values())
    n = len(rows)
    if not (EXPECT_MIN <= n <= EXPECT_MAX):
        fails.append(f"STRUCT entry-count {n} outside [{EXPECT_MIN},{EXPECT_MAX}]")
    for r in rows:
        tag = f"p{r['page']} {r['headword']!r}"
        for c in r["native_coinages"]:
            if CYR.search(c) or LAT.search(c):
                fails.append(f"STRUCT coinage-leak {tag}: {c!r}")
        if r["definition"] and (CYR.search(r["definition"]) or LAT.search(r["definition"])):
            fails.append(f"STRUCT def-leak {tag}: {r['definition'][:40]!r}")
        if r["ru"] and ARM.search(r["ru"]):
            fails.append(f"STRUCT ru-armenian-leak {tag}: {r['ru']!r}")
        if r["headword"] and MERGE.search(r["headword"]):
            fails.append(f"STRUCT merged-headword {tag}")
    return fails


def main() -> int:
    idx = load_entries()
    fails = check_golden(idx) + check_structural(idx)
    if fails:
        print(f"FAIL ({len(fails)} issue(s)):", file=sys.stderr)
        for f in fails:
            print("  " + f, file=sys.stderr)
        return 1
    print(f"OK — {len(idx)} entries, golden anchors + structural invariants pass",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
