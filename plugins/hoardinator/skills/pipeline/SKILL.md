---
name: pipeline
description: >
  Check the Hoardinator intelligence pipeline status. Shows recent
  classifications, queued dispatch items, topic segments, and pipeline
  health. Use for "/pipeline", "pipeline status", "what's in the queue",
  "show recent classifications", "hoardinator status".
---

# Pipeline Status

Query The Hoardinator's intelligence pipeline to show what has been processed,
what's queued, and the overall health of the system.

## Prerequisites

- `SUPABASE_PROJECT_REF` environment variable set (hdhmwaldvzxwhimoemap)
- `SUPABASE_ACCESS_TOKEN` environment variable set

## Queries to Run

Run all queries in parallel for speed.

### 1. Recent Classifications

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT id, type, created_at, data->'\''flags'\'' as flags, data->'\''summary'\'' as summary FROM classified ORDER BY created_at DESC LIMIT 5"
  }'
```

### 2. Dispatch Queue Status

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT type, status, COUNT(*) as count FROM dispatch_queue GROUP BY type, status ORDER BY count DESC LIMIT 15"
  }'
```

### 3. Inputs by Status

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT status, COUNT(*) as count FROM inputs GROUP BY status"
  }'
```

### 4. Topics Created Today

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT COUNT(*) as count, MAX(created_at) as last_created FROM topics WHERE created_at > NOW() - INTERVAL '\''24 hours'\''"
  }'
```

## Report Format

Present results in this format:

```
## Hoardinator Pipeline Status

**Inputs:** X ingested, Y classified, Z pending
**Topics:** N segments created (last: <timestamp>)
**Dispatch Queue:** A queued, B delivered, C failed

**Recent Classifications:**
1. [<type>] <summary> — flags: jtbd, story (+N)
2. ...

**Queue by Type:**
| Flag/Type    | Queued | Delivered |
|--------------|--------|-----------|
| action-item  | 12     | 0         |
| jtbd         | 8      | 0         |
| story        | 5      | 0         |
```

## Important Notes

- The dispatch queue accumulates items when no consumer is processing them
- Items with `status=queued` or `status=pending` are waiting to be processed
- Topics are created by the Digestinator (classify-input → digestinator flow)
- Inputs with `status=ingested` haven't been classified yet
