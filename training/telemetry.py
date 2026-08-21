"""
F.A.R.T. telemetry integration for intent-recovery-model-v2's dataset-
generation workflow. Implements training/FART_TELEMETRY_INTEGRATION.md's
spec -- see that file for the full schema and design rationale; this
module is just that spec turned into code.

Writes a small JSON file at ~/.claude/.fart/telemetry_data.json describing
current dataset-generation progress. F.A.R.T. (a separate desktop app)
reads this file on its own poll cycle -- there's no API call and no server
dependency in this direction; if F.A.R.T. isn't running, writes here are
inert and harmless.

Three checkpoints per batch, matching what already happens in the
workflow (no new bookkeeping):
    1. batch_starting()  -- right before a gemini-query batch call
    2. batch_progress()  -- optional, while reviewing
    3. batch_finished()  -- once reviewed, same moment as a new
                             COST_LEDGER.md row

Token/cost fields stay 0 throughout -- gemini-query doesn't return that
metadata (see COST_LEDGER.md's "Known gap"). Not estimated, not invented.
"""
import json
import time
from pathlib import Path

TELEMETRY_PATH = Path.home() / ".claude" / ".fart" / "telemetry_data.json"

PROJECT_NAME = "Intent Recovery — Batch Generation"


def _read_existing() -> dict:
    if TELEMETRY_PATH.exists():
        try:
            return json.loads(TELEMETRY_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass  # corrupt/missing -- start fresh rather than fail the run
    return {}


def _deep_merge(base: dict, updates: dict) -> None:
    """Merge `updates` into `base` in place, recursing into nested dicts
    instead of replacing them wholesale. The integration doc's own
    reference implementation uses a single-level dict.update(), which
    silently wipes sibling fields one level down -- e.g. writing
    api_usage={"gemini": {"active_model": x}} would blow away
    api_usage.gemini.requests_today entirely instead of merging alongside
    it. Fixed here rather than copied as-is."""
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def update_telemetry(**changes) -> None:
    """Generic read-modify-write, matching the integration doc's reference
    helper (with the shallow-merge bug above fixed). `changes` is
    {section_name: {field: value, ...}, ...} and gets merged into
    whatever sections already exist -- never a blind overwrite of the
    whole file, and never a blind overwrite of a nested section either.
    `api_usage.claude` is silently dropped if present: F.A.R.T. fills that
    section in on its own by detecting the active Claude Code process
    directly, so this integration never writes it.
    """
    data = _read_existing()
    for section, fields in changes.items():
        if section == "api_usage":
            fields = {k: v for k, v in fields.items() if k != "claude"}
        data.setdefault(section, {})
        _deep_merge(data[section], fields)
    data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    TELEMETRY_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def batch_starting(batch_size: int, phase: str, model: str = "") -> None:
    """Call right before the gemini-query call for a new batch goes out."""
    changes = {
        "project": {
            "name": PROJECT_NAME,
            "active_process": PROJECT_NAME,
            "status": "running",
            "current_step": 0,
            "total_steps": batch_size,
            "percentage": 0.0,
            "current_phase": phase,
        },
    }
    if model:
        changes["api_usage"] = {"gemini": {"active_model": model}}
    update_telemetry(**changes)


def batch_progress(current_step: int, total_steps: int, phase: str) -> None:
    """Optional incremental update while a batch is being reviewed."""
    pct = round(current_step / total_steps * 100, 2) if total_steps else 0.0
    update_telemetry(
        project={
            "current_step": current_step,
            "total_steps": total_steps,
            "percentage": pct,
            "current_phase": phase,
        },
    )


def batch_finished(accepted_delta: int, rejected_delta: int,
                    model: str = "", response_ms: int = 0) -> None:
    """Call once a batch is fully reviewed and accepted examples have been
    appended to the corpus -- the same moment a new row goes into
    COST_LEDGER.md. Takes THIS BATCH's counts, not running totals; adds
    them to whatever's already in the telemetry file.
    """
    data = _read_existing()
    stats = data.get("llm_stats", {})
    accepted = stats.get("accepted_examples", 0) + accepted_delta
    rejected = stats.get("rejected_examples", 0) + rejected_delta
    total = accepted + rejected
    rate = round(accepted / total * 100, 2) if total else 0.0

    gemini = data.get("api_usage", {}).get("gemini", {})
    requests_today = gemini.get("requests_today", 0) + 1

    update_telemetry(
        project={
            "status": "idle",
            "current_phase": (
                f"Idle — last batch: {accepted_delta} accepted, "
                f"{rejected_delta} rejected"
            ),
        },
        llm_stats={
            "accepted_examples": accepted,
            "rejected_examples": rejected,
            "total_examples": total,
            "acceptance_rate": rate,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0,
        },
        api_usage={
            "gemini": {
                "requests_today": requests_today,
                "tokens_today": 0,
                "active_model": model or gemini.get("active_model", ""),
                "last_response_ms": response_ms,
            }
        },
    )


if __name__ == "__main__":
    # Read-only sanity check, matching FART_TELEMETRY_INTEGRATION.md's own
    # "Quick sanity check" section exactly -- confirms the file is present
    # and well-formed without writing anything. Deliberately does NOT call
    # batch_starting/batch_finished here: those mutate real cumulative
    # state (requests_today, accepted/rejected totals), so a self-test
    # that calls them on every run would corrupt the real numbers instead
    # of just checking them.
    if not TELEMETRY_PATH.exists():
        print(f"No telemetry file yet at {TELEMETRY_PATH} -- nothing written so far.")
    else:
        data = json.loads(TELEMETRY_PATH.read_text(encoding="utf-8"))
        print(f"Read {TELEMETRY_PATH}")
        print(data["project"]["current_phase"], "|", data["llm_stats"]["accepted_examples"], "accepted")
