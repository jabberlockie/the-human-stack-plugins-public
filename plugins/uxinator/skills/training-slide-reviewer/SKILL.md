---
name: training-slide-reviewer
description: >
  Evaluate slides for narrator mode, working-memory gaps, and inferred expectation signals.
  Two-axis review plus expectation audit. Use for "review my slides", "check my deck", "slide review".
version: 2.0.0
---

# Slide Reviewer

## Context: Tim's Slide Relationship

Tim has low working memory and compensates by leaning on slides. Two failure modes:

1. **Slide Narrator Mode** — Slides carry so much content Tim reads them. Energy dies.
2. **Working Memory Gap** — Slides too sparse, Tim loses his thread.

Sweet spot: slides that ANCHOR Tim's delivery without REPLACING it.

## Core Behavior

1. Pull slide deck from Canva (via connector) or accept uploaded images/PDF
2. Map each slide to the session run-of-show (if available)
3. Evaluate each slide on two axes plus expectation signals

### Axis 1: Content Load (is the slide doing too much?)

- **RED**: Full sentences Tim will read verbatim. "This slide is a teleprompter."
- **YELLOW**: Key points present but could be condensed. "Trim to keywords."
- **GREEN**: Keywords, visuals, or framework only. "Anchors without narrating."

### Axis 2: Anchor Strength (does it support Tim's working memory?)

- **RED**: Blank or decorative only. Tim will lose his place.
- **YELLOW**: Some structure but missing concept label.
- **GREEN**: Clear concept anchor with visual support.

### Axis 3: Expectation Signals (NEW — what does this slide tell the audience to expect?)

Slides create INFERRED expectations. The audience reads a slide and forms an expectation about what the session IS, what's coming next, and what kind of experience they're having.

- **RED**: Slide promises something the session doesn't deliver. (e.g., slide says "Workshop Exercises" but the session is all lecture; slide lists 8 topics but only 3 get covered)
- **YELLOW**: Slide is ambiguous — audience could interpret it as a promise. (e.g., agenda slide with items that may get cut; slide with "Q&A" that might not happen)
- **GREEN**: Slide accurately represents what's coming. No false promises.

## Output Format

```
SLIDE REVIEW: [Session Title] — [N slides for X min session]

SLIDE RATIO: [N slides / X min = Y slides per minute]
TARGET: ~1 slide per 2-3 min for keynote, ~1 per 1-2 min for workshop
VERDICT: [Too many slides / Just right / Too few]

SLIDE | CONTENT | ANCHOR | EXPECT. | ISSUE                          | FIX
──────|─────────|────────|─────────|────────────────────────────────|──────
  1   | GREEN   | GREEN  | GREEN   | —                              | —
  2   | RED     | GREEN  | GREEN   | Full paragraph on slide        | Cut to 3 keywords
  3   | GREEN   | RED    | GREEN   | Decorative, no anchor          | Add concept header
  5   | GREEN   | GREEN  | RED     | Lists 6 outcomes, only 3 get   | Remove outcomes
      |         |        |         | covered — creates broken promise| you won't deliver
  7   | YELLOW  | YELLOW | YELLOW  | 5 bullets, agenda might shift  | Pick top 2
 12   | RED     | GREEN  | GREEN   | Tim will read this verbatim    | Replace with visual
...   |         |        |         |                                |

SUMMARY:
- RED content load: [N] — Tim will narrate these.
- RED anchor: [N] — Tim will lose his place.
- RED expectation: [N] — Slides promise what session doesn't deliver.
- Slide-narrator risk: [HIGH/MEDIUM/LOW]
- Working-memory risk: [HIGH/MEDIUM/LOW]
- False-promise risk: [HIGH/MEDIUM/LOW]
```

## Evaluation Rules

- **Slide titles should be headlines, not labels.**
- **One idea per slide.**
- **Tim's verbal skills carry detail. Slides carry structure.**
- **Flag any slide that takes more than 3 seconds to read.**
- **If 40+ slides for 45 minutes, flag the ratio immediately.**
- **Agenda slides are expectation contracts.** If the agenda lists something, the session must deliver it. Flag any agenda item that might get cut.
- **Title slides set the first inferred expectation.** If the title says "Workshop" but it's a lecture, flag it.
