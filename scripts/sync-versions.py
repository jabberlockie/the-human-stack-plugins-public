#!/usr/bin/env python3
"""
sync-versions.py - Sync plugin versions from plugin.json into marketplace.json.

Reads each plugin's .claude-plugin/plugin.json version and updates the
corresponding entry in .claude-plugin/marketplace.json. Run this before
committing plugin changes, or wire it into a pre-commit hook.

Usage:
    python3 scripts/sync-versions.py          # sync and report
    python3 scripts/sync-versions.py --check  # check only, exit 1 if out of sync
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = REPO_ROOT / "plugins"


def get_plugin_versions():
    """Read version from each plugin's .claude-plugin/plugin.json."""
    versions = {}
    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            data = json.loads(plugin_json.read_text())
            versions[data.get("name", plugin_dir.name)] = data.get("version", "0.0.0")
    return versions


def sync():
    check_only = "--check" in sys.argv

    marketplace = json.loads(MARKETPLACE_PATH.read_text())
    plugin_versions = get_plugin_versions()

    changes = []
    for entry in marketplace["plugins"]:
        name = entry["name"]
        if name in plugin_versions:
            old = entry["version"]
            new = plugin_versions[name]
            if old != new:
                changes.append((name, old, new))
                if not check_only:
                    entry["version"] = new

    if not changes:
        print("All marketplace versions match plugin.json versions.")
        return 0

    for name, old, new in changes:
        print(f"  {name}: {old} -> {new}")

    if check_only:
        print(f"\n{len(changes)} plugin(s) out of sync. Run 'python3 scripts/sync-versions.py' to fix.")
        return 1

    MARKETPLACE_PATH.write_text(json.dumps(marketplace, indent=2) + "\n")
    print(f"\nUpdated marketplace.json with {len(changes)} version change(s).")
    return 0


if __name__ == "__main__":
    sys.exit(sync())
