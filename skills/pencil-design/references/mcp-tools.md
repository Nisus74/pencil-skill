# Pencil MCP tools, cookbook

The full surface of the Pencil MCP server: **nine tools**, what each is for, when to reach for it, when
not, and a worked invocation. Load this when you need a tool you haven't used before, when a tool errors
in a way you don't recognise, or when planning a multi-step task and you want the cheapest path.

Several operations that used to be standalone tools are now **JavaScript functions inside
`batch_design`**: tokens (`SetVariables`), empty-space search (`FindEmptySpace`), and image generation
(`Generate`). Bulk property replacement and unique-value auditing have **no dedicated tool** any more, do
them with `batch_get` plus a JavaScript loop of `Update`. The `batch_design` op grammar lives in
[`batch-design-grammar.md`](batch-design-grammar.md); this file does not restate it.

**`filePath` is a required parameter on every read/write tool** (`batch_get`, `batch_design`,
`snapshot_layout`, `get_screenshot`, `get_variables`, `export_nodes`, `export_html`). Pass an empty
string `""` to target the active editor, or an absolute path (or one relative to the editor's working
directory) to target a specific `.pen`. `get_editor_state` and `get_guidelines` take no `filePath`.

| Phase | Tools |
|-------|-------|
| Connect | `get_editor_state` |
| Reference | `get_guidelines` |
| Read / inspect | `batch_get`, `get_variables`, `snapshot_layout`, `get_screenshot` |
| Write | `batch_design` |
| Export | `export_nodes`, `export_html` |

## Connect

### `get_editor_state`

**Purpose.** Ping the host. Returns the active document's path (if any), the current selection, and
(optionally) the document schema plus the `batch_design` documentation.

**Reach for it.** First action of every task. Without a successful response, every other MCP call fails
with `transport not connected to app: desktop`.

**Worked call.**

```
get_editor_state({ include_schema: true })
```

Pass `include_schema: true` on the **first** call of every conversation. The server requires the schema
be loaded once per session before any read or write, and the payload doubles as the authoritative
`batch_design` reference. Subsequent calls can pass `include_schema: false` to skip the (large) payload.
`pen-schema.md` is a static snapshot for offline reading; it does not substitute for loading the live
schema.

**Pitfalls.** A succeeding call with **no active document** is not a failure, the user just hasn't opened
a `.pen`. There is no `open_document` tool; ask the user to open or create a file in the editor. Branch
into the "no document open" failure path (SKILL.md § Failure modes).

## Reference

### `get_guidelines`

**Purpose.** Load Pencil's built-in design guidelines for a category (task guides) or a visual style
archetype. Server-maintained, loaded fresh per task.

**Reach for it.** Step 3 of the workflow, before planning any design. Different task shapes need
different guides.

**Don't reach for it** for one-off edits to existing nodes ("change this colour", "swap this label").

**Worked calls.** Three steps: discover, load a guide, optionally load a style.

```
get_guidelines()
get_guidelines({ category: "guide", name: "Web App" })
get_guidelines({ category: "style", name: "Soft Bento" })
```

**Guides** (8): `Code`, `Design System`, `Landing Page`, `Mobile App`, `Slides`, `Table`, `Tailwind`,
`Web App`. **Styles** are visual archetypes (the set rotates between releases, e.g. `Soft Bento`,
`Modular Bento Showcase`, `Editorial Scientific`, `Product Demo`, `Spatial Plus`, …). Run
`get_guidelines()` with no args for the current lists. A style archetype called with `{ category, name }`
returns its required `params` signature (colour palette, roundness, elevation, four typography slots);
call again with `params` filled in to load the instantiated style.

**Decision shortcuts (guides):**

| Task | Load `name: ...` |
|------|------------------|
| Dashboard | `Web App`; `Table` if data-heavy; `Tailwind` if the stack matches; `Design System`. |
| Native iOS / Android app | `Mobile App`, `Design System`. |
| Pricing or marketing page | `Landing Page`, `Design System`. |
| Building a `.lib.pen` from scratch | `Design System`, `Code`. |
| Pitch deck | `Slides`. |
| Admin grid / data-heavy table | `Table`, `Web App`. |

