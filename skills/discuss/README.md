# discuss

Structured requirements discussion — identifies gray areas, gathers implementation decisions, and documents what's locked vs what's flexible. Use before planning complex work.

## Usage

```
/discuss
/discuss the new authentication system
```

## What It Does

1. Establishes scope boundaries (in/out of scope)
2. Identifies "gray areas" — decisions that affect the user experience
3. Categorizes by domain (Visual, Interaction, Data, Integration, Behavior)
4. Walks through each selected area with tradeoffs
5. Documents decisions as locked / discretionary / deferred / open

## When to Use

- Before starting a complex feature
- When requirements are vague or ambiguous
- When multiple valid approaches exist
- To align on design decisions before coding

## Output

Updates STATE.md with a structured decision log that constrains subsequent planning.
