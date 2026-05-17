# Pencil MCP tools, cookbook

The full surface of the Pencil MCP server: thirteen tools, what each is for, when to reach for it, when not, and a worked invocation. Load this when you need a tool you haven't used before, when a tool errors in a way you don't recognise, or when planning a multi-step task and you want to pick the cheapest path.

This file does **not** restate `batch_design`'s op grammar, that lives in [`batch-design-grammar.md`](batch-design-grammar.md). The `batch_design` section here is a stub that points out.

## Reading this file

For each tool: a one-line purpose, a "when to reach for it" line, a "when not to" line, a worked call, and pitfalls. Tools are grouped by phase of work, *connect, read, write, verify, audit, export*.

**All Pencil MCP tools accept an optional `filePath`.** Omit it to target the active editor; pass an absolute path (or a path relative to the editor's working directory) to target a specific `.pen` file. Examples in this file omit `filePath` to focus on each tool's own shape, add it any time you're operating on a non-active file or want to be explicit.

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
get_editor_state({ include_schema: true })
```

Pass `include_schema: true` on the **first** call of every conversation. The server requires the schema be loaded once per session before any read or write operation. After that, subsequent calls in the same conversation can pass `include_schema: false` to skip the (large) schema payload. `pen-schema.md` is a static snapshot for offline reading; it does not substitute for loading the live schema.

**Pitfalls.** A succeeding call with no active document is *not* a failure, it just means the user hasn't opened a `.pen`. Branch into the "no document open" failure path (SKILL.md § Failure modes §2).

### `open_document`

**Purpose.** Open an existing `.pen` or create a new one.

**Reach for it.** When `get_editor_state` reports no active document and the user has confirmed they want one. Use `"new"` for greenfield, an absolute or relative path for an existing file.

**Don't reach for it** if the user already has a `.pen` open in the editor, operate on that one. Opening a second document silently switches the editor's focus.

**Worked call.**

```
open_document()
open_document({ path: "/abs/path/to/screens/onboarding.pen" })
```

Omit `path` entirely to create a new document. Pass an absolute path to open an existing `.pen`. The next `get_editor_state` will reflect the change.

**Pitfalls.** The path must be absolute when specified, relative paths are resolved against the host's working directory and that may not be the user's repo root. There is no `path: "new"` magic value; just leave the argument off. Don't open a second document while the user has one focused, it silently switches the editor.

## Reference

### `get_guidelines`

**Purpose.** Load Pencil's built-in design guidelines for a category (typography rules, color guidance, mobile patterns, etc.). These are server-maintained and load fresh per task.

**Reach for it.** Step 3 of the workflow, before planning any design. Different task shapes need different categories, a marketing landing page draws on different guidelines than a settings page.

**Don't reach for it** for one-off edits to existing nodes ("change this color", "swap this label"), the guidelines won't tell you anything the existing design doesn't already encode.

**Worked calls.** Three calls in order: discovery, guide load, optional style load.

**1. Discover.** Call with no args to list both top-level categories, `guide` (task guides) and `style` (visual archetypes):

```
get_guidelines()
```

**2. Load a guide.** Pass `category: "guide"` plus the guide's `name`:

```
get_guidelines({ category: "guide", name: "Web App" })
get_guidelines({ category: "guide", name: "Tailwind" })
```

**3. Load a style (optional).** Pass `category: "style"` plus the style's `name`. Style archetypes have **required params**; calling with no params returns the params signature. Call again with `params` filled in:

```
get_guidelines({ category: "style", name: "Soft Bento" })
get_guidelines({ category: "style", name: "Soft Bento", params: { colorPalette: "Warm Linen", roundness: "Basic Roundness", elevation: "Soft Lift", headings: "Playfair Display", body: "Geist", captions: "Geist", data: "Geist Mono" } })
```

**Guides**: `Code`, `Design System`, `Landing Page`, `Mobile App`, `Slides`, `Table`, `Tailwind`, `Web App`. Call `get_guidelines()` with no args to confirm the current list.

**Styles**: visual archetypes (variable list, examples include `Aerial Gravitas`, `Anchored Ribbon Grid`, `Artisan Editorial`, `Blueprint Technical`, `Cinematic Alternating`, `Color Block Stack`, `Dark Centered Platform`, `Editorial Scientific`, `Gradient Prompt Stack`, `Illustrated Warm`, `Modular Bento Showcase`, `Monumental Editorial`, `Product Data Grid`, `Soft Bento`, `Split Inverse Showcase`, `Zigzag Bold Split`, and others). Run `get_guidelines()` with no args for the current list, the set rotates between server releases.

**Decision shortcuts (guides):**

| Task | Load `name: ...` |
|------|------------------|
| Dashboard | `Web App`; `Table` if data-heavy; `Tailwind` if the stack matches; `Design System`. Also `references/chart-anatomy.md`. |
| Native iOS / Android app | `Mobile App`, `Design System`. |
| Pricing or marketing page | `Landing Page`, `Design System`. |
| Building a `.lib.pen` from scratch | `Design System`, `Code`. |
| Pitch deck | `Slides`. |
| Admin grid / data-heavy table | `Table`, `Web App`. |

**Style archetypes**: each style has a required `params` signature. The shared params across all observed styles are `colorPalette`, `roundness`, `elevation`, and four typography slots, `headings`, `body`, `captions`, `data`. Each takes a named value from the style's enum (e.g. `colorPalette: "Warm Linen"`, `headings: "Playfair Display"`). Two-step pattern: call with `{ category, name }` to see the enum, then call again with `params` filled in to load the instantiated style.

**Pitfalls.** Loading three or four guides at once burns context for limited gain. Pick the one or two most relevant; reach for more only if the first pass leaves an obvious blind spot. For styles, only load one, they're aesthetic archetypes, mixing two confuses direction.

**Guidelines carry generic defaults. Filter them against the stated aesthetic direction.** The built-in guidelines teach schema syntax and accessibility constraints, both worth following. Their *stylistic* defaults (chart types, surface colours, shadow use) are generic and will produce AI-slop output if applied without filtering. Read the guidelines for schema rules, then apply only the stylistic defaults that match the direction stated in step 2.

The most common stylistic overrides:

| What the guideline says | When to override | What to use instead |
|-------------------------|------------------|---------------------|
| "Prefer bar charts for data" | Always on sparklines inside KPI cards | Sparkline bars: explicit `width: 3`, `height: <N>`, `gap: 2`, parent `alignItems: "flex_end"`. Never `fill_container` on bar width. See `batch-design-grammar.md` for the exact anatomy. |
| Blue/purple gradient fills on charts | For data-dense product surfaces | Flat `fill: "$accent"`. No gradients on data bars. |
| Card drop shadows everywhere | For utility/data surfaces (not marketing or consumer surfaces) | Hairline `stroke: { color: "$border", thickness: 1 }`, no shadow at all. |
| Inter as UI font | When direction doesn't call for it | `Geist` for UI text, `Geist Mono` for numerals and data. |
| Dark sidebar + white body as default shell | For data products where the direction calls for all-light layout | Don't default to a dark sidebar. It's not a neutral choice. |

## Read / inspect

### `batch_get`

**Purpose.** Read nodes, by id list, by pattern match, by depth-first scan. Returns full property JSON.

**Reach for it.** When you need to see the current shape of something before editing it. Three common patterns: (a) inventory components (`patterns: [{ reusable: true }]`), (b) inspect a known node by id, (c) scan a library (`filePath: "./design/system.lib.pen"`).

**Don't reach for it** to verify a structural change you just made, `snapshot_layout` is cheaper for layout numbers. Use `batch_get` for property-level confirmation (a variable resolved correctly, a `ref` instantiated correctly, a text body matches).

**Worked calls.**

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ nodeIds: ["loginButton", "loginForm"] })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ nodeIds: ["LoginPage"], readDepth: 4, resolveInstances: true, resolveVariables: true })
```

**Cost levers.**

- `readDepth`, how deep to walk children. `2` for inventory, `4` for thorough inspection of a subtree, omit for full depth (expensive).
- `resolveInstances`, when `true`, `ref` nodes return their resolved component shape, not just `{ ref: "..." }`. Use sparingly; payloads grow fast.
- `resolveVariables`, when `true`, `"$primary"` is replaced with its current value. Useful for contrast checking; otherwise leave off so you see the binding.
- `searchDepth`, how deep pattern matching scans before giving up. Defaults are usually fine.
- `parentId`, scope pattern matching to a subtree. Cheaper than scanning the whole document for a known region.
- `includePathGeometry`, pass `true` only when you need to inspect a `path` node's raw SVG geometry. By default the server returns `"..."` for the `geometry` field to save tokens.

**Pitfalls.** Calling without `nodeIds` and without `patterns` returns the **top-level children of the document** (not the whole tree). This is intentional, useful for orientation, but don't rely on it for deep inspection. Always pass `nodeIds` or `patterns` when you want specific nodes.

### `get_variables`

**Purpose.** Read all document-level design tokens.

**You must call this before any token work on an existing document.** Not optional — mandatory. If it returns a non-empty set, the user's tokens exist and may be customised. Treat them as authoritative; only bootstrap the variables that are absent from the result. This applies equally before `set_variables` calls and before `U("doc", { variables: {...} })` ops.

Also reach for it: before adding a theme axis; before binding a color you're not sure exists; as a sanity check after `set_variables`.

**Don't reach for it** for every single color usage, once you have the token list in mind, just bind by name (`"$primary"`).

**Worked call.**

```
get_variables()
```

Returns an object keyed by variable name, with `{ type, value }` per entry. Theme-aware variables return a `value` array of `{ value, theme }` entries.

**Pitfalls.** `get_variables` only returns the *current* document's tokens. Imported library tokens (via `imports`) are visible by reference but not in this call's response.

### `snapshot_layout`

**Purpose.** Numerical layout state, positions, sizes, gaps, flex behavior, without rendering pixels.

**Reach for it.** Verification ladder rung 2. The default after any structural `batch_design` call. Cheap and decisive for "did the layout do what I asked?".

**Don't reach for it** to verify property changes that aren't layout-shaped (a color, a label text). `batch_get` is right for those.

**Worked calls.**

```
snapshot_layout({ parentId: "LoginPage", maxDepth: 2 })
snapshot_layout({ parentId: "LoginPage", maxDepth: 3, problemsOnly: true })
```

**Cost levers.**

- `maxDepth`, how deep to walk. `2` is enough for most "did the gap land?" questions. `3-4` for nested layouts.
- `problemsOnly: true`, returns only nodes with computed-layout issues (overflow, undefined sizes). Useful when you're hunting for what broke.

**Pitfalls.** A snapshot doesn't tell you whether two adjacent buttons *visually* read as the same height, fonts and stroke can shift perceived size. For that, climb to `get_screenshot`.

### `get_screenshot`

**Purpose.** Rendered pixel preview of a node and its descendants.

**Reach for it.** Verification ladder rung 4, the most expensive. Use only when the question genuinely needs pixels: contrast under real rendering, image content (AI-generated assets, photos), spacing/type rhythm at scale, or final sign-off before handing back.

**Don't reach for it** to "check progress" between writes. Don't screenshot the document root when a card subtree would do. Don't screenshot both light and dark modes for designs built entirely from variables, the variable system guarantees mode parity.

**Worked call.**

```
get_screenshot({ nodeId: "LoginCard" })
```

**Pitfalls.**

- Always pass the most specific `nodeId` containing the change. Page-frame screenshots are 5× the tokens of card screenshots and reveal nothing extra.
- Screenshots are PNG by default; the model receives them as image input. They count against context, not just billing, keep the cadence to ~one per task.
- For asset handoff (export to a file), use `export_nodes`, not `get_screenshot`.

## Write

### `batch_design`

**Purpose.** Mutate the document, insert, copy, replace, update, delete, move nodes; generate AI/stock images on existing nodes.

See [`batch-design-grammar.md`](batch-design-grammar.md) for the full op grammar (`I`, `C`, `R`, `U`, `G`, `D`, `M`), binding syntax, the ≤25-ops chunking rule, sizing/color rules, and common error fixes.

**Reach for it.** Every time you're changing the document. This is the workhorse.

**Don't reach for it** to declare a token suite at the top of a fresh doc, `set_variables` is purpose-built for that and it's cleaner. Don't reach for it to bulk-rewrite a property value across many nodes, `replace_all_matching_properties` exists for that.

### `set_variables`

**Purpose.** Bulk add or update document-level variables. Replaces or merges with the existing variable set.

**Reach for it.** The right way to bootstrap a token suite at the start of a new document. Also the right way to add a missing token mid-task (e.g. an `$illustration` color you discovered you need).

**Don't reach for it** for purely visual one-shot updates that don't change tokens. `set_variables` is the only documented MCP path for tokens; `U("document", ...)` errors and `U(<frameId>, { variables })` is rejected. If you need to change a single token's value mid-task, call `set_variables` with just that one variable; `replace: false` (the default) merges it into the existing suite.

**Two value shapes.** A **scalar** `value` is for flat (non-themed) tokens, `{ type: "color", value: "#A3B59A" }`, `{ type: "number", value: 16 }`. A **themed** value is an **array** of `{ value, theme }` entries, one per axis value, `{ type: "color", value: [{ value: "#FAFAFA", theme: { mode: "light" } }, { value: "#0B1117", theme: { mode: "dark" } }] }`. The server **auto-registers** any theme axis it sees in your values, no separate `U(<docRoot>, themes: ...)` step is needed.

The themed-value array on a **variable** is a different shape from the `theme: { mode: "..." }` object passed on a **frame** to activate a theme (see SKILL.md § Themes). Variables carry every themed value; frames pick one.

Variable types: `"color"`, `"number"`, `"string"`, `"boolean"`. Variable name must **not** start with `$`, the `$` prefix is the *reference* syntax only (a node property reads `fill: "$primary"`; the variable itself is keyed `primary`).

**Worked call, declaring a full token suite for a new doc.** The values below are illustrative, they show the call shape, not a prescribed palette. Agents pick concrete values from the aesthetic direction (step 2 of the SKILL.md workflow) and the loaded `style` archetype (step 3). Do not copy these hexes verbatim into a real design.

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

- `replace: false` does **not** protect existing variable values. If you pass `surface: { value: "#FAFAFA" }` and the doc already has `surface` set to a user-configured `#E63946`, the `#E63946` is silently overwritten. Call `get_variables()` first and only pass variables that are absent from the response.
- `replace: true` wipes the entire existing variable set and applies only what you pass. Almost never what you want — leave `replace: false` (the merge default) unless you're consciously resetting tokens.
- Theme-aware values require the document to declare matching theme axes first (`U("doc", { themes: { mode: ["light", "dark"] } })`). Set the axes, then call `set_variables`.
- A theme-aware variable's `value` is an array; a flat variable's `value` is a scalar. Mixing the two shapes for the same variable across calls causes silent corruption.
- Bare values are rejected. `{ accent: "#A3B59A" }` (no wrapper) errors with `Variable 'accent' does not have a valid definition`. Always wrap as `{ type: "color", value: "#A3B59A" }`.
- Flattened-key themed values are rejected. `{ accent: { value: { "mode.light": "#FAFAFA", "mode.dark": "#0B1117" } } }` does not work. Use the array form.
- Variable names starting with `$` are tool-rule-forbidden, the contract says `$` is the reference syntax only. The server doesn't currently enforce this on write, but reference resolution against `$`-prefixed names is undefined. Use plain names.
- Multi-axis themes layer independently. A value with `theme: { mode: "light", brand: "acme" }` is selected only when both axes are active.
### `replace_all_matching_properties`

**Purpose.** Bulk swap: every node under given parents whose property `from` matches gets that property updated to `to`.

**Reach for it.** Tokenization passes (rewrite raw `#1F6FEB` to `$primary` everywhere), refactors (rename a font family, update a corner radius globally), drift cleanup. The canonical companion to `search_all_unique_properties`.

**Don't reach for it** for one or two changes, `U` ops are clearer when you can name the targets.

**Worked call.** The `properties` argument is an **object keyed by property name** (not an array of `{property, from, to}` entries):

```
replace_all_matching_properties({
  parents: ["LoginPage"],
  properties: {
    fillColor: [{ from: "#1F6FEB", to: "$primary" }],
    cornerRadius: [{ from: [8], to: [12] }]
  }
})
```

Returns a success message; the per-property change count is not exposed in the response.

**Allowed property keys** (10 total): `cornerRadius`, `fillColor`, `fontFamily`, `fontSize`, `fontWeight`, `gap`, `padding`, `strokeColor`, `strokeThickness`, `textColor`. No others are accepted.

**Per-property value-type quirks:**

- `cornerRadius`: `from` and `to` are **number arrays** (single value `[N]` or four-value `[tl, tr, br, bl]`), not bare numbers. `{ from: [8], to: [12] }`.
- `fillColor`, `textColor`, `strokeColor`, `fontFamily`, `fontWeight`: **strings**. Hex colours, variable references (`"$primary"`), or font names/weights.
- `fontSize`, `gap`, `padding`, `strokeThickness`: bare **numbers**. `{ from: 8, to: 12 }`.

**Pitfalls.**

- Always run `search_all_unique_properties` first to confirm the set you're replacing, otherwise you might rewrite a value that's *legitimately* a one-off elsewhere in the file.
- Numeric `from` values match exactly. `8` matches `8`, not `8.0` or `"8"`.
- `parents` is a list of subtree roots. Pass the document root id (or a top-level frame id) to span the whole doc.
- Wrap each property's entries in an **array** even for a single replacement: `fillColor: [{ from, to }]`, not `fillColor: { from, to }`.

## Audit

### `search_all_unique_properties`

**Purpose.** Audit pass, for given parents, return every distinct value seen for the listed properties.

**Reach for it.** Pre-refactor (before a `replace_all_matching_properties`), drift detection (how many distinct shadow values are in this doc?), a11y audit (every text color present in this view), pre-tokenization (what raw colors are in use?).

**Don't reach for it** when you already know the values you're targeting, go straight to `replace_all_matching_properties`.

**Worked call.**

```
search_all_unique_properties({
  parents: ["<docRootOrTopFrameId>"],
  properties: ["fillColor", "textColor", "fontSize", "cornerRadius", "strokeColor"]
})
```

Returns each property name mapped to a list of unique values.

**Allowed property values** (10 total, the same set as `replace_all_matching_properties`): `cornerRadius`, `fillColor`, `fontFamily`, `fontSize`, `fontWeight`, `gap`, `padding`, `strokeColor`, `strokeThickness`, `textColor`. Anything else (e.g. `shadowBlur`, `letterSpacing`, `opacity`) is rejected.

**Pitfalls.** A value of `"$primary"` and a value of `#1F6FEB` are different unique values, even if they currently resolve to the same colour. That's a feature, it surfaces variable drift you should fix.

### `find_empty_space_on_canvas`

**Purpose.** Locate empty canvas coordinates of a given size, away from existing nodes.

**Reach for it.** Before placing a new top-level frame on a populated canvas. Any time the user has multiple top-level frames already on the canvas and you're about to add another, call this in step 4 (Plan), pass the returned position as `x`/`y` on the outermost frame in your first `batch_design` call.

**Don't reach for it** for nested children, auto-layout positions those automatically.

**Worked call.** All four of `width`, `height`, `padding`, `direction` are required:

```
find_empty_space_on_canvas({
  width: 1440,
  height: 900,
  padding: 80,
  direction: "right"
})
```

Returns `{ x, y }` for an empty region.

`direction` enum: `"top" | "right" | "bottom" | "left"`. Each biases search away from the named edge, `"right"` places to the right of existing content, `"bottom"` places below.

**Optional `nodeId`.** When passed, the search anchors to that node's bounding box instead of the whole canvas. Useful for placing a sibling frame near a known frame (a mobile companion to a desktop, an empty-state variant beside the populated state):

```
find_empty_space_on_canvas({
  width: 390,
  height: 844,
  padding: 80,
  direction: "right",
  nodeId: "<existingFrameId>"
})
```

**Pitfalls.** Omitting any of the four required params errors out. Without `nodeId`, the search anchors to the whole canvas, fine when starting fresh, but on a wide canvas the result can be far from where the user is looking. Pass `nodeId` to anchor near the user's current selection or the most-recently-edited frame.

## Export

### `export_nodes`

**Purpose.** Render nodes to image/PDF files on disk. The handoff path.

**Reach for it.** When the user asks for assets ("export this", "give me a PNG of the hero", "generate the icon set"). When packaging for engineering handoff.

**Don't reach for it** to inspect what something looks like, that's `get_screenshot`. Don't substitute screenshots for exports either; screenshots aren't sized like exports and don't have predictable filenames.

**Worked call.**

```
export_nodes({
  nodeIds: ["HomePage_Desktop", "HomePage_Mobile"],
  format: "png",
  scale: 2,
  outputDir: "./design/exports/"
})
```

**Required params:** `nodeIds`, `outputDir`. **Optional:** `format` (default `png`), `scale` (default `2`), `quality` (default `95` for JPEG, `100` for WEBP; ignored for PNG and PDF).

**Format choices.**

- `png`, UI assets, screenshots-as-deliverables, anything that needs alpha.
- `jpeg`, large hero photos, where alpha doesn't matter and file size does.
- `webp`, modern web; smaller than PNG/JPEG for the same quality.
- `pdf`, print, slide decks, vector handoff. **PDF combines all `nodeIds` into a single multi-page document**, not separate files (one page per node).

**Pitfalls.**

- Always confirm format with the user if not specified. PNG is a safe default for UI; PDF is right for slides/print.
- `outputDir` is relative to the host's working directory. Pass an absolute path when the user names one.
- `scale: 2` is the default for retina-quality assets. Bump to `3` only when explicitly required (App Store screenshots, 3× phone density).
- `quality` only takes effect for JPEG and WEBP. Setting it on PNG or PDF is silently ignored.

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

2. Compare against `tokens.md`, note raw values that should be variables, and divergent values that should collapse.
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
2. `U(document, { themes: { mode: ["light", "dark"] } })` via `batch_design` — declare the theme axis first.
3. `set_variables({ variables: { ... }, replace: false })` — declare the full token suite.
4. First `batch_design` — page frame + skeleton (≤10 ops).
5. `snapshot_layout({ parentId: "<page>", maxDepth: 2 })` — confirm structure.
6. Region-by-region `batch_design` calls — fill in.
7. Final `get_screenshot({ nodeId: "<page>" })` — sign-off.

### Library import smoke test

Reach for this **only when the project already has a `.lib.pen` library**. Most projects don't, a library is something users create when they want shared components across several `.pen` files, and many designs are single-file. If `batch_get({ patterns: [{ reusable: true }] })` on the active doc finds no components, and no `.lib.pen` is referenced in the user's workspace, skip this section: build from primitives or extract a component when one becomes worth reusing.

1. `U(document, { imports: { "ds": "./design/system.lib.pen" } })` via `batch_design`.
2. `batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })` — see what the library exposes.
3. Insert a single `ref` to a known component:

   ```
   test=I(document, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Smoke" } } })
   ```

4. `batch_get({ nodeIds: ["<test-id>"], resolveInstances: true })`, confirm the library component resolved (not an error).
5. `D("<test-id>")` once you've confirmed.

Note step 3 uses `descendants: { label: { content: "..." } }`, the text content property is `content`, not `text`.

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
| `get_screenshot` | PNG image | **Expensive**, image input to the model |

When two tools could answer the same question, pick the cheaper one and only climb if it doesn't resolve. The verification ladder in SKILL.md formalizes this for read-after-write; the same instinct applies for read-before-write planning.

## See also

- [`pen-schema.md`](pen-schema.md), the underlying `.pen` data model, every node type and property.
- [`batch-design-grammar.md`](batch-design-grammar.md), `batch_design` op grammar, binding, chunking, common errors.
- [`pencil-cli.md`](pencil-cli.md), the CLI surface, when CLI is the right tool vs MCP.
- SKILL.md § Verification ladder, when to climb from `snapshot_layout` to `get_screenshot`.
- SKILL.md § Failure modes, the six concrete cases and their responses.
