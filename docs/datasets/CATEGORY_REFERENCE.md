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

**Narrative-voice drift — corpus-wide, found and fixed 2026-08-23.** This was
diagnosed twice and got smaller each time it was looked at properly. It was
first logged as a two-example nit in `voice_to_text_artifact`; listing that
category side by side made it look like a category problem beginning at batch
5. Scanning the whole corpus by batch showed the actual shape: **26 of 115
examples, spanning nine categories, with batch 4 affected 15/15 — every
narrative in it.** The drift originated at batch 4, not batch 5, and was never
category-specific at all. It tracks the *prompt used for a batch*, which is
why it spreads across whatever categories that batch contained.

Affected: all of batch 4 (#42–#56), #59 and #65 and #67 from batch 5, #84,
#86, #88, #90, #91 from batch 6–7, #94 and #95 from batch 7, and the five
`voice_to_text_artifact` examples fixed earlier the same day. Third-person
narration ("The author is planning a large spring vegetable garden…") and
meta-framing openers ("Notes on houseplant care…", "Brainstorming food options
for…") are the same defect in two shapes: the narrative describing the note
rather than being it.

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

The rewrite also cleared eight further defects that had gone unnoticed inside
those narratives — six frame completions ("houseplant care", "freelance work",
"kombucha brewing", "Dobsonian telescope", "bioactive terrarium", "donations
of towels"), one invented certainty (#56 asserting a coffee chat "will happen"
where the input said only "sometime soon maybe"), and one added emphasis
("The critical first step is"). Fragment coverage was re-verified
token-by-token across all 26; the only input tokens absent afterward are
ordinary normalizations (`uhaul`→"U-Haul", `idk`→"I don't know",
`tmrw`→"tomorrow").

**Why no review caught it for four batches**: every check in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) items 0–5 evaluates one example against
its own `input`, and each of these narratives was individually defensible.
Convention drift is invisible to a per-example check by construction — the
first adversarial re-review sampled 15 examples from batches 1–4 and did not
flag it. This is the same shape as the frame-completion blind spot found the
same day: both only appear when you look *across* examples. Added as new
checklist section 6b, which after this correction checks **by batch first**
and by category second — the earlier version had the axis wrong, which is what
made the first diagnosis undercount the problem by a factor of five. The
first-person rule is pinned in
[`DATASET_SPEC.md`](../../training/DATASET_SPEC.md)'s `output` rules and in the
generation prompt template.

**Also corrected 2026-08-23**: `minimal_fragment` #65 relabeled
`expert`→`medium`. A 9-word, two-fragment note cannot satisfy the `expert`
tier's "dense combination of categories, longer note, more state to hold";
comparable 6-word notes in the same category are labeled `medium`. This is the
same instruction conflict as `topic_switching` in batch 8 — a global
difficulty skew applied to a category whose definition resists it — and the
batch 9 prompt now bars `minimal_fragment` from `expert` explicitly.

## Depth by category (running total, after batch 9)

Batch 9 (16 requested, 15 accepted, 1 rejected, 6 fixed) cleared every
category that was sitting at the depth floor of 7. Depth is now banded 8-9
across all 15 categories, the tightest the corpus has ever been, and category
coverage is no longer a meaningful targeting axis at all.

`contradictory_statement` (8), `long_rambling` (8), `minimal_fragment` (8),
`topic_interleaving` (8), `voice_to_text_artifact` (8), `dangling_reference`
(9), `interrupted_thought` (9), `multi_person_note` (9), `rapid_branching`
(9), `repeated_reminder` (9), `self_correction` (9), `simple_list` (9),
`time_ambiguous` (9), `topic_switching` (9), `zero_action_items` (9).

**Difficulty distribution, full corpus**: easy 23, medium 41, hard 40,
expert 26 (130 total). Hard has effectively caught medium.

**First batch to assign difficulty per category instead of as a batch-wide
skew.** This followed directly from batch 8's finding that a global
hard/expert push can structurally contradict a category's own definition.
Pulling the per-category difficulty breakdown for the first time showed the
corpus-wide "medium leads" framing had been misleading: the imbalance is
substantially structural, because some categories are intrinsically low
difficulty (`simple_list` was easy 6 / medium 1) and others intrinsically
high (`long_rambling` was expert 6 / medium 1). Asking every batch to skew
hard was therefore asking several categories to become something they aren't.
Batch 9 instead asked each category for the tier it was actually missing —
`rapid_branching` at medium (it had no low end at all), `long_rambling` at
hard (it was nearly all expert) — and returned 16/16 on category *and*
difficulty, which no prior batch had managed.

**The main lesson from batch 9 is about prompt design, not the examples.**
It ran the most heavily constrained prompt yet, seven distinct rule blocks,
and bought that perfect compliance at a visible cost in realism. Several
inputs read as engineered to demonstrate a category rather than as something
a person actually typed: two adjacent sentences manufacturing a contradiction
with no reason a writer would produce them, five restatements of "email Dave"
in one short note, bare comma-separated lists with none of the mess that
defines the `input` field. A corpus of engineered notes trains a model that
works on engineered notes. **Batch 10 should state fewer rules more briefly
and add an explicit realism requirement** — the rules are now in
`DATASET_SPEC.md`'s template and don't all need restating inline.

**The voice drift returned in a new surface form.** Two
`contradictory_statement` examples narrated the act of writing — "I noted that
the dog needs half a scoop... but I also wrote..." — which is first person and
therefore passed the rule as written, while still describing the note rather
than being it. It appeared only in that category, where presenting two
conflicting statements creates pressure to narrate the conflict rather than
simply state both halves. The regression pattern in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §6b has been widened to catch "I
noted / I wrote / I stated" alongside the third-person forms.

Running that widened pattern over the existing corpus immediately found #77,
a `multi_person_note` example whose *previous* fix — applied by the second
adversarial re-review, which had correctly caught it silently resolving the
ambiguous conditional "I'll do it if Greg doesn't" — had introduced this exact
meta-commentary while fixing the original defect, plus an invented causal
link. Now corrected, with the ambiguous conditional kept verbatim rather than
paraphrased. Worth noting as a general caution: **a fix applied to satisfy one
checklist item can introduce a violation of another**, and nothing in the
review process currently re-checks a corrected example against the full list.

130 accepted examples total across 9 batches
(13 + 14 + 14 + 15 + 15 + 15 + 15 + 15 + 15, less 2 rejected on review).

## Depth by category (running total, after batch 10)

Batch 10 (12 requested, 12 accepted, 0 rejected, 6 fixed) targeted the four
categories that were clustered in one or two difficulty tiers rather than the
thinnest categories, since depth is no longer the binding constraint.

`minimal_fragment` (8), `dangling_reference` (9), `interrupted_thought` (9),
`multi_person_note` (9), `rapid_branching` (9), `repeated_reminder` (9),
`self_correction` (9), `simple_list` (9), `time_ambiguous` (9),
`topic_switching` (9), `zero_action_items` (9), `contradictory_statement`
(11), `long_rambling` (11), `topic_interleaving` (11),
`voice_to_text_artifact` (11).

**Difficulty distribution, full corpus**: easy 25, medium 48, hard 42,
expert 27 (142 total).

**The exemplar experiment.** Batch 9 established that a heavily-constrained
prompt buys spec compliance at the cost of realism — its inputs read as
illustrations of categories rather than notes. Batch 10 tested the opposite
lever: roughly half the prompt length, the evidence rules compressed to a
single paragraph pointing at
[`DATASET_SPEC.md`](../../training/DATASET_SPEC.md), and five real `input`
values from the corpus shown as the standard for the field, chosen from
categories the batch was *not* generating so they would demonstrate texture
without pulling content toward themselves.

It worked on the axis it targeted. The resulting inputs are the most natural
in the corpus — tangles that are incidental and uneven rather than end to end,
which is the property batch 9's examples could not produce. The load-bearing
sentence appears to have been *"do not write a note that demonstrates its
category; write a note a person would actually type, which happens to have
that property"*, reinforced by quoting batch 9's two worst inputs back as
negative examples.

**It was a trade, not a free win.** The defect rate rose from 0.44 per example
in batch 9 to 0.58 in batch 10. Fewer stated rules meant slightly weaker rule
compliance. Worth accepting — realism cannot be recovered later by editing,
while an evidence-rule slip can — but worth tracking rather than assuming the
shorter prompt is strictly better.

**Meta-commentary appeared in a third distinct surface form**: not third
person ("The author is planning…"), not first-person reporting ("I noted
that… but I also wrote…"), but a parenthetical narrating the recording
session — "(I heard a strange noise while recording this note.)" Three
different shapes across three batches, each one appearing after the previous
shape was banned by name. The durable fix is the principle rather than the
pattern list: the narrative *is* the note rewritten, never a report about it.
The regression grep helps but will always trail the newest form.

**A defect fixed in the corpus recurred in generation.** Batch 10's #2
flattened "he said" to "I was told" — the exact defect fixed in batch 9's #3
earlier the same day. The corpus is not a feedback loop into the prompt;
nothing carries a lesson forward except writing it into `DATASET_SPEC.md` or
the prompt template. This is worth treating as a standing risk rather than a
one-off: **every fix applied only to the data will recur** unless the reason
for it also lands in the generation instructions.

**New structural gap: scenario repetition is invisible to
`check_duplicates.py`.** The batch produced a "40 gal tank setup" note and a
"the magic system is based on…" note, both scenarios the corpus already had.
Measured lexical similarity was 0.14 and 0.15 against a 0.55 threshold,
because the two versions share almost no wording — it is the *situation* that
repeats, not the phrasing. The checker is lexical by design and cannot catch
this; its own docstring already notes that embeddings would be needed for
paraphrase, and this is adjacent but distinct. Both examples were kept (two
per scenario is inside the diversity rule) and a scenario-level read is now
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §6b.

142 accepted examples total across 10 batches
(13 + 14 + 14 + 15 + 15 + 15 + 15 + 15 + 15 + 12, less 2 rejected on review).

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
