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

Similarity function (word_ratio) is imported from evaluate_real.py rather
than reimplemented, so both scripts tokenize and score a single pair of
strings identically -- but the AGGREGATE number each script reports is
not the same measurement (corrected 2026-09-08, external review Claude
API/Fable 5.1, finding C5, which read this claim as stronger than it is):
copy_ratio() below takes max(word_ratio(a,b), word_ratio(b,a)) across
both argument orders, while evaluate_real.py reports a single order
directly. Comparable, sharing the same underlying tokenization and
sequence-matching, but not identical numbers for the same record.

Usage (from the repository root or training/):
    python check_copy_ratio.py
    python check_copy_ratio.py --threshold 0.80
    python check_copy_ratio.py --dataset ../datasets/synthetic.jsonl --quiet

Exit codes: 0 = no non-allowlisted breach, no allowlisted record over its
own ceiling, and no orphaned allowlist entry; 1 = at least one of those
three; 2 = bad invocation (missing file, etc).
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
# Raised from 0.85 to 0.90, 2026-09-08 (docs/decisions/PDR-011.md). 0.85 was
# calibrated entirely from within the synthetic-batch history this docstring
# describes above -- never checked against real data. All 15
# real_validation.jsonl records measure 0.429-0.889 (mean 0.690); 0.90 sits
# just above that observed ceiling rather than being an arbitrary relaxation.
# This is a metric-INTERPRETATION change, not a corpus rewrite -- applies to
# already-existing measurements corpus-wide (legacy records included), unlike
# PDR-011's register/voice change, which applies to new generation only.
DEFAULT_THRESHOLD = 0.90

