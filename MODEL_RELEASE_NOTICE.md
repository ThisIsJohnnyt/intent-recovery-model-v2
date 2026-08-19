# Model Release Notice

**No model has been released from this repository yet.** This file is
scaffolded now so the license posture is decided before the fact, per
[PDR-002](docs/decisions/PDR-002.md), and will be completed with real
release-specific detail (exact base-model revision, asset provenance) when
the first `intent-recovery-model-v2-*` release is actually prepared —
mirroring the predecessor project's `THIRD_PARTY_NOTICES.md` process, not
skipping it.

This file covers released model weights specifically. It is **not** a
license, and nothing in this file is an asserted, legally enforceable
condition. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for what a
released file will actually be made of, and [PDR-002](docs/decisions/PDR-002.md)
for the full reasoning behind this approach.

## Why this isn't a license

Whether trained model weights are copyrightable at all — and separately,
whether fine-tuned weights are a derivative of the base model or of the data
used to train it — is not a settled question. The U.S. Copyright Office's
May 2025 Part III report on AI and copyright discusses this directly:
weights that substantially memorize training data may themselves constitute
infringing copies of *someone else's* copyrighted work, independent of
whether the weights are original, copyrightable subject matter in their own
right. No blanket rule currently resolves either question.

Given that, asserting "these weights are licensed under [X]" would overstate
what this project can actually grant. Instead:

> To the extent ThisIsJohnnyt owns copyright or similar rights in
> project-created release material, those rights are made available under
> the terms below. No claim is made that the numerical model weights
> themselves are copyrightable or exclusively owned by ThisIsJohnnyt.

## Project request (not a license condition)

When a release exists, we will ask — but not represent as a legally
enforceable license condition — that anyone using it:

1. **Acknowledge** ThisIsJohnnyt
   (https://github.com/ThisIsJohnnyt/intent-recovery-model-v2) as the
   creator of this implementation and its annotation/training framework.
2. **Use the weights noncommercially** — consistent with the rest of this
   project's licensing posture (see [PDR-002](docs/decisions/PDR-002.md)).

This is a request about how we'd like the project treated, not a copyright
claim over ideas, methods, or the project name.

## Third-party and provenance disclosure

- Model-weight copyright and derivative-work status varies by jurisdiction
  and remains legally unsettled generally, not specific to this project.
- The intended base model (`google/flan-t5-base`) and other upstream
  components retain their original terms (Apache 2.0) regardless of
  anything stated here — see `THIRD_PARTY_NOTICES.md`.
- This project makes no representation that it owns or can license
  third-party rights that may subsist in upstream components, or in any
  material a model output might reproduce.
- Training data provenance: this repository's dataset is a fresh start with
  no rows carried over from the predecessor project — see
  [PDR-003](docs/decisions/PDR-003.md). Private validation/holdout notes
  (`datasets/real_validation.jsonl`, `datasets/real_holdout.jsonl`) are not
  used as training data and are never published.
- No memorization or output-provenance audit has been performed — there is
  no released checkpoint yet to audit.
