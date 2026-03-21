---
name: ship
description: >
  Pick the highest-priority unblocked Linear issue, build it, open a PR, and
  update issue state. Use for "/ship", "/ship next", "/ship HOARD-XX".
---

# Ship Skill

Pick the next item from Linear, branch, build, test, open a PR, and transition
the issue through In Progress -> In Review -> Done.

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

| Invocation         | Action                                             |
|--------------------|----------------------------------------------------|
| `/ship`            | Pick next unblocked item, build, PR, done          |
| `/ship next`       | Same as `/ship`                                    |
| `/ship HOARD-XX`   | Ship a specific issue                              |

## Step 1: Find the Project

Resolve the Linear team from context:
- Check `docs/architect/master_intent.md` for the active team key (e.g. `HOARD`)
- Or ask the user: "Which Linear team? (e.g. HOARD)"

## Step 2: Pick an Item

If a specific identifier was given (e.g. `HOARD-26`), fetch that issue:

```graphql
{
  issue(id: "HOARD-26") {
    id
    identifier
    title
    description
    priority
    state { id name type }
    blockedBy { nodes { identifier state { name type } } }
    team { id key states { nodes { id name type } } }
  }
}
```

If no identifier given, fetch the highest-priority unblocked Todo issue:

```graphql
{
  issues(
    filter: {
      team: { key: { eq: "HOARD" } }
      state: { type: { in: ["unstarted"] } }
    }
    orderBy: priority
    first: 20
  ) {
    nodes {
      id
      identifier
      title
      description
      priority
      state { id name type }
      blockedBy { nodes { identifier state { name type } } }
      team { id key states { nodes { id name type } } }
    }
  }
}
```

Filter locally: pick the first issue where ALL `blockedBy` items have state type `completed`.

If no unblocked items exist, report: "No unblocked items ready. Check blockers." and stop.

## Step 3: Confirm Selection

Show the user what will be built:

```
ITEM: [HOARD-XX] Title
PRIORITY: P1 (Urgent)
DESCRIPTION: <first 2-3 sentences>
```

## Step 4: Transition to In Progress

Fetch the "In Progress" state ID from the team's states:

```graphql
{
  team(id: "<team-id>") {
    states { nodes { id name type } }
  }
}
```

Find the state where `type == "started"` and `name == "In Progress"`.

Update the issue:

```graphql
mutation {
  issueUpdate(id: "<issue-id>", input: { stateId: "<in-progress-state-id>" }) {
    success
    issue { identifier state { name } }
  }
}
```

## Step 5: Create a Branch

Create a git branch named after the issue:

```bash
BRANCH="feature/hoard-XX-short-title"
git checkout -b $BRANCH
```

Branch naming: `feature/<team-key-lowercase>-<number>-<slug>`
- `HOARD-26` + "Create RLS policies" -> `feature/hoard-26-rls-policies`

## Step 6: Build the Thing

Execute the work described in the issue. Follow the project's CLAUDE.md for conventions:
- Tech stack, testing approach, commit format
- Do NOT skip tests if they are required

Commit often with the issue reference:

```bash
git add <files>
git commit -m "feat: description (HOARD-XX)"
```

## Step 7: Open a Pull Request

Push the branch and open a PR:

```bash
git push -u origin $BRANCH
gh pr create \
  --title "[HOARD-XX] Short title" \
  --body "Closes HOARD-XX

## What
<what was built>

## Why
<why it was needed>

## Verified
<how it was tested>"
```

## Step 8: Transition to In Review

Find the "In Review" state ID (type: `started`, name: `In Review`).

Update the issue to In Review:

```graphql
mutation {
  issueUpdate(id: "<issue-id>", input: { stateId: "<in-review-state-id>" }) {
    success
    issue { identifier state { name } }
  }
}
```

## Step 9: Merge and Close

Once the PR is approved and merged:

1. Delete the feature branch (optional, GitHub can do this automatically)
2. Transition issue to Done:

Find "Done" state (type: `completed`).

```graphql
mutation {
  issueUpdate(id: "<issue-id>", input: { stateId: "<done-state-id>" }) {
    success
    issue { identifier state { name } }
  }
}
```

## State Transition Summary

```
Todo -> In Progress  (Step 4: before branching)
In Progress -> In Review  (Step 8: after PR opened)
In Review -> Done  (Step 9: after merged)
```

## Output Format

```
SHIPPING: [HOARD-XX] Title
BRANCH: feature/hoard-XX-title
STATUS: In Progress

[build work happens]

PR: https://github.com/org/repo/pull/N
STATUS: In Review

DONE: [HOARD-XX] moved to Done
```

## Notes

- Never skip the In Progress transition -- it signals to the team that work has started
- If the PR push fails (no write access), commit locally and report the blocker
- The git branch/PR/merge flow is unchanged from GitHub workflow -- only the board management uses Linear
- If working from a shift context (no interactive user), pick the item automatically without confirmation
