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

## Depth by category (running total, after batch 5)

Batch 5 (15/15 accepted, 0 fixes — see `training/COST_LEDGER.md`) weighted
the 8 categories then at the floor (3 each) and also tested the adversarial
review's "invented certainty" finding as a *preventive* prompt instruction
rather than only a review-time check — it worked cleanly across all 15,
first batch needing zero corrections of any kind.

`simple_list` (5), `interrupted_thought` (4), `topic_switching` (4),
`topic_interleaving` (5), `dangling_reference` (5), `repeated_reminder`
(5), `zero_action_items` (4), `contradictory_statement` (5),
`rapid_branching` (5), `minimal_fragment` (5), `long_rambling` (5),
`multi_person_note` (4), `voice_to_text_artifact` (5), `self_correction`
(6), `time_ambiguous` (4).

71 accepted examples total across 5 batches (13 + 14 + 14 + 15 + 15).
Depth is now tightly banded (4–6 across every category) — no category is
meaningfully thin relative to the others anymore.

## Depth by category (running total, after batch 6)

Batch 6 (15/15 accepted, 0 fixes) closed out the remaining categories
still at the depth floor and deliberately skewed toward `expert`/`hard`
difficulty, since the corpus-wide difficulty spread had grown lopsided
(`expert` at 9/71 vs. 18-27 for the other tiers) even as category depth
evened out — depth and difficulty are independent things to track, and
this batch is the first one to target difficulty specifically rather than
category.

`simple_list` (5), `interrupted_thought` (6), `topic_switching` (6),
`topic_interleaving` (5), `dangling_reference` (7), `repeated_reminder`
(5), `zero_action_items` (6), `contradictory_statement` (7),
`rapid_branching` (5), `minimal_fragment` (5), `long_rambling` (5),
`multi_person_note` (6), `voice_to_text_artifact` (5), `self_correction`
(7), `time_ambiguous` (6).

**Difficulty distribution, full corpus**: easy 19, medium 29, hard 23,
expert 15 (86 total). Improved from pre-batch-6 (easy 17, medium 27, hard
18, expert 9) but medium still leads by a wide margin — worth another
difficulty-targeted batch at some point, same approach as batch 6.

86 accepted examples total across 6 batches (13 + 14 + 14 + 15 + 15 + 15).

## Depth by category (running total, after batch 7)

Batch 7 (15/15 accepted, 0 fixes, 2 relabeled — first batch run with live
F.A.R.T. telemetry, see `training/telemetry.py`) closed the depth floor on
6 of the 7 targeted categories, but confirmed a real gap: `topic_switching`
vs. `topic_interleaving` needs the same contrastive-definition treatment
`contradictory_statement`/`dangling_reference` got in batch 4 — both
requested `topic_switching` examples this round were structurally
interleaved instead, so the category gained zero net depth despite being
targeted twice in a row now (also true in the second adversarial review's
sample).

`simple_list` (7), `interrupted_thought` (6), `topic_switching` (5, now
the clear outlier — needs a dedicated future batch), `topic_interleaving`
(8), `dangling_reference` (7), `repeated_reminder` (7), `zero_action_items`
(6), `contradictory_statement` (7), `rapid_branching` (7),
`minimal_fragment` (7), `long_rambling` (7), `multi_person_note` (6),
`voice_to_text_artifact` (8), `self_correction` (7), `time_ambiguous` (6).

**Difficulty distribution, full corpus**: easy 21, medium 31, hard 28,
expert 21 (101 total). Meaningfully better balanced — hard and expert are
now close to easy, only medium still leads by a real margin.

101 accepted examples total across 7 batches
(13 + 14 + 14 + 15 + 15 + 15 + 15).

## Depth by category (running total, after batch 8)

Batch 8 (15/15 accepted, 0 relabeled, 3 narrative fixes) closed the
`topic_switching` gap that had persisted across two consecutive batches.
All 4 requested examples came back structurally correct — a strict A→B
sequence with exactly one transition and zero returns to subject A — and
the category went 5 → 9, from clear outlier to joint-highest.

The batch also surfaced a likely root cause that goes beyond "the category
definition was too weak," the explanation carried since batch 7.
[`TAXONOMY.md`](TAXONOMY.md) defines `expert` as a "dense combination of
categories, longer note, more restated/branching content" — which is
*structurally* alternation, and therefore structurally
`topic_interleaving`. Batches 6 and 7 both deliberately skewed hard/expert,
so for this one category the difficulty instruction and the category
instruction were pulling in opposite directions, and Gemini resolved the
conflict toward difficulty both times. That also explains why batch 4's
contrastive fix worked immediately for `contradictory_statement` and
`dangling_reference`: neither is at odds with density. Batch 8 removed the
conflict by capping the `topic_switching` examples at `hard` and routing
the expert quota elsewhere, and specifying where their difficulty should
come from instead (jarring subject pairs, low-salience fragments, an
unresolved reference inside one block, hedged time language).

