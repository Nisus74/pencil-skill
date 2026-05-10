# Data viz

Charts and dashboards. **Delete this file if your project doesn't render charts**, it's noise for marketing-only sites.

The agent reads this when designing or generating a chart, sparkline, or dashboard tile. Without rules here, AI defaults to rainbow palettes, gridlines as loud as the data, and wildly inconsistent chart types. Decisions below pick a calm, scannable default. The *Archetype-keyed chart styles* section maps each shipped archetype to its chart treatment.

## Categorical palette

For up to 8 series. Each colour works in light AND dark, holds 3:1 contrast against `$surface` and `$surfaceMuted`, and is distinguishable for the most common colour-vision deficiencies.

| Variable | Light | Dark | Notes |
|----------|-------|------|-------|
| `$chart-1` | `<#hex>` | `<#hex>` | Primary series, usually the brand `$primary` if it works at this saturation. |
| `$chart-2` | `<#hex>` | `<#hex>` | |
| `$chart-3` | `<#hex>` | `<#hex>` | |
| `$chart-4` | `<#hex>` | `<#hex>` | |
| `$chart-5` | `<#hex>` | `<#hex>` | |
| `$chart-6` | `<#hex>` | `<#hex>` | |
| `$chart-7` | `<#hex>` | `<#hex>` | |
| `$chart-8` | `<#hex>` | `<#hex>` | |

**Rules:**

- **Don't use `$primary` for every chart.** It defeats the purpose of "primary == this is important." Reserve `$primary` for the focal series; rotate other chart colours otherwise.
- **No raw `#hex` in chart code.** Use the variables.
- **Charts with > 8 series:** group, filter, or switch to a different visualisation. Don't add `$chart-9, 10, 11`.
- **Colour-blind verification:** at least one in 12 men is colour-blind. Test the palette in a deuteranopia simulator before shipping.

## Sequential palette (heatmaps, density)

For ordered data (low to high). Single-hue, varying lightness/saturation.

| Variable | Light | Dark | Use |
|----------|-------|------|-----|
| `$chartSeq-50` | `<#hex>` | `<#hex>` | Lowest |
| `$chartSeq-300` | `<#hex>` | `<#hex>` | |
| `$chartSeq-500` | `<#hex>` | `<#hex>` | Mid |
| `$chartSeq-700` | `<#hex>` | `<#hex>` | |
| `$chartSeq-900` | `<#hex>` | `<#hex>` | Highest |

For diverging data (negative to positive), declare a separate diverging palette here when needed, anchored on a neutral middle.

## Chart type picker

The question the chart answers determines the type. Categories follow the Financial Times Visual Vocabulary taxonomy, enriched with guidance from Cole Nussbaumer Knaflic's *Storytelling with Data* chart guide. Pick the category, then the chart within it.

### Deviation: how far from a reference point?

Use when the story is the gap from zero, a target, or a baseline.

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Diverging bar | Values run positive and negative (revenue vs loss, net promoter score) | Axis at zero always. Colour positive/negative separately. Sort by one direction. |
| Diverging stacked bar | Survey results with agree/neutral/disagree buckets | Neutral in the centre, diverging outward. Two baselines make the top and bottom series easy to compare. |
| Surplus/deficit filled area | Running balance or cumulative delta over time | Shade above/below the baseline with two chart colours. Axis must be zero. |

### Correlation: do two variables move together?

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Scatter | Two continuous variables; finding clusters or outliers | Don't connect dots unless showing progression over time. Remove fitted trend lines in explanatory contexts . They add clutter when the trend is not obvious. Use opacity to handle overplotting. Label quadrants or notable outliers directly. |
| Bubble | Scatter where a third variable adds meaningful variation | Size by area, not radius. Only justified when all three variables matter and the size differences are visible. Cap at 4 dimensions or cognitive load breaks down. |
| Connected scatter | How two variables shifted together over time | Use directional arrows or labels to show time progression. |
| Line + column (dual axis) | One amount (bars) vs one rate (line) on the same time range | Use sparingly; dual axes mislead easily. Label both y-axes. |
| XY heatmap | Patterns between two categorical dimensions | Good for "time of day × day of week" request volume grids. |

