---
name: architect
description: Initialize and manage the Architect three-layer context framework for any project
---

# Architect Skill

Bootstrap and manage a unified AI context system using the three-layer model: Product (stable reference), Project (current build cycle), and Task (subagent capabilities).

## Commands

### /architect init

Bootstrap the Architect framework in the current project.

**Collects via AskUserQuestion:**
- `PROJECT_NAME` - Human-readable name (e.g., "My Awesome App")
- `PROJECT_DESCRIPTION` - 2-3 sentence domain description
- `TECH_STACK` - Primary language/framework (TypeScript, Python, Go, etc.)
- `DEPLOYMENT` - Target platform (Replit, Vercel, Local, AWS, etc.)

**Creates:**
- `docs/architect/` directory with three-layer structure
- `docs/architect/Master_Context.md` - Hub file, single source of truth
- `docs/architect/product/` - Stable reference (architecture, design, domain)
- `docs/architect/project/` - Current build cycle (active, decisions, state)
- `docs/plans/` - Task documentation and backlog (at docs/ level)
- `docs/architect/subagents/` - Specialized agent capabilities
- `docs/architect/hooks/` - Automation scripts
- `docs/architect/sessions/` - Exported conversation history
- `.claude/settings.json` - Hook configuration
- `.claude/agents/architect.md` - Project-specific orchestrator
- IDE symlinks: `CLAUDE.md`, `replit.md`, `.cursorrules`, `.github/copilot-instructions.md`

**Implementation Steps:**
1. Use AskUserQuestion to collect project details
2. Create all directories under `docs/architect/` and `docs/plans/`
3. Process templates from the plugin's `templates/` directory (use `${CLAUDE_PLUGIN_ROOT}/templates/`)
4. Substitute `{{VARIABLE}}` placeholders with collected values
5. Copy hook scripts (executable)
6. Create symlinks for IDE integration
7. Report success with next steps

### /architect status

Check context health and report any issues.

**Checks:**
- Required files exist (Master_Context.md, project/active.md, etc.)
- Symlinks are valid
- Hooks are executable
- project/state.md is recent (warn if > 7 days stale)

**Reports:**
- Missing files
- Broken symlinks
- Permission issues
- Stale context warnings

### /architect archive

Archive current project context and prepare for next cycle.

**Actions:**
1. Create `docs/architect/archive/{feature-name}/` directory
2. Move `project/active.md`, `project/decisions.md`, `project/state.md` to archive
3. Move relevant `plans/*.md` files to archive
4. Create fresh `project/` files from templates
5. Update `Master_Context.md` to reflect cleared state
6. Report what was archived

**Usage:**
```
/architect archive auth-system
```

### /architect setup-context

Initialize the pgvector context system in the project's database.

**Prerequisites:**
- PostgreSQL database with pgvector extension available
- `DATABASE_URL` environment variable set
- `OPENAI_API_KEY` environment variable set (for embeddings)
- `ANTHROPIC_API_KEY` environment variable set (for classification)

**Actions:**
1. Enable pgvector extension in database
2. Create `session_embeddings` table with vector column
3. Create indexes for efficient similarity search
4. Copy context system files to `docs/architect/context/`
5. Report success

**Usage:**
```
/architect setup-context
```

### /architect log

Manually ingest the current or specified session into the context database.

**Actions:**
1. Export current session to `sessions/` (if not already exported)
2. Chunk session by conversation turns
3. Classify each chunk by layer/sublayer using Claude
4. Generate embeddings using OpenAI
5. Store in pgvector database

**Usage:**
```
/architect log                    # Log current session
/architect log sessions/my-session.md  # Log specific session file
```

### /architect context

Query the context database for relevant information.

**Modes:**
- `project` - Query based on current project/active.md (default)
- `layer <layer> [sublayer]` - Query specific layer
- `search <query>` - Free-text semantic search

**Usage:**
```
/architect context                      # Auto-query based on current work
/architect context layer user patterns  # Query user patterns
/architect context search "auth flow"   # Semantic search
```

### /architect session

Manage named sessions for better context organization.

**Actions:**
- `start <name>` - Start a named session (writes to `.current-session`)
- `end` - End current named session
- (no args) - Show current session name

**Usage:**
```
/architect session start auth-refactor  # Start named session
/architect session                      # Show current session
/architect session end                  # End session
```

When a named session is active, all `/compact` exports append to the same session file instead of creating new timestamped files.

## Context Layers

The Architect system organizes knowledge into five retrieval layers, each with sublayers:

### Five-Layer Model (for Context Retrieval)

