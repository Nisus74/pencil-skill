# Pencil MCP tools — cookbook

The full surface of the Pencil MCP server: thirteen tools, what each is for, when to reach for it, when not, and a worked invocation. Load this when you need a tool you haven't used before, when a tool errors in a way you don't recognize, or when planning a multi-step task and you want to pick the cheapest path.

This file does **not** restate `batch_design`'s op grammar — that lives in [`batch-design-grammar.md`](batch-design-grammar.md). The `batch_design` section here is a stub that points out.

## Reading this file

For each tool: a one-line purpose, a "when to reach for it" line, a "when not to" line, a worked call, and pitfalls. Tools are grouped by phase of work — *connect, read, write, verify, audit, export*.

| Phase | Tools |
|-------|-------|
| Connect | `get_editor_state`, `open_document` |
| Reference | `get_guidelines` |
| Read / inspect | `batch_get`, `get_variables`, `snapshot_layout`, `get_screenshot` |
| Write | `batch_design`, `set_variables`, `replace_all_matching_properties` |
| Audit | `search_all_unique_properties`, `find_empty_space_on_canvas` |
| Export | `export_nodes` |

## Connect

### `get_editor_state`

**Purpose.** Ping the host. Returns the active document's path (if any), the current selection, and (optionally) the document schema.

**Reach for it.** First action of every task. Without a successful response, every other MCP call fails with `transport not connected to app: desktop`.

**Don't reach for it** in the middle of a long batch of writes; it doesn't refresh meaningfully and the MCP server is the source of truth either way.

**Worked call.**

```
get_editor_state({ include_schema: false })
```

Set `include_schema: true` only when you need the full schema for a downstream validation (rare — `pen-schema.md` documents it statically). The schema payload is large.

**Pitfalls.** A succeeding call with no active document is *not* a failure — it just means the user hasn't opened a `.pen`. Branch into the "no document open" failure path (SKILL.md § Failure modes §2).

### `open_document`

**Purpose.** Open an existing `.pen` or create a new one.

**Reach for it.** When `get_editor_state` reports no active document and the user has confirmed they want one. Use `"new"` for greenfield, an absolute or relative path for an existing file.

**Don't reach for it** if the user already has a `.pen` open in the editor — operate on that one. Opening a second document silently switches the editor's focus.

**Worked call.**

```
open_document({ path: "new" })
open_document({ path: "./screens/onboarding.pen" })
```

The server returns the document root id. The next `get_editor_state` will reflect the change.

**Pitfalls.** A relative path is resolved against the host's working directory, which may not be the user's repo root. Prefer absolute paths or paths the user typed verbatim.

## Reference

### `get_guidelines`

**Purpose.** Load Pencil's built-in design guidelines for a category (typography rules, color guidance, mobile patterns, etc.). These are server-maintained and load fresh per task.

**Reach for it.** Step 3 of the workflow, before planning any design. Different task shapes need different categories — a marketing landing page draws on different guidelines than a settings page.

**Don't reach for it** for one-off edits to existing nodes ("change this color", "swap this label") — the guidelines won't tell you anything the existing design doesn't already encode.

**Worked call.** Always call once with no args first to discover the live category list:

```
get_guidelines()
```

Then load specific categories:

```
get_guidelines({ category: "Web App" })
get_guidelines({ category: "Tailwind" })
```

**Categories live as of 2026-05** (call with no args to confirm — the list can change):

| Category | Load when… |
|----------|-----------|
| `Code` | Generating code from a `.pen`, scaffolding a `.lib.pen`, or working on the design-to-code boundary. |
| `Design System` | Building or editing reusable components, scaffolding a `design-system/` folder, or auditing token usage. |
| `Landing Page` | Marketing surfaces, hero sections, pricing pages, signup flows targeting conversion. |
| `Mobile App` | Native iOS / Android / React Native / Flutter / SwiftUI work. Mobile-web that should *feel* native. |
| `Slides` | Presentation decks, slide layouts, talk visuals. |
| `Table` | Data tables, dashboards, spreadsheet-shaped UIs, admin grids. |
| `Tailwind` | Project ships Tailwind v4 — load alongside whichever surface category fits (Web App / Landing Page / etc.). |
| `Web App` | Product UI in a browser — dashboards, settings, forms, list+detail. The default for SaaS work. |

**Decision shortcuts:**

