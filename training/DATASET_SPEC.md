# Training data spec

This is the format `training/prepare_data.py` will expect, and the spec you
can hand to Gemini (or fill in yourself for real notes) to generate
examples.

**Mission (keep this in view for every example you write or generate):** help
people recover their own intent with as little cognitive and emotional
burden as possible. Not "organize notes." Not "summarize text." See
[`docs/vision/NORTH_STAR.md`](../docs/vision/NORTH_STAR.md).

## Data contract

The schema below is the **one authoritative format** for anything that
gets trained on. This format itself is unrelated to which AI generates the
data — it exists to match what the training pipeline and the deployed
model's output format (`###NARRATIVE###`/`###BULLETS###`/`###ACTIONS###`,
a small model's tokenizer can't reliably represent `{`/`}`, so a delimited
format is used instead of JSON for the model's actual output — though the
*dataset* itself is still stored as JSON/JSONL) actually require, not by
preference.

Before proposing a richer per-example format (additional fields,
restructured output, etc.), put it in
[`docs/datasets/DESIGN_NOTES_TEMPLATE.md`](../docs/datasets/DESIGN_NOTES_TEMPLATE.md)
instead — design notes carry boundary evidence, failure modes, and any
other analysis, and are never read by the training pipeline, so they're
free to be as rich as useful without risking rejection for not matching the
pipeline's actual schema.

## Model output serialization (the delimited format)

