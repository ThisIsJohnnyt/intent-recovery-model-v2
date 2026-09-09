#!/usr/bin/env python3
"""
Reads the HELD-section experimental checkpoint's output against the 7
records held back from training (prepare_held_data.py's test slice) --
genuinely unseen by this checkpoint, not just held out of the loss
computation.

Uses the FORKED deserialize_target_held from this directory, not
prepare_data.deserialize_target / evaluate_real.py -- the production
3-marker parser would silently misparse this checkpoint's 4-section
output (###HELD### content absorbed into whatever section precedes it).
See prepare_held_data.py's module docstring for why this fork exists.

No automated pass/fail scoring, same principle as evaluate_real.py: at
this size a numeric score carries false precision. Prints full
input/expected/actual for every held-back record -- reading them is the
actual evaluation. The product owner judges: did held-worthy content
route to "held" rather than being forced into bullets/action_items?

Usage (from this directory):
    python read_held_results.py
"""
import json
import sys
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).resolve().parent
TRAINING_DIR = EXPERIMENT_DIR.parent.parent
CHECKPOINT = TRAINING_DIR / "checkpoints" / "experiment-held-section"
TEST_RECORDS = EXPERIMENT_DIR / "prepared" / "test_records_raw.jsonl"

sys.path.insert(0, str(TRAINING_DIR))
import prepare_data  # noqa: E402  (TASK_PREFIX, MAX_INPUT_LENGTH, MAX_TARGET_LENGTH)
from evaluate_real import ConsecutiveRepeatStop, dedupe_consecutive  # noqa: E402
from prepare_held_data import deserialize_target_held  # noqa: E402


def main():
    if not CHECKPOINT.exists():
        print(f"error: checkpoint not found at {CHECKPOINT} -- run train.py "
              f"against this experiment's prepared/ first.", file=sys.stderr)
        return 2
    if not TEST_RECORDS.exists():
        print(f"error: {TEST_RECORDS} not found -- run prepare_held_data.py "
              f"first.", file=sys.stderr)
        return 2

    records = []
    with TEST_RECORDS.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"Loading checkpoint from {CHECKPOINT} ...")
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, StoppingCriteriaList
    tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)
    model = AutoModelForSeq2SeqLM.from_pretrained(CHECKPOINT)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device).eval()
    print(f"Device: {device}. Evaluating {len(records)} held-back "
          f"(genuinely unseen) example(s).\n")

    stopping_criteria = StoppingCriteriaList([ConsecutiveRepeatStop()])
    routed_correctly = 0
    routed_missed = 0

    for i, r in enumerate(records, 1):
        prompt = prepare_data.TASK_PREFIX + r["input"]
        enc = tokenizer(prompt, max_length=prepare_data.MAX_INPUT_LENGTH,
                         truncation=True, return_tensors="pt").to(device)
        with torch.no_grad():
            out_ids = model.generate(
                **enc,
                max_new_tokens=prepare_data.MAX_TARGET_LENGTH,
                stopping_criteria=stopping_criteria,
            )
        raw_output = tokenizer.decode(out_ids[0], skip_special_tokens=True)
        parsed = deserialize_target_held(raw_output)
        parsed["bullets"] = dedupe_consecutive(parsed["bullets"])
        parsed["action_items"] = dedupe_consecutive(parsed["action_items"])
        parsed["held"] = dedupe_consecutive(parsed["held"])

        expected_held = r["output"].get("held", [])
        got_held = parsed["held"]
        # Directional signal only, not a score: did the checkpoint produce
        # ANY held item on a record that has ANY expected held item, or
        # correctly produce none on a record with none expected. Doesn't
        # check content match -- that's for the product owner to read.
        if bool(expected_held) == bool(got_held):
            routed_correctly += 1
        else:
            routed_missed += 1

        print(f"{'=' * 70}\n#{i} [{r.get('category', '?')}/{r.get('difficulty', '?')}]")
        print(f"INPUT:    {r['input']}")
        print(f"EXPECTED  narrative: {r['output']['narrative']}")
        print(f"          bullets:      {r['output']['bullets']}")
        print(f"          action_items: {r['output']['action_items']}")
        print(f"          held:         {expected_held}")
        if not parsed["narrative"]:
            print(f"ACTUAL    (did not parse -- raw output below)")
            print(f"          raw model output: {raw_output!r}")
        else:
            print(f"ACTUAL    narrative: {parsed['narrative']}")
            print(f"          bullets:      {parsed['bullets']}")
            print(f"          action_items: {parsed['action_items']}")
            print(f"          held:         {got_held}")
        print()

    print(f"{'=' * 70}\nSummary: {len(records)} held-back (unseen) records.")
    print(f"Coarse routing signal (has-any-held vs. expects-any-held match): "
          f"{routed_correctly}/{len(records)}")
    print("\nThis is NOT a pass/fail score -- it only checks whether the "
          "checkpoint produced something in 'held' when something was "
          "expected there, not whether the CONTENT is right. At this "
          "sample size (7 unseen records) read every example above -- "
          "that's the actual evaluation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
