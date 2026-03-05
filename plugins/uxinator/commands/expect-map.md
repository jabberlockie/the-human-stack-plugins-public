---
description: Map expectations for a client, audience, or session
allowed-tools: Read, Grep
argument-hint: [context: transcript, brief, or description]
---

Run the expectation-mapper skill at `${CLAUDE_PLUGIN_ROOT}/skills/expectation-mapper/SKILL.md`.

Read that skill first. Then analyze the context the user provides (pasted text, description, or file at @$1) and produce a full Expectation Map:

**Layer 1 — Origins:** Identify all 5 expectation types (Declared, Transferred, Inferred, Default, Social) with specific evidence from the input.

**Layer 2 — Dynamics:** Flag which dynamics are active (Asymmetry, Anchoring, Peak-End Weight, Compounding, Decay) with risk ratings.

**Layer 3 — Architecture:** Recommend specific operations (Audit, Declare, Inoculate, Monitor, Redirect) with scripted language Tim can use.

If JTBD data is available, map Pull→Declared, Push→Transferred, Anxiety→Unmanaged, Habit→Default.

Output in the Expectation Map template format from the skill. Flag the single highest-risk expectation prominently at the top.
