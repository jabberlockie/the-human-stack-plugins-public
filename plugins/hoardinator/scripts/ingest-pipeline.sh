#!/usr/bin/env bash
# Hoardinator Ingest Pipeline - Single-script runner for background agents and cron
# Usage: bash ingest-pipeline.sh [--sessions-dir <path>] [--project-dir <path>] [--date <YYYY-MM-DD>]
#
# Credentials (checked in order):
#   1. SUPABASE_ACCESS_TOKEN env var (already set)
#   2. ~/.config/hoardinator/credentials file
#   3. 1Password CLI (interactive -- requires biometric)
#
# Setup for cron (one-time):
#   mkdir -p ~/.config/hoardinator && chmod 700 ~/.config/hoardinator
#   echo 'SUPABASE_ACCESS_TOKEN=your_token' > ~/.config/hoardinator/credentials
#   echo 'SUPABASE_PROJECT_REF=your_ref' >> ~/.config/hoardinator/credentials
#   chmod 600 ~/.config/hoardinator/credentials
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="/tmp/hoardinator-sql"
CRED_FILE="${HOME}/.config/hoardinator/credentials"

# Parse arguments
SESSIONS_DIR=""
PROJECT_DIR=""
DATE_FILTER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --sessions-dir) SESSIONS_DIR="$2"; shift 2 ;;
    --project-dir) PROJECT_DIR="$2"; shift 2 ;;
    --date) DATE_FILTER="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Step 1: Load credentials (three-tier fallback)
if [[ -n "${SUPABASE_ACCESS_TOKEN:-}" && -n "${SUPABASE_PROJECT_REF:-}" ]]; then
  echo "Credentials loaded from environment."
elif [[ -f "${CRED_FILE}" ]]; then
  # shellcheck source=/dev/null
  source "${CRED_FILE}"
  export SUPABASE_ACCESS_TOKEN SUPABASE_PROJECT_REF
  echo "Credentials loaded from ${CRED_FILE}."
else
  export SUPABASE_ACCESS_TOKEN
  SUPABASE_ACCESS_TOKEN=$(op item get "SUPABASE_HOARDINATOR_ACCESS_TOKEN" --vault "MCP Tokens" --fields credential --reveal 2>/dev/null || true)
  export SUPABASE_PROJECT_REF="hdhmwaldvzxwhimoemap"
  echo "Credentials loaded from 1Password."
fi

if [[ -z "${SUPABASE_ACCESS_TOKEN:-}" ]]; then
  echo "ERROR: No Supabase credentials found."
  echo "Set SUPABASE_ACCESS_TOKEN env var, create ${CRED_FILE}, or configure 1Password CLI."
  exit 1
fi

# Step 2: Query Supabase for existing sessions
echo "Querying Supabase for existing sessions..."
curl -s -X POST \
  "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/database/query" \
  -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT session_id, last_message_at, total_messages, total_tool_calls FROM sessions"}' \
  > /tmp/hoardinator-existing.json

# Build incremental JSON
python3 <<'PYEOF'
import json

with open("/tmp/hoardinator-existing.json") as f:
    data = json.load(f)

rows = data if isinstance(data, list) else data.get("rows", data.get("result", []))
incremental = {}
for row in rows:
    if isinstance(row, dict):
        incremental[row["session_id"]] = {
            "last_message_at": row.get("last_message_at"),
            "total_messages": row.get("total_messages"),
            "total_tool_calls": row.get("total_tool_calls")
        }

with open("/tmp/hoardinator-incremental.json", "w") as f:
    json.dump(incremental, f)

print(f"Found {len(incremental)} existing sessions in Supabase")
PYEOF

# Step 3: Run parser
echo "Running parser..."
PARSER_ARGS=(
  --output "${OUTPUT_DIR}"
  --incremental "$(cat /tmp/hoardinator-incremental.json)"
)

if [[ -n "${SESSIONS_DIR}" ]]; then
  PARSER_ARGS+=(--sessions-dir "${SESSIONS_DIR}")
fi
if [[ -n "${PROJECT_DIR}" ]]; then
  PARSER_ARGS+=(--project-dir "${PROJECT_DIR}")
fi
if [[ -n "${DATE_FILTER}" ]]; then
  PARSER_ARGS+=(--date "${DATE_FILTER}")
fi

python3 "${SCRIPT_DIR}/parse-sessions.py" "${PARSER_ARGS[@]}"

# Step 4: Check summary
if [[ ! -f "${OUTPUT_DIR}/summary.json" ]]; then
  echo "ERROR: No summary.json found after parsing"
  exit 1
fi

echo ""
echo "=== Parse Summary ==="
cat "${OUTPUT_DIR}/summary.json"
echo ""

NEEDS_UPLOAD=$(python3 -c "
import json
with open('${OUTPUT_DIR}/summary.json') as f:
    s = json.load(f)
print('yes' if s.get('new_sessions', 0) + s.get('updated_sessions', 0) > 0 else 'no')
")

if [[ "${NEEDS_UPLOAD}" == "no" ]]; then
  echo "All sessions up to date. Nothing to upload."
  exit 0
fi

# Step 5: Upload
echo "Uploading to Supabase..."
bash "${SCRIPT_DIR}/upload-sessions.sh" --input "${OUTPUT_DIR}"

echo ""
echo "=== Ingestion Complete ==="
cat "${OUTPUT_DIR}/summary.json"