`prepare_data.py` converts each record's `output` object (JSON in the
dataset) into the literal text the model is trained to generate — the
delimited format named above. Designed fresh for v2.0, not inherited from
v1; [Thought Organizer](https://github.com/ThisIsJohnnyt/thought-organizer-app)
will be updated separately to parse it, not the other way around.

Exact shape — three section headers, always present and always in this
order, each on its own line, `bullets`/`action_items` as `- `-prefixed
lines (zero or more; an empty list means the header appears with nothing
after it):

```
###NARRATIVE###
<narrative, one paragraph, no literal newlines>
###BULLETS###
- <bullet 1>
- <bullet 2>
###ACTIONS###
- <action 1>
```

Empty `action_items` example (a `zero_action_items` record):

```
###NARRATIVE###
<narrative>
###BULLETS###
- <bullet 1>
###ACTIONS###
```

Rules:
- Headers are always present, even when a section is empty — a parser
  splitting on the three fixed markers never has to guess whether a
  section was omitted vs. genuinely empty.
- One list item per line, `- ` prefix, no trailing punctuation added
  beyond what the item text itself has.
- `narrative` must not contain literal newlines (it's a single paragraph
  per the data contract already) — `prepare_data.py` collapses any
  present to spaces as a defensive measure, not an expected case.
- Round-trip: `prepare_data.py` exposes both `serialize_target()` (dict →
  this text) and `deserialize_target()` (text → dict), so the same logic
  used to build training targets can validate model output at eval time.
- **The `\n` between sections above is a spec convenience, not something
  that survives to a real model.** flan-t5's SentencePiece tokenizer
  normalizes `\n` to a plain space at *encode* time — confirmed by
  tokenizing `"X\nY"` and `"X Y"` and getting identical token ids — so it
  is already gone from the training targets themselves, not just from
  generated output. A real checkpoint's raw output looks like
  `"###NARRATIVE### text ###BULLETS### - one - two ###ACTIONS### - a1"`,
  all on one line. `deserialize_target()` splits on the marker strings
  directly and then on `" - "` within each section, not on `\n` — found
  2026-08-25 when the first real eval run showed every example failing to
  parse despite visibly-correct, well-formed output; the parser was
  checking for a newline that no longer existed anywhere in the pipeline,
  not a model or data defect. Anyone reusing the model's raw generation
  output directly (rather than through `deserialize_target()`) needs to
  know this too.

## Task prefix (model input, not just the raw note)

`google/flan-t5-base` is instruction-tuned — fine-tuning it well means
feeding it an instruction, not just the bare scattered note, especially
valuable with a corpus this small (leans on its pretrained
instruction-following prior more than a larger fine-tuning run would need
to). `prepare_data.py` prepends a fixed prefix to every `input` before
tokenizing:

```
Recover the intent behind these scattered notes:

<input>
```

This is part of the model's actual input contract now, same status as the
output delimiters above — [Thought Organizer](https://github.com/ThisIsJohnnyt/thought-organizer-app)
must prepend the identical prefix at inference time, or the model sees
out-of-distribution input it wasn't fine-tuned on.

## File format

One JSON object per line (JSONL), UTF-8:

```json
{"input": "<raw scattered thoughts, as the user would actually type them>", "output": {"narrative": "<coherent flowing narrative>", "bullets": ["<key point 1>", "<key point 2>"], "action_items": ["<task 1>"]}, "difficulty": "easy|medium|hard|expert", "category": "<short label for the one lesson this example teaches>"}
```

Rules for `output`:
- `narrative`: rewrites `input` as a coherent narrative. Same meaning and tone as the input, just organized. Not therapy-speak, not generic — it should clearly be about the specific things mentioned in `input`.
  **The narrative must actually reorganize `input`, not echo it.** Reproducing the note in its original order with only capitalization and punctuation repaired is a defect, even though it violates none of the evidence rules — it passes them by doing nothing. Every evidence rule is a prohibition on addition, so echoing is their degenerate optimum; this is the counterweight. Added 2026-08-23 after the fourth adversarial re-review measured input→narrative similarity climbing as the evidence rules tightened.
  **Always written in the writer's own voice — first person, never third.** Never "the speaker needs to…", "the author notes that…", "dictated notes about…". The narrative reorganizes the note; it does not describe, classify, or comment on it. This applies to every category including `voice_to_text_artifact`, where the temptation is strongest: the lesson that category teaches is recovering intent *through* transcription noise, not annotating the noise. A narrative opening "Dictated notes containing spoken punctuation commands…" is describing the input instead of recovering it, and reads wrong to a user seeing their own note organized. Pinned 2026-08-23 after the drift below.
  *History*: `voice_to_text_artifact` narratives were first person in batches 2-3, drifted to third-person meta-description from batch 5 onward, and by batch 7 the drift was the category majority (5 of 8). No review pass caught it — including two adversarial re-reviews — because every check evaluates one example against its own `input`, and each of those narratives was individually defensible. All 5 were rewritten to first person on 2026-08-23. Cross-example consistency is not covered by the per-example checklist; see [`REVIEW_GUIDE.md`](../docs/datasets/REVIEW_GUIDE.md) §6.
- `bullets`: one short key point per source-supported idea in `input`, up to 7. **Written as list items, not sentences — no terminal period** (consistent with the `- ` prefixed serialization above, which adds no trailing punctuation). Pinned 2026-08-23: the corpus had drifted to 0% terminal periods in batch 9 and 100% in batch 10, and was normalized to bare list items throughout. Source-determined count — use fewer than 7 when `input` supports fewer ideas; never add, split, or repeat content to reach a target count. A one-idea input gets one bullet.
- `action_items`: concrete tasks/next steps mentioned in `input`. Use an empty array `[]` when the input has none — never invent one.
  **Ownership** (settled 2026-08-23, after the third adversarial re-review found the corpus teaching two conventions at once): an entry may be a task committed to by *any* person named in `input`, attributed to them — `"Uncle Bob to handle the catering"` is a valid action item, not only the writer's own tasks. A note-organizer that silently drops other people's commitments loses real planning information, and `multi_person_note` is a whole category. What does **not** belong is a past event carrying no forward commitment (`"Dr. Patel called"` is not an action item). A third party's expected arrival (`"plumber is supposed to come by"`) does belong, since it is a commitment — but it keeps its hedge, exactly like any other field.
- **No inferred setting or frame** (applies to all three output fields): never name an activity, venue, occasion, relationship, domain, or object class that `input` only implies through its props. "Sleeping bag" and "camp stove" do not license "camping trip"; "chapter 4" does not license "chapter 4 of the book". The inference is usually correct — that is exactly why it has to be checked deliberately rather than trusted. See [`REVIEW_GUIDE.md`](../docs/datasets/REVIEW_GUIDE.md) §4.

`difficulty` and `category` are optional annotations, not part of what the
model trains on — `prepare_data.py` will only read `input`/`output` and
ignore everything else, so adding them costs nothing and pays off later when
measuring accuracy per category instead of one aggregate number.

Three files:
- `datasets/synthetic.jsonl` — Gemini-generated examples (see prompt below).
- `datasets/real_validation.jsonl` — your real notes, same format, for
  **routine development-time evaluation**. Written entirely by hand — the
  product owner writes both the `input` and the `output`. **No generative
  model assists in drafting this file, not even to draft an `output` you
  then correct.** This is a deliberate tightening versus the predecessor
  project's spec, which allowed ChatGPT-assisted drafting here: the point of
  the "real" tier is to be uncontaminated by any generative model, not just
  by whichever model this project happens to be using at the time. Not
  trained on.
- `datasets/real_holdout.jsonl` — your real notes, same format, but
  **sealed for declared release milestones only** — never consulted for
  routine development, curriculum authoring, seed selection, or checkpoint
  tuning, and never generative-model-assisted, same as `real_validation.jsonl`
  above. Evaluated only by a separate, explicit holdout-evaluation script.
  Not trained on.

  **First split, 2026-08-25**, via
  [`training/split_real_holdout.py`](split_real_holdout.py): 27 real notes
  existed (all product-owner-authored, converted through
  `convert_real_notes.py`); 12 were sealed into `real_holdout.jsonl`, 15 stay
  in `real_validation.jsonl`. The product owner's own call, made deliberately
  early rather than waiting for the original ~35-40 target -- current volume
  still supports a holdout of value while he keeps adding examples.
  Seed `8112748308428165860`, drawn from `os.urandom()` at run time so no
  person (including whoever ran the script) chose it; shuffled with
  `random.Random(seed)` over the 27 lines in the order
  `convert_real_notes.py` wrote them. Sealed into `real_holdout.jsonl`
  (by original line index): 4, 5, 8, 9, 10, 11, 14, 18, 19, 21, 24, 26.
  Everything else stayed in `real_validation.jsonl`: 0, 1, 2, 3, 6, 7, 12,
  13, 15, 16, 17, 20, 22, 23, 25. Recorded here, not in either data file,
  because both are gitignored and this is the only durable record that the
  split was a genuine random draw.

  **Future real notes**, once converted, land in `real_validation.jsonl`
  only -- the holdout stays sealed and is not the intended target for
  `split_real_holdout.py`'s normal path (it refuses to run against a
  non-empty holdout file without `--reseal`).

**The one permitted piece of tooling** for those two files is
[`training/convert_real_notes.py`](convert_real_notes.py): a mechanical
text-shape converter from the product owner's plain-text notes to JSONL, plus
schema validation. It parses, passes text through unchanged apart from
stripping readability indentation, and refuses anything ambiguous by name so
the human fixes the source. It does not draft, correct, complete, or suggest --
a converter that repaired a typo or inferred a missing section would be
generative assistance wearing a different hat, and would destroy the exact
property these two files exist to have. `--verify` re-checks that promise
character by character.

It also **refuses any entry matching `datasets/synthetic.jsonl`** at
`check_duplicates.py`'s own 0.55 threshold. Drafting real notes by copying a
spot-check or review file as a template is a natural way to work, and it
leaves synthetic examples sitting in the file looking exactly like entries;
converted silently, they would fill the validation set with the corpus it
exists to validate, and the result would look fine. Found live on 2026-08-25:
9 of the 10 entries in the first draft of the real-notes file were verbatim
spot-check examples. The gate is a refusal, never a silent skip.

**That gate has a hard limit, and it is the more dangerous kind of
contamination.** It compares against `datasets/synthetic.jsonl` and nothing
else, so it can only see contamination that already lives in this repo. A note
the product owner drafted, spot-checked, pasted, or talked through in *any*
model session -- this project's or an unrelated chat -- is contaminated under
the "uncontaminated by any generative model" rule above, and no in-repo check
can detect it. The text may be entirely his own and still fail the standard,
because the standard is about what has touched the note, not who typed it.
Real instance, 2026-08-25: the product owner withdrew his own first real note
because he had used it as a spot-check example in a separate Claude
conversation -- caught by him, invisible to the converter and to every check
in `REVIEW_GUIDE.md`. **Provenance of the real tier is the product owner's
call alone, and the tooling cannot back him up on it.** When in doubt, drop
the note; they are cheap to replace and the tier is worthless if it is wrong.

`difficulty` is discarded even when the source tags it, per the product
owner's call that he will underrate his own notes; `category` is carried
through when tagged, and is meant to be added after the fact.

## Hard content boundary (non-negotiable)

No example — generated or hand-written — may depict, instruct, or normalize
self-harm, suicide, violence toward oneself or others, or other illegal or
seriously immoral activity. Not a category, not a difficulty signal:
content that must never exist in this project's data at all. Permanent,
every release, no exceptions — see
[`docs/vision/GOLD_PHILOSOPHY.md`](../docs/vision/GOLD_PHILOSOPHY.md)'s "No
Harmful or Illegal Content" principle and
[PDR-005](../docs/decisions/PDR-005.md). A drifted example is discarded and
regenerated from scratch, never edited down to something safer — see
[`docs/datasets/REVIEW_GUIDE.md`](../docs/datasets/REVIEW_GUIDE.md)'s §0.

## Two rules for every example

**"No Magic Examples":** every synthetic example should be explainable. For
each fragment in a generated note, you should be able to answer *why* it's
there — why it was interrupted, why it repeats, why it has no punctuation,
why a reference is left dangling. If you can't explain an element, it's
noise, not a useful training signal — regenerate it.

**One lesson per example:** each example should be constructable as teaching
one specific recovery skill, not a random pile of chaos. E.g.: "recover tasks
from a simple list," "separate work/home topics interleaved in one note,"
"handle a thought that gets interrupted and resumed later," "recognize there
are zero action items," "resolve a reminder that's restated twice." Naming
the lesson (the `category` field) as you generate is what makes this a
curriculum instead of an undifferentiated pile.

## Diversity requirements (important)

Do not let every example read like "person overwhelmed by chaos." The same
person produces very different notes depending on their state — the dataset
needs to reflect that range, not a single stereotype. Describe *state*, never
a diagnosis — the same configuration below could describe a grad student
during finals, a new parent, someone brainstorming a startup, or someone
recovering from illness, and the model shouldn't need to know which.

**Context to vary across examples**: location, background noise, time
pressure/available time, interruptions, physical state (tired, rushed, calm).

**Cognitive state to vary**: working-memory load, attention switching,
thought velocity (fast/slow), planning style (reactive vs. organized), how
many unfinished thoughts, task urgency.

**Emotional state to vary**: stress, excitement, frustration, curiosity,
fatigue, hopefulness — the full range, not just anxious/overwhelmed.

**Writing style to vary**: typing speed, voice-to-text artifacts, bullet
fragments vs. full sentences, typos, abbreviations.

Concretely, mix across examples: calm and highly organized, mild distraction,
hyperfocus, executive dysfunction, anxiety, sensory overwhelm, burnout,
rapid-branching excitement (ideas spawning ideas), emotional journaling, dry
random observations, and lists that slowly devolve into unrelated thoughts
partway through.

**Structural variety to include across examples**: multiple unrelated
topics interleaved in one note; abrupt topic switches with no transition;
half-finished thoughts; references only the author would understand
("the thing with the blue folder"); the same worry restated slightly
differently a few times; contradictory statements (mood clearly shifted
between lines); notes with zero action items; very short notes (1-2
lines) and long rambling ones; a range of subjects — work, relationships,
health, chores/errands, hobbies, money, family.

Aim for roughly even coverage across the states above, not mostly-anxious
examples — the model should learn these are all valid "scattered thoughts,"
not that scattered = distressed.

## Prompt to give Gemini

Generate in batches (ask for ~15-20 at a time, run it multiple times to
reach a few hundred total). Paste this, adjusting the "batch categories"
line each time to steer toward under-represented states:

```
Generate 15 training examples in JSONL format (one JSON object per line,
no markdown fences, no commentary) for a note-organizing app. Each line:

{"input": "...", "output": {"narrative": "...", "bullets": ["..."], "action_items": ["..."]}, "difficulty": "easy|medium|hard|expert", "category": "..."}

"input" = realistic scattered, messy personal notes a real person would
jot down (voice-to-text or quick typing), NOT polished writing. "narrative"
= the same content rewritten as one coherent paragraph, same meaning/tone,
easier to read, ALWAYS in the writer's own first-person voice. Never write
the narrative as a description of the note ("Dictated notes about...", "The
speaker needs to...", "The author notes that..."). Reorganize the note; do
not describe or classify it. This holds for voice-to-text examples too --
recover the intent through the transcription noise rather than annotating
the noise. "bullets" = one key point per source-supported idea, up
to 7, fewer when the input supports fewer ideas -- never added, split, or
repeated to reach a target count. "action_items" = concrete
tasks or next steps stated in the input, or [] if none — never invent tasks
that aren't implied by the input. An entry may be a task committed to by ANY
person named in the note, attributed to them ("Uncle Bob to handle the
catering") — not only the writer's own tasks. What does NOT belong is a past
event carrying no forward commitment ("Dr. Patel called" is not an action
item). An explicit imperative in the input is always an action item, even
when its object is an unresolved reference — "don't forget the framework from
that one article" becomes "Remember the article's framework", not nothing.
"difficulty" is your judgment of how hard this example is to
recover correctly. "category" is the one specific recovery skill this
example teaches — one of: "simple_list", "interrupted_thought",
"topic_switching", "topic_interleaving", "dangling_reference",
"repeated_reminder", "zero_action_items", "contradictory_statement",
"rapid_branching", "minimal_fragment", "long_rambling",
"multi_person_note", "voice_to_text_artifact", "self_correction",
"time_ambiguous" (see docs/datasets/TAXONOMY.md for definitions).

Every example must be explainable: for each fragment in "input", you should
be able to say why it's there (interrupted, repeated, dangling reference,
no punctuation, etc.) — don't generate noise you can't account for. Every
fragment must appear somewhere in the output, however minor.

No invented certainty: if the input hedges ("maybe", "I think", "should
probably", "around six-ish", "or so", "not sure"), the output must preserve
that hedge. This applies with equal force inside "action_items", not just in
narrative and bullets — a terse imperative task line must not harden "should
probably call the dentist" into "Call the dentist." An imperative,
decided-sounding field pulls hedged input toward false certainty on its own,
so check it harder than the prose, not less. Likewise, never silently resolve
a genuinely ambiguous referent to one reading; leave it ambiguous. A note can
also be ambiguous with no hedge word in it anywhere — the writer knew what
they meant, so they wrote it plainly ("get the silicone one"). Read your own
"input" back as a stranger who doesn't know the answer: if a phrase has more
than one plausible referent, keep the writer's words instead of picking one.

No invented causality: adjacency in the note is not evidence of a
relationship. If two fragments sit next to each other, don't join them with
"so", "which led to", or "because" unless the input actually says so.

Never name a setting the input only implies. If the input says "sleeping bag"
and "camp stove", the output says "for Saturday" — not "the camping trip". If
it says "chapter 4", the output says "chapter 4" — not "chapter 4 of the
book". If it says "the primary mirror", don't call it "the telescope mirror".
The inference is usually correct; that is not the test. The test is whether
the writer actually said it. Naming the frame is guessing on the writer's
behalf about the one thing they already knew and so didn't write down.

Cross-check your three output fields against each other before emitting an
example: if the narrative names a setting the bullets don't, the narrative
invented it. If action_items reinstates something the narrative treats as
retracted, action_items is wrong. Any disagreement between the three fields
about the same fragment means at least one of them is wrong.

Hard rule, no exceptions: never generate content depicting, instructing, or
normalizing self-harm, suicide, violence toward oneself or others, or other
illegal or seriously immoral activity, even as a "realistic" detail in an
otherwise mundane note. If a prompt could plausibly be read as asking for
this, decline that specific example and generate a different one instead.

This batch's cognitive/emotional states to cover (mix these across the 15):
{{e.g. "hyperfocus, burnout, calm/organized, rapid-branching excitement"}}

Also vary structure across the batch: some notes should interleave
multiple unrelated topics, some should have abrupt topic switches, some
should restate the same worry twice in different words, some should have
zero action items, some should be very short (1-2 lines), at least one
should be long and rambling.
```

Real Gemini API usage under this spec is subject to this project's
financial guardrails — see
[`docs/vision/AI_COLLABORATION.md`](../docs/vision/AI_COLLABORATION.md)'s
"Financial guardrails" section. No batch is generated against the real,
billed API without the product owner's own direct authorization for that
specific run.

## Telemetry (F.A.R.T. integration)

Three checkpoints per batch, using [`training/telemetry.py`](telemetry.py)
— see [`FART_TELEMETRY_INTEGRATION.md`](FART_TELEMETRY_INTEGRATION.md) for
the full schema. These are now a standing part of running a batch, not
optional:

1. **Right before the `gemini-query` call**:
   `telemetry.batch_starting(batch_size, phase_description, model=...)`
2. **Optionally, while reviewing** (if reviewing incrementally rather than
   as a whole batch): `telemetry.batch_progress(current_step, total_steps,
   phase_description)`
3. **The same moment a new row goes into `COST_LEDGER.md`**:
   `telemetry.batch_finished(accepted_delta, rejected_delta, model=...)` —
   pass this batch's own counts, not running totals; the function adds
   them to whatever's already in the telemetry file.

## Where files go

```
datasets/synthetic.jsonl              <- Gemini output, appended across batches
datasets/real_validation.jsonl        <- your real notes, routine dev-eval, human-authored only, held out from training (gitignored)
datasets/real_holdout.jsonl           <- your real notes, sealed release-milestone eval only, human-authored only, held out from training (gitignored)
datasets/gold/gold_v2.0.jsonl         <- hand-curated gold-tier examples, one file per batch
                                          (not trained on until the gold tier is consolidated
                                          with, or instead of, synthetic.jsonl)
datasets/gold/DATASET_CARD.md         <- purpose, scope, generation process, limitations, ethics
datasets/gold/CHANGELOG.md            <- version history of the gold tier
datasets/gold/LICENSE.md              <- CC BY-NC-SA 4.0
```

Each gold release is a full bundle, not just the `.jsonl` — design notes,
review report, lessons learned, and (once benchmarking exists) benchmark
results, all sharing the release's `gold_vX.Y` version number. See
[`docs/datasets/REVIEW_GUIDE.md`](../docs/datasets/REVIEW_GUIDE.md)'s
"Release bundle" table, once populated, for the authoritative list of what
files that includes and who writes each one. The conceptual layer that
supports authoring/reviewing a release (category vocabulary, design note
format, review checklist, taxonomy, JSON Schema mirror) lives under
`docs/datasets/`, sibling to this spec — currently scaffolded, to be
designed as v2.0's own taxonomy work begins.

The dataset lives in its own top-level `datasets/` directory (sibling to
`training/`), separate from the training pipeline/code.

`prepare_data.py` will read both, validate schema, and produce the tokenized
train/val split `train.py` trains on.