### Ranking: what's the order?

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Ordered bar | Any ranking where label matters more than time | Sort descending (largest to smallest) unless there's a natural order. Horizontal when labels are long. Must start at zero. Gap between bars should be roughly 30–40% of bar width. |
| Ordered column | Ranking over a time axis | Sort by most recent period. |
| Lollipop | Ranking where values are spread wide and bar thickness adds nothing | Cleaner than bars at 15+ categories. Does not need to start at zero. |
| Slope | How ranks shifted between exactly two points in time | Two labelled columns connected by lines. Do not use when middle data points are important . The slope skips them. |
| Dot strip | Ranking across multiple groups on one axis | Space-efficient; good for benchmark comparisons. Axis flexibility: does not require zero baseline. |
| Connected dot plot | Change between two data series across categories | Emphasises the difference between the two points. Works for two time periods; not multiple. |

### Distribution: what's the shape of the data?

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Histogram | Distribution of one continuous variable | Keep bar gaps narrow . The shape is the message. Don't confuse with a bar chart: histogram shows distribution, bar chart shows comparison. |
| Box plot | Comparing distributions across categories (median + quartiles) | Annotate what each element means for non-technical audiences. Build piece by piece in presentations. Does not reveal multimodal distributions . Use violin or histogram instead. |
| Violin | Bimodal or complex distributions where box plot oversimplifies | Heavier visual weight. Use in analysis contexts, not summary dashboards. |
| Dot strip | Distribution where individual values matter | Works up to a few hundred points before overplotting. Transparency helps with overlap. |

### Change over time: what's the trend?

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Line | Continuous time series, one or a few series | Default for trend. Cap at 4–5 series before it becomes untrackable. Non-zero y-axis baseline acceptable when range is narrow and clearly labelled; label it explicitly. Remove point markers unless highlighting a specific event. Allocate 70–80% of vertical space to the data range. |
| Column | Discrete time periods (daily, weekly, monthly counts) | Best with one series. Must start at zero. Multiple series: grouped or stacked. |
| Area | Total accumulated over time, or uncertainty band | Zero baseline mandatory. Use semi-transparent fills when series overlap. Stacked areas obscure all series below the top one. Only use stacked when the total AND components both matter. |
| Sparkline | Trend at a glance, secondary to a primary number | No axes, no labels. Shape only. Each bar: explicit pixel width (3–4 px), explicit height, `gap: 2`, parent `alignItems: flex_end`. Never `fill_container` on bar width. See `batch-design-grammar.md` for the full anatomy. |
| Calendar heatmap | Daily patterns over a long period (GitHub-style activity grid) | Loses precision; the temporal pattern is the point. |
| Grouped column | Multiple series compared across discrete time periods | Cap at 3–4 series. |
| Stacked column | Composition changing over time when total AND breakdown both matter | Hard to read below the top series. Normalise to 100% when proportion is the point. |

### Part-to-whole: how do components add up?

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Stacked bar (normalised) | Proportional composition across categories | 100% scale; two baselines (top and bottom) make those series easiest to compare. Interior segments remain hard to compare . Reduce segment count or highlight one. |
| Treemap | Hierarchical breakdown, many categories where area = magnitude | Works to ~15–20 leaf nodes before labelling fails. Zero and negative values cannot be sized . Don't use treemaps for data that includes them. |
| Waffle / gridplot | Simple whole-number percentages for non-technical audiences | Always whole numbers. A 10×10 grid = 1 square per percent. Fractional squares require rounding. |
| Unit chart | Making individual items feel human or countable | Memorable but polarising. Keep symbols consistent in size. Include a legend. Do not add time comparisons . It becomes too complex. |
| Donut | Single proportional breakdown where the total matters | Total in the centre. Cap at 4–5 segments. More than that: use a horizontal bar. |
| Pie | Two to three segments with a clear dominant share | More than 3 segments: use a bar instead. Slices must sum to 100%. Sort by value. No 3D or exploded effects. Use direct labels, not a legend. |
| Waterfall | Sequential additions and subtractions to a running total | Colour increases one colour, decreases another. Direct-label each bar when precision matters. Group related increases and decreases together; don't intersperse. |
| Square area chart | Alternative to pie where area comparison is clearer | Rectangular shapes are easier to compare than wedges. Use when the audience is present to be guided through it; static contexts require more explanation. |

