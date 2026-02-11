---
name: skill-creator
version: 1.0.0
author: onetest-ai
description: Guide for creating new Octo skills. Use when users want to create, update, or package a skill for the marketplace.
tags: [meta, development, skills, marketplace]
model-invocation: true

dependencies:
  python:
    - pyyaml
  npm: []
  mcp: []
  system: []

requires:
  - command: git
    reason: "Skills are distributed via GitHub"

permissions:
  filesystem: write
  network: false
  shell: true
  mcp_servers: []
---

# Skill Creator

You are helping the user create a new Octo skill for the marketplace. Skills are markdown-based workflow instructions that extend Octo's capabilities.

## Skill Anatomy

A skill is a directory containing:

```
my-skill/
├── SKILL.md          # REQUIRED — frontmatter + instructions
├── README.md         # Recommended — human documentation
├── scripts/          # Optional — executable code (Python/Bash)
├── references/       # Optional — docs loaded on demand by the agent
└── assets/           # Optional — templates, images, fonts
```

### Progressive Disclosure (3 Levels)

1. **Metadata** (always in context, ~100 tokens) — `name` + `description` from frontmatter
2. **SKILL.md body** (loaded when triggered) — workflow instructions, keep under 500 lines
3. **Bundled resources** (loaded on demand) — `references/`, `scripts/`, `assets/`

The `description` field is the trigger mechanism — it tells the agent WHEN to use the skill. Write it to describe both what the skill does AND when to activate it.

### Frontmatter Specification

```yaml
---
name: my-skill                   # Lowercase with dashes, must match directory name
version: 1.0.0                   # Semantic versioning
author: github-username
description: >-
  What the skill does AND when to use it. This is always in context
  and serves as the trigger mechanism. Max 120 chars for search, but
  can be longer for trigger accuracy.
tags: [category1, category2]
model-invocation: true           # true = agent can invoke proactively

dependencies:
  python: []                     # pip packages needed
  npm: []                        # npm global packages
  mcp: []                        # MCP server configs
  system: []                     # System packages (prompt-only)

requires: []                     # Pre-checks: commands, env vars

permissions:
  filesystem: read               # read | write | execute
  network: false
  shell: false
  mcp_servers: []
---
```

## Creation Process

### 1. Understand the Skill

Ask the user:
- **What does it do?** — Concrete examples of input → output
- **When should it trigger?** — What user requests activate it?
- **What tools does it need?** — Read, Bash, MCP tools, external APIs?
- **What's the workflow?** — Sequential steps, decision trees, parallel tasks?

### 2. Plan Reusable Contents

From the examples, identify:
- **Scripts** — Repetitive operations that benefit from exact code (e.g., file conversion, validation, API calls)
- **References** — Domain knowledge too large for SKILL.md body (e.g., API docs, format specs, style guides)
- **Assets** — Files used in output (templates, schemas, fonts)

### 3. Initialize the Skill

Create the directory structure:

```bash
mkdir -p skills/my-skill/{scripts,references}
```

### 4. Write the Skill

**Frontmatter:**
- `name`: lowercase-with-dashes, matches directory name
- `description`: serves as trigger — describe WHEN to use, not just WHAT it does
- `tags`: 2-5 relevant categories
- `dependencies`: only what's actually needed

**Body structure:**
```markdown
# Skill Title

Brief overview of purpose and philosophy.

## Process

### 1. Phase Name
What to do, tools to use, expected output.

### 2. Phase Name
...

## Guidelines
- Dos and don'ts
- Quality standards
- When to escalate

## Guardrails
- Scope limits
- Error handling approach
- Context budget
```

**Key principles:**
- **Concise is key** — Context window is a shared resource. Only include what the agent doesn't already know.
- **Appropriate freedom** — High freedom (text instructions) for variable tasks, low freedom (specific scripts) for fragile operations.
- **Anti-patterns** — Explicitly list what NOT to do. This prevents generic AI output.
- **Scripts as black boxes** — Include `--help` in scripts so the agent runs them without reading source.

### 5. Validate

Run the marketplace validator:

```bash
python /path/to/skills-repo/scripts/validate_skill.py skills/my-skill/SKILL.md
```

Check:
- Required frontmatter fields present
- Name matches directory
- Valid semver version
- Description under 120 chars
- At least 1 tag
- No dangerous commands in body

### 6. Test and Iterate

1. Install locally: `octo skills install my-skill --local ./skills/my-skill`
2. Test with real requests — does it trigger correctly? Does the workflow produce good output?
3. Refine instructions based on what worked and what didn't
4. Check context usage — is the skill body too large? Move content to `references/`

## Workflow Patterns

See `references/workflows.md` for detailed patterns:

- **Sequential** — Step-by-step phases (most common)
- **Conditional** — Decision trees based on input type
- **Parallel** — Multiple agents working simultaneously
- **Iterative** — Build → verify → fix loops

## Output Patterns

See `references/output-patterns.md` for content organization:

- **Template pattern** — Fill in a provided template
- **Examples pattern** — Generate based on examples
- **Progressive refinement** — Draft → review → refine cycle

## Guidelines

- Keep SKILL.md under 500 lines — split large content into `references/`
- Write the description as a trigger — "Use when..." not just "Does..."
- Test with users who didn't write the skill — it should work without explanation
- Include a README.md for human readers (not loaded by the agent)
- Don't include: CHANGELOG, INSTALLATION_GUIDE, or redundant docs
