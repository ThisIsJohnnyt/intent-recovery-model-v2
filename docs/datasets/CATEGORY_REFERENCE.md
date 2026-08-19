# Category Reference

Per-category detail for [`TAXONOMY.md`](TAXONOMY.md)'s category vocabulary
— a fuller worked example than that file's one-liner, plus the tracking
sections [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §6 checks a new batch against
and updates after review. Definitions live in `TAXONOMY.md`, linked here,
not restated.

**Status**: first draft, 2026-08-19, alongside `TAXONOMY.md`'s acceptance.
Tracking sections below reflect batches 1–2 (`datasets/synthetic.jsonl`,
2026-08-19 — see `training/COST_LEDGER.md`).

## Per-category detail

Each entry: a fuller worked example than `TAXONOMY.md`'s one-liner, plus
lifecycle. All 15 categories were introduced together in this draft — no
deprecations yet.

| Category | Worked example (`input`) | Introduced | Status |
|---|---|---|---|
| `simple_list` | "milk, eggs, bread, call dentist about the appt, drop off the library books, text sam back" | v2.0 draft, 2026-08-19 | Active |
| `interrupted_thought` | "need to talk to sam about the— oh also don't forget the electric bill is due friday. wait what was I gonna say about sam" | v2.0 draft, 2026-08-19 | Active |
| `topic_switching` | "deck is due wednesday, need three more slides on the budget section. also should get mia a birthday present, she likes that one candle brand" | v2.0 draft, 2026-08-19 | Active |
| `topic_interleaving` | "budget slides due wed. mia's present — candle brand. slides also need the timeline chart. maybe the lavender one for mia. timeline chart pulls from last quarter's numbers" | v2.0 draft, 2026-08-19 | Active |
| `dangling_reference` | "still need to deal with the thing from tuesday before it becomes a problem. also grab the folder off the blue chair" | v2.0 draft, 2026-08-19 | Active |
| `repeated_reminder` | "don't forget to call the insurance company. ugh, seriously need to call insurance before end of week. also water the plants" | v2.0 draft, 2026-08-19 | Active |
| `zero_action_items` | "weird how quiet the office was today. nobody said much at lunch either. kind of a strange day overall" | v2.0 draft, 2026-08-19 | Active |
| `contradictory_statement` | "really excited to start the garden project this weekend. ...actually not sure I even have the energy for it anymore, might just skip it" | v2.0 draft, 2026-08-19 | Active |
| `rapid_branching` | "what if the app had a widget — actually what if the widget synced across devices — that means we'd need an account system — which means onboarding — which we haven't even designed yet" | v2.0 draft, 2026-08-19 | Active |
| `minimal_fragment` | "pick up dry cleaning" | v2.0 draft, 2026-08-19 | Active |
| `long_rambling` | A long, loosely structured note touching six or more small unrelated points (work deadline, a errand, a passing worry about a friend, a grocery item, a half-formed idea, a scheduling conflict), none individually load-bearing. | v2.0 draft, 2026-08-19 | Active |
| `multi_person_note` | "sam wants pizza tonight, jen said she's not that hungry so just grab her a salad, and tell dad we're not coming till 7" | v2.0 draft, 2026-08-19 | Active |
| `voice_to_text_artifact` | "so i need to um pick up the the dry cleaning before like six and also uh call the the insurance place tomorrow" | v2.0 draft, 2026-08-19 | Active |
| `self_correction` | "call the plumber tomorrow about the sink — actually no forget that, already got it fixed" | v2.0 draft, 2026-08-19 | Active |
| `time_ambiguous` | "need to deal with this before the thing on friday, or maybe after, depends how the week goes" | v2.0 draft, 2026-08-19 | Active |

## Target categories not yet represented

Updated after each batch per `REVIEW_GUIDE.md` §6 — a category is removed
from this list once at least one accepted example exists for it.

After batches 1–2 (`datasets/synthetic.jsonl`, 2026-08-19; batch 1: 13
accepted of 15; batch 2: 14 accepted of 15, targeted at closing batch 1's
gaps — see `training/COST_LEDGER.md`):

*(none — every category now has at least one accepted example)*

Batch 2 targeted all three of batch 1's gaps directly, with explicit
guidance to avoid each one's specific failure mode:
`interrupted_thought` (2/2 accepted — the cut-off fragment now correctly
preserved as unresolved instead of dropped) and `contradictory_statement`
(2/2 accepted — now correctly an unresolved tension, not conflated with
`self_correction`) both fully resolved. `voice_to_text_artifact` improved
but not fully — 1 of 2 accepted; the rejected one repeated the same "No
Magic Examples" failure mode as batch 1 (one fragment not traceable to a
plausible dictation error), just subtler. Worth another attempt in a future
batch if more `voice_to_text_artifact` coverage is wanted, though one
accepted example now exists where none did before.

