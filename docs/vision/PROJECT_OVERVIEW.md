# Project Overview

This repository (`intent-recovery-model-v2`) is the successor to
`intent-recovery-model`, pursuing the same **Intent Recovery** task — see
[NORTH_STAR.md](NORTH_STAR.md) for the mission and task definition — under a
new collaboration model (Claude + Gemini, not Claude + ChatGPT/Codex; see
[PDR-001](../decisions/PDR-001.md)) and a fresh corpus (see
[PDR-003](../decisions/PDR-003.md)).

The reference application,
[**Thought Organizer**](https://github.com/ThisIsJohnnyt/thought-organizer-app)
(React + TypeScript + Vite, in-browser inference via transformers.js),
remains a separate, independently maintained repository, unaffected by this
fork.

## Where things live

| Area | Location |
|---|---|
| Gold Curriculum Series' stable principles (constitution — link, don't restate) | [`GOLD_PHILOSOPHY.md`](GOLD_PHILOSOPHY.md) |
| How the AI collaborators actually work together (roles, review, conflict resolution) | [`AI_COLLABORATION.md`](AI_COLLABORATION.md) |
| Fine-tuning pipeline (data prep → train → export → release) | [`../../training/`](../../training/) |
| Dataset generation spec (schema, rules, Gemini prompt) | [`../../training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md) |
| The actual dataset (gold, synthetic, real validation/holdout) | [`../../datasets/`](../../datasets/) |
| Category reference, taxonomy, batch review rubric, schemas | [`../datasets/`](../datasets/) *(this `docs/datasets/`, not the data itself)* |
| Formal decision records (PDRs) | [`../decisions/`](../decisions/) |

## Current status

**Actively in development.** This repository was created 2026-08-19 as
part of the OpenAI-exit fork ([PDR-001](../decisions/PDR-001.md)). As of
2026-09-07: a synthetic corpus spans all 15 taxonomy categories (see
[`../datasets/CATEGORY_REFERENCE.md`](../datasets/CATEGORY_REFERENCE.md)
for current, exact counts — this grows by batch, tracked there rather than
restated here), a real hand-written validation/holdout tier exists per
`training/DATASET_SPEC.md` (never generative-model-touched, by design),
and two full training runs have completed against `google/flan-t5-base`
with results evaluated against the real tier — see
[`../../training/COST_LEDGER.md`](../../training/COST_LEDGER.md) for the
full batch-by-batch and review history. No versioned model release exists
yet. `google/flan-t5-base` (Apache 2.0) remains the base model, carried
forward unchanged from the predecessor project.

## Roles

Product owner (the user), engineering lead and corpus steward (Claude),
dataset generator (Gemini) — see `NORTH_STAR.md`'s "Collaboration model"
for what each role owns. Since 2026-09-07, Gemini also reviews Claude's
engineering/pipeline proposals and model-diagnostics discussion via a
standing session, and independently re-reviews sampled corpus content as
its own blind subagent during periodic adversarial re-review — see
[PDR-006](../decisions/PDR-006.md)'s amendments.

## Claude + Gemini tooling

Tooling-level integration between Claude and Gemini (not just raw API
calls from a script) is done: an MCP server wraps the Gemini API for
dataset generation, evaluated and selected per
[PDR-004](../decisions/PDR-004.md). The most recent extension of it is
the review bridge (`review_bridge/`, [PDR-006](../decisions/PDR-006.md)'s
2026-09-07 amendment) — a file-based channel to a standing Antigravity
session for engineering/pipeline proposal review and model-diagnostics
discussion, separate from the batch-generation API and gated by its own
standing authorization rather than per-call.
