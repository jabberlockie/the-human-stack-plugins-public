---
name: story-finder
description: Find story options for a section concept or harvest stories from Notion transcripts into a reusable library. Use for "find me a story", "harvest stories".
---

# Story-Finder Skill

## Problem
Tim doesn't naturally create "story moments" — the story that launches a section and makes people care before teaching the framework. He tends to jump straight to the concept.

## Solution
Two modes: **Find stories for a concept** or **Harvest stories from transcripts** into a reusable library.

---

## Mode 1: Find Me a Story

**Triggers:** "find me a story", "story for [section]", "story options", "I need a story for..."

### Input
A concept name and brief description (e.g., "Concept 3: The Technology Trap — organizations buy more tools instead of fixing process")

### Process
1. Search the story library in Notion (if populated via Mode 2)
2. Search Tim's transcript pages in Notion for relevant anecdotes
3. Search the Academy in Notion for past session content on similar ground
4. If nothing in Notion, generate fresh story options based on the concept

### Output Format
```
STORY OPTIONS FOR: [Concept Name]
PURPOSE: Make the audience care about [concept] before you teach it

OPTION 1: [Story Title] — [Source: transcript / past session / generated]
Setup:    [1-2 sentences: what's the situation?]
Tension:  [What goes wrong or what's at stake?]
Turn:     [What changes or what's revealed?]
Bridge:   [Exact transition sentence from story → concept]
Time:     [Estimated 60-90 sec]

OPTION 2: [Story Title]
...

OPTION 3: [Story Title]
...

RECOMMENDATION: Option [X] because [specific reason tied to audience and concept]
```

### Story Selection Criteria
- **Creates a need:** After hearing it, the audience should think "yeah, so what do we do about that?" before Tim teaches the framework
- **Prefer authenticity:** Tim's own stories (transcripts/past sessions) over generated ones
- **Match audience context:** A story about enterprise IT doesn't land with nonprofit program managers unless the parallel is explicit
- **Short > long:** Target 60-90 seconds. Tim can expand live if the room is leaning in
- **Bridge is critical:** The exact sentence that transitions from story to teaching — Tim should almost memorize this

---

## Mode 2: Harvest Stories

**Triggers:** "harvest stories", "harvest all", "extract stories from [transcript]"

### Input
A Notion transcript page URL/ID, or "harvest all" to scan the transcript database

### Process
1. Read transcript(s) from Notion
2. Identify story moments — anecdotes, case studies, metaphors, examples, personal experiences, client stories
3. Extract each story with structured metadata
4. Store in story library (Notion database or structured page)

### What Counts as a "Story Moment"
- Tim says "let me give you an example" or "I had a client who..." or "here's what happened..."
- A specific situation with characters, tension, and outcome
- A metaphor or analogy extended beyond one sentence
- A case study with before/after
- A personal experience that illustrates a principle

### Extraction Format Per Story
```
STORY: [Descriptive title]
SOURCE: [Transcript name + approximate timestamp/location]
TOPIC TAGS: [2-3 topics this story could illustrate]
AUDIENCE FIT: [Enterprise / Nonprofit / Technical / Leadership / General]
TONE: [Funny / Serious / Cautionary / Inspiring / Provocative]
LENGTH: [Short (30-60 sec) / Medium (60-90 sec) / Long (2+ min)]
SETUP: [1-2 sentence summary of the situation]
KEY MOMENT: [The turn/punchline/insight]
BRIDGE OPTIONS: [2-3 sentences that could transition from this story to a teaching point]
TIMES USED: [Track if Tim uses it in a session — prevents overuse]
```

### Harvesting Rules
- **Don't extract every anecdote.** Only extract stories that could stand alone and be reused in a different context
- **Tag generously.** A story about a nonprofit client might also work for "leadership resistance" or "technology adoption"
- **The library compounds.** Every transcript processed adds to Tim's story arsenal
- **Show before saving.** When harvesting, show Tim what was found and let him confirm/edit before saving

### Notion Integration
- **Transcripts source:** Tim's transcript pages in Notion
- **Academy source:** Past session content in Notion
- **Story library destination:** A dedicated Notion page or database (create if doesn't exist, or ask Tim where to put it)

---

## Design Notes
- The skill lives in the gap between concept and teaching: **Story → Why It Matters → Framework**
- Reuse builds over time. Each session harvested strengthens future story options
- Authenticity beats polish. Tim's real examples land harder than AI-generated hypotheticals
- The Bridge line is the hinge. If Tim can't naturally transition from story to concept, the story isn't ready
