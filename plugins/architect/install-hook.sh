#!/bin/bash
# install-hook.sh
# Installs the Architect SessionStart hook to user-level settings
# This enables auto-detection of uninitialized projects

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_SCRIPT="$SCRIPT_DIR/templates/hooks/session-start-init.sh"
CLAUDE_DIR="$HOME/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
HOOKS_DIR="$CLAUDE_DIR/hooks"

echo "Installing Architect SessionStart hook..."

# Create directories if needed
mkdir -p "$CLAUDE_DIR"
mkdir -p "$HOOKS_DIR"

# Copy hook script to ~/.claude/hooks/
cp "$HOOK_SCRIPT" "$HOOKS_DIR/architect-session-init.sh"
chmod +x "$HOOKS_DIR/architect-session-init.sh"
echo "Copied hook script to $HOOKS_DIR/architect-session-init.sh"

# Create or update settings.json
if [ ! -f "$SETTINGS_FILE" ]; then
    # Create new settings.json
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/architect-session-init.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF
    echo "Created $SETTINGS_FILE with SessionStart hook"
else
    # Check if SessionStart hook already exists
    if jq -e '.hooks.SessionStart' "$SETTINGS_FILE" > /dev/null 2>&1; then
        echo "SessionStart hook already exists in $SETTINGS_FILE"
        echo "Please manually add the architect-session-init.sh hook if needed"
    else
        # Add SessionStart to existing hooks
        tmp_file=$(mktemp)
        jq '.hooks.SessionStart = [{"matcher": "startup", "hooks": [{"type": "command", "command": "~/.claude/hooks/architect-session-init.sh", "timeout": 5}]}]' "$SETTINGS_FILE" > "$tmp_file"
        mv "$tmp_file" "$SETTINGS_FILE"
        echo "Added SessionStart hook to existing $SETTINGS_FILE"
    fi
fi

echo ""
echo "Installation complete!"
echo ""
echo "The Architect skill will now detect uninitialized projects on session start."
echo "When you open a project without Architect, you'll see a suggestion to run:"
echo "  /architect init"
echo ""
