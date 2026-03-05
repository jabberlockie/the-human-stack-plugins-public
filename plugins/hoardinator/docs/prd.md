# Session Hoardinator — PRD

> **Status**: Draft
> **Author**: thehumanstack + Claude
> **Date**: 2026-02-23
> **Plugin**: `hoardinator` (standalone plugin)

---

## Problem Statement

Claude Code sessions generate rich JSONL transcripts — every user prompt, AI response, thinking block, tool call, and result — but this data **disappears after the session ends**. There's no way to answer: "How efficient am I?", "Where do tools fail most?", "Is the AI's reasoning improving?", or "Are my habits changing over time?" Without structured ingestion, each session starts from zero. The learning loop is broken.

## Goals

1. **Ingest** all Claude Code JSONL session transcripts into a normalized, queryable schema
2. **Classify** every message (user text, assistant response, thinking, tool results) and every tool call (category, success, security flags)
3. **Namespace** all data by repo/org/author/environment so one database serves all projects
4. **Close the learning loop** — SessionStart queries past learnings, PreCompact saves new ones
5. **Enable analytics** — tool failure rates, thinking patterns, efficiency trends, security audit trails

## Non-Goals

- **Real-time streaming** — ingestion is on-demand (`/log`) or batch (`/ingest`), not live
- **Embedding generation** — the module ingests structured data; embedding is a separate concern (OpenAI API dependency)
- **UI/dashboard** — analytics are consumed via SQL queries, not a built-in frontend
- **Subagent transcript parsing** — Phase 1 covers main session files only; subagent JSONL is Phase 2
- **PII scrubbing** — content is stored as-is; access control is handled via Supabase RLS

---

## Architecture

### Database: Supabase (pgvector-enabled)

Single Supabase project serves all repos. Data is namespaced, not siloed.

### Four-Table Schema

#### `sessions` — One row per conversation

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial PK | |
| `session_id` | text UNIQUE | UUID from JSONL filename |
| `repo` | text | e.g. `jabberlockie/AI-Readiness-and-Digital-Health-Diagnostic` |
| `org` | text | e.g. `jabberlockie` |
| `author` | text | git config user.name |
| `app_name` | text | project identifier |
| `environment` | text | `codespace`, `local`, `replit` |
| `claude_version` | text | e.g. `"2.1.50"` |
| `model` | text | primary model used (e.g. `"claude-opus-4-6"`) |
| `session_date` | date | |
| `first_message_at` | timestamptz | |
| `last_message_at` | timestamptz | |
| `total_messages` | int | all message rows (text + thinking + tool_result + system) |
| `total_user_messages` | int | user text messages only |
| `total_assistant_messages` | int | assistant text messages only |
| `total_thinking_blocks` | int | thinking messages |
| `total_tool_results` | int | tool_result messages |
| `total_system_events` | int | system event messages |
| `total_tool_calls` | int | tool invocations |
| `total_failures` | int | tool calls where `success = false` |
| `total_rejections` | int | tool calls where `was_rejected = true` |
| `total_input_tokens` | int | sum of input_tokens across all assistant messages |
| `total_output_tokens` | int | sum of output_tokens |
| `total_cache_read_tokens` | int | sum of cache_read_input_tokens |
| `total_cache_creation_tokens` | int | sum of cache_creation_input_tokens |
| `total_thinking_chars` | int | total chars in thinking blocks |
| `app_tool_calls` | int | tool calls for app work |
| `infra_tool_calls` | int | tool calls for git/npm/infra |
| `compaction_count` | int | how many times context was compressed |
| `has_continuation` | bool | resumed from a prior session |
| `agents_used` | text[] | e.g. `{Explore, feature-dev:code-architect}` |
| `plugins_used` | text[] | e.g. `{supabase, playwright}` |
| `skills_used` | text[] | e.g. `{commit, feature-dev}` |
| `git_branches` | text[] | all branches active during session |
| `permission_modes` | text[] | all permission modes used |
| `models_used` | text[] | all models used (e.g. `{claude-opus-4-6, claude-haiku-4-5}`) |
| `security_flags` | text[] | e.g. `{destructive_command, user_rejection}` |
| `sensitive_files_touched` | int | |
| `destructive_commands` | int | |
| `ingested` | bool | |
| `ingested_at` | timestamptz | |

