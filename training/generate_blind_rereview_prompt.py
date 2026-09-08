#!/usr/bin/env python3
"""
Generate a self-contained, sanitized prompt for a genuinely blind periodic
adversarial re-review (PDR-006), for manual copy-paste into an isolated
Gemini session with NO filesystem/repo access -- a fresh AI Studio chat, not
an API/CLI call from this repo. See docs/decisions/PDR-006.md's 2026-09-07
amendment for why: the CLI transport that replaced Antigravity
(PDR-009/gemini_bridge.py) has no equivalent to invoke_subagent's isolated
context -- it always has read-only access to this whole repo, which could
let it reconstruct prior review context the design wants kept out entirely.

WHAT THIS SCRIPT DOES NOT DO: it does not call any API, does not talk to
Gemini, and does not write anything outside review_bridge/ (already
gitignored in full -- see .gitignore). It only reads the local corpus and
writes three local files: a rubric (paste into the reviewing app's
instructions box), a sample (.jsonl -- drag-and-drop as the target file),
and a private index -> line-number mapping for reconciling findings
afterward. The mapping file is never included in the rubric or sample and
must never be pasted/uploaded anywhere external -- it is the one place
original corpus position survives. (Output shape matches the product
owner's own blind-review app: a separate rubric-instructions field and a
drag-dropped data file, not one combined blob -- adjusted 2026-09-08 after
seeing that app's actual interface.)

Two design decisions, reached via review_bridge/ before this script was
written (round on "genuinely blind re-review prompt generator", 2026-09-08):
- The sample carries NO prior disposition/verdict, anonymized or otherwise.
  Matches REVIEW_GUIDE.md's existing rule ("not the original review's
  conclusions"), not a new restriction invented for this tool.
- Category + difficulty labels ARE included per record -- several checklist
  rules (verbatim-preservation scoped to exactly three categories;
  difficulty-comparison) only apply correctly with the category known.
  Tried omitting them first; rejected as more likely to reproduce a known
  failure mode (a reviewer over-applying verbatim-preservation to
  self_correction, which the checklist explicitly excludes).

There is deliberately NO automatic "weight toward historically-fixed
categories" default, unlike REVIEW_GUIDE.md's hand-run process. That
weighting has only ever lived in this project's prose (re-review log
entries, CATEGORY_REFERENCE.md), never in a machine-readable form this
script could read without guessing -- pass --weight-categories explicitly
if you want that skew for a given round; omitted, the sample is uniform
random within each pool.

Usage (from training/):
    python generate_blind_rereview_prompt.py --since-line 500
    python generate_blind_rereview_prompt.py --since-line 500 --sample-size 14 --controls 5
    python generate_blind_rereview_prompt.py --since-line 500 --weight-categories dangling_reference,self_correction
"""
import argparse
import hashlib
import json
import math
import random
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
DEFAULT_DATASET = DATASETS_DIR / "synthetic.jsonl"
OUT_DIR = REPO_ROOT / "review_bridge"

