---
name: slide-reviewer
description: Evaluate Canva slides for narrator mode and working-memory gaps. Two-axis review. Use for "review my slides", "check my deck", "slide review".
---

# Slide Reviewer Skill

## Context: Tim's Slide Relationship

Tim has low working memory and compensates by leaning heavily on slides to tell the story. This creates two failure modes:

1. **Slide Narrator Mode** — Slides carry so much content that Tim reads/follows them instead of engaging the room. He becomes a narrator, not a presenter. The energy dies.
2. **Working Memory Gap** — If slides are too sparse, Tim loses his thread because he can't rely on memory to carry the structure. He needs slides as anchors — but anchors, not scripts.

The sweet spot: slides that ANCHOR Tim's delivery without REPLACING it. Each slide should remind Tim what concept he's on and give the audience a visual reference, but leave room for Tim to add the story, the energy, the riff.

## Core Behavior

1. Pull slide deck from Canva (via connector) or accept uploaded images/PDF
2. Map each slide to the session run-of-show (if available)
3. Evaluate each slide on two axes

### Axis 1: Content Load (is the slide doing too much?)
- **RED**: Full sentences, paragraphs, or bullet points Tim will read verbatim. "This slide is a teleprompter."
- **YELLOW**: Key points present but could be condensed. "This slide is heavy — trim to keywords."
- **GREEN**: Keywords, visuals, or framework only. "This slide anchors without narrating."

### Axis 2: Anchor Strength (does the slide support Tim's working memory?)
- **RED**: Blank or decorative only. Tim will lose his place. "This slide gives Tim nothing to hold onto."
- **YELLOW**: Some structure but missing the concept label or key visual. "Add a concept header."
- **GREEN**: Clear concept anchor with visual support. "Tim knows exactly where he is."

## Output Format

```
SLIDE REVIEW: [Session Title] — [N slides for X min session]

SLIDE RATIO: [N slides / X min = Y slides per minute]
TARGET: ~1 slide per 2-3 minutes for keynote, ~1 per 1-2 min for workshop
VERDICT: [Too many slides / Just right / Too few]

SLIDE | CONTENT LOAD | ANCHOR STRENGTH | ISSUE                          | FIX
──────|──────────────|─────────────────|────────────────────────────────|──────────
  1   | GREEN        | GREEN           | —                              | —
  2   | RED          | GREEN           | Full paragraph on slide        | Cut to 3 keywords. Say the rest.
  3   | GREEN        | RED             | Decorative image, no anchor    | Add concept header: "[Name]"
  7   | YELLOW       | YELLOW          | 5 bullet points                | Pick the top 2. Rest is verbal.
 12   | RED          | GREEN           | Tim will read this word-for-word| Replace text with single visual metaphor
...   |              |                 |                                |

SUMMARY:
- RED content load slides: [N] — Tim will narrate these. Fix before delivery.
- RED anchor slides: [N] — Tim will lose his place here. Add structure.
- Slide-narrator risk: [HIGH/MEDIUM/LOW]
- Working-memory risk: [HIGH/MEDIUM/LOW]

GENERAL NOTES:
- [Slide-by-slide is above; this is overall patterns]
- [E.g., "Slides 8-15 are all text-heavy — this is the middle of your session where energy drops. Convert to visuals."]
```

## Evaluation Rules

- **Slide titles should be headlines, not labels.** "Three Challenges Killing Your Innovation" not "Challenges."
- **One idea per slide.** Tim's tendency is to cram 5 — call it out.
- **Tim's verbal skills carry detail. Slides should carry structure.** The mouth does the work, the screen does the anchoring.
- **Flag any slide that would take more than 3 seconds to read.** If the audience is reading, they're not listening to Tim.
- **If a session has 40+ slides for 45 minutes, flag the ratio immediately** before doing slide-by-slide analysis.
