# Designing the SaaS analytics dashboard

Happy to take this on, but before I open Pencil and start dropping frames, the prompt is doing a lot of work in one sentence ("the dashboard", "everything we'd need before engineering can start") and I want to make sure I scope it the way you actually want. I'll lay out (a) what I need from you to commit to a plan, (b) what I'd do unprompted if you said "just go", and (c) the full design completeness checklist I'd work against either way.

## References I consulted (and why)

- `SKILL.md` — the seven discipline rules (naming, context, components-first, themes, responsive, accessibility, design completeness) and the default workflow. The prompt is real project work, multi-screen, will need a `design-system/` folder, and will need theme + responsive coverage from the start. SKILL.md governs all of that.
- `references/states.md` — the design completeness rule says I have to ship more than the default state of every component and the happy path of every screen. A dashboard is the worst offender for "ships only the default state". I loaded the state matrix, the empty-state taxonomy (first-use vs no-results vs no-permission vs post-action), and the screen-level fault states (404 / 403 / 500 / 503 / 408 / 429 / offline / partial-failure).
- `references/flows.md` — anything that crosses screens needs validation timing, modal-vs-page choices, and back-stack behavior documented. A dashboard for an analytics product implies filters, drilldowns, date pickers, share/export modals, alert-rule editors. All of that is flow work.
- `references/modern-patterns.md` — analytics dashboards rot fast aesthetically. I want container queries on tiles (same KPI tile renders in a sidebar, a 3-up grid, and a wide hero), skeleton screens (data takes 800ms, charts 1500ms — staggered reveal beats one big spinner), and modern dark mode (real dark mode, not inverted light). Also flagged the AI-tells to avoid: glassmorphism, three-card grids as the default for everything, fabricated "99.7% accuracy" stats.
- `assets/design-system/patterns.md` § Dashboard shell — the canonical app shell (TopNav, SideNav, Main, optional right rail) so I don't reinvent it.
- `assets/design-system/data-viz.md` — categorical and sequential palettes, default chart types per question, dashboard tile anatomy, the four chart states (loading / empty / error / partial). The skill says scaffold this conditionally; for an analytics product it's mandatory.

## What I need from you before I plan

These are the cheap-to-answer questions whose answers reshape the whole design. Asking now saves a rebuild.

1. **Audience and primary job-to-be-done.** "SaaS analytics" covers product analytics (Mixpanel / Amplitude / PostHog), web analytics (Plausible / Fathom), revenue analytics (ChartMogul / Baremetrics), customer-success analytics (Vitally), and observability-flavoured analytics (Honeycomb / Datadog). Each one wants a different default dashboard. Which are you?
2. **Single-tenant or multi-tenant.** Does a user belong to one workspace or switch between many? This decides whether the SideNav has a workspace switcher at the top.
3. **Roles.** Admin / editor / viewer? Read-only viewers force me to design every action's disabled state and a sensible 403.
4. **Real-time or batch.** Live-updating tiles ("12 users active right now") need presence and refresh affordances; nightly-batched dashboards don't, and dressing them as live is dishonest.
5. **Build target.** Web only, web + responsive (tablet / mobile breakpoints), or web + a native mobile app? Mobile changes the layout enough that I'd scaffold `mobile.md` and design per-breakpoint frames.
6. **Brand and existing design system.** Do you have a `design-system/` folder, a `.lib.pen` library, brand tokens, a logo? If yes I read them and follow them; if no I'll offer to scaffold (see below).
7. **Stack for code export.** Influences `code-export.md` and the chart library assumptions (Recharts vs Visx vs ECharts vs nivo render different defaults).

If you'd rather not answer all seven, the minimum I need is **#1, #4, and #5**. The rest I'll make defensible defaults for and document in the design's `context` strings so you can challenge them.

## What "everything before engineering can start" actually covers

Here's the full surface area I'd commit to. This is the design completeness contract for this project — engineering should be able to read it and know what to build without coming back to ask "what about the empty state?"

### 0. Foundations (`design-system/` folder)

If the repo doesn't have one yet, I'd offer to scaffold the 11 core templates plus `data-viz.md` (mandatory for analytics) and conditionally `mobile.md` (if you ship native or responsive mobile) and `brand.md` / `imagery.md` (if you have a marketing surface). Per SKILL.md the offer is once per session — if you decline, I proceed without and don't ask again.

The scaffold gives engineering a single source of truth for tokens, components, voice, motion, and code-export rules — agent-readable across sessions and tools, not just by me.

