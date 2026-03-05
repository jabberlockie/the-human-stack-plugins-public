---
description: Run Jobs-to-be-Done analysis on a call transcript from pasted text, ~~conversation intelligence link, or ~~knowledge base meeting transcript. Saves to company folder with ~~CRM connections and populates the JTBD Analyses Notion database.
argument-hint: "<transcript text, Notion link, or Fathom/app URL>"
---

# JTBD Call Analysis

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Analyze a call transcript through Tim Lockie's Jobs-to-be-Done framework with UXinator Expectation Mapping. Produces a structured analysis file saved to a company folder under `Jobs To Be Done/`, then creates a corresponding record in the **JTBD Analyses** Notion database.

**Related commands:** Use after sales calls (pairs with `sales:call-summary`), for product research synthesis (pairs with `product-management:synthesize-research`), and for productivity tracking (pairs with `productivity:update`).

## Dispatch Architecture

**This command runs as a background agent.** The main conversation is a thin dispatcher:

1. **Read** this command file and the SKILL.md
2. **Acquire the transcript** (Step 1 only -- this happens in the foreground so the user can provide input)
3. **Extract company, participants, date** from the transcript (Step 2 -- no user input needed, path is deterministic)
4. **Launch a background agent** for everything else (Steps 2b through 6)

```
Agent(
  subagent_type: "general-purpose",
  description: "JTBD Analysis: {company} ({date})",
  run_in_background: true,
  prompt: "You are the autonomous JTBD analysis runner. Run the FULL analysis
    pipeline without stopping. Never ask questions. Never wait for approval.

    ## Input
    Company: {company}
    Participants: {participants}
    Call Date: {date}
    Save Path: /Users/tim/Dev/claude-cowork/Clients/{company}/Meetings/Analysis/
    Transcript Source: {notion_url_or_'pasted'}
    Fathom Recording: {fathom_url_or_'[Add link]'}

    ## Transcript
    {full_transcript_text}

    ## Instructions
    Follow the JTBD Analysis command Steps 2b through 6:
    - Create directory structure if needed (Meetings/Analysis/, Meetings/Transcripts/, Synthesis/)
    - Step 2b: Query JTBD Analyses DB for series context
    - Step 3: Run full 9-dimension JTBD analysis
    - Step 4: Build CONNECTIONS section (run CRM lookups)
    - Step 5: Save .md file to Meetings/Analysis/
    - Step 5b: Run uxinator:expectation-mapper against the raw transcript, append output
    - Step 6: Push to Notion (full text, use curl fallback if MCP truncates)

    Do NOT stop on errors. Retry once, log, and continue.
    Do NOT prompt the user about anything.

    ## JTBD Analysis SKILL.md
    {paste full SKILL.md content}

    ## UXinator Expectation Mapper
    Invoke the uxinator:expectation-mapper skill with the raw transcript.
    Append the FULL output under ## EXPECTATION MAP at the end of the document.

    ## JTBD Analysis Prompt
    {paste JTBD-Analysis-Prompt.md content if it exists, otherwise use the
     9-dimension framework from the SKILL.md}"
)
```

**After dispatching**, tell the user:
- "JTBD analysis for {company} is running in the background."
- "It will save to `{file_path}` and push to the JTBD Analyses Notion DB."
- Do NOT block waiting for results.

## Key References

- **JTBD Analyses Notion DB**: `2f218faa725b41828194e8fc0f93453b`
- **JTBD Analyses Data Source**: `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`
- **Meeting Transcripts DB**: `8368d3474cac4e71bf945934fce957f7`, collection `669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5`
- **HubSpot Portal**: `22283601`
- **Database Schema**: Inline below in Step 6b (authoritative source for all valid property values)

## Workspace Structure

All analyses are stored under a single, consistent path:

```
/Users/tim/Dev/claude-cowork/Clients/[Organization Name]/
├── Meetings/
│   ├── Transcripts/        ← raw transcripts
│   └── Analysis/           ← JTBD analysis files (this plugin writes here)
└── Synthesis/              ← cross-call synthesis reports
```

