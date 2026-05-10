# analytics-dashboard

Data-led overview surfaces where every visible element earns its pixels through measurable insight. The user scans for anomalies in seconds. Chrome that asserts itself is a design failure.

**Surface category:** saas-apps/b2b
**Exemplars:** Mixpanel, Amplitude, PostHog (free-tier dashboards)
**Confidence:** high; values confirmed against live devtools measurements

Read this alongside `references/chart-anatomy.md` (chart node trees and ops) and `references/batch-design-grammar.md` (op grammar). This file covers the archetype-specific rules that override the chart-anatomy.md defaults.

---

## When to use this archetype

The user is silent on aesthetics and the product's job is making numbers legible. The audience lives inside this surface daily and wants the chrome to disappear so the data speaks. Skip this archetype when the dashboard is occasional or executive-summary; those suit a lighter archetype. If the user has supplied their own direction, follow it and use this file only for the parts they didn't specify.

---

## Design token reference

All values are variable references. No raw hex in ops.

| Token | Light value | Dark value | Role |
|-------|-------------|------------|------|
| `$bg` | `#FAFAF9` | `#0C0A09` | Page background. Off-white, not pure white. |
| `$surface` | `#FFFFFF` | `#1A1814` | Card backgrounds. One step brighter than `$bg`. |
| `$surfaceMuted` | `#F4F4F2` | `#221E1A` | Table headers, section dividers, sidebar fill. |
| `$surfaceSidebar` | `#F7F7F5` | `#161412` | Sidebar background. Slightly cooler than `$surface`. |
| `$border` | `#E4E4E0` | `#2E2A26` | 1px hairlines on cards, panels, rows. |
| `$borderMuted` | `#EDEDEA` | `#252420` | Chart grid lines. Lighter than `$border`. |
| `$textPrimary` | `#111110` | `#EEEEEC` | KPI values, table data, active labels. |
| `$textSecondary` | `#78716C` | `#A8A29E` | Supporting copy, column headers, nav labels. |
| `$textMuted` | `#A8A29E` | `#57534E` | Axis labels, timestamps, de-emphasised data. |
| `$accent` | Deep brand colour, not violet. Saturation under 70%. | | Chart bars, primary CTA, active nav indicator, delta arrows. Appears in at most 3 visual locations. |
| `$positive` | `#16A34A` | `#22C55E` | Positive deltas. Never `$accent`. |
| `$negative` | `#DC2626` | `#F87171` | Negative deltas. |
| `$fontUI` | `Geist` or `Satoshi` | | Labels, nav, body copy. |
| `$fontMono` | `Geist Mono` or `JetBrains Mono` | | Every numeric value. No exceptions. |
| `$chart-1` | `$accent` | | Primary data series. |
| `$chart-2` through `$chart-4` | Distinct muted hues, same lightness level | | Secondary series. Cap at 4 total series per chart. |

---

## Page shell

The `chart-anatomy.md` dashboard shell section has the full node tree. Use those ops verbatim, with these archetype-specific overrides:

```
page=I(document, {
  type: "frame", name: "DashboardPage",
  context: "Analytics overview. 1440-wide desktop layout.",
  layout: "horizontal", width: 1440, height: 900,
  fill: "$bg",
  placeholder: true
})
sidebar=I(page, {
  type: "frame", name: "Sidebar",
  layout: "vertical", width: 220, height: "fill_container",
  fill: "$surfaceSidebar",
  stroke: { color: "$border", thickness: 1 }
  // No drop_shadow. The 1px stroke handles separation.
})
main=I(page, {
  type: "frame", name: "MainContent",
  layout: "vertical", width: "fill_container", height: "fill_container",
  fill: "$bg"
})
```

---

## Sidebar

### Anatomy

