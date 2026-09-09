"""
Data preparation for intent-recovery-model-v2's fine-tuning pipeline.
See training/DATASET_SPEC.md's "Model output serialization" and "Task
prefix" sections for the exact contract this module implements.

Stages: load raw JSONL -> validate against the schema -> serialize each
record's `output` into the model's actual training target (indented JSON
by default; see TARGET_FORMAT below) -> build a chat-templated prompt
(TASK_PREFIX as a system message, the note as the user message) ->
tokenize with Qwen/Qwen3.5-4B's tokenizer, masking the prompt span out of
the labels (-100) so the causal LM is only ever trained to predict the
target, never to reproduce its own prompt -> write token-id JSONL that
train.py reads directly. See docs/decisions/PDR-012.md for why the base
model moved off google/flan-t5-base (encoder-decoder) onto this
decoder-only causal LM, and review_bridge/ round 5 (2026-09-09) for the
length constants below and the reasoning behind them.

Split: train = synthetic.jsonl + any consolidated gold releases, MINUS a
selection slice carved out of that same pool by deterministic content-hash
bucketing (see SELECTION_SLICE_FRACTION / is_in_selection_slice below).
train.py evaluates against that slice during training and uses it for
load_best_model_at_end checkpoint selection.

datasets/real_validation.jsonl is NOT part of this split -- it is schema-
checked here for hygiene but never written into prepared/ or used for
selection. It stays reserved for evaluate_real.py's independent, untouched
reporting run. This replaces the original design (train = synthetic.jsonl,
val = real_validation.jsonl by file) after an external review (2026-09-02,
finding C3) found that design meant a checkpoint was being selected on the
exact 15 records the eval then reported as the generalization result --
once you select on a set, results on it stop being a generalization
estimate. Product owner chose option (a) of the three the review offered:
carve a selection-only slice out of synthetic.jsonl, keep the real tier
untouched for reporting. See docs/decisions/PDR-007.md.

Usage (from training/):
    python prepare_data.py                 # full run, writes to prepared/
    python prepare_data.py --validate-only  # schema check only, no tokenizing
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
PREPARED_DIR = Path(__file__).resolve().parent / "prepared"

MODEL_NAME = "Qwen/Qwen3.5-4B"

# Re-measured directly against Qwen's tokenizer on all 547 records this
# pipeline actually tokenizes (synthetic + gold + real_validation) --
# NOT assumed to carry over from flan-t5-base's 256/384 (review_bridge/
# round 5, 2026-09-09). Observed: chat-templated prompt max=174 tokens
# (system+user, add_generation_prompt=True), JSON target max=384 tokens,
# delimited-fallback target max=347 tokens. Both caps below sit close to
# 2x their p99 (143 / 319), not their max, so a modest future outlier
# doesn't immediately start truncating as the corpus grows past 532.
MAX_INPUT_LENGTH = 224
MAX_TARGET_LENGTH = 480  # covers both TARGET_FORMAT options' observed max
MAX_SEQ_LENGTH = MAX_INPUT_LENGTH + MAX_TARGET_LENGTH  # 704 -- Stage 0's
    # hardware test measured 4.66GB/7.93GB peak at the prior, shorter
    # combined length (640); Gemini's review_bridge round-5 assessment
    # was that the ~10% increase to 704 is comfortably inside that
    # margin and re-testing would be overkill -- not independently
    # re-measured on hardware, flagging that rather than asserting it.

# The model's I/O contract's system-message content -- same wording as the
# original flan-t5 raw-string prefix, just delivered via apply_chat_template
# as a system message now instead of string concatenation onto the input.
TASK_PREFIX = "Recover the intent behind these scattered notes:\n\n"

# "json" (default) or "delimited". See serialize_target/deserialize_target
# below -- PDR-012 moved the training target to indented JSON but kept the
# original ###NARRATIVE###/###BULLETS###/###ACTIONS### format available as
# a measured fallback, to be switched back to only if the JSON format's
# genuine syntax-error rate (as distinct from early-stop-truncation
# failures -- see evaluate_real.py's parse-failure categorization) proves
# poor in practice. A one-line constant change, not a rewrite, by design.
TARGET_FORMAT = "json"

# Fraction of the synthetic+gold pool reserved for training-time checkpoint
# selection (train.py's load_best_model_at_end), carved out per record by
# is_in_selection_slice() rather than a stored/randomized index list. At the
# 525-record corpus this is ~52 records -- a much quieter selection signal
# than the 15-record real_validation.jsonl set it replaces for this purpose.
# See PDR-007 for why this exists and prepare_data.py's module docstring for
# what it replaced.
SELECTION_SLICE_FRACTION = 0.10


def is_in_selection_slice(record: dict) -> bool:
    """Deterministic content-hash bucketing: a record's train/selection
    membership depends only on its own `input` text, never on its position
    in the file. Same pattern as check_copy_ratio.py's ALLOWLIST keys
    (sha256(input) rather than line number) -- for the same reason: a
    membership rule keyed on position silently reassigns the wrong records
    the moment something is inserted, removed, or reordered upstream.
    Recomputed fresh every prepare_data.py run rather than stored anywhere,
    so there is no separate seed/index file that can drift out of sync with
    the corpus."""
    digest = hashlib.sha256(record["input"].encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 1000
    return bucket < int(SELECTION_SLICE_FRACTION * 1000)


REQUIRED_TOP = {"input", "output"}
REQUIRED_OUTPUT = {"narrative", "bullets", "action_items"}
# DATASET_SPEC.md's bullets rule: "up to 7". Unenforced until an external
# review (2026-09-02, finding L4) found one record had drifted to 8 with
# nothing catching it -- neither this validator nor training_data.schema.json
# had a maxItems check. Fixed in the corpus and enforced here now.
MAX_BULLETS = 7

VALID_DIFFICULTIES = {"easy", "medium", "hard", "expert"}


class SchemaError(ValueError):
    """Raised when a record violates training_data.schema.json's contract."""


