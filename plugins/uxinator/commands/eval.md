---
description: Post-delivery retrospective — evaluate a session against its mode
allowed-tools: Read, Grep
argument-hint: [transcript or session notes]
---

Evaluate a completed session. First, determine the delivery mode from context, then route to the correct evaluation skill:

- **STRATEGY** → Read `${CLAUDE_PLUGIN_ROOT}/skills/strategy-evaluate/SKILL.md`
- **KEYNOTE** → Read `${CLAUDE_PLUGIN_ROOT}/skills/speech-evaluate/SKILL.md`
- **TRAINING** → Use the dry-run-coach framework at `${CLAUDE_PLUGIN_ROOT}/skills/dry-run-coach/SKILL.md` in post-hoc mode

Also read `${CLAUDE_PLUGIN_ROOT}/skills/expectation-mapper/SKILL.md` to assess expectation alignment.

Analyze the transcript or notes at @$1 and produce:

1. **MODE FIDELITY** — Did Tim stay in the right mode? Where did he drift?
2. **EXPECTATION ALIGNMENT** — Were declared expectations met? What was unmanaged?
3. **OUTCOME ASSESSMENT** — Did the session achieve what it was designed to achieve?
4. **TOP 3 FIXES** — Most important changes for next time. Specific, actionable.
5. **KEEP LIST** — What worked. Tim needs to know what to repeat.

Be direct. "This section was boring" beats "consider increasing energy."
