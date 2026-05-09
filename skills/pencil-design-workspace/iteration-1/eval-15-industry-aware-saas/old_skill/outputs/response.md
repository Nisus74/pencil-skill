# Dashboard for a developer-tools SaaS

Good brief. Before I lay anything down on the canvas I want to name the audience-shaped decisions out loud, because "feels right for engineers" is the whole job and a generic SaaS dashboard would miss it.

## What "feels right for engineers" means here

Professional engineers reading a dev-tools dashboard at 9am are not the same audience as a marketing-ops team reading Salesforce. They will:

- Glance at numbers in monospace and trust them; glance at numbers in a soft sans-serif and re-read them.
- Skim 6–8 things on screen at once. Density is a feature, not a bug. Whitespace-heavy "elegant" dashboards waste their time.
- Open the page already knowing what they came for (a build, a deploy, a region's error rate). Hero greetings, "Welcome back" copy, and animated chevrons are friction.
- Notice when a status pill is colour-only. Many of them are colour-blind; all of them switch between dark and light mode constantly.
- Live in a terminal. The dashboard should feel like a respectful neighbour to the terminal, not a competing aesthetic.

So the atmosphere I'm committing to up front (per the skill's "name the atmosphere before you plan" rule, references/modern-patterns.md and SKILL.md aesthetic defaults):

**Dense, symmetric, static.** No cinematic motion. No marketing-grade hero. No three-column equal-card "stats" grid pretending to be a dashboard.

## Skill references I consulted and why

I read the SKILL.md cover-to-cover, then loaded:

- `references/modern-patterns.md` — to make sure I avoid 2026's already-dated defaults (glassmorphism, gradient-on-everything, three-card grids) and reach for the patterns engineers expect (skeleton loads, optimistic UI, modern dark mode with `color-scheme`, presence cues for shared dashboards, container queries for widgets reused at multiple sizes).
- `references/mcp-tools.md` — for the `get_guidelines` decision table. A dashboard task maps to **`Web App` + `Table` + `Design System`** (and `Tailwind` if the project ships it). I'd load those before planning.
- `references/component-anatomy.md` — because if the project has an existing `.lib.pen`, every metric tile, table row, and chart wrapper should be a `ref` to the library, not a hand-built lookalike. I need to know how to read slots and `descendants` paths before I instantiate.
- `references/states.md` first 80 lines — dashboards are 80% non-default states (skeleton on first load, empty for new accounts, partial-failure when one widget's API is down, error/403 when permissions narrow, 503 when the whole control plane is degraded). I'd load the rest at step 6 for fault-state coverage.

I did **not** load `flows.md` (no multi-screen flow asked for), `accessibility.md` deep dive (the SKILL baseline 5 covers what's relevant for this scope), or the `Landing Page` / `Mobile App` guidelines (wrong surface).

## What I'd do, step by step, against the Pencil MCP

### Step 1 — Detect the host

```
get_editor_state({ include_schema: false })
```

Expected response: an object with the active document path (or null), current selection, and document version. If it errors with `transport not connected to app: desktop`, I stop and tell you to open the Pencil desktop app or IDE extension. No silent CLI fallback.

What I'd check: is a `.pen` already open? If yes, I work in it. If not, I'd ask whether to `open_document({ path: "new" })` or open an existing file you name.

### Step 2 — Locate context

From the `get_editor_state` result I'd note: filename, selection, schema version, and the `imports` field (does it already point at a `.lib.pen`?). Then I'd list the project root via shell to look for a `design-system/` folder. The combination of (a) doc state, (b) library imports, (c) design-system docs determines whether I'm working from existing tokens or bootstrapping.

Three branches:

- **`design-system/` exists with a `.lib.pen` already imported.** Best case. I load `design-system/README.md`, then `design-system.md` and `tokens.md`, and I lean entirely on the existing component library. My job is to compose, not to invent.
- **`design-system/` exists, no library yet.** I follow tokens.md but build primitives. I'd flag that the patterns I'm about to ship — metric tile, status pill, log row — look reusable and offer to extract them into a `.lib.pen` after.
- **No `design-system/` folder.** I'd offer the scaffold once (per SKILL Failure mode §3), defaulting to including `data-viz.md` as an optional template since dashboards live or die on chart palettes and tile shape.

### Step 3 — Load guidelines + inventory components

```
get_guidelines()                              // discover live category list
get_guidelines({ category: "Web App" })       // primary
get_guidelines({ category: "Table" })         // dashboards are table-shaped
get_guidelines({ category: "Design System" }) // for component reuse
```

If the stack file mentions Tailwind v4, I'd add `Tailwind`. I'd not load `Landing Page` or `Mobile App` — wrong surface, burns context.

Then component inventory, both halves of the components-first rule:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "<each .lib.pen in imports>", patterns: [{ reusable: true }], readDepth: 2 })
```

What I'd check in the response: every `id` of a `reusable: true` node, its top-level children's ids, any `slot` markers, and any `theme` axes (especially a `state` axis). I'd hold a mental list — Button, Input, Select, Card, Badge, IconButton, etc. — and any data-viz primitives (Chart, Sparkline, MetricTile) that already exist.

For any unfamiliar reusable I plan to use, a deeper read:

```
batch_get({ nodeIds: ["MetricTile"], readDepth: 4 })
```

— so I know its slots and the `descendants` path to set the value, label, delta, and sparkline. This is what `references/component-anatomy.md` exists for.

Then tokens:

```
get_variables()
```

Mandatory before any token work. If the doc has a populated set already, I treat it as authoritative and only declare what's missing. I never call `set_variables` with a full default suite on an existing doc — that clobbers the user's customisations even with `replace: false`, because the merge default still overwrites named keys.

### Step 4 — Plan (state to you before any write)

Atmosphere: **dense, symmetric, static.** Audience: **professional engineers.**

The dashboard I'd build, sized 1440×900 for desktop primary, with a tablet (768) and mobile (390) sibling frame to follow:

```
DashboardPage_Desktop (1440 × 900, fill: $surface)
├── AppShell (horizontal layout)
│   ├── SideNav (256w, vertical)
│   │   ├── ProductLockup (logo + product name, monospace setting)
│   │   ├── EnvSwitcher (Production / Staging / Preview — segmented)
│   │   ├── PrimaryNav (Overview, Deployments, Logs, Metrics, Database, Functions, Settings)
│   │   └── UserBlock (avatar, email, status dot)
│   └── Main (vertical, fill_container)
│       ├── TopBar (project breadcrumb · region selector · time-range picker · cmd-K · presence avatars · theme toggle)
│       ├── StatusStrip (single horizontal row: Build status · Deploy status · Region health · Incident pill)
│       ├── MetricRow (4 monospace metric tiles — see below)
│       ├── ContentGrid (2-up, asymmetric: 2/3 + 1/3)
│       │   ├── RequestsChart (area chart, last 24h, p50/p95/p99 lines)
│       │   └── RecentDeploys (compact list, sha · branch · author · status · time)
│       └── LogsPanel (full-width, monospace stream with severity gutter, filter chips on top)
```

Why these choices, against engineer expectations:

- **Sidebar over top-tab nav.** Engineers expect persistent nav so they can pivot between Logs and Metrics in a beat. Top-tab nav makes them re-orient.
- **EnvSwitcher prominent and obvious.** The single most-feared mistake is "I just deployed to prod thinking it was staging." Make the current env unmissable; the switcher belongs at the top of the nav, not buried under Settings.
- **Status strip below the top bar, not above the fold.** First glance: is anything on fire? One row, four pills. If green, the eye moves on. If anything's red, it's the only thing they look at.
- **Metric tiles are monospace numbers.** Per SKILL aesthetic defaults: high-density layouts use a monospace font for figures. Tile shows: big number, label below, delta vs previous period, tiny sparkline. Four tiles: Requests, Error rate, p95 latency, Active deploys.
- **Asymmetric 2/3 + 1/3 split, not 3-up cards.** The three-column equal-card grid is called out in the SKILL anti-patterns as an AI tell. A real dashboard has hierarchy — the chart is more important than the deploy list, and the layout should say so.
- **Logs at the bottom, full width, monospace.** Engineers will spend more time looking at this panel than anywhere else. It deserves the width. Severity gutter on the left (single-character: `I W E F`) plus colour, never colour alone — that satisfies the SKILL accessibility check on "colour is never the only signal."
- **Presence avatars in the top bar.** Per `modern-patterns.md`, presence is no longer a collaboration-features-only concern. If two SREs are watching the same incident, the dashboard should say so.
- **`cmd+K` affordance shown in the top bar.** Engineers expect command palettes. Showing the keybinding pill (`⌘K`) communicates "this thing is fast and keyboard-driven" before they've even tried it.

What I'd build from primitives vs reach for components: I'd reach for `Button`, `IconButton`, `Input`, `Select`, `Badge`, and (if they exist) `MetricTile`, `Chart`, `Sparkline`, `LogRow`, `Avatar`, `Breadcrumb`, `SegmentedControl`. Anything not in the library I'd build once and surface it: *"StatusPill and LogRow look library-shaped — want me to add them to your `.lib.pen`?"*

### Step 5 — Execute

Multiple `batch_design` calls, ≤25 ops each, page-frame and main columns first, then fill in. I'd use the `foo=I("parent", {...})` binding pattern to chain ids, never hard-code an id I just created.

Token bindings I'd lean on (assuming the project has them; otherwise I'd declare only the ones missing):

- `$surface` / `$surfaceMuted` / `$surfaceRaised` for backgrounds (theme-aware light + dark).
- `$textPrimary` / `$textMuted` for type.
- `$borderSubtle` for hairline dividers between regions (modern dark mode swaps shadow for border per `references/modern-patterns.md` § Modern dark mode).
- `$success` / `$warning` / `$danger` / `$info` for status, **always paired with an icon**.
- `$accent` reserved for the single brand accent — used on the "Deploy" primary CTA and selected nav item, nowhere else. One accent, low saturation, per SKILL aesthetic defaults.
- Typography: `Geist` + `Geist Mono` if the stack is silent on fonts. Banned: `Inter` (AI tell), generic serifs, neon glow.

For sizing I'd use bare-string `width: "fill_container"` and `width: "fit_content"` per the batch_design grammar — never `"100%"`, never the older `{ sizing: ... }` object form.

For images (avatars, environment icons), I'd reach for `icon_font` — Lucide if the project hasn't named one — rather than importing SVGs.

### Step 6 — Verify (structural-first)

After the page-frame and main column ops:

```
snapshot_layout({ parentId: "DashboardPage_Desktop", maxDepth: 3 })
```

Cheap. Confirms the shell, the top bar height (typically 56), the sidebar width (256), the main column fill, and the gap rhythm. If any of those are off, fix with targeted `U` ops.

Then property checks on the bits where the binding matters:

```
batch_get({ nodeIds: ["MetricTile_Errors", "StatusStrip", "DeployButton"], resolveVariables: false })
```

I want to see `$accent` not `#xxxxxx` on the deploy button, and `$danger` plus an icon (not just a fill colour) on the error tile.