def validate_record(record: dict, source: str, lineno: int) -> None:
    """Raise SchemaError with a precise location on any contract violation.
    Mirrors docs/datasets/training_data.schema.json -- if the two ever
    disagree, this function wins, since it's what actually gates training
    (per that schema file's own stated authority order)."""
    where = f"{source}:{lineno}"

    if not isinstance(record, dict):
        raise SchemaError(f"{where}: record is not a JSON object")

    missing = REQUIRED_TOP - record.keys()
    if missing:
        raise SchemaError(f"{where}: missing top-level field(s) {sorted(missing)}")

    if not isinstance(record["input"], str) or len(record["input"]) < 1:
        raise SchemaError(f"{where}: 'input' must be a non-empty string")

    output = record["output"]
    if not isinstance(output, dict):
        raise SchemaError(f"{where}: 'output' must be an object")

    missing_out = REQUIRED_OUTPUT - output.keys()
    if missing_out:
        raise SchemaError(f"{where}: 'output' missing field(s) {sorted(missing_out)}")

    if not isinstance(output["narrative"], str) or len(output["narrative"]) < 1:
        raise SchemaError(f"{where}: 'output.narrative' must be a non-empty string")

    for field in ("bullets", "action_items"):
        value = output[field]
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise SchemaError(f"{where}: 'output.{field}' must be a list of strings")
    if len(output["bullets"]) > MAX_BULLETS:
        raise SchemaError(
            f"{where}: 'output.bullets' has {len(output['bullets'])} items, "
            f"more than the documented cap of {MAX_BULLETS} (DATASET_SPEC.md: "
            f"'up to 7')"
        )

    if "difficulty" in record and record["difficulty"] not in VALID_DIFFICULTIES:
        raise SchemaError(
            f"{where}: 'difficulty' {record['difficulty']!r} not in {sorted(VALID_DIFFICULTIES)}"
        )

    if "category" in record and (
        not isinstance(record["category"], str) or len(record["category"]) < 1
    ):
        raise SchemaError(f"{where}: 'category' must be a non-empty string")


def load_jsonl(path: Path) -> list:
    """Load and validate a JSONL dataset file. Raises on the first schema
    violation or malformed JSON line -- fix before anything else, per
    docs/datasets/REVIEW_GUIDE.md §1: 'If this throws, the batch has a
    schema problem ... fix before anything else.'"""
    records = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                raise SchemaError(f"{path.name}:{lineno}: invalid JSON ({e})") from e
            validate_record(record, path.name, lineno)
            records.append(record)
    return records


def serialize_target(output: dict) -> str:
    """dict -> the literal text the model is trained to generate, in
    whichever format TARGET_FORMAT currently selects. This function IS
    DATASET_SPEC.md's "Model output serialization" spec, not a separate
    reimplementation of it."""
    if TARGET_FORMAT == "json":
        return _serialize_target_json(output)
    return _serialize_target_delimited(output)


