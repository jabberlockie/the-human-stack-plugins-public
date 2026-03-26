#!/bin/bash
# docs/architect/hooks/check-architect-init.sh
# Called by SessionStart hook to check if Architect is initialized
# If not initialized, outputs a reminder message
# If initialized, loads master context for automatic architectural awareness

# Read JSON input from stdin
input=$(cat)

project_dir=$(echo "$input" | jq -r '.cwd // empty')

if [ -z "$project_dir" ]; then
    exit 0
fi

ARCHITECT_DIR="$project_dir/docs/architect"

# Check if docs/architect folder exists
if [ ! -d "$ARCHITECT_DIR" ]; then
    echo "Architect context system not initialized in this project."
    echo "Run /architect init to set up the three-layer context model."
    exit 0
fi

# Check if Master_Context.md exists
if [ ! -f "$ARCHITECT_DIR/Master_Context.md" ]; then
    echo "docs/architect folder exists but Master_Context.md is missing."
    echo "Run /architect init to complete setup."
    exit 0
fi

# Architect is initialized -- load context
line_count=0
max_lines=200

echo "<architect-context>"

# Load master_intent.md (current work, priorities, active items)
if [ -f "$ARCHITECT_DIR/master_intent.md" ]; then
    echo "## Intent"
    intent_lines=$(wc -l < "$ARCHITECT_DIR/master_intent.md")
    if [ "$intent_lines" -gt 80 ]; then
        head -n 80 "$ARCHITECT_DIR/master_intent.md"
        echo "... (truncated, ${intent_lines} total lines)"
        line_count=$((line_count + 82))
    else
        cat "$ARCHITECT_DIR/master_intent.md"
        line_count=$((line_count + intent_lines + 1))
    fi
fi

# Load Corrections section from master_memory.md
if [ -f "$ARCHITECT_DIR/master_memory.md" ]; then
    # Extract from "## Corrections" heading to the next heading or EOF
    corrections=$(sed -n '/^## Corrections/,/^## [^C]/p' "$ARCHITECT_DIR/master_memory.md" | sed '${ /^## [^C]/d }')
    if [ -n "$corrections" ]; then
        echo ""
        correction_lines=$(echo "$corrections" | wc -l)
        if [ "$correction_lines" -gt 40 ]; then
            echo "$corrections" | head -n 40
            echo "... (truncated, ${correction_lines} total lines)"
            line_count=$((line_count + 42))
        else
            echo "$corrections"
            line_count=$((line_count + correction_lines + 1))
        fi
    fi
fi

echo "</architect-context>"
exit 0
