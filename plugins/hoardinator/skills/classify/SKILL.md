---
name: classify
description: >
  Send text, a transcript, or any content to The Hoardinator's classification
  router. Returns flags (jtbd, story, deal, etc.), a 2-sentence summary,
  action items, memories, and best quotes. Use for "/classify", "classify this",
  "what flags does this have", "route this content".
---

# Classify Input

Send arbitrary text or content to The Hoardinator's classification router
(classify-input Edge Function). Returns structured intelligence: flags,
summary, action items, memories, and best quotes.

## Prerequisites

- `SUPABASE_PROJECT_REF` environment variable set (hdhmwaldvzxwhimoemap)
- `SUPABASE_ACCESS_TOKEN` or `SUPABASE_ANON_KEY` environment variable set
- Content to classify (pasted text, a file, or the current conversation context)

## Step 1: Determine What to Classify

Accept content from:
- **Explicit argument**: `/classify <text>` — use the provided text directly
- **Clipboard/file**: If user says "classify this file" or pastes content, use that
- **Current context**: If no argument, summarize what's being discussed and classify it

## Step 2: Create an Input Record

First insert the content into `public.inputs` so the classifier can process it:

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "INSERT INTO public.inputs (type, status, data) VALUES ('\''note'\'', '\''ingested'\'', '\''{\"source_type\": \"manual\", \"content\": \"<ESCAPED_CONTENT>\"}'\''::jsonb) RETURNING id"
  }'
```

Capture the returned `id` as `INPUT_ID`.

## Step 3: Call classify-input Edge Function

```bash
curl -s -X POST \
  "https://${SUPABASE_PROJECT_REF}.supabase.co/functions/v1/classify-input" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"input_id\": \"${INPUT_ID}\"}"
```

The response includes:
```json
{
  "classified_id": "ops_clsf_XXXXX",
  "flags": ["jtbd", "story", "action-item"],
  "summary": "Two-sentence summary of what was classified."
}
```

## Step 4: Fetch Full Classification

To get the full structured output (action items, memories, quotes):

```bash
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"SELECT data FROM classified WHERE id = '${CLASSIFIED_ID}'\"}"
```

## Step 5: Report Results

Present to the user:

```
## Classification Results

**Summary:** <2-sentence summary>

**Flags:** jtbd, story, action-item (+ N others)

**Action Items:**
- [ ] <task> (@owner)

**Memories Captured:**
- <person>: <durable fact>

**Best Quotes:**
> "<quote>" — <speaker>

**Classified ID:** ops_clsf_XXXXX (stored in Hoardinator)
```

## Important Notes

- Content is stored permanently in Supabase after classification
- `action-item` flags automatically create dispatch_queue entries for downstream agents
- The classifier uses 25 flags: jtbd, story, quote, deal, outreach, proposal, asset-needed,
  idea, framework, expert, product-gap, pricing, market, channel, memory, permission,
  action-item, coaching, delivery, partnership, and others