**Generalizable lesson**: before blaming a recurring mislabel on a weak
category definition, check whether some *other* instruction in the same
prompt structurally contradicts that category. A contrastive definition
fixes ambiguity; it does not fix a prompt that asks for two incompatible
things at once.

`simple_list` (7), `interrupted_thought` (7), `topic_switching` (9),
`topic_interleaving` (8), `dangling_reference` (7), `repeated_reminder`
(7), `zero_action_items` (9), `contradictory_statement` (7),
`rapid_branching` (7), `minimal_fragment` (7), `long_rambling` (7),
`multi_person_note` (9), `voice_to_text_artifact` (8), `self_correction`
(7), `time_ambiguous` (9).

Depth is tightly banded at 7–9 across all 15 categories — no category is
thin relative to the others, and there is no longer an obvious targeting
priority. Future batches can weight toward difficulty balance and
subject-matter variety rather than category coverage.

**Difficulty distribution, full corpus**: easy 22, medium 36, hard 34,
expert 23 (115 total, post-adversarial-review). Hard has nearly caught
medium; medium's lead is the smallest it has been.

**Review note**: all 3 defects this batch were invented content confined to
`narrative`, with `bullets` and `action_items` clean in every case — the
inverse of batch 7's pattern, where `action_items` was the weak field.
Worth watching whether the heavy `action_items`-specific prompt guidance
has shifted the failure mode upstream into narrative prose rather than
eliminating it.

115 accepted examples total across 8 batches
(13 + 14 + 14 + 15 + 15 + 15 + 15 + 15, less 1 rejected by the third
adversarial re-review).

**Third adversarial re-review (2026-08-23), applied to this corpus.** Run
immediately after batch 8 per the every-2-batches cadence; full findings in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. It found a failure mode none of
§4's bullets named — *world-knowledge frame completion*, the output naming an
activity or object class the input only implies through its props — which
accounted for 7 of its 11 fixes and is now its own checklist item, a
`DATASET_SPEC.md` rule, and a standing instruction in the generation prompt.
Net corpus effect: 17 in-place fixes across 9 examples, 2 difficulty
relabels (`zero_action_items` #107 `expert`→`medium`,
`voice_to_text_artifact` #97 `expert`→`hard`), and 1 rejection — an
`interrupted_thought` example in which nothing was actually cut off, so it
taught none of the unfinished-vs-resumed judgment the category exists for.
That rejection is why `interrupted_thought` reads 7 here rather than 8; it
is parked for regeneration in a future batch rather than replaced by
editing.

**Narrative-voice drift in `voice_to_text_artifact` — found and fixed
2026-08-23.** Initially logged as a two-example nit; listing all 8 examples in
the category side by side showed it was the category majority and had been
drifting for four batches. Narratives were first person in batches 2–3 (#18,
#28, #29), turned to third-person meta-description from batch 5 (#69, #70) and
stayed that way through batch 7 (#96, #97, #98) — "Voice-recorded reminders
regarding tennis equipment preparation. The speaker needs to…" rather than "I
need to get my racket restrung…".

All 5 were rewritten to first person, with the transcription commentary
removed: the category's lesson is recovering intent *through* transcription
noise, not annotating the noise, and a narrative that opens by classifying
itself as "dictated notes" is describing the input rather than reorganizing
it. Fragment coverage was re-verified token-by-token for all 5 afterward —
including the garbled asterisk dictation in #96, which the meta-description
had been carrying and which now resolves in-voice ("…buy a moon filter —
asterisk"). The rewrite also caught two frame completions the new §4 rule had
not yet been applied to: "tennis" in #70 (the input says only "racket", "pro
shop", "tournament") and "freelance" in #98.

**Why no review caught it for four batches**: every check in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) items 0–5 evaluates one example against
its own `input`, and each of these narratives was individually defensible.
Convention drift is invisible to a per-example check by construction. This is
the same shape as the frame-completion blind spot found the same day — both
only appear when you look *across* examples. Added as new checklist section
6b (cross-example consistency), and the first-person rule is now pinned in
[`DATASET_SPEC.md`](../../training/DATASET_SPEC.md)'s `output` rules and in
the generation prompt template.

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
