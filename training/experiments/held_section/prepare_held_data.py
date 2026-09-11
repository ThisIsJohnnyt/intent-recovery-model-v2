"""
Isolated, throwaway data prep for the HELD-section learnability test. See
this directory's design provenance: review_bridge/GeminiReview.md's round-9
ALIGNED verdict (2026-09-09) and docs/decisions/ (a PDR gets written only if
this test succeeds and HELD gets promoted for real -- see that round's
"After the test" section).

WHY THIS IS A FORK, NOT AN EXTENSION OF training/prepare_data.py:
training/prepare_data.py's serialize_target/deserialize_target is a proven,
tested contract that the production checkpoint, 532 real corpus records,
and 17 of 24 tests in training/tests/test_serialization.py currently depend
on. This experiment might not pan out -- that's the explicit premise of
"fail cheap." Extending the production module defensively for an untested
hypothesis would mean carrying that conditional complexity in shared code
regardless of outcome. So: a small, self-contained fork of JUST the
serialization functions, extended to a fourth "held" section. Everything
else (MODEL_NAME, MAX_INPUT_LENGTH, MAX_TARGET_LENGTH, TASK_PREFIX,
tokenization) is imported from the real prepare_data.py -- those aren't
part of the thing being tested, no reason to duplicate them.

If this test succeeds, the real implementation goes into prepare_data.py
properly, with its own updated tests, as a deliberate follow-up change --
this fork gets deleted, not promoted.

Usage (from this directory):
    python prepare_held_data.py
"""
import hashlib
import json
import sys
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).resolve().parent
TRAINING_DIR = EXPERIMENT_DIR.parent.parent
RAW_BATCH = EXPERIMENT_DIR / "raw_batch.jsonl"
PREPARED_DIR = EXPERIMENT_DIR / "prepared"

sys.path.insert(0, str(TRAINING_DIR))
import prepare_data  # noqa: E402  (reuse MODEL_NAME/MAX_*_LENGTH/TASK_PREFIX/tokenize_examples -- NOT serialize_target/deserialize_target, which are forked below)

# ~10/45 held back as an in-batch test set, per review_bridge round 2's
# "~35-45 train / ~10-15 held back" design. Content-hash bucketed (same
# technique as prepare_data.is_in_selection_slice, independently scoped to
# this experiment's own tiny batch) so membership depends only on each
# record's own input text, not its position in the file.
TEST_FRACTION = 0.22


def is_in_test_slice(record: dict) -> bool:
    digest = hashlib.sha256(record["input"].encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 1000
    return bucket < int(TEST_FRACTION * 1000)


def serialize_target_held(output: dict) -> str:
    """Forked from prepare_data.serialize_target -- adds a fourth
    ###HELD### section, appended after ###ACTIONS### (additive to the end,
    not interleaved, so the existing three sections' relative
    structure/order is unchanged for anyone eyeballing raw output)."""
    narrative = " ".join(output["narrative"].split("\n"))
    lines = ["###NARRATIVE###", narrative, "###BULLETS###"]
    lines += [f"- {b}" for b in output["bullets"]]
    lines.append("###ACTIONS###")
    lines += [f"- {a}" for a in output["action_items"]]
    lines.append("###HELD###")
    lines += [f"- {h}" for h in output.get("held", [])]
    return "\n".join(lines)


def deserialize_target_held(text: str) -> dict:
    """Forked from prepare_data.deserialize_target -- adds ###HELD### as a
    fourth marker. Same non-lossless " - " splitting heuristic as the
    original (see that function's docstring); accepted here for the same
    reason -- it matches what this experimental checkpoint is actually
    trained to produce."""
    import re
    parts = {"narrative": "", "bullets": [], "action_items": [], "held": []}
    marker_pattern = r"###NARRATIVE###|###BULLETS###|###ACTIONS###|###HELD###"
    chunks = re.split(marker_pattern, text)
    markers = re.findall(marker_pattern, text)
    field_by_marker = {
        "###BULLETS###": "bullets",
        "###ACTIONS###": "action_items",
        "###HELD###": "held",
    }
    for marker, content in zip(markers, chunks[1:]):
        content = content.strip()
        if marker == "###NARRATIVE###":
            parts["narrative"] = content
        else:
            field = field_by_marker[marker]
            items = [i.strip() for i in re.split(r"(?:^|\s)-\s", content)]
            parts[field] = [i for i in items if i]
    return parts


def build_examples_held(records: list) -> list:
    # Stale-fork fix, 2026-09-11: TASK_PREFIX used to be concatenated onto
    # the raw input string here because that's how the pre-PDR-012 seq2seq
    # pipeline's tokenize_examples() expected it. Since PDR-012's causal-LM
    # migration, prepare_data.tokenize_examples() applies TASK_PREFIX itself
    # via apply_chat_template as a system message -- concatenating it here
    # too would double it. Pass the raw input straight through, matching
    # the current production contract.
    return [
        {"input": r["input"],
         "target": serialize_target_held(r["output"])}
        for r in records
    ]


def write_prepared(records: list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def main():
    if not RAW_BATCH.exists():
        print(f"error: {RAW_BATCH} not found -- nothing to prepare.", file=sys.stderr)
        return 2

    records = []
    with RAW_BATCH.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    print(f"Loaded {len(records)} records from {RAW_BATCH.name}")

    train_records = [r for r in records if not is_in_test_slice(r)]
    test_records = [r for r in records if is_in_test_slice(r)]
    print(f"Split: {len(train_records)} train / {len(test_records)} held-back test "
          f"(content-hash bucketed, target {TEST_FRACTION:.0%})")

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(prepare_data.MODEL_NAME)

    train_examples = build_examples_held(train_records)
    train_prepared = prepare_data.tokenize_examples(train_examples, tokenizer)
    write_prepared(train_prepared, PREPARED_DIR / "train.jsonl")

    # train.py's TokenizedDataset reads "selection.jsonl" for its
    # load_best_model_at_end evaluation slice (same role PDR-007's
    # selection slice plays for the real pipeline) -- reuse the same
    # filename so train.py needs zero changes to consume this directory
    # via --data-dir, beyond the fix already aligned in round 3.
    selection_examples = build_examples_held(test_records)
    selection_prepared = prepare_data.tokenize_examples(selection_examples, tokenizer)
    write_prepared(selection_prepared, PREPARED_DIR / "selection.jsonl")

    # Held-back records are also kept as raw JSON (not just tokenized) so
    # the reader script can print real input/expected/actual after
    # training, same as evaluate_real.py does for the real tier.
    with (PREPARED_DIR / "test_records_raw.jsonl").open("w", encoding="utf-8") as f:
        for r in test_records:
            f.write(json.dumps(r) + "\n")

    meta = {
        "model_name": prepare_data.MODEL_NAME,
        "max_input_length": prepare_data.MAX_INPUT_LENGTH,
        "max_target_length": prepare_data.MAX_TARGET_LENGTH,
        "task_prefix": prepare_data.TASK_PREFIX,
        "train_examples": len(train_prepared),
        "selection_examples": len(selection_prepared),
        "test_fraction": TEST_FRACTION,
        "source": str(RAW_BATCH.relative_to(TRAINING_DIR.parent)),
        "note": "EXPERIMENTAL -- HELD-section learnability test, isolated "
                "from the production pipeline. See this file's module "
                "docstring.",
    }
    (PREPARED_DIR / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"\nWrote {len(train_prepared)} train / {len(selection_prepared)} "
          f"selection examples to {PREPARED_DIR.relative_to(TRAINING_DIR.parent)}/")


if __name__ == "__main__":
    main()