def deserialize_target(text: str) -> dict:
    """Inverse of serialize_target() -- text -> dict, in whichever format
    TARGET_FORMAT currently selects. Used to check real model output at
    eval time against the same logic that built the training targets,
    rather than a second hand-written parser that could silently drift
    from what training actually used.

    Unlike the delimited format's parser (see _deserialize_target_delimited
    below), this can raise json.JSONDecodeError on malformed or
    early-stop-truncated model output -- callers (evaluate_real.py,
    probe_adversarial.py) catch that explicitly rather than this function
    silently swallowing it into an empty result."""
    if TARGET_FORMAT == "json":
        return _deserialize_target_json(text)
    return _deserialize_target_delimited(text)


def _serialize_target_json(output: dict) -> str:
    """dict -> indented JSON text. The default target format since
    PDR-012 (base model migration) -- see review_bridge/ for why: a strict
    parser (json.loads) that fails loudly on genuine malformation, instead
    of the delimited format's forgiving-but-lossy heuristic splitting.
    Field order is dict-insertion order (narrative, bullets, action_items
    -- REQUIRED_OUTPUT's own declared order), not re-sorted, so the
    serialized shape is stable across runs for the same input dict."""
    ordered = {k: output[k] for k in ("narrative", "bullets", "action_items")}
    return json.dumps(ordered, indent=2)


def _deserialize_target_json(text: str) -> dict:
    """Inverse of _serialize_target_json(). Raises json.JSONDecodeError on
    anything that doesn't parse -- including a string that happens to
    parse but isn't a dict, which is re-raised as the same exception type
    so callers only need one except clause. Confirmed empirically
    (2026-09-09) that Qwen's tokenizer does NOT collapse "\\n" to a space
    at encode time the way flan-t5's SentencePiece tokenizer did -- but
    it wouldn't matter either way here, since JSON parsing is whitespace-
    agnostic regardless of how the surrounding indentation survives
    tokenization."""
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise json.JSONDecodeError(
            f"expected a JSON object, got {type(parsed).__name__}", text, 0
        )
    return {
        "narrative": parsed.get("narrative", ""),
        "bullets": parsed.get("bullets", []),
        "action_items": parsed.get("action_items", []),
    }


def _serialize_target_delimited(output: dict) -> str:
    """dict -> the literal delimited text format used before PDR-012, kept
    available as TARGET_FORMAT's measured fallback -- see that constant's
    comment. Not currently the active format; see _serialize_target_json
    for what actually runs by default."""
    narrative = " ".join(output["narrative"].split("\n"))  # defensive, not expected
    lines = ["###NARRATIVE###", narrative, "###BULLETS###"]
    lines += [f"- {b}" for b in output["bullets"]]
    lines.append("###ACTIONS###")
    lines += [f"- {a}" for a in output["action_items"]]
    return "\n".join(lines)


def _deserialize_target_delimited(text: str) -> dict:
    """Inverse of _serialize_target_delimited() -- text -> dict. Kept
    available as TARGET_FORMAT's fallback; not currently the active format.

    Does NOT split on literal "\\n". flan-t5's SentencePiece tokenizer
    normalized "\\n" to a plain space at *encode* time -- confirmed by
    tokenizing "X\\nY" and "X Y" and getting identical token ids -- so a
    real generated sequence never contained a newline to split on in the
    first place, and neither did the training targets built by
    _serialize_target_delimited() above once they passed through that
    tokenizer. A trained flan-t5 checkpoint's raw output looked like:
        "###NARRATIVE### text here ###BULLETS### - one - two ###ACTIONS### - a1"
    all on one line. Found 2026-08-25 when the first real eval run showed
    every example failing to parse despite the raw output visibly
    containing all three markers in order with real content -- the parser
    was checking for a newline that no longer existed anywhere in the
    pipeline, not a model or data defect. This behavior was specific to
    flan-t5's SentencePiece tokenizer -- Qwen's tokenizer does not collapse
    newlines this way (confirmed 2026-09-09) -- but this parser never
    relied on newlines surviving in the first place, so it needs no change
    either way if this fallback is ever reactivated on the current model.

    Splits on the marker strings directly instead, then splits each
    list section on " - " (matching how _serialize_target_delimited's own
    "- {item}" lines get glued back-to-back by the same normalization).
    This is a heuristic, not lossless: an item whose own text contains a
    literal " - " substring will be split apart. Accepted for now since it
    matches what the model was actually trained to produce; revisit if
    that collision shows up in practice."""
    import re
    parts = {"narrative": "", "bullets": [], "action_items": []}
    chunks = re.split(r"###NARRATIVE###|###BULLETS###|###ACTIONS###", text)
    markers = re.findall(r"###NARRATIVE###|###BULLETS###|###ACTIONS###", text)
    # chunks[0] is whatever precedes the first marker (should be empty/junk);
    # chunks[i+1] is the content following markers[i].
    for marker, content in zip(markers, chunks[1:]):
        content = content.strip()
        if marker == "###NARRATIVE###":
            parts["narrative"] = content
        else:
            field = "bullets" if marker == "###BULLETS###" else "action_items"
            items = [i.strip() for i in re.split(r"(?:^|\s)-\s", content)]
            parts[field] = [i for i in items if i]
    return parts