**Pitfalls.** Loading three or four guides at once burns context for little gain. Pick one or two. For
styles, load only one, they're aesthetic archetypes and mixing two confuses direction.

**Guidelines carry generic defaults. Filter them against the stated aesthetic direction.** Read the
guidelines for schema rules and accessibility constraints (worth following), but treat their *stylistic*
defaults (chart types, surface colours, shadow use) critically, applied unfiltered they produce AI-slop
output. The most common overrides:

| What the guideline says | When to override | What to use instead |
|-------------------------|------------------|---------------------|
| "Prefer bar charts for data" | Sparklines inside KPI cards | Explicit `width: 3` bars, `gap: 2`, parent `alignItems: "end"`. Never `fill_container` on bar width. See `batch-design-grammar.md`. |
| Blue/purple gradient fills on charts | Data-dense product surfaces | Flat `fill: "$accent"`. No gradients on data bars. |
| Card drop shadows everywhere | Utility/data surfaces | Hairline `stroke: "$border", strokeWidth: 1`, no shadow. |
| Inter as UI font | When direction doesn't call for it | `Geist` for UI, `Geist Mono` for numerals. |
| Dark sidebar + white body default shell | All-light data products | Don't default to a dark sidebar; it's not neutral. |

## Read / inspect

### `batch_get`

**Purpose.** Read nodes by id list, by pattern match, or by depth-first scan. Returns full property JSON.

**Reach for it.** When you need to see the current shape of something before editing it. Common patterns:
inventory components (`patterns: [{ reusable: true }]`), inspect a known node by id, scan a library
(`filePath: "./design/system.lib.pen"`).

**Don't reach for it** to verify a structural change you just made, `snapshot_layout` is cheaper for
layout numbers. Use `batch_get` for property-level confirmation (a variable resolved, a `ref` instantiated
correctly, a text body matches).

**Worked calls.**

```
batch_get({ filePath: "", patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "", nodeIds: ["loginButton", "loginForm"] })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "", nodeIds: ["LoginPage"], readDepth: 4, resolveInstances: true, resolveVariables: true })
```

**Cost levers.** `readDepth` (2 for inventory, 4 for thorough; omit for full depth, expensive);
`resolveInstances` (expands `ref` nodes to their resolved shape, payloads grow fast); `resolveVariables`
(replaces `"$primary"` with its current value, useful for contrast checks); `searchDepth`, `parentId`
(scope to a subtree); `includePathGeometry` (full `path` geometry, off by default).

**Pitfalls.** Calling without `nodeIds` and without `patterns` returns the **top-level children of the
document**, useful for orientation, not deep inspection. The pattern `type` enum has no `icon` value and
its legacy `icon_font` does **not** match v2.14 `icon` nodes; find icons by `name` or read them by id.

### `get_variables`

**Purpose.** Read all document-level design tokens.

**You must call this before any token work on an existing document.** If it returns a non-empty set, the
user's tokens exist and may be customised. Treat them as authoritative; only declare variables that are
absent. This applies before every `SetVariables(...)` call inside `batch_design`.

**Worked call.**

```
get_variables({ filePath: "" })
```

Returns an object keyed by variable name with `{ type, value }` per entry. Themed variables return a
`value` array of `{ value, theme }` entries.

**Pitfalls.** Returns only the *current* document's tokens. Read an imported library's tokens by passing
its path as `filePath`.

### `snapshot_layout`

**Purpose.** Numerical layout state, positions, sizes, gaps, flex behaviour, without rendering pixels.

**Reach for it.** Verification rung 2, the default after any structural `batch_design` call. Cheap and
decisive for "did the layout do what I asked?".

**Don't reach for it** to verify non-layout property changes (a colour, a label); `batch_get` is right
for those.

**Worked calls.**

```
snapshot_layout({ filePath: "", parentId: "LoginPage", maxDepth: 2 })
snapshot_layout({ filePath: "", parentId: "LoginPage", maxDepth: 3, problemsOnly: true })
```

**Cost levers.** `maxDepth` (2 for most checks, 3-4 for nested layouts; `0` for top-level only);
`problemsOnly: true` (only nodes with layout issues, overflow/clipping/undefined sizes).

