# map-codebase

Analyze an existing codebase in parallel — produces structured docs on tech stack, architecture, quality, and concerns. Use when onboarding to a new project.

## Usage

```
/map-codebase
/map-codebase /path/to/project
```

## What It Does

1. Identifies the target project directory
2. Runs 4 parallel analysis passes:
   - Technology & Stack
   - Architecture & Structure
   - Code Quality
   - Concerns & Risks
3. Synthesizes results into a structured map
4. Saves detailed docs to `.octo/codebase-maps/<project>/`

## Output

Creates 5 files per project:
- `MAP.md` — Executive summary
- `STACK.md` — Full tech stack analysis
- `ARCHITECTURE.md` — Architecture deep-dive
- `QUALITY.md` — Quality assessment
- `CONCERNS.md` — Risk register

## When to Use

- Onboarding to a new codebase
- Before starting a major refactor
- Periodic project health checks
- Understanding inherited or legacy code