| Layer | Sublayers | What it captures |
|-------|-----------|------------------|
| **USER** | patterns, preferences, learnings, mistakes | How you work, recurring approaches, lessons learned |
| **PRODUCT** | architecture, design, domain | System knowledge that persists across features |
| **PROJECT** | active, decisions, state | Current feature context and choices |
| **PLAN** | strategy, steps, backlog | Implementation approaches and future work |
| **TASK** | implementation, debugging, verification | How specific work was executed |

### Three-Layer File Model (for Organization)

```
PRODUCT (Architecture Agent)     - What is this? How does it work?
        |                          Stable reference, rarely changes
        v
PROJECT (Build Agent)            - What are we building right now?
        |                          Current cycle, cleared when done
        v
TASK    (Subagents)              - How do specific things work?
                                   Capabilities for specialized work
```

| Layer | Folder | Purpose | Changes |
|-------|--------|---------|---------|
| PRODUCT | `docs/architect/product/` | Stable reference (architecture, design, domain knowledge) | Rarely |
| PROJECT | `docs/architect/project/` | Current build cycle (active work, decisions, state) | Each feature |
| TASK | `docs/architect/subagents/` | Specialized capabilities (domain experts) | As needed |

### How They Connect

- **Files** (product/, project/, plans/) are the explicit, curated context you maintain
- **Sessions** are ingested into pgvector and classified by the five-layer model
- **Queries** combine file context (active.md) with semantic search of session history

## Lifecycle

1. **New feature starts** - Create/update `project/active.md`
2. **During build** - Update `state.md`, log decisions
3. **Feature ships** - Run `/architect archive {feature}`
4. **Learnings graduate** - Move stable patterns to `product/`
5. **Clear project/** - Ready for next cycle

## Auto-Detection (SessionStart Hook)

The skill includes an optional SessionStart hook that detects uninitialized projects.

**What it does:**
- Runs when you start a new Claude Code session
- Checks if `docs/architect/` folder exists in the project
- If missing, suggests running `/architect init`

**Installation:**
```bash
cd $CLAUDE_PLUGIN_ROOT
./install-hook.sh
```

This installs a user-level hook to `~/.claude/settings.json` that runs for all projects.

## Hooks

The framework includes automation hooks for session management and context retrieval.

### Ingestion Hooks (write to context DB)

| Hook | Trigger | Action |
|------|---------|--------|
| **PreCompact** | Before `/compact` | Export session, then ingest into pgvector |
| **ExitPlanMode** | Plan approved | Commit, export session, ingest with plan metadata |
| **post-commit** | After git commit | Ingest recent session with commit hash |

### Query Hooks (read from context DB)

| Hook | Trigger | Action |
|------|---------|--------|
| **SessionStart** | Opening project | Query relevant context, inject into system prompt |

### Activity Tracking

| Hook | Trigger | Action |
|------|---------|--------|
| **post-commit** | After git commit | Update `project/state.md` and `Master_Context.md` Recent Activity |

### Hook Details

**PreCompact** (`export-session.sh`)
- Exports conversation to `sessions/{timestamp}-session.md` or `sessions/{session-name}.md`
- If context system configured, ingests session into pgvector

**ExitPlanMode** (`plan-approved.sh`)
- Commits staged changes
- Exports session
- Creates plan doc in `plans/`
- Ingests session with `plan_approved` trigger and commit hash

**SessionStart** (`session-start-context.sh`)
- Queries pgvector for context relevant to current `project/active.md`
- Outputs context wrapped in `<architect-context>` tags
- Silently skips if context system not configured

## IDE Symlinks

All AI tools read the same context via symlinks to `Master_Context.md`:

| File | Tool |
|------|------|
| `CLAUDE.md` | Claude Code |
| `replit.md` | Replit AI |
| `.cursorrules` | Cursor |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.windsurfrules` | Windsurf |

One file to edit, all tools updated.

## Template Variables

Templates use `{{VARIABLE}}` syntax:

| Variable | Example | Description |
|----------|---------|-------------|
| `{{PROJECT_NAME}}` | "Brain Pinecone Manager" | Human-readable name |
| `{{PROJECT_SLUG}}` | "brain-pinecone-manager" | URL-safe lowercase |
| `{{PROJECT_DESCRIPTION}}` | "A vector database management app..." | Brief description |
| `{{TECH_STACK}}` | "TypeScript" | Primary language/framework |
| `{{DEPLOYMENT}}` | "Replit" | Target platform |
| `{{DATE}}` | "2026-01-17" | Current date |

## Subagent Catalog

Optional specialized agents available in `catalog/`:

| Agent | Focus |
|-------|-------|
| `ui-agent.md` | Frontend components, styling, UX |
| `api-agent.md` | Backend endpoints, services, data flow |
| `db-agent.md` | Database schema, queries, migrations |

Domain-specific agents can be added based on project needs.
