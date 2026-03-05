#!/usr/bin/env bash
# query-sessions.sh - SessionStart hook
# Shows a one-line status if this project has ingested sessions in Supabase.
# Exits silently if prerequisites are not met.

input=$(cat)
project_dir=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null)

if [ -z "$project_dir" ]; then exit 0; fi
if [ -z "${SUPABASE_ACCESS_TOKEN:-}" ] || [ -z "${SUPABASE_PROJECT_REF:-}" ]; then exit 0; fi

app_name=$(basename "$project_dir" | tr -d "'\"\`")

response=$(curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"SELECT session_id, total_messages, ingested_at FROM sessions WHERE app_name = '${app_name}' ORDER BY ingested_at DESC LIMIT 1\"}" \
  --max-time 8 2>/dev/null)

count=$(echo "$response" | jq 'if type == "array" then length else 0 end' 2>/dev/null)
if [ "${count:-0}" = "0" ] || [ -z "$count" ]; then exit 0; fi

last_date=$(echo "$response" | jq -r '.[0].ingested_at // empty' 2>/dev/null)
total_msgs=$(echo "$response" | jq -r '.[0].total_messages // 0' 2>/dev/null)

if [ -n "$last_date" ]; then
  echo "Hoardinator: last ingested ${last_date} (${total_msgs} messages). Run /status for details."
fi
exit 0
