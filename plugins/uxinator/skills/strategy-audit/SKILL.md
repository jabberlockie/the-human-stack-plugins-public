---
name: strategy-audit
description: Detect mode drift in Tim's client delivery. Catches when he's explaining instead of deciding, teaching instead of architecting. Content-agnostic, context-aware. Use for "strategy check", "mode check", "am I explaining again".
---

# Strategy Audit

Pre-delivery and real-time audit that detects when Tim is in the wrong delivery mode for the context. The most common drift: Tim defaults to EXPLAIN (teaching frameworks) when the client hired him to DECIDE (make recommendations).

## Tim's Delivery Profile

- **Kolbe Quickstart 9**: Generates ideas faster than he filters. Strategy requires filtering.
- **High D, Extremely High I**: Overindexes on "did they get it" when strategy clients need "did he decide something for me."
- **Low S, Low C**: Resists sustained structured output. Strategy delivery requires both.
- **ADD, Low Working Memory**: Compensates by explaining — talking through thinking helps HIM process. Client experiences a lecture.
- **High Conceptual Aptitude**: Sees patterns others miss. Jumps between patterns without landing them as recommendations.

## Input Types

- **JTBD analysis** → Are we setting up strategy delivery or cataloging insights?
- **Session agenda/outline** → Does this deliver what the mode demands?
- **Call transcript/notes** → What mode was Tim in? What mode should he have been in?
- **Slide deck** → Are slides built for the right mode?
- **Diagnostic or sales asset** → Does this set the right expectations for what follows?

## Step 1: Determine Required Mode

From the input, identify:

```
CONTEXT CHECK
─────────────
Client:           [Who is this for?]
Relationship:     [Prospect | New client 0-90 days | Active client | Conference attendee]
Audience Size:    [1-5 | 6-30 | 30+]
Engagement Type:  [One-time | Multi-session | Ongoing retainer]
What They Paid For: [Keynote | Workshop/Training | Diagnostic | Managed Success | Advisory]
Their JTBD:       [What job did they hire Tim for? — pull from JTBD if available]

REQUIRED MODE:    [KEYNOTE | TRAINING | STRATEGY]
CONFIDENCE:       [HIGH | MEDIUM — explain if medium]
```

**Mode Selection Logic:**
- Conference/event + large audience + one-time = **KEYNOTE**
- Workshop/learning lab + group + skill-building = **TRAINING**
- Paid client engagement + specific org + ongoing = **STRATEGY**
- Diagnostic readout + leadership team + decisions needed = **STRATEGY**
- Webinar + broad audience + educational = **TRAINING**
- Sales call + prospect + discovery = **STRATEGY** (they need to feel decided-for, not taught)

## Step 2: Detect Actual Mode

Scan the input for mode signals:

**EXPLAIN signals** (Tim is teaching — WRONG for strategy):
- Defines terms or concepts unprompted
- Says "the research says" or "studies show"
- Walks through framework steps
- Uses "think of it this way" or "the way I think about this"
- Asks "does that make sense?"
- Presents theory before recommendation
- Offers multiple options without ranking them
- Spends time on WHY something works instead of WHAT to do
- Long preambles before getting to the point

**DECIDE signals** (Tim is strategizing — RIGHT for strategy):
- Makes explicit recommendations: "I recommend," "you should," "do this first"
- Prioritizes: "this matters most because"
- Assigns ownership: "this is yours, delegate that"
- Sets timelines: "in the next 30 days"
- Names tradeoffs and picks a side
- Creates structured deliverables (matrices, plans, sequences)
- Sets expectations for what comes next

**PROVOKE signals** (Tim is keynoting — RIGHT for keynotes):
- Tells a story without explaining the lesson
- Creates surprise with a data point or reframe
- Uses repetition for rhetorical effect
- Builds to an emotional peak
- Lands one idea, not many
- Closes with a memorable line, not a to-do list

## Step 3: Generate the Audit

