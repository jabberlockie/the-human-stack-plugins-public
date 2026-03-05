---
description: Find or harvest stories for a concept, section, or inoculation need
allowed-tools: Read, Grep
argument-hint: [concept or section name]
---

Read the story-finder skill at `${CLAUDE_PLUGIN_ROOT}/skills/story-finder/SKILL.md` first.

The user needs a story. Determine which mode based on their request:

**Mode 1 — Find a Story:** User has a concept and needs story options. Generate 3 options with setup/turn/bridge structure. Rate each for emotional weight, relevance, and Tim's natural delivery fit.

**Mode 2 — Harvest Stories:** User has a transcript or source. Extract every story, anecdote, and example. Tag each with concept, emotional weight, and reuse potential.

**Mode 3 — Inoculation Story:** User has a TRANSFERRED expectation to neutralize. Design a story that acknowledges the audience's past experience and redirects to the current session's value. Include exact scripted language for the setup and bridge.

Ask which mode if unclear, but default to Mode 1 if the user just names a concept.

Output in the story-finder template format. Stories need setup, turn, bridge, and exact words Tim can say.
