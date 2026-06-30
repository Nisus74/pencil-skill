# Chart anatomy

Concrete Pencil build instructions for every chart type agents build in product dashboards. Each section has three parts:

1. **Anatomy**: the exact node tree, pixel values, and property rules.
2. **Worked ops**: a `batch_design` excerpt you can copy and adapt.
3. **What generic looks like**: the exact ops that produce slop output, and why they fail.

Read this alongside `data-viz.md` (which tells you *which* chart to pick) and `batch-design-grammar.md` (which covers the op grammar). When `data-viz.md` says "use a line chart", come here to know what a polished line chart looks like in Pencil coordinates.

---

## Dashboard shell

The frame everything lives inside. Get this wrong and every chart inside it looks wrong too.

### Anatomy

```
DashboardPage (frame, 1440 x 900, layout: none)
├── Sidebar (frame, 220 x fill_container, layout: vertical)
│   ├── SidebarHeader (frame, fill_container x 56, layout: horizontal)
│   │   ├── Logo (frame or icon, 24 x 24)
│   │   └── ProductName (text, $textSm, $textPrimary, fontWeight: 600)
│   ├── SidebarNav (frame, fill_container x fit_content, layout: vertical, gap: 2, padding: [4, 8])
│   │   └── NavItem × N (frame, fill_container x 32, layout: horizontal, gap: 8, padding: [0, 8], cornerRadius: 6)
│   │       ├── NavIcon (icon, 16 x 16, $iconMd)
│   │       └── NavLabel (text, $textSm, $textSecondary)
│   └── SidebarFooter (frame, fill_container x 56, layout: horizontal, padding: [0, 12])
│       └── UserRow (avatar + name)
└── MainContent (frame, fill_container x fill_container, layout: vertical)
    ├── Topbar (frame, fill_container x 56, layout: horizontal, alignItems: center, padding: [0, 24], justifyContent: space_between)
    │   ├── PageTitle (text, $textBase, $textPrimary, fontWeight: 600)
    │   └── TopbarActions (layout: horizontal, gap: 8)
    ├── ContentArea (frame, fill_container x fill_container, layout: vertical, gap: 24, padding: [24, 24])
    │   ├── KPIRow (frame, fill_container x fit_content, layout: horizontal, gap: 16)
    │   │   └── KPICard × N
    │   └── ChartRow (frame, fill_container x fit_content, layout: horizontal, gap: 16)
    │       └── ChartCard × N
```

### Critical measurements

| Element | Width | Height | Notes |
|---------|-------|--------|-------|
| Sidebar | 220 | fill_container | Never wider than 240. Narrower (180) for dense tools. |
| Topbar | fill_container | 56 | 48 for compact. Never below 44 (touch target). |
| Content padding | 24 on all sides | | 16 for dense products (data tables, developer consoles). |
| Card gap | 16 | | 24 for spacious layouts (marketing, consumer apps). |
| KPI card | fill_container | fit_content | Equal width across the row via fill_container + gap. |
| Chart card | fill_container | 280–360 | Height depends on chart type; declare explicitly. |

### Worked ops (skeleton, one call)

```
page = Insert(document, {
  type: "frame", name: "DashboardPage",
  context: "Main dashboard view. 1440-wide desktop layout.",
  layout: "horizontal", width: 1440, height: 900,
  fill: "$surfaceBase"
})
sidebar = Insert(page, {
  type: "frame", name: "Sidebar",
  context: "Primary navigation. Persistent on desktop.",
  layout: "vertical", width: 220, height: "fill_container",
  fill: "$surfaceSidebar",
  stroke: "$border", strokeWidth: 1
})
main = Insert(page, {
  type: "frame", name: "MainContent",
  layout: "vertical", width: "fill_container", height: "fill_container",
  fill: "$surfaceBase"
})
topbar = Insert(main, {
  type: "frame", name: "Topbar",
  context: "Page-level header. Contains breadcrumb, actions, user context.",
  layout: "horizontal", alignItems: "center",
  justifyContent: "space_between",
  width: "fill_container", height: 56,
  padding: [0, 24],
  fill: "$surface",
  stroke: "$border", strokeWidth: 1
})
content = Insert(main, {
  type: "frame", name: "ContentArea",
  layout: "vertical", gap: 24, padding: [24, 24],
  width: "fill_container", height: "fill_container",
  fill: "$surfaceBase"
})
```

