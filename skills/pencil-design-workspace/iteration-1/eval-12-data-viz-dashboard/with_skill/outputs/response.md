# SaaS analytics dashboard — four tiles

I'll design this as a real Pencil workflow: detect the host, locate context, load the right guidelines, plan, execute, verify. Here is exactly what I'd do, the tool calls I'd issue, the response shapes I'd expect, and what I'd check at each step.

## Skill references consulted

Before planning a single op, I loaded these files from the `pencil-design` skill:

- `references/data-viz.md` — for the 25-chart selection matrix (data shape → ideal chart), the colour-blind-safe palette families (Okabe-Ito, ColorBrewer, Viridis), dashboard tile shapes (KPI / chart / table), default chart styling rules, and the chart anti-patterns (3D, pie > 5 slices, dual y-axes, red-green only). This is the single most relevant file for the prompt — every tile in the request is a different chart shape, so picking correctly per data shape is the core decision.
- `assets/examples/example-data-visualization.md` — a near-identical worked example (revenue trend, conversion by channel, churn cohort heatmap, top customers). I'm not going to slavishly copy it, but its structure validates my plan and gives me a known-good Pencil expression for each tile shape.
- `references/layout-patterns.md` § Dashboard layouts — to pick the page shell. Sidebar + main is the SaaS default; this prompt is squarely in that family.
- `assets/examples/example-dashboard.md` — for the simpler precedent: KPI row → chart row → table row, KPI card anatomy (value / label / delta / sparkline), partial-failure error pattern (one tile failing doesn't black out the whole dashboard).
- `references/industry-patterns.md` § SaaS § Analytics — confirms the defaults: data-dense, chart-forward, number-first, dark mode shipped by default, ⌘+K command palette is table-stakes, plan-restricted / no-permission states designed.
- `references/batch-design-grammar.md` — to make sure the ops I write below are valid (`foo=I("parent", {...})` binding form, `placeholder: true` on the top-level frame, `width: "fill_container"` bare-string, no `/` in ids).

I did not load `forms.md`, `mobile-patterns.md`, `flows.md`, or `iconography.md` — none of them is on the critical path for a four-tile static dashboard. I also skipped `style-catalogue.md` / `colour-palettes.md` / `font-pairings.md`: those govern *committing* a fresh visual style, but the prompt is implicitly building inside an existing analytics SaaS, so I'd defer to the project's `design-system/` and only fall back to the SaaS analytics defaults from `industry-patterns.md` if it's missing.

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

**Expected response shape.** A JSON object with `documentId`, `documentPath` (e.g. `./design/dashboard.pen`), `selection` (array of node ids), `themes`, `imports`, and the document-level `variables` summary. If it errors with `transport not connected to app: desktop`, I stop and tell the user to open the Pencil desktop app or the Pencil IDE extension. I do **not** silently fall back to the CLI — that's the no-auto-fall-back policy from the skill's failure modes table (case 1) and `references/pencil-cli.md`.

If it succeeds and reports no active document, I'd ask whether to open an existing `.pen` (give me the path) or create a new one with `open_document('new')` (failure mode 2).

## Step 2 — Locate context

From `get_editor_state`'s response I'd note:

- Which `.pen` is open and whether it has any existing top-level frames I'd collide with.
- The `imports` field — I want to know if a `system.lib.pen` (or similar) is attached, because that's where the `KPICard`, `ChartTile`, `TableTile`, `Sidebar`, and `Button` reusables almost certainly live in a real analytics SaaS.
- Existing `themes`. If there's already a `mode` axis with `light` and `dark`, I do not redeclare it.

Then I'd check the project filesystem (directory listing, not MCP) for `./design-system/`. The Components-first rule and the design-system convention both hinge on this.

## Step 3 — Load guidelines, inventory components, read tokens

```
get_guidelines({})                                  // see what categories the server reports
get_guidelines({ categories: ["Web App", "Table"] }) // load the relevant ones
get_variables({})                                   // critical: read existing tokens before set_variables can clobber them
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })  // inventory components in the open doc
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })  // and in each imported library
```

**What I'd check.**

- `get_guidelines` confirms the categories applicable to this document. For an analytics SaaS dashboard I want `Web App` and `Table` at minimum. If `Tailwind` shows up, I note it for the eventual code-export commitment.
- `get_variables` returns whatever tokens already exist. **I never call `set_variables` with a default suite before reading this** — `replace: false` (the merge default) still overwrites any keys I pass, so blindly bootstrapping clobbers the user's customisations. This is failure mode 7 in the skill.
- The `batch_get` patterns sweep tells me whether `KPICard`, `ChartTile`, `TableTile`, `Sidebar`, `Badge`, and `Button` already exist as `reusable: true` components. If they do, I instantiate via `ref` nodes. If they don't, I'll surface that to the user before building anything from primitives ("This pattern looks reusable — should I add `KPICard` to your `.lib.pen`?").

If the project has `design-system/`, I'd then read `README.md`, then `design-system.md` (icon library, `.lib.pen` path, tech stack), then `tokens.md` (which colour / spacing / type token to use when), then `data-viz.md` if it exists (the project's *committed* chart palette — this overrides the catalogue defaults). If not, I'd offer once to scaffold (failure mode 3) and proceed with the SaaS analytics defaults from `references/industry-patterns.md`: Indigo Calm palette, Inter + JetBrains Mono, very dense.

