---
name: mode-router
description: Determines which delivery mode (keynote, training, strategy) a situation calls for and routes to the right plugin. The front door for all delivery work. Use for "what mode should this be", "which plugin", "route this".
---

# Mode Router

The front door for all of Tim's delivery work. Takes any context — a client, an event, a deliverable request — and determines which delivery mode it requires, then routes to the correct plugin and skill.

## Why This Exists

Tim has three delivery plugins:
- **Speechwriter** — for keynotes and provocation
- **Instructinator** (Instructional Designer) — for training and education
- **Strategist** — for strategy and client architecture

The problem: Tim often doesn't know which mode a situation calls for, or starts in one mode and should be in another. Mode Router makes the determination and points him to the right tools.

## Mode Determination Logic

### Input

Any of the following:
- A client name or engagement description
- An event or talk request
- A deliverable request ("they want a plan")
- A JTBD analysis
- A vague "I need to prepare for [X]"

### Decision Tree

```
START
  │
  ├─ Is this a conference/event/public stage?
  │   ├─ Audience > 30? ──────────────────────── → KEYNOTE (Speechwriter)
  │   ├─ Audience 6-30 + learning outcomes? ──── → TRAINING (Instructinator)
  │   ├─ Audience 6-30 + no exercises? ────────── → KEYNOTE (Speechwriter)
  │   └─ Panel/fireside chat? ──────────────────── → KEYNOTE (Speechwriter)
  │
  ├─ Is this a paid client engagement?
  │   ├─ Discovery/sales call? ──────────────────── → STRATEGY (Strategist)
  │   ├─ Diagnostic readout? ────────────────────── → STRATEGY (Strategist)
  │   ├─ Post-diagnostic session? ───────────────── → STRATEGY (Strategist)
  │   ├─ Managed Success check-in? ──────────────── → STRATEGY (Strategist)
  │   ├─ Advisory session? ──────────────────────── → STRATEGY (Strategist)
  │   ├─ Training/workshop for client staff? ────── → TRAINING (Instructinator)
  │   └─ Accidental Techie training? ────────────── → TRAINING (Instructinator)
  │
  ├─ Is this a webinar?
  │   ├─ Broad audience + educational? ──────────── → TRAINING (Instructinator)
  │   ├─ Thought leadership + no exercises? ─────── → KEYNOTE (Speechwriter)
  │   └─ Client-specific + decisions needed? ────── → STRATEGY (Strategist)
  │
  └─ Is this content creation?
      ├─ Blog/article/social? ───────────────────── → Neither (use content skills)
      ├─ Proposal/SOW? ─────────────────────────── → STRATEGY (Strategist)
      └─ Course/curriculum? ─────────────────────── → TRAINING (Instructinator)
```

### Edge Cases

**Mixed-mode situations** — some engagements legitimately require mode-switching:
- A diagnostic readout (STRATEGY) followed by AI training (TRAINING) in the same day
- A conference talk (KEYNOTE) followed by a workshop (TRAINING)
- A sales call that starts as discovery (STRATEGY) and turns into a demo (shifts toward TRAINING)

For mixed-mode: Identify the PRIMARY mode and the SECONDARY mode. Route to the primary plugin. Flag the secondary mode and when the switch should happen.

```
MIXED MODE ALERT
────────────────
PRIMARY MODE:   [KEYNOTE | TRAINING | STRATEGY] — [X]% of time
SECONDARY MODE: [KEYNOTE | TRAINING | STRATEGY] — [Y]% of time
SWITCH POINT:   [When/where the mode should change]
PRIMARY PLUGIN: [Which plugin to route to]
ALSO USE:       [Which secondary plugin for the other segment]
```

## Output

```
MODE DETERMINATION
══════════════════
CONTEXT:       [What was provided]
MODE:          [KEYNOTE | TRAINING | STRATEGY]
CONFIDENCE:    [HIGH | MEDIUM | LOW]
PLUGIN:        [Speechwriter | Instructinator | Strategist]

RECOMMENDED FIRST SKILL:
[Which specific skill to start with and why]

SKILL SEQUENCE:
1. [First skill] — [What it does for this situation]
2. [Second skill] — [What it does next]
3. [Third skill] — [If applicable]

MODE RISK:
[Where Tim is most likely to drift into the wrong mode for this situation.
 E.g., "This is a diagnostic readout (STRATEGY). Tim will want to
 TEACH the vitals framework. Instead, he should APPLY it and recommend."]
```

## Quick Reference: Which Plugin Has What

```
SPEECHWRITER PLUGIN
───────────────────
speech-audit     → Is this outline/deck built for provocation?
speech-design    → Design a keynote from scratch
speech-rehearse  → Coach delivery of a keynote
speech-evaluate  → Did the provocation land?
speech-iterate   → Version the talk across deliveries

INSTRUCTINATOR PLUGIN (Instructional Designer)
──────────────────────────────────────────────
session-architect  → Design a training session
slide-reviewer     → Audit slides for content load + anchor strength
timing-check       → Realistic time audit with Tim's time tax
engagement-check   → Audit for passive stretches + scripted questions
story-finder       → Find story options for a section
survey-builder     → Generate outcome-aligned surveys
dry-run-coach      → Coach delivery of a training

STRATEGIST PLUGIN
─────────────────
strategy-audit     → Detect mode drift in strategy delivery
strategy-architect → Design + draft strategy deliverables
strategy-evaluate  → Post-delivery evaluation of strategy sessions
```

## Cross-Plugin Skills

Some skills are useful across modes:
- **tim-voice** — Language calibration for any mode
- **story-finder** — Stories serve keynotes AND trainings (not strategy — strategy uses data, not stories)
- **slide-reviewer** — Slides exist in keynotes AND trainings (strategy rarely uses slides)
- **JTBD analysis** — Feeds strategy-audit AND strategy-architect AND speech-design (for audience insight)
- **thought-leadership-librarian** — Captures concepts that emerge from any mode

## Triggers

- "what mode should this be"
- "which plugin"
- "route this"
- "how should I approach this"
- "I have [event/meeting/session] coming up"
- "prep me for [anything]"
- Any request that could go to multiple plugins

## What This Skill Does NOT Do

- Do the work (it routes to the skill that does the work)
- Override Tim's judgment (if Tim says "this is a keynote," this skill can flag disagreement but Tim decides)
- Handle content creation that isn't delivery (blogs, social, articles = different skill set)
