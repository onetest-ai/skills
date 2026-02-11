# pause

Preserve cognitive state before stopping work. Creates a structured handoff note with current state, decisions, and exact next steps for seamless resume.

## Usage

```
/pause
```

## What It Does

1. Reads current plan (todos) and STATE.md
2. Assesses what's completed, in-progress, and remaining
3. Creates a structured handoff note in STATE.md
4. Records decisions, blockers, and concrete next steps

## When to Use

- Before ending a work session
- Before switching to a different task
- When handing off work to another agent or person
- When you need to save progress on a long-running task

## Notes

- This is a user-only command (`model-invocation: false`) — the agent won't invoke it proactively
- The handoff note is saved to STATE.md and persists across sessions
