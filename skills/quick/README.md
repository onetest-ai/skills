# quick

Execute ad-hoc tasks quickly — minimal planning, no heavyweight agents. Use for small fixes, one-off changes, and simple features.

## Usage

```
/quick fix the typo in README
/quick add a --verbose flag to the CLI
```

Or just describe a small task — the agent will invoke this skill proactively if it's a good fit.

## What It Does

1. Assesses task scope (tiny / small / too big)
2. Creates a 1-3 item quick plan
3. Executes with appropriate tools or worker agents
4. Verifies results with lightweight checks
5. Updates state and reports back

## When to Use

- Single file changes
- Config tweaks
- Small bug fixes
- Adding a simple function
- One-off refactors

## When NOT to Use

- Multi-file architecture changes
- New subsystems
- Tasks requiring research or requirements gathering
- Changes to public APIs or database schemas