#### `messages` — One row per conversational unit

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial PK | |
| `session_id` | text FK | |
| `message_index` | int | ordering within session |
| `role` | text | `user`, `assistant`, or `system` |
| `message_type` | text | `text`, `thinking`, `tool_result`, `system`, `compaction_summary` |
| `content` | text | truncated to 2000 chars |
| `thinking_length` | int | char count of full thinking block (NULL for non-thinking) |
| `model` | text | model that generated this message (assistant only) |
| `input_tokens` | int | from `message.usage.input_tokens` |
| `output_tokens` | int | from `message.usage.output_tokens` |
| `cache_read_tokens` | int | from `message.usage.cache_read_input_tokens` |
| `cache_creation_tokens` | int | from `message.usage.cache_creation_input_tokens` |
| `permission_mode` | text | active permission mode at time of message |
| `git_branch` | text | active branch at time of message |
| `is_compaction_summary` | bool | true if this is a compaction summary |
| `tool_use_id` | text | for tool_result messages: links to the tool_use that produced this |
| `is_error` | bool | for tool_result messages: whether the result was an error |
| `intent_category` | text | future: classify user intent |
| `response_type` | text | future: classify response type |
| `files_referenced` | text[] | file paths mentioned in text |
| `skills_invoked` | text[] | skills referenced |
| `tool_call_count` | int | tools triggered by this message |
| `tool_failure_count` | int | failed tools from this message |
| `created_at` | timestamptz | |

**Unique constraint**: `(session_id, message_index)`

#### `tool_calls` — One row per tool invocation

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial PK | |
| `session_id` | text FK | |
| `message_id` | int FK | which message triggered this (nullable) |
| `call_index` | int | ordering within session |
| `tool_name` | text | e.g. `Bash`, `Read`, `mcp__plugin_supabase_supabase__execute_sql` |
| `tool_category` | text | `file`, `bash`, `agent`, `plugin`, `skill`, `web`, `interaction`, `todo`, `tool_search`, `other` |
| `input_summary` | text | truncated input description |
| `output_summary` | text | truncated output |
| `success` | bool | NULL if no result received |
| `was_rejected` | bool | user rejected the tool call |
| `was_revision` | bool | retry of a previous failed call |
| `error_type` | text | `rejected`, `exit_code`, `permission`, `not_found`, `other` |
| `error_message` | text | truncated error |
| `exit_code` | int | for Bash commands |
| `target_file` | text | file path operated on |
| `target_domain` | text | URL domain for web tools |
| `is_background` | bool | `run_in_background: true` |
| `is_agent` | bool | Task tool call |
| `agent_type` | text | e.g. `Explore`, `feature-dev:code-architect` |
| `plugin_name` | text | e.g. `supabase`, `playwright` |
| `is_sensitive_file` | bool | `.env`, credentials, keys |
| `has_secret_exposure` | bool | secret patterns in output |
| `is_destructive` | bool | `rm -rf`, `DROP`, `--force` |
| `was_blocked_by_hook` | bool | hook prevented execution |
| `security_flags` | text[] | array of all flags |
| `caller_type` | text | `direct` or `agent` (from `tool_use.caller.type`) |
| `was_interrupted` | bool | user interrupted tool execution |
| `was_truncated` | bool | output was truncated |
| `agent_id` | text | for agent tool calls: the agent instance ID |
| `agent_tokens` | int | tokens consumed by agent (`totalTokens`) |
| `agent_tool_count` | int | tools used by agent (`totalToolUseCount`) |
| `agent_duration_ms` | int | agent execution time (`totalDurationMs`) |
| `background_task_id` | text | for background Bash/Task calls |
| `result_duration_ms` | int | execution duration from `toolUseResult.durationMs` |
| `duration_ms` | int | estimated from timestamps |
| `repo` | text | namespace |
| `org` | text | namespace |
| `session_date` | date | denormalized for partitioning |
| `created_at` | timestamptz | |

#### `session_embeddings` — Classified learnings (existing)

Unchanged from current schema. Five-layer classification (user/product/project/plan/task) with pgvector HNSW index. Fed by PreCompact hook, queried by SessionStart hook.

---

## JSONL Record Type Mapping

