#!/usr/bin/env python3
"""Fixture-replay tests for the Armenian grounding hooks.

Run: python3 .claude/hooks/test_hooks.py
No third-party deps. Never touches the real `.claude/logs/`:
both hooks honor ARMENIAN_HOOK_LOG_DIR, which is pointed at a
temp dir. `frequency/query_kb.py` is never invoked: both hooks
honor ARMENIAN_HOOK_KB_STUB (path to a canned bundle).

The transcript fixture copies the schema observed in real session
transcripts (CC v2.1.x, 2026-06): one JSON object per line; an
assistant turn is split across several lines sharing `message.id`,
one line per content block (thinking / text / tool_use).
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
SELF_CHECK = os.path.join(HOOKS_DIR, 'armenian_self_check.py')
AUTOGROUND = os.path.join(HOOKS_DIR, 'armenian_autoground.py')

# A stub bundle that bundle_has_matches must treat as substantive:
# two `match(es)` topic-hit headers plus a book-passage header.
BUNDLE_WITH_MATCHES = """\
# KB bundle for: ...

## Matched topic files

### `topics/lexicon/yerevan_slang.md` — 2 match(es): `խոտ`, `արա`

## Matched project notes

### `armenian-grammar.md` — 1 match(es): `գալ`

## Matched book passages

### ghamoyan

**p 48** (1 passage)

## Gaps — query lemmas with no KB coverage

*(none — every query lemma has at least one KB hit)*
"""

# A stub bundle with only no-coverage placeholders.
BUNDLE_NO_MATCHES = """\
# KB bundle for: ...

## Matched topic files

*(no topic files matched)*

## Matched project notes

*(no project notes matched)*

## Matched book passages

*(no book passages matched)*

## Gaps — query lemmas with no KB coverage

