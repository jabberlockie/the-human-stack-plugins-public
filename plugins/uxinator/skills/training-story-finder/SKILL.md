---
name: training-story-finder
description: >
  Find story options for a section concept, harvest stories from transcripts, or find
  expectation-inoculation stories. Use for "find me a story", "harvest stories",
  "inoculation story".
version: 2.0.0
---

# Story Finder

Tim doesn't naturally create "story moments" — the story that launches a section and makes people care before teaching the framework. He jumps straight to the concept.

Two modes plus a new expectation-specific mode: **Find stories**, **Harvest stories**, or **Find inoculation stories**.

---

## Mode 1: Find Me a Story

**Triggers:** "find me a story", "story for [section]", "story options", "I need a story for..."

### Input
A concept name and brief description.

### Process
1. Search story library in Notion (if populated via Mode 2)
2. Search Tim's transcript pages in Notion for relevant anecdotes
3. Search Academy in Notion for past session content
4. If nothing in Notion, generate fresh story options

### Output
```
STORY OPTIONS FOR: [Concept Name]
PURPOSE: Make the audience care about [concept] before you teach it

OPTION 1: [Story Title] — [Source: transcript / past session / generated]
Setup:    [1-2 sentences: what's the situation?]
Tension:  [What goes wrong or what's at stake?]
Turn:     [What changes or what's revealed?]
Bridge:   [Exact transition sentence from story → concept]
Time:     [Estimated 60-90 sec]

OPTION 2: ...
OPTION 3: ...

RECOMMENDATION: Option [X] because [specific reason tied to audience and concept]
```

### Story Selection Criteria
- **Creates a need:** Audience thinks "so what do we do?" before Tim teaches
- **Prefer authenticity:** Tim's own stories over generated ones
- **Match audience context:** Enterprise IT stories don't land with nonprofit program managers unless parallel is explicit
- **Short > long:** Target 60-90 seconds
- **Bridge is critical:** The exact transition sentence Tim should almost memorize

---

## Mode 2: Harvest Stories

**Triggers:** "harvest stories", "harvest all", "extract stories from [transcript]"

### Input
Notion transcript page URL/ID, or "harvest all" to scan the transcript database.

### Process
1. Read transcript(s) from Notion
2. Identify story moments — anecdotes, case studies, metaphors, examples, personal experiences
3. Extract each with structured metadata
4. Store in story library

### What Counts as a "Story Moment"
- "Let me give you an example" or "I had a client who..."
- A specific situation with characters, tension, and outcome
- A metaphor or analogy extended beyond one sentence
- A case study with before/after
- A personal experience illustrating a principle

### Extraction Format
```
STORY: [Descriptive title]
SOURCE: [Transcript + approximate location]
TOPIC TAGS: [2-3 topics this story could illustrate]
AUDIENCE FIT: [Enterprise / Nonprofit / Technical / Leadership / General]
TONE: [Funny / Serious / Cautionary / Inspiring / Provocative]
LENGTH: [Short (30-60 sec) / Medium (60-90 sec) / Long (2+ min)]
SETUP: [1-2 sentence summary]
KEY MOMENT: [The turn/punchline/insight]
BRIDGE OPTIONS: [2-3 transition sentences]
EXPECTATION TYPE: [Does this story illustrate or inoculate against an expectation?
                   DECLARED / TRANSFERRED / INFERRED / DEFAULT / SOCIAL / NONE]
TIMES USED: [Track usage — prevents overuse]
```

### Harvesting Rules
- Only extract stories that could stand alone and be reused
- Tag generously — a nonprofit story might also work for "leadership resistance"
- The library compounds with every transcript
- Show before saving — let Tim confirm/edit

---

## Mode 3: Find Inoculation Story (NEW — from Expectation Architecture)

**Triggers:** "inoculation story", "inoculate against", "they're going to expect..."

### Purpose
Find or generate a story that preemptively addresses a TRANSFERRED expectation — something the audience expects based on past experience that doesn't apply to Tim's delivery.

### Input
The transferred expectation to inoculate against. Examples:
- "They've had consultants who gave them a binder and disappeared"
- "Their last training was death by PowerPoint"
- "They expect to be sold to, not taught"
- "They think AI training means 'learn to use ChatGPT'"

### Output
```
INOCULATION STORY FOR: [Transferred expectation]
PURPOSE: Name the past experience, separate Tim's delivery from it

OPTION 1: [Story Title]
Setup:    [Acknowledge the past experience — make them feel SEEN]
Turn:     [Here's how this is different]
Bridge:   [Transition to what they CAN expect from today]
Exact words: "[Full script Tim can say — 30-60 seconds]"

OPTION 2: ...

DELIVERY NOTE: Place this in the first 5 minutes. Inoculation works best
before the audience has time to project their transferred expectation
onto Tim's session.
```

### Inoculation Design Principles
- **Name it.** Don't dance around the past experience. Say it directly.
- **Empathize first.** "You've probably had trainings where..." — make them feel understood.
- **Then separate.** "That's not what today is." — clear, no hedging.
- **Then declare.** "Here's what IS going to happen." — set the new expectation.
- **Keep it short.** 30-60 seconds. This isn't a segment. It's a reset.

---

## Notion Integration
- **Transcripts source:** Tim's transcript pages in Notion
- **Academy source:** Past session content in Notion
- **Story library destination:** Dedicated Notion page/database
