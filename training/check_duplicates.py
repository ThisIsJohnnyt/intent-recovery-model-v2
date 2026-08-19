#!/usr/bin/env python3
"""
Near-duplicate check for datasets/*.jsonl, per docs/datasets/TAXONOMY.md's
"No near-duplicate content" labeling rule and docs/datasets/REVIEW_GUIDE.md's
near-duplicate check step.

Flags pairs of examples whose "input" text is suspiciously similar -- same
scenario, same phrasing pattern -- so a reviewer can judge whether they're
genuine near-duplicates before a batch is accepted into the corpus. This
script surfaces candidates; it doesn't auto-reject anything -- the product
owner/reviewer decides what a flagged pair actually means.

This is a lexical check only (character-sequence ratio + word-overlap
ratio). It will NOT catch a paraphrase that reuses no wording (e.g. two
differently-worded "mom's birthday gift" notes with no shared phrasing) --
see TAXONOMY.md's near-duplicate rule if embedding-based similarity becomes
worth the added API cost later.

Usage:
    python check_duplicates.py [path/to/file.jsonl ...] [--threshold 0.55]

With no path given, defaults to datasets/synthetic.jsonl relative to the
repository root.
"""
import argparse
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path


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


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def char_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def main():
    parser = argparse.ArgumentParser(
        description="Flag near-duplicate examples across dataset JSONL files."
    )
    parser.add_argument(
        "paths", nargs="*", type=Path,
        help="JSONL file(s) to check (default: datasets/synthetic.jsonl)",
    )
    parser.add_argument(
        "--threshold", type=float, default=0.55,
        help="Flag pairs at or above this similarity, 0-1 (default 0.55)",
    )
    args = parser.parse_args()

    paths = args.paths or [Path(__file__).resolve().parent.parent / "datasets" / "synthetic.jsonl"]

    records = []
    for path in paths:
        if not path.exists():
            print(f"error: {path} does not exist", file=sys.stderr)
            sys.exit(1)
        records.extend(load_records(path))

    n = len(records)
    print(f"Loaded {n} records from {len(paths)} file(s).\n")

    flagged = []
    for i in range(n):
        text_i = records[i].get("input", "")
        words_i = word_set(text_i)
        for j in range(i + 1, n):
            text_j = records[j].get("input", "")
            words_j = word_set(text_j)
            ratio = char_ratio(text_i, text_j)
            jac = jaccard(words_i, words_j)
            score = max(ratio, jac)
            if score >= args.threshold:
                flagged.append((score, ratio, jac, i, j))

    flagged.sort(reverse=True)

    if not flagged:
        print(f"No pairs at or above similarity {args.threshold:.2f}. Nothing flagged.")
        return

    print(f"{len(flagged)} pair(s) at or above similarity {args.threshold:.2f}:\n")
    for score, ratio, jac, i, j in flagged:
        a, b = records[i], records[j]
        print(
            f"[{score:.2f}] (char={ratio:.2f} word={jac:.2f}) "
            f"{a['_source']} ({a.get('category', '?')}) <-> "
            f"{b['_source']} ({b.get('category', '?')})"
        )
        print(f"  A: {a.get('input', '')[:120]}")
        print(f"  B: {b.get('input', '')[:120]}")
        print()


if __name__ == "__main__":
    main()
