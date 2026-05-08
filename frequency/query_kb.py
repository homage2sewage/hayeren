#!/usr/bin/env python3
"""Phase 1 KB-grounding tool for Armenian-language Q&A.

Given an Armenian text (a question, a tweet, an excerpt), surface
the workspace material that should ground an answer:

  - matched topic files under `topics/`
  - matched book passages under `<book>/out/full.jsonl`
  - matched project notes (armenian-grammar.md, transliteration-
    notes.md, grammar-terms.md)
  - lemmas with no coverage anywhere (gaps)

Output is Markdown to stdout, suitable as an LLM-context bundle
for a follow-on "answer this with citations" turn. No model calls
here — this is the deterministic retrieval step. The LLM consumes
the bundle separately.

Usage:

    python3 frequency/query_kb.py "<armenian text>"
    echo "<armenian text>" | python3 frequency/query_kb.py
    python3 frequency/query_kb.py --file path/to/text.md

Why this exists: the 2026-05-09 Pashinyan-tweet-comparison
(`research/2026-05-09-tweet-llm-comparison.md`) showed that even
when the answer was sitting in a citation-checked topic file,
neither external LLMs nor a workspace-aware Claude session looked.
This script makes "look at the KB first" mechanical instead of
habitual. See `llm-workflow.md` § "Before answering an Armenian-
language question" + `CLAUDE.md` § same.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# Reuse the existing tokeniser + lemmatiser. Same path machinery
# as `build_deck.py` so this file stays drop-in.
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import build_ours  # noqa: E402

TOPICS = ROOT / "topics"
PROJECT_NOTES = [
    ROOT / "armenian-grammar.md",
    ROOT / "transliteration-notes.md",
    ROOT / "grammar-terms.md",
]
BOOKS = ["sakayan", "ghamoyan", "parnasyan", "tioyan"]


# ---------- query lemmatisation ----------


# Function words / clitics / common particles that match almost
# everything if we let them through. Excluding them from KB-grep
# keeps signal high. This list is a *baseline* — the challenge
# protocol applies if we want to grow it (cf. `CLAUDE.md`
# § "Heuristic validation"). The cost of a false-positive
# (extra context loaded) is much smaller than a false-negative
# (the right topic missed), so err small.
QUERY_STOPWORDS: set[str] = {
    "եմ", "ես", "է", "ենք", "եք", "են",
    "էի", "էիր", "էր", "էինք", "էիք", "էին",
    "ա",
    "որ", "ու", "և", "բայց", "կամ", "իսկ", "նաև",
    "ոչ", "չէ", "այո", "հա",
    "մի", "էլ", "հատ",
    "ի", "ին", "ից", "ով", "ում", "ից",
    "ինչ", "ով", "ինչու", "որտեղ", "երբ", "ինչպես",
    "այս", "այդ", "այն", "սա", "դա", "նա",
    "այսպես", "այդպես", "այնպես", "այստեղ", "այնտեղ",
    "շատ", "քիչ", "բոլոր", "ամեն", "որոշ",
    "միայն", "հենց", "բա", "դե", "ուրեմն", "ինքն",
}


def query_lemmas(text: str) -> list[tuple[str, str]]:
    """Return [(token, lemma)] for content-word Armenian tokens.

    Filters QUERY_STOPWORDS at *both* the token and lemma level so
    inflected stopwords don't sneak through. Preserves order; dedup
    by lemma to avoid grepping the same KB twice."""
    tokens = build_ours.tokenize(text)
    inflected = build_ours.collect_inflected_to_lemma()
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for t in tokens:
        t_low = t.lower()
        if t_low in QUERY_STOPWORDS:
            continue
        lemma = build_ours.lemmatize(t_low, None, inflected)
        if lemma in QUERY_STOPWORDS:
            continue
        if lemma in seen:
            continue
        seen.add(lemma)
        out.append((t, lemma))
    return out


# ---------- topic-file grep ----------


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def grep_topics(lemmas: list[str]) -> list[tuple[Path, list[str], int]]:
    """For each topic file, count how many query lemmas it contains
    (substring-match, lowercased on both sides). Returns
    [(path, matched_lemmas, count)] sorted descending by count.
    Zero-match topics are excluded."""
    if not lemmas:
        return []
    hits: list[tuple[Path, list[str], int]] = []
    for path in sorted(TOPICS.rglob("*.md")):
        body = _read_text(path).lower()
        if not body:
            continue
        matched = [le for le in lemmas if le.lower() in body]
        if matched:
            hits.append((path, matched, len(matched)))
    hits.sort(key=lambda x: (-x[2], str(x[0])))
    return hits


def grep_project_notes(lemmas: list[str]) -> list[tuple[Path, list[str], int]]:
    """Same shape as grep_topics, against the project-root note
    files (armenian-grammar.md, transliteration-notes.md, etc.)."""
    if not lemmas:
        return []
    hits: list[tuple[Path, list[str], int]] = []
    for path in PROJECT_NOTES:
        if not path.exists():
            continue
        body = _read_text(path).lower()
        matched = [le for le in lemmas if le.lower() in body]
        if matched:
            hits.append((path, matched, len(matched)))
    hits.sort(key=lambda x: -x[2])
    return hits


# ---------- book JSONL grep ----------


def grep_books(lemmas: list[str]) -> dict[str, list[dict]]:
    """For each book, return the JSONL records containing any query
    lemma. Grouped by book; preserves on-disk order so callers can
    reconstruct page context.

    Each record: {page, bbox, text, matched_lemmas}.
    """
    out: dict[str, list[dict]] = {}
    if not lemmas:
        return out
    lemmas_low = [le.lower() for le in lemmas]
    for book in BOOKS:
        jsonl = ROOT / book / "out" / "full.jsonl"
        if not jsonl.exists():
            jsonl = ROOT / "books" / book / "out" / "full.jsonl"
        if not jsonl.exists():
            continue
        records: list[dict] = []
        with jsonl.open(encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                text = (e.get("text") or "").lower()
                if not text:
                    continue
                matched = [le for le in lemmas_low if le in text]
                if matched:
                    records.append({
                        "page": e.get("page"),
                        "bbox": e.get("bbox"),
                        "text": e.get("text", "").strip(),
                        "matched": matched,
                    })
        if records:
            out[book] = records
    return out


# ---------- output ----------


def _topic_excerpt(path: Path, matched_lemmas: list[str],
                   context_lines: int = 4) -> str:
    """Return excerpts of the topic file showing each matched lemma
    in context (a few lines around each hit). Cheaper than dumping
    the whole file when many topics match; preserves citation
    pointers because the topic frontmatter `[#N]` markers and the
    body's discussion of the lemma usually appear within a few
    lines of each other."""
    lines = _read_text(path).splitlines()
    if not lines:
        return ""
    keep: set[int] = set()
    for i, line in enumerate(lines):
        ll = line.lower()
        if any(le.lower() in ll for le in matched_lemmas):
            for j in range(max(0, i - context_lines),
                           min(len(lines), i + context_lines + 1)):
                keep.add(j)
    if not keep:
        return ""
    out: list[str] = []
    prev = -2
    for i in sorted(keep):
        if i > prev + 1 and out:
            out.append("…")
        out.append(f"{i+1:4d}  {lines[i]}")
        prev = i
    return "\n".join(out)


def _book_page_groups(records: list[dict]) -> list[tuple[int, list[dict]]]:
    """Group consecutive records by page; preserves order."""
    grouped: dict[int, list[dict]] = defaultdict(list)
    for r in records:
        grouped[r["page"]].append(r)
    return sorted(grouped.items())


def render_bundle(
    text: str,
    pairs: list[tuple[str, str]],
    topic_hits: list[tuple[Path, list[str], int]],
    note_hits: list[tuple[Path, list[str], int]],
    book_hits: dict[str, list[dict]],
    *,
    full_topics: bool,
) -> str:
    out: list[str] = []
    out.append("# KB-grounding bundle\n")
    out.append("## Query\n")
    out.append("```")
    out.append(text.strip())
    out.append("```\n")

    out.append("## Lemmas extracted\n")
    if pairs:
        out.append("| token | lemma |")
        out.append("|---|---|")
        for tok, lem in pairs:
            out.append(f"| `{tok}` | `{lem}` |")
    else:
        out.append("*(no Armenian content-word tokens after stopword filter)*")
    out.append("")

    queried = [le for _, le in pairs]
    found_anywhere: set[str] = set()
    for _, ms, _ in topic_hits:
        found_anywhere.update(ms)
    for _, ms, _ in note_hits:
        found_anywhere.update(ms)
    for _book, recs in book_hits.items():
        for r in recs:
            for m in r["matched"]:
                found_anywhere.add(m)
    gaps = [le for le in queried if le.lower() not in
            {x.lower() for x in found_anywhere}]

    out.append("## Matched topic files\n")
    if topic_hits:
        for path, matched, count in topic_hits:
            rel = path.relative_to(ROOT)
            ms = ", ".join(f"`{m}`" for m in matched)
            out.append(f"### `{rel}` — {count} match(es): {ms}\n")
            if full_topics:
                body = _read_text(path)
                out.append("```markdown")
                out.append(body.rstrip())
                out.append("```\n")
            else:
                excerpt = _topic_excerpt(path, matched)
                if excerpt:
                    out.append("```")
                    out.append(excerpt)
                    out.append("```\n")
    else:
        out.append("*(no topic files matched)*\n")

    out.append("## Matched project notes\n")
    if note_hits:
        for path, matched, count in note_hits:
            rel = path.relative_to(ROOT)
            ms = ", ".join(f"`{m}`" for m in matched)
            out.append(f"### `{rel}` — {count} match(es): {ms}\n")
            excerpt = _topic_excerpt(path, matched)
            if excerpt:
                out.append("```")
                out.append(excerpt)
                out.append("```\n")
    else:
        out.append("*(no project notes matched)*\n")

    out.append("## Matched book passages\n")
    if book_hits:
        for book, records in book_hits.items():
            out.append(f"### {book}\n")
            for page, page_recs in _book_page_groups(records):
                # Show up to 3 records per page to avoid context bloat.
                out.append(f"**p {page}** "
                           f"({len(page_recs)} hit"
                           f"{'s' if len(page_recs) != 1 else ''}):\n")
                out.append("```")
                for r in page_recs[:3]:
                    bbox = r["bbox"]
                    y_lo = int(bbox[1]) if bbox else "?"
                    y_hi = int(bbox[3]) if bbox else "?"
                    out.append(f"  y[{y_lo}-{y_hi}] {r['text']}")
                if len(page_recs) > 3:
                    out.append(f"  … +{len(page_recs) - 3} more on p{page}")
                out.append("```\n")
    else:
        out.append("*(no book passages matched)*\n")

    out.append("## Gaps — query lemmas with no KB coverage\n")
    if gaps:
        out.append(", ".join(f"`{g}`" for g in gaps))
        out.append("")
        out.append("These lemmas appear in the query but are absent from "
                   "the topic graph, project notes, and all four book "
                   "extractions. An answer about these terms would be "
                   "**guessing from pre-training**, not citation-grounded.")
    else:
        out.append("*(none — every query lemma has at least one KB hit)*")

    out.append("")
    return "\n".join(out)


# ---------- main ----------


def _read_input(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("no input — pass text as argv, --file, or stdin")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("text", nargs="?", help="Armenian text to look up")
    ap.add_argument("--file", help="read text from file instead")
    ap.add_argument("--full-topics", action="store_true",
                    help="dump full topic-file bodies (default: excerpts only)")
    args = ap.parse_args()

    text = _read_input(args)
    pairs = query_lemmas(text)
    queried = [le for _, le in pairs]
    topic_hits = grep_topics(queried)
    note_hits = grep_project_notes(queried)
    book_hits = grep_books(queried)
    bundle = render_bundle(
        text, pairs, topic_hits, note_hits, book_hits,
        full_topics=args.full_topics,
    )
    print(bundle)
    return 0


if __name__ == "__main__":
    sys.exit(main())