```
Sidebar (frame, 220 x fill_container, layout: vertical,
         fill: "$surfaceSidebar",
         stroke: { color: "$border", thickness: 1 })
├── SidebarHeader (frame, fill_container x 56, layout: horizontal,
│                  alignItems: center, gap: 8, padding: [0, 16])
│   ├── Logo (frame, 24 x 24)
│   └── ProductName (text, $textSm, fontWeight: 600, $textPrimary)
├── SidebarNav (frame, fill_container x fill_container,
│               layout: vertical, gap: 2, padding: [8, 8])
│   ├── SectionLabel (text, 11px, fontWeight: 600, $textMuted,
│   │                 content: "OVERVIEW", letterSpacing: "0.06em",
│   │                 padding: [8, 4, 4, 4])
│   ├── NavItem_Active (frame, fill_container x 32, layout: horizontal,
│   │                    alignItems: center, gap: 8, padding: [0, 8], cornerRadius: 6)
│   │   ├── ActiveIndicator (frame, 2 x 20, fill: "$accent")
│   │   │   // 2px wide, 20px tall. NOT fill_container height. Centred vertically by flex.
│   │   ├── NavIcon (icon_font, 16 x 16, iconFontFamily: "lucide",
│   │   │           iconFontName: "bar-chart-2", fill: "$accent")
│   │   └── NavLabel (text, $textSm, fontWeight: 500, $textPrimary)
│   └── NavItem_Default (frame, fill_container x 32, layout: horizontal,
│                         alignItems: center, gap: 8, padding: [0, 8], cornerRadius: 6)
│       ├── NavIcon (icon_font, 16 x 16, iconFontFamily: "lucide",
│       │           iconFontName: "users", fill: "$textSecondary")
│       └── NavLabel (text, $textSm, $textSecondary)
└── SidebarFooter (frame, fill_container x 56, layout: horizontal,
                    alignItems: center, gap: 8, padding: [0, 12])
    ├── UserAvatar (frame, 28 x 28, cornerRadius: 14, fill: "$surfaceMuted")
    └── UserName (text, $textSm, $textSecondary, content: "travis@example.com")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Sidebar width | 220px | Range: 200–240. Never wider. 280px eats content space with no benefit. |
| Item height | 32px | Dense tools: 28px. Never below 28px. |
| Item corner radius | 6px | Not 0 (too rigid), not 8+ (too friendly for data tools). |
| Active indicator width | 2px | Height: 20px, not fill_container. The indicator is an accent line, not a tab. |
| Section label tracking | `"0.06em"` | Do not use raw px values for letterSpacing. They render differently. |
| SidebarHeader height | 56px | Matches topbar height so the two align across the horizontal break. |

### Worked ops (sidebar with one active item)

```
sidebarHeader=I(sidebar, {
  type: "frame", name: "SidebarHeader",
  layout: "horizontal", alignItems: "center",
  width: "fill_container", height: 56,
  gap: 8, padding: [0, 16]
})
logo=I(sidebarHeader, {
  type: "frame", name: "Logo",
  width: 24, height: 24, cornerRadius: 4,
  fill: "$accent"
})
productName=I(sidebarHeader, {
  type: "text", name: "ProductName",
  content: "Analytics", fontFamily: "$fontUI",
  fontSize: "$textSm", fontWeight: 600, fill: "$textPrimary"
})
nav=I(sidebar, {
  type: "frame", name: "SidebarNav",
  layout: "vertical", gap: 2, padding: [8, 8],
  width: "fill_container", height: "fill_container"
})
sectionLabel=I(nav, {
  type: "text", name: "SectionLabel",
  content: "OVERVIEW", fontFamily: "$fontUI",
  fontSize: 11, fontWeight: 600, fill: "$textMuted",
  letterSpacing: "0.06em", padding: [8, 4, 4, 4]
})
activeItem=I(nav, {
  type: "frame", name: "NavItem_Active",
  layout: "horizontal", alignItems: "center",
  width: "fill_container", height: 32,
  gap: 8, padding: [0, 8], cornerRadius: 6
})
indicator=I(activeItem, {
  type: "frame", name: "ActiveIndicator",
  width: 2, height: 20, fill: "$accent"
})
activeIcon=I(activeItem, {
  type: "icon_font", name: "NavIcon",
  iconFontFamily: "lucide", iconFontName: "bar-chart-2",
  width: 16, height: 16, fill: "$accent"
})
activeLabel=I(activeItem, {
  type: "text", name: "NavLabel",
  content: "Overview", fontFamily: "$fontUI",
  fontSize: "$textSm", fontWeight: 500, fill: "$textPrimary"
})
```

### What generic looks like

```
// WRONG: filled pill active state — the generic SaaS default
activeItem=I(nav, {
  fill: [{ type: "color", color: "$accent", opacity: 0.1 }]
  // Even a subtle background pill is wrong. Use the 2px indicator instead.
})

// WRONG: sidebar with a drop shadow on the right edge
sidebar=I(page, {
  effect: [{ type: "drop_shadow", x: 2, y: 0, blur: 8, opacity: 0.1 }]
  // The 1px border handles separation. No shadow.
})

// WRONG: sidebar 280px wide
sidebar=I(page, { width: 280 })
// 280px consumes 19% of a 1440 canvas. 220px is the ceiling.

