#!/usr/bin/env python3
"""UserPromptSubmit hook: auto-ground Armenian-language prompts in the KB.

Detects Armenian Unicode (U+0530..U+058F) in the user's prompt; if
found, runs `frequency/query_kb.py` and emits the resulting bundle
as additional context (Claude Code injects hook stdout into the
model's view of the prompt).

This enforces the CLAUDE.md rule "Before answering an Armenian-
language question, grep the KB first." Without this hook the rule
is suggestion-strength prose; with the hook the bundle is in
context whether the model remembers to look or not.

Suppression knobs:
  - Skipped if the prompt has no Armenian characters.
  - Skipped if the prompt is longer than MAX_PROMPT_CHARS (likely a
    paste of file content rather than a question).
  - Skipped if the prompt looks like a meta-instruction about the
    workspace itself rather than a content question (heuristic on
    leading verbs).
  - To disable for a specific prompt, prefix it with `#nogrep`.

Exits 0 on every path. Failures (timeout, query_kb.py crash) are
silent — the model still answers, just without the auto-bundle.

Place at `.claude/hooks/armenian_autoground.py` and reference from
`.claude/settings.json` under `hooks.UserPromptSubmit`.
"""
import json
import os
import re
import subprocess
import sys

ARMENIAN_RANGE = re.compile(r'[԰-֏]')
MAX_PROMPT_CHARS = 3000
QUERY_KB_TIMEOUT_SECONDS = 30
SUPPRESS_TOKEN = "#nogrep"

META_PROMPT_PATTERNS = [
    re.compile(r'^\s*(commit|push|pull|merge|rebase|stash|amend)\b', re.IGNORECASE),
    re.compile(r'^\s*(read|show|cat|edit|write|run|fix)\s+(the\s+)?[a-z_./-]+\.(md|py|tsv|jsonl|sh|json|yaml|yml)\b', re.IGNORECASE),
]


def repo_root():
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def should_skip(prompt):
    if SUPPRESS_TOKEN in prompt:
        return True
    if not ARMENIAN_RANGE.search(prompt):
        return True
    if len(prompt) > MAX_PROMPT_CHARS:
        return True
    if any(pat.search(prompt) for pat in META_PROMPT_PATTERNS):
        return True
    return False


def run_query_kb(root, prompt):
    script = os.path.join(root, 'frequency', 'query_kb.py')
    if not os.path.isfile(script):
        return None
    try:
        result = subprocess.run(
            ['python3', script, prompt],
            capture_output=True,
            text=True,
            timeout=QUERY_KB_TIMEOUT_SECONDS,
            cwd=root,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    prompt = payload.get('prompt', '') or ''
    if should_skip(prompt):
        return

    root = repo_root()
    bundle = run_query_kb(root, prompt)
    if not bundle:
        return

    print("<system-reminder>")
    print("Armenian content detected in this prompt. The KB lookup")
    print("below was auto-run via the `armenian-autoground` hook")
    print("(`.claude/hooks/armenian_autoground.py`).")
    print()
    print("**Ground your answer in this bundle** — quote citations,")
    print("mark uncited claims as project-knowledge, name gaps. See")
    print("`CLAUDE.md` § 'Before answering an Armenian-language")
    print("question'. To skip the auto-grounding for a specific")
    print("prompt, prefix it with `#nogrep`.")
    print("</system-reminder>")
    print()
    print(bundle)


if __name__ == '__main__':
    main()
