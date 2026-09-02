# External code review — training core

**Reviewed commit:** `78d5ae8` (`main`, 2026-09-02)
**Scope:** everything in `training/*.py`, `datasets/synthetic.jsonl` (525 records),
`requirements.txt`, and the consistency between the tracked docs and the code.
**Reviewer:** a separate Claude Code session with no prior context on this project,
working from a fresh clone of the hosted repository.
**Verification level:** every finding below was checked against the actual files or
the actual corpus. Findings are labelled `[VERIFIED]` (I ran it and observed the
result), `[ESTIMATED]` (arithmetic from real corpus measurements, assumption stated),
or `[UNVERIFIED]` (blocked in my environment — commands to check are given).

---

## How to use this document

This is a review, not a work order. Read the guardrails before acting.

### Guardrails

1. **Do not mass-rewrite corpus narratives.** Finding C1 identifies 58 records that
   breach a documented threshold. Rewriting them is a *data* judgment governed by
   `docs/datasets/REVIEW_GUIDE.md` and the product owner's final say, not a mechanical
   fix. The engineering deliverable for C1 is **the missing check script**, plus a
   report. Rewrites are a separate, owner-approved batch.
2. **`REVIEW_GUIDE.md` §"Fixing voice raises the copy ratio" warns these two rules pull
   against each other.** Any narrative edit must be re-measured on both axes. Do not
   optimise the copy ratio in isolation.
3. **Do not touch `datasets/real_validation.jsonl` or `datasets/real_holdout.jsonl`
   until C4 is fixed.** They are gitignored, hand-written, and unreproducible. The two
   scripts that write them currently do so non-atomically.
4. **Verify before you fix.** Every finding has a repro command. Run it. If a finding
   does not reproduce on your working tree, say so and stop — do not fix a phantom.
5. **Findings marked `[OWNER CALL]` are decisions, not defects.** Surface them; do not
   resolve them unilaterally.

### Suggested order

| # | Finding | Type | Blast radius |
|---|---|---|---|
| 1 | C2 — requirements pins | Mechanical | `training/requirements.txt` |
| 2 | C4 — atomic writes for real-tier data | Mechanical | 2 scripts |
| 3 | C1 — write the missing copy-ratio check | New script | new file + report |
| 4 | M7 — round-trip + schema tests | New tests | new files |
| 5 | M5, M6, M8, M9, M10, M11 | Mechanical | 4 scripts |
| 6 | C3 — eval leakage | `[OWNER CALL]` | methodology |
| 7 | L-series hygiene | Mechanical | docs + 3 scripts |

---

## Critical

### C1 — The copy-ratio rule has silently failed corpus-wide `[VERIFIED]`

`docs/datasets/REVIEW_GUIDE.md` calls input→narrative similarity *"the strongest
quantitative signal available,"* records the corpus mean as *"settled at 0.561,"* and
states that exactly **two** records sit above 0.85 *"permanently, by decision"* —
`#127` (0.87) and `#118` (0.91) — with the instruction *"Do re-open any other record
that climbs."*

Measured on `datasets/synthetic.jsonl` at `78d5ae8`, using `evaluate_real.py`'s own
`word_ratio` (difflib `SequenceMatcher` over lowercased whitespace tokens):

| | Documented | Actual |
|---|---|---|
| Corpus mean | 0.561 | **0.647** |
| Records > 0.85 | 2 | **60** |
| Records > 0.90 | — | 19 |
| Max | — | 0.96 |

**The metric is confirmed to match yours:** it reproduces `#118` at exactly **0.91**
and `#127` at exactly **0.87**, the two values `REVIEW_GUIDE.md` records. The gap is
real, not a measurement artifact.

The drift is monotonic by corpus position:

```
lines   1- 75: 0.497      lines 226-300: 0.690      lines 451-525: 0.706
lines  76-150: 0.639      lines 301-375: 0.633
lines 151-225: 0.657      lines 376-450: 0.704
```

This is exactly the failure `REVIEW_GUIDE.md` predicted: *"a whole batch shifting
upward is generation retreating into non-recovery."*

Worst case, line 262 (`interrupted_thought` / medium, 0.96) — the narrative is the
input verbatim apart from `call mom` → `I need to call Mom`, and the interruption
artifact `-- wait did i leave the stove on` is copied into both the narrative *and*
a bullet:

```
INPUT    : call mom about the thanksgiving menu and ask if she has the recipe for
           the sweet potato casserole because last year it was so -- wait did i
           leave the stove on
NARRATIVE: I need to call Mom about the Thanksgiving menu and ask if she has the
           recipe for the sweet potato casserole because last year it was so --
           wait did i leave the stove on
BULLETS  : [..., '-- wait did i leave the stove on']
```

Mean copy ratio by category, worst first:

```
0.77 interrupted_thought     0.70 long_rambling          0.61 simple_list
0.74 multi_person_note       0.68 contradictory_statement 0.56 self_correction
0.71 zero_action_items       0.68 topic_switching        0.52 topic_interleaving
0.70 dangling_reference      0.67 rapid_branching        0.51 minimal_fragment
0.70 time_ambiguous          0.63 voice_to_text_artifact 0.50 repeated_reminder
```

**Root cause is an engineering gap, not a review failure.** Nothing in `training/`
computes this distribution. `check_duplicates.py` measures input↔input similarity —
a different quantity. So the project's strongest quality signal is recomputed by hand
inside review sessions and drifts invisibly between them.

**Deliverable:** `training/check_copy_ratio.py` — prints the distribution, the mean,
per-category means, and names every record above a `--threshold` (default 0.85), with
`#118` and `#127` in an explicit allowlist carrying the `REVIEW_GUIDE.md` rationale.
Exit non-zero when any non-allowlisted record breaches. Wire it into the per-batch
review step in `REVIEW_GUIDE.md`. Reuse `evaluate_real.py`'s `word_ratio` — do not
write a second similarity implementation.

The 58 breaching records are `[OWNER CALL]`. Report the list; do not rewrite them.

Repro: Appendix A.

---

### C2 — `requirements.txt` declares a range where neither endpoint works `[VERIFIED]`

Both ends checked against real package sources.

**Floor fails.** `requirements.txt` declares `transformers>=4.40`. `train.py:137`
passes `eval_strategy=`. I downloaded `transformers==4.40.2` and grepped
`transformers/training_args.py`: the field is `evaluation_strategy`, not
`eval_strategy` (renamed in 4.41). A clean install at the declared minimum raises
`TypeError` on `Seq2SeqTrainingArguments`.

**Ceiling fails.** `>=4.40` is unbounded, so a fresh install today resolves to
`transformers==5.16.1`, whose `utils/import_utils.py` sets
`ACCELERATE_MIN_VERSION = "1.1.0"` — while `requirements.txt` declares
`accelerate>=0.30`.

All four dependencies are floor-only with no upper bound.

**Fix:** raise the transformers floor to `>=4.41`, and pin or upper-bound the versions
the 2026-09-02 run actually used. `training/SETUP.md` already documents a bespoke
install sequence; the pinned versions belong next to it.

---

### C3 — The generalization eval is also the model-selection set `[VERIFIED]` `[OWNER CALL]`

`train.py:140` sets `load_best_model_at_end=has_val` with
`metric_for_best_model="eval_loss"`, evaluated on `datasets/real_validation.jsonl`.
`evaluate_real.py` then reports on **the same 15 records** and its module docstring
describes them as *"the generalization check this project's real tier exists for"* and
*"a good result here means something a synthetic-only eval can't."*

Once a checkpoint is selected on a set, results on that set stop being a
generalization estimate. Two distinct problems:

- **Bias.** Best-of-8-epochs on `eval_loss` fits the checkpoint choice to those 15.
- **Noise.** 15 examples is a very loud selection signal; the epoch-to-epoch
  `eval_loss` ordering at that size is substantially chance.

The sealed 12-record holdout is the right instrument and is correctly reserved for
milestones, so it is not the answer for routine dev-time checks.

**Options, for the product owner:** (a) carve a selection-only slice out of
`synthetic.jsonl` and select on that, keeping the real tier untouched for reporting;
(b) keep selecting on the real set but drop the generalization claim from
`evaluate_real.py`'s docstring and report it as a fitting curve; (c) revert to
last-epoch and state that overfitting is unmanaged at this corpus size. Do not pick
one unilaterally — this is a methodology decision the project's governance model
reserves to the owner.

Note this was introduced by `78d5ae8` itself, which added best-checkpoint selection
for good reasons. The fix for one problem created this one.

---

### C4 — Destructive in-place rewrites of unversioned, irreplaceable data `[VERIFIED]`

