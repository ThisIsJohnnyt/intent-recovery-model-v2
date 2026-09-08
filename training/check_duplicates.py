#!/usr/bin/env python3
"""
Near-duplicate check for datasets/*.jsonl, per docs/datasets/TAXONOMY.md's
"No near-duplicate content" labeling rule and docs/datasets/REVIEW_GUIDE.md's
near-duplicate check step.

Flags pairs of examples that are suspiciously similar -- same scenario, same
phrasing pattern -- so a reviewer can judge whether they are genuine
near-duplicates before a batch is accepted. This script surfaces candidates;
it does not auto-reject anything.

SCORING (rewritten 2026-09-02 after external review finding M6)
---------------------------------------------------------------
The primary signal is jaccard overlap of CONTENT words (function words
removed -- see STOPWORDS below). char_ratio is kept only as a secondary
trigger at a high value, because on short strings it largely measures
length agreement rather than meaning.

The previous version scored max(char_ratio, jaccard) against a single 0.55
threshold, which let whichever metric was noisier decide. Measured on the
525-record corpus that produced 3 flagged pairs, all noise (word overlap
0.13-0.21 -- the correct signal was present, and max() discarded it), while
MISSING every genuine scenario repetition in the corpus. It was crying wolf
and going silent at the same time.

The review suggested min() instead. Not adopted: it would have missed the
real near-duplicate caught by hand during batch 26 ("need to buy flour
sugar and check if the--" against a batch-24 record, char 0.70 / word
0.38), which scores 0.38 under min(). Separate signals, separate scales.

What the current settings surface on the corpus at f036664 -- none of which
the old scoring could see:
  - three prescription-pickup notes (lines 22, 122, 291)
  - three dry-cleaning notes (lines 146, 236, 481)
  - an exhausted/background-noise pair (lines 420, 494)
  - two take-out-the-trash notes (lines 5, 268)
TAXONOMY.md tolerates two examples per scenario and calls a third a signal
that generation is falling into a well; two of these are at three.

MIN_WORDS counts content words, and exists because very short notes are
structurally alike by design -- minimal_fragment is an entire category
("the green one", "ask him about it"). Comparing those is meaningless.

Both `input` and `output.narrative` are compared. The narrative pass exists
because two records can share a scenario while wording their inputs
differently -- exactly the scenario-repetition finding recorded in commit
abee8d2, which had to be found by hand because this script only read
`input`. Stopword filtering is what makes that pass usable: an earlier
draft of this rewrite reused the input-tuned threshold on raw word sets and
flagged 45 narrative pairs, essentially all noise, because every narrative
in this corpus opens "I need to ...". That was the same mistake M6
describes in the original max() scoring -- applying a threshold to a
distribution it was never measured against.

This remains a lexical check. It will NOT catch a paraphrase that reuses no
wording at all; see TAXONOMY.md if embedding-based similarity ever becomes
worth the API cost.

Usage:
    python check_duplicates.py [path/to/file.jsonl ...]
    python check_duplicates.py --word-threshold 0.20 --min-words 4

Exit codes: 0 = nothing flagged, or every flagged pair is allowlisted
(ALLOWLIST below -- added 2026-09-08, external review Claude API/Fable
5.1 finding M2); 1 = at least one non-allowlisted pair flagged (so this
can gate a batch); 2 = bad invocation.
"""
import argparse
import hashlib
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path

DEFAULT_WORD_THRESHOLD = 0.25
DEFAULT_CHAR_THRESHOLD = 0.75
DEFAULT_MIN_WORDS = 5


def load_records(path: Path):
    records = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"{path}:{lineno}: skipping invalid JSON ({e})", file=sys.stderr)
                continue
            rec["_source"] = f"{path.name}:{lineno}"
            records.append(rec)
    return records


def word_set(text: str) -> set:
    return set(text.lower().split())


# Function words carry no scenario information but dominate word-overlap on
# short texts: every narrative in this corpus starts "I need to ...", so raw
# word-set jaccard over narratives scores ~0.31 for any two unrelated records.
# Measured directly -- an earlier draft of this rewrite flagged 45 narrative
# pairs, essentially all noise, by reusing the input-tuned threshold on a
# distribution it had not been measured against (the same mistake finding M6
# describes in the original max() scoring). Filtering these first turns the
# narrative pass from noise into the check that finds scenario repetition.
STOPWORDS = frozenset("""
a an the this that these those there here
i me my mine myself we us our ours you your yours he him his she her hers it its they them their theirs
is am are was were be been being do does did doing have has had having
will would shall should can could may might must need needs needed
to of in on at for with about from by as into over after before
and or but so if then than because just also not no nor too very
what when where which who whom how why
""".split())


