# Screenshot Token Reduction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce token consumption from screenshot-heavy verification in the pencil-design skill by reframing verification as structural-first, visual-last — and prove the change is both cheaper and not quality-degrading via the existing eval harness.

**Architecture:** Five surgical edits to `skills/pencil-design/SKILL.md` (no new sections, no restructure), one new worked-example subsection, and three updates to `skills/pencil-design/evals/evals.json` (two assertion additions, one new execution eval). All changes are content-only — no Python, no runner code, no new tooling. The existing pre-commit hook (`tools/skill-lint.py`) validates the SKILL.md frontmatter; nothing else needs to compile.

**Tech Stack:** Markdown (SKILL.md), JSON (evals.json), git for version control, pre-commit hooks for validation. No build step. No test framework — verification is the eval harness, run externally by the user.

**Reference spec:** `docs/superpowers/specs/2026-05-03-screenshot-token-reduction-design.md` — read this before starting if you have not.

---

## File Structure

Files this plan touches:

- **Modify:** `skills/pencil-design/SKILL.md` — five surgical edits + one new subsection. This is the substance of the change.
- **Modify:** `skills/pencil-design/evals/evals.json` — add behavioral assertions to existing evals 0 and 2; add new eval 3 (execution-based).
- **Modify:** `docs/CHANGELOG.md` — log the change. (Existing project convention; check the file first to match its format.)

Files this plan does NOT touch:
- No Python under `tools/` — the lint/pre-commit setup already covers the change set.
- No `references/` — the new guidance lives inline in SKILL.md per the spec.
- No `.claude-plugin/plugin.json` or `gemini-extension.json` — manifest unchanged.
- No `assets/` — no new templates.

Each task below is self-contained: it changes one logical thing, verifies it, and commits. Run pre-commit hooks after each commit (they run automatically via `git commit`); a hook failure is a real failure, not noise — fix the underlying issue and create a new commit.

---

## Task 1: Read the spec and confirm preconditions

**Files:** Read-only.

- [ ] **Step 1: Read the spec end-to-end**

Run: open and read `docs/superpowers/specs/2026-05-03-screenshot-token-reduction-design.md`.
Expected: you understand the verification ladder (4 rungs), the five SKILL.md edits, the worked example, and the eval acceptance criteria.

- [ ] **Step 2: Verify the SKILL.md line numbers in the spec still match the current file**

Run: `grep -n "Screenshot is cheap" skills/pencil-design/SKILL.md && grep -n "Re-screenshot under" skills/pencil-design/SKILL.md && grep -n "snapshot_layout\` vs \`get_screenshot" skills/pencil-design/SKILL.md`
Expected: three line-number hits. The spec references lines 153, 170, 244 — minor drift is fine (the spec text quotes the surrounding content, which is what you match against). If the lines have changed substantially, update your mental map of which paragraph each edit targets but proceed — the *content* of the edits in the spec is authoritative, not the line numbers.

- [ ] **Step 3: Confirm the eval harness output is what the spec assumes**

Run: `cat skills/pencil-design/evals/evals.json && ls skills/pencil-design-workspace/iteration-1/eval-0-login-screen-greenfield/with_skill/run-1/`
Expected: you see three current evals (ids 0, 1, 2) and per-run `timing.json` + `grading.json`. This confirms acceptance-criteria measurement is feasible.

No commit (read-only task).

---

## Task 2: Edit 1 — Replace step 6 of the default workflow

**Files:**
- Modify: `skills/pencil-design/SKILL.md` (the paragraph beginning "6. **Verify.** Call `get_screenshot()` after each meaningful chunk")

- [ ] **Step 1: Locate the current step 6**

Run: `grep -n "^6\. \*\*Verify\.\*\*" skills/pencil-design/SKILL.md`
Expected: one line number. Note it.

- [ ] **Step 2: Apply the replacement**

Use the `Edit` tool. Replace this exact text:

```
6. **Verify.** Call `get_screenshot()` after each meaningful chunk — not after every op. Scan in this order: layout integrity → spacing rhythm → type rhythm → **contrast under WCAG AA in BOTH light and dark modes** → component fidelity → **hit-target sizes ≥ 44×44 for interactive elements** → **non-color status signals** (errors carry an icon, not just red). Re-screenshot under `theme: { mode: "dark" }` to confirm both modes hold up.
```

