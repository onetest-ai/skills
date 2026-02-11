# Octo Skills Marketplace

A curated collection of skills for [Octo](https://github.com/onetest-ai/Octo) — the LangGraph multi-agent CLI.

Skills are markdown-based workflow instructions that guide Octo's agents. They're lightweight (kilobytes, not megabytes), language-agnostic, and require zero backend infrastructure.

## Quick Start

```bash
# Search for skills
octo skills search "codebase"

# View skill details
octo skills info map-codebase

# Install a skill
octo skills install map-codebase

# Install with dependencies
octo skills install map-codebase --deps

# List installed skills
octo skills list

# Update all skills
octo skills update --all
```

## Available Skills

### Workflow

| Skill | Description | Tags |
|-------|-------------|------|
| [quick](skills/quick/) | Execute ad-hoc tasks quickly without heavyweight planning | development, quick-fix |
| [verify](skills/verify/) | Conversational verification and user acceptance testing | testing, qa |
| [discuss](skills/discuss/) | Structured requirements discussion with gray-area identification | planning, requirements |
| [pause](skills/pause/) | Preserve cognitive state before stopping work | workflow, handoff |
| [doc-coauthoring](skills/doc-coauthoring/) | Structured 3-stage workflow for co-authoring docs and specs | writing, collaboration |
| [map-codebase](skills/map-codebase/) | Parallel codebase analysis for onboarding | analysis, documentation |

### Document Processing

| Skill | Description | Dependencies |
|-------|-------------|-------------|
| [pdf](skills/pdf/) | Read, create, merge, split, watermark, fill forms, encrypt, OCR | pypdf, pdfplumber, reportlab |
| [docx](skills/docx/) | Create, read, and edit Word documents | python-docx, pandoc |
| [xlsx](skills/xlsx/) | Create, read, edit, and analyze Excel spreadsheets | openpyxl, pandas |
| [pptx](skills/pptx/) | Create and edit PowerPoint presentations with design guidelines | python-pptx, Pillow |

### Meta

| Skill | Description |
|-------|-------------|
| [skill-creator](skills/skill-creator/) | Guide for creating new Octo skills for the marketplace |

## How Skills Work

A skill is a directory containing a `SKILL.md` file with YAML frontmatter and markdown instructions:

```yaml
---
name: my-skill
version: 1.0.0
author: your-github-username
description: One-line description for search results
tags: [category1, category2]
model-invocation: true

dependencies:
  python: []
  npm: []
  mcp: []
  system: []
---

# Skill Title

Your workflow instructions here...
```

When invoked (via `/my-skill` command or proactively by the agent), the skill body is injected into the conversation as workflow instructions for the supervisor agent.

## Creating a Skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick version:

1. Fork this repo
2. Copy `templates/SKILL_TEMPLATE.md` to `skills/your-skill/SKILL.md`
3. Fill in the frontmatter and write your instructions
4. Add a `README.md` to your skill directory
5. Submit a PR

## Registry

The [`registry.json`](registry.json) file is auto-generated from skill frontmatter and git stats. It's rebuilt on every push to `main` and daily via GitHub Actions. The Octo CLI fetches this file for search and install operations.

## License

MIT
