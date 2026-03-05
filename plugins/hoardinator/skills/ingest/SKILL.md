---
name: ingest
description: >
  Batch-sweep local Claude Code session transcripts to Supabase. Supports three
  scope modes: current repo (default), all repos, or filtered by date. Use for
  "/ingest", "/ingest all", "/ingest 2026-02-23", "upload sessions", "sync sessions".
---

# Ingest Sessions

Batch-sweep local Claude Code JSONL session files, parse them into SQL-ready
payloads, and upload to Supabase. Incremental by default -- only new or updated
sessions are processed.

## Scope Modes

| Invocation            | Scope                              |
|-----------------------|------------------------------------|
| `/ingest`             | All sessions for the current repo  |
| `/ingest all`         | All sessions across all repos      |
| `/ingest 2026-02-23`  | Sessions from a specific date only |

## Prerequisites

- `python3` available in PATH
- `SUPABASE_ACCESS_TOKEN` and `SUPABASE_PROJECT_REF` environment variables set
- `${CLAUDE_PLUGIN_ROOT}/scripts/parse-sessions.py` and
  `${CLAUDE_PLUGIN_ROOT}/scripts/upload-sessions.sh` present

## Step 1: Parse the Argument

Determine scope from the user's argument:

- **No argument** -- current repo only. Resolve `<project-dir>` from the current
  working directory.
- **`all`** -- all repos on this machine. No project-dir filter.
- **Date string (YYYY-MM-DD)** -- current repo, filtered to sessions from that date.

Derive the repo namespace from `git remote get-url origin` in the current working
directory. This is used for the Supabase query in the next step. For `all` mode,
skip namespace resolution.

## Step 2: Query Supabase for Existing Ingestion State

Query the `sessions` table for what has already been ingested:

**For current-repo and date modes:**

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT session_id, last_message_at, total_messages, total_tool_calls FROM sessions WHERE repo = '"'"'<current-repo>'"'"'"}'
```

**For `all` mode:**

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT session_id, last_message_at, total_messages, total_tool_calls FROM sessions"}'
```

Build a JSON object from the results, mapping `session_id` to its state:

```json
{
  "abc123-def456": {
    "last_message_at": "2026-02-23T14:30:00Z",
    "total_messages": 42,
    "total_tool_calls": 18
  }
}
```

If the query returns zero rows, pass an empty object `{}`. This means all
discovered sessions will be treated as new.

## Step 3: Run the Parser in Batch Mode

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-sessions.py \
  --output /tmp/hoardinator-sql/ \
  --project-dir <project-dir> \
  --incremental '<json-from-step-2>'
```

**Variations by scope:**

- **Current repo:** Include `--project-dir <project-dir>`.
- **`all` mode:** Omit `--project-dir` to scan all projects.
- **Date mode:** Add `--date <YYYY-MM-DD>` to filter by date.

Sessions are identified by UUID extracted from the JSONL filename. The parser
compares each session against the incremental JSON to decide:
- **New** -- session_id not in the JSON. Full parse.
- **Updated** -- session_id exists but local file has more messages. Incremental parse.
- **Current** -- session_id exists and counts match. Skip.
- **Empty** -- 0 messages and 0 tool calls. Always skip.

## Step 4: Check the Summary Before Uploading

Read `/tmp/hoardinator-sql/summary.json`. It contains counts of new, updated,
skipped-current, and skipped-empty sessions.

- If all sessions are skipped (0 new, 0 updated), report to the user:
  **"All sessions up to date. Nothing to upload."** Then stop.
- Otherwise, show the user what will be uploaded:
  - Number of new sessions
  - Number of updated sessions
  - Number of skipped sessions (current + empty)
  - Total messages and tool calls to be uploaded

Proceed to upload.

## Step 5: Run the Uploader

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/upload-sessions.sh \
  --input /tmp/hoardinator-sql/
```

Wait for completion. Check the exit code. If the upload fails, report the error
and stop.

## Step 6: Report Summary

Present results to the user in this format:

```
Ingested: X new, Y updated, Z skipped (current), W skipped (empty)
Total: N messages, M tool calls across P sessions
```

Include the scope that was used (repo name, "all repos", or date filter) so the
user knows exactly what was processed.

## Important Notes

- Sessions are identified by UUID from JSONL filename -- not by content hash.
- Incremental ingestion: only new messages are uploaded for partially-ingested
  sessions. The parser uses `last_message_at` and counts to determine the delta.
- Empty sessions (0 messages, 0 tool calls) are always skipped regardless of
  whether they exist in Supabase.
- Namespace is derived from `git remote get-url origin` in the project directory.
- The `/tmp/hoardinator-sql/` directory is used as a staging area. It is
  overwritten on each run.