With this exact text:

```
6. **Verify (structural-first).** Walk the verification ladder, stopping at the cheapest rung that answers the question: (a) did the `batch_design` response report success? (b) `snapshot_layout` on the affected subtree to confirm structure landed (gaps, padding, child order, sizing); (c) `batch_get` on specific nodes to confirm property-level changes (color variables bound, text content, refs instantiated); (d) `get_screenshot` on the most specific `nodeId` containing the change — only when the question is genuinely visual (rhythm, contrast in render, image quality, reference-image match) or as the final sign-off before handing back. **Dual-mode rule:** screenshot the primary mode only. Re-screenshot the alternate mode only if the design uses mode-conditional colors *and* you have reason to suspect they were set wrong (e.g. raw hex used instead of a variable). Routine theme-aware designs — those built entirely from variables with both light/dark values — do not need a second screenshot to "confirm both modes hold up"; the variable system guarantees it.
```

- [ ] **Step 3: Verify the edit landed**

Run: `grep -n "structural-first" skills/pencil-design/SKILL.md`
Expected: at least one match (in step 6).

Run: `grep -c "Re-screenshot under \`theme" skills/pencil-design/SKILL.md`
Expected: `0` — the old dual-mode mandate is fully gone from step 6.

- [ ] **Step 4: Commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "feat(skill): rewrite verify step as structural-first ladder

Replace 'screenshot after each chunk' with a verification ladder that
stops at the cheapest rung: batch_design response → snapshot_layout →
batch_get → get_screenshot. Dual-mode screenshotting becomes conditional
rather than mandatory."
```

Pre-commit hooks will run. If `skill-lint.py` fails, read its output, fix the underlying issue, re-stage, and commit again (do NOT use `--amend`).

---

## Task 3: Edit 2 — Replace the verification-cadence paragraph

**Files:**
- Modify: `skills/pencil-design/SKILL.md` (the paragraph that begins "**Verification cadence.** Screenshot is cheap")

- [ ] **Step 1: Locate the current cadence paragraph**

Run: `grep -n "Screenshot is cheap" skills/pencil-design/SKILL.md`
Expected: one line number.

- [ ] **Step 2: Apply the replacement**

Use the `Edit` tool. Replace this exact text:

```
**Verification cadence.** Screenshot is cheap, blind iteration is expensive. After a chunk worth ~10–25 ops, screenshot. Then between substantive change sets. Stop when: no rhythm-breaking issues remain, components match the library, contrast OK, the user's stated requirements are covered. Hand back with a one-paragraph summary of what landed.
```

With this exact text:

```
**Verification cadence.** Screenshots are the most expensive thing this skill does — each one returns a sizeable image payload to the model, costing tokens and consuming context. Do not screenshot "to check progress." Walk the verification ladder (workflow step 6) and stop at the cheapest rung. A typical end-to-end design task should need **one or two screenshots** total: optionally one mid-flight if a structural snapshot reveals something pixel-only can resolve, and one at the end before handing back. Stop when: no rhythm-breaking issues remain, components match the library, contrast OK, the user's stated requirements are covered. Hand back with a one-paragraph summary of what landed.
```

- [ ] **Step 3: Verify**

Run: `grep -c "Screenshot is cheap" skills/pencil-design/SKILL.md`
Expected: `0`.

Run: `grep -c "one or two screenshots" skills/pencil-design/SKILL.md`
Expected: `1`.

- [ ] **Step 4: Commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "feat(skill): rewrite cadence paragraph to flag screenshots as costly

Replace 'Screenshot is cheap' with explicit token-cost framing and a
typical-task budget (1-2 screenshots), pointing the reader at the
verification ladder in step 6."
```

---

## Task 4: Edit 3 — Rewrite the "Verification: get_screenshot loop" section

**Files:**
- Modify: `skills/pencil-design/SKILL.md` (the section header `## Verification: get_screenshot loop` and its intro paragraph)

