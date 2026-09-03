#!/usr/bin/env python3
"""
Measure input->narrative similarity (the "copy ratio") across a dataset file
and fail when a record breaches the threshold.

WHY THIS EXISTS: docs/datasets/REVIEW_GUIDE.md calls this metric "the
strongest quantitative signal available" and records the corpus mean as
"settled at 0.561" with exactly two records permanently above 0.85 by
decision. Nothing in training/ ever computed it. It was recomputed by hand
inside review sessions, which meant it drifted invisibly between them: an
external review on 2026-09-02 measured the actual mean at 0.647 with 60
records above 0.85, and a monotonic climb from 0.497 in the earliest 75
records to 0.706 in the most recent 75. check_duplicates.py does NOT cover
this -- it measures input<->input similarity between records, a different
quantity entirely.

The rule this enforces is REVIEW_GUIDE.md ss4's "No non-recovery": every
other evidence rule in that section prohibits *adding* something, which
makes copying the input the degenerate optimum of the whole checklist.
This is the counterweight, and it is the only one of those rules that can
be checked mechanically.

IMPORTANT, per REVIEW_GUIDE.md's "Fixing voice raises the copy ratio":
this metric and the first-person-voice rule pull against each other -- the
cheapest way to stop describing a note is to start reciting it. Re-measure
BOTH after any narrative edit. Do not optimise this number in isolation.

Similarity function is imported from evaluate_real.py rather than
reimplemented, so the number here and the number that script reports for
real model output are the same measurement.

Usage (from the repository root or training/):
    python check_copy_ratio.py
    python check_copy_ratio.py --threshold 0.80
    python check_copy_ratio.py --dataset ../datasets/synthetic.jsonl --quiet

Exit codes: 0 = no non-allowlisted breach, 1 = at least one breach,
2 = bad invocation (missing file, etc).
"""
import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_real import word_ratio  # noqa: E402  -- single similarity impl

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = REPO_ROOT / "datasets" / "synthetic.jsonl"
DEFAULT_THRESHOLD = 0.85

