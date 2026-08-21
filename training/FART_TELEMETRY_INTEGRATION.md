# F.A.R.T. Telemetry Integration

Instructions for wiring intent-recovery-model-v2's dataset-generation workflow into F.A.R.T. (Friendly Assistant for Relaying Telemetry) — Johnny T.'s desktop telemetry HUD. Hand this document to a Claude Code session working in this repo; it's self-contained.

## What this is, in one line

At natural checkpoints in the dataset-generation workflow (a Gemini batch call starting, finishing, being reviewed), write a small JSON file describing current progress. F.A.R.T. reads it and displays it live — progress bar, accept/reject counts, API usage — no other coupling between the two projects.

## Where to write it

```
C:\Users\thisi\.claude\.fart\telemetry_data.json
```

Create the `.fart` directory if it doesn't exist. This is the only integration point — there's no API to call, no server that needs to be running. F.A.R.T.'s server reads this file fresh on every request, so it picks up changes whenever it's next open; nothing breaks if it isn't running when you write.

**Always read-modify-write, never blind-overwrite.** Read the existing file first (if present), update only the fields below, and write the whole object back. Match `last_updated` to actual write time, UTC, ISO 8601:

```python
import json, time
from pathlib import Path

TELEMETRY_PATH = Path.home() / ".claude" / ".fart" / "telemetry_data.json"

def update_telemetry(**changes):
    TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if TELEMETRY_PATH.exists():
        try:
            data = json.loads(TELEMETRY_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass  # corrupt/missing — start fresh rather than fail the run
    for section, fields in changes.items():
        data.setdefault(section, {}).update(fields)
    data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    TELEMETRY_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
```

## Schema

Three top-level sections. Everything is a plain value — no nesting beyond what's shown.

### `project` — what's happening right now

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Short label for the current activity, e.g. `"Intent Recovery — Batch Generation"` |
| `active_process` | string | Same idea, shown as the primary line — keep `name` and this in sync |
| `status` | string | `"running"` while a batch is in flight, `"idle"` between batches, `"completed"` if you want a distinct end-state |
| `current_step` / `total_steps` | integer | See "Progress bar mapping" below — this project doesn't have a natural single step counter, so map it deliberately, not by convention copied from elsewhere |
| `percentage` | float | `round(current_step / total_steps * 100, 2)` — F.A.R.T. doesn't compute this for you |
| `current_phase` | string | One short phrase describing the current sub-step, e.g. `"Reviewing batch 7 (15 requested)"` |

**Progress bar mapping — the actual decision to make:** this project runs in occasional batches with no fixed corpus-size target (per `DATASET_SPEC.md`, it's quality-over-quantity, not a count to hit). Two honest options, pick one and stay consistent:

- **Per-batch progress** (recommended): `total_steps` = the batch size requested from Gemini (e.g. 15), `current_step` = examples received/reviewed so far in that batch. Resets each batch. Between batches, set `status: "idle"`, `current_step`/`total_steps` to `0`/`0` or leave at the last batch's final values — either reads fine.
- **Session progress**: if you've told Claude "let's do 3 batches" or similar, `total_steps` = batches planned this session, `current_step` = batches completed. Only use this when there's an actual stated session goal — don't invent one.

Don't try to track "toward eventual corpus completion" — there isn't one.

### `llm_stats` — dataset quality/volume, cumulative

| Field | Type | Meaning |
|---|---|---|
| `accepted_examples` | integer | Running total across the whole corpus (i.e. current line count of `datasets/synthetic.jsonl`, or your running tally — same thing) |
| `rejected_examples` | integer | Running total of examples generated but rejected on review, across all batches (see `COST_LEDGER.md`'s existing per-batch rejection notes — sum them) |
| `total_examples` | integer | `accepted_examples + rejected_examples` |
| `acceptance_rate` | float | `round(accepted / total * 100, 2)` |
| `prompt_tokens` / `completion_tokens` / `total_tokens` | integer | **Leave at `0` for now** — see "Known gap" below |
| `estimated_cost_usd` | float | **Leave at `0` for now** — same gap |

### `api_usage.gemini` — this project's own generation calls

| Field | Type | Meaning |
|---|---|---|
| `requests_today` | integer | Count of `gemini-query` MCP calls made today — increment per batch call, reset at your own local midnight or just let it run (F.A.R.T. doesn't enforce the "today" boundary itself) |
| `tokens_today` | integer | **Leave at `0`** — see "Known gap" |
| `active_model` | string | The actual model alias used, e.g. `"gemini-3.1-pro-preview"` (match what's already going into `COST_LEDGER.md` rows) |
| `last_response_ms` | integer | Round-trip time of the last `gemini-query` call, if you have it; `0` if not worth tracking |

### `api_usage.claude` — don't write this section

F.A.R.T. fills this in on its own (it detects an active Claude Code process directly). Leave it out of your updates entirely — just update `project`, `llm_stats`, and `api_usage.gemini`.

## Known gap: no token/cost data yet

`COST_LEDGER.md` already flags this: the `gemini-query` MCP tool doesn't return token/cost metadata in its response. Until that's resolved (either the MCP server starts exposing it, or costs get checked manually against the AI Studio billing console), the token and cost fields above should just stay `0` — don't estimate or invent numbers to fill them. F.A.R.T.'s token/cost pods will just read zero until this gap closes; that's an accurate reflection of what's actually known, not a display bug.

## When to write

Tie writes to checkpoints that already exist in the workflow — don't add new bookkeeping just for this:

1. **Before a `gemini-query` batch call** — `status: "running"`, `current_phase` describing what's being requested (e.g. `"Requesting 15 examples — contrastive definitions batch"`), `current_step: 0`.
2. **As examples come back / get reviewed** — update `current_step` incrementally if reviewing one at a time, or jump straight to the final count if reviewing as a batch.
3. **When the batch is fully reviewed** (the same moment you'd add a new row to `COST_LEDGER.md`) — update `llm_stats.accepted_examples`/`rejected_examples` to the new running totals, `api_usage.gemini.requests_today` +1, `status: "idle"`, `current_phase: "Idle — last batch: N accepted, M rejected"`.

That's roughly 2–3 writes per batch, not a continuous stream — this project doesn't run a background loop, so there's no "every N seconds" cadence to hit.

## Example

A full file mid-batch:

```json
{
  "project": {
    "name": "Intent Recovery — Batch Generation",
    "active_process": "Intent Recovery — Batch Generation",
    "status": "running",
    "current_step": 9,
    "total_steps": 15,
    "percentage": 60.0,
    "current_phase": "Reviewing batch 7 — targeting contradictory_statement, dangling_reference"
  },
  "llm_stats": {
    "accepted_examples": 86,
    "rejected_examples": 12,
    "total_examples": 98,
    "acceptance_rate": 87.76,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "estimated_cost_usd": 0
  },
  "api_usage": {
    "gemini": {
      "requests_today": 3,
      "tokens_today": 0,
      "active_model": "gemini-3.1-pro-preview",
      "last_response_ms": 0
    }
  }
}
```

## Quick sanity check

After wiring this in, confirm it worked without needing F.A.R.T. running:

```python
import json
from pathlib import Path
data = json.loads((Path.home() / ".claude" / ".fart" / "telemetry_data.json").read_text())
print(data["project"]["current_phase"], data["llm_stats"]["accepted_examples"])
```

If F.A.R.T. is open, it'll pick up the change on its next poll (sub-second) — no restart needed either direction.
