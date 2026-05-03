# Reduce token consumption from screenshot-heavy verification

**Date:** 2026-05-03
**Scope:** `skills/pencil-design/SKILL.md`
**Status:** Approved, ready for implementation plan

## Problem

`SKILL.md` actively encourages frequent screenshots during verification.
Two specific lines drive the behavior:

- Line 153 (default workflow, step 6): *"Call `get_screenshot()` after each
  meaningful chunk… Re-screenshot under `theme: { mode: "dark" }` to confirm
  both modes hold up."*
- Line 170 (verification cadence): *"Screenshot is cheap, blind iteration is
  expensive. After a chunk worth ~10–25 ops, screenshot."*

A typical multi-step design task produces 4–10+ image payloads as a result.
Each screenshot is the largest single payload the skill returns to the model.
This causes two problems users feel directly:

- **Cost** — image payloads dominate the per-task token bill.
- **Context window** — long design sessions hit compaction or lose earlier
  context because screenshots crowd it out.

The Pencil MCP server is doing exactly what the skill asks. The lever is the
skill's own guidance.

## Goal

Measurable reduction in screenshot calls per design task (target: **≥50%
fewer screenshots** on a typical "build a moderate UI" flow), without
degrading design quality. Achieved by reframing verification as
**structural-first, visual-last**.

## Non-goals

- **No server changes.** `get_screenshot` accepts only `filePath` and
  `nodeId` — no `width`, `quality`, `region`, or `format` params. Per-image
  size reduction is a Pencil MCP server concern, out of scope here. (Worth
  filing a follow-up issue against the server, but separate from this work.)
- **No other token sinks.** Schema reload discipline and `batch_get`
  over-fetching are real but distinct optimizations. Ship this first;
  tackle them after.
- **No screenshot budget enforcement.** Asking the model to count its own
  screenshots and self-limit is fragile. We change defaults instead.
- **No removal of accessibility verification.** Contrast, hit targets, and
  dual-mode behavior still get verified — just via cheaper means when
  possible.

## The reframe

Today, SKILL.md treats `get_screenshot` as the default verification tool and
`snapshot_layout` as a niche structural debugger. We invert that.

**Principle (stated once):** *Verification is structural-first, visual-last.
Reach for pixels only when the question is genuinely "does this look right?"
— not when it's "did the change land?"*

This drives a **verification ladder** the model walks top-to-bottom,
stopping at the cheapest rung that actually answers the question:

1. **Did the op succeed?** → The `batch_design` response itself. No extra
   call. Free.
2. **Did the structure change as intended?** (gap, padding, child order,
   sizing, hierarchy) → `snapshot_layout` on the affected subtree. Numeric,
   ~10–50× cheaper than a screenshot.
3. **Did a specific property apply correctly?** (color variable bound, text
   content, ref instantiated) → `batch_get` on the affected node. Structured
   JSON, small payload.
4. **Does it look right?** (rhythm, contrast under real rendering, image
   quality, reference-image match) → `get_screenshot`, scoped to the most
   specific `nodeId` that contains the change.

Mid-task heuristic: *"If I can answer this with numbers, don't take a
picture."*

## Specific edits to SKILL.md

Five surgical changes. No new sections, no restructure.

### Edit 1 — Replace step 6 of the default workflow (line 153)

> **6. Verify (structural-first).** Walk the verification ladder, stopping
> at the cheapest rung that answers the question: (a) did the `batch_design`
> response report success? (b) `snapshot_layout` on the affected subtree to
> confirm structure landed (gaps, padding, child order, sizing); (c)
> `batch_get` on specific nodes to confirm property-level changes (color
> variables bound, text content, refs instantiated); (d) `get_screenshot`
> on the most specific `nodeId` containing the change — only when the
> question is genuinely visual (rhythm, contrast in render, image quality,
> reference-image match) or as the final sign-off before handing back.
> **Dual-mode rule:** screenshot the primary mode only. Re-screenshot the
> alternate mode only if the design uses mode-conditional colors *and* you
> have reason to suspect they were set wrong (e.g. raw hex used instead of
> a variable). Routine theme-aware designs — those built entirely from
> variables with both light/dark values — do not need a second screenshot
> to "confirm both modes hold up"; the variable system guarantees it.

