---
name: push
description: >
  Push text or content into The Hoardinator's intelligence pipeline. Creates
  an input record and optionally triggers classification. Use for "/push",
  "push this to Hoardinator", "ingest this note", "send this to the pipeline",
  "store this for later analysis".
---

# Push to Pipeline

Push arbitrary text, notes, or content into The Hoardinator's inputs pipeline.
The content will be stored and can be classified, searched, and routed by
downstream agents.

## Prerequisites

- `SUPABASE_PROJECT_REF` environment variable set (hdhmwaldvzxwhimoemap)
- `SUPABASE_ACCESS_TOKEN` environment variable set

## Step 1: Determine What to Push

Accept content from:
- **Explicit argument**: `/push <text>` — use the provided text
- **Clipboard/paste**: If user pastes content, use that
- **Current conversation context**: Summarize relevant context to push

Also determine input type:
- `note` — general text, observations, ideas (default)
- `call` — meeting/call content with participants
- `slack` — Slack thread or message
- `email` — Email content

## Step 2: Insert into inputs Table

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "INSERT INTO public.inputs (type, status, data) VALUES ('\''<TYPE>'\'', '\''ingested'\'', '\''{\"source_type\": \"manual\", \"content\": \"<ESCAPED_CONTENT>\", \"pushed_from\": \"claude-plugin\"}'\''::jsonb) RETURNING id, created_at"
  }'
```

Capture the returned `id` and `created_at`.

## Step 3: Offer to Classify Immediately

After successful insert, ask the user:

```
Pushed to pipeline. Input ID: <id>

Want me to classify it now? (flags, summary, action items)
```

If yes, invoke the `classify` skill with the input ID (skip steps 1-2 of classify,
jump directly to the classify-input Edge Function call with the existing input ID).

## Step 4: Report Result

```
## Pushed to Hoardinator

**Input ID:** <id>
**Type:** <type>
**Created:** <timestamp>
**Status:** ingested (ready for classification)

Content stored. Use /classify to extract flags and intelligence.
```

## Important Notes

- Status `ingested` means it's in the pipeline but not yet classified
- The auto-classify function processes ingested inputs in batches (if configured)
- Escaped content must have single quotes doubled and special chars handled
- For large content (>10K chars), consider using the `/ingest` skill instead