- *Dashboard task* → `Web App`, `Table` (if data-heavy), `Tailwind` (if stack matches), `Design System`. Also load `references/chart-anatomy.md` — it has the exact Pencil node tree, pixel values, and anti-examples for every chart type you will build.
- *Native iOS app* → `Mobile App`, `Design System`.
- *Pricing or marketing page* → `Landing Page`, `Design System`.
- *Building a `.lib.pen` from scratch* → `Design System`, `Code`.
- *Pitch deck* → `Slides`.
- *Admin grid / data-heavy table* → `Table`, `Web App`.

**Pitfalls.** Loading three or four categories at once burns context for limited gain. Pick the one or two most relevant; reach for more only if the first pass leaves an obvious blind spot.

**Guidelines carry generic defaults. The archetype overrides them.** The built-in guidelines teach schema syntax and accessibility constraints — both worth following. Their *stylistic* defaults (chart types, surface colours, shadow use) are generic and will produce AI-slop output if applied without filtering. After reading guidelines, consult the chosen archetype and override any stylistic default that conflicts.

The most common overrides:

| What the guideline says | When to override | What to use instead |
|-------------------------|------------------|---------------------|
| "Prefer bar charts for data" | Always on sparklines inside KPI cards | Sparkline bars: explicit `width: 3`, `height: <N>`, `gap: 2`, parent `alignItems: "flex_end"`. Never `fill_container` on bar width. See `batch-design-grammar.md` for the exact anatomy. |
| Blue/purple gradient fills on charts | When archetype is `analytics-dashboard` or `modern-pro-tool` | Flat `fill: "$accent"`. No gradients on data bars. |
| Card drop shadows everywhere | `analytics-dashboard` archetype | Hairline `stroke: { color: "$border", thickness: 1 }`, no shadow at all. |
| Inter as UI font | Unless archetype explicitly opts in (e.g., `modern-pro-tool`) | `Geist` for UI text, `Geist Mono` for numerals and data. |
| Dark sidebar + white body as default shell | Unless user direction or archetype calls for it | `analytics-dashboard` defaults to an all-light layout. Dark sidebar is not a neutral default. |

## Read / inspect

### `batch_get`

**Purpose.** Read nodes — by id list, by pattern match, by depth-first scan. Returns full property JSON.

**Reach for it.** When you need to see the current shape of something before editing it. Three common patterns: (a) inventory components (`patterns: [{ reusable: true }]`), (b) inspect a known node by id, (c) scan a library (`filePath: "./design/system.lib.pen"`).

**Don't reach for it** to verify a structural change you just made — `snapshot_layout` is cheaper for layout numbers. Use `batch_get` for property-level confirmation (a variable resolved correctly, a `ref` instantiated correctly, a text body matches).

