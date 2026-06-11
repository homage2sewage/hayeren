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
  - To disable for a specific prompt, PREFIX it with `#nogrep`
    (a `#nogrep` mentioned mid-prompt does not suppress).

Every invocation — including every failure path — appends one JSONL
record to `armenian_autoground.jsonl` in the log dir (fields: ts,
action, prompt_chars, armenian_chars, bundle_chars, duration_ms).

Env overrides (used by `.claude/hooks/test_hooks.py`):
  - ARMENIAN_HOOK_LOG_DIR  — directory for the JSONL activation
    log (default: `<repo>/.claude/logs`).
  - ARMENIAN_HOOK_KB_STUB  — path to a file whose contents are
    returned instead of running `frequency/query_kb.py`.

Exits 0 on every path. Failures (timeout, query_kb.py crash) are
silent to the model — it still answers, just without the
auto-bundle — but they are logged.

Place at `.claude/hooks/armenian_autoground.py` and reference from
`.claude/settings.json` under `hooks.UserPromptSubmit`.
"""
import json
import os
import re
import subprocess
import sys
import time

ARMENIAN_RANGE = re.compile(r'[԰-֏]')
MAX_PROMPT_CHARS = 8000
QUERY_KB_TIMEOUT_SECONDS = 30
SUPPRESS_TOKEN = "#nogrep"
LOG_FILENAME = "armenian_autoground.jsonl"

META_PROMPT_PATTERNS = [
    re.compile(r'^\s*(commit|push|pull|merge|rebase|stash|amend)\b', re.IGNORECASE),
    re.compile(r'^\s*(read|show|cat|edit|write|run|fix)\s+(the\s+)?[a-z_./-]+\.(md|py|tsv|jsonl|sh|json|yaml|yml)\b', re.IGNORECASE),
]


def repo_root():
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def log_dir(root):
    env_dir = os.environ.get('ARMENIAN_HOOK_LOG_DIR')
    if env_dir:
        return env_dir
    return os.path.join(root, '.claude', 'logs')


def log_activation(root, action, prompt, bundle, started):
    """Append a single-line jsonl record mirroring the self-check
    hook's log style."""
    log_path = os.path.join(log_dir(root), LOG_FILENAME)
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "action": action,
                "prompt_chars": len(prompt),
                "armenian_chars": len(ARMENIAN_RANGE.findall(prompt)),
                "bundle_chars": len(bundle) if bundle else 0,
                "duration_ms": int((time.monotonic() - started) * 1000),
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass


def skip_reason(prompt):
    """Return a skip-action string, or None if the hook should fire."""
    if prompt.lstrip().startswith(SUPPRESS_TOKEN):
        return "skip-nogrep"
    if not ARMENIAN_RANGE.search(prompt):
        return "skip-no-armenian"
    if len(prompt) > MAX_PROMPT_CHARS:
        return "skip-too-long"
    if any(pat.search(prompt) for pat in META_PROMPT_PATTERNS):
        return "skip-meta-prompt"
    return None


def run_query_kb(root, prompt):
    stub = os.environ.get('ARMENIAN_HOOK_KB_STUB')
    if stub is not None:
        try:
            with open(stub, 'r', encoding='utf-8') as f:
                return f.read()
        except OSError:
            return None
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
    started = time.monotonic()
    root = repo_root()
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        log_activation(root, "skip-bad-payload", "", None, started)
        return
    prompt = payload.get('prompt', '') or ''

    reason = skip_reason(prompt)
    if reason:
        log_activation(root, reason, prompt, None, started)
        return

    bundle = run_query_kb(root, prompt)
    if not bundle:
        log_activation(root, "skip-no-bundle", prompt, None, started)
        return

    log_activation(root, "fired", prompt, bundle, started)

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
