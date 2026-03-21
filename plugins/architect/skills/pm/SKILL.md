---
name: pm
description: >
  Manage a Linear project board: fetch issues, assess state, plan waves by dependency,
  and update issue status. Use for "/pm", "/pm status", "/pm plan", "/pm wave".
---

# PM Skill

Fetch the Linear board, assess what is done/in-progress/blocked, build a dependency
graph, plan parallel work waves, and update issue states.

## Linear API Access

**Preferred:** Use Linear MCP tools when available (`mcp__plugin_linear_linear_*`).

**Fallback:** GraphQL via curl:

```bash
LINEAR_TOKEN=$(op-connect gc364u5r25bfme5mrvd3jj5yke credential)
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "<graphql>"}'
```

## Commands

| Invocation  | Action                                           |
|-------------|--------------------------------------------------|
| `/pm`       | Full board overview: fetch, assess, and summarize|
| `/pm plan`  | Dependency graph + wave plan                     |
| `/pm wave`  | Show the current executable wave (no blockers)   |

## Step 1: Resolve Team and Project

Determine the Linear team key from context:
- Check `docs/architect/master_intent.md` for the active team key (e.g. `HOARD`)
- Or ask the user: "Which Linear team? (e.g. HOARD)"

Fetch team details:

```graphql
{
  team(id: "<team-key-or-id>") {
    id
    name
    key
    projects { nodes { id name } }
    states { nodes { id name type position } }
  }
}
```

Alternative: query by key filter:

```graphql
{
  teams(filter: { key: { eq: "HOARD" } }) {
    nodes { id name key states { nodes { id name type } } }
  }
}
```

## Step 2: Fetch the Board

Query all issues for the team, including their state and blocker relations:

```graphql
{
  issues(
    filter: { team: { key: { eq: "HOARD" } } }
    orderBy: priority
  ) {
    nodes {
      identifier
      title
      priority
      state { id name type }
      blockedBy { nodes { identifier title state { name type } } }
      blocks { nodes { identifier title } }
      assignee { name }
      estimate
      labels { nodes { name } }
      updatedAt
    }
  }
}
```

Build a local board map keyed by `identifier`.

## Step 3: Board Assessment

Categorize issues by state type:

| State Type   | State Names                        | Meaning                  |
|--------------|------------------------------------|--------------------------|
| `unstarted`  | Backlog, Todo                      | Not yet started          |
| `started`    | In Progress, In Review             | Active work              |
| `completed`  | Done                               | Finished                 |
| `cancelled`  | Cancelled                          | Dropped                  |

For each unstarted issue, check if it is blocked:
- **Blocked**: has a `blockedBy` issue that is NOT in `completed` state
- **Unblocked**: no blockers, or all blockers are completed

Report:
```
Board: <team> (<N> issues)
  Done:        X
  In Progress: X
  In Review:   X
  Todo:        X (Y unblocked, Z blocked)
  Backlog:     X
```

## Step 4: Dependency Graph

For each unstarted issue, resolve its full blocker chain:

1. Mark issues with no active blockers as Wave 1 candidates
2. Mark issues blocked only by Wave 1 items as Wave 2 candidates
3. Continue until all issues are assigned to a wave

Output the graph as a text tree:

```
Wave 1 (executable now):
  HOARD-20 essence schema (P1)
  HOARD-22 ledger table (P2)

Wave 2 (unblocked after Wave 1):
  HOARD-26 RLS policies -- blocked by HOARD-20, HOARD-22

Wave 3:
  HOARD-30 bootstrap -- blocked by HOARD-26
```

## Step 5: Wave Planning

For the current wave, identify which items can run in parallel:
- Items with no shared blockers can run simultaneously
- Items that share a blocker must run sequentially (complete the blocker first)

Output a parallel execution plan:

```
Current wave (can run in parallel):
  Thread A: HOARD-20 -> HOARD-22
  Thread B: HOARD-21 (independent)

Start here: HOARD-20, HOARD-21 (no blockers)
```

## Step 6: Status Updates

To move an issue to a new state:

1. Fetch the state ID for the target state name:

```graphql
{
  team(id: "<team-id>") {
    states { nodes { id name type } }
  }
}
```

2. Update the issue:

```graphql
mutation {
  issueUpdate(id: "<issue-id>", input: { stateId: "<state-id>" }) {
    success
    issue { identifier state { name } }
  }
}
```

Or using MCP: `mcp__plugin_linear_linear_update_issue`

Confirm the update succeeded before reporting to the user.

## Output Format

```
BOARD: <team-name> (<N> total)
  Done:        X
  In Progress: X
  Todo:        X (Y ready)
  Blocked:     Z

WAVE 1 (start now):
  [HOARD-XX] Title (P1)
  [HOARD-YY] Title (P2)

WAVE 2 (after wave 1):
  [HOARD-ZZ] Title -- blocked by HOARD-XX
```

## Notes

- Priority: 1=Urgent, 2=High, 3=Medium, 4=Low
- Always sort within waves by priority (P1 first)
- Do NOT include completed or cancelled issues in wave planning
- If the board has no unblocked items, report that explicitly: "No unblocked items ready."
