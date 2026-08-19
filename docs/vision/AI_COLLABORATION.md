# AI Collaboration Protocol

An entry point for how this project is actually built, not a second copy of
it. Each topic below is defined once, in one canonical place — this doc
summarizes and links rather than restates, so it can't drift out of sync
with the source.

## Roles

See [`NORTH_STAR.md`](NORTH_STAR.md)'s "Collaboration model" for the full
definition. Summary: product owner (the user, owns the problem/vision and
has final decision authority), Claude (engineering lead and corpus
steward — repo, pipeline, dataset spec, review, commits), Gemini (dataset
generator — produces synthetic examples against the spec).

**On the predecessor project's history**: `intent-recovery-model` (this
project's predecessor) used ChatGPT as its dataset curator and Codex
alongside Claude Code for parts of its tooling. This project no longer uses
either — see [PDR-001](../decisions/PDR-001.md) for why. That history isn't
restated here beyond this note; the predecessor repository's own docs
describe it in full.

## Stable principles

See [`GOLD_PHILOSOPHY.md`](GOLD_PHILOSOPHY.md) — the constitution that
doesn't change release to release (Evidence First, No Magic Examples, One
Lesson Per Example, Progressive Difficulty, Boundary Evidence, Preserve
Uncertainty, Human-Centered Intent Recovery).

## Review workflow

See [`docs/datasets/REVIEW_GUIDE.md`](../datasets/REVIEW_GUIDE.md) once
populated — checklist, release bundle contents, and who writes each piece.

## Decision ownership

See [`docs/decisions/`](../decisions/) — Project Decision Records capture
decisions with lasting consequences.

## Dataset lifecycle

See `REVIEW_GUIDE.md`'s release bundle table (design notes → review report
→ lessons learned) and `CATEGORY_REFERENCE.md`'s category lifecycle section,
once those are populated with this repository's own taxonomy.

## Conflict resolution

The procedure behind [`NORTH_STAR.md`](NORTH_STAR.md)'s "Repository
Authority" and "Preserve Decision History" values:

1. **Check before acting.** Claude checks a Gemini-generated proposal
   against the actual current repo before applying it — never overwrites or
   contradicts existing content on the assumption a proposal is already
   correct. This is what catches proposals made without full repo
   visibility (schema mismatches, duplicate files, terminology drift, etc.)
   before they land.
2. **Surface, don't silently resolve.** A found conflict gets presented to
   the product owner with a concrete recommendation — Claude doesn't
   silently pick a side, and doesn't silently reject a proposal either.
3. **Product owner has final decision authority** on any dataset-content or
   process question. Claude and Gemini can both recommend; neither
   unilaterally decides.
4. **Fix the gap, not just the instance.** When a conflict reveals a
   recurring pattern (e.g. a principle restated in multiple places, a
   missing convention), the preferred fix consolidates or cross-links so
   the same conflict doesn't resurface in the next release.
5. **Low-judgment fixes don't need a round trip.** A broken cross-reference
   or an obviously stale link can be corrected directly. Anything that
   changes meaning, scope, or an established convention gets flagged to the
   product owner first, not applied unilaterally.

## Financial guardrails (Gemini API usage)

Gemini API billing is real and per-token. Every real-money call needs the
product owner's own direct statement — never inferred from a prior
approval, never assumed to carry over between sessions. See a future PDR
once the concrete Claude+Gemini tooling integration (MCP-based, see
[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)) is built, for the specific
guardrail mechanism in place.