### What generic looks like

```
// WRONG: pure black sidebar, white content, no border
sidebar = Insert(page, { fill: "#000000", ... })
main = Insert(page, { fill: "#FFFFFF", ... })

// WRONG: sidebar too wide (wastes content space)
sidebar = Insert(page, { width: 280, ... })

// WRONG: no topbar height declared, no border between sidebar and content
// Result: floating sidebar, undefined edge, AI-assembled look
```

The dark-sidebar-on-white-content combination is the single strongest AI-assembled signal in dashboard design. Use `$surfaceSidebar` (a variable that resolves to a subtle tint of `$surface` in light mode, not pure black) and a `1px $border` stroke between panels instead.

---

## Bar chart (vertical column)

### Anatomy

```
BarChartCard (frame, fill_container x 280, layout: vertical, gap: 0,
              fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8)
├── ChartHeader (frame, fill_container x fit_content, layout: horizontal,
│               justifyContent: space_between, alignItems: center, padding: [16, 16, 12, 16])
│   ├── ChartTitle (text, $textBase, $textPrimary, fontWeight: 600)
│   └── ChartPeriod (text, $textSm, $textMuted)
├── ChartBody (frame, fill_container x fill_container, layout: none, padding: [0, 16, 16, 16])
│   ├── YAxisLabels (frame, 32 x fill_container, layout: vertical, justifyContent: space_between,
│   │               alignItems: end)
│   │   └── YLabel × 5 (text, $textXs, $textMuted, content: "30M", "20M", "10M", "0")
│   ├── GridLines (frame, fill_container x fill_container, layout: none)
│   │   └── GridLine × 4 (frame, fill_container x 1, fill: "$borderMuted")
│   │       // positioned at 25%, 50%, 75%, 100% of chart height via y values
│   └── BarsArea (frame, fill_container x fill_container, layout: horizontal,
│                 alignItems: end, justifyContent: space_between, gap: 8)
│       └── BarGroup × N (frame, fill_container x fill_container, layout: vertical,
│                          alignItems: center, gap: 4)
│           ├── Bar (frame, fill_container x <explicit px>, fill: "$chart-1", cornerRadius: [2,2,0,0])
│           └── XLabel (text, $textXs, $textMuted, content: "Apr 28")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Bar width | `fill_container` inside BarGroup | The BarGroup uses `fill_container` in the horizontal parent; bar fills that group. |
| Bar gap | `gap: 8` on BarsArea, or use `justifyContent: space_between` | Gap should read as ~30–40% of bar width visually. |
| Bar corner radius | `[2, 2, 0, 0]` | Top corners only. Full cornerRadius makes bars look like pills. |
| Y-axis label width | 32 px | Fixed. Labels right-aligned. |
| Grid lines | `$borderMuted`, 1 px height, `fill_container` width | Horizontal only. Never vertical. |
| Chart card height | 280 px minimum | Less and the bars become too short to read. |

### Worked ops

```
chartCard = Insert(content, {
  type: "frame", name: "BarChartCard",
  context: "API call volume per day. Bars are discrete daily buckets.",
  layout: "vertical", gap: 0,
  width: "fill_container", height: 280,
  fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8
})
chartHeader = Insert(chartCard, {
  type: "frame", name: "ChartHeader",
  layout: "horizontal", alignItems: "center", justifyContent: "space_between",
  width: "fill_container", height: "fit_content", padding: [16, 16, 12, 16]
})
chartTitle = Insert(chartHeader, {
  type: "text", name: "ChartTitle", content: "API Call Volume",
  fontSize: "$textBase", fontWeight: 600, fill: "$textPrimary"
})
chartPeriod = Insert(chartHeader, {
  type: "text", name: "ChartPeriod", content: "Last 7 days",
  fontSize: "$textSm", fill: "$textMuted"
})
chartBody = Insert(chartCard, {
  type: "frame", name: "ChartBody",
  layout: "none",
  width: "fill_container", height: "fill_container",
  padding: [0, 16, 16, 48]   // 48px left padding for y-axis labels
})
barsArea = Insert(chartBody, {
  type: "frame", name: "BarsArea",
  layout: "horizontal", alignItems: "end", justifyContent: "space_between",
  gap: 8,
  width: "fill_container", height: "fill_container"
})
// Repeat for each bar — vary height to represent data
bar1 = Insert(barsArea, {
  type: "frame", name: "BarGroup_Apr28",
  layout: "vertical", alignItems: "center", gap: 4,
  width: "fill_container", height: "fill_container"
})
barFill1 = Insert(bar1, {
  type: "frame", name: "Bar",
  width: "fill_container", height: 120,   // px proportional to data value
  fill: "$chart-1", cornerRadius: [2, 2, 0, 0]
})
xLabel1 = Insert(bar1, {
  type: "text", name: "XLabel", content: "Apr 28",
  fontSize: "$textXs", fill: "$textMuted"
})
```

### What generic looks like

```
// WRONG: gradient fill on bars
barFill = Insert(barsArea, { fill: [{ type: "gradient", ... }] })

