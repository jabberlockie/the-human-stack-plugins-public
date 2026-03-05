# UXinator

**Expectation Architecture for all delivery modes.**

UX² = User Expectations × User Experience. This plugin routes any delivery context to the right mode (strategy, keynote, training), maps expectations, detects mode drift, designs deliverables, and evaluates sessions.

Built on Tim Lockie's Expectation Architecture Framework:
- **Layer 1 — Origins:** Declared, Transferred, Inferred, Default, Social
- **Layer 2 — Dynamics:** Asymmetry, Anchoring, Peak-End Weight, Compounding, Decay
- **Layer 3 — Architecture:** Audit, Declare, Inoculate, Monitor, Redirect

## Components

### Commands (5)

| Command | What it does |
|---------|-------------|
| `/mode-check` | Determine delivery mode for a context |
| `/expect-map` | Map expectations for a client or audience |
| `/eval` | Post-delivery retrospective |
| `/speech-check` | Quick keynote outline audit |
| `/story-find` | Find or harvest stories |

### Skills (16)

**Orchestration (2)**
- `mode-router` — Routes any context to the right delivery mode
- `expectation-mapper` — The theoretical engine for all 3 layers

**Strategy (3)**
- `strategy-audit` — Pre-session check for strategy delivery
- `strategy-architect` — Build strategy deliverables (Priority Maps, Delegation Matrices)
- `strategy-evaluate` — Post-session: did Tim decide or teach?

**Keynote (5)**
- `speech-audit` — Audit a keynote concept for provocation and arc
- `speech-design` — Design the full keynote structure
- `speech-rehearse` — Rehearsal coaching and refinement
- `speech-evaluate` — Post-delivery keynote retrospective
- `speech-iterate` — Evolve a keynote across multiple deliveries

**Training (7)**
- `session-architect` — Design training sessions with expectation mapping
- `engagement-check` — Audit for passive stretches + expectation checks
- `timing-check` — Realistic timing with decay risk assessment
- `slide-reviewer` — Two-axis slide review + expectation signals
- `dry-run-coach` — Walkthrough coaching with mode drift detection
- `story-finder` — Find, harvest, or design inoculation stories
- `survey-builder` — Pre/post/pulse surveys with expectation measurement

### MCP Servers

- **Notion** — Pull session context, transcripts, client data
- **Canva** — Review and audit slide decks

## Setup

1. Install the plugin in Cowork
2. Connect Notion and Canva when prompted
3. Use `/mode-check` with any new delivery context to get started

## Usage

**Starting a new engagement:** `/mode-check` → follow the skill sequence it recommends.

**Before any session:** `/expect-map` with whatever context you have (transcript, brief, email thread).

**Before a keynote:** `/speech-check` with your outline.

**Need a story:** `/story-find` with the concept name.

**After delivery:** `/eval` with the transcript or your notes.

## Author

The Human Stack — Tim Lockie
