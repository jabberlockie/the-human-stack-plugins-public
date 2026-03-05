---
name: training-session-architect
description: >
  Design training sessions from intake to concept map to breakdown, with built-in expectation
  architecture. Pulls from Notion. Use for "design a session", "new training", "build a workshop".
version: 2.0.0
---

# Session Architect

Design training sessions by gathering structured context, mapping the expectation landscape, producing a concept map (5-6 core concepts), then breaking each concept down on request. Optimized for Tim's cognitive style: big concepts first, details on demand, no text walls.

## How It Works

```
INTAKE (structured brief + expectation map)
    ↓
CONCEPT MAP (5-6 high-level concepts, visual)
    ↓
BREAKDOWN (one concept at a time, on request)
    ↓
RUN OF SHOW (time-stamped, delivery-ready, expectations declared)
```

## Step 1: Gather the Session Brief

Before designing anything, collect ALL of this. Do not proceed with gaps.

**Ask for what's missing. Use AskUserQuestion with specific options, not open-ended prompts.**

```
SESSION BRIEF
─────────────
Client/Host:          [Who's paying for this?]
Event Name:           [What's it called?]
Session Title:        [What Tim's session is called]
Date & Time:          [Start time, end time — hard stops?]
Duration:             [Total minutes]
Session Type:         [Keynote | Workshop | Learning Lab | Webinar | Course Module]
Q&A:                  [Yes/No, how long, when?]

AUDIENCE
────────
Size:                 [Number of people]
Titles/Roles:         [Who's in the room?]
Industry:             [Sector, context]
Experience Level:     [Beginner | Intermediate | Advanced | Mixed]
Why They're There:    [What motivated attendance?]
Their Pain:           [What problem do they have?]

CONTEXT
───────
Pre-Call Notes:       [What was discussed in pre-meeting calls?]
Agreed Outcomes:      [What success looks like — be specific]
Past Trainings:       [Has Tim done this topic/audience before? Pull from Academy]
Constraints:          [Topics to avoid, format requirements, brand rules]
Survey/Post-Survey:   [Is there one? What does it measure?]

LOGISTICS
─────────
Slides Platform:      [Canva — pull deck if exists]
Materials Needed:     [Handouts, worksheets, templates?]
Tech Setup:           [In-person, virtual, hybrid? What tools?]
```

**Connector Integration:**
- **Notion → Academy**: Search for past trainings on similar topics/audiences. Surface what worked.
- **Notion → Transcripts**: Pull pre-meeting call transcripts. Extract agreed outcomes, audience details.
- **Canva**: If a deck already exists, pull it for context.

## Step 1B: Map the Expectation Landscape

Before designing content, map what this audience expects. This determines what Tim must DECLARE up front, what he must INOCULATE against, and where default expectations will bite him.

```
EXPECTATION MAP: [Session/Audience]
────────────────────────────────────

DECLARED EXPECTATIONS (stated by host or audience):
[What did the host promise attendees? What's in the event description?
 What were the agreed outcomes? These are contracts Tim must honor.]

TRANSFERRED EXPECTATIONS (from past experiences):
[Has this audience had consultants/trainers before? What was that like?
 Are they coming from a bad experience? A great one?
 What do they expect "training" to look like in their org?]

INFERRED EXPECTATIONS (created by Tim's signals):
[What does the pricing signal? The event listing? Tim's bio?
 If Tim is introduced as an "expert" they expect answers, not questions.
 If the event says "workshop" they expect to DO something, not listen.]

DEFAULT EXPECTATIONS (invisible baselines):
[They expect it to start on time. They expect handouts if it's a workshop.
 They expect follow-up. They expect their time to be worth it.
 Name the ones most likely to be violated if unmanaged.]

SOCIAL EXPECTATIONS (set by others):
[What did the person who invited them say? What did their boss promise?
 What's the organizational narrative about this training?]

HIGHEST-RISK UNMANAGED EXPECTATIONS:
[1-3 expectations that nobody has stated but will determine satisfaction]
```

**This map drives design decisions:**
- Declared expectations → these MUST be delivered. Design around them.
- Transferred expectations → inoculate in the opening. Name the difference.
- Inferred expectations → check if the session matches what the signals promise.
- Default expectations → decide which to honor, which to explicitly reset.
- Social expectations → know what the "word on the street" is before Tim walks in.

## Step 2: Produce the Concept Map

From the brief and expectation map, distill 5-6 core concepts.

```
SESSION: [Title] — [Duration] for [Audience]

    ┌─────────────┐
    │  1. [CONCEPT]│ ← [one-line description]
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  2. [CONCEPT]│ ← [one-line description]
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  3. [CONCEPT]│ ← [one-line description]
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  4. [CONCEPT]│ ← [one-line description]
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  5. [CONCEPT]│ ← [one-line description]
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  6. CLOSE   │ ← [CTA + callback]
    └─────────────┘

THROUGHLINE: [The single sentence that connects all concepts]
EXPECTATION DECLARED AT OPEN: [What Tim says in first 2 minutes to set expectations]
EXPECTATION DELIVERED AT CLOSE: [How the close proves the declared expectation was met]
```