Every category has at least one accepted example after batches 1–2.

## Depth by category (running total, after batch 4)

Batch 3 (14 accepted of 15 — see `training/COST_LEDGER.md`) surfaced a
pattern: Gemini kept defaulting to clean-resolution `self_correction`-shaped
content when asked for `contradictory_statement` or `dangling_reference`
specifically. Batch 4 tested a fix — explicit contrastive definitions
(what each category is NOT) instead of just naming them — and it worked:
**15 of 15 accepted, 0 relabeled**, all 6 targeted `contradictory_statement`/
`dangling_reference` examples correctly distinct from `self_correction` this
time. Worth reusing this contrastive-definition approach for any category
that shows the same confusion pattern in the future.

Every category now has at least 3 accepted examples — first time the corpus
has had no thin categories at all:

`simple_list` (3), `interrupted_thought` (4), `topic_switching` (4),
`topic_interleaving` (3), `dangling_reference` (5), `repeated_reminder` (3),
`zero_action_items` (4), `contradictory_statement` (5), `rapid_branching`
(3), `minimal_fragment` (3), `long_rambling` (3), `multi_person_note` (4),
`voice_to_text_artifact` (3), `self_correction` (6), `time_ambiguous` (3).

56 accepted examples total across 4 batches (13 + 14 + 14 + 15). A future
batch could deepen any category further, or shift focus to `difficulty`
balance and continued subject-matter variety rather than category coverage,
which is no longer the binding constraint.

## Cognitive / emotional / structural states covered

Mirrors [`training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md)'s
diversity requirements — updated after each batch with what that batch
newly covers, so under-represented states are visible at a glance rather
than requiring a re-read of the whole corpus.

**Cognitive/emotional states** (target: roughly even coverage, not
mostly-anxious): calm/organized, mild distraction, hyperfocus, executive
dysfunction, anxiety, sensory overwhelm, burnout, rapid-branching
excitement, emotional journaling, dry/neutral observation.

- Covered so far (batches 1–2, 2026-08-19): calm/organized, mild
  distraction, hyperfocus, rapid-branching excitement, dry/neutral
  observation (batch 1); executive dysfunction, anxiety, sensory overwhelm,
  burnout, emotional journaling (batch 2).
- Not yet covered: *(none — all target states have at least one example;
  future batches can now deepen coverage rather than fill gaps)*.

**Structural variety**: interleaved topics, abrupt topic switches,
half-finished thoughts, dangling references, restated worries, contradictory
statements, zero-action-item notes, very short notes, long rambling notes,
subjects spanning work/relationships/health/chores/hobbies/money/family.

- Covered so far (batches 1–2, 2026-08-19): interleaved topics, abrupt
  topic switches, half-finished thoughts left genuinely unresolved (batch 2
  fixed batch 1's dropped-fragment failure), dangling references, restated
  worries, contradictory statements (batch 2 fixed batch 1's category
  mismatch), zero-action-item notes, very short notes, long rambling notes,
  subjects spanning work/relationships/health/chores/hobbies/money/family.
- Not yet covered: *(none identified so far)*.

## Category lifecycle

No deprecations or renames yet — this section exists per
[`AI_COLLABORATION.md`](../vision/AI_COLLABORATION.md)'s "Dataset
lifecycle" reference and will record any future addition, rename, or
deprecation (and why) as those happen, rather than only ever showing the
current state.

## See also

- [`TAXONOMY.md`](TAXONOMY.md) — category definitions, difficulty tiers,
  boundary/confidence categories, dataset labeling rules.
- [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §6 — how this file gets checked and
  updated as part of batch review.
- [`DESIGN_NOTES_TEMPLATE.md`](DESIGN_NOTES_TEMPLATE.md) — per-example
  design notes; this file tracks the corpus in aggregate, that one tracks a
  single example.
