# SaaS analytics dashboard — design plan

Before I touch the canvas, I'm walking the skill's seven-step workflow. This response describes the tools I'd call, the shape of each response I'd expect, and the design decisions I'd take. I cannot actually call `mcp__pencil__*` tools in this isolated run, so this is a plan-and-talk-through rather than a live build.

## References I consulted from the skill

- **`SKILL.md`** — the seven-step default workflow, discipline rules (naming, context, components-first, themes, responsive, accessibility, design completeness), aesthetic defaults, the verification ladder, failure modes.
- **`assets/design-system/data-viz.md`** — categorical and sequential palette structure (`$chart-1..8`, `$chartSeq-50..900`), default chart-type-by-question table, the dashboard-tile lockup (header → big-number → delta → chart), the four chart states (loading / empty / error / partial). This is the load-on-demand template the skill scaffolds for chart-bearing projects, and the dashboard task hits every one of its decisions.
- **`references/mcp-tools.md`** — `get_guidelines` category guidance (for a SaaS dashboard, that's `Web App` + `Table` + optionally `Tailwind` + `Design System`), the cookbook calls for `get_variables` / `set_variables`, the cost cheatsheet that tells me to lean on `snapshot_layout` over `get_screenshot`.
- **`references/batch-design-grammar.md`** — op syntax (`I` / `C` / `R` / `U` / `G`), the `foo=I(...)` binding pattern, the ≤25 ops chunking rule, the `placeholder: true` discipline on top-level frames, the sizing-string rules (`fill_container` / `fit_content`, no `"100%"`), the padding-array gotcha.
- **`assets/design-system/patterns.md`** — the dashboard-shell page template (TopNav, SideNav, main content with `padding $space-6`, optional right rail), and its rule that one of TopNav/SideNav is primary, not both.
- **`assets/examples/example-login-screen.md`** — closest worked greenfield example. Same skeleton-then-fill rhythm I'll use here, scaled up.

I deliberately did **not** load: `flows.md` (this is a single screen, no multi-screen flow), `states.md` (yes for tile states, but the tile-level coverage already lives in `data-viz.md`), `accessibility.md` (the SKILL baseline covers what I need; a dashboard with paged data isn't doing anything ARIA-exotic).

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Expected response shape: `{ activeDocument: <path | null>, selection: [...], schemaVersion: "..." }`. If this errors with `transport not connected to app: desktop`, I stop and tell the user to open the Pencil desktop app or IDE extension. Do not silently fall back to the CLI.

## Step 2 — Locate context

From the `get_editor_state` result I'd note:

- **Document state.** Is a `.pen` open? If yes, I work in that one (and check its `imports` for any attached `.lib.pen`). If no, I'd ask: *"No `.pen` file is open. Should I (a) open an existing one — give me the path, or (b) create a new one with `open_document('new')`?"* For this plan I'll assume the user wants a new doc.
- **Project filesystem.** A directory listing of the project root looking for `design-system/`. If absent, I'd offer once to scaffold the 12 core templates plus the optional `data-viz.md` (this project clearly ships charts, so `data-viz.md` is opt-in-with-a-strong-recommendation). If declined, proceed without; do not ask again.

For this plan I'll assume `design-system/` exists with the 12 core templates and a `data-viz.md` already present, plus a `design/system.lib.pen` library with at least `Card`, `IconButton`, and `Avatar` components.

## Step 3 — Load guidelines and inventory components

Two parallel reads.

**Guidelines.** First call `get_guidelines()` with no args to discover the live category list, then load:

```
get_guidelines({ category: "Web App" })
get_guidelines({ category: "Table" })
get_guidelines({ category: "Design System" })
```

`Web App` is the default for SaaS product UI; `Table` is essential for tile 4 (Top 10 customers); `Design System` keeps the build aligned with the library. I'd skip `Tailwind` unless `design-system.md` declares the stack.

**Project files.** Read `design-system/README.md`, then `design-system/design-system.md` (for the library path, stack, icon library), `design-system/tokens.md` (spacing, type scale), `design-system/data-viz.md` (chart palettes, tile shape, chart-state rules), and `design-system/patterns.md` (dashboard shell template).

**Component inventory.** Two `batch_get` calls:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

What I'm checking: which of `Card`, `Tile`, `MetricTile`, `IconButton`, `Avatar`, `Badge`, `Tab`, `SegmentedControl`, `Menu`, `Tooltip` already exist. If a `MetricTile` or `DashboardTile` component exists, every tile becomes a `ref` to it with descendants overrides — much cheaper than rebuilding the lockup four times. If only `Card` exists, I'll build the tile internals from primitives but instantiate the outer container as a `ref`. I would not build a one-off card from scratch when a library card exists.

**Token check.** Before any token work:

```
get_variables()
```

I expect a response like `{ surface: { type: "color", value: [...] }, primary: {...}, ... }`. I scan for chart tokens (`$chart-1..8`, `$chartSeq-50..900`). If any are missing, I'll add only the absent ones via `set_variables` with `replace: false`. If `$chart-1` resolves to the user's brand `$primary` already, I keep it. I never re-declare a variable that already exists — that's the token-clobber failure mode.

## Step 4 — Plan (told to user before any write)

Before I touch the canvas I'd say to the user:

> *"I'll build a desktop dashboard at 1440×900 inside a standard dashboard shell — TopNav (56h, brand + breadcrumb + search + account), SideNav primary nav (240w with Overview selected), main content with a page header ('Analytics') and a 4-tile grid below. The tiles, in order: (1) MRR trend — line chart with the current month's MRR as the big-number, monthly delta, and a 12-month line; (2) Conversion by source — horizontal bar chart with the top source as big-number, ranked top-five sources as bars; (3) Cohort retention — heatmap, 8 cohorts × 8 months, sequential palette anchored on `$chartSeq-500`; (4) Top 10 customers by MRR — compact table, customer name + MRR + delta vs last month. Layout: tiles 1 and 2 share row 1 (1fr 1fr), tile 3 spans row 2 full-width (heatmap needs the breathing room), tile 4 spans row 3 full-width (table). All tiles are `ref` instances of your library `Card` (or `MetricTile` if it exists), padded with `$space-6`. Chart colors come from the `$chart-*` and `$chartSeq-*` tokens; if any are missing I'll add the absent ones only — won't touch values you've configured. Atmosphere: balanced, symmetric, static — a dashboard isn't where motion earns its keep."*

That's the moment to catch a wrong assumption cheaply. If the user wanted, e.g., the heatmap above the trend, they'd say so now.

**Atmosphere line (per skill aesthetic defaults):** *Balanced, symmetric, static.* This is a SaaS analytics surface — density should read calm, not dense, and there's no motion brief.

**Layout note:** I'd use `find_empty_space_on_canvas` here only if the user already had other top-level frames on the canvas. For a fresh doc I skip it — the new page goes at origin.

## Step 5 — Execute (planned `batch_design` calls)

Greenfield bootstrap rhythm from `mcp-tools.md`'s composite recipe. I'd plan **four** `batch_design` calls, each ≤25 ops:

### Call A — document setup, theme axis, page skeleton (≤10 ops)

```
U("doc", { themes: { mode: ["light", "dark"] } })
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
page=I(document, { type: "frame", name: "AnalyticsDashboard_Desktop", layout: "vertical", width: 1440, height: 900, fill: "$surface", placeholder: true })
topNav=I(page, { type: "frame", name: "TopNav", layout: "horizontal", height: 56, width: "fill_container", padding: [0, 24, 0, 24], alignItems: "center", justifyContent: "space-between", fill: "$surface", stroke: { thickness: 1, fill: "$border" } })
shell=I(page, { type: "frame", name: "AppShell", layout: "horizontal", width: "fill_container", height: "fill_container", gap: 0 })
sideNav=I(shell, { type: "frame", name: "SideNav", layout: "vertical", width: 240, height: "fill_container", padding: "$space-4", gap: "$space-1", fill: "$surfaceMuted", stroke: { thickness: 1, fill: "$border" } })
main=I(shell, { type: "frame", name: "Main", layout: "vertical", width: "fill_container", height: "fill_container", padding: "$space-6", gap: "$space-6" })
header=I(main, { type: "frame", name: "PageHeader", layout: "horizontal", justifyContent: "space-between", alignItems: "center", width: "fill_container" })
grid=I(main, { type: "frame", name: "TileGrid", layout: "vertical", width: "fill_container", gap: "$space-6" })
```

Then I'd verify the skeleton landed via `snapshot_layout(parentId: "page", maxDepth: 2)` before continuing. Cheap, decisive — confirms `topNav` is 56h, `sideNav` is 240w, `main` is filling, the gap between rows is 24.

If `MetricTile` or `DashboardTile` doesn't already exist in the library, this is also where I'd surface that and ask: *"Worth adding a `DashboardTile` to your `.lib.pen` so the four tiles share an origin? It'd be cheap to do now."* If yes, scope shifts to defining the component first, then instantiating four times. If no or "later", I build the tile lockup inline and flag it as a candidate for extraction.

### Call B — TopNav and SideNav contents (≤20 ops)

TopNav: brand lockup (logo + product name), breadcrumb ("Workspace · Analytics"), spacer, search input (`ref` to library `Input` with leading icon), notification icon button, account avatar. SideNav: section label "Workspace", nav items (`Overview`, `Analytics` selected, `Cohorts`, `Customers`, `Reports`), divider, secondary section label "Settings", nav items (`Integrations`, `Billing`), spacer, user menu at bottom.

Selected nav item gets the strong selection treatment from `patterns.md` — `$primaryMuted` background AND a 3px left accent bar in `$primary`. Subtle hover ≠ selected.

Page header gets: title `Analytics` (`$text3xl`), date-range `SegmentedControl` (`Last 7 days` / `Last 30 days` (selected) / `Last 90 days` / `Custom`), `Export` secondary button. No fabricated company name in the brand — use `Pencil` or whatever `design-system.md` declares.

### Call C — row 1 tiles: MRR trend + Conversion by source (≤25 ops)

```
row1=I(grid, { type: "frame", name: "TileRow1", layout: "horizontal", width: "fill_container", gap: "$space-6" })
mrrTile=I(row1, { type: "ref", ref: "Card", name: "MrrTrendTile", width: "fill_container", height: 320, descendants: { ... } })
convTile=I(row1, { type: "ref", ref: "Card", name: "ConversionByTrafficTile", width: "fill_container", height: 320, descendants: { ... } })
```

Then build the inside of each tile. Per `data-viz.md`'s tile lockup:

**MrrTrendTile contents:**
- Header row: title `Monthly recurring revenue` (`$textBase`, `$textPrimary`), helper `Last 12 months` (`$textSm`, `$textMuted`), action menu icon (`IconButton` ref, `more-horizontal`, top-right).
- Big number: `$48,200` (`$text3xl`, `$textPrimary`, `$fontMono` because `data-viz.md` calls for mono on dense numerics).
- Delta: `+12.4% vs last month` (`$textSm`, `$success`, with up-arrow icon — the rule is *color is never the only signal*, so the arrow is mandatory).
- Chart: 12-month line. 2px stroke, `$chart-1`. Horizontal gridlines only in `$borderMuted`. X-axis ticks: every other month label so we stay under 6 visible ticks at the rendered width. Y-axis: 4 ticks, starting at zero, comma-grouped. Plausible monthly data — not "trusted by 10,000 teams" filler.

The chart itself is a child frame with explicit `width: "fill_container"`, `height: 160`, and the line drawn as a series of segments or a vector path. If the library has a `LineChart` component I instantiate it; if not, I sketch the line as a polyline frame and flag the chart subtree as a candidate for extraction into the library.

**ConversionByTrafficTile contents:**
- Header: title `Conversion by traffic source`, helper `Visitors → trial signups`, action menu.
- Big number: `Organic search` (the top source, `$text2xl` — string here, not numeric, so smaller than the numeric big-number rule).
- Delta: `4.8% conversion` (`$textSm`, `$textMuted`).
- Chart: horizontal bar chart, top 5 sources. Labels are long (`Organic search`, `Direct`, `Paid social`, `Referral`, `Email`), so horizontal is right per `data-viz.md`. Bars in `$chart-1`. Bar gap ~20% of bar width. Value labels right of each bar in `$fontMono`.

### Call D — row 2 (heatmap) + row 3 (table) (≤25 ops)

**Row 2 — CohortRetentionTile, full-width.**

The heatmap needs horizontal real estate. Title `Cohort retention`, helper `Weekly cohorts, % active by week N` or whatever the data's actual semantics are. No big-number — this tile is the chart. The grid: 8 cohorts (rows, labelled by start date e.g. `Mar 4 – Mar 10`) × 8 weeks (columns, `Wk 0` through `Wk 7`). Each cell is a 36×36 frame with `cornerRadius: 4`, fill bound to `$chartSeq-50/300/500/700/900` based on retention bucket. Lowest bucket maps to `$chartSeq-50` (almost surface), highest to `$chartSeq-900`. Cell value text overlaid in `$fontMono`, `$textSm`, color flips to white when the cell's lightness drops below threshold (per `accessibility.md` contrast rule, but I can encode this with two sets of cell components: light-cell-with-dark-text and dark-cell-with-light-text). Legend at the bottom: a horizontal strip of the 5 sequential swatches with `0%` and `100%` end labels.

**Row 3 — TopCustomersTile, full-width.**

Compact table. If the library has a `Table` / `TableRow` component, instantiate it. Columns: `Customer` (left, account name + small contract badge), `MRR` (right-aligned, `$fontMono`, formatted `$XX,XXX`), `Δ vs last month` (right-aligned, `$fontMono`, `$success`/`$danger` color + arrow icon, never color-alone), `Plan` (badge — `Enterprise` / `Growth` / `Starter`), `Owner` (avatar + name, leveraging `Avatar` ref).

10 rows. Names are plausible-sounding but not real-customer-real-revenue ("Northwind Logistics", "Atlas Systems", "Fieldwire", "Helix Bio") — definitely not `Acme` / `Nexus` / `John Doe`. If the user has real anonymized data, swap it in; otherwise this is acceptable filler labelled as illustrative.

After Call D, every top-level frame is built. I issue:

```
U("page", { placeholder: false })
```

…as a one-op `batch_design` call to flip the page out of placeholder mode (per `batch-design-grammar.md`'s placeholder discipline).

## Step 6 — Verify (structural-first)

The verification ladder, in order. The skill's whole point is to climb only as far as needed.

### Rung 1 — `batch_design` response

After each of Calls A–D, the server reports per-op success and the assigned ids. If anything errored, I read the message verbatim and cross-reference `batch-design-grammar.md`'s common-errors table. The likely candidates here:

- `width expected ... fit_content or fill_container` — I used `"100%"` instead of `"fill_container"`. Fix and retry.
- `slot frame must be empty in origin` — only relevant if I was building a component origin, not for instances. N/A here.
- `parent not found` — I referenced a binding before declaring it. Reorder.

### Rung 2 — `snapshot_layout` after each call

```
snapshot_layout({ parentId: "page", maxDepth: 2 })           // after Call A
snapshot_layout({ parentId: "topNav", maxDepth: 2 })         // after Call B
snapshot_layout({ parentId: "row1", maxDepth: 3 })           // after Call C
snapshot_layout({ parentId: "grid", maxDepth: 2, problemsOnly: true })  // after Call D
```

What I'm confirming: tile heights are 320 in row 1, gap between tiles is 24, grid spans the full width of `main`, the heatmap row's 8×8 grid actually shows 64 cells of 36×36, the table has 10 rows of equal height. `problemsOnly: true` on the final pass surfaces overflow or undefined sizes I missed.

If row 1 tiles are unequal width, the auto-layout `width: "fill_container"` on both didn't take — most likely cause is the parent is `layout: "horizontal"` but I forgot to set `gap` so flex distribution fell back. Targeted `U` fix.

### Rung 3 — `batch_get` for property-level confirmation

```
batch_get({ nodeIds: ["mrrBigNumber", "mrrDelta", "convBigNumber"], resolveVariables: true })
batch_get({ nodeIds: ["heatmapCell_0_0", "heatmapCell_7_7"], resolveVariables: true })
```

What I'm checking: text colors resolve to `$success` / `$danger` (not raw hex), heatmap corner cells use `$chartSeq-50` and `$chartSeq-900` (not interpolated raw hex), the chart line stroke is bound to `$chart-1`. `resolveVariables: true` so I see actual hex values and can sanity-check contrast against `$surface`.

If any color is raw hex when it should be a token, fix with `U` ops in a small follow-up `batch_design` call. This is also where I'd run `replace_all_matching_properties` if the audit surfaced 3+ instances of the same drift (e.g. `#16A34A` showing up where `$success` was intended).

### Rung 4 — `get_screenshot`, scoped, once

```
get_screenshot({ nodeId: "page" })
```

This is the one screenshot of the build, scoped to `page` (not document root). I'm scanning for, in this order from `mcp-tools.md`:

1. **Layout integrity** — does the dashboard read as a coherent page? Any tile off-canvas, the heatmap not visibly distinguishable as a grid, any column wildly mis-sized?
2. **Spacing rhythm** — gaps between sections match `$space-6` (24). The tile-internal padding reads as `$space-6` not less. Heatmap cell gap reads consistent.
3. **Type rhythm** — the four tile titles are the same size (`$textBase`). Big-numbers all `$text3xl`. Page title clearly larger than tile titles. Body text legible at the rendered scale.
4. **Contrast** — body text passes WCAG AA against `$surface`. Sequential heatmap cells in the lightest bucket still pass 4.5:1 for their overlaid value text (this is the bit I most want pixels to confirm — sequential palettes have a habit of failing contrast at the low end).
5. **Component fidelity** — every tile reads as the same `Card`. The selected SideNav item has both the muted background AND the 3px accent bar. Status chips in the table have both icon and color.

**Dual-mode rule from SKILL.md.** I would NOT screenshot dark mode separately. The design is built entirely from `$variable` tokens with both light and dark values; the variable system guarantees mode parity. I'd only re-screenshot in dark if I'd used a raw hex by mistake (rung 3 would have caught that).

### Things I expect rung 4 to surface and fix

- The heatmap cell value text is illegible on `$chartSeq-700` and `$chartSeq-900` cells (color is too similar to background). Fix: cells with bucket ≥ 700 use a dark-cell variant whose text is `$surface` (off-white) instead of `$textPrimary`. One `U` op pair, no re-screenshot needed unless the change cascades.
- The MRR trend line is hard to read against the gridlines. Fix: bump line stroke from 2px to 2.5px, or make gridlines lighter (`$borderMuted` may already be too strong against `$surface`).
- The conversion-tile big-number ("Organic search") wraps awkwardly because it's a string not a number. Fix: smaller font (`$textXl` instead of `$text2xl`) or constrain width.

If three iterations don't converge on a single issue, I stop and ask the user — the requirement is probably ambiguous (e.g., "is the tile headline supposed to be the source name or the conversion %?").

## Step 7 — Iterate or report

Total tool budget for this build, planned:

| Tool | Calls | Why |
|------|-------|-----|
| `get_editor_state` | 1 | Step 1 |
| `get_guidelines` | 4 | Discovery + 3 categories |
| `get_variables` | 1 | Token check before any write |
| `batch_get` | 4 | Component inventory ×2, post-build property check, post-build heatmap check |
| `set_variables` | 1 | Only if chart tokens are absent — call would pass only the absent keys |
| `batch_design` | 5 | Calls A–D + the placeholder flip |
| `snapshot_layout` | 4 | After each `batch_design` write |
| `get_screenshot` | 1 | Final sign-off, scoped to `page` |

**One screenshot** for the full build. The pre-skill version of this same task would have produced 3–5 (one mid-flight per tile, one full-canvas final, possibly one in dark).

## Final report I'd give the user

> *"Done. `AnalyticsDashboard_Desktop` at 1440×900 — dashboard shell with TopNav (brand + breadcrumb + search + account) and SideNav (Overview / Analytics selected / Cohorts / Customers / Reports / Settings). Main content holds a page header ('Analytics' + date-range segmented control + Export button) and a tile grid: row 1 has the MRR trend (line, 12 months, big-number `$48,200`, +12.4% delta) and Conversion by traffic source (horizontal bars, top 5 sources, organic search leading at 4.8%); row 2 is the cohort retention heatmap (8 × 8, sequential `$chartSeq-*` palette with legend); row 3 is the Top 10 customers table (name, MRR, delta with arrows, plan badge, owner avatar). Every tile is a `ref` to your library's `Card`. Chart colors bound to `$chart-1` and `$chartSeq-*` tokens — I added `$chart-2..4` and `$chartSeq-300/500/700` because they were missing; left every existing token untouched. Numbers throughout are illustrative — swap them for real data when you're ready. Contrast verified at the heatmap's high-density end where it's most likely to fail; cells in the top two buckets use light text. The dashboard tile pattern reads consistently; if you want me to extract `DashboardTile` into your `.lib.pen` so the four tiles share an origin, say the word."*

## What I would NOT do

- **Not** build a one-off `Card` from primitives if `Card` exists in the library.
- **Not** fabricate metrics. The numbers are flagged as illustrative; I'd ask for real data if the user wants production-ready copy.
- **Not** screenshot after every tile to "check progress." That's the older verification reflex; `snapshot_layout` is the right tool for "did the geometry land?" and is what the skill points me to.
- **Not** ship a pie chart for the conversion tile, even though it's a natural reach for "parts of a whole." `data-viz.md` bans pie above 3 slices, and "top 5 sources" wants a bar chart.
- **Not** use neon/glow chart fills, raw `#000000` / `#FFFFFF` for tile surfaces, or Inter as the body font — every one of those is on the AI-tells list in SKILL.md.
- **Not** add a third call for "polish" if rungs 1–4 of verification show clean. Stop when the user's requirements are met and the discipline rules check out.
