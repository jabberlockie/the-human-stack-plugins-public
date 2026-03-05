---
description: Determine delivery mode for a context (strategy/keynote/training)
allowed-tools: Read, Grep
argument-hint: [context description or transcript]
---

Route the following context through the mode-router skill at `${CLAUDE_PLUGIN_ROOT}/skills/mode-router/SKILL.md`.

Read that skill first. Then analyze the context the user provides (pasted text, description, or file at @$1) and output:

1. MODE determination (STRATEGY / KEYNOTE / TRAINING) with confidence level
2. REASONING — which decision tree branches led here
3. RECOMMENDED FIRST SKILL from the UXinator plugin
4. MODE RISK — where Tim is likely to drift and why
5. SKILL SEQUENCE — ordered list of which skills to run

Keep the output under the mode-router template format. Be direct. Tim needs a fast answer, not a dissertation.