| JSONL `type` | `content[].type` | Maps to | `message_type` |
|-------------|-----------------|---------|----------------|
| `user` | string content | `messages` | `text` |
| `user` | `tool_result` | `messages` | `tool_result` |
| `assistant` | `text` | `messages` | `text` |
| `assistant` | `thinking` | `messages` | `thinking` |
| `assistant` | `tool_use` | `tool_calls` | — |
| `system` | — | `messages` | `system` |
| `system` | compaction | `messages` | `compaction_summary` |
| `progress` | — | skipped (hook/bash progress) | — |
| `file-history-snapshot` | — | skipped | — |
| `queue-operation` | — | skipped | — |

---

## Distribution

Session Hoardinator ships as a standalone plugin installable via `/plugin install`.

## Plugin Components

### Hooks (architect plugin)

#### `SessionStart` — Query past learnings
```bash
#!/bin/bash
# Derives namespace from git remote
REPO=$(git -C "$CLAUDE_PROJECT_DIR" remote get-url origin 2>/dev/null | sed 's|.*github.com[:/]||;s|\.git$||')
ORG=$(echo "$REPO" | cut -d'/' -f1)
# Outputs instructions for Claude to query session_embeddings via Supabase MCP
```

#### `PreCompact` — Save learnings before compression
```bash
#!/bin/bash
# Same namespace derivation
# Outputs instructions for Claude to classify and INSERT learnings into session_embeddings
```

### Skills (architect plugin)

#### `/log` — Log the current session

Primary in-session command. User says `/log` (or "log this session") and the current conversation is ingested immediately.

**How it works:**
1. Identify the current session's JSONL file (`~/.claude/projects/<project-hash>/<session-id>.jsonl`)
2. Parse it using the embedded parser (Python script or inline logic)
3. Check if session already exists in DB → incremental or full insert
4. Generate dollar-quoted SQL, upload via Supabase Management API
5. Report: "Logged: 47 messages, 32 tool calls, 5 thinking blocks"

**Incremental behavior:** If the session is already partially ingested (e.g., user ran `/log` mid-session and again later), only new messages are uploaded.

#### `/ingest` — Batch sweep all sessions

Daily/weekly sweep command. User opens Claude Code and runs `/ingest` to process all local sessions.

**How it works:**
1. Scan `~/.claude/projects/` for all `.jsonl` files across all projects
2. Query DB for already-ingested sessions (`SELECT session_id, last_message_at FROM sessions WHERE repo = :repo`)
3. For each local session: skip if current, delta-ingest if partially ingested, full-ingest if new
4. Filter out empty sessions (0 messages, 0 tool calls)
5. Generate batched SQL (40 stmts/file), upload via Management API
6. Report summary: "Ingested: 12 new, 3 updated, 8 skipped (current), 5 skipped (empty)"

**Scope options:**
- `/ingest` — all sessions for the current repo
- `/ingest all` — all sessions across all repos/projects on this machine
- `/ingest 2026-02-23` — sessions from a specific date

#### `/hoardinator:query` — Quick analytics
Pre-built queries: tool failure rates, efficiency trends, security audit, thinking patterns, session comparison.

#### `/hoardinator:status` — Check ingestion state
Shows which local sessions are ingested vs pending, total row counts, last ingestion timestamp.

### Agents (architect plugin)

#### `hoardinator:parser` — JSONL parsing agent
Reads JSONL files and extracts structured data. Handles:
- Linked-list traversal via `parentUuid` → `uuid`
- Tool use → tool result matching via `tool_use_id`
- Security detection (destructive patterns, sensitive files, secret exposure)
- Tool classification (10 categories)
- Duration estimation from timestamp pairs
- Empty session filtering

### Parser Implementation

The parser is a Python script bundled with the architect plugin at `plugins/architect/scripts/parse-sessions.py`. It is invoked by the `/log` and `/ingest` skills via Bash.

**Key algorithms:**
1. **Linked-list traversal**: JSONL records are linked via `parentUuid` → `uuid`. Parser builds a dict of `{uuid: record}`, finds the root (no parentUuid), then walks the chain to establish message ordering.
2. **Tool use → tool result matching**: Each `tool_use` block has an `id`. The next `user` record contains `tool_result` blocks with matching `tool_use_id`. Parser pairs these to determine success/failure and extract result metadata.
3. **Content block splitting**: A single assistant record may contain multiple content blocks (text + thinking + tool_use). Each becomes a separate row in `messages` or `tool_calls`.
4. **Dollar-quoting**: All string content is escaped using PostgreSQL `$content$...$content$` syntax, avoiding all issues with markdown, shell output, and nested quotes.
5. **Batching**: Output is split into files of 40 INSERT statements each to stay under Supabase API payload limits.

