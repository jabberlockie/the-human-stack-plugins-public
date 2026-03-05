---
name: log
description: >
  Log the current Claude Code session to Supabase. Parses the active JSONL
  transcript, generates SQL, and uploads it. Supports incremental updates for
  sessions already partially ingested. Use for "/log", "log this session",
  "save session to database".
---

# Log Session

Parse the current session's JSONL transcript, generate dollar-quoted SQL, and
upload to Supabase. Supports full and incremental ingestion.

## Prerequisites

Before doing anything, verify:

1. `python3` is available: `which python3`. If missing, HALT and tell the user.
2. `SUPABASE_ACCESS_TOKEN` is set: `echo $SUPABASE_ACCESS_TOKEN | head -c4`. If empty, HALT: "Set SUPABASE_ACCESS_TOKEN to run /log."
3. `SUPABASE_PROJECT_REF` is set: `echo $SUPABASE_PROJECT_REF | head -c4`. If empty, HALT: "Set SUPABASE_PROJECT_REF to run /log."

## Step 1: Identify the Current Session JSONL

The session ID is available from the conversation context. JSONL files live at
`~/.claude/projects/<project-hash>/<session-id>.jsonl`.

To find the right file:

1. List all `.jsonl` files under `~/.claude/projects/`:
   ```bash
   find ~/.claude/projects/ -name '*.jsonl' -type f
   ```
2. Match by session ID if known. Otherwise, pick the most recently modified
   `.jsonl` file:
   ```bash
   find ~/.claude/projects/ -name '*.jsonl' -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-
   ```
3. Extract the session ID from the filename (strip the `.jsonl` extension and
   parent path). Also resolve the project directory from the file path.

Store these for later steps:
- `SESSION_ID` -- the UUID
- `JSONL_PATH` -- full path to the file
- `PROJECT_DIR` -- the `<project-hash>` directory containing the file

## Step 2: Check for Incremental State

Query Supabase for existing session data to determine if this is a fresh
ingestion or an incremental update:

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT session_id, last_message_at, total_messages, total_tool_calls FROM sessions WHERE session_id = '"'"'<SESSION_ID>'"'"'"}'
```

Three scenarios:

| DB State | Action |
|----------|--------|
| No row returned | Full ingestion -- all messages and tool calls |
| Row exists, counts match local | Skip -- session already current. Report and stop. |
| Row exists, local has more | Incremental -- pass existing state to the parser |

If incremental, build a JSON string keyed by session_id with the DB values:
```
--incremental '{"<SESSION_ID>":{"last_message_at":"<ts>","total_messages":<n>,"total_tool_calls":<n>}}'
```

## Step 3: Run the Parser

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-sessions.py \
  --session <SESSION_ID> \
  --output /tmp/hoardinator-sql/ \
  --project-dir <PROJECT_DIR>
```

If incremental state was found in Step 2, append the flag:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-sessions.py \
  --session <SESSION_ID> \
  --output /tmp/hoardinator-sql/ \
  --project-dir <PROJECT_DIR> \
  --incremental '{"<SESSION_ID>":{"last_message_at":"...","total_messages":N,"total_tool_calls":N}}'
```

The parser uses stdlib-only Python. No pip install needed.

If the parser exits non-zero, report the error and HALT.

If the parser reports an empty session (0 messages, 0 tool calls), report
"Session is empty -- nothing to log." and stop.

## Step 4: Run the Uploader

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/upload-sessions.sh \
  --input /tmp/hoardinator-sql/
```

This requires `SUPABASE_ACCESS_TOKEN` and `SUPABASE_PROJECT_REF` environment
variables (verified in Prerequisites).

The uploader sends batched SQL files (40 statements per file) to the Supabase
Management API. Dollar-quoted SQL handles all content safely -- markdown, shell
output, nested quotes.

If the uploader exits non-zero, report the error and HALT.

## Step 5: Report Results

Read `/tmp/hoardinator-sql/summary.json` for counts.

**Full ingestion:** Report:
```
Logged: X messages, Y tool calls, Z thinking blocks
```

**Incremental update:** Report:
```
Updated: +X new messages, +Y new tool calls
```

**Skipped (already current):** Report:
```
Session already logged and up to date.
```

Include the session ID in the report so the user can reference it.

## Technical Notes

- Sessions are namespaced by repo/org/author derived from `git remote get-url origin`
- Dollar-quoted SQL (`$content$...$content$`) avoids all escaping issues
- Batched uploads (40 statements per file) stay under Supabase API payload limits
- Empty sessions (0 messages, 0 tool calls) are skipped automatically
- Incremental ingestion uses `message_index` and `call_index` to detect deltas -- running `/log` twice on the same session produces zero duplicates
- The parser handles linked-list traversal (`parentUuid` -> `uuid`), tool use/result matching, thinking block extraction, and security flag detection

## What This Skill Does NOT Do

- Batch-sweep all sessions (use `/ingest` for that)
- Query analytics (use `/status` for that)
- Parse subagent transcripts (future work)
