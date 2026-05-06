#!/usr/bin/env python3
"""Citation checker for hayeren topic files.

Reads a topic markdown file's YAML frontmatter, extracts the `sources:`
list, and verifies that each `verbatim_quote` actually appears at the
cited (page, y_range) in the corresponding book's `full.jsonl`.

Usage:
    sakayan/.venv/bin/python .claude/skills/citation-check/check.py \\
        topics/<domain>/<phenomenon>.md
    sakayan/.venv/bin/python .claude/skills/citation-check/check.py \\
        topics/<domain>/<phenomenon>.md --json

Exit code 0 iff every fragment verifies, else 1.
"""

import argparse
import json
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FATAL: pyyaml not installed. Install with:", file=sys.stderr)
    print("  sakayan/.venv/bin/pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def find_project_root() -> Path:
    """Walk up from this file until we find kb-design.md (the project marker)."""
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "kb-design.md").exists():
            return p
        p = p.parent
    raise RuntimeError("could not find project root (no kb-design.md ancestor)")


PROJECT_ROOT = find_project_root()


def book_jsonl(book_name: str) -> Path:
    """Resolve a `book:` slug to its full.jsonl path.

    Tries the future layout `books/<name>/out/full.jsonl` first,
    falls back to the current top-level `<name>/out/full.jsonl`.
    """
    for candidate in (
        PROJECT_ROOT / "books" / book_name / "out" / "full.jsonl",
        PROJECT_ROOT / book_name / "out" / "full.jsonl",
    ):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Could not find full.jsonl for book {book_name!r}; tried\n"
        f"  {PROJECT_ROOT / 'books' / book_name / 'out' / 'full.jsonl'}\n"
        f"  {PROJECT_ROOT / book_name / 'out' / 'full.jsonl'}"
    )


def normalize(s: str) -> str:
    """NFC-normalise — Armenian script and Sakayan's Armtrans diacritics
    show up in either NFC or NFD; matching needs a canonical form."""
    return unicodedata.normalize("NFC", s)


def parse_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{md_path}: no YAML frontmatter (must start with ---)")
    end = text.index("\n---\n", 4)
    return yaml.safe_load(text[4:end])


def load_spans(book: str) -> list[dict]:
    path = book_jsonl(book)
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]


def check_source(src: dict, spans_by_book: dict) -> list[dict]:
    """Verify each fragment in src['verbatim_quote'] against the cited region.

    Returns a list of result dicts (one per fragment).
    """
    book = src["book"]
    page = src["page"]
    ylo, yhi = src["y_range"]

    if book not in spans_by_book:
        spans_by_book[book] = load_spans(book)
    spans = spans_by_book[book]

    region = [s for s in spans
              if s["page"] == page and ylo <= s["bbox"][1] <= yhi]
    haystack = normalize(" ".join(s["text"] for s in region))

    quote = src["verbatim_quote"]
    fragments = [quote] if isinstance(quote, str) else list(quote)

    results = []
    for frag in fragments:
        needle = normalize(frag)
        ok = needle in haystack
        diagnostic = ""
        if not ok:
            wider = [s for s in spans
                     if s["page"] == page and ylo - 30 <= s["bbox"][1] <= yhi + 30]
            diagnostic = (
                f"region had {len(region)} spans containing no match; "
                f"widening y to ±30pt yields {len(wider)} spans"
            )
        results.append({
            "source_id": src.get("id", "?"),
            "book": book,
            "page": page,
            "y_range": [ylo, yhi],
            "fragment": frag,
            "ok": ok,
            "diagnostic": diagnostic,
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("topic_md", type=Path,
                    help="path to topics/<domain>/<phenomenon>.md")
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON instead of human output")
    args = ap.parse_args()

    fm = parse_frontmatter(args.topic_md)
    sources = fm.get("sources", [])
    if not sources:
        print(f"{args.topic_md}: no `sources:` in frontmatter", file=sys.stderr)
        return 2

    spans_by_book: dict = {}
    all_results = []
    for src in sources:
        all_results.extend(check_source(src, spans_by_book))

    n_pass = sum(1 for r in all_results if r["ok"])
    n_total = len(all_results)

    if args.json:
        json.dump({
            "topic": str(args.topic_md),
            "n_pass": n_pass,
            "n_total": n_total,
            "results": all_results,
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"{args.topic_md}: {n_pass}/{n_total} verbatim fragments verified")
        print()
        for r in all_results:
            flag = "OK  " if r["ok"] else "FAIL"
            print(f"  [{flag}] src#{r['source_id']} {r['book']} "
                  f"p{r['page']} y={r['y_range']}  {r['fragment']!r}")
            if not r["ok"]:
                print(f"          {r['diagnostic']}")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
