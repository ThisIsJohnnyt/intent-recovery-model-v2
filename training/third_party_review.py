"""
Occasional, manually-invoked independent review of the training code and
the corpus via a fresh Claude API call (Claude Fable 5.1) -- a third
opinion beyond this project's standing Claude(session)+Gemini(review_bridge)
loop, with zero context of this project or any prior conversation about it.

Not a standing automated process. See docs/decisions/PDR-008.md for why
this exists and how it differs from the 2026-09-02 external training-core
review (docs/reviews/2026-09-02-training-core-review.md), which was run by
a separate Claude Code session rather than a raw API call, and from the
Claude<->Gemini review bridge (review_bridge/), which is a standing,
non-blind collaborator relationship, not a fresh one-shot review.

The API key is never read from an environment variable or typed anywhere
in this tool -- it's retrieved at runtime from Windows Credential Manager
via the `keyring` package (target "ANTHROPIC_API_KEY", username
"Fable Review"), so it never appears in shell history, conversation logs,
or this file. See docs/vision/AI_COLLABORATION.md's "Financial guardrails"
section: this follows the same rule as every Gemini call -- the product
owner's own explicit in-the-moment go-ahead, every single time, never
inferred or carried over from a prior run.

Usage (from training/):
    python third_party_review.py --dry-run   # free: real token count + cost
                                               # estimate, no billed call
    python third_party_review.py --run       # the real, billed call --
                                               # only invoke this on the
                                               # product owner's explicit,
                                               # in-the-moment authorization
    python third_party_review.py --run --effort max   # deeper (costlier) pass
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import keyring
from anthropic import Anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = REPO_ROOT / "docs" / "reviews"

MODEL = "claude-fable-5-1"
CREDENTIAL_SERVICE = "ANTHROPIC_API_KEY"
CREDENTIAL_USERNAME = "Fable Review"

# Per-MTok pricing (input, output), cached 2026-06-24 -- an estimate for
# planning purposes, not a substitute for reading the actual invoice.
PRICING = {
    "claude-fable-5-1": (10.00, 50.00),
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
}

# The bundle: everything the reviewer gets, and nothing else.
#
# Deliberately excluded, not oversights:
# - datasets/real_holdout.jsonl -- sealed, never touched for routine work
#   per DATASET_SPEC.md. Not a judgment call this script gets to make.
# - review_bridge/ -- ephemeral, gitignored, not meaningful review material.
# - docs/reviews/*.md -- prior review reports and their conclusions.
#   Excluded on purpose (co-drafted with Gemini via the bridge, 2026-09-07):
#   the whole point of paying for a from-scratch pass is genuine freshness:
#   including past findings risks anchoring the reviewer on what's already
#   been decided, either rubber-stamping settled dispositions or re-treading
#   them as if new. If a truly independent pass re-surfaces something
#   already settled, that's a legitimate (if redundant) result; the reverse
#   -- a stale reviewer that only confirms old conclusions -- defeats the
#   purpose entirely.
BUNDLE_GLOBS = [
    "training/*.py",
    "training/requirements.txt",
    "training/COST_LEDGER.md",
    "datasets/synthetic.jsonl",
    "datasets/real_validation.jsonl",
    "docs/datasets/*.md",
    "docs/decisions/*.md",
    "docs/vision/*.md",
]

# Co-drafted with Gemini on the review bridge (review_bridge/, 2026-09-07)
# before this script's first real run -- see that round's history and
# docs/decisions/PDR-008.md. Requires actionability (a Recommended Action
# per finding, since this reviewer gets exactly one shot, no follow-up
# round) and preempts a specific false-positive risk: with docs/reviews/
# excluded, the reviewer has no way to know some high input/output overlap
# in the corpus is an intentional, already-judged-correct choice for
# certain categories (already-short or already-well-ordered notes), not a
# missed defect.
SYSTEM_PROMPT = """You are doing an independent code and data-quality review of an open
training pipeline for a language model, with no other context than the
files provided. Do not assume anything you haven't been given is true.