**Always create the directory structure if it doesn't exist.** Never ask the user which folder to use.

---

## Workflow

### 1. Acquire Transcript

Accept transcript from ONE of these sources. If unclear, ask which:

**Option A — Pasted text**: User pastes transcript directly. Use as-is.

**Option B — ~~conversation intelligence link**: User provides a URL (e.g., Fathom, Fireflies, Gong). Use WebFetch to retrieve transcript content. Save the source URL for the Fathom Recording connection field.

**Option C — ~~knowledge base Meeting Transcript**: User provides either:
- A direct Notion page link → Use `notion-fetch` tool to retrieve it
- A company/meeting name to search → Use `notion-search` tool with `data_source_url: "collection://669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5"` to find the transcript in the Meeting Transcripts database (ID: `8368d3474cac4e71bf945934fce957f7`). If multiple matches, present options and ask user to pick.

**Extract from ~~knowledge base transcripts:**
- Notion page ID/URL (for Connections section and Meeting Transcript link)
- `Fathom ID` property (if present, construct Fathom video link)
- `Fathom Invitees` / `Attendees 1` properties (participant names)
- Page title and created date (for file naming)
- Full transcript content from page body

### 2. Identify Company, Participants & Path

From the transcript content, extract:
- **Company name** — the prospect/client organization (NOT The Human Stack)
- **Individual participant names** and their roles
- **Call date** — from metadata, transcript header, or ask user

**Path is always deterministic -- never ask the user:**

```
/Users/tim/Dev/claude-cowork/Clients/[Organization Name]/Meetings/Analysis/
```

1. Check if the organization already has a folder under `/Users/tim/Dev/claude-cowork/Clients/` (fuzzy match at >=90% similarity, case-insensitive)
2. If a match exists, use that folder name exactly
3. If no match, create the full path: `Clients/[Organization Name]/Meetings/Analysis/`
4. Also ensure `Meetings/Transcripts/` and `Synthesis/` exist alongside

### 2b. Determine Series Context

If this organization has prior JTBD analyses, this call is part of a **series**. Determine the session number and link to the previous session.

**Procedure:**

1. **Query the JTBD Analyses Notion DB** — use `notion-query-database-view` with data source `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`, filtering by `Organization` matching the company name identified in Step 2. Sort by `date:Date:start` ascending.
2. **Count results** — the number of existing records = number of prior sessions. This session's number = count + 1.
3. **Get the most recent record** — save its Notion page URL as the "Previous Session" link.
4. **If count = 0** — this is Session 1. No series context needed; skip the SERIES section in the output.

**Add a `Plugin Version` line** at the bottom of `## CONTEXT METADATA`:

```markdown
**Plugin Version**: 5.0.0
```

**Add a `## SERIES` section** immediately after `## CONTEXT METADATA` in the analysis output:

```markdown
## SERIES

**Session**: [N] (of [total] with [Organization])
**Previous Session**: [Notion page URL of most recent JTBD analysis for this org, or "First session"]
**JTBD Evolution**: [1-2 sentences describing how the client's primary JTBD has shifted since the previous session. Compare the previous session's PRIMARY JTBD one-sentence synthesis with this session's. If Session 1, write "Baseline session — no prior reference."]
```

**File naming for series sessions**: When Session >= 2, include the session number in the filename:
- `[YYYY-MM-DD] - [First Last, Company Name] - Session [N] - JTBD Analysis.md`

### 3. Load and Run JTBD Analysis

1. **Read the master prompt** from: `Jobs To Be Done/Jobs 2B Done - Plugin & Skills/JTBD-Analysis-Prompt.md`
2. **Apply the full prompt framework** to the transcript — all 9 analysis dimensions
3. **Generate the complete analysis** following the OUTPUT FORMAT in that prompt file
4. **Analysis rules:**
   - Be specific, not generic ("get 12-person team to use CRM for case notes" NOT "improve technology adoption")
   - Quote liberally with exact language from the transcript
   - Distinguish explicit statements from inferences (mark with [INFERRED] or [IMPLIED])
   - Flag contradictions between what they say vs. behavior/evidence
   - Intensity = importance (repeated phrases, long explanations, emotional language)
   - Context matters — same JTBD means different things from prospect vs. 90-day client

