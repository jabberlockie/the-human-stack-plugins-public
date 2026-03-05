# Plans Directory

This directory contains task documentation and planning artifacts.

## File Types

### Active Plans
- `{timestamp}-plan.md` - Auto-created when plans are approved
- Contains commit hash and session export links

### Backlog
- `backlog.md` - Future enhancements queue

### Feature Plans
- `{feature-name}.md` - Detailed plans for specific features

## Plan Lifecycle

1. **Create**: Write plan for new feature
2. **Approve**: Use ExitPlanMode to approve (triggers commit + session export)
3. **Execute**: Implement the plan
4. **Archive**: Move to `docs/architect/archive/{feature}/` when complete

## Auto-Generated Plans

When you use `ExitPlanMode` to approve a plan, the `plan-approved.sh` hook:
1. Commits all staged changes
2. Exports the current session
3. Creates a plan doc with links to both

## Format

```markdown
# Plan: Feature Name

## References
- **Commit**: `abc1234`
- **Session**: [timestamp-session.md](../sessions/timestamp-session.md)

## Summary
What was planned and approved.

## Details
Implementation specifics.
```
