#!/usr/bin/env python3
"""
Mechanical converter: the product owner's plain-text real notes -> JSONL for
datasets/real_validation.jsonl (or real_holdout.jsonl).

WHY THIS SCRIPT IS DELIBERATELY DUMB
------------------------------------
training/DATASET_SPEC.md forbids generative-model assistance anywhere in the
real-notes pipeline. The whole value of real_validation.jsonl is that no
model wrote, corrected, or nudged any of it -- it is the only evidence
available that the synthetic corpus generalizes to notes a person actually
typed. A converter that "helpfully" fixed a typo, repaired capitalization,
split a run-on bullet, or inferred a missing ACTIONS section would be
generative assistance wearing a different hat, and would quietly destroy the
one property the file exists to have.

So this script does exactly three things:

  1. Parses the entry blocks.
  2. Passes the text through unchanged, apart from stripping the uniform
     indentation and trailing whitespace the text file carries for
     readability. --verify re-checks that promise character by character.
  3. Refuses anything it cannot parse unambiguously, naming the entry so the
     product owner fixes the source. It never guesses.

It is a text-shape tool. Every judgment call belongs to the human.

CONTAMINATION GATE
------------------
Entries whose "input" matches datasets/synthetic.jsonl are REFUSED, not
skipped quietly. Real notes drafted by copying a spot-check or review file as
a template is a natural way to work, and it leaves synthetic examples sitting
in the file looking exactly like entries. If those reached
real_validation.jsonl, the validation set would be partly the very corpus it
is supposed to independently validate, and the result would look fine.
Found live on 2026-08-25: 9 of the 10 entries in the first draft of
"Real Examples for Human Input.txt" were verbatim spot-check examples.

Similarity uses check_duplicates.py's own functions and default threshold, so
there is one definition of "too similar" in this project rather than two that
can drift apart.

The gate only sees THIS repo. A note drafted, spot-checked, or talked through
in any other model session is contaminated under DATASET_SPEC.md's rule and is
invisible here -- the text can be entirely the product owner's own and still
fail the standard, because the standard is about what has touched the note.
Provenance of the real tier is his call alone; this script cannot back him up
on it. (2026-08-25: he withdrew his own first real note for exactly this,
having used it as a spot-check example in a separate conversation.)

INPUT FORMAT
------------
Free text before the first entry is ignored (title, notes to self). Entries:

    --- 1 of 10 ---            (an optional [category / difficulty] tag may
                                follow on the same line)

    INPUT:
    <the raw note, as typed>

    NARRATIVE:
    <the recovered narrative>

    BULLETS:
      - point
      - point

    ACTIONS:
      - task
      - task

ACTIONS may be absent or contain "(none)" for a note with no action items;
both produce []. BULLETS follows the same rule. Section order is not
enforced. Lines after the last section that look like review scaffolding
("1. input reads real?") are ignored, but their presence is reported --
they mean the entry was copied from a review file.

"difficulty" is never emitted, even when the tag carries one: DATASET_SPEC.md
records that the product owner will underrate his own notes. "category" is
emitted only when the tag supplies it, and is meant to be added after the
fact rather than while writing.

USAGE
-----
    # dry run -- parse, validate, report, write nothing
    python training/convert_real_notes.py "training/Real Examples for Human Input.txt"

    # write it out (refuses to clobber an existing file without --force)
    python training/convert_real_notes.py "training/Real Examples for Human Input.txt" \
        --out datasets/real_validation.jsonl --verify

Exit status is non-zero if any entry was refused, so this can gate a pipeline.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_duplicates as dup  # noqa: E402  (same-dir sibling, intentional)
import prepare_data  # noqa: E402

ENTRY_RE = re.compile(r"^---\s*(\d+)\s*(?:of\s*\d+)?\s*---(.*)$", re.M)
TAG_RE = re.compile(r"\[([^\]/\]]+?)\s*(?:/\s*([^\]]+?))?\s*\]")
SECTION_RE = re.compile(r"^\s*(INPUT|NARRATIVE|BULLETS|ACTIONS)\s*:\s*$", re.I)
BULLET_RE = re.compile(r"^\s*[-*•]\s+(.*\S)\s*$")
REVIEW_SCAFFOLD_RE = re.compile(r"^\s*\d+\.\s+(input reads real|narrative useful|worth learning)", re.I)
NONE_RE = re.compile(r"^\s*\(?\s*none\s*\)?\s*$", re.I)


class Refused(Exception):
    """An entry this script will not convert. Always names the entry."""


def dedent_block(lines):
    """Strip trailing whitespace and the uniform leading indent the text file
    carries for readability. Relative indentation inside the block survives."""
    kept = [ln.rstrip() for ln in lines]
    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    if not kept:
        return []
    indents = [len(ln) - len(ln.lstrip()) for ln in kept if ln.strip()]
    cut = min(indents) if indents else 0
    return [ln[cut:] if ln.strip() else "" for ln in kept]


def split_sections(body, entry_no):
    """Body text -> {SECTION: [lines]}. Refuses a duplicated section rather
    than silently keeping the last one."""
    sections, current = {}, None
    for line in body.split("\n"):
        if REVIEW_SCAFFOLD_RE.match(line):
            sections.setdefault("_SCAFFOLD", []).append(line.strip())
            current = None
            continue
        m = SECTION_RE.match(line)
        if m:
            name = m.group(1).upper()
            if name in sections:
                raise Refused(f"entry {entry_no}: two '{name}:' sections")
            sections[name] = []
            current = name
            continue
        if current:
            sections[current].append(line)
    return sections


def as_prose(lines, entry_no, field, collapse):
    text = dedent_block(lines)
    if not text:
        raise Refused(f"entry {entry_no}: '{field}' is empty")
    if collapse and len(text) > 1:
        # prepare_data.serialize_target() collapses newlines in narrative, so
        # a multi-line narrative would silently change shape at training time.
        # Do it here, visibly, and report it rather than letting it happen later.
        return " ".join(t for t in text if t), True
    return "\n".join(text), False


def as_list(lines, entry_no, field):
    text = dedent_block(lines)
    if not text or all(NONE_RE.match(t) for t in text if t):
        return []
    items, stray = [], []
    for line in text:
        if not line.strip():
            continue
        m = BULLET_RE.match(line)
        if m:
            items.append(m.group(1))
        elif re.match(r"^\s*[-*•]\s*$", line):
            # a dash with no content after it -- an empty list item, not
            # unparseable content. Treat like a blank line, not a stray.
            continue
        else:
            stray.append(line)
    if stray:
        raise Refused(
            f"entry {entry_no}: '{field}' has {len(stray)} line(s) not starting "
            f"with '-': {stray[0][:60]!r}"
        )
    return items


def parse(text):
    """-> (entries, refusals). Never raises on a bad entry; collects it."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    marks = list(ENTRY_RE.finditer(text))
    entries, refusals = [], []
    for idx, m in enumerate(marks):
        entry_no = m.group(1)
        tag_text = m.group(2) or ""
        body = text[m.end():marks[idx + 1].start() if idx + 1 < len(marks) else len(text)]
        body = re.sub(r"^\s*=+\s*$", "", body, flags=re.M)
        try:
            sec = split_sections(body, entry_no)
            missing = [s for s in ("INPUT", "NARRATIVE") if s not in sec]
            if missing:
                raise Refused(f"entry {entry_no}: missing {', '.join(missing)} section(s)")
            note, _ = as_prose(sec["INPUT"], entry_no, "INPUT", collapse=False)
            narrative, collapsed = as_prose(sec["NARRATIVE"], entry_no, "NARRATIVE", collapse=True)
            record = {
                "input": note,
                "output": {
                    "narrative": narrative,
                    "bullets": as_list(sec.get("BULLETS", []), entry_no, "BULLETS"),
                    "action_items": as_list(sec.get("ACTIONS", []), entry_no, "ACTIONS"),
                },
            }
            tag = TAG_RE.search(tag_text)
            if tag and tag.group(1).strip():
                # difficulty (tag.group(2)) is deliberately discarded -- see module docstring
                record["category"] = tag.group(1).strip()
            entries.append({
                "no": entry_no,
                "record": record,
                "collapsed": collapsed,
                "scaffold": bool(sec.get("_SCAFFOLD")),
                "had_difficulty": bool(tag and tag.group(2)),
            })
        except Refused as e:
            refusals.append(str(e))
    return entries, refusals


