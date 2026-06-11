#!/usr/bin/env python3
"""Citation checker for hayeren topic files.

Reads a topic markdown file's YAML frontmatter, extracts the `sources:`
list, and verifies that each `verbatim_quote` actually appears at the
cited (page, y_range) in the corresponding book's `full.jsonl`.

Per-fragment statuses:
    OK    fragment found in the cited (page, y_range) window
    FAIL  fragment not found — the only hard error
    SKIP  fragment structurally unverifiable (book has no extracted
          JSONL — e.g. external sources like bararan.am — or `page`
          is null); reported, never fatal

Non-fatal WARNs (precision downgrades, printed per fragment):
    - `y_range` null/missing → fragment is checked against the WHOLE
      page and the result is marked page-wide (location precision
      lost, existence still verified)
    - fragment has < 4 Armenian letters and < 8 letters total
      (would verify almost anywhere; long English prose fragments —
      legitimate in the bilingual textbooks — are exempt)
    - y-window spans > 60% of the page's actual span y-extent
      (computed from that page's spans, so unit-agnostic: points for
      sakayan/ghamoyan, pixels for parnasyan/tioyan)

Usage:
    sakayan/.venv/bin/python .claude/skills/citation-check/check.py \\
        topics/<domain>/<phenomenon>.md
    sakayan/.venv/bin/python .claude/skills/citation-check/check.py \\
        topics/<domain>/<phenomenon>.md --json

Exit codes: 0 = no FAILs (WARN/SKIP allowed), 1 = at least one FAIL,
2 = usage/input error (missing frontmatter, no sources, missing deps).
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
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        raise ValueError(
            f"{md_path}: unterminated YAML frontmatter (no closing ---)"
        ) from None
    return yaml.safe_load(text[4:end])


def load_spans(book: str) -> list[dict]:
    path = book_jsonl(book)
    spans = []
    for line in path.read_text(encoding="utf-8").splitlines():
        # Tolerate a truncated/garbled line (the JSONL may be mid-
        # rewrite by an extraction run) rather than crashing the check.
        try:
            spans.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return spans


ARMENIAN_MIN_LETTERS = 4
# A fragment with this many letters of ANY script is distinctive
# enough even with few Armenian letters (sakayan is a bilingual
# textbook — long English prose fragments are legitimate and have 0
# Armenian letters; warning on them would be pure noise).
TOTAL_MIN_LETTERS = 8
Y_WINDOW_MAX_FRACTION = 0.60


def count_armenian_letters(s: str) -> int:
    """Count chars in the Armenian block U+0530–U+058F."""
    return sum(1 for ch in s if 0x0530 <= ord(ch) <= 0x058F)


def is_short_fragment(frag: str) -> bool:
    """True for fragments too short to be distinctive: fewer than
    ARMENIAN_MIN_LETTERS Armenian letters AND fewer than
    TOTAL_MIN_LETTERS letters overall."""
    if count_armenian_letters(frag) >= ARMENIAN_MIN_LETTERS:
        return False
    return sum(1 for ch in frag if ch.isalpha()) < TOTAL_MIN_LETTERS


def check_source(src: dict, spans_by_book: dict) -> list[dict]:
    """Verify each fragment in src['verbatim_quote'] against the cited region.

    Returns a list of result dicts (one per fragment), each with
    `status` in {"OK", "FAIL", "SKIP"} and a `warnings` list. `ok`
    is kept (True iff found) for backward compatibility of --json
    consumers; SKIP rows carry ok=None.
    """
    book = src["book"]
    page = src.get("page")
    y_range = src.get("y_range")

    quote = src["verbatim_quote"]
    fragments = [quote] if isinstance(quote, str) else list(quote)

    def result(frag, status, *, ok, warnings, diagnostic=""):
        return {
            "source_id": src.get("id", "?"),
            "book": book,
            "page": page,
            "y_range": list(y_range) if y_range else None,
            "fragment": frag,
            "status": status,
            "ok": ok,
            "warnings": warnings,
            "diagnostic": diagnostic,
        }

    # --- structural skips: nothing to verify against ---------------
    if book not in spans_by_book:
        try:
            spans_by_book[book] = load_spans(book)
        except FileNotFoundError:
            spans_by_book[book] = None
    spans = spans_by_book[book]
    if spans is None:
        msg = (f"book {book!r} has no extracted full.jsonl — "
               f"fragment unverifiable against a corpus")
        return [result(f, "SKIP", ok=None, warnings=[], diagnostic=msg)
                for f in fragments]
    if page is None:
        msg = "page is null — fragment unverifiable at any location"
        return [result(f, "SKIP", ok=None, warnings=[], diagnostic=msg)
                for f in fragments]

    page_spans = [s for s in spans if s["page"] == page]

    # --- y-window handling ------------------------------------------
    src_warnings: list[str] = []
    if y_range is None:
        # Downgrade precision, don't crash: verify existence against
        # the whole page and say so.
        region = page_spans
        ylo = yhi = None
        src_warnings.append(
            "y_range missing — fragment unverifiable at location; "
            "checked page-wide")
    else:
        ylo, yhi = y_range
        region = [s for s in page_spans if ylo <= s["bbox"][1] <= yhi]
        # Window-width sanity: a y-window spanning most of the page
        # verifies almost anything, defeating the location check.
        # Extent comes from the page's own spans, so the test is
        # unit-agnostic (points vs pixels).
        if page_spans:
            ext_lo = min(s["bbox"][1] for s in page_spans)
            ext_hi = max(s["bbox"][3] for s in page_spans)
            extent = ext_hi - ext_lo
            if extent > 0 and (yhi - ylo) > Y_WINDOW_MAX_FRACTION * extent:
                src_warnings.append(
                    f"y-window [{ylo}-{yhi}] covers "
                    f"{(yhi - ylo) / extent:.0%} of the page's span "
                    f"y-extent [{ext_lo:.0f}-{ext_hi:.0f}] — location "
                    f"check is nearly page-wide")

    haystack = normalize(" ".join(s["text"] for s in region))

    results = []
    for frag in fragments:
        warnings = list(src_warnings)
        if is_short_fragment(frag):
            warnings.append(
                f"fragment has < {ARMENIAN_MIN_LETTERS} Armenian "
                f"letters (and < {TOTAL_MIN_LETTERS} letters total) — "
                f"short enough to verify almost anywhere")
        needle = normalize(frag)
        ok = needle in haystack
        diagnostic = ""
        if not ok:
            if y_range is None:
                diagnostic = (f"page {page} had {len(region)} spans "
                              f"containing no match (page-wide check)")
            else:
                wider = [s for s in page_spans
                         if ylo - 30 <= s["bbox"][1] <= yhi + 30]
                diagnostic = (
                    f"region had {len(region)} spans containing no match; "
                    f"widening y to ±30 yields {len(wider)} spans"
                )
        results.append(result(frag, "OK" if ok else "FAIL",
                              ok=ok, warnings=warnings,
                              diagnostic=diagnostic))
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

    try:
        fm = parse_frontmatter(args.topic_md)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if not isinstance(fm, dict):
        print(f"ERROR: {args.topic_md}: frontmatter is not a YAML mapping",
              file=sys.stderr)
        return 2
    sources = fm.get("sources", [])
    if not sources:
        print(f"{args.topic_md}: no `sources:` in frontmatter", file=sys.stderr)
        return 2

    spans_by_book: dict = {}
    all_results = []
    for src in sources:
        all_results.extend(check_source(src, spans_by_book))

    n_pass = sum(1 for r in all_results if r["status"] == "OK")
    n_fail = sum(1 for r in all_results if r["status"] == "FAIL")
    n_skip = sum(1 for r in all_results if r["status"] == "SKIP")
    n_warn = sum(len(r["warnings"]) for r in all_results)
    n_total = len(all_results)

    if args.json:
        json.dump({
            "topic": str(args.topic_md),
            "n_pass": n_pass,
            "n_fail": n_fail,
            "n_skip": n_skip,
            "n_warnings": n_warn,
            "n_total": n_total,
            "results": all_results,
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        summary = f"{args.topic_md}: {n_pass}/{n_total} verbatim fragments verified"
        extras = []
        if n_skip:
            extras.append(f"{n_skip} skipped")
        if n_warn:
            extras.append(f"{n_warn} warning{'s' if n_warn != 1 else ''}")
        if extras:
            summary += f" ({', '.join(extras)})"
        print(summary)
        print()
        for r in all_results:
            flag = {"OK": "OK  ", "FAIL": "FAIL", "SKIP": "SKIP"}[r["status"]]
            print(f"  [{flag}] src#{r['source_id']} {r['book']} "
                  f"p{r['page']} y={r['y_range']}  {r['fragment']!r}")
            if r["status"] != "OK" and r["diagnostic"]:
                print(f"          {r['diagnostic']}")
            for w in r["warnings"]:
                print(f"          warn: {w}")

    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
