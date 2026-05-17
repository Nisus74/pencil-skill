# SaaS Dashboard in Pencil: Design Spec

**File:** `pencil-new.pen`
**Domain:** Product analytics SaaS (Mixpanel/Amplitude-lite)
**Visual direction:** Light surface with bold violet accent
**Scope:** Single overview screen, ~1440×900

## Layout

Two-column shell.

- **Sidebar:** 240px. Workspace switcher at top, nav list, account footer.
- **Main area:** top bar, page header with date range, KPI row, chart row (2/3 + 1/3), recent users table.

Vertical stack inside the main area, gap 24, padding 32. The chart row uses horizontal flex with the trend chart on `fill_container` (~2/3) and the breakdown on a fixed share (~1/3).

## Components (built reusable, in this order)

1. **NavItem.** Icon + label + active state. Active uses `--accent-soft` background and `--accent` for icon/text.
2. **KPICard.** Label (Small), value (Numeric 32/600), delta chip (`--positive` or `--negative` background tint), placeholder sparkline frame at the bottom.
3. **BarChart.** Flex-layout bars per Pencil's Graphs rules (no absolute positioning over the chart, labels via layout). Vertical bars, `--accent` fill, x-axis labels below.
4. **TableRow.** Strict `frame → cell frame → cell content` hierarchy. Cells use `fill_container` with column weights.
5. **DateRangeSegmented.** Four segments: 7d / 30d / 90d / Custom. The active segment uses `--surface` over a `--bg` track with a subtle shadow. Default active: 7d.
6. **Avatar.** Circular frame with `--accent-soft` fill and the initial as text in `--accent`. Used inside the TableRow's user cell.

## Tokens (Pencil variables)

| Variable | Value |
|---|---|
| `--bg` | `#FAFAF9` |
| `--surface` | `#FFFFFF` |
| `--border` | `#E7E5E4` |
| `--font-primary` | `#1C1917` |
| `--font-secondary` | `#78716C` |
| `--font-tertiary` | `#A8A29E` |
| `--accent` | `#7C3AED` |
| `--accent-soft` | `#F3EBFF` |
| `--positive` | `#16A34A` |
| `--negative` | `#DC2626` |
| `--radius-sm` / `--radius-md` / `--radius-lg` | 6 / 10 / 14 |

Spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 48.
Type: Inter. H1 28/600, H2 18/600, Body 14/400, Small 12/500, Numeric 32/600.

## Content

- **Sidebar nav:** Overview (active), Events, Funnels, Cohorts, Users, Settings.
- **Top bar:** workspace switcher (left), search input (centre), date pill + notifications + avatar (right).
- **Page header:** "Overview" plus DateRangeSegmented.
- **KPIs:** MAU 48,210 (+12.4%), DAU 7,842 (+3.1%), Conversion 4.6% (-0.2%), Retention (D30) 38% (+1.8%).
- **Trend chart:** "Active users, last 7 days", 7 bars.
- **Top events:** horizontal bar list of `signup_completed`, `event_tracked`, `dashboard_viewed`, `report_exported`, `invite_sent`. Counts plus relative bars.
- **Table:** "Recent users". Columns: User (avatar + name + email), Plan (badge), Last seen, Events (7d), Status. ~6 rows.

## Build order (live in Pencil)

1. Set Pencil variables via `set_variables`.
2. Mark the existing top-level frame `bi8Au` as the dashboard screen: rename, set `placeholder: true`, size 1440×900, background `--bg`.
3. Build reusable components off-canvas, using `find_empty_space_on_canvas` to the right of the screen.
4. Compose the screen using component instances:
   a. Sidebar (vertical layout, `--surface` background, right border)
   b. Main column (vertical layout, padding 32, gap 24)
   c. Top bar, then page header, KPI row, chart row, table.
5. Snapshot the layout after each major section.
6. Screenshot the whole screen once after compose, critique, polish, screenshot again.
7. Unset `placeholder: true` once the screen is done.

## Out of scope

- Empty, loading, and error states. The skill treats these as a separate concern; they're not part of this single overview frame.
- Mobile and responsive variants.
- Onboarding overlay.
- Light/dark theming variants. The spec assumes a single light theme.

## Success criteria

- The final screenshot reads as a coherent SaaS analytics overview at a glance: where am I, what's healthy, what's changed, where to look next.
- Violet appears intentionally and sparingly: chart fill, active nav, KPI deltas, primary CTA. It doesn't show up as decorative colour anywhere else.
- Layout uses Pencil flex correctly: no `x`/`y` on flex children, `fill_container` for proportions, no hardcoded text widths.
- All `frame → cell → content` table rules are satisfied.
