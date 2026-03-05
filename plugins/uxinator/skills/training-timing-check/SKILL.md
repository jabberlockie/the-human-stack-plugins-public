---
name: training-timing-check
description: >
  Audit session timing with realistic estimates and Tim's time tax. Flags what to cut
  or expand. Includes expectation decay risk for sessions that run long.
  Use for "timing check", "will this fit", "time audit".
version: 2.0.0
---

# Timing Check

Reality-check a session plan or run-of-show against realistic time estimates. Tim chronically underestimates interactive segments, so this skill applies a "time tax" and flags what won't fit.

## Core Behavior

### 1. Calculate Realistic Time

Apply **Tim's Time Tax**:
- Storytelling/examples: **+30%**
- Group exercises/pair-share: **+50%**
- Q&A segments: **+25%**
- Content delivery/demos: no adjustment

### 2. Generate Single-Table Audit

```
TIMING AUDIT: [Session Title] — [Allocated: X min]

SEGMENT              | PLANNED | REALISTIC | DELTA  | VERDICT
─────────────────────|─────────|───────────|────────|────────
Opening Hook         |   5 min |     5 min |   0    | OK
Expectation Set      |   3 min |     3 min |   0    | OK
Concept 1 + discuss  |  12 min |    17 min |  +5    | OVER
Pair-share exercise  |  10 min |    15 min |  +5    | OVER
...                  |         |           |        |
─────────────────────|─────────|───────────|────────|────────
TOTAL                |  55 min |    72 min | +17    | WON'T FIT

HARD STOP: [Time] | BUFFER NEEDED: 5 min | ACTUAL BUFFER: -12 min
```

### 3. Diagnose & Recommend

**If timing is over:**
- Name exactly what to cut (with duration saved)
- Explain why that segment is the weakest
- Show revised total after cuts
- Calculate remaining buffer

**If timing fits:**
- Flag segments with 0% buffer as "tight"
- Identify back-to-back dense segments
- Warn if the close is squeezed

**If timing is under:**
- Name exactly what to expand and why

### 4. Expectation Decay Risk Assessment

**NEW — from Expectation Architecture**

When sessions run long, expectations decay. The audience's initial expectations (set in the opening) erode as cognitive fatigue builds. This creates a compounding problem: they forget what was promised AND they're less satisfied with what's delivered.

```
DECAY RISK ASSESSMENT
─────────────────────
Session exceeds 60 min without break?     [YES/NO] → If YES: decay risk HIGH
Close segment squeezed below 5 min?       [YES/NO] → If YES: peak-end risk HIGH
Expectation check planned mid-session?    [YES/NO] → If NO: recommend adding one
Written artifact promised during session? [YES/NO] → If NO: decay accelerates post-session
Follow-up touchpoint within 72 hours?     [YES/NO] → If NO: verbal commitments will fade
```

**Decay mitigation recommendations:**
- If session > 60 min: add a break OR a physical engagement move at the midpoint
- If close is squeezed: protect it by cutting content, not the close
- If no written artifact: recommend Tim send a 1-page "What We Covered" within 24 hours
- If no follow-up planned: flag this — expectations made verbally decay in 72 hours

## Output Rules

- **Be blunt.** "This won't fit" beats diplomatic hedging.
- **Be specific.** "Cut Concept 4 entirely, saves 12 min" not "consider trimming."
- **Protect non-negotiables:** opening hook, expectation declaration, close/CTA, and any Q&A end-slot.
- **Always calculate buffer.**
- **Flag the close.** If the close is the thing getting squeezed, that's the worst-case peak-end failure.

## What This Skill Does NOT Do

- Design the session (use session-architect)
- Suggest new content (only recommends cuts/expansions)
- Handle variable audience size or room chaos
