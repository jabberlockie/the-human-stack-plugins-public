# JTBD Analysis Skill

Run Jobs-to-be-Done analysis on call transcripts using Tim Lockie's structured framework, with UXinator Expectation Mapping and coaching series tracking. This skill powers both the `jtbd-analysis` command and the standalone `jtbd-analysis` skill.

## Quick Reference

- **Analysis Prompt**: `Jobs To Be Done/Jobs 2B Done - Plugin & Skills/JTBD-Analysis-Prompt.md`
- **Synthesis Prompt**: `Jobs To Be Done/Jobs 2B Done - Plugin & Skills/JTBD-Synthesis-Prompt.md`
- **JTBD Analyses Notion DB**: ID `2f218faa725b41828194e8fc0f93453b`, data source `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`
- **Database Schema**: Inline in `commands/jtbd-analysis.md` Step 6 (authoritative source for all valid property values)
- **Notion Meeting Transcripts DB**: ID `8368d3474cac4e71bf945934fce957f7`, collection `669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5`
- **HubSpot Portal**: `22283601`
- **UXinator Skill**: `uxinator:expectation-mapper` (runs against raw transcript)

## Transcript Sources

1. **Pasted text** — use directly
2. **~~conversation intelligence URL** (Fathom, Fireflies, Gong) — fetch via WebFetch
3. **~~knowledge base Meeting Transcript** — fetch via `notion-fetch` or search via `notion-search` with `data_source_url: "collection://669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5"`

## Folder Structure

All analyses use a single deterministic path -- never ask the user which folder:

```
/Users/tim/Dev/claude-cowork/Clients/[Organization Name]/
├── Meetings/
│   ├── Transcripts/        ← raw transcripts
│   └── Analysis/           ← JTBD analysis files
└── Synthesis/              ← cross-call synthesis reports
```

Create the directory structure if it doesn't exist.

## Core Workflow

1. **Get transcript** from one of the three sources
2. **Extract** company name, participants, call date
3. **Determine series context** — query JTBD Analyses DB for same Organization to get session number and link to previous session (see command Step 2b)
4. **Create directory** — path is always `/Users/tim/Dev/claude-cowork/Clients/[Org Name]/Meetings/Analysis/` (never ask, fuzzy-match existing org folders)
5. **Read `JTBD-Analysis-Prompt.md`** fresh every time (it evolves)
6. **Run full 9-dimension analysis** per the prompt
7. **Build CONNECTIONS section** at top of output:
   - Fathom Recording link
   - Notion Meeting Notes link
   - HubSpot Account (search ~~CRM companies, portal `22283601`, record type `0-2`)
   - HubSpot Contacts (search ~~CRM contacts, record type `0-1`)
   - HubSpot Deal (search ~~CRM deals, record type `0-3`)
   - Clay URL (if available)
8. **Run UXinator expectation-mapper** against the raw transcript (NOT the JTBD analysis) and append the full output as the final `## EXPECTATION MAP` section
9. **Save** to `/Users/tim/Dev/claude-cowork/Clients/[Org Name]/Meetings/Analysis/[filename].md`
10. **Populate JTBD Analyses DB** — create a page in the Notion database (data source `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`) with:
    - **Page body**: The COMPLETE analysis text, verbatim — all sections including SERIES and EXPECTATION MAP (never summarize or truncate)
    - **Properties**: Using exact valid values from command file Step 6b
    - **Meeting Transcript**: Two-way relation to source transcript (auto-creates back-link)

## Output Sections (in order)

1. CONTEXT METADATA (includes `Plugin Version: 5.0.0` at bottom)
2. SERIES (session number, previous session link, JTBD evolution)
3. PRIMARY JTBD
4. DETAILED JTBD ANALYSIS
5. SWITCH TRIGGER
6. DESIRED OUTCOME
7. OBSTACLES & ANXIETIES
8. MESSAGING GOLD
9. AUDIENCE SEGMENT
10. IP & FRAMEWORK APPLICATION
11. PRODUCT/OFFERING IMPLICATIONS
12. PATTERN RECOGNITION
13. CONNECTIONS
14. EXPECTATION MAP (from UXinator, run against raw transcript)

