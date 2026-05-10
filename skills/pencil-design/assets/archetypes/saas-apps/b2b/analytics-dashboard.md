# analytics-dashboard

> Data-led overview surfaces where every visible element earns its pixels through measurable insight.

**Surface category:** saas-apps/b2b
**Confidence:** inferred from public knowledge of Mixpanel, Amplitude, PostHog
**Exemplars:** Mixpanel, Amplitude, PostHog (free-tier dashboards)

## When to choose this archetype

Pick this when the user is silent on aesthetics and the product's job is *making numbers legible*. The user lives inside this surface daily, scans for anomalies in seconds, and wants the chrome to disappear so the data speaks. Avoid when the dashboard is occasional or executive-summary; `consumer-productivity` or a future `soft-overview` archetype suits those. If the user has supplied their own direction, follow that instead and use this file only as scaffolding for the parts they didn't specify.

## Typography

- **Display and numerals:** `Geist Mono` or `JetBrains Mono` for KPI values, table figures, axis labels. Numerics must be monospace so columns of figures align.
- **UI and labels:** `Geist` or `Satoshi` 13–14px for body, 11px small caps with 0.04em tracking for column headers and section labels.
- **Headings:** sparing. H1 sits on the page title at 24px/600. Section headers convert to small-caps labels.
- **Pairing rule:** mono numerals *inside* sans labels, never the other way.

## Density

- Spacing scale: 4 / 8 / 12 / 16 / 24. Skip 32+ unless separating major page regions.
- Card padding: 16–20, not 24+. Table row padding 8–12 vertical.
- Line-height: 1.4 for body, 1.1–1.2 for headings, 1.0 for monospace numerals.

## Accent strategy

- One accent. It appears in: chart bars (one fill, opacity-stepped for stacked series), KPI delta arrows, primary CTA, link affordances. Nowhere else.
- Avoid the violet default. Stronger pulls: a deep desaturated colour like ink, sage, terracotta, slate-blue. Saturation under 70%.
- Positive and negative deltas use semantic colours (`$positive`, `$negative`), not the brand accent.

## Surface treatment

- Hairline borders, not shadows. 1px borders at `$borderSubtle` (Zinc-200 light, Zinc-800 dark) for cards and tables. Shadows are an anti-cue here.
- Card corner radius: 6–10. No pills, no fully-rounded.
- Background hierarchy: `$bg` (page) > `$surface` (cards) > `$surfaceMuted` (table headers, section dividers). Three levels max.

## Data display

- Bar charts default, not line. Lines only when continuous time matters more than discrete comparison. Per Pencil's Graphs guideline, bars use flex layout with no absolute positioning over the chart.
- Sparklines render as actual mini-charts (12–14 thin bars), never as decorative coloured blocks under a value.
- Tables are the workhorse. Always `frame → cell frame → cell content`. Row separators are 1px borders, not zebra stripes. Hover state is `$surfaceMuted` on the row, not a colour shift.
- Numeric formatting: thousand separators always. Percentages to 1 decimal. Trends shown as delta + percent + arrow icon.

## Microcopy and voice

- Confident, terse, present-tense. "MAU climbed 12%" beats "Monthly active users showed an increase of 12% over the period."
- Empty states name what's missing and the next action: *"No events tracked yet. Send your first one →"*. Avoid "It's quiet here" or illustration-heavy emptiness.
- Loading states are skeleton bars matching the final shape, not spinners.
- Error states: short cause, then retry. *"Couldn't load events. Retry"* beats apology theatre.

## Motion personality

- Instant. No animations on data updates. Numbers just change. Charts redraw without count-up animation that delays comprehension.
- Allowed: 120–160ms ease-out on hover, dropdown opens, tooltip reveals. Nothing else.
- Anti-cue: count-up KPI animations, chart line tracing on entry, sparkline pulse.

## Anti-cues (don't reach for these in this archetype)

- Cards with shadows and no borders (reads as marketing-page leakage).
- Decorative gradients on KPI cards.
- Avatar groups in headers (this is a tool, not a social product).
- Three-column "feature card" grids on empty states.
- Round-cornered table cells.
- "Insights" callout cards summarising the chart you're already looking at.
- Emoji in any data label.
- Count-up animation on KPI values when the page first loads.

## Worked example: SaaS analytics overview

The dashboard from `pencil-new.pen`, redone in this archetype:

- Sidebar drops the "Pro workspace" subtitle, becomes pure nav. Active state is a 2px left border in accent, not a soft-violet pill.
- Top bar loses the gradient Invite button. It becomes a hairline-bordered secondary action with the accent applied to text only.
- KPI cards lose the violet sparklines beneath each value. Mono numerals sit beside the delta chip, not above it. Sparklines move to a single dedicated trend card.
- The trend chart's bars use one colour with the latest day at full opacity and prior days at 60%, instead of pale-and-strong contrast.
- Top events list: mono numerals right-aligned, a thin progress bar at full width below. Labels and values read as the same row of data, not separate columns.
- Recent users table: row borders only, no shadows. Status pills become inline coloured dots with text. Plan badges become one-letter monogram chips (P / F / T) instead of word badges.

## Notes for AI implementers

Tokens this archetype implies (illustrative; rename to project's scheme):

| Token | Value |
|---|---|
| `$accent` | Deep ink (`#1F2937`) or a saturated brand variant. Not violet by default. |
| `$bg` | Off-white (`#FAFAF9` light, `#0C0A09` dark). Never pure white or black. |
| `$surface` | One step warmer than `$bg`. |
| `$surfaceMuted` | Table headers, section dividers. |
| `$borderSubtle` | Zinc-200 / Zinc-800 hairline. |
| `$fontUI` | `Geist` or `Satoshi`. |
| `$fontMono` | `Geist Mono` or `JetBrains Mono`. |

Components most affected: `KPICard`, `BarChart`, `TableRow`, `Sparkline`, `DateRangeSegmented`. Each gets a variant inside this archetype.

Common slip-ups:

- Reaching for shadows when "the cards feel flat". The flatness is the point.
- Adding count-up animation because the numbers feel inert. They aren't inert; the data updates plenty.
- Using the brand accent for positive deltas. Use `$positive` instead.
- Letting the AI default to violet because Tailwind's preset says so.
