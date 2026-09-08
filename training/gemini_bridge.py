"""
Runs one review_bridge/ round over a direct Gemini CLI call, replacing the
standing Antigravity session as this bridge's transport. See
docs/decisions/PDR-009.md for why, and PDR-006/PDR-008 for what the bridge
itself is and isn't (a standing, cumulative engineering/pipeline-review
relationship, separate from the Gemini MCP batch-generation path and from
third_party_review.py's fresh one-shot Claude API check).

Sends review_bridge/ClaudeProposal.md to Gemini via `gemini -p ... --skip-trust
--approval-mode plan`, writes Gemini's raw, unedited reply to
review_bridge/GeminiReview.md, appends the exchange to a live-tailable
transcript log, and logs real cost to COST_LEDGER.md.

Non-negotiable guardrails, hardcoded rather than exposed as flags:
- `--approval-mode plan`: Gemini gets read-only tool access. It cannot edit
  files or run shell commands, full stop -- this is enforced by the CLI
  itself, not just by convention.
- `--skip-trust`: required for headless use (see PDR-009); scope of what
  Gemini can read is the repo root passed as `cwd`, nothing wider.
- GeminiReview.md always gets Gemini's stdout written verbatim -- no
  summarizing, editing, or filtering by this script or by Claude Code.
  (Gemini's own suggestion when it aligned on this mechanism, 2026-09-08.)

Usage (from training/):
    python gemini_bridge.py                    # default model (flash-lite)
    python gemini_bridge.py --model gemini-3.1-pro-preview   # explicit
                                                  # upgrade -- only on the
                                                  # product owner's
                                                  # in-the-moment
                                                  # authorization, same rule
                                                  # as every other real
                                                  # Gemini call.
"""
import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BRIDGE_DIR = REPO_ROOT / "review_bridge"
PROPOSAL_FILE = BRIDGE_DIR / "ClaudeProposal.md"
REVIEW_FILE = BRIDGE_DIR / "GeminiReview.md"
TRANSCRIPT = BRIDGE_DIR / "transcript.log"
COST_LEDGER = Path(__file__).resolve().parent / "COST_LEDGER.md"

DEFAULT_MODEL = "gemini-3.5-flash-lite"

# $/million tokens. Verified against live web pricing 2026-09-08 -- re-check
# before trusting this for a real budget decision if it's been a while.
PRICING_PER_MILLION = {
    "gemini-3.5-flash-lite": {"input": 0.15, "output": 1.25},
    "gemini-3.1-pro-preview": {"input": 2.00, "output": 12.00},
}

# Strengthened 2026-09-08: the original version specified output FORMAT
# only, not review DEPTH, and the observed result on this CLI transport
# (esp. the flash-lite default) was a fast, low-effort "Approve / None /
# None / ALIGNED" even on rounds carrying direct questions -- a real,
# noticed regression from the Antigravity/Pro rounds earlier this
# session, which had genuine pushback and independent technical catches.
# Reviewed and aligned on via this bridge itself before adopting.
INSTRUCTION = (
    "You are the Gemini side of a standing Claude<->Gemini review bridge "
    "for a solo ML project. Claude's proposal is provided on stdin below "
    "(the content of review_bridge/ClaudeProposal.md).\n\n"
    "Read it in full, then review it genuinely adversarially -- do not "
    "agree by default. Claude is not infallible and this bridge exists "
    "specifically to catch what Claude's own reasoning misses, not to "
    "rubber-stamp it. Before agreeing with any claim that's checkable "
    "from what you were given (a number, a specific record, a described "
    "code behavior), actually check it rather than taking Claude's word "
    "for it, and say what you checked. If the proposal asks you a direct "
    "question, answer it explicitly -- do not skip a question just "
    "because the overall proposal looks sound. If you have no genuine "
    "issue after actually checking, say so plainly rather than inventing "
    "one, but a fast, low-effort 'Approve' with no issues found and no "
    "direct questions answered is a failure of this review, not a "
    "successful one.\n\n"
    "Reply in exactly this format: a '## Verdict' line (Approve / "
    "Approve with changes / Object), a '## Issues Found' bulleted "
    "section (or 'None', with a one-line note on what you specifically "
    "checked), a '## Suggested Changes' bulleted section (or 'None'), a "
    "'## Direct Questions' section explicitly answering any question "
    "Claude asked (or 'None asked'), and a '## Alignment' section "
    "stating plainly ALIGNED or NOT ALIGNED, with what would need to "
    "change if not."
)


def log(text: str) -> None:
    """Writes to the transcript and stdout. A non-blank line gets a
    [HH:MM:SS] stamp on its own first line only -- one stamp per event
    (e.g. the whole multi-line Gemini reply is one event), not one per
    physical line, so a wrapped paragraph doesn't get re-stamped line by
    line."""
    lines = text.split("\n", 1)
    if lines[0]:
        lines[0] = f"[{datetime.now().strftime('%H:%M:%S')}] {lines[0]}"
    stamped = "\n".join(lines)
    with TRANSCRIPT.open("a", encoding="utf-8") as f:
        f.write(stamped + "\n")
    print(stamped)


