# Hoardinator

Ingest Claude Code JSONL session transcripts into normalized Supabase tables
for analytics and learning loop closure.

## What It Does

Every Claude Code session generates a JSONL transcript. Hoardinator parses
those transcripts and stores them in three Supabase tables: `sessions`,
`messages`, and `tool_calls`. This enables analytics like tool failure rates,
token trends, efficiency patterns, and security audit trails.

## Setup

### 1. Supabase Project

Tables must exist in your Supabase project. See `docs/prd.md` for the full
schema definition.

### 2. Environment Variables

Add these to your shell profile:

```bash
export SUPABASE_ACCESS_TOKEN="your-personal-access-token"
export SUPABASE_PROJECT_REF="your-project-ref"
```

- **Access token**: https://supabase.com/dashboard/account/tokens
- **Project ref**: the alphanumeric ID in your Supabase project URL

### 3. Verify

Start a Claude Code session and run `/hoardinator:status`.

## Commands

| Command | Purpose |
|---------|---------|
| `/hoardinator:log` | Log the current session (incremental) |
| `/hoardinator:ingest` | Batch-sweep sessions for current repo |
| `/hoardinator:ingest all` | Batch-sweep all repos |
| `/hoardinator:ingest 2026-02-23` | Sessions from a specific date |
| `/hoardinator:status` | Show ingestion stats and recent sessions |

## Automatic Hooks

Two hooks run automatically when credentials are configured:

- **SessionStart**: Shows a one-line status if the current project has
  prior ingested sessions.
- **PreCompact**: Auto-ingests the current session before context
  compaction so no data is lost.

Both degrade silently if env vars are not set.

## Credentials

All operations use the Supabase Management API. One credential pair:

| Variable | Purpose |
|----------|---------|
| `SUPABASE_ACCESS_TOKEN` | Personal access token |
| `SUPABASE_PROJECT_REF` | Project reference ID |

## Schema

Three tables, one Supabase project serves all repos (namespaced by git remote):

- `sessions` -- one row per conversation
- `messages` -- one row per message unit (text, thinking, tool_result, system)
- `tool_calls` -- one row per tool invocation (10 categories)
