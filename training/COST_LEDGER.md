# Cost Ledger

The lightweight running cost ledger [PDR-004](../docs/decisions/PDR-004.md)
calls for — a plain log of what was spent, when, on what. Not the full
attestation ceremony the predecessor project used (see PDR-004's "Guardrail
redesign"); just enough to keep a running record. Google's platform-level
spend cap (set in AI Studio) is the hard backstop underneath this, not a
replacement for it.

Every entry below corresponds to a real, billed Gemini API call the product
owner explicitly authorized in the moment — never inferred, never carried
over from a prior approval (see `AI_COLLABORATION.md`'s "Financial
guardrails").

| Date | Model | Purpose | Requested | Accepted | Cost | Notes |
|---|---|---|---|---|---|---|
| 2026-08-19 | `gemini-3.1-pro-preview` (`pro` alias) | First test batch, v2.0 taxonomy — 15 examples, broad cognitive/emotional starter mix (calm/organized, mild distraction, hyperfocus, rapid-branching excitement, dry/neutral observation) | 15 | 13 (2 rejected on review — see `docs/datasets/CATEGORY_REFERENCE.md`) | *Not retrieved — the MCP tool call didn't return token/cost metadata. Confirm actual spend against the AI Studio billing console.* | First real, billed call under this repository. Authorized directly by the product owner ("I am ready to test this"), confirmed batch size (15) and target states via follow-up questions before the call ran. |

## Known gap

This ledger's `Cost` column can't be filled in from the MCP tool's response
alone — `gemini-query` doesn't return usage/billing metadata. Until that's
resolved (either the MCP server exposes it, or costs are checked manually
in AI Studio after each call), treat this column as informational-only, not
a substitute for checking the actual AI Studio billing console
periodically.
