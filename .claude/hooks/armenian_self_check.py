#!/usr/bin/env python3
"""Stop hook: post-emit verification of Armenian-content claims.

After the model finishes generating a draft response, this hook:

1. Detects Armenian Unicode (U+0530..U+058F) in the response.
2. Skips if the response has no / too little Armenian content.
3. Runs `frequency/query_kb.py` on the Armenian-bearing lines.
4. If the bundle has substantive matches (topic files or book
   passages), BLOCKS the response with the bundle as feedback,
   forcing the model to reconcile its claims with corpus
   evidence before re-emitting.

This is the post-emit mirror of `armenian_autoground.py` (which
runs on `UserPromptSubmit` to inject the bundle BEFORE the model
sees the prompt). Together they form the verification layer the
operator has been providing manually all session.

See `research/2026-05-26-pre-emit-verification-automation.md` for
design rationale.

Anti-loop guard: payload's `stop_hook_active` field signals the
hook has already fired in this turn. If true, the hook returns
silently — the second-attempt response is allowed through whether
or not it aligns with the bundle. This prevents infinite blocking.

Suppression knobs:
  - Skipped if the response contains the literal `#nocheck` token.
  - Skipped if Armenian-character count is below MIN_ARMENIAN_CHARS
    (response is just a passing mention, not analysis).
  - Skipped if the response is longer than MAX_RESPONSE_CHARS
    (likely a deck dump or other bulk emission).
  - Skipped if `stop_hook_active` is set in the payload.

Exits 0 on every path. Failures (timeout, query_kb crash) are
silent — the response goes through whether or not verification
succeeds.

Place at `.claude/hooks/armenian_self_check.py` and reference from
`.claude/settings.json` under `hooks.Stop`.
"""
import json
import os
import re
import subprocess
import sys
import time

ARMENIAN_RANGE = re.compile(r'[԰-֏]')
MIN_ARMENIAN_CHARS = 20
MAX_RESPONSE_CHARS = 50000
QUERY_KB_TIMEOUT_SECONDS = 30
SUPPRESS_TOKEN = "#nocheck"
LOG_FILENAME = ".claude/logs/armenian_self_check.jsonl"


def repo_root():
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def extract_armenian_content(text):
    """Pull lines from a response that carry substantive Armenian.

    Threshold: a line must have at least 3 Armenian characters to
    count; this filters out passing mentions while keeping cited
    forms, examples, glosses, and analysis-prose.
    """
    if not text:
        return ""
    lines_with_armenian = [
        line for line in text.split('\n')
        if len(ARMENIAN_RANGE.findall(line)) >= 3
    ]
    return '\n'.join(lines_with_armenian)


def should_skip(payload, response):
    if payload.get('stop_hook_active'):
        return True
    if SUPPRESS_TOKEN in response:
        return True
    if not response:
        return True
    armenian_chars = len(ARMENIAN_RANGE.findall(response))
    if armenian_chars < MIN_ARMENIAN_CHARS:
        return True
    if len(response) > MAX_RESPONSE_CHARS:
        return True
    return False


def run_query_kb(root, query):
    script = os.path.join(root, 'frequency', 'query_kb.py')
    if not os.path.isfile(script):
        return None
    try:
        result = subprocess.run(
            ['python3', script, query],
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


def bundle_has_matches(bundle):
    """Heuristic for whether the bundle is worth surfacing to
    the model. Looks for actual hit counts ('N match(es)' or
    'N hit(s)') rather than the 'no matches' placeholders.
    """
    if not bundle:
        return False
    # Count meaningful hit markers
    hit_markers = (
        bundle.count('match(es)') +
        bundle.count('hit)') +
        bundle.count('hits)')
    )
    return hit_markers >= 2


def extract_response_from_payload(payload):
    """Pull the assistant's draft response out of the hook payload.

    Claude Code's Stop-hook payload shape isn't a stable public
    contract, so try several reasonable keys and fall back to a
    string scan as a last resort.
    """
    for key in ('response', 'message', 'content', 'assistant_message'):
        v = payload.get(key)
        if isinstance(v, str) and v:
            return v
    # If payload has a list of messages, take the last assistant one
    messages = payload.get('messages') or []
    for msg in reversed(messages):
        if isinstance(msg, dict) and msg.get('role') == 'assistant':
            content = msg.get('content', '')
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                texts = [c.get('text', '') for c in content if isinstance(c, dict)]
                return '\n'.join(texts)
    return ''


def log_activation(root, payload, response_len, armenian_chars, action, bundle_summary):
    """Append a single-line jsonl record so we can measure
    hook firings without disturbing the model."""
    log_path = os.path.join(root, LOG_FILENAME)
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "stop_hook_active": payload.get('stop_hook_active', False),
                "response_chars": response_len,
                "armenian_chars": armenian_chars,
                "action": action,
                "bundle": bundle_summary,
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    response = extract_response_from_payload(payload)
    root = repo_root()

    if should_skip(payload, response):
        log_activation(root, payload, len(response),
                       len(ARMENIAN_RANGE.findall(response)),
                       "skip", "")
        return

    armenian_content = extract_armenian_content(response)
    if not armenian_content:
        log_activation(root, payload, len(response),
                       len(ARMENIAN_RANGE.findall(response)),
                       "skip-no-armenian-lines", "")
        return

    bundle = run_query_kb(root, armenian_content)
    if not bundle or not bundle_has_matches(bundle):
        log_activation(root, payload, len(response),
                       len(ARMENIAN_RANGE.findall(response)),
                       "pass-no-corpus-matches",
                       (bundle or '')[:200])
        return

    feedback = (
        "<system-reminder>\n"
        "Armenian content was detected in your draft response. The "
        "KB lookup below was auto-run via the `armenian-self-check` "
        "hook (`.claude/hooks/armenian_self_check.py`).\n\n"
        "**Reconcile your claims with this bundle** before "
        "re-emitting. If your analysis aligns with the corpus "
        "citations, you can proceed. If your claims disagree with, "
        "extend beyond, or assert what the corpus doesn't support, "
        "revise the response or explicitly flag the gap (e.g., "
        "'the four-book corpus doesn't cover this register'). "
        "See `research/2026-05-26-pre-emit-verification-automation.md` "
        "for design rationale.\n\n"
        "To skip self-check for a specific response, include the "
        "token `#nocheck` in the response prose. Note: this hook "
        "fires only once per turn (anti-loop guard via "
        "`stop_hook_active`).\n"
        "</system-reminder>\n\n"
    )
    output = {
        "decision": "block",
        "reason": feedback + bundle
    }

    log_activation(root, payload, len(response),
                   len(ARMENIAN_RANGE.findall(response)),
                   "block",
                   bundle[:300])

    print(json.dumps(output))


if __name__ == '__main__':
    main()
