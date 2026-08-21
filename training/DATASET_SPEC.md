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

## File format

One JSON object per line (JSONL), UTF-8:

```json
{"input": "<raw scattered thoughts, as the user would actually type them>", "output": {"narrative": "<coherent flowing narrative>", "bullets": ["<key point 1>", "<key point 2>"], "action_items": ["<task 1>"]}, "difficulty": "easy|medium|hard|expert", "category": "<short label for the one lesson this example teaches>"}
```

Rules for `output`:
- `narrative`: rewrites `input` as a coherent narrative. Same meaning and tone as the input, just organized. Not therapy-speak, not generic — it should clearly be about the specific things mentioned in `input`.
- `bullets`: one short key point per source-supported idea in `input`, up to 7. Source-determined count — use fewer than 7 when `input` supports fewer ideas; never add, split, or repeat content to reach a target count. A one-idea input gets one bullet.
- `action_items`: concrete tasks/next steps mentioned in `input`. Use an empty array `[]` when the input has none — never invent one.

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
easier to read. "bullets" = one key point per source-supported idea, up
to 7, fewer when the input supports fewer ideas -- never added, split, or
repeated to reach a target count. "action_items" = concrete
tasks mentioned, or [] if none — never invent tasks that aren't implied by
the input. "difficulty" is your judgment of how hard this example is to
recover correctly. "category" is the one specific recovery skill this
example teaches — one of: "simple_list", "interrupted_thought",
"topic_switching", "topic_interleaving", "dangling_reference",
"repeated_reminder", "zero_action_items", "contradictory_statement",
"rapid_branching", "minimal_fragment", "long_rambling",
"multi_person_note", "voice_to_text_artifact", "self_correction",
"time_ambiguous" (see docs/datasets/TAXONOMY.md for definitions).

Every example must be explainable: for each fragment in "input", you should
be able to say why it's there (interrupted, repeated, dangling reference,
no punctuation, etc.) — don't generate noise you can't account for.

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