### 1. Tokens, themes, and the `.lib.pen` library

- `get_variables()` first to see what already exists. Never clobber existing tokens.
- `mode` axis with `light` and `dark` declared up front. Every color carries both. Retrofitting dark mode is brutal.
- Tokens to set if absent: surface scale (`$surface`, `$surfaceMuted`, `$surfaceInverse`), text scale (`$textPrimary`, `$textMuted`, `$textInverse`), borders, shadows/elevation, primary + accent + semantic (`$success`, `$warning`, `$danger`, `$info`), spacing scale, type scale, radius scale, and the categorical chart palette (`$chart-1` through `$chart-8`) plus a sequential palette for heatmaps.
- A `.lib.pen` for the project (`./design/system.lib.pen`), imported into the dashboard `.pen` via the document's `imports`. Components live there once, instantiated everywhere.

### 2. Components in the library

The dashboard reuses these everywhere; I'd build them as `reusable: true` nodes in the `.lib.pen` with state coverage per `references/states.md`:

- **Buttons.** Primary, secondary, tertiary, destructive, ghost. Sizes sm/md/lg. States: default, hover, focus, pressed, disabled, loading. Icon-only variant with 44x44 hit target enforced.
- **Inputs.** Text, number, password, search, textarea, select, multi-select, combobox, date picker, date-range picker (critical for analytics), checkbox, radio, toggle. States: default, hover, focus, filled, error, focused-with-error, disabled, success, loading (for async validation).
- **Form scaffolding.** Field (label + input + helper + error), fieldset, form footer. Validation timing per `flows.md`: don't shame mid-keystroke; on-blur for sync, on-submit for async.
- **Navigation.** SideNav (expanded 240 / collapsed 64), TopNav, breadcrumb, tabs, segmented control, pagination. SideNav with workspace switcher at top if multi-tenant.
- **Surfaces.** Card / tile (the dashboard tile is a specialised card), modal, sheet (right-anchored for filters), popover, toast, banner, divider.
- **Data.** Table (sortable column header, row hover, row selection, sticky header, sticky first column for wide tables, expandable row), data grid for heavier interactivity, list, list+detail, KV list (for definitions / metadata).
- **Feedback.** Tag, badge, status pill (text + icon — never colour alone), avatar, avatar pile, tooltip, skeleton, progress (bar + indeterminate), spinner.
- **Charts.** Line, bar (vertical + horizontal), stacked bar, area, sparkline, scatter, heatmap, big-number tile, percentile / distribution. Each with the four states from `data-viz.md`: default, loading (skeleton in chart shape), empty (with copy), error (inline retry).

For each I'd use `batch_get({ patterns: [{ reusable: true }], readDepth: 2 })` against the open doc and any imported `.lib.pen` first to see what already exists. Components-first rule — I never rebuild a button when one exists.

### 3. App shell

Per `patterns.md` § Dashboard shell:

```
App (full viewport)
├── TopNav (h: 56, sticky) — workspace switcher (if multi-tenant), global search,
│       notifications, account menu, theme toggle, "What's new"
├── SideNav (w: 240 / 64) — Logo, primary nav (≤ 7 items, grouped if more),
│       secondary nav (Settings, Help), user menu at bottom
├── Main (fill_container, padding $space-6)
│   ├── Page header (title, breadcrumb, date range, primary action)
│   └── Content
└── (Optional) Right rail (w: 320) — context, AI assist, alert detail
```

Side nav holds primary nav (overview, dashboards, reports, segments, alerts, settings — match to your product). TopNav is chrome. The skill is explicit: pick one as primary, the other is thin chrome — don't weight both.

### 4. Dashboard pages

For a SaaS analytics product I'd plan, at minimum:

- **Overview / home.** Big-number tiles row (4–6 KPIs, each one question), one or two hero charts, a recent-activity / signal feed, optional AI-summary section.
- **Drilldown / report builder.** A specific metric as the focus. Date range, comparison range, breakdown / group-by, filter chips, the chart, a results table beneath.
- **Segment / cohort builder.** If your product does cohorts.
- **Saved dashboards list.** List+detail or grid, with search, sort, owner filter, "+ New dashboard".
- **Single saved dashboard view.** Customisable tile grid. Edit mode for arranging tiles.
- **Alerts.** List of alert rules, alert detail, alert-fired notification, alert history.
- **Account / settings.** Single column max ~720px (per `patterns.md` § Settings page). Profile, workspace, members + roles, billing, integrations, API keys, notifications, danger zone.

