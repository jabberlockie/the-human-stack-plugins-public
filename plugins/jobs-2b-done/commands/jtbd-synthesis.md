---
description: Synthesize patterns across multiple JTBD call analyses — surface recurring jobs, evolving patterns, emerging frameworks, and audience segments across companies, folders, and engagement stages.
argument-hint: "<company name, folder, date range, 'all', or specific filter>"
---

# JTBD Synthesis

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Aggregate and synthesize insights across multiple JTBD call analyses stored in `Jobs To Be Done/`. Surfaces patterns invisible in any single call.

## Key References

- **JTBD Analyses Notion DB**: `2f218faa725b41828194e8fc0f93453b`
- **JTBD Analyses Data Source**: `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`
- **Synthesis Prompt**: `Jobs To Be Done/Jobs 2B Done - Plugin & Skills/JTBD-Synthesis-Prompt.md`

## Workspace Structure

```
/Users/tim/Dev/claude-cowork/Clients/[Organization Name]/
├── Meetings/
│   ├── Transcripts/        ← raw transcripts
│   └── Analysis/           ← JTBD analysis files (source for synthesis)
└── Synthesis/              ← synthesis reports saved here
```

Also check legacy paths under `Jobs To Be Done/` for older analyses.

---

## Workflow

### 1. Scope the Synthesis

Ask the user what they want to synthesize. Options:

- **All calls** — Read every analysis across all folders
- **Single folder** — All calls within one folder (e.g., `Diagnostic & Managed Success`)
- **Single company** — All calls for one company across folders (useful for JTBD evolution tracking)
- **Date range** — Filter by call date across all folders
- **Engagement stage** — Filter by stage (Pre-sale, Discovery, Active Client, Alumni)
- **Custom** — Any combination of filters

### 2. Load Source Data

**Primary source: JTBD Analyses Notion DB**

Use the Notion database as the index to identify which analyses to include:
1. Search the JTBD Analyses DB (`collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`) using the user's filter criteria (Engagement Stage, Organization, Sector, etc.)
2. For each matching record, read the page content for the full analysis
3. Use the structured properties (Themes, Frameworks Applied, Persona Label, etc.) for cross-cutting aggregation

**Fallback: Read .md files directly**

If the Notion DB is not yet backfilled or records are missing:
1. **Read the synthesis prompt** from: `Jobs To Be Done/Jobs 2B Done - Plugin & Skills/JTBD-Synthesis-Prompt.md`
2. List all `Meetings/Analysis/` subdirectories under `/Users/tim/Dev/claude-cowork/Clients/` (and legacy `Jobs To Be Done/` paths)
3. Apply the user's filter (folder, company, date, stage, or all)
4. Read each matching `.md` analysis file
5. Also load any existing synthesis reports from `Synthesis/` folders for context on established findings

**Extract from each analysis:**
- Company name (from folder or Organization property)
- Call date (from filename or record)
- Parent folder (from path or File Path property)
- Participant names and roles
- Primary JTBD
- Functional / Emotional / Social jobs
- Switch triggers
- Obstacles & anxieties
- Messaging gold quotes
- Audience segment / persona
- IP & framework applications
- Product/offering fit
- Pattern recognition flags (known and emerging)
- Confidence scores

### 3. Run Cross-Call Analysis

Follow the synthesis methodology in `JTBD-Synthesis-Prompt.md`. Key synthesis dimensions:

**A. Recurring Functional Jobs** — Clustered by theme, ranked by frequency and confidence

**B. Recurring Emotional Jobs** — Fears/anxieties and aspirations, ranked by intensity

**C. Recurring Social Jobs** — Who they're performing for (board, peers, staff, funders)

**D. Switch Trigger Patterns** — What pushes orgs to act, with sector/size correlations

**E. Obstacle & Anxiety Clusters** — Grouped by theme, evolution over time

**F. Language & Messaging Patterns** — Cross-call quotes, recurring metaphors, vocabulary gaps

**G. Audience Segment Convergence** — Persona clusters, archetype validation (Lone Wolf Champion, Mission-Driven Skeptic Coalition)

**H. IP & Framework Application** — Framework usage, gaps, emerging concepts worth naming

**I. Product/Offering Fit** — Offering-to-job mapping, entry point patterns, capability gaps