def content_words(text: str) -> set:
    """Word set with punctuation stripped and function words removed."""
    words = (w.strip(".,!?;:\"'()[]") for w in text.lower().split())
    return {w for w in words if w and w not in STOPWORDS}


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def char_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def similar(a: str, b: str, word_threshold: float = DEFAULT_WORD_THRESHOLD,
            char_threshold: float = DEFAULT_CHAR_THRESHOLD) -> tuple:
    """Single-pair version of compare_field's own scoring (content-word
    jaccard OR character ratio) -- the one shared definition of "too
    similar" this project uses, for callers outside the all-pairs sweep
    below (convert_real_notes.py's contamination gate). Returns (jaccard,
    char_ratio, flagged). External review (Claude API/Fable 5.1,
    2026-09-07, finding M1): convert_real_notes.py used to reimplement its
    own scoring (max(char_ratio, word_set-jaccard) against a single stale
    0.55 threshold) that had drifted from this script's actual current
    scoring -- one function now, not two that can drift apart again."""
    jac = jaccard(content_words(a), content_words(b))
    ch = char_ratio(a, b)
    return jac, ch, (jac >= word_threshold or ch >= char_threshold)


def input_hash(record: dict) -> str:
    return hashlib.sha256(record.get("input", "").encode("utf-8")).hexdigest()[:16]


# Keyed by frozenset({hash_a, hash_b}) -- order-independent, and stable
# across an INPUT-pass vs NARRATIVE-pass flag on the same record pair (one
# entry covers both, since both hashes are always the two records' INPUT
# hashes regardless of which field actually tripped the flag). Same
# pattern as check_copy_ratio.py's own hash-keyed ALLOWLIST. External
# review (Claude API/Fable 5.1, 2026-09-07, finding M2): this checker used
# to have no exemption path at all, so the gate was permanently red the
# moment the corpus accumulated its first tolerated scenario pair,
# indistinguishable from a genuinely new duplicate. Each entry judged
# directly against its actual content, 2026-09-08 -- not assumed correct
# because past re-reviews called the aggregate "confirmed false
# positives" without a recorded per-pair reason.
ALLOWLIST = {
    frozenset({"70388b9d8837c348", "06ca08b3f847b7d8"}): (
        "zero_action_items -- both 'feeling exhausted', but from "
        "different causes (noise/can't focus vs. rain/wants to rest). "
        "Shared theme, not the same scenario."
    ),
    frozenset({"fd8e9f91ec7abee1", "3a91fba80ed1b1c6"}): (
        "repeated_reminder -- both 'take out the trash' reminders. "
        "Genuine same-scenario pair, within the documented "
        "two-per-scenario tolerance."
    ),
    frozenset({"4dad0e27c417ce79", "b39f29167d579fbf"}): (
        "repeated_reminder -- both prescription pickup/refill reminders. "
        "The deliberate pair left in place after the 2026-09-02 "
        "copy-ratio remediation pass replaced a third prescription "
        "record (#291)."
    ),
    frozenset({"8085dee23b00dbcc", "87399415c8081926"}): (
        "repeated_reminder -- one is emailing a contract, the other "
        "sending a link. Different objects; the overlap is the "
        "category's own shared reminder phrasing, not a duplicate "
        "scenario."
    ),
    frozenset({"1932286b19ad6b7e", "a92efdf32b4cfaa9"}): (
        "simple_list / time_ambiguous -- both canceling a streaming "
        "subscription before it renews. Same scenario, two instances "
        "across two different categories -- tolerance is corpus-wide, "
        "not per-category."
    ),
    frozenset({"538ec0e62931f993", "2809755fc1e0a781"}): (
        "interrupted_thought / time_ambiguous -- both renewing a "
        "passport (DS-82 form). Same scenario, two instances across two "
        "categories."
    ),
    frozenset({"75dc97a31d775f9e", "b8a48573ceb66dcb"}): (
        "topic_switching -- both mention mom's birthday gift, but each "
        "note carries substantial additional distinct content "
        "(netflix/savings vs. electric bill/blender) -- one shared "
        "thread, not near-duplicate notes."
    ),
    frozenset({"b39f29167d579fbf", "07d36e9735f265e9"}): (
        "repeated_reminder -- the prescription record (see above) again, "
        "here flagged against 'Call Dr. Lin' -- different referent "
        "(pharmacy vs. a named doctor), same category reminder-phrasing "
        "coincidence."
    ),
    frozenset({"39ed8ce95f868c4d", "b11a44f16814cf59"}): (
        "minimal_fragment / simple_list -- coincidental overlap on the "
        "word 'blue' plus short-fragment structural similarity. A "
        "dangling-referent fragment vs. a numbered supply list -- not "
        "the same scenario."
    ),
    frozenset({"431466940fdf95b6", "ff97c2128eba856d"}): (
        "simple_list / interrupted_thought -- both mention milk and "
        "bread, a generic grocery pairing. Different shape and purpose "
        "(dry cleaning + dangling reference vs. a literal cutoff "
        "checking a brand) despite the shared items."
    ),
}


