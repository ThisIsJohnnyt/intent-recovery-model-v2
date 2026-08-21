# Dataset Batch Review Guide

A checklist for reviewing a new batch of examples (gold or synthetic)
before it's accepted into `datasets/`. Process before scale — write and
prove out this review discipline before generating at volume.

## 0. No harmful or illegal content (hard gate — checked first)

Before anything else: does any example depict, instruct, or normalize
self-harm, suicide, violence toward oneself or others, or other illegal or
seriously immoral activity? Permanent, non-negotiable, and checked ahead of
every other item on this list — see
[`GOLD_PHILOSOPHY.md`](../vision/GOLD_PHILOSOPHY.md)'s "No Harmful or
Illegal Content" principle and [PDR-005](../decisions/PDR-005.md).

If any example fails this check, the remedy is always **discard and
regenerate that example from scratch** — never edit it down to something
safer. A partial edit risks leaving residual unsafe phrasing in the
corpus. This is not a "needs revision" outcome like the other checklist
items below; it's an immediate reject.

## 0.5. Near-duplicate check

Run [`training/check_duplicates.py`](../../training/check_duplicates.py)
against the full corpus (not just the new batch — a new example can
collide with one from an earlier batch) before anything else in this list:

```bash
cd training
python check_duplicates.py
```

This is the mechanism [`TAXONOMY.md`](TAXONOMY.md)'s "No near-duplicate
content" rule refers to — a lexical similarity check (character-sequence +
word-overlap) flagging pairs at or above a 0.55 threshold by default. It
surfaces candidates, it doesn't auto-reject: a flagged pair still needs a
human read to judge whether it's a genuine near-duplicate (same scenario,
same phrasing pattern) or just incidental word overlap (shared names,
common filler). It's lexical-only — it will not catch a paraphrase that
reuses no wording; see the script's docstring for when embedding-based
similarity would be worth the added API cost instead.

## 1. Schema validity

Run it through the pipeline's own validator — don't eyeball this one:

```bash
cd training
C:\Users\thisi\.venvs\intent-recovery-v2\Scripts\python.exe -c "
from prepare_data import load_jsonl
from pathlib import Path
records = load_jsonl(Path('../datasets/<path-to-batch>.jsonl'))
print(f'{len(records)} records validated OK')
"
```

(See [`training/SETUP.md`](../../training/SETUP.md) for why the venv
lives outside `training/` — a Windows path-length limit, not a change of
convention worth remembering as "just how it is.")

If this throws, the batch has a schema problem (missing field, wrong type)
— fix before anything else. This Python validator is authoritative (it's
literally what gates training) once `prepare_data.py` exists;
[`training_data.schema.json`](training_data.schema.json) is a
machine-checkable mirror of the same contract, useful for a self-check with
any standard JSON Schema tool before a batch even reaches that step.

## 2. "No Magic Examples"