### Magnitude: how big?

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Column | Comparing counts or amounts across categories | Must start at zero. Sort descending unless order has inherent meaning. Gap roughly 30–40% of bar width. Direct labels inside bar ends reduce visual clutter. |
| Bar | Same as column; prefer when labels are long or there are many categories | Must start at zero. |
| Bullet graph | Single metric vs its target and performance ranges (poor/satisfactory/good) | Anatomy: foreground bar = actual value; horizontal line = target; background shaded bands = reference ranges (darker to lighter, same hue). Label the ranges if the audience is unfamiliar with the format. Far more honest and compact than a gauge or speedometer dial. |
| Proportional symbol | Large variation between values where bar length would be hard to read | Size by area, not radius. Differences in area are harder to judge than length . Annotate values directly. |
| Radar / spider | Comparing one entity across multiple performance dimensions | Hard to read with > 6 axes. Never use for cross-entity comparisons: the shaded area grows geometrically rather than linearly, creating false impressions of magnitude. Parallel coordinates are a clearer alternative. |
| Gantt | Project timelines: tasks as horizontal bars on a time axis | Use when duration and sequence are both important. Limit colours; mark milestones. Include a "today" line. |

### Flow: how does it move between states?

| Chart | When to use | Critical rules |
|-------|-------------|----------------|
| Sankey | Volume moving through stages of a funnel or process (signup → activated → paid) | Flow band width = magnitude. Good for conversion analysis. Don't use for categorical comparisons without real directional flow . It confuses the format. Cap complexity; too many nodes and overlapping flows become unreadable. |
| Waterfall | Budget or P&L flow (starting value → adjustments → ending value) | Show net increases in one colour, decreases in another. Group increases together, decreases together. Floating bars make comparisons hard . Label values directly. |
| Network graph | Relationships and connection strength between many nodes | Use only when the topology is the insight. Hard to read above ~30 nodes. |
| Flowchart | Documenting a decision process or system logic | Use standard shape conventions: oval = start/end, diamond = decision, rectangle = action. Remove decorative borders and unnecessary colour. |

### Quick-reference: question to chart

| The question | First choice | Second choice |
|--------------|-------------|---------------|
| Trend over time | Line | Column (discrete periods) |
| Compare categories | Bar/column | Lollipop (many items) |
| Part of a whole | Normalised stacked bar | Donut (≤ 4 parts) |
| Distribution shape | Histogram | Box plot |
| Correlation | Scatter | Bubble (3rd variable) |
| Deviation from baseline | Diverging bar | Surplus/deficit area |
| Funnel / conversion | Sankey | Stacked column |
| Ranking | Ordered bar | Slope (rank change) |
| Trend at a glance | Sparkline | Calendar heatmap |
| Metric vs target | Bullet graph | Progress bar (less informative) |
| Composition over time | Stacked column | Area |
| Hierarchical breakdown | Treemap | Waffle / unit chart |
| Task sequence and duration | Gantt | Slope (if only start/end matter) |
| Geographic pattern | Choropleth (rates only) | Proportional symbol map |

**Banned by default:**

- Pie charts with > 3 slices.
- 3D anything.
- Donut with a giant number in the centre that doesn't match the slice data.
- Word clouds.
- Radar charts for cross-entity comparisons (geometric area distorts the data).
- Dual-axis charts unless the two measures are genuinely related and both y-axes clearly labelled.
- Fitted trend lines in explanatory scatterplots (add noise, invite contention).
- Gauges and speedometer dials . Use a bullet graph instead.

## Defaults for every chart

- **Zero baseline:** mandatory for bar and column charts. Optional for line and dot charts . When you truncate, label the axis explicitly so the reader can't miss it.
- **Gridlines:** horizontal only, `$borderMuted`. No vertical gridlines except on time-series with discrete buckets. Gridlines should be quieter than the data.
- **Axis labels:** `$textSm`, `$textMuted`. Never bold. Never rotate more than 45° . If labels need rotation, use a horizontal bar chart instead.
- **Tick density:** no more than 6 x-axis ticks visible at once. Skip labels before letting them overlap.
- **Numbers:** comma-separated above 999 (`1,284` not `1284`). Use `$fontMono` for value labels in dense or data-heavy charts. Use abbreviated suffixes (K, M, B) when space is tight; be consistent across the whole chart.
- **Line stroke:** 2 px default, 1.5 px in small multiples. Point markers only when highlighting a specific event . Remove them for plain trend lines.
- **Bar gap:** gap should be roughly 30–40% of bar width (not 20%, which is too tight). Gaps narrower than bars make it a histogram, not a comparison chart.
- **Direct labels vs legends:** prefer direct labels on the last data point of a line or inside the end of a bar over a separate legend. Legends make the reader's eyes travel; direct labels answer the question immediately.
- **Tooltips:** hover only (desktop), tap only (mobile). Show precise value, series name, and date/category. Never show raw database field names in a tooltip.
- **Vertical space:** allocate 70–80% of chart height to the data range, leaving balanced white space above and below. A chart where the data sits in the bottom 20% of the frame is mis-scaled.
- **Colour:** chart colours come from the palette declared above. Never use raw hex. Never use the same colour for two different series in the same chart.
- **Tables vs charts:** use a table when the audience needs to look up individual values; use a chart when the pattern or trend is the message. Don't use a table in a live presentation where the audience needs to read and listen simultaneously.