// WRONG: all bars same height (placeholder data with equal values)
// Every bar at height: 100 — looks like a loading state, not data

// WRONG: cornerRadius on all four corners
barFill = Insert(..., { cornerRadius: 8 })  // bars become pills

// WRONG: purple/blue gradient that matches the sidebar
// Result: the AI "signature" dashboard — recognisable in under 1 second

// WRONG: full fill_container height on bars (no variation)
// Makes the chart look like a solid rectangle
```

**Highlight-latest move:** the most recent bar gets `fill: "$chart-1"` at full opacity. Prior bars get `opacity: 0.5`. This signals "this is the current period" without a separate legend — not all bars the same colour.

---

## Bar chart (horizontal)

Use when category labels are long or there are more than 8 categories.

### Anatomy

Same as vertical bar but rotated:

```
BarsArea (layout: vertical, justifyContent: space_between, gap: 6)
└── BarRow × N (layout: horizontal, alignItems: center, gap: 8,
                width: fill_container, height: 24)
    ├── RowLabel (text, $textXs, $textMuted, width: 80, textAlign: right)
    ├── BarTrack (frame, fill_container x 8, fill: "$surfaceMuted", cornerRadius: 4)
    │   └── BarFill (frame, <% width> x 8, fill: "$chart-1", cornerRadius: 4)
    └── ValueLabel (text, $textXs, $textMuted, content: "847K")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Bar track height | 8 px | Thin bars read as data. Thick bars (24+ px) look like buttons. |
| Bar fill width | explicit px based on data proportion | Calculate: `(value / max) * trackWidth`. Never `fill_container`. |
| Label width | 80–120 px | Fixed; right-aligned. Adjust if labels are longer. |
| Row height | 24 px | Gives breathing room between bars. |
| Gap between rows | 6 px | Tighter = more data-dense. |

### What generic looks like

```
// WRONG: thick bars (height: 32+) — looks like a settings list, not a chart
// WRONG: no value labels — user can't read precise values
// WRONG: bars all the same width — same issue as vertical chart, looks like loading state
// WRONG: no track background — bar appears to float in space with no reference
```

---

## Line chart

### Anatomy

Line charts in Pencil are built as SVG `path` nodes or approximated with connected frame segments. The approximation approach (small rectangles at each data point, connected by rotated thin lines) works for static mockups. The path approach is cleaner.