**Pitfalls.** A snapshot doesn't tell you whether two adjacent buttons *visually* read as the same
height. For that, climb to `get_screenshot`.

### `get_screenshot`

**Purpose.** Rendered pixel preview of a node and its descendants.

**Reach for it.** Verification rung 4, the most expensive. Use only when the question genuinely needs
pixels: contrast under real rendering, image content, spacing/type rhythm at scale, or final sign-off.

**Don't reach for it** to "check progress" between writes. Don't screenshot the document root when a card
subtree would do. Don't screenshot both modes for a design built entirely from variables, the variable
system guarantees mode parity.

**Worked call.**

```
get_screenshot({ filePath: "", nodeId: "LoginCard" })
```

Use `nodeId: "document"` for the whole canvas (rarely needed).

**Pitfalls.** Always pass the most specific `nodeId` containing the change, page-frame screenshots are 5×
the tokens of card screenshots and reveal nothing extra. Screenshots are image input, they count against
context, keep cadence to ~one per task. For asset handoff, use `export_nodes`, not `get_screenshot`.

## Write

### `batch_design`

**Purpose.** Mutate the document. Runs a JavaScript snippet whose functions insert, copy, replace,
update, move, and delete nodes; set variables (`SetVariables`); generate images (`Generate`); and find
empty canvas space (`FindEmptySpace`).

**Reach for it.** Every time you change the document. This is the workhorse, and the only write tool.

See [`batch-design-grammar.md`](batch-design-grammar.md) for the full function set, id handling, chunking,
and common errors.

**Worked call.**

```
batch_design({ filePath: "", input: 'page = Insert(document, { type: "frame", name: "LoginPage", width: 1440, height: 900, clip: true, placeholder: true })\nInsert(page, { type: "text", name: "Title", content: "Sign in", fontSize: 28, fill: "#0F172A" })\nUpdate(page, { placeholder: false })' })
```

**Migrated operations.** Several former standalone tools are now functions here:

- **Tokens** → `SetVariables({ ... }, replace?)`. Read existing tokens with `get_variables` first;
  `replace: false` (the default, merge) still overwrites any key you pass.
- **Empty space** → `FindEmptySpace({ width, height, direction?, padding?, nodeId? })`, returns
  `{ x, y, parentId? }`.
- **Images** → `Generate(nodeId, "ai" | "stock", prompt)` onto an existing `frame`/`rectangle`.
- **Bulk property replace** (the old `replace_all_matching_properties`) → read the targets with
  `batch_get`, then loop `Update`:
  ```
  for (id of ["card1","card2","card3"]) Update(id, { stroke: "$border", strokeWidth: 1 })
  ```
- **Unique-value audit** (the old `search_all_unique_properties`) → `batch_get` the subtree and tally the
  values you care about in your own logic; there is no dedicated audit tool.

## Export

### `export_nodes`

**Purpose.** Render nodes to image/PDF files on disk. The asset-handoff path.

