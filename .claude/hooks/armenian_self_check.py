#!/usr/bin/env python3
"""Stop hook: post-emit verification of Armenian-content claims.

After the model finishes generating a draft response, this hook:

1. Reads the draft response out of the session transcript
   (`transcript_path` in the Stop payload — the payload itself
   carries no response text). The response is the concatenated
   `text` content blocks of the LAST assistant message in the
   transcript JSONL.
2. Detects Armenian Unicode (U+0530..U+058F) in the response;
   skips if there is no / too little Armenian content.
3. Skips if the response already carries a citation marker
   (a `topics/<...>.md` path or a `<book> pN` cite) — an
   already-grounded draft doesn't need a forced re-read.
4. Runs `frequency/query_kb.py` on the Armenian-bearing lines.
5. If the bundle has substantive matches (topic files or book
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
  - Skipped if the response already contains a citation marker.
  - Skipped if `stop_hook_active` is set in the payload.

Env overrides (used by `.claude/hooks/test_hooks.py`):
  - ARMENIAN_HOOK_LOG_DIR  — directory for the JSONL activation
    log (default: `<repo>/.claude/logs`).
  - ARMENIAN_HOOK_KB_STUB  — path to a file whose contents are
    returned instead of running `frequency/query_kb.py`.

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
LOG_FILENAME = "armenian_self_check.jsonl"

# A draft counts as "already grounded" if it carries either a topic-
# file path or a book-page citation. Anchored tightly so that a mere
# mention of `topics/` or a bare page number does NOT match.
CITATION_RE = re.compile(
    r'topics/[\w\-]+(?:/[\w\-]+)*\.md'
    r'|(?:sakayan|ghamoyan|parnasyan|tioyan|acharyan|gharagyulyan)'
    r'\s+p\.?\s*\d+',
    re.IGNORECASE,
)


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


def skip_reason(payload, response):
    """Return a skip-action string, or None if the check should run."""
    if payload.get('stop_hook_active'):
        return "skip-stop-hook-active"
    if not response:
        return "skip-no-response"
    if SUPPRESS_TOKEN in response:
        return "skip-nocheck"
    armenian_chars = len(ARMENIAN_RANGE.findall(response))
    if armenian_chars < MIN_ARMENIAN_CHARS:
        return "skip-low-armenian"
    if len(response) > MAX_RESPONSE_CHARS:
        return "skip-too-long"
    return None


def is_already_cited(response):
    """Cheap discriminator: the draft already carries a citation
    marker, so the forced re-read would be redundant."""
    return bool(CITATION_RE.search(response))


def run_query_kb(root, query):
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
    """Heuristic for whether the bundle is worth surfacing to the
    model. `query_kb.py` emits `N match(es): ...` headers for topic
    and project-note hits, and `**p N**` headers for book passages;
    the no-coverage placeholders (`*(no topic files matched)*` etc.)
    emit neither marker.
    """
    if not bundle:
        return False
    topic_note_hits = bundle.count('match(es)')
    book_page_hits = len(re.findall(r'^\*\*p \d+\*\*', bundle, re.MULTILINE))
    return (topic_note_hits + book_page_hits) >= 2


def extract_response_from_transcript(transcript_path):
    """Read the last assistant message's text from a Claude Code
    session transcript.

    Transcript schema (observed 2026-06, CC v2.1.x): one JSON object
    per line; assistant output lines look like

        {"type": "assistant", "isSidechain": false,
         "message": {"id": "msg_...", "role": "assistant",
                     "content": [{"type": "text", "text": ...}, ...]},
         ...}

    A single logical assistant turn is split across SEVERAL lines
    sharing `message.id` (one line per content block: thinking /
    text / tool_use). So: iterate the file, group consecutive
    assistant lines by message id, and keep only the text blocks of
    the LAST group. Memory cost is one message's text regardless of
    transcript size; sidechain (subagent) lines are ignored.
    """
    if not transcript_path or not os.path.isfile(transcript_path):
        return None
    last_id = object()  # sentinel that never equals a real id
    texts = []
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '"assistant"' not in line:
                    continue  # cheap pre-filter before json.loads
                try:
                    obj = json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue
                if obj.get('type') != 'assistant' or obj.get('isSidechain'):
                    continue
                msg = obj.get('message') or {}
                if not isinstance(msg, dict):
                    continue
                mid = msg.get('id') or obj.get('requestId') or obj.get('uuid')
                if mid != last_id:
                    last_id = mid
                    texts = []
                content = msg.get('content')
                if isinstance(content, str):
                    if content:
                        texts.append(content)
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'text':
                            t = block.get('text', '')
                            if t:
                                texts.append(t)
    except OSError:
        return None
    if not texts:
        return None
    return '\n'.join(texts)


def extract_response_from_payload(payload):
    """Pull the assistant's draft response out of the hook payload.

    Primary path: the Stop payload carries `transcript_path` (it
    does NOT carry the response text itself); parse the transcript
    JSONL and return the last assistant message's text blocks.

    Fallback: legacy key-probing, kept in case a future payload
    shape embeds the response directly.
    """
    text = extract_response_from_transcript(payload.get('transcript_path'))
    if text:
        return text
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
    log_path = os.path.join(log_dir(root), LOG_FILENAME)
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
    armenian_chars = len(ARMENIAN_RANGE.findall(response))

    reason = skip_reason(payload, response)
    if reason:
        log_activation(root, payload, len(response), armenian_chars, reason, "")
        return

    if is_already_cited(response):
        log_activation(root, payload, len(response), armenian_chars,
                       "skip-cited", "")
        return

    armenian_content = extract_armenian_content(response)
    if not armenian_content:
        log_activation(root, payload, len(response), armenian_chars,
                       "skip-no-armenian-lines", "")
        return

    bundle = run_query_kb(root, armenian_content)
    if not bundle or not bundle_has_matches(bundle):
        log_activation(root, payload, len(response), armenian_chars,
                       "pass-no-corpus-matches",
                       (bundle or '')[:200])
        return

    feedback = (
        "<system-reminder>\n"
        "Armenian content was detected in your draft response, and "
        "the draft carries no corpus citation. The KB lookup below "
        "was auto-run via the `armenian-self-check` hook "
        "(`.claude/hooks/armenian_self_check.py`).\n\n"
        "**Reconcile your claims with this bundle** before "
        "re-emitting. If your analysis aligns with the corpus "
        "citations, cite them and proceed. If your claims disagree "
        "with, extend beyond, or assert what the corpus doesn't "
        "support, revise the response or explicitly flag the gap "
        "(e.g., 'the four-book corpus doesn't cover this register'). "
        "See `research/2026-05-26-pre-emit-verification-automation.md` "
        "for design rationale.\n\n"
        "Note: this hook fires only once per turn (anti-loop guard "
        "via `stop_hook_active`).\n"
        "</system-reminder>\n\n"
    )
    output = {
        "decision": "block",
        "reason": feedback + bundle
    }

    log_activation(root, payload, len(response), armenian_chars,
                   "block",
                   bundle[:300])

    print(json.dumps(output))


if __name__ == '__main__':
    main()
