#!/usr/bin/env python3
"""Validate the generated lemmas against Wiktionary.

For each lemma in our top-N list, query Wiktionary (via
sakayan/glosser.gloss_token). Each lemma gets a status flag:

    valid          — Wiktionary has an Armenian entry
    multi-meaning  — entry exists, multiple POS / definitions
    suspicious     — heuristic: very short stem, awkward ending,
                     or pattern that suggests lemmatizer over-stripping
    not-found      — no Wiktionary Armenian entry; needs manual review

Output:

    out/lemma_validation.tsv  rank | lemma | count | status | gloss/notes
    out/lemma_validation.md   summary report

By default validates the top-200 (the high-value head; long-tail
quality degrades by design). Override with --top N.

Wiktionary calls are cached at ../sakayan/.cache/lookup/ so repeat
runs are instant. First run on the top-200 takes a few minutes for
new entries.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAKAYAN = HERE.parent / "sakayan"
sys.path.insert(0, str(SAKAYAN))

import glosser  # noqa: E402  (path-modified import)


OUT = HERE / "out"


def looks_suspicious(lemma: str) -> str:
    """Heuristic flag for likely lemmatizer over-stripping.

    Returns a short reason string if suspicious, else empty string."""
    if len(lemma) <= 2:
        return "very short (≤2 chars)"
    if lemma.endswith(("ե", "ա")) and len(lemma) <= 4:
        # Things like 'այդպե', 'քանզ' are usually truncated.
        return f"ends in bare vowel '{lemma[-1]}', likely truncated"
    return ""


def validate_top_n(n: int) -> list[dict]:
    rows = list(csv.reader(open(OUT / "our_top_1000.tsv"), delimiter="\t"))
    results: list[dict] = []
    for row in rows[:n]:
        if len(row) < 4:
            continue
        rank = int(row[0])
        lemma = row[1]
        count = int(row[2])
        sources = row[3]

        # Lemma sanity flag (no Wiktionary call yet).
        suspicion = looks_suspicious(lemma)

        # Wiktionary lookup.
        gloss = glosser.gloss_token(lemma)
        status = gloss["status"]
        if status == "found" and not suspicion:
            final_status = "valid"
        elif status == "found" and suspicion:
            final_status = "suspicious-but-found"
        elif status == "multi-meaning":
            final_status = "multi-meaning"
        elif status == "not-found" and suspicion:
            final_status = "suspicious"
        else:
            final_status = "not-found"

        notes = "; ".join(gloss["definitions"][:2]) if gloss["definitions"] else ""
        if suspicion:
            notes = f"[{suspicion}] {notes}".strip()

        results.append({
            "rank": rank,
            "lemma": lemma,
            "count": count,
            "sources": sources,
            "status": final_status,
            "notes": notes,
        })
        print(f"  {rank:4d}  {lemma:25s}  {final_status}",
              file=sys.stderr)
    return results


def write_outputs(results: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    tsv_path = OUT / "lemma_validation.tsv"
    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["rank", "lemma", "count", "status", "notes"])
        for r in results:
            w.writerow([r["rank"], r["lemma"], r["count"], r["status"], r["notes"]])

    md_path = OUT / "lemma_validation.md"
    by_status: dict[str, list[dict]] = {}
    for r in results:
        by_status.setdefault(r["status"], []).append(r)

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Lemma validation\n\n")
        f.write(f"Validated top-{len(results)} lemmas of `our_top_1000.tsv` ")
        f.write("via `sakayan/glosser.py` (Wiktionary lookup) + a small ")
        f.write("'looks-suspicious' heuristic for short truncated stems.\n\n")

        f.write("## Summary\n\n")
        for status in ("valid", "multi-meaning", "suspicious-but-found",
                       "not-found", "suspicious"):
            n = len(by_status.get(status, []))
            pct = 100 * n / len(results) if results else 0
            f.write(f"- **{status}**: {n} ({pct:.0f}%)\n")
        f.write("\n")

        for status in ("not-found", "suspicious", "suspicious-but-found",
                       "multi-meaning", "valid"):
            entries = by_status.get(status, [])
            if not entries:
                continue
            f.write(f"\n## {status}  ({len(entries)})\n\n")
            f.write("| rank | lemma | count | notes |\n")
            f.write("|-----:|-------|------:|-------|\n")
            limit = 60 if status == "valid" else 200
            for r in entries[:limit]:
                # Trim notes for table readability.
                notes = (r["notes"] or "—").replace("|", "\\|")[:120]
                f.write(f"| {r['rank']} | {r['lemma']} | {r['count']} | {notes} |\n")
            if len(entries) > limit:
                f.write(f"\n_… {len(entries) - limit} more (see "
                        f"`{tsv_path.name}` for the full list)_\n")

    print(f"\nWrote {tsv_path.name} and {md_path.name}", file=sys.stderr)
    print(f"Status breakdown:", file=sys.stderr)
    for status, entries in by_status.items():
        print(f"  {status:25s}  {len(entries)}", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=200,
                    help="how many top lemmas to validate (default 200)")
    args = ap.parse_args()
    results = validate_top_n(args.top)
    write_outputs(results)


if __name__ == "__main__":
    main()