def build_examples(records: list) -> list:
    """record -> {"input": ..., "target": ...} training pair. `input`
    stays the raw note text -- TASK_PREFIX is no longer concatenated onto
    it here, since it's delivered as a separate chat-template system
    message at tokenization time now (see tokenize_examples), not a raw
    string prefix."""
    return [
        {"input": r["input"], "target": serialize_target(r["output"])}
        for r in records
    ]


def resolve_source_files() -> list:
    """Per DATASET_SPEC.md's 'Where files go': synthetic.jsonl + any
    consolidated gold releases. The selection slice train.py evaluates
    against is carved out of this same pool (see is_in_selection_slice),
    not read from a separate file -- see PDR-007."""
    files = [DATASETS_DIR / "synthetic.jsonl"]
    files += sorted((DATASETS_DIR / "gold").glob("gold_v*.jsonl"))
    return files


def split_train_selection(records: list) -> tuple:
    """Partition into (train, selection) by is_in_selection_slice(). A
    plain list comprehension pair rather than one pass with two accumulators
    -- there's no shared state to keep in sync, so two clear passes read
    better than one pass juggling both lists."""
    train = [r for r in records if not is_in_selection_slice(r)]
    selection = [r for r in records if is_in_selection_slice(r)]
    return train, selection


def tokenize_examples(examples: list, tokenizer) -> list:
    """Causal-LM tokenization (since PDR-012): one concatenated sequence
    per example -- chat-templated prompt (TASK_PREFIX as a system message,
    the note as the user message, `add_generation_prompt=True`,
    `enable_thinking=False`) followed by the serialized target and an
    explicit EOS -- with labels set to -100 over the entire prompt span so
    the loss only ever scores the target, never the model's own prompt.
    Replaces the old seq2seq version, which tokenized input/target as two
    independent, separately-padded sequences for the encoder/decoder.

    -100 is the standard HF convention for "ignore this position in the
    loss" -- both the prompt span and any padding must not contribute
    gradient."""
    prepared = []
    for ex in examples:
        messages = [
            {"role": "system", "content": TASK_PREFIX},
            {"role": "user", "content": ex["input"]},
        ]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
            enable_thinking=False,
        )
        prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        if len(prompt_ids) > MAX_INPUT_LENGTH:
            # Truncating a rendered chat template from the right risks
            # cutting into the assistant-priming suffix
            # (<|im_start|>assistant...\n<think>...) that
            # add_generation_prompt=True appends -- unlike the old
            # seq2seq path's plain-text truncation, that would corrupt
            # structure the model needs, not just drop content. Measured
            # max across all 547 real records is 174 (review_bridge/
            # round 5) -- this is a safety net, not expected to fire; fail
            # loudly rather than silently truncate into something broken.
            raise ValueError(
                f"prompt exceeds MAX_INPUT_LENGTH ({len(prompt_ids)} > "
                f"{MAX_INPUT_LENGTH} tokens) -- input: {ex['input'][:80]!r}"
            )

        target_ids = tokenizer(ex["target"], add_special_tokens=False)["input_ids"]
        target_ids = target_ids[:MAX_TARGET_LENGTH - 1]  # truncate BEFORE
            # appending EOS, not after -- an over-length example that got
            # truncated after appending EOS would have its EOS cut off
            # too, teaching the model no clean stop signal for exactly
            # the examples that most need one.

        input_ids = prompt_ids + target_ids + [tokenizer.eos_token_id]
        labels = [-100] * len(prompt_ids) + target_ids + [tokenizer.eos_token_id]
        pad_len = MAX_SEQ_LENGTH - len(input_ids)
        input_ids += [tokenizer.pad_token_id] * pad_len
        labels += [-100] * pad_len  # -100 explicitly, never the real pad token id
        attention_mask = [1] * (len(input_ids) - pad_len) + [0] * pad_len

        prepared.append({
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        })
    return prepared