## Step 4 — Plan (atmosphere + chart picks + layout)

**Atmosphere commitment** (per the Aesthetic defaults rule — name the atmosphere before planning ops): *Dense dashboard, symmetric, static.* Number-first, chart-forward, calm chrome. No hero typography, no decorative gradients, no animation past the chart load-in.

**Chart pick per tile** (per `references/data-viz.md` § The 25-chart selection matrix):

| Tile | Data shape | Chart pick | Why this and not the AI default |
|---|---|---|---|
| 1. MRR trend | One series over time | **Line chart** (single series, optional dashed prior-period overlay) | Default-correct. Avoid "MRR by month" as a bar chart — bars over time misrepresent continuity. |
| 2. Conversion rate by traffic source | Compare across categories with potentially long labels (`organic-search`, `paid-social`, `direct`, `referral-partner`) | **Horizontal bar** | The AI default would be a pie chart; humans can't compare slice areas, and source labels overflow vertical bar labels. Horizontal fits the labels and lets us sort descending by conversion rate. |
| 3. Cohort retention heatmap | Two-dimensional matrix (cohort month × months since signup) with ordered intensity (% retained) | **Heatmap with Viridis** (or Cividis specifically — designed for colour-blind viewers) | Heatmap is the only chart shape that fits this data. Viridis is perceptually uniform: equal steps in retention map to equal steps in perceived colour. Don't use a diverging palette here — retention has a one-direction intensity (high is good), not a meaningful midpoint. |
| 4. Top 10 customers by MRR | Ranked list of named entities with multiple per-row attributes (name, MRR, plan, tenure, trend) | **Table tile** (sortable header, tabular numerics on MRR, optional sparkline column for 6-month trend) | Could be a horizontal bar chart, but for "top customers" the user usually wants the names *and* the numbers *and* secondary attributes, which only a table delivers. |

**Avoid** (per § Anti-patterns and the AI tells in SKILL): no pie chart for source mix, no 3D, no dual y-axes, no donut KPI, no red-green-only state coding, no "Nothing here yet" empty states. Status / delta indicators always pair colour with shape (`↑` `↓` arrows, `+` / `−` signs).

**Page layout** (per `layout-patterns.md` § Dashboard layouts and `data-viz.md` § Dashboard tile shapes):

- Sidebar + main shell. Sidebar = 240px, main = scrollable.
- Inside main, two rows:
  - **Row A:** MRR trend line chart (60% width, ~720px) + Conversion-by-source horizontal bar chart (40% width, ~480px). Both 320px tall.
  - **Row B:** Cohort retention heatmap (60% width) + Top 10 customers table (40% width). Both ~440px tall.