Per the responsive rule, each high-traffic page gets per-breakpoint frames named `Overview_Desktop`, `Overview_Tablet`, `Overview_Mobile` (1440 / 768 / 390). Settings can usually be a single fluid frame because layout doesn't shift dramatically.

### 5. Tile anatomy and chart defaults

Per `data-viz.md` § Dashboard layout:

```
Tile (Card, $elevation1, padding $space-6)
├── Header — title, optional helper, optional action menu
├── Big-number ($text3xl) — the single most important number
├── Delta ($textSm, $success or $danger, with up/down arrow)
└── Chart (sparkline or small chart)
```

One tile = one question. Big-number > delta > chart in visual weight. Sparklines under big-numbers don't get y-axis labels.

Chart defaults: axes start at zero (always for bars, default for lines), horizontal gridlines only in `$borderMuted`, ≤ 6 x-axis ticks visible, monospace numerics in dense charts, 2px stroke for line charts, ~20% bar gap, tooltips on hover/tap with precise value + series + timestamp. No pies past 3 slices, no 3D, no donut-with-giant-number-that-doesnt-match-the-data, no rainbow palettes.

### 6. State coverage (the part most "done" designs skip)

Per the design completeness rule, every component I author gets the states from the `states.md` matrix. Every page gets the fault states from the screen-level taxonomy. Concretely for this project:

**Per-component states.** Default, hover, focus, pressed, disabled, loading, error, success, skeleton, in-component empty, partial-failure. Inputs additionally get filled and focused-with-error. I'd author these as variant siblings inside each `reusable: true` component (`Button_Default`, `Button_Hover`, etc.) — clearer than a `state` theme axis when there are this many states.

**Per-page states.** For each dashboard / report / list page:

- **First-use empty** ("You haven't created any dashboards yet. Create your first.")
- **No-results empty** (filters return nothing — distinct copy from first-use, primary CTA is "Clear filters" not "Create")
- **No-permission empty** (viewer role hits an editor-only page — "Request access" or "Contact admin")
- **Loading** (skeleton screens matching tile and chart shapes; staggered reveal as data arrives — chrome instant, data 800ms, charts 1500ms)
- **Partial failure** (one tile errored; the rest render normally with an inline error block + retry on the failed tile — never page-wide error wall when one widget broke)

**Screen-level fault pages.** 404, 403, 500, 503, offline. Built as sibling top-level frames sharing one `ErrorBlock` component from the library. Each instantiates via `ref` with `descendants` overrides for title / description / icon / CTA. Copy follows `voice.md` — concrete, no "An error occurred", no "the dev team has been notified" filler.

**Offline.** For analytics specifically: banner pattern (non-blocking) is right because the page is still useful read-only when cached data is shown. Pending-write reconciliation (alert rule edited offline) shows quiet "synced" indicator on reconnect, not a celebratory toast.

### 7. Flows that cross screens

Per `flows.md`, anything multi-screen needs documented decisions:

- **Modal-vs-page-vs-sheet decisions.** Filter drawer is a sheet on mobile, popover on desktop. Tile detail / drilldown is a routed page (deep-linkable, refreshable). "Delete dashboard" is a hard-confirm modal naming the thing. "Hide tile" is a soft confirmation with undo toast.
- **Validation timing.** Date range pickers, alert thresholds, segment definitions — sync on-blur for format, on-submit for cross-field and async. Long forms (alert builder, segment builder) get a submit-time summary banner that focuses-on-click.
- **Back-stack.** Drilldown via tile click should `pushState`. Filter changes should update the URL (`/dashboard?range=30d&segment=enterprise`) so refresh restores them — this is one of the most common SaaS frustrations when missing. Modal opens use `replaceState` so back closes the modal, not the page.
- **Deep links.** Filters, sort, selected tab, selected item, page-in-pagination all live in the URL. Modal-open state, dirty-form state, scroll position do not.
- **Optimistic UI.** Toggling a tile's visibility, favouriting a dashboard, marking an alert acknowledged — yes, optimistic. Editing alert thresholds or saving a segment — no, those go through a real loading state. Document the choice in each component's `context` so engineering ships the rollback logic.
- **Real-time / presence.** If multiple users edit the same dashboard, avatar pile in TopNav showing who else is viewing; "Last edited by X 2 minutes ago" indicators on saved dashboards; subtle banner when someone else is editing the same tile.

### 8. AI surfaces (if applicable)

