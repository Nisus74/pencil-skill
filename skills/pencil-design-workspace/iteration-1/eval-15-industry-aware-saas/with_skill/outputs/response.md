# Dashboard for a developer-tools SaaS

Before I touch the canvas, I want to commit to a stance. The brief — *developer-tools SaaS, professional engineers, make it feel right for them* — maps cleanly to a specific sub-family in the SaaS industry catalogue, and that catalogue tells me what the audience expects rather than what feels generic-safe.

## What I consulted in the skill

I read `SKILL.md` end-to-end first, then loaded three references that the deviation table explicitly points at for this kind of brief:

- **`references/industry-patterns.md`** — because the brief names an industry (SaaS) and a sub-category (developer tools). The catalogue gives me default style, palette, fonts, density, must-have completeness screens, and the SaaS pressure test.
- **`references/data-viz.md`** — because *dashboard* implies KPI cards, charts, and tables, and this file owns the 25-chart selection matrix, colour-blind-safe palettes, and the three dashboard tile shapes.
- **`assets/examples/example-dashboard.md`** — because there's a worked walkthrough of exactly this layout shape, and the skill points at it for any dashboard task.

I did not load `mobile-patterns.md`, `forms.md`, or `flows.md` — none of them match the brief. I will hold `references/states.md` in reserve; the SaaS pressure test demands states, and I'll need it once the happy-path layout is locked.

## The atmosphere I'm committing to

Per the aesthetic-defaults rule in the skill, I have to name a vibe before I plan. For a dev-tools dashboard:

> **Dense. Symmetric. Static.**

That stance comes from `industry-patterns.md` § SaaS § Developer tools verbatim — *dense, monospace-friendly, terminal-aesthetic OK, keyboard-first*. Engineers spend eight-hour sessions in these surfaces; airy marketing-page chrome wastes their pixels and reads as condescending. Static (not fluid) because motion-heavy dashboards distract from the numbers; the engineer wants the chart to be where it was when they last looked.

## Style, palette, and fonts

Drawn straight from the SaaS § Developer tools recommendations:

- **Style:** Swiss / International with a Terminal / Hacker accent. Strict grid, minimal chrome, monospace where it earns its place (timestamps, IDs, version strings, latency values).
- **Palette:** Cursor Dark or Linear Dark recipe. Dark-mode-first — the skill's industry rules are explicit that *dark mode shipped by default; users expect it, especially in developer tools*. I'd still ship a light-mode variant via the `mode` theme axis (the discipline rule is non-negotiable), but the canonical screenshot lives in dark.
- **Fonts:** Geist + Geist Mono. The skill bans Inter as the default in the aesthetic-defaults section; Geist reads as deliberate without being eccentric. JetBrains Mono is the alternative if the project's `tokens.md` already pins it.
- **Tabular numerics everywhere a number sits in a column.** KPI values, latency cells in tables, timestamps. This is in the typography defaults and the data-viz file both.

## What I'd actually build

### Step 1: Detect host and locate context

I'd call `get_editor_state({ include_schema: false })` first. If the host isn't connected I stop and tell the user to open Pencil — no silent CLI fallback. Assuming it succeeds, I check whether a `.pen` is open, what's selected, and whether the project has a `design-system/` folder with `visual-style.md`, `tokens.md`, and `data-viz.md` populated. If those files exist they override every default I just named — the Discipline rule on themes and the design-system convention are both clear that committed project tokens beat agent recommendations.

If the project has no `design-system/`, I'd offer to scaffold it once (the skill's failure-mode #3 wording), including `data-viz.md` as an optional Tier 2 template since this is explicitly a dashboard project.

### Step 2: Inventory components

Per the Components-first rule, before I draw anything I'd run two scans:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "<each .lib.pen in imports>", patterns: [{ reusable: true }], readDepth: 2 })
```

I'm hunting for `Sidebar`, `KPICard`, `LineChart` / `Chart`, `TableTile`, `Button`, `Badge`, `Input`, `CommandPalette` (or similar). If `KPICard` exists, I instantiate it via `ref` rather than rebuilding from a frame + text + sparkline. If only the Linear-style atoms exist and there's no `KPICard`, I'd flag that the pattern looks reusable and offer to extract it to the `.lib.pen` after the first instance.

### Step 3: Token bootstrap — only if needed

`get_variables()` first. If the document already has tokens, I use them. If empty, I'd declare the `mode: ["light","dark"]` axis and seed the neutral five (`surface`, `surfaceMuted`, `border`, `textPrimary`, `textMuted`) plus one accent (`accent`) plus chart series tokens (`$chart1`–`$chart8`) bound to Okabe-Ito hex values, per `data-viz.md`. Both light and dark values for every colour. No bare `#000` or `#FFF` for surfaces — `surface` resolves to Zinc-950 in dark, `#FAFAFA` in light.

