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

**Scaffolded, not yet populated.** This repository was created 2026-08-19 as
part of the OpenAI-exit fork ([PDR-001](../decisions/PDR-001.md)). No
dataset content, trained checkpoint, or model release exists here yet.
`google/flan-t5-base` (Apache 2.0) is the intended base model, carried
forward unchanged from the predecessor project.

Next real work: design this repository's own taxonomy and category
reference in `docs/datasets/`, then begin dataset generation against
`training/DATASET_SPEC.md` using Gemini.

## Roles

Product owner (the user), engineering lead and corpus steward (Claude),
dataset generator (Gemini) — see `NORTH_STAR.md`'s "Collaboration model"
for what each role owns.

## Claude + Gemini tooling

This project intends tooling-level integration between Claude and Gemini
(not just raw API calls from a script) — an MCP server wrapping the Gemini
API, evaluated and selected once concrete. See a future PDR once that
selection is made.