**Worked calls.**

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ nodeIds: ["loginButton", "loginForm"] })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ nodeIds: ["LoginPage"], readDepth: 4, resolveInstances: true, resolveVariables: true })
```

**Cost levers.**

- `readDepth` — how deep to walk children. `2` for inventory, `4` for thorough inspection of a subtree, omit for full depth (expensive).
- `resolveInstances` — when `true`, `ref` nodes return their resolved component shape, not just `{ ref: "..." }`. Use sparingly; payloads grow fast.
- `resolveVariables` — when `true`, `"$primary"` is replaced with its current value. Useful for contrast checking; otherwise leave off so you see the binding.
- `searchDepth` — how deep pattern matching scans before giving up. Defaults are usually fine.

**Pitfalls.** Calling without `nodeIds` AND without `patterns` returns the whole document — fine for small docs, ruinous for large ones. Always scope.

### `get_variables`

**Purpose.** Read all document-level design tokens.

**Reach for it.** Before you author tokens for a new doc (so you don't duplicate). Before adding a theme axis. Before binding a color you're not sure exists. As a sanity check after `set_variables`.

**Don't reach for it** for every single color usage — once you have the token list in mind, just bind by name (`"$primary"`).

**Worked call.**

```
get_variables()
```

Returns an object keyed by variable name, with `{ type, value }` per entry. Theme-aware variables return a `value` array of `{ value, theme }` entries.

**Pitfalls.** `get_variables` only returns the *current* document's tokens. Imported library tokens (via `imports`) are visible by reference but not in this call's response.

### `snapshot_layout`

**Purpose.** Numerical layout state — positions, sizes, gaps, flex behavior — without rendering pixels.

**Reach for it.** Verification ladder rung 2. The default after any structural `batch_design` call. Cheap and decisive for "did the layout do what I asked?".

**Don't reach for it** to verify property changes that aren't layout-shaped (a color, a label text). `batch_get` is right for those.

**Worked calls.**

```
snapshot_layout({ parentId: "LoginPage", maxDepth: 2 })
snapshot_layout({ parentId: "LoginPage", maxDepth: 3, problemsOnly: true })
```

**Cost levers.**

- `maxDepth` — how deep to walk. `2` is enough for most "did the gap land?" questions. `3-4` for nested layouts.
- `problemsOnly: true` — returns only nodes with computed-layout issues (overflow, undefined sizes). Useful when you're hunting for what broke.

**Pitfalls.** A snapshot doesn't tell you whether two adjacent buttons *visually* read as the same height — fonts and stroke can shift perceived size. For that, climb to `get_screenshot`.

### `get_screenshot`

**Purpose.** Rendered pixel preview of a node and its descendants.

**Reach for it.** Verification ladder rung 4 — the most expensive. Use only when the question genuinely needs pixels: contrast under real rendering, image content (AI-generated assets, photos), spacing/type rhythm at scale, or final sign-off before handing back.

**Don't reach for it** to "check progress" between writes. Don't screenshot the document root when a card subtree would do. Don't screenshot both light and dark modes for designs built entirely from variables — the variable system guarantees mode parity.

**Worked call.**

```
get_screenshot({ nodeId: "LoginCard" })
```

**Pitfalls.**

- Always pass the most specific `nodeId` containing the change. Page-frame screenshots are 5× the tokens of card screenshots and reveal nothing extra.
- Screenshots are PNG by default; the model receives them as image input. They count against context, not just billing — keep the cadence to ~one per task.
- For asset handoff (export to a file), use `export_nodes`, not `get_screenshot`.

## Write

### `batch_design`

**Purpose.** Mutate the document — insert, copy, replace, update, delete, move nodes; generate AI/stock images on existing nodes.

See [`batch-design-grammar.md`](batch-design-grammar.md) for the full op grammar (`I`, `C`, `R`, `U`, `G`, `D`, `M`), binding syntax, the ≤25-ops chunking rule, sizing/color rules, and common error fixes.

**Reach for it.** Every time you're changing the document. This is the workhorse.

**Don't reach for it** to declare a token suite at the top of a fresh doc — `set_variables` is purpose-built for that and it's cleaner. Don't reach for it to bulk-rewrite a property value across many nodes — `replace_all_matching_properties` exists for that.

### `set_variables`

**Purpose.** Bulk add or update document-level variables. Replaces or merges with the existing variable set.

**Reach for it.** The right way to bootstrap a token suite at the start of a new document. Also the right way to add a missing token mid-task (e.g. an `$illustration` color you discovered you need).

**Don't reach for it** for one-shot edits inside a `batch_design` call — if you're changing a single token's hex value as part of a wider edit, `U("doc", { variables: { primary: { ... } } })` works too.

**Worked call — declaring a full token suite for a new doc:**

```
set_variables({
  variables: {
    surface:        { type: "color",  value: [
      { value: "#FAFAFA", theme: { mode: "light" } },
      { value: "#0B1117", theme: { mode: "dark"  } }
    ] },
    surfaceMuted:   { type: "color",  value: [
      { value: "#F4F4F5", theme: { mode: "light" } },
      { value: "#18181B", theme: { mode: "dark"  } }
    ] },
    border:         { type: "color",  value: [
      { value: "#E4E4E7", theme: { mode: "light" } },
      { value: "#27272A", theme: { mode: "dark"  } }
    ] },
    textPrimary:    { type: "color",  value: [
      { value: "#0B1117", theme: { mode: "light" } },
      { value: "#FAFAFA", theme: { mode: "dark"  } }
    ] },
    textMuted:      { type: "color",  value: [
      { value: "#52525B", theme: { mode: "light" } },
      { value: "#A1A1AA", theme: { mode: "dark"  } }
    ] },
    primary:        { type: "color",  value: [
      { value: "#1F6FEB", theme: { mode: "light" } },
      { value: "#3B82F6", theme: { mode: "dark"  } }
    ] },
    primaryMuted:   { type: "color",  value: [
      { value: "#DBEAFE", theme: { mode: "light" } },
      { value: "#172554", theme: { mode: "dark"  } }
    ] },
    danger:         { type: "color",  value: [
      { value: "#DC2626", theme: { mode: "light" } },
      { value: "#F87171", theme: { mode: "dark"  } }
    ] },
    success:        { type: "color",  value: [
      { value: "#16A34A", theme: { mode: "light" } },
      { value: "#4ADE80", theme: { mode: "dark"  } }
    ] },
    focusRing:      { type: "color",  value: [
      { value: "#1F6FEB", theme: { mode: "light" } },
      { value: "#3B82F6", theme: { mode: "dark"  } }
    ] },

    "space-1": { type: "number", value: 4   },
    "space-2": { type: "number", value: 8   },
    "space-3": { type: "number", value: 12  },
    "space-4": { type: "number", value: 16  },
    "space-5": { type: "number", value: 24  },
    "space-6": { type: "number", value: 32  },
    "space-8": { type: "number", value: 48  },
    "space-12": { type: "number", value: 128 },

    textXs:    { type: "number", value: 12 },
    textSm:    { type: "number", value: 14 },
    textBase:  { type: "number", value: 16 },
    textLg:    { type: "number", value: 18 },
    textXl:    { type: "number", value: 20 },
    text2xl:   { type: "number", value: 24 },
    text3xl:   { type: "number", value: 32 },
    text4xl:   { type: "number", value: 48 }
  },
  replace: false
})
```

**Pitfalls.**

- `replace: true` wipes the existing variable set and applies only what you pass. Almost never what you want — leave `replace: false` (the merge default) unless you're consciously resetting tokens.
- Theme-aware values require the document to declare matching theme axes first (`U("doc", { themes: { mode: ["light", "dark"] } })`). Set the axes, then call `set_variables`.
- A theme-aware variable's `value` is an array; a flat variable's `value` is a scalar. Mixing the two shapes for the same variable across calls causes silent corruption.

### `replace_all_matching_properties`

**Purpose.** Bulk swap: every node under given parents whose property `from` matches gets that property updated to `to`.

**Reach for it.** Tokenization passes (rewrite raw `#1F6FEB` to `$primary` everywhere), refactors (rename a font family, update a corner radius globally), drift cleanup. The canonical companion to `search_all_unique_properties`.