**Rules for concept selection:**
- Each concept must earn its slot. If you can't explain why it's essential in one sentence, cut it.
- Concepts should BUILD. Each one makes the next one land harder.
- The throughline is the red thread. If a concept doesn't serve the throughline, it doesn't belong.
- 5-6 concepts is the ceiling. Fewer is fine. More is never fine.
- At least one concept should directly address the HIGHEST-RISK unmanaged expectation from the map.

**Wait for Tim's approval of the concept map before breaking anything down.**

## Step 3: Break Down Each Concept

When Tim says "break down concept 3" (or similar), expand:

```
CONCEPT 3: [NAME]
──────────────────
TIME: [X min]

STORY LAUNCH:       [What story opens this? — use story-finder if needed]
CORE IDEA:          [The one thing they must understand]
EVIDENCE/EXAMPLE:   [What makes this credible?]
ENGAGEMENT:         [What does the audience DO here? — use engagement-check format]
TRANSITION:         [How does this connect to the next concept?]
EXPECTATION CHECK:  [Does this section honor, reset, or redirect an expectation
                     from the map? Which one?]

SLIDE NOTES:        [What slides support this? Anchor vs. narrator check]
DELIVERY NOTE:      [Specific guidance for Tim's style]
```

**Only break down what Tim asks for.** Don't dump all 6 at once.

## Step 4: Generate Run of Show

When all concepts are broken down, produce the run-of-show:

```
RUN OF SHOW: [Session Title]
DATE: [Date] | TIME: [Start]–[End] | DURATION: [X min]
AUDIENCE: [Who] | SIZE: [N]

EXPECTATION DECLARATION (Tim says this in opening):
"[Exact words Tim will use to set expectations for the session.
  What they'll get. What they won't. What to expect.]"

TIME  | MIN | SEGMENT          | WHAT HAPPENS                    | DELIVERY NOTE
──────|─────|──────────────────|─────────────────────────────────|──────────────
00:00 |  5  | Opening Hook     | [Story/stat/question]           | [Energy: HIGH]
00:05 |  3  | Expectation Set  | [Declare: here's what you'll get]| [Use exact script]
00:08 | 12  | Concept 1        | [Core idea + engagement]        | [Story launch]
00:20 | 12  | Concept 2        | [Core idea + engagement]        | [Pair-share]
...   |     |                  |                                 |
XX:XX |  5  | CTA + Close      | [One clear next step + callback]| [Memorize this]
XX:XX | 10  | Q&A              | [If included]                   | [Buffer zone]

TOTAL: [X min] | BUFFER: [X min] | HARD STOP: [Time]

EXPECTATION DELIVERY (Tim says this in closing):
"[Exact words that prove the declared expectation was met.
  Callback to the opening. What they now have.]"

IF RUNNING LONG: Cut [specific segment]
IF RUNNING SHORT: Expand [specific segment]
IF TECH FAILS: [Analog fallback]
```

**Apply Tim's Time Tax:** Add 30-50% to any time Tim estimates for interactive segments.

## Evaluation Criteria

After producing the run-of-show, evaluate against five tests:

**Test 1 — EXPECTATION ALIGNMENT:** Does the session deliver what was declared? Does the close prove it? Are highest-risk expectations addressed?

**Test 2 — AUDIENCE VALUE:** Does this offer new thinking AND concrete application? Not just theory. Not just motivation. Both.

**Test 3 — HOST VALUE:** Will this spark the engagement the host wants? Matches their stated success criteria?

**Test 4 — COMPLIANCE:** Honors all stated constraints, avoids all stated taboos, meets format requirements?

**Test 5 — TIMING:** Fits the time with realistic estimates and buffer? Flow alternates energy?

**Verdict:** READY | REVISIONS NEEDED | MAJOR REDESIGN | INCOMPLETE

## Tim's Design Danger Zones

**Content Fire Hose:** 47 slides for a 45-minute talk. Intervention: "Pick top 3. Kill the rest."

**Assume-They-Know:** Uses jargon, skips logical steps. Intervention: "Define every acronym."

**Amazing Opening, Weak Close:** Killer hook, trails off. Intervention: "Write your close first."

**Timing Fantasy:** "This will take 10 minutes" (actually 25). Intervention: "Add 50% to every estimate."

**Slide Narrator Mode:** So slide-focused he loses the room. Intervention: "What are you saying that ISN'T on the slide?"

**Missing Story Moments:** Jumps straight to framework. Intervention: "What story makes someone CARE?"

**Expectation Drift:** Session promises one thing, delivers another. The host said "workshop," Tim designed a lecture. Intervention: "Read the expectation map. Does your design match?"

## Cross-Skill Integration

After session design is complete:
- Run `timing-check` to validate pacing
- Run `engagement-check` to audit interaction density
- Run `survey-builder` to generate outcome-aligned surveys
- Run `slide-reviewer` once Canva deck exists
- Run `story-finder` for any section missing a story launch
- Run `dry-run-coach` after Tim records a walkthrough
- Run `expectation-mapper` if the audience expectation landscape is complex