// WRONG: active indicator full item height (looks like a left border on a pill)
indicator=I(activeItem, { width: 2, height: "fill_container" })
// Height: 20px. The indicator is shorter than the item — it floats centred.
```

**Detect:** If the screenshot shows a coloured background on the active nav item, that is the generic SaaS pattern. The active state in this archetype should read as a thin accent line left of slightly brighter text, subtle enough to look for.

---

## Top bar

### Anatomy

```
Topbar (frame, fill_container x 56, layout: horizontal, alignItems: center,
         justifyContent: space_between, padding: [0, 24],
         fill: "$surface",
         stroke: { color: "$border", thickness: 1 })
├── TopbarLeft (frame, fit_content x fill_container, layout: horizontal,
│               alignItems: center, gap: 12)
│   ├── PageTitle (text, $textBase, fontWeight: 600, $textPrimary,
│   │              content: "Overview")
│   └── PageMeta (text, $textSm, $textMuted,
│                 content: "Last updated 2 min ago")
└── TopbarRight (frame, fit_content x fill_container, layout: horizontal,
                  alignItems: center, gap: 8)
    ├── DateRangePicker (frame, fit_content x 32, layout: horizontal,
    │                    alignItems: center, gap: 6, padding: [0, 12],
    │                    cornerRadius: 6,
    │                    stroke: { color: "$border", thickness: 1 })
    │   ├── DateLabel (text, $textSm, $textPrimary, content: "Last 30 days")
    │   └── ChevronIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
    │                    iconFontName: "chevron-down", fill: "$textMuted")
    └── ExportButton (frame, fit_content x 32, layout: horizontal,
                      alignItems: center, gap: 6, padding: [0, 10],
                      cornerRadius: 6,
                      stroke: { color: "$border", thickness: 1 })
        ├── ExportIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
        │              iconFontName: "download", fill: "$textSecondary")
        └── ExportLabel (text, $textSm, $textSecondary, content: "Export")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Topbar height | 56px | 48px for ultra-dense tools. Never below 44px (touch target floor). |
| Control height | 32px | All topbar controls (date picker, export, filter) use the same height. |
| Control corner radius | 6px | Matches sidebar item radius. Consistent rounding throughout the archetype. |
| Right-side gap | 8px | Between controls. Grouped controls get 4px. |

### What generic looks like

```
// WRONG: filled primary button in the top bar
ExportButton=I(topbar, {
  fill: [{ type: "color", color: "$accent" }]
  // Filled button competes with KPI data for visual weight.
  // Controls in this archetype are always hairline-bordered ghost style.
})

// WRONG: avatar cluster in the top bar (AvatarGroup: "3 users online")
// This is a collaborative editing or social pattern — not a data tool.

// WRONG: breadcrumb + page title both at full visual weight
// Use one or the other. If breadcrumb, the current page segment gets fontWeight: 600.
// If standalone title, no breadcrumb.

// WRONG: topbar with gradient background
topbar=I(main, {
  fill: [{ type: "gradient", ... }]
  // Plain "$surface" only. The topbar is not decorative.
})
```

---

## KPI card

### Anatomy

