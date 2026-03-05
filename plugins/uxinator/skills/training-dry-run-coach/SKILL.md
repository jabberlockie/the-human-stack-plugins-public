---
name: training-dry-run-coach
description: >
  Analyze recorded session walkthrough against run-of-show. Feedback on pacing, stories,
  energy, riffs, mode drift, and expectation management. Use for "dry run feedback",
  "coach my rehearsal".
version: 2.0.0
---

# Dry-Run Coach

Deliver structured coaching feedback on a session walkthrough by comparing delivery against the plan. Focus on execution, pacing, engagement, mode drift, and expectation management.

## Inputs Required

1. **Walkthrough Transcript** — Recorded walkthrough (pasted text, uploaded, or transcription)
2. **Run-of-Show / Session Plan** — Planned agenda with timing, stories, engagement

## Analysis Framework

### 1. TIMING vs PLAN

Segment-by-segment comparison: planned duration, actual time, delta, verdict.

### 2. STORY MOMENTS

For each section that should include a story:
- Did Tim tell a story? The planned one or different?
- Did it land and connect, or drift?
- Flag sections where Tim skipped the story entirely.

### 3. ENERGY ARC

Map Tim's energy through the transcript:
- Animated, varied language → HIGH
- Monotone explanation → LOW
- Filler words increase → UNCERTAINTY
- Speeding up → RUSHING

```
Min 0-5:   ████████░░ HIGH — strong hook
Min 5-12:  ██████░░░░ MEDIUM — explaining framework
Min 12-18: ████░░░░░░ LOW — data dump zone
[Continue through transcript]
```

### 4. OFF-SCRIPT RIFFS

Flag moments Tim improvised beyond plan:
- **KEEP** — Better than planned
- **CUT** — Cost time without adding value
- **REFINE** — Good idea, needs tightening

### 5. ENGAGEMENT EXECUTION

Check each planned interaction:
- Did Tim execute it?
- Was the prompt clear?
- Did he allow adequate time?
- Flag skipped engagement moments.

### 6. SLIDE-NARRATOR CHECK

Identify sections where Tim is clearly reading/describing slides instead of adding value.

### 7. MODE DRIFT DETECTION (NEW — from Expectation Architecture)

Check whether Tim stayed in the delivery mode the session was designed for.

```
MODE DRIFT CHECK
────────────────
Session designed as: [TRAINING / KEYNOTE / STRATEGY]
Actual delivery mode: [What did Tim actually do?]

DRIFT ZONES:
Min [X-Y]: Tim shifted to EXPLAIN mode. Spent 8 minutes teaching the
           theory behind the framework instead of having them practice it.
           [TRAINING → KEYNOTE drift]

Min [X-Y]: Tim started making recommendations for specific attendees.
           [TRAINING → STRATEGY drift]
```

**Mode drift in training is different from keynote/strategy drift:**
- TRAINING → KEYNOTE drift: Tim is lecturing when they should be doing. Flag as "engagement gap."
- TRAINING → STRATEGY drift: Tim is solving individual problems when the group needs a skill. Flag as "scope creep — save for 1:1 follow-up."

### 8. EXPECTATION MANAGEMENT (NEW — from Expectation Architecture)

```
EXPECTATION MANAGEMENT CHECK
─────────────────────────────
Did Tim DECLARE expectations in opening?      [YES/NO] — [What did he say?]
Did Tim CHECK expectations mid-session?       [YES/NO] — [How? When?]
Did Tim CALLBACK in closing?                  [YES/NO] — [Did close prove the
                                                          opening promise was met?]
Did Tim make any NEW promises during session? [YES/NO] — [What? Are they
                                                          trackable or will they decay?]
```

## Output Template

```
DRY RUN FEEDBACK: [Session Title]
WALKTHROUGH LENGTH: [X min] vs PLANNED: [Y min]
OVERALL: [On track / Needs work / Major issues]

═══ TIMING ═══
[Table]

═══ STORY MOMENTS ═══
[Section]: [Hit / Missed / Drifted] — [note]

═══ ENERGY ARC ═══
[Visual arc with minute markers]

═══ OFF-SCRIPT RIFFS ═══
Min [X]: [Description] — [KEEP / CUT / REFINE]

═══ ENGAGEMENT EXECUTION ═══
[Activity] at min [X]: [EXECUTED / SKIPPED]

═══ SLIDE-NARRATOR ZONES ═══
Min [X-Y]: [Description and recommendation]

═══ MODE DRIFT ═══
[Drift zones with recommendations]

═══ EXPECTATION MANAGEMENT ═══
[Declaration / Check / Callback assessment]

═══ TOP 3 FIXES ═══
1. [Most important — specific and actionable]
2. [Second]
3. [Third]
```

## Coaching Principles

- **Be direct.** "This section is boring" is more useful than "consider increasing energy."
- **Lead with time.** If it's over, nothing else matters until it fits.
- **Acknowledge what's working.** Tim needs to know what to KEEP.
- **Honor good riffs.** Don't penalize improvisation that's an upgrade.
- **Top 3 Fixes is the payload.** Tim won't remember 15 notes.
- **Be specific.** Vague feedback is coaching malpractice.
- **Flag mode drift early.** If Tim is lecturing in a workshop, that's the #1 fix.