For every example, for every fragment in `input`: can you say *why* it's
there? Why interrupted, why repeated, why no punctuation, why a dangling
reference? If you can't explain a fragment, it's noise — reject or
regenerate that example. (See
[`training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md).)

## 3. One lesson per example

Does the example's `category` actually match what it teaches? Would someone
reading only the `input`/`output` pair understand what skill this example is
meant to test? If an example seems to be testing two unrelated things at
once, split it or simplify it.

## 4. No invented content ("evidence-first" compliance)

Check the model/reference output against each of these specifically —
don't just eyeball for a general sense of accuracy:

- **Preserved uncertainty**: uncertain references (e.g. "the blue folder")
  or genuinely open questions in `input` stay uncertain/open in the
  output — never resolved with a guessed answer.
- **No invented chronology**: the output never asserts an order of events
  that `input` doesn't state.
- **No invented causality**: the output never asserts one fragment caused
  or explains another unless `input` actually says so — adjacency in the
  text is not evidence of a relationship.
- **No merged unrelated intentions**: two fragments that are actually
  unrelated stay represented as separate items, never combined into one
  (even a superficially plausible-sounding) combined statement.
- **No lost low-salience reminders**: every fragment in `input` — however
  brief or seemingly minor — appears *somewhere* in the output (narrative,
  bullets, or action_items). A short fragment being easy to drop is not a
  reason to drop it.
- **No over-summarization**: don't compress `input` so much that a
  distinct fragment disappears into a vaguer, more general statement.
- **No unsupported tasks**: `action_items` never contains a task that
  isn't implied by `input`.
- **No misattribution**: when a note mentions more than one person, a
  fragment belonging to one of them is never reassigned to another.
- **No invented certainty**: a hedge in `input` ("i think," "maybe," "if
  not... totally stuck") stays a hedge in the output — never smoothed into
  a flat, confident, or causally-linked statement the input didn't
  actually make. Distinct from invented chronology/causality above: this
  is asserting a *tone* (certainty, finality, a decision) that isn't
  there, not asserting a new fact. Easy to miss specifically because the
  schema asks for "coherent flowing narrative" — smoothing a hedge is what
  makes prose read well, which is exactly why it's worth checking for
  deliberately rather than trusting a fluency read. Identified by the
  first periodic adversarial re-review (PDR-006, 2026-08-19) — see this
  file's "Periodic adversarial re-review" section's log.
  **Check `action_items` at least as carefully as narrative/bullets, not
  less** — the second adversarial re-review found this exact failure mode
  recurring specifically in `action_items`, even in examples where
  narrative/bullets correctly preserved the hedge. `action_items` has no
  fluency pressure (it's terse and imperative by design), so the smoothing
  mechanism there isn't "prose reads better" — it's that an imperative,
  decided-sounding field seems to pull hedged input toward false certainty
  on its own. Also watch for a genuinely ambiguous referent (e.g. a
  pronoun or conditional that could plausibly point to either of two
  established threads) getting silently resolved to one reading instead of
  flagged as unresolved — a distinct but related trap from smoothing a
  literal hedge word.

These categories of failure carried real, observed instances in the
predecessor project — use this list as a concrete checklist against real
failure modes, not just an abstract one, even though v2.0 starts with a
fresh corpus and no lessons-learned history of its own yet.

## 5. No diagnosis framing

Nothing in `input`, `output`, or design notes should reference a diagnosis
(ADHD, autism, etc.) or assume *why* the note is fragmented. Cognitive/
emotional *state* is fine (rushed, distracted, excited); a label for a
condition is not. (See
[`docs/vision/NORTH_STAR.md`](../vision/NORTH_STAR.md).)

## 6. Diversity coverage

Check the new batch against [`CATEGORY_REFERENCE.md`](CATEGORY_REFERENCE.md)'s
target-categories-not-yet-represented and cognitive/emotional-states-covered
sections, once those exist. Does this batch fill a gap, or does it pile onto
an already-covered category/state? Update `CATEGORY_REFERENCE.md` after
review with whatever this batch newly covers.

## 7. Design notes match the data

For gold-tier batches specifically: does the `*_design_notes.md` file
actually describe what's in the `.jsonl`? (Easy to drift if the JSONL gets
edited after the notes are written.)

## 8. Curriculum Integrity

Beyond whether a single example is internally sound (item 3), does this
*batch* still fit the release it's part of? Check the batch's
`gold_vX.Y_curriculum.md`'s "Out of Scope" section for capabilities reserved
for future releases — a well-written example that quietly exercises one of
those is curriculum creep, even on its own terms.

## Periodic adversarial re-review

Per [PDR-006](../decisions/PDR-006.md): items 0–8 above run on every batch,
by the same collaborator (Claude) who wrote that batch's generation prompt
and taxonomy understanding — a real correlation-bias risk, since a
systematic blind spot would be consistent between the two roles rather
than visible as a contradiction. This section is a supplementary,
periodic audit against that specific risk, not a replacement for items
0–8, which still gate every batch's initial acceptance.

**Cadence**: every 2 batches of synthetic generation (i.e. after batch 4,
6, 8, ...), and always before any gold-tier release bundle is finalized —
whichever comes first. Tightened from every 3 batches to every 2 after the
first run (see log below) — the product owner's call, as generation volume
grows and each batch adds more corpus for a blind spot to hide in.

**Sample**: at least 10 examples, or 15% of the corpus accepted since the
last adversarial re-review, whichever is larger. Weight the sample toward
categories that have had the most fixes/relabels historically (see
`CATEGORY_REFERENCE.md`'s "Depth by category" section) — those are where a
shared blind spot is most likely to be hiding, precedent already shown by
batches 1 and 3.

**Process**: spawn a fresh agent with no involvement in writing the
sampled batches' generation prompts or taxonomy revisions. Give it this
file's items 0–8 and the sampled examples — **not** the original review's
conclusions or reasoning for accepting them. Instruct it to look
adversarially: assume nothing already reviewed is necessarily correct, and
report findings independent of what the first pass concluded.

**Reconciling findings**: per
[`AI_COLLABORATION.md`](../vision/AI_COLLABORATION.md)'s "Conflict
resolution" — surface disagreements between the original review and the
adversarial pass to the product owner rather than silently resolving them
either way. A finding that holds up gets the same disposition as any other
review defect (fix in place, relabel, or reject and regenerate).

**What this doesn't solve**: the fresh-context reviewer is still Claude,
not an architecturally independent model — this reduces same-context
correlation bias, not model-family correlation bias. See PDR-006 for the
stronger options considered and not adopted.

**Log**:

| Date | Sample | Result | Findings |
|---|---|---|---|
| 2026-08-19 | 15 examples (batches 1–4), weighted toward `voice_to_text_artifact`/`contradictory_statement`/`dangling_reference`/`self_correction`/`interrupted_thought` — the categories with the most historical fixes/relabels, plus 2 control examples from never-flagged categories | 10 ACCEPT, 5 FIX, 0 REJECT, 0 hard RELABEL | First run — validated the safeguard itself works (found real, previously-uncaught defects, not just noise) and surfaced a genuine checklist gap: 4 of the 5 fixes shared one root pattern (a hedge in `input` smoothed into unearned certainty in the output) that §4's existing bullets didn't separately name. Added as "No invented certainty" above. The 5 flagged examples were fixed in place directly (not rejected — none were fundamentally unsound, all were narrow wording overreaches). Next run due after batch 6 — product owner tightened the cadence to every 2 batches after this run, rather than every 3. |
| 2026-08-19 | 12 examples (batches 5–6), all 12 originally reviewed by Claude as "zero issues" — deliberately sampled to stress-test that confidence, weighted toward dense/expert-difficulty examples (multiple hedges, ambiguous cross-person attribution) since that's where a same-reviewer blind spot is most likely | 9 ACCEPT, 3 FIX, 0 REJECT | **The original "zero issues" verdict was not justified for 3 of 12.** Two were the same "No invented certainty" failure mode recurring — both specifically in `action_items`, even where narrative/bullets got the hedge right (one flattened "kinda liked" to "likes"; one silently resolved a genuinely ambiguous conditional — "I'll do it if Greg doesn't," where Greg's only established role was driving, not calling — into a flat, unhedged action item). The third was an unrelated mislabel (`topic_switching` when the structure was textbook `topic_interleaving`, confirmed by direct comparison with a correctly-labeled neighboring example). All 3 fixed in place. §4's "No invented certainty" bullet updated to name `action_items` as the higher-risk field specifically, per the reviewer's diagnosis that the field's terse, imperative format — not narrative fluency pressure — is the actual mechanism. Next run due after batch 8. |

## After review

- Accepted batches: update `datasets/gold/CHANGELOG.md` (or the synthetic
  equivalent) and `CATEGORY_REFERENCE.md`.
- Rejected/needs-revision: send back with which checklist item(s) failed —
  specific enough that the fix is obvious, not just "doesn't feel right."
- Same moment as the new `COST_LEDGER.md` row: call
  `training/telemetry.py`'s `batch_finished(accepted_delta, rejected_delta)`
  — see `training/DATASET_SPEC.md`'s "Telemetry" section.

## Release bundle

Every gold release is more than a `.jsonl` file:

| File | Written by | When |
|---|---|---|
| `gold_vX.Y.jsonl` | Gemini (generation), reviewed by the product owner | Before release |
| `gold_vX.Y_design_notes.md` (using [DESIGN_NOTES_TEMPLATE.md](DESIGN_NOTES_TEMPLATE.md)) | Product owner (author intent) | Before release |
| `gold_vX.Y_review_report.md` (this checklist, filled in) | Claude (independent check) | Before release |
| `CHANGELOG.md` entry | Whoever accepts the release | At acceptance |
| `gold_vX.Y_lessons_learned.md` | Shared — product owner, Claude, and findings from Gemini-side generation notes | After training + evaluation |
| `gold_vX.Y_benchmark_results.md` | Whoever runs the benchmark | After training + evaluation |

Three of these ask genuinely different questions, not overlapping ones:

- **Design notes**: why was each example written?
- **Review report**: does this batch pass the quality bar, independently
  checked?
- **Lessons learned**: after actually training and evaluating on it, what
  did we discover — unexpected successes, unexpected failures, surprises,
  recommendations for the next release?

Reuses the existing `gold_vX.Y` version number for every file in the
bundle — one identifier per release, not a separate numbering scheme.

## Release Checklist

The reusable acceptance-criteria core every `gold_vX.Y_curriculum.md` should
link to instead of restating:

- [ ] No harmful or illegal content (§0, hard gate, checked first)
- [ ] Near-duplicate check run against the full corpus (§0.5)
- [ ] Schema validation passes (§1)
- [ ] Design notes complete, including Boundary Evidence (§7, per
      [`DESIGN_NOTES_TEMPLATE.md`](DESIGN_NOTES_TEMPLATE.md))
- [ ] Review report complete (this checklist, filled in)
- [ ] Category reference updated (§6)
- [ ] `CHANGELOG.md` updated
- [ ] Benchmark and holdout cases identified
- [ ] Independent review passes (Claude reviews Gemini-generated content
      before acceptance — never accepted unreviewed)
- [ ] Periodic adversarial re-review completed (always due before a
      release, per PDR-006 — see "Periodic adversarial re-review" above)
- [ ] Training compatibility confirmed (`prepare_data.py` reads it cleanly,
      once it exists)
- [ ] Evaluation shows no unacceptable regression against prior releases
      (once a benchmark suite exists to measure this)
- [ ] Lessons learned recorded after training + evaluation

A release-specific curriculum doc adds only what's genuinely unique to that
release on top of this — not a parallel restatement of the items above.
