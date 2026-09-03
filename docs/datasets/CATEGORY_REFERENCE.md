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

## Fourth adversarial re-review (2026-08-23) — corpus 142 → 141

Run immediately after batch 10 per the every-2-batches cadence. 13 examples
from batches 9–10; full findings in [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log.
Result: 3 ACCEPT, 9 FIX, 1 REJECT, 4 difficulty relabels, 3 further defects
found outside the sample.

**The headline finding is about the checklist, not the data.** `narrative` had
an upper bound and no lower bound: every §4 bullet prohibits *addition*, so a
narrative that copies `input` verbatim passes the whole checklist trivially —
it invents nothing, loses nothing and smooths nothing precisely by doing
nothing. Measured input→narrative similarity had climbed from a batch 1–7 mean
of 0.50 to 0.67 across batches 8–9, with two narratives at 0.97–0.98. Ten
batches of tightening the evidence rules had made *doing less* the safe
strategy, and generation found that gradient. Now §4's "No non-recovery"
bullet, the first §4 item that is not a prohibition.

**Meta-commentary was diagnosed rather than banned again.** Three categories —
`interrupted_thought`, `contradictory_statement`, `dangling_reference` — ask
the output to represent an *absence*: a thought that stops, two claims that
can't both hold, a referent never resolved. No output field has a device for
absence, so generation describes the note instead. That is why the defect
reappeared in four successive surface forms, each after the previous was
banned by name — the pressure was never addressed. Confirmed by scan: every
meta-commentary hit in the corpus was `interrupted_thought`. Replaced with a
convention: **preserve the note's own broken-off text verbatim** (`"Print
the—"`, `"Oh look the mailman is—"`), which is the note rather than a report
about it.

**§6b was tested for the first time, vindicated, and corrected in the same
run.** It found two things per-example review cannot reach — bullet terminal
punctuation at 0% in batch 9 and 100% in batch 10 (normalized corpus-wide to
bare list items, 274 periods stripped), and the `interrupted_thought`
meta-commentary cluster. But its own bolded "check by batch first" advice was
wrong, generalized from a single incident, and would have diluted the second
finding across three batches. Batch-tracking drift is a prompt artifact;
category-tracking drift is structural pressure from what the category asks the
output to represent, spans batches, and is the more durable of the two.
Neither is primary. §6b also gained the two axes it was missing — copy ratio
and difficulty calibration — both purely comparative, the proof case being
#127 and #128: the same note with different nouns, carrying different
difficulty tiers, in the same batch.

**A sweep that looked complete was not.** The standing regression grep scanned
only `narrative`. Widening it to all three fields immediately surfaced 8
third-person bullets across 7 batch-4 records — the same drift the corpus-wide
sweep earlier the same day had reported as fully cleared. The grep now scans
the whole `output` object.

**Two §4 rules were found to contradict each other**: "every fragment must
appear somewhere" versus `voice_to_text_artifact`'s "recover through the
noise, don't annotate it". Dictation commands are both fragments and noise,
and two examples answered both ways at once. Resolved with an explicit
artifact exception — such fragments are represented by their *effect*, never
their surface text, applied uniformly within an example.

**Rejected**: #122, the dog-kibble note. Verbatim narrative (0.980), two
flatly contradictory imperatives in `action_items` that would have a user feed
a dog one and a half scoops, and no mood or intention *shift* — so it was
never `contradictory_statement` as defined. This reverses the first pass's
"borderline, keep it" call; surfaced to the product owner per the
reconciliation rule and agreed.

**Still open, deferred to the product owner**: what `action_items` should do
when a note commits to two incompatible things. The three available moves are
pick a side (invention), emit both flat (what #122 did, and actively harmful),
or describe the conflict (banned by the voice rule). The reviewer correctly
declined to invent a convention. Rejecting #122 removed the only instance, so
this is documented rather than decided — it needs settling before a note like
that recurs.

**Scenario wells already past the two-per-scenario line**, found by reading
the whole `input` column rather than the new batch: car-maintenance errands
(#48, #85, #94, #102, #132 — five) and garden/tomatoes (#6, #30, #42, #130 —
four). Worth avoiding in batches 11+.

141 accepted examples after ten batches and four adversarial re-reviews.

## Depth by category (running total, after batch 11)

Batch 11 (12 requested, 12 accepted, 0 rejected, 4 fixed) targeted the six
difficulty-tier gaps left after batch 10: `rapid_branching`,
`multi_person_note`, `time_ambiguous`, and `topic_interleaving` all had zero
`easy` examples; `simple_list` had zero `hard` or `expert`;
`contradictory_statement` had zero `expert`. First batch generated after
2026-08-23's voice sweep, spot-check fixes, and the double-review
calibration — also the first whose prompt carries the two rules that run
landed (unmarked ambiguity, no dropped imperatives).

`minimal_fragment` (8), `topic_switching` (9), `dangling_reference` (9),
`repeated_reminder` (9), `zero_action_items` (9), `self_correction` (9),
`interrupted_thought` (9), `simple_list` (11), `rapid_branching` (11),
`long_rambling` (11), `multi_person_note` (11), `time_ambiguous` (11),
`voice_to_text_artifact` (11), `contradictory_statement` (12),
`topic_interleaving` (13).

**Difficulty distribution, full corpus**: easy 34, medium 48, hard 43,
expert 28 (153 total).

**All six requested gaps closed exactly as requested** — 12/12 on category
and difficulty tier both, matching batches 9 and 10's mechanical compliance.

**Two API calls returned `503 UNAVAILABLE`** before a third succeeded — the
model was under high demand, not a problem with the prompt; the product
owner authorized a retry rather than falling back to `flash` mid-corpus.

**The telemetry `batch_starting()` checkpoint was missed** — noted here
rather than quietly dropped, per this project's standing practice of owning
process misses directly. `batch_finished()` still ran at completion; full
detail in `COST_LEDGER.md`'s new row.

**Four fixes, two of one shape**: `action_items` flattening a genuine
dependency into unconditional flat tasks ("greg will do the grocery run if
I text him a list" → two separate unconditional items) — the same fix
`#125` needed the same day, from the calibration run. One dropped fragment
(`bullets` correctly listed milk/eggs, `action_items` didn't). One
reinstated two superseded instructions in `action_items` next to the two
still-live ones — the exact contradictory-imperatives shape `#122` was
rejected for, caught this time before it reached the corpus rather than
after.

**Batch mean copy ratio (0.75) ran well above the corpus's 0.56, but mostly
for a structural reason rather than a defect one.** The four newly-covered
`easy`-tier categories sit at 0.71–0.83: an easy-tier `rapid_branching`,
`multi_person_note`, `time_ambiguous`, or `topic_interleaving` note is short
and already close to spoken order, so there's genuinely less to reorganize
— not the same failure as a longer note copying itself. The two
`contradictory_statement`/`expert` examples were the real exception: both
at 0.88, above the documented 0.85 line and not covered by the
short-input exception (dense, multi-position notes with real structure to
recover available), so both were rewritten to actually reorganize —
0.88/0.88 → 0.61/0.53. Worth watching whether `easy`-tier requests in
reorganization-heavy categories keep running structurally high; one batch
isn't enough to call it a pattern.

153 accepted examples after eleven batches and four adversarial re-reviews.

## Depth by category (running total, after batch 12)

Batch 12 (14 requested, 14 accepted, 0 rejected, 2 relabeled, 1 fixed),
same day as batch 11 — floor-raising for the 7 categories still at 8–9
after batch 11, rather than chasing a new difficulty ceiling.

`minimal_fragment` (8), `simple_list` (11), `topic_switching` (11),
`repeated_reminder` (11), `zero_action_items` (11), `self_correction`
(11), `rapid_branching` (11), `long_rambling` (11), `multi_person_note`
(11), `time_ambiguous` (11), `interrupted_thought` (11),
`voice_to_text_artifact` (11), `contradictory_statement` (12),
`topic_interleaving` (13), `dangling_reference` (13).

**Difficulty distribution, full corpus**: easy 38, medium 50, hard 48,
expert 31 (167 total).

**`minimal_fragment` is now the only category below 11, and the only one
still missing `hard`/`expert` entirely** — both requested examples were
relabeled to `dangling_reference` instead. The prompt asked for
`minimal_fragment` to reach higher difficulty "through how much ambiguity
packs into very few words," and what came back were dense conditional
decision trees with real structure — directly contradicting the
category's own "little structure" definition. Same shape as batch 8's
`topic_switching`/`expert` finding: a requested difficulty tier can
structurally contradict a category's own definition, and asking harder
doesn't fix that, a differently-shaped request does. Both relabeled rather
than rejected, since what they actually teach (preserving several
unresolved referents without guessing) is sound. Needs a future batch
with a `minimal_fragment`-specific instruction that keeps genuinely
minimal — very few words, plainly stated, no conditional branches — while
still finding a way to be hard to recover.

167 accepted examples after twelve batches and four adversarial re-reviews.

## Fifth adversarial re-review (2026-08-25) — first Gemini-first run, corpus 167 → 167

The first re-review under `PDR-006`'s 2026-08-25 amendment: Gemini reviews
first against the full 0–8 checklist, Claude second, following the
calibration run's finding that a same-family reviewer under-detects this
project's own characteristic defects. 13 examples — 7 edited or relabeled
during this session's first-pass review (the calibration's worst-case
stratum), 6 never-touched controls. Full findings in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. Result: 6 ACCEPT, 7 FIX, 0
REJECT, 3 further 6b findings (1 confirmed corpus-wide, 2 declined).

**The amendment's premise held on its second data point.** Gemini found real
defects in examples Claude's own first-pass review had cleared minutes
earlier, including a category mismatch: #153 was labelled
`contradictory_statement`, which requires an unresolved tension preserved
verbatim, but the note is a mistaken belief corrected within itself,
resolving to one consistent stance — `self_correction`'s shape. Relabeled;
Gemini's own separate reasoning about a different example (self_correction
permits narrating the pivot, unlike the three verbatim-preservation
categories) independently confirms the relabel is what makes the existing
narrative correct.

**A fix introduced a regression that a second check caught immediately.**
#163's frame-completion fix (removing an unstated "*my* basement drywall")
briefly stripped every first-person pronoun from the narrative, regressing
the exact voice defect fixed corpus-wide earlier the same day. Caught by
re-running the standing checks right after applying the fix — the first
concrete case of this section's own "re-check the full checklist, not just
the item that prompted the correction" rule doing its job in real time
rather than being cited after the fact.

**The largest finding: the field-register regression check only ever
covered one grammatical shape.** It tested for subject-led third-person
bullets ("Needs to check X") but never passive constructions with no
subject at all ("X must be checked") — a different shape entirely. Gemini's
flag on #151 ("The knock box must be emptied") exposed this, and a
corpus-wide scan found **19 lines across 18 records, spanning nearly every
category**, not confined to recent batches. All rewritten to
active/imperative, matching the register `action_items` already used
correctly throughout — the defect concentrated entirely in `bullets`. The
check itself now covers both shapes.

**#151 also lost its `expert` tag**, downgraded to `hard`: `TAXONOMY.md`
defines `expert` as a dense combination of categories with branching or
restated content, and this is a long flat enumeration with a few appended
exceptions — structurally identical to #150 (already `hard`), differing
only in raw length, which the definition doesn't credit. `simple_list` is
without an `expert` example again, the same open gap `minimal_fragment` has
for `hard`/`expert` — a third instance of the same pattern as batch 8's
`topic_switching`/`expert` conflict: a requested difficulty tier can
structurally contradict what a category is built to hold.

**Two findings read and declined, not silently dropped**: an alleged
ambiguity in #155's "wipe it" (USB vs. envelope) — declined, since "wipe"
pragmatically constrains to the USB strongly enough that the envelope isn't
a *plausible* second reading, not just an unlikely one. #157's "make sure
the slide deck has the updated margins" read as verification rather than
authoring — declined as ordinary inference for someone presenting their own
deck. A third claim, that domestic-chore and grocery themes recurring
across examples signals scenario-well over-reliance, was declined outright
— the flagged examples don't share an actual situation, only a broad
household-task theme, which doesn't meet this project's established
narrow definition of a scenario well.

167 accepted examples after twelve batches and five adversarial re-reviews.

## Depth by category (running total, after batch 13)

Batch 13 (18 requested, 18 accepted, 0 rejected, 2 relabeled, 3 fixed) —
first batch generated under `TAXONOMY.md`'s new "structural ceiling on
`expert`" principle, written up 2026-09-01 after batch 12's `minimal_fragment`
gap was the third independent instance of the same finding. Targeted
`minimal_fragment` (the last category below 11, missing `hard`/`expert`
entirely) with a differently-shaped instruction — ambiguity density in very
few words, explicit ban on if/then branching — rather than another plain
retry at higher difficulty.

`topic_switching` (11), `contradictory_statement` (11), `dangling_reference`
(14), `interrupted_thought` (12), `long_rambling` (12), `minimal_fragment`
(12), `multi_person_note` (12), `rapid_branching` (12), `repeated_reminder`
(12), `self_correction` (14), `simple_list` (14), `time_ambiguous` (12),
`topic_interleaving` (13), `voice_to_text_artifact` (12),
`zero_action_items` (12).

**Difficulty distribution, full corpus**: easy 39, medium 55, hard 59,
expert 32 (185 total).

**The ceiling-aware instruction worked on the first attempt.** All 4
`minimal_fragment` examples came back genuinely thin — one line, no
conditional structure — with the difficulty carried entirely in unstated
referents ("the blue one", "the other middle one", "the last batch"). No
relabel needed; the category's last open gap is closed. `simple_list`'s 3
new `hard` examples similarly stayed flat lists with a genuine wrinkle
(a restated item, an ambiguous entry) rather than accreting branching
structure toward `expert` — consistent with the same principle's `hard`
cap for this category.

**Two relabels, both category mismatches this project has hit before.**
A paint-color note requested as `topic_switching` returns to its original
subject after an oven-related aside — the textbook `interrupted_thought`
shape (cut off, resumed), not a permanent switch. A meeting-time note
requested as `contradictory_statement` resolves to one consistent final
stance (2pm, after briefly considering 3pm) rather than preserving an
unresolved tension — the same `contradictory_statement`-vs-`self_correction`
mismatch the fifth adversarial re-review found in `#153` five days earlier,
this time in fresh generation rather than legacy data. Both relabeled
rather than rejected; both examples otherwise sound.

**Three fixes, one repeating a defect fixed corpus-wide five days
earlier.** One `simple_list` example listed a restated item ("grab
measuring tape" / "grab measuring tape again but the long one") as two
separate bullets/action_items instead of merging per the repeated-item
convention. One `simple_list` example's `bullets` merged a restated errand
("buy caffeine" / "get coffee again") into one line while `action_items`
kept it as two — a `bullets`/`action_items` disagreement on the same
fragment, a §4 "fields must agree" violation. Most notable: a
`rapid_branching` example's bullets used the passive "`X` needs to be
`Y`-ed" shape (`"the guest room needs to be cleared out"`, `"Jamie needs
to be asked..."`) — the exact pattern the fifth re-review had corpus-wide
fixed five days earlier. **Confirms the standing warning not to assume one
fix means a shape can't reappear in fresh generation** — the fix lives in
the corpus, not in the prompt, so nothing prevented it recurring. Both
bullets rewritten to active voice; the full three-check voice-regression
suite re-run afterward, 0/185 clean.

No near-duplicates (`check_duplicates.py` run against the full 185-record
corpus), no scenario-well repetition, no mojibake.

185 accepted examples after thirteen batches and five adversarial
re-reviews. Next periodic adversarial re-review due after batch 14.

## Depth by category (running total, after batch 14)

Batch 14 (18 requested, 18 accepted, 0 rejected, 2 relabeled, 3 fixed)
targeted `topic_switching` and `contradictory_statement`, tied at the
depth floor (11) after batch 13, each with an explicit contrastive-
definition instruction rather than a plain re-request.

`minimal_fragment` (12), `rapid_branching` (12), `interrupted_thought`
(13), `multi_person_note` (13), `repeated_reminder` (13), `time_ambiguous`
(13), `voice_to_text_artifact` (13), `zero_action_items` (13),
`contradictory_statement` (14), `long_rambling` (14), `simple_list` (14),
`topic_switching` (14), `dangling_reference` (15), `self_correction` (15),
`topic_interleaving` (15).

**Difficulty distribution, full corpus**: easy 40, medium 61, hard 64,
expert 38 (203 total).

**Both contrastive-definition instructions worked cleanly on the first
attempt.** All 3 `topic_switching` examples came back strict A-A-B with
exactly one transition and zero returns to the first subject, capped at
easy/medium as instructed — no relabels needed, unlike batches 6 and 7's
repeated failures on this exact category. All 3 `contradictory_statement`
examples genuinely stayed unresolved at the end (no closing "let's just go
with X"), correctly distinct from `self_correction` — this is the same
defect batch 13 found recurring in fresh generation days after the fifth
re-review fixed a legacy instance of it, and the explicit "the note must
stay split, not resolve" instruction held on the first retry.

**Two relabels, unrelated to the two targeted categories.** A
`dangling_reference` example requested at `expert` was a short flat list
(four unrelated errands) with one embedded unresolved reference — no
dense or branching combination, matching the same structural-ceiling
principle already applied to `minimal_fragment`/`simple_list`; downgraded
to `hard`. A `rapid_branching` example was actually a flat dump of
unrelated meeting-note facts (hero image, logo size, server migration,
copywriter, vendor, a cancelled meeting) with no idea spawning the next —
`long_rambling`'s shape (many small points, none load-bearing), not this
category's (one idea branching into related sub-ideas); relabeled.

**Three fixes.** A `multi_person_note` example had a stated third-party
commitment ("David said he would pay for the drinks") sitting in
`bullets` but missing from `action_items` — the ownership-rule
dropped-commitment failure mode named in `REVIEW_GUIDE.md` §4, added. A
`zero_action_items` example was tagged `hard` for a note with no genuine
ambiguity or near-miss task language anywhere in it — nothing a reviewer
could plausibly have mistaken for a task — downgraded to `medium`. An
`interrupted_thought` example elevated a real-time in-scene request
("honey, get the door") into two forward-looking `action_items`; it's an
already-resolved momentary aside captured mid-dictation, the same class as
"Dr. Patel called" (a past event, not a forward commitment) — removed
from `action_items`, kept in `bullets` where the interruption itself is
already represented.

No near-duplicates, no scenario-well repetition, no voice/meta-commentary
regressions (0/203 on the full three-check suite, re-run after fixes).

203 accepted examples after fourteen batches and five adversarial
re-reviews. Periodic adversarial re-review now due, per the
every-2-batches cadence.

## Sixth adversarial re-review (2026-09-01) — corpus 203 → 203

Due after batch 14. 14 examples: 10 touched (relabeled or fixed) during
batches 13-14's own first-pass review, 4 never-touched controls. Gemini
reviewed first against the full checklist, then a genuinely fresh Claude
subagent — spawned with no exposure to this session's reasoning — as the
independent second pass, per `PDR-006`'s amendment. Full findings in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. Result: 7 confirmed fixes, 0
relabels, several claims from each reviewer declined after reconciliation.

**The two passes disagreed on 6 of 14 examples, and the disagreement
itself is what surfaced the real defects — this run's whole point.**
Gemini flagged 11 of 14, including two claims that contradicted this
project's own settled precedent: extending the verbatim-preservation
"representing an absence" convention to `self_correction` (already
excluded by the fifth re-review's own finding), and flagging gerund
bullets like "Feeling tired of X" as a register violation when that shape
is the corpus's sanctioned convention, not one of the two actually-banned
shapes. The fresh Claude pass, given the same checklist with those two
boundaries stated explicitly, held the line on both — the value of
stating settled precedent in the prompt rather than assuming a reviewer
has absorbed project history it never saw.

**Confirmed by both passes:** a `simple_list` example silently merged two
distinct fragments ("buy caffeine" / "get coffee again") into one item
across both `bullets` and `action_items`, asserting an equivalence
`input` never states — reverted to two separate items. A
`multi_person_note` example flattened "David said he would pay for the
drinks" into the flat action item "David to pay for the drinks," dropping
the reported-speech hedge — restored. A `long_rambling` example opened
with "These are my notes from the website redesign meeting" — the exact
banned meta-framing shape this file's history already named — rewritten,
and the standing regression regex widened to catch this phrase going
forward. An `interrupted_thought` example inferred "my partner" from the
input's bare "honey" — the same class of violation as "sleeping bag" →
"camping trip" — reverted to the input's own word.

**Confirmed by one pass alone, and held up on inspection anyway** — the
reconciliation step doing real work, not just averaging two votes. The
fresh Claude pass alone caught a `self_correction` example whose narrative
dropped an entire stated fragment: the input gives two separate objections
to 2pm (an unstated one — "actually 2pm is no good" — and a stated one —
"3pm conflicts with the all-hands"), and the output kept only the second,
erasing that the first was ever raised; restored as its own bullet. The
fresh Claude pass alone also caught a `rapid_branching`/`expert` example
that was a single mechanism (nested conditionals) with nothing genuinely
combined from a second category — precisely the "structural ceiling on
`expert`" principle this session wrote into `TAXONOMY.md` two batches
earlier, independently re-derived by a reviewer who never saw that
write-up; downgraded to `hard`.

**One finding needed real judgment, not a mechanical fix.** A
`contradictory_statement` example has a genuinely ambiguous "them" (Japan
flights or hotels, both recently mentioned) that the original output
silently resolved to hotels, while `action_items` dropped the stated
flight-booking intent without ever contradicting it. This is the same
still-open question the fourth adversarial re-review left for the product
owner — what `action_items` should do when a note's own ending swallows
an earlier intent into unresolved indecision with no explicit retraction.
Resolved narrowly for this one instance (kept "them" genuinely ambiguous,
left `action_items` at the note's actual behavioral outcome) without
generalizing a rule, matching that question's own disposition.

**One finding read and left undecided.** Both reviewers independently
flagged the same `interrupted_thought` example (paint color / oven-check
aside / return to paint) on different grounds — Gemini on voice, the
fresh pass on category fit, since nothing in it is literally cut off
mid-clause the way the category's own worked example is. Neither specific
complaint held up alone, and no better-fitting category exists among the
15 for "a fully-resolved aside interrupts, then the note returns to the
original point" — but two independent reviewers flagging the same record
for different reasons is itself the disagreement-is-the-signal pattern
this process exists to catch. Recorded as a borderline case worth
watching, not relabeled.

Full three-check voice-regression suite, schema validation, and duplicate
check all clean at 203/203 after the 7 fixes. No rejections, no relabels
— every fix applied in place. 203 accepted examples after fourteen
batches and six adversarial re-reviews. Next periodic re-review due after
batch 16.

## Depth by category (running total, after batch 15)

Batch 15 (18 requested, 18 accepted, 0 rejected, 2 relabeled, 1 fixed)
targeted `rapid_branching` and `minimal_fragment`, tied at the depth floor
(12) after batch 14.

`voice_to_text_artifact` (13), `contradictory_statement` (14),
`interrupted_thought` (14), `multi_person_note` (14), `repeated_reminder`
(14), `simple_list` (14), `time_ambiguous` (14), `topic_switching` (14),
`long_rambling` (15), `minimal_fragment` (15), `topic_interleaving` (16),
`rapid_branching` (16), `dangling_reference` (17), `self_correction` (17).

**Difficulty distribution, full corpus**: easy 41, medium 65, hard 72,
expert 43 (221 total).

**The `rapid_branching`/`expert` instruction worked immediately** —
requested with the exact "genuine second-category combination, not
branching alone" wording the sixth re-review's fresh-Claude pass had
independently re-derived hours earlier. The one `expert`-tagged example
combined branching with a second person's input, a hedge, and an
unresolved venue decision; the other 3 stayed correctly capped at
medium/hard as single-mechanism branching chains, with no over-claim.

**Two relabels, one repeating a known failure mode.** A `minimal_fragment`
example ("buy the grey one for him not the big one unless it's on sale")
included a conditional ("unless") despite the prompt explicitly barring
branching structure for this category — the same mistake batch 12 made;
relabeled to `dangling_reference`, whose actual lesson (multiple
genuinely unresolved referents — which grey one, which big one) is what
the example teaches. A Chicago-packing note requested as
`contradictory_statement` resolved cleanly on every point it raised
(light jackets over heavy coats, blue sweater over green) with nothing
left unresolved at the end — the **fourth** instance of this exact
category-vs-`self_correction` mismatch this project has hit (see the
fifth and sixth re-review logs, plus batch 13); relabeled.

**One fix, applying a principle within hours of it being confirmed.** An
`interrupted_thought` example (Q3 goals document drafting cleanly
interrupted by a finished laundry cycle, then explicitly resumed) was
tagged `expert` for what is structurally a single clean
interruption-and-resume mechanism with nothing else genuinely combined —
downgraded to `hard`, the same call the sixth re-review's fresh-Claude
pass made on a different record the same day.

Full voice-regression suite, schema validation, and duplicate check clean
at 221/221 after fixes. No scenario-well repetition; car-maintenance,
garden, dentist, and budget-spreadsheet scenarios also excluded this
round as newly well-represented.

221 accepted examples after fifteen batches and six adversarial
re-reviews.

## Depth by category (running total, after batch 16)

Batch 16 (18 requested, 18 accepted, 0 rejected, 3 relabeled, 1 fixed)
targeted `voice_to_text_artifact`, the sole category at the depth floor
(13) after batch 15, with each of the 5 requested examples using a
genuinely different transcription-layer artifact type rather than
repeating one shape.

`topic_switching` (14), `contradictory_statement` (15), `interrupted_thought`
(15), `multi_person_note` (15), `repeated_reminder` (15), `simple_list`
(15), `time_ambiguous` (15), `zero_action_items` (15), `minimal_fragment`
(15), `long_rambling` (16), `rapid_branching` (17), `dangling_reference`
(18), `self_correction` (18), `topic_interleaving` (18),
`voice_to_text_artifact` (18).

**Difficulty distribution, full corpus**: easy 42, medium 69, hard 80,
expert 48 (239 total).

**This batch's prompt carried three category-specific traps as explicit
standing instructions for the first time, rather than only fixing them
after the fact** — and all three held. `contradictory_statement` and
`interrupted_thought` both came back correctly shaped, with no repeat of
the mismatches found in batches 13-15. `voice_to_text_artifact` hit its
target exactly: 5 examples, 5 genuinely distinct artifact types
(mishearing, run-on, filler words, a spoken self-correction, and a
mishearing combined with a hedge and conditional for the one `expert`
example), closing the last open depth gap.

**Three relabels, one a category-fit issue and two the now-familiar
`expert` over-claim.** A `topic_switching` example was structurally
A-B-A (pottery class → passport reminder → a return to pottery detail) —
a real return to the first subject, which this category's own zero-returns
definition (settled at batch 8) rules out; relabeled to
`topic_interleaving`. Two `expert`-tagged examples — a `self_correction`
built on a single paint-color pivot, and a `topic_interleaving` built on
two flat threads with nothing else combined in — were each a single
mechanism, however elaborate; downgraded to `hard`, the same principle
the sixth re-review's fresh-Claude pass surfaced and batch 15 first
applied, now caught within the same batch that stated it as an explicit
prompt instruction rather than discovered after the fact.

**One fix**: a `voice_to_text_artifact` bullet ("Asking Sarah if the
sitting times need to be adjusted") tripped the passive-voice regression
check via an embedded subordinate clause — not the blatant
subjectless-passive shape the check was written for, but rephrased
anyway rather than arguing the check's judgment case-by-case.

Full voice-regression suite, schema validation, and duplicate check clean
at 239/239 after fixes. No scenario-well repetition.

239 accepted examples after sixteen batches and six adversarial
re-reviews. Periodic adversarial re-review due, per the every-2-batches
cadence.

## Seventh adversarial re-review (2026-09-01) — corpus 239 → 239

Due after batch 16. 13 examples: 7 touched (relabeled or fixed) during
batches 15-16's own first-pass review, 6 never-touched controls. Gemini
first, then a genuinely fresh Claude subagent as the independent second
pass, per `PDR-006`'s amendment. Gemini's API returned three consecutive
`503`/fetch errors before a fourth attempt succeeded. Full findings in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. Result: 3 confirmed fixes, 0
relabels.

**Gemini ran hot in a specific, identifiable way this run**: it flagged
ordinary causal connectives ("so", "since", "because") as invented
causality in 7 of 13 examples, even where the input's own text already
stated that exact reasoning ("it's basically empty right now" as the
stated reason for buying more flour). The "no invented causality" rule
targets asserting a relationship between genuinely unrelated fragments —
adjacency between two facts already part of the same stated thought isn't
the violation it exists to catch. The fresh Claude pass, given the same
checklist with that boundary stated explicitly, independently reached the
same accept/fix split on all but one soft note — a clean instance of a
reviewer extending a real rule past its documented scope at volume,
caught by the second independent pass rather than compounding into the
corpus.

**The 3 fixes both passes converged on, separate from the causality
noise, were all real.** A `self_correction` example (Chicago packing, two
coat/sweater pivots) was tagged `expert` for a single mechanism run
twice — made sharper this time because another record in the *same
13-example sample* (a paint-color pivot) is the identical category at the
identical complexity and was already correctly capped at `hard`, making
the inconsistency directly comparable within one small sample rather than
needing corpus-wide memory. Downgraded to `hard`. An `interrupted_thought`
example (Q3 goals document, literal `"by--"` mid-clause cutoff) had its
broken-off text smoothed into a complete sentence in every field — the
exact case the "representing an absence" convention exists to prevent,
missed during first-pass review because the causal story (laundry
interrupting drafting) reads as obviously recovered even though the
literal broken text never survives anywhere. Fixed by preserving `"by--"`
verbatim. A `topic_interleaving` example (gym membership / quarterly
report) narrated `"For work, I need to draft the quarterly report..."` —
a domain label `input` never states, matching this project's own worked
example of a banned inference almost verbatim, missed during first-pass
review despite being the clearest defect in the sample by both reviewers'
independent read. Fixed by removing the frame.

Full three-check voice-regression suite, schema validation, and duplicate
check clean at 239/239 after the 3 fixes. No rejections, no relabels —
every fix applied in place. 239 accepted examples after sixteen batches
and seven adversarial re-reviews. Next periodic re-review due after
batch 18.

## Depth by category (running total, after batch 17)

Batch 17 (18 requested, 18 accepted, 0 rejected, 0 relabeled, corpus-wide
capitalization fix applied) targeted `topic_switching`, the sole category
at the depth floor (14), and `easy` difficulty, the thinnest tier
corpus-wide after several expert-weighted batches.

`contradictory_statement` (16), `interrupted_thought` (16),
`minimal_fragment` (16), `multi_person_note` (16), `repeated_reminder`
(16), `simple_list` (16), `time_ambiguous` (16), `zero_action_items`
(16), `long_rambling` (17), `rapid_branching` (17), `dangling_reference`
(19), `self_correction` (19), `topic_interleaving` (19), `topic_switching`
(19), `voice_to_text_artifact` (19).

**Difficulty distribution, full corpus**: easy 48, medium 75, hard 85,
expert 49 (257 total).

**First batch this session with a completely clean category/difficulty
read on first-pass review — zero relabels.** All four standing traps
(topic_switching zero-returns/no-expert, contradictory_statement must end
unresolved, interrupted_thought needs a preserved verbatim cutoff, expert
requires named cross-category combination) held without exception. All 5
`topic_switching` examples came back strict single-transition/zero-return,
correctly capped, with 2 genuinely `easy`. The `interrupted_thought`
example's literal dash cutoff ("I can't do the --") survived verbatim in
every field — the exact gap the sixth and seventh re-reviews found
missing elsewhere, now correctly applied at generation time.

**The real finding this batch was structural, not content-level, and it
reached backward into the existing corpus rather than staying contained
to the new batch.** Reading the batch's `action_items` column found
nearly every entry started lowercase against the corpus's established
capitalized convention — a fresh batch-tracking drift, fixed before
acceptance. Checking whether the same shape already existed elsewhere in
the corpus (the standing lesson: a detector gap is rarely confined to
where it was first noticed) found **7 pre-existing records with the
identical pattern, apparently dating to early batches and invisible to
every prior review pass because no check for it existed until this
session built one**. One of the 7 was `#151`, the "knock box" record the
fifth re-review fixed for passive voice — that fix corrected the
grammar but never re-capitalized the result, so the defect had been
sitting one layer beneath an already-applied fix. All 7 corrected. One
lowercase entry was deliberately left alone: `#167`'s bullet preserves an
interruption verbatim in the input's own lowercase, run-on style, per the
absence-representation convention — capitalizing it would have broken
the very rule it satisfies, confirmed by checking the record's `input`
before treating it as a defect rather than assuming the pattern-match
was automatically right.

Full voice-regression suite, schema validation, and duplicate check clean
at 257/257. No scenario-well repetition.

257 accepted examples after seventeen batches and seven adversarial
re-reviews.

## Depth by category (running total, after batch 18)

Batch 18 (18 requested, 18 accepted, 0 rejected, 0 relabeled, 1 systemic
fix across 3 records) targeted all 8 categories tied at the depth floor
(16) after batch 17, exactly 2 examples each, weighted overall toward
easy/medium difficulty.

`long_rambling` (17), `rapid_branching` (17), `contradictory_statement`
(18), `interrupted_thought` (18), `minimal_fragment` (18),
`multi_person_note` (18), `repeated_reminder` (18), `simple_list` (18),
`time_ambiguous` (18), `zero_action_items` (18), `topic_switching` (19),
`dangling_reference` (19), `self_correction` (19), `topic_interleaving`
(20), `voice_to_text_artifact` (20).

**Difficulty distribution, full corpus**: easy 52, medium 83, hard 90,
expert 50 (275 total).

**Exact category-count compliance and correct capitalization
throughout** — the explicit capitalization instruction added after
batch 17's discovery held cleanly, with one correct, deliberate
exception: a verbatim-preserved interruption kept its original lowercase,
matching the absence-representation convention rather than breaking it.

**The one real finding was a first-person-voice gap in bare, verb-less
fragments, not a repeat of prior meta-commentary drift.** Two
`minimal_fragment` examples ("cat food chicken flavor", "jennifer's old
scarf") and one `zero_action_items` example (a third-person
creative-writing critique with no personal referent at all) produced
narratives with zero first-person pronoun. This is the genuine edge case
the standing check's "essentially always contains a first-person
pronoun" phrasing already anticipated — an input with no verb and no
personal referent has nothing for a faithful recovery to attach a
pronoun to without inventing one. Fixed with minimal, non-inventive
framing that adds only the implicit personal frame every such note
carries ("I need cat food in chicken flavor"; "Jennifer's old scarf is
on my mind"; "I think the protagonist's motivation feels a bit weak..."),
not a specific action or reason the input never stated.

Full voice-regression suite, schema validation, and duplicate check
clean at 275/275 after fixes. Noted, not actioned: "streaming
subscription cancellation" (batches 17-18) and "quarterly report due
Friday" (batches 16, 18) are each now at 2 instances — within the
diversity rule's tolerance, but at the line; avoid both in future
batches.

275 accepted examples after eighteen batches and seven adversarial
re-reviews. Periodic adversarial re-review due, per the every-2-batches
cadence.

## Eighth adversarial re-review (2026-09-01) — corpus 275 → 275

Due after batch 18. 13 examples: 7 touched (relabeled/fixed) during
batches 17-18's own first-pass review, 6 never-touched controls. Gemini
first, then a genuinely fresh Claude subagent as the independent second
pass, per `PDR-006`'s amendment. Full findings in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. Result: 2 confirmed fixes
from the formal sample, plus 10 corpus-wide fixes from a self-directed
catch before the sample was even sent out.

**A pre-review catch found a corpus-wide gap in the standing passive-voice
check itself.** The fifth re-review's check (2026-08-25) only matched
regular `-ed` past participles ("X must be checked"); an irregular
participle ("X must be told/given/drawn/sent/found/written...") is the
identical passive-with-no-actor shape in different verb morphology, and
slipped through entirely. A corpus-wide scan found **10 lines across 10
records, spanning nearly every category, some dating to early batches** —
the same "detector enumerates a shape instead of testing the underlying
pattern" mechanism as the original discovery. All 10 rewritten to active
voice; the standing check widened to cover both participle types in one
pattern.

**The formal sample produced the widest Gemini/fresh-Claude divergence of
any re-review so far, and it was entirely Gemini overreach.** Gemini
flagged 4 of 13 examples, 2 at REJECT severity; the fresh pass
independently declined all 4: extending the banned-bullet-shape rule to
ordinary declarative sentences with explicit subjects that match neither
documented shape; misreading a stative sentence ("mopping is left for the
morning crew") as a modal-passive obligation, which requires the literal
verb "be" the sentence doesn't have; claiming a `voice_to_text_artifact`
example lost content by not keeping "comma"/"period" as literal text —
directly contradicting this project's own documented noise-exception for
that category, traced to an incomplete checklist this session's own
review prompt sent to Gemini rather than a new Gemini failure mode; and
calling a correctly-unattributed action item ("someone needs to email the
prof") wrongly assigned.

**Both passes agreed on two real, different findings.** A
`topic_switching` example (vacuum the stairs / clean the sink / order pet
food) is actually three independent, unrelated items — A-B-C, not a
coherent two-subject A-A-B transition — relabeled to `simple_list` rather
than stretching the category's own strict definition to fit, a call this
session had left as a defensible-but-borderline stretch back in batch 17.
A `long_rambling`/`expert` example (three hours staring at a canvas, one
item mentioned twice) was tagged `expert` for what both reviewers
concluded is a single mechanism — rambling drift and internal repetition
are native to *how the category works*, not a second structure layered
on top — downgraded to `hard`.

**Explicitly confirmed rather than merely accepted**: a
`voice_to_text_artifact`/`expert` example was specifically re-examined
per this session's own request, and both of its component mechanisms (a
destination self-correction correctly treated as transcription noise; a
drive-vs-fly deliberation correctly treated as real, preserved content)
verified as genuinely distinct and handled differently — the difficulty
tag holds, unlike the canvas example carrying the same nominal tag for a
shallower reason.

Full three-check voice-regression suite (now including the widened
passive check), schema validation, and duplicate check clean at 275/275
after all 12 fixes this round. No rejections — every fix applied in
place. 275 accepted examples after eighteen batches and eight adversarial
re-reviews. Next periodic re-review due after batch 20.

## Depth by category (running total, after batch 19)

Batch 19 (25 requested, 25 accepted, 0 rejected, 0 relabeled, 0 fixes) —
first batch run at increased size (25, up from the 15-20 range this
project used since batch 1), tested after several consecutive low-defect
batches rather than assumed safe by default. Targeted `rapid_branching`
and `long_rambling`, tied at the depth floor (17).

`contradictory_statement` (19), `minimal_fragment` (19), `multi_person_note`
(19), `repeated_reminder` (19), `time_ambiguous` (19), `zero_action_items`
(19), `dangling_reference` (20), `interrupted_thought` (20), `self_correction`
(20), `simple_list` (20), `topic_switching` (20), `topic_interleaving` (21),
`voice_to_text_artifact` (21), `long_rambling` (22), `rapid_branching` (22).

**Difficulty distribution, full corpus**: easy 55, medium 93, hard 101,
expert 51 (300 total).

**The size increase produced no visible quality drop — first batch this
session with zero relabels and zero fixes of any kind.** All 5
`rapid_branching` and all 5 `long_rambling` examples came back correctly
capped at medium/hard except one `expert` each, and both `expert`
examples had a genuinely named second mechanism rather than density
alone (branching combined with a hedged third-party commitment and an
unattributed task; rambling combined with a dependent scheduling
decision). Capitalization, the ownership-hedge convention, and the
widened passive-voice check all held with no manual correction needed.

One judgment call worth recording rather than silently deciding either
way: a `minimal_fragment` example ("laundry detergent") got a filled
action item where an equivalently bare fragment in batch 18 ("cat food
chicken flavor") was left empty. Read as a genuine difference in
ambiguity — an unqualified grocery noun has essentially one plausible
reading, while a flavor-qualified one plausibly reads as either a
shopping note or a description of what's already being fed — not an
inconsistency needing correction.

Full voice-regression suite, schema validation, and duplicate check
clean at 300/300 on first pass. No scenario-well repetition.

**Recommend keeping 25 as the new standing batch size** given this
result; revisit only if a future batch's defect rate rises.

300 accepted examples after nineteen batches and eight adversarial
re-reviews.

## Depth by category (running total, after batch 20)

Batch 20 (25 requested, 25 accepted, 0 rejected, 0 relabeled, 2 fixed) —
second batch at the increased size (25) — targeted 6 categories tied at
the depth floor (19) with exactly 3 examples each, plus 7 more, and
deliberately weighted toward `expert` difficulty (the corpus's thinnest
tier) with the requirement that every `expert` example name its two
combined structural elements before being tagged.

`dangling_reference` (21), `interrupted_thought` (21), `self_correction`
(21), `simple_list` (21), `topic_switching` (21), `voice_to_text_artifact`
(21), `contradictory_statement` (22), `long_rambling` (22),
`minimal_fragment` (22), `multi_person_note` (22), `repeated_reminder`
(22), `time_ambiguous` (22), `topic_interleaving` (22), `zero_action_items`
(22), `rapid_branching` (23).

**Difficulty distribution, full corpus**: easy 57, medium 101, hard 109,
expert 58 (325 total).

**The expert-weighting instruction landed close to target (7 of 25) with
every single one carrying a genuinely nameable combination** —
`repeated_reminder` + `dangling_reference` (a repeated wool order plus an
unresolved "that other thing"), `contradictory_statement` + a second
person's conflicting input (a gecko-vs-dragon disagreement that never
resolves), `time_ambiguous` + `dangling_reference` (a vague pickup window
plus an unnamed "backing fee"), and others in the same shape. Naming the
two elements before tagging, rather than tagging on density alone,
continues to hold up as the right instruction.

**Two fixes.** A `multi_person_note`/`expert` example flattened "Dave is
supposed to bring the folding tables" (an expectation, not a settled
fact) into "Dave to bring the folding tables" in `action_items` —
restored the hedge, the same convention this session has repeatedly
reinforced and previously fixed elsewhere. A `simple_list` example's
narrative invented "For the beach day" as a frame — the input (sunscreen,
towels, cooler, sunglasses) never states "beach" anywhere, matching this
project's own canonical banned-inference example almost exactly; removed.

**Noted, not actioned**: a `topic_interleaving` example's
Python-syntax-error-on-line-42 scenario is suspiciously close to batch
19's own Python debugging example one batch earlier. Still only the
second instance, and the surrounding content diverges enough (cooking
dinner vs. a cat knocking over a glass) to stay within the diversity
rule's tolerance — but "Python debugging" / "line 42" specifically
should be excluded from future batch prompts given it recurred
immediately rather than after several batches.

Full voice-regression suite, schema validation, and duplicate check
clean at 325/325 after fixes. 325 accepted examples after twenty batches
and eight adversarial re-reviews. Periodic adversarial re-review due,
per the every-2-batches cadence.

## Ninth adversarial re-review (2026-09-01) — corpus 325 → 325

Due after batch 20. 14 examples: 2 touched (fixed) during batch 20's own
first-pass review, 12 never-touched controls, deliberately weighted
toward the batch's own `expert`-tagged examples. Gemini first, then a
genuinely fresh Claude subagent as the independent second pass, per
`PDR-006`'s amendment. Full findings in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. Result: 5 confirmed difficulty
downgrades, 7 confirmed content fixes, 0 relabels.

**The sharpest, most convergent reconciliation this project has run.**
Both passes independently found the same core defects. Both flagged the
same two inferred-frame violations, matching this project's own canonical
examples almost exactly: a `multi_person_note` narrative invented
"community" for a note that only ever said "cleanup day"; a
`topic_interleaving` narrative invented "cooking dinner" for a note that
only ever listed boiling rice, checking stove heat, and chopping onions.
Both independently found a hedge-dropping pattern spanning 4 examples —
"not sure... Tuesday or Wednesday" flattened into a bare scheduling
imperative; "maybe" dropped twice in a home-hub example; "I think I
should" dropped from a scan-the-cards action item; and a `time_ambiguous`
example's `bullets` field stating "the backing fee" as settled while its
own narrative correctly hedged "possibly" — the same defect the fifth
re-review named by title recurring in a new field, five re-reviews later.
All 7 fixed with minimal, faithful hedge restoration or frame removal.

**The two passes diverged sharply on `self_correction`, and the
divergence is instructive.** Gemini REJECTed the antique-fair-directions
example on the theory that retracted content and dictation noise must
survive somewhere in the output — directly contradicting this project's
own settled convention that `self_correction`'s entire purpose is
dropping retracted content. The fresh pass, given that exemption stated
explicitly, found the *actual* defect instead: the narrative said "exit
15, rather than 14," reintroducing the retracted number that `bullets`
and `action_items` had already correctly dropped — a genuine
field-disagreement, narrower and better-targeted than Gemini's blanket
claim. Fixed by removing the reintroduced number from the narrative
alone.

**On `expert`-difficulty calibration, the fresh pass's example-by-example
reasoning proved more reliable than either its own blanket instinct or
Gemini's.** Gemini claimed 6 examples were single-mechanism; the fresh
pass, checking each individually, confirmed only 5 (a branching note with
one incidental hedged line from a second person, the kitten rambling
note, a repeated wool order with one incidental unresolved referent, a
reptile-expo disagreement newly caught rather than previously suspected,
and the self-correction example), while explicitly defending three others
Gemini had also flagged: a `multi_person_note` combining 3+ named people
at genuinely different certainty registers (a stated fact, a reported
hedge, a stated expectation, plus an unassigned task) is exactly the
carve-out this project's own difficulty rule names for that category, not
density; a second `multi_person_note` combining a literal interruption
with mixed registers; and a `topic_interleaving` example's branching
conditional genuinely combining with the interleaving structure. 5
downgraded to `hard`, 4 confirmed as correctly `expert`.

Full three-check voice-regression suite, schema validation, and duplicate
check clean at 325/325 after all 12 fixes. No rejections, no relabels —
every fix applied in place. 325 accepted examples after twenty batches
and nine adversarial re-reviews. Next periodic re-review due after
batch 22.

## Depth by category (running total, after batch 21)

Batch 21 (25 requested, 25 accepted, 0 rejected, 1 relabeled, 3 fixed) —
third batch at size 25 — targeted 6 categories tied at the depth floor
(21) with exactly 3 examples each, plus 7 more, and folded the ninth
re-review's sharpened per-field hedge-check and named-combination
requirements directly into the prompt for the first time.

`long_rambling` (22), `time_ambiguous` (22), `contradictory_statement`
(23), `minimal_fragment` (23), `multi_person_note` (23), `repeated_reminder`
(23), `simple_list` (23), `topic_interleaving` (23), `dangling_reference`
(24), `interrupted_thought` (24), `rapid_branching` (24), `self_correction`
(24), `topic_switching` (24), `voice_to_text_artifact` (24),
`zero_action_items` (24).

**Difficulty distribution, full corpus**: easy 59, medium 108, hard 124,
expert 59 (350 total).

**The per-field hedge-preservation instruction worked cleanly across the
whole batch** — every hedge checked landed correctly inside its own
bullet/action_item, not just the narrative, the exact discipline the
ninth re-review had to enforce after the fact five separate times just
one batch earlier.

**One relabel and one difficulty downgrade, both caught during first-pass
review rather than needing a later re-review.** A `simple_list` example
(folded laundry, fed dog, wiped counters — all completed past actions,
correctly empty action_items) was actually teaching `zero_action_items`'s
specific lesson — recognizing a list-shaped note has nothing to add —
rather than `simple_list`'s baseline list-recovery lesson; relabeled. A
`rapid_branching`/`expert` career-daydream example was elaborate
branching with emotional flavor but no second nameable mechanism — the
same single-mechanism pattern the ninth re-review had just downgraded
five examples for; downgraded to `hard`.

**Two more fixes.** The duplicate checker flagged a genuine
phrasing-pattern match between a new antibiotics-reminder example and an
existing corpus record — different content (antibiotics vs. trash bins)
but the identical "don't forget to X... seriously remember the Y"
rhetorical template, matching `TAXONOMY.md`'s "same phrasing pattern"
prohibition directly even though the words themselves barely overlap;
reworded rather than declined. A `contradictory_statement` example (app
update status) had zero first-person pronoun in its narrative — genuine
content, not the documented bare-fragment exception, so a real voice
gap; fixed with minimal framing.

Full three-check voice-regression suite, schema validation, and
duplicate check clean after fixes — one remaining flagged pair confirmed
as a false positive (13% word overlap, coincidental short-sentence
structure).

350 accepted examples after twenty-one batches and nine adversarial
re-reviews.

## Depth by category (running total, after batch 22)

Batch 22 (25 requested, 25 accepted, 0 rejected, 1 relabeled, 4 fixed)
closed `long_rambling`/`time_ambiguous`, tied at the depth floor, with
exactly 4 examples each, plus 17 more, weighted toward both `easy` and
`expert` (the two tied-thinnest difficulty tiers at once, rather than one
at a time). Prompt added a pre-emptive rhetorical-template check after
batch 21's phrasing-pattern duplicate finding — no repeat this round.

`contradictory_statement` (23), `minimal_fragment` (24), `multi_person_note`
(24), `repeated_reminder` (24), `simple_list` (24), `topic_interleaving`
(24), `dangling_reference` (25), `interrupted_thought` (25), `topic_switching`
(25), `long_rambling` (26), `rapid_branching` (26), `time_ambiguous` (26),
`voice_to_text_artifact` (26), `zero_action_items` (26), `self_correction`
(27).

**Difficulty distribution, full corpus**: easy 67, medium 114, hard 131,
expert 63 (375 total).

**One relabel, the same recurring category mismatch.** A note requested
as `contradictory_statement` resolves cleanly to one settled decision
("I have to text Mark that I cannot help him") — it never stays
unresolved, which is `self_correction`'s shape instead; relabeled.

**Four fixes, three matching the exact single-mechanism pattern the
ninth re-review spent a full pass finding.** A `long_rambling`/`expert`
(passport panic) and a `self_correction`/`expert` (duck-pond sketch
correction) were each one elaborate mechanism with mood flavor but no
genuinely separate second structure, both downgraded to `hard`; a
`minimal_fragment` tagged `hard` ("need sleep now") had no actual
ambiguity at all, downgraded to `easy` to match an equivalent
already-accepted example. One hedge-drop: "I think I need to stop and
make a cup of tea" was flattened to a bare action item; restored.

**Two `expert` tags held up on inspection with real, distinct
combinations.** A `time_ambiguous` example combined its own date hedge
with a genuinely unresolved pronoun ("remind him") that has no
antecedent anywhere in the input — a real `dangling_reference` layered
on top. A `multi_person_note` hit the category's specific 3+-person
mixed-certainty carve-out exactly: a self-hedge, a firm assertion, and a
reported hedge, three different registers in one note.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 375/375 after fixes (the one remaining flagged
pair is the already-confirmed false positive from batch 21).

375 accepted examples after twenty-two batches and nine adversarial
re-reviews. Periodic adversarial re-review due, per the every-2-batches
cadence.

## Depth by category (running total, after batch 23)

Batch 23 (25 requested, 25 accepted, 0 rejected, 0 relabeled, 4 fixed) —
first batch since the tenth re-review's billing interruption, run on the
exact pre-drafted targeting: `topic_switching`/`expert` x6 (via a second
category's mechanism layered on the strict A-then-B switch — time
ambiguity, a repeated reminder, or multiple people's commitments), and
`zero_action_items`/`expert` x5 (via a second category's structure around
a genuinely empty task list — topic interleaving, several people
mentioned with no one committing, or extended reflection), closing both
categories' `expert` gaps from zero and one respectively. Also
`contradictory_statement`/`easy` x3 and `long_rambling`/`easy` x3,
padding both categories' thinnest tier. Remaining 8 free mix. Prompt
carried the new invented-emotional-content rule from the tenth re-review
for the first time.

`multi_person_note` (24), `topic_interleaving` (24), `minimal_fragment`
(25), `repeated_reminder` (25), `simple_list` (25), `contradictory_statement`
(26), `dangling_reference` (26), `interrupted_thought` (26),
`self_correction` (27), `rapid_branching` (27), `time_ambiguous` (27),
`voice_to_text_artifact` (27), `long_rambling` (29), `topic_switching`
(31), `zero_action_items` (31).

**Difficulty distribution, full corpus**: easy 75, medium 117, hard 136,
expert 72 (400 total).

**Four fixes found on this session's own first-pass review, before any
periodic re-review touched the batch.** One `topic_switching`/`expert`
example ("Q3 slide deck" / walk) returned to the original subject
("shouldn't leave Marcus hanging") after switching to the second topic —
violates the category's own zero-returns definition (settled at batch
8); the returning line was removed rather than relabeling, since the
rest of the example is a clean A-then-B switch combined with a genuine
contradictory-tension mechanism. Two invented-causality fixes, both the
same shape: a `topic_switching` example ("thaw the chicken" / concert
tickets) added "since" linking two facts the input states only as
adjacent, no causal word present ("clean the lint trap. the dryer takes
two cycles now."); a `zero_action_items` example (Dana/Kevin/Maya) added
"because" linking Kevin's doubt to the client's timeline questions, same
adjacency-as-causation pattern. Both de-linked back to the input's own
plain adjacency. One cross-field fix: a `contradictory_statement`/`easy`
example (old tablet, sell-vs-keep) had `action_items` listing "Sell my
old tablet online" as a firm task while the narrative correctly ends on
unresolved indecision — `action_items` reinstating what the ending
retracts, the exact cross-check violation the generation prompt's own
rules name directly; removed, leaving only "Decide if I want to get rid
of it."

**No new near-duplicates.** The duplicate checker's one flagged pair
(0.57) is both pre-existing corpus lines (#205, #343), unrelated to this
batch.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 400/400 after fixes.

400 accepted examples after twenty-three batches and ten adversarial
re-reviews. Periodic adversarial re-review due after batch 24, per the
every-2-batches cadence.

## Depth by category (running total, after batch 24)

Batch 24 (25 requested, 25 accepted, 0 rejected, 0 relabeled, 1 fixed) —
closed the depth floor, `topic_interleaving` and `multi_person_note`
(both tied at 24), with exactly 5 examples each, weighted 3 `easy`/2
`medium` per category to also close their local `easy` gap (both sat at
2 `easy` — the same tier thinnest corpus-wide at 75/425 before this
batch). Remaining 15 free mix, weighted toward `easy` generally across
`rapid_branching`, `voice_to_text_artifact`, `topic_switching`,
`long_rambling`, `dangling_reference`, `contradictory_statement`,
`self_correction`, `repeated_reminder`, `time_ambiguous`.

`simple_list` (25), `minimal_fragment` (26), `repeated_reminder` (26),
`contradictory_statement` (27), `interrupted_thought` (27),
`dangling_reference` (28), `rapid_branching` (28), `voice_to_text_artifact`
(28), `long_rambling` (30), `multi_person_note` (29), `self_correction`
(29), `time_ambiguous` (29), `topic_interleaving` (29), `topic_switching`
(32), `zero_action_items` (32).

**Difficulty distribution, full corpus**: easy 93, medium 124, hard 136,
expert 72 (425 total).

**One fix, found on this session's own first-pass review.** A
`repeated_reminder`/`easy` example ("wash the guest towels seriously
wash the guest towels today") collapsed the input's two distinct
restatements into a single bullet and a single action item — losing the
exact repetition this category exists to teach, and inconsistent with
every prior `repeated_reminder` example (including batch 23's landlord
one), which kept each restatement as its own separate item. Split back
into two bullets and two action items, matching the standing convention.

**No new near-duplicates.** The duplicate checker's one flagged pair
(0.57) is the same pre-existing corpus lines (#205, #343) flagged since
batch 21, unrelated to this batch.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 425/425 after the fix.

425 accepted examples after twenty-four batches and ten adversarial
re-reviews. Periodic adversarial re-review due now, per the
every-2-batches cadence.

## Tenth adversarial re-review (2026-09-01) — corpus 375 → 375

Due after batch 22. 14 examples: 9 touched (relabeled/fixed) during
batches 21-22's own first-pass review, 5 never-touched controls. Gemini
first, then a genuinely fresh Claude subagent as the independent second
pass, per `PDR-006`'s amendment. Full findings in
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. Result: 9 confirmed fixes, 0
relabels.

**A new, previously-undiscovered systemic pattern.** Both passes
independently found that batch 22's own emotional-state diversity
instruction had created pressure to invent a named feeling with zero
textual basis, in the same shape three times — "because I am completely
spent," "I feel sheepish because...," "I am confident and ready" /
"confidently" — each removed since the input gave no seed for it at all.
Two further candidates were correctly *declined*: "I am feeling serene"
(the input's own "it's just so peaceful here" is a direct textual seed)
and "preparing confidently" ("fully prepared" already implies it). **This
distinction — zero textual seed versus a close paraphrase of one the
input already states — is now the operative test**, not whether the
exact word appears in the input.

**Two more content fixes.** A `long_rambling` example asserted a uniform
"tonight" for milk-disposal and general fridge-emptying when the input
only explicitly times the leftovers that way; reworded to keep the
specific timing where actually stated. A second `long_rambling` example's
hedge "I think I just need to stop and make a cup of tea" had been
converted into the action item "Think about stopping to make a cup of
tea" — changing the task from *doing* the thing to *thinking about* it,
distinct from a plain dropped hedge; restored to "Probably stop and make
a cup of tea."

**Two `expert` overclaims the fresh pass caught that Gemini hadn't
precisely named.** A `voice_to_text_artifact` example's mistranscription
fumbling and its resolution are both manifestations of the *same* single
category mechanism, not two combined structures — downgraded to `hard`,
correcting this session's own earlier judgment that treated
"self-correction-style name recall" as a second element when it wasn't.
A `multi_person_note` example was tagged `expert` under the category's
"3+ named people, mixed certainty" carve-out, but literally only 2 people
were named — the narrator's own unnamed "I" doesn't satisfy "named," so
the carve-out's literal bar wasn't met; downgraded to `hard`. One
`dangling_reference`/`expert` (single mechanism) was downgraded the same
way both passes agreed on directly.

**Two of Gemini's claims were confirmed as overreach, both instructive.**
Gemini argued a `voice_to_text_artifact` example should preserve its
mistranscription fragments verbatim because the category field isn't
literally "self_correction" — the fresh pass correctly identified the
noise-as-effect convention as a property of `voice_to_text_artifact`
itself, not gated on matching a different category's name. Gemini also
argued a `rapid_branching` example's hedged musings shouldn't be
`action_items` at all since nothing is truly committed to — directly
contradicting this project's own settled, extensively-reinforced
convention that a hedged intention belongs in `action_items` with the
hedge preserved.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 375/375 after all 9 fixes (one remaining
flagged pair is the already-confirmed false positive from batch 21). No
rejections, no relabels — every fix applied in place. 375 accepted
examples after twenty-two batches and ten adversarial re-reviews. Next
periodic re-review due after batch 24.

## Eleventh adversarial re-review (2026-09-02) — corpus 425 → 425

Due after batch 24, first run after the mid-batch-23 billing
interruption. 12 examples: 5 touched (fixed) during batches 23-24's own
first-pass review, 7 never-touched controls. Gemini first, then a
genuinely fresh Claude subagent as the independent second pass, per
`PDR-006`'s amendment. Full findings in [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s
log. Result: 9 confirmed fixes from the sample, plus 2 more found by a
systemic corpus-wide follow-up check, 0 relabels.

**Settled a direct contradiction between the two passes over
`repeated_reminder`'s own definition by reading `TAXONOMY.md` itself.**
Gemini wanted a third restated item added to `#378`; the fresh pass
argued the opposite for `#416` — that this session's own batch-24 fix,
which split one restated task into two items, broke the category's
defined lesson. `TAXONOMY.md` settles it: restated tasks are "one item,
not two." The fresh pass was right, and **this session's own batch-24
fix was itself the defect** — reverted. The same standard, checked
corpus-wide rather than per-instance, found the identical shape in two
more places outside the sample: batch 23's landlord example (`#400`, 3
items for one repeated instruction) and `#220` (vitamins reminder split
across two items). All four collapsed to one item each.

**A second finding only the side-by-side comparison caught.** `#387`
("I don't know if I should do green or just keep it white") correctly
produced empty `action_items`. `#389` ("I can't decide if I want to get
rid of it"), the identical ending shape, had an invented "Decide if I
want to get rid of it" task left over from this session's own earlier
batch-23 fix, which hadn't gone far enough. Reverted to `[]` to match
`#387`'s precedent.

Three more real fixes: `#376`'s bullet described an interrupted
fragment as "an unfinished thought about... an unspecified thing"
instead of preserving it, while the record's own narrative correctly
kept the input's broken-off text verbatim — rewritten. `#384`'s bullet
dropped a stated "I think" hedge its own narrative had correctly kept —
restored. `#396`'s bullet read as a settled preference where the input
only asks a question — reworded. `#377` lost its `expert` tag as a
direct consequence of this session's own earlier fix removing its
return-to-subject-A line: correct on the zero-returns rule, but it also
removed the only candidate for a second combined mechanism, leaving a
single-mechanism switch — downgraded to `medium`. Two Gemini claims
declined as overreach, both on `#384`: an invented-hedge claim
("I suspect Kevin was...") where the input's line was already a
character judgment, not a fact-claim; and a missing-second-mechanism
claim where the three-named-people/zero-commitment structure is exactly
the combination this project's own batch-23 targeting asked for.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 425/425 after all 11 fixes. No rejections, no
relabels — every fix applied in place. 425 accepted examples after
twenty-four batches and eleven adversarial re-reviews. Next periodic
re-review due after batch 26.

## Depth by category (running total, after batch 25)

Batch 25 (25 requested, 25 accepted, 0 rejected, 0 relabeled, 12 records
fixed) —
closed the depth floor, `simple_list` (25, structurally capped below
`expert`), with exactly 5 examples weighted toward its thinnest
non-structural tier (`hard`). Also 5× `repeated_reminder`/`expert`,
raising it from 3 to 8 `expert` examples via genuine second-mechanism
combinations (time-ambiguity, multi-person attribution, embedded
dangling references) — the first batch generated with the eleventh
re-review's "one item, not two" rule stated directly in the prompt.
Remaining 15 free mix weighted toward `expert` in categories thin on
that tier (`contradictory_statement`, `dangling_reference`,
`interrupted_thought`, `self_correction`).

`voice_to_text_artifact` (29), `rapid_branching` (29), `contradictory_statement`
(28), `interrupted_thought` (28), `minimal_fragment` (27),
`dangling_reference` (30), `multi_person_note` (30), `simple_list` (30),
`time_ambiguous` (30), `topic_interleaving` (30), `long_rambling` (31),
`repeated_reminder` (31), `self_correction` (31), `topic_switching` (33),
`zero_action_items` (33).

**Difficulty distribution, full corpus**: easy 93, medium 127, hard 142,
expert 88 (450 total).

**Twelve records fixed on this session's own first-pass review, before
any periodic re-review touched the batch — the "one item, not two" rule
held cleanly across all 5 `repeated_reminder` examples with no
violations, first real test of the eleventh re-review's fix.** Found in
two passes: a manual read caught four instances first, then the
standing automated checks caught eight more the manual read missed.

Manual read (4 records): three bullets used clinical, report-style
phrasing ("an unnamed male," "unspecified materials") in place of the
writer's own referring words ("him," "the stuff") — a new surface form
of the describing-instead-of-being register violation, rewritten to
match the narrative's natural register. A `self_correction` example's
bullet listed all three previously-considered flight dates (14th, 16th,
week after) as "potential options," reasserting retracted content
alongside the correction — the exact class of violation the tenth
re-review's "exit 15, rather than 14" case named; collapsed to the one
settled outcome (hold off entirely), matching that fix's own precedent
rather than repeating the mistake fresh.

Automated checks (8 more, across 8 records — one of which needed two
separate fixes): the standing passive-voice check caught 6 subjectless
bullets ("The vendor needs to be contacted...", "Milk needs to be
purchased...") this batch's own generation introduced fresh — rewritten
to active voice with a clear subject, matching the register
`action_items` already used correctly throughout. The standing
meta-commentary check caught one narrative using "my train of thought
was interrupted" — the exact literal phrase this project's regression
regex already bans by name — rewritten in the same record as one of the
six passive-voice fixes.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 450/450 after fixes.

450 accepted examples after twenty-five batches and eleven adversarial
re-reviews. Periodic adversarial re-review due after batch 26.

## Depth by category (running total, after batch 26)

Batch 26 (25 requested, 25 accepted, 0 rejected, 1 relabeled, 5 fixed) —
closed the depth floor, `minimal_fragment` (27, structurally capped
below `expert`), weighted toward `hard` via ambiguity density. Also 5×
`contradictory_statement` (3 `expert` via a genuine second mechanism, 2
`easy`) and 5× `interrupted_thought` (3 `easy`, 2 `medium`), both
addressing thin tiers. Remaining 10 free mix weighted toward `easy` in
`rapid_branching`/`voice_to_text_artifact` (both very thin on that tier)
and `expert` generally elsewhere.

`time_ambiguous` (30), `simple_list` (30), `voice_to_text_artifact` (31),
`repeated_reminder` (31), `minimal_fragment` (31), `multi_person_note`
(31), `rapid_branching` (31), `topic_interleaving` (31), `dangling_reference`
(32), `long_rambling` (32), `self_correction` (32), `contradictory_statement`
(33), `interrupted_thought` (33), `topic_switching` (33),
`zero_action_items` (34).

**Difficulty distribution, full corpus**: easy 102, medium 131, hard
147, expert 95 (475 total).

**One relabel: a `minimal_fragment` example requested as `hard` actually
contained a conditional** ("three if they still have the thing") —
directly violating this category's own no-branching/no-conditional
definition, the same recurring failure mode batches 8 and 12 hit on this
exact category. Relabeled to `dangling_reference`, which correctly holds
the conditional plus the unresolved "the thing."

**Five fixes, three from a systematic gap and two from the
structural-ceiling principle.** Two `minimal_fragment` bullets read as
hedged or conditional intended purchases ("maybe those blue ones for
him," "eggs milk the big cheese") with empty `action_items`, while two
sibling records in the very same batch with equally implicit but
explicit-verb inputs correctly filled theirs — an internal batch
inconsistency caught by comparing all five side by side, matching the
established convention that a hedged intention belongs in `action_items`
with its hedge preserved; all three given a matching hedged/implied
action item. Two `expert` tags (`zero_action_items`, a solo reflection
on whether to journal dreams; `long_rambling`, a rambling walk with an
incidental task) were each a single mechanism elaborated at length with
no genuine second, distinct structure combined — the same pattern the
eighth re-review named directly ("rambling drift... [is] a native
feature of how the category works, not a second, distinct structure");
both downgraded to `hard`.

**One near-duplicate caught before it entered the corpus**: a new
`interrupted_thought` example ("need to buy flour sugar and check if
the—") scored 0.70 against an existing batch-24 record with the same
opening and grocery items — reworded to a different task entirely rather
than declined, since the phrasing match was real. One remaining flagged
pair (0.58, "text Mike about the Thursday thing" / "tell her about the
tall one") judged incidental — different verbs, different referents, low
word overlap — same class as the standing #205/#343 false positive.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 475/475 after fixes.

475 accepted examples after twenty-six batches and eleven adversarial
re-reviews. Periodic adversarial re-review due now, per the
every-2-batches cadence.

## Depth by category (running total, after batch 27) — corpus hits 500

Batch 27 (25 requested, 25 accepted, 0 rejected, 0 relabeled, 5 fixed) —
the final batch to close the 500 target. Spread 2 examples each across
the 8 categories tied lowest (`simple_list`, `time_ambiguous`,
`topic_interleaving`, `repeated_reminder`, `rapid_branching`,
`minimal_fragment`, `multi_person_note`, `voice_to_text_artifact`, 16
total), remaining 9 free mix weighted toward `easy`/`expert`, the two
overall-thinnest tiers going in.

`simple_list` (32), `time_ambiguous` (32), `dangling_reference` (33),
`long_rambling` (33), `minimal_fragment` (33), `multi_person_note` (33),
`rapid_branching` (33), `repeated_reminder` (33), `topic_interleaving`
(33), `voice_to_text_artifact` (33), `contradictory_statement` (34),
`interrupted_thought` (34), `self_correction` (34), `topic_switching`
(34), `zero_action_items` (36).

**Difficulty distribution, full corpus**: easy 118, medium 133, hard
149, expert 100 (500 total).

**Five fixes.** Two `multi_person_note` bullets attributed a third
party's task with a colon-label format ("Alex: Clean the bathrooms")
that doesn't match this corpus's own established convention for
third-party commitments (`"[Name] to [verb]"`, e.g. "Uncle Bob to handle
the catering") — a small batch-tracking drift, caught by comparing this
batch's phrasing against the standing corpus pattern rather than any
per-example rule; rewritten to match. Three narratives had zero
first-person pronoun — the standing regression check's genuine edge
case: bare, verb-less or near-verb-less fragments ("the green one," "the
meeting got moved to 3:30") with nothing for a faithful recovery to
attach a pronoun to without inventing content, the same shape batch 18
first found and fixed; given minimal, non-inventive first-person framing
matching that precedent.

**No fixes needed on category structure or evidence rules this batch** —
every `expert` tag checked out with a genuine, nameable second mechanism
(a factual dispute between two people layered on a contradiction; a
topic-switch combined with a dangling reference; a self-correction
combined with a second unresolved referent; a reflection combined with
an embedded, unrelated task insertion), `repeated_reminder`'s "one item,
not two" rule held clean again, and `self_correction` correctly dropped
retracted content throughout.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 500/500 after fixes (one new flagged pair
judged incidental — a shared "call the [X] about the [Y]" phrase
template with low word overlap and unrelated topics, the same class as
the two standing false positives).

**500 accepted examples after twenty-seven batches and eleven
adversarial re-reviews — the corpus hits `train.py`'s
`SMALL_CORPUS_WARNING_THRESHOLD` target.** Periodic adversarial re-review
due now, per the every-2-batches cadence — batches 25-27 haven't had one
yet (last was after batch 24).

## Twelfth adversarial re-review (2026-09-02) — corpus 500 → 500

Due after batch 27, first run since the corpus hit 500. 13 examples: 8
touched (fixed) during batches 25-27's own first-pass review, 5
never-touched controls. Gemini first, then a genuinely fresh Claude
subagent as the independent second pass, per `PDR-006`'s amendment. Full
findings in [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)'s log. Result: 2
confirmed content fixes, plus 1 scenario-repetition rework both passes
found independently, 0 relabels.

**Correction to this section's own batch-27 write-up above**: it claimed
"self_correction correctly dropped retracted content throughout" — this
re-review's sample included `#449` (a batch-25 record, reviewed here for
the first time) and found that claim false for that record; see the fix
below.

**Both passes independently and strongly flagged the same
scenario-repetition problem, needing no reconciliation.** `#473`,
`#436`, and `#497` — three separate records in this one 13-example
sample — all center on deciding a paint color for a room, a third
instance past this project's own two-per-scenario tolerance, and found
within a single review sample rather than only visible spread across
many batches like prior scenario-well findings. `#497` reworked
entirely to a different scenario (choosing a font for wedding
invitations, same long_rambling + interleaved-unrelated-task structure)
rather than the other two, since its lesson doesn't depend on the
paint-specific content.

**Two confirmed content fixes.** `#431` (`repeated_reminder`/expert)
split one restated worry into two bullets — the same "one item, not
two" violation the eleventh re-review settled by reading `TAXONOMY.md`
directly; merged. `#449` (`self_correction`/expert) had its narrative
and a bullet both narrate the retracted "email the vendor" plan instead
of dropping it — checked against this session's other `self_correction`
fixes, all of which land directly on the final decision with zero
mention of the retracted option, confirming this record as the outlier;
fixed.

**Two Gemini claims declined as overreach, both confirmed wrong by
checking the input directly.** A REJECT on `#471` argued a hedged
musing must produce an `action_items` entry, but the input's own closing
line ("I really don't know if I'll actually do it") is a bare state of
indecision with nothing committed to — the established exception, not
an instance of the rule. A FIX on `#442` claimed "sensory input feels
excessively loud" violates no-diagnosis-framing — declined, since that
rule targets naming an actual diagnosis, not descriptive paraphrase.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 500/500 after fixes. No rejections, no
relabels — every fix applied in place. 500 accepted examples after
twenty-seven batches and twelve adversarial re-reviews. Next periodic
re-review due after batch 28.

## Depth by category (running total, after batch 28) — targeted at a real eval failure, not a corpus gap

Batch 28 (25 requested, 25 accepted, 0 rejected, 2 relabeled) — the
first batch generated in direct response to the first real training
run's evaluation results (`training/eval_run_2026-09-02.log`), not a
depth-tracking gap. The trained checkpoint repeatedly promoted hedged
reflection into invented `action_items` on real (non-synthetic) input.
Targeted: 6× `zero_action_items` built as pure reflection with
genuinely zero nameable task, 6× deliberate near-miss contrasts (same
reflective tone, but containing one real hedged task, correctly
categorized as whatever they actually teach rather than forced into
`zero_action_items`), 4× `contradictory_statement` + 2×
`rapid_branching` + 2× `long_rambling` each with a hedged task buried in
otherwise uncertain content, plus 5 free-mix examples deliberately
written longer and messier than this corpus's average register — closer
to the real notes' own style — without ever consulting
`real_validation.jsonl`'s actual content.

`simple_list` (32), `time_ambiguous` (33), `dangling_reference` (34),
`interrupted_thought` (34), `minimal_fragment` (34), `multi_person_note`
(34), `repeated_reminder` (34), `topic_interleaving` (34),
`topic_switching` (34), `voice_to_text_artifact` (34), `long_rambling`
(35), `rapid_branching` (36), `self_correction` (36),
`contradictory_statement` (38), `zero_action_items` (42).

**Difficulty distribution, full corpus**: easy 118, medium 143, hard
158, expert 106 (525 total).

**Two relabels, both the same recurring failure this project has caught
many times: Gemini defaulting to a structural category name that
doesn't actually fit.** One example (uninspired → considering old
sketchbooks) was requested/labeled `topic_switching`, but it's a single
continuous, thematically-connected train of thought, not an abrupt
switch to an unrelated subject — relabeled to `rapid_branching`. Another
(boxes → realizing Greg is out of town) was requested/labeled
`interrupted_thought`, but "actually he's out of town" is a
realization-driven pivot, not an external interruption cutting off a
clause — `self_correction`'s shape instead; relabeled, and per that
category's own convention, the retracted "ask Greg" mention removed
from narrative and bullets to match this session's own earlier fix to a
near-identical case (`#449`).

**One fix matching the established "representing an absence" convention
exactly**: an `interrupted_thought` example's narrative smoothed over
the input's actual mid-clause cutoff ("I think I have everything except
the...") into a vague paraphrase ("thought I had everything") instead of
preserving the broken-off text verbatim — restored.

**The batch's own deliberate push toward longer, messier, more
real-feeling input had a real cost, caught before it entered the
corpus**: 7 of 25 narratives landed above the corpus's 0.85 copy-ratio
flag line (mean 0.776 for the batch), the same non-recovery failure
mode the eval itself found in the trained model — training on more
near-copies would have reinforced the exact behavior this batch exists
to correct. All 7 rewritten to genuinely reorganize (different sentence
order, real paraphrase) rather than lightly rephrase in the input's own
order; batch mean dropped to 0.691, max to 0.83, nothing left above the
flag line.

Full three-check voice-regression suite, schema validation, and
duplicate check clean at 525/525 after fixes.

525 accepted examples after twenty-eight batches and twelve adversarial
re-reviews. Periodic adversarial re-review due after batch 29, per the
every-2-batches cadence continuing from the twelfth re-review's baseline
(after batch 27).

## Copy-ratio remediation pass (2026-09-02) — corpus 525 → 525

Not a batch and not a re-review: a corpus-wide data-quality pass closing
the external review's finding C1, after the product owner reviewed and
approved all 58 proposed dispositions in
[`../reviews/2026-09-02-copy-ratio-disposition.md`](../reviews/2026-09-02-copy-ratio-disposition.md).

**The finding being closed.** `REVIEW_GUIDE.md` §6b calls input→narrative
similarity "the strongest quantitative signal available" and recorded the
corpus mean as 0.561 with exactly two records permanently above 0.85.
Nothing in `training/` ever computed it, so it drifted invisibly: the
measured mean at commit `78d5ae8` was **0.647 with 60 records above 0.85**,
climbing monotonically by corpus position (0.497 in the earliest 75 records,
0.706 in the most recent 75). This is the same non-recovery behaviour the
first real training run's evaluation found in the trained model, which
echoed its input at 0.77 on real notes — the corpus taught it that.

**29 records rewritten** to genuinely reorganize: lead with different
content, group related items, compress. Every rewrite preserves hedges
exactly as stated, leaves ambiguous referents unresolved, and keeps
`interrupted_thought` cutoffs (`"the—"`, `"hallw-"`, `"befo—"`) verbatim —
no cutoff was touched. Bullets and action_items were left alone except for
one record (`#365`), whose narrative *and* first bullet both narrated a
retraction ("I initially thought I was definitely free...") instead of
dropping it, which `self_correction`'s own convention forbids; flagged in
the disposition as a separate non-copy-ratio issue and fixed here.

**29 records allowlisted** in `check_copy_ratio.py`, each with its own
recorded rationale, as the same shape as the two pre-existing entries: the
input is already short, already in the correct narrative order, or a single
continuous reflection where reordering would be artificial rather than
recovery. Several short `interrupted_thought` records qualify for a
structural reason worth naming — almost all their content *is* the verbatim
cutoff, so there is nothing left to reorganize around it, the same argument
that allowlists `#118` for `dangling_reference`.

**Result:** corpus mean 0.647 → **0.631**, max non-allowlisted breach
eliminated, `check_copy_ratio.py` exits 0. The metric is now enforced by
code rather than by prose, so the next drift is visible immediately.

**Two scenario wells broken** (external review M6, surfaced by the rebuilt
`check_duplicates.py`): `#291` was the third prescription-pickup note and
`#146` one of two dry-cleaning-plus-contact-Mom notes. `TAXONOMY.md`
tolerates two examples per scenario and calls a third a signal that
generation is falling into a well. Both replaced with fresh scenarios (a
parcel-locker pickup code; returning a spare key and watering plants),
category, difficulty and lesson preserved in each. Prescription is now a
pair (`#22`/`#122`) and dry-cleaning no longer flags at all.

**PROVENANCE NOTE, recorded deliberately rather than left silent:** those
two replacement `input` values are **Claude-authored**, unlike the rest of
`synthetic.jsonl`, which is Gemini-generated per batch. Generating
replacements through Gemini would have required the product owner's
per-batch authorization for a billed call, which was not in hand at the
time. Anyone auditing batch provenance should know these two records belong
to no batch.

**Caught during the pass, worth recording as a live instance of a
documented trap.** `REVIEW_GUIDE.md` §6b warns that the copy-ratio rule and
the first-person-voice rule pull against each other — "the cheapest way to
stop describing a note is to start reciting it," and the inverse. Three of
the rewrites (`#146`, `#231`, `#338`) dropped every first-person pronoun
while chasing a lower ratio, and were caught by the standing voice check,
not by eye. Fixing `#338`'s voice pushed its ratio straight back to 0.917;
it took three attempts to land a version that satisfies both rules at 0.73
while keeping "maybe"/"could" and the verbatim cutoff. Re-measure both axes
after any narrative edit — that instruction is load-bearing, not
theoretical.

Full three-check voice-regression suite, schema validation, duplicate
check, copy-ratio check, and the 17-test serialization suite all clean at
525/525. No `<unk>`-producing records.

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