def append_cost_ledger_row(model: str, input_tok: int, output_tok: int,
                            cost: float, purpose: str) -> None:
    """Best-effort: appends one row to COST_LEDGER.md's Gemini CLI (review
    bridge) table, right after that table's last existing row (found by
    scanning for '|'-prefixed lines within the section, not by assuming a
    fixed byte offset -- the section also holds a descriptive paragraph
    with its own blank lines before the table starts). Never blocks the
    actual review round on a formatting failure -- prints a warning and
    moves on rather than raising."""
    row = (f"| {date.today().isoformat()} | `{model}` | {purpose} | "
           f"{input_tok:,} | {output_tok:,} | ${cost:.4f} | |")
    marker = "## Gemini CLI (review bridge)"
    try:
        text = COST_LEDGER.read_text(encoding="utf-8")
        if marker not in text:
            print(f"warning: {marker!r} section not found in COST_LEDGER.md "
                  f"-- add the row manually:\n{row}", file=sys.stderr)
            return
        start = text.index(marker)
        next_heading = text.find("\n## ", start + len(marker))
        section_end = next_heading if next_heading != -1 else len(text)
        lines = text[start:section_end].split("\n")
        last_table_idx = next(
            (i for i in range(len(lines) - 1, -1, -1)
             if lines[i].strip().startswith("|")),
            None,
        )
        if last_table_idx is None:
            print(f"warning: no table found under {marker!r} in "
                  f"COST_LEDGER.md -- add the row manually:\n{row}", file=sys.stderr)
            return
        lines.insert(last_table_idx + 1, row)
        text = text[:start] + "\n".join(lines) + text[section_end:]
        COST_LEDGER.write_text(text, encoding="utf-8")
    except OSError as e:
        print(f"warning: could not update COST_LEDGER.md automatically "
              f"({e}) -- add this row manually:\n{row}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default=DEFAULT_MODEL,
                         help=f"Gemini model (default: {DEFAULT_MODEL}). "
                              f"Upgrade only on explicit, in-the-moment "
                              f"product-owner authorization.")
    parser.add_argument("--purpose", default="review_bridge round",
                         help="One-line description for the cost-ledger row.")
    args = parser.parse_args()

    if not PROPOSAL_FILE.exists():
        parser.error(f"{PROPOSAL_FILE} does not exist -- write the proposal "
                      f"first.")

    TRANSCRIPT.touch(exist_ok=True)
    proposal_text = PROPOSAL_FILE.read_text(encoding="utf-8")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    log(f"=== review_bridge round -- {ts} ===")
    log("")
    log(f"[SENDING] ClaudeProposal.md ({len(proposal_text)} chars, via stdin) "
        f"to Gemini ({args.model})...")

    # INSTRUCTION (which now contains literal newlines, added 2026-09-08
    # when it was strengthened for review depth) must go on stdin WITH the
    # proposal, not in argv via -p -- discovered live, same failure mode
    # PDR-009 already diagnosed for large proposal content: cmd.exe's argv
    # parsing silently drops --skip-trust on a multi-line argument, not
    # just a long one. -p stays a short, single-line, static marker; stdin
    # carries everything with real structure.
    try:
        result = subprocess.run(
            [
                "cmd", "/c", "gemini.cmd",
                "-p", "Review the proposal below.",
                "--skip-trust",
                "--approval-mode", "plan",
                "--output-format", "json",
                "-m", args.model,
            ],
            cwd=str(REPO_ROOT),
            input=INSTRUCTION + "\n\n---\n\n" + proposal_text,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        log("[ERROR] Gemini CLI call timed out after 180s.")
        return 1

    if result.returncode != 0:
        log(f"[ERROR] gemini exited {result.returncode}")
        if result.stderr.strip():
            log(f"[STDERR]\n{result.stderr.strip()}")
        return 1

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        log("[ERROR] Could not parse gemini's JSON output.")
        log(result.stdout[:2000])
        return 1

    reply = payload.get("response", "").strip()

    # Verbatim, no post-processing -- Gemini's own explicit condition for
    # aligning on this mechanism, 2026-09-08.
    REVIEW_FILE.write_text(
        f"# Gemini Review — via Gemini CLI ({args.model}), {ts}\n\n{reply}\n",
        encoding="utf-8",
    )

    log("")
    log(f"[GEMINI REPLY]\n{reply}")

    models = payload.get("stats", {}).get("models", {})
    for model_name, model_stats in models.items():
        tok = model_stats.get("tokens", {})
        input_tok = tok.get("input", 0)
        output_tok = tok.get("candidates", 0) + tok.get("thoughts", 0)
        price = PRICING_PER_MILLION.get(model_name)
        cost = None
        cost_str = ""
        if price:
            cost = (input_tok * price["input"] + output_tok * price["output"]) / 1_000_000
            cost_str = f" | est. cost: ${cost:.4f}"
        log(f"[USAGE] model={model_name} input_tokens={input_tok} "
            f"output_tokens={output_tok}{cost_str}")
        if cost is not None:
            append_cost_ledger_row(model_name, input_tok, output_tok, cost,
                                    args.purpose)

    log("")
    log(f"[WRITTEN] {REVIEW_FILE.relative_to(REPO_ROOT)}")
    log("=== Round complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
