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
| 2026-08-19 | `gemini-3.1-pro-preview` (`pro` alias) | Second batch, targeted at batch 1's 3 gaps (`interrupted_thought`, `contradictory_statement`, `voice_to_text_artifact` — 2 each, with explicit guidance to avoid batch 1's specific failure modes) plus 5 previously-uncovered cognitive/emotional states (executive dysfunction, anxiety, sensory overwhelm, burnout, emotional journaling) | 15 | 14 (1 rejected — a `voice_to_text_artifact` example with one unexplainable fragment, same failure mode as batch 1's #13) | *Not retrieved — same known gap as above.* | Authorized directly ("Let's go ahead and run another batch... several examples generated before moving on"). All 3 targeted gap categories improved; `voice_to_text_artifact` still only 1-for-2 on the "No Magic Examples" bar. |
| 2026-08-19 | `gemini-3.1-pro-preview` (`pro` alias) | Third batch, part of a 2-batch authorization ("Let's run 2 more batches") — 2× `voice_to_text_artifact` (still thin), 1 each of 13 other categories, fresher subjects (home improvement, travel, fitness, hobbies, moving, pets-beyond-food, fundraising), roughly even difficulty spread | 15 | 14 (1 rejected outright — polished encyclopedia-style prose, violated "NOT polished writing"; 1 fixed in place — an invented "2x4" lumber dimension not in the input; 3 relabeled — mislabeled `interrupted_thought`/`dangling_reference`/`contradictory_statement` that were actually `topic_switching`/`self_correction`/`self_correction`) | *Not retrieved — same known gap as above.* | Recurring pattern flagged: Gemini defaults to clean-resolution `self_correction`-shaped content when asked for `contradictory_statement` or `dangling_reference` specifically — 2nd occurrence for `contradictory_statement`. Net zero new depth this batch for `interrupted_thought`/`dangling_reference`/`contradictory_statement` despite being requested. |
| 2026-08-19 | `gemini-3.1-pro-preview` (`pro` alias) | Fourth batch, 2nd of the 2-batch authorization — weighted entirely at the 7 thin categories from `CATEGORY_REFERENCE.md`'s depth tracking (`contradictory_statement` x3, `dangling_reference` x3, `simple_list`/`interrupted_thought`/`zero_action_items`/`multi_person_note` x2, `time_ambiguous` x1), with explicit contrastive definitions (what `contradictory_statement`/`dangling_reference` are NOT) replacing batch 3's plain re-statement of the category names | 15 | **15 (0 rejected, 0 relabeled — first perfect batch)** | *Not retrieved — same known gap as above.* | The contrastive-definition fix worked: all 3 `contradictory_statement` and all 3 `dangling_reference` examples correctly distinct this time. One soft, non-blocking note: 2 examples put a stated *wish* ("I want to cancel the trip") in `action_items` rather than just `bullets` — worth watching for consistency, not rejecting. |

## Known gap

This ledger's `Cost` column can't be filled in from the MCP tool's response
alone — `gemini-query` doesn't return usage/billing metadata. Until that's
resolved (either the MCP server exposes it, or costs are checked manually
in AI Studio after each call), treat this column as informational-only, not
a substitute for checking the actual AI Studio billing console
periodically.
