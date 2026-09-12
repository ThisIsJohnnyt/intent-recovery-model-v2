# This experiment is retired

**Retired 2026-09-12 by [PDR-015](../../../docs/decisions/PDR-015.md).**
Left in place as historical record, per this project's convention of not
deleting experiment artifacts — but nothing in this repository may
reference it as an open follow-up going forward. `docs/decisions/PDR-012.md`'s
"Explicitly out of scope" section, which previously called this "still a
separate, experimental, undecided feature," has been updated to reflect
this.

## Why

This experiment tested a 4th "held" output field: content with real affect
but no underlying fact/decision, extracted out of `narrative` and stored
separately. Never merged into `training/prepare_data.py`'s production
`serialize_target`/`deserialize_target` or into `datasets/synthetic.jsonl`
— it stayed exactly what its own original design said it would be if it
didn't pan out: an isolated, throwaway fork, deleted from consideration
rather than promoted.

The reason isn't the mixed 5/7 result reported in `docs/decisions/PDR-012.md`.
It's that `held`'s entire mechanism — extracting a fragment out of
`narrative` based on emotional intensity/affect alone, independent of what
the content actually is — was built on the wrong axis. This project's
actual principle (see `docs/vision/GOLD_PHILOSOPHY.md`'s "Human-Centered
Intent Recovery," as clarified by PDR-015): emotional content, of any
valence or intensity, is legitimate context that belongs in `narrative`
exactly as the writer expressed it. The only legitimate grounds for
excluding content from an output field is content-type — specifically the
self-harm/violence boundary from PDR-001/PDR-005 — never how much feeling
is behind it. `held` would have routed a stressed, furious, or heavily
distressed but completely benign note away from its own narrative for no
reason other than its intensity — exactly what this project does not want.

See PDR-015 for the full reasoning.
