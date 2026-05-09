# Data visualisation

How to pick the right chart for the shape of the data, how to colour charts so they read for everyone, and how to lay out dashboards that make the numbers findable. Most AI-generated dashboards default to bar + line + pie regardless of what the data actually says, then colour-code with red and green and ship colour-blind-broken charts. This file gives the agent a 25-chart selection matrix and a colour-blind-safe palette set drawn from established sources.

**What this file owns:** the 25-chart selection matrix (data shape → ideal chart → failure mode), colour-blind-safe palette recommendations, dashboard tile shapes (KPI / chart / table), default chart styling rules, and chart anti-patterns.

**What this file does NOT own:** the project's *committed* chart palette. That lives in `assets/design-system/data-viz.md` (when populated) or `assets/design-system/tokens.md`. General colour theory is in [`colour-palettes.md`](colour-palettes.md). Dashboard layout patterns (sidebar / top nav / three-column) are in [`layout-patterns.md`](layout-patterns.md). Performance for chart rendering is in [`performance-design.md`](performance-design.md).

## When to load this file

- The agent is designing a dashboard, KPI card, chart tile, sparkline, or any data visualisation.
- The user names a chart type ('bar', 'line', 'pie', 'sankey') or a data shape ('compare across categories', 'over time', 'distribution').
- The agent needs colour-blind-safe palettes for state coding or chart series.
- The agent is auditing an existing chart for the common failure modes (3D, pie > 5 slices, dual y-axes, red-green only).

## The 25-chart selection matrix

Pick by the *shape* of the data, not by the chart that's familiar. Each row: chart, data shape, ideal use case, failure mode, alternative when this chart fails.

| Chart | Data shape | Ideal use case | Failure mode | Alternative |
|---|---|---|---|---|
| **Sparkline** | One series over time, no axis needed | Inline trend within a number ('+12% ↗') in tables, KPI cards, list rows | Reading exact values impossible | Bar (when exact values matter) |
| **Big-number** | Single value, possibly with delta | KPI cards: 'Revenue $1.2M ↗ +14%' | No context (vs target? vs last period?) | Add subtitle with context, or pair with sparkline |
| **Bar (vertical)** | Compare across categories | Revenue by region, conversions by channel | Too many bars (> 12) becomes unreadable | Horizontal bar (longer category names), or grouped/stacked |
| **Bar (horizontal)** | Compare across categories with long labels | Top 10 customers, ranked lists | Same overflow issue | Truncate to top N, link to full table |
| **Stacked bar** | Compare totals AND composition across categories | Revenue by region (stacked by product line) | Hard to compare individual segments across bars | Grouped bar (compare segments) or 100% stacked (compare proportions) |
| **Grouped bar** | Compare segments side-by-side across categories | Q1 vs Q2 revenue per region | Visual clutter when > 3 groups per category | Small multiples (one chart per group) |
| **100% stacked bar** | Compare proportions (not totals) across categories | Market share by region (each bar sums to 100%) | Hides absolute values | Pair with a totals table |
| **Line** | One or more series over time | Revenue trend, user growth, latency over time | Too many series (> 5) becomes spaghetti | Small multiples (one line per series) |
| **Area** | Cumulative trend over time | Total signups over time (cumulative) | Hides individual periods | Line + bar combo |
| **Stacked area** | Composition trend over time | Revenue by product line over time | Hard to read non-bottom series | 100% stacked area or small multiples |
| **Scatter** | Correlation between two variables | Spend vs conversion per campaign | Overplotting at high density | Heatmap (density) or hexbin |
| **Bubble** | Three variables (X, Y, size) | Customers plotted by spend (X), tenure (Y), MRR (bubble size) | Bubble area is hard to compare visually; circular bias | Sort by size dimension, use bar chart |
| **Heatmap** | Two-dimensional density or matrix values | Calendar (day × hour activity), correlation matrix, A/B test results | Diverging values without diverging palette | Use diverging colour scale; flag absolute zero |
| **Treemap** | Hierarchical part-to-whole | File sizes by directory, market share by category-and-subcategory | Hard to compare sibling rectangles by area | Sunburst or horizontal bar |
| **Sankey** | Flow between categories (cause → effect) | User funnel (visit → signup → activation → paid), traffic sources to outcomes | Visually busy with > 5 source/sink nodes | Funnel chart (linear flow) |
| **Funnel** | Linear conversion sequence | Marketing funnel: visit → trial → paid | Misrepresents drop-off when bars are equal-width | Use proportional widths or pair with conversion rates |
| **Radar / spider** | Multiple metrics for one or two entities | Performance scoring across 5-7 dimensions | Hard to compare > 2 entities; area distortion | Bar chart per dimension, small multiples |
| **Gauge / dial** | Single value within a range | KPI vs target ('80% of monthly target') | Ink-to-data ratio is poor | Big-number with progress bar |
| **Progress** | Linear progress toward a target | Plan limit usage ('72 of 100 seats used') | Just a bar; nothing fancy needed | Big-number + horizontal bar |
| **Candlestick** | Open / high / low / close per period | Stock charts, forex, OHLC time series | Industry-specific; outside finance, OHLC isn't the right shape | Line + range bands |
| **Boxplot** | Distribution summary (quartiles, median, outliers) | Latency distribution per service, salary by role | Reading takes training; not for general audiences | Histogram or violin plot |
| **Histogram** | Distribution of a single variable | Response time distribution, age distribution | Bin width affects shape; defaults often misleading | Density plot or violin |
| **Chord** | Bidirectional flows between same set of entities | Migration between regions, communication between teams | Hard to read with > 8 entities | Heatmap (matrix view) |
| **Ridgeline** | Distribution comparison across categories | Sales distribution per month over a year | Vertical space limits how many categories | Boxplot per category, small multiples |
| **Network / graph** | Entities and relationships | Org charts, social graph, system dependencies | Force-directed layouts unstable across renders | Hierarchical layout, sankey for flows |
| **Choropleth (map)** | Geographic data | Sales by country, election results | Visual area bias (Russia looks bigger than it economically is) | Tile cartogram or value-coded list |