**Don't reach for it** for one or two changes — `U` ops are clearer when you can name the targets.

**Worked call.**

```
replace_all_matching_properties({
  parents: ["LoginPage"],
  properties: [
    { property: "fillColor",   from: "#1F6FEB", to: "$primary" },
    { property: "cornerRadius", from: 8,         to: "$radiusMd" }
  ]
})
```

Returns a count of replacements per property mapping.

**Pitfalls.**

- Always run `search_all_unique_properties` first to confirm the set you're replacing — otherwise you might rewrite a value that's *legitimately* a one-off elsewhere in the file.
- Numeric `from` values match exactly. `8` matches `8`, not `8.0` or `"8"`.
- `parents` is a list of subtree roots. Pass the document root id to span the whole doc.

## Audit

### `search_all_unique_properties`

**Purpose.** Audit pass — for given parents, return every distinct value seen for the listed properties.

**Reach for it.** Pre-refactor (before a `replace_all_matching_properties`), drift detection (how many distinct shadow values are in this doc?), a11y audit (every text color present in this view), pre-tokenization (what raw colors are in use?).

**Don't reach for it** when you already know the values you're targeting — go straight to `replace_all_matching_properties`.

**Worked call.**

```
search_all_unique_properties({
  parents: ["doc"],
  properties: ["fillColor", "textColor", "fontSize", "cornerRadius", "shadowBlur"]
})
```

Returns each property name mapped to a list of unique values.

**Pitfalls.** A value of `"$primary"` and a value of `#1F6FEB` are different unique values, even if they currently resolve to the same color. That's a *feature* — it surfaces variable drift you should fix.

### `find_empty_space_on_canvas`

**Purpose.** Locate empty canvas coordinates of a given size, away from existing nodes.

**Reach for it.** Before placing a new top-level frame on a populated canvas. Any time the user has multiple top-level frames already on the canvas and you're about to add another — call this in step 4 (Plan), pass the returned position as `x`/`y` on the outermost frame in your first `batch_design` call.

**Don't reach for it** for nested children — auto-layout positions those automatically.

**Worked call.**

```
find_empty_space_on_canvas({
  width: 1440,
  height: 900,
  padding: 80,
  direction: "right"
})
```

Returns `{ x, y }` of an empty region. `direction` biases search ("right" places to the right of existing content; "bottom" places below).

**Pitfalls.** Calling without `direction` returns *some* empty region, but on a wide canvas this can be far away from where the user is looking. Bias toward the user's current selection or the most-recently-edited frame.

## Export

### `export_nodes`

**Purpose.** Render nodes to image/PDF files on disk. The handoff path.

**Reach for it.** When the user asks for assets ("export this", "give me a PNG of the hero", "generate the icon set"). When packaging for engineering handoff.

**Don't reach for it** to inspect what something looks like — that's `get_screenshot`. Don't substitute screenshots for exports either; screenshots aren't sized like exports and don't have predictable filenames.