If your product has any AI affordances — natural-language query, AI summaries, anomaly detection narratives, suggested insights — `modern-patterns.md` § AI-UI gives the rules:

- **Disclosure.** Sparkle + "AI" badge on AI-generated content. Footer note when an entire summary is AI: "Summary written by AI."
- **Regenerate.** Small icon button near generated content. Don't blank the prior on regenerate; overlay loading so the user can compare.
- **Confidence.** "Best guess" / "Verify before sharing" not "82%". Numeric confidence is opaque to non-technical users.
- **Inline citations.** Numbered superscripts that expand to a popover with source title + link — not a wall of links at the end.
- **Abort controls.** Stop button visible during streaming. A hard square or X, not a triangle.
- **No fake typewriter.** If the response arrives whole, render it whole.

### 9. Voice and copy

Per `voice.md` (which I'd scaffold if absent), every empty state, error, confirmation, and toast gets concrete copy. Banned: "An error occurred", "Elevate", "Seamless", "Unleash", "Next-Gen", "Empower", `John Doe`, `Acme`, `Lorem Ipsum`. For mock data per `flows.md` § Plausible content: real-shape KPIs (not all multiples of 10, some up some down), domain-specific dashboard names ("Q4 Activation funnel" not "Project Apollo"), realistic time clustering in activity feeds, varied name and email shapes in user lists.

### 10. Accessibility (built in, not bolted on)

The five baseline checks from SKILL.md run as part of verification:

1. WCAG AA contrast (4.5:1 body, 3:1 large/UI), tested in **both** modes.
2. Hit targets ≥ 44x44 even for 16px icon buttons.
3. Colour is never the only signal — status pills and chart-series legends pair text + colour + (often) icon.
4. Names map to roles (`PrimaryAction`, `FormError`, `SectionHeading`) so code generators downstream consume them.
5. Every component has a focus state — even if it's just a 2px `$focusRing` outline at 2px offset.

For `references/accessibility.md` topics — focus order through a complex dashboard, keyboard nav of tiles, screen-reader content for charts, `prefers-reduced-motion` for skeleton shimmer and staggered reveal — I'd reference them per page where they apply.

### 11. Code-export contract

`code-export.md` documents how Pencil concepts map to your stack. For a SaaS analytics product, engineering needs to know: which icon library (Lucide / Material Symbols / Phosphor), which chart library, which form library, which date library, how component variants map (e.g. shadcn-style `cva` variants vs styled-components vs Tailwind classes vs CSS modules). Pinning this before component build saves a translation pass.

## What I'd do unprompted if you said "just go"

If you genuinely want me to start without answering the questions above, my defensible defaults would be:

- Product analytics flavour (Mixpanel-shaped). Multi-tenant with workspace switcher. Admin / editor / viewer roles. Real-time-ish (5-minute-fresh, not live-streaming). Web + responsive down to mobile, no native app.
- Stack assumption: React + TypeScript + Tailwind + shadcn/ui + Recharts + Lucide icons. (Easy to change if wrong.)
- One accent hue, low saturation. Zinc neutrals. Geist + Geist Mono typography. Off-white surfaces, never `#FFFFFF`. Off-black for dark, never `#000000`.
- Density: dense (it's a dashboard). Variance: symmetric. Motion: static with skeleton shimmer and `$durationFast` interactions only.

I would still ask before scaffolding `design-system/` (it's a one-time offer per session, and I want explicit yes / no on the optional templates).

## My execution plan, when you give the go-ahead

1. **Detect host.** `get_editor_state({ include_schema: false })`. If it errors, I stop and tell you to open the Pencil app or extension. No silent CLI fallback.
2. **Locate context.** Note which `.pen` is open, what's selected, document version. Check the project filesystem (with a directory listing, not the MCP) for `design-system/`.
3. **Load guidelines + inventory.** `get_guidelines()` first, then the categories that match (`Web App`, `Dashboard`, `Table`, `Design System`, plus `Tailwind` if that's the stack). `get_variables()` to see what tokens exist. `batch_get({ patterns: [{ reusable: true }], readDepth: 2 })` against the open doc and any imported `.lib.pen` to inventory components.
4. **Plan.** Two or three sentences naming the atmosphere ("dense, symmetric, static"), the top-level frames I'll create (per-breakpoint sets per page), the components I'll instantiate by id, and roughly the layout. This is the cheap moment to catch bad assumptions.
5. **Execute.** A sequence of `batch_design` calls, each ≤ 25 ops. Outermost frames first; if the canvas is populated, `find_empty_space_on_canvas` for placement coords. Use `foo=I("parent", {...})` binding for new ids. `G(node, "ai", "<prompt>")` or `G(node, "unsplash", "<query>")` for any imagery — never grey "Image" rectangles. Every node gets a meaningful PascalCase name and a `context` string explaining its role.
6. **Verify (structural-first).** `batch_design` response confirms ops landed. `snapshot_layout(parentId, maxDepth: 2)` confirms structure (gaps, padding, sizing) — this is the default verification tool. `batch_get({ nodeIds: [...] })` confirms property-level intent (variables bound, refs resolved). `get_screenshot(nodeId)` only when the question is genuinely visual — final sign-off, real-rendered contrast, image content, rhythm at scale. One or two screenshots total for the whole job, scoped to the smallest meaningful subtree, not the page frame.
7. **Iterate or report.** Targeted `U` or `R` ops for any issues; one-paragraph summary when it's clean.

## Tools I'd reach for, with expected shapes

- `get_editor_state({ include_schema: false })` → returns `{ activeDocument, selection, schemaVersion, imports, ... }`. I check that a `.pen` file is open and which.
- `get_guidelines()` → returns the list of available categories for this document. Then `get_guidelines({ categories: ["Web App", "Dashboard", "Table"] })` or similar. I read the ones that match the task.
- `get_variables()` → returns `{ variables: { ... } }`. I read it before any `set_variables` call so I never clobber existing tokens.
- `batch_get({ patterns: [{ reusable: true }], readDepth: 2 })` → returns `reusable: true` nodes in the open doc. Repeated with `filePath: "./design/system.lib.pen"` for each imported library. I use this to build a mental inventory of components that already exist.
- `batch_get({ nodeIds: ["ButtonPrimary"], readDepth: 4 })` → for any unfamiliar component I'm about to instantiate, deep read to identify slots, named children (valid `descendants` keys), and theme variants. Per `references/component-anatomy.md`.
- `find_empty_space_on_canvas` → if the canvas has existing top-level frames, returns coordinates I should pass as `x` / `y` on my outermost frame. Avoids invisible overlap.
- `set_variables({ variables: { ... }, replace: false })` → only for tokens absent from the `get_variables` result. Each colour carries both `mode: light` and `mode: dark` values.
- `batch_design` → the main authoring tool. Ops grammar: `foo=I("parent", { type, name, context, ... })`, `R("id", { ... })`, `U("id", { ... })`, `C("source", "parent", { ... })`, `G("id", "ai", "<prompt>")`. ≤ 25 ops per call, ids no `/`, sizing as `width: "fill_container"` / `width: "fit_content"` bare strings, colours as `"$variableName"` over raw hex, `padding: [top, right, bottom, left]` (no `paddingTop`), `stroke.fill` singular.
- `snapshot_layout({ nodeId: "<page>", maxDepth: 2 })` → structural verification. Returns positions, sizes, gaps as numbers. My default verification tool, not a niche one.
- `get_screenshot({ nodeId: "<smallest meaningful subtree>" })` → reserved for final sign-off and genuinely-visual questions. One or two for the whole job.
- `export_nodes` → if and when you ask for handoff assets (PNG / SVG / PDF). I'd ask for format and destination path before calling.

## What I'd verify before declaring done

Per the design-completeness rule, I won't mark this done until:

1. Every component I authored has its required state set (matrix in `states.md`).
2. Every page has its fault states (404 / 403 / 500 / 503 / offline) and its empty states (first-use / no-results / no-permission where relevant).
3. Every component has a focus state visible in both modes.
4. Body text contrast ≥ 4.5:1, large/UI text ≥ 3:1, in both modes.
5. Hit targets ≥ 44x44 for every interactive element.
6. No raw `#000000` or `#FFFFFF` bound directly. All colours via variables.
7. No banned patterns: Inter, generic serifs, neon glow, three-card "features" grids as the dashboard default, fabricated metrics, `John Doe` / `Acme` / `Lorem Ipsum`.
8. Every non-trivial node has a meaningful PascalCase `name` and a `context` string explaining its role and any flow / optimism / validation behaviour engineering needs to ship.
9. All filters, sort, selected tab, and page-in-pagination state lives in URL parameters per the deep-link rules in `flows.md`.

## My ask

Tell me which of the seven scoping questions you want to answer (minimum: product flavour, real-time-ness, build target), and whether to scaffold `design-system/` if it's not there. Once I have those, I'll give you the 2–3 sentence plan, then start building.