```
LineChartCard (frame, fill_container x 280, layout: vertical,
               fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8)
├── ChartHeader (same as bar chart)
├── ChartCanvas (frame, fill_container x fill_container, layout: none, padding: [16, 16, 32, 48])
│   ├── GridLines (frame, fill_container x fill_container, layout: none)
│   │   └── GridLine × 4 (frame, fill_container x 1, y: proportional, fill: "$borderMuted")
│   ├── LinePath (path or line node representing the data line)
│   │   // Stroke: 2px, color: "$chart-1", no fill
│   ├── (Optional) AreaFill (frame below the line — see Area chart section)
│   ├── DataPoints (icon circles or small frames at each data point)
│   │   // Only when highlighting specific events, not on every point
│   ├── XAxis (frame, fill_container x 1, y: bottom, fill: "$border")
│   └── XLabels (frame, fill_container x fit_content, layout: horizontal,
│                justifyContent: space_between, padding: [4, 0, 0, 0])
│       └── XLabel × N (text, $textXs, $textMuted)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Line stroke | 2 px | 1.5 px in small multiples or sparklines. Never thinner than 1.5. |
| Grid line stroke | 1 px | `$borderMuted`. Horizontal only. 4–6 lines maximum. |
| Data point marker | 4–6 px circle | Only at event callouts, never on every point. |
| Chart padding | 16 top, 48 left (y-axis space), 16 right, 32 bottom (x-labels) | Adjust left padding for y-axis label width. |
| Multiple series cap | 4 series maximum | Label directly at line ends, not with a legend. |

### Worked ops (line approximation with dots)

```
canvas = Insert(chartCard, {
  type: "frame", name: "ChartCanvas",
  layout: "none",
  width: "fill_container", height: "fill_container",
  padding: [16, 16, 32, 48]
})
// Grid lines — horizontal, evenly spaced
grid1 = Insert(canvas, { type: "frame", name: "Grid1", width: "fill_container", height: 1,
                  fill: "$borderMuted", y: 0 })
grid2 = Insert(canvas, { type: "frame", name: "Grid2", width: "fill_container", height: 1,
                  fill: "$borderMuted", y: 55 })
grid3 = Insert(canvas, { type: "frame", name: "Grid3", width: "fill_container", height: 1,
                  fill: "$borderMuted", y: 110 })
grid4 = Insert(canvas, { type: "frame", name: "Grid4", width: "fill_container", height: 1,
                  fill: "$borderMuted", y: 165 })
// X-axis labels
xLabels = Insert(canvas, {
  type: "frame", name: "XLabels",
  layout: "horizontal", justifyContent: "space_between",
  width: "fill_container", height: "fit_content",
  y: 200   // bottom of canvas
})
// Add individual x-labels as text nodes inside xLabels
```

### What generic looks like

```
// WRONG: line stroke 1px — disappears on high-DPI screens
// WRONG: point markers on every data point — visual noise, not signal
// WRONG: gradient fill under the line applied by default
//   → If you want an area chart, declare it explicitly (see Area chart section)
//   → A line chart with a semi-transparent fill is a different chart type
// WRONG: y-axis starting at a non-zero value without a label — misleads the reader
// WRONG: 6+ series, all the same weight — unreadable, use small multiples instead
// WRONG: legend in a box on the right — label lines directly at their endpoints
```

**For data-dense product surfaces:** lines are thinner (1.5 px), filled area optional (5–10% opacity), colour from `$chart-1` only unless a second series is genuinely needed. No point markers — they add visual noise at small sizes.

---

## Area chart

An area chart is a line chart where the region below the line is filled. Build as a line chart (above) with one additional fill frame.

### The fill layer

```
// Below the LinePath, insert:
AreaFill (frame, fill_container x <height from line to x-axis>, layout: none)
// Fill: semi-transparent version of $chart-1
// Opacity: 0.08–0.12 (light mode); 0.15–0.20 (dark mode)
// Position: y aligns with the line's lowest point; height reaches x-axis
// cornerRadius: 0 (it touches the axis baseline)
```

### Critical rules

- Zero baseline is mandatory. An area chart where the bottom of the fill doesn't reach zero misrepresents the data.
- When two series overlap, the front series must be semi-transparent so the one behind shows through. Use opacity on the frame, not on the fill colour.
- Stacked area (where series stack on top of each other) requires all series except the bottom one to use a chart library. In Pencil mockups, approximate with two frame fills.
- Do not use an area chart when the trend is the message and the area adds no information. A plain line is cleaner.

### What generic looks like

```
// WRONG: full opacity fill (blocks view of data behind it)
AreaFill = Insert(canvas, { fill: "$chart-1", opacity: 1.0 })

// WRONG: gradient fill from full colour to transparent
// → AI's go-to area chart treatment. Looks decorative, not analytical.
// → Use flat semi-transparent fill instead.
AreaFill = Insert(canvas, { fill: [{ type: "gradient", ... }] })