### 4. Build Connections Section

Prepend a `## CONNECTIONS` section at the top of the analysis. Populate each field:

```markdown
## CONNECTIONS

**Fathom Recording**: [URL from input or ~~knowledge base Fathom ID field, or "[Add link]"]
**Notion Meeting Notes**: [~~knowledge base page URL if source was Notion, or "[Add link]"]
**HubSpot Account**: [~~CRM company record link]
**HubSpot Contacts**: [~~CRM linked contact names]
**HubSpot Deal**: [~~CRM deal link or "[Add link]"]
**Clay URL**: [Clay enrichment URL if available, or "[Add link]"]
```

**~~CRM lookup procedure:**

1. **Company**: Search CRM objects (objectType: `COMPANY`) by company name. Get the company ID.
2. **Contacts**: For each participant name, search CRM objects (objectType: `CONTACT`). Get contact IDs.
3. **Deals**: Search CRM objects (objectType: `DEAL`) filtered by company association. Get active deal IDs.
4. **Construct URLs** using HubSpot portal ID `22283601`:
   - Company: `https://app.hubspot.com/contacts/22283601/record/0-2/{companyId}`
   - Contact: `https://app.hubspot.com/contacts/22283601/record/0-1/{contactId}`
   - Deal: `https://app.hubspot.com/contacts/22283601/record/0-3/{dealId}`
5. Format contacts as: `[Person Name](hubspot_url)`
6. If no ~~CRM match found: `[Person Name - Add link]`

### 5. Assemble and Save File

**File naming convention:**
- **Single external participant**: `[YYYY-MM-DD] - [First Last, Company Name] - JTBD Analysis.md`
- **Multiple participants from same org**: `[YYYY-MM-DD] - [Company Name] - JTBD Analysis.md`

Examples:
- `2025-07-02 - Haley MacDonald, Imagine Canada - JTBD Analysis.md`
- `2025-07-22 - Episcopal Relief & Development - JTBD Analysis.md`

**Save to**: `/Users/tim/Dev/claude-cowork/Clients/[Organization Name]/Meetings/Analysis/[filename].md`

**Always show the user the completed analysis before saving** so they can review.

### 5b. Generate Expectation Map (UXinator)

After the JTBD analysis is complete, run the **UXinator expectation-mapper** skill against the **raw transcript** (from Step 1) to generate an Expectation Map. Append the result as the final section of the document (after CONNECTIONS).

This bridges JTBD (what the client needs) with UX (what expectations exist and what Tim should do about them). The JTBD analysis looks at the client; the Expectation Map looks at the relationship between Tim and the client.

**How to run:**

1. Invoke the `uxinator:expectation-mapper` skill, passing the **raw transcript text** as input (NOT the JTBD analysis output).
2. The skill will produce a structured Expectation Map with three layers (Origins, Dynamics, Architecture) and an Expectation Math summary.
3. Append the full, unmodified skill output under a `## EXPECTATION MAP` heading at the end of the document.

**Do NOT:**
- Summarize or condense the expectation-mapper output.
- Rewrite the skill's tables or sections.
- Derive the map from the JTBD analysis -- it must come from the raw transcript independently.

**For series sessions (Session 2+):** When invoking the expectation-mapper, also provide the previous session's JTBD analysis (fetched from Notion in Step 2b) as additional context so the skill can identify how expectations have shifted.

### 6. Populate JTBD Analyses Notion Database

After saving the .md file, create a page in the **JTBD Analyses** database. This is the structured, queryable layer that links back to the full analysis and the source transcript.

**Database**: `2f218faa725b41828194e8fc0f93453b`
**Data source**: `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94`

