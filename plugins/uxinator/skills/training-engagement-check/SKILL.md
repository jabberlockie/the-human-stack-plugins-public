---
name: training-engagement-check
description: >
  Audit session for passive stretches, energy gaps, and expectation-checking moments.
  Flags problems with exact scripted questions and timers.
  Use for "engagement check", "energy audit", "is this interactive enough".
version: 2.0.0
---

# Engagement Check

Audit a session plan or run-of-show for engagement gaps, energy problems, and missing expectation-check moments. For every flagged issue, output an actionable fix with exact words Tim can say and a timer.

## Input

Pass a session plan, run-of-show, transcript, or outline. Include timestamps or time markers.

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
- Questions are calibrated to his High I style — designed to give the room something to give HIM so he can riff.
- Timers are mandatory because Tim will either cut it short (impatience) or let it run long (he got interested).

**For Balance:**
- Flag sections where he's so interaction-heavy there's no space to land a concept.
- Target: 3-4 interactive moments per 30 minutes, varied in type.

## Expectation Architecture Integration

### Expectation-Checking Engagement Moves

Beyond standard engagement, flag opportunities for Tim to CHECK whether the audience's expectations are being met during the session. These are expectation monitoring operations disguised as interaction.

**Expectation Check Move — "Is This Landing?"**
Use at: ~25% into session (after first major concept)
```
SAY THIS: "Quick pulse check — on a scale of 1 to 5, hold up your fingers:
how well does what we've covered so far match what you expected when you
walked in? Don't overthink it. Just a gut number."
TIMER: 30 sec
PURPOSE: Surfaces expectation alignment early enough to course-correct.
IF LOW (lots of 1-2s): Tim needs to address the gap. "Okay, I see some
low numbers. Tell me — what were you expecting that we haven't hit yet?"
IF HIGH (lots of 4-5s): Confirm and continue. "Good. We're tracking."
```

**Expectation Redirect Move — "Let Me Reset"**
Use at: When Tim detects drift (audience disengaged, wrong questions)
```
SAY THIS: "I want to pause for a second. I promised you [declared expectation
from opening]. Let me check — are we on track for what you need? Raise your
hand if you want me to go deeper on [current topic]. Keep it down if you'd
rather I move to [next topic]."
TIMER: 30 sec
PURPOSE: Real-time expectation redirect. Prevents Tim from pushing content
the room doesn't need.
```

**Peak-End Awareness**
Flag the session's peak moment and closing moment. If neither is designed for interaction, flag it:
- The PEAK moment (most intense) should include audience participation — it's what they'll remember.
- The CLOSE should include a declared callback — "Remember when I said [opening expectation]? Here's what you now have."

### Engagement Audit Additions

Add to the summary section:

```
EXPECTATION CHECKS: [X planned] — target is 1-2 per session
PEAK MOMENT: [Is it interactive?] YES/NO — [If no, flag as risk]
CLOSE MOMENT: [Does it callback to declared expectation?] YES/NO
```

## "Say This" Question Design Principles

- **Short setup, specific ask.** Not "what do you think about X?" but "what's ONE thing that..."
- **Physical engagement when possible.** Raise hand, stand up, turn to neighbor.
- **Surface experience, not knowledge.** "Tell me a time when..." not "Who can define..."
- **Give Tim material to riff.** Responses should create moments he can improvise from.
- **Avoid put-on-the-spot.** Never call someone by name cold.
- **Vary the type.** Pair-share, full-room poll, shout-out, think-then-share, show of hands.

## Engagement Toolkit

Load `references/engagement-toolkit.md` for the full library of 10 engagement move types with "Say This" templates and timing.

## Summary Section

```
ENGAGEMENT SCORE: [X/10]
PASSIVE STRETCHES: [N flagged]
INTERACTION DENSITY: [X interactions per 30 min — target is 3-4]
ENERGY ARC: [Describe the shape — front-loaded? flat? builds? dips?]
EXPECTATION CHECKS: [X planned — target 1-2]
PEAK MOMENT INTERACTIVE: [YES/NO]
CLOSE CALLBACKS DECLARED: [YES/NO]
```
