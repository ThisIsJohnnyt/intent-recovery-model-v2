#!/usr/bin/env python3
"""
Zero-Trust Blind Re-Review Auditor
Stateless CLI auditor specifically for:
  - blind_rereview_rubric_{date}.txt
  - blind_rereview_sample_{date}.jsonl

Sends a single stateless google-genai generate_content() call -- no tools,
no function-calling, no chat/session object -- so the model sees exactly
and only the rubric + sample text embedded in the payload below, nothing
else on this machine, regardless of what invokes this script. That's the
same isolation property the AI Studio version relies on; it doesn't depend
on this running through a browser vs. a local CLI call, only on the model
never being handed tool access to anything.

Credential fix, 2026-09-08 (script authored outside this repo, reviewed and
adjusted before first run): the original version read a plain
GEMINI_API_KEY environment variable. That variable already exists on this
machine (gemini_bridge.py's underlying CLI tool reads it directly per
PDR-009), but this project's established convention for a separate,
occasional-use credential is Windows Credential Manager via `keyring`
(PDR-008's precedent for the Claude API key) rather than adding a second
consumer of the same persistent env var. Confirmed with the product owner:
target "Intent-Recovery-V2", username "Gemini".

Balance fix, 2026-09-08 (same day, after the first real run): the original
SYSTEM_INSTRUCTION had no counterweight against inventing findings --
"assume nothing is compliant until proven," "flag it immediately," with no
equivalent of gemini_bridge.py's own INSTRUCTION ("if you have no genuine
issue after actually checking, say so plainly rather than inventing one").
First real run: 10/10 records flagged FIX, 0 ACCEPT -- checked directly
against several of the cited "violations" and multiple were either
backwards (a hedge word like "probably" cited as *invented certainty*,
which is the opposite of what that word is), factually wrong about which
record field the claim was even about, or flagged an order/connective
already present in the input's own text. Added an explicit
verify-before-flagging directive with the same worked exceptions this
project's own REVIEW_GUIDE.md has already had to learn the hard way
(a shared-breath causal connective isn't invented causality; a carried-
through hedge isn't invented certainty), before trusting this tool's
output for a real re-review round.

Usage (from training/, using the project's own venv per SETUP.md):
    python blind_rereviewer.py --dir ../review_bridge --output ../review_bridge/blind_rereview_report_2026-09-08.md
    python blind_rereviewer.py --dir ../review_bridge --date 2026-09-08
"""
import argparse
import os
import sys
from pathlib import Path

import keyring
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """You are an uncompromising, independent Zero-Trust Blind Re-Review Auditor.
Your only mission is to rigorously evaluate the provided anonymized sample records (containing: id, category, difficulty, input, output.narrative, output.bullets, output.action_items) against the strict rules in the rubric file.

CORE OPERATING DIRECTIVES:
1. ZERO-TRUST STRICTNESS: Assume nothing is compliant until proven. Scrutinize every sentence in the narrative, every bullet point, and every action item against the rubric rules.
2. RULE FIDELITY: Every rule in the rubric is absolute. If an output violates a constraint, contradicts the input, hallucinates details, or fails stylistic/structural requirements, flag it immediately.
3. GRANULAR AUDIT: For each record, evaluate:
   - Narrative: Consistency with input, absence of hallucination, compliance with rubric.
   - Bullets: Direct relevance, absence of unsupported leaps, adherence to constraints.
   - Action Items: Actionability, feasibility, compliance with rubric prohibitions.
4. CITATION: Always cite the exact rubric rule that was breached, quoting or closely paraphrasing the specific rubric text, not just its name.

5. VERIFY BEFORE FLAGGING -- THIS IS NOT OPTIONAL: strictness means checking
   every claim against the actual record text before it counts as a finding,
   not flagging more often. Before citing a violation:
   - Re-read the exact `input` substring and the exact `output` substring
     you are about to cite, side by side, and confirm the violation is
     actually present in that text -- not a paraphrase of it, not something
     you inferred should be there.
   - If the rubric rule you are citing has an explicit exception or a
     worked example distinguishing a real violation from a similar-looking
     but acceptable case (e.g. a connective word that merely reflects an
     order the input itself already lists; a hedge word like "probably" or
     "maybe" carried through, which is compliance with "no invented
     certainty," not a violation of it; two fragments the input itself
     states together in the same breath, which is not "invented
     causality"), check which side of that line this specific record
     actually falls on before flagging.
   - A record with zero genuine violations gets **ACCEPT**, stated plainly,
     with no violation invented to justify a different verdict. Zero-trust
     strictness applies to your own claims too: an unverified or
     paraphrased "violation" is a failure of this audit, not a successful
     one, exactly as much as missing a real one is. A batch of real,
     varied records with a 100% FIX/REJECT rate and zero ACCEPT verdicts is
     a signal to re-check your own findings, not a plausible audit result
     on its own."""