**One screenshot at the end**, scoped to the dashboard frame:

```
get_screenshot({ nodeId: "DashboardPage_Desktop" })
```

I scan it in the order from the SKILL verification ladder: layout integrity → spacing rhythm → type rhythm → contrast → component fidelity. Specifically for an engineer audience I'd also check: does the monospace numeric column align? Does the env switcher read as obviously the current environment? Does the status strip show severity through both icon and colour?

I'd **not** screenshot dark mode separately — every colour comes from a theme-aware variable, so the variable system guarantees mode parity. I'd flip the page's `theme: { mode: "dark" }` and re-screenshot **only** if I had reason to suspect a raw hex slipped through.

### Step 7 — State coverage and report

Before I'd call this done, the SKILL "design completeness" rule asks for state coverage. For a dashboard that means:

- **Skeleton.** The metric tiles, chart, deploy list, and logs panel all need a skeleton variant — first-load is the worst-case for engineers because the absence of data is itself information ("is the API down or is it loading?"). 1.4s shimmer per `motion.md`.
- **Empty.** A brand-new project has zero deploys. Empty state copy: *"No deployments yet. Push to `main` to ship one."* Plus a `gh` command snippet they can copy. Not *"You don't have any deployments — get started!"* — too marketing.
- **Partial failure.** If the metrics API is down but logs are fine, the metric tiles get an inline retry affordance, the rest of the page renders. Per `references/states.md` partial-failure recipe.
- **Error / degraded.** A 503 banner across the top when the control plane is degraded, with a status-page link. Not a full-page takeover.

These four are part of the deliverable; I'd build them as sibling frames or as state variants of each component.

For the responsive piece, I'd build `DashboardPage_Tablet` (768) and `DashboardPage_Mobile` (390) as siblings sharing the same components and variables. On tablet the asymmetric 2/3 + 1/3 collapses to stacked. On mobile the side-nav becomes a sheet behind a hamburger, the metric row becomes a horizontal scroll of cards, and the logs panel becomes the primary view.

When everything's landed, one paragraph back to you: what frames exist, which library components got instantiated vs built, what state variants are covered, which optional templates I'd recommend scaffolding (`data-viz.md` for sure, `mobile.md` if the project ships a mobile companion).

## Things I'd want from you before I started writing ops

Three short questions, only if the answers aren't already in the project:

1. **Stack and library.** Is there an existing `.lib.pen`? Tailwind v4? Geist or something else as the type stack?
2. **The product's actual surface.** Is this an infrastructure dashboard (deploys, regions, logs), an observability dashboard (traces, metrics, alerts), a data dashboard (queries, tables, jobs), or something else? The skeleton above leans infra; observability would swap the deploy list for a trace explorer, data would lead with a query editor.
3. **One brand accent or none.** If you have a brand colour, name it. If you don't, I'll default to a desaturated electric-blue or sodium-orange — both work in light and dark, both feel native to a developer tool, neither is the AI default of cobalt-on-white.

If you'd rather I just go, I'll assume infra-flavoured, infer the stack from the repo, and surface the brand-accent question only if I find no `tokens.md`.

---

**Artifact written:** `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-15-industry-aware-saas/old_skill/outputs/response.md`
