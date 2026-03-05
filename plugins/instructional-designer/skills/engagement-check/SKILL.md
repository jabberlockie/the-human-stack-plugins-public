---
name: engagement-check
description: Audit session for passive stretches. Flags problems with exact scripted questions and timers. Use for "engagement check", "energy audit".
---

# Engagement-Check Skill

## How It Works

This skill audits a session plan or run-of-show for engagement gaps and energy problems. It identifies:
- Passive stretches longer than 8 minutes without audience participation
- Energy patterns that are unbalanced (all lecture, all activity, flat arc)
- Moments where interaction could unlock understanding

For every flagged issue, it outputs an actionable fix with exact words Tim can say and a timer.

## Input

Pass a session plan, run-of-show, transcript, or outline. Include timestamps or time markers (e.g., "Min 12-22", "Slide 3", "Segment 2").

## Output Format

```
ENGAGEMENT AUDIT: [Session Title]

WHERE     | WHAT'S WRONG                    | DO THIS        | SAY THIS (exact words)                                          | TIMER
──────────|─────────────────────────────────|────────────────|─────────────────────────────────────────────────────────────────|──────
Min 12-22 | 10 min passive, no interaction  | Pair-share     | "Turn to the person next to you. What's one thing in your      | 90 sec
          |                                 |                |  org that this framework explains? 90 seconds."                 |
```

## Critical Design Rules

**For Tim:**
- Tim is self-described "really bad at engagement questions." Every question must be EXACT WORDS he can say. Not a concept. Not "ask about their experience." The literal sentence.
- Questions are calibrated to his High I style — designed to give the room something to give HIM so he can riff. He's great at improvising off audience responses. The question just needs to open the door.
- Timers are mandatory because Tim will either cut it short (impatience) or let it run long (he got interested in what someone said).

**For Balance:**
- Flag sections where he's so interaction-heavy there's no space to land a concept. Sometimes 5-7 min of uninterrupted Tim is exactly right IF the content earns it.
- Target: 3-4 interactive moments per 30 minutes, varied in type.

## Engagement Toolkit

Load `references/engagement-toolkit.md` for the full library of 10 engagement move types (pair-share, cascading poll, one-word harvest, think-write-share, etc.) with "Say This" templates and timing for each. Use that library to select the right move for each flagged zone.

## "Say This" Question Design Principles

- **Short setup, specific ask.** Not "what do you think about X?" but "what's ONE thing that..."
- **Physical engagement when possible.** Raise hand, stand up, turn to neighbor — breaks the passive mode.
- **Surface experience, not knowledge.** "Tell me a time when..." not "Who can define..."
- **Give Tim material to riff.** The responses should create a moment he can improvise from.
- **Avoid put-on-the-spot.** Never call someone by name cold. Offer write-it-down or shout-it-out options.
- **Vary the type.** Pair-share, full-room poll, shout-out, think-then-share, show of hands — rhythmic variety matters.

## Summary Section (At End)

```
ENGAGEMENT SCORE: [X/10]
PASSIVE STRETCHES: [N flagged]
INTERACTION DENSITY: [X interactions per 30 min — target is 3-4]
ENERGY ARC: [Describe the shape — front-loaded? flat? builds? dips at min 35?]
```

## How to Trigger This Skill

Use any of these phrases:
- "engagement check"
- "check engagement"
- "is this interactive enough"
- "energy audit"
- "does this have dead zones"

Then paste the session plan, run-of-show, or transcript you want audited.
