---
name: training-survey-builder
description: >
  Generate pre/post/pulse surveys tied to learning outcomes and expectation alignment.
  Copy-ready for Nancy. Use for "build surveys", "create survey", "post-survey".
version: 2.0.0
---

# Survey Builder

Generate outcome-aligned surveys that measure learning, gather actionable feedback, and assess expectation alignment. Surveys are copy-ready for Nancy and tied to the session's agreed learning outcomes.

## Input Requirements

- Session brief with: agreed outcomes (3-4 specific, measurable), audience profile, session type/duration
- Session title and date
- Preferred survey platform (Google Forms, Typeform, etc.)
- Expectation map (if available from session-architect or expectation-mapper)

## Survey Types

### Pre-Survey (Before Session)

**Purpose:** Baseline knowledge, surface pain points, set expectations, gather material for Tim, AND discover what the audience expects before they walk in.

- 5-7 questions max
- Format mix: 1-2 scale, 2-3 multiple choice, 1-2 open-ended
- Content focus: current state, experience level, challenges, expectations

**Expectation Discovery Questions (include 1-2):**
- "What do you most hope to walk away with from this session?" (DECLARED expectations)
- "What has your experience been with similar trainings in the past?" (TRANSFERRED expectations)
- "What's your biggest concern about this session?" (UNMANAGED expectations / anxiety)

These feed directly into Tim's expectation map. Pre-survey responses = expectation audit data.

### Post-Survey (Within 24 Hours)

**Purpose:** Measure outcome achievement, capture takeaways, AND assess expectation alignment.

- 7-10 questions max
- Structure:
  - 1 NPS question (1-10: "How likely to recommend to a colleague?")
  - 2-3 outcome-specific questions (mirror agreed outcomes; scale 1-5)
  - 1-2 application questions ("What's one thing you'll do differently in 30 days?")
  - 1 best-moment question ("What was the most valuable part?")
  - 1 improvement question ("What would have made this more useful?")
  - 1 open-ended ("Anything else?")

**Expectation Alignment Questions (include 1-2):**
- "How well did this session match what you expected?" (Scale 1-5) — direct expectation disconfirmation measurement
- "Was there anything you expected to cover that we didn't?" (surfaces unmet DECLARED or DEFAULT expectations)
- "What surprised you about this session?" (surfaces where reality exceeded or violated expectations)

**Expectation Math:**
If pre-survey asked "What do you hope to walk away with?" and post-survey asks "How well did this match expectations?" — the delta IS the Emotion = Experience ± Expectations formula, measured.

### Mid-Session Pulse (Optional, Sessions > 90 min)

**Purpose:** Real-time temperature check to adjust pacing AND check expectation alignment.

- 2-3 questions max
- Quick format: emoji or 1-5 scale
- Content: pacing, clarity, expectation tracking

**Expectation Pulse:**
- "So far, is this session what you expected? (thumbs up / sideways / down)" — real-time monitoring operation

## Output Format

```
SURVEYS FOR: [Session Title] — [Date]
HAND OFF TO: Nancy
OUTCOMES MEASURED: [List 3-4 agreed outcomes]
EXPECTATIONS TRACKED: [Which expectation types are being surfaced]

═══════════════════════════════════════
PRE-SURVEY
Send: [X days before session]
Platform: [Google Forms / Typeform / etc.]
═══════════════════════════════════════

1. [Question text]
   Type: [Scale 1-5 / Multiple choice / Open-ended]
   Options: [If applicable]
   Measures: [Outcome or Expectation type]

...

═══════════════════════════════════════
POST-SURVEY
Send: [Within 24 hours of session]
═══════════════════════════════════════

1. [Question text]
   Type: [Scale / Open-ended]
   Maps to: [Which outcome or expectation]

...

═══════════════════════════════════════
MID-SESSION PULSE (if session > 90 min)
Deliver: [At what minute mark]
Method: [Show of hands / Poll tool / Chat]
═══════════════════════════════════════

1. [Question text]
   ...
```

## Rules

- **Outcome alignment:** Every post-survey question must map to a stated outcome or expectation.
- **Expectation pairing:** If the pre-survey asks about expectations, the post-survey MUST measure whether they were met. The pair creates measurable data.
- **Actionable data:** Pre-survey surfaces information Tim can use in-session.
- **Brevity:** Completable in 5 minutes or less.
- **Plain language:** No jargon. No double-barreled questions.
- **Timing & delivery:** Include "send by" timing and method for Nancy.