```
KPICard (frame, fill_container x fit_content, layout: vertical,
          gap: 8, padding: [16, 16, 12, 16],
          fill: "$surface",
          stroke: { color: "$border", thickness: 1 },
          cornerRadius: 8)
          // NO effect property. No drop_shadow. Ever.
├── MetricLabel (text, $textSm, $textMuted,
│               content: "Monthly active users",
│               fontFamily: "$fontUI")
├── ValueRow (frame, fill_container x fit_content, layout: horizontal,
│             alignItems: center, justifyContent: space_between)
│   ├── MetricValue (text, $text2xl, fontWeight: 600, $textPrimary,
│   │               content: "24.7M", fontFamily: "$fontMono")
│   └── DeltaBadge (text, $textXs, $positive,
│                   content: "+18%", fontFamily: "$fontMono")
│       // Use $negative when the delta is a decrease.
│       // Never use $accent for deltas.
└── Sparkline (frame, 60 x 24, layout: horizontal,
               alignItems: flex_end, gap: 2)
    // See Sparkline section for bar ops.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Card padding | `[16, 16, 12, 16]` | 12px bottom (slightly less; the sparkline sits close to the card edge). |
| Label font size | `$textSm` (14px) | Muted colour (`$textMuted`). Label is subordinate to value. |
| Value font size | `$text2xl` (24px) | Monospace (`$fontMono`). fontWeight: 600. |
| Delta font size | `$textXs` (12px) | Monospace. $positive or $negative. Never $accent. |
| Sparkline size | 60 × 24px | Inside KPI card. Larger trend cards get 120 × 48px sparklines. |

### Worked ops

```
kpiRow=I(content, {
  type: "frame", name: "KPIRow",
  layout: "horizontal", gap: 16,
  width: "fill_container", height: "fit_content"
})
kpiCard=I(kpiRow, {
  type: "frame", name: "KPICard_MAU",
  context: "Monthly active users. Populated from /v1/stats/mau. Click → Users view.",
  layout: "vertical", gap: 8, padding: [16, 16, 12, 16],
  width: "fill_container", height: "fit_content",
  fill: "$surface",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 8
})
metricLabel=I(kpiCard, {
  type: "text", name: "MetricLabel",
  content: "Monthly active users",
  fontFamily: "$fontUI", fontSize: "$textSm", fill: "$textMuted"
})
valueRow=I(kpiCard, {
  type: "frame", name: "ValueRow",
  layout: "horizontal", alignItems: "center", justifyContent: "space_between",
  width: "fill_container", height: "fit_content"
})
metricValue=I(valueRow, {
  type: "text", name: "MetricValue",
  content: "24.7M",
  fontFamily: "$fontMono", fontSize: "$text2xl",
  fontWeight: 600, fill: "$textPrimary"
})
deltaBadge=I(valueRow, {
  type: "text", name: "DeltaBadge",
  content: "+18%",
  fontFamily: "$fontMono", fontSize: "$textXs", fill: "$positive"
})
spark=I(kpiCard, {
  type: "frame", name: "Sparkline",
  layout: "horizontal", alignItems: "flex_end", gap: 2,
  width: 60, height: 24
})
// See Sparkline section for bar ops to add inside spark
```

### What generic looks like

```
// WRONG: drop_shadow on the card (the most common regression)
kpiCard=I(kpiRow, {
  ...,
  effect: [{ type: "drop_shadow", blur: 8, y: 2, opacity: 0.08 }]
})
// Even a subtle shadow breaks the archetype. Fix: U(kpiCard, { effect: [] })

// WRONG: value in proportional font
metricValue=I(valueRow, {
  content: "24.7M",
  fontFamily: "$fontUI"   // WRONG: must be "$fontMono"
})
// Without monospace, figures in a row of KPI cards don't align.

// WRONG: delta below the value in its own row
deltaRow=I(kpiCard, { type: "frame", layout: "horizontal" })
delta=I(deltaRow, { type: "text", content: "+18%" })
// Three-row card (label, value, delta) creates three reads.
// Put delta in ValueRow, right-aligned via justifyContent: space_between.

// WRONG: $accent for positive delta
deltaBadge=I(valueRow, { ..., fill: "$accent" })
// $accent is a branding signal. $positive is a semantic signal. They are different roles.

// WRONG: gradient or coloured card background
kpiCard=I(kpiRow, {
  fill: [{ type: "gradient", ... }]
})
// Plain "$surface" only. Data is the decoration.
```

**Detect:**
- Shadow visible under any card: `U(cardId, { effect: [] })`
- Value text uses proportional width digits: change `fontFamily` to `"$fontMono"`
- Delta sits below the value rather than beside it: restructure `ValueRow`
- Positive delta colour matches chart bars: change `fill` to `"$positive"`

---

## Sparkline

### Anatomy

```
Sparkline (frame, 60 x 24, layout: horizontal, alignItems: flex_end, gap: 2)
// alignItems: flex_end — bars grow upward from the bottom of the container
// Explicit px for both width and height — never fill_container on a sparkline parent
├── Bar1 (frame, 3 x 6,  fill: "$accent", cornerRadius: 1, opacity: 0.4)
├── Bar2 (frame, 3 x 9,  fill: "$accent", cornerRadius: 1, opacity: 0.45)
├── Bar3 (frame, 3 x 8,  fill: "$accent", cornerRadius: 1, opacity: 0.5)
├── Bar4 (frame, 3 x 12, fill: "$accent", cornerRadius: 1, opacity: 0.55)
├── Bar5 (frame, 3 x 15, fill: "$accent", cornerRadius: 1, opacity: 0.6)
├── Bar6 (frame, 3 x 14, fill: "$accent", cornerRadius: 1, opacity: 0.65)
├── Bar7 (frame, 3 x 18, fill: "$accent", cornerRadius: 1, opacity: 0.7)
├── Bar8 (frame, 3 x 16, fill: "$accent", cornerRadius: 1, opacity: 0.75)
├── Bar9 (frame, 3 x 20, fill: "$accent", cornerRadius: 1, opacity: 0.85)
└── Bar10 (frame, 3 x 24, fill: "$accent", cornerRadius: 1, opacity: 1.0)
    // Most recent bar: full opacity and tallest. Trend reads oldest-to-newest left-to-right.
    // Vary heights to encode trend shape. Equal heights look like a loading bar.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Bar width | 3px explicit | Never `fill_container`. At 60px wide with `fill_container`, each bar is 40–60px: a loading skeleton, not a sparkline. |