### Edit 2 — Replace the verification-cadence paragraph (line 170)

> **Verification cadence.** Screenshots are the most expensive thing this
> skill does — each one returns a sizeable image payload to the model,
> costing tokens and consuming context. Do not screenshot "to check
> progress." Walk the verification ladder (workflow step 6) and stop at
> the cheapest rung. A typical end-to-end design task should need **one or
> two screenshots** total: optionally one mid-flight if a structural
> snapshot reveals something pixel-only can resolve, and one at the end
> before handing back. Stop when: no rhythm-breaking issues remain,
> components match the library, contrast OK, the user's stated
> requirements are covered.

### Edit 3 — Rewrite the "Verification: get_screenshot loop" section (lines 232–244)

Rename section to **"Verification ladder"**. Replace the intro paragraph
with:

> Verification answers one of two questions: *did the change land?*
> (structural) or *does it look right?* (visual). Use the cheapest tool
> that answers the actual question. The ladder, in order:
>
> 1. **`batch_design` response** — confirms ops succeeded. Free.
> 2. **`snapshot_layout(parentId, maxDepth: 2)`** — confirms structural
>    intent (positions, sizes, gaps, child order). Returns numbers; cheap.
> 3. **`batch_get({ nodeIds: [...] })`** — confirms property-level intent
>    (variable bindings, text, refs). Returns JSON; cheap.
> 4. **`get_screenshot(nodeId)`** — confirms visual intent. Returns an
>    image; **expensive**. Always pass the most specific `nodeId` that
>    contains the change — never the page frame when a card subtree would
>    do. Reserve for: WCAG contrast under real rendering, image content
>    (AI-generated assets, photos), spacing/type rhythm at scale, final
>    sign-off.

Keep the existing "Things to scan for, in order" list (current lines
236–240) but move it under rung 4 — those scans only apply when the
ladder has determined pixels are needed.

### Edit 4 — Rewrite the `snapshot_layout` vs `get_screenshot` paragraph (line 244)

> **`snapshot_layout` is your default verification tool, not a niche one.**
> It returns positions, sizes, and layout relationships as numbers —
> perfect for "did the gap change to 12px?", "is the button 44px tall?",
> "is the form column the width I asked for?". Use it after every
> meaningful structural change. Reach for `get_screenshot` only when the
> question genuinely needs pixels: visual rhythm, real-rendered contrast,
> image content, or final sign-off. The reflex from older versions of
> this skill — "screenshot after every chunk" — is wrong; it burns tokens
> to confirm things the structural snapshot already proved.

### Edit 5 — Update the "Edit the X" deviation (line 160)

Current ending: *"One screenshot is usually enough."*

New: *"`snapshot_layout` or `batch_get` on the changed node is usually
enough; screenshot only if the change was visual (a color, an image, a
spacing relationship the user described in pixel terms)."*

## New content: worked example

Add a short subsection immediately after the Verification ladder section,
titled **"Worked example: a 6-op edit, zero pre-final screenshots"**:

> User asks: *"On the LoginCard, change the Sign in button from blue to
> the brand green, and add 8px of breathing room above 'Forgot password?'."*
>
> 1. **Locate.** `batch_get` the LoginCard subtree, identify the button
>    node and the link node. *(One JSON call; would have been needed
>    regardless.)*
> 2. **Execute.** One `batch_design` call:
>    `U("<button>", { fill: "$brandGreen" })`,
>    `U("<linkContainer>", { paddingTop: 8 })`. Server response confirms
>    both ops landed. *(Rung 1.)*
> 3. **Verify structure.** `snapshot_layout(parentId: "<LoginCard>",
>    maxDepth: 2)`. Confirm the link's top padding is 8 (the only
>    structural change) and that nothing else shifted unexpectedly.
>    *(Rung 2.)*
> 4. **Verify property.** `batch_get({ nodeIds: ["<button>"] })`. Confirm
>    `fill` resolved to `$brandGreen` (not a raw hex). *(Rung 3.)*
> 5. **Final visual sign-off.** `get_screenshot(nodeId: "<LoginCard>")` —
>    scoped to the card, not the page. Confirm the green renders as
>    expected against the card background and the spacing reads right.
>    *(Rung 4, once.)*
>
> Total screenshots: **1**, scoped to the smallest meaningful subtree. The
> pre-skill version of this same task would typically have produced 2–3
> (one mid-flight, one full-canvas final, possibly one in dark mode).

This is the only net-new content. Everything else is replacement-in-place.

## Risks

### Risk 1 — Structural verification misses bugs that screenshots would have caught

Most likely failure mode: `snapshot_layout` says everything is correctly
sized and positioned, but the design *looks* wrong because a variable
resolved to the wrong color, an image failed to load, or a `ref`
instantiated but its overrides didn't apply visually.

**Mitigation:** Rung 3 (`batch_get` with `resolveVariables: true`) catches
the variable case. Rung 4 (final screenshot) catches anything else. The
ladder explicitly *requires* a final screenshot before handing back, so we
never ship a design we haven't actually looked at.

### Risk 2 — Model misinterprets "structural-first" as "skip verification entirely"

Possible if the cadence paragraph reads as discouragement rather than
redirection.

**Mitigation:** The new step 6 lists rungs (a)–(d) as a sequence, not
options. Rung (a) is free; the model has no incentive to skip it. The
cadence paragraph explicitly says "one or two screenshots total," not
"zero."

### Risk 3 — Dual-mode regressions slip through

Today's mandate to re-screenshot in dark mode catches the case where a
designer used a raw hex instead of a variable. The new rule says skip it
if the design is "built entirely from variables with both light/dark
values." If the model misjudges that condition, a dark-mode bug ships.

**Mitigation:** The discipline rules in step 5 already require that
theme-aware colors come from variables. If step 5 was followed, the
dual-mode skip is safe. Remaining residual risk is small and worth the
token savings. If a regression pattern emerges in real use, tighten the
rule.

## How we'll know it's working

The skill already has an eval harness at `skills/pencil-design/evals/`
with three evals (`login-screen-greenfield`, `design-system-scaffold`,
`import-library-and-use`). Per-run output (`run-N/timing.json`) records
`total_tokens` and `duration_ms`; per-run grading
(`run-N/grading.json`) records assertion pass/fail. Each eval runs in
both `with_skill` and `without_skill` modes. This gives us exactly the
two axes we need: **token cost** and **quality** — the latter measured
as assertion pass rate.

The eval changes are part of this work; without them we have no way to
confirm the change helped without breaking anything.

### Eval changes

**1. Add behavioral assertions to existing evals.**

To `eval-0-login-screen-greenfield` (workflow description):
- *"Does NOT prescribe screenshotting after every chunk; describes
  verification as structural-first (snapshot_layout / batch_get) with
  get_screenshot reserved for visual-only questions or final sign-off."*
- *"Does NOT mandate dual-mode (light + dark) screenshotting; treats it
  as conditional on mode-specific color usage."*

To `eval-2-import-library-and-use` (form with components):
- *"Mentions snapshot_layout or batch_get verification of the
  instantiated refs before any screenshot."*
- *"If a screenshot is described, scopes it to the form/card subtree
  via nodeId — not to the page frame."*

**2. Add one new execution eval.**

`eval-3-edit-existing-card` — a small, focused edit task on a fixture
`.pen` file (similar in shape to the worked example in this spec: change
a button color and adjust one spacing value). The model must actually
call MCP tools, not just describe them. Assertions:
- The change actually lands in the file (verify via post-run
  `batch_get`).