`foo`, `bar`
"""

ARMENIAN_UNCITED = (
    "Here is my analysis of the line.\n"
    "Բարև ձեզ, այս բառը նշանակում է մի բան որ կապված է խոսակցական "
    "ռեգիստրի հետ։\n"
    "Երկրորդ տողը նույնպես հայերեն է և բավական երկար է ստուգման համար։\n"
    "So the gloss is probably 'grass' in the literal sense."
)

ARMENIAN_CITED = (
    "Here is my analysis of the line.\n"
    "Բարև ձեզ, այս բառը նշանակում է մի բան որ կապված է խոսակցական "
    "ռեգիստրի հետ։\n"
    "Երկրորդ տողը նույնպես հայերեն է և բավական երկար է ստուգման համար։\n"
    "Per topics/lexicon/yerevan_slang.md and ghamoyan p48 [#3], the "
    "gloss is 'naive / clueless person'."
)

# Cited draft whose QUOTED Armenian fragment IS at the cited page.
CITED_VERIFIED = (
    "Here is my analysis of the line.\n"
    "Բարև ձեզ, այս բառը խոսակցական ռեգիստրի հետ կապված է և բավական երկար։\n"
    "The slang `խոտ` means 'naive / clueless person' (ghamoyan p48)."
)

# Cited draft whose QUOTED fragment is NOT at the cited page — the
# documented wrong-book song fabrication (errors/2026-06-01-001):
# `կուսական` is parnasyan p383, absent from sakayan.
CITED_FABRICATED = (
    "Here is my analysis of the line.\n"
    "Բարև ձեզ, այս բառը խոսակցական ռեգիստրի հետ կապված է և բավական երկար։\n"
    "The word «կուսական» means 'virginal' — sakayan p383."
)

# Regression for the span-boundary false positive (found by the verify
# subagents 2026-06-13): a MULTIWORD Armenian phrase that is split across
# token-granular spans on a clean page (`Հայաստան\nհայ` on sakayan p31).
# A byte-exact match against the `\n`-joined page text would wrongly block
# it; the whitespace-insensitive match must let it pass.
CITED_MULTIWORD = (
    "Here is my analysis of the line.\n"
    "Բարև ձեզ, այս բառը խոսակցական ռեգիստրի հետ կապված է և բավական երկար։\n"
    "The phrase `Հայաստան հայ` appears in the vocabulary (sakayan p31)."
)

# Cited IPA respelling that IS on the cited dumtragut page (p42 has the
# bracketed IPA [mɑɾtʰ] for մարդ). dumtragut has a clean text layer, so
# its Armenian + IPA are byte-verifiable.
CITED_IPA_VERIFIED = (
    "Here is my analysis of the line.\n"
    "Բարև ձեզ, այս բառը խոսակցական ռեգիստրի հետ կապված է և բավական երկար։\n"
    "The word «մարդ» devoices to [mɑɾtʰ] (dumtragut p42)."
)

# Fabricated IPA respelling: [mɑɾt] omits the aspiration the page shows
# ([mɑɾtʰ]) — a wrong respell must block at emit time.
CITED_IPA_FABRICATED = (
    "Here is my analysis of the line.\n"
    "Բարև ձեզ, այս բառը խոսակցական ռեգիստրի հետ կապված է և բավական երկար։\n"
    "The word «մարդ» is pronounced [mɑɾt] (dumtragut p42)."
)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_transcript(path, response_text, session_id="test-session"):
    """Write a transcript JSONL with the real schema: meta lines, a
    user line, a mid-conversation assistant turn (thinking + text +
    tool_use sharing one message id), the FINAL assistant turn split
    across two lines sharing another id, and a trailing sidechain
    assistant line that must be ignored."""
    common = {"isSidechain": False, "sessionId": session_id,
              "cwd": "/home/alexey/work/hayeren", "version": "2.1.172",
              "gitBranch": "main", "userType": "external"}

    def aline(mid, block, **over):
        rec = dict(common)
        rec.update({"type": "assistant", "requestId": "req_" + mid,
                    "uuid": "uuid-" + mid + "-" + block.get("type", "?"),
                    "message": {"id": mid, "type": "message",
                                "role": "assistant", "model": "claude-x",
                                "content": [block],
                                "stop_reason": None, "usage": {}}})
        rec.update(over)
        return rec

    half = len(response_text) // 2
    lines = [
        {"type": "mode", "mode": "normal", "sessionId": session_id},
        {"type": "file-history-snapshot", "messageId": "m0",
         "snapshot": {}, "isSnapshotUpdate": False},
        dict(common, type="user", uuid="u1",
             message={"role": "user", "content": "ինչ է նշանակում խոտ"}),
        # earlier assistant turn — must NOT leak into extraction
        aline("msg_early", {"type": "thinking", "thinking": "hmm"}),
        aline("msg_early", {"type": "text",
                            "text": "EARLIER TURN — must not be extracted"}),
        aline("msg_early", {"type": "tool_use", "id": "tu1",
                            "name": "Bash", "input": {"command": "ls"}}),
        dict(common, type="user", uuid="u2",
             message={"role": "user",
                      "content": [{"type": "tool_result",
                                   "tool_use_id": "tu1", "content": "ok"}]}),
        # final assistant turn, text split across two lines (same id)
        aline("msg_final", {"type": "thinking", "thinking": "thinking..."}),
        aline("msg_final", {"type": "text", "text": response_text[:half]}),
        aline("msg_final", {"type": "text", "text": response_text[half:]}),
        # sidechain noise after the final turn — must be ignored
        aline("msg_side", {"type": "text", "text": "SIDECHAIN — ignore me"},
              isSidechain=True),
    ]
    with open(path, 'w', encoding='utf-8') as f:
        for rec in lines:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def run_hook(script, payload, env_extra):
    env = dict(os.environ)
    env.update(env_extra)
    proc = subprocess.run(
        ['python3', script], input=json.dumps(payload),
        capture_output=True, text=True, env=env, timeout=60)
    return proc


def last_log(log_dir_path, filename):
    path = os.path.join(log_dir_path, filename)
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    return json.loads(lines[-1]) if lines else None


FAILURES = []


def check(name, cond, detail=""):
    status = "ok" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def test_citation_regex():
    print("citation regex (skip-cited discriminator)")
    sc = load_module(SELF_CHECK, 'sc')
    cited = [
        "per topics/lexicon/yerevan_slang.md line 114",
        "see ghamoyan p48 [#3]",
        "attested in sakayan p. 132 and elsewhere",
        "Parnasyan p 7 has the paradigm",
        "tioyan\tp12",  # whitespace variant
        "cf. topics/grammar/2026-05-09-aorist-stems.md for the stems",
        "ACHARYAN P.45 (capitalised cite)",
    ]
    uncited = [
        ARMENIAN_UNCITED,
        "the topics/ directory has a file for this",          # bare dir
        "see page 48 of the slang dictionary",                # no book name
        "ghamoyan has an entry for this somewhere",           # book, no page
        "the p48 form is colloquial",                         # page, no book
        "I ran frequency/query_kb.py and got nothing",        # script path
        "look in cards/top_1000.tsv row 7",                   # non-topic path
        "Ghamoyan published in 2009",                         # book + year, no pN
    ]
    for s in cited:
        check(f"cited matches: {s[:48]!r}", sc.is_already_cited(s))
    for s in uncited:
        check(f"uncited does not match: {s[:48]!r}",
              not sc.is_already_cited(s))


def test_bundle_has_matches():
    print("bundle_has_matches")
    sc = load_module(SELF_CHECK, 'sc2')
    check("substantive bundle -> True",
          sc.bundle_has_matches(BUNDLE_WITH_MATCHES))
    check("placeholder-only bundle -> False",
          not sc.bundle_has_matches(BUNDLE_NO_MATCHES))
    check("empty bundle -> False", not sc.bundle_has_matches(""))


def stop_payload(transcript_path, **over):
    p = {"session_id": "test-session",
         "transcript_path": transcript_path,
         "hook_event_name": "Stop",
         "stop_hook_active": False,
         "cwd": "/home/alexey/work/hayeren",
         "permission_mode": "default"}
    p.update(over)
    return p


def test_self_check(tmp):
    print("armenian_self_check.py end-to-end")
    logd = os.path.join(tmp, 'logs-sc')
    stub = os.path.join(tmp, 'bundle.md')
    with open(stub, 'w', encoding='utf-8') as f:
        f.write(BUNDLE_WITH_MATCHES)
    env = {"ARMENIAN_HOOK_LOG_DIR": logd, "ARMENIAN_HOOK_KB_STUB": stub}

    # (a) uncited Armenian-rich response -> block
    t_uncited = os.path.join(tmp, 'uncited.jsonl')
    make_transcript(t_uncited, ARMENIAN_UNCITED)
    proc = run_hook(SELF_CHECK, stop_payload(t_uncited), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(a) exit 0", proc.returncode == 0, proc.stderr[:200])
    out = {}
    try:
        out = json.loads(proc.stdout)
    except ValueError:
        pass
    check("(a) stdout decision=block", out.get("decision") == "block",
          proc.stdout[:200])
    check("(a) reason carries bundle", "yerevan_slang" in out.get("reason", ""))
    check("(a) no #nocheck advertisement in feedback",
          "#nocheck" not in out.get("reason", ""))
    check("(a) log action=block", rec and rec.get("action") == "block",
          str(rec))
    check("(a) log response_chars > 0",
          rec and rec.get("response_chars", 0) > 0, str(rec))
    # the two text blocks of msg_final are joined with '\n', hence +1
    check("(a) extraction got full final msg, not earlier turn",
          rec and rec.get("response_chars") == len(ARMENIAN_UNCITED) + 1,
          str(rec))

    # (b) cited but no quoted Armenian fragment to byte-check
    #     -> skip-cited-unverifiable, no block
    t_cited = os.path.join(tmp, 'cited.jsonl')
    make_transcript(t_cited, ARMENIAN_CITED)
    proc = run_hook(SELF_CHECK, stop_payload(t_cited), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(b) exit 0, no stdout", proc.returncode == 0 and not proc.stdout.strip(),
          proc.stdout[:200])
    check("(b) log action=skip-cited-unverifiable",
          rec and rec.get("action") == "skip-cited-unverifiable", str(rec))

    # (e) cited draft whose quoted fragment IS at the cited page
    #     -> pass-citations-verified, no block (verified, not blindly trusted)
    t_ok = os.path.join(tmp, 'cited_ok.jsonl')
    make_transcript(t_ok, CITED_VERIFIED)
    proc = run_hook(SELF_CHECK, stop_payload(t_ok), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(e) verified citation -> exit 0, no block",
          proc.returncode == 0 and not proc.stdout.strip(), proc.stdout[:200])
    check("(e) log action=pass-citations-verified",
          rec and rec.get("action") == "pass-citations-verified", str(rec))

    # (f) cited draft whose quoted fragment is NOT at the cited page
    #     (the song wrong-book fabrication) -> block-citation-unverified
    t_bad = os.path.join(tmp, 'cited_bad.jsonl')
    make_transcript(t_bad, CITED_FABRICATED)
    proc = run_hook(SELF_CHECK, stop_payload(t_bad), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    out = {}
    try:
        out = json.loads(proc.stdout)
    except ValueError:
        pass
    check("(f) fabricated citation -> decision=block",
          out.get("decision") == "block", proc.stdout[:200])
    check("(f) feedback names the bad fragment + page",
          "կուսական" in out.get("reason", "")
          and "sakayan p383" in out.get("reason", ""),
          out.get("reason", "")[:200])
    check("(f) log action=block-citation-unverified",
          rec and rec.get("action") == "block-citation-unverified", str(rec))

    # (g) REGRESSION: multiword phrase split across spans on a clean page
    #     must NOT false-block (whitespace-insensitive match).
    t_mw = os.path.join(tmp, 'cited_multiword.jsonl')
    make_transcript(t_mw, CITED_MULTIWORD)
    proc = run_hook(SELF_CHECK, stop_payload(t_mw), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(g) multiword split phrase -> NOT blocked",
          proc.returncode == 0 and not proc.stdout.strip(), proc.stdout[:200])
    check("(g) log action=pass-citations-verified",
          rec and rec.get("action") == "pass-citations-verified", str(rec))

    # (h) dumtragut IPA respelling that IS on the cited page -> verified.
    #     Guards both the dumtragut-in-VERIFIABLE_BOOKS addition and the
    #     IPA-bracket claim extraction.
    t_ipa = os.path.join(tmp, 'cited_ipa.jsonl')
    make_transcript(t_ipa, CITED_IPA_VERIFIED)
    proc = run_hook(SELF_CHECK, stop_payload(t_ipa), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(h) verified IPA respell -> exit 0, no block",
          proc.returncode == 0 and not proc.stdout.strip(), proc.stdout[:200])
    check("(h) log action=pass-citations-verified",
          rec and rec.get("action") == "pass-citations-verified", str(rec))

    # (i) fabricated IPA respelling ([mɑɾt] vs page's [mɑɾtʰ]) -> block.
    t_ipa_bad = os.path.join(tmp, 'cited_ipa_bad.jsonl')
    make_transcript(t_ipa_bad, CITED_IPA_FABRICATED)
    proc = run_hook(SELF_CHECK, stop_payload(t_ipa_bad), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    out = {}
    try:
        out = json.loads(proc.stdout)
    except ValueError:
        pass
    check("(i) fabricated IPA respell -> decision=block",
          out.get("decision") == "block", proc.stdout[:200])
    check("(i) feedback names the bad IPA fragment",
          "[mɑɾt]" in out.get("reason", ""), out.get("reason", "")[:200])
    check("(i) log action=block-citation-unverified",
          rec and rec.get("action") == "block-citation-unverified", str(rec))

    # (c) stop_hook_active -> skip (anti-loop)
    proc = run_hook(SELF_CHECK,
                    stop_payload(t_uncited, stop_hook_active=True), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(c) exit 0, no stdout", proc.returncode == 0 and not proc.stdout.strip())
    check("(c) log action=skip-stop-hook-active",
          rec and rec.get("action") == "skip-stop-hook-active", str(rec))

    # (d) #nocheck in response -> skip
    t_nocheck = os.path.join(tmp, 'nocheck.jsonl')
    make_transcript(t_nocheck, ARMENIAN_UNCITED + "\n#nocheck")
    proc = run_hook(SELF_CHECK, stop_payload(t_nocheck), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(d) exit 0, no stdout", proc.returncode == 0 and not proc.stdout.strip())
    check("(d) log action=skip-nocheck",
          rec and rec.get("action") == "skip-nocheck", str(rec))

    # extra: missing transcript file -> graceful skip
    proc = run_hook(SELF_CHECK,
                    stop_payload(os.path.join(tmp, 'nope.jsonl')), env)
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(x) missing transcript -> exit 0, skip-no-response",
          proc.returncode == 0 and rec
          and rec.get("action") == "skip-no-response", str(rec))

    # extra: placeholder-only bundle -> pass-no-corpus-matches
    stub_empty = os.path.join(tmp, 'bundle_empty.md')
    with open(stub_empty, 'w', encoding='utf-8') as f:
        f.write(BUNDLE_NO_MATCHES)
    proc = run_hook(SELF_CHECK, stop_payload(t_uncited),
                    {"ARMENIAN_HOOK_LOG_DIR": logd,
                     "ARMENIAN_HOOK_KB_STUB": stub_empty})
    rec = last_log(logd, 'armenian_self_check.jsonl')
    check("(x) placeholder bundle -> pass-no-corpus-matches",
          proc.returncode == 0 and not proc.stdout.strip() and rec
          and rec.get("action") == "pass-no-corpus-matches", str(rec))


def test_autoground(tmp):
    print("armenian_autoground.py end-to-end")
    logd = os.path.join(tmp, 'logs-ag')
    stub = os.path.join(tmp, 'bundle.md')
    with open(stub, 'w', encoding='utf-8') as f:
        f.write(BUNDLE_WITH_MATCHES)
    env = {"ARMENIAN_HOOK_LOG_DIR": logd, "ARMENIAN_HOOK_KB_STUB": stub}

    def payload(prompt):
        return {"session_id": "test-session", "prompt": prompt,
                "hook_event_name": "UserPromptSubmit",
                "cwd": "/home/alexey/work/hayeren"}

    # Armenian prompt fires
    proc = run_hook(AUTOGROUND, payload("ինչ է նշանակում խոտ բառը"), env)
    rec = last_log(logd, 'armenian_autoground.jsonl')
    check("armenian prompt -> exit 0", proc.returncode == 0, proc.stderr[:200])
    check("armenian prompt -> bundle on stdout",
          "yerevan_slang" in proc.stdout, proc.stdout[:200])
    check("armenian prompt -> log action=fired",
          rec and rec.get("action") == "fired", str(rec))
    check("log has required fields",
          rec and all(k in rec for k in
                      ("ts", "action", "prompt_chars", "armenian_chars",
                       "bundle_chars", "duration_ms")), str(rec))
    check("log bundle_chars > 0", rec and rec.get("bundle_chars", 0) > 0)

    # #nogrep prefix skips (also with leading whitespace)
    for p in ("#nogrep ինչ է նշանակում խոտ", "  #nogrep ինչ է նշանակում խոտ"):
        proc = run_hook(AUTOGROUND, payload(p), env)
        rec = last_log(logd, 'armenian_autoground.jsonl')
        check(f"prefix {p[:12]!r}... -> no stdout", not proc.stdout.strip(),
              proc.stdout[:120])
        check(f"prefix {p[:12]!r}... -> log skip-nogrep",
              rec and rec.get("action") == "skip-nogrep", str(rec))

    # token mentioned mid-prompt does NOT skip
    proc = run_hook(
        AUTOGROUND,
        payload("ինչ է նշանակում խոտ — and explain the #nogrep token too"),
        env)
    rec = last_log(logd, 'armenian_autoground.jsonl')
    check("mid-prompt #nogrep -> still fires",
          "yerevan_slang" in proc.stdout
          and rec and rec.get("action") == "fired", str(rec))

    # no Armenian -> skip, logged
    proc = run_hook(AUTOGROUND, payload("plain english prompt"), env)
    rec = last_log(logd, 'armenian_autoground.jsonl')
    check("no armenian -> skip-no-armenian",
          not proc.stdout.strip()
          and rec and rec.get("action") == "skip-no-armenian", str(rec))

    # over-length prompt -> skip, logged (cap is 8000 now)
    proc = run_hook(AUTOGROUND, payload("խոտ " + "x" * 8100), env)
    rec = last_log(logd, 'armenian_autoground.jsonl')
    check("(>8000 chars) -> skip-too-long",
          rec and rec.get("action") == "skip-too-long", str(rec))

    # ~7k chars (old cap was 3000) -> fires
    proc = run_hook(AUTOGROUND,
                    payload(("խոտ արա ինչ է նշանակում " * 280)[:7000]), env)
    rec = last_log(logd, 'armenian_autoground.jsonl')
    check("7k-char Armenian prompt -> fires (cap raised)",
          rec and rec.get("action") == "fired", str(rec))

    # failure path: stub points at nonexistent file -> skip-no-bundle logged
    proc = run_hook(AUTOGROUND, payload("ինչ է նշանակում խոտ"),
                    {"ARMENIAN_HOOK_LOG_DIR": logd,
                     "ARMENIAN_HOOK_KB_STUB": os.path.join(tmp, 'absent.md')})
    rec = last_log(logd, 'armenian_autoground.jsonl')
    check("kb failure -> exit 0 + log skip-no-bundle",
          proc.returncode == 0 and rec
          and rec.get("action") == "skip-no-bundle", str(rec))


def main():
    with tempfile.TemporaryDirectory(prefix="hayeren-hook-tests-") as tmp:
        test_citation_regex()
        test_bundle_has_matches()
        test_self_check(tmp)
        test_autoground(tmp)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s):")
        for name in FAILURES:
            print(f"  - {name}")
        sys.exit(1)
    print("all checks passed")


if __name__ == '__main__':
    main()
