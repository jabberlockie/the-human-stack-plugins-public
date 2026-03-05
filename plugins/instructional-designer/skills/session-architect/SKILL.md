---
name: session-architect
description: Design training sessions from intake to concept map to breakdown. Pulls from Notion. Use for "design a session", "new training", "build a workshop".
---

# Session Architect

Design training sessions by gathering structured context, producing a high-level concept map (5-6 core concepts), then breaking each concept down on request. Optimized for Tim's cognitive style: big concepts first, details on demand, no text walls.

## How It Works

```
INTAKE (structured brief)
    ↓
CONCEPT MAP (5-6 high-level concepts, visual)
    ↓
BREAKDOWN (one concept at a time, on request)
    ↓
RUN OF SHOW (time-stamped, delivery-ready)
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
- **Notion → Academy**: Search for past trainings Tim has done on similar topics or for similar audiences. Surface what worked and what didn't.
- **Notion → Transcripts**: Pull any pre-meeting call transcripts with the client. Extract agreed outcomes, audience details, constraints.
- **Canva**: If a deck already exists, pull it for context.

## Step 2: Produce the Concept Map

From the brief, distill 5-6 core concepts. Present them as a visual map, not a text wall.

**Format — the concept map:**
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
```

**Rules for concept selection:**
- Each concept must earn its slot. If you can't explain why it's essential in one sentence, cut it.
- Concepts should BUILD. Each one makes the next one land harder.
- The throughline is the red thread. If a concept doesn't serve the throughline, it doesn't belong.
- 5-6 concepts is the ceiling for Tim's style. Fewer is fine. More is never fine.

**Wait for Tim's approval of the concept map before breaking anything down.**

## Step 3: Break Down Each Concept

When Tim says "break down concept 3" (or similar), expand that concept into:

```
CONCEPT 3: [NAME]
──────────────────
TIME: [X min]

STORY LAUNCH:    [What story opens this section? — use story-finder if needed]
CORE IDEA:       [The one thing they must understand]
EVIDENCE/EXAMPLE:[What makes this credible?]
ENGAGEMENT:      [What does the audience DO here? — use engagement-check format]
TRANSITION:      [How does this connect to the next concept?]

SLIDE NOTES:     [What slides support this? Anchor vs. narrator check]
DELIVERY NOTE:   [Specific guidance for Tim's style]
```

**Only break down what Tim asks for.** Don't dump all 6 at once. This respects his working memory.

## Step 4: Generate Run of Show

When all concepts are broken down, produce the run-of-show:

```
RUN OF SHOW: [Session Title]
DATE: [Date] | TIME: [Start]–[End] | DURATION: [X min]
AUDIENCE: [Who] | SIZE: [N]

TIME  | MIN | SEGMENT          | WHAT HAPPENS                    | DELIVERY NOTE
──────|─────|──────────────────|─────────────────────────────────|──────────────
00:00 |  5  | Opening Hook     | [Story/stat/question]           | [Energy: HIGH]
00:05 |  3  | Roadmap          | [What they'll get]              | [Slide: agenda]
00:08 | 12  | Concept 1        | [Core idea + engagement]        | [Story launch]
00:20 | 12  | Concept 2        | [Core idea + engagement]        | [Pair-share]
...   |     |                  |                                 |
XX:XX |  5  | CTA + Close      | [One clear next step + callback]| [Memorize this]
XX:XX | 10  | Q&A              | [If included]                   | [Buffer zone]

TOTAL: [X min] | BUFFER: [X min] | HARD STOP: [Time]

IF RUNNING LONG: Cut [specific segment]
IF RUNNING SHORT: Expand [specific segment]
IF TECH FAILS: [Analog fallback]
```

**Apply Tim's Time Tax:** Add 30-50% to any time Tim estimates for interactive segments. He chronically underestimates.

## Evaluation Criteria

After producing the run-of-show, evaluate against four tests. Load `references/tim-design-profile.md` for pattern-matching.

**Test 1 — AUDIENCE VALUE:** Does this offer new thinking AND concrete application? Not just theory. Not just motivation. Both.

**Test 2 — HOST VALUE:** Will this spark the engagement the host wants? Matches their stated success criteria?

**Test 3 — COMPLIANCE:** Honors all stated constraints, avoids all stated taboos, meets format requirements?

**Test 4 — TIMING:** Fits the time with realistic estimates and buffer? Flow alternates energy (not all lecture, not all activity)?

**Verdict:** READY | REVISIONS NEEDED | MAJOR REDESIGN | INCOMPLETE

## Cross-Skill Integration

After session design is complete:
- Run `timing-check` to validate pacing
- Run `engagement-check` to audit interaction density and get scripted questions
- Run `survey-builder` to generate outcome-aligned surveys
- Run `slide-reviewer` once Canva deck exists
- Run `story-finder` for any section missing a story launch
- Run `dry-run-coach` after Tim records a walkthrough

## Tim's Design Danger Zones

Watch for these patterns and call them out directly:

**Content Fire Hose:** 47 slides for a 45-minute talk. Quick Start 9 generates ideas faster than he filters. Intervention: "Pick top 3. Kill the rest."

**Assume-They-Know:** Uses jargon, skips logical steps, references inside context. Intervention: "Define every acronym. Explain every jump."

**Amazing Opening, Weak Close:** Killer hook, great content, trails off. Intervention: "Write your close first. Make it as strong as your open."

**Timing Fantasy:** "This will take 10 minutes" (actually 25). Intervention: "Add 50% to every estimate. Now does it fit?"

**Slide Narrator Mode:** So slide-focused he loses the room. Intervention: "What are you saying that ISN'T on the slide? That's where your energy should be."

**Missing Story Moments:** Jumps straight to framework without a story to launch it. Intervention: "What story makes someone CARE about this concept before you teach it?"