def compare_field(texts, min_words, word_threshold, char_threshold):
    """All-pairs comparison over one field. Returns [(jac, ch, i, j), ...].

    Two cheap gates run before the expensive full ratio, because this is
    quadratic: at 525 records that is 137,550 pairs, and a full
    SequenceMatcher on every one measured ~70s (roughly 4.5 min at 1000
    records, 18 min at 2000). The gates are (a) the word-set jaccard, which
    is pure set arithmetic, and (b) difflib's own real_quick_ratio() upper
    bound. The full ratio runs only for pairs that could still qualify.

    set_seq2 is set once per outer iteration so difflib builds its
    b-sequence index once per row instead of once per pair.
    """
    n = len(texts)
    wsets = [content_words(t) for t in texts]
    flagged = []
    sm = SequenceMatcher()  # autojunk default, as before
    for i in range(n):
        if len(wsets[i]) < min_words:
            continue
        sm.set_seq2(texts[i])
        for j in range(i + 1, n):
            if len(wsets[j]) < min_words:
                continue
            jac = jaccard(wsets[i], wsets[j])
            if jac >= word_threshold:
                sm.set_seq1(texts[j])
                flagged.append((jac, sm.ratio(), i, j))
                continue
            # only the char trigger could still fire; bound it cheaply first
            sm.set_seq1(texts[j])
            if sm.real_quick_ratio() < char_threshold:
                continue
            ch = sm.ratio()
            if ch >= char_threshold:
                flagged.append((jac, ch, i, j))
    return flagged


def report(label, flagged, records, get_text, word_threshold, char_threshold):
    """Prints every flagged pair (allowlisted ones tagged, not hidden) and
    returns the count that ISN'T allowlisted -- that count is what gates
    the exit code in main(), not len(flagged)."""
    if not flagged:
        print(f"{label}: nothing at or above word {word_threshold:.2f} / "
              f"char {char_threshold:.2f}.")
        return 0
    real = 0
    print(f"{label}: {len(flagged)} pair(s) flagged:")
    for jac, ch, i, j in sorted(flagged, reverse=True):
        a, b = records[i], records[j]
        key = frozenset({input_hash(a), input_hash(b)})
        allowlisted = key in ALLOWLIST
        if not allowlisted:
            real += 1
        trigger = "word" if jac >= word_threshold else "char"
        tag = "  [ALLOWLISTED]" if allowlisted else ""
        print(f"  [{trigger}] word={jac:.2f} char={ch:.2f}  "
              f"{a['_source']} ({a.get('category', '?')}) <-> "
              f"{b['_source']} ({b.get('category', '?')}){tag}")
        print(f"    A: {get_text(a)[:110]}")
        print(f"    B: {get_text(b)[:110]}")
        if allowlisted:
            print(f"    rationale: {ALLOWLIST[key]}")
    print()
    return real


def main():
    parser = argparse.ArgumentParser(
        description="Flag near-duplicate examples across dataset JSONL files."
    )
    parser.add_argument("paths", nargs="*", type=Path,
                        help="JSONL file(s) to check (default: datasets/synthetic.jsonl)")
    parser.add_argument("--word-threshold", type=float, default=DEFAULT_WORD_THRESHOLD,
                        help=f"jaccard word-overlap trigger (default {DEFAULT_WORD_THRESHOLD})")
    parser.add_argument("--char-threshold", type=float, default=DEFAULT_CHAR_THRESHOLD,
                        help=f"character-sequence trigger (default {DEFAULT_CHAR_THRESHOLD})")
    parser.add_argument("--min-words", type=int, default=DEFAULT_MIN_WORDS,
                        help=f"skip texts with fewer content words than this "
                             f"(default {DEFAULT_MIN_WORDS}); "
                             f"very short notes are structurally alike by design")
    parser.add_argument("--inputs-only", action="store_true",
                        help="skip the output.narrative pass")
    args = parser.parse_args()

    paths = args.paths or [Path(__file__).resolve().parent.parent / "datasets" / "synthetic.jsonl"]

    records = []
    for path in paths:
        if not path.exists():
            print(f"error: {path} does not exist", file=sys.stderr)
            return 2
        records.extend(load_records(path))

    print(f"Loaded {len(records)} records from {len(paths)} file(s).")
    print(f"Thresholds: word >= {args.word_threshold}, char >= {args.char_threshold}, "
          f"min words {args.min_words}.")
    print()

    inputs = [r.get("input", "") for r in records]
    input_hits = compare_field(inputs, args.min_words, args.word_threshold,
                               args.char_threshold)
    real_input = report("INPUT", input_hits, records, lambda r: r.get("input", ""),
                         args.word_threshold, args.char_threshold)

    narrative_hits = []
    real_narrative = 0
    if not args.inputs_only:
        narratives = [r.get("output", {}).get("narrative", "") for r in records]
        narrative_hits = compare_field(narratives, args.min_words,
                                       args.word_threshold, args.char_threshold)
        real_narrative = report("NARRATIVE", narrative_hits, records,
               lambda r: r.get("output", {}).get("narrative", ""),
               args.word_threshold, args.char_threshold)

    total = real_input + real_narrative
    if total:
        print(f"{total} non-allowlisted flagged pair(s). These are candidates for a "
              f"reviewer to judge, not automatic rejections -- see this file's "
              f"docstring and TAXONOMY.md's near-duplicate rule.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
