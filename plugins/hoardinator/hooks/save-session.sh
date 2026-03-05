#!/usr/bin/env bash
# save-session.sh - PreCompact hook
# Auto-ingests the current session into Supabase before context compaction.
# Exits silently on any failure or missing prerequisites.

input=$(cat)
project_dir=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null)
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null)

if [ -z "$project_dir" ]; then exit 0; fi
if [ -z "$transcript_path" ]; then exit 0; fi
if [ ! -f "$transcript_path" ]; then exit 0; fi
if [ -z "${SUPABASE_ACCESS_TOKEN:-}" ] || [ -z "${SUPABASE_PROJECT_REF:-}" ]; then exit 0; fi

session_id=$(basename "$transcript_path" .jsonl)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

output_dir="/tmp/hoardinator-sql/"
mkdir -p "$output_dir"

if python3 "$PLUGIN_ROOT/scripts/parse-sessions.py" \
    --session "$session_id" \
    --project-dir "$project_dir" \
    --output "$output_dir" \
    2>/tmp/hoardinator-debug.log; then

  if bash "$PLUGIN_ROOT/scripts/upload-sessions.sh" \
      --input "$output_dir" \
      2>>/tmp/hoardinator-debug.log; then

    summary_file="${output_dir}summary.json"
    msg_count=0
    if [ -f "$summary_file" ]; then
      msg_count=$(jq '.total_messages // 0' "$summary_file" 2>/dev/null || echo 0)
    fi
    echo "Hoardinator: saved ${msg_count} messages from this session."
  fi
fi

rm -rf "$output_dir"
exit 0