Use `notion-create-pages` with `parent: { data_source_id: "fbf274fd-5cf0-4afe-9eaf-cb511cae6b94" }`.

#### 6a. Page Body Content (MANDATORY -- DO THIS FIRST)

The Notion page body MUST contain the **complete, unmodified analysis text** -- the exact same content saved in the .md file. This includes all sections: CONTEXT METADATA, SERIES, PRIMARY JTBD, DETAILED JTBD ANALYSIS, SWITCH TRIGGER, DESIRED OUTCOME, OBSTACLES & ANXIETIES, MESSAGING GOLD, AUDIENCE SEGMENT, IP & FRAMEWORK APPLICATION, PRODUCT/OFFERING IMPLICATIONS, PATTERN RECOGNITION, CONNECTIONS, and EXPECTATION MAP.

**HARD RULES:**
- Copy the ENTIRE .md file content into the page body. Every section, every quote, every line.
- Do NOT summarize, truncate, abbreviate, or paraphrase any part of the analysis.
- Do NOT skip sections to save space or reduce length.
- Do NOT rewrite headings, quotes, or formatting.
- The page body must be a verbatim copy of the saved .md file.
- If the Notion API has length limits, split across multiple content blocks -- never cut content.

**FULL-TEXT FALLBACK:** If the MCP `notion-create-pages` tool truncates or drops content (e.g., the page body is shorter than the .md file), use the Notion API directly via curl to append the missing content. Use the `NOTION_API_KEY` environment variable:

```bash
curl -X PATCH "https://api.notion.com/v1/blocks/{block_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{json_body_with_remaining_content}'
```

Split long content into paragraph blocks of ~2000 characters each. After pushing, fetch the page back with `notion-fetch` and verify the full content is present. If any section is missing, append it.

#### 6b. Property Mapping (exact valid values)

Extract properties from the completed analysis. For select/multi-select fields, use ONLY the exact values listed below. If a value from the analysis doesn't match any listed option, OMIT the field -- never guess or create new values.

**Text properties:**

| Property | Source |
|----------|--------|
| Name | File title (e.g., "2025-07-02 - Haley MacDonald, Imagine Canada") |
| Organization | Company name from Step 2 |
| Date | Call date from Step 2 (use `date:Date:start` with ISO-8601 date) |
| File Path | Full path where .md was saved |
| Primary JTBD | From `### PRIMARY JTBD` one-sentence synthesis |
| Quick Summary | From `### QUICK SUMMARY` -- concatenate all 5 summary lines |
| Persona Label | From `### AUDIENCE SEGMENT` -> Persona Label |
| Known Pattern | From `### PATTERN RECOGNITION` -> Known Pattern |
| Emerging Pattern | From `### PATTERN RECOGNITION` -> Emerging Pattern |
| HubSpot Contacts | From CONNECTIONS -- formatted as "Name (link), Name (link)" |
| Plugin Version | Always set to current plugin version (currently `5.0.0`) |

**Select properties (pick exactly ONE from the listed values):**

| Property | Source | Valid Values |
|----------|--------|-------------|
| Engagement Stage | `CONTEXT METADATA` -> Engagement Stage | `Pre-sale`, `Discovery`, `Active 0-90`, `Active 90+`, `Alumni` |
| Best-Fit Offering | `### PRODUCT/OFFERING IMPLICATIONS` | `Coaching`, `Diagnostic`, `Managed Success`, `Training`, `Speaking`, `Upskillerator` |
| Urgency Level | `### SWITCH TRIGGER` -> Urgency Level | `High`, `Medium`, `Low`, `Unclear` |
| Confidence Score | `### DETAILED JTBD ANALYSIS` | `High`, `Medium`, `Low` |
| Speaker Role | `CONTEXT METADATA` -> Primary Speaker role | `CEO/ED`, `COO/VP`, `CTO/Tech Director`, `Program Director`, `Development/Fundraising`, `Operations`, `Board Member`, `Consultant/Partner`, `Other` |
| Speaker POV | `CONTEXT METADATA` -> Primary Speaker POV | `Executive`, `Practitioner`, `Influencer`, `Champion`, `End User`, `Channel Partner` |
| Decision Authority | `### AUDIENCE SEGMENT` | `Decision-maker`, `Influencer`, `Champion`, `End User` |
| Org Size | `CONTEXT METADATA` -> Org Size | `Small (<50)`, `Mid (50-500)`, `Large (500+)` |
| Sector | `CONTEXT METADATA` -> Sector | `Human Services`, `Education`, `Health`, `Faith-based`, `Infrastructure`, `Arts`, `Environment`, `Cross-sector Consulting`, `Other` |

