#!/bin/bash
# docs/architect/hooks/ingest-session.sh
# Wrapper script to ingest session into pgvector
# Called by other hooks or manually via /architect log

set -e

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CONTEXT_DIR="$PROJECT_ROOT/docs/architect/context"

# Parse arguments
SESSION_PATH="$1"
TRIGGER="${2:-manual}"
COMMIT_HASH="$3"

# Validate session path format (alphanumeric, slashes, dots, hyphens, underscores only)
if [[ ! "$SESSION_PATH" =~ ^[/a-zA-Z0-9._-]+$ ]]; then
    echo "Invalid session path format: $SESSION_PATH"
    exit 1
fi

# Validate trigger value
if [[ ! "$TRIGGER" =~ ^(precompact|plan_approved|commit|manual)$ ]]; then
    echo "Invalid trigger: $TRIGGER"
    echo "  Valid triggers: precompact, plan_approved, commit, manual"
    exit 1
fi

# Validate commit hash format if provided (hex only)
if [ -n "$COMMIT_HASH" ] && [[ ! "$COMMIT_HASH" =~ ^[a-fA-F0-9]+$ ]]; then
    echo "Invalid commit hash format: $COMMIT_HASH"
    exit 1
fi

# Validate
if [ -z "$SESSION_PATH" ]; then
    echo "Usage: ingest-session.sh <session-path> [trigger] [commit-hash]"
    echo "  trigger: precompact, plan_approved, commit, manual"
    exit 1
fi

if [ ! -f "$SESSION_PATH" ]; then
    echo "Session file not found: $SESSION_PATH"
    exit 1
fi

# Check for required environment variables
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY not set, skipping ingestion"
    exit 0
fi

if [ -z "$DATABASE_URL" ]; then
    echo "Warning: DATABASE_URL not set, skipping ingestion"
    exit 0
fi

# Run the TypeScript ingestion script
cd "$PROJECT_ROOT"

if command -v npx &> /dev/null; then
    npx ts-node "$CONTEXT_DIR/ingest.ts" "$SESSION_PATH" "$TRIGGER" "$COMMIT_HASH"
else
    echo "npx not found, cannot run ingestion"
    exit 1
fi