def find_files_by_date(directory: Path, date: str | None = None):
    rubrics = list(directory.glob("blind_rereview_rubric_*.txt"))
    samples = list(directory.glob("blind_rereview_sample_*.jsonl"))

    if date:
        rubric_match = directory / f"blind_rereview_rubric_{date}.txt"
        sample_match = directory / f"blind_rereview_sample_{date}.jsonl"
        return rubric_match if rubric_match.exists() else None, sample_match if sample_match.exists() else None

    if rubrics and samples:
        # Sort by name descending (most recent date)
        rubrics.sort(reverse=True)
        samples.sort(reverse=True)
        return rubrics[0], samples[0]

    return None, None


def main():
    parser = argparse.ArgumentParser(
        description="Zero-Trust Blind Re-Review Auditor (2-file validator)"
    )
    parser.add_argument("--dir", default=".", help="Directory containing blind_rereview_rubric_{date}.txt and sample_{date}.jsonl")
    parser.add_argument("--rubric", help="Explicit path to blind_rereview_rubric_{date}.txt")
    parser.add_argument("--sample", help="Explicit path to blind_rereview_sample_{date}.jsonl")
    parser.add_argument("--date", help="Specific date tag to pair (e.g., 2026-09-08)")
    parser.add_argument("--model", default="gemini-3.8-flash", help="Gemini model (default: gemini-3.8-flash)")
    parser.add_argument("--temperature", type=float, default=0.1, help="Analytical determinism (default: 0.1)")
    parser.add_argument("--output", help="Optional output path for markdown report")

    args = parser.parse_args()

    api_key = keyring.get_password("Intent-Recovery-V2", "Gemini")
    if not api_key:
        print("[Error] Could not read the Gemini API key from Windows Credential "
              "Manager (target 'Intent-Recovery-V2', username 'Gemini').",
              file=sys.stderr)
        sys.exit(1)

    work_dir = Path(args.dir)
    rubric_path = Path(args.rubric) if args.rubric else None
    sample_path = Path(args.sample) if args.sample else None

    if not rubric_path or not sample_path:
        found_rubric, found_sample = find_files_by_date(work_dir, args.date)
        rubric_path = rubric_path or found_rubric
        sample_path = sample_path or found_sample

    if not rubric_path or not rubric_path.is_file():
        print(f"[Error] Could not find rubric file (blind_rereview_rubric_*.txt) in {work_dir}", file=sys.stderr)
        sys.exit(1)

    if not sample_path or not sample_path.is_file():
        print(f"[Error] Could not find sample file (blind_rereview_sample_*.jsonl) in {work_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Pairing Rubric: {rubric_path.name}")
    print(f"[*] Pairing Sample: {sample_path.name}")

    rubric_content = rubric_path.read_text(encoding="utf-8", errors="replace")
    sample_lines = sample_path.read_text(encoding="utf-8", errors="replace").strip().splitlines()

    print(f"[*] Loaded {len(sample_lines)} records from sample file.")
    print(f"[*] Executing Zero-Trust Blind Review with {args.model} (temp={args.temperature})...")

    client = genai.Client(api_key=api_key)

    payload = f"""### BLIND RE-REVIEW RUBRIC (RULES ONLY):
{rubric_content}

### ANONYMIZED SAMPLE (ONE RECORD PER LINE):
{chr(10).join(sample_lines)}

Execute a strict, uncompromising Zero-Trust audit of every record against the rubric rules.
Output structured report."""

    response = client.models.generate_content(
        model=args.model,
        contents=payload,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=args.temperature,
        )
    )

    print("\n=== AUDIT RESULTS ===\n")
    print(response.text)

    if args.output:
        Path(args.output).write_text(response.text, encoding="utf-8")
        print(f"\n[+] Saved report to {args.output}")


if __name__ == "__main__":
    main()