# Keyed by sha256(input)[:16] rather than line number: line numbers shift the
# moment a record is inserted, removed, or reordered, and an allowlist that
# silently starts exempting the wrong record is worse than no allowlist.
ALLOWLIST = {
    "ac1f970c69ed67e3": (
        "dangling_reference/medium, 0.91 -- REVIEW_GUIDE.md ss6b: input is "
        "already a single well-formed sentence, so there is no structure left "
        "for the narrative to recover and the extraction work is entirely the "
        "bullets'. The narrative correctly leaves both 'he' and 'it' "
        "unresolved. Forcing this number down would mean padding."
    ),
    "2e8b25e9cc7db74b": (
        "simple_list/easy, 0.87 -- REVIEW_GUIDE.md ss6b: same rationale. A high "
        "ratio is the RIGHT answer for a short, already-ordered note."
    ),

    # --- Added 2026-09-02 after the product owner reviewed the full
    # disposition in docs/reviews/2026-09-02-copy-ratio-disposition.md and
    # approved all 58 calls. These 29 are the same shape as #118/#127 above:
    # the input is already short, already in the correct narrative order, or a
    # single continuous reflection, so a high ratio is the right answer and
    # forcing it down would mean padding. The other 29 breaches were rewritten
    # to genuinely reorganize instead. ---
    "b22ea34135ac1f82": (
        "dangling_reference/hard -- single flowing conditional sentence, "
        "already well-ordered; the ambiguous 'the blue one' and 'it' are "
        "correctly carried through unresolved."
    ),
    "ff97c2128eba856d": (
        "interrupted_thought/easy -- minimal content before the literal "
        "cutoff; the preserved cutoff itself dominates the text."
    ),
    "b53d08febfdbd9da": (
        "zero_action_items/easy -- three short observations already in "
        "natural order; the only available compression (tying the haze to "
        "the AQI) would invent a causal claim the input does not make."
    ),
    "ffdac11711824e66": (
        "rapid_branching/hard -- already an ordered conditional chain (if X "
        "then Y, unless Z); reordering would break the logic rather than "
        "recover it."
    ),
    "e8a13fec39707902": (
        "time_ambiguous/hard -- single already-ordered sentence, nothing "
        "left to reorganize."
    ),
    "70e784aca3b7b102": (
        "topic_switching/medium -- naturally sequential plan ('do X then "
        "Y'); chronological order is the correct narrative order."
    ),
    "4a05f1d8dba111a4": (
        "zero_action_items/medium -- single continuous observation narrated "
        "in the order it happened."
    ),
    "7c0c6750c77dd1cb": (
        "time_ambiguous/hard -- already logically ordered as hedge, hedge, "
        "deadline, which is also the right narrative order."
    ),
    "4f5b3aa44ba323df": (
        "time_ambiguous/hard -- natural sequential planning order (deadline "
        "hedge, call-to-check, milk on the way back)."
    ),
    "1e2fe17ce35e0ee3": (
        "zero_action_items/easy -- very short, single sentence."
    ),
    "2141a4d2d3d72d88": (
        "dangling_reference/easy -- short, two sentences."
    ),
    "d1911e8c4e740fac": (
        "zero_action_items/medium -- single continuous reminiscence; "
        "reordering someone's own train of memory would be artificial, not "
        "recovery."
    ),
    "26c04e3b8daf0666": (
        "time_ambiguous/medium -- short, sequential logical hedge (problem, "
        "plumber, when to call)."
    ),
    "88cd4e66bf16e56b": (
        "topic_switching/medium -- very short, two sentences."
    ),
    "57570b26ebded959": (
        "dangling_reference/hard -- short, two sentences, with a "
        "deliberately disconnected fragment; little to reorganize."
    ),
    "df27585ea26cdbcd": (
        "dangling_reference/medium -- single sentence."
    ),
    "ac98c375b6faa336": (
        "self_correction/expert -- compact list of four short facts already "
        "in a reasonable order; the retracted day has already been "
        "correctly dropped."
    ),
    "dd7b5b9d1dda8d76": (
        "contradictory_statement/hard -- very short, two sentences."
    ),
    "60c1d61fab759d39": (
        "contradictory_statement/easy -- short, single flowing "
        "deliberation; content confirmed correct in an earlier re-review."
    ),
    "6cbdf84c5ab0ee34": (
        "long_rambling/easy -- reflective monologue in natural "
        "chronological order; matches this category's own 'easy' definition "
        "of low structural complexity."
    ),
    "4fb0a1917cbdb77c": (
        "multi_person_note/easy -- short, single sentence; content "
        "confirmed correct in an earlier re-review."
    ),
    "a8cfbfc88ae7c9cc": (
        "contradictory_statement/expert -- short, single flowing sentence, "
        "already well-ordered."
    ),
    "137af4005bb77a89": (
        "interrupted_thought/easy -- minimal content before the literal "
        "cutoff, single clause."
    ),
    "a9a8ae729ff40367": (
        "interrupted_thought/easy -- minimal content before the literal "
        "cutoff, single clause."
    ),
    "42290905cb98eb65": (
        "interrupted_thought/easy -- minimal content before the literal "
        "cutoff, single clause."
    ),
    "d1bad3a1d3835fa8": (
        "zero_action_items/hard -- single flowing thought ending in genuine "
        "indecision; confirmed content-correct in the twelfth re-review, "
        "and the extraction work is the bullets'."
    ),
    "38aec1099460c13b": (
        "multi_person_note/easy -- very short, single sentence."
    ),
    "20718ddf7c2da9e5": (
        "multi_person_note/easy -- very short, single sentence."
    ),
    "c45b1c9d2282d8af": (
        "topic_switching/expert -- very short, two sentences."
    ),
}


