#!/bin/bash
# session-start-init.sh
# SessionStart hook for Architect auto-detection
# Installed to user-level (~/.claude/settings.json)
# Checks if Architect is initialized and suggests /architect init if not

# Read JSON input from stdin
input=$(cat)

project_dir=$(echo "$input" | jq -r '.cwd // empty')
source_type=$(echo "$input" | jq -r '.source // empty')

# Only run on startup (not resume/clear/compact)
if [ "$source_type" != "startup" ]; then
    exit 0
fi

if [ -z "$project_dir" ]; then
    exit 0
fi

# Check if this looks like a project directory (has .git or package.json or similar)
is_project=false
if [ -d "$project_dir/.git" ] || [ -f "$project_dir/package.json" ] || [ -f "$project_dir/Cargo.toml" ] || [ -f "$project_dir/pyproject.toml" ] || [ -f "$project_dir/go.mod" ]; then
    is_project=true
fi

# Only suggest Architect for actual projects
if [ "$is_project" = false ]; then
    exit 0
fi

# Check if Architect folder exists
if [ -d "$project_dir/docs/architect" ] && [ -f "$project_dir/docs/architect/Master_Context.md" ]; then
    # Architect is initialized - no message needed
    exit 0
fi

# Architect not initialized - output additionalContext
cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "This project does not have the Architect context system initialized. The Architect skill provides a three-layer context model (Product/Project/Task) for AI-assisted development. To set it up, run: /architect init"
  }
}
EOF

exit 0
