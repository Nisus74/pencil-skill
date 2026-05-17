# Designing the SaaS analytics dashboard — and what "ready for engineering" actually means

Before I touch the canvas, I want to flag a tension in the brief. You asked for "the dashboard," but you also asked me to "cover everything we'd need designed before engineering can start building." Those are two different scopes, and the SaaS completeness pressure test in the skill is unambiguous about it:

> *If the file does not show roles, permissions, empty states, loading states and error recovery, it is not comprehensive. It is a sales demo.*

A single dashboard frame, no matter how polished, is a sales demo. Engineering can't build from it because they'll hit the first empty state, the first 403, the first failed chart fetch, and have to make design decisions on the fly. So I'm going to do both: design the dashboard properly, and lay out the rest of the screen set you'll need committed before a build starts. You can prune what doesn't apply.

## Skill references I'm pulling from

- `SKILL.md` — default workflow, discipline rules (naming, context, components-first, themes, responsive, a11y, file architecture), aesthetic defaults, anti-patterns.
- `references/industry-patterns.md` § SaaS — sub-category rules (analytics is "very dense, chart-forward, number-first"), per-industry rules (one primary action per view, autosave, ⌘K, dark mode by default, sample-data onboarding, plan/trial states), and the SaaS completeness pressure test that drives the screen list below.
- `assets/examples/example-dashboard.md` — the canonical KPI-row + chart-tile + table layout, with the tile shapes and verification cadence.
- `references/data-viz.md` (referenced by the example) — chart selection, tile shapes, colour-blind-safe palettes, tabular numerics.
- `references/states.md` (referenced by both above) — component states matrix and screen-level fault states.
- `references/file-architecture.md` (referenced by SKILL) — Cover frame, section regions, hierarchical naming for the multi-screen flow.
- `references/layout-patterns.md` § Dashboard layouts — the four shapes and when to pick each.

I haven't loaded `flows.md`, `forms.md`, `accessibility.md`, or `microcopy.md` yet — I'll load each on demand when I get to the screens that need them (auth flows, settings forms, deep accessibility audit, copy pass).

## Step 1: Host check and context

Before any of this lands, I'd run:

```
get_editor_state({ include_schema: false })
```

If it errors with `transport not connected to app: desktop`, I stop and ask you to open the Pencil desktop app or the IDE extension. I do not silently fall back to the CLI.

Assuming it succeeds, I capture: which `.pen` is open (if any), what's selected, the schema version. Then I check the project filesystem for `./design-system/`. I expect three possible states:

- **Folder exists, populated** — I read `README.md`, then `design-system.md` (for the `.lib.pen` path, tech stack, icon library), `tokens.md`, `components.md`, `patterns.md`, `states.md`, `voice.md`. Whatever those say overrides the aesthetic defaults in the skill.
- **No folder** — I offer once to scaffold the 12 core templates plus the optional `data-viz.md` (we have charts) and `brand.md` (analytics SaaS usually ship a marketing surface). I don't ask twice this session.
- **Folder with code in it** — I ask where to put the docs (`design-system/docs/`, `docs/design-system/`, etc.) and don't overwrite.

I'd also need the following from you before planning, because the brief is open-ended:

1. **Who uses this?** Customer-success ops looking at a single account, founders watching company-wide metrics, end-users on a self-serve plan? The audience changes density, the metric set, and the navigation depth.
2. **Atmosphere or brand direction?** Words, references, or an existing `tokens.md`. If you say nothing, I'll commit to "dense, symmetric, static" — the analytics-SaaS default — using Inter + JetBrains Mono and the Indigo Calm palette.
3. **Hard constraints?** Stack (so `code-export.md` mirrors it), responsive targets (do tablets matter for an internal tool?), dark-mode-only (common for analytics tools used 8+ hours), reference dashboards you admire.

I'll proceed assuming a generic answer below: B2B analytics SaaS for a product/growth team, ⌘K table-stakes, dark mode shipped, three breakpoints, no committed brand yet.

## Step 2: Tokens — protect what's already there

Before declaring any variables I'd run:

```
get_variables()
```

If the doc has tokens, I treat them as authoritative — `set_variables` with `replace: false` (the default) still overwrites any key I pass, so calling it with a "default suite" silently clobbers your work. If `get_variables` returns empty, I declare the `mode` axis and bootstrap only what's missing:

```
U("doc", { themes: { mode: ["light", "dark"] } })
set_variables({ variables: {
  surface:        { type: "color", value: [{ value: "#FAFAFA", theme: { mode: "light" } }, { value: "#0B1117", theme: { mode: "dark" } }] },
  surfaceMuted:   { type: "color", value: [{ value: "#F4F4F5", theme: { mode: "light" } }, { value: "#11161D", theme: { mode: "dark" } }] },
  border:         { type: "color", value: [{ value: "#E4E4E7", theme: { mode: "light" } }, { value: "#1F2630", theme: { mode: "dark" } }] },
  textPrimary:    { type: "color", value: [{ value: "#0B0B0F", theme: { mode: "light" } }, { value: "#F4F4F5", theme: { mode: "dark" } }] },
  textMuted:      { type: "color", value: [{ value: "#71717A", theme: { mode: "light" } }, { value: "#9CA3AF", theme: { mode: "dark" } }] },
  accent:         { type: "color", value: [{ value: "#4F46E5", theme: { mode: "light" } }, { value: "#818CF8", theme: { mode: "dark" } }] },
  success:        { type: "color", value: [{ value: "#15803D", theme: { mode: "light" } }, { value: "#4ADE80", theme: { mode: "dark" } }] },
  warning:        { type: "color", value: [{ value: "#B45309", theme: { mode: "light" } }, { value: "#FBBF24", theme: { mode: "dark" } }] },
  danger:         { type: "color", value: [{ value: "#B91C1C", theme: { mode: "light" } }, { value: "#F87171", theme: { mode: "dark" } }] },
  focusRing:      { type: "color", value: [{ value: "#4F46E5", theme: { mode: "light" } }, { value: "#A5B4FC", theme: { mode: "dark" } }] },
}, replace: false })
```

Plus typography tokens (`fontDisplay`, `fontBody`, `fontMono`, the `fontSize-*` and `fontWeight-*` scale), spacing scale (`space-1` through `space-12`), radii (`radius-sm/md/lg`), and the chart palette from `references/data-viz.md` (Okabe-Ito for categorical series — colour-blind-safe).

I'd verify with `get_variables()` again; I would *not* screenshot to "check" tokens — they're a JSON-level concern.

## Step 3: Components — inventory before building

Before any frame goes down, I scan for existing components:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

And if the doc has a `.lib.pen` in `imports`, I repeat the call against it. I expect (or want to end up with) at least: `Sidebar`, `TopBar`, `Button` (Primary/Secondary/Destructive/Ghost/IconOnly × 7 states each), `Input`, `Select`, `DateRangePicker`, `Tag`, `Badge`, `Avatar`, `Tooltip`, `Modal`, `Sheet`, `Dropdown`, `Toast`, `KPICard`, `LineChart`, `BarChart`, `AreaChart`, `Sparkline`, `TableTile`, `EmptyState`, `Skeleton`, `Spinner`, `CommandPalette`. Anything missing becomes a new `reusable: true` node in the `.lib.pen`. I won't fork the library because of a naming preference — if `PrimaryButton` exists, I use it even if you said "Submit button."

For any component I haven't used before, I'd run `batch_get({ nodeIds: ["X"], readDepth: 4 })` to find slot frames, named children, and theme states before instantiating.

## Step 4: File architecture — Cover frame and sections

Per `references/file-architecture.md`, before any screens I lay down:

- **`Cover` frame at canvas origin.** Owner, status (`In design`), version, last-updated, scope (in/out), links (brief, ticket, prototype, design-system folder). Without this no one can answer "is this safe to build from?" in 30 seconds.
- **Section regions** placed via `find_empty_space_on_canvas` so they don't overlap:
  - `SourceOfTruth` — the canonical Dashboard once approved.
  - `BuildReady` — current iteration in flight.
  - `UXStates` — the state matrices (loading, empty, error, no-permission, plan-restricted) for each tile.
  - `Responsive` — per-breakpoint variants.
  - `Exploration` — alternate layouts I tried.
  - `Archive` — superseded versions.

Multi-screen names use the path form: `Analytics / Dashboard / 01 / Overview / Default / Desktop`.

## Step 5: The plan (vibe + layout, before any batch_design)

**Atmosphere:** *Dense, symmetric, static.* Analytics-SaaS default — number-first, chrome-out-of-the-way, no animation theatrics. Dark mode shipped from day one (the audience uses this in long sessions).

**Layout:** Sidebar (240px collapsed to 64px) + main, per `references/layout-patterns.md` § Dashboard layouts. Main column has a sticky `TopBar` (workspace switcher, global search/⌘K, date range, environment, user menu), then:

- **KPI row** — 4 tiles across at desktop, 2×2 at tablet, stacked at mobile. Big-number value, label, delta (arrow + percentage with paired colour), inline sparkline. `tabular-nums` on every value so they align across tiles.
- **Chart row** — one full-width primary trend chart (line, 12-month rolling window, current period solid `$accent`, prior period dashed `$textMuted`). Below it, two side-by-side secondary tiles (e.g. funnel + breakdown bar). Direct labels at line ends; gridlines only on the value axis; legend inline, not boxed.
- **Recent activity table** — full-width, virtualised after 50 rows, columns: User · Action · Resource · Time. Sort defaults to Time descending. Time column shows relative (`2 minutes ago`) with absolute on hover.

