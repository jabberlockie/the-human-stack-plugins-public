#!/bin/bash
# docs/architect/hooks/plan-approved.sh
# Called by PreToolUse:ExitPlanMode hook
# Commits changes, exports session, creates plan doc with links

DEBUG_LOG="/tmp/claude-hook-debug.log"

# Read JSON input from stdin
input=$(cat)

echo "=== Plan Approved Hook at $(date) ===" >> "$DEBUG_LOG"
echo "Raw input: $input" >> "$DEBUG_LOG"

project_dir=$(echo "$input" | jq -r '.cwd // empty')
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty')

if [ -z "$project_dir" ]; then
    echo "No project directory, exiting" >> "$DEBUG_LOG"
    exit 0
fi

timestamp=$(date +%Y-%m-%d-%H%M)
plans_dir="$project_dir/docs/plans"
sessions_dir="$project_dir/docs/architect/sessions"

mkdir -p "$plans_dir" "$sessions_dir"

# 1. Commit changes (if any)
cd "$project_dir"
commit_hash=""
if [ -n "$(git status --porcelain)" ]; then
    # Stage tracked files and new docs/plans files only (not all untracked)
    git add -u
    git add docs/plans/ docs/architect/ 2>/dev/null || true
    git commit -m "Plan approved: $timestamp

Co-Authored-By: Claude <noreply@anthropic.com>" 2>> "$DEBUG_LOG"
    commit_hash=$(git rev-parse HEAD 2>/dev/null)
    echo "Committed: $commit_hash" >> "$DEBUG_LOG"
else
    echo "No changes to commit" >> "$DEBUG_LOG"
fi

# 2. Export session
session_file="${timestamp}-session.md"
if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
    echo "{\"transcript_path\":\"$transcript_path\",\"cwd\":\"$project_dir\"}" | \
        "$project_dir/docs/architect/hooks/export-session.sh" >> "$DEBUG_LOG" 2>&1
    echo "Session exported" >> "$DEBUG_LOG"
else
    echo "No transcript to export: $transcript_path" >> "$DEBUG_LOG"
fi

# 3. Create plan document
plan_file="$plans_dir/${timestamp}-plan.md"
{
    echo "# Plan: $timestamp"
    echo ""
    echo "## References"
    echo ""
    if [ -n "$commit_hash" ]; then
        echo "- **Commit**: \`$commit_hash\`"
    else
        echo "- **Commit**: (no changes)"
    fi
    echo "- **Session**: [${timestamp}-session.md](../architect/sessions/${timestamp}-session.md)"
    echo ""
    echo "## Summary"
    echo ""
    echo "(Plan approved at $timestamp)"
    echo ""
} > "$plan_file"

echo "Plan doc created: $plan_file" >> "$DEBUG_LOG"

# 4. Ingest session into pgvector (if configured)
INGEST_SCRIPT="$project_dir/docs/architect/hooks/ingest-session.sh"
session_exported="$sessions_dir/${timestamp}-session.md"
if [ -x "$INGEST_SCRIPT" ] && [ -f "$session_exported" ]; then
    echo "Ingesting session into context database..." >> "$DEBUG_LOG"
    "$INGEST_SCRIPT" "$session_exported" "plan_approved" "$commit_hash" 2>> "$DEBUG_LOG" || true
    echo "Ingestion complete" >> "$DEBUG_LOG"
fi

# 5. Output instructions for Claude to continue
echo "Plan approved and committed."
if [ -n "$commit_hash" ]; then
    echo "Commit: $commit_hash"
fi
echo "Plan saved to: docs/plans/${timestamp}-plan.md"
echo ""
echo "Ready for implementation. Use /feature-dev to begin building."
exit 0