- 32px page padding, 24px row gap, 16px tile gap.
- Above Row A: a slim filter bar (date range picker, segment selector). Mentioned but not built in this pass unless the user asks — keeps the call under 25 ops.

**Frame name.** `Dashboard_Analytics` (PascalCase, semantic, role-bearing — per the Naming discipline rule).

**Components I'll instantiate vs build from primitives.** Assuming the inventory in step 3 surfaces them: `Sidebar`, `ChartTile`, `TableTile` as `ref` nodes. If `ChartTile` doesn't exist, I'll build a minimal `ChartFrame` (header + body) inline and surface to the user that this should be extracted to the library. I'd never silently rebuild a Button or Badge from primitives.

I'd state this plan to the user (2–3 sentences) before any `batch_design` call. Concretely:

> *"Adding a `Dashboard_Analytics` frame to your canvas with sidebar + main. Two rows of two tiles: MRR trend (line) + Conversion by source (horizontal bar) on top, Cohort heatmap (Viridis) + Top 10 customers (table with MRR sparkline) below. All chart series use Okabe-Ito or Viridis tokens for colour-blind safety. I'm using your `ChartTile` and `TableTile` reusables from the imported library; pause me if you'd rather I build a custom variant."*

## Step 5 — Execute (find space, then batch_design)

```
find_empty_space_on_canvas({ width: 1440, height: 1100 })
```

The canvas almost certainly has other top-level frames already. This call returns `{ x, y }` for a region that doesn't overlap. I'd pass those coordinates on the outermost frame in the next call. Skipping this on a populated canvas produces invisible overlaps — that's specifically called out in the "Adding frames to a populated canvas" branch of the workflow.

Then one `batch_design` call. Approximately 18–22 ops, well under the 25-op ceiling.

