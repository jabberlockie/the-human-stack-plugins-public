---
name: timing-check
description: Audit session timing with realistic estimates and Tim's time tax. Flags what to cut or expand. Use for "timing check", "will this fit".
---

# Timing-Check Skill

## Purpose
Reality-check a session plan or run-of-show against realistic time estimates. Tim chronically underestimates interactive segments, so this skill applies a "time tax" and flags what won't fit.

## Triggers
- "timing check"
- "check my timing"
- "will this fit"
- "time audit"

## Input
Tim's current run-of-show or session plan (can be pasted, linked, or referenced from session context).

## Core Behavior

### 1. Calculate Realistic Time
Apply **Tim's Time Tax**:
- Storytelling/examples: **+30%**
- Group exercises/pair-share: **+50%**
- Q&A segments: **+25%**
- Content delivery/demos: no adjustment (use as-is)

### 2. Generate Single-Table Audit
```
TIMING AUDIT: [Session Title] — [Allocated: X min]

SEGMENT              | PLANNED | REALISTIC | DELTA  | VERDICT
─────────────────────|─────────|───────────|────────|────────
Opening Hook         |   5 min |     5 min |   0    | OK
Roadmap              |   3 min |     3 min |   0    | OK
Concept 1 + discuss  |  12 min |    17 min |  +5    | OVER
Pair-share exercise  |  10 min |    15 min |  +5    | OVER
...                  |         |           |        |
─────────────────────|─────────|───────────|────────|────────
TOTAL                |  55 min |    72 min | +17    | WON'T FIT

HARD STOP: [Time] | BUFFER NEEDED: 5 min | ACTUAL BUFFER: -12 min
```

### 3. Diagnose & Recommend

**If timing fits:**
- Flag any segments with 0% buffer as "tight"
- Identify back-to-back dense segments
- Warn if the close is squeezed

**If timing is over:**
- Name exactly what to cut (with duration)
- Explain why that segment is the weakest or least critical
- Show revised total after cuts
- Calculate remaining buffer

**If timing is under:**
- Name exactly what to expand
- Explain why (weak close, weak opening, insufficient examples)
- Show revised total and where extra time goes

## Output Rules
- **Be blunt.** "This won't fit" beats diplomatic hedging.
- **Be specific.** "Cut Concept 4 entirely, saves 12 min" not "consider trimming."
- **Protect non-negotiables:** opening hook, close/CTA, and any Q&A end-slot.
- **Always calculate buffer:** Show how much breathing room remains after cuts.
- **Flag danger zones:** Hard stops with no buffer, weak closing segment, no Q&A protection.

## Example Output
```
CUT LIST (to get back on time):
1. Concept 4 demo — remove entirely, saves 12 min. Why: Weakest of three concepts, covered briefly in Concept 3 anyway.
2. Group debrief — cut from 8 min to 4 min, saves 4 min. Why: Can do quick popcorn share instead of full circle.

AFTER CUTS: 64 min content + 3 min buffer = 67 min (4 min under 71-min hard stop) ✓
```

## What This Skill Does NOT Do
- Design the session (only audits timing)
- Suggest new content (only recommends cuts/expansions)
- Handle variable audience size or room chaos (use as a planning baseline only)