// WRONG: area chart where the baseline is not at zero
// The fill bottom hangs in mid-air — the data looks like it starts at a non-zero baseline
```

---

## Donut chart

### Anatomy

Donut charts in Pencil are built with ellipse nodes (full circle) and overlapping frame masks. The simplest approach for a mockup: a full-circle ellipse with a stroke, overlaid with a smaller white (surface) ellipse to create the donut hole.

```
DonutCard (frame, fill_container x 200, layout: vertical, gap: 8,
           fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8,
           padding: [16, 16])
├── ChartTitle (text, $textBase, $textPrimary, fontWeight: 600)
├── DonutWrapper (frame, 120 x 120, layout: none; centred via parent alignItems/justifyContent)
│   ├── DonutRing (ellipse, 120 x 120, fill: none,
│   │             stroke: "$chart-1", strokeWidth: 16)
│   │   // For multi-segment: use multiple ellipses with stroke-dasharray offsets
│   │   // For a single proportion: one filled arc ellipse + one "$surfaceMuted" arc
│   ├── DonutHole (ellipse, 80 x 80, fill: "$surface", centered)
│   │   // Creates the donut hole by covering the centre
│   └── CentreValue (text, $text2xl, $textPrimary, fontWeight: 700, centered)
│       // The single most important number. Only one number in the centre.
└── Legend (frame, fill_container x fit_content, layout: vertical, gap: 6)
    └── LegendItem × N (layout: horizontal, gap: 8, alignItems: center)
        ├── Swatch (frame, 8 x 8, cornerRadius: 2, fill: "$chart-N")
        └── LegendLabel (text, $textSm, $textSecondary)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Outer ring diameter | 120 px (card), 80 px (small tile) | Scale proportionally. |
| Stroke thickness | 16 px | ~13% of outer diameter. Thinner = harder to read. Thicker = looks like a pie. |
| Donut hole diameter | outer - (2 × stroke) = 88 px | Centre value needs space; don't make the hole too small. |
| Centre value size | `$text2xl` (24 px) | One number only. No unit abbreviation that changes the meaning. |
| Maximum segments | 4 | More than 4: use a horizontal bar chart instead. |

### What generic looks like

```
// WRONG: giant number in the centre that doesn't match any segment
DonutHoleValue = Insert(hole, { content: "1,284" })
// ...but the donut shows a percentage breakdown — the number is the total,
// not readable from the segments. Confusing.

// WRONG: 6+ segments with no grouping
// → Use "Other" for anything below 5% of the total

// WRONG: equal-sized segments used as a design pattern
// → A donut where all segments are the same size communicates nothing

// WRONG: 3D donut (rendered with perspective)
// → 3D distorts area perception; the front segments look larger than the back
```

---

## Bullet graph

The bullet graph replaces gauge/speedometer dials. It shows actual vs target vs performance ranges in a compact bar.

### Anatomy

```
BulletCard (frame, fill_container x fit_content, layout: vertical, gap: 8,
            fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8,
            padding: [12, 16])
├── BulletLabel (text, $textSm, $textMuted, content: "P95 Latency")
├── BulletChart (frame, fill_container x 20, layout: none)
│   ├── RangePoor (frame, <30% of fill_container> x 20, fill: "$chartSeq-200", cornerRadius: [4,0,0,4])
│   │   // The "poor" performance band — leftmost, lightest shade
│   ├── RangeSatisfactory (frame, <next 30%> x 20, fill: "$chartSeq-400", x: 30%)
│   │   // Mid range — medium shade, same hue
│   ├── RangeGood (frame, <remaining 40%> x 20, fill: "$chartSeq-600", x: 60%)
│   │   // Good range — darkest shade of the same hue
│   ├── ActualBar (frame, <value%> x 12, fill: "$textPrimary", y: 4, cornerRadius: 2)
│   │   // The actual value — foreground bar, centred vertically in the track
│   │   // Darker, more prominent than the background ranges
│   └── TargetMarker (frame, 2 x 20, fill: "$textPrimary", x: <target%>)
│       // Vertical line at the target value. Same colour as ActualBar.
│       // Width: 2px. Height: full track height (20px).
└── BulletValues (frame, fill_container x fit_content, layout: horizontal,
                 justifyContent: space_between)
    ├── ActualValue (text, $textSm, $textPrimary, fontWeight: 600, content: "142ms")
    └── TargetValue (text, $textXs, $textMuted, content: "Target: 120ms")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Track height | 20 px | Background ranges fill the full height. |
| Actual bar height | 12 px | Centred in the track (`y: 4`). Narrower than the track so ranges show around it. |
| Target marker width | 2 px | Exact pixel position = `(target / max) * trackWidth`. |
| Range proportions | Customise per metric | Typical: 0–50% poor, 50–80% satisfactory, 80–100% good. |
| Track colour | Same hue, three lightness steps | `$chartSeq-200`, `$chartSeq-400`, `$chartSeq-600`. Never three different hues. |

### Why agents get this wrong

Most agents have never seen a bullet graph described in Pencil coordinates. Without this anatomy they default to:

```
// WHAT AGENTS PRODUCE BY DEFAULT:
// A progress bar with a single flat fill — no performance bands, no target marker
ProgressBar = Insert(card, { type: "frame", width: "fill_container", height: 8,
                       fill: "$chart-1", cornerRadius: 4 })
