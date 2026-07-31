"""Step A: structure recovery — span JSONL → markdown + provenance.

Reads a page range from `<book>/out/full.jsonl`, reconstructs lines,
paragraphs, headings and footnotes, and writes:

    interlinear/<book>/<chunk>/book.md    readable markdown, block anchors
    interlinear/<book>/<chunk>/blocks.tsv provenance: id, kind, pages, y, text
    interlinear/<book>/<chunk>/drops.tsv  spans excluded (footers) — the
                                          byte-check subtracts these

The artifact is final input to steps B-E; rerunning A regenerates it
from the source only. Hyphens at line ends are KEPT (in this book they
are mostly genuine compound hyphens of standard-colloquial pairs, not
soft hyphenation) — the golden-page check guards this choice.

Usage:
    python3 structure.py --book ghamoyan --pages 35-40 --chunk ch2
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (PROFILES, Line, cluster_lines, load_spans,  # noqa: E402
                    md_to_plain)

CHAPTER_NUM_RE = re.compile(r"^ԳԼՈՒԽ\s+\d+\s*$")


def classify_lines(lines: list[Line], profile: dict):
    """Split raw lines into body/heading lines, footnotes, drops."""
    body: list[Line] = []
    footnotes: list[Line] = []
    markers: list[tuple[int, float, str]] = []  # (page, y, digits)
    drops: list[tuple[int, float, str, str]] = []
    for ln in lines:
        text = ln.text.strip()
        if ln.y0 >= profile["footer_y"]:
            drops.append((ln.page, ln.y0, "footer", text))
        elif ln.max_size <= profile["footnote_max_size"] and ln.y0 > 500:
            footnotes.append(ln)
        elif (ln.max_size <= profile["marker_max_size"]
              and text.isdigit()):
            markers.append((ln.page, ln.y0, text))
        else:
            # tiny digit spans *inside* a normal line are footnote
            # markers that got clustered with their line
            kept_runs = []
            for t, st in ln.runs:
                kept_runs.append((t, st))
            ln.runs = kept_runs
            body.append(ln)
    return body, footnotes, markers, drops


def mark_footnote_refs(spans: list[dict], profile: dict) -> list[str]:
    """Rewrite tiny mid-page digit spans to [^N] in place.

    Done *before* line clustering so the x-sort positions the marker
    exactly where the superscript sits. Bottom-of-page small digits
    (the footnote's own leading number) are left alone.
    """
    notes = []
    for s in spans:
        if (s["size"] <= profile["marker_max_size"]
                and s["text"].strip().isdigit()
                and s["bbox"][1] < 500):
            notes.append(f"[^{s['text'].strip()}] at p{s['page']}"
                         f" y{s['bbox'][1]:.0f}")
            s["text"] = f"[^{s['text'].strip()}]"
            s["font"] = "marker"
    return notes


STYLE_MD = {"": ("", ""), "b": ("**", "**"), "i": ("*", "*"),
            "bi": ("***", "***")}


_NO_LETTER_RE = re.compile(r"^[^\w]*$|^\d{1,3}$")


def runs_to_md(runs: list[tuple[str, str]]) -> str:
    """Merge adjacent same-style runs, emit markdown emphasis.

    Short letter-less runs (diacritics like ՛/՞, commas, braces) that
    sit between styled runs adopt the preceding run's style — bytes
    are unchanged, and it prevents broken emphasis like ***x***՛***y***.
    Emphasis delimiters must sit flush against non-space text, so
    leading/trailing spaces of a styled group are moved outside.
    """
    absorbed: list[tuple[str, str]] = []
    for i, (t, st) in enumerate(runs):
        stripped = t.strip()
        if (stripped and len(stripped) <= 3
                and not t.startswith("[^")
                and _NO_LETTER_RE.match(stripped)):
            # openers bind forward ("(զգույշ" opens the italic gloss),
            # everything else (closers, commas, diacritics) backward
            if stripped[0] in "({[«":
                nxt = next((s for tt, s in runs[i + 1:] if tt.strip()),
                           None)
                if nxt is not None:
                    st = nxt
            elif absorbed:
                st = absorbed[-1][1]
        absorbed.append((t, st))
    merged: list[tuple[str, str]] = []
    for t, st in absorbed:
        if merged and merged[-1][1] == st:
            merged[-1] = (merged[-1][0] + t, st)
        else:
            merged.append((t, st))

    # nested-emphasis emitter: bold/italic as a tag stack, so an
    # italic letter inside a bold word becomes **ար*ց*յունք** rather
    # than ambiguous close-reopen (****). Whitespace between runs is
    # held back so delimiters stay flush against text.
    DELIM = {"b": "**", "i": "*"}
    WANT = {"": set(), "b": {"b"}, "i": {"i"}, "bi": {"b", "i"}}
    out: list[str] = []
    stack: list[str] = []
    pending_ws = ""
    for t, st in merged:
        lead = t[: len(t) - len(t.lstrip())]
        core = t.strip()
        trail = t[len(t.rstrip()):]
        if not core:
            pending_ws += t
            continue
        want = WANT[st]
        # close styles not wanted (unwind stack top-down)
        while stack and (set(stack) - want or
                         not set(stack) <= want):
            if set(stack) <= want:
                break
            out.append(DELIM[stack.pop()])
        out.append(pending_ws + lead)
        pending_ws = ""
        for sty in ("b", "i"):  # bold outermost: italic toggles cheap
            if sty in want and sty not in stack:
                stack.append(sty)
                out.append(DELIM[sty])
        out.append(core)
        pending_ws = trail
    while stack:
        out.append(DELIM[stack.pop()])
    out.append(pending_ws)
    return "".join(out)


def escape_md(line: str) -> str:
    if line[:1] in "#>-+" or re.match(r"^\d+[.)]", line):
        return "\\" + line
    return line


def build_blocks(body: list[Line], profile: dict):
    """Lines → (kind, [lines]) blocks with paragraph/heading logic."""
    blocks: list[tuple[str, list[Line]]] = []
    for ln in body:
        is_heading = (ln.max_size >= profile["heading_min_size"]
                      and ln.has_bold)
        if is_heading:
            if (blocks and blocks[-1][0] == "heading"
                    and not CHAPTER_NUM_RE.match(blocks[-1][1][-1].text.strip())):
                blocks[-1][1].append(ln)
            else:
                blocks.append(("heading", [ln]))
            continue
        new_para = ln.x0 >= profile["indent_left"] - 3.0
        cont = (blocks and blocks[-1][0] == "para" and not new_para)
        if cont:
            blocks[-1][1].append(ln)
        else:
            blocks.append(("para", [ln]))
    return blocks


def join_para_lines(lines: list[Line]) -> list[tuple[str, str]]:
    """Concatenate line runs; line break → space unless hyphen-joined."""
    runs: list[tuple[str, str]] = []
    for i, ln in enumerate(lines):
        if i > 0:
            prev_text = runs[-1][0] if runs else ""
            if not prev_text.rstrip().endswith("-"):
                if runs and not runs[-1][0].endswith(" "):
                    runs.append((" ", ""))
            else:
                # keep hyphen, join flush (compound split across lines)
                runs[-1] = (runs[-1][0].rstrip(), runs[-1][1])
        runs.extend(ln.runs)
    return runs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=sorted(PROFILES))
    ap.add_argument("--pages", required=True, help="e.g. 35-40")
    ap.add_argument("--chunk", required=True, help="output subdir name")
    args = ap.parse_args()

    profile = PROFILES[args.book]
    a, b = args.pages.split("-")
    pages = range(int(a), int(b) + 1)
    out_dir = Path(__file__).resolve().parent / args.book / args.chunk
    out_dir.mkdir(parents=True, exist_ok=True)

    spans = load_spans(profile, pages)
    marker_notes = mark_footnote_refs(spans, profile)
    lines = cluster_lines(spans, profile)
    body, foot_lines, _, drops = classify_lines(lines, profile)
    blocks = build_blocks(body, profile)

    md_lines: list[str] = [f"<!-- {args.book} pages {args.pages}"
                           f" — generated by interlinear/structure.py -->", ""]
    tsv_rows = []
    next_id = 1

    def emit(kind: str, lines_: list[Line], md_text: str):
        nonlocal next_id
        pgs = sorted({ln.page for ln in lines_})
        pages_str = (f"{pgs[0]}-{pgs[-1]}" if len(pgs) > 1 else str(pgs[0]))
        # y0 of the FIRST line / y1 of the LAST — not min/max, so a
        # cross-page block keeps its true reading-order start position
        y0 = lines_[0].y0
        y1 = lines_[-1].y1
        md_lines.append(f"<!--b:{next_id:04d} p:{pages_str}"
                        f" y:{y0:.0f}-{y1:.0f} k:{kind}-->")
        md_lines.append(md_text)
        md_lines.append("")
        plain = re.sub(r"\s+", " ", md_to_plain(md_text))
        tsv_rows.append((f"{next_id:04d}", kind, pages_str,
                         f"{y0:.0f}", f"{y1:.0f}", plain))
        next_id += 1

    for kind, block_lines in blocks:
        if kind == "heading":
            text = " ".join(ln.text.strip() for ln in block_lines)
            emit("heading", block_lines, f"## {text}")
        else:
            runs = join_para_lines(block_lines)
            emit("para", block_lines, escape_md(runs_to_md(runs).strip()))

    # footnotes: group consecutive small lines, leading digits = id
    if foot_lines:
        joined = join_para_lines(foot_lines)
        text = runs_to_md(joined).strip()
        m = re.match(r"^(\d+)\s*(.*)$", text, re.S)
        if m:
            text = f"[^{m.group(1)}]: {m.group(2)}"
        emit("footnote", foot_lines, text)

    (out_dir / "book.md").write_text("\n".join(md_lines) + "\n",
                                     encoding="utf-8")
    with (out_dir / "blocks.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["block_id", "kind", "pages", "y0", "y1", "text"])
        w.writerows(tsv_rows)
    with (out_dir / "drops.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["page", "y", "reason", "text"])
        w.writerows(drops)

    print(f"wrote {len(tsv_rows)} blocks, {len(drops)} drops -> {out_dir}")
    for note in marker_notes:
        print("note:", note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