```
dash=I(document, {
  type: "frame", name: "Dashboard_Analytics", placeholder: true,
  context: "Main analytics dashboard. Sidebar + main; KPI-less by user request. Two rows: (Row A) MRR trend line + Conversion-by-source horizontal bar; (Row B) Cohort retention heatmap (Viridis, perceptually uniform, colour-blind-safe) + Top 10 customers table. All chart series use Okabe-Ito ($chart1..$chart8) or Viridis ($viridis050..$viridis950) tokens. Loading: skeleton with axis hints per tile. Partial-failure: a tile that errors shows inline retry; the rest of the dashboard renders normally. Filter bar (date range, segment) referenced in design but not yet built — add when product confirms scope.",
  size: { width: 1440, height: 1100 }, x: <fromFindEmptySpace>, y: <fromFindEmptySpace>,
  layout: { direction: "row", gap: 0 }
})
sidebar=I(dash, { type: "ref", ref: "Sidebar", descendants: { active: { content: "Analytics" } }, name: "DashSidebar" })
main=I(dash, { type: "frame", name: "Main", width: "fill_container",
  layout: { direction: "column", padding: 32, gap: 24 } })

rowA=I(main, { type: "frame", name: "RowA_TrendsAndConversion",
  width: "fill_container", layout: { direction: "row", gap: 16 } })

trendTile=I(rowA, {
  type: "frame", name: "ChartTile_MRRTrend",
  context: "Line chart, MRR over the last 12 months. Single solid series in $chart6 (Okabe-Ito Blue). Optional dashed prior-period overlay in $textMuted when comparison toggle on. Y-axis starts at zero (MRR is a magnitude, truncating distorts comparison). Direct label at the line endpoint — no separate legend needed for single-series. Tabular numerics on axis labels and tooltip. Skeleton with axis hints during load (better than a spinner; tells the user the chart's shape).",
  width: "fill_container(720)", layout: { direction: "column", padding: 24, gap: 16 }
})
trendHeader=I(trendTile, { type: "frame", name: "Header", layout: { direction: "row", gap: 8 } })
I(trendHeader, { type: "text", name: "Title", content: "MRR trend",
  fontFamily: "$fontDisplay", fontWeight: "$fontWeightSemibold", fontSize: "$textLg" })
I(trendHeader, { type: "text", name: "Subtitle", content: "Last 12 months",
  fontFamily: "$fontBody", color: "$textMuted", fontSize: "$textSm" })
I(trendTile, { type: "ref", ref: "ChartTile",
  descendants: { chartType: { content: "line" }, series: { content: "<bind: mrr.last12months>" }, colour: { content: "$chart6" } } })

convTile=I(rowA, {
  type: "frame", name: "ChartTile_ConversionBySource",
  context: "Horizontal bar chart, top 8 traffic sources by conversion rate (descending). Bars in $chart2 (Okabe-Ito Orange) — single colour because the dimension being compared is rate, not category identity. Source names on Y axis (long labels — that's why horizontal, not vertical). Value labels at the right end of each bar (per data-viz.md: direct labels beat tooltips when space allows). Sort descending by default; user can toggle to alphabetical via the chart's footer chip.",
  width: "fill_container(480)", layout: { direction: "column", padding: 24, gap: 16 }
})
I(convTile, { type: "ref", ref: "ChartTile",
  descendants: { chartType: { content: "barHorizontal" }, series: { content: "<bind: conversion.bySource.top8>" }, colour: { content: "$chart2" } } })

rowB=I(main, { type: "frame", name: "RowB_CohortAndCustomers",
  width: "fill_container", layout: { direction: "row", gap: 16 } })

cohortTile=I(rowB, {
  type: "frame", name: "ChartTile_CohortRetention",
  context: "Cohort retention heatmap. Y axis: signup cohort (month). X axis: months since signup (0..11). Cell value: % of cohort still active. Viridis sequential colour scale (perceptually uniform; equal data steps map to equal perceived colour steps; colour-blind-safe). Sequential is correct — not diverging — because retention has a one-direction intensity (higher is better), not a meaningful midpoint. Cell labels show % directly (no tooltip-only); pair colour with text per data-viz.md § Pairing colour with shape.",
  width: "fill_container(720)", layout: { direction: "column", padding: 24, gap: 16 }
})
I(cohortTile, { type: "ref", ref: "ChartTile",
  descendants: { chartType: { content: "heatmap" }, colourScale: { content: "viridis" }, data: { content: "<bind: cohort.retentionMatrix>" } } })

topCustTile=I(rowB, {
  type: "frame", name: "TableTile_TopCustomers",
  context: "Top 10 customers by MRR (descending). Columns: Customer, Plan, MRR, Tenure (months), Trend (sparkline, last 6 months). Tabular numerics on MRR and Tenure (font-variant-numeric: tabular-nums) so numbers align by column width — without this, proportional digits create visible jitter. Sparkline endpoint marker emphasises 'now'. Sort by MRR descending by default; sortable header. Pair growth/decline indicators with arrow shape (↑ / ↓) so colour-blind users get the signal. Plan column shows a subtle pill (use Badge component); MRR right-aligned per fintech/SaaS table conventions.",
  width: "fill_container(480)", layout: { direction: "column", padding: 24, gap: 16 }
})
I(topCustTile, { type: "ref", ref: "TableTile",
  descendants: { columns: { content: "Customer,Plan,MRR,Tenure,Trend" }, rows: { content: "<bind: customers.topByMRR.10>" } } })

U("dash", { placeholder: false })
```

Notes on the ops above:

- `placeholder: true` on the outer frame the moment it's created and `placeholder: false` at the end of the same call — per `references/batch-design-grammar.md` § Placeholder frames.
- Every frame has a meaningful `name` and the substantive ones have a `context` annotating *intent and behaviour* (data source, palette token, axis baseline, sort default, accessibility pairing) — never spacing or colour duplicates that `batch_get` could re-derive.
- `width: "fill_container(720)"` uses the bare-string with fallback form. Never `"100%"`, never the older `{ sizing: ... }` object — both are common schema errors per failure mode 6.
- All chart colours are bound to tokens (`$chart6`, `$chart2`, `$viridis*`) rather than raw hex, so theme-axis behaviour and downstream palette swaps stay safe. This also means I don't need a second screenshot in dark mode — the variable system guarantees the swap (per the dual-mode rule in workflow step 6).
- IDs (`dash`, `trendTile`, `cohortTile`, etc.) contain no `/`. The schema rejects `/` in `id`; it's allowed only in `name` for hierarchical flow paths.

