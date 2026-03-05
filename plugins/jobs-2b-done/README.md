# Jobs 2B Done

JTBD (Jobs to be Done) call transcript analysis plugin for The Human Stack. Analyzes sales, coaching, and industry calls through a structured framework, enriches with CRM and knowledge base connections, saves to organized folders, and populates a queryable Notion database.

## Commands

### `jtbd-analysis`
Run JTBD analysis on a single call transcript. Accepts pasted text, a conversation intelligence URL, or a Notion meeting transcript. Outputs a structured analysis with a CONNECTIONS section linking to HubSpot, Clay, and Notion records. Saves to a company folder under the appropriate top-level folder in `Jobs To Be Done/`, then creates a record in the JTBD Analyses Notion database.

### `jtbd-synthesis`
Synthesize patterns across multiple JTBD analyses. Scopes to all calls, a single folder, a single company, a date range, or engagement stage. Cross-references established findings, validates archetypes, and tracks evidence levels (N=1 hypothesis, N=2 pattern, N=3+ finding). Can query the JTBD Analyses Notion DB for filtered access.

## Databases

| Database | Notion ID | Data Source | Purpose |
|----------|-----------|-------------|---------|
| JTBD Analyses | `2f218faa725b41828194e8fc0f93453b` | `collection://fbf274fd-5cf0-4afe-9eaf-cb511cae6b94` | Queryable index of all analyses |
| Meeting Transcripts | `8368d3474cac4e71bf945934fce957f7` | `collection://669e7e0b-dfe6-43c4-b4c3-d7b734e06ed5` | Source transcripts |

## Connectors

| Connector | Purpose |
|-----------|---------|
| HubSpot | Company, contact, and deal lookups for CONNECTIONS section |
| Notion | Meeting transcript retrieval, page linking, JTBD Analyses DB population |
| Fireflies | Call transcript retrieval |
| Clay | Contact/company enrichment |

## Workspace

Analyses live in `Jobs To Be Done/` organized by top-level folders, each with `Calls & Meetings/[Company]/` and `Synthesis/` subfolders. The prompts, templates, and plugin files live in `Jobs 2B Done - Plugin & Skills/`.
