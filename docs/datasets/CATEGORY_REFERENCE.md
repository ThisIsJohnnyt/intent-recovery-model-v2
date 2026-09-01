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