CHECKLIST_TEXT = """\
## Task

You are conducting an independent quality audit of a dataset used to train a
text-normalization system. A separate file has been provided alongside this
rubric containing the records to audit, each with:

- `input`: a raw, unedited freeform note (often messy -- incomplete
  sentences, hedges, interruptions, contradictions, dictation artifacts)
- `output.narrative`: a cleaned-up, reorganized first-person paragraph
  version of the same content
- `output.bullets`: short discrete points pulled from the note
- `output.action_items`: concrete commitments/tasks stated or implied in
  the note, worded as imperatives
- `id`: an arbitrary per-record number, only for referring to a record in
  your findings -- it carries no other meaning (not a position, not a date,
  not a count of anything).

This is a fully independent audit. Do not assume any record is already
correct -- nothing has been pre-verified for you. Report every defect you
find, however small, using the rules below. Do not attempt to identify,
search for, or speculate about the origin of this dataset or any system
that produced it -- treat this purely as a self-contained document review
using only the material given.

## Rules

**0. Hard safety gate, checked first.** Flag as REJECT immediately if any
record depicts, instructs, or normalizes self-harm, violence, or other
seriously illegal/immoral content.

**1. No invented content** -- check `output` against `input` for each
record:

- *Preserved uncertainty*: a hedge or vague reference in `input` ("the blue
  folder," "maybe") stays a hedge/vague reference in `output` -- never
  resolved to a specific guessed answer.
- *Unmarked ambiguity*: even with no hedge word present, if a phrase in
  `input` has more than one plausible reading (test: read `input` alone, as
  a stranger with no outside context), `output` must not silently pick one.
- *No invented chronology*: `output` must not assert an order of events
  `input` doesn't state.
- *No invented causality*: `output` must not assert one fragment
  caused/explains another unless `input` actually says so -- two facts
  merely sitting next to each other in the same sentence is not evidence
  of a causal link, UNLESS the input's own phrasing already reads as
  cause-and-effect (e.g. a comma splice stating one thing right after its
  own stated reason).
- *No merged unrelated items*: two genuinely unrelated fragments stay
  represented separately, never combined into one (even plausible-sounding)
  statement.
- *No lost fragments*: every fragment in `input`, however brief, appears
  somewhere in `output` (any of the three fields). Exception: dictation/
  transcription artifacts (spoken punctuation like "comma," "period,"
  self-corrections like "write down -- wait, right down") are noise
  represented by their *effect* on the content, never their own literal
  text -- apply this consistently within one record, never half-and-half.
- *No over-summarization*: a distinct fragment must not disappear into a
  vaguer, more general statement.
- *No unsupported tasks*: `action_items` never contains a task `input`
  doesn't actually imply.
- *No dropped imperatives*: an explicit imperative/commitment stated in
  `input` belongs in `action_items`, even if its object is an unresolved
  reference (e.g. "don't forget the framework from that article" ->
  "Remember the article's framework," not nothing).
  **But imperative mood alone does not make something an action item.**
  People genuinely meander between self-suggested possible activities
  ("watch movies, play with the dog" -- open-ended, nothing actually
  decided) versus a specific named commitment ("I'm going to watch [a
  specific named film] tomorrow" -- a determined action on a named object).
  Only the second belongs in `action_items`. The test is whether the
  sentence commits to a specific, determined action, not whether the verb
  is imperative or whether the object is named.
- *No misattribution*: a fragment belonging to one named person is never
  reassigned to another.
- *No invented certainty*: a hedge in `input` ("I think," "maybe," "not
  sure") stays a hedge in `output` -- never smoothed into a flat, confident
  statement `input` didn't make. **Check `action_items` at least as
  carefully as narrative/bullets** -- its terse, imperative phrasing creates
  its own pressure toward false certainty, separate from ordinary prose
  fluency pressure.
- *No inferred setting/frame*: `output` never names an activity, venue,
  occasion, relationship, domain, or object category that `input` only
  implies through incidental props/details, however likely the inference
  actually is. ("Sleeping bag" + "camp stove" does not license "camping
  trip.") Test: would `input` alone justify this label to a stranger with
  no outside context?
- *Fields must agree with each other*: after checking each field against
  `input` individually, cross-check `narrative`/`bullets`/`action_items`
  against each other. A disagreement about the same fragment means at
  least one of them is wrong.
- *No non-recovery*: `narrative` must actually reorganize `input`, not
  just repeat it back with capitalization/punctuation fixed. A narrative
  that is near word-for-word identical to its input is a defect even if
  nothing in it is technically false -- the whole point of this field is
  reorganization, not transcription.
- *Representing an absence*: each record below carries a category label.
  For records labeled **interrupted_thought**, **contradictory_statement**,
  or **dangling_reference** specifically -- and only those three -- if
  `input` contains a thought that stops mid-sentence, two claims that
  can't both be true, or a reference that's never resolved, `output`
  should preserve that literally (the actual broken-off text verbatim,
  both contradictory claims stated plainly, the referent left unresolved)
  -- never smoothed over or described from outside ("the note trails off
  here," "the writer contradicts themselves"). Do not apply this
  requirement to records with a different category label, even if they
  also contain a retraction or a stopped thought -- e.g. a record that
  corrects itself and settles on one final answer is telling a different
  kind of story (a decision arrived at, not an unresolved tension) and
  should read as a clean, resolved narrative, not as preserving the
  discarded option.
- *`action_items` ownership*: an entry may belong to any person named in
  `input`, not only the writer, as long as it's attributed to them. A past
  event with no forward commitment is not an action item ("Dr. Patel
  called" is not one). A stated expectation of someone else's future
  action IS an action item, but must keep its hedge if `input` had one.

**2. No diagnosis framing**: nothing should reference a specific medical or
psychological diagnosis, or assume *why* a note is fragmented. A described
emotional/cognitive state (rushed, distracted, excited) is fine; a
diagnostic label is not.

**3. No unexplained fragments**: for every unusual feature of `input`
(missing punctuation, an interruption, a repeated phrase, a contradiction,
etc.), you should be able to say why it's there. If you can't explain a
fragment's presence, flag it.

**4. Within this sample only** (you're being given a sample, not the full
dataset, so only check what's visible in front of you):

- *Voice*: `narrative` should always be first person ("I ...") and read as
  the note itself reorganized -- never a report about the note ("the author
  is planning...", "I noted that...", "I stated..."). First person alone
  isn't sufficient -- "I noted that X" is first person and still describes
  the note rather than being it.
- *Register consistency*: `bullets`/`action_items` should be phrased
  consistently across the sample -- this dataset's convention is elided
  first-person imperative ("Buy milk"), not third person ("Needs to buy
  milk") or passive ("Milk must be bought").
- *Direct comparison*: if any records in this sample look similar to each
  other (near-identical structure, wording, or stated difficulty), compare
  them side by side and flag any inconsistency in how they were handled.

Each record also carries `category` and `difficulty`. Category/difficulty
are included because several rules above only apply correctly when the
category is known (see "Representing an absence"). Treat a category label
as just that -- a name for what this record is meant to test -- not as an
invitation to infer anything about how these labels were assigned or by
what process. Difficulty is a purely relative label (harder relative to
other records in this file only, not an absolute score) -- useful only for
the "Direct comparison" check above.

## Output format

For each record (by its `id`), give a verdict of **ACCEPT**, **FIX**, or
**REJECT**, a one-line reason citing the specific rule violated, and -- if
FIX -- your proposed corrected text for the affected field(s). At the end,
give a total count of each verdict.
"""


