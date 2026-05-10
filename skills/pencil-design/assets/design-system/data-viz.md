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

## Default chart types

Pick the chart type that matches the question, not the prettiest one.

| Question | Chart |
|----------|-------|
| "How does X change over time?" | Line. |
| "How does X compare across categories?" | Bar (horizontal if labels are long). |
| "How do parts make up a whole?" | Stacked bar. **Avoid pie.** Pie charts ≤ 3 slices are tolerable; > 3 is illegible. |
| "How are values distributed?" | Histogram or box plot. |
| "How does one axis correlate with another?" | Scatter. |
| "What's the trend at a glance?" | Sparkline. |

**Banned by default:**

- Pie charts with > 3 slices.
- 3D anything.
- Donut with a giant number in the middle that doesn't match the data shown.
- Word clouds.
- Radial / spiderweb.

## Defaults for every chart

- **Axes start at zero** for bar charts (always) and line charts (default; declare exceptions).
- **Gridlines:** horizontal only, light, `$borderMuted`. Vertical gridlines only on time-series with discrete time buckets.
- **Axis labels:** `$textSm`, `$textMuted`. Don't bold them.
- **Tick density:** ≤ ~6 x-axis ticks visible at any time. Rotate or skip when needed; never let labels overlap.
- **Numbers:** group with commas above 999. Use `$fontMono` for value labels in dense charts.
- **Stroke width on lines:** 2px default, 1.5px in dense small multiples.
- **Bar gap:** ~20% of bar width.
- **Tooltips:** on hover only (desktop) / on tap (mobile). Show the precise value, the series name, and the date/category.

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
