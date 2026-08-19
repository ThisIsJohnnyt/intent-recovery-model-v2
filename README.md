# Intent Recovery Model v2.0

The Intent Recovery Model is an open language-model training and
evaluation project designed to help people recover what mattered from
fragmented, rushed, incomplete, or interleaved notes — with as little
cognitive and emotional burden as possible.

This repository is the successor to
[`intent-recovery-model`](https://github.com/ThisIsJohnnyt/intent-recovery-model),
started fresh on 2026-08-19 — see "Ethical Development & Tooling" below for
why, and [PDR-001](docs/decisions/PDR-001.md) for the full decision record.
It does not contain the application — see
[**Thought Organizer**](https://github.com/ThisIsJohnnyt/thought-organizer-app),
the reference application powered by a versioned release of this model.

## Ethical Development & Tooling

This project does not use OpenAI products (ChatGPT, Codex, or the OpenAI
API) as tools or collaborators, effective 2026-08-19. This is a deliberate,
permanent policy set by the project's owner, based on his own research into
how AI companies handle the safety and downstream use of the content their
products produce — including public reporting and litigation concerning
OpenAI specifically — weighed against his personal values. This repository
states the project's resulting policy; it does not itself make legal or
factual findings about OpenAI beyond that.

Development uses two AI collaborators going forward:

- **[Claude](https://www.anthropic.com/claude) (Anthropic)** — engineering
  lead and corpus steward: repository, training pipeline, dataset
  specification and review, documentation.
- **[Gemini](https://deepmind.google/technologies/gemini/) (Google)** —
  dataset generation, against the spec Claude and the product owner define.

This continues the project's existing governance model — surface
disagreement rather than silently resolve it, product owner has final
say — applied to which AI vendors this project trusts as collaborators, not
just which model architectures it trains. See
[`docs/vision/AI_COLLABORATION.md`](docs/vision/AI_COLLABORATION.md).

**This project's predecessor** — `intent-recovery-model`, built in part with
ChatGPT and Codex as collaborators through 2026-08-19 — remains publicly
readable at
[github.com/ThisIsJohnnyt/intent-recovery-model](https://github.com/ThisIsJohnnyt/intent-recovery-model),
unaltered and clearly marked as superseded. That history isn't hidden,
deleted, or rewritten; this project believes in an honest record over a
tidied-up one. See [PDR-001](docs/decisions/PDR-001.md) for exactly what did
and didn't carry forward from it into this repository (short answer:
nothing — this is a genuine fresh start, not a rebrand).

## The task: Intent Recovery

Common NLP tasks — translation, summarization, classification — take
well-formed text as input. This one doesn't.

- **Input**: fragmented human cognition — scattered, interrupted,
  incomplete notes written under real-world conditions (time pressure,
  distraction, fatigue, excitement).
- **Output**: recovered intent — what the person was actually trying to
  capture, structured and readable, without inventing what wasn't there.

Every dataset, evaluation, and architecture decision is checked against
one question: **does this make it easier for the person to recover what
mattered, without forcing them to relive more than they need to?** See
[`docs/vision/NORTH_STAR.md`](docs/vision/NORTH_STAR.md) for the full
mission and [`docs/vision/GOLD_PHILOSOPHY.md`](docs/vision/GOLD_PHILOSOPHY.md)
for the stable principles behind every dataset release.

Cognitive/emotional *state* is fair game in this project's data and
documentation (rushed, distracted, excited, overwhelmed); a diagnosis
label is not.

## Where things live

| Area | Location |
|---|---|
| Mission, stable principles, AI collaboration protocol | [`docs/vision/`](docs/vision/) |
| Dataset generation spec, category reference, review checklist, schemas | [`docs/datasets/`](docs/datasets/), [`training/DATASET_SPEC.md`](training/DATASET_SPEC.md) |
| The dataset itself (currently empty — see Current state) | [`datasets/`](datasets/) |
| Fine-tuning pipeline (prepare → train → export → release) | [`training/`](training/) |
| Formal decision records | [`docs/decisions/`](docs/decisions/) |
| Model releases | [Releases](https://github.com/ThisIsJohnnyt/intent-recovery-model-v2/releases) (none yet) |

## Current state

**Scaffolded, not yet populated.** This repository was created 2026-08-19.
No dataset content, trained checkpoint, or model release exists here yet —
see [PROJECT_OVERVIEW.md](docs/vision/PROJECT_OVERVIEW.md) for what's next.
`google/flan-t5-base` (Apache 2.0) is the intended base model, carried
forward unchanged from the predecessor project — it was never an OpenAI
dependency.

## Collaboration model

Built by a product owner, an engineering-lead AI (Claude), and a
dataset-generator AI (Gemini) working from a documented, versioned process —
see [`docs/vision/AI_COLLABORATION.md`](docs/vision/AI_COLLABORATION.md).

## Issues

Open an issue here for dataset problems, evaluation problems, training
problems, export problems, model behavior, or inference contract changes.
For UI, storage, or application-level issues, open one in
[thought-organizer-app](https://github.com/ThisIsJohnnyt/thought-organizer-app) instead.

## License

This repository uses multiple, artifact-appropriate license classes rather
than one blanket license — see [LICENSE](LICENSE) for the full routing:
CC BY-NC-SA 4.0 for the dataset and documentation, PolyForm Noncommercial
1.0.0 for code, and a plain acknowledgment/noncommercial-use *request* (not
an asserted license) for any released model weights — see
[`MODEL_RELEASE_NOTICE.md`](MODEL_RELEASE_NOTICE.md) and
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Decision record:
[PDR-002](docs/decisions/PDR-002.md).