def load(path: Path) -> list:
    records = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if line:
                records.append((lineno, json.loads(line)))
    return records


def anonymized_record(idx: int, record: dict) -> dict:
    # Only the fields the blind reviewer needs -- explicitly NOT the source
    # line number, corpus position, or anything else that could hint at
    # scale/history. `id` is the sample-local anonymous index, unrelated to
    # any real position in the corpus.
    return {
        "id": idx,
        "category": record.get("category"),
        "difficulty": record.get("difficulty"),
        "input": record["input"],
        "output": {
            "narrative": record["output"]["narrative"],
            "bullets": record["output"]["bullets"],
            "action_items": record["output"]["action_items"],
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--since-line", type=int, required=True,
                     help="1-indexed line number: records after this were "
                          "added/touched since the last re-review and form "
                          "the 'new' pool. Records at or before this line "
                          "form the 'control' pool. No auto-detected "
                          "default -- read the actual boundary from "
                          "REVIEW_GUIDE.md's re-review log each time.")
    ap.add_argument("--sample-size", type=int, default=None,
                     help="Total records in the sample. Default: "
                          "max(10, ceil(0.15 * len(new pool))), per "
                          "REVIEW_GUIDE.md's cadence rule.")
    ap.add_argument("--controls", type=int, default=None,
                     help="Never-touched controls within the sample. "
                          "Default: max(2, round(0.3 * sample-size)).")
    ap.add_argument("--weight-categories", type=str, default="",
                     help="Comma-separated category names to oversample "
                          "from the 'new' pool. No default -- this "
                          "project's 'most historically fixed categories' "
                          "list only exists in prose (CATEGORY_REFERENCE.md, "
                          "re-review log entries); pass it explicitly rather "
                          "than have this script guess it.")
    ap.add_argument("--seed", type=int, default=None,
                     help="Random seed, for a reproducible sample. Printed "
                          "either way so a run can be reproduced later.")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = ap.parse_args()

    if not args.dataset.exists():
        print(f"error: {args.dataset} not found", file=sys.stderr)
        return 2

    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**31)
    rng = random.Random(seed)

    all_records = load(args.dataset)
    new_pool = [(ln, r) for ln, r in all_records if ln > args.since_line]
    control_pool = [(ln, r) for ln, r in all_records if ln <= args.since_line]

    if not new_pool:
        print(f"error: no records after line {args.since_line} -- nothing "
              f"new to sample. Check --since-line against the actual corpus "
              f"size ({len(all_records)} records).", file=sys.stderr)
        return 2

    sample_size = args.sample_size or max(10, math.ceil(0.15 * len(new_pool)))
    controls_n = args.controls if args.controls is not None else max(2, round(0.3 * sample_size))
    controls_n = min(controls_n, len(control_pool))
    new_n = max(0, sample_size - controls_n)

    weight_cats = {c.strip() for c in args.weight_categories.split(",") if c.strip()}

    # New-pool selection: if weighting requested, take up to half of new_n
    # from the weighted categories first (as many as available), then fill
    # the rest uniformly from whatever's left in the new pool.
    new_shuffled = list(new_pool)
    rng.shuffle(new_shuffled)
    if new_n >= len(new_shuffled):
        selected_new = new_shuffled
    elif weight_cats:
        weighted = [x for x in new_shuffled if x[1].get("category") in weight_cats]
        rest = [x for x in new_shuffled if x[1].get("category") not in weight_cats]
        weighted_n = min(len(weighted), max(1, new_n // 2))
        selected_new = weighted[:weighted_n] + rest[:new_n - weighted_n]
    else:
        selected_new = new_shuffled[:new_n]

    control_shuffled = list(control_pool)
    rng.shuffle(control_shuffled)
    selected_controls = control_shuffled[:controls_n]

    selected = selected_new + selected_controls
    rng.shuffle(selected)  # so touched-vs-control order isn't inferable

    if not selected:
        print("error: sample is empty after selection -- check pool sizes "
              "and --sample-size/--controls.", file=sys.stderr)
        return 2

    today = date.today().isoformat()
    rubric_path = args.out_dir / f"blind_rereview_rubric_{today}.txt"
    sample_path = args.out_dir / f"blind_rereview_sample_{today}.jsonl"
    mapping_path = args.out_dir / f"blind_rereview_mapping_{today}.json"

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rubric_path.write_text(CHECKLIST_TEXT, encoding="utf-8")
    with sample_path.open("w", encoding="utf-8") as f:
        for i, (_, r) in enumerate(selected, 1):
            f.write(json.dumps(anonymized_record(i, r), ensure_ascii=False) + "\n")

    mapping = {
        str(i): {
            "line": lineno,
            "category": r.get("category"),
            "difficulty": r.get("difficulty"),
            "input_hash": hashlib.sha256(r["input"].encode("utf-8")).hexdigest()[:16],
            "pool": "new" if lineno > args.since_line else "control",
        }
        for i, (lineno, r) in enumerate(selected, 1)
    }
    mapping_path.write_text(
        json.dumps({"seed": seed, "since_line": args.since_line, "dataset": str(args.dataset),
                    "generated": today, "mapping": mapping}, indent=2),
        encoding="utf-8",
    )

    cat_counts = {}
    for _, r in selected:
        cat_counts[r.get("category", "?")] = cat_counts.get(r.get("category", "?"), 0) + 1

    print(f"Sampled {len(selected)} record(s): {len(selected_new)} from the "
          f"new pool ({len(new_pool)} total, lines {args.since_line + 1}-"
          f"{all_records[-1][0]}), {len(selected_controls)} controls "
          f"(from {len(control_pool)} pre-boundary records).")
    print(f"Seed: {seed} (pass --seed {seed} to reproduce this exact sample).")
    print("Category distribution in sample:")
    for cat, n in sorted(cat_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {cat}: {n}")
    print(f"\nRubric -- paste into the review-instructions box: {rubric_path}")
    print(f"Sample -- drag-and-drop as the target file (.jsonl, native support): {sample_path}")
    print(f"Private mapping (local only -- NEVER paste/upload this anywhere external): {mapping_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
