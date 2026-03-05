---
name: status
description: >
  Show Hoardinator ingestion status and recent sessions. Use for "/status",
  "hoardinator status", "show ingestion stats", "how many sessions are logged",
  or "what sessions have been ingested".
---

# Status

Show ingestion stats and recent sessions from Supabase.

## Prerequisites

- `SUPABASE_ACCESS_TOKEN` environment variable set
- `SUPABASE_PROJECT_REF` environment variable set

If either is missing, HALT with: "Set SUPABASE_ACCESS_TOKEN and SUPABASE_PROJECT_REF to use /status."

## Step 1: Query Recent Sessions

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT session_id, repo, app_name, total_messages, total_tool_calls, session_date, ingested_at FROM sessions ORDER BY ingested_at DESC LIMIT 10"}'
```

## Step 2: Query Totals

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT COUNT(*) AS sessions, COALESCE(SUM(total_messages), 0) AS messages, COALESCE(SUM(total_tool_calls), 0) AS tool_calls FROM sessions"}'
```

## Step 3: Format Output

```
Hoardinator Status:
  Total sessions: 19
  Total messages: 3,931
  Total tool calls: 2,034

Recent sessions:
  Session                              App           Messages  Tools   Date
  proof-test-xscore-triangle           xscore-sand.  1074      544     2026-02-21
  ...
```

## Schema Reference

- `sessions` -- one row per conversation
- `messages` -- one row per message (text, thinking, tool_result, system)
- `tool_calls` -- one row per tool invocation (10 categories)

Run `/log` to ingest the current session. Run `/ingest` to batch-sweep all sessions.