**Multi-select properties (pick one or more from the listed values, pass as JSON array):**

| Property | Source | Valid Values |
|----------|--------|-------------|
| Product Context | `CONTEXT METADATA` -> Product | `Diagnostic`, `Managed Success`, `Training`, `Speaking`, `Consulting` |
| Pillar Focus | `CONTEXT METADATA` -> Pillar | `Capacity`, `Strategy`, `Transformation` |
| Frameworks Applied | `### IP & FRAMEWORK APPLICATION` | `Digital Guidance`, `Digital Health Framework`, `Culture Eats Tech`, `Capacity Building`, `Orchestra Metaphor` |
| Themes | Scan analysis for theme indicators (see below) | `vendor-dependency`, `tech-trauma`, `lone-wolf`, `permission-to-lead`, `AI-anxiety`, `change-saturation`, `bright-shiny-object`, `training-gap`, `trust-deficit`, `silo`, `accidental-techie`, `governance-vacuum`, `channel-partner`, `strategy-execution-gap`, `lone-ranger-blocker` |

**URL properties (omit if value is `[Add link]` or empty):**

| Property | Source |
|----------|--------|
| Fathom Recording | From CONNECTIONS section |
| HubSpot Account | From CONNECTIONS section |
| HubSpot Deal | From CONNECTIONS section |
| Clay URL | From CONNECTIONS section |

**Relation property:**

| Property | Source |
|----------|--------|
| Meeting Transcript | Notion page URL of source transcript (from Step 1, Option C). This is a relation to collection `669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5`. |

#### 6c. Themes Detection

Scan the analysis for these theme indicators and tag accordingly:

| Theme tag | Indicators in transcript/analysis |
|-----------|----------------------------------|
| `vendor-dependency` | consultant/vendor lock-in, outsourced knowledge |
| `tech-trauma` | past failed implementations, burned by technology |
| `lone-wolf` | single person carrying all tech responsibility |
| `permission-to-lead` | seeking validation to make decisions |
| `AI-anxiety` | fear or uncertainty about AI adoption |
| `change-saturation` | too many changes happening at once |
| `bright-shiny-object` | chasing new tools without strategy |
| `training-gap` | staff lack skills to use systems |
| `trust-deficit` | low trust in systems, data, or leadership |
| `silo` | disconnected departments, data, or systems |
| `accidental-techie` | non-technical staff managing technology |
| `governance-vacuum` | no decision framework for technology |
| `channel-partner` | intermediary/partner relationship |
| `strategy-execution-gap` | good strategy but poor implementation |
| `lone-ranger-blocker` | individual blocking organizational progress |

### 7. Backwards Compatibility & Batch Upgrade

Every analysis file carries an implicit version based on which sections are present. When new features are added to the plugin, older files can be upgraded in batch.

#### 7a. Version Detection

Check for the `**Plugin Version**:` line in `## CONTEXT METADATA`. If present, use that version directly. If absent, infer from section markers:

| Section Present | Introduced In | Inferred Version |
|----------------|---------------|-----------------|
| `## CONTEXT METADATA` only | Original | v1.x |
| `## CONNECTIONS` | v2.0 | v2.x |
| `## QUICK SUMMARY` | v3.0 | v3.x |
| Notion DB record exists | v4.0 | v4.x |
| `## SERIES` + `## EXPECTATION MAP` | v5.0 | v5.0 |