**Invocation:**
```bash
# Log current session
python3 /path/to/parse-sessions.py --session <session-id> --output /tmp/hoardinator-sql/

# Batch sweep
python3 /path/to/parse-sessions.py --output /tmp/hoardinator-sql/

# Dry run (no SQL files, just counts)
python3 /path/to/parse-sessions.py --dry-run
```

---

## Namespace Strategy

All data is namespaced — one Supabase project serves every repo. Namespace is derived at runtime from `git remote get-url origin`:

```
git remote → github.com:thehumanstackteam/AI-Readiness-and-Digital-Health-Diagnostic.git
            ├── repo: thehumanstackteam/AI-Readiness-and-Digital-Health-Diagnostic
            ├── org:  thehumanstackteam
            └── author: (from git config user.name)
```

Cross-repo queries use `org` filter. Per-repo queries use `repo` filter.

---

## Incremental Ingestion

Every JSONL record has a `uuid` and `timestamp`, and every ingested message has a `message_index`. This enables delta ingestion — only new messages are uploaded, not the entire session.

### Detection

```sql
SELECT session_id, last_message_at, total_messages, total_tool_calls
FROM sessions
WHERE repo = :repo
```

Compare against the local JSONL file: if the local session has more records than `total_messages + total_tool_calls`, or its latest timestamp exceeds `last_message_at`, new content exists.

### Three Scenarios

| Local State | DB State | Action |
|---|---|---|
| Session not in DB | — | Full INSERT (all messages, tool_calls, session row) |
| Session in DB, same counts | `last_message_at` matches | **Skip** — already current |
| Session in DB, more messages locally | Local timestamp > DB `last_message_at` | **Delta INSERT** for messages with `message_index > max_ingested_index`, then UPDATE session aggregates |

### Delta Logic

1. Parser reads the full JSONL file (messages are ordered by `message_index`)
2. Query DB for `MAX(message_index)` and `MAX(call_index)` for that session
3. Generate INSERT statements only for records beyond those indexes
4. Generate a single UPDATE on `sessions` to refresh aggregates (`total_messages`, `total_tool_calls`, `last_message_at`, token counts, etc.)

### Benefits

- **Idempotent re-runs**: Running `/hoardinator:ingest` twice on the same data produces zero duplicates
- **Live session support**: Can ingest a session that's still active — new messages appear on next run
- **Reduced upload volume**: Only changed sessions produce SQL; unchanged sessions are skipped entirely
- **Compaction-safe**: Compacted sessions may have fewer JSONL records but higher `message_index` values — the index-based approach handles this correctly

---

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| SQL escaping | Dollar-quoting (`$$..$$`) | Standard escaping breaks on markdown, shell output, nested quotes |
| Batch size | 40 statements per file | Stays under Supabase API payload limits |
| Upload transport | curl with `json.dump` to temp file, `-d @file` | Avoids OS argument length limits that break `jq --arg` |
| Vector storage | pgvector (not Vector Buckets) | Tiny dataset, sub-100K vectors, needs low latency. Vector Buckets are alpha and optimized for millions. |
| Thinking blocks | Stored as `message_type = 'thinking'`, content truncated, full length in `thinking_length` | Enables reasoning analytics without bloating storage |
| Tool result content | Stored as `message_type = 'tool_result'` in messages | Connects tool outputs to the conversation flow |
| Session hook pattern | Hooks output instructions → Claude acts via Supabase MCP | No API keys in hooks, no standalone scripts, uses existing MCP auth |

---

## Security

- **RLS policies**: `service_role` (full CRUD), `authenticated` (read), `anon` (read)
- **Secret detection**: Regex patterns for API keys, tokens, Bearer headers flagged in `has_secret_exposure`
- **Destructive command detection**: `rm -rf`, `DROP`, `--force`, `git reset --hard` flagged in `is_destructive`
- **Sensitive file detection**: `.env`, `.pem`, `.key`, credentials, tokens flagged in `is_sensitive_file`
- **No secrets in hooks**: Hooks emit text instructions; authentication happens via Supabase MCP (already configured)

