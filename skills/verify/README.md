# verify

Conversational verification and user acceptance testing. Walks through expected behaviors one by one, infers severity from responses, and auto-plans fixes for issues found.

## Usage

```
/verify
/verify check the new authentication flow
```

Or complete a task — the agent may invoke this skill proactively to verify results.

## What It Does

1. Gathers context from plan and STATE.md
2. Generates prioritized test cases (critical path → edge cases → integration → regression)
3. Walks through tests one at a time with the user
4. Infers issue severity from user language (never asks "how severe?")
5. Produces a results summary grouped by severity
6. Auto-plans fixes for blockers and major issues

## Severity Inference

| User says... | Severity |
|---|---|
| "crashes", "error", "broken" | Blocker |
| "doesn't work", "wrong result" | Major |
| "works but...", "mostly ok" | Minor |
| "color", "spacing", "nitpick" | Cosmetic |