| Bar gap | 2px | 10 bars × 3px + 9 gaps × 2px = 48px. Fits inside 60px. |
| Bar corner radius | 1px | Minimal rounding. Not 0 (too hard), not 4+ (too pill-like). |
| Opacity range | 0.4 → 1.0 | Oldest bars dimmer. Newest bar full opacity. Encodes recency without a second colour. |
| Parent height | 24px (KPI card), 48px (standalone trend tile) | Always explicit px. Never fit_content on a sparkline parent. Bars shrink to 0. |

### Worked ops (10 bars, inside an existing spark frame)

```
I(spark, { type: "frame", name: "Bar1",  width: 3, height: 6,  fill: "$accent", cornerRadius: 1, opacity: 0.4 })
I(spark, { type: "frame", name: "Bar2",  width: 3, height: 9,  fill: "$accent", cornerRadius: 1, opacity: 0.45 })
I(spark, { type: "frame", name: "Bar3",  width: 3, height: 8,  fill: "$accent", cornerRadius: 1, opacity: 0.5 })
I(spark, { type: "frame", name: "Bar4",  width: 3, height: 12, fill: "$accent", cornerRadius: 1, opacity: 0.55 })
I(spark, { type: "frame", name: "Bar5",  width: 3, height: 15, fill: "$accent", cornerRadius: 1, opacity: 0.6 })
I(spark, { type: "frame", name: "Bar6",  width: 3, height: 14, fill: "$accent", cornerRadius: 1, opacity: 0.65 })
I(spark, { type: "frame", name: "Bar7",  width: 3, height: 18, fill: "$accent", cornerRadius: 1, opacity: 0.7 })
I(spark, { type: "frame", name: "Bar8",  width: 3, height: 16, fill: "$accent", cornerRadius: 1, opacity: 0.75 })
I(spark, { type: "frame", name: "Bar9",  width: 3, height: 20, fill: "$accent", cornerRadius: 1, opacity: 0.85 })
I(spark, { type: "frame", name: "Bar10", width: 3, height: 24, fill: "$accent", cornerRadius: 1, opacity: 1.0 })
```

### What generic looks like

```
// WRONG: fill_container on bars (the most common sparkline failure)
I(spark, { type: "frame", width: "fill_container", height: "fill_container" })
// Result: one bar that fills the entire 60px container. Identical to a loading skeleton.
// Bars must have explicit pixel widths.

// WRONG: all bars the same height
I(spark, { type: "frame", width: 3, height: 24, ... })  // × 10 identical ops
// Equal heights communicate nothing. Vary heights to show the trend shape.

// WRONG: 12–16 bars at 2px each
// They collapse to hairlines at this size. 3px per bar, 10 bars maximum in 60px.

// WRONG: sparkline with axes and labels
// A sparkline is a trend indicator, not a chart. No axes, no x-labels, no tooltip.
```

---

## Data table

### Archetype overrides

Full node tree and ops are in `references/chart-anatomy.md` (Data table section). Apply these overrides on top:

```
// Override 1: No alternating row fills — dividers only
TableRow=I(tableBody, {
  ...,
  stroke: { color: "$border", thickness: 1 }  // bottom border only
  // Do NOT use fill: "$surfaceMuted" on alternating rows.
  // Alternating fills compete with status badge colours. Dividers are cleaner.
})

// Override 2: Status cells — dot + text, not background pill
StatusCell=I(row, {
  type: "frame", name: "StatusCell",
  layout: "horizontal", alignItems: "center", gap: 6,
  width: 100, height: "fill_container"
})
statusDot=I(statusCell, {
  type: "frame", name: "StatusDot",
  width: 6, height: 6, cornerRadius: 3, fill: "$positive"
})
statusLabel=I(statusCell, {
  type: "text", name: "StatusLabel",
  content: "Active", fontFamily: "$fontUI",
  fontSize: "$textSm", fill: "$textSecondary"
})
// Dot + text reads faster than a background pill at table density.
// Background pills in analytics tables look like UI controls, not data.

// Override 3: Plan/tier cells — single-letter monogram chip, not word badge
planChip=I(row, {
  type: "frame", name: "PlanChip",
  layout: "horizontal", alignItems: "center", justifyContent: "center",
  width: 24, height: 20, cornerRadius: 4,
  fill: "$surfaceMuted"
})
planInitial=I(planChip, {
  type: "text", content: "P",
  fontFamily: "$fontMono", fontSize: 11,
  fontWeight: 600, fill: "$textSecondary"
})
// "P" for Pro, "F" for Free, "T" for Trial.
// A word badge ("Pro") at table density takes 40–50px and competes with data.
// A monogram chip reads in 24px.
```