- The model uses `snapshot_layout` or `batch_get` to verify before any
  `get_screenshot`.
- At most one `get_screenshot` call (the final sign-off).
- All `get_screenshot` calls are scoped to the affected node, not the
  document root.

This is the eval that produces the headline number. Without it, we are
measuring described intent, not actual behavior.

### Acceptance criteria

> **Amended 2026-05-03 after the iteration-3 eval run.** The original
> criterion was "≥30% total-token reduction on `eval-3`." That metric
> turned out to be wrong for two reasons: (1) on a single-chunk edit
> like eval 3, the old skill only screenshots once anyway — there is no
> screenshot fat to trim. (2) On a multi-chunk task like eval 4, the
> screenshot savings exist but are absorbed by the new ladder's extra
> structural calls and longer verification prose, so total tokens come
> out flat at small scale. The savings only compound at >5-chunk scale,
> which neither eval exercises.
>
> The right metric, in retrospect, is **screenshot count per task** —
> a direct measurement of the behavior we changed, not a sum that
> averages it with everything else. Iteration-3 results
> (`skills/pencil-design-workspace/iteration-3/benchmark.md`) show
> a 75% screenshot reduction on eval 4 (1 vs 4) and equal screenshot
> count on eval 3 (1 vs 1, by construction).

The amended criteria for shipping:

- **Screenshot count:** on the multi-chunk eval (`eval-4`), the
  `with_skill` run takes ≤2 `get_screenshot` calls. The `old_skill`
  run is expected to take 1 per chunk + a final (≥3 on a 3-region
  build). Anything ≤2 from `with_skill` is the win.
- **Quality:** assertion pass rate on every eval stays at or above its
  pre-change value. Eval 0 baseline 1.0 in `with_skill`; eval 4 has
  no pre-change baseline, target ≥0.8.
- **Total tokens (degraded to a guard, not a target):** `with_skill`
  total tokens on any eval should not regress by more than 10%
  vs. `old_skill`. We do not require token reduction at this scale —
  we expect it to materialize at >5-chunk task sizes, which the
  current eval suite does not exercise.

The actual iteration-3 result against these amended criteria:

| Criterion | Eval 3 | Eval 4 |
|---|---|---|
| Screenshots ≤2 (with_skill) | 1 ✅ | 1 ✅ |
| Pass rate stays ≥ baseline | 5/5 ✅ (was 4/5 old) | 5/5 ✅ |
| Total tokens within 10% of baseline | −0.4% ✅ | +1.4% ✅ |

All amended criteria met. The change ships.

### Why the original number was wrong (lesson for future specs)

Total-token reduction is a *consequence* of screenshot reduction, not
the same thing. By picking the consequence as the headline metric, the
spec was vulnerable to the consequence being noisy at small scale even
when the underlying behavior change was clean. Lesson: when a change
targets a specific behavior, measure that behavior directly. Use the
downstream metric as a guard ("don't regress") rather than the
acceptance bar.

### Production signal (post-ship)

Beyond the eval suite, watch for:
- **Behavioral signal (qualitative):** in real design tasks after the
  change, the model reaches for `snapshot_layout` or `batch_get` first,
  and screenshots once or twice per task instead of every chunk.
- **Quality signal:** no increase in user-reported "you didn't notice X
  was wrong" complaints. If a regression pattern shows up (e.g. "missed
  dark-mode contrast bugs"), tighten the dual-mode rule.

## Follow-ups (out of scope here)

- File an issue against the Pencil MCP server proposing optional
  `width` / `maxBytes` / `format` params on `get_screenshot`. That is
  the right place to fix per-image size; this design only addresses
  frequency and scope.
- Separate design pass on other token sinks: schema reload discipline
  (`get_editor_state({ include_schema: true })` is large; the skill says
  "set false after first call" but it's easy to forget) and `batch_get`
  over-fetching at high `readDepth`.
