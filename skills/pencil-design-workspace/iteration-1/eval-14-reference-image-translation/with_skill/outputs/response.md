# Translating Linear's issue list into our project

Quick housekeeping first: no screenshot is actually attached to this turn, so I'll walk you through the protocol I'd follow when one arrives, with the specific tool calls and decisions baked in. When you paste the image, I'd run this exact sequence — not improvise.

## Why this is a "translate, don't copy" job

Linear's issue list is a strong reference because it's a famously well-tuned **three-column nav / list / detail** layout (per `references/layout-patterns.md` § Dashboard layouts and § List-detail layouts). It's also a famously *Linear* design — its typography, its near-monochrome palette, its specific row density, and its keyboard-first chrome are all part of Linear's brand. Lifting it verbatim would ship a Linear clone with our logo on it, which is the **reference-image translation anti-pattern** called out in `references/iteration-patterns.md` § Anti-patterns.

So the goal is: same *layout pattern*, our *atmosphere*. That's what the protocol below enforces.

## The protocol I'd follow when the screenshot arrives

I'm working from `references/iteration-patterns.md` § Reference-image translation protocol, which gives a six-step sequence. I'm grounding the rest in `SKILL.md` § Default workflow (steps 1 through 7) and the *"User shows you a reference image"* branch in § Design intelligence, which says: read the image, name the layout pattern out loud, *then* plan the tree.

### Step 0: host check (always first)

```
get_editor_state({ include_schema: false })
```

Expected response shape: an object with the active document, the current selection, and the schema version. If it errors with `transport not connected to app: desktop`, I stop and tell you to open the Pencil desktop app — I never silently fall back (`SKILL.md` § Failure modes #1).

What I'd check: which `.pen` is open, what's selected, what `imports` the document declares (especially whether your `.lib.pen` is already attached).

### Step 1: name the layout pattern out loud

This is the single highest-value thing the skill teaches for reference-image work. Before any planning, I'd say something like:

> "This is a **three-column nav / list / detail** layout (per `layout-patterns.md`). Left rail is a workspace sidebar with team and view navigation. Middle column is a high-density issue list — flat rows, no card chrome, status pill + identifier + title + assignee + labels + priority + estimate + date. The right edge sometimes hosts a detail panel; sometimes the list takes the full right area. It's a **command-driven dashboard** in spirit (cmd+K is the primary nav), so the visible chrome stays minimal."

Naming the pattern matters because the skill's research note (Nielsen Norman, plus observed AI design tells) is that the model produces visibly better designs when it labels the structure first. Skipping this is how you end up with a list that looks technically right but reads as Generic Issue Tracker #47.

### Step 2: extract the palette and map it to our tokens

Linear's palette is roughly: near-black background, a single neutral surface step lighter for hover/selection, a single muted accent (Linear's purple), priority colours that pair with shape (urgent = red, high = orange, medium = yellow, low = grey), and label tints that the user assigns.

I would *not* sample those hex values directly. The protocol (step 2 of `iteration-patterns.md`) is:

1. `get_variables()` — see what tokens we already have. If the project's `.pen` already has `surface`, `surfaceHover`, `border`, `textPrimary`, `textMuted`, `accent`, `success`, `warning`, `danger`, I use those.
2. `get_guidelines()` — see what the document declares about colour conventions.
3. Read `design-system/tokens.md` if it exists — it's authoritative over my defaults.

The mapping I'd make in my head: Linear's near-black → our `$surface` (which should already resolve to off-black in dark mode and off-white in light mode, never raw `#000` per the AI-tells list). Linear's selection grey → `$surfaceHover`. Linear's accent purple → our `$accent` (which might be a totally different hue). Their priority colours → our existing `$danger / $warning / $caution / $textMuted` semantic colours.

What I'd *not* port: Linear's specific purple. We have our own accent.

### Step 3: identify the type pairing

Linear ships in a custom-cut Inter variant. We don't — and per `SKILL.md` § Aesthetic defaults § Typography, **Inter is banned by default** as the AI signature. I'd check `tokens.md` for our committed `$fontBody` / `$fontMono`. If the project hasn't committed yet and this is a real software-UI surface, defaults from the skill are `Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`.

The list itself wants tabular numerics on the identifier column (PR-1234, PR-1235) and the date column. That's `font-variant-numeric: tabular-nums`, documented in the row component's `context` so the engineer ships the CSS (per `SKILL.md` § Typography).

### Step 4: name the design movement / era

Linear sits in the **modern dark-mode-first SaaS** tradition (also: Vercel, Raycast, Arc). The vocabulary: extremely flat surfaces, near-zero border-radius on rows, single-pixel borders instead of shadows, monochrome with one restrained accent, command-palette-as-primary-nav, type doing most of the hierarchy work.

If our project already commits to a different style (per `references/style-catalogue.md` and our `assets/design-system/visual-style.md` if scaffolded) — say we're an editorial brand, or we're light-mode-first — I'd flag the mismatch and ask whether we want our list to feel like Linear's tradition or our own. I would not silently translate a brutalist reference into a Swiss design system.

