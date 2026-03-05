#!/bin/bash
# docs/architect/hooks/export-session.sh
# Called by Claude Code PreCompact hook
# Exports conversation session to docs/architect/sessions/

# Debug log location
DEBUG_LOG="/tmp/claude-hook-debug.log"

# Read JSON input from stdin
input=$(cat)

# Log the raw input for debugging
echo "=== Hook called at $(date) ===" >> "$DEBUG_LOG"
echo "Raw input:" >> "$DEBUG_LOG"
echo "$input" >> "$DEBUG_LOG"
echo "" >> "$DEBUG_LOG"

# Extract transcript path from hook input
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty')

echo "Extracted transcript_path: $transcript_path" >> "$DEBUG_LOG"

if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then
    echo "No transcript found, skipping export"
    echo "Reason: transcript_path empty or file doesn't exist" >> "$DEBUG_LOG"
    exit 0
fi

# Get project directory from hook input
project_dir=$(echo "$input" | jq -r '.cwd // empty')
echo "Extracted project_dir: $project_dir" >> "$DEBUG_LOG"

if [ -z "$project_dir" ]; then
    echo "No project directory found"
    echo "Reason: project_dir empty" >> "$DEBUG_LOG"
    exit 0
fi

sessions_dir="$project_dir/docs/architect/sessions"
echo "sessions_dir: $sessions_dir" >> "$DEBUG_LOG"

# Create sessions directory if needed
mkdir -p "$sessions_dir"
echo "mkdir result: $?" >> "$DEBUG_LOG"

# Generate filename with timestamp
timestamp=$(date +%Y-%m-%d-%H%M)
filename="${timestamp}-session.md"
echo "Will write to: $sessions_dir/$filename" >> "$DEBUG_LOG"

# Extract and format session content
{
    echo "# Session Export: $timestamp"
    echo ""
    echo "## Summary"
    echo "(Auto-exported on /compact)"
    echo ""
    echo "---"
    echo ""
    echo "## Conversation"
    echo ""

    # Parse JSONL transcript - Claude Code format has nested message object
    # Structure: {"type": "user"|"assistant", "message": {"role": "...", "content": ...}}
    while IFS= read -r line; do
        # Skip empty lines
        [ -z "$line" ] && continue

        # Get the record type (user, assistant, summary, etc.)
        record_type=$(echo "$line" | jq -r '.type // empty')

        # Only process user and assistant messages
        if [ "$record_type" != "user" ] && [ "$record_type" != "assistant" ]; then
            continue
        fi

        # Extract role from nested message object
        role=$(echo "$line" | jq -r '.message.role // empty')

        # Handle different content formats in the nested message object
        content=$(echo "$line" | jq -r '
            if .message.content then
                if (.message.content | type) == "array" then
                    [.message.content[] | select(.type == "text") | .text] | join("\n")
                elif (.message.content | type) == "string" then
                    .message.content
                else
                    empty
                end
            else
                empty
            end
        ')

        if [ -n "$role" ] && [ -n "$content" ]; then
            # Capitalize first letter of role for readability
            role_display=$(echo "$role" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')
            echo "### $role_display"
            echo ""
            echo "$content"
            echo ""
            echo "---"
            echo ""
        fi
    done < "$transcript_path"
} > "$sessions_dir/$filename"

echo "Session exported to docs/architect/sessions/$filename"

# Ingest session into pgvector (if configured)
INGEST_SCRIPT="$project_dir/docs/architect/hooks/ingest-session.sh"
if [ -x "$INGEST_SCRIPT" ]; then
    echo "Ingesting session into context database..." >> "$DEBUG_LOG"
    "$INGEST_SCRIPT" "$sessions_dir/$filename" "precompact" 2>> "$DEBUG_LOG" || true
    echo "Ingestion complete" >> "$DEBUG_LOG"
fi

exit 0