WHAT THIS PROJECT IS: read docs/vision/PROJECT_OVERVIEW.md and
docs/vision/NORTH_STAR.md first -- they explain the mission, the
collaboration model, and where things stand. Then read
docs/vision/AI_COLLABORATION.md and docs/vision/GOLD_PHILOSOPHY.md for
the stable principles every dataset decision is checked against.

YOUR TASK, two parts:
1. CODE REVIEW of every file under training/*.py plus requirements.txt --
   prioritize systemic correctness bugs, edge cases, inconsistency between
   what a script's own docstring/comments claim and what it actually does,
   and anything that looks unsafe or fragile, over stylistic nits.
   Cross-check code behavior against docs/datasets/*.md's stated rules
   (schema, review checklist, taxonomy) -- a mismatch between documented
   behavior and actual behavior is a real finding.
2. CORPUS REVIEW of datasets/synthetic.jsonl against
   docs/datasets/TAXONOMY.md's category definitions and
   docs/datasets/REVIEW_GUIDE.md's checklist (items 0-6b) -- sample it
   yourself, don't just trust that every record is correct because it's
   in the file. Note: some records intentionally have high input/output
   overlap based on their category (an already-short or already
   well-ordered input leaves nothing to reorganize) -- evaluate whether a
   high-overlap record fulfills its structural intent rather than flagging
   overlap on its own as a defect. Also check datasets/real_validation.jsonl
   (15 hand-written real notes, never generative-model-touched -- treat
   these as ground truth, not as data to critique) against the corpus:
   does the synthetic corpus actually resemble what real notes look like,
   or does it systematically diverge in some way the review process so
   far hasn't caught?

Also flag anything in training/COST_LEDGER.md or the docs/decisions/*.md
PDRs that looks internally inconsistent, or where documented process and
actual code disagree.

OUTPUT FORMAT -- match this exactly, it needs to slot into this project's
existing docs/reviews/ convention:

# External code review -- training core (Claude API / Fable 5.1)
**Reviewed:** <what you were given, described briefly>
**Scope:** <restate what you actually reviewed>
**Reviewer:** Claude Fable 5.1, fresh API call, zero prior context on
this project.
**Verification level:** every finding below labeled [VERIFIED] (you
directly confirmed it against the provided files), [ESTIMATED]
(arithmetic/inference from what's given, state the assumption), or
[UNVERIFIED] (you could not check it from what you were given -- state
what would be needed to check it).

Then findings, most consequential first. Be specific -- cite exact
file:line or record content, not general impressions. For each finding,
you MUST provide a concrete Recommended Action or remediation step. If
you find nothing wrong in some area, say so plainly rather than
manufacturing a finding."""


def gather_bundle() -> str:
    """Concatenate every file in BUNDLE_GLOBS, each under a clear header,
    in deterministic order. Raises if a glob matches nothing -- a silently
    empty section (e.g. a renamed directory) should fail loud, not ship a
    quietly incomplete review."""
    parts = []
    for pattern in BUNDLE_GLOBS:
        matches = sorted(REPO_ROOT.glob(pattern))
        if not matches:
            raise SystemExit(f"Bundle glob matched nothing: {pattern!r} -- "
                              f"fix BUNDLE_GLOBS before running, don't ship "
                              f"a review missing an entire section.")
        for path in matches:
            rel = path.relative_to(REPO_ROOT)
            text = path.read_text(encoding="utf-8")
            parts.append(f"=== {rel.as_posix()} ===\n{text}")
    return "\n\n".join(parts)


def get_client() -> Anthropic:
    key = keyring.get_password(CREDENTIAL_SERVICE, CREDENTIAL_USERNAME)
    if not key:
        raise SystemExit(
            f"No credential found in Windows Credential Manager for "
            f"service={CREDENTIAL_SERVICE!r} username={CREDENTIAL_USERNAME!r}. "
            f"This script never accepts the key any other way -- fix the "
            f"Credential Manager entry rather than exporting an env var."
        )
    return Anthropic(api_key=key)


def print_cost_table(input_tokens: int) -> None:
    print(f"\nReal input token count (via count_tokens, free): {input_tokens:,}")
    print(f"\nEstimated cost by model and assumed output size "
          f"(thinking + report; actual cost depends on what's actually "
          f"generated, this is planning-only):")
    print(f"{'Model':<20}{'10K out':>12}{'30K out':>12}{'60K out':>12}")
    for model, (in_price, out_price) in PRICING.items():
        row = f"{model:<20}"
        for out_tokens in (10_000, 30_000, 60_000):
            cost = (input_tokens / 1_000_000 * in_price
                    + out_tokens / 1_000_000 * out_price)
            row += f"{'$' + format(cost, '.2f'):>12}"
        print(row)
    print("\nPricing cached 2026-06-24 -- re-verify before trusting this for "
          "a real budget decision.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                         help="Free: count real tokens and print a cost "
                              "estimate table. No billed call.")
    parser.add_argument("--run", action="store_true",
                         help="The real, billed call. Only pass this on "
                              "the product owner's explicit, in-the-moment "
                              "authorization -- see AI_COLLABORATION.md's "
                              "Financial guardrails section.")
    parser.add_argument("--effort", default="high",
                         choices=["low", "medium", "high", "xhigh", "max"],
                         help="Thinking depth for the real call (default: "
                              "high). Higher costs more; see --dry-run's "
                              "cost table before raising it.")
    parser.add_argument("--max-tokens", type=int, default=48000,
                         help="Output token ceiling for the real call "
                              "(default 48000). A cap, not a target -- "
                              "billing is by tokens actually generated.")
    args = parser.parse_args()

    if not args.dry_run and not args.run:
        parser.error("pass exactly one of --dry-run or --run")
    if args.dry_run and args.run:
        parser.error("pass exactly one of --dry-run or --run, not both")

    print("Assembling bundle...")
    bundle = gather_bundle()
    print(f"Bundle assembled: {len(bundle):,} characters from "
          f"{sum(1 for _ in REPO_ROOT.glob('*'))} top-level entries scanned.")

    client = get_client()

    user_content = bundle + "\n\nPerform the review now, per the instructions above."

    print("Counting tokens (free)...")
    count = client.messages.count_tokens(
        model=MODEL,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    print_cost_table(count.input_tokens)

    if args.dry_run:
        print("\n--dry-run only: no billed call made.")
        return 0

    print(f"\nMaking the real, billed call to {MODEL} at effort={args.effort}...")
    print("(This can take several minutes on a large bundle at high effort.)")
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=args.max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
        output_config={"effort": args.effort},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason == "refusal":
        print("error: the request was refused (and any fallback also "
              "refused). No review produced.", file=sys.stderr)
        if response.stop_details:
            print(f"  category: {response.stop_details.category}", file=sys.stderr)
            print(f"  explanation: {response.stop_details.explanation}", file=sys.stderr)
        return 2

    served_by = response.model
    fell_back = served_by != MODEL
    text_parts = [b.text for b in response.content if b.type == "text"]
    review_text = "\n".join(text_parts)

    if fell_back:
        review_text = (
            f"**Note: {MODEL} declined this request; served instead by "
            f"{served_by} via the automatic fallback.**\n\n" + review_text
        )

    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REVIEWS_DIR / f"{date.today().isoformat()}-claude-api-review.md"
    out_path.write_text(review_text, encoding="utf-8", newline="\n")

    in_price, out_price = PRICING.get(served_by, PRICING[MODEL])
    actual_cost = (response.usage.input_tokens / 1_000_000 * in_price
                   + response.usage.output_tokens / 1_000_000 * out_price)

    print(f"\nWrote review to {out_path.relative_to(REPO_ROOT)}")
    print(f"Served by: {served_by}" + (" (fallback)" if fell_back else ""))
    print(f"Actual usage: {response.usage.input_tokens:,} input / "
          f"{response.usage.output_tokens:,} output tokens")
    print(f"Actual cost (at cached pricing): ${actual_cost:.2f}")
    print(f"\nNext: record this run in training/COST_LEDGER.md's "
          f"'Claude API (third-party review)' section with these exact "
          f"numbers, then read the review and disposition its findings the "
          f"same way the 2026-09-02 external review's were.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
