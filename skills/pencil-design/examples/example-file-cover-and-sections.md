# Example: set up a `.pen` file with Cover frame, section regions, and hierarchical naming

User says:

> *"Start a new `.pen` file for the customer-portal redesign. Set up the file architecture properly: Cover, sections, naming."*

This example shows the agent setting up a fresh `.pen` per the file-architecture conventions: Cover frame at canvas origin, section regions for Source of Truth / Build Ready / UX States / Exploration / Archive, and hierarchical naming for multi-screen flows.

---

## Step 1: Read context

```js
get_editor_state();
```

The agent reads `design-system/file-architecture.md` (project's file-architecture commitments), `visual-style.md`, and `tokens.md`. Loads `references/file-architecture.md` (the canonical Cover frame, section regions, hierarchical naming reference).

## Step 2: Find canvas origin

The Cover frame lives at canvas origin (0, 0). Subsequent sections lay out below or to the right. `FindEmptySpace` runs as the first line inside the `batch_design` snippet (it returns `{x, y}`):

```js
batch_design({ filePath: "", input: `
const slot = FindEmptySpace({ width: 1440, height: 900 })
// For a fresh .pen, slot is { x: 0, y: 0 }. Build the Cover there.
` })
```

For a fresh `.pen`, this returns (0, 0). Build the Cover there.

## Step 3: Build the Cover frame

Per `references/file-architecture.md` § Cover frame template: every `.pen` opens with a top-level `Cover` frame at canvas origin containing file owner, status, version, last updated, scope, and links.

```js
batch_design({ filePath: "", input: `
Insert(document, {
  type: "frame",
  name: "Cover",
  context: "File operating manual: owner, status, version, scope, links.",
  width: 800,
  height: 600,
  x: 0,
  y: 0,
  layout: "vertical",
  padding: 48,
  gap: 24,
  fill: "$surface",
  children: [
    { type: "text", name: "FileTitle", content: "Customer portal redesign", fontFamily: "$fontDisplay", fontWeight: "$fontWeightBold", fontSize: 48 },
    { type: "frame", name: "Meta", layout: "horizontal", gap: 32, children: [
      { type: "frame", name: "MetaItem_Owner", children: [
        { type: "text", content: "Owner", fill: "$textSecondary" },
        { type: "text", content: "<Designer Name>" },
      ]},
      { type: "frame", name: "MetaItem_Status", children: [
        { type: "text", content: "Status", fill: "$textSecondary" },
        { type: "text", content: "In design" },
      ]},
      { type: "frame", name: "MetaItem_Version", children: [
        { type: "text", content: "Version", fill: "$textSecondary" },
        { type: "text", content: "0.1" },
      ]},
      { type: "frame", name: "MetaItem_Updated", children: [
        { type: "text", content: "Last updated", fill: "$textSecondary" },
        { type: "text", content: "<YYYY-MM-DD>" },
      ]},
    ]},
    { type: "frame", name: "Scope", children: [
      { type: "text", content: "Scope", fill: "$textSecondary" },
      { type: "text", content: "In: customer-facing dashboard, billing, profile, support entry. Out: admin panels (separate file)." },
    ]},
    { type: "frame", name: "Links", children: [
      { type: "text", content: "Links", fill: "$textSecondary" },
      { type: "text", content: "Brief: <link>. Linear: <link>. Prototype: <link>. Design system: design-system.lib.pen." },
    ]},
  ],
})
` })
```

The Cover takes about 30 seconds to scan; without it, no one (human or AI) can answer 'is this safe to build from?' in under 30 seconds.

## Step 4: Set up the section regions

Per `references/file-architecture.md` § Section regions: each `.pen` organises its top-level frames into named sections positioned in canvas regions.

| Section | Canvas region | Purpose |
|---|---|---|
| Cover | (0, 0) | File operating manual |
| Source of Truth | Row 1 (right of Cover or below) | Build-ready, approved frames |
| Build Ready | Row 2 | Current iteration in flight |
| UX States | Row 3 | State matrices (loading, empty, error per surface) |
| Responsive | Row 4 | Per-breakpoint variants |
| Exploration | Far-right region | Drafts, rejected directions |
| Archive | Bottom region | Superseded designs |

The agent creates section header frames as visual anchors so the canvas reads intuitively. These aren't required per the schema; they're convention so the next agent recognises which region is which.

```js
batch_design({ filePath: "", input: `
Insert(document, {
  type: "frame",
  name: "_Section_SourceOfTruth",
  context: "Visual anchor for the Source of Truth region. Build-ready, approved frames live here. Code generation reads from this region only.",
  width: 400,
  height: 60,
  x: 0,
  y: 700,
  fill: "$surfaceMuted",
  children: [
    { type: "text", content: "Source of Truth", fontFamily: "$fontDisplay", fontWeight: "$fontWeightSemiBold" },
  ],
})
Insert(document, {
  type: "frame",
  name: "_Section_BuildReady",
  context: "Visual anchor for the Build Ready region. Current iteration in flight; about to be promoted to Source of Truth.",
  x: 0,
  y: 2000,
  // ... similar shape
})
// Repeat for UXStates, Responsive, Exploration, Archive
` })
```

The agent calls `FindEmptySpace` (inside `batch_design`) between regions to honour the layout. Never place an Exploration frame in the Source of Truth region.

## Step 5: Add the first Source of Truth frame

Now the agent adds the first design under Source of Truth. For a multi-screen flow, use hierarchical naming per `references/file-architecture.md` § Hierarchical naming patterns: `[Area] / [Flow] / [Step] / [Screen] / [State] / [Breakpoint]`.

```js
batch_design({ filePath: "", input: `
const slot = FindEmptySpace({ width: 1440, height: 900, nodeId: "<source-of-truth-region-anchor>" })
Insert(document, {
  type: "frame",
  name: "Customer / Dashboard / Default / Desktop",
  context: "Customer dashboard, default state, desktop breakpoint. Source of Truth.",
  x: 0,
  y: 800,
  width: 1440,
  height: 900,
  // ... dashboard content
})
` })
```

The slash-delimited name is allowed in the `name` field. Slashes are forbidden in `id` (the schema rejects them).

## Step 6: Add a multi-screen flow with hierarchical naming

For a flow that crosses multiple screens, each screen is a sibling top-level frame:

```js
batch_design({ filePath: "", input: `
Insert(document, {
  type: "frame",
  name: "Customer / Billing / 01 / SelectPlan / Default / Desktop",
  x: 0, y: 1750,
  width: 1440, height: 900,
})
Insert(document, {
  type: "frame",
  name: "Customer / Billing / 02 / EnterPayment / Default / Desktop",
  x: 1500, y: 1750,
  width: 1440, height: 900,
})
Insert(document, {
  type: "frame",
  name: "Customer / Billing / 03 / Confirm / Default / Desktop",
  x: 3000, y: 1750,
  width: 1440, height: 900,
})
Insert(document, {
  type: "frame",
  name: "Customer / Billing / 03 / Confirm / ValidationError / Desktop",
  x: 3000, y: 2700,
  width: 1440, height: 900,
})
` })
```

The naming carries: Area (Customer), Flow (Billing), Step (01, 02, 03), Screen (SelectPlan, EnterPayment, Confirm), State (Default, ValidationError), Breakpoint (Desktop).

## Step 7: Add an Exploration frame

When the agent (or designer) wants to try an alternative approach, the work goes in the Exploration region, far from Source of Truth.

```js
batch_design({ filePath: "", input: `
Insert(document, {
  type: "frame",
  name: "Customer / Billing / 01 / SelectPlan / Exploration_Bento_v1",
  context: "Exploration: Bento-style plan selector instead of the three-card layout. Status: draft, do not generate code from this frame.",
  x: 8000, y: 1750,
  width: 1440, height: 900,
})
` })
```

If the exploration gets promoted, the agent moves the frame into the Source of Truth region (reposition; rename to drop the `Exploration_` suffix). Don't dual-track once promoted.

## Step 8: Add a UX State matrix

Per the section convention, state matrices for each surface live in the UX States region.

```js
batch_design({ filePath: "", input: `
Insert(document, {
  type: "frame",
  name: "Customer / Dashboard / States",
  context: "State matrix for the Customer Dashboard: Default, Loading, Empty, Error, NoPermission.",
  x: 0, y: 3000,
  layout: "horizontal",
  gap: 32,
  children: [
    // Sibling sub-frames per state
  ],
})
` })
```

## Step 9: Component status workflow

For any reusable component the agent creates while working on this `.pen`, document the status in `context` per `references/composition-patterns.md` § Component status workflow:

- `status: "draft"`: under construction.
- `status: "ready"`: functional; safe to use; may evolve.
- `status: "stable"`: locked; safe long-term.
- `status: "needs-review"`: changed recently; verify before use.
- `status: "deprecated"`: replaced; see `replacedBy: "<componentId>"`.

## Step 10: Verify

Walk through the file:

1. Cover frame at (0, 0) with all required fields populated.
2. Section regions present and used (Source of Truth, Build Ready, etc.).
3. Hierarchical naming applied to multi-screen flows.
4. `design-system.lib.pen` listed in `imports`.
5. No Exploration frames in the Source of Truth region.
6. Components carry status in `context`.

```js
get_screenshot({ filePath: "", nodeId: document });
```

The full canvas screenshot shows the regions visually. Cover top-left, Source of Truth in row 1, Build Ready in row 2, etc.

## See also

- `references/file-architecture.md`: the canonical reference for Cover frames, sections, naming, multi-`.pen` decisions.
- `references/composition-patterns.md` § Component status workflow.
- `design-system/file-architecture.md`: project's file-architecture commitments.
- `design-system/visual-style.md`: project's chosen style.
- `examples/example-component-deep-dive.md`: deeper example of working with components within a `.pen`.
- `SKILL.md` § Discipline rules § File architecture.
