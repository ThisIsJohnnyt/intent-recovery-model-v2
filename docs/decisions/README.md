# Project Decision Records (PDRs)

A PDR captures a significant project decision at the time it's made: what
was decided, why, and who approved it — so nobody has to reconstruct the
reasoning from chat history months later.

**This repo's PDR numbering starts fresh at PDR-001, unrelated to
`intent-recovery-model`'s (this project's predecessor) PDR series**, which
ran through PDR-008 and stays exactly as-is in that repository's own
history.

## When to write one

Write a PDR for decisions with lasting consequences: architecture choices,
dataset/process rules, format changes, anything that would be genuinely
confusing to reverse-engineer later. Not every choice needs one —
day-to-day implementation details belong in code comments or a roadmap
document, not here.

## Format

Each PDR is a short file: `PDR-NNN.md`, three-digit zero-padded, sequential.

```markdown
# PDR-NNN: <short title>

**Date**: YYYY-MM-DD
**Status**: Accepted | Superseded by PDR-XXX

## Decision
<what was decided, one or two sentences>

## Reasoning
<why>

## Approved by
- Product Owner
- Engineering Lead
- Dataset Curator
```

## Index

- [PDR-001](PDR-001.md) — Discontinue OpenAI as a project collaborator; fork to a standalone v2.0 repository
- [PDR-002](PDR-002.md) — License classes for v2.0 (re-derived, not inherited)
- [PDR-003](PDR-003.md) — Corpus fresh start: zero rows carry over from the predecessor's dataset
- [PDR-004](PDR-004.md) — Claude + Gemini tooling integration: MCP server selection and guardrail redesign
