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
— fix before anything else.

Schema validity does not catch text corruption: a replacement character or
stray control character is a perfectly valid JSON string and will pass both
this validator and `training_data.schema.json`, then go straight into
training. Grep the batch for U+FFFD, control characters, and common mojibake
sequences (`â€"`, `Â`) before accepting — two seconds, and neither tool above
can do it by construction:

```bash
python -c "
import json, unicodedata
for i, l in enumerate(open('datasets/synthetic.jsonl', encoding='utf-8'), 1):
    for ch in l:
        if ch == '�' or (unicodedata.category(ch) == 'Cc' and ch != '	'):
            print('line', i, 'suspicious char', hex(ord(ch)))
"
```

(Note: a console that cannot render an em dash will *display* one as a
replacement character. Verify a suspected hit by printing the codepoint, not
by eye — the third adversarial re-review reported a corrupted em dash that
turned out to be a clean U+2014 rendered through a cp1252 terminal.) This Python validator is authoritative (it's
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
- **Unmarked ambiguity** (a detection problem, not a new prohibition): the
  bullet above, and "No invented certainty" below, both find ambiguity by its
  *markers* — "i think", "maybe", a deliberately vague noun phrase ("the blue
  folder"), a pronoun with two candidate antecedents. A note can also be
  underdetermined with **no marker at all**, because the writer was not
  uncertain: they knew what they meant, wrote it plainly, and only a *reader*
  is left guessing. "get the silicone one" — silicone caulk, or a silicone
  caulk remover? — reads as flat and decided as any other imperative and trips
  no hedge-word check. The output then picks a reading and states it as fact,
  and every marker-based bullet in this section passes it, because nothing new
  is *named*: what was added is the confidence. **Test by reading `input`
  alone, as a stranger who does not already know the answer.** If a phrase has
  more than one plausible referent under that reading, the output may not
  choose one — carry the writer's own words through instead ("get the silicone
  one"). Note that the categories most prone to this are *not* the ones
  labelled for it: `dangling_reference` examples handle their marked reference
  correctly because the label announces it, while an unmarked ambiguity
  sitting inside a `topic_interleaving` note goes unexamined. Identified by
  the product owner's hand spot check, 2026-08-25.
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
  **Exception, transcription-layer artifacts** (`voice_to_text_artifact`):
  spoken punctuation ("comma", "period", "new paragraph"), dictation commands
  ("write down", "remind me", "cancel that", "pause"), and mistranscription
  self-corrections ("right down — wait, write down") are *noise, not
  fragments*. They are represented by their **effect** on the recovered
  content, never by their own surface text. The test is whether the writer
  intended it as content or as an instruction to the device. Apply uniformly
  within a single example — never keep half of one artifact event and drop
  the other half. Without this exception the rule above and the category's own
  definition ("recover intent *through* the noise, don't annotate the noise")
  give opposite answers; the fourth adversarial re-review found two examples
  answering both ways at once, which was a gap in this guide rather than an
  error by either reviewer.
- **No over-summarization**: don't compress `input` so much that a
  distinct fragment disappears into a vaguer, more general statement.
- **No unsupported tasks**: `action_items` never contains a task that
  isn't implied by `input`.
- **No dropped imperatives** (the only under-extraction rule in this
  section): every other `action_items` bullet here constrains what must *not*
  go in — "No unsupported tasks" above, "No invented certainty" below. None of
  them required a task the input genuinely *does* state to actually appear. An
  explicit imperative in `input` is a committed next step and belongs in
  `action_items` **even when its object is an unresolved reference**: "don't
  forget the framework from that one article" becomes "Remember the article's
  framework for behavioral questions", not nothing. Being hard to act on is
  not a reason to omit it — carry the imperative through with its reference
  still unresolved. This failure passes review because preserving the fragment
  in `bullets` alone already satisfies "No lost low-salience reminders" while
  still losing the commitment. Identified by the product owner's hand spot
  check, 2026-08-25.
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
- **No inferred setting or frame**: the output never names an activity,
  venue, occasion, relationship, domain, or object class that `input` only
  implies through its props. "Sleeping bag" and "camp stove" do not license
  "camping trip"; "honey" and "carboy" do not license "mead"; "chapter 4"
  and "discussion questions" do not license "the book" or "the group";
  "primary mirror" does not license "telescope". The test is **not** whether
  the inference is probably right — it usually is, which is exactly why this
  survives a fluency read — but whether the writer actually said it. A
  note-organizer that names the frame is guessing on the writer's behalf
  about the one thing the writer already knew and therefore didn't bother to
  write down. Distinct from invented causality (no new event or link is
  asserted) and from invented certainty (no hedge is smoothed); this is
  supplying a *category* for something the input left unnamed. Identified by
  the third periodic adversarial re-review (2026-08-23) — see this file's
  "Periodic adversarial re-review" log.
- **Fields must agree with each other**: after checking `narrative`,
  `bullets`, and `action_items` against `input` individually, check the three
  against *each other*. A disagreement about the same fragment means at least
  one of them is wrong, and it is the fastest way to locate an invention —
  the field carrying prose-fluency pressure (`narrative`) typically names an
  inferred frame first while the others stay literal, and `action_items` can
  contradict a retraction that `narrative` correctly honored. Two real
  instances: a narrative saying "Saturday's camping trip" where its own
  bullets said only "for Saturday"; an `action_items` entry leading with
  "Clean (or maybe just air dust) the primary mirror" where the narrative
  correctly honored the input's "actually maybe just air dust it" retraction.
- **No non-recovery** (the narrative must actually do something): the
  narrative has to *reorganize*. A narrative that reproduces `input` in its
  original order with only capitalization and punctuation repaired has
  performed no recovery — and passes every other bullet in this section
  trivially, because it invents nothing, loses nothing and smooths nothing
  precisely by doing nothing. **Every bullet in §4 except this one is a
  prohibition on addition, which means copying the input is the degenerate
  optimum of the whole checklist.** This bullet is the counterweight. Cheap
  detector: token-sequence similarity between `input` and `narrative` (see
  §6b). Corpus mean across batches 1–7 is ~0.50; anything above ~0.85 should
  be read deliberately, and a near-verbatim narrative is a defect however
  clean it looks. Identified by the fourth adversarial re-review (2026-08-23),
  which measured the corpus mean climbing from 0.50 to 0.67 over batches 8–9
  as the evidence rules were tightened — generation finding the safe gradient.
- **Representing an absence** (a convention, not a prohibition): three
  categories — `interrupted_thought`, `contradictory_statement`, and
  `dangling_reference` — require the output to convey something that *isn't
  there*: a thought that stops, two claims that can't both hold, a referent
  never resolved. No output field has a device for absence, so generation
  reaches for the only one available and starts describing the note ("The
  note cuts off mid-sentence while mentioning the mailman"). This is why
  meta-commentary has reappeared in four successive surface forms, each after
  the previous was banned by name: the *pressure* was never addressed, only
  its symptom. **The convention: preserve the note's own broken-off text
  verbatim** — `"Print the—"`, `"Oh look the mailman is—"`. That is the note
  itself rather than a report about it, and it satisfies the voice rule
  without inventing a completion. Adopted 2026-08-23 after the fourth
  adversarial re-review diagnosed the mechanism.
- **`action_items` ownership**: an entry may be a task committed to by *any*
  person named in `input`, attributed to them ("Uncle Bob to handle the
  catering") — not only the writer's own tasks. What does **not** belong is a
  past event with no forward commitment ("Dr. Patel called" is not an action
  item). A third party's expected arrival ("plumber is supposed to come by")
  does belong, since it is a commitment, but must keep its hedge. Settled by
  the product owner 2026-08-23 after the third adversarial re-review found
  the corpus teaching two conventions at once; see
  [`training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md)'s "File
  format" rules for `output`.

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

### 6b. Cross-example consistency (not covered by items 0–5)

Everything above judges one example against its own `input`. That structure
has a blind spot: a *convention* can drift across batches while every
individual example remains defensible against its own input, so no per-example
check ever fires. Items 0–5 cannot catch this by construction.

**Batch and category are two different generators of drift. Check both; rank
neither.**

- **Batch-tracking drift is a prompt artifact.** It appears in whatever
  categories that batch happened to contain, is uniform within the batch, and
  shows up faintly in each category and obviously in none. Example: batch 4
  was 15/15 third-person narratives across nine categories. Example: bullet
  terminal punctuation ran 0% in batch 9 and 100% in batch 10 — perfectly and
  oppositely uniform, and invisible to any per-example check because a period
  is never *wrong* against its own input.
- **Category-tracking drift is structural pressure from what the category
  asks the output to represent.** It spans batches, concentrates in one
  category, and recurs in *every* batch that touches that category — which
  makes it the more durable and more dangerous of the two. Example:
  meta-commentary concentrates in `interrupted_thought` (3 of 9 examples,
  across three batches) because that category asks the output to represent an
  absence and no field can. See §4's "Representing an absence".

An earlier version of this section said, in bold, to check by batch *first*.
That was generalized from a single incident and it is wrong: the fourth
adversarial re-review found a category-tracking defect that a batch-first read
would have diluted across three batches. Neither axis is primary.

So, once per batch: read the new batch's narratives (or bullets, or
`action_items`) as a **column**, all of them together, and ask whether the
batch as a whole has adopted a convention the rest of the corpus doesn't
share. Then do the same down each category the batch touched. Ask whether
they still agree on:

- **Narrative voice.** First person throughout, per
  [`DATASET_SPEC.md`](../../training/DATASET_SPEC.md)'s `output` rules. Never
  "the speaker", "the author", "dictated notes about…". **First person is not
  sufficient on its own** — "I noted that…", "I wrote that…", "I also
  stated…" are first person and still describe the note rather than being it.
  Batch 9 produced exactly this after the third-person forms were banned, in
  `contradictory_statement` specifically, where presenting two conflicting
  statements creates pressure to narrate the conflict instead of simply
  stating both halves. The test is not the pronoun; it is whether the
  narrative is the note reorganized or a report about the note.
- **`action_items` ownership.** Same convention as the rest of the corpus
  (any named person's commitment, attributed; not past events) — see §4.
- **Field register.** Bullets phrased consistently rather than switching
  between imperative, impersonal, and first-person within a category.
- **Depth of transcription/artifact commentary**, for
  `voice_to_text_artifact` specifically — recover intent through the noise,
  don't annotate the noise.
- **Input→narrative copy ratio.** Purely comparative, and the strongest
  quantitative signal available. Token-sequence similarity between `input` and
  `narrative`, read as a distribution rather than per example: a single high
  value may be inherent to a category, a whole batch shifting upward is
  generation retreating into non-recovery (see §4's "No non-recovery").
  **Two records sit above 0.85 permanently, by decision, 2026-08-25**: #127
  (`simple_list`/easy, 0.87) and #118 (`dangling_reference`/medium, 0.91).
  Both inputs are already single well-formed sentences, so there is no
  structure left for the narrative to recover and the extraction work is
  entirely the bullets' -- #118's narrative correctly leaves both "he" and
  "it" unresolved. A high ratio is the *right* answer for a short,
  already-ordered note, and forcing it down would mean padding. Don't
  re-open these two. Do re-open any other record that climbs: the four fixed
  that day (#67, #83, #94, #125) were all `long_rambling`,
  `dangling_reference` and `rapid_branching` at hard or expert, where
  tracking the note's own order means no recovery happened at all.
  **Now enforced by `training/check_copy_ratio.py`, 2026-09-02 — run it on
  every batch.** For most of this project's life the rule above lived only in
  this document: nothing in `training/` computed the distribution, so it was
  recomputed by hand inside review sessions and drifted invisibly between
  them. An external review measured the damage at commit `78d5ae8`: the mean
  had gone from the 0.561 recorded here to **0.647**, with **60** records
  above 0.85 rather than the two named above, and a monotonic climb by corpus
  position (0.497 in the first 75 records, 0.706 in the most recent 75).
  Reproduced exactly, including both anchor values, before being accepted.
  The script names every breaching record, prints per-category and
  per-position means, carries #118 and #127 in an allowlist keyed by content
  hash (not line number, which shifts), and exits non-zero on any other
  breach. `check_duplicates.py` does **not** cover this — it measures
  input↔input similarity between records, a different quantity.
- **Difficulty calibration.** `difficulty` is a purely comparative judgment —
  it means nothing against one input and everything against the corpus — and
  so it is the most cross-example field in the schema. The proof case: #127
  and #128 are the same note with different nouns, one labelled `easy` and one
  `medium`, in the same batch. Per-example inspection cannot catch that; only
  putting them side by side can. Every difficulty relabel this project has
  made was found by comparison, never by inspection.
- **Scenario repetition.** `check_duplicates.py` is lexical and cannot see
  this: two notes can describe the same situation while sharing almost no
  wording. Batch 10 produced a "40 gal tank setup" note and a "the magic
  system is based on…" note, both of which the corpus already had; measured
  similarity was 0.14 and 0.15 against a 0.55 threshold. Read the batch's
  `input` values as a list and ask whether any *situation* is already in the
  corpus, not whether any wording is. Two examples per scenario is acceptable
  under the diversity rule; a third is a signal that generation is falling
  into a well. **Read the whole `input` column for this, not just the new
  batch** — the fourth adversarial re-review did, and found two wells already
  past the line that nobody had noticed: car-maintenance errands (#48, #85,
  #94, #102, #132 — five) and garden/tomatoes (#6, #30, #42, #130 — four).
  Applying the threshold only to scenarios someone happens to notice is not
  applying it.

Real instance, and the reason this section exists: narratives written in the
third person ("The author is planning a large spring vegetable garden…",
"Voice-recorded reminders regarding tennis equipment preparation. The speaker
needs to…") instead of the writer's own voice. **26 of 115 examples were
affected — batch 4 in its entirety (15/15), plus 2 from batch 5, 2 from batch
7, and 7 more carrying meta-framing openers ("Notes on houseplant care…",
"Brainstorming food options for…").** Nine different categories.

Neither routine review nor any of the three adversarial re-reviews caught it —
the first re-review sampled 15 examples from batches 1–4 and did not flag it —
because every check in items 0–5 evaluates one example against its own
`input`, and each of those narratives was individually faithful. The first
attempt to diagnose it also got the shape wrong, reading it as one category's
problem because that was the only category listed side by side at the time.
All 26 were rewritten to first person on 2026-08-23, the rule pinned in
`DATASET_SPEC.md`, and this section rewritten to check by batch first.

**That fix did not take, and the check written to guard it was the reason.**
The product owner's hand spot check on 2026-08-25 found third-person bullets in
a record whose bullets had been edited during that very sweep. A positive test
(does the narrative contain a first-person pronoun at all?) then found **15
narratives still not in the writer's voice, none of them touched by the
26-example rewrite**, plus 26 records carrying third-person bullets and 9
narratives still carrying meta-commentary — in `interrupted_thought` and
`contradictory_statement`, exactly where the paragraph above predicts, and
sitting alongside correct exemplars (#80, #81, #117) so the corpus was teaching
both conventions at once. The banned-form regex returned **one** hit on all of
that, and it was a false positive: `the\s+author` matching "the authorization
form" in #83. Zero true positives, for three weeks, while reading clean.

**The lesson is about the shape of the check, not this defect.** A test that
enumerates forms already seen goes quiet exactly as generation moves to the
next form — the same mechanism §4's "Representing an absence" describes for
prohibitions. Prefer a positive test for the property you actually want. The
checks below were rewritten on that principle 2026-08-25.

**Fixing voice raises the copy ratio.** All 24 narratives rewritten that day
moved *up* on input→narrative similarity (corpus mean 0.535 → 0.582, worst
case 0.67 → 0.93), because the cheapest way to stop describing a note is to
start reciting it. Twelve had to be reorganized a second time to bring them
back (mean settled at 0.561). **Measure the copy ratio after any voice fix**;
the two rules pull against each other and satisfying one silently breaks the
other.

**Re-check every corrected example against the full checklist, not just the
item that prompted the correction.** A fix applied to satisfy one item can
introduce a violation of another. Real instance: the second adversarial
re-review correctly caught #77 silently resolving the ambiguous conditional
"I'll do it if Greg doesn't"; the fix applied then preserved the ambiguity but
introduced meta-commentary ("I noted I'd take care of it") and an invented
causal link ("since Greg is frequently late"), neither of which existed
before. Both survived two further review passes and were only found when batch
9's widened voice pattern was run over the corpus.

Cheap way to run this: dump one field for every example in a category and
read the column, rather than reading examples one at a time.

```bash
# by batch — the primary axis. Adjust the slice to the batch under review.
python -c "
import json
rows = [json.loads(l) for l in open('datasets/synthetic.jsonl', encoding='utf-8') if l.strip()]
for i, r in enumerate(rows[101:], 102):
    print(i, '|', r['category'][:20].ljust(20), '|', r['output']['narrative'][:70])
"

# and a standing regression check for this specific drift.
#
# The regex that lived here until 2026-08-25 tested for BANNED SURFACE FORMS
# ("the author", "I noted", openers starting "Notes|Dictated|..."). It scored
# 1 hit on a 141-record corpus that a positive test found 15 defects in -- and
# that single hit was a FALSE POSITIVE, matching "the authorization form" on an
# unbounded `the\s+author`. Zero true positives. Banning forms by name is the
# same losing game §4's "Representing an absence" describes: each ban teaches
# generation the next surface form, and the check goes quiet while the corpus
# gets worse. TEST FOR THE PROPERTY YOU WANT, NOT THE FORMS YOU HAVE SEEN.
#
# (1) POSITIVE TEST -- the load-bearing one. A narrative in the writer's own
# voice essentially always contains a first-person pronoun. This catches
# subject-elided third person ("Needs to check if Adobe price increased"),
# which no banned-form list ever will.
python -c "
import json, re
rows = [json.loads(l) for l in open('datasets/synthetic.jsonl', encoding='utf-8') if l.strip()]
fp = re.compile(r\"\b(I|I'm|I'd|I'll|I've|my|me|mine|we|we're|our|us)\b\", re.I)
for i, r in enumerate(rows, 1):
    if not fp.search(r['output']['narrative']): print(i, r['category'], '|', r['output']['narrative'][:70])
"

# (2) Same property, applied to bullets and action_items. Third-person leads
# only; \"Need to X\" is elided first person and is the corpus register.
# Two shapes: subject-led (\"Needs to check X\") and passive with no subject
# at all (\"X must be checked\"). The batch-12 re-review (2026-08-25) found
# only the first shape was ever checked -- the passive shape had 19 lines
# across 18 records corpus-wide, invisible to this script for weeks. The
# eighth re-review (2026-09-01) found the passive check itself only matched
# regular \"-ed\" participles (\"X must be checked\") -- an IRREGULAR participle
# (\"X must be told/given/sent/drawn/found/written...\") is just as passive
# and just as subjectless, but slipped through \\w+ed\\b entirely. 10 lines
# across 10 records corpus-wide, some dating to early batches, invisible for
# the same reason the first gap was: the check enumerated a verb SHAPE
# instead of testing for the grammatical pattern itself.
python -c "
import json, re
rows = [json.loads(l) for l in open('datasets/synthetic.jsonl', encoding='utf-8') if l.strip()]
third = re.compile(r'^\s*(Needs to|Plans to|Intends to|Wants to|Feels|Suspects|Hopes|Thinks|Finds|Has to|Notes)\b')
irregular_pp = r'(told|given|shown|taken|written|sent|done|made|seen|said|kept|held|brought|bought|sold|left|put|set|cut|known|found|read|paid|broken|chosen|driven|drawn|thrown|worn|torn|spoken|forgotten|frozen|hidden|ridden|risen|sworn|woken|beaten|bitten|blown|born|built|burnt|caught|dealt|dug|fed|felt|fought|flown|forbidden|forgiven|gotten|grown|hung|hurt|laid|led|lent|lit|lost|meant|met|proven|sought|shot|shut|slept|slain|spent|spun|spread|stolen|struck|swept|swum|taught|understood|upset|withdrawn)'
passive = re.compile(r'^\s*(The\s+\w[\w\s]*?|All\s+\w[\w\s]*?|\w[\w\s]*?)\s+(must|needs?|has|have|is|are)\s+(to\s+)?be\s+(\w+ed|' + irregular_pp + r')\b', re.I)
for i, r in enumerate(rows, 1):
    for f in ('bullets', 'action_items'):
        bad = [x for x in r['output'][f] if third.match(x) or passive.match(x)]
        if bad: print(i, r['category'], f, bad)
"

# (3) Meta-commentary: the output reporting ON the note instead of being it.
# Note \b on author/writer/speaker -- without it this matches \"authorization\".
# KNOWN FALSE POSITIVE: #98 opens \"Notes for the historic society article:\"
# because its INPUT dictates exactly that. Flagging a note's own words is the
# kind of false positive that teaches a reviewer to skim; verify before acting.
python -c "
import json, re
rows = [json.loads(l) for l in open('datasets/synthetic.jsonl', encoding='utf-8') if l.strip()]
bad = re.compile(r\"[Tt]he\s+(author|writer|speaker)\b|I (?:\w+ly )?(?:noted|wrote|stated)|contradict\w*|didn't finish|lost my train|got distracted|my planning was|was brainstorming|[Tt]he note (cuts off|is abruptly|breaks off)|thought was (left )?(incomplete|interrupted)|opinions were shared|^\s*(Dictated|Voice-recorded|Rambling|A (brief|short|basic) (note|reminder))|[Tt]hese are my notes\", re.I)
for i, r in enumerate(rows, 1):
    if bad.search(json.dumps(r['output'], ensure_ascii=False)): print(i, r['category'])
"

# (4) COPY RATIO -- the one check in this section that is a real script
# rather than an inline one-liner, because it needs an allowlist and a
# non-zero exit code. See the copy-ratio bullet above for why it exists.
# Run it on every batch; it gates on the whole corpus, not just the new
# records, because the failure it catches is drift across batches.
python training/check_copy_ratio.py
```

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
| 2026-08-23 | 13 examples (batches 7–8), weighted toward `topic_switching` (4 — the category with the most historical relabels) and `voice_to_text_artifact` (2), plus the 3 batch-8 examples touched during first-pass review (reviewer not told which) and 3 never-flagged controls | 2 ACCEPT, 11 FIX, 0 REJECT — plus 1 REJECT and 2 difficulty relabels added on reconciliation | **Found a failure mode none of §4's bullets named: *world-knowledge frame completion*** — the output names an activity, venue, or object class that `input` only implies through its props ("sleeping bag" + "camp stove" → "camping trip"; honey + carboy → "blackberry mead or wine"; "chapter 4" → "chapter 4 of the book"; "primary mirror" → "primary telescope mirror"). 7 of 11 fixes shared this root cause. It survives review precisely because the inference is usually *correct*, and it is distinct from invented causality (no new event asserted) and invented certainty (no hedge smoothed). Added as its own §4 bullet. The reviewer also identified a cheap detector — **the three output fields disagree with each other** when an invention is present (bullets said "for Saturday" where the narrative said "camping trip"; `action_items` reinstated a retraction the narrative had correctly honored) — added as a second new §4 bullet. Notably the first-pass reviewer had *seen* two of these instances and explicitly waved them through as acceptable inference: the blind spot was not failing to notice the instances but failing to recognize them as one mechanism. A third gap — no rule governing what qualifies as an `action_item` — was surfaced to the product owner, who settled it (any named person's commitment, attributed; not past events) and it is now a §4 bullet and a `DATASET_SPEC.md` rule. One finding was a **false positive**: a claimed U+FFFD corruption was a clean U+2014 em dash rendered through a cp1252 console, verified by codepoint dump across the whole corpus; the suggested encoding grep was still adopted into §1, with a note about verifying by codepoint rather than by eye. Dispositions: 9 clear-cut §4 fixes and 8 frame-completion fixes applied in place; `zero_action_items` #107 relabeled `expert`→`medium` and `voice_to_text_artifact` #97 `expert`→`hard` (both single-thread notes failing the tier definition's "dense combination of categories"); one `interrupted_thought` example rejected outright and parked for regeneration — nothing in it was actually cut off, so it taught none of the unfinished-vs-resumed judgment the category exists for. Corpus 116 → 115. Next run due after batch 10. |
| 2026-08-23 | 13 examples (batches 9–10), weighted toward `voice_to_text_artifact` (3, the most-fixed category this arc), plus the 6 examples touched during first-pass review and 4 never-flagged controls; the reviewer was additionally asked to judge whether §6b earns its place, since every check in it had been written *after* the fact and none had ever found anything new | 3 ACCEPT, 9 FIX, 1 REJECT, plus 4 difficulty relabels and 3 defects found outside the sample | **The most productive run of this exercise so far, and the first to find a defect in the checklist's own incentives.** Headline finding: **`narrative` has an upper bound but no lower bound.** Every §4 bullet is a prohibition on *addition*, so a narrative that copies `input` verbatim passes the entire checklist trivially — inventing nothing, losing nothing and smoothing nothing precisely by doing nothing. Measured input→narrative similarity climbed from a batch 1–7 mean of 0.50 to 0.67 across batches 8–9 as the evidence rules were tightened: generation had found the safe gradient the rules created. Two narratives sat at 0.97–0.98. Added as §4's "No non-recovery" bullet — the first §4 item that is not a prohibition. Second finding: **meta-commentary is not a mutating voice bug but the predictable symptom of an unsolved representation problem.** Three categories (`interrupted_thought`, `contradictory_statement`, `dangling_reference`) ask the output to convey an *absence*; no field has a device for that, so generation describes the note instead. Confirmed: the only meta-commentary hits corpus-wide were all `interrupted_thought`. Banning each new phrasing had produced four successive surface forms. Replaced with a **convention** — preserve the note's own broken-off text verbatim (`"Print the—"`) — which is the note rather than a report about it. Third: **two §4 rules contradicted each other** ("every fragment must appear" vs. `voice_to_text_artifact`'s "don't annotate the noise"), and two examples answered both ways at once; now resolved with an explicit artifact exception. **§6b was vindicated and corrected in the same run.** It found two things items 0–5 cannot reach: bullet terminal punctuation ran 0% in batch 9 and 100% in batch 10, perfectly and oppositely uniform (normalized corpus-wide to bare list items per `DATASET_SPEC` line 68, 274 periods stripped); and the `interrupted_thought` meta-commentary cluster. But its own bolded advice to "check by batch first" was wrong — generalized from one incident — and would have diluted the second finding across three batches. Batch and category are two *different* generators (prompt artifact vs. structural pressure from the category) and neither is primary; §6b rewritten to say so, and given the two axes it was missing, copy ratio and difficulty calibration. Both are purely comparative and therefore invisible per-example — the proof case being #127 and #128, the same note with different nouns carrying different difficulty tiers in the same batch. Also caught: the standing regression grep only scanned `narrative`, and widening it to all three fields immediately found 8 third-person bullets in 7 records that the earlier corpus-wide voice sweep had missed entirely. One rejection (#122): verbatim narrative, two flatly contradictory imperatives in `action_items` that would have a user feed a dog 1½ scoops, and no mood or intention *shift*, so it was never the category — a reversal of the first pass's "borderline, keep it" call, surfaced to the product owner per the reconciliation rule and agreed. **Still open, deferred to the product owner**: what `action_items` should do when a note commits to two incompatible things. The reviewer correctly declined to invent a convention; rejecting #122 removed the only instance, so it is documented rather than decided. Next run due after batch 12. |
| 2026-08-25 | **Calibration run, not a periodic re-review** — 12 examples, blind, half known defects pulled from this session's own pre-fix git history (not invented), half untouched controls; identical prompt sent to Gemini and to a fresh Claude agent independently, neither shown the other's output nor this conversation, per the double-review design in `PDR-006`'s "Revisit if..." clause | Gemini: 5/6 known defects caught, 1 missed. Claude (fresh agent): 2/6 caught, 4 missed | **The four Claude misses are exactly the three defect classes this session spent all day fixing** — third-person narrative voice, third-person bullets, non-recovery — including one (subject-elided third-person bullets, "Needs to verify...") using close to the checklist's own example phrasing, quoted verbatim in the prompt the agent received. This is the correlation-bias risk `PDR-006` named as the reason for this whole exercise, observed directly rather than inferred: a same-family reviewer under-suspicious of its own family's characteristic failure. Gemini independently derived the *correct mechanism* on every one of its 5 hits, in the checklist's own vocabulary, not just "something's off." Both reviewers missed the same example (meta-commentary, `contradictory_statement`) — uninformative at n=1, consistent with either "genuinely borderline" or "shared blind spot." **Unplanned finding**: two records treated as clean controls (#78, #1) were independently flagged by one or both reviewers on defensible grounds; human read confirmed #78 as a genuine frame-completion defect ("interview" never stated, only implied by "python migration"/"architecture question"/"system design") and fixed it, and confirmed a smaller invented-chronology defect in #1 ("Afterward") while declining a second claim on the same record (an alleged "blue suit" ambiguity, judged to be an ordinary reading of a flat list, not the same class as a genuine two-way referent). A third finding, on a record already known to be defective (#125, this session's non-recovery fix), held up on inspection: `action_items` still presented two mutually-contingent tasks (curry ingredients vs. pasta ingredients) as flat and certain, missed because only the narrative had been touched by the earlier fix — also corrected. **Adopted, single-run caveat stated explicitly**: the next periodic re-review (due after batch 12, already slated to sample examples edited this session — the worst case for a same-family check) gives Gemini first pass on the full 0–8 checklist, Claude second, per the existing disagreement-is-the-signal design — not a replacement of Claude from the loop off one 12-example run. See `PDR-006`'s 2026-08-25 amendment. |
| 2026-08-25 | 13 examples after batch 12, **first re-review run under the amendment above — Gemini first, full 0–8 checklist**: 7 examples edited or relabeled during this session's own first-pass review (the worst-case stratum the calibration flagged), 6 never-touched controls, weighted toward `dangling_reference`/`self_correction`/`contradictory_statement`/`zero_action_items` | Gemini: 6 ACCEPT, 7 FIX, 0 REJECT, plus 3 6b findings (1 confirmed corpus-wide, 2 declined) | **The second data point the amendment asked for, and it held up — Gemini found real defects Claude's own first-pass review had missed minutes earlier**, including one in an example Claude had just fixed. Two were narrow: `#142`'s new action-item phrasing was ambiguous enough to misread as claiming the (scarf-only) chunky wool applied to the blanket too — fixed. `#154`'s narrative/action_items invented a governing verb ("decide on"/"Get") for a referent ("the blue one") whose verb `input` never states — carried the bare referent through instead, matching `#140`'s established convention. One was a genuine category mismatch this session's own review missed: `#153` (the homepage-dev note) was labelled `contradictory_statement`, which requires an unresolved tension preserved verbatim — but the note is a mistaken belief that gets corrected within itself and resolves to one consistent stance, which is `self_correction`'s shape, not `contradictory_statement`'s. Relabeled; Gemini's own reasoning on a different example (`#165` — "`self_correction` is not one of the three categories requiring verbatim preservation, so narrating the pivot is allowed") independently confirms the relabel is what makes the existing narrative correct. `#163` correctly caught an inferred-frame violation this session's own review missed — "the basement drywall" narrated as "*my* basement drywall," an unstated possessive (the writer could be a contractor or inspector, not necessarily the homeowner) — but the fix itself briefly introduced a *new* defect: removing "my" stripped every first-person pronoun from the narrative, regressing exactly the voice defect fixed corpus-wide earlier the same day. Caught by re-running the standing checks immediately after applying the fix, per this section's own "re-check the full checklist, not just the item that prompted the correction" rule — worth naming as direct proof that rule is not just recording something already secured before now, but working. **The 6b finding with the largest blast radius: a standing blind spot in the field-register regression check.** The check only ever tested for *subject-led* third-person bullets ("Needs to check X"); Gemini's flag on `#151` ("The knock box must be emptied", passive, no subject at all) was a different grammatical shape the regex had never covered. A corpus-wide scan for the pattern found **19 lines across 18 records, spanning nearly every category** — not confined to today's batches, going back to early single-digit corpus indices. All rewritten to active/imperative, matching the register `action_items` already used correctly throughout (the defect concentrated entirely in `bullets`); the check itself widened to catch both shapes going forward. **Two findings read, declined, and recorded rather than silently dropped**: `#155`'s "wipe it" flagged as ambiguous between the USB and the envelope — declined, since "wipe" pragmatically constrains to the USB (a data-erasure reading) strongly enough that "the envelope" isn't a *plausible* second reading by the checklist's own stranger-test, not just an unlikely one. `#157`'s "make sure the slide deck has the updated margins" read as a verification task, versus the output's "update the slide deck" read as an authoring task — declined as ordinary inference for someone presenting their own deck, distinct from the frame-completion pattern the rule targets (naming a venue/occasion/domain the input only implies through props). A third 6b claim — that domestic-chore and grocery-list *themes* recurring across examples constitutes scenario-well over-reliance — declined outright: the flagged examples (Saturday home chores vs. a cafe's closing checklist; "eggs" appearing incidentally in two unrelated notes) don't share an actual situation, only a broad household-task theme, which doesn't meet this project's established narrow definition of a scenario well (a specific recurring situation, not a category of situation). **`#151` also lost its `expert` difficulty tag**, downgraded to `hard`: `TAXONOMY.md` defines `expert` as a dense *combination of categories* with branching or restated content, and this is a long flat enumeration with a few appended exceptions — structurally identical to `#150` (already `hard`), differing only in raw length, which the definition doesn't credit. This leaves `simple_list` without an `expert` example again, the same open gap `minimal_fragment` has for `hard`/`expert` — a third instance of the same underlying finding as batch 8's `topic_switching`/`expert` conflict: a requested difficulty tier can structurally contradict what a category is actually built to hold, and a future batch needs a differently-shaped instruction, not just another attempt. Next run due after batch 14. |
| 2026-09-01 | 14 examples after batches 13-14, sixth periodic re-review — Gemini first against the full 0-6b checklist, then a genuinely fresh Claude subagent (spawned with no exposure to this session's reasoning) as the second, independent pass, per `PDR-006`'s amendment. 10 examples touched (relabeled or fixed) during batches 13-14's own first-pass review — the worst-case stratum — plus 4 never-touched controls | Gemini: 2 ACCEPT, 11 FIX, 1 REJECT-severity (treated as FIX). Fresh Claude: 6 ACCEPT, 8 FIX. Reconciled: 7 confirmed fixes, 0 relabels, several of each reviewer's claims declined | **The two independent passes disagreed with each other on 6 of 14 examples, and reconciling the disagreement — not either pass alone — is what found the real defects.** Gemini ran hot: 11 of 14 flagged, including several claims that contradicted this project's own settled precedent (extending the verbatim-preservation "representing an absence" convention to `self_correction`, which `REVIEW_GUIDE.md`'s own fifth-re-review log already excludes; flagging gerund/noun-phrase bullets like "Feeling tired of X" as a register violation when that shape is the corpus's own sanctioned convention, not one of the two actually-documented banned shapes). The fresh Claude pass, given the same checklist with those two boundaries stated explicitly, correctly held the line on both — confirming the value of stating a settled precedent in the prompt rather than trusting a reviewer to have absorbed project history it never saw. **Where the two passes agreed, both were right**: a `simple_list` example had silently merged two input fragments ("buy caffeine" / "get coffee again") into one item across bullets *and* action_items, asserting an equivalence `input` never states — reverted to two separate items. A `multi_person_note` example flattened "David said he would pay for the drinks" (reported speech, a hedge) into the flat action item "David to pay for the drinks" — the exact ownership-hedge failure mode this file names by example — hedge restored. A `long_rambling` example opened its narrative with "These are my notes from the website redesign meeting" — the specific banned meta-framing form named in this file's history (`"Notes on houseplant care…"` is the same shape) — rewritten, and the standing regression regex widened to catch this exact phrase going forward. An `interrupted_thought` example inferred "my partner" from the input's bare "honey" — a relationship the input only implies through a term of address, the same class of violation as "sleeping bag" → "camping trip" — reverted to the input's own word. **Two findings came from only one pass each and held up anyway on inspection — the reconciliation step doing real work, not just averaging two votes.** The fresh Claude pass alone caught that a `self_correction` example's narrative dropped an entire stated fragment: the input gives *two* separate objections to 2pm ("actually 2pm is no good" — reason never stated — and "3pm conflicts with the all-hands"), and the output kept only the second, silently erasing that the first objection was ever raised; restored as its own bullet. The fresh Claude pass alone also caught that a `rapid_branching`/`expert` example was a single mechanism (nested conditionals) with no second category's structure genuinely combined — exactly the "structural ceiling on `expert`" principle this session wrote into `TAXONOMY.md` two batches earlier, independently re-derived by a reviewer who had never seen that write-up; downgraded to `hard`. **One finding needed real judgment rather than a mechanical fix.** A `contradictory_statement` example ("book the Japan flights... don't book *them* yet... maybe book *them* anyway... leave the tab open") has a genuinely ambiguous "them" (flights or hotels, both plural, both recently mentioned) that the original output silently resolved to "hotels," while `action_items` dropped the stated flight-booking intent entirely without ever contradicting it. This is the same open question the fourth adversarial re-review surfaced and left for the product owner — what `action_items` should do when a note's own ending swallows an earlier stated intent into unresolved indecision, without an explicit retraction. Resolved narrowly for this instance (kept "them" genuinely ambiguous in the narrative rather than naming a referent, and left `action_items` at the note's actual behavioral outcome — nothing got booked, so "leave the tab open" stands alone) without generalizing a rule, per that still-open question's own disposition. **One finding read and left undecided rather than forced either way**: both reviewers separately flagged the same `interrupted_thought` example (paint color / oven-check aside / return to paint) on different grounds — Gemini on voice, the fresh pass on category fit, arguing nothing in it is literally cut off mid-clause the way the category's own worked example is. Neither specific complaint held up on its own (the voice reading conflates ordinary first-person recounting with describing-the-note; no better-fitting category exists among the 15 for "a fully-resolved aside interrupts and the note returns to the original point"), but two independent reviewers flagging the same record for different reasons is itself the disagreement-is-the-signal pattern this process exists to catch — recorded as a borderline instance worth watching rather than silently cleared, not relabeled since nothing else fits better. Full three-check voice-regression suite, schema validation, and duplicate check all clean at 203/203 after the 7 fixes. Corpus 203 → 203 (no rejections, no relabels — every fix was in-place). Next periodic re-review due after batch 16. |
| 2026-09-01 | 13 examples after batches 15-16, seventh periodic re-review — Gemini first against the full checklist, then a genuinely fresh Claude subagent (no exposure to this session's reasoning) as the independent second pass, per `PDR-006`'s amendment. 7 examples touched (relabeled or fixed) during batches 15-16's own first-pass review, 6 never-touched controls. Gemini's API returned three consecutive `503 UNAVAILABLE`/`fetch failed` errors before a fourth attempt succeeded — the most retries any call this session has needed | Gemini: 2 ACCEPT, 7 FIX, plus systemic over-flagging on "invented causality" (7 of 13 examples). Fresh Claude: 9 ACCEPT, 4 FIX (3 of which match Gemini's non-causality findings exactly). Reconciled: 3 confirmed fixes | **Gemini ran hot in a specific, identifiable way this run: it flagged ordinary causal connectives ("so", "since", "because") as "invented causality" in 7 of 13 examples, even where the input's own text already stated that exact reasoning** ("it's basically empty right now" as the stated reason for buying more flour; "needs dry cleaning first" as the stated reason for leaving a sweater). The rule targets asserting a relationship between fragments that are actually unrelated — adjacency between two facts already part of the same stated thought is not the violation it's written to catch. The fresh Claude pass, given the same checklist with that boundary stated explicitly, independently reached the identical accept/fix split on all but one soft note — strong convergence, and a clear instance of a reviewer extending a real rule past its documented scope at volume rather than on one example. **The 3 fixes both passes converged on, independent of the causality noise, were all real**: a `self_correction` example (Chicago packing, two coat/sweater pivots) was tagged `expert` for what both reviewers independently identified as a single mechanism run twice — sharper this time because another record in the *same sample* (the sage-green/mint paint example) is the identical category at the identical complexity and was already correctly capped at `hard`, making the inconsistency directly comparable within one batch of 13 rather than requiring corpus-wide memory. Downgraded to `hard`. An `interrupted_thought` example (Q3 goals document, literal `"by--"` mid-clause cutoff) had its broken-off text smoothed into a complete, grammatical sentence in every field — the exact case the "representing an absence" convention exists to prevent, missed during batches 15-16's own review because the *causal story* (laundry interrupting drafting) reads as obviously recovered even though the literal broken text never survives anywhere. Fixed by preserving `"by--"` verbatim in the narrative and a bullet. A `topic_interleaving` example (gym membership / quarterly report) narrated `"For work, I need to draft the quarterly report..."` — a domain label `input` never states, matching the checklist's own worked example of a banned inference almost verbatim, missed during first-pass review despite being the single clearest defect in the sample by both reviewers' independent read. Fixed by removing the frame. Full three-check voice-regression suite, schema validation, and duplicate check clean at 239/239 after the 3 fixes. Corpus 239 → 239 (no rejections, no relabels this round — every fix in place). Next periodic re-review due after batch 18. |
| 2026-09-01 | 13 examples after batches 17-18, eighth periodic re-review — Gemini first against the full checklist, then a genuinely fresh Claude subagent (no exposure to this session's reasoning) as the independent second pass, per `PDR-006`'s amendment. 7 examples touched (relabeled/fixed) during batches 17-18's own first-pass review, 6 never-touched controls. Also the first re-review to open with a self-directed catch before the formal sample was even sent out (see below) | Gemini: 9 ACCEPT, 2 FIX, 2 REJECT-severity. Fresh Claude: 11 ACCEPT, 2 FIX, 0 REJECT. Reconciled: 2 confirmed fixes from the sample, plus 10 corpus-wide fixes from the pre-review catch | **Before assembling the sample, re-reading one of its own candidate records surfaced a corpus-wide gap independently of either reviewer**: the fifth re-review's passive-voice regression check (added 2026-08-25) only ever matched regular `-ed` past participles ("X must be checked"); an irregular participle ("X must be told/given/drawn/sent/found/written...") is the identical passive-with-no-actor shape but a different verb morphology, and slipped through `\w+ed\b` entirely. A corpus-wide scan found **10 lines across 10 records, spanning nearly every category, some dating to early batches** — the same "detector enumerates a shape instead of testing the underlying pattern" mechanism as the original October discovery. All 10 rewritten to active voice; the standing regex widened to cover both regular and irregular participles in one pattern. **The formal sample then produced the widest Gemini/fresh-Claude divergence of any re-review so far**: Gemini flagged 4 of 13 examples (2 REJECT-severity), and on inspection all 4 were overreach the fresh pass independently declined — extending the banned-bullet-shape rule to ordinary declarative sentences with explicit subjects that don't match either documented shape ("Dave is responsible for bringing the PA system", "Thursday practice requires specific gear"); misreading a stative "mopping is left for the morning crew" as a modal-passive obligation, which requires the literal verb "be" the sentence doesn't have; claiming a `voice_to_text_artifact` example lost content by not keeping "comma"/"period" as literal text, directly contradicting this project's own documented noise-exception for that category (traced back to an incomplete checklist this round's reviewer prompt sent to Gemini — an omission on this session's part, not a new Gemini failure mode); and calling an unassigned "someone needs to email the prof" wrongly "assigned" when it was correctly kept as a bare, unattributed action item. **Both passes agreed on two real, different findings.** A `topic_switching` example (vacuum the stairs / clean the sink / order pet food) is actually three independent, unrelated items — A-B-C, not a coherent two-subject A-A-B transition — relabeled to `simple_list` rather than stretching the category's own strict definition to fit. A `long_rambling`/`expert` example (three hours staring at a canvas, several small decisions and a repeated item) was tagged `expert` for what both reviewers concluded is a single mechanism — rambling drift and internal repetition are native features of *how the category works*, not a second, distinct structure layered on top — downgraded to `hard`. **Explicitly confirmed rather than merely accepted**: a `voice_to_text_artifact`/`expert` example (a destination self-correction treated as noise, a drive-vs-fly deliberation treated as real content) was specifically re-examined per this session's own request and both mechanisms verified as genuinely distinct and correctly handled differently — the difficulty tag holds, unlike the painting-canvas example carrying the same nominal tag for a shallower reason. Full three-check voice-regression suite (now including the widened passive check), schema validation, and duplicate check clean at 275/275 after all 12 total fixes this round. Corpus 275 → 275 (no rejections — every fix in place, including the two from the pre-review catch). Next periodic re-review due after batch 20. |
| 2026-09-01 | 14 examples after batches 19-20, ninth periodic re-review — Gemini first against the full checklist, then a genuinely fresh Claude subagent (no exposure to this session's reasoning) as the independent second pass, per `PDR-006`'s amendment. 2 examples touched (fixed) during batch 20's own first-pass review, 12 never-touched controls, deliberately weighted toward the batch's own `expert`-tagged examples since that tier has been the most recurring finding all session | Gemini: 5 ACCEPT, 8 FIX, 1 REJECT-severity, plus a blanket claim that 6 `expert` tags were miscalibrated. Fresh Claude: 5 ACCEPT, 9 FIX, 0 REJECT, with a narrower and better-supported 5-example calibration claim. Reconciled: 5 confirmed difficulty downgrades, 7 confirmed content fixes | **The sharpest, most convergent reconciliation this project has run — both passes independently found the same core defects, described more precisely by the fresh pass each time.** Both flagged the same two inferred-frame violations, matching this project's own canonical examples almost exactly: a `multi_person_note` narrative invented "community" for a note that only ever said "cleanup day," and a `topic_interleaving` narrative invented "cooking dinner" for a note that only ever listed boiling rice, checking stove heat, and chopping onions. Both independently found a hedge-dropping pattern spanning 4 examples: a `long_rambling`/`kitten` action item flattened "not sure... Tuesday or Wednesday" into a bare "Schedule the vet check for Tuesday or Wednesday"; a `rapid_branching`/home-hub example dropped "maybe" twice converting hedged intentions into flat commands; a second `long_rambling`/recipe-box example dropped "I think I should" from a scan-the-cards action item; a `time_ambiguous`/picture-frame example's *bullets* field stated "the backing fee" as settled when its own narrative correctly hedged "possibly" — the same defect the fifth re-review named by title ("check the field itself, not just whether the narrative got it right") recurring in a new field five re-reviews later. All 7 fixed with minimal, faithful hedge restoration or frame removal. **The two passes diverged sharply on `self_correction`, and the divergence is instructive.** Gemini REJECTed the antique-fair-directions example on the theory that the input's retracted "turn left" and dictation noise ("period," "erase that") must survive somewhere in the output — directly contradicting this project's own settled, non-negotiable convention that `self_correction`'s entire purpose is dropping retracted content, not preserving it. The fresh pass, given that exemption stated explicitly, found the *actual* defect instead: the narrative said "exit 15, rather than 14," reintroducing the retracted number that `bullets` and `action_items` correctly already dropped — a genuine field-disagreement, narrower and better-targeted than Gemini's blanket claim. Fixed by removing the reintroduced number from the narrative alone. **On `expert`-difficulty calibration, the fresh pass's example-by-example reasoning proved more reliable than either its own blanket instinct or Gemini's.** Gemini claimed 6 examples were single-mechanism; the fresh pass, checking each individually against the specific two-nameable-elements standard, confirmed only 5 of those (a branching-plus-one-hedged-line software rollout, the kitten rambling note, a repeated wool order with one incidental unresolved referent, a reptile-expo disagreement — newly caught, not previously suspected — and the self-correction example), while explicitly *defending* three others Gemini had also flagged: a `multi_person_note` combining 3+ named people at genuinely different certainty registers (a stated fact, a reported hedge, a stated expectation, plus an unassigned task) is exactly the carve-out this project's own difficulty rule names for that category, not density; a second `multi_person_note` combining a literal interruption with mixed registers; and the `topic_interleaving` example's branching conditional (Python-version-vs-library) genuinely combining with the interleaving structure. 5 downgraded to `hard`, 4 confirmed as correctly `expert`. Full three-check voice-regression suite, schema validation, and duplicate check clean at 325/325 after all 12 fixes. Corpus 325 → 325 (no rejections, no relabels — every fix in place). Next periodic re-review due after batch 22. |
| 2026-09-01 | 14 examples after batches 21-22, tenth periodic re-review — Gemini first against the full checklist, then a genuinely fresh Claude subagent (no exposure to this session's reasoning) as the independent second pass, per `PDR-006`'s amendment. 9 examples touched (relabeled/fixed) during batches 21-22's own first-pass review, 5 never-touched controls | Gemini: 2 ACCEPT, 12 FIX, plus a systemic invented-emotion-label claim across 6 examples. Fresh Claude: 5 ACCEPT, 9 FIX, a narrower 4-example invented-emotion claim plus 3 of its own new findings. Reconciled: 9 confirmed fixes | **A new, previously-undiscovered systemic pattern, caught because Gemini's blanket claim was specific enough to check rather than dismiss outright.** Both passes independently found that this batch's own emotional-state diversity instruction ("cover: serene, frantic, curious, ... sheepish, ... spent") had created pressure to invent a named feeling with zero textual basis, in the same shape three times: `minimal_fragment` ("need sleep now" → narrative added "because I am completely spent"), `self_correction` ("Mark's couch" → narrative added "I feel sheepish because..."), and `voice_to_text_artifact` ("blog domain" → "I am confident and ready," "Launching the new blog confidently"). All three phrases were removed rather than reworded, since the input gives literally no seed for them. A fourth candidate (`self_correction`/duck-pond, "I am feeling serene") was correctly **declined by the fresh pass and, on inspection, rightly so** — the input's own "it's just so peaceful here" is a direct textual seed, making "serene" a close paraphrase rather than an invention; a fifth (`time_ambiguous`/server-migration, "preparing confidently") was declined the same way ("fully prepared" already implies it). **This distinction — a feeling with zero textual seed versus a close paraphrase of one the input already states — is now the operative test, not "does this word appear in the input."** Two more content fixes: a `long_rambling` example asserted a uniform "tonight" for milk-disposal and general fridge-emptying when the input only explicitly times the leftovers that way; reworded to keep the specific timing where the input actually states it. A separate `long_rambling` example's hedge "I think I just need to stop and make a cup of tea" had been converted into the action item "Think about stopping to make a cup of tea" — changing the actual task from *doing* the thing to *thinking about* it, a distinct defect from a plain dropped hedge; restored to "Probably stop and make a cup of tea." **On difficulty calibration, the fresh pass caught two `expert` overclaims Gemini itself hadn't precisely named.** A `voice_to_text_artifact` example's mistranscription fumbling and its correct resolution are *both manifestations of the same single category mechanism* (transcription noise), not two distinct combined structures — downgraded to `hard`, correcting this session's own earlier judgment that "self-correction-style name recall" counted as a second element when it doesn't. A `multi_person_note` example was tagged `expert` under this category's specific "3+ named people, mixed certainty" carve-out, but literally only 2 people were named (Mark, Chloe) — the narrator's own unnamed "I" doesn't satisfy "named," so the carve-out's literal bar wasn't actually met; downgraded to `hard`. One `dangling_reference`/expert (single mechanism, no second combined element) was downgraded the same way both passes agreed on directly. **Two of Gemini's claims were confirmed as overreach by the fresh pass, both instructive.** Gemini argued a `voice_to_text_artifact` example should have preserved its mistranscription-fumbling fragments verbatim because the category field isn't literally "self_correction" — the fresh pass correctly identified that the noise-as-effect convention is a property of `voice_to_text_artifact` itself (one of its three documented artifact types is exactly this shape), not gated on the category label matching a different category's name. Gemini also argued that a `rapid_branching` example's hedged musings ("maybe I should go back to school," "perhaps... as a side hustle") shouldn't be `action_items` at all since nothing is truly committed to — directly contradicting this project's own settled, extensively-reinforced convention that a hedged intention belongs in `action_items` as long as the hedge itself is preserved. Full three-check voice-regression suite, schema validation, and duplicate check clean at 375/375 after all 9 fixes (one remaining flagged pair is the already-confirmed false positive from batch 21). Corpus 375 → 375 (no rejections, no relabels — every fix in place). Next periodic re-review due after batch 24. |
| 2026-09-02 | 12 examples after batches 23-24, eleventh periodic re-review — first run after the mid-batch-23 billing interruption. Gemini first against the full checklist, then a genuinely fresh Claude subagent (no exposure to this session's reasoning) as the independent second pass, per `PDR-006`'s amendment. 5 examples touched (fixed) during batches 23-24's own first-pass review, 7 never-touched controls | Gemini: 6 ACCEPT, 6 FIX. Fresh Claude: 8 ACCEPT, 4 FIX. Reconciled: 9 confirmed fixes, plus 2 corpus-wide fixes from a systemic follow-up check | **The most consequential finding of any re-review so far was a direct contradiction between the two passes over `repeated_reminder`'s own definition, settled by reading `TAXONOMY.md` itself rather than trusting either reviewer's paraphrase.** Gemini argued `#378` (topic_switching, an embedded restated "check ticketmaster") should have a *third* restatement added back as its own item. The fresh pass argued the opposite for `#416` (repeated_reminder itself, "wash the guest towels... seriously... today"): that splitting the restatement into two items — this session's own batch-24 review fix — directly contradicts the category's defined lesson. `TAXONOMY.md` line 37 settles it unambiguously: "Recognize a task/worry restated more than once ... as **one item, not two**." This means the fresh pass was right and Gemini's claim was overreach — and that **this session's own batch-24 fix to `#416` was itself the defect**, reverting Gemini's originally-correct single-item generation. Reverted. The same standard, applied for the first time as a genuine cross-example sweep rather than per-instance, found the identical shape in two more places: `#378` needed *merging* (the opposite of Gemini's request), and batch 23's landlord example (`#400`, 3 action items for one repeated instruction) had the same defect and had gone uncaught through that batch's own first-pass review. A full corpus-wide scan of every `repeated_reminder`-labeled record then found one more instance outside the sample entirely: `#220` ("buy more vitamins... don't forget... put that at the top of the list") had split the same vitamins reminder into two action items ("Buy more vitamins" / "Put vitamins at the top of the list") where "put at the top of the list" is emphasis on the same task, not a second one — the exact pattern `#88`'s correctly-collapsed "pay the dues" repetition (three restatements, one item) had already gotten right in the same scan. All four fixed to one item each. **A second, separate finding from the reconciliation**: both passes independently read the same ending shape two different ways on two different examples, and only the side-by-side comparison caught the inconsistency. `#387` ("I don't know if I should do green or just keep it white") correctly produced empty `action_items` — a state of indecision, not a stated intention. `#389` ("I can't decide if I want to get rid of it"), the identical ending shape, had `action_items: ["Decide if I want to get rid of it"]` — a task the input never actually states, left over from this session's own earlier batch-23 fix, which had correctly removed a firmer over-claim from that record but not gone far enough. Reverted to `[]` to match `#387`'s already-correct precedent. **Three more real, narrower fixes, one from each source plus one from cross-checking both against the input directly**: `#376`'s bullet ("Recalled an unfinished thought about whether Sarah sent dimensions for an unspecified thing") was meta-commentary describing the fragment instead of preserving it, while the record's own narrative correctly kept the input's broken-off text verbatim — both passes flagged this independently; rewritten to carry the fragment itself. `#384`'s bullet ("The presentation slides appeared fine") dropped the input's stated "I think" hedge that the record's own narrative had correctly kept — restored. `#396`'s bullet ("Want David to design the UI") read as a settled preference where the input only asks whether David wants the role ("Text David to see if he wants to design the UI") — reworded to "Ask David if he wants to design the UI." **`#377` lost its `expert` tag as a direct consequence of this session's own earlier batch-23 fix**: removing the record's return-to-subject-A line (correctly, per the zero-returns rule) also removed the only candidate for a second combined mechanism, leaving a single clean topic_switching with an ordinary hedge — not sufficient for `expert` under this project's own structural-ceiling principle. Downgraded to `medium`. **Two of Gemini's claims were declined as overreach, both on `#384`**: that "I suspect Kevin was just being pessimistic as usual" invents a hedge the input's flat "Kevin was just being pessimistic as usual" doesn't have — declined, since the input line is already a subjective character judgment, not a fact-claim, and recasting it as "I suspect" doesn't materially change its epistemic status; and that the record lacks a second `expert`-qualifying mechanism — declined, since the three-named-people, zero-commitment structure (Dana/Kevin/Maya) is exactly the `zero_action_items` + `multi_person_note`-shaped combination this project's own batch-23 targeting asked for. Full three-check voice-regression suite, schema validation, and duplicate check clean at 425/425 after all 11 fixes (9 from the sample plus the 2 additional `repeated_reminder` instances found by the systemic follow-up). Corpus 425 → 425 (no rejections, no relabels — every fix in place). Next periodic re-review due after batch 26. |
| 2026-09-02 | 13 examples after batches 25-27, twelfth periodic re-review — first run since the corpus hit the 500 target. Gemini first against the full checklist, then a genuinely fresh Claude subagent (no exposure to this session's reasoning) as the independent second pass, per `PDR-006`'s amendment. 8 examples touched (fixed) during batches 25-27's own first-pass review, 5 never-touched controls | Gemini: 8 ACCEPT, 4 FIX, 1 REJECT. Fresh Claude: 11 ACCEPT, 2 FIX. Reconciled: 2 confirmed content fixes, plus 1 scenario-repetition rework both passes found independently | **Both passes independently and strongly flagged the same scenario-repetition problem — a stronger signal than either verdict alone, since it needed no reconciliation.** `#473`, `#436`, and `#497`, three separate records in this 13-example sample, all center on deciding a paint color for a room — a third instance past this project's own two-per-scenario tolerance, and unlike prior scenario-well findings (car-maintenance, garden/tomatoes), found within a single review sample rather than only visible spread across many batches. `#497` reworked entirely to a different scenario (choosing a font for wedding invitations, with the same long_rambling + interleaved-unrelated-task structure that earned its `expert` tag) rather than `#473` or `#436`, per the fresh pass's reasoning that its lesson doesn't depend on the paint-specific content. **Two confirmed content fixes, both passes agreeing on one and the fresh pass narrowing the other.** `#431` (`repeated_reminder`/expert) split one restated worry — who calls the insurance broker — into two bullets, the same "one item, not two" violation the eleventh re-review settled by reading `TAXONOMY.md` directly; merged into one. `#449` (`self_correction`/expert) had its narrative and a bullet both narrate the retracted "email the vendor" plan instead of dropping it — checked against this session's own other `self_correction` fixes this session (boots 8→9, a meeting time correction, a chapter-number correction), all of which land directly on the final decision with zero mention of the retracted option, confirming this record as the outlier rather than the convention; both passes flagged it, fresh Claude at explicitly lower confidence, but the cross-check against established precedent settled it — fixed. **Two of Gemini's claims declined as overreach, both confirmed wrong by the fresh pass and by checking the input directly.** A REJECT on `#471` (`zero_action_items`/hard, therapist/dream-journaling) argued a hedged musing must produce an `action_items` entry — but the input's own closing line ("I really don't know if I'll actually do it") is a bare state of indecision with nothing actually committed to, the established exception to the hedged-musing rule, not an instance of it; correctly stays empty. A FIX on `#442` (`zero_action_items`/hard, sensory overwhelm) claimed "sensory input feels excessively loud" violates the no-diagnosis-framing rule — declined, since that rule targets naming an actual diagnosis or condition, not descriptive (if somewhat clinical-sounding) paraphrase; no diagnosis or label is named anywhere in the record. Full three-check voice-regression suite, schema validation, and duplicate check clean at 500/500 after all 3 fixes (the three standing flagged pairs are all already-confirmed false positives). Corpus 500 → 500 (no rejections, no relabels — every fix in place). Next periodic re-review due after batch 28. |

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
