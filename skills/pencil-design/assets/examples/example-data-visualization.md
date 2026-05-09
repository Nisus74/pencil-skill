# Example: design a multi-chart dashboard with colour-blind-safe palettes

User says:

> *"Build the analytics dashboard. Show revenue by month, conversion by channel, churn cohort heatmap, and top customers. Use a colour-blind-safe palette."*

This example shows the agent picking the right chart per data shape, applying a colour-blind-safe palette, and designing the dashboard with proper hierarchy.

---

## Step 1: Read context

```js
get_editor_state();
```

The agent reads `assets/design-system/visual-style.md`, `tokens.md`, and `data-viz.md` (the project's chart palette and library commitments). Loads `references/data-viz.md` (the 25-chart selection matrix and the Okabe-Ito / ColorBrewer / Viridis palettes) and `references/layout-patterns.md` § Dashboard layouts.

## Step 2: Pick the chart per data shape

Per `references/data-viz.md` § The 25-chart selection matrix:

| Metric | Data shape | Chart pick | Why |
|---|---|---|---|
| Revenue by month | One series over time | Line chart | Trend over time |
| Conversion by channel | Compare across categories | Horizontal bar | Channel names are long; horizontal fits the labels |
| Churn cohort | Two-dimensional (cohort × month) | Heatmap | Two-dimensional density matrix |
| Top customers | Ranked list | Horizontal bar | Top 10 with sortable header |

Avoid the AI defaults: no pie chart for channels (use bar; humans can't compare slice areas); no 3D anywhere; no dual y-axes if revenue and conversion go on one chart (split into small multiples).

## Step 3: Pick the colour-blind-safe palette

Per `references/data-viz.md` § Colour-blind-safe palettes, three families:

- **Okabe-Ito** (8 colours): for categorical chart series.
- **ColorBrewer Sequential / Diverging**: for ordered data (heatmaps).
- **Viridis**: for continuous, perceptually uniform.

The project commits in `assets/design-system/data-viz.md`. For this example: Okabe-Ito for categorical (bar charts, line series), Viridis for the cohort heatmap.

The agent commits the chart palette tokens in `tokens.md`:

```
$chart1: #000000 (Black)
$chart2: #E69F00 (Orange)
$chart3: #56B4E9 (Sky Blue)
$chart4: #009E73 (Bluish Green)
$chart5: #F0E442 (Yellow)
$chart6: #0072B2 (Blue)
$chart7: #D55E00 (Vermilion)
$chart8: #CC79A7 (Reddish Purple)
```

And calls `set_variables` to mirror them into the `.pen` file's `variables`.

## Step 4: Plan the dashboard layout

Three rows:

- **Row 1 (KPIs)**: 4 KPI cards across (Revenue, Conversions, Churn, Top customer). Per `references/data-viz.md` § Dashboard tile shapes.
- **Row 2 (charts)**: 2 chart tiles across (Revenue by month line chart; Conversion by channel horizontal bar).
- **Row 3 (chart + table)**: heatmap (left, 60% width) + Top customers table (right, 40% width).

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<canvas-root-id>",
      node: {
        type: "frame",
        name: "Dashboard_Analytics",
        context: "Analytics dashboard. Three rows: KPIs (4 cards), charts (2 tiles), heatmap + table (split). Uses Okabe-Ito for categorical and Viridis for the cohort heatmap. All charts colour-blind-safe; state coding pairs colour with shape.",
        layout: { direction: "column", padding: 32, gap: 24 },
        children: [
          { type: "frame", name: "Row_KPIs", layout: { direction: "row", gap: 16 } },
          { type: "frame", name: "Row_Charts", layout: { direction: "row", gap: 16 } },
          { type: "frame", name: "Row_HeatmapAndTable", layout: { direction: "row", gap: 16 } },
        ],
      },
    },
  ],
});
```

## Step 5: Build the line chart (revenue by month)

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<row-charts-id>",
      node: {
        type: "frame",
        name: "ChartTile_RevenueByMonth",
        context: "Line chart, monthly revenue, 12-month rolling window. Single series (current period in $chart6 / Blue). Y-axis starts at zero; gridlines on the value axis only. Direct label at the line endpoint. Skeleton with axis hints during load.",
        children: [
          { type: "ref", componentId: "ChartTile", descendants: { title: "Revenue by month", chartType: "line", series: "<data>", colour: "$chart6" } },
        ],
      },
    },
  ],
});
```

