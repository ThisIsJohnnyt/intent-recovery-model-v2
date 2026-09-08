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
generator — produces synthetic examples against the spec; since 2026-09-07
also reviews Claude's engineering/pipeline proposals and model-diagnostics
discussion via a standing session, and independently re-reviews sampled
corpus content as its own blind subagent during periodic adversarial
re-review — see [PDR-006](../decisions/PDR-006.md)).

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
Uncertainty, Human-Centered Intent Recovery, No Harmful or Illegal
Content).

## Review workflow

See [`docs/datasets/REVIEW_GUIDE.md`](../datasets/REVIEW_GUIDE.md) —
checklist, release bundle contents, periodic adversarial re-review
process, and who writes each piece.

## Decision ownership

See [`docs/decisions/`](../decisions/) — Project Decision Records capture
decisions with lasting consequences.

## Dataset lifecycle

See `REVIEW_GUIDE.md`'s release bundle table (design notes → review report
→ lessons learned) and `CATEGORY_REFERENCE.md`'s category lifecycle section.

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

Gemini API billing is real and per-token. Every real-money generation or
adversarial-re-review call needs the product owner's own direct statement
in the moment — never inferred from a prior approval, never assumed to
carry over between sessions or between batches. See
[PDR-004](../decisions/PDR-004.md) for the MCP-based tooling integration
this runs through, and [`training/COST_LEDGER.md`](../../training/COST_LEDGER.md)
for the running record of every authorized call.

The review bridge's engineering-proposal lane (Gemini reviewing Claude's
own pipeline/methodology proposals, see [PDR-006](../decisions/PDR-006.md)'s
2026-09-07 amendment) is a separate lane with its own standing
authorization — it isn't a real-money generation call, so it doesn't need
a fresh per-instance statement the way a corpus batch or adversarial
re-review does.

**A second real-money API surface exists as of 2026-09-07**:
`training/third_party_review.py`, an occasional, manually-invoked
independent review via a raw Claude API call (see
[PDR-008](../decisions/PDR-008.md)). Same rule applies — the product
owner's own explicit in-the-moment authorization before every real,
billed call, never inferred or carried over between runs. The tool always
runs a free `count_tokens` check first and prints an exact cost estimate
before any spend is possible; no default path spends money without that
number being shown first.