def copy_ratio(record: dict) -> float:
    """Symmetric max of both argument orders.

    difflib's SequenceMatcher is not symmetric (its autojunk heuristic keys
    off the second sequence): on this corpus the two orders disagree by
    >0.005 on 55 of 525 records. Taking the max makes a record's score
    independent of argument order and is the conservative choice for
    copy detection. Both values REVIEW_GUIDE.md records as anchors --
    0.91 and 0.87 -- reproduce exactly under this definition, so it is
    comparable to the historical numbers in that document.
    """
    narrative = record["output"]["narrative"]
    text = record["input"]
    return max(word_ratio(narrative, text), word_ratio(text, narrative))


def load(path: Path) -> list:
    records = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if line:
                records.append((lineno, json.loads(line)))
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--quiet", action="store_true",
                    help="only print the summary and any breaches")
    ap.add_argument("--block-size", type=int, default=75,
                    help="records per position block in the drift table")
    args = ap.parse_args()

    if not args.dataset.exists():
        print(f"error: {args.dataset} not found", file=sys.stderr)
        return 2

    records = load(args.dataset)
    if not records:
        print(f"error: {args.dataset} has no records", file=sys.stderr)
        return 2

    scored = []
    for lineno, r in records:
        h = hashlib.sha256(r["input"].encode("utf-8")).hexdigest()[:16]
        scored.append((copy_ratio(r), lineno, r.get("category", "?"),
                       r.get("difficulty", "?"), h))

    vals = [s[0] for s in scored]
    n = len(vals)
    mean = sum(vals) / n
    ordered = sorted(vals)

    def pct(p):
        return ordered[min(int(p / 100 * n), n - 1)]

    print(f"{args.dataset.name}: {n} records")
    print(f"  mean {mean:.3f}   p50 {pct(50):.3f}   p90 {pct(90):.3f}   "
          f"p99 {pct(99):.3f}   max {max(vals):.3f}")
    print(f"  >{args.threshold}: {sum(v > args.threshold for v in vals)}"
          f"   >0.90: {sum(v > 0.90 for v in vals)}")

    if not args.quiet:
        by_cat = defaultdict(list)
        for v, _, c, _, _ in scored:
            by_cat[c].append(v)
        print("\nBy category (worst first):")
        for c, vs in sorted(by_cat.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
            print(f"  {sum(vs)/len(vs):.3f}  {c}  (n={len(vs)})")

        print("\nBy corpus position (drift -- a rising trend means generation "
              "is retreating into non-recovery):")
        for s in range(0, n, args.block_size):
            chunk = [x[0] for x in scored[s:s + args.block_size]]
            print(f"  records {s+1:>4}-{s+len(chunk):>4}: {sum(chunk)/len(chunk):.3f}")

    breaches = [s for s in scored if s[0] > args.threshold and s[4] not in ALLOWLIST]
    exempted = [s for s in scored if s[0] > args.threshold and s[4] in ALLOWLIST]

    if exempted:
        print(f"\nAllowlisted (above {args.threshold} by recorded decision, not counted):")
        for v, lineno, c, d, h in sorted(exempted, reverse=True):
            print(f"  line {lineno:>4}  {v:.3f}  [{c}/{d}]")
            print(f"      {ALLOWLIST[h]}")

    if breaches:
        print(f"\n{len(breaches)} record(s) above {args.threshold}, "
              f"not allowlisted:")
        for v, lineno, c, d, h in sorted(breaches, reverse=True):
            print(f"  line {lineno:>4}  {v:.3f}  [{c}/{d}]  {h}")
        print(f"\nThese are a DATA judgment, governed by "
              f"docs/datasets/REVIEW_GUIDE.md and the product owner's call -- "
              f"not a mechanical fix. Re-measure the voice checks after any "
              f"narrative edit; the two rules pull against each other.")
        return 1

    print(f"\nNo non-allowlisted record above {args.threshold}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