## Step 6: Build the horizontal bar chart (conversion by channel)

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<row-charts-id>",
      node: {
        type: "frame",
        name: "ChartTile_ConversionByChannel",
        context: "Horizontal bar chart, top 8 channels by conversion. Channel names on the Y axis (long labels). Bars in $chart2 / Orange (Okabe-Ito). Sort descending by default. Value labels at the right end of each bar.",
        children: [
          { type: "ref", componentId: "ChartTile", descendants: { title: "Conversion by channel", chartType: "barHorizontal", series: "<data>", colour: "$chart2" } },
        ],
      },
    },
  ],
});
```

## Step 7: Build the heatmap (churn cohort)

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<row-heatmap-id>",
      node: {
        type: "frame",
        name: "ChartTile_ChurnCohort",
        context: "Cohort heatmap. Y axis: cohort (signup month). X axis: months since signup. Cell value: % of cohort still active. Viridis sequential colour scale (perceptually uniform, colour-blind-safe). Diverging value not appropriate; sequential right.",
        children: [
          { type: "ref", componentId: "ChartTile", descendants: { title: "Churn cohort", chartType: "heatmap", colourScale: "viridis", data: "<matrix>" } },
        ],
      },
    },
  ],
});
```

## Step 8: Build the top customers table

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<row-table-id>",
      node: {
        type: "frame",
        name: "TableTile_TopCustomers",
        context: "Top 10 customers by MRR. Columns: Customer, MRR, Tenure, Status. Sort by MRR descending by default. Tabular numerics on MRR column. Sparkline column shows MRR trend (last 6 months).",
        children: [
          { type: "ref", componentId: "TableTile", descendants: { columns: "<spec>", rows: "<data>", virtualised: true } },
        ],
      },
    },
  ],
});
```

## Step 9: Default chart styling

Per `references/data-viz.md` § Default chart styling:

- Y-axis starts at zero on bar charts (truncated y-axis distorts comparison).
- Gridlines only on the value axis, light weight (`$borderMuted`).
- Direct labels at line endpoints (no separate legend for single-series charts).
- Tabular numerics on all monetary values.
- Number format with locale (`$1,234` for en-US; `1.234 €` for de-DE; document the locale in `tokens.md`).

## Step 10: Pair colour with shape

State coding (e.g. growth vs decline, success vs failure) never relies on colour alone. Per `references/data-viz.md` § Pairing colour with shape:

- Up arrow `↑` paired with `$success` colour for growth.
- Down arrow `↓` paired with `$danger` colour for decline.
- Solid line for current period; dashed line for prior period.

Document each pairing in the relevant component's `context`.

## Step 11: Loading and empty states

Per `references/data-viz.md` § Loading states for charts:

- Skeleton with axis hints during chart load (better than a spinner; tells the user the shape).
- Empty state per chart (per `assets/design-system/empty-states.md` § Search results style: name what's empty, suggest refinements).

## Step 12: Verify with one screenshot

```js
get_screenshot({ documentId, nodeId: "<dashboard-frame-id>" });
get_screenshot({ documentId, nodeId: "<dashboard-frame-id>", theme: { mode: "dark" } });
```

Confirm:
- All charts use Okabe-Ito or Viridis (colour-blind-safe).
- No pie charts, no 3D, no dual y-axes.
- Y-axis starts at zero on bar chart.
- Heatmap uses sequential Viridis (correct for ordered data).
- State coding pairs colour with shape.
- Loading skeletons match chart shapes.

Run a colour-blind simulator (Stark, Sim Daltonism, Chrome DevTools Vision Deficiencies) to verify all chart series remain distinguishable for deuteranopia and protanopia.

## See also

- `references/data-viz.md`: 25-chart selection matrix, colour-blind-safe palettes, dashboard tile shapes.
- `references/layout-patterns.md` § Dashboard layouts.
- `references/states.md` § Loading taxonomy.
- `assets/design-system/data-viz.md`: project's chart palette and library commitments.
- `assets/examples/example-dashboard.md`: simpler dashboard example.
- `assets/design-system/tokens.md`: chart palette tokens (`$chart1` through `$chart8`).
