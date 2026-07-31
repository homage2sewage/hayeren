"""Repeat-window expansion: glosses.tsv → glosses_expanded.tsv.

Implements `repeat_scope: pages` with a window of 1 source page:
a glossed lemma may re-gloss on every source page. Mechanical —
no judgement, re-runnable after any glosses.tsv edit.

For every authored row of kind `word`, occurrences of the same
heuristic lemma (per candidates.tsv) on OTHER source pages are found
and the first occurrence per page becomes an additional anchor row
(kind `auto`, same gloss/source/conf). Authored anchors register
their own (lemma, page) so pages already covered stay single-gloss.
`hl` / `mwe` / `abbr` rows never expand: colloquial surfaces don't
lemma-match reliably (and a wrong match would be a homograph bug —
e.g. the surface մեր "our" vs the hl row մեր → մայր "mother").

Usage: python3 expand_anchors.py --book ghamoyan --chunk ch2v2
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "frequency"))
import build_ours  # noqa: E402
from query_kb import load_known_lemmas  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--chunk", required=True)
    args = ap.parse_args()
    out_dir = HERE / args.book / args.chunk

    known = load_known_lemmas()
    inflected = build_ours.collect_inflected_to_lemma()

    def heur(surface: str) -> str:
        return build_ours.lemmatize(surface.split()[0].lower(), known,
                                    inflected)

    with (out_dir / "blocks.tsv").open(encoding="utf-8") as f:
        block_page = {r["block_id"]: int(r["pages"].split("-")[0])
                      for r in csv.DictReader(f, delimiter="\t")}
    with (out_dir / "candidates.tsv").open(encoding="utf-8") as f:
        cands = list(csv.DictReader(f, delimiter="\t"))
    with (out_dir / "glosses.tsv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fields = reader.fieldnames
        rows = list(reader)

    covered: set[tuple[str, int]] = set()
    for r in rows:
        covered.add((heur(r["surface"]), block_page[r["block_id"]]))

    added = []
    for r in rows:
        if r["kind"] != "word":
            continue
        lemma_h = heur(r["surface"])
        for c in cands:
            if c["lemma"] != lemma_h:
                continue
            page = block_page[c["block_id"]]
            if (lemma_h, page) in covered:
                continue
            covered.add((lemma_h, page))
            added.append({**r, "block_id": c["block_id"],
                          "surface": c["surface"], "kind": "auto"})

    ordered = sorted(rows + added,
                     key=lambda r: (r["block_id"], r["kind"] == "auto"))
    with (out_dir / "glosses_expanded.tsv").open(
            "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(ordered)
    print(f"{len(rows)} authored + {len(added)} page-repeat anchors "
          f"-> glosses_expanded.tsv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