**Decision shortcuts:**

- Comparing categories? Bar chart.
- Trend over time? Line chart.
- Composition? Stacked bar (absolute) or 100% stacked bar (proportion).
- Distribution? Histogram or boxplot.
- Correlation? Scatter (or heatmap if dense).
- Flow? Sankey (multi-step) or funnel (linear).
- Single value? Big-number (with delta and context).
- Inline trend? Sparkline.

## Charts to avoid (almost always)

- **3D charts.** Distortion, not insight. The third dimension hides the data behind the foreground bars/slices.
- **Pie charts with > 5 slices.** Humans can't compare slice areas accurately. Use a horizontal bar instead.
- **Donut charts as KPI replacement.** A KPI card with a donut showing 'progress to goal' is bigger than the number. Use a big-number with a horizontal progress bar.
- **Dual y-axes.** Almost always misleading. The two axes can be scaled to show any correlation. Use small multiples (two charts side-by-side, each with its own axis).
- **Word clouds.** Reading is by font size; the eye can't compare. Use a horizontal bar chart of frequencies.
- **Stacked area with > 5 series.** The lower series dominate; the upper series are unreadable.
- **Polar area / Nightingale rose.** Florence Nightingale's invention was great for one specific historical purpose; modern data doesn't need it.

## Colour-blind-safe palettes

Roughly 8% of male users and 0.5% of female users have some form of colour-blindness (most commonly red-green). A chart that codes by colour alone fails for them. Two safe palette families are widely used.

### Okabe-Ito (8 colours, distinguishable across all common colour-blind types)

- Black `#000000`
- Orange `#E69F00`
- Sky Blue `#56B4E9`
- Bluish Green `#009E73`
- Yellow `#F0E442`
- Blue `#0072B2`
- Vermilion `#D55E00`
- Reddish Purple `#CC79A7`

