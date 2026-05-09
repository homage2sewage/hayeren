---
name: error-log
description: |
  Build / refresh the indices for the structured LLM-failure log
  at `errors/`. Walks every error file, parses YAML frontmatter,
  emits `errors/INDEX.md` (chronological) and
  `errors/BY-CATEGORY.md` (grouped). Run after adding a new
  error file. See `errors/README.md` for the schema.
---

# error-log

Auto-generates two index files from `errors/`. The error log
itself is the durable inventory of LLM-failure cases this
project has seen — see `errors/README.md` for the schema, the
tiered logging rule, and the categorisation guide.

## When to invoke

- After adding a new error file (`errors/YYYY-MM-DD-NNN.md`).
- After editing an existing entry's frontmatter (status,
  severity, mitigation).
- Periodically — quarterly or so — to refresh the indices and
  surface stale `status: open` entries.

## How to invoke

```sh
python3 .claude/skills/error-log/build_index.py
```

Writes (overwriting):

- `errors/INDEX.md` — chronological table (id, date, category,
  severity, status, summary).
- `errors/BY-CATEGORY.md` — grouped by category, then
  subcategory.

Both files start with a generated-by header so a human reader
knows not to hand-edit them.

## Failure modes

- Frontmatter parse errors → script reports the offending file
  and exits non-zero.
- Missing required fields → flagged in the index with `[?]`
  placeholders, not silently dropped.
- Pre-existing INDEX.md / BY-CATEGORY.md content → overwritten
  unconditionally; these are auto-generated, not authored.

## Cross-references

- `errors/README.md` — schema and rules of the log.
- `llm-workflow.md` — broader hygiene principles.
- `kb-design.md` — agent-flow design where the error log fits
  next to walks and topics.