def write_jsonl_atomic(records: list, path: Path) -> None:
    """Write JSONL via temp-file + validate + os.replace(), never truncating
    the destination until the replacement is known good.

    Exists for datasets/real_validation.jsonl and datasets/real_holdout.jsonl
    specifically. Those two files are gitignored, hand-written by the product
    owner, and the only artifacts in this project that cannot be regenerated
    -- DATASET_SPEC.md's real tier is defined by never having been touched by
    a generative model, so a lost record cannot be rebuilt, only replaced by
    a different note. The scripts that rewrite them (split_real_holdout.py,
    backfill_categories.py) previously opened the destination in "w" mode
    directly, which truncates on open: an exception, an interrupt, or a full
    disk between opening and finishing left a partial or empty file, and
    backfill_categories.py writes TWO such files in sequence, so a failure
    between them left the pair inconsistent. Flagged by an external review,
    2026-09-02.

    Validation happens on the temp file BEFORE the swap, so a schema-invalid
    write can never land on the real path (the previous code validated only
    after it had already overwritten the original).
    """
    tmp = path.with_name(path.name + ".tmp")
    try:
        with tmp.open("w", encoding="utf-8", newline="\n") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        load_jsonl(tmp)  # schema-gate the replacement before it lands
        os.replace(tmp, path)  # atomic on POSIX and Windows (same filesystem)
    except BaseException:
        tmp.unlink(missing_ok=True)  # leave the original untouched
        raise


def write_prepared(records: list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Load and schema-check every source file, print counts, exit -- no tokenizing.",
    )
    args = parser.parse_args()

    source_files = resolve_source_files()

    all_records = []
    for path in source_files:
        if not path.exists():
            print(f"skip (not found): {path.relative_to(REPO_ROOT)}")
            continue
        records = load_jsonl(path)
        print(f"{path.relative_to(REPO_ROOT)}: {len(records)} records validated OK")
        all_records += records

    train_records, selection_records = split_train_selection(all_records)
    print(
        f"Carved {len(selection_records)} of {len(all_records)} into the "
        f"model-selection slice (target {SELECTION_SLICE_FRACTION:.0%}, "
        f"content-hash bucketed per record -- see PDR-007), "
        f"{len(train_records)} remain for training."
    )

    # real_validation.jsonl: schema-checked for hygiene only. Since PDR-007
    # it is NOT written into prepared/ and NOT used for selection -- it
    # stays reserved for evaluate_real.py's own independent, untouched
    # reporting run against the real tier.
    real_validation_file = DATASETS_DIR / "real_validation.jsonl"
    real_validation_records = []
    if real_validation_file.exists():
        real_validation_records = load_jsonl(real_validation_file)
        print(
            f"{real_validation_file.relative_to(REPO_ROOT)}: "
            f"{len(real_validation_records)} records validated OK "
            f"(reporting only, via evaluate_real.py -- not used for "
            f"training or selection)"
        )
    else:
        print(f"{real_validation_file.relative_to(REPO_ROOT)}: not found")

    if not real_validation_records:
        print(
            "\nWARNING: datasets/real_validation.jsonl is empty or missing. "
            "Per DATASET_SPEC.md, this file is meant to be hand-written "
            "real notes, never generative-model-assisted -- it is NOT "
            "auto-populated from synthetic.jsonl by this script. "
            "evaluate_real.py will have nothing to report against until "
            "the product owner writes real examples into that file."
        )

    if args.validate_only:
        print(
            f"\n{len(train_records)} train records, {len(selection_records)} "
            f"selection records, {len(real_validation_records)} real-validation "
            f"records. Validation only, nothing written."
        )
        return

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_examples = build_examples(train_records)
    selection_examples = build_examples(selection_records)

    train_prepared = tokenize_examples(train_examples, tokenizer)
    selection_prepared = tokenize_examples(selection_examples, tokenizer)

    write_prepared(train_prepared, PREPARED_DIR / "train.jsonl")
    write_prepared(selection_prepared, PREPARED_DIR / "selection.jsonl")

    meta = {
        "model_name": MODEL_NAME,
        "max_input_length": MAX_INPUT_LENGTH,
        "max_target_length": MAX_TARGET_LENGTH,
        "max_seq_length": MAX_SEQ_LENGTH,
        "target_format": TARGET_FORMAT,
        "task_prefix": TASK_PREFIX,
        "train_examples": len(train_prepared),
        "selection_examples": len(selection_prepared),
        "selection_slice_fraction": SELECTION_SLICE_FRACTION,
        "train_sources": [str(p.relative_to(REPO_ROOT)) for p in source_files if p.exists()],
        "real_validation_examples": len(real_validation_records),
    }
    (PREPARED_DIR / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(
        f"\nWrote {len(train_prepared)} train / {len(selection_prepared)} "
        f"selection examples to {PREPARED_DIR.relative_to(REPO_ROOT)}/"
    )


if __name__ == "__main__":
    main()
