# Workflow Patterns for Skills

## Sequential Workflow

The most common pattern. Steps execute in order, each building on the previous.

```
1. Gather context → 2. Plan → 3. Execute → 4. Verify → 5. Report
```

**When to use:** Tasks with clear phases where each step needs the output of the previous one.

**Example:** The `quick` skill — understand → plan → execute → verify → update state.

**Template:**
```markdown
### 1. Phase Name
What to do. What tools to use. What output to produce.

### 2. Next Phase
Depends on output of Phase 1...
```

## Conditional Workflow

Decision tree based on input characteristics. Different paths for different situations.

```
Input → Classify → Path A (simple) → Done
                 → Path B (complex) → Sub-steps → Done
                 → Path C (unknown) → Escalate
```

**When to use:** Skills that handle multiple input types or scenarios.

**Example:** A document processing skill that handles .pdf, .docx, .xlsx differently.

**Template:**
```markdown
### 1. Classify the Request
Determine which category:
- **Type A**: [criteria] → go to Phase 2A
- **Type B**: [criteria] → go to Phase 2B
- **Unknown**: escalate to user

### 2A. Handle Type A
...

### 2B. Handle Type B
...
```

## Parallel Workflow

Multiple independent tasks that can run simultaneously via worker agents.

```
Input → Dispatch → Agent 1: Focus A ─┐
                → Agent 2: Focus B ─┤→ Synthesize → Output
                → Agent 3: Focus C ─┘
```

**When to use:** Analysis tasks where different aspects are independent.

**Example:** The `map-codebase` skill — 4 parallel analysis passes (stack, architecture, quality, concerns).

**Template:**
```markdown
### 1. Setup
Identify target and prepare context.

### 2. Parallel Analysis
Dispatch these tasks to worker agents simultaneously:

**Focus 1: [Area]**
- What to analyze
- Tools to use
- Expected output format

**Focus 2: [Area]**
...

### 3. Synthesize
Combine results into unified output.
```

## Iterative Workflow

Build → verify → fix loops until quality threshold is met.

```
Draft → Verify → Issues? → Yes → Fix → Verify → ...
                          → No → Done
```

**When to use:** Skills that produce complex output where first attempts need refinement.

**Example:** The `verify` skill — walk through tests, find issues, fix, re-verify.

**Template:**
```markdown
### 1. Initial Pass
Produce first version of output.

### 2. Verification
Check output against criteria:
- [Criterion 1]
- [Criterion 2]

### 3. Fix Loop
For each issue found:
1. Diagnose root cause
2. Apply fix
3. Re-verify

Maximum N iterations. If issues persist, escalate.
```

## Hybrid Patterns

Most real skills combine patterns:
- Sequential phases with conditional branching within phases
- Parallel execution followed by iterative refinement
- Sequential setup → parallel work → sequential synthesis → iterative QA