---

## Phasing

### Phase 1 — Core (prototype complete, packaging needed)
- [x] 3-table schema (sessions, messages, tool_calls) with indexes and RLS
- [x] JSONL parser with tool classification and security detection
- [x] Batched upload via Supabase Management API
- [x] SessionStart hook (query learnings)
- [x] PreCompact hook (save learnings)
- [x] Empty session filtering
- [x] Thinking block extraction (`message_type = 'thinking'`)
- [x] Tool result extraction (`message_type = 'tool_result'`)
- [ ] Incremental ingestion (delta detect via `message_index` + `last_message_at`)
- [ ] `/log` skill — log current session from within a conversation
- [ ] `/ingest` skill — batch sweep all local sessions
- [ ] Bundle parser script into architect plugin (`plugins/architect/scripts/parse-sessions.py`)
- [ ] Upload script into architect plugin (`plugins/architect/scripts/upload-sessions.sh`)
- [ ] Publish via architect marketplace update

### Phase 2 — Enhanced Analytics
- [ ] `/hoardinator:query` skill with pre-built analytics
- [ ] `/hoardinator:status` skill (ingestion state overview)
- [ ] Intent classification for user messages (ask/command/debug/review/explore)
- [ ] Response type classification (explanation/code/question/error)
- [ ] Subagent transcript parsing (read JSONL from `subagents/` dirs)
- [ ] Compaction detection (count compaction events per session)

### Phase 3 — Learning Loop Improvements
- [ ] Embedding generation (OpenAI text-embedding-3-small) for session_embeddings
- [ ] Semantic search across sessions via pgvector
- [ ] Auto-classify learnings from session content (not just PreCompact)
- [ ] Cross-repo pattern detection (what works in repo A that could help repo B)

### Phase 4 — Automation
- [ ] Auto-ingest hook on session end (PostToolUse or SessionEnd event)
- [ ] Dashboard queries accessible via architect context
- [ ] Efficiency scoring: sessions rated by outcome/effort ratio
- [ ] Scheduled daily sweep (cron or CI-triggered)

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Sessions ingested | 100% of non-empty sessions | `SELECT count(*) FROM sessions WHERE ingested` |
| Tool failure rate trend | Decreasing week-over-week | `GROUP BY session_date` on `success = false` |
| User rejection rate | < 5% of tool calls | `was_rejected = true / total` |
| Ingestion reliability | 0 failed uploads | upload script exit codes |
| Time-to-insight | < 30 seconds from `/hoardinator:query` | wall clock |

---

## Appendix A: Complete JSONL Property Reference

### Top-Level Record Types

Every line in a `.jsonl` session file is a JSON object with a `type` field. Six record types exist:

#### `type: user` — Human messages and tool results

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"user"` |
| `uuid` | string | Unique ID for this record |
| `parentUuid` | string | Links to previous record (linked-list ordering) |
| `sessionId` | string | Session UUID |
| `timestamp` | string | ISO 8601 |
| `cwd` | string | Working directory at time of message |
| `gitBranch` | string | Active git branch |
| `version` | string | Claude Code version (e.g. `"2.1.50"`) |
| `slug` | string | Human-readable session slug (appears after first tool use) |
| `userType` | string | Always `"external"` |
| `isSidechain` | bool | Whether this is a sidechain message |
| `permissionMode` | string | `"default"`, `"plan"`, etc. (only on text messages) |
| `isCompactSummary` | bool | True if this is a compaction summary |
| `isMeta` | bool | System meta-message |
| `isVisibleInTranscriptOnly` | bool | Not shown in UI |
| `message.role` | string | Always `"user"` |
| `message.content` | string \| array | String = user typed text. Array = tool results |
| `toolUseResult` | string \| dict \| list | Structured result from tool (see below) |
| `sourceToolAssistantUUID` | string | UUID of the assistant record that triggered this tool |
| `sourceToolUseID` | string | ID of the tool_use block that triggered this result |

#### `type: assistant` — AI responses

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"assistant"` |
| `uuid` | string | Unique ID |
| `parentUuid` | string | Links to previous record |
| `sessionId` | string | Session UUID |
| `timestamp` | string | ISO 8601 |
| `requestId` | string | API request ID (e.g. `"req_011CY..."`) |
| `cwd` | string | Working directory |
| `gitBranch` | string | Active branch |
| `version` | string | Claude Code version |
| `slug` | string | Session slug |
| `userType` | string | Always `"external"` |
| `isSidechain` | bool | Sidechain message |
| `isApiErrorMessage` | bool | True if this is an API error |
| `message.model` | string | Model used (e.g. `"claude-opus-4-6"`) |
| `message.id` | string | API message ID |
| `message.role` | string | Always `"assistant"` |
| `message.content` | array | Array of content blocks (see below) |
| `message.stop_reason` | string \| null | `"end_turn"`, `"tool_use"`, etc. |
| `message.usage` | object | Token counts (input, output, cache) |

