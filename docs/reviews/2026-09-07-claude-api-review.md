# External code review -- training core (Claude API / Fable 5.1)
**Reviewed:** A single bundled text dump containing: `training/*.py` (backfill_categories, check_copy_ratio, check_duplicates, convert_real_notes, evaluate_real, prepare_data, split_real_holdout, telemetry, third_party_review, train), `training/requirements.txt`, `training/COST_LEDGER.md`, `datasets/synthetic.jsonl` (~532 records), `datasets/real_validation.jsonl` (15 records), `docs/datasets/*.md` (CATEGORY_REFERENCE, DESIGN_NOTES_TEMPLATE, REVIEW_GUIDE, TAXONOMY), `docs/decisions/PDR-001..008` + README, `docs/vision/*.md`. Not provided, though referenced as authoritative throughout: `training/DATASET_SPEC.md`, `docs/datasets/training_data.schema.json`, `training/tests/*`, `training/SETUP.md`, `training/FART_TELEMETRY_INTEGRATION.md`, `docs/reviews/*`.
**Scope:** (1) Correctness/consistency review of every `training/*.py` file and `requirements.txt`, cross-checked against the rules stated in `docs/datasets/*.md`; (2) sampled content review of `synthetic.jsonl` against `TAXONOMY.md` definitions and `REVIEW_GUIDE.md` items 0–6b, plus a register/shape comparison of the synthetic corpus against the 15 hand-written real notes; (3) internal-consistency read of `COST_LEDGER.md` and the PDRs against each other and against the code. I could not execute code; every numeric claim below that depends on running a script is marked [ESTIMATED] or [UNVERIFIED].
**Reviewer:** Claude Fable 5.1, fresh API call, zero prior context on this project.
**Verification level:** every finding below labeled [VERIFIED] (you directly confirmed it against the provided files), [ESTIMATED] (arithmetic/inference from what's given, state the assumption), or [UNVERIFIED] (you could not check it from what you were given -- state what would be needed to check it).

---

## Critical / systemic

### C1. `contradictory_statement` teaches three incompatible `action_items` conventions -- the "still open" question from the 4th re-review is live in the corpus [VERIFIED]

REVIEW_GUIDE §4 and CATEGORY_REFERENCE (4th and 6th re-reviews) record as *undecided* what `action_items` should do when a note commits to two incompatible things. The corpus has not waited for the decision; it currently teaches all three of the options the reviewer declined to invent:

- **Pick the first stance:** `"gonna plant a massive vegetable plot this spring ... i think im just gonna pave over the whole dirt patch"` → `action_items: ["Plant a spring vegetable plot"]`. The note *ends* on paving; the action item asserts planting.
- **List both sides flat:** `"prep the guest room for inlaws ... i want to cancel the trip"` → `["Prepare the guest room for the in-laws", "Cancel the in-laws' trip"]`; `"starting strict no spend month ... putting that 800 dollar espresso machine in my cart"` → `["Build an emergency fund", "Purchase the $800 espresso machine"]`. These are exactly the "two flatly contradictory imperatives" shape #122 was rejected for.
- **Empty:** `"finally setting up the 40 gal planted tank ... cichlids would be so much easier"` → `[]`; `"greg wants to do dinner friday at 7 ... maybe dinner is fine"` → `[]`; `"paint it white or maybe black I can't decide"` → `[]`.

A model trained on this cannot learn a rule, because there isn't one. This is the same category the real-tier eval failure (invented action items on hedged reflection) sits closest to.

**Recommended action:** Put the decision to the product owner now, then apply one convention corpus-wide. My recommendation, consistent with the project's own "hedged intention belongs in `action_items` with its hedge preserved" rule: when the note's *ending* is unresolved, `action_items` carries the unresolved state as a single hedged item or nothing -- never the first stance alone, never both as flat commands. Add a `grep`-able check in the §6b suite: any `contradictory_statement` record whose `action_items` contains two items that both appear as plain imperatives in the input is flagged for read.

### C2. `self_correction` teaches two incompatible narrative conventions, and the project's own docs contradict each other on which is right [VERIFIED]

CATEGORY_REFERENCE's 5th re-review: *"self_correction is not one of the three categories requiring verbatim preservation, so narrating the pivot is allowed."* Its 12th re-review: self_correction fixes *"all of which land directly on the final decision with zero mention of the retracted option"* and #449 was fixed as the outlier. The corpus is split roughly down the middle:

- Narrate the pivot: `"need to buy cat food today. wait, no ..."` → *"I initially thought I needed to buy cat food today, but then remembered..."*; `"Pack the heavy coats for Chicago. No wait ..."` → *"Initially, I thought about packing the heavy coats, but the weather app says..."* (and `action_items` even includes `"Leave the green sweater"`, a retraction); `"buy the witcher 3 dlc ... never mind"` → *"I initially thought I needed to buy The Witcher 3 DLC ... but then I quickly realized and corrected myself"*; `"let's paint the living room sage green. wait ..."` → *"I initially thought about painting the living room sage green, but realized..."*.
- Drop the retraction entirely: `"order the size 8 boots no make it size 9"` → *"I need to order the boots in a size 9 instead of an 8, because they run small"* (still mentions 8, but as correction); `"meet Chloe at 5 no wait she said 5:30"` → *"I need to meet Chloe at 5:30, not 5."*; `"flight leaves at 6pm no 8pm"` → *"My flight leaves at 8pm"*; `"Email Greg ... send it to Marcus instead"` → *"I need to email Marcus..."*; `"I need to email the vendor ... call the vendor tomorrow"` → *"I need to call the vendor tomorrow"*.

TAXONOMY's definition ("the retracted content is dropped from the output, not preserved alongside the correction") supports the second convention, which means roughly half the `self_correction` records violate their own category definition.

**Recommended action:** Pick one (TAXONOMY's wording says drop). Sweep every `self_correction` record and rewrite narratives that open with "I initially / I originally / I was going to ... but" unless the record is deliberately kept as a hard case. Amend the 5th re-review's note in CATEGORY_REFERENCE so it no longer asserts the opposite of the 12th.

### C3. The synthetic corpus systematically diverges from the real notes on the two axes the project polices hardest: narrative reorganization and bullet register [VERIFIED for register; ESTIMATED for ratios]

Reading all 15 `real_validation.jsonl` records as ground truth:

- **Real narratives do not reorganize.** Every real narrative is the input in its original order, expanded into complete first-person sentences (e.g. #7 `"September long weekend needs plans ... Fill the Subaru with gas and seafoam treatment. Needs to be driven..."` → *"I need to plan to do some additional house chores ... I need to fill the Subaru with gas and seafoam treatment. The Subaru needs to be driven..."*). By hand-estimating `word_ratio` on #7, #9, #10, these land roughly 0.65–0.85 -- i.e. at or near the 0.85 line the corpus treats as a defect, and squarely in the range the 2026-09-02 remediation pass rewrote 29 synthetic records *away* from ("lead with different content, group related items, compress"). `evaluate_real.py` then prints "high here means the model is echoing the input rather than recovering it" -- but the expected narratives *are* high. The metric's interpretation is calibrated to the synthetic convention, not to what the product owner actually writes.
- **Real bullets are third-person, subject-elided, often with terminal periods.** All 15 real records use bullets like `"Needs to finish the workout booklet in Claude."`, `"Expresses joy for the days off after"`, `"Thinks it could be used as a panning platform"`, `"Is ridiculed for being different"`. REVIEW_GUIDE §6b's own regression regex (`^\s*(Needs to|Plans to|...|Thinks|Finds|Has to|Notes)\b`) would flag the majority of the ground-truth bullets, and 274 bullet periods were stripped corpus-wide as drift. The synthetic corpus is training the model to a bullet register the product owner does not produce.

Neither is a critique of the real notes -- they define the target. It means the synthetic conventions were derived from within the synthetic loop and never checked against the 15 real records (which the docs say were deliberately not consulted). `evaluate_real.py` only measures narrative similarity, so the bullet divergence is invisible in eval output.

**Recommended action:** (1) Decide explicitly whether the model should learn the product owner's register or the synthetic one; if the former, relax the bullet-register rule and re-read the "No non-recovery" threshold against real-tier ratios rather than treating 0.85 as universal. (2) Add a real-tier baseline print to `evaluate_real.py`: `word_ratio(expected_narrative, input)` per record and its mean, so the model's narrative-vs-input number is read *relative to the ground truth's own ratio* rather than as an absolute. (3) Record this as a PDR-level decision -- it changes what "recovery" means for this project.

### C4. Batch-tracking drift the §6b column-read is supposed to catch is present, uncaught, in a contiguous ~26-record run: terminal-period bullets, single-sentence summary bullets, and inconsistent empty `action_items` on shopping lists [VERIFIED]

From `"to buy: oats soy milk the good vanilla extract..."` through `"did he bring the stuff for it? I thought Rachel was going to remind him..."`, every record's bullets end in a period and most collapse the note into one or two long sentences (`"Items to buy include oats, soy milk, the good vanilla extract, spinach, bananas, some kind of berries, dish soap, and sponges."`). REVIEW_GUIDE states bullets were "normalized corpus-wide to bare list items". The run also contains a cross-example inconsistency within the same batch: `"art supplies for the workshop heavy watercolor paper..."` and `"party prep list balloons crepe paper streamers..."` (both `simple_list`) have `action_items: []` while `"to buy: oats..."` and `"need to order from the hardware store..."` in the same run have a filled purchase item. Nothing in the input distinguishes them.

**Recommended action:** Add a mechanical check to the §6b suite for bullet terminal punctuation (count of bullets ending in `.`), run it, and strip the periods in this run. Fill the two empty `action_items` (or empty the other two) and record the convention: a bare shopping list yields one "Buy/Get ..." item. Consider adding "bullets per record" and "median bullet length" to `check_copy_ratio.py`'s per-position drift table -- the drift table already exists; it just measures one axis.

### C5. The copy-ratio metric is punctuation-gameable, so the 0.85 gate under-detects non-recovery; and the two scripts don't compute the same number despite the docstring's claim [ESTIMATED / VERIFIED]

`evaluate_real.word_ratio` tokenizes by `str.lower().split()`, so `"him but"` vs `"him, but"` and `"dr chen"` vs `"Dr. Chen"` count as mismatches. Take `"dad's appointment with dr chen is tuesday. greg said he can drive him but greg is always late..."` (multi_person_note/expert): the narrative is the input word-for-word in order with capitalization, an em-dash, and three commas added. By hand count roughly 50 of ~65 tokens match → ~0.78, under the gate, though no recovery occurred. The remediation pass's "add commas, split a sentence" edits would lower ratios for the same reason. Assumption: whitespace tokenization as written; I did not run it.

Separately, `check_copy_ratio.copy_ratio` takes `max(word_ratio(a,b), word_ratio(b,a))` while `evaluate_real.py` reports the single order `word_ratio(narrative, input)`. `check_copy_ratio`'s docstring says the two are "the same measurement"; they are not.

**Recommended action:** In `word_ratio`, strip punctuation from tokens before comparing (`re.sub(r"[^\w']", "", tok)`), and use the symmetric max in both scripts (define it once in `evaluate_real.py`). Re-run `check_copy_ratio.py`; expect the mean and breach count to rise, and re-triage what surfaces rather than raising the threshold.

### C6. `evaluate_real.py`'s `no_repeat_ngram_size=6` bans output shapes the training targets contain constantly [ESTIMATED]

The comment argues n=6 "permits" entity reuse across sections. But in this corpus a bullet and an action item are routinely the same ≥6-token span: `"Wash the guest towels today"` / `"Wash the guest towels today"`; `"Grab the parcel from the locker today before the pickup code expires tonight"` (bullet ends `...expires tonight`, action item is the same clause); `"Take out the trash bins tonight"` ×2; `"Order the velvet curtains for the living room"` ×2. Under sentencepiece these are 6–12 tokens. The model was trained to emit the action item verbatim after the bullet and is forbidden from doing so at inference, so it is forced onto a paraphrase or a truncated item -- a degradation the eval then attributes to the model or the data. Assumption: T5 sentencepiece token counts ≈ word count + punctuation.

**Recommended action:** Measure before deciding: for each real-tier record, compute the longest token n-gram shared between `bullets` and `action_items` in the *expected* output; if the median is ≥6, the guard is fighting the target. Prefer a targeted fix for the observed degenerate loop (e.g. `repetition_penalty` restricted via a `LogitsProcessor` to *exact repeated action items*, or a post-hoc dedupe of identical `action_items` entries) over a global n-gram ban. Whatever is chosen, run the same `generate()` settings against a handful of *training* records and confirm the trained target is still reachable.

---

## Medium

### M1. `convert_real_notes.py`'s contamination gate uses the scoring `check_duplicates.py` retired, while its docstring promises "one definition of too similar" [VERIFIED]

`contamination()` computes `max(dup.char_ratio(note, other), dup.jaccard(words, dup.word_set(other)))` against `--threshold 0.55`, help text "matching check_duplicates.py (default 0.55)". `check_duplicates.py`'s docstring describes exactly that as "the previous version ... crying wolf and going silent at the same time" and now uses content-word jaccard ≥0.25 OR char ≥0.75. REVIEW_GUIDE §0.5 still documents the 0.55 single threshold. Three places, two definitions, one stale doc -- the drift the docstring said the design existed to prevent.

**Recommended action:** Expose a `similar(a, b) -> (jac, ch, flagged)` function in `check_duplicates.py` using its current thresholds and call it from `convert_real_notes.contamination()`; delete the local `--threshold` default or make it two flags mirroring the checker's. Update REVIEW_GUIDE §0.5 to the current thresholds and scoring.

### M2. `check_duplicates.py` can no longer gate anything: it exits 1 on "12 pre-existing flagged duplicate pairs" that are documented false positives, with no allowlist mechanism [VERIFIED via COST_LEDGER / CATEGORY_REFERENCE]

The 13th re-review row records "same 12 pre-existing flagged duplicate pairs, none new" as a clean result. With the script's documented exit codes ("1 = at least one pair flagged (so this can gate a batch)"), the gate is permanently red and a new genuine pair is only distinguishable by a human remembering the standing 12. `check_copy_ratio.py` solved the identical problem with a hash-keyed allowlist.

**Recommended action:** Add a pair allowlist keyed by `(sha256(input_a)[:16], sha256(input_b)[:16])` with a recorded rationale per pair, exclude allowlisted pairs from the exit code, and print them separately like `check_copy_ratio.py` does. Warn on allowlist entries whose hashes are no longer in the corpus.

### M3. `backfill_categories.py` exits 0 and writes with `--apply` even when the source failed to parse, contradicting "Exit status is non-zero if any entry was refused" [VERIFIED]

`entries, refusals = converter.parse(raw)`; each `r in refusals` is printed as `REFUSED (source parse)`, but `refusals` is not part of `ok = not (untagged or bad_cat or unmatched or ambiguous or conflicting)`. A malformed entry block therefore vanishes from the pipeline with exit code 0, and `--apply` proceeds. `convert_real_notes.py` gets this right (`return 1 if (refusals or hits) else 0`).

**Recommended action:** Include `refusals` in `ok`; add the count to the "refused" summary line.

### M4. `check_copy_ratio.py`'s allowlist has no liveness or ceiling check, and REVIEW_GUIDE still says the allowlist holds two records [VERIFIED]

The code carries 31 hash-keyed entries (2 original + 29 from 2026-09-02). REVIEW_GUIDE §6b says "Two records sit above 0.85 permanently ... Don't re-open these two. Do re-open any other record that climbs" and describes the script as carrying "#118 and #127 in an allowlist". Two gaps in the mechanism itself: (a) if an allowlisted record's `input` is later edited, its hash changes and the entry goes silently dead -- nothing reports "allowlist key not found"; (b) an allowlisted record is exempt at *any* ratio, so a narrative rewritten to 0.99 never fires. One allowlist rationale is also contradicted by its own record: `b53d08febfdbd9da` says compressing `"The sky looks very hazy today. The AQI must be high..."` "would invent a causal claim the input does not make" -- but that record's first bullet already reads `"The sky is very hazy, indicating the AQI must be high"`.

**Recommended action:** Store `(rationale, ceiling)` per entry, using each record's ratio at allowlisting time + 0.02 as the ceiling; fail if exceeded. Warn (non-zero exit) on allowlist keys absent from the corpus. Update REVIEW_GUIDE §6b to reference the disposition doc and the current count. Reword the hazy/AQI bullet to drop "indicating" or amend the rationale.

### M5. `third_party_review.py`'s bundle omits the documents its own prompt tells the reviewer to cross-check against, and silently overwrites a same-day prior report [VERIFIED]

`SYSTEM_PROMPT` says "Cross-check code behavior against docs/datasets/*.md's stated rules (schema, review checklist, taxonomy)". `BUNDLE_GLOBS` sends `docs/datasets/*.md` but not `docs/datasets/training_data.schema.json`, and sends no `training/*.md` except `COST_LEDGER.md` -- so `training/DATASET_SPEC.md`, cited in this bundle as *the* authority on the output schema, first-person rule, real-tier provenance, model serialization, and telemetry, was not provided. `training/tests/*.py` (referenced by requirements.txt, PDR-007, and CATEGORY_REFERENCE as the "17-test serialization suite") is also absent, so the tests' claims are unverifiable. This limits the present review (see UNVERIFIED items below). Also: `out_path = REVIEWS_DIR / f"{date.today().isoformat()}-claude-api-review.md"` with `write_text` -- a second run the same day overwrites the first billed report with no warning.

**Recommended action:** Add `training/DATASET_SPEC.md`, `training/SETUP.md`, `docs/datasets/*.json`, `training/tests/*.py` to `BUNDLE_GLOBS` (re-run `--dry-run` for the new token count). Refuse to overwrite an existing `out_path`, or append `-HHMM`. Drop the meaningless `sum(1 for _ in REPO_ROOT.glob('*'))` "top-level entries scanned" statistic.

### M6. `action_items` register is inconsistent across the corpus in at least four shapes, including the colon-label format batch 27 says was rewritten away [VERIFIED]

- Imperative (majority): `"Buy milk, eggs, and bread."`
- First-person declarative copied from input: `"I think I'll t