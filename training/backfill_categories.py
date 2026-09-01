#!/usr/bin/env python3
"""
Mechanical backfill: merge `category` from the tagged
"Real Examples for Human Input.txt" into datasets/real_validation.jsonl and
datasets/real_holdout.jsonl, without re-running the split or touching
anything else.

WHY A SEPARATE SCRIPT RATHER THAN RE-RUNNING convert_real_notes.py
-------------------------------------------------------------------
The 27 real notes were already converted once and split into a sealed
holdout (12) and validation (15) -- see DATASET_SPEC.md's split record,
2026-08-25. Re-running convert_real_notes.py --out would regenerate a
fresh 27-record file with no relationship to that split; writing it over
either existing file would silently unseal the holdout. This script only
ever adds a "category" field to a record that already exists in one of
the two target files, matched by its "input" text verbatim. It does not
call split_real_holdout.py and does not touch "input"/"output" at all.

Same "refuse rather than guess" discipline as convert_real_notes.py: an
entry that doesn't match exactly one record across both target files is
refused, not silently skipped or guessed at.

USAGE
-----
    # dry run -- parse, match, report, write nothing
    python training/backfill_categories.py "training/Real Examples for Human Input.txt"

    # write it
    python training/backfill_categories.py "training/Real Examples for Human Input.txt" --apply

Exit status is non-zero if any entry was refused.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import convert_real_notes as converter  # noqa: E402  (reuse its parser)
import prepare_data  # noqa: E402

VALID_CATEGORIES = {
    "simple_list", "interrupted_thought", "topic_switching", "topic_interleaving",
    "dangling_reference", "repeated_reminder", "zero_action_items",
    "contradictory_statement", "rapid_branching", "minimal_fragment",
    "long_rambling", "multi_person_note", "voice_to_text_artifact",
    "self_correction", "time_ambiguous",
}


def load_target(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("source", type=Path, help="the tagged plain-text notes file")
    ap.add_argument("--validation", type=Path,
                    default=Path(__file__).resolve().parent.parent / "datasets" / "real_validation.jsonl")
    ap.add_argument("--holdout", type=Path,
                    default=Path(__file__).resolve().parent.parent / "datasets" / "real_holdout.jsonl")
    ap.add_argument("--apply", action="store_true", help="write the backfilled category fields")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"error: {args.source} does not exist", file=sys.stderr)
        return 2

    raw = args.source.read_text(encoding="utf-8-sig")
    entries, refusals = converter.parse(raw)
    for r in refusals:
        print(f"REFUSED (source parse) -- {r}")

    tagged = [e for e in entries if e["record"].get("category")]
    untagged = [e for e in entries if not e["record"].get("category")]
    print(f"Parsed {len(entries)} entries: {len(tagged)} tagged, {len(untagged)} untagged.")
    for e in untagged:
        print(f"  entry {e['no']}: no category tag")

    bad_cat = [e for e in tagged if e["record"]["category"] not in VALID_CATEGORIES]
    for e in bad_cat:
        print(f"REFUSED -- entry {e['no']}: '{e['record']['category']}' is not a known category "
              f"(see training/category_quick_reference.md)")
    tagged = [e for e in tagged if e not in bad_cat]

    val_records = load_target(args.validation)
    hold_records = load_target(args.holdout)
    by_input = {}
    for src_name, records in ((args.validation.name, val_records), (args.holdout.name, hold_records)):
        for rec in records:
            by_input.setdefault(rec["input"], []).append((src_name, rec))

    matched, unmatched, ambiguous, conflicting = [], [], [], []
    for e in tagged:
        note = e["record"]["input"]
        hits = by_input.get(note, [])
        if not hits:
            unmatched.append(e)
        elif len(hits) > 1:
            ambiguous.append(e)
        else:
            src_name, rec = hits[0]
            if "category" in rec and rec["category"] != e["record"]["category"]:
                conflicting.append((e, src_name, rec["category"]))
            else:
                matched.append((e, src_name, rec))

    for e in unmatched:
        print(f"REFUSED -- entry {e['no']}: input not found (verbatim) in "
              f"{args.validation.name} or {args.holdout.name}")
    for e in ambiguous:
        print(f"REFUSED -- entry {e['no']}: input matches more than one record across both files")
    for e, src_name, existing in conflicting:
        print(f"REFUSED -- entry {e['no']}: {src_name} already has category "
              f"'{existing}', source says '{e['record']['category']}'")

    print(f"\n{len(matched)} of {len(entries)} entries ready to backfill "
          f"({len(untagged) + len(bad_cat) + len(unmatched) + len(ambiguous) + len(conflicting)} refused).")

    ok = not (untagged or bad_cat or unmatched or ambiguous or conflicting)

    if not args.apply:
        print("\n(dry run -- pass --apply to write)")
        return 0 if ok else 1

    if not ok:
        print("\nerror: refusing to write while any entry is refused -- fix the source or re-run without --apply "
              "to see what's still outstanding", file=sys.stderr)
        return 1

    for e, src_name, rec in matched:
        rec["category"] = e["record"]["category"]

    with args.validation.open("w", encoding="utf-8", newline="\n") as f:
        for rec in val_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with args.holdout.open("w", encoding="utf-8", newline="\n") as f:
        for rec in hold_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    prepare_data.load_jsonl(args.validation)
    prepare_data.load_jsonl(args.holdout)
    print(f"\nWrote categories to {args.validation.name} and {args.holdout.name}; both validate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
