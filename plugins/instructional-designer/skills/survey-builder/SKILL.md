---
name: survey-builder
description: Generate pre/post/pulse surveys tied to learning outcomes. Copy-ready for Nancy. Use for "build surveys", "create survey", "post-survey".
---

## Overview

The survey-builder skill generates outcome-aligned surveys that measure learning and gather actionable feedback. Surveys are copy-ready for Nancy and tied directly to the session's agreed learning outcomes — not generic satisfaction surveys.

## Input Requirements

- Session brief with: agreed outcomes (3–4 specific, measurable), audience profile, session type/duration
- Session title and date
- Preferred survey platform (Google Forms, Typeform, etc.)

## Output

Copy-ready survey text with timing, delivery method, and outcome mappings.

## Survey Types

### Pre-Survey (Before Session)
**Purpose:** Baseline knowledge, surface pain points, set expectations, gather live material for Tim

- 5–7 questions max
- Format mix: 1–2 scale questions, 2–3 multiple choice, 1–2 open-ended
- Content focus: current state, experience level, specific challenges, hopes/expectations
- Always include: "What's your biggest question about [topic]?" — Tim uses this in-session

### Post-Survey (Within 24 Hours)
**Purpose:** Measure outcome achievement, capture takeaways, gather satisfaction feedback

- 7–10 questions max
- Structure:
  - 1 NPS question (1–10 scale: "How likely to recommend this session to a colleague?")
  - 2–3 outcome-specific questions (directly mirror agreed outcomes; scale 1–5)
  - 1–2 application questions ("What's one thing you'll do differently in the next 30 days?")
  - 1 best-moment question ("What was the most valuable part of this session?")
  - 1 improvement question ("What would have made this session more useful?")
  - 1 open-ended ("Anything else you'd like to share?")

### Mid-Session Pulse (Optional, Sessions > 90 min)
**Purpose:** Real-time temperature check to adjust pacing/clarity on the fly

- 2–3 questions max
- Quick format: emoji or 1–5 scale
- Content: pacing ("too fast / just right / too slow"), clarity, energy/engagement

## Output Format

```
SURVEYS FOR: [Session Title] — [Date]
HAND OFF TO: Nancy
OUTCOMES MEASURED: [List 3–4 agreed outcomes mapped by these surveys]

═══════════════════════════════════════
PRE-SURVEY
Send: [X days before session]
Platform: [Google Forms / Typeform / etc.]
═══════════════════════════════════════

1. [Question text]
   Type: [Scale 1–5 / Multiple choice / Open-ended]
   Options: [If applicable]

2. [Question text]
   ...

═══════════════════════════════════════
POST-SURVEY
Send: [Within 24 hours of session]
═══════════════════════════════════════

1. [Question text]
   Type: [Scale 1–10 / Scale 1–5 / Open-ended]
   Options: [If applicable]
   Maps to outcome: [Which agreed outcome this measures]

2. [Question text]
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

- **Outcome alignment:** Every post-survey question must map to a stated outcome. No questions that don't measure something agreed upon.
- **Actionable data:** Pre-survey should surface information Tim can use in the session — not data collection for its own sake.
- **Brevity:** Surveys must be completable in ≤5 minutes. Short surveys get higher response rates.
- **Plain language:** No jargon. No double-barreled questions. Clear, direct wording.
- **Timing & delivery:** Include "send by" timing and delivery method. Nancy needs to know WHEN and HOW.

## Triggers

- "build surveys"
- "create survey"
- "post-survey"
- "pre-survey"
- "what should the survey say"
