---
name: strategy-evaluate
description: Post-delivery retrospective — did the strategy experience manage expectations and land as intended? Reviews transcripts, notes, and client signals against what was planned. Use for "how did that go", "evaluate my session", "strategy eval".
---

# Strategy Evaluate

Post-delivery retrospective that assesses whether a strategy session managed expectations effectively and delivered what the context demanded. Compares what was planned against what actually happened, and what the client expected against what they experienced.

## When To Use

After any strategy delivery — client call, diagnostic readout, advisory session, managed success check-in. The sooner after delivery the better, while signals are fresh.

## Input Types

- **Call transcript or notes** (primary) — what actually happened
- **Session agenda/outline** (if available) — what was planned
- **JTBD analysis** (if available) — what the client expected
- **Strategy-audit output** (if run pre-delivery) — what was flagged as risk
- **Strategy-architect output** (if used) — what deliverables were designed
- **Client follow-up signals** — emails, Slack messages, next meeting requests, silence

## Step 1: Reconstruct the Expectation Landscape

```
EXPECTATION LANDSCAPE: [Client] — [Session Date]
───────────────────────────────────────────────────

WHAT WAS THE SESSION SUPPOSED TO DO?
[Pull from agenda, strategy-audit, or strategy-architect if available.
 If not available, reconstruct from transcript opening.]

WHAT DID THE CLIENT EXPECT?
[Pull from JTBD desired outcome. If no JTBD, infer from:
 - Questions they asked early in the session
 - Statements about what they hoped to get
 - Transferred expectations from their history]

WHAT DID TIM EXPECT TO DELIVER?
[Pull from agenda or pre-session notes. If unavailable, infer from
 how Tim opened the session.]

EXPECTATION ALIGNMENT AT START:
[Were Tim's expectations and client's expectations aligned?
 Misaligned? Unknown to each other?]
```

## Step 2: Mode Analysis

```
MODE PERFORMANCE
────────────────
REQUIRED MODE:     [KEYNOTE | TRAINING | STRATEGY]
ACTUAL MODE:       [What Tim actually did — may shift across segments]

MODE MAP:
TIME/SECTION        | MODE      | ON TARGET? | NOTES
────────────────────|───────────|────────────|──────────────
[Opening 0-5 min]   | [mode]    | ✓ or ✗    | [what happened]
[Section 1]         | [mode]    | ✓ or ✗    | [what happened]
[Section 2]         | [mode]    | ✓ or ✗    | [what happened]
[Close]             | [mode]    | ✓ or ✗    | [what happened]

TIME IN CORRECT MODE:  [X]%
TIME IN WRONG MODE:    [X]%
DOMINANT DRIFT TYPE:   [EXPLAIN | PROVOKE | other]
```

## Step 3: Expectation Outcome Map

For each expectation identified, assess whether it was met:

```
EXPECTATION OUTCOMES
────────────────────
┌─────────────────────────────┬──────────┬────────────┬──────────────┐
│ EXPECTATION                 │ ORIGIN   │ MET?       │ EVIDENCE     │
├─────────────────────────────┼──────────┼────────────┼──────────────┤
│ [Client expected X]         │ DECLARED │ YES/NO/    │ [Quote or    │
│                             │          │ PARTIALLY  │  signal]     │
│ [Client expected Y]         │ DEFAULT  │ YES/NO/    │ [Quote or    │
│                             │          │ PARTIALLY  │  signal]     │
│ [Client expected Z]         │ TRANSFER │ YES/NO/    │ [Quote or    │
│                             │          │ PARTIALLY  │  signal]     │
└─────────────────────────────┴──────────┴────────────┴──────────────┘

EXPECTATIONS MET:      [N of N]
EXPECTATIONS UNMET:    [N] — [which ones]
EXPECTATIONS EXCEEDED: [N] — [which ones, if any]
NEW EXPECTATIONS CREATED: [What expectations now exist for the NEXT session?]
```

## Step 4: Emotional Math

Apply the UX² formula: Emotion = Experience ± Expectations

```
EMOTIONAL MATH
──────────────
EXPERIENCE QUALITY: [How good was the actual delivery? HIGH | MEDIUM | LOW]

EXPECTATION CALIBRATION:
- Expectations were [TOO HIGH | CALIBRATED | TOO LOW] relative to experience
- This means the emotional outcome was likely: [DISAPPOINTMENT | SATISFACTION | DELIGHT]

PEAK MOMENT: [What was the most intense moment? Was it positive or negative?]
END MOMENT:  [How did the session end? Strong close or trail-off?]
PEAK-END PREDICTION: [Based on peak + end, what will the client REMEMBER?]

ASYMMETRY CHECK: [Were any unmet expectations in the "2x hurt" zone?
                   E.g., they expected a deliverable and got a conversation]
```