## Dashboard layout

A typical dashboard tile:

```
Tile (Card, $elevation1, padding $space-6)
├── Header
│   ├── Title ($textBase, $textPrimary)
│   ├── (Optional) Helper / context ($textSm, $textMuted)
│   └── (Optional) Action menu ($iconMd, top-right)
├── Big-number ($text3xl, $textPrimary), the single most important number
├── Delta ($textSm, $success or $danger, with up/down arrow)
└── Chart (sparkline or small chart)
```

**Rules:**

- Each tile answers **one** question. If a tile has two big numbers, it's two tiles.
- Big-number > delta > chart in visual weight. Reverse it and the user has to hunt for the answer.
- Sparklines under big numbers should not have y-axis labels, they're a shape, not a precise reference.

## Chart states

Every chart needs four states:

| State | Treatment |
|-------|-----------|
| **Loading** | Skeleton, a placeholder rectangle in `$surfaceMuted` with the shimmer recipe from `motion.md`. Never a spinner inside a chart frame. |
| **Empty** | Centred, muted icon + "No data yet" + (optional) "Connect a source" CTA. Match `voice.md` empty-state rules. |
| **Error** | Inline message + retry. Don't break layout, keep the tile's outer dimensions. |
| **Partial / stale** | A subtle banner or label noting the data range is incomplete; don't silently render misleading numbers. |

## Annotation

When a chart needs a callout (a spike, a launch event, a threshold):

- Use a single accent colour (`$accent`) for annotations, distinct from the chart series colours.
- Threshold lines: dashed, 1px, `$borderMuted`. Label at the right edge.
- Don't annotate every interesting point; pick one.

## Archetype-keyed chart styles

The same chart reshapes meaningfully by archetype. See `assets/archetypes/` for the full bundles.

- **`saas-apps/b2b/analytics-dashboard`** (the canonical chart archetype):
  - **Bar charts default**, not line. Lines only when continuous time matters more than discrete comparison.
  - Bars use one accent fill colour with the latest period at full opacity and prior periods at 60%, instead of pale-and-strong contrast.
  - Sparklines render as actual mini-charts (12–14 thin bars in the cards), never as decorative coloured blocks under a value.
  - Gridlines are nearly invisible; the hairline border around the chart frame does the framing.
  - No count-up animations on values; the data just appears.
- **`saas-apps/b2b/modern-pro-tool`** (Linear-style):
  - Charts are uncommon; when needed, treated as inline data summaries (small, tight, restrained colour) rather than centrepiece visualisations.
  - Cycle-burndown style: subtle gradient fill below the line, dashed lines for projections, solid lines for actuals, two-colour palette max (yellow for started + blue for completed).
  - Render small and embedded in their data context.
- **`saas-apps/b2b/workflow-platform`** (when populated): more colour-coded series, status-segmented bars, more visual variety per chart because status IS the data.
- **`marketing-websites/*`**: charts, when shown, are *editorial moments*, large numerals paired with one line of context (*"3.3x faster"*) instead of full chart frames. Use `editorial-storytelling` archetype if the chart IS the section.

**What generic looks like (don't ship this):** rainbow palette across 6 series, vertical AND horizontal gridlines at full saturation, line chart for everything regardless of question, count-up animation on KPIs when the page loads, gradient fill under every line.

## Adding a chart token

If a chart needs a colour or style that doesn't fit, add it here first (with both light and dark values, palette role explained). Don't ship a one-off chart palette inside a single component.
