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

Exit codes: 0 = nothing flagged, 1 = at least one pair flagged (so this can
gate a batch), 2 = bad invocation.
"""
import argparse
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
    if not flagged:
        print(f"{label}: nothing at or above word {word_threshold:.2f} / "
              f"char {char_threshold:.2f}.")
        return
    print(f"{label}: {len(flagged)} pair(s) flagged:")
    for jac, ch, i, j in sorted(flagged, reverse=True):
        a, b = records[i], records[j]
        trigger = "word" if jac >= word_threshold else "char"
        print(f"  [{trigger}] word={jac:.2f} char={ch:.2f}  "
              f"{a['_source']} ({a.get('category', '?')}) <-> "
              f"{b['_source']} ({b.get('category', '?')})")
        print(f"    A: {get_text(a)[:110]}")
        print(f"    B: {get_text(b)[:110]}")
    print()


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
    report("INPUT", input_hits, records, lambda r: r.get("input", ""),
           args.word_threshold, args.char_threshold)

    narrative_hits = []
    if not args.inputs_only:
        narratives = [r.get("output", {}).get("narrative", "") for r in records]
        narrative_hits = compare_field(narratives, args.min_words,
                                       args.word_threshold, args.char_threshold)
        report("NARRATIVE", narrative_hits, records,
               lambda r: r.get("output", {}).get("narrative", ""),
               args.word_threshold, args.char_threshold)

    total = len(input_hits) + len(narrative_hits)
    if total:
        print(f"{total} flagged pair(s). These are candidates for a reviewer to "
              f"judge, not automatic rejections -- see this file's docstring and "
              f"TAXONOMY.md's near-duplicate rule.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
