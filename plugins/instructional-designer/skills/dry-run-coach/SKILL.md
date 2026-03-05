---
name: dry-run-coach
description: Analyze recorded session walkthrough against run-of-show. Feedback on pacing, stories, energy, riffs. Use for "dry run feedback", "coach my rehearsal".
---

# Dry-Run Coach Skill

## Purpose
Deliver structured, actionable coaching feedback on a session walkthrough by comparing what was delivered against the planned run-of-show. Focus on execution, pacing, engagement, and delivery mechanics.

## Inputs Required
1. **Walkthrough Transcript** — The recorded walkthrough (pasted text, uploaded file, or transcription service output)
2. **Run-of-Show / Session Plan** — The planned agenda with timing, story moments, and engagement activities

## Analysis Framework

### 1. TIMING vs PLAN
Create a segment-by-segment comparison table showing planned duration, actual time spent, delta, and verdict.

### 2. STORY MOMENTS
For each section that should include a story per the session design:
- Did Tim actually tell a story?
- Was it the planned story or a different one?
- Did it land and connect to the concept, or did it drift?
- Flag sections where Tim skipped the story entirely.

### 3. ENERGY ARC
Map Tim's energy qualitatively through the transcript:
- Where did language become more animated or varied? (HIGH energy)
- Where did he fall into monotone explanation? (LOW energy)
- Where did filler words increase? (UNCERTAINTY)
- Where did he speed up? (RUSHING)

Plot as a simple visual arc with minute markers.

### 4. OFF-SCRIPT RIFFS
Flag moments where Tim improvised beyond the plan. Rate each:
- **KEEP** — This was better than planned
- **CUT** — Cost time without adding value
- **REFINE** — Good idea but needs tightening

### 5. ENGAGEMENT EXECUTION
Check each planned interaction:
- Did Tim execute it?
- Was the prompt clear?
- Did he allow adequate time?
- Flag skipped engagement moments (critical for session flow).

### 6. SLIDE-NARRATOR CHECK
Identify sections where Tim is clearly reading or describing slides instead of adding value beyond the visual.

## Output Template

```
DRY RUN FEEDBACK: [Session Title]
WALKTHROUGH LENGTH: [X min] vs PLANNED: [Y min]
OVERALL: [On track / Needs work / Major issues]

═══ TIMING ═══
SEGMENT              | PLANNED | ACTUAL  | DELTA  | VERDICT
[Table format as specified]

═══ STORY MOMENTS ═══
[Section name]: [Hit / Missed / Drifted] — [specific note]

═══ ENERGY ARC ═══
Min 0-5:   ████████░░ HIGH — [reason]
Min 5-12:  ██████░░░░ MEDIUM — [reason]
[Continue through transcript]

═══ OFF-SCRIPT RIFFS ═══
Min [X]: [Description] — [KEEP / CUT / REFINE], [explanation]

═══ ENGAGEMENT EXECUTION ═══
[Activity name] at min [X]: [EXECUTED / SKIPPED] — [specific note]

═══ SLIDE-NARRATOR ZONES ═══
Min [X-Y]: [Description of zone and recommendation]

═══ TOP 3 FIXES ═══
1. [Most important change — specific and actionable]
2. [Second most important]
3. [Third most important]
```

## Coaching Principles

- **Be direct.** Tim can handle honest feedback. "This section is boring" is more useful than "consider increasing energy."
- **Lead with time.** If the walkthrough is significantly over, nothing else matters until it fits.
- **Acknowledge what's working.** Tim needs to know what to KEEP doing, not just what to fix.
- **Honor good riffs.** Don't penalize improvisation that's an upgrade to the plan.
- **Top 3 Fixes is the payload.** Tim won't remember 15 notes. Give him 3 that matter.
- **Be specific.** Vague feedback ("more energy") is coaching malpractice. Say exactly what to change and why.

## Triggering Phrases
- "review my dry run"
- "give me feedback on my walkthrough"
- "dry run feedback"
- "coach my rehearsal"