// This is not a bullet graph. It shows actual but not target, and has no performance context.

// Or worse: a speedometer dial built from arc ellipses
// → Gauges are banned. They waste space and encode data inaccurately.
```

---

## Heatmap grid (XY / calendar)

### XY heatmap anatomy

```
HeatmapCard (frame, fill_container x fit_content, layout: vertical, gap: 8,
             fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8,
             padding: [16, 16])
├── ChartTitle (text)
├── HeatmapGrid (frame, fill_container x fit_content, layout: vertical, gap: 2)
│   └── HeatmapRow × N (frame, fill_container x fit_content, layout: horizontal, gap: 2)
│       ├── RowLabel (text, $textXs, $textMuted, width: 48, textAlign: right)
│       └── HeatmapCell × M (frame, 20 x 20, cornerRadius: 2, fill: "$chartSeq-<N>")
│           // Cell fill comes from the sequential palette based on value intensity
│           // No text inside cells unless the grid is large enough to read it (cell ≥ 28px)
└── XAxisLabels (frame, fill_container x fit_content, layout: horizontal,
                 justifyContent: space_between, padding: [0, 0, 0, 48])
    └── XLabel × M (text, $textXs, $textMuted)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Cell size | 20 x 20 px (compact); 28 x 28 (readable) | Smaller than 16 px: labels become unreadable. |
| Cell gap | 2 px | Tighter than bar charts because cells are already contained shapes. |
| Row label width | 48 px | Fixed; right-aligned. Enough for "Mon", "23:00". |
| Sequential palette depth | 5 steps minimum | `$chartSeq-50` through `$chartSeq-900`. More steps = finer gradient. |

### Calendar heatmap anatomy (GitHub-style activity grid)

```
CalendarGrid (frame, fill_container x fit_content, layout: horizontal, gap: 2,
              alignItems: start)
└── WeekColumn × 52 (frame, fit_content x fit_content, layout: vertical, gap: 2)
    └── DayCell × 7 (frame, 12 x 12, cornerRadius: 2, fill: "$chartSeq-<N>")
    // Cells with no activity: fill "$surfaceMuted"
    // Cells with activity: fill from sequential palette proportional to intensity
```

### What generic looks like

```
// WRONG: rainbow palette on heatmap cells (different hue per value range)
// Sequential data needs a single-hue palette varying in lightness.
// Multiple hues imply categorical differences, not magnitude.

// WRONG: cells with text values when cells are 16px — unreadable

// WRONG: equal colours across all cells (no variation in intensity)
// This happens when all placeholder values are set to the same number.
// Always vary cell values to show gradient.
```

---

## Data table

Tables are charts too. They need the same care.

### Anatomy