**If `ChartTile` / `TableTile` / `Sidebar` aren't in the inventory.** I'd surface that to the user before this call: *"Your library doesn't have `ChartTile` / `TableTile` yet. I can either (a) build a minimal `ChartFrame` inline for this dashboard now and you extract it later, or (b) author them into your `.lib.pen` first so this dashboard and future ones share the same component. Which?"* I would not silently rebuild reusables.

## Step 6 — Verify (structural-first, one screenshot at most)

Walk the verification ladder, stopping at the cheapest rung that answers the question:

1. **`batch_design` response.** Confirms ops succeeded and returns the assigned ids for `dash`, `main`, `trendTile`, `convTile`, `cohortTile`, `topCustTile`, etc. Free.
2. **`snapshot_layout({ nodeId: "<dash>", maxDepth: 3 })`.** Confirms the structural intent landed: the outer frame is 1440 × 1100 at the empty-space coordinate; `Main` fills container width with 32px padding; `RowA` and `RowB` are `direction: row` with 16px gap; tile widths split 720/480; tile heights both 320 (Row A) and ~440 (Row B). Returns positions/sizes/gaps as numbers — perfect for "did the gap land at 16px? are the rows actually side-by-side?". Cheap.
3. **`batch_get({ nodeIds: ["<trendTile>", "<convTile>", "<cohortTile>", "<topCustTile>"] })`.** Confirms property-level intent: each tile's `ref` resolved to the right component id, the `descendants` overrides bound the right tokens (`$chart6`, `$chart2`, `viridis`), the `context` strings persisted, names match what I authored. Cheap.
4. **`get_screenshot({ nodeId: "<dash>" })` — once, scoped to the dashboard frame, not the whole canvas.** This is the only expensive call. I'd only reach for it for: chart-text contrast under real rendering, sparkline endpoint visibility in the table cells, the cohort heatmap actually using Viridis (not a stand-in palette), and the rhythm of the two rows reading right at full canvas. Anything visible *only* via pixels.

**Dual-mode rule.** I screenshot the primary mode only (likely `light`, since SaaS analytics defaults to light unless the project commits dark-first). Because every chart colour resolves through a variable that has both light and dark values, the variable system guarantees the swap — re-screenshotting in dark mode "just to check" would burn tokens to confirm something the structural snapshot already proved. I'd only re-screenshot in dark mode if step 3's `batch_get` revealed a raw hex slipped in somewhere.

**What I'd scan in the screenshot, in order** (per the verification-ladder checklist):

1. Layout integrity — both rows hold side-by-side at 1440 wide; no tile overflowing or off-canvas; sidebar 240px and main scrollable.
2. Spacing rhythm — 32px page padding, 24px row gap, 16px tile gap, all match `tokens.md`.
3. Type rhythm — tile titles at `$textLg`, subtitles at `$textSm` `$textMuted`, body labels legible at the rendered size.
4. Contrast — body text passes WCAG AA (4.5:1) against tile background; small chart-axis labels pass too.
5. Component fidelity — tiles are `ref`s to library components, not hand-built drift-prone lookalikes.
6. Chart-specific: line chart Y-axis starts at zero; horizontal bar sorted descending with right-end value labels; cohort heatmap visibly Viridis (yellow at high retention, deep purple at low); top-customers MRR column right-aligned and tabular-aligned across rows.

## Step 7 — Self-critique gate (60 seconds)

Per the four-question gate in SKILL § Self-critique gate:

