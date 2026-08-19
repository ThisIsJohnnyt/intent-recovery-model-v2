# Gold Philosophy

The constitution of the Gold Curriculum Series: principles that hold across
every release, unlike a `gold_vX.Y_curriculum.md` (one release's specific
theme and examples), a dataset card (one release's scope/limitations), or a
review report (one release's quality check) — all of which are expected to
change release to release. These eight don't. A new release proposing to
violate one of these isn't a new curriculum choice, it's a regression.

Curriculum specs should **link here, not restate these**.

## The eight principles

**Evidence First** — every recovered fragment, boundary, and relationship in
the output must be traceable to something actually in the input. Nothing is
inferred from plausibility alone. Operationalized in
[`docs/datasets/REVIEW_GUIDE.md`](../datasets/REVIEW_GUIDE.md)'s "No invented
content" checklist.

**No Magic Examples** — every fragment in a generated note must be
explainable: why it's interrupted, why it repeats, why it has no
punctuation, why a reference dangles. An unexplainable fragment is noise,
not signal. Defined in
[`training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md)'s "Two rules
for every example."

**One Lesson Per Example** — each example teaches one specific recovery
skill, named as its `category`. An example testing two unrelated things at
once should be split or simplified. Also defined in `DATASET_SPEC.md`'s
"Two rules," enforced by `REVIEW_GUIDE.md`.

**Progressive Difficulty** — a release's examples build in difficulty
deliberately, each tier introducing traits named by that tier's own
definition, not just more topics. See
[`docs/datasets/TAXONOMY.md`](../datasets/TAXONOMY.md)'s "Difficulty
categories" for the tier vocabulary once it's defined for this repository.

**Boundary Evidence** — a segmentation boundary is never asserted without
citing what in the text signals it and how confident that signal is. Turns
"the model segmented this correctly" from a subjective read into something
checkable. Design-notes-only — never a field in the trained JSONL (see
`DATASET_SPEC.md`'s "Data contract").

**Preserve Uncertainty** — an incomplete thought or an unresolved reference
stays incomplete/unresolved in the output. The model is never rewarded for
guessing a plausible resolution.

**Human-Centered Intent Recovery** — the task is recovering what a person
meant to capture, not diagnosing why they wrote it that way. Cognitive/
emotional *state* is fair game (rushed, distracted, excited); a diagnosis
label (ADHD, autism, etc.) never is. See
[`NORTH_STAR.md`](NORTH_STAR.md)'s mission statement and
`REVIEW_GUIDE.md`'s "No diagnosis framing" check.

**No Harmful or Illegal Content** — no content depicting, instructing, or
normalizing self-harm, suicide, violence toward oneself or others, or other
illegal or seriously immoral activity is ever permitted in this project's
data, at any tier, at any release. Not a category, not a difficulty signal
— content that must never exist in this project's data at all. A drifted
example is discarded and regenerated from scratch, never edited down to
something safer. Permanent and non-negotiable; see
[PDR-001](../decisions/PDR-001.md) and [PDR-005](../decisions/PDR-005.md)
for why this project holds this boundary. Operationalized in
`training/DATASET_SPEC.md`'s generation-prompt exclusion and
`REVIEW_GUIDE.md`'s hard-gate check.

## Why this document exists

Without a stable reference, these principles get re-stated inside every
`gold_vX.Y_curriculum.md`'s "Design Principles" section — harmless the first
time, but a duplication risk on every release after: a wording tweak in one
curriculum doc doesn't propagate to the others, and eventually two releases
describe "Evidence First" slightly differently. Centralizing them here means
a curriculum spec only needs to state what's *new* about that release, and
link back here for what isn't.