Three breakpoints per the canonical sizes (390 / 768 / 1440), built as sibling per-breakpoint frames since dashboard layout shifts dramatically on mobile.

## Step 6: Execution sketch (one batch per logical chunk)

I'd execute in roughly five `batch_design` calls, ≤25 ops each, using the `foo=I("parent", {...})` binding form so later ops can reference newly-created nodes. Sketches:

**Batch 1 — outer frame + sidebar + topbar (Desktop):**
```
dash=I("<canvas>", { type: "frame", name: "Analytics / Dashboard / 01 / Overview / Default / Desktop",
                     context: "Main analytics dashboard. Sidebar nav (240px) + main (scroll). KPI row, primary trend chart, two secondary charts, recent activity table.",
                     size: { width: 1440, height: 900 }, layout: { direction: "row" } })
side=I(dash, { type: "ref", ref: "Sidebar", descendants: { "active": "Dashboard" } })
main=I(dash, { type: "frame", name: "Main", layout: { direction: "column", padding: [0,0,0,0], gap: 0 }, width: "fill_container" })
top=I(main, { type: "ref", ref: "TopBar", descendants: { "dateRange": "Last 30 days", "env": "Production" } })
body=I(main, { type: "frame", name: "Body", layout: { direction: "column", padding: [24,32,32,32], gap: 24 }, width: "fill_container" })
```

**Batch 2 — KPI row** with 4 `KPICard` refs (Revenue, MRR, Active users, Churn), each with `value`, `label`, `delta`, `deltaDirection`, `sparkline` overrides via `descendants`. Delta carries arrow shape (`↑`/`↓`) AND `$success`/`$danger` colour — never colour alone.

**Batch 3 — primary chart tile** with `Header` (title + subtitle + period selector + overflow menu) and a `LineChart` ref. `context` notes the data source, the rolling window, and the prior-period series.

**Batch 4 — secondary charts row** (two tiles side-by-side: a `BarChart` for top-N breakdown, an `AreaChart` for cumulative).

**Batch 5 — activity table** wrapping a `TableTile` ref with column spec and row data.

For all imagery / charts where I want plausible content (e.g. user avatars), I'd use `G(nodeId, "ai", "<prompt>")` rather than placeholder rectangles. Absolutely no `John Doe` / `Acme` filler.

## Step 7: Verification (one screenshot, scoped tight)

I walk the verification ladder:

1. `batch_design` response confirms each call succeeded — free.
2. `snapshot_layout({ nodeId: "<dash>", maxDepth: 3 })` — confirms KPI row is 4-across with 16px gap, sticky topbar height, body padding, table column widths land where intended. This is the workhorse and should answer 90% of "did it land" questions.
3. `batch_get({ nodeIds: ["<kpi1>", "<chart1>", "<table1>"] })` — confirms refs resolved, variables bound (no raw hex anywhere), `tabular-nums` set on numeric text.
4. `get_screenshot({ nodeId: "<dash>" })` — once, as final sign-off, scoped to the dashboard frame, not the full canvas. I screenshot dark mode only if I have reason to suspect a mode-conditional colour was set wrong (e.g. a raw hex slipped in). Theme-aware designs built entirely from variables don't need a second screenshot to confirm dark holds up — the variable system guarantees it.

What I check on the screenshot:
- KPI numbers tabular-aligned across all four tiles.
- Delta arrows AND colours present, not colour-only.
- Chart axis labels readable; direct line-end labels not clipped.
- Sparkline endpoints visible inside KPI cards.
- Table fits without horizontal scroll at 1440.
- Body text passes 4.5:1 against `surface` (and `surfaceMuted` where used); button fills pass 3:1.
- Hit targets ≥ 44×44 for every interactive element.

## Step 8 — and this is where the brief actually starts widening

Engineering cannot build from a single Default/Desktop frame. The SaaS pressure test requires the following to be designed before they start. This is the section you should push back on if it's more than your team needs, but I'd flag each gap to you rather than ship a sales demo.

### Per-tile state matrices (in `UXStates`)

Each KPI card, chart tile, and the table needs:

