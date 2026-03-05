#!/bin/bash
# docs/architect/hooks/query-context.sh
# Query relevant context from pgvector
# Called by SessionStart hook or manually via /architect context

set -e

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CONTEXT_DIR="$PROJECT_ROOT/docs/architect/context"

# Parse arguments
MODE="${1:-project}"
shift || true

# Check for required environment variables
if [ -z "$OPENAI_API_KEY" ] || [ -z "$DATABASE_URL" ]; then
    # Silently exit if not configured - don't break SessionStart
    exit 0
fi

# Validate DATABASE_URL format (basic check for postgresql scheme)
if [[ ! "$DATABASE_URL" =~ ^postgres(ql)?:// ]]; then
    # Invalid format, silently exit
    exit 0
fi

# Check if context system is initialized (table exists)
# Use stdin to avoid any potential command injection
if ! echo "SELECT 1 FROM session_embeddings LIMIT 1" | psql "$DATABASE_URL" &> /dev/null; then
    # Table doesn't exist yet, silently exit
    exit 0
fi

# Run the TypeScript query script
cd "$PROJECT_ROOT"

if command -v npx &> /dev/null; then
    npx ts-node "$CONTEXT_DIR/query.ts" "$MODE" "$@"
else
    exit 0
fi