### Critical rules (analytics-dashboard specific)

- Row height: 40px desktop-only, 44px if touch interaction is likely.
- All numeric columns: `fontFamily: "$fontMono"`, right-aligned.
- Primary text column: `fontFamily: "$fontUI"`, left-aligned, `fill: "$textPrimary"`.
- Secondary columns: `fill: "$textSecondary"`.
- Timestamps: `fontFamily: "$fontMono"`, `fill: "$textMuted"`, right-aligned.

### What generic looks like

```
// WRONG: all columns fill_container (widths become random)
// Fixed widths for status (100px), plan chip (40px), timestamps (120px),
// numbers (80px). Only the primary name/label column uses fill_container.

// WRONG: status as text-only with colour change
statusLabel=I(row, { content: "Active", fill: "$positive" })
// Colour alone fails accessibility. Always dot + text, or background + text.

// WRONG: full-opacity alternating fills ("zebra striping")
// The alternating colours compete with status badge colours in adjacent cells.
// Use row dividers instead.
```

---

## Empty state

### Anatomy

```
EmptyState (frame, fill_container x fit_content, layout: vertical,
             alignItems: center, justifyContent: center,
             gap: 12, padding: [48, 24],
             fill: "$surface",
             stroke: { color: "$border", thickness: 1 },
             cornerRadius: 8)
├── EmptyIcon (icon_font, 32 x 32, iconFontFamily: "lucide",
│              iconFontName: "bar-chart-2", fill: "$textMuted")
│   // Single muted icon. No illustration, no mascot scene.
├── EmptyHeading (text, $textBase, fontWeight: 600, $textPrimary,
│                 content: "No events tracked yet",
│                 textAlign: center)
│   // Name what's missing. Not "It's quiet here".
├── EmptyBody (text, $textSm, $textSecondary,
│              content: "Send your first event and it'll appear here.",
│              textAlign: center, width: 280)
└── EmptyCTA (frame, fit_content x 32, layout: horizontal, alignItems: center,
               gap: 6, padding: [0, 12], cornerRadius: 6,
               fill: "$accent")
    └── CTALabel (text, $textSm, fontWeight: 500, fill: "$surface",
                   content: "Send a test event")
    // One CTA. Not three buttons offering Import / Create / Explore Demo.
```

### Critical rules

- Skip the illustration. A muted icon is enough.
- Heading names what's missing: "No events tracked yet", "No users this period", "No API keys configured".
- Body says what to do next in one sentence.
- One CTA. The action should be the obvious next step, not a menu of options.

### What generic looks like

```
// WRONG: illustrated mascot empty state
// A character holding an empty box, "It's quiet here!", three buttons, confetti shapes.
// Costs 8+ ops, communicates nothing specific, looks like a landing page not a data tool.

// WRONG: three CTAs (Import / Create / Explore Demo)
// A user looking at an empty events table has one job: send an event.
// Give them one button.

// WRONG: empty state with no icon and no copy
// A blank white card with a faint dashed border is not an empty state — it is a broken layout.
```

---

## Microcopy library

Write microcopy in this register: confident, terse, present-tense. The product knows things and says them plainly.

### Metric labels (KPI cards)

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Monthly Active Users | Monthly active users |
| Total API Requests | API calls |
| Error Rate (%) | Error rate |
| Average Response Time | P95 latency |
| Number of New Signups | New users |

Lowercase except proper nouns. Short enough to skim in 200ms.

### Empty states

| Context | Heading | Body | CTA |
|---------|---------|------|-----|
| No events | No events tracked yet | Send your first event and it'll appear here. | Send a test event |
| No users this period | No active users | Nobody matched the selected filters. | Clear filters |
| API key not configured | SDK not connected | Install the SDK and add your write key to start collecting data. | View setup guide |
| Query returned nothing | No matching results | Adjust your filters or date range. | Reset filters |
| Chart loading failed | Couldn't load data | Check your connection and retry. | Retry |

### Delta labels

| Condition | Label | Colour |
|-----------|-------|--------|
| Up, positive signal | +18% | `$positive` |
| Down, negative signal | −4.2% | `$negative` |
| No change | 0.0% | `$textMuted` |
| Up, but ambiguous (e.g. error rate rose) | +18% | `$negative` |
| Insufficient data | — | `$textMuted` |