## Step 5: Client Signals

```
POST-SESSION SIGNALS
────────────────────
IMMEDIATE SIGNALS (during or right after):
- [Quote/behavior — e.g., "This is really helpful" vs. "I need to think about this"]
- [Engagement level — asking follow-up questions? Going quiet?]
- [Action signals — "let's schedule the next one" vs. no mention of next steps]

FOLLOW-UP SIGNALS (hours/days after):
- [Email response time and tone]
- [Did they share materials with their team?]
- [Did they ask for the recording/notes?]
- [Did they schedule the next session proactively?]
- [Silence — how long? Silence after strategy = red flag]

SIGNAL INTERPRETATION:
[What do these signals suggest about whether expectations were met?]
```

## Step 6: Verdict and Actions

```
SESSION VERDICT
═══════════════
OVERALL: [EXPECTATIONS MET | PARTIALLY MET | EXPECTATIONS MISSED]

WHAT WORKED:
1. [Specific moment/deliverable that landed — with evidence]
2. [Specific moment that managed expectations well]

WHAT DIDN'T:
1. [Specific gap — with evidence and what it cost]
2. [Specific drift moment — what should have happened instead]

DANGER ZONE TRIGGERS:
[Which of Tim's danger zones activated? Professor Trap? Options Buffet?
 Insight Without Artifact? Be specific.]

FOR NEXT SESSION:
1. DECLARE: [What expectation to explicitly set at the start]
2. INOCULATE: [What transferred/default expectation to address proactively]
3. DELIVER: [What artifact/deliverable the client needs to receive]
4. AVOID: [What mode drift to watch for]
5. CLOSE WITH: [How to end — specific, not "end strong"]

EXPECTATION DEBT:
[What expectations from THIS session are now carried forward as obligations?
 E.g., "Rob expects benchmarks next time. Abagail expects a guidance
 framework draft. These are now DECLARED expectations — unmet = 2x hurt."]
```

## Expectation Debt Tracking

This is the most critical output. Every session creates expectations for the next one. Untracked expectation debt compounds.

```
EXPECTATION DEBT LEDGER: [Client]
──────────────────────────────────
SESSION    │ EXPECTATION CREATED           │ STATUS          │ DUE BY
───────────│───────────────────────────────│─────────────────│──────────
[Date 1]   │ [What was promised/implied]   │ OPEN | PAID     │ [Date]
[Date 1]   │ [What was promised/implied]   │ OPEN | PAID     │ [Date]
[Date 2]   │ [What was promised/implied]   │ OPEN | PAID     │ [Date]

TOTAL OPEN DEBT: [N items]
HIGHEST RISK: [Which unmet expectation will hurt most if not addressed?]
```

## Evaluation Criteria

Rate the session on five dimensions:

```
STRATEGY DELIVERY SCORECARD
────────────────────────────
MODE ALIGNMENT:      [1-10] Did Tim stay in the right mode?
EXPECTATION MGMT:    [1-10] Were expectations set, monitored, met?
DELIVERABLE QUALITY: [1-10] Did the client receive a useful artifact?
FOLLOW-THROUGH:      [1-10] Clear next steps, ownership, timeline?
PEAK-END QUALITY:    [1-10] Will the client remember this positively?

OVERALL:             [X/50]

TREND: [If previous evaluations exist: improving, declining, or stable?]
```

## Cross-Skill Integration

- **After strategy-audit**: Compare pre-delivery predictions against actual performance
- **After strategy-architect**: Did the designed deliverable actually get delivered? Was it useful?
- **Into JTBD analysis**: Evaluation insights feed back into understanding this client's evolving jobs
- **Into thought-leadership-librarian**: Pattern-level insights (e.g., "diagnostic readouts consistently drift to explain mode") become concept candidates

## Triggers

- "how did that go"
- "evaluate my session"
- "strategy eval"
- "did that land"
- "session review"
- "what did I miss"
- "expectation check"

## What This Skill Does NOT Do

- Detect drift in advance (use strategy-audit)
- Build deliverables (use strategy-architect)
- Evaluate training or keynote sessions (those have different criteria — use instructional-designer or speechwriter evaluate)
- Replace asking the client directly how it went (always do both)