### Step 5: call out what to deliberately change

The protocol requires me to name two or three intentional deviations *before* building. Without this, the translation drifts into a clone. My typical list for a Linear-derived issue list:

1. **Our accent, not theirs.** Wherever Linear uses purple (selected row, primary action, focus ring), we use `$accent`.
2. **Our typography.** No Inter; whatever `$fontBody` resolves to in our tokens. Probably a slightly more characterful display face for the page heading.
3. **One density step looser than Linear** if our audience isn't power-user-first. Linear ships ~32px row height; we might ship 40px and let the column padding breathe. If we *are* power-user-first, we keep Linear's density but pick a different lever to differentiate (see #4).
4. **One "brave" choice** per `iteration-patterns.md` § Failure mode: too generic. The single-biggest tell of AI design is "every choice was the safe one." Options I'd consider: an asymmetric column header treatment, a custom empty-state illustration, an unconventional priority indicator (a vertical bar on the row's leading edge instead of a coloured dot — borrowed from Things 3), or treating the keyboard-shortcut hints as first-class visible chrome instead of hiding them.

I'd surface these to you before spending ops, because they're the choices most worth pushing back on cheaply.

### Step 6: components-first inventory (before any insertion)

This is `SKILL.md` § Discipline rules § Components first, and it's non-negotiable. Two scans:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Expected response shape: an array of component nodes, each with `id`, `name`, `context`, child slot structure. What I'd check: do we already have `Sidebar`, `RowList`, `Row`, `StatusPill`, `Avatar`, `Label`, `PriorityIndicator`, `EmptyState`, `Pagination`? If yes, I instantiate them via `ref` nodes with `descendants` overrides. I do *not* hand-build a button when a `Button` exists in the library — that ships drift. If a component looks promising but I haven't read it deeply, I drill in:

```
batch_get({ nodeIds: ["RowComponentId"], readDepth: 4 })
```

…to find slot frames, named children, and theme states (per `references/component-anatomy.md`). The component's `id` for each named child is the addressable path I'd use in `descendants`.

### Step 7: plan the tree (state it back to you in 2-3 sentences)

Per `SKILL.md` § Default workflow step 4. Something like:

> "I'll create one top-level frame `IssueList_Desktop` (1440 × 900) using our `MasterDetail` reusable. Left column: `Sidebar` ref (240px wide) with active state on 'All issues'. Middle: a `RowList` containing 12 `Row` refs with realistic-but-not-real content (no John Doe, no Acme — plausible engineering-team issue titles). Right detail panel collapsed by default; `IssueDetail` ref filling it when an issue is selected. Atmosphere is **dense / symmetric / static** per the aesthetic vibe rule. Cover frame stays where it is; new frame placed in the BuildReady region via `find_empty_space_on_canvas` so it doesn't overlap existing work."

Vibe sentence is required — `SKILL.md` § Aesthetic defaults § Name the atmosphere. Without it the design defaults to "balanced / symmetric / fluid" and reads generic.

This is the moment to catch bad assumptions cheaply. If you want a single-column list (no detail panel ever) or a modal detail (mobile-style), now's the time to redirect — not after 25 ops.

### Step 8: execute (one batch_design call, ≤25 ops)

A single `batch_design` call building the outer frame, the sidebar ref, the list container, the rows. Tool call shape:

```
batch_design({
  documentId,
  ops: "list=I(\"<canvas>\", { type: \"frame\", name: \"IssueList_Desktop\", ... })\n
        sidebar=I(list, { type: \"ref\", ref: \"Sidebar\", descendants: { active: \"AllIssues\" } })\n
        main=I(list, { type: \"frame\", name: \"Main\", layout: { direction: \"column\" } })\n
        header=I(main, { type: \"frame\", name: \"ListHeader\", ... })\n
        rows=I(main, { type: \"frame\", name: \"RowList\", ... })\n
        r1=I(rows, { type: \"ref\", ref: \"Row\", descendants: { ... } })\n
        ... (rest of the rows)"
})
```

Bound variables (`list=`, `sidebar=`, `main=`) so later ops can reference the just-created node without me hardcoding ids the server hasn't issued yet. Per `references/batch-design-grammar.md`.

Discipline I'd apply at every op:

- **Every node gets a meaningful PascalCase `name`** — `IssueList_Desktop`, `Row`, `StatusPill`, `AssigneeAvatar`. Never `Frame`, `Group`, `wrapper`. Per `SKILL.md` § Naming.
- **Every non-trivial node gets a `context`** documenting intent and behaviour. For the row: *"List item for a single issue. Click navigates to /issue/[id]. Hover reveals quick-actions on the right (assign, change status, set priority). Status pill colour pairs with text label so colour-blind users get the signal. Tabular numerics on identifier and date columns."* Not visual specs.
- **Colours via `$variables`, never raw hex.** `fill: "$surface"`, not `fill: "#0B1117"`. Per § Themes.
- **Fill content with plausible context-appropriate strings** — engineering issue titles like "Refresh token expires before silent re-auth fires", not Lorem Ipsum and not Acme.

