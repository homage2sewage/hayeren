"""Step C prep: mechanical dictionary lookups for the selected words.

For every selection.tsv row, gathers gloss candidates from:
  kaikki      frequency/data/armenian.jsonl (EN, wiktextract)
  terms       grammar-terms.md trilingual tables (EN|HY|RU)
  ru-layer    cards/frequency/russian_glosses.tsv
The LLM authoring pass turns this into glosses.tsv, correcting the
heuristic lemma and choosing ru (primary) / en (fallback); rows with
no source hit anywhere must be marked source=prior (FRD gap policy).

Usage: python3 gloss_prep.py --book ghamoyan --chunk ch2
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "frequency"))
from common import ROOT  # noqa: E402
import build_ours  # noqa: E402
from query_kb import load_known_lemmas  # noqa: E402


def load_kaikki() -> dict[str, list[str]]:
    idx: dict[str, list[str]] = {}
    with (ROOT / "frequency" / "data" / "armenian.jsonl").open(
            encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            word = r.get("word", "")
            glosses = []
            for s in r.get("senses", [])[:3]:
                for g in (s.get("glosses") or [])[:1]:
                    glosses.append(g)
            if word and glosses:
                idx.setdefault(word.lower(), []).extend(
                    f"{r.get('pos','?')}: {g}" for g in glosses)
    return idx


def load_terms() -> dict[str, tuple[str, str]]:
    """Armenian term -> (en, ru) from grammar-terms.md tables."""
    idx: dict[str, tuple[str, str]] = {}
    row_re = re.compile(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|")
    for line in (ROOT / "grammar-terms.md").read_text(
            encoding="utf-8").splitlines():
        m = row_re.match(line)
        if not m:
            continue
        en, hy, ru = (c.strip() for c in m.groups())
        if en.lower() in ("english", "---------", ""):
            continue
        for term in re.split(r"[/,]", hy):
            term = re.sub(r"\(.*?\)", "", term).strip()
            if term and re.search(r"[԰-֏]", term):
                idx.setdefault(term.lower(), (en, ru))
    return idx


def load_ru_layer() -> dict[str, str]:
    idx: dict[str, str] = {}
    path = ROOT / "cards" / "frequency" / "russian_glosses.tsv"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or "\t" not in line:
            continue
        lemma, ru = line.split("\t", 1)
        idx[lemma.strip().lower()] = ru.strip()
    return idx


def variants(lemma: str, surface: str) -> list[str]:
    out = [lemma, surface.lower()]
    if lemma.endswith("ել"):
        out.append(lemma[:-2] + "ալ")
    if lemma.endswith("ալ"):
        out.append(lemma[:-2] + "ել")
    # verbal nouns the lemmatizer may leave inflected: -ման -> -ում
    if surface.lower().endswith("ման"):
        out.append(surface.lower()[:-3] + "ում")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--chunk", required=True)
    args = ap.parse_args()
    out_dir = HERE / args.book / args.chunk

    kaikki = load_kaikki()
    terms = load_terms()
    ru_layer = load_ru_layer()
    known = load_known_lemmas()
    inflected = build_ours.collect_inflected_to_lemma()

    with (out_dir / "selection.tsv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    out_rows = []
    hit_k = hit_t = hit_r = miss = 0
    for r in rows:
        head = r["surface"].split()[0].lower()
        lemma = build_ours.lemmatize(head, known, inflected)
        cand = variants(lemma, r["surface"])
        k = next((kaikki[v] for v in cand if v in kaikki), [])
        t = next((terms[v] for v in cand if v in terms), ("", ""))
        ru = next((ru_layer[v] for v in cand if v in ru_layer), "")
        hit_k += bool(k)
        hit_t += bool(t[0])
        hit_r += bool(ru)
        if not (k or t[0] or ru):
            miss += 1
        out_rows.append((r["block_id"], r["surface"], r["kind"], lemma,
                         " | ".join(k[:3]), t[0], t[1], ru))

    with (out_dir / "gloss_prep.tsv").open("w", encoding="utf-8",
                                           newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["block_id", "surface", "kind", "lemma_heur",
                    "kaikki_en", "terms_en", "terms_ru", "ru_layer"])
        w.writerows(out_rows)
    print(f"{len(out_rows)} rows: kaikki {hit_k}, terms {hit_t}, "
          f"ru-layer {hit_r}, no-source {miss} "
          f"-> {out_dir/'gloss_prep.tsv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