```
TableCard (frame, fill_container x fit_content, layout: vertical, gap: 0,
           fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8)
├── TableHeader (frame, fill_container x 36, layout: horizontal, alignItems: center,
│               fill: "$surfaceMuted", padding: [0, 16])
│   └── ColumnHeader × N (text, $textXs, $textMuted, fontWeight: 600, fill: "$textSecondary",
│                          textTransform: uppercase, letterSpacing: 0.5)
│       // Column widths: declare explicitly (not fill_container on all)
│       // Text columns: fill_container. Number columns: fixed (64–80 px). Status: 80–100 px.
├── TableDivider (frame, fill_container x 1, fill: "$border")
└── TableBody (frame, fill_container x fit_content, layout: vertical)
    └── TableRow × N (frame, fill_container x 44, layout: horizontal,
                      alignItems: center, padding: [0, 16])
        // Alternating row fill: every other row gets fill: "$surfaceMuted" at opacity 0.4
        // Or: no alternating fill, rely on row hover state + 1px dividers
        ├── Cell_Text (text, $textSm, $textPrimary, width: fill_container)
        ├── Cell_Mono (text, $textSm, $fontMono, $textPrimary, textAlign: right, width: 80)
        │   // Numbers: monospaced font, right-aligned, never left-aligned
        └── Cell_Badge (frame, fit_content x 20, layout: horizontal, padding: [0, 6],
                        cornerRadius: 10, fill: "$success-100")
            └── BadgeText (text, $textXs, fontWeight: 500, fill: "$success-700")
```

### Critical rules

- **Numbers: right-aligned, monospaced.** `$fontMono` for all numeric cells. Never left-aligned numbers: decimal places won't line up and values become hard to compare.
- **Text: left-aligned.** Standard reading direction.
- **Status columns: badge with colour + text.** Never colour-only (accessibility). Badge background at 10–15% opacity of status colour; text at 700-weight of status colour.
- **Header height: 36 px.** Row height: 44 px minimum (touch target). 40 px acceptable on desktop-only products.
- **Column widths: mixed, not all fill_container.** Fixed widths for status, number, and action columns. fill_container only for the primary label/name column.
- **Dividers: 1 px `$border` between rows, OR alternating row fill, not both.** Both at once is visual noise.

### What generic looks like

```
// WRONG: all columns fill_container (columns are random widths)
// WRONG: numbers left-aligned with a system font (values don't line up)
// WRONG: status as coloured text with no background (invisible at a glance)
// WRONG: 32px row height (too small for touch, cramped on desktop)
// WRONG: no column header distinction from data rows (header lost in the table)
// WRONG: full-opacity alternating row fills that compete with status colours
```

---

## Sparkline (recap)

Full anatomy is in `batch-design-grammar.md`. Summary:

- Parent: `layout: "horizontal"`, `alignItems: "end"`, `gap: 2`, explicit `width` and `height` in px.
- Each bar: `width: 3` (never `fill_container`), explicit height in px, `fill: "$accent"`, `cornerRadius: 1`.
- Vary heights across bars. Do not use equal heights.
- No axes, no labels, no tooltip on the sparkline itself.

```
// WRONG (the most common agent failure):
bar = Insert(sparklineArea, { width: "fill_container", height: "fill_container" })
// Result: one bar filling the entire sparkline area. Looks like a loading bar.

// RIGHT:
bar = Insert(sparklineArea, { width: 3, height: 18, fill: "$accent", cornerRadius: 1 })
```

---

## General polish rules (apply to every chart)

These are the differences between "technically correct" and "looks finished".

| Detail | Wrong | Right |
|--------|-------|-------|
| Card edge | No border, floating | `stroke: "$border", strokeWidth: 1` |
| Card corner | `cornerRadius: 0` or `cornerRadius: 16` | `cornerRadius: 8` (default for data cards) |
| Chart title weight | `fontWeight: 400` (same as body) | `fontWeight: 600` |
| Y-axis labels | Missing entirely | Present, right-aligned, `$textXs`, `$textMuted` |
| X-axis labels | Rotated 45° | Horizontal; reduce count if they overlap |
| Grid lines | Both horizontal and vertical | Horizontal only |
| Grid line colour | `$border` (same weight as card edge) | `$borderMuted` (lighter than card edge) |
| Numbers in chart | System font, left-aligned | `$fontMono`, right-aligned |
| Data labels | Missing on bar ends | Present on the last bar or all bars when they fit |
| Tooltip | Always visible as a floating box | Invisible until hover |
| Empty chart | Blank white space | Placeholder with icon + "No data" message |
| Loading chart | Spinner in the centre | Skeleton shimmer matching chart shape |
| Chart palette | `$primary` for all series | `$chart-1` through `$chart-8`; `$primary` only for the focal series |
| Shadow | `drop_shadow` on every card | No shadow for `analytics-dashboard`; hairline border instead |