# Keyed by sha256(input)[:16] rather than line number: line numbers shift the
# moment a record is inserted, removed, or reordered, and an allowlist that
# silently starts exempting the wrong record is worse than no allowlist.
#
# Each entry is (rationale, ceiling) -- external review (Claude API/Fable
# 5.1, 2026-09-07, finding M4): the allowlist used to be a bare rationale
# string with no ceiling, so an allowlisted record was exempt at ANY ratio
# forever, even if a later edit pushed it well past what was actually
# judged acceptable. ceiling = the record's measured ratio at allowlisting
# time + 0.02 headroom (a small, deliberate margin for float noise, not an
# invitation to drift). If a record's current ratio exceeds its own
# ceiling, it is treated as a genuine breach, not exempted -- see the
# ceiling check in main() below. Liveness (an allowlist key no longer
# present in the corpus at all) is checked separately, also in main().
ALLOWLIST = {
    "ac1f970c69ed67e3": (
        'dangling_reference/medium, 0.91 -- REVIEW_GUIDE.md ss6b: input is '
        'already a single well-formed sentence, so there is no structure '
        'left for the narrative to recover and the extraction work is '
        "entirely the bullets'. The narrative correctly leaves both 'he' "
        "and 'it' unresolved. Forcing this number down would mean padding.",
        0.929,
    ),
    "2e8b25e9cc7db74b": (
        'simple_list/easy, 0.87 -- REVIEW_GUIDE.md ss6b: same rationale. A '
        'high ratio is the RIGHT answer for a short, already-ordered note.',
        0.89,
    ),
    "b22ea34135ac1f82": (
        'dangling_reference/hard -- single flowing conditional sentence, '
        "already well-ordered; the ambiguous 'the blue one' and 'it' are "
        'correctly carried through unresolved.',
        0.975,
    ),
    "ff97c2128eba856d": (
        'interrupted_thought/easy -- minimal content before the literal '
        'cutoff; the preserved cutoff itself dominates the text.',
        0.925,
    ),
    "b53d08febfdbd9da": (
        'zero_action_items/easy -- three short observations already in '
        'natural order; the only available compression (tying the haze to '
        'the AQI) would invent a causal claim the input does not make.',
        0.97,
    ),
    "ffdac11711824e66": (
        'rapid_branching/hard -- already an ordered conditional chain (if X '
        'then Y, unless Z); reordering would break the logic rather than '
        'recover it.',
        0.973,
    ),
    "e8a13fec39707902": (
        'time_ambiguous/hard -- single already-ordered sentence, nothing '
        'left to reorganize.',
        0.972,
    ),
    "70e784aca3b7b102": (
        "topic_switching/medium -- naturally sequential plan ('do X then "
        "Y'); chronological order is the correct narrative order.",
        0.981,
    ),
    "4a05f1d8dba111a4": (
        'zero_action_items/medium -- single continuous observation narrated '
        'in the order it happened.',
        0.946,
    ),
    "7c0c6750c77dd1cb": (
        'time_ambiguous/hard -- already logically ordered as hedge, hedge, '
        'deadline, which is also the right narrative order.',
        0.956,
    ),
    "4f5b3aa44ba323df": (
        'time_ambiguous/hard -- natural sequential planning order (deadline '
        'hedge, call-to-check, milk on the way back).',
        0.953,
    ),
    "1e2fe17ce35e0ee3": (
        'zero_action_items/easy -- very short, single sentence.',
        0.947,
    ),
    "2141a4d2d3d72d88": (
        'dangling_reference/easy -- short, two sentences.',
        0.95,
    ),
    "d1911e8c4e740fac": (
        'zero_action_items/medium -- single continuous reminiscence; '
        "reordering someone's own train of memory would be artificial, not "
        'recovery.',
        0.988,
    ),
    "26c04e3b8daf0666": (
        'time_ambiguous/medium -- short, sequential logical hedge (problem, '
        'plumber, when to call).',
        0.929,
    ),
    "88cd4e66bf16e56b": (
        'topic_switching/medium -- very short, two sentences.',
        0.947,
    ),
    "57570b26ebded959": (
        'dangling_reference/hard -- short, two sentences, with a '
        'deliberately disconnected fragment; little to reorganize.',
        0.972,
    ),
    "df27585ea26cdbcd": (
        'dangling_reference/medium -- single sentence.',
        0.97,
    ),
    "ac98c375b6faa336": (
        'self_correction/expert -- compact list of four short facts already '
        'in a reasonable order; the retracted day has already been '
        'correctly dropped.',
        0.92,
    ),
    "dd7b5b9d1dda8d76": (
        'contradictory_statement/hard -- very short, two sentences.',
        0.929,
    ),
    "60c1d61fab759d39": (
        'contradictory_statement/easy -- short, single flowing '
        'deliberation; content confirmed correct in an earlier re-review.',
        0.95,
    ),
    "6cbdf84c5ab0ee34": (
        'long_rambling/easy -- reflective monologue in natural '
        "chronological order; matches this category's own 'easy' definition "
        'of low structural complexity.',
        0.97,
    ),
    "4fb0a1917cbdb77c": (
        'multi_person_note/easy -- short, single sentence; content '
        'confirmed correct in an earlier re-review.',
        0.999,
    ),
    "a8cfbfc88ae7c9cc": (
        'contradictory_statement/expert -- short, single flowing sentence, '
        'already well-ordered.',
        0.999,
    ),
    "137af4005bb77a89": (
        'interrupted_thought/easy -- minimal content before the literal '
        'cutoff, single clause.',
        0.89,
    ),
    "a9a8ae729ff40367": (
        'interrupted_thought/easy -- minimal content before the literal '
        'cutoff, single clause.',
        0.9,
    ),
    "42290905cb98eb65": (
        'interrupted_thought/easy -- minimal content before the literal '
        'cutoff, single clause.',
        0.999,
    ),
    "d1bad3a1d3835fa8": (
        'zero_action_items/hard -- single flowing thought ending in genuine '
        'indecision; confirmed content-correct in the twelfth re-review, '
        "and the extraction work is the bullets'.",
        0.999,
    ),
    "38aec1099460c13b": (
        'multi_person_note/easy -- very short, single sentence.',
        0.949,
    ),
    "20718ddf7c2da9e5": (
        'multi_person_note/easy -- very short, single sentence.',
        0.988,
    ),
    "c45b1c9d2282d8af": (
        'topic_switching/expert -- very short, two sentences.',
        0.956,
    ),

    # Added 2026-09-08, PDR-011's C5-backlog disposition round: reorganization
    # is now deliberately less aggressive (real-corpus target, not the old
    # synthetic-only one), so these 34 -- checked individually against their
    # own input, not swept in bulk -- are legitimate under the new standard,
    # not non-recovery. review_bridge/ aligned before this round landed.
    "afcbbfb875f45a65": (
        'zero_action_items/easy -- single sequential stream of '
        'feelings/observations, already in the order they occurred.',
        0.955,
    ),
    "e6685c7f030605ff": (
        'zero_action_items/easy -- single sequential stream of complaints '
        'about a book, already in order.',
        0.969,
    ),
    "8c60b16ac31a5106": (
        'multi_person_note/medium -- three-person packing plan already '
        'stated in natural order.',
        0.929,
    ),
    "7878731c2527bfd3": (
        'multi_person_note/medium -- three-person tax-prep plan already '
        'stated in natural order.',
        0.935,
    ),
    "dbbb488b1e66eefe": (
        'time_ambiguous/medium -- single already-ordered sentence with two '
        'time hedges, nothing left to reorganize.',
        0.946,
    ),
    "821f28ae7a69a8c7": (
        'multi_person_note/expert -- dense but already-sequential note; '
        "preserves the established \"I'll do it if Greg doesn't\" "
        'ambiguity.',
        0.935,
    ),
    "793f8231bb402beb": (
        'interrupted_thought/easy -- literal mid-word cutoff preserved '
        'verbatim.',
        0.921,
    ),
    "32aec38101ff8679": (
        'interrupted_thought/expert -- sequential asides ending in a '
        'genuine cutoff, preserved verbatim.',
        0.949,
    ),
    "8add0f383b5307e5": (
        'long_rambling/expert -- rambling monologue; original order is '
        "this category's own defining feature (8th re-review).",
        0.934,
    ),
    "b535df56318099b7": (
        'interrupted_thought/hard -- short, ends in a literal cutoff '
        'preserved verbatim.',
        0.997,
    ),
    "538ec0e62931f993": (
        'interrupted_thought/expert -- short, ends in a literal cutoff '
        'preserved verbatim.',
        0.947,
    ),
    "39beb5d152c629a6": (
        'rapid_branching/easy -- already an ordered branch-and-pivot '
        '(yarn -> scarf instead).',
        0.975,
    ),
    "a69bcd28cd841d75": (
        'multi_person_note/easy -- three-person Saturday chore list '
        'already in natural order.',
        0.969,
    ),
    "5dd23cf8479ef9e9": (
        'multi_person_note/easy -- three-person practice-prep list '
        'already in natural order.',
        0.972,
    ),
    "a92efdf32b4cfaa9": (
        'time_ambiguous/easy -- single already-ordered sentence with a '
        'time hedge.',
        0.959,
    ),
    "0f9d31fd0ceea125": (
        'simple_list/hard -- long but already-ordered closing checklist; '
        'grouped into sentences without reordering or inventing.',
        0.926,
    ),
    "019bdadc7e656508": (
        'voice_to_text_artifact/medium -- filler ("um") correctly dropped '
        'as noise; content already in order.',
        0.956,
    ),
    "f31a2e1e2bb6476d": (
        'topic_switching/medium -- two topics stated in the order they '
        'occur; chronological is correct.',
        0.927,
    ),
    "285b372c003bc901": (
        'interrupted_thought/medium -- ends in a literal cutoff preserved '
        'verbatim.',
        0.964,
    ),
    "79262254e10aaa20": (
        'interrupted_thought/easy -- ends in a literal trailing ellipsis '
        'preserved verbatim.',
        0.946,
    ),
    "055c3948e4d92904": (
        'multi_person_note/expert -- five-person cleanup-day list already '
        'in natural order.',
        0.931,
    ),
    "8c439eb8170b43ee": (
        'long_rambling/easy -- rambling reconsideration; original order is '
        "the category's own defining feature.",
        0.937,
    ),
    "c2f5884640fa0ca6": (
        'multi_person_note/easy -- two-person Thanksgiving plan already in '
        'natural order.',
        0.958,
    ),
    "975f401cb5e8d160": (
        'multi_person_note/easy -- two-person band-practice plan already '
        'in natural order.',
        0.99,
    ),
    "b7f92c182a367e91": (
        'multi_person_note/medium -- three-step sequential plan already '
        'in natural order.',
        0.943,
    ),
    "4a5a098582c94748": (
        'interrupted_thought/easy -- short, ends in a genuine real-time '
        'interruption preserved near-verbatim.',
        0.999,
    ),
    "5eea103fa19911c9": (
        'minimal_fragment/hard -- six-word fragment; nothing to '
        'reorganize by definition.',
        0.943,
    ),
    "444109e85fed5484": (
        'contradictory_statement/expert -- single flowing deliberation '
        'ending in genuine indecision, already well-ordered.',
        0.999,
    ),
    "2f650f771f1b3905": (
        'rapid_branching/easy -- already an ordered branch-and-pivot '
        '(hallway -> bedroom -> ask Leo -> brass or glass).',
        0.999,
    ),
    "d1d113218a7f3013": (
        'dangling_reference/expert -- preserves multiple unresolved '
        'referents and a genuine cutoff verbatim.',
        0.969,
    ),
    "6e851899f7c7959d": (
        'multi_person_note/expert -- already-sequential two-person dinner '
        'disagreement.',
        0.97,
    ),
    "4566d6ebcfa21848": (
        'rapid_branching/easy -- already an ordered branch-and-pivot '
        '(Paris -> Rome -> Mexico -> Cancun).',
        0.991,
    ),
    "8eb3f15068cc392f": (
        'long_rambling/expert -- rambling font deliberation with an '
        "interjected unrelated reminder; original order is the category's "
        'own defining feature.',
        0.942,
    ),
    "3c4acf287c02d4c9": (
        'voice_to_text_artifact/hard -- filler ("comma"/"period") '
        'correctly dropped as noise; content already in order.',
        0.951,
    ),
    "ddf5085c847e6b8b": (
        'long_rambling/expert -- rambling deliberation; ratio rose '
        "specifically because this session's C5 disposition round removed "
        "invented \"Initially, I thought\" framing, bringing the wording "
        "closer to input's own phrasing -- not padding.",
        0.942,
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

    non_allowlisted_breaches = [s for s in scored if s[0] > args.threshold and s[4] not in ALLOWLIST]
    # A record allowlisted at ratio R is exempt only up to its own ceiling
    # (R + 0.02), not forever at any ratio -- external review (Claude
    # API/Fable 5.1, 2026-09-07, finding M4). If a later narrative edit
    # pushed it past that, it's a fresh breach needing a fresh decision,
    # not a silent pass on the strength of the original allowlisting.
    over_ceiling = [s for s in scored if s[4] in ALLOWLIST and s[0] > ALLOWLIST[s[4]][1]]
    over_ceiling_hashes = {s[4] for s in over_ceiling}
    exempted = [s for s in scored
                if s[0] > args.threshold and s[4] in ALLOWLIST and s[4] not in over_ceiling_hashes]
    breaches = non_allowlisted_breaches + over_ceiling

    # Liveness: an allowlist key whose record was edited (hash changed) or
    # removed sits there silently doing nothing forever -- also M4. A
    # record's hash only changes if its `input` text changed, so this
    # can't false-positive on an untouched record.
    live_hashes = {s[4] for s in scored}
    orphaned = sorted(h for h in ALLOWLIST if h not in live_hashes)

    if exempted:
        print(f"\nAllowlisted (above {args.threshold} by recorded decision, within ceiling, not counted):")
        for v, lineno, c, d, h in sorted(exempted, reverse=True):
            rationale, ceiling = ALLOWLIST[h]
            print(f"  line {lineno:>4}  {v:.3f}  (ceiling {ceiling:.3f})  [{c}/{d}]")
            print(f"      {rationale}")

    if over_ceiling:
        print(f"\n{len(over_ceiling)} allowlisted record(s) now EXCEED their own ceiling -- "
              f"treated as breaches below, not exempted:")
        for v, lineno, c, d, h in sorted(over_ceiling, reverse=True):
            rationale, ceiling = ALLOWLIST[h]
            print(f"  line {lineno:>4}  {v:.3f}  (was allowlisted at ceiling {ceiling:.3f})  [{c}/{d}]  {h}")
            print(f"      original rationale: {rationale}")

    if orphaned:
        print(f"\n{len(orphaned)} allowlist key(s) not found in the current corpus -- "
              f"orphaned (the record's input text changed since allowlisting, or the "
              f"record was removed). Remove the entry or find the record's new hash:")
        for h in orphaned:
            print(f"  {h}: {ALLOWLIST[h][0][:80]}")

    if breaches:
        extra = f", plus {len(over_ceiling)} allowlisted record(s) over their own ceiling" if over_ceiling else ""
        print(f"\n{len(non_allowlisted_breaches)} non-allowlisted record(s) above "
              f"{args.threshold}{extra}:")
        for v, lineno, c, d, h in sorted(non_allowlisted_breaches, reverse=True):
            print(f"  line {lineno:>4}  {v:.3f}  [{c}/{d}]  {h}")
        print(f"\nThese are a DATA judgment, governed by "
              f"docs/datasets/REVIEW_GUIDE.md and the product owner's call -- "
              f"not a mechanical fix. Re-measure the voice checks after any "
              f"narrative edit; the two rules pull against each other.")
        return 1

    if orphaned:
        return 1

    print(f"\nNo non-allowlisted record above {args.threshold}, and no allowlisted "
          f"record over its own ceiling.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
