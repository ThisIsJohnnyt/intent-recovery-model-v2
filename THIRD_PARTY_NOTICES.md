# Third-Party Notices

**No model has been trained or released from this repository yet.** This
file records the intended upstream dependency now; the provenance/hash
verification table (which files match the pinned upstream revision
byte-for-byte, which are reserialized) will be completed against real
release assets when the first `intent-recovery-model-v2-*` release is
prepared — see the predecessor project's `THIRD_PARTY_NOTICES.md` for the
methodology this will follow (download real release assets, hash them
against the pinned upstream revision, disclose exactly what matches and
what doesn't, rather than assuming compliance).

## Upstream component: `google/flan-t5-base`

- **Source**: https://huggingface.co/google/flan-t5-base
- **License**: Apache License, Version 2.0.
- **Full license text**: [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)
  (vendored verbatim from https://www.apache.org/licenses/LICENSE-2.0.txt).

### Revision pinning

Learning from the predecessor project's disclosed gap (its first release
never pinned an explicit Hugging Face revision, making that release's exact
base-model bytes unreproducible after the fact), this project's training
code will pin `google/flan-t5-base` to an explicit revision from its first
training run, not add pinning retroactively after an unpinned release.

## What this will mean practically

- This project does not claim ownership of `google/flan-t5-base`'s
  tokenizer, configuration, or architecture. Those remain Google's, under
  Apache 2.0.
- This project's actual contribution — fine-tuning, the training data (see
  [PDR-003](docs/decisions/PDR-003.md)), and any export/quantization work —
  is what this project's own licensing terms apply to, not the upstream
  components wholesale.
- See [`MODEL_RELEASE_NOTICE.md`](MODEL_RELEASE_NOTICE.md) for why released
  model *weights* specifically will be handled as a request rather than an
  asserted license, and [PDR-002](docs/decisions/PDR-002.md) for the full
  reasoning.
