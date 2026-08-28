#!/usr/bin/env python3
"""
One-time (per real-tier growth) random split of datasets/real_validation.jsonl
into a sealed datasets/real_holdout.jsonl and the remaining validation set.

Both files are gitignored (training/DATASET_SPEC.md's "Where files go"), so
the split itself leaves no trace in git -- this script exists partly to
produce a record someone can paste into a tracked file (DATASET_SPEC.md) as
proof the split was a genuine random draw and not hand-picked.

METHOD
------
The seed is drawn from os.urandom() at run time -- nobody chooses it,
including the person running this script -- then printed and used to shuffle
the current line order with Python's random.Random(seed). The first
`--holdout` records after shuffling go to real_holdout.jsonl; the rest stay
in real_validation.jsonl. Printed output names exactly which record (by its
`input` text) went where, so the split is auditable from the transcript alone
even without re-running the script.

SEALING
-------
Refuses to run if real_holdout.jsonl already has content, unless --reseal is
passed explicitly. DATASET_SPEC.md's holdout tier is "sealed for declared
release milestones only" -- silently reshuffling a sealed holdout on a later
run would quietly break that. Future real notes, once converted, are meant to
land in real_validation.jsonl only; this script is not the intended way to
add to an already-sealed holdout.

USAGE
-----
    python training/split_real_holdout.py --holdout 12
"""
import argparse
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare_data  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--validation", type=Path,
                    default=Path(__file__).resolve().parent.parent / "datasets" / "real_validation.jsonl")
    ap.add_argument("--holdout-file", type=Path,
                    default=Path(__file__).resolve().parent.parent / "datasets" / "real_holdout.jsonl")
    ap.add_argument("--holdout", type=int, required=True,
                    help="number of records to seal into real_holdout.jsonl")
    ap.add_argument("--reseal", action="store_true",
                    help="allow re-splitting an already-sealed (non-empty) holdout file")
    args = ap.parse_args()

    if args.holdout_file.exists() and args.holdout_file.stat().st_size > 0 and not args.reseal:
        print(f"error: {args.holdout_file} is already sealed (non-empty). "
              f"Pass --reseal to override -- this is not the normal path.", file=sys.stderr)
        return 2

    records = prepare_data.load_jsonl(args.validation)
    n = len(records)
    if args.holdout >= n:
        print(f"error: --holdout {args.holdout} >= {n} total records", file=sys.stderr)
        return 2

    seed = int.from_bytes(os.urandom(8), "big")
    rng = random.Random(seed)
    order = list(range(n))
    rng.shuffle(order)

    holdout_idx = sorted(order[:args.holdout])
    validation_idx = sorted(order[args.holdout:])

    print(f"seed (os.urandom-drawn): {seed}")
    print(f"total: {n}  ->  holdout: {len(holdout_idx)}  validation: {len(validation_idx)}\n")

    print(f"SEALED into {args.holdout_file.name}:")
    for i in holdout_idx:
        print(f"  [{i:>3}] {records[i]['input'][:76]}")
    print(f"\nStaying in {args.validation.name}:")
    for i in validation_idx:
        print(f"  [{i:>3}] {records[i]['input'][:76]}")

    with args.holdout_file.open("w", encoding="utf-8", newline="\n") as f:
        for i in holdout_idx:
            f.write(json.dumps(records[i], ensure_ascii=False) + "\n")
    with args.validation.open("w", encoding="utf-8", newline="\n") as f:
        for i in validation_idx:
            f.write(json.dumps(records[i], ensure_ascii=False) + "\n")

    prepare_data.load_jsonl(args.holdout_file)
    prepare_data.load_jsonl(args.validation)
    print(f"\nWrote and validated both files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