Source: Masataka Okabe and Kei Ito, 2002 (https://jfly.uni-koeln.de/color/). Adopted by Nature Publishing, used in scientific publications. The agent commits these as semantic chart series tokens (`$chart1` through `$chart8`) in the project's `tokens.md`.

### ColorBrewer (sequential, diverging, qualitative; web-accessible)

- **Sequential** (one-direction intensity): use for ordered data (low → high). Examples: Blues, Greens, YlOrRd. Ideal for choropleth maps and heatmaps where the value direction matters.
- **Diverging** (two-direction from a centre): use for data with a meaningful midpoint (e.g., -100% to +100%, below/at/above target). Examples: RdBu, PiYG, BrBG. Pair with a clearly labelled midpoint.
- **Qualitative** (categorical, no order implied): use for unordered category coding. Examples: Set2, Paired. Most variants are colour-blind-safe; the catalogue at colorbrewer2.org flags which.

Source: Cynthia Brewer, ColorBrewer 2.0 (https://colorbrewer2.org). Open-source palettes designed for cartography, widely adopted in data visualisation libraries.

### Viridis (continuous, perceptually uniform)

For continuous data where ordered intensity matters (heatmaps, density plots). The Viridis family (Viridis, Magma, Plasma, Inferno, Cividis) is colour-blind-safe and perceptually uniform: equal steps in the data map to equal steps in perceived colour. Cividis is specifically designed for colour-blind viewers.

Source: Stéfan van der Walt, Nathaniel Smith (matplotlib), 2015. Adopted by matplotlib, ggplot2, D3.

### Pairing colour with shape

Colour alone fails for colour-blind users. Pair colour with at least one other coding:

- **Shape** for scatter/point markers (circle, square, triangle).
- **Pattern** for bar/area fills (solid, hatched, dotted).
- **Position** for ordered data (top-to-bottom in a stacked chart).
- **Text labels** directly on the chart (no separate legend key).

In financial contexts, the convention 'red = down, green = up' is so universal that abandoning it confuses users. Pair with shape (down arrow ↓, up arrow ↑) or sign (+/-) so the meaning persists for colour-blind users.

## Default chart styling

The chart's job is to surface data; the chart itself should fade. Most AI-default chart styling adds visual noise (gridlines on every line, legends in corners, axis labels at every tick).

**Axes:**

- Show only the axis lines that the data needs. The line at zero matters; the four-side box around the chart usually doesn't.
- Axis labels at sensible intervals (every 100, 1000, 10000), not at every tick.
- Format numbers with locale (1,234 in en-US; 1.234 in de-DE) and unit (`$1,234`, `12 ms`, `87%`).
- Y-axis usually starts at zero for bar charts (truncated y-axis distorts comparison). Line charts can start above zero when the variation matters more than the absolute value, but flag the truncation.

**Gridlines:**

- Light gridlines on the value axis (Y for vertical bar; X for horizontal bar) help the eye estimate values. Gridlines on the category axis usually don't.
- Default gridline weight: 1px, low-contrast colour (`$border` token; near `$border-muted`).

**Legend:**

- Place the legend close to the data, not in the corner. For line charts, label the lines directly at the right end (no legend needed).
- For categorical charts (bar, stacked bar), the legend goes above or to the side. Inline labels are better when space allows.

**Labels:**

- Direct labels beat tooltips when space allows. Tooltips hide information; labels show it.
- For bar charts, value labels above (or inside) the bars when the bars are tall enough to fit.
- For pie charts (in the rare cases they're used), label slices directly (avoid legend).

**Empty space:**

- Charts need padding around them, not just within the data area. The chart container has internal margin (≥ 16px) so the data doesn't touch the edges.

## Dashboard tile shapes

Three tile types compose most dashboards. Mixing them is fine; the layout decides which goes where.

- **KPI card.** A single big-number with optional subtitle (context), delta (change vs previous period), and sparkline (inline trend). Width varies; height typically 100-160px. Used for top-level metrics ('Revenue', 'MRR', 'Active users').
- **Chart tile.** A header (title + optional subtitle), the chart itself, optional footer (caption, legend, filter chip). Width varies; height typically 240-400px. Used for trends, comparisons, distributions.
- **Table tile.** Sortable header row, scrollable body rows, optional pagination. Width usually full-row; height varies. Used for raw data exploration, recent activity, top-N lists.

Layout shortcut: KPI cards in the top row (3 to 6 across); chart tiles in the middle (2 to 3 across); table tile at the bottom (full-width).

## Sparklines

Inline within text or table cells. Trend without scale.

- **Width:** matches the surrounding text or column width.
- **Height:** 16-24px (inline with body text), 32-48px (in table cells).
- **No axes.** A sparkline is an at-a-glance trend; if the user needs the value, the number sits next to the sparkline.
- **Single colour** matching the surrounding text or `$accent`.
- **Endpoint emphasis** (small dot at the latest value) helps the eye land on 'now'.

Use sparklines in:

- Big-number cards (next to the number).
- Tables (a 'Trend' column with a sparkline per row).
- List rows (showing each entity's recent activity).

## Loading states for charts

Charts often load over multiple seconds. Two patterns:

- **Skeleton with axis hints.** The chart container shows the axis frame, axis labels, and placeholder rectangles where data will render. Better than a spinner; tells the user the chart's shape before the data arrives.
- **Progressive reveal.** Render the axes first, then animate the data in (line drawing left-to-right, bars rising, scatter points fading in). 200-400ms total animation; cancellable on user interaction.

Per [`interactions.md`](interactions.md) § Loading states, don't show the loading state at all if the data arrives in < 150ms.

## Anti-patterns

- **3D anything.** Always wrong.
- **Pie chart with > 5 slices.** Use horizontal bar.
- **Donut KPI.** Use big-number + progress bar.
- **Dual y-axes.** Use small multiples.
- **Truncated y-axis without flag.** Either zero-baseline or label the truncation explicitly.
- **Red-green only state coding.** Pair with shape, position, or text.
- **Chart without context.** A 'Revenue' chart without 'vs target' or 'vs last period' is a number floating in space.
- **Spinner for chart load.** Use skeleton with axis hints.
- **Fancy animation that delays the data.** The user wants the number; flashy animation that delays it by 800ms is hostile.
- **Word cloud.** Reading is impossible by font-size comparison; use horizontal bar.
- **Stacked area with > 5 series.** Use small multiples.

## Pencil expression

Charts in `.pen` are slot-filled containers. The pattern:

- A `Chart` reusable component with slots for `header` (title), `body` (the chart itself), `footer` (caption, legend).
- A `KPICard` reusable with slots for `value` (big number), `label` (subtitle), `delta` (+/-%), `sparkline`.
- The chart-specific render (bar, line, area) lives in code, not `.pen` (unless designing the static visual reference). The `.pen` file shows the *shape* and *layout*; the engineer ships the rendering library (D3, Recharts, Chart.js, Vega-Lite).
- The `context` on a chart component documents: the data shape it expects, the colour palette tokens it uses (`$chart1` through `$chart8`), the recommended size range, the loading-state behaviour.

Example `context` for a bar-chart component: *'Renders a vertical bar chart. Expects an array of `{label: string, value: number}`. Uses `$chart1` for the bar fill. 240-400px height; 100% width within container. Skeleton with axis hints during load. Animation: bars rise from baseline over 300ms.'*

For the project's chart palette commitment (which Okabe-Ito or ColorBrewer scale is used), see `assets/design-system/data-viz.md` (when populated; an optional Tier 2 design-system template).

## Sources

- **Okabe-Ito (2002)**: Masataka Okabe and Kei Ito, 'Color Universal Design', https://jfly.uni-koeln.de/color/. The 8-colour palette adopted by Nature Publishing for colour-blind-safe scientific visualisation.
- **ColorBrewer 2.0**: Cynthia Brewer (Penn State), https://colorbrewer2.org. Sequential, diverging, qualitative palettes for cartography and data visualisation. Open-source.
- **Viridis colour map (2015)**: Stéfan van der Walt, Nathaniel Smith (matplotlib), https://bids.github.io/colormap/. Perceptually uniform, colour-blind-safe continuous palettes.
- **The Visual Display of Quantitative Information** (Edward Tufte): the foundational text on data visualisation. Ink-to-data ratio, chartjunk avoidance, sparkline invention.
- **Datawrapper**: https://www.datawrapper.de. Chart type selection guidance and accessibility-first defaults.
- **Observable**: https://observablehq.com. D3-based exemplars; the Plot API is a useful reference for the 25-chart vocabulary.
- **WCAG 2.2 (ISO/IEC 40500:2025)**: Success Criterion 1.4.1 (Use of Color) and 1.4.11 (Non-text Contrast) underpin the colour-blind safety guidance.
- **Real-product chart exemplars (accessed 2025/2026)**: Stripe Sigma (analytics dashboards), Linear Insights, Vercel Analytics, Google Analytics 4, Mixpanel, Amplitude, Bloomberg Terminal (web equivalent).
- **Apple HIG: Charts**: https://developer.apple.com/design/human-interface-guidelines/charts. Chart type selection and accessibility patterns.
- **Material 3: Charts**: chart anatomy and accessibility guidance.

## See also

- [`colour-palettes.md`](colour-palettes.md): general colour theory; this file inherits the two-role architecture.
- [`accessibility.md`](accessibility.md): WCAG 2.2 colour and non-text contrast requirements applied here.
- [`layout-patterns.md`](layout-patterns.md) § Dashboard layouts: where chart tiles live within the page.
- [`states.md`](states.md): loading and empty states for charts.
- [`performance-design.md`](performance-design.md): rendering performance for charts with > 1000 data points.
- [`interactions.md`](interactions.md): loading-state timing rules for chart loads.
- [`microcopy.md`](microcopy.md): chart titles, captions, and KPI label patterns.
- [`industry-patterns.md`](industry-patterns.md) § Fintech (trading), § SaaS (analytics), § Healthcare (clinical): industries where data-viz is dominant.
- [`assets/design-system/data-viz.md`](../assets/design-system/data-viz.md): the project's chart palette and library commitment (optional Tier 2 template).
- [`example-data-visualization.md`](../assets/examples/example-data-visualization.md): worked example of a multi-chart dashboard (Phase 4).
