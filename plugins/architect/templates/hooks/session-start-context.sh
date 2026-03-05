#!/bin/bash
# docs/architect/hooks/session-start-context.sh
# SessionStart hook: loads relevant context from previous sessions
# Outputs context to stdout which becomes part of Claude's system prompt

# Read JSON input from stdin (Claude hook format)
input=$(cat)

# Extract project directory
project_dir=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null)

if [ -z "$project_dir" ]; then
    exit 0
fi

# Check if Architect is initialized
if [ ! -d "$project_dir/docs/architect" ]; then
    exit 0
fi

HOOKS_DIR="$project_dir/docs/architect/hooks"
QUERY_SCRIPT="$HOOKS_DIR/query-context.sh"

if [ ! -x "$QUERY_SCRIPT" ]; then
    exit 0
fi

# Query context and output
# This becomes additional context in Claude's system prompt
context=$("$QUERY_SCRIPT" project "$project_dir" 2>/dev/null)

if [ -n "$context" ]; then
    echo ""
    echo "<architect-context>"
    echo "$context"
    echo "</architect-context>"
fi

exit 0