Always include the sign (+/−). Never just "18%". The sign is the data.

### Loading and error states

- Loading KPI: skeleton frame at the exact dimensions of the value (not a spinner).
- Loading table: skeleton rows at row height, column widths matching the live table.
- Error: "Couldn't load [thing]. Retry", not "Something went wrong" or "Oops!".
- Timeout: "Request timed out. Retry". Name the cause.

### Section and page titles

One to three words. No verbs. No superlatives.

| Generic | This archetype |
|---------|----------------|
| Performance Dashboard | Overview |
| User Analytics & Insights | Users |
| API Request Monitoring | API |
| Your Amazing Dashboard | Dashboard |

---

## Verification checklist

Run this after every build. Each item has a WHY. The reason matters for adjacent cases the checklist doesn't cover.

### Structure

- [ ] **Page uses horizontal layout with sidebar left and main content right.**
  WHY: Sidebar on the right is unusual enough to feel like a bug. Left sidebar is universal in data tools and sets the user's spatial expectation before the data appears.

- [ ] **Sidebar width is 220px (range: 200–240px).**
  WHY: Wider sidebars consume content space without adding navigation utility. 280px eats 4% more of a 1440-wide canvas: 60px of chart width across every card in the layout.

- [ ] **Top bar height is 56px.**
  WHY: Consistent with sidebar header height. They visually lock to the same horizontal line. Below 48px: controls feel cramped. Above 64px: top bar competes with KPI row for vertical space.

### Sidebar

- [ ] **Active nav item has a 2px accent border, not a filled background.**
  WHY: A filled pill claims territory. In this archetype the content is dominant; the nav is subordinate. A 2px border marks position without claiming visual weight.

- [ ] **Section labels are uppercase, 11px, letterSpacing 0.06em, `$textMuted`.**
  WHY: Section labels are structural metadata, not content. Muted colour and small caps keep them legible without competing with nav item labels.

- [ ] **No drop shadow on the sidebar right edge.**
  WHY: Shadows imply elevation. The sidebar is not elevated above the main content; it is flush with it. The 1px `$border` stroke handles separation without implying a layering metaphor that doesn't exist.

### KPI cards

- [ ] **All KPI values use `$fontMono`.**
  WHY: Monospace locks decimal points to the same x-position across all KPI cards in the row. Proportional fonts make "24.7M" and "1,284" drift at different widths. The eye has to re-read each number rather than scan the row.

- [ ] **Delta badge is in `ValueRow` (right-aligned), not in its own row below the value.**
  WHY: Two items in a row (value + delta) = one read. Delta in its own row creates three reads (label, value, delta) and a taller card that takes longer to scan.

- [ ] **Delta uses `$positive` or `$negative`, not `$accent`.**
  WHY: `$accent` is a branding signal; `$positive`/`$negative` are semantic signals. A user conditioned to read `$accent` as "primary action" will misread a delta encoded in `$accent`. They are different communication roles and must use different colours.

- [ ] **No `effect` property on any card.**
  WHY: Drop shadows signal "elevated surface." This archetype's cards are part of the page, not floating above it. Even an 8% opacity, 4px blur shadow makes a card read as marketing-page chrome. The hairline border is the card's boundary; nothing else should be.

### Charts

- [ ] **Bar chart: most recent bar at full opacity, prior bars at 60%.**
  WHY: Full-opacity bars on every period implies all periods are equally relevant. In an analytics tool, the current period is the reference point; prior periods are context. The opacity gradient encodes that hierarchy without a legend.

- [ ] **Sparkline bars have explicit pixel widths (3px), not `fill_container`.**
  WHY: `fill_container` at 60px wide with 10 bars produces 6px-wide bars before gaps: still a loading skeleton. The correct measurement is 3px × 10 bars + 2px × 9 gaps = 48px in a 60px frame. Each bar must be explicitly sized.

- [ ] **All numeric table cells use `$fontMono` and are right-aligned.**
  WHY: Right-aligned monospace numbers let the eye scan a column and compare values by their decimal positions. Left-aligned proportional numbers require reading each value individually. The column becomes unreadable for comparison.

### General

- [ ] **No raw hex values in any op.**
  WHY: Raw hex bypasses the token system. Dark mode, theme switching, and brand updates all fail when hex values are hardcoded. Every colour comes from a variable.

- [ ] **`$accent` appears in at most 3 visual locations in the entire design.**
  WHY: An accent that appears everywhere is not an accent; it becomes the base colour. The signal strength of the accent comes from scarcity. Restrict it to chart bars, the primary CTA, and the active nav indicator.

