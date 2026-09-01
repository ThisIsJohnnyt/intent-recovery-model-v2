"""
Data preparation for intent-recovery-model-v2's fine-tuning pipeline.
See training/DATASET_SPEC.md's "Model output serialization" and "Task
prefix" sections for the exact contract this module implements.

Stages: load raw JSONL -> validate against the schema -> serialize each
record's `output` into the model's actual training target (the delimited
###NARRATIVE###/###BULLETS###/###ACTIONS### format) -> tokenize with
google/flan-t5-base's tokenizer -> write token-id JSONL that train.py
reads directly.

Split, per DATASET_SPEC.md's "Where files go": train = synthetic.jsonl +
any consolidated gold releases; val = real_validation.jsonl. This is a
split BY FILE, not a random carve-out of synthetic.jsonl -- real_validation
exists specifically so the eval signal isn't contaminated by the same
model that generated the training data. See main()'s warning if that file
is empty.

Usage (from training/):
    python prepare_data.py                 # full run, writes to prepared/
    python prepare_data.py --validate-only  # schema check only, no tokenizing
"""
import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
PREPARED_DIR = Path(__file__).resolve().parent / "prepared"

MODEL_NAME = "google/flan-t5-base"
MAX_INPUT_LENGTH = 256
MAX_TARGET_LENGTH = 384  # narrative + bullets + actions can run longer than input
TASK_PREFIX = "Recover the intent behind these scattered notes:\n\n"

REQUIRED_TOP = {"input", "output"}
REQUIRED_OUTPUT = {"narrative", "bullets", "action_items"}
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
    """dict -> the literal delimited text the model is trained to
    generate. This function IS DATASET_SPEC.md's "Model output
    serialization" spec, not a separate reimplementation of it."""
    narrative = " ".join(output["narrative"].split("\n"))  # defensive, not expected
    lines = ["###NARRATIVE###", narrative, "###BULLETS###"]
    lines += [f"- {b}" for b in output["bullets"]]
    lines.append("###ACTIONS###")
    lines += [f"- {a}" for a in output["action_items"]]
    return "\n".join(lines)


def deserialize_target(text: str) -> dict:
    """Inverse of serialize_target() -- text -> dict. Used to check real
    model output at eval time against the same logic that built the
    training targets, rather than a second hand-written parser that could
    silently drift from what training actually used.

    Does NOT split on literal "\\n". flan-t5's SentencePiece tokenizer
    normalizes "\\n" to a plain space at *encode* time -- confirmed by
    tokenizing "X\\nY" and "X Y" and getting identical token ids -- so a
    real generated sequence never contains a newline to split on in the
    first place, and neither did the training targets built by
    serialize_target() above once they passed through the tokenizer. A
    trained checkpoint's raw output looks like:
        "###NARRATIVE### text here ###BULLETS### - one - two ###ACTIONS### - a1"
    all on one line. Found 2026-08-25 when the first real eval run showed
    every example failing to parse despite the raw output visibly
    containing all three markers in order with real content -- the parser
    was checking for a newline that no longer existed anywhere in the
    pipeline, not a model or data defect.

    Splits on the marker strings directly instead, then splits each
    list section on " - " (matching how serialize_target's own "- {item}"
    lines get glued back-to-back by the same normalization). This is a
    heuristic, not lossless: an item whose own text contains a literal
    " - " substring will be split apart. Accepted for now since it matches
    what the model was actually trained to produce; revisit if that
    collision shows up in practice."""
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
    """record -> {"input": ..., "target": ...} training pair. The task
    prefix is applied here, not left for the caller to remember."""
    return [
        {"input": TASK_PREFIX + r["input"], "target": serialize_target(r["output"])}
        for r in records
    ]


def resolve_split_files() -> tuple:
    """Per DATASET_SPEC.md's 'Where files go': train = synthetic + any
    consolidated gold releases; val = real_validation.jsonl -- kept
    separate specifically so eval signal isn't contaminated by the same
    model that generated the training data."""
    train_files = [DATASETS_DIR / "synthetic.jsonl"]
    train_files += sorted((DATASETS_DIR / "gold").glob("gold_v*.jsonl"))
    val_file = DATASETS_DIR / "real_validation.jsonl"
    return train_files, val_file


def tokenize_examples(examples: list, tokenizer) -> list:
    prepared = []
    for ex in examples:
        input_enc = tokenizer(
            ex["input"], max_length=MAX_INPUT_LENGTH, truncation=True, padding="max_length"
        )
        target_enc = tokenizer(
            ex["target"], max_length=MAX_TARGET_LENGTH, truncation=True, padding="max_length"
        )
        # -100 is the standard HF convention for "ignore this position in
        # the loss" -- padding must not contribute gradient.
        labels = [
            tok if tok != tokenizer.pad_token_id else -100
            for tok in target_enc["input_ids"]
        ]
        prepared.append({
            "input_ids": input_enc["input_ids"],
            "attention_mask": input_enc["attention_mask"],
            "labels": labels,
        })
    return prepared


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

    train_files, val_file = resolve_split_files()

    train_records = []
    for path in train_files:
        if not path.exists():
            print(f"skip (not found): {path.relative_to(REPO_ROOT)}")
            continue
        records = load_jsonl(path)
        print(f"{path.relative_to(REPO_ROOT)}: {len(records)} records validated OK")
        train_records += records

    val_records = []
    if val_file.exists():
        val_records = load_jsonl(val_file)
        print(f"{val_file.relative_to(REPO_ROOT)}: {len(val_records)} records validated OK")
    else:
        print(f"{val_file.relative_to(REPO_ROOT)}: not found")

    if not val_records:
        print(
            "\nWARNING: no validation examples "
            "(datasets/real_validation.jsonl is empty or missing). Per "
            "DATASET_SPEC.md, this file is meant to be hand-written real "
            "notes, never generative-model-assisted -- it is NOT "
            "auto-populated from synthetic.jsonl by this script. Training "
            "will proceed with an empty validation set until the product "
            "owner writes real examples into that file."
        )

    if args.validate_only:
        print(
            f"\n{len(train_records)} train records, {len(val_records)} val "
            f"records. Validation only, nothing written."
        )
        return

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_examples = build_examples(train_records)
    val_examples = build_examples(val_records)

    train_prepared = tokenize_examples(train_examples, tokenizer)
    val_prepared = tokenize_examples(val_examples, tokenizer)

    write_prepared(train_prepared, PREPARED_DIR / "train.jsonl")
    write_prepared(val_prepared, PREPARED_DIR / "val.jsonl")

    meta = {
        "model_name": MODEL_NAME,
        "max_input_length": MAX_INPUT_LENGTH,
        "max_target_length": MAX_TARGET_LENGTH,
        "task_prefix": TASK_PREFIX,
        "train_examples": len(train_prepared),
        "val_examples": len(val_prepared),
        "train_sources": [str(p.relative_to(REPO_ROOT)) for p in train_files if p.exists()],
        "val_source": str(val_file.relative_to(REPO_ROOT)) if val_file.exists() else None,
    }
    (PREPARED_DIR / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(
        f"\nWrote {len(train_prepared)} train / {len(val_prepared)} val "
        f"examples to {PREPARED_DIR.relative_to(REPO_ROOT)}/"
    )


if __name__ == "__main__":
    main()