#### `type: progress` — Hook and bash progress events

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"progress"` |
| `uuid` | string | Unique ID |
| `parentUuid` | string \| null | May be null for first record |
| `parentToolUseID` | string | Tool use ID this progress relates to |
| `toolUseID` | string | Progress event ID |
| `data.type` | string | `"hook_progress"` or `"bash_progress"` |
| `data.hookEvent` | string | Hook event name (for hook_progress) |
| `data.hookName` | string | Hook identifier |
| `data.command` | string | Hook command |
| `data.output` | string | Incremental output (for bash_progress) |
| `data.fullOutput` | string | Complete output so far |
| `data.elapsedTimeSeconds` | int | Time elapsed |
| `data.totalLines` | int | Lines of output |
| `data.totalBytes` | int | Bytes of output |
| `data.taskId` | string | Background task ID |

#### `type: system` — System events (compaction, hooks, errors)

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"system"` |
| `uuid` | string | Unique ID |
| `parentUuid` | string \| null | |
| `subtype` | string | Event subtype |
| `content` | string | System message text |
| `level` | string | Log level |
| `isMeta` | bool | Meta-message flag |
| `compactMetadata` | object | Compaction details (token counts, duration) |
| `stopReason` | string | Why execution stopped |
| `preventedContinuation` | bool | Whether continuation was blocked |
| `hookCount` | int | Number of hooks executed |
| `hookInfos` | array[object] | Hook execution details |
| `hookErrors` | array | Hook error details |
| `durationMs` | int | Event duration |
| `hasOutput` | bool | Whether event produced output |
| `logicalParentUuid` | string | Logical parent (may differ from parentUuid) |
| `toolUseID` | string | Related tool use |

#### `type: queue-operation` — Background task queue events

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"queue-operation"` |
| `operation` | string | `"enqueue"`, `"dequeue"`, `"remove"` |
| `timestamp` | string | ISO 8601 |
| `sessionId` | string | Session UUID |
| `content` | string | JSON string with task details (`task_id`, `tool_use_id`, `description`, `task_type`) |

#### `type: file-history-snapshot` — File backup snapshots

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"file-history-snapshot"` |
| `messageId` | string | Associated message UUID |
| `isSnapshotUpdate` | bool | Whether this updates an existing snapshot |
| `snapshot.messageId` | string | Message UUID |
| `snapshot.trackedFileBackups` | object | Map of file paths to backup content |
| `snapshot.timestamp` | string | ISO 8601 |

---

### Content Block Types (inside `message.content[]`)

#### `type: text` — Visible text output

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"text"` |
| `text` | string | The text content |

#### `type: thinking` — Internal reasoning (not shown to user)

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"thinking"` |
| `thinking` | string | Full reasoning text |
| `signature` | string | Cryptographic signature of thinking block |

#### `type: tool_use` — Tool invocation

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"tool_use"` |
| `id` | string | Unique tool use ID (matches `tool_result.tool_use_id`) |
| `name` | string | Tool name (e.g. `"Bash"`, `"Read"`, `"mcp__plugin_supabase_supabase__execute_sql"`) |
| `input` | object | Tool-specific input parameters |
| `caller` | object | `{type: "direct"}` or `{type: "agent", ...}` |

#### `type: tool_result` — Tool execution result (inside user records)

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"tool_result"` |
| `tool_use_id` | string | Matches `tool_use.id` |
| `content` | string \| array | Result text or structured content |
| `is_error` | bool | Whether execution failed |