### Step 4: Plan the tree out loud

Before any `batch_design` call I'd state the plan:

> *Single 1440 × 900 frame named `Dashboard_Desktop`. Sidebar (240px, fixed) + main column. Main column has four sections stacked: header strip with breadcrumb + ⌘+K invocation hint + user avatar; KPI row with 4 cards (Build success rate, p95 build duration, Deploy frequency, Open incidents); a 2-column chart grid (Build duration trend over 30 days as a line chart; Deploys by environment as a stacked bar); a full-width table tile of recent builds. Section gap 24px, padding 32px, sidebar gap 0.*

Naming the layout out loud is the deviation table's rule for any non-trivial brief; it surfaces bad assumptions cheaply. The user gets a chance to redirect before I burn ops.

### Step 5: Execute with `batch_design`

I'd find empty canvas space first since real projects rarely have an empty canvas:

```
find_empty_space_on_canvas({ width: 1440, height: 900 })
```

Then a first `batch_design` call building the outer frame, sidebar ref, main column, and the KPI row skeleton (≤25 ops). A second call fills the chart tiles. A third call fills the table tile. The skill is explicit that cramming 60 ops into one call invites ordering bugs.

The KPI metrics I'd pick are the ones engineers actually scan a dev-tools dashboard for — not generic *Revenue / MRR / Active users / Churn* (those are the analytics-SaaS defaults from the worked example, and would betray the audience):

