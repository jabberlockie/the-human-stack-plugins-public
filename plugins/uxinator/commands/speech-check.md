---
description: Quick keynote outline audit — structure, arc, expectation signals
allowed-tools: Read, Grep
argument-hint: [outline or draft]
---

Run a quick audit on a keynote outline or draft. Read the speech-audit skill at `${CLAUDE_PLUGIN_ROOT}/skills/speech-audit/SKILL.md` first.

Analyze the outline the user provides (pasted text or file at @$1) and produce a fast assessment:

1. **PROVOCATION CHECK** — Does it provoke or just inform? Keynotes need a "wait, what?" moment.
2. **ARC CHECK** — Does it follow Hook → Tension → Turn → Resolution → Call?
3. **EXPECTATION SIGNALS** — What will the audience INFER from the title, opening, and first 2 minutes? Does the rest deliver on that promise?
4. **MODE DRIFT RISK** — Where will Tim slip into TRAINING mode (explaining frameworks instead of provoking)?
5. **STORY DENSITY** — Enough stories? Right placement? Any data dumps without narrative?
6. **VERDICT** — Ready / Needs Work / Major Issues — with the single most important fix.

Keep it tight. This is a pre-flight checklist, not a full redesign.
