#!/usr/bin/env python3
"""Structural lint for hayeren topic files.

Validates frontmatter schema, source-block consistency, and [#N]
references in the body. Phase 1 of the `critic-pass` skill — pairs
with `citation-check` (which verifies the verbatim quotes).

Usage:
    sakayan/.venv/bin/python .claude/skills/critic-pass/lint.py \\
        topics/<domain>/<phenomenon>.md [more.md ...]
    sakayan/.venv/bin/python .claude/skills/critic-pass/lint.py \\
        topics/**/*.md --json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import yaml
except ImportError:
    print("FATAL: pyyaml not installed.", file=sys.stderr)
    sys.exit(2)


KNOWN_DOMAINS = {
    "phonology", "morphology", "syntax", "semantics",
    "pragmatics", "lexicon", "pedagogy",
}

VALID_SUPPORTS = {"supported", "partially-supported", "unsupported", "uncertain"}
VALID_ATTESTATION = {"single-source", "multi-attested", "conflicting"}
VALID_STATUS = {"draft", "reviewed", "stable"}

REQUIRED_TOP_LEVEL = {"topic", "domain", "status", "attestation", "sources"}
REQUIRED_SOURCE = {"id", "book", "page", "y_range", "verbatim_quote", "supports", "note"}


class Finding(NamedTuple):
    severity: str   # 'error' | 'warning' | 'info'
    where: str
    message: str


def parse_topic(md_path: Path) -> tuple[dict, str]:
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("no YAML frontmatter (must start with ---)")
    end = text.index("\n---\n", 4)
    return yaml.safe_load(text[4:end]), text[end + 5:]


def lint(md_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        fm, body = parse_topic(md_path)
    except Exception as e:
        return [Finding("error", "frontmatter", str(e))]

    if not isinstance(fm, dict):
        return [Finding("error", "frontmatter", "must be a YAML mapping")]

    for f in sorted(REQUIRED_TOP_LEVEL - fm.keys()):
        findings.append(Finding("error", "frontmatter", f"missing field: {f}"))

    if "domain" in fm and fm["domain"] not in KNOWN_DOMAINS:
        findings.append(Finding("warning", "frontmatter",
            f"unknown domain {fm['domain']!r}; known: {sorted(KNOWN_DOMAINS)}"))
    if "status" in fm and fm["status"] not in VALID_STATUS:
        findings.append(Finding("error", "frontmatter",
            f"invalid status {fm['status']!r}; must be one of {sorted(VALID_STATUS)}"))
    if "attestation" in fm and fm["attestation"] not in VALID_ATTESTATION:
        findings.append(Finding("error", "frontmatter",
            f"invalid attestation {fm['attestation']!r}; must be one of {sorted(VALID_ATTESTATION)}"))

    sources = fm.get("sources", [])
    if not isinstance(sources, list) or not sources:
        findings.append(Finding("error", "sources", "no sources defined"))
        return findings

    ids_seen: dict = {}
    books: set = set()
    for i, src in enumerate(sources):
        where = f"sources[{i}]"
        if not isinstance(src, dict):
            findings.append(Finding("error", where, "must be a mapping"))
            continue
        for f in sorted(REQUIRED_SOURCE - src.keys()):
            findings.append(Finding("error", where, f"missing field: {f}"))
        sid = src.get("id")
        if sid is not None:
            if sid in ids_seen:
                findings.append(Finding("error", where,
                    f"duplicate id {sid} (also in sources[{ids_seen[sid]}])"))
            ids_seen[sid] = i
        if "supports" in src and src["supports"] not in VALID_SUPPORTS:
            findings.append(Finding("warning", where,
                f"invalid supports {src['supports']!r}; must be one of {sorted(VALID_SUPPORTS)}"))
        yr = src.get("y_range")
        if yr is not None:
            if not (isinstance(yr, list) and len(yr) == 2
                    and all(isinstance(v, (int, float)) for v in yr)):
                findings.append(Finding("error", where,
                    "y_range must be a list of two numbers"))
            elif yr[0] >= yr[1]:
                findings.append(Finding("error", where,
                    f"y_range[0] ({yr[0]}) must be < y_range[1] ({yr[1]})"))
        if not str(src.get("note", "")).strip():
            findings.append(Finding("warning", where, "empty or missing note"))
        if src.get("book"):
            books.add(src["book"])

    attestation = fm.get("attestation")
    if attestation == "multi-attested" and len(books) < 2:
        findings.append(Finding("warning", "frontmatter",
            f"attestation=multi-attested but only {len(books)} distinct book(s) cited"))
    if attestation == "single-source" and len(books) > 1:
        findings.append(Finding("warning", "frontmatter",
            f"attestation=single-source but {len(books)} distinct books cited"))

    body_refs = set(int(m) for m in re.findall(r"\[#(\d+)\]", body))
    src_ids = set(ids_seen.keys())
    for ref in sorted(body_refs - src_ids):
        findings.append(Finding("error", "body",
            f"reference [#{ref}] but no source has id={ref}"))
    for ref in sorted(src_ids - body_refs):
        findings.append(Finding("info", "body",
            f"source #{ref} defined but not referenced in body"))

    gaps = fm.get("gaps", [])
    if not gaps:
        findings.append(Finding("info", "frontmatter",
            "no gaps listed — every topic should have at least one open question"))
    elif isinstance(gaps, list):
        for i, g in enumerate(gaps):
            if not str(g).strip():
                findings.append(Finding("warning", f"gaps[{i}]", "empty gap"))

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic_md", type=Path, nargs="+",
                    help="topic markdown files to lint")
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON")
    args = ap.parse_args()

    all_files = []
    n_errors = 0
    for path in args.topic_md:
        findings = lint(path)
        n_errors += sum(1 for f in findings if f.severity == "error")
        all_files.append({
            "path": str(path),
            "findings": [f._asdict() for f in findings],
        })

    if args.json:
        json.dump({"n_errors": n_errors, "files": all_files},
                  sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sev_prefix = {"error": "ERR ", "warning": "WARN", "info": "INFO"}
        for entry in all_files:
            findings = entry["findings"]
            n_err = sum(1 for f in findings if f["severity"] == "error")
            n_warn = sum(1 for f in findings if f["severity"] == "warning")
            n_info = sum(1 for f in findings if f["severity"] == "info")
            tag = "OK" if n_err == 0 else "FAIL"
            print(f"[{tag}] {entry['path']}: "
                  f"{n_err} error(s), {n_warn} warning(s), {n_info} info")
            for f in findings:
                print(f"  [{sev_prefix[f['severity']]}] {f['where']}: {f['message']}")
            if findings:
                print()
        print(f"TOTAL: {n_errors} error(s) across {len(all_files)} file(s)")

    return 0 if n_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
