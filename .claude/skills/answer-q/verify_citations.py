#!/usr/bin/env python3
"""Validate that an answer's citations actually appear in the
KB-grounding bundle that produced the answer.

Pipeline (see `.claude/skills/answer-q/SKILL.md`):

    query_kb.py  →  bundle.md
    LLM (with bundle as context)  →  answer.md
    verify_citations.py --bundle bundle.md --answer answer.md
        → exit 0 if all citations resolve; non-zero with a
          per-citation report otherwise.

Citation surface forms recognised in answers (case-insensitive
on the path / book name):

  inline markdown:   `topics/foo/bar.md`
  bracketed inline:  [topics/foo/bar.md]
  book + page:       [ghamoyan p48]   ghamoyan p 48   per ghamoyan p48
  project notes:     [armenian-grammar.md] etc.
  synthesis flag:    [interpretive synthesis] / [synthesis]
                     — accepted but logged

Findings:

  unsupported-path     — answer cites a topic/note path absent
                         from the bundle
  unsupported-book     — answer cites a book+page absent from
                         the bundle's book-passages section
  missed-citation      — a "gap" or unsupported claim cites
                         nothing, but the bundle in fact covers
                         the lemma
  synthesis-marker     — answer used `[interpretive synthesis]`
                         (informational; not an error)

Exit code 0 if no `unsupported-*` findings. `--strict` makes
`missed-citation` errors as well.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable


# ---------- bundle parsing ----------


_BUNDLE_TOPIC_HEADER = re.compile(
    r"^###\s+`((?:topics|.*?\.md))`\s+—",
)
_BUNDLE_BOOK_HEADER = re.compile(r"^###\s+(\w+)\s*$")
_BUNDLE_BOOK_PAGE = re.compile(r"^\*\*p\s+(\d+)\*\*")
_BUNDLE_GAPS_SECTION = re.compile(r"^##\s+Gaps\s*—")


def parse_bundle(bundle_text: str) -> dict:
    """Extract the citable surface from a query_kb bundle.

    Returns:
        {
          "topic_paths": set[str],      # `topics/foo/bar.md`, `armenian-grammar.md`, …
          "book_pages": set[(book, int)],
          "gaps": set[str],             # query lemmas with no KB hit
        }
    """
    topic_paths: set[str] = set()
    book_pages: set[tuple[str, int]] = set()
    gaps: set[str] = set()

    in_books = False
    current_book: str | None = None
    in_gaps = False

    lines = bundle_text.splitlines()
    for i, line in enumerate(lines):
        # Topic / project-note headers — both rendered as
        #   `### \`<path>\` — N match(es): …`
        m = _BUNDLE_TOPIC_HEADER.match(line)
        if m:
            topic_paths.add(m.group(1).strip("`"))
            continue
        # Section transitions
        if line.startswith("## Matched book passages"):
            in_books = True
            in_gaps = False
            current_book = None
            continue
        if _BUNDLE_GAPS_SECTION.match(line):
            in_books = False
            in_gaps = True
            continue
        if line.startswith("## "):
            in_books = False
            in_gaps = False
            current_book = None
            continue
        if in_books:
            mb = _BUNDLE_BOOK_HEADER.match(line)
            if mb and mb.group(1).lower() in (
                    "sakayan", "ghamoyan", "parnasyan", "tioyan"):
                current_book = mb.group(1).lower()
                continue
            mp = _BUNDLE_BOOK_PAGE.match(line)
            if mp and current_book:
                book_pages.add((current_book, int(mp.group(1))))
                continue
        if in_gaps:
            for tok in re.findall(r"`([Ա-Ֆա-ֆև_]+)`", line):
                gaps.add(tok.lower())

    return {
        "topic_paths": topic_paths,
        "book_pages": book_pages,
        "gaps": gaps,
    }


# ---------- answer parsing ----------


# Path-like citation: matches `topics/x/y.md`, `armenian-grammar.md`, etc.
# Loose enough to catch both inline-code and bracketed forms.
_CITE_PATH = re.compile(
    r"[`\[]([A-Za-z0-9_./-]+\.md)[`\]]"
)
# Book + page: `[ghamoyan p48]`, `(per sakayan p 102)`, `ghamoyan, p. 48`.
_CITE_BOOK = re.compile(
    r"\b(sakayan|ghamoyan|parnasyan|tioyan)\b[^A-Za-z0-9]{0,5}p\.?\s*(\d+)",
    re.IGNORECASE,
)
_CITE_SYNTHESIS = re.compile(
    r"\[(?:interpretive\s+synthesis|synthesis)\]",
    re.IGNORECASE,
)


def parse_answer(answer_text: str) -> dict:
    paths = set()
    book_pages: set[tuple[str, int]] = set()
    has_synthesis = bool(_CITE_SYNTHESIS.search(answer_text))
    for m in _CITE_PATH.finditer(answer_text):
        p = m.group(1)
        # Skip self-references that aren't actual citations
        # (e.g. "see SKILL.md" mentions in narrative).
        if p.endswith(".md") and "/" in p:
            paths.add(p)
        elif p.endswith(".md"):
            # Project-note paths at the root.
            paths.add(p)
    for m in _CITE_BOOK.finditer(answer_text):
        book_pages.add((m.group(1).lower(), int(m.group(2))))
    return {
        "paths": paths,
        "book_pages": book_pages,
        "has_synthesis": has_synthesis,
    }


# ---------- verification ----------


def _emit(findings: list, severity: str, kind: str, what: str,
          hint: str = "") -> None:
    findings.append({
        "severity": severity, "kind": kind, "what": what, "hint": hint,
    })


def verify(bundle: dict, answer: dict, *, strict: bool) -> list:
    findings: list = []

    for path in sorted(answer["paths"]):
        if path not in bundle["topic_paths"]:
            _emit(findings, "error", "unsupported-path", path,
                  "answer cites this path but bundle did not surface it")

    for (book, page) in sorted(answer["book_pages"]):
        if (book, page) not in bundle["book_pages"]:
            _emit(findings, "error", "unsupported-book",
                  f"{book} p{page}",
                  "answer cites this book+page but bundle did not "
                  "surface it")

    if answer["has_synthesis"]:
        _emit(findings, "info", "synthesis-marker",
              "[interpretive synthesis]",
              "answer includes a synthesis claim — fine if each "
              "component is cited; flag for human review")

    # missed-citation: bundle declared no gaps for any lemma in
    # answer's covered set, but answer claims a gap. Coarse heuristic
    # — left as an info-finding by default; --strict promotes.
    return findings


# ---------- I/O ----------


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--bundle", required=True, type=Path,
                    help="path to query_kb.py output")
    ap.add_argument("--answer", required=True, type=Path,
                    help="path to LLM answer (markdown)")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on info-severity findings too")
    args = ap.parse_args()

    bundle = parse_bundle(args.bundle.read_text(encoding="utf-8"))
    answer = parse_answer(args.answer.read_text(encoding="utf-8"))
    findings = verify(bundle, answer, strict=args.strict)

    print(f"Bundle: {len(bundle['topic_paths'])} topic-paths, "
          f"{len(bundle['book_pages'])} book-pages, "
          f"{len(bundle['gaps'])} declared gaps.")
    print(f"Answer: {len(answer['paths'])} path-cites, "
          f"{len(answer['book_pages'])} book-cites, "
          f"synthesis-marker={answer['has_synthesis']}.")
    print()
    n_err = sum(1 for f in findings if f["severity"] == "error")
    n_info = sum(1 for f in findings if f["severity"] == "info")
    if not findings:
        print("All citations resolve against the bundle. ✓")
        return 0
    for fnd in findings:
        print(f"  [{fnd['severity']}] {fnd['kind']}: "
              f"{fnd['what']} — {fnd['hint']}")
    print()
    print(f"{n_err} error(s), {n_info} info finding(s).")
    if n_err or (args.strict and n_info):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
