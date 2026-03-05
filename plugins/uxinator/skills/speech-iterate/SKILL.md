---
name: speech-iterate
description: Version and evolve a keynote across multiple deliveries. Tracks what works, what doesn't, and produces updated talk structures. CI/CD for speeches. Use for "update my talk", "iterate the keynote", "what should I change".
---

# Speech Iterate

Continuous improvement system for keynotes delivered multiple times. Tracks performance across deliveries, identifies what's working and what's not, and produces updated talk structures. This is CI/CD for speeches — each delivery is a deployment, each evaluation is a test suite, each iteration is a release.

## The Problem This Solves

Tim gives the same talk to different audiences. Without a system, he either:
1. Delivers the same version forever (stale)
2. Improvises changes each time with no tracking (inconsistent)
3. Rewrites from scratch when he should be refining (wasteful)

This skill creates a version history so Tim knows what to keep, what to cut, what to try, and what's proven.

## Talk Registry

Every keynote Tim gives gets a registry entry:

```
TALK REGISTRY
─────────────
TALK ID:        [Slug — e.g., "expectations-unplugged"]
TITLE:          [Current working title]
CORE ARGUMENT:  [One sentence]
THE ONE LINE:   [Current version of the repeatable line]
CURRENT VERSION: [v1.0, v1.1, v2.0, etc.]
TOTAL DELIVERIES: [N]

VERSION HISTORY:
┌─────────┬────────────┬──────────────────────┬───────┬───────────────────┐
│ VERSION │ DATE       │ EVENT                │ SCORE │ KEY CHANGE        │
├─────────┼────────────┼──────────────────────┼───────┼───────────────────┤
│ v1.0    │ [Date]     │ [Event name]         │ [/50] │ Initial delivery  │
│ v1.1    │ [Date]     │ [Event name]         │ [/50] │ [What changed]    │
│ v2.0    │ [Date]     │ [Event name]         │ [/50] │ [Major rework]    │
└─────────┴────────────┴──────────────────────┴───────┴───────────────────┘
```

## Version Numbering

- **v1.0** → First delivery
- **v1.X** → Minor iterations (adjusted timing, refined a story beat, swapped a data point)
- **vX.0** → Major iterations (new anchor story, restructured arc, changed core argument)

## Iteration Process

### Step 1: Collect Evaluation Data

Pull from speech-evaluate output. If multiple evaluations exist, compare across them.

```
CROSS-DELIVERY COMPARISON: [Talk ID]
──────────────────────────────────────

                    │ v1.0         │ v1.1         │ v1.2
────────────────────│──────────────│──────────────│──────────────
PROVOCATION SCORE   │ [/10]        │ [/10]        │ [/10]
ARC SCORE           │ [/10]        │ [/10]        │ [/10]
CLOSE SCORE         │ [/10]        │ [/10]        │ [/10]
MODE DISCIPLINE     │ [/10]        │ [/10]        │ [/10]
AUDIENCE SHIFT      │ [/10]        │ [/10]        │ [/10]
────────────────────│──────────────│──────────────│──────────────
TOTAL               │ [/50]        │ [/50]        │ [/50]
────────────────────│──────────────│──────────────│──────────────
AUDIENCE TYPE       │ [Who]        │ [Who]        │ [Who]
DURATION            │ [Min]        │ [Min]        │ [Min]
NOTABLE             │ [What worked │ [What worked │ [What worked
                    │  or failed]  │  or failed]  │  or failed]
```

### Step 2: Identify Patterns

```
WHAT ALWAYS WORKS (keep — these are proven):
1. [Element] — Worked in [N/N] deliveries. Evidence: [specific]
2. [Element] — Worked in [N/N] deliveries.

WHAT NEVER WORKS (cut — these are disproven):
1. [Element] — Failed in [N/N] deliveries. Evidence: [specific]
2. [Element] — Failed in [N/N] deliveries.

WHAT'S INCONSISTENT (test — need more data):
1. [Element] — Worked for [audience type], failed for [other type]
2. [Element] — Worked at [duration], failed at [other duration]

WHAT'S UNTESTED (consider for next version):
1. [Idea from evaluation feedback]
2. [Alternative story/data point/close]
```

### Step 3: Produce the Next Version

```
ITERATION PLAN: [Talk ID] v[X.X] → v[Y.Y]
──────────────────────────────────────────

CHANGES:
┌────────────────────┬─────────────────────┬───────────────────────────┐
│ SECTION            │ CURRENT (v[X.X])    │ NEXT (v[Y.Y])             │
├────────────────────┼─────────────────────┼───────────────────────────┤
│ Hook               │ [Current]           │ [Change or KEEP]          │
│ Story setup        │ [Current]           │ [Change or KEEP]          │
│ Turn               │ [Current]           │ [Change or KEEP]          │
│ Peak               │ [Current]           │ [Change or KEEP]          │
│ Close              │ [Current]           │ [Change or KEEP]          │
│ The one line       │ [Current]           │ [Change or KEEP]          │
└────────────────────┴─────────────────────┴───────────────────────────┘

RATIONALE: [Why these changes, based on data]

RISK: [What could go wrong with the changes? What's the fallback?]

TEST HYPOTHESIS: [What specific thing are we testing in this version?
                   E.g., "Does the new close line get more approach-rate
                   responses than the original?"]
```

### Step 4: Update Talk Structure

Produce a fresh talk structure (using speech-design format) incorporating the changes. Tag it with the new version number.

## Audience-Specific Adaptation

Some talks get adapted for different audiences without changing the core argument. Track these as branches:

```
AUDIENCE ADAPTATIONS: [Talk ID]
────────────────────────────────
BASE VERSION: v[X.X]

ADAPTATION       │ AUDIENCE TYPE    │ WHAT CHANGES             │ WHAT STAYS
─────────────────│──────────────────│──────────────────────────│──────────
[Talk]-nonprofit │ Nonprofit leaders│ [Specific swaps]         │ Core argument,
                 │                  │                          │ anchor story
[Talk]-tech      │ Tech partners    │ [Specific swaps]         │ Core argument
[Talk]-short     │ Any (20 min)     │ [What gets cut for time] │ Core argument,
                 │                  │                          │ close
```

## Talk Retirement Criteria

A talk should be retired or fundamentally rebuilt when:
- Score plateaus below 35/50 for 3+ deliveries
- The core argument has been absorbed by the market (no longer surprising)
- Tim is bored delivering it (his energy drops → audience energy drops)
- The data points are stale
- A better version of the argument exists in a newer talk

## Cross-Skill Integration

- **From speech-evaluate**: Every evaluation feeds this skill's data
- **Into speech-design**: Major version changes trigger a redesign pass
- **Into speech-rehearse**: New versions need rehearsal before delivery
- **With thought-leadership-librarian**: Track which concepts resonate across audiences — feeds IP development

## Triggers

- "update my talk"
- "iterate the keynote"
- "what should I change"
- "speech iterate"
- "version my talk"
- "next version of [talk name]"
- "how has this talk evolved"

## What This Skill Does NOT Do

- Evaluate a single delivery (use speech-evaluate)
- Design a new talk from scratch (use speech-design)
- Coach delivery (use speech-rehearse)
- Track training or strategy iterations (different delivery modes, different criteria)
