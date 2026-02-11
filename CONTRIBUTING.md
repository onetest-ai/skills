# Contributing Skills

Thank you for contributing to the Octo Skills Marketplace!

## Skill Structure

Each skill lives in `skills/<skill-name>/` and must contain:

- **`SKILL.md`** (required) — Frontmatter + workflow instructions
- **`README.md`** (recommended) — Human-readable documentation, examples, screenshots

## Frontmatter Specification

```yaml
---
# Required
name: skill-name              # Lowercase with dashes, must match directory name
version: 1.0.0                # Semantic versioning (MAJOR.MINOR.PATCH)
author: github-username        # Your GitHub username
description: Brief summary     # One-liner shown in search results (max 120 chars)
tags: [cat1, cat2]            # For filtering (2-5 tags recommended)

# Optional
model-invocation: true         # true = agent can invoke proactively; false = user-only slash command

# Dependencies (all optional)
dependencies:
  python:                      # pip packages
    - playwright>=1.40.0
  npm:                         # npm global packages
    - @playwright/browser-chromium
  mcp:                         # MCP server configurations
    - server: playwright
      package: "@modelcontextprotocol/server-playwright"
      args: ["--browser", "chromium"]
      env:
        PLAYWRIGHT_BROWSERS_PATH: /usr/local/bin
  system:                      # System packages (displayed only, never auto-installed)
    - chromium

# Pre-checks (validated before install)
requires:
  - command: git               # Required CLI command
    reason: "Needed for repository cloning"
  - env: OPENAI_API_KEY        # Required environment variable
    reason: "Used for LLM calls"

# Permissions declaration
permissions:
  filesystem: read             # read | write | execute
  network: false               # Whether the skill needs network access
  shell: false                 # Whether the skill runs shell commands
  mcp_servers: []              # Which MCP servers the skill uses
---
```

## Naming Rules

- Use lowercase letters, numbers, and dashes only
- Directory name must match the `name` field in frontmatter
- Keep names short and descriptive (2-4 words max)
- Avoid generic names like "helper" or "utils"

## Writing Good Instructions

- **Be specific.** "Use the Read tool" is better than "read the file"
- **Include file paths** when referencing code locations
- **Structure with phases.** Process > Guidelines > Guardrails
- **Define done.** What does successful execution look like?
- **Set boundaries.** When should the skill escalate or stop?

## Submission Process

1. Fork this repository
2. Create your skill directory under `skills/`
3. Add `SKILL.md` with proper frontmatter
4. Add `README.md` with usage examples
5. Run validation locally: `python scripts/validate_skill.py skills/your-skill/SKILL.md`
6. Submit a Pull Request

## Validation

PRs are automatically validated by CI. The checks include:

- Required frontmatter fields present
- Valid semver version
- Directory name matches skill name
- No dangerous commands (`rm -rf`, `curl | bash`, `eval()`, `exec()`)
- Description under 120 characters
- At least 1 tag

## Review Process

All new skills are reviewed by a maintainer before merge. We check for:

- Clear, actionable instructions
- Appropriate permissions declarations
- No security concerns
- No duplicate functionality with existing skills

## Updating Existing Skills

- Bump the `version` field (follow semver)
- Describe changes in the PR description
- Backward-compatible changes = minor version bump
- Breaking changes = major version bump