**Detection logic**: First check for explicit `**Plugin Version**:` field. If missing, read the file and check for section headings -- the highest version marker present = the file's inferred version. When upgrading a file, always add the `**Plugin Version**:` field set to the current plugin version.

#### 7b. Batch Upgrade Command

When user says "upgrade all", "update all", "backfill", or "update connections":

1. **Scan** all `.md` files in `Meetings/Analysis/` subdirectories under `/Users/tim/Dev/claude-cowork/Clients/`
   - Also scan legacy paths: `Jobs To Be Done/*/Calls & Meetings/*/` for pre-v5 files
2. **Detect version** of each file using the table above
3. **Group by missing features** and report to user:
   ```
   Found 23 analysis files:
   - 5 files missing SERIES section (pre-v5)
   - 8 files missing EXPECTATION MAP (pre-v5)
   - 3 files missing CONNECTIONS (pre-v2)
   - 2 files have no Notion DB record (pre-v4)
   ```
4. **Upgrade in batch** — launch background agents (one per file or grouped by org) to backfill missing sections:

   **Missing SERIES**: Query JTBD Analyses DB for the org, count records by date to determine session number, insert `## SERIES` section after `## CONTEXT METADATA`.

   **Missing EXPECTATION MAP**: If a raw transcript is available (via Meeting Transcript relation in Notion, or in `Meetings/Transcripts/`), run `uxinator:expectation-mapper` against it and append the output. If no transcript is available, skip and log.

   **Missing CONNECTIONS**: Run CRM lookups (Step 4) and insert the section.

   **Missing Notion DB record**: Create one (Step 6) from the existing file content.

   **Incomplete CONNECTIONS** (contains `[Add link]`): Run CRM lookups for placeholder fields only — never overwrite existing links.

5. **After upgrading each file**, also update the corresponding Notion DB page body to include the new sections (full text, no truncation).

6. **Log results**: Write a summary to `/Users/tim/Dev/claude-cowork/Clients/_upgrade-log.md` with file paths, what was added, and any errors.

#### 7c. Legacy Path Migration

Files found in the old `Jobs To Be Done/` folder structure should be:
1. Copied to the new path (`Clients/[Org Name]/Meetings/Analysis/`)
2. Original left in place (do not delete -- user may have references)
3. `File Path` property on the Notion DB record updated to the new location

#### 7d. Future-Proofing

When adding new sections to the plugin in future versions:
1. Add a row to the version detection table (7a)
2. Add a backfill procedure to the batch upgrade (7b)
3. Bump the plugin version
4. Existing files will be auto-detected as needing upgrade on the next batch run

## Important Notes

- The `JTBD-Analysis-Prompt.md` in `Jobs 2B Done - Plugin & Skills/` is the single source of truth for methodology. Always read it fresh — it gets updated.
- Fuzzy match company folders aggressively. Only create new folders for clearly different organizations.
- ~~CRM searches may return multiple results. Use the most likely match. If ambiguous, ask.
- If the transcript source was ~~knowledge base, always include the page link in connections AND in the Meeting Transcript property.
- After saving, mention related next steps: run `jtbd-synthesis` to update cross-call patterns, log concepts with `thought-leadership-librarian`, or prep for next call with `sales:call-prep`.
- The Notion DB record is the queryable index. The .md file is the full human-readable analysis. Both get created every time.

## Background Execution

When running as a background agent or in batch mode:
- **Do NOT stop or ask for confirmation** on Bash tool failures. If a curl or API call fails, retry once, then log the error and continue with the next step.
- **Do NOT prompt the user** about file permissions, directory creation, or tool errors. Handle them silently.
- The only user interaction point is Step 5 ("show the user the completed analysis before saving"). In background mode, skip this and save directly.
- If the MCP Notion tools fail, fall back to the curl-based Notion API approach (see Step 6a) without asking.
