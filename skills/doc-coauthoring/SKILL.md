---
name: doc-coauthoring
version: 1.0.0
author: onetest-ai
description: Structured 3-stage workflow for co-authoring docs, proposals, specs, and decision documents.
tags: [writing, documentation, collaboration, workflow]
model-invocation: true

dependencies:
  python: []
  npm: []
  mcp: []
  system: []

requires: []

permissions:
  filesystem: write
  network: false
  shell: false
  mcp_servers: []
---

# Document Co-Authoring

You are guiding the user through a structured 3-stage workflow for co-authoring documentation. This produces better results than freeform writing because it separates context gathering, refinement, and verification into distinct phases.

## When to Use

Trigger on requests like: "write a doc", "draft a proposal", "create a spec", "PRD", "design doc", "RFC", "technical spec", "decision doc", or any structured content creation. Offer the 3-stage workflow. If the user declines, work freeform.

## Stage 1: Context Gathering

### Meta-Context Questions

Start by understanding the big picture. Ask these 5 questions (adapt to context):

1. **Document type** — What kind of doc is this? (proposal, spec, RFC, guide, memo, etc.)
2. **Audience** — Who will read this? What do they already know?
3. **Desired impact** — What should the reader think/do/feel after reading?
4. **Template or examples** — Any existing docs to match in style or structure?
5. **Constraints** — Length limits, format requirements, deadlines, approval process?

### Info Dumping

Encourage the user to dump ALL context they have:

> "Tell me everything relevant — background, prior discussions, alternatives considered, org context, timeline pressures, technical constraints, stakeholder concerns. Don't worry about structure, I'll organize it."

Pull from available integrations (Slack, GitHub issues, existing docs) if the user points to them.

### Clarifying Questions

After the brain dump, ask 5-10 targeted questions based on gaps you identified. Focus on:
- Edge cases and trade-offs
- Audience-specific concerns
- Missing technical details
- Implicit assumptions that should be explicit

**Exit criteria:** You can discuss edge cases and trade-offs without needing to ask about basics.

## Stage 2: Refinement & Structure

### Section-by-Section Building

For each section of the document:

1. **Clarifying questions** — What belongs in this section?
2. **Brainstorm options** — Generate 5-20 possible approaches/framings
3. **User curates** — Keep, remove, combine, or rephrase
4. **Gap check** — What's missing?
5. **Draft** — Write the section
6. **Iterate** — Refine based on feedback

### Section Ordering

Start with the hardest parts first:
- **Decision docs**: core proposal and alternatives first
- **Technical specs**: technical approach first
- **Proposals**: value proposition first
- **Always**: executive summary / abstract LAST (needs full context)

### Working Document

Create a scaffold with clear section placeholders. Build it incrementally using `update_state_md` or write to a workspace file. Use targeted edits — never rewrite the whole document from scratch unless the user asks.

### Quality Checkpoints

After 3 consecutive revision passes with no changes:
- Ask: "What can we remove? Shorter is almost always better."
- Check for: redundancy, filler phrases, passive voice, unclear referents

When the document is ~80% complete:
- Re-read the entire document end-to-end
- Check for: flow between sections, consistent terminology, redundant content, filler/slop
- Verify the document achieves the desired impact from Stage 1

## Stage 3: Reader Testing

### With Sub-Agents (Preferred)

1. **Predict questions** — List 5-10 questions a reader would have after reading
2. **Test with fresh context** — Delegate to a worker agent that ONLY sees the document (no conversation history). Ask it to:
   - Summarize the document in 2-3 sentences
   - List the key decisions/recommendations
   - Identify anything unclear or missing
   - Answer the predicted questions
3. **Analyze gaps** — Where did the fresh reader struggle or get it wrong?
4. **Fix and re-test** — Address gaps, test again

### Without Sub-Agents

1. Generate a testing prompt the user can paste into a fresh conversation
2. Include the document and predicted questions
3. User reports back with findings
4. Address issues together

**Exit criteria:** A fresh reader consistently understands the document and answers questions correctly with no new gaps.

## Final Review

- User does a final read-through
- Double-check: facts, links, technical details, names, dates
- Verify the desired impact is achieved
- Save the final version

## Guidelines

- **Direct, procedural tone** — Guide the user step by step, don't lecture
- **Handle deviations gracefully** — If the user skips a stage or goes off-track, note where you are and adapt
- **Manage context proactively** — If the conversation grows long, summarize periodically
- **Quality over speed** — Better to spend an extra round refining than to ship something mediocre
- **Appendices for depth** — If a topic needs detail that would bloat the main doc, suggest an appendix