- [ ] **`$bg` is `$FAFAF9` (off-white), not pure white (`#FFFFFF`).**
  WHY: A pure white background at 1440px wide feels clinical and harsh at high brightness. Off-white reduces contrast fatigue for users who live in the dashboard for hours. The card fill (`$surface`) is white, so the off-white `$bg` creates the card lift without a shadow.

---

## Contrast examples

### Example 1: KPI card (correct vs generic)

**Correct:**

```
kpiCard=I(kpiRow, {
  type: "frame",
  layout: "vertical", gap: 8, padding: [16, 16, 12, 16],
  fill: "$surface",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 8
  // No effect property.
})
metricLabel=I(kpiCard, { type: "text", content: "API calls",
  fontFamily: "$fontUI", fontSize: "$textSm", fill: "$textMuted" })
valueRow=I(kpiCard, { type: "frame", layout: "horizontal",
  alignItems: "center", justifyContent: "space_between", width: "fill_container" })
metricValue=I(valueRow, { type: "text", content: "24.7M",
  fontFamily: "$fontMono", fontSize: "$text2xl", fontWeight: 600, fill: "$textPrimary" })
delta=I(valueRow, { type: "text", content: "+18%",
  fontFamily: "$fontMono", fontSize: "$textXs", fill: "$positive" })
```

Why this is right: hairline border, no shadow, monospace value, delta beside (not below) the value, semantic green for positive delta.

**Generic (what the AI produces by default):**

```
kpiCard=I(kpiRow, {
  type: "frame",
  layout: "vertical", gap: 16, padding: [24, 24],
  fill: "$surface",
  cornerRadius: 12,
  effect: [{ type: "drop_shadow", blur: 12, y: 4, opacity: 0.1 }]  // WRONG: shadow
})
metricLabel=I(kpiCard, { type: "text", content: "API Calls",  // WRONG: title case
  fontFamily: "$fontUI", fontSize: "$textBase", fill: "$textPrimary" })  // WRONG: label too prominent
metricValue=I(kpiCard, { type: "text", content: "24.7M",
  fontFamily: "$fontUI",  // WRONG: proportional font
  fontSize: "$text3xl", fontWeight: 700, fill: "$textPrimary" })
delta=I(kpiCard, { type: "text", content: "+18%",  // WRONG: delta in its own row below value
  fill: "$accent" })  // WRONG: accent not semantic colour
```

Why this is wrong: shadow makes it read as a marketing card, not a data card. Proportional font misaligns columns. Title-case label competes with value. Delta in its own row creates three reads. Accent colour on a semantic signal erases the semantic meaning.

---

### Example 2: Sidebar active state (correct vs generic)

**Correct:**

```
activeItem=I(nav, {
  type: "frame", name: "NavItem_Active",
  layout: "horizontal", alignItems: "center",
  width: "fill_container", height: 32,
  gap: 8, padding: [0, 8], cornerRadius: 6
  // No fill property — background matches the sidebar fill.
})
indicator=I(activeItem, {
  type: "frame", name: "ActiveIndicator",
  width: 2, height: 20, fill: "$accent"
})
activeIcon=I(activeItem, {
  type: "icon_font", iconFontFamily: "lucide", iconFontName: "bar-chart-2",
  width: 16, height: 16, fill: "$accent"
})
activeLabel=I(activeItem, {
  type: "text", content: "Overview",
  fontFamily: "$fontUI", fontSize: "$textSm",
  fontWeight: 500, fill: "$textPrimary"
})
```

Why this is right: 2px left border in accent with slightly brighter label. The sidebar recedes; content dominates.

**Generic (what the AI produces by default):**

```
activeItem=I(nav, {
  type: "frame", name: "NavItem_Active",
  layout: "horizontal", alignItems: "center",
  width: "fill_container", height: 36,
  gap: 8, padding: [0, 8], cornerRadius: 8,
  fill: [{ type: "color", color: "$accent", opacity: 0.15 }]  // WRONG: filled pill
})
// No ActiveIndicator frame — the pill IS the active state
activeIcon=I(activeItem, {
  type: "icon_font", fill: "$accent"  // Icon matches the pill fill, over-emphasised
})
activeLabel=I(activeItem, {
  type: "text", content: "Overview",
  fontFamily: "$fontUI", fontSize: "$textSm",
  fontWeight: 600, fill: "$accent"  // WRONG: accent label + accent pill + accent icon
})
```

Why this is wrong: a filled pill in the accent colour makes the sidebar the loudest element on the page. The main content (where the data is) becomes secondary. The active item should whisper, not shout.