- **Build success rate** — `98.4%`, delta `+0.6%` over 7d, sparkline of last 30 builds.
- **p95 build duration** — `4m 12s`, delta `-18s` (a *lower* delta is good here, so the down arrow gets `$success`, which the table cell would document in `context`).
- **Deploys today** — `47`, delta `+12 vs yesterday`, sparkline of hourly deploys.
- **Open incidents** — `2`, delta `-1 since yesterday`, no sparkline (incident counts don't trend meaningfully at small numbers; a sparkline would be noise).

Each KPI uses a `KPICard` `ref` with `descendants` for the four slot keys. Values use `font-variant-numeric: tabular-nums` (documented in the card's `context`), the delta pairs an arrow shape with the colour token, and the sparkline lives in the card's sparkline slot.

### Step 6: Charts

Per `data-viz.md` § the 25-chart selection matrix:

- **Trend over time → line chart.** Build duration over 30 days. Single series (current period); optional dashed second series for prior period. Direct end-of-line label, light gridlines on the y-axis only, axis labels at every 100ms, no legend.
- **Composition + comparison across categories → stacked bar.** Deploys per environment (production / staging / preview), grouped by day for the last 14 days.

Both render inside `ChartTile` refs with header + body + footer slots. I'd document in each tile's `context` that the rendering library (Recharts or visx) lives in code; the `.pen` shows shape and layout, not the rendered chart. The chart `context` also names the data shape, the `$chart1` / `$chart2` tokens used, and the skeleton-with-axis-hints loading pattern from `data-viz.md`.

I would *not* use:
- Pie / donut for environment split (it would have ≤ 5 slices so it's technically allowed, but stacked bar lets the engineer compare totals across days).
- Dual y-axis for *build duration vs deploy count* (the skill bans this — small multiples instead).
- A gauge for build success rate (poor ink-to-data ratio; the big-number with sparkline does the job).

### Step 7: The recent-builds table

Full-width `TableTile` ref. Columns: Status (icon + label, never icon-only — pairs colour with shape per the accessibility baseline), Branch, Commit (mono short-hash, e.g. `a3f2c91`), Author, Duration, Triggered. Sort by Triggered descending by default. Virtualised after 50 rows (per `performance-design.md`, which I'd load if I were going deeper). Time column shows relative by default (`2m ago`) with absolute on hover.

### Step 8: Industry must-haves I'd add or surface

The SaaS § Developer tools rules list non-negotiables that a *just the dashboard* design will miss. I'd surface these to the user explicitly rather than silently skip them:

- **⌘+K command palette is table-stakes.** I'd at minimum show its invocation hint in the header strip (`⌘ K` chip, with a non-breaking space binding the keys per the typography rules) and either include the open palette as an overlay state on a sibling frame or note it as the next screen to design.
- **Keyboard shortcuts surfaced in tooltips and a `?` keyboard-help overlay.** Not optional for this audience.
- **Dark mode default; light mode tested.** Already covered by the theme axis discipline rule.
- **Empty / loading / skeleton states per tile.** From the SaaS pressure test: *if the file does not show empty states, loading states, and error recovery, it is not comprehensive — it is a sales demo.* I'd build the skeleton variant of each KPI card and the chart tiles in a sibling `UXStates` section, plus an empty state for the activity table (worded actively per the microcopy rule: *"No builds in the last 24 hours. Push to a tracked branch to trigger one."* — not *"No data."*).
- **No-permission and plan-restricted variants** of the same dashboard. I'd flag these as the next screens once the canonical view is locked.

### Step 9: Verify

Walking the verification ladder, not jumping to screenshots:

1. **`batch_design` response** — confirms ops landed.
2. **`snapshot_layout(parentId: "<dashboard-frame-id>", maxDepth: 3)`** — confirms the sidebar is 240px, the KPI row has gap 16, the chart row sits in two equal columns with gap 24, and the activity table is full-width. Numbers, not pixels.
3. **`batch_get({ nodeIds: ["<KPICard-instance-1>", "<ChartTile_BuildDuration>"] })`** — confirms the `descendants` slot fills resolved (the value text is what I asked for, the sparkline ref is bound, the chart's `$chart1` token resolved).
4. **`get_screenshot(nodeId: "<dashboard-frame-id>")`** — *one* screenshot, scoped to the dashboard frame, in the canonical dark mode. I'd skip a second light-mode screenshot because every colour is bound to a variable with both theme values (the variable system guarantees the swap, per the skill's dual-mode rule). I'd only re-screenshot if `batch_get` showed a raw hex snuck through.

When I scan that screenshot, the order is: layout integrity → spacing rhythm → type rhythm → contrast (body text against `$surface` ≥ 4.5:1, both modes) → component fidelity (sidebar matches the library, KPI cards match each other, chart tiles align).

### Step 10: Self-critique gate

Before declaring done, the four-question gate from the aesthetic defaults:

1. *Could a non-designer recognise this as a dev-tools brand?* — the monospace timestamps, the `⌘ K` chip, the `Build success rate` KPI rather than `Revenue`, the dense Zinc-950 surface — yes, it reads as *Linear / Vercel / Cursor* before it reads as *generic SaaS*.
2. *Where does the eye go first / second / third?* — KPIs (the at-a-glance state of the system), then the build-duration trend (is it getting slower?), then the activity table (what just happened?). That matches what an engineer opens this dashboard to find out.
3. *What's decorative-only?* — I'd remove anything that doesn't earn its pixels. No hero illustration. No gradient borders. The accent colour appears on exactly one CTA and the active sidebar item.
4. *What single change would make this less AI-generated?* — pinning real data (`a3f2c91` commit hashes, `prod-us-east-1` environment names, plausible service names like `api-gateway` rather than `Service A`) is the highest-leverage one. *Filler hero copy* and *fabricated metrics* are both in the anti-patterns list.

## What I'd hand back

A single `Dashboard_Desktop` frame in the `BuildReady` section of the canvas, sidebar + KPI row + chart pair + activity table, dark-mode canonical with light-mode tested via the variable system, every node named in PascalCase with a `context` documenting data source / loading behaviour / accessibility role, and a one-paragraph summary naming the industry stance, the components instantiated, and the must-have states still to design (empty / loading / error / no-permission / plan-restricted).

I'd also flag — once — that a real dev-tools SaaS design needs the ⌘+K palette, the `?` keyboard-help overlay, the build-detail screen this dashboard links into, and the incident-detail screen the *Open incidents* KPI links into. Building one dashboard frame in isolation passes the *can the user see what the product does* test; it fails the SaaS pressure test from `industry-patterns.md`. I'd offer to design the next screen rather than declare the project done.
