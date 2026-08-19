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
./venv/Scripts/python.exe -c "
from prepare_data import load_jsonl
from pathlib import Path
records = load_jsonl(Path('../datasets/<path-to-batch>.jsonl'))
print(f'{len(records)} records validated OK')
"
```

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

## After review

- Accepted batches: update `datasets/gold/CHANGELOG.md` (or the synthetic
  equivalent) and `CATEGORY_REFERENCE.md`.
- Rejected/needs-revision: send back with which checklist item(s) failed —
  specific enough that the fix is obvious, not just "doesn't feel right."

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
- [ ] Training compatibility confirmed (`prepare_data.py` reads it cleanly,
      once it exists)
- [ ] Evaluation shows no unacceptable regression against prior releases
      (once a benchmark suite exists to measure this)
- [ ] Lessons learned recorded after training + evaluation

A release-specific curriculum doc adds only what's genuinely unique to that
release on top of this — not a parallel restatement of the items above.
