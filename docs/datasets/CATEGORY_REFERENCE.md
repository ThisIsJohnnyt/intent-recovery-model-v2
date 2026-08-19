# Category Reference

Per-category detail for [`TAXONOMY.md`](TAXONOMY.md)'s category vocabulary
— a fuller worked example than that file's one-liner, plus the tracking
sections [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §6 checks a new batch against
and updates after review. Definitions live in `TAXONOMY.md`, linked here,
not restated.

**Status**: first draft, 2026-08-19, alongside `TAXONOMY.md`'s acceptance.
No batches exist yet — every tracking section below starts empty, by
construction, not by omission.

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
from this list once at least one accepted example exists for it. Starts as
the full list, since no batches exist yet:

`simple_list`, `interrupted_thought`, `topic_switching`,
`topic_interleaving`, `dangling_reference`, `repeated_reminder`,
`zero_action_items`, `contradictory_statement`, `rapid_branching`,
`minimal_fragment`, `long_rambling`, `multi_person_note`,
`voice_to_text_artifact`, `self_correction`, `time_ambiguous`

## Cognitive / emotional / structural states covered

Mirrors [`training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md)'s
diversity requirements — updated after each batch with what that batch
newly covers, so under-represented states are visible at a glance rather
than requiring a re-read of the whole corpus.

**Cognitive/emotional states** (target: roughly even coverage, not
mostly-anxious): calm/organized, mild distraction, hyperfocus, executive
dysfunction, anxiety, sensory overwhelm, burnout, rapid-branching
excitement, emotional journaling, dry/neutral observation.

- Covered so far: *(none — no batches generated yet)*

**Structural variety**: interleaved topics, abrupt topic switches,
half-finished thoughts, dangling references, restated worries, contradictory
statements, zero-action-item notes, very short notes, long rambling notes,
subjects spanning work/relationships/health/chores/hobbies/money/family.

- Covered so far: *(none — no batches generated yet)*

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