## File Naming

- Single participant: `[YYYY-MM-DD] - [First Last, Company] - JTBD Analysis.md`
- Series session (Session 2+): `[YYYY-MM-DD] - [First Last, Company] - Session [N] - JTBD Analysis.md`
- Multiple from same org: `[YYYY-MM-DD] - [Company] - JTBD Analysis.md`

## Organization Folder Matching

- Check existing folders under `/Users/tim/Dev/claude-cowork/Clients/`
- Fuzzy match at >=90% similarity (case-insensitive)
- If match exists, use that folder name exactly
- If no match, create new org folder with full directory structure

## Analysis Rules

- Specific over generic
- Quote exact language from transcript
- Mark inferences with [INFERRED] or [IMPLIED]
- Flag contradictions (stated vs. observed)
- Intensity = importance
- Context matters (prospect vs. 90-day client)

## Notion DB Population

After saving the .md file, always create a JTBD Analyses record. The database serves as the queryable, filterable index across all analyses. The .md file remains the authoritative full-text source.

**Use `notion-create-pages`** with:
```
parent: { data_source_id: "fbf274fd-5cf0-4afe-9eaf-cb511cae6b94" }
```

**CRITICAL -- Page body content comes first.** The complete, unmodified analysis text (the exact .md file content) MUST be pasted as the page body. Do NOT summarize, truncate, or paraphrase. Every section, every quote, every line -- verbatim. This includes the SERIES section and the EXPECTATION MAP section.

**Full-text fallback**: If MCP tools truncate content, use the Notion API directly via curl with `$NOTION_API_KEY` to append missing blocks. See command Step 6a for details.

**Property mapping**: See `commands/jtbd-analysis.md` Step 6b for the complete field-by-field mapping with exact valid values for every select/multi-select field.

**Meeting Transcript** is a two-way relation to the Meeting Transcripts DB (`collection://669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5`). Setting this relation automatically creates a back-link visible on the transcript page under "JTBD Analyses".

**Multi-select values must match exactly** — only use values listed in Step 6b. Omit rather than guess or create unknown options.

## Dispatch Architecture

**This skill dispatches as a background agent.** The main conversation handles only transcript acquisition (Step 1) and company/folder identification (Step 2) in the foreground -- these may require user input. Everything else (Steps 2b-6) runs as a single background agent:

1. Foreground: Acquire transcript, extract company/participants/date (no user input needed for path -- it's deterministic)
2. Background agent: Series context, JTBD analysis, CRM lookups, UXinator expectation map, file save, Notion push

See `commands/jtbd-analysis.md` Dispatch Architecture section for the full agent prompt template.

**Background rules:**
- Do not stop for Bash tool errors -- retry once, then log and continue.
- Do not prompt about file permissions or directory creation.
- If MCP Notion tools fail, fall back to curl-based API calls silently.
- Skip the user review step and save directly.

## Backwards Compatibility & Batch Upgrade

Every analysis file carries an implicit version based on which sections are present. When the user says "upgrade all", "update all", or "backfill":

1. Scan all files in `Meetings/Analysis/` under `Clients/` (and legacy `Jobs To Be Done/` paths)
2. Detect each file's version by checking which sections exist (SERIES, EXPECTATION MAP, CONNECTIONS, etc.)
3. Report grouped counts of what's missing
4. Launch background agents to backfill: SERIES (from DB query), EXPECTATION MAP (from raw transcript via expectation-mapper), CONNECTIONS (from CRM lookups), Notion DB records
5. Update Notion page bodies with full text after upgrade
6. Log results to `Clients/_upgrade-log.md`

See `commands/jtbd-analysis.md` Step 7 for the full version detection table and upgrade procedures.