`split_real_holdout.py:86-91` and `backfill_categories.py:137-142` truncate-and-rewrite
`real_validation.jsonl` / `real_holdout.jsonl` directly:

```python
with args.validation.open("w", encoding="utf-8", newline="\n") as f:
```

These files are gitignored, hand-written by the product owner, and unreproducible —
the only artifacts in the project that cannot be regenerated. There is no
temp-file-plus-rename and no backup. An interrupt, a full disk, or an exception
between the two writes in `backfill_categories.py` leaves one or both truncated.

**Second, worse problem: `--reseal` does not do what its docstring implies.**
`split_real_holdout.py` reads **only** `--validation`. After the first split that file
no longer contains the sealed records. So re-sealing draws a new holdout from the
*remainder* and overwrites `real_holdout.jsonl` — **permanently discarding the
previously sealed records.** The docstring (*"allow re-splitting an already-sealed
(non-empty) holdout file"*) reads as "re-split the union"; the behaviour is "delete
the holdout."

**Fix:**
1. Write to `path.with_suffix('.jsonl.tmp')`, `load_jsonl()` the temp file to validate,
   then `os.replace()`. Both scripts, every write.
2. Either make `--reseal` read both files and re-split their union, or remove the flag
   and refuse outright. Update the docstring to match whichever is chosen.
3. `backfill_categories.py` `load_target()` returns `[]` for a missing file and then
   opens it `"w"` — so a missing `real_holdout.jsonl` is *created* as a 0-byte file.
   Skip the write when the source file did not exist.

---

## Medium

### M5 — The contamination gate warns and proceeds `[VERIFIED]`

`convert_real_notes.py:231-248` returns `gate_warning` when `--corpus` is missing;
`main()` at line 293-295 prints `WARNING: corpus ... not found -- contamination gate
DID NOT RUN` and then **continues to write `real_validation.jsonl`**.

That gate exists because 9 of the 10 entries in the first draft of the real-notes file
were verbatim spot-check examples (module docstring, 2026-08-25). A gate that a typo'd
`--corpus` path silently disables is not a gate.

**Fix:** make a missing corpus fatal (`return 2`) unless an explicit
`--no-corpus-check` is passed, and have that flag print what it is waiving.

### M6 — `check_duplicates.py` returns 100% false positives, quadratically `[VERIFIED]`

Run against the corpus it defaults to, it produces 3 hits. All 3 are noise:

```
[0.58] (char=0.58 word=0.21) :343 <-> :491
  A: call the plumber about the league under the sync
  B: call the landlord period ask about the weird noise in the wall
[0.58] (char=0.58 word=0.20) :128 <-> :453
  A: text Mike about the Thursday thing.
  B: tell her about the tall one
[0.57] (char=0.57 word=0.13) :205 <-> :343
```

Three defects:

1. **`score = max(ratio, jac)` (line 98) lets the noisier metric decide.** On short
   strings `SequenceMatcher` measures length agreement, not meaning. Word overlap
   correctly reported 0.13–0.21 on all three; `max()` discarded the correct signal.
   Use `min`, or separate thresholds per metric, or length-normalise `char_ratio`.
2. **Quadratic with a full `SequenceMatcher` per pair.** Measured: **70 s at 525
   records** (137,550 pairs). Extrapolating: ~4.5 min at 1000, ~18 min at 2000. Add a
   `real_quick_ratio()` / length-ratio prefilter before the full comparison.
3. **It only compares `input`, never `output`.** This is why the scenario-repetition
   finding recorded in commit `abee8d2` had to be found by hand — two records can share
   a scenario while wording their inputs differently. Add an output-side pass.

Also: `main()` returns `None`, so the script always exits 0 and cannot gate anything.
Return non-zero when pairs are flagged.

### M7 — No tests, no CI `[VERIFIED]`

There is no `tests/`, no `conftest.py`, no `pyproject.toml`, no `Makefile`, and no
`.github/`. The subtlest bug the project has hit — flan-t5 collapsing `\n` at encode
time, commit `0749442` — was found by burning a training run.

That specific bug is a ~10-line property test. I ran the property by hand across all
525 records (serialize → simulate newline collapse → deserialize): **0 mismatches** on
narrative, bullets, and action_items, including the 86 records with empty
`action_items`. The contract is currently correct — and nothing stops it breaking
silently again.

**Deliverable:** `training/tests/test_serialization.py` covering, at minimum:
round-trip over the whole corpus under newline collapse; the empty-`action_items` case;
the empty-`bullets` case; a `validate_record` rejection case per schema rule. Appendix B
has the round-trip harness to start from. `pytest` only — no other new dependency.

### M8 — The overfitting guard is permanently disabled `[VERIFIED]`

`train.py:32` sets `SMALL_CORPUS_WARNING_THRESHOLD = 500`. The corpus is **525
records**, so the warning can no longer fire.

It was calibrated to the corpus *target* rather than to observed overfitting — and the
run that motivated it (train 0.47 / eval 1.6 after 8 epochs, per `78d5ae8`'s message)
had 500 examples, i.e. it would not have fired for that run either.

**Fix:** replace the size heuristic with a post-run check on the actual signal — read
`trainer.state.log_history`, compare final `train_loss` against best `eval_loss`, and
warn on the gap. That measures the thing you care about and does not need recalibrating
every time the corpus grows.

### M9 — Truncation is silent `[VERIFIED]` / count is `[ESTIMATED]`

`prepare_data.py:185-205` tokenizes with `truncation=True` at `MAX_INPUT_LENGTH=256`
and `MAX_TARGET_LENGTH=384` and never reports how many examples were cut. A truncated
target trains the model to stop mid-output.

Measured corpus lengths (whitespace words):

```
input  : p50 42   p90 73   p99 107  max 130
target : p50 91   p90 156  p99 218  max 276
```

Inputs are comfortably inside budget. Targets are not comfortably clear: at ~33 tokens
of `###MARKER###` overhead, the longest target (276 words) crosses 384 tokens at
anything above ~1.27 tokens/word. Estimated truncations: 0 at 1.25 tok/word, 1 at
1.30–1.35, 2 at 1.40, 3 at 1.50. Small either way — but currently invisible.

**Fix:** count truncations in `tokenize_examples()`, print them, and record
`train_truncated` / `val_truncated` in `prepared/meta.json`. Consider also recording a
hash of each source file there for reproducibility.

### M10 — The "structural sanity check" checks one of three markers `[VERIFIED]`

`evaluate_real.py:97`:

```python
structurally_valid = bool(parsed["narrative"])
```

A model that emits `###NARRATIVE### ...` and stops is scored **valid**, with silently
empty `bullets` and `action_items`. The stated failure mode from the first real run is
`action_items` over-invention — the metric does not examine the failing field.

**Fix:** require all three markers present; report per-section presence and item counts
separately in the summary, so over- and under-generation of `action_items` is visible
as its own number.

### M11 — `word_ratio` is reported with no baseline `[VERIFIED]`

`evaluate_real.py:126-128` prints mean narrative-vs-input similarity with the gloss
*"high here means the model is echoing the input rather than recovering it."* There is
no reference value, so the number is uninterpretable: the training corpus's own mean on
that metric is **0.647** (C1). A checkpoint scoring 0.67 on real notes is reproducing
its training distribution, not echoing.

**Fix:** compute the corpus baseline once and print it alongside — e.g.
`mean 0.67 (synthetic corpus baseline 0.65; real_validation gold baseline X)`. The gold
baseline for the real tier is the more honest comparator, since those narratives were
written by hand.

---

## Low / hygiene

| ID | Finding | Location |
|---|---|---|
| L1 | README still says *"currently empty,"* *"Scaffolded, not yet populated,"* *"No dataset content, trained checkpoint, or model release exists here yet"* — 525 records, 28 batches and a trained checkpoint later. First thing a reader sees. | `README.md:79`, `:86-87` |
| L2 | `training/category_quick_reference.md` cited in an error message; file does not exist. Point it at `docs/datasets/CATEGORY_REFERENCE.md`. | `backfill_categories.py:86` |
| L3 | `gate5_pre_execution_attestation_template.json` referenced by two PDRs; file does not exist. | `PDR-004.md:48`, `PDR-006.md:32` |
| L4 | Record on line 215 has **8 bullets**; `training_data.schema.json` documents *"up to 7."* Neither the schema (no `maxItems`) nor `validate_record()` enforces it. Decide which is right, then encode it in both. | `synthetic.jsonl:215`, `training_data.schema.json` |
| L5 | `VALID_CATEGORIES` hardcoded, duplicating the taxonomy. `validate_record()` accepts any non-empty string, so `synthetic.jsonl` is never checked against the list. Single-source it and enforce in the validator. | `backfill_categories.py:42-48`, `prepare_data.py:83-86` |
| L6 | `requests_today` is never reset on a day boundary — it is a monotonic counter with a name that says otherwise. | `telemetry.py:123` |
| L7 | Non-atomic `write_text` plus `except Exception: pass` on read means a truncated telemetry file silently zeroes cumulative `accepted_examples` / `rejected_examples` instead of failing loudly. | `telemetry.py:32-38`, `:74` |
| L8 | No export script, despite README's *"prepare → train → export → release"* and `.gitignore`'s `*.onnx`. Either write it or correct the pipeline description. | `README.md:80`, `.gitignore` |
| L9 | `train.py` saves model + tokenizer but not `TASK_PREFIX` or the marker contract. A released checkpoint carries no record of the prompt it requires. Copy `prepared/meta.json` into the output dir. | `train.py:157-159` |
| L10 | The *reject* set is named `keep`. | `convert_real_notes.py:305` |
| L11 | `e not in bad_cat` does deep dict equality where identity was meant; the sibling script correctly uses `id()`. | `backfill_categories.py:87` |
| L12 | `--limit 0` is silently ignored (`if args.limit:`). | `evaluate_real.py:73` |
| L13 | Checkpoint existence is checked with a friendly error; the `--real-validation` path is not, and raises a raw traceback. | `evaluate_real.py:62-68` |
| L14 | 4 characters in the corpus are absent from T5's vocab and become `<unk>`: `>` ×1, `~` ×3. | `synthetic.jsonl` |

---

## Verified clean — do not re-litigate

These were checked and found correct. Recorded so no one spends time on them again.

- **Serialization round-trip:** 525/525 records survive serialize → newline collapse →
  deserialize with zero mismatches, including all 86 empty-`action_items` records.
- **No `###` sequences** anywhere inside record content — the delimiter format cannot be
  corrupted by data.
- **No `" - "` substrings** inside any bullet or action item, so
  `deserialize_target`'s acknowledged split heuristic does not currently misfire.
  (1 item begins with a dash; harmless under the current regex.)
- **No duplicate inputs, no duplicate narratives, no empty list items, no newlines
  inside any narrative.**
- **Category coverage** is balanced: all 15 categories present, 32–42 records each.
  Difficulty spread: 118 easy / 143 medium / 158 hard / 106 expert.
- **`.mcp.json`** uses `${GEMINI_API_KEY}` expansion — no secret is committed.
- **`_deep_merge`** in `telemetry.py` correctly fixes the shallow-merge bug in the
  integration doc's reference implementation rather than copying it.
- **`prepare_data.py:121-147`** — the newline-collapse root-cause docstring is accurate
  and is the best documentation in the repository. Preserve it through any refactor.

---

## Unverified — please confirm locally

`huggingface.co` returns 403 through my sandbox's proxy, so I could not load the real
tokenizer. Three things below are estimates, and one is a genuine open risk.

**Open risk: 133 em-dashes.** The corpus contains 133 `—` (U+2014) and 2 `é` (U+00E9).
T5's SentencePiece has no byte-fallback, so any character outside its 32k vocab becomes
`<unk>`. If `—` is not in the vocab, 133 training targets teach the model to emit
`<unk>`, and `skip_special_tokens=True` at decode silently drops it — producing
narratives with missing punctuation that look like a model defect rather than a data
defect. Note `—` is used inside narratives, not just inputs (see line 262 above).

Run this and record the result in this file:

```python
from transformers import AutoTokenizer
t = AutoTokenizer.from_pretrained("google/flan-t5-base")
for s in ["—", "é", ">", "~", "###NARRATIVE###", "###BULLETS###", "###ACTIONS###"]:
    toks = t.tokenize(s)
    print(f"{s!r:20} n={len(toks):>3} {toks}  {'<<< UNK' if t.unk_token in toks else ''}")
```

This also settles the other two estimates: the true per-marker token cost (I assumed
~11 each, 33 total) and therefore the exact truncation count for M9. With the tokenizer
loaded, get the real numbers directly:

```python
from transformers import AutoTokenizer
import json, sys; sys.path.insert(0, "training")
import prepare_data as pd
t = AutoTokenizer.from_pretrained(pd.MODEL_NAME)
recs = [json.loads(l) for l in open("datasets/synthetic.jsonl", encoding="utf-8") if l.strip()]
over_in = over_tg = 0
for r in recs:
    ni = len(t(pd.TASK_PREFIX + r["input"])["input_ids"])
    nt = len(t(pd.serialize_target(r["output"]))["input_ids"])
    over_in += ni > pd.MAX_INPUT_LENGTH
    over_tg += nt > pd.MAX_TARGET_LENGTH
print(f"inputs over {pd.MAX_INPUT_LENGTH}: {over_in} | targets over {pd.MAX_TARGET_LENGTH}: {over_tg}")
```

---

## Appendix A — reproduce C1

Stdlib only. Run from the repository root.

```python
import json
from difflib import SequenceMatcher
from collections import defaultdict

recs = [json.loads(l) for l in open("datasets/synthetic.jsonl", encoding="utf-8") if l.strip()]

def word_ratio(a, b):                      # identical to evaluate_real.py's
    return SequenceMatcher(None, a.lower().split(), b.lower().split()).ratio()

rows = []
for i, r in enumerate(recs, 1):
    f = word_ratio(r["output"]["narrative"], r["input"])
    b = word_ratio(r["input"], r["output"]["narrative"])
    rows.append((max(f, b), i, r["category"], r["difficulty"]))

vals = [x[0] for x in rows]
print(f"n={len(rows)}  mean={sum(vals)/len(vals):.3f}  (REVIEW_GUIDE.md: 0.561)")
print(f">0.85: {sum(v > 0.85 for v in vals)}  (REVIEW_GUIDE.md: 2)   >0.90: {sum(v > 0.90 for v in vals)}")
print("\nAbove 0.85:")
for v, i, c, d in sorted(rows, reverse=True):
    if v > 0.85:
        print(f"  line {i:>3}  {v:.2f}  [{c}/{d}]")

by = defaultdict(list)
for v, i, c, d in rows:
    by[c].append(v)
print("\nBy category:")
for c, vs in sorted(by.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
    print(f"  {sum(vs)/len(vs):.2f}  {c}  (n={len(vs)})")

print("\nBy corpus position:")
for s in range(0, len(rows), 75):
    ch = [x[0] for x in rows[s:s + 75]]
    print(f"  lines {s+1:>3}-{s+len(ch):>3}: {sum(ch)/len(ch):.3f}")
```

Sanity check the metric before trusting the output: line 118 must print `0.91` and
line 127 must print `0.87`, matching `REVIEW_GUIDE.md`. If they do not, the metric has
drifted from the one the guide used and the comparison is invalid.

## Appendix B — round-trip harness for M7

```python
import json, re, sys
sys.path.insert(0, "training")
import prepare_data as pd

def through_tokenizer(s):        # flan-t5 SentencePiece collapses newlines at encode
    return re.sub(r"\s*\n\s*", " ", s)

recs = [json.loads(l) for l in open("datasets/synthetic.jsonl", encoding="utf-8") if l.strip()]
bad = 0
for i, r in enumerate(recs, 1):
    got = pd.deserialize_target(through_tokenizer(pd.serialize_target(r["output"])))
    exp = r["output"]
    if (got["narrative"] != " ".join(exp["narrative"].split("\n"))
            or got["bullets"] != exp["bullets"]
            or got["action_items"] != exp["action_items"]):
        bad += 1
        print(f"  MISMATCH line {i}")
print(f"round-trip: {len(recs) - bad}/{len(recs)} clean")
```

Expected at `78d5ae8`: `525/525 clean`.

---

## One-paragraph summary

The pipeline is well-built and unusually well-reasoned for its size; the newline-collapse
diagnosis in `prepare_data.py` and the refuse-don't-guess discipline in
`convert_real_notes.py` are genuinely good engineering. The structural problem is that
the project's quality bar lives in prose rather than in code: ~272 KB of process
documentation against ~60 KB of Python, zero tests, zero CI — and the single most
important data-quality rule in all of it (`REVIEW_GUIDE.md`'s copy-ratio threshold) is
enforced by nothing, which is why it has drifted from a documented mean of 0.561 to an
actual 0.647 with 60 records above a limit that was supposed to hold exactly two. The
three highest-value fixes are: make the copy-ratio check executable (C1), pin the
dependencies so a clean install works at all (C2), and make the real-tier file writes
atomic before they lose data that cannot be regenerated (C4).
