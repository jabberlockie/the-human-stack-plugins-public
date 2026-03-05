# Architect Template

A Claude Code plugin for bootstrapping unified AI context systems in any project.

## Quick Start

1. **Install the plugin**:
   ```
   /plugin install https://github.com/jabberlockie/architect-template
   ```

2. **Initialize in your project**:
   ```
   /architect init
   ```

3. **Answer the prompts** for project name, description, tech stack, and deployment target.

The plugin includes a SessionStart hook that auto-detects uninitialized projects and suggests `/architect init`.

## What It Creates

```
your-project/
├── CLAUDE.md                     # Symlink -> docs/architect/Master_Context.md
├── replit.md                     # Symlink -> docs/architect/Master_Context.md
├── .cursorrules                  # Symlink -> docs/architect/Master_Context.md
├── .github/copilot-instructions.md
│
├── .claude/
│   ├── settings.json             # Hook configuration
│   └── agents/
│       └── architect.md          # Project orchestrator
│
└── docs/
    ├── plans/                    # Task documentation & planning
    │   ├── README.md
    │   └── backlog.md
    │
    └── architect/
        ├── Master_Context.md     # Hub - single source of truth
        ├── manifest.json         # Project tracking
        │
        ├── product/              # LAYER 1: Stable reference
        │   ├── architecture.md   # Tech stack, system design
        │   └── design.md         # UI patterns, styling
        │
        ├── project/              # LAYER 2: Current build
        │   ├── active.md         # What we're building
        │   ├── decisions.md      # Why we chose X over Y
        │   └── state.md          # Progress, blockers
        │
        ├── subagents/            # LAYER 3: Capabilities
        │   └── README.md
        │
        ├── sessions/             # Exported conversations
        ├── hooks/                # Automation scripts
        └── archive/              # Completed features
```

## Three-Layer Context Model

| Layer | Purpose | Changes |
|-------|---------|---------|
| **PRODUCT** | What is this? How does it work? | Rarely |
| **PROJECT** | What are we building right now? | Each feature |
| **TASK** | Specialized agent capabilities | As needed |

## Commands

- `/architect init` - Bootstrap framework in current project
- `/architect status` - Check context health
- `/architect archive {feature}` - Archive and clear for next cycle

## Hooks

**Project-level hooks** (installed per-project by `/architect init`):
1. **Git post-commit** - Updates Recent Activity sections
2. **PreCompact** - Exports session on `/compact`
3. **PreToolUse:ExitPlanMode** - Commits + exports on plan approval

**User-level hook** (optional, installed by `./install-hook.sh`):
4. **SessionStart** - Detects uninitialized projects, suggests `/architect init`

## Lifecycle

```
New Feature -> project/active.md -> Build -> Archive -> Clear -> Repeat
                    |                   |
                    v                   v
             project/state.md    archive/{feature}/
             project/decisions.md
```

Stable patterns graduate from `project/` to `product/` over time.

## Customization

### Add Domain Knowledge

Create files in `product/domain/`:
```
docs/architect/product/domain/
├── pinecone.md       # Vector database patterns
├── notion.md         # Notion API reference
└── stripe.md         # Payment integration
```

### Add Subagents

Copy from `catalog/` or create custom agents in `subagents/`:
```
docs/architect/subagents/
├── README.md
├── ui-agent.md
├── api-agent.md
└── custom-agent.md
```

## Development

This plugin is installed via `/plugin install` from `https://github.com/jabberlockie/architect-template`.

### Structure

```
architect-template/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest
├── skills/
│   └── architect/
│       └── SKILL.md      # Skill definition (auto-discovered)
├── hooks/
│   └── hooks.json        # SessionStart auto-detection hook
├── templates/            # Template files with {{VARIABLE}}
├── catalog/              # Optional subagent library
├── examples/             # Reference implementation
└── README.md
```

### Testing

1. Install the plugin: `/plugin install https://github.com/jabberlockie/architect-template`
2. Create a test project directory
3. Run `/architect init`
4. Verify all files created correctly
5. Test hooks by making commits and running `/compact`

## License

MIT