- **Skeleton** — placeholder values + sparkline shimmer for KPI; axis hints + ghost line for chart; 5 placeholder rows for table. Show within 100ms; spinner only for unknown-duration <1s operations.
- **Empty** — first-use ("Connect a data source to see revenue here", with a primary CTA), no-results ("No events match these filters", with a Clear filters secondary action), post-action ("All caught up — no recent activity").
- **Partial failure** — one tile errored, the rest of the dashboard renders normally. Inline retry on the broken tile. Never blow up the page because one query failed.
- **Error** — full tile error with retry; copy follows the "what happened, why if non-obvious, what to do" pattern.
- **No-permission** — viewer role can see the tile shape but not the values; "Ask an admin to grant Analytics: Read."

### Screen-level fault states

- **404** — page that doesn't exist within the app; offer the dashboard and search.
- **403** — no-permission for an entire route; same lockup, different copy.
- **500** — something on our side; status link, retry, copy a trace ID for support.
- **Offline** — connection lost banner; cached data visible with a "Last synced X" stamp.
- **Plan-restricted** — Analytics is a Pro feature; the dashboard is dimmed behind a paywall lockup with the upgrade CTA. (`industry-patterns.md` SaaS rules require this.)
- **Trial-expired** — same shape, different copy + reactivate CTA.
- **Read-only** — workspace is in maintenance / billing failed; banner explains why and what to do.

### Auth and workspace (separate flows file)

Before they can land on the dashboard:

- Sign-in (email + password, SSO, magic link).
- Sign-up.
- Password reset (request + confirm).
- MFA enrollment + challenge.
- Session-expired modal (re-auth without losing context).
- No-workspace state (just signed up, hasn't created or been invited).
- Create workspace + workspace switcher.

Each of these I'd load `references/flows.md` and `references/forms.md` for before designing — validation timing, autocomplete attributes, focus-first-error-on-submit, mobile font-size to defeat iOS zoom, Enter-to-submit semantics.

### Navigation

- Global nav (sidebar collapsed and expanded, with sub-routes).
- Breadcrumbs for nested resources.
- Global search / ⌘K command palette — table-stakes for B2B SaaS in 2025/2026 per the SaaS rules. Recent searches, jump-to-anywhere, run-an-action.
- Notifications panel (badge count, list, settings deep-link).

### Admin

- Users list + invite flow.
- Roles & permissions matrix (this is where the no-permission states earn their keep).
- Billing (plan, payment method, invoices, usage). High-stakes — explicit Save here, not autosave.
- Integrations (connect/disconnect data sources; auth flows per integration).
- Audit log.

### Settings

- Profile (autosave).
- Workspace settings (autosave for non-billing, explicit save for high-stakes).
- API keys / webhooks (with copy-once secret reveal + rotation flow).

### Core dashboard variants you'll likely want

- **Filtered view** — date range changed, segment filter applied. Shows how the chrome reflects active filters and how to clear them.
- **Drilldown** — clicking a KPI takes you to a detail view. Needs the route shape designed.
- **Compare mode** — toggle prior period on/off; how the legend and labels handle two series.
- **Export** — CSV / PDF / scheduled email. The export confirmation toast and the scheduled-export management screen.

### Responsive

- **Tablet (768)** — KPI row collapses to 2×2; secondary charts stack; sidebar becomes overlay drawer behind a hamburger.
- **Mobile (390)** — KPI cards stack vertically; primary chart full-width with horizontal scroll for the time axis; table converts to a card list (one row per card) since horizontal scrolling tables are user-hostile on mobile.

## What I'd ask you before starting any of this

1. **How wide do you actually want me to go?** Just the Default/Desktop dashboard frame? Default + state matrix for each tile? Or the full pressure-test set above?
2. **Audience and metrics** — confirm the KPI set. "Revenue / MRR / Active users / Churn" is a guess; for a product analytics tool the right four might be Active users / Activation rate / Feature adoption / Retention.
3. **Brand direction or existing `design-system/`** — if there's a `tokens.md` already, the colour and typography decisions above defer to it.
4. **Roles and plans** — list the roles (Owner / Admin / Member / Viewer? Custom roles?) and the plan tiers (so the no-permission and plan-restricted states are accurate, not invented).
5. **Data sources and integrations** — which ones ship in v1, because each is its own auth flow.

Tell me which of those are settled and which are still open, and I'll either (a) design just the dashboard frame + its state matrix as a focused first pass, then loop back for the rest in a follow-up, or (b) plan the full set across multiple `.pen` files (one per area: `auth.pen`, `dashboard.pen`, `admin.pen`, `settings.pen`) with a shared `design-system.lib.pen`.

The dashboard frame on its own is roughly a 60-minute design task. The "everything engineering needs" version is closer to 8–12 hours of design work spread across 4–6 `.pen` files. Both are reasonable answers depending on what you actually want — I just don't want to call the first one done and have you discover the gap when engineering opens a ticket asking what the empty state is supposed to look like.
