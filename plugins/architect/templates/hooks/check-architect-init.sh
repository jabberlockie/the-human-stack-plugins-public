#!/bin/bash
# docs/architect/hooks/check-architect-init.sh
# Called by SessionStart hook to check if Architect is initialized
# If not initialized, outputs a reminder message

# Read JSON input from stdin
input=$(cat)

project_dir=$(echo "$input" | jq -r '.cwd // empty')

if [ -z "$project_dir" ]; then
    exit 0
fi

# Check if docs/architect folder exists
if [ ! -d "$project_dir/docs/architect" ]; then
    echo "Architect context system not initialized in this project."
    echo "Run /architect init to set up the three-layer context model."
    exit 0
fi

# Check if Master_Context.md exists
if [ ! -f "$project_dir/docs/architect/Master_Context.md" ]; then
    echo "docs/architect folder exists but Master_Context.md is missing."
    echo "Run /architect init to complete setup."
    exit 0
fi

# All good - Architect is initialized
exit 0
