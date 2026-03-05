---
description: Find all meetings in a coaching/training/recurring series for an organization and run JTBD analysis on the full series, building session-by-session context.
argument-hint: "<organization name>"
---

# JTBD Series Analysis

Analyze an entire meeting series for an organization -- coaching engagements, Upskillerator cohorts, weekly meetings, or any recurring relationship. Finds all transcripts, orders them chronologically, and runs JTBD analysis on each with full series context.

## Key References

- **Meeting Transcripts DB**: `8368d3474cac4e71bf945934fce957f7`, collection `669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5`
- **JTBD Analyses DB**: `2f218faa725b41828194e8fc0f93453b`, data source `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`

## Workflow

### 1. Identify the Organization

- `$ARGUMENTS` is the organization name (e.g., `/jtbd-series Downtown Boxing Gym`)
- If no argument provided, ask the user which organization

### 2. Find All Transcripts for the Organization

Fetch the **Meeting Transcripts** Notion DB and filter for this org:

1. Use `notion-fetch` with `id: "8368d3474cac4e71bf945934fce957f7"` to get all transcripts
2. Filter results for the organization name (also check common abbreviations, e.g., "DBG" for "Downtown Boxing Gym")
3. Collect all matching transcript pages
4. Sort chronologically by date (ascending -- oldest first)

**Do NOT use `notion-search`, `notion-query-meeting-notes`, or `notion-query-database-view`.**

### 3. Check Existing Analyses & Versions

Query the **JTBD Analyses DB** for this organization to find which transcripts have analyses and whether they're current:

1. Filter by `Organization` matching the org name
2. For each record, check:
   - `Meeting Transcript` relation -- which transcript does it cover?
   - `Plugin Version` property -- is it current (`5.0.0`)?
3. Categorize each transcript:
   - **Current** -- has analysis at current plugin version (skip)
   - **Outdated** -- has analysis but older plugin version (needs upgrade)
   - **New** -- no analysis exists (needs full analysis)

### 4. Report and Confirm

```
Series: [Organization Name]
Total transcripts found: [N]

Current (v5.0.0): [A] sessions (skipped)
Outdated (needs upgrade): [B] sessions
  - Session 3 (2025-04-16) — v4.1.0, missing: SERIES, EXPECTATION MAP
  - Session 5 (2025-05-14) — v4.1.0, missing: SERIES, EXPECTATION MAP
New (needs full analysis): [C] sessions
  - Session 8 (2025-06-18) — no analysis
  - Session 9 (2025-06-25) — no analysis

Launching sequential agent for [B+C] sessions.
```

If ALL transcripts are current, report that and offer to run a synthesis instead (`/jtbd-synthesis [org name]`).

### 5. Dispatch Sequential Processing

Series processing MUST run sequentially (not in parallel) because each session's SERIES section references the previous one. The background agent handles the full chain, doing the right thing for each session based on its category:

```
Agent(
  subagent_type: "general-purpose",
  description: "JTBD Series: {org} (Sessions {start}-{end})",
  run_in_background: true,
  prompt: "You are the autonomous JTBD series runner.
    Process each session IN ORDER. Each builds on the previous.
    Never ask questions. Never wait for approval.

    ## Organization
    {org_name}

    ## Sessions to Process (in chronological order)

    ### Current (skip, but use for series context)
    - Session 1: {notion_url} — v5.0.0 (up to date)
    - Session 2: {notion_url} — v5.0.0 (up to date)

    ### Outdated (upgrade only -- do NOT re-run full analysis)
    - Session 3: {notion_analysis_url} — v4.1.0
      Transcript: {transcript_url}
      Missing: SERIES, EXPECTATION MAP, Plugin Version
      Action: Add missing sections, update version to 5.0.0

    ### New (full analysis)
    - Session 8: {transcript_url} — no analysis
      Action: Run full JTBD analysis pipeline

    ## For OUTDATED Sessions
    1. Fetch the existing analysis from Notion
    2. Fetch the raw transcript
    3. Add SERIES section (referencing previous session)
    4. Run uxinator:expectation-mapper against raw transcript, append EXPECTATION MAP
    5. Add/update Plugin Version to 5.0.0
    6. Update local .md file AND Notion page body (full text, curl fallback)
    7. Update Plugin Version property on Notion DB record
    Do NOT modify existing JTBD analysis sections.

    ## For NEW Sessions
    1. Fetch the transcript from Notion using notion-fetch
    2. Run the full JTBD analysis (Steps 3-6 from jtbd-analysis.md)
    3. The SERIES section must reference the PREVIOUS session's analysis
    4. The EXPECTATION MAP must reference how expectations shifted
    5. Save .md file to /Users/tim/Dev/claude-cowork/Clients/{org}/Meetings/Analysis/
    6. Push to Notion JTBD Analyses DB with full text
    7. WAIT for Notion push to complete before starting the next session

    ## JTBD Analysis SKILL.md
    {paste full SKILL.md content}

    ## Error Handling
    - If a transcript is too short (<500 words), skip it and log
    - If a transcript is a cancellation, skip and log
    - If Notion push fails, use curl fallback, then continue to next
    - Log progress after each session: 'Completed Session {N} of {total}'"
)
```

### 6. After Completion

Once the series agent finishes, suggest next steps:
- **Run synthesis**: `/jtbd-synthesis {org name}` to surface patterns across the full series
- **Review evolution**: The SERIES sections in each analysis track how the JTBD shifted session to session
- **Check expectation trends**: The EXPECTATION MAP sections show how the relationship evolved

## Series Types

This command handles any recurring meeting series:

| Series Type | Example | How Detected |
|------------|---------|-------------|
| Coaching | Weekly AI coaching with DBG | Recurring org, "coaching" in title |
| Upskillerator | 6-session cohort program | "Upskillerator" in title, fixed cadence |
| Weekly meeting | Standing team call | Same org, weekly cadence |
| Diagnostic | Multi-session diagnostic | "Diagnostic" in title, 3-5 sessions |
| Training | Multi-day training series | "Training" or "Workshop" in title |

The command doesn't need to distinguish between types -- it finds all transcripts for the org and analyzes them in order regardless.

## Important Notes

- **Sequential, not parallel** -- series context depends on order. Each session references the previous.
- **Idempotent** -- already-analyzed sessions are skipped. Safe to re-run after adding new transcripts.
- **Session numbering** -- determined by chronological position in the full series, not just the unanalyzed subset.
- Transcripts that are cancellations or non-substantive (< 500 words) are skipped and logged.
- For very long series (20+ sessions), the background agent may hit context limits. In that case, it should process in batches of 10 and chain to a new agent for the next batch.