**J. JTBD Evolution** — For single-company or longitudinal: how jobs shift across calls

**K. Evidence Level Assessment** — N=1 hypothesis, N=2 pattern, N=3+ finding (per synthesis prompt rules)

### 4. Determine Save Location

**Ask the user** which folder's `Synthesis/` to save in, unless:
- The synthesis is scoped to a single folder → save in that folder's `Synthesis/`
- The synthesis is cross-folder ("all calls") → ask user, or default to root level

If the `Synthesis/` subfolder doesn't exist in the target folder, create it.

**File naming:** `[YYYY-MM-DD] - JTBD Synthesis - [scope description].md`
- Examples:
  - `2026-02-08 - JTBD Synthesis - All Calls.md`
  - `2026-02-08 - JTBD Synthesis - Episcopal Relief & Development.md`
  - `2026-02-08 - JTBD Synthesis - Pre-sale Calls Q3 2025.md`

### 5. Generate Synthesis Report

**Output structure:**

```markdown
# JTBD Synthesis: [Scope]
**Generated**: [Date]
**Calls analyzed**: [Count]
**Companies**: [List]
**Folders**: [List of folders included]
**Date range**: [Earliest] to [Latest]

---

## Executive Summary
[3-5 sentences: the most important patterns]

---

## Top Recurring Jobs
[Ranked list with frequency, evidence level (N=?), and representative quotes]

### Functional Jobs
[Clustered by theme with cross-references to source calls]

### Emotional Jobs
[Ranked by intensity and frequency]

### Social Jobs
[Grouped by audience they're performing for]

---

## Established Findings Update
[Cross-reference against the 7 established findings from the synthesis prompt]
[Note which findings gained new supporting evidence]
[Flag any findings that need revision]

---

## Archetype Validation
[Update evidence for Lone Wolf Champion and Mission-Driven Skeptic Coalition]
[New archetype signals if any]

---

## Switch Trigger Patterns
[What pushes orgs to act, ranked]
[Sector/size correlations]

---

## Obstacle & Anxiety Map
[Clustered themes with frequency]
[Which obstacles block which jobs]

---

## Messaging Gold: Cross-Call Patterns
[Highest-value quotes appearing across calls]
[Recurring metaphors]
[Vocabulary gaps = content opportunities]

---

## Framework Application Map
[Which frameworks solve which recurring jobs]
[Gap analysis — unaddressed jobs]
[Emerging concepts worth developing]

---

## Product/Offering Insights
[Offering-to-job cluster mapping]
[Entry point patterns]
[Capability gaps]

---

## JTBD Evolution
[For companies with multiple calls: how jobs shifted]
[Engagement stage patterns]

---

## Emerging Patterns to Watch
[N=1 hypotheses needing validation]
[N=2 patterns gaining evidence]
[Newly validated N=3+ findings]

---

## Recommended Actions
[Specific things to do with these insights]
[Content to create, frameworks to develop, offerings to adjust]

---

## Source Calls
| Date | Folder | Company | Participants | Stage | Primary JTBD |
|------|--------|---------|-------------|-------|-------------|
```

**Save to**: `/Users/tim/Dev/claude-cowork/Clients/[Organization Name]/Synthesis/[filename].md` (or `Clients/_Cross-Org/Synthesis/` for cross-org syntheses)

**Always show the user the synthesis before saving** so they can review.

### 6. Cross-Reference with ~~CRM (Optional)

If ~~CRM is connected, enrich the synthesis:
- Deal status for each company — which JTBD patterns correlate with won deals?
- Pipeline stage data — do certain jobs predict where deals stall?
- Contact roles — do certain personas convert at higher rates?

## Important Notes

- Read the `JTBD-Synthesis-Prompt.md` fresh each time — it contains established findings, archetypes, and meta-jobs that evolve.
- Distinguish evidence levels: N=1 hypothesis, N=2 pattern, N=3+ finding.
- Synthesis, not summary — identify what's invisible at the individual call level.
- When quoting across calls, always cite which call/company the quote came from.
- This synthesis is most valuable with 3+ calls. With fewer, flag conclusions as preliminary.
- The Notion DB properties (Themes, Frameworks, Engagement Stage, etc.) enable faster filtering than reading every .md file. Use DB queries first, then read page content for details.