**Reach for it.** When the user asks for assets ("export this", "give me a PNG of the hero", "generate the
icon set"), or when packaging for engineering handoff.

**Don't reach for it** to inspect what something looks like, that's `get_screenshot`.

**Worked call.**

```
export_nodes({ filePath: "", nodeIds: ["HomePage_Desktop", "HomePage_Mobile"], format: "png", scale: 2, outputDir: "./design/exports/" })
```

**Required:** `filePath`, `nodeIds`, `outputDir`. **Optional:** `format` (`png` default, `jpeg`, `webp`,
`pdf`), `scale` (default `2`; 8192 max resolution), `quality` (default `95` JPEG / `100` WEBP; ignored for
PNG and PDF). Each node is a separate file named by node id, **except PDF**, which combines all `nodeIds`
into one multi-page document.

**Pitfalls.** Confirm format with the user if unstated, PNG is a safe UI default; PDF is right for
slides/print. `outputDir` is relative to the host's working directory; pass an absolute path when the
user names one.

### `export_html`

**Purpose.** Export nodes to HTML, either HTML + Tailwind or HTML + CSS. The code-handoff path.

**Reach for it.** When the user wants markup, not images: "export this to HTML", "give me the Tailwind for
this section", "hand this to engineering as code".

**Don't reach for it** for visual review (`get_screenshot`) or image assets (`export_nodes`).

**Worked call.**

```
export_html({ filePath: "", nodeIds: ["HeroSection"], outputPath: "./design/exports/hero.html", format: "html-tailwind" })
```

**Required:** `filePath`, `nodeIds`, `outputPath`. **Optional:** `format` (`html-tailwind` default, or
`html-css`), `includeHtmlScaffold` (default `true`), `includeLayerNames` (default `true`),
`includeLayerIds` (default `false`). Image assets are always referenced by relative path, never embedded.
Writes one HTML file to `outputPath` and returns its absolute path.

**Pitfalls.** Pair `includeLayerIds: true` with `includeLayerNames: true` when the team wants to map
generated markup back to canvas nodes. The output is a faithful structural export, not a hand-tuned
component, treat it as a starting point for engineering.

## Composite recipes

### Token audit & cleanup

There is no `search`/`replace` property tool any more; do the audit in your own logic.

1. Read the subtree and inventory raw values you find:
   ```
   batch_get({ filePath: "", nodeIds: ["<topFrameId>"], readDepth: 6, resolveVariables: false })
   ```
2. Compare against `get_variables()`. Note raw hexes that should be tokens and divergent values that
   should collapse.
3. Retoken with a `batch_design` loop of `Update`:
   ```
   for (id of ["heroTitle","ctaButton","badge"]) Update(id, { fill: "$primary" })
   ```
4. Re-read to confirm the rewrite landed.

### Greenfield document bootstrap

1. Confirm an empty doc is open (`get_editor_state`; there's no `open_document` tool, the user opens it).
2. `get_variables({ filePath: "" })` — see what (if anything) already exists.
3. One `batch_design` call: `SetVariables({ ... })` to declare the token suite (themed values
   auto-register the `mode` axis), then `Insert` the page skeleton (≤8 ops).
4. `snapshot_layout({ filePath: "", parentId: "<page>", maxDepth: 2 })` — confirm structure.
5. Region-by-region `batch_design` calls — fill in.
6. Final `get_screenshot({ filePath: "", nodeId: "<page>" })` — sign-off.

### Library import smoke test

Reach for this **only when the project already has a `.lib.pen` library** (most don't).

1. Inventory the library: `batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })`.
2. Instance one known component into the active doc:
   ```
   batch_design({ filePath: "", input: 'test = Insert(document, { type: "ref", ref: "ButtonPrimary", descendants: { Label: { content: "Smoke" } } })' })
   ```
3. `batch_get({ filePath: "", nodeIds: ["<test id>"], resolveInstances: true })` — confirm it resolved.
4. `batch_design({ filePath: "", input: 'Delete("<test id>")' })` once confirmed.

## Tool cost cheatsheet

Roughly cheapest → most expensive in tokens / context:

| Tool | Payload shape | Cost |
|------|---------------|------|
| `get_variables` | Variables block | Small |
| `snapshot_layout` | Nested numbers | Small-medium |
| `batch_design` | Op success + new ids (image `Generate` is slower) | Small for short calls; medium for long |
| `batch_get` | Full node JSON | Medium → large with depth and `resolveInstances` |
| `get_editor_state` | Document/selection metadata | Small (large with `include_schema: true`) |
| `get_guidelines` | Markdown text | Medium per category |
| `export_nodes` / `export_html` | File paths written | Small (files land on disk) |
| `get_screenshot` | PNG image | **Expensive**, image input to the model |

When two tools could answer the same question, pick the cheaper one and only climb if it doesn't resolve.

## See also

- [`batch-design-grammar.md`](batch-design-grammar.md), the `batch_design` JavaScript API.
- [`pen-schema.md`](pen-schema.md), the `.pen` data model (v2.14), every node type and property.
- [`advanced-canvas.md`](advanced-canvas.md), shader fills, mesh gradients, `script` nodes, arcs/donuts.
- [`pencil-cli.md`](pencil-cli.md), the CLI surface and the When-CLI-vs-MCP decision table.
- SKILL.md § Verification ladder and § Failure modes.