1. **Could a non-designer recognise this as analytics for a SaaS product?** Yes — chart-forward, number-first, two rows of two tiles, no marketing flourish. The atmosphere commitment ("dense, symmetric, static") is honoured.
2. **Where does the eye go first / second / third?** First: the MRR trend line (largest visual mass, top-left, the primary metric). Second: the conversion bars (top-right, sorted descending — the eye lands on the longest bar). Third: the cohort heatmap (visual texture pulls the eye second-row). The customers table is a deliberate fourth — text-dense, intentional read-stop. This matches the priority of an analytics dashboard.
3. **What's decorative-only?** Nothing. No brand gradient, no decorative iconography, no "stats" filler. Each tile carries information.
4. **What single change would make this less AI-generated?** The most common pull would be: drop the assumption that all four tiles have to share equal visual weight. If MRR is genuinely the headline metric (which it is for most SaaS), the trend line tile could span the full top row width and push the conversion chart to row B. I'd flag this to the user: *"If MRR is the headline metric, want me to give it the full top row instead of splitting with conversion?"* — but I would not unilaterally apply it; the prompt asked for four equal tiles.

**Accessibility checks** (the five non-negotiables from SKILL § Accessibility):

1. Contrast: chart-axis labels and body text against tile background ≥ 4.5:1 in both light and dark; tile borders ≥ 3:1 against page background.
2. Hit targets: any sortable header / chip / row-action ≥ 44 × 44.
3. Colour is never the only signal: cohort cells show % numerically *and* by Viridis intensity; top-customers trend uses arrow shape paired with `$success` / `$danger`; all chart series have direct labels (no legend-only).
4. Names map to roles: `ChartTile_MRRTrend`, `ChartTile_CohortRetention`, `TableTile_TopCustomers` are role-bearing (the first agent or developer reading this knows what each frame *is*).
5. Component states cover keyboard focus: `ChartTile` and `TableTile` reusables already define hover / focus / disabled states (I'd verify this in the inventory; if not, that's a library bug to surface before shipping).

## Step 8 — Hand back

A one-paragraph summary along the lines of:

> *"Added `Dashboard_Analytics` to your canvas: sidebar + main, two rows of two tiles. MRR trend as a single-series line in `$chart6`; Conversion by source as a horizontal bar in `$chart2`; Cohort retention as a Viridis heatmap (perceptually uniform, colour-blind-safe); Top 10 customers as a sortable table with MRR-trend sparklines. All chart series bound to tokens (`$chart1..$chart8`, `$viridis*`) so light/dark and palette swaps are free. Y-axis starts at zero on the trend; bars sorted descending; cells show % directly so colour isn't the only signal. Loading: skeleton with axis hints per tile. Partial-failure noted in the dashboard's `context` so a single tile error doesn't black out the whole view. Want me to add a filter bar (date range, segment) above Row A as a follow-up?"*

If the project lacked `ChartTile` / `TableTile` reusables, the summary would also surface the extraction recommendation rather than treating the inline build as final.

## What I deliberately did *not* do

- **Did not add a KPI row** (Revenue / MRR / Active users / Churn cards across the top). The prompt asked for four specific tiles, and adding a fifth row would be gold-plating. If MRR-as-a-number is genuinely useful at the top, I'd ask first.
- **Did not commit a chart palette to `tokens.md`**. The Components-first / read-before-write discipline says I check the project's existing tokens first. If `data-viz.md` already names a palette, I use it; if not, I'd offer to commit Okabe-Ito categorical + Viridis sequential and update `tokens.md` accordingly — but I'd ask once, not assume.
- **Did not screenshot in dark mode preemptively.** Variable-bound colours guarantee the swap; re-screenshotting just to confirm is wasted tokens (per the dual-mode rule).
- **Did not load `forms.md`, `mobile-patterns.md`, `flows.md`, `iconography.md`, `style-catalogue.md`, `colour-palettes.md`, or `font-pairings.md`.** None is on the critical path for a four-tile static analytics dashboard. The skill's "load on demand" architecture exists exactly so I can stay focused.
