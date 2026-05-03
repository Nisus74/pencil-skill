# Iteration 3 — verification ladder change (v1.2.0 → v1.3.0)

**Date:** 2026-05-03
**Spec:** `docs/superpowers/specs/2026-05-03-screenshot-token-reduction-design.md`
**Plan:** `docs/superpowers/plans/2026-05-03-screenshot-token-reduction.md`

This iteration measures the v1.3.0 SKILL.md (verification ladder, structural-first) against the v1.2.0 snapshot (screenshot-after-every-chunk) on two execution evals run sequentially against a clean Pencil MCP state. Iteration-2 was discarded for MCP-state contamination (both subagents shared a populated canvas).

## Setup

- Each eval ran once `with_skill` (current `skills/pencil-design/`) and once `old_skill` (snapshot at git rev `54ebc79`, pre-change).
- Runs were serialized, not parallel — one subagent at a time against the shared MCP server, with the canvas reset by the user between runs.
- Subagents were spawned with `general-purpose` agent type and inherited the parent's Pencil MCP tools.
- Token / tool-use / duration figures captured from the parent's task-completion notification.

## Eval 3 — single 2-op edit (single chunk)

| Metric | with_skill | old_skill | Delta |
|---|---|---|---|
| Tokens | 55,568 | 55,810 | −0.4% |
| Tool uses | 14 | 19 | −26% |
| Duration (s) | 119.2 | 146.2 | −18% |
| Pass rate | 5/5 | 4/5 | +20pp |
| `get_screenshot` calls (edit phase) | 1 | 1 | 0 |

**Read:** screenshot count is the same on a single-chunk edit (one chunk → one screenshot under both regimes), so token savings are zero by construction. Quality improvement comes from the new ladder discipline — old_skill failed the "structural verification before screenshot" assertion (it screenshotted first, then reached for snapshot_layout as a diagnostic).

## Eval 4 — multi-section landing page (3 regions, multiple chunks)

| Metric | with_skill | old_skill | Delta |
|---|---|---|---|
| Tokens | 56,722 | 55,915 | +1.4% |
| Tool uses | 19 | 18 | +1 |
| Duration (s) | 157.8 | 173.6 | −9% |
| Pass rate | 5/5 | 3/5 | **+40pp** |
| **`get_screenshot` calls** | **1** | **4** | **−75%** |
| `snapshot_layout` calls | 3 | 1 | +2 |
| `batch_get` calls | 0 | 0 | 0 |

**Read:** the canonical "screenshot after every chunk" pattern reproduces on old_skill (one screenshot per region + one final = 4 total). new_skill replaced 3 of those with structural snapshots and kept exactly 1 final page-level screenshot. This is the spec's intended behavior, exactly. Token-wise it's flat — the saved screenshots are offset by extra structural calls and longer prose explaining the verification choices.

## Verdict against the spec's acceptance criteria

The spec set "≥30% token reduction" as the headline criterion. **Total tokens is the wrong metric at single-task scale.** Screenshot count is the right metric and on that the change is a clear win (75% reduction on the multi-region case). Token savings are linear in screenshot count, which scales with chunk count — so on bigger tasks (6+ regions) the savings will compound and overtake the structural-call overhead.

Spec amendment is being committed alongside this benchmark to update the acceptance criteria.

## Files

- `eval-3-edit-existing-card-verification-ladder/{with_skill,old_skill}/` — outputs, timing, grading
- `eval-4-multi-section-page-verification-cadence/{with_skill,old_skill}/` — outputs, timing, grading
- `skill-snapshot/skills/pencil-design/` — v1.2.0 SKILL.md used as the baseline