This edit is two parts: rename the section, and replace its intro. The five-item "Things to scan for" list (layout integrity → spacing rhythm → ...) stays in the file — but it gets re-anchored as guidance for "when you've decided to use rung 4 (screenshot)."

- [ ] **Step 1: Locate the section header and its intro**

Run: `grep -n "^## Verification" skills/pencil-design/SKILL.md`
Expected: one line — the existing `## Verification: get_screenshot loop` header.

Run: `sed -n '232,245p' skills/pencil-design/SKILL.md`
Expected: you see the header, the intro paragraph (`get_screenshot()` returns a rendered image of the current canvas...`), and the numbered list of five scan items.

- [ ] **Step 2: Rename the section header**

Use the `Edit` tool. Replace:

```
## Verification: get_screenshot loop
```

With:

```
## Verification ladder
```

- [ ] **Step 3: Replace the intro paragraph (the one that begins "`get_screenshot()` returns a rendered image")**

Use the `Edit` tool. Replace this exact text:

```
`get_screenshot()` returns a rendered image of the current canvas (or a selected node). Use it as your eyes. Things to scan for, in order:
```

With this exact text:

```
Verification answers one of two questions: *did the change land?* (structural) or *does it look right?* (visual). Use the cheapest tool that answers the actual question. The ladder, in order:

1. **`batch_design` response** — confirms ops succeeded. Free.
2. **`snapshot_layout(parentId, maxDepth: 2)`** — confirms structural intent (positions, sizes, gaps, child order). Returns numbers; cheap.
3. **`batch_get({ nodeIds: [...] })`** — confirms property-level intent (variable bindings, text, refs). Returns JSON; cheap.
4. **`get_screenshot(nodeId)`** — confirms visual intent. Returns an image; **expensive**. Always pass the most specific `nodeId` that contains the change — never the page frame when a card subtree would do. Reserve for: WCAG contrast under real rendering, image content (AI-generated assets, photos), spacing/type rhythm at scale, final sign-off.

When you've decided rung 4 is needed, scan the rendered image in this order:
```

The trailing line ("When you've decided rung 4 is needed, scan the rendered image in this order:") is what now anchors the existing five-item list — the five items themselves stay untouched.

- [ ] **Step 4: Verify**

Run: `grep -c "^## Verification ladder" skills/pencil-design/SKILL.md`
Expected: `1`.

Run: `grep -c "^## Verification: get_screenshot loop" skills/pencil-design/SKILL.md`
Expected: `0`.

Run: `grep -A1 "When you've decided rung 4" skills/pencil-design/SKILL.md`
Expected: the next line begins with `1. **Layout integrity**` (the existing scan list).

- [ ] **Step 5: Commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "feat(skill): rename verification section to 'Verification ladder'

Replace the screenshot-centric intro with a four-rung ladder
(batch_design response → snapshot_layout → batch_get → get_screenshot).
The existing five-item visual scan list is preserved and re-anchored
under rung 4."
```

---

## Task 5: Edit 4 — Rewrite the `snapshot_layout` vs `get_screenshot` paragraph

**Files:**
- Modify: `skills/pencil-design/SKILL.md` (the paragraph beginning "**`snapshot_layout` vs `get_screenshot`.**")

- [ ] **Step 1: Locate**

Run: `grep -n "snapshot_layout\` vs \`get_screenshot" skills/pencil-design/SKILL.md`
Expected: one match.

- [ ] **Step 2: Apply the replacement**

Use the `Edit` tool. Replace this exact text:

```
**`snapshot_layout` vs `get_screenshot`.** `get_screenshot` returns pixels — use it for visual validation. `snapshot_layout` returns a structural snapshot of node positions, sizes, and layout relationships. Reach for `snapshot_layout` when you need numbers rather than pixels: verifying an exact gap width, capturing a before/after state across a sequence of updates, or debugging an auto-layout issue where the visual looks right but you need to confirm the computed values. In practice you'll use `get_screenshot` far more often; reserve `snapshot_layout` for cases where a rendered image can't tell you what you need.
```

With this exact text:

```
**`snapshot_layout` is your default verification tool, not a niche one.** It returns positions, sizes, and layout relationships as numbers — perfect for "did the gap change to 12px?", "is the button 44px tall?", "is the form column the width I asked for?". Use it after every meaningful structural change. Reach for `get_screenshot` only when the question genuinely needs pixels: visual rhythm, real-rendered contrast, image content, or final sign-off. The reflex from older versions of this skill — "screenshot after every chunk" — is wrong; it burns tokens to confirm things the structural snapshot already proved.
```

- [ ] **Step 3: Verify**

Run: `grep -c "your default verification tool" skills/pencil-design/SKILL.md`
Expected: `1`.

Run: `grep -c "you'll use \`get_screenshot\` far more often" skills/pencil-design/SKILL.md`
Expected: `0` (the old "use screenshot more often" framing is gone).

- [ ] **Step 4: Commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "feat(skill): flip snapshot_layout vs get_screenshot guidance

snapshot_layout is now the default verification tool; get_screenshot
is reserved for genuinely-visual questions. Explicitly calls out the
prior 'screenshot after every chunk' reflex as wrong."
```

---

## Task 6: Edit 5 — Update the "Edit the X" deviation

**Files:**
- Modify: `skills/pencil-design/SKILL.md` (the bullet beginning "**\"Edit the X\" or \"change the Y to Z\".**")

- [ ] **Step 1: Locate**

Run: `grep -n "One screenshot is usually enough" skills/pencil-design/SKILL.md`
Expected: one match.

- [ ] **Step 2: Apply the replacement**

Use the `Edit` tool. Replace this exact text:

```
One screenshot is usually enough.
```

With this exact text:

```
`snapshot_layout` or `batch_get` on the changed node is usually enough; screenshot only if the change was visual (a color, an image, a spacing relationship the user described in pixel terms).
```

- [ ] **Step 3: Verify**

Run: `grep -c "snapshot_layout\` or \`batch_get\` on the changed node" skills/pencil-design/SKILL.md`
Expected: `1`.

- [ ] **Step 4: Commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "feat(skill): update 'Edit the X' deviation to prefer structural verify"
```

---

## Task 7: Add the worked-example subsection

**Files:**
- Modify: `skills/pencil-design/SKILL.md` (insert a new subsection immediately after the Verification ladder section's existing scan list, before the next top-level `##` heading)

- [ ] **Step 1: Locate the insertion point**

Run: `grep -n "^## " skills/pencil-design/SKILL.md`
Expected: a list of all top-level section headings. Find `## Verification ladder` (created in Task 4) and the next `##` heading after it. The insertion goes between them, after the existing five-item scan list and the paragraph that contains "When something is off, fix it with a targeted `U` op".

Run: `grep -n "When something is off, fix it with a targeted" skills/pencil-design/SKILL.md`
Expected: one line number. The insertion goes immediately after the paragraph this line begins.

- [ ] **Step 2: Read the surrounding context**

Read the SKILL.md region from the line of the "When something is off" paragraph through the next `##` heading. You need to see exactly what comes immediately after the "When something is off" paragraph so your `Edit` `old_string` includes enough surrounding text to be unique.

Run: `sed -n '/When something is off, fix it with a targeted/,/^## /p' skills/pencil-design/SKILL.md`
Expected: the "When something is off" paragraph, then any following content (including the `snapshot_layout` vs `get_screenshot` paragraph from Task 5), then the next `##` heading. You'll insert the new subsection before that next `##`.

- [ ] **Step 3: Insert the new subsection**

Use the `Edit` tool. The cleanest insertion is to anchor on the new `snapshot_layout is your default verification tool` paragraph (created in Task 5) and insert AFTER it but BEFORE the next `##` heading. Replace the line that contains the end of that paragraph PLUS the blank line PLUS the next `##` heading, expanding to include the new subsection between the blank line and the next heading.

Concretely: identify the next `##` heading's exact text (call it `<NEXT_HEADING>`). Then replace:

```
it burns tokens to confirm things the structural snapshot already proved.

<NEXT_HEADING>
```

With:

```
it burns tokens to confirm things the structural snapshot already proved.

### Worked example: a 6-op edit, zero pre-final screenshots

User asks: *"On the LoginCard, change the Sign in button from blue to the brand green, and add 8px of breathing room above 'Forgot password?'."*

1. **Locate.** `batch_get` the LoginCard subtree, identify the button node and the link node. *(One JSON call; would have been needed regardless.)*
2. **Execute.** One `batch_design` call: `U("<button>", { fill: "$brandGreen" })`, `U("<linkContainer>", { paddingTop: 8 })`. Server response confirms both ops landed. *(Rung 1.)*
3. **Verify structure.** `snapshot_layout(parentId: "<LoginCard>", maxDepth: 2)`. Confirm the link's top padding is 8 (the only structural change) and that nothing else shifted unexpectedly. *(Rung 2.)*
4. **Verify property.** `batch_get({ nodeIds: ["<button>"] })`. Confirm `fill` resolved to `$brandGreen` (not a raw hex). *(Rung 3.)*
5. **Final visual sign-off.** `get_screenshot(nodeId: "<LoginCard>")` — scoped to the card, not the page. Confirm the green renders as expected against the card background and the spacing reads right. *(Rung 4, once.)*

Total screenshots: **1**, scoped to the smallest meaningful subtree. The pre-skill version of this same task would typically have produced 2–3 (one mid-flight, one full-canvas final, possibly one in dark mode).

<NEXT_HEADING>
```

(Substitute the actual next heading text discovered in step 2 in both `old_string` and `new_string`.)

- [ ] **Step 4: Verify**

Run: `grep -c "Worked example: a 6-op edit" skills/pencil-design/SKILL.md`
Expected: `1`.

Run: `grep -c "Total screenshots: \*\*1\*\*" skills/pencil-design/SKILL.md`
Expected: `1`.

Run: `grep -n "^## " skills/pencil-design/SKILL.md`
Expected: same set of top-level headings as before — your insertion added an `###` (subsection), not a new `##`. If a top-level heading disappeared, you over-replaced; revert and try again.

- [ ] **Step 5: Commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "docs(skill): add worked example showing 1-screenshot verification flow

Concrete example of the verification ladder applied to a 6-op edit:
locate, execute, snapshot_layout, batch_get, single final screenshot
scoped to the affected subtree."
```

---

## Task 8: Add behavioral assertions to eval 0 (login-screen-greenfield)

**Files:**
- Modify: `skills/pencil-design/evals/evals.json` (the `expected_output` field for `id: 0`)

The current eval format uses a single `expected_output` string (not a structured assertion list). The richer per-assertion structure visible in the workspace's `eval_metadata.json` is generated by the harness, not authored. So our additions need to extend the existing string while staying parseable to the harness.

- [ ] **Step 1: Read the current evals.json**

Run: `cat skills/pencil-design/evals/evals.json`
Expected: you see the three current evals. Each has a single `expected_output` string.

- [ ] **Step 2: Update eval 0's `expected_output`**

Use the `Edit` tool. Replace the exact current value:

```
"expected_output": "Agent describes the seven-step workflow: detects host first, locates context (open .pen, design-system/ folder, selection), loads guidelines, plans, executes via batch_design, verifies via get_screenshot, iterates. References design-system/ check and library import. Plans before executing.",
```

With:

```
"expected_output": "Agent describes the seven-step workflow: detects host first, locates context (open .pen, design-system/ folder, selection), loads guidelines, plans, executes via batch_design, verifies via the verification ladder (structural-first: batch_design response → snapshot_layout → batch_get → get_screenshot reserved for visual-only questions or final sign-off), iterates. References design-system/ check and library import. Plans before executing. Does NOT prescribe screenshotting after every chunk. Treats dual-mode (light + dark) screenshotting as conditional on mode-specific color usage, not mandatory.",
```

- [ ] **Step 3: Verify the JSON still parses**

Run: `python3 -c "import json; json.load(open('skills/pencil-design/evals/evals.json'))"`
Expected: no output, exit 0. Any error means the JSON is malformed — fix the quoting/escaping.

- [ ] **Step 4: Commit**

```bash
git add skills/pencil-design/evals/evals.json
git commit -m "test(eval-0): add structural-first verification assertions

Eval 0's expected output now requires the agent to describe the
verification ladder (not 'screenshot every chunk') and treat dual-mode
screenshotting as conditional. These assertions catch behavioral drift
in workflow descriptions."
```

---

## Task 9: Add behavioral assertions to eval 2 (import-library-and-use)

**Files:**
- Modify: `skills/pencil-design/evals/evals.json` (the `expected_output` field for `id: 2`)

- [ ] **Step 1: Update eval 2's `expected_output`**

Use the `Edit` tool. Replace the exact current value:

```
"expected_output": "Agent verifies the document's imports field, adds an imports entry via U op on document root if missing, queries the library's reusable components, instantiates Button and Input via ref nodes (not from primitives), uses descendants for instance-level overrides, screenshots to verify the refs resolve correctly.",
```

With:

```
"expected_output": "Agent verifies the document's imports field, adds an imports entry via U op on document root if missing, queries the library's reusable components, instantiates Button and Input via ref nodes (not from primitives), uses descendants for instance-level overrides. Verifies via the verification ladder: snapshot_layout or batch_get on the instantiated refs first to confirm structure and bindings, then a single get_screenshot scoped to the form/card subtree (via nodeId) — never the page frame — only as final sign-off.",
```

- [ ] **Step 2: Verify JSON parses**

Run: `python3 -c "import json; json.load(open('skills/pencil-design/evals/evals.json'))"`
Expected: no output, exit 0.

- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/evals/evals.json
git commit -m "test(eval-2): require structural verification before scoped screenshot"
```

---

## Task 10: Add eval 3 — execution-based edit task

**Files:**
- Modify: `skills/pencil-design/evals/evals.json` (append a new eval object with `id: 3`)

This eval differs from the existing three in that it asks the model to **actually execute** an edit via MCP tools, then explain what it did. The harness records `tool_calls` and per-run token counts, so we can measure both the count of `get_screenshot` calls (via the response text mentioning each) and the total tokens.

Because the harness has no mechanism we know of to provide a pre-existing `.pen` fixture, the prompt instructs the model to first create a tiny scratch design (one card, one button, one link) and then perform the edit. The eval's pass criteria focus on the **edit phase**, not the scratch creation.

- [ ] **Step 1: Read current evals.json**

Run: `cat skills/pencil-design/evals/evals.json`
Expected: confirm the JSON ends with `]` for the `evals` array followed by the closing `}`. You'll add a new object before that closing `]`.

- [ ] **Step 2: Append eval 3**

Use the `Edit` tool. Replace this exact text (the closing of eval 2):

```
    {
      "id": 2,
      "name": "import-library-and-use",
      "prompt": "I have a design library at design/system.lib.pen with Button and Input components. Add a sign-up form to my open .pen file using those components. Explain the tools you'd call and why.",
      "expected_output": "Agent verifies the document's imports field, adds an imports entry via U op on document root if missing, queries the library's reusable components, instantiates Button and Input via ref nodes (not from primitives), uses descendants for instance-level overrides. Verifies via the verification ladder: snapshot_layout or batch_get on the instantiated refs first to confirm structure and bindings, then a single get_screenshot scoped to the form/card subtree (via nodeId) — never the page frame — only as final sign-off.",
      "files": []
    }
  ]
}
```

With:

```
    {
      "id": 2,
      "name": "import-library-and-use",
      "prompt": "I have a design library at design/system.lib.pen with Button and Input components. Add a sign-up form to my open .pen file using those components. Explain the tools you'd call and why.",
      "expected_output": "Agent verifies the document's imports field, adds an imports entry via U op on document root if missing, queries the library's reusable components, instantiates Button and Input via ref nodes (not from primitives), uses descendants for instance-level overrides. Verifies via the verification ladder: snapshot_layout or batch_get on the instantiated refs first to confirm structure and bindings, then a single get_screenshot scoped to the form/card subtree (via nodeId) — never the page frame — only as final sign-off.",
      "files": []
    },
    {
      "id": 3,
      "name": "edit-existing-card-verification-ladder",
      "prompt": "I want to test how you verify edits. First, create a brand-new .pen scratch document with a single LoginCard frame containing: a 'Sign in' heading, an Email input, a Password input, a primary 'Sign in' button (blue fill), and a 'Forgot password?' link below the button. Once that's in place, perform this edit: change the Sign in button's fill to a brand green color, and add 8px of paddingTop to the link's container so it has more breathing room. After the edit, explain — step by step — exactly which MCP tools you called to verify the edit landed correctly, in what order, and why you chose each. Be precise about which nodeId you passed to each verification call.",
      "expected_output": "Agent first creates the scratch design via batch_design (this phase is not graded). For the edit phase: identifies the affected nodes via batch_get, performs the two-op edit in a single batch_design call. Verification follows the four-rung ladder: (1) acknowledges the batch_design response confirmed both ops landed; (2) calls snapshot_layout scoped to the LoginCard (parentId is the card, not the document root) to confirm the link's paddingTop is 8 and the button's geometry is unchanged; (3) calls batch_get on the button node to confirm fill resolved to the brand green variable (not a raw hex); (4) calls get_screenshot AT MOST ONCE, scoped to the LoginCard nodeId (NOT the document root or page frame), as a final visual sign-off. Total get_screenshot calls in the edit phase: exactly 1. Does NOT re-screenshot in dark mode (the change is structural + a variable-bound color, not mode-conditional). Does NOT screenshot the document root.",
      "files": []
    }
  ]
}
```

- [ ] **Step 3: Verify JSON parses**

Run: `python3 -c "import json; d = json.load(open('skills/pencil-design/evals/evals.json')); print(len(d['evals']), 'evals,', [e['id'] for e in d['evals']])"`
Expected: `4 evals, [0, 1, 2, 3]`.

- [ ] **Step 4: Commit**

```bash
git add skills/pencil-design/evals/evals.json
git commit -m "test(eval-3): add execution-based edit task for verification ladder

New eval where the model actually invokes MCP tools to perform a small
edit, then must explain its verification choices. Pass criteria: at most
one get_screenshot call in the edit phase, scoped to the affected
subtree (not the document root), structural verification (snapshot_layout
+ batch_get) before any screenshot, no dark-mode re-screenshot."
```

---

## Task 11: Update the changelog

**Files:**
- Modify: `docs/CHANGELOG.md`

- [ ] **Step 1: Read the current changelog format**

Run: `cat docs/CHANGELOG.md`
Expected: you see the existing entries and their format. Match it. The current SKILL.md version is `1.2.0` (per its frontmatter); decide whether this change warrants a minor (`1.3.0`) or patch bump. The change is additive guidance with no breaking removals — minor bump (`1.3.0`) is correct.

- [ ] **Step 2: Add an entry for this change**

Use the `Edit` tool to add a new entry at the top of the changelog (or in the place the existing format dictates — match what you see). The entry should briefly summarize: verification ladder reframe, reduced screenshot defaults, conditional dual-mode rule, new worked example, eval suite updated with one new execution eval.

If the changelog format is unclear or the file does not exist, skip this task and note it in the next commit message instead. The change is not blocked by an unwritten changelog.

- [ ] **Step 3: Bump SKILL.md version**

Use the `Edit` tool. In `skills/pencil-design/SKILL.md` frontmatter, replace:

```
  version: "1.2.0"
```

With:

```
  version: "1.3.0"
```

- [ ] **Step 4: Verify**

Run: `grep -A1 "^metadata:" skills/pencil-design/SKILL.md | head -3`
Expected: shows `version: "1.3.0"`.

- [ ] **Step 5: Commit**

```bash
git add docs/CHANGELOG.md skills/pencil-design/SKILL.md
git commit -m "chore(skill): bump version to 1.3.0 and update changelog

Verification ladder reframe + eval suite updated."
```

If you skipped the changelog edit in step 2, drop `docs/CHANGELOG.md` from the `git add` and adjust the commit message accordingly.

---

## Task 12: Final consistency pass

**Files:**
- Read: `skills/pencil-design/SKILL.md` (whole file)

- [ ] **Step 1: Read the whole edited SKILL.md**

Run: open `skills/pencil-design/SKILL.md` end-to-end.
Expected: you can read it as a single coherent document. Watch for: (a) any *remaining* references to "screenshot after every chunk" or similar legacy framing; (b) any cross-reference to "step 6" that no longer matches; (c) any internal contradiction between the new ladder and any other section.

- [ ] **Step 2: Search for stale phrasings**

Run: `grep -in "screenshot is cheap\|after each meaningful chunk\|after each chunk\|re-screenshot under" skills/pencil-design/SKILL.md`
Expected: zero matches. If any remain, they're stale legacy framing — apply targeted edits to bring them into alignment with the ladder, then commit.

- [ ] **Step 3: Search for accidental duplication**

Run: `grep -c "verification ladder" skills/pencil-design/SKILL.md`
Expected: a small number (≤6). If you see something like 15+ matches, the worked example or one of the edits duplicated the phrase excessively — review and trim.

- [ ] **Step 4: Run the lint**

Run: `python3 tools/skill-lint.py`
Expected: exit 0. The lint protects the skill's frontmatter and structural conventions; it should pass cleanly because no structural change was made.

- [ ] **Step 5: If anything was changed in steps 2 or 3, commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "refactor(skill): clean up stale screenshot framing in remaining paragraphs"
```

If nothing changed, no commit needed.

---

## Task 13: Hand off to the user for eval-harness validation

**Files:** None.

This task is the human handoff. The implementer cannot run the eval harness (it lives outside this repo).

- [ ] **Step 1: Summarize the change set in a hand-off message**

Tell the user:

> SKILL.md has been edited per `docs/superpowers/specs/2026-05-03-screenshot-token-reduction-design.md`. The eval suite has been updated with assertion changes to evals 0 and 2 plus a new execution eval (id 3). To validate the change against the spec's acceptance criteria, please run the skill-developer eval harness against `skills/pencil-design/` and compare the resulting `benchmark.json` to `skills/pencil-design-workspace/iteration-1/benchmark.json` (the pre-change baseline). Specifically check:
>
> 1. **Pass rate on every eval (`with_skill` mode) holds at or above the baseline.** Baseline: eval 0 = 1.0, eval 1 = 1.0, eval 2 = 1.0. Eval 3 has no baseline (it is new); a pass rate ≥ 0.7 is the bar.
> 2. **Tokens on eval 3 (`with_skill`) are at least 30% below the same eval running `without_skill`.** This is the headline acceptance number.
> 3. **No `with_skill` eval regresses on tokens by more than 10% versus baseline.** Some shift is expected; large regression suggests the SKILL.md edits added bloat.
>
> If criteria are met, the change ships. If criteria fail, iterate on the SKILL.md edits and re-run.

- [ ] **Step 2: Stop**

Implementation is complete. The user owns the eval-harness run and the merge decision. Do not loop on hypothetical eval results.

---

## Self-review

Spec coverage check:

- ✅ "Five surgical edits to SKILL.md" → Tasks 2, 3, 4, 5, 6.
- ✅ "Worked example to add" → Task 7.
- ✅ "Behavioral assertions on existing evals" → Tasks 8, 9.
- ✅ "One new execution eval" → Task 10.
- ✅ "Acceptance criteria measured against eval harness" → Task 13.
- ✅ Version + changelog bump (project hygiene the spec implies but doesn't spell out) → Task 11.
- ✅ Final read-through to catch stray legacy phrasings → Task 12.

Placeholder scan: no "TBD" or "implement later" in the plan. The one conditional ("if changelog format is unclear, skip") is bounded with explicit fallback behavior.

Type/name consistency: every task references `skills/pencil-design/SKILL.md`, `skills/pencil-design/evals/evals.json`, and `docs/CHANGELOG.md` consistently. The "verification ladder" phrase appears identically across SKILL.md edits (Tasks 2–7) and eval assertions (Tasks 8–10). Eval 3's pass criteria reference the same four rungs in the same order as Task 4's rewrite. The new section heading is `## Verification ladder` (Task 4) and is referenced by the worked-example anchor in Task 7 and by the cadence paragraph in Task 3 (`workflow step 6`) and by Task 5 (`older versions of this skill`). No drift.
