# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~CRM` might mean HubSpot or any other CRM with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (CRM, knowledge base, transcripts) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin


| Category              | Placeholder                   | Included servers | Other options              |
| --------------------- | ----------------------------- | ---------------- | -------------------------- |
| CRM                   | `~~CRM`                       | HubSpot          | Salesforce, Close, Copper  |
| Knowledge base        | `~~knowledge base`            | Notion           | Confluence, Guru           |
| Meeting transcription | `~~conversation intelligence` | Fireflies        | Gong, Fathom, Otter.ai    |
| Enrichment            | `~~enrichment`                | Clay             | Apollo, Clearbit           |