---

### `toolUseResult` Shapes (top-level on user records)

The `toolUseResult` field appears on user records that contain tool results. It has **three possible shapes**:

**Shape 1: String** — Simple status (e.g. `"User rejected tool use"`)

**Shape 2: Dict** — Structured result with tool-specific fields:

| Property | Type | Present On | Description |
|----------|------|-----------|-------------|
| `stdout` | string | Bash | Standard output |
| `stderr` | string | Bash | Standard error |
| `interrupted` | bool | Bash | User interrupted execution |
| `isImage` | bool | Bash, Read | Output contains image data |
| `noOutputExpected` | bool | Bash | Command not expected to produce output |
| `filePath` | string | Read, Write, Edit | Target file path |
| `numLines` | int | Read | Lines read |
| `numFiles` | int | Glob | Files matched |
| `filenames` | array | Glob | Matched file paths |
| `matches` | array | Grep | Search matches |
| `content` | string \| array | Multiple | Result content |
| `oldString` | string | Edit | Original text |
| `newString` | string | Edit | Replacement text |
| `replaceAll` | bool | Edit | Whether all occurrences replaced |
| `structuredPatch` | array | Edit | Diff patch data |
| `originalFile` | string \| null | Edit | Original file content |
| `userModified` | bool | Edit | User modified the edit |
| `success` | bool | Multiple | Operation succeeded |
| `message` | string | Multiple | Status message |
| `status` | string | Multiple | Status string |
| `mode` | string | Permission | Permission mode |
| `answers` | object | AskUserQuestion | User's answers |
| `questions` | array | AskUserQuestion | Questions asked |
| `description` | string | Task | Task description |
| `agentId` | string | Task | Agent identifier |
| `isAsync` | bool | Task | Background agent |
| `outputFile` | string | Task | Agent output file path |
| `backgroundTaskId` | string | Bash (bg) | Background task ID |
| `canReadOutputFile` | bool | Bash (bg) | Output file readable |
| `persistedOutputPath` | string | Bash (bg) | Output file location |
| `persistedOutputSize` | int | Bash (bg) | Output file size |
| `retrieval_status` | string | TaskOutput | `"success"` or `"error"` |
| `taskId` | string | TaskOutput | Task being retrieved |
| `totalDurationMs` | int | Task | Agent total duration |
| `totalTokens` | int | Task | Tokens consumed by agent |
| `totalToolUseCount` | int | Task | Tools used by agent |
| `commandName` | string | Skill | Skill that was invoked |
| `query` | string | ToolSearch | Search query |
| `total_deferred_tools` | int | ToolSearch | Tools found |
| `appliedLimit` | int | Grep | Line limit applied |
| `truncated` | bool | Multiple | Output was truncated |
| `durationMs` | int | Multiple | Execution duration |
| `returnCodeInterpretation` | string | Bash | Exit code meaning |
| `statusChange` | object | TaskUpdate | Task fields changed |
| `updatedFields` | array | TaskUpdate | Field names updated |
| `task` | object | TaskGet | Full task details |
| `tasks` | array | TaskList | All tasks |
| `file` | object | Write | Written file info |
| `prompt` | string | WebFetch | Fetch prompt |
| `usage` | object | Multiple | Token usage details |

**Shape 3: Array[Dict]** — Multiple results (rare, from multi-tool calls)

---

## Open Questions

| Question | Owner | Notes |
|----------|-------|-------|
| How to handle the repo namespace mismatch (fork `jabberlockie/` vs upstream `thehumanstackteam/`)? | Engineering | Hook derives from git remote — need a canonical mapping or accept both |
| Auto-ingest trigger: PostToolUse hook on session end, or manual `/ingest`? | Product | Auto is cleaner but adds overhead to every session |
| Supabase project: shared with other plugins or dedicated? | Infrastructure | Current: shared `hdhmwaldvzxwhimoemap`. Namespacing makes sharing safe. |

### Resolved

| Question | Decision |
|----------|----------|
| Should `tool_result` content be stored in `messages`? | **Yes** — stored as `message_type = 'tool_result'` with `tool_use_id` linking back to the tool call |
| Should thinking content be stored or just the length? | **Both** — content truncated to 2000 chars in `content`, full char count in `thinking_length` |
