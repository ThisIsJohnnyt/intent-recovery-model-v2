# Taxonomy

**Status: category vocabulary and difficulty/boundary/confidence categories
accepted by the product owner, 2026-08-19** — settled enough to draft
`CATEGORY_REFERENCE.md` against. Still open to expansion as real generation
surfaces further gaps; this isn't a closed list. See
[PDR-001](../decisions/PDR-001.md)–[PDR-005](../decisions/PDR-005.md) for
why this repository exists and starts from zero.

v1's category structure was judged sound on its own terms — this draft
carries its shape forward (category vocabulary, difficulty tiers, boundary/
confidence categories, failure categories) rather than reinventing it, per
the product owner's own read that the structure wasn't the problem. One
thing is genuinely new here, process-driven, not v1-driven: a corpus-
uniqueness rule (see "Dataset labeling rules" below). The content-safety
boundary is also new, but lives at the constitutional layer now — see
[`GOLD_PHILOSOPHY.md`](../vision/GOLD_PHILOSOPHY.md) and
[PDR-005](../decisions/PDR-005.md) — not as a taxonomy-specific rule.

## Category vocabulary

The `category` field in
[`training_data.schema.json`](training_data.schema.json) — the one specific
recovery skill an example teaches (see `DATASET_SPEC.md`'s "One lesson per
example"). Drawn directly from the structural variety `DATASET_SPEC.md`
already asks Gemini to cover, named as skills rather than left as an
unlabeled list — every category below should already be recognizable from
that spec.

| Category | What it teaches | Example shape |
|---|---|---|
| `simple_list` | Baseline recovery: a mostly-explicit list, low ambiguity. | "milk, eggs, call dentist, return library books" |
| `interrupted_thought` | Distinguish a thought that's cut off and stays unfinished from one that's cut off and resumed later in the note. | "need to talk to sam about the— oh also don't forget the—" |
| `topic_switching` | Segment an abrupt, transition-free jump from one unrelated subject to another without merging them. | A note that jumps from a work deadline straight into a birthday gift idea. |
| `topic_interleaving` | Separate two or more topics that are *woven* through the note out of order, not just sequenced. | Work and home threads alternating line by line. |
| `dangling_reference` | Preserve a reference only the writer would understand exactly as unresolved — never guess what it means. | "the thing with the blue folder" |
| `repeated_reminder` | Recognize a task/worry restated more than once (sometimes with drifting wording) as one item, not two. | The same errand mentioned near the top and again near the bottom, worded differently. |
| `zero_action_items` | Produce a correctly empty `action_items` array rather than inventing a task to fill it. | Pure observation or venting, no task implied. |
| `contradictory_statement` | Preserve a mood or stated intention that shifts partway through, rather than resolving it into one consistent stance. | "so excited about this" ... later ... "not sure I even want to do it anymore" |
| `rapid_branching` | Capture one idea spawning several related sub-ideas in quick succession without flattening them into a single generic point. | A hyperfocus/excitement burst where each line spins off the last. |
| `minimal_fragment` | Don't over-elaborate a very short, thin note into something more substantial than the input supports. | 1–2 lines, little structure. |
| `long_rambling` | Don't lose or merge low-salience fragments under compression pressure in a long, loosely structured note. | Many small points across a long note, none individually load-bearing. |
| `multi_person_note` | Correctly attribute a fragment to the right person when a note mentions more than one, rather than merging or reassigning. | "sam wants pizza, jen said she's not hungry, need to grab a salad for her" |
| `voice_to_text_artifact` | Recover intent through transcription-layer noise (misheard words, run-ons from missing punctuation, filler) as distinct from the writer's own phrasing choices. | "so i need to um pick up the the dry cleaning before like six" |
| `self_correction` | Honor an explicit retraction — the retracted content is dropped from the output, not preserved alongside the correction. | "call the plumber tomorrow — actually no, forget that, already handled it" |
| `time_ambiguous` | Preserve a vague time reference as still vague in the output, rather than resolving it to an invented specific time. | "need to deal with this before the thing on friday, or maybe after" |

Accepted by the product owner, 2026-08-19: these four close real gaps —
each maps to a skill this project anticipated elsewhere (`misattribution`
as a review-guide failure mode, "voice-to-text artifacts" as a
`DATASET_SPEC.md` style variation, "preserve uncertainty" already applied to
`dangling_reference` but not to time) without a category of its own until
now. Still open to further expansion — this isn't a closed list.

## Difficulty categories

Carried forward from v1 unchanged, since the tier *names* weren't the
problem: **Basic / Moderate / Complex / High Cognitive Load**, mapping to
`easy`/`medium`/`hard`/`expert` in `training_data.schema.json`.

| Tier | Schema value | What raises the difficulty |
|---|---|---|
| Basic | `easy` | One clear topic, no interruptions, minimal ambiguity — close to `simple_list`. |
| Moderate | `medium` | One or two categories above present, still low ambiguity resolving them. |
| Complex | `hard` | Multiple categories combined in one note (e.g. `topic_interleaving` + `dangling_reference`). |
| High Cognitive Load | `expert` | Dense combination of categories, longer note, more restated/branching content — more state to hold to recover correctly. |

## Boundary categories

Design-notes-only (see [`DESIGN_NOTES_TEMPLATE.md`](DESIGN_NOTES_TEMPLATE.md)'s
"Boundary Evidence") — **never** a field in the trained JSONL. Carried
forward from v1's names; definitions below are proposed, since v1's names
came without documented definitions.

- **Topic Shift** — the note moves from one subject to an unrelated one.
- **Intent Shift** — the writer's goal for a passage changes mid-thought
  (e.g., starts venting, ends up planning).
- **Context Shift** — the surrounding situation changes (e.g., work → home)
  without the subject itself necessarily changing.
- **Thought Interruption** — a sentence/idea is cut off, resumed later or
  not.
- **Embedded Reminder** — a task or note-to-self appears folded inside a
  larger passage rather than standing alone.

## Confidence categories

Design-notes-only, same scope restriction as above: **High / Medium /
Low** — how clearly the input text itself signals a boundary, versus how
much must be inferred to place it.

## Dataset labeling rules

The eight-principle constitution lives in
[`GOLD_PHILOSOPHY.md`](../vision/GOLD_PHILOSOPHY.md) — linked here, not
restated, per that document's own instruction, including its "No Harmful or
Illegal Content" principle (see [PDR-005](../decisions/PDR-005.md)). One
rule below is specific to this repository, not yet part of that
constitution:

**No near-duplicate content.** A new example must not closely restate one
already accepted into the corpus — same scenario, same phrasing pattern,
same category-plus-detail combination. Named explicitly because v1's
generation runs repeatedly stalled on exactly this (Gemini producing
near-duplicates of already-protected content, tripping collision rules) —
this entry states the principle; the actual similarity-check mechanics
belong in `DATASET_SPEC.md`'s generation process, not here, and are still
to be defined.

## Failure category vocabulary

Short names for the checks [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) §4 already
runs in prose — this is a naming convenience for tracking which failure mode
a rejected example hit, not a redefinition. See `REVIEW_GUIDE.md` for the
authoritative detail on each.

`topic_merge` · `topic_loss` · `unsupported_addition` · `invented_causality`
· `invented_chronology` · `over_summarization` · `misattribution`

## See also

- [`CATEGORY_REFERENCE.md`](CATEGORY_REFERENCE.md) — per-category detail
  (definition, example, lifecycle) for the vocabulary above, not yet
  populated.
- [`DESIGN_NOTES_TEMPLATE.md`](DESIGN_NOTES_TEMPLATE.md) — where boundary/
  confidence categories actually get used per example.
- [`training/DATASET_SPEC.md`](../../training/DATASET_SPEC.md) — the
  generation prompt and diversity requirements this vocabulary plugs into.
