# Output Patterns for Skills

## Template Pattern

Provide a template that the agent fills in. Good for structured output with consistent format.

**How it works:**
1. Skill body defines the template structure
2. Agent gathers information to fill each section
3. Output follows the template exactly

**Example:**
```markdown
### Output Template

# [Project Name] — Codebase Map

## Quick Facts
- Language: [fill]
- Framework: [fill]
- Size: [fill]

## Architecture
[1-2 paragraph summary]

## Top Concerns
1. [fill]
2. [fill]
```

**When to use:** Reports, assessments, summaries, any output where structure matters.

## Examples Pattern

Provide examples of good output. The agent learns the style and format from examples rather than explicit rules.

**How it works:**
1. Skill body includes 2-3 examples of good output
2. Agent matches the style, tone, and format
3. Output is original but stylistically consistent

**When to use:** Creative output, communications, anything where "feel" matters more than structure.

**Tips:**
- Include diverse examples (different topics, lengths)
- Annotate examples with what makes them good
- Avoid examples that are too similar (agent will interpolate)

## Progressive Refinement Pattern

Output improves through multiple passes. Each pass focuses on a different aspect.

**How it works:**
1. First pass: content and structure
2. Second pass: clarity and conciseness
3. Third pass: polish and formatting
4. (Optional) Fourth pass: reader testing

**When to use:** Long-form content, technical documentation, anything where quality matters.

**Template:**
```markdown
### 1. Draft
Write the full content focusing on completeness and accuracy.

### 2. Refine
Re-read and improve:
- Remove redundancy
- Tighten prose
- Fix logical flow

### 3. Polish
Final pass:
- Check formatting consistency
- Verify all links/references
- Proofread for errors
```

## Accumulation Pattern

Build output incrementally by adding pieces. Good for complex documents assembled from multiple sources.

**How it works:**
1. Create a scaffold with section placeholders
2. Fill sections one at a time
3. Each section can trigger its own sub-workflow
4. Final pass for coherence across sections

**When to use:** Large documents, multi-source reports, anything too big to write in one pass.
