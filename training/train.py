"""
Fine-tuning script for intent-recovery-model-v2. Reads
training/prepared/{train,val}.jsonl produced by prepare_data.py -- already
tokenized, padded, and labeled -- and fine-tunes the base model named in
training/prepared/meta.json (google/flan-t5-base as of this writing).

Usage (from training/, after running prepare_data.py):
    python train.py                           # a real run, defaults below
    python train.py --max-steps 5              # smoke test only -- proves
                                                 # the pipeline runs end to
                                                 # end, not a usable model
"""
import argparse
import json
from pathlib import Path

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

PREPARED_DIR = Path(__file__).resolve().parent / "prepared"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "checkpoints" / "flan-t5-base-v2.0"

# Below this many training examples, a run is a pipeline correctness check,
# not a deployable checkpoint -- see training/DATASET_SPEC.md and
# docs/datasets/CATEGORY_REFERENCE.md for actual corpus size/target.
SMALL_CORPUS_WARNING_THRESHOLD = 500


class TokenizedDataset(Dataset):
    """Reads prepare_data.py's token-id JSONL directly -- already padded
    and labeled (labels use -100 for positions the loss should ignore per
    the standard HF convention), so this is just a thin list-backed
    Dataset. No collation logic needed since nothing here is variable
    length."""

    def __init__(self, path: Path):
        self.records = []
        if not path.exists():
            return
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.records.append(json.loads(line))

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        r = self.records[idx]
        return {
            "input_ids": torch.tensor(r["input_ids"], dtype=torch.long),
            "attention_mask": torch.tensor(r["attention_mask"], dtype=torch.long),
            "labels": torch.tensor(r["labels"], dtype=torch.long),
        }


def load_meta() -> dict:
    meta_path = PREPARED_DIR / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(
            f"{meta_path} not found -- run prepare_data.py first. This "
            f"script reads its output; it doesn't tokenize raw data itself."
        )
    return json.loads(meta_path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=float, default=8.0)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--max-steps", type=int, default=-1,
        help="Cap total optimizer steps, overriding --epochs. Use a small "
             "value (e.g. 5) to smoke-test the pipeline without a real run.",
    )
    args = parser.parse_args()

    meta = load_meta()
    print(
        f"Prepared data: {meta['train_examples']} train / "
        f"{meta['val_examples']} val examples, model={meta['model_name']}"
    )

    train_ds = TokenizedDataset(PREPARED_DIR / "train.jsonl")
    val_ds = TokenizedDataset(PREPARED_DIR / "val.jsonl")
    print(f"Loaded {len(train_ds)} train / {len(val_ds)} val examples")

    if len(train_ds) == 0:
        raise SystemExit("No training examples -- run prepare_data.py first.")

    if len(train_ds) < SMALL_CORPUS_WARNING_THRESHOLD and args.max_steps == -1:
        print(
            f"\nWARNING: only {len(train_ds)} training examples (threshold "
            f"for this warning: {SMALL_CORPUS_WARNING_THRESHOLD}). A run "
            f"this small will overfit -- treat the resulting checkpoint as "
            f"a pipeline correctness check, not a deployable model. Pass "
            f"--max-steps to make that explicit, or ignore this if that's "
            f"exactly what you're doing.\n"
        )

    if len(val_ds) == 0:
        print(
            "WARNING: no validation examples -- eval loss won't be "
            "reported. See prepare_data.py's own warning about "
            "datasets/real_validation.jsonl.\n"
        )

    tokenizer = AutoTokenizer.from_pretrained(meta["model_name"])
    model = AutoModelForSeq2SeqLM.from_pretrained(meta["model_name"])

    training_args = Seq2SeqTrainingArguments(
        output_dir=str(args.output_dir),
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        eval_strategy="epoch" if len(val_ds) > 0 else "no",
        save_strategy="no",  # we save explicitly at the end, not per-epoch checkpoints
        logging_steps=1,
        predict_with_generate=False,
        report_to=[],
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds if len(val_ds) > 0 else None,
    )

    trainer.train()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(args.output_dir))
    tokenizer.save_pretrained(str(args.output_dir))
    print(f"\nSaved model + tokenizer to {args.output_dir}")


if __name__ == "__main__":
    main()
