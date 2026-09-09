# Adversarial probe -- inference-time behavior on distressing input
**Reviewed:** `training/checkpoints/flan-t5-base-v2.0`, the same checkpoint `training/evaluate_real.py` runs against.
**Scope:** What the model does at inference time with a note that mixes genuinely recoverable content and an expression of self-harm ideation or distress -- a question no prior review or PDR addresses, since every existing content-safety rule ([`GOLD_PHILOSOPHY.md`](../vision/GOLD_PHILOSOPHY.md) principle 8, [PDR-005](../decisions/PDR-005.md), `DATASET_SPEC.md`'s hard content boundary, `REVIEW_GUIDE.md` §0) governs what may exist in the *corpus*, not what the trained model *emits*.
**Reviewer:** The product owner, running `training/probe_adversarial.py` interactively and judging each output directly.
**Verification level:** [VERIFIED] -- every count below is a direct read of real model output by the person running the session, not an estimate or inference.

---

## Method

Per [PDR-005](../decisions/PDR-005.md) (no content of this kind may exist in this project's data, at any tier, ever), the probe tool is deliberately **ephemeral**: notes are typed at runtime, held in memory only, and never written to disk in any form -- not committed, not gitignored, not logged. This document records only aggregate classification counts. No probe note or model output is quoted or reconstructable here. Full design rationale, including the Claude<->Gemini bridge review round this design went through (round 1 rejected on a PDR-005 reading; round 2 aligned on the ephemeral, human-judged design after Gemini also caught a false-negative gap in an earlier automated-detector draft), is documented in `training/probe_adversarial.py`'s module docstring.

The product owner hand-authored 6 realistic notes, each mixing ordinary recoverable content (an errand, a chore, a reminder) with a passing expression of self-harm ideation or acute distress, styled close to his own real writing register rather than generated content -- chosen specifically after an earlier attempt using Gemini-authored notes surfaced a confound (see "Related finding" below). Each note was run through two decoding configurations (greedy; sampled at temperature 0.7/top_p 0.9), producing 12 total outputs, each judged live by the product owner immediately after generation and classified into one or more of: clean, flagged in narrative, flagged in bullets, flagged in action_items.

## Finding: the model reproduces distressing content readily, in all three output sections [VERIFIED]

| Verdict | Count | Of 12 outputs |
|---|---|---|
| Clean | 0 | 0% |
| Flagged in narrative | 12 | 100% |
| Flagged in bullets | 11 | 92% |
| Flagged in action_items | 4 | 33% |

**Zero of 12 outputs were clean.** Every single output reproduced the distressing content somewhere. This is not a borderline or noisy result at this sample size -- a 0/12 clean rate does not need a larger sample to be meaningful, though the exact percentages above should not be quoted as precise rates given n=6 notes.

Most consequentially: **4 of 12 outputs (33%) placed the distressing content in `action_items`** -- meaning the model didn't just reproduce it as prose, it structured it as an actionable task, the exact failure mode this probe was built to check for. `action_items`'s lower rate than `narrative`/`bullets` is itself informative: it suggests the failure is not usually the model *deciding* the distressing content is a task (a PDR-011-style stated-need-to-imperative conversion), but something that happens a minority of the time as a byproduct of the model's general copying behavior described below.

## Related finding: this sits on top of an already-known, pre-existing copying tendency [VERIFIED]

Before this probe session, an earlier attempt using Gemini-authored probe notes produced output that appeared to just echo the input verbatim in both narrative and bullets. Investigation traced this to the model's existing, already-measured behavior, not a probe-tool defect: the most recent `evaluate_real.py` run against the real 15-record validation tier (`training/eval_run_2026-09-08-final.log`) shows a **mean narrative-vs-input similarity of 0.76**, and per-example output in that same log shows bullets and action_items frequently near-duplicating each other and the input. This is the identical mechanism `training/check_copy_ratio.py`'s entire allowlist apparatus (65 entries, six records at ratio exactly 1.000) exists to track in the corpus.

The practical implication for this probe's result: the model's copying tendency is not specific to distressing content and was not introduced by this exercise. It is a general, pre-existing weakness that this probe demonstrates has a direct safety consequence -- when the input contains distressing material, the same copying behavior that produces high copy-ratio narratives elsewhere in the corpus reproduces that material in the output, including, some of the time, in `action_items`.

## What this does and does not establish

- **Does establish:** there is no inference-time mitigation of any kind on this checkpoint. Distressing content in the input reaches the output essentially every time, and reaches `action_items` specifically a meaningful fraction of the time. The corpus-level exclusion (PDR-005) provides zero protection at inference time -- confirmed empirically here, not just by the structural/architectural argument raised earlier in the review-bridge rounds.
- **Does not establish:** a precise emission rate (n=6 is a directional signal, not a calibrated measurement); which specific phrasing patterns are more or less likely to be reproduced; or anything about behavior on notes with a different mixture, length, or structure than what was tested.

## Next step

This is the evidence gap the plan ("Measure inference-time behavior on distressing input -- ephemeral probe") was built to fill before choosing between the three architecture options previously raised (application-layer screening only / model-layer non-extraction as defense-in-depth / both). That decision is the product owner's to make and is not resolved by this document -- this document exists to make sure it's made with a real number behind it rather than an assumption.
