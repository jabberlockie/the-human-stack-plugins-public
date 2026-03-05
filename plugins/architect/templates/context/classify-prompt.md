# Session Chunk Classification

You are classifying a conversation chunk for semantic retrieval. Your task is to identify what type of knowledge this chunk contains so it can be retrieved when relevant.

## Layer Definitions

| Layer | Description | What it captures |
|-------|-------------|------------------|
| **user** | Human's patterns and growth | How they work, preferences, lessons learned, recurring mistakes |
| **product** | System knowledge | Architecture, design patterns, domain concepts that persist |
| **project** | Current work cycle | Active feature context, decisions made, current state |
| **plan** | Implementation approach | Strategy, steps to execute, future work |
| **task** | Execution details | How specific work was done, debugging steps, verification |

## Sublayer Definitions

### user sublayers
- `patterns`: Recurring approaches, workflows, habits
- `preferences`: Style choices, tool preferences, communication style
- `learnings`: New knowledge gained, insights discovered
- `mistakes`: Errors made, things to avoid, gotchas encountered

### product sublayers
- `architecture`: Tech stack, system design, service boundaries
- `design`: UI patterns, component structure, styling conventions
- `domain`: Business concepts, terminology, domain rules

### project sublayers
- `active`: What is being built right now, goals, scope
- `decisions`: Why X was chosen over Y, trade-offs considered
- `state`: Progress, blockers, what's working, what's not

### plan sublayers
- `strategy`: High-level approach, phasing, priorities
- `steps`: Concrete implementation steps, sequence
- `backlog`: Future work, deferred items, nice-to-haves

### task sublayers
- `implementation`: Code written, patterns used, how it was built
- `debugging`: Problems encountered, investigation steps, fixes
- `verification`: Testing done, validation steps, quality checks

## Classification Rules

1. Choose the MOST SPECIFIC layer that applies
2. A chunk about "how the auth system works" → product/architecture
3. A chunk about "we decided to use JWT" → project/decisions
4. A chunk about "I usually debug by..." → user/patterns
5. If genuinely ambiguous, prefer: task > project > plan > product > user

## Input Chunk

```
{chunk_content}
```

## Output

Return ONLY valid JSON, no other text:

```json
{
  "layer": "product|project|plan|task|user",
  "sublayer": "see definitions above",
  "product_area": "auth|payments|api|database|ui|etc or null if not applicable",
  "summary": "One sentence capturing the key knowledge in this chunk",
  "topics": ["topic1", "topic2", "topic3"]
}
```
