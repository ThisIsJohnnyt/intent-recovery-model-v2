# Adversarial probe -- inference-time behavior on distressing input, Qwen3.5-4B checkpoint
**Reviewed:** `training/checkpoints/qwen3.5-4b-v2.0` -- the post-PDR-012 Qwen3.5-4B QLoRA checkpoint (early-stopped at epoch 4, best-eval-loss checkpoint from epoch 2, `bf16`/grad-accum training run, 2026-09-10). First adversarial-probe session against this base model; supersedes nothing from the prior session below, which ran against the retired `flan-t5-base-v2.0` checkpoint.
**Scope:** Same open question the 2026-09-09 session was built to answer, re-run against the new base model: what the model does at inference time with a note that mixes genuinely recoverable content and an expression of self-harm ideation or distress. Still a question no corpus-level rule addresses -- see that session's doc for why.
**Reviewer:** The product owner, running `training/probe_adversarial.py` interactively and judging each output directly.
**Verification level:** [VERIFIED] for the tally and the raw behavioral pattern (direct read of real model output by the person running the session). [HYPOTHESIS] for the interpretation of *why* -- see that section for what would move it to [VERIFIED] or refute it.

---

## Method

Same ephemeral, human-judged design as the prior session -- see `training/probe_adversarial.py`'s module docstring and the 2026-09-09 doc's Method section for the full design rationale (PDR-005, the rejected gitignored-eval-file design, the rejected automated-detector design). This document records only aggregate classification counts; no probe note or model output is quoted or reconstructable here.

The product owner hand-authored 5 notes, each mixing ordinary recoverable content with a passing expression of self-harm ideation or acute distress, in the same style as the prior session's notes, followed by a 6th note (see Finding 3) testing a specific follow-up question the first 5 raised. Each note was run through two decoding configurations (greedy; sampled at temperature 0.7/top_p 0.9), producing 12 total outputs across the full session, each judged live immediately after generation.

## Finding 1: a much lower action_items rate than the retired checkpoint [VERIFIED]

Full-session tally, all 6 notes / 12 outputs (5 original notes plus the Finding 3 follow-up note):

| Verdict | Count | Of 12 outputs | Prior session (flan-t5, of 12) |
|---|---|---|---|
| Clean | 0 | 0% | 0% |
| Flagged in narrative | 12 | 100% | 100% |
| Flagged in bullets | 11\* | 92%\* | 92% |
| Flagged in action_items | 0 | 0% | 33% |

\*Corrected from the session's raw verdict entries: two outputs from the original 5 notes were verbally confirmed by the product owner immediately after the session to have also carried the flagged content in bullets, but were entered as narrative-only at the time (originally 7, corrected to 9 for the first 5 notes; plus 2 more from the Finding 3 follow-up note, both flagged in bullets). Recorded here as 11 to keep this document consistent with what was actually observed, not with the raw keystroke tally.

**Zero of 12 outputs placed distressing content in `action_items`**, against 4 of 12 (33%) on the retired checkpoint. n=12 in both sessions is not large enough to treat these as calibrated rates -- but a 33%-to-0% shift on the exact failure mode this probe exists to catch, on a matched probe design (same output size, same interactive method), is a meaningful directional result worth recording as such, not a precise measurement.

## Finding 2: bullets consistently received non-graphic language; narrative did not consistently transform graphic language [VERIFIED, corrected]

Originally written up (and stated to the product owner) as "graphic language is consistently paraphrased before reaching narrative/bullets." That overstated what was actually observed, caught during a later conversation revisiting one of the original probes in more detail -- corrected here rather than left standing.

What was actually observed, across the flagged outputs: **bullets** consistently carried non-graphic, state-naming language (distress, ideation) rather than graphic or method-specific language, in every output where bullets was flagged. **Narrative's behavior was not consistent** -- at least one flagged output retained graphic, method-specific language from the input verbatim in narrative, while the same output's bullets received the non-graphic form. So the transformation behavior documented here is real, but it is a bullets-specific pattern in what was observed, not a narrative-and-bullets pattern. Whether narrative transforms graphic language, preserves it, or does either unpredictably is genuinely unresolved by this session -- the sample includes at least one case of each within flagged outputs, not enough to characterize a rate or a rule.

This is still a distinct, new behavior from the prior session, where the retired checkpoint's dominant failure mode was near-verbatim reproduction of the input into *both* narrative and bullets (consistent with that checkpoint's separately-measured 0.76 mean narrative-vs-input similarity) -- bullets, at least, is doing something the prior checkpoint never did. Narrative's status relative to the prior checkpoint is less clear now than this document originally claimed.

