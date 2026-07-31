"""Shared machinery for the interlinear pipeline.

Line clustering is shared between structure.py (step A) and
validate.py (step E) so the byte-check compares the *same* reading
order the builder used — see FRD § E.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per-book layout profile. Constants measured from the span data
# (see research/2026-07-23-interlinear-reader-frd.md § A).
PROFILES: dict[str, dict] = {
    "ghamoyan": dict(
        jsonl=ROOT / "ghamoyan" / "out" / "full.jsonl",
        pdf=ROOT / "ghamoyan" / "erewani_khosaktsakan_lezown.pdf",
        manifest=ROOT / "ghamoyan" / "manifest.yaml",
        body_left=51.1,        # continuation-line left margin
        indent_left=79.4,      # paragraph-initial indent
        heading_min_size=11.5, # bold >= this → heading line
        footer_y=525.0,        # below this: page number footer
        footnote_max_size=7.6, # small text near bottom → footnote
        marker_max_size=7.0,   # tiny digit span → footnote marker
        line_tol=4.0,          # y-cluster tolerance (styled runs sit
                               # ~1.3pt below baseline; pitch is 10.3)
        gap_space=0.9,         # x-gap wider than this → word space
    ),
}

# font name → style key
_STYLE = [
    ("BoldItalic", "bi"), ("Bold", "b"), ("Italic", "i"),
]


def span_style(font: str) -> str:
    for needle, key in _STYLE:
        if needle in font:
            return key
    return ""


@dataclass
class Line:
    page: int
    y0: float
    y1: float
    x0: float
    # list of (text, style) runs in x order
    runs: list[tuple[str, str]] = field(default_factory=list)
    max_size: float = 0.0
    has_bold: bool = False

    @property
    def text(self) -> str:
        return "".join(t for t, _ in self.runs)


def load_spans(profile: dict, pages: range) -> list[dict]:
    out = []
    with open(profile["jsonl"], encoding="utf-8") as f:
        for raw in f:
            r = json.loads(raw)
            if r["page"] in pages and r["text"].strip():
                out.append(r)
    return out


def cluster_lines(spans: list[dict], profile: dict) -> list[Line]:
    """Group spans into visual lines per page, reading order."""
    lines: list[Line] = []
    for page in sorted({s["page"] for s in spans}):
        page_spans = sorted(
            (s for s in spans if s["page"] == page),
            key=lambda s: (s["bbox"][1], s["bbox"][0]),
        )
        clusters: list[list[dict]] = []
        for s in page_spans:
            if clusters and s["bbox"][1] - clusters[-1][0]["bbox"][1] <= profile["line_tol"]:
                clusters[-1].append(s)
            else:
                clusters.append([s])
        for cl in clusters:
            cl.sort(key=lambda s: s["bbox"][0])
            line = Line(
                page=page,
                y0=min(s["bbox"][1] for s in cl),
                y1=max(s["bbox"][3] for s in cl),
                x0=cl[0]["bbox"][0],
                max_size=max(s["size"] for s in cl),
                has_bold=any("Bold" in s["font"] for s in cl),
            )
            prev_end = None
            for s in cl:
                text = s["text"]
                if (prev_end is not None
                        and s["bbox"][0] - prev_end > profile["gap_space"]
                        and line.runs
                        and not line.runs[-1][0].endswith(" ")
                        and not text.startswith(" ")):
                    text = " " + text
                line.runs.append((text, span_style(s["font"])))
                prev_end = s["bbox"][2]
            lines.append(line)
    return lines


def squash(text: str) -> str:
    """Whitespace-insensitive normal form (NFC assumed upstream)."""
    return re.sub(r"\s+", "", text)


# ---------- markdown (step-A artifact) parsing ----------

ANCHOR_RE = re.compile(
    r"^<!--b:(?P<id>\d+) p:(?P<pages>[\d,-]+) y:(?P<y0>[\d.]+)-(?P<y1>[\d.]+)"
    r" k:(?P<kind>\w+)-->$"
)


@dataclass
class Block:
    id: int
    pages: list[int]
    y0: float
    y1: float
    kind: str          # heading | para | footnote
    md: str            # markdown source (no anchor line)

    @property
    def plain(self) -> str:
        return md_to_plain(self.md)


def md_to_plain(md: str) -> str:
    t = md
    t = re.sub(r"^#+\s*", "", t)
    t = re.sub(r"\[\^(\d+)\]:?\s?", r"\1 ", t)   # footnote marker/def → digits
    t = t.replace("***", "").replace("**", "").replace("*", "")
    t = t.replace("\\", "")
    return t


def md_runs(md: str) -> list[tuple[str, str]]:
    """Inverse of structure.runs_to_md: markdown → [(text, style)].

    Styles: '' | 'b' | 'i' | 'bi' | 'marker' (footnote ref [^N]).
    Asterisk runs are disambiguated by flanking (space side opens /
    closes) and, when flush on both sides (intra-word), by which
    styles are currently open — matching the emitter's grammar.
    """
    text = md
    if text.startswith("## "):
        text = text[3:]
    if text.startswith("\\"):
        text = text[1:]
    runs: list[tuple[str, str]] = []
    bold = italic = False
    stack: list[str] = []
    buf = []

    def flush():
        if buf:
            st = ("b" if bold else "") + ("i" if italic else "")
            runs.append(("".join(buf), st))
            buf.clear()

    i = 0
    n = len(text)
    while i < n:
        m = re.match(r"\[\^(\d+)\]", text[i:])
        if m:
            flush()
            runs.append((m.group(0), "marker"))
            i += m.end()
            continue
        if text[i] != "*":
            buf.append(text[i])
            i += 1
            continue
        j = i
        while j < n and text[j] == "*":
            j += 1
        cnt = j - i
        left = text[i - 1] if i > 0 else " "
        right = text[j] if j < n else " "
        can_close = not left.isspace() and stack
        can_open = not right.isspace()
        flush()

        def close_top():
            nonlocal bold, italic
            top = stack.pop()
            if top == "b":
                bold = False
            else:
                italic = False

        while cnt > 0:
            if can_close and not can_open:
                need = 2 if stack and stack[-1] == "b" else 1
                if stack and cnt >= need:
                    cnt -= need
                    close_top()
                    continue
                break
            if can_open and not can_close:
                if cnt >= 2 and not bold:
                    stack.append("b"); bold = True; cnt -= 2
                elif cnt >= 1 and not italic:
                    stack.append("i"); italic = True; cnt -= 1
                else:
                    break
                continue
            # flush on both sides: prefer closing what is open
            if italic and stack and stack[-1] == "i":
                close_top(); cnt -= 1
            elif cnt >= 2 and bold and stack and stack[-1] == "b":
                close_top(); cnt -= 2
            elif cnt >= 2 and not bold:
                stack.append("b"); bold = True; cnt -= 2
            elif cnt >= 1 and not italic:
                stack.append("i"); italic = True; cnt -= 1
            else:
                break
        buf.extend("*" * cnt)  # unmatched leftovers stay literal
        i = j
    flush()
    return runs


def parse_book_md(path: Path) -> list[Block]:
    blocks: list[Block] = []
    cur: Block | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = ANCHOR_RE.match(raw)
        if m:
            pages = []
            for part in m.group("pages").split(","):
                if "-" in part:
                    a, b = part.split("-")
                    pages.extend(range(int(a), int(b) + 1))
                else:
                    pages.append(int(part))
            cur = Block(int(m.group("id")), pages, float(m.group("y0")),
                        float(m.group("y1")), m.group("kind"), "")
            blocks.append(cur)
        elif cur is not None and raw.strip():
            cur.md = (cur.md + "\n" + raw) if cur.md else raw
    return blocks