def contamination(entries, corpus_path, threshold):
    """Refuse any entry too close to an existing synthetic record."""
    if not corpus_path.exists():
        return [], f"corpus {corpus_path} not found -- contamination gate DID NOT RUN"
    corpus = dup.load_records(corpus_path)
    hits = []
    for e in entries:
        note = e["record"]["input"]
        words = dup.word_set(note)
        best = (0.0, None)
        for rec in corpus:
            other = rec.get("input", "")
            score = max(dup.char_ratio(note, other), dup.jaccard(words, dup.word_set(other)))
            if score > best[0]:
                best = (score, rec["_source"])
        if best[0] >= threshold:
            hits.append((e, best))
    return hits, None


def verify(entries, source_text):
    """Confirm the promise in the docstring: every character of every emitted
    field appears in the source. Whitespace-insensitive, nothing else."""
    def squeeze(s):
        return re.sub(r"\s+", " ", s).strip()
    haystack = squeeze(source_text)
    problems = []
    for e in entries:
        r = e["record"]
        fields = [("input", r["input"]), ("narrative", r["output"]["narrative"])]
        fields += [("bullet", b) for b in r["output"]["bullets"]]
        fields += [("action", a) for a in r["output"]["action_items"]]
        for name, value in fields:
            if squeeze(value) not in haystack:
                problems.append(f"entry {e['no']}: {name} text not found verbatim in source")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="plain-text notes file")
    ap.add_argument("--out", type=Path, help="JSONL to write (omit for a dry run)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing --out")
    ap.add_argument("--verify", action="store_true",
                    help="re-check that no emitted text differs from the source")
    ap.add_argument("--corpus", type=Path,
                    default=Path(__file__).resolve().parent.parent / "datasets" / "synthetic.jsonl",
                    help="synthetic corpus to check contamination against")
    ap.add_argument("--threshold", type=float, default=0.55,
                    help="contamination threshold, matching check_duplicates.py (default 0.55)")
    ap.add_argument("--no-corpus-check", action="store_true",
                    help="proceed even though the contamination gate could not run "
                         "(missing --corpus). Prints exactly what is being waived. "
                         "Without this flag a missing corpus is fatal.")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"error: {args.source} does not exist", file=sys.stderr)
        return 2

    raw = args.source.read_text(encoding="utf-8-sig")
    entries, refusals = parse(raw)
    print(f"Parsed {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} "
          f"from {args.source.name}.\n")

    hits, gate_warning = contamination(entries, args.corpus, args.threshold)
    if gate_warning:
        # A gate that a typo'd --corpus path silently disables is not a gate.
        # This one exists because 9 of the 10 entries in the first draft of the
        # real-notes file were verbatim spot-check examples (2026-08-25); it
        # previously printed a warning and wrote real_validation.jsonl anyway.
        # External review, 2026-09-02 (M5).
        if not args.no_corpus_check:
            print(f"error: {gate_warning}", file=sys.stderr)
            print("The contamination gate is the only automated protection the",
                  "real tier has", file=sys.stderr)
            print("against synthetic examples being converted into it.",
                  "Refusing rather than writing unchecked.", file=sys.stderr)
            print("Fix the --corpus path, or pass --no-corpus-check to waive it",
                  "deliberately.", file=sys.stderr)
            return 2
        print(f"WARNING: {gate_warning}")
        print("WAIVED via --no-corpus-check: entries are being converted WITHOUT any")
        print("check that they are absent from the synthetic corpus. Provenance of the")
        print("real tier is now entirely manual -- see DATASET_SPEC.md's note that the")
        print("tooling cannot back you up on it.")
        print()
    if hits:
        print(f"REFUSED -- {len(hits)} entr{'y' if len(hits) == 1 else 'ies'} already in "
              f"{args.corpus.name}. These are synthetic examples, not real notes;\n"
              f"converting them would contaminate the validation set with the corpus\n"
              f"it exists to validate. Replace them in the source file:\n")
        for e, (score, src) in hits:
            print(f"  entry {e['no']}: {score:.2f} similar to {src}")
            print(f"      {e['record']['input'][:76]}")
        print()
        keep = {id(e) for e, _ in hits}
        entries = [e for e in entries if id(e) not in keep]

    for r in refusals:
        print(f"REFUSED -- {r}")
    if refusals:
        print()

    noisy = [e for e in entries if e["scaffold"]]
    if noisy:
        print(f"NOTE: {len(noisy)} entr{'y' if len(noisy) == 1 else 'ies'} still carry review "
              f"scaffolding ('1. input reads real?'): {', '.join(e['no'] for e in noisy)}")
    collapsed = [e for e in entries if e["collapsed"]]
    if collapsed:
        print(f"NOTE: narrative newlines collapsed to spaces (training does this anyway) in "
              f"entr{'y' if len(collapsed) == 1 else 'ies'}: {', '.join(e['no'] for e in collapsed)}")
    dropped = [e for e in entries if e["had_difficulty"]]
    if dropped:
        print(f"NOTE: 'difficulty' discarded per DATASET_SPEC.md in "
              f"entr{'y' if len(dropped) == 1 else 'ies'}: {', '.join(e['no'] for e in dropped)}")
    if noisy or collapsed or dropped:
        print()

    if args.verify:
        problems = verify(entries, raw)
        if problems:
            print("VERIFY FAILED -- emitted text differs from the source:")
            for p in problems:
                print(f"  {p}")
            return 1
        print("VERIFY: every emitted field appears verbatim in the source.\n")

    for e in entries:
        try:
            prepare_data.validate_record(e["record"], args.source.name, int(e["no"]))
        except prepare_data.SchemaError as err:
            print(f"REFUSED -- entry {e['no']} fails schema: {err}")
            refusals.append(str(err))
            entries = [x for x in entries if x is not e]

    zero = [e["no"] for e in entries if not e["record"]["output"]["action_items"]]
    print(f"{len(entries)} entr{'y' if len(entries) == 1 else 'ies'} ready"
          + (f" ({len(zero)} with no action items: {', '.join(zero)})" if zero else ""))

    if args.out:
        if args.out.exists() and not args.force:
            print(f"\nerror: {args.out} exists -- pass --force to overwrite", file=sys.stderr)
            return 2
        if not entries:
            print("\nnothing to write", file=sys.stderr)
            return 1
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="\n") as f:
            for e in entries:
                f.write(json.dumps(e["record"], ensure_ascii=False) + "\n")
        loaded = prepare_data.load_jsonl(args.out)
        print(f"\nWrote {len(loaded)} record(s) to {args.out}; load_jsonl validates.")
    else:
        print("\n(dry run -- pass --out to write)")

    return 1 if (refusals or hits) else 0


if __name__ == "__main__":
    sys.exit(main())
