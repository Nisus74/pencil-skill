# Example: design a dashboard with KPI cards, chart tile, and recent activity

User says:

> *"Design the main dashboard for our analytics SaaS. Show key metrics at the top, a trend chart in the middle, and recent activity below."*

This example shows the agent reading project context, picking the dashboard layout, building the three tile types (KPI, chart, table), and verifying with one screenshot.

---

## Step 1: Read context

```js
get_editor_state();
```

The agent reads `assets/design-system/visual-style.md` (style + palette + fonts), `tokens.md` (token values), `navigation.md` (project commits sidebar + main), and `data-viz.md` (project's chart palette and library commitments).

Loads `references/layout-patterns.md` § Dashboard layouts and `references/data-viz.md` (the 25-chart selection matrix and tile shapes).

## Step 2: Pick the layout

Per `references/layout-patterns.md` § Dashboard layouts, four shapes:

- **Sidebar + main** (default for B2B SaaS).
- **Top nav + content** (lighter chrome).
- **Three-column** (nav / list / detail).
- **Command-driven**.

The project commits sidebar + main in `navigation.md`. Use that.

Layout shortcut for dashboards (per `references/data-viz.md` § Dashboard tile shapes):
- KPI cards in the top row (3 to 6 across).
- Chart tiles in the middle (2 to 3 across).
- Table tile at the bottom (full-width).

## Step 3: Find canvas space and create the outer frame

```js
find_empty_space_on_canvas({ documentId, width: 1440, height: 900 });
```

The MCP returns a position. Use it for the new top-level frame.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<canvas-root-id>",
      node: {
        type: "frame",
        name: "Dashboard",
        context: "Main dashboard route. Sidebar nav (left, 240px) + main content (right, scrollable). KPI row at top, chart tile mid-page, recent-activity table at the bottom.",
        size: { width: 1440, height: 900 },
        layout: { direction: "row" },
        children: [
          { type: "ref", componentId: "Sidebar", descendants: { "active": "Dashboard" } },
          { type: "frame", name: "Main", layout: { direction: "column", padding: 32, gap: 24 }, children: [] }
        ],
      },
    },
  ],
});
```

## Step 4: KPI cards (top row)

Pick the metrics. For an analytics SaaS: Revenue, MRR, Active users, Churn. Four KPI cards across the top.

Each KPI uses the `KPICard` component from `design-system.lib.pen`. Anatomy per `references/data-viz.md` § Dashboard tile shapes:

- Big-number value
- Label (subtitle)
- Delta (vs previous period; arrow + percentage)
- Sparkline (inline trend)

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<main-id>",
      node: {
        type: "frame",
        name: "KPIRow",
        layout: { direction: "row", gap: 16 },
        children: [
          { type: "ref", componentId: "KPICard", descendants: { value: "$1.24M", label: "Revenue (MTD)", delta: "+14%", deltaDirection: "up", sparkline: "<series>" } },
          { type: "ref", componentId: "KPICard", descendants: { value: "$87K", label: "MRR", delta: "+5%", deltaDirection: "up", sparkline: "<series>" } },
          { type: "ref", componentId: "KPICard", descendants: { value: "12,847", label: "Active users", delta: "+8%", deltaDirection: "up", sparkline: "<series>" } },
          { type: "ref", componentId: "KPICard", descendants: { value: "2.1%", label: "Churn (30d)", delta: "-0.4%", deltaDirection: "down", sparkline: "<series>" } },
        ],
      },
    },
  ],
});
```

Use `tabular-nums` on the value (numbers align across cards). The delta colours pair with shape: `↑` for up, `↓` for down, plus `$success` / `$danger` colour. Don't rely on colour alone (per `references/data-viz.md` § Pairing colour with shape).

## Step 5: Chart tile (middle)

Pick the chart per `references/data-viz.md` § The 25-chart selection matrix:
- Trend over time? Line chart.
- One or more series? Up to 5 lines on one chart; small multiples beyond that.

Use a single line chart for monthly revenue trend. Optional second line for prior-period comparison.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<main-id>",
      node: {
        type: "frame",
        name: "ChartTile_Revenue",
        context: "Revenue trend, monthly. Line chart, 12-month rolling window. Two series: current period (solid, $accent) and prior period (dashed, $textMuted). Skeleton with axis hints during load. 320px height; 100% width.",
        layout: { direction: "column", padding: 24, gap: 16 },
        children: [
          { type: "frame", name: "Header", children: [
            { type: "text", name: "Title", text: "Revenue trend", fontFamily: "$fontDisplay", fontWeight: "$fontWeightSemiBold" },
            { type: "text", name: "Subtitle", text: "Last 12 months", fontFamily: "$fontBody", color: "$textSecondary" },
          ]},
          { type: "ref", componentId: "LineChart", descendants: { series: "<data>", colour: "$accent" } },
        ],
      },
    },
  ],
});
```

Default chart styling (per `references/data-viz.md` § Default chart styling): minimal axes, light gridlines on the value axis only, direct labels at the line ends, tabular numerics on values.

## Step 6: Recent activity table (bottom)

Use a `TableTile` component. Sortable headers, virtualised rows for long lists per `references/performance-design.md` § Virtualisation for long lists.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<main-id>",
      node: {
        type: "frame",
        name: "ActivityTable",
        context: "Recent activity, last 50 events. Columns: User, Action, Resource, Time. Sort by Time descending by default. Virtualised after 50 rows. Empty state when no activity.",
        children: [
          { type: "ref", componentId: "TableTile", descendants: { columns: "<spec>", rows: "<data>" } },
        ],
      },
    },
  ],
});
```

Time column uses absolute time on hover (relative time by default: '2 minutes ago'). Per `references/microcopy.md` § System status: 'Saved 2 minutes ago' beats 'Up to date'.

## Step 7: States to design

Per `references/states.md` § Component states matrix and § Loading taxonomy:
- KPI card skeleton (placeholder values + sparkline skeleton).
- Chart tile skeleton (axis hints + placeholder line).
- Activity table skeleton (5 rows of placeholder cells).
- Empty state per tile (per `assets/design-system/empty-states.md`).
- Error state per tile (inline retry; rest of the dashboard renders normally per `references/states.md` § Partial-failure).

## Step 8: Verify with one screenshot

```js
get_screenshot({ documentId, nodeId: "<dashboard-frame-id>" });
get_screenshot({ documentId, nodeId: "<dashboard-frame-id>", theme: { mode: "dark" } });
```

Confirm:
- KPI numbers tabular-aligned.
- Chart axis labels readable.
- Delta colour pairs with arrow shape.
- Sparkline endpoints visible.
- Recent activity table fits without horizontal scroll at default width.
- Empty / loading / error states designed (or noted as TODO in the project's Phase 1 of the design pass).

Hand back with one-paragraph summary.

## See also

- `references/layout-patterns.md` § Dashboard layouts: the four shapes and when to pick each.
- `references/data-viz.md`: the 25-chart selection matrix and dashboard tile shapes.
- `references/states.md` § Component states matrix and § Loading taxonomy.
- `references/microcopy.md` § System status: time-based copy.
- `references/performance-design.md` § Virtualisation: when to virtualise the activity table.
- `assets/examples/example-data-visualization.md`: deeper example of a multi-chart dashboard.
- `assets/design-system/data-viz.md`: project's chart palette commitments.