**Worked call.**

```
export_nodes({
  nodeIds: ["HomePage_Desktop", "HomePage_Mobile"],
  format: "png",
  scale: 2,
  outputDir: "./design/exports/"
})
```

**Format choices.**

- `png` — UI assets, screenshots-as-deliverables, anything that needs alpha.
- `jpeg` — large hero photos, where alpha doesn't matter and file size does.
- `webp` — modern web; smaller than PNG/JPEG for the same quality.
- `pdf` — print, slide decks, vector handoff.

**Pitfalls.**

- Always confirm format with the user if not specified. PNG is a safe default for UI; PDF is right for slides/print.
- `outputDir` is relative to the host's working directory. Pass an absolute path when the user names one.
- `scale: 2` is the default for retina-quality assets. Bump to `3` only when explicitly required (App Store screenshots, 3× phone density).

## Composite recipes

### Token audit & cleanup

The `search` → review → `replace` workflow:

1. Run an audit pass to see what's in use:

   ```
   search_all_unique_properties({
     parents: ["doc"],
     properties: ["fillColor", "textColor", "cornerRadius", "fontSize"]
   })
   ```

2. Compare against `tokens.md` — note raw values that should be variables, and divergent values that should collapse.
3. Run a tokenization pass:

   ```
   replace_all_matching_properties({
     parents: ["doc"],
     properties: [
       { property: "fillColor",    from: "#1F6FEB", to: "$primary" },
       { property: "cornerRadius", from: 8,          to: "$radiusMd" }
     ]
   })
   ```

4. Re-run `search_all_unique_properties` to confirm the rewrite landed and nothing odd was missed.

### Greenfield document bootstrap

Setting up a brand-new `.pen`:

1. `open_document({ path: "new" })` — get a fresh doc id.
2. `U("doc", { themes: { mode: ["light", "dark"] } })` via `batch_design` — declare the theme axis first.
3. `set_variables({ variables: { ... }, replace: false })` — declare the full token suite.
4. First `batch_design` — page frame + skeleton (≤10 ops).
5. `snapshot_layout({ parentId: "<page>", maxDepth: 2 })` — confirm structure.
6. Region-by-region `batch_design` calls — fill in.
7. Final `get_screenshot({ nodeId: "<page>" })` — sign-off.

### Library import smoke test

Pulling a `.lib.pen` into a doc and confirming components resolve:

1. `U("doc", { imports: { "ds": "./design/system.lib.pen" } })` via `batch_design`.
2. `batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })` — see what the library exposes.
3. Insert a single `ref` to a known component:

   ```
   test=I("doc", { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Smoke" } } })
   ```

4. `batch_get({ nodeIds: ["test"], resolveInstances: true })` — confirm the library component resolved (not an error).
5. `D("test")` once you've confirmed.

## Tool cost cheatsheet

Order roughly cheapest → most expensive in tokens / context:

| Tool | Payload shape | Cost |
|------|---------------|------|
| `find_empty_space_on_canvas` | One `{ x, y }` pair | Trivial |
| `set_variables` | Echoed variables block | Small |
| `get_variables` | Variables block | Small |
| `replace_all_matching_properties` | Replacement counts | Small |
| `search_all_unique_properties` | Lists of unique values | Small–medium |
| `snapshot_layout` | Nested numbers | Small–medium |
| `batch_design` | Op success + new ids | Small for short calls; medium for max-25 |
| `batch_get` | Full node JSON | Medium → large with depth and `resolveInstances` |
| `get_editor_state` | Document/selection metadata | Small (large with `include_schema: true`) |
| `get_guidelines` | Markdown text | Medium per category |
| `open_document` | Doc id + metadata | Small |
| `export_nodes` | File paths written | Small (the files themselves are on disk) |
| `get_screenshot` | PNG image | **Expensive** — image input to the model |

When two tools could answer the same question, pick the cheaper one and only climb if it doesn't resolve. The verification ladder in SKILL.md formalizes this for read-after-write; the same instinct applies for read-before-write planning.

## See also

- [`pen-schema.md`](pen-schema.md) — the underlying `.pen` data model, every node type and property.
- [`batch-design-grammar.md`](batch-design-grammar.md) — `batch_design` op grammar, binding, chunking, common errors.
- [`pencil-cli.md`](pencil-cli.md) — the CLI surface, when CLI is the right tool vs MCP.
- SKILL.md § Verification ladder — when to climb from `snapshot_layout` to `get_screenshot`.
- SKILL.md § Failure modes — the six concrete cases and their responses.