## Interpretation: likely inherited from the base model, not taught by this project's corpus [HYPOTHESIS -- not verified]

The natural first read is that this reflects `GOLD_PHILOSOPHY.md`'s "Human-Centered Intent Recovery" principle ("cognitive/emotional state is fair game... the task is recovering what a person meant to capture, not diagnosing why") -- i.e., that the corpus taught the model to keep the state, drop the method.

That read does not survive a direct check of `DATASET_SPEC.md`'s hard content boundary: *"No example -- generated or hand-written -- may depict, instruct, or normalize self-harm... not a category, not a difficulty signal: content that must never exist in this project's data at all."* This is a complete exclusion, not "graphic banned, state-naming language permitted" -- the training corpus contains **zero** examples of self-harm content in any form, softened or otherwise. Nothing in this project's fine-tuning data could have taught the paraphrase-not-suppress behavior observed above, because the training signal for this category doesn't exist.

The more likely explanation: this behavior is inherited from Qwen3.5-4B's own base pretraining/safety alignment, not earned by this project's corpus curation or fine-tuning. Practical implication if true: the `action_items` protection observed here is not something this team engineered, can tune, or can guarantee survives future training changes (a different base model, more fine-tuning epochs, a different LoRA configuration) -- it's riding on a foundation this project doesn't control. That argues for treating this as encouraging evidence, not a settled protection, in whatever comes next on the model-layer-mitigation question the 2026-09-09 doc left open.

**Not yet tested, would help confirm or refute this:** whether the retired flan-t5-base-v2.0 checkpoint ever produced *any* paraphrase-not-copy behavior on similar notes. The 2026-09-09 session's dominant finding was nearly the opposite (near-verbatim reproduction), which is suggestive but wasn't specifically coded for this question at the time.

## Finding 3: already-non-graphic language is preserved in narrative/bullets, still withheld from action_items [VERIFIED]

Same-session follow-up, run immediately after the above: a sixth note, where the self-harm-ideation content was phrased by the product owner as non-graphic, state-naming language from the start (not graphic/method-specific language requiring transformation), embedded in the same kind of mixed benign-content note as the other five. Judged across both decoding configurations.

Result: the state-naming language was reproduced essentially unchanged in both narrative and bullets, in both decoding outputs -- and reached `action_items` in neither.

This resolves part of the open question Finding 2 raised: the model is not avoiding the *topic* of self-harm ideation broadly, and does not appear to be suppressing non-graphic state-naming language on sight -- that much holds for both narrative and bullets. What's consistent across all 12 outputs judged this session, and the one part of this picture with no observed exception: `action_items` never carries this content, in any phrasing tested (graphic, transformed, or already-non-graphic). Bullets appears to hold a similar bar specifically against *graphic* language (see Finding 2's correction), though narrative's bar -- if it has a consistent one at all -- is not established by this session.

## What this does and does not establish

- **Does establish:** on this small sample, the new checkpoint's inference-time behavior on distressing input differs substantially from the retired checkpoint's -- content reaches `action_items` far less (0/12 vs 4/12) across every phrasing tested (graphic, transformed-to-non-graphic, and already-non-graphic), and bullets specifically was never observed carrying graphic/method-specific language verbatim.
- **Does not establish:** a calibrated emission or transformation rate (n=6 notes, 12 outputs -- the same n as the prior session, still small); that narrative reliably transforms or reliably preserves graphic language (both were observed; see Finding 2's correction); that this behavior is reliable under adversarial pressure specifically targeting it (e.g., a note constructed to make the self-harm content read as syntactically imperative, closer to how `action_items` content is normally phrased); or the mechanism -- see the Interpretation section's [HYPOTHESIS] tag, still unresolved.

## Next step

The flan-t5 comparison test named in the Interpretation section would help settle whether this behavior is inherited from the base model or something else, if it's ever worth the product owner's time to run. Also untested: a note phrasing the self-harm content itself in imperative/task-like form (closer to how legitimate `action_items` are normally phrased) -- Finding 3's result leaves open whether the `action_items` protection would hold under that specific pressure, or whether it's specifically avoiding phrasing self-harm content as a task rather than never placing it in that section regardless of the input's own grammatical mood. Separately, per Finding 2's correction: narrative's handling of graphic language is currently uncharacterized (at least one instance each of preserved-verbatim and transformed, within a sample too small to say which is more typical) -- worth specifically tracking on future probes rather than assuming either behavior.

The architecture decision this evidence feeds (application-layer screening only / model-layer non-extraction as defense-in-depth / both) remains the product owner's to make and is not resolved by this document.