### Step 9: verify (structural-first, then one screenshot)

This is the part the skill rewrote in v1.4 to push back against the old "screenshot after every change" reflex. The verification ladder (`SKILL.md` § Verification ladder):

1. **`batch_design` response** — confirms ops landed. Free.
2. **`snapshot_layout(parentId: "<list>", maxDepth: 3)`** — confirms structural intent. Returns positions, sizes, gaps as numbers. Cheap. I'd check: is the sidebar 240px wide? Is the row gap 0 (Linear ships flush rows) or our chosen step? Is each row 40px tall (or whatever we committed in step 5)?
3. **`batch_get({ nodeIds: ["<row>", "<statusPill>"] })`** — confirms `fill` resolved to `$surface`, not a raw hex. Confirms refs instantiated. Cheap.
4. **`get_screenshot({ nodeId: "<list>" })`** — *one* screenshot, scoped to the list frame, not the whole canvas. Reserved for the genuinely-visual checks: does the rendered density read right? Does the contrast on the muted text actually pass WCAG AA against `$surface` (4.5:1 for body, 3:1 for large/UI)? Is the priority indicator visible without being shouty?

Total screenshots for this task: **one**, at the end. The pre-skill version of this same task would typically have screenshotted three times (sidebar pass, list pass, full final). The skill explicitly calls that out as the wrong reflex.

I would *not* screenshot the dark mode separately if every colour is bound to a `$variable` with both `light` and `dark` values. The variable system guarantees the dual-mode behaviour; re-screenshotting just to "confirm both modes hold up" burns tokens for no information (`SKILL.md` § Default workflow step 6, dual-mode rule).

### Step 10: run the four-question self-critique gate

Before declaring done, the 60-second gate from `SKILL.md` § Self-critique gate (and expanded in `iteration-patterns.md`):

1. **Could a non-designer recognise this as our brand or industry?** If our list could belong to any issue tracker, I haven't committed hard enough. The "brave choice" from step 5 should be visible at this point.
2. **Where does the eye go first / second / third?** Trace the path. On a list, the answer should be: row title (primary content) → status pill (state) → assignee (who). If the eye lands on a label colour or a decorative divider, demote it.
3. **What's decorative-only?** Removing zebra-striping, gratuitous borders, or shadows that don't carry information.
4. **What single change would make this feel less AI-generated?** If I can name one and it's cheap, do it. If I can't name one, it's probably fine.

I fix what surfaces. I don't ship with a TODO.

### Step 11: document the translation in `context`

Per `iteration-patterns.md` § Reference-image translation protocol step 6, I document the translation choices in the page frame's `context` so the next agent reading the file can trace which decisions came from the source and which were ours:

> "Layout derived from Linear's issue list (three-column nav / list / detail). Deviations from source: our `$accent` (not Linear's purple); our `$fontBody` (not Inter); priority shown as leading vertical bar on each row instead of dot (differentiation choice). Density matches source (~32px row height) — power-user audience justifies it. Empty state and skeleton row to be designed in Phase 2."

This is the part most reference-image work skips. It's the difference between an agent six months from now understanding "we did this on purpose" vs. assuming the row height is a bug to fix.

## What I'd hand back

A single short paragraph naming what landed: *"Built `IssueList_Desktop` — three-column layout with `Sidebar`, `RowList` of 12 issues, and a `IssueDetail` panel — instantiated from the design library. Deviations from the Linear reference are documented in the frame's `context`. Verified: structure (snapshot_layout), variable bindings (batch_get), and final visual (one screenshot scoped to the list frame). Empty state, skeleton, and loading states noted as Phase 2."*

If you ship the screenshot, I'll drive this for real. The protocol above is the same one I'd execute the moment the image is in front of me — no more, no less.

## References I consulted (and why)

- `SKILL.md` — for the host-check, the default workflow steps, the discipline rules (naming, context, components-first, themes, responsive, accessibility, file architecture), and the *"User shows you a reference image"* branch in § Design intelligence.
- `references/iteration-patterns.md` — owns the **Reference-image translation protocol** (the six-step sequence), the four-question self-critique gate, and the failure-mode rescues I'd reach for if iteration 2 is needed.
- `references/layout-patterns.md` — for naming the pattern (three-column nav/list/detail; command-driven dashboard) and for the list-detail variants table that justifies the layout choice over alternatives like modal-detail or full-page-detail.
- `assets/examples/example-dashboard.md` — for the worked shape of `find_empty_space_on_canvas` → outer frame → inner refs sequence and the verification cadence on a real dashboard task.

I did *not* load `references/visual-hierarchy.md`, `references/data-viz.md`, `references/interactions.md`, `references/forms.md`, or `references/mcp-tools.md` for this task. They'd be loaded if the iteration revealed an unclear hierarchy, if you asked for inline charts in the rows, if we got into keyboard nav details, if there was form behaviour, or if I needed a less-familiar tool. The skill's design is to load on demand, not upfront — and a translation task that's mostly about naming and palette mapping doesn't need them yet.
