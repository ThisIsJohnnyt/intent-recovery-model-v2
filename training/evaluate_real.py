#!/usr/bin/env python3
"""
Run a trained checkpoint against datasets/real_validation.jsonl -- the
generalization check this project's real tier exists for. See
DATASET_SPEC.md's "real_validation.jsonl" entry: no generative model wrote
these 15 examples, so a good result here means something a synthetic-only
eval can't -- that the model recovers a real person's notes, not just
Gemini's idea of what a messy note looks like.

This is deliberately NOT wired to real_holdout.jsonl. DATASET_SPEC.md is
explicit that the holdout tier is "evaluated only by a separate, explicit
holdout-evaluation script" -- sealed for declared release milestones, not
routine dev-time checks. Add that script only when there's an actual
release milestone to evaluate against, as its own deliberate action.

Reuses prepare_data.py's serialize_target/deserialize_target and
TASK_PREFIX rather than a second implementation of the model's I/O
contract -- see that module's "Model output serialization" docstring.

No automatic pass/fail scoring: at corpus sizes this small, a numeric
score would carry false precision. What this prints is (a) whether the
model's raw output even parses as the delimited format at all -- a
structural sanity check -- and (b) narrative-to-narrative and
narrative-to-input similarity, using this project's own established
copy-ratio methodology (see REVIEW_GUIDE.md ss4 "No non-recovery"), so a
model that's just echoing the input is visible the same way a bad
synthetic example would be. Full input/expected/actual is printed for
every example -- reading them is the actual evaluation.

Usage (from training/):
    python evaluate_real.py
    python evaluate_real.py --checkpoint checkpoints/flan-t5-base-v2.0
    python evaluate_real.py --max-new-tokens 384
"""
import argparse
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
DEFAULT_CHECKPOINT = Path(__file__).resolve().parent / "checkpoints" / "flan-t5-base-v2.0"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare_data  # noqa: E402  (reuse serialize/deserialize + TASK_PREFIX)


def word_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().split(), b.lower().split()).ratio()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT,
                    help="directory holding the fine-tuned model (default: training/checkpoints/flan-t5-base-v2.0)")
    ap.add_argument("--real-validation", type=Path, default=DATASETS_DIR / "real_validation.jsonl")
    ap.add_argument("--max-new-tokens", type=int, default=prepare_data.MAX_TARGET_LENGTH)
    ap.add_argument("--limit", type=int, default=None, help="evaluate only the first N examples")
    args = ap.parse_args()

    if not args.checkpoint.exists():
        print(f"error: checkpoint not found at {args.checkpoint}\n"
              f"Train one first (see training/train.py) -- there is nothing to evaluate yet.",
              file=sys.stderr)
        return 2

    records = prepare_data.load_jsonl(args.real_validation)
    if not records:
        print(f"error: {args.real_validation} has no records -- nothing to evaluate against.",
              file=sys.stderr)
        return 2
    if args.limit:
        records = records[:args.limit]

    print(f"Loading checkpoint from {args.checkpoint} ...")
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.checkpoint)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device).eval()
    print(f"Device: {device}. Evaluating {len(records)} example(s) from {args.real_validation.name}.\n")

    parse_ok = 0
    narrative_vs_expected, narrative_vs_input = [], []

    for i, r in enumerate(records, 1):
        prompt = prepare_data.TASK_PREFIX + r["input"]
        enc = tokenizer(prompt, max_length=prepare_data.MAX_INPUT_LENGTH,
                        truncation=True, return_tensors="pt").to(device)
        with torch.no_grad():
            out_ids = model.generate(**enc, max_new_tokens=args.max_new_tokens)
        raw_output = tokenizer.decode(out_ids[0], skip_special_tokens=True)
        parsed = prepare_data.deserialize_target(raw_output)

        structurally_valid = bool(parsed["narrative"])
        if structurally_valid:
            parse_ok += 1

        print(f"{'=' * 70}\n#{i} [{r.get('category', '?')}]")
        print(f"INPUT:    {r['input']}")
        print(f"EXPECTED: {r['output']['narrative']}")
        print(f"  bullets:      {r['output']['bullets']}")
        print(f"  action_items: {r['output']['action_items']}")
        print(f"ACTUAL:   {parsed['narrative'] or '(did not parse -- raw output below)'}")
        if not structurally_valid:
            print(f"  raw model output: {raw_output!r}")
        else:
            print(f"  bullets:      {parsed['bullets']}")
            print(f"  action_items: {parsed['action_items']}")
            r_exp = word_ratio(parsed["narrative"], r["output"]["narrative"])
            r_inp = word_ratio(parsed["narrative"], r["input"])
            narrative_vs_expected.append(r_exp)
            narrative_vs_input.append(r_inp)
            print(f"  narrative-vs-expected similarity: {r_exp:.2f}   "
                  f"narrative-vs-input similarity: {r_inp:.2f}")
        print()

    print(f"{'=' * 70}\nSummary: {parse_ok}/{len(records)} produced a structurally valid "
          f"(parseable) output.")
    if narrative_vs_expected:
        print(f"Mean narrative-vs-expected similarity: "
              f"{sum(narrative_vs_expected) / len(narrative_vs_expected):.2f}")
        print(f"Mean narrative-vs-input similarity:    "
              f"{sum(narrative_vs_input) / len(narrative_vs_input):.2f}  "
              f"(high here means the model is echoing the input rather than recovering it -- "
              f"see REVIEW_GUIDE.md's 'No non-recovery')")
    print("\nThese numbers are not a pass/fail score -- read the per-example output above. "
          "At this corpus size a small numeric summary would carry false precision.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
