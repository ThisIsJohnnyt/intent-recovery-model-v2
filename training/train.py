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

# Warn when the best validation loss exceeds the final training loss by
# this ratio. Overfitting is what we actually care about, so measure it
# directly rather than using corpus size as a proxy for it.
#
# Replaced SMALL_CORPUS_WARNING_THRESHOLD = 500 on 2026-09-02 (external
# review, finding M8). That constant was calibrated to the corpus *target*
# rather than to observed overfitting, which made it useless twice over:
# the corpus passed 500 so it could never fire again, and the run that
# motivated it -- train 0.4654 / eval 1.6 after 8 epochs, a 3.4x gap --
# had exactly 500 examples, so it would not have fired for that run
# either. A ratio needs no recalibration as the corpus grows.
OVERFIT_RATIO_WARNING = 1.5


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


def report_overfit(trainer, is_smoke_test: bool) -> None:
    """Post-run check on the signal we actually care about: how far the
    best validation loss sits above the final training loss.

    Reads trainer.state.log_history rather than recomputing anything --
    the Trainer already logged every eval. Also names the epoch that
    produced the best eval_loss, because with load_best_model_at_end that
    is the checkpoint actually being saved: a best epoch well before the
    last one is direct evidence the later epochs were overfitting, and
    that the checkpoint-selection is earning its keep.
    """
    history = getattr(trainer.state, "log_history", None) or []
    evals = [(h["eval_loss"], h.get("epoch")) for h in history if "eval_loss" in h]
    if not evals:
        return  # no validation set; the no-val warning already fired

    finals = [h["train_loss"] for h in history if "train_loss" in h]
    if not finals:
        finals = [h["loss"] for h in history if "loss" in h][-1:]
    if not finals:
        return
    train_loss = finals[-1]
    best_eval, best_epoch = min(evals, key=lambda t: t[0])
    last_eval = evals[-1][0]

    print()
    ep = f"{best_epoch:.2f}" if isinstance(best_epoch, float) else str(best_epoch)
    print(f"final train_loss {train_loss:.4f}   best eval_loss {best_eval:.4f}"
          f" (epoch {ep})   last eval_loss {last_eval:.4f}")
    if len(evals) > 1 and best_epoch is not None and evals[-1][1] != best_epoch:
        print(f"  eval_loss was still improving at epoch {ep} and got worse "
              f"after -- the saved checkpoint is that epoch, not the last one.")

    if is_smoke_test:
        print("  (smoke test -- loss numbers are not meaningful)")
        return
    if train_loss <= 0:
        return
    ratio = best_eval / train_loss
    if ratio > OVERFIT_RATIO_WARNING:
        print(
            f"\n  WARNING: best eval_loss is {ratio:.1f}x the final train_loss "
            f"(threshold {OVERFIT_RATIO_WARNING}x). The model fits the training "
            f"corpus substantially better than held-out data, which is what "
            f"overfitting looks like. load_best_model_at_end has kept the "
            f"least-overfit checkpoint available, but that only picks the best of "
            f"epochs actually run -- it does not remove the gap. Read the eval "
            f"output before treating this checkpoint as deployable; see "
            f"training/evaluate_real.py.\n"
        )
    else:
        print(f"  eval/train loss ratio {ratio:.1f}x, under the "
              f"{OVERFIT_RATIO_WARNING}x warning threshold.")


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

    if len(val_ds) == 0:
        print(
            "WARNING: no validation examples -- eval loss won't be "
            "reported. See prepare_data.py's own warning about "
            "datasets/real_validation.jsonl.\n"
        )

    tokenizer = AutoTokenizer.from_pretrained(meta["model_name"])
    model = AutoModelForSeq2SeqLM.from_pretrained(meta["model_name"])

    # Keep the best-generalizing checkpoint, not just whatever state exists
    # after the last epoch. The first real run (2026-09-02, 500 examples)
    # showed eval_loss (1.6) well above train_loss (0.47) after 8 epochs --
    # a classic overfitting signature at this corpus size -- and train.py
    # was evaluating every epoch but never acting on that signal, saving
    # the final (likely most-overfit) state regardless. Only possible when
    # there's a validation set to evaluate against; falls back to the old
    # save-only-at-the-end behavior otherwise, since load_best_model_at_end
    # requires save_strategy to match eval_strategy.
    has_val = len(val_ds) > 0
    training_args = Seq2SeqTrainingArguments(
        output_dir=str(args.output_dir),
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        eval_strategy="epoch" if has_val else "no",
        save_strategy="epoch" if has_val else "no",
        save_total_limit=2 if has_val else None,  # keep best + most recent only
        load_best_model_at_end=has_val,
        metric_for_best_model="eval_loss" if has_val else None,
        greater_is_better=False if has_val else None,
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

    report_overfit(trainer, is_smoke_test=args.max_steps != -1)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(args.output_dir))
    tokenizer.save_pretrained(str(args.output_dir))
    print(f"\nSaved model + tokenizer to {args.output_dir}")


if __name__ == "__main__":
    main()