```
STRATEGY AUDIT
══════════════

INPUT:            [What was reviewed]
REQUIRED MODE:    [KEYNOTE | TRAINING | STRATEGY]
ACTUAL MODE:      [What Tim is actually doing]
DRIFT DETECTED:   [YES — explain | NO]

MODE DRIFT MAP:
──────────────────────────────────────────────────────
SECTION/MOMENT          | REQUIRED  | ACTUAL    | ISSUE
──────────────────────────────────────────────────────
[Section 1]             | STRATEGY  | EXPLAIN   | [What's happening and why it's wrong]
──────────────────────────────────────────────────────
[Section 2]             | STRATEGY  | STRATEGY  | ✓ On mode
──────────────────────────────────────────────────────

DRIFT SCORE: [X/10] — 10 = perfectly on mode, 1 = completely wrong mode

TOP 3 DRIFT MOMENTS:
1. [Exact quote or section] — SHOULD HAVE BEEN: [what to say/do instead]
2. [Exact quote or section] — SHOULD HAVE BEEN: [what to say/do instead]
3. [Exact quote or section] — SHOULD HAVE BEEN: [what to say/do instead]
```

## Step 4: Expectation Gap Check

```
EXPECTATION GAP ANALYSIS
─────────────────────────

EXPECTATION ORIGINS:
┌─────────────┬──────────────────────────────────────┬──────────┐
│ ORIGIN      │ EXPECTATION FOUND                    │ MANAGED? │
├─────────────┼──────────────────────────────────────┼──────────┤
│ DECLARED    │ [What Tim explicitly promised]        │ YES | NO │
│ TRANSFERRED │ [From past experiences with similar]  │ YES | NO │
│ INFERRED    │ [What Tim's signals imply]            │ YES | NO │
│ DEFAULT     │ [What fills the vacuum — invisible]   │ YES | NO │
│ SOCIAL      │ [What third parties set]              │ YES | NO │
└─────────────┴──────────────────────────────────────┴──────────┘

UNMANAGED EXPECTATIONS: [List — these are active risk]

DYNAMICS AT PLAY:
- Asymmetry:   [Downside expectation that could hurt 2x?]
- Anchoring:   [First impression set that's hard to move?]
- Peak-End:    [Peak moment and ending managed?]
- Compounding: [Expectations cascading across stakeholders?]
- Decay:       [Expectations eroding without reinforcement?]
```

## Step 5: Deliverable Check

```
DELIVERABLE GAP
───────────────
What the client expects to RECEIVE:
[List — pull from JTBD "desired outcome" if available]

What Tim is currently PRODUCING:
[List — based on actual mode analysis]

GAP:
[Where deliverable expectations ≠ actual output]

ACTIONS:
1. [Specific and concrete]
2. [Specific and concrete]
3. [Specific and concrete]
```

## Tim's Strategy Danger Zones

**The Professor Trap:** Explaining WHY a framework works instead of APPLYING it. → "They didn't hire a professor. What's your recommendation?"

**The Options Buffet:** Presenting 3-4 approaches and asking the client to choose. → "Pick one. Recommend it. Defend it."

**The Insight Without Artifact:** Brilliant verbal insight that disappears when the call ends. → "If it's not written down, it didn't happen."

**The Theory Preamble:** 15 minutes of theoretical context before the recommendation. → "Lead with the recommendation. Add theory only if they ask why."

**The Empathy Detour:** High I spends too long validating feelings instead of moving to action. → "You've acknowledged it. Now solve it."

**The Adjacent Exploration:** Quickstart 9 chases a related pattern. → "Park it. Come back to what they're paying for."

**The Missing Follow-Through:** Session ends without documented next steps. → "Before this call ends: who does what by when?"

## Triggers

- "strategy check"
- "strategy audit"
- "mode check"
- "am I explaining again"
- "check my mode"
- "is this strategy or training"

## What This Skill Does NOT Do

- Design the deliverable (use strategy-architect)
- Evaluate post-delivery outcomes (use strategy-evaluate)
- Design training sessions (use instructional-designer)
- Design keynotes (use speechwriter)
