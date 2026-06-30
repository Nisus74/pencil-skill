# `batch_design` API

`batch_design` takes a single `input` string that is a **JavaScript snippet**. The server runs it
top to bottom in one scope, then returns a `name → id` map for every node you created so you can
reference those ids in later calls.

It is not a line-based op grammar. You write real JavaScript: arrays, `for...of` loops, computed
values, conditionals, object spreads, helper functions, and template strings all work, and you are
expected to use them to remove repetition (nav items, table rows, cards, metrics, menus).

> If you ever need the authoritative API mid-task, call `get_editor_state({ include_schema: true })`.
> Its payload carries the live schema and the `batch_design` documentation. This file mirrors it.

## The functions

These are the **only** functions available inside a `batch_design` snippet. Everything else (reading
nodes, screenshots, exports) is a separate MCP tool.

```
const document: string;                                  // predefined root-node id

Insert(parent, nodeData)            → string             // create a child, returns new id
Copy(path, parent, copyNodeData)    → string             // duplicate a node into a parent, returns new id
Update(path, updateData)            → void               // merge properties onto an existing node
Replace(path, nodeData)             → string             // swap a node for a new one, returns new id
Move(path, parent?, index?)         → void               // reparent / reorder
Delete(path)                        → void               // remove a node and its descendants
SetVariables(variables, replace?)   → void               // define / update document variables + themes
Generate(nodeId, "ai" | "stock", prompt) → void          // fill a node with an AI or stock image
FindEmptySpace({ width, height, direction?, padding?, nodeId? }) → { x, y, parentId? }
```

`path` (for `Copy`/`Update`/`Replace`/`Move`/`Delete`) is a node id, or a slash-separated path to a
node nested inside a component instance (`instanceId/childId`). Slashes are **only** valid for
component-instance nesting, never for normal layer structure, and they work to any depth.

### Rules that bite if you forget them

- **Never set `id`.** Pencil always generates a random id and overrides anything you pass. To reference
  a node later, capture the return value.
- **Capture ids with bare assignment, no `const`/`let`.** `card = Insert(...)` registers `card` in the
  returned `name → id` map; `const card = Insert(...)` may not surface in that map. Within a call you
  can reference the variable directly.
- **Bindings do not survive into the next call.** Each `batch_design` runs in a fresh scope: a variable
  from a previous call is `not defined` and using it throws. To reference a node in a later call, pass
  its **literal id** from the returned `name → id` map (or from `get_editor_state` / `batch_get`).
  Verified live: re-using a prior call's binding name raises `ReferenceError`.
- **On error the whole call rolls back.** Every insert and every binding from the call is reverted.
  Fix and re-run.
- **Warnings come back in the response.** Always fix them in the next call.
- **No comments in the snippet.** Keep `input` small. Comments are noise the server parses for nothing.
- **One screen at a time.** Don't leave several top-level frames half-built. Finish (or `placeholder`)
  one before starting the next, unless you are deliberately fanning out with sub-agents.

## `Insert`

Create a child at the end of a parent's `children`.

```
form = Insert(page, { type: "frame", name: "LoginForm", layout: "vertical", gap: "$space-4", padding: "$space-6" })
title = Insert(form, { type: "text", name: "Title", content: "Sign in", fontSize: "$text2xl", fill: "$textPrimary" })
```

- `parent` is an existing id (from `get_editor_state` / `batch_get`, or bound earlier in this call).
  Use the predefined `document` binding for top-level frames.
- The object is the node's properties, minus `id`.
- `layout` accepts only `"none"`, `"vertical"`, `"horizontal"`. Frames default to `"horizontal"`,
  groups to `"none"`. CSS words (`"flex"`, `"row"`, `"column"`, `"grid"`) are rejected and roll back.
- One `Insert` makes one node. To give it children, capture its id and `Insert` into that.

### The `document` predefined binding

`document` always resolves to the document root. Use it **only** for top-level frames (screens,
canvas-level containers). Never name your own binding `document`; it shadows the predefined one and
breaks every later root insert.

```
page = Insert(document, { type: "frame", name: "LoginPage", width: 1440, height: 900, clip: true, placeholder: true })
```

Keep the root clean: only page/screen frames, reusable component frames, and major container frames
belong directly under `document`. Never place text, icons, buttons, cards, rows, or shapes there.

## `Copy`

Duplicate a node into a parent, with optional overrides. `Copy` is for duplicating screens and
non-reusable nodes; to place a component, prefer an `Insert` `ref` (see Components below).

```
dashV2 = Copy("Dashboard", document, { name: "Dashboard V2", x: pos.x, y: pos.y, descendants: { "Header/Title": { content: "Reports" } } })
```

- First arg: source id (any node on the canvas, reusable or not).
- Second arg: target parent id.
- Third arg: overrides for the copy. Customise nested nodes with the `descendants` map **in the same
  `Copy` call**.
- **Copying a non-reusable node gives its descendants fresh ids**, so a *separate* `Update` against an
  old descendant id fails. Put all descendant customisation in the `Copy`'s `descendants` map.
- **Copying a `reusable` node creates a connected instance (a `ref`).** Its descendants keep the
  **origin child ids**, so two gotchas apply (both verified live): `descendants` keyed by child **name**
  is *ignored* on `Copy` (works on `Insert` `ref`, not here); key by the origin child id instead. A
  post-copy `Update(copyId + "/originChildId", {...})` does work, because the instance keeps origin ids.

## `Update`

Merge properties onto an existing node. Only the named properties change.

```
Update("heroTitle", { fontSize: "$text3xl" })
Update(card + "/Title", { content: "Account Details" })
```

- Cannot change `id`, `type`, or `ref`.
- Do **not** use it to set `children`; use `Replace` for that.
- Instance descendants are reachable by slash-path (`instanceId/childId`), to any nesting depth.

**Bulk property change is a JavaScript loop of `Update`.** There is no `replace_all_matching_properties`
tool any more. To retoken a set of nodes, read them with `batch_get`, then loop:

```
for (id of ["card1", "card2", "card3"]) Update(id, { stroke: "$border", strokeWidth: 1 })
```

## `Replace`

Swap a node for a new one. Every property, including `x`/`y`, is replaced. Ideal for swapping a slot
or a descendant subtree inside an instance.

```
content = Replace(card + "/ContentSlot", { type: "frame", name: "Content", layout: "vertical", gap: 8 })
```

Returns the new node's id. Use `Update` instead when you only want to tweak a few properties.

## `Move`

```
Move("loginButton", form, 2)
```

Reparent `loginButton` under `form` at index `2`. Omit `parent` to reorder within the current parent;
omit `index` to append. Properties are preserved.

## `Delete`

```
Delete("legacyBanner")
```

Removes the node and its descendants. When deleting and re-creating, delete first.

## `SetVariables` (tokens + themes)

Define or update document variables. Read existing variables with `get_variables` first so you don't
clobber user-configured tokens.

```
SetVariables({
  surface:     { type: "color", value: [
    { value: "#FAFAFA", theme: { mode: "light" } },
    { value: "#0B1117", theme: { mode: "dark" } }
  ] },
  textPrimary: { type: "color", value: [
    { value: "#0B1117", theme: { mode: "light" } },
    { value: "#FAFAFA", theme: { mode: "dark" } }
  ] },
  primary:     { type: "color",  value: "#1F6FEB" },
  "space-4":   { type: "number", value: 16 },
  "font-body": { type: "string", value: "Geist" }
})
```

- Each value MUST be an object with a `type` (`"color"`, `"number"`, `"string"`, or `"boolean"`) and a
  `value`. A bare `"#A3B59A"` or `16` is rejected.
- Variable names are arbitrary strings and MUST NOT begin with `$`. The `$` prefix is the **reference**
  syntax only: a property reads `fill: "$surface"`; the variable itself is keyed `surface`.
- **Themes auto-register.** Pass an array of `{ value, theme }` entries and any theme axis/value not yet
  in the document is created on the fly. There is no separate theme-declaration step.
- `replace` defaults to `false` (merge). `replace: false` still **overwrites** any key you pass, so only
  pass variables that are absent from `get_variables`. `replace: true` wipes the entire variable set,
  almost never what you want.

## `Generate` (images)

There is **no `image` node type**. Images are applied as a `fill` to an existing `frame` or
`rectangle`. Create the node, then fill it:

```
hero = Insert(page, { type: "rectangle", name: "HeroBackground", width: "fill_container", height: 480 })
Generate(hero, "ai", "soft morning light through a kitchen window, photorealistic, shallow depth of field")

avatar = Insert(row, { type: "rectangle", name: "Avatar", width: 40, height: 40, cornerRadius: 20 })
Generate(avatar, "stock", "smiling barista")
```

- `"ai"`: a detailed descriptive prompt for the AI pipeline.
- `"stock"`: 1-3 concrete keywords (no use-case or abstract terms) for an Unsplash search.
- The target node id must not contain `/`. Never guess image URLs; always go through `Generate`.

## `FindEmptySpace` (placement)

When you insert a frame directly into `document` and don't know the exact coordinates, call
`FindEmptySpace` first so root frames never overlap.

```
pos = FindEmptySpace({ width: 1440, height: 900, direction: "right", padding: 80 })
page = Insert(document, { type: "frame", name: "Dashboard", x: pos.x, y: pos.y, width: 1440, height: 900, clip: true, placeholder: true })
```

- `direction` (default `"right"`): `"top" | "right" | "bottom" | "left"`. Bias away from that edge.
- `padding` (default `0`): minimum gap from existing content.
- `nodeId` (optional): anchor the search to a node's bounding box instead of the whole canvas. For
  sequential screens, pass the **previous** screen's id so the new one chains beside it.
- Returns `{ x, y, parentId? }`. Insert into `parentId` (or `document` if absent) at the returned `x`/`y`.
- Place components at the top of the canvas and screens below, growing right and down.

## Components and instances

- A node with `reusable: true` is a component. Its id is always server-generated and cannot be set.
- **Split component creation into its own `batch_design` call** so you get the generated id back before
  you instance it.
- Instance a component with a `ref`: `Insert(parent, { type: "ref", ref: componentId, name: "..." })`.
- Override the instance root by putting properties on the `ref` object. Override nested nodes with the
  `descendants` map, keyed by the descendant's id, unique name, or slash-path. A descendant entry that
  includes `type` **replaces** that subtree; without `type` it **merges** properties.
- An instance can hide a nested node by overriding its `enabled: false`.
- Position an instance that is not inside a layout by overriding **both** `x` and `y` (even at `0,0`).

```
card = Insert("Casf3fX", { type: "ref", ref: "AccountCard", name: "Account Card" })
Update(card + "/Title", { content: "Account Details" })
custom = Replace(card + "/ContentSlot", { type: "frame", name: "Content", layout: "vertical", gap: 8 })
Insert(custom, { type: "text", name: "Item 1", content: "Item 1", fontFamily: "$font-body", fill: "$textPrimary" })
```

## Placeholder discipline

Every new, copied, or modified **top-level** frame carries `placeholder: true` for the whole time you
are building it.

- Set it in the same `Insert`/`Copy` that creates the frame.
- You may update layout/size on the placeholder while filling it.
- Remove it per-frame (`Update(id, { placeholder: false })`) the moment that frame is done, not at the
  end of the whole task.
- Do not set `placeholder` on inner content frames, only on top-level page frames.

```
page = Insert(document, { type: "frame", name: "LoginPage", width: 1440, height: 900, clip: true, placeholder: true })
card = Insert(page, { type: "frame", name: "LoginCard", width: 440, layout: "vertical" })
Update(page, { placeholder: false })
```

## Stroke, fill, and effects: the current shapes

The schema changed how borders are expressed. Get these wrong and the call rolls back.

- **Stroke is a fill plus a width, on two separate properties.** `stroke` is a `Fills` value (a bare
  colour string, a `$variable`, or a fill object/array). `strokeWidth` is the thickness (a number, or a
  per-side object). The old `stroke: { color, thickness }` form is **rejected**.

  ```
  Insert(row, { type: "frame", name: "Card", fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8 })
  Insert(row, { type: "frame", name: "TopRule", stroke: "$border", strokeWidth: { top: 2, right: 0, bottom: 0, left: 0 } })
  ```

  Optional: `strokeLinecap` (`butt`/`round`/`square`), `strokeLinejoin` (`miter`/`bevel`/`round`),
  `strokeAlignment` (`inner`/`center`/`outer`).

- **`fill` accepts a bare colour, a fill object, or an array** painted bottom-to-top. Fill object types:
  `color`, `gradient`, `image`, `shader`, `mesh_gradient` (see
  [`advanced-canvas.md`](advanced-canvas.md) for shader and mesh-gradient recipes). There is no
  `solid_color` type; use a bare string or `{ type: "color", color: ... }`.

- **Effects** are `blur`, `background_blur`, and `shadow`. The shadow type string is `"shadow"`, not
  `"drop_shadow"`:

  ```
  Update("Card", { effect: [{ type: "shadow", shadowType: "outer", offset: { x: 0, y: 4 }, blur: 12, spread: 0, color: "#0000001A" }] })
  ```

  For data-dense product surfaces, prefer a hairline `stroke` over a shadow. Remove a shadow with
  `Update(id, { effect: [] })`.

## Icons

Icons are `type: "icon"` (not `icon_font`), with `library` and `icon` properties.

```
Insert(button, { type: "icon", name: "ArrowIcon", library: "lucide", icon: "arrow-right", width: 16, height: 16, fill: "$textPrimary" })
```

- `library`: `"lucide"`, `"feather"`, `"Material Symbols Outlined"`, `"Material Symbols Rounded"`,
  `"Material Symbols Sharp"`, or `"phosphor"`.
- `icon`: the icon name within that library. `weight` (100-700) only for variable-weight libraries.
- The icon scales to fit `width`/`height`. It needs a `fill` to be visible.
- **Reading icons back:** `batch_get`'s pattern enum has no `icon` type, and `type: "icon_font"` does
  **not** match `icon` nodes. Find icons by `name` pattern, by `parentId`, or read them by id.

## Sizing and layout constraints

- **`fill_container` requires a flex parent.** A child set to `width: "fill_container"` does nothing if
  its parent has `layout: "none"`. The parent needs `layout: "vertical"` or `"horizontal"`.
- **`fit_content` requires a flex node.** Only meaningful on nodes with flex layout.
- **Circular dependency.** A `fit_content` parent whose direct children are *all* `fill_container`
  cannot resolve. Give at least one child a fixed or `fit_content` size. Don't rely on the `()` fallback.
- **`x`/`y` are ignored in flex children.** Only set them when the parent is `layout: "none"` or the
  child is `layoutPosition: "absolute"`. When you set position, set both axes.
- **Text is invisible without `fill`.** Text nodes have no default colour. Always set `fill`.
- **Text wrapping needs `textGrowth`.** `auto` (default) never wraps and ignores any width/height you
  set. To wrap, use `fixed-width` (set `width`, height grows) or `fixed-width-height` (set both). For
  headings/paragraphs that should match their parent: `textGrowth: "fixed-width", width: "fill_container"`.
- **No `alignItems` stretch/baseline, no `margin`, no percentage sizes.** `alignItems` is
  `start`/`center`/`end`; `justifyContent` is `start`/`center`/`end`/`space_between`/`space_around`.
  (`flex_end`/`flex_start` are tolerated and normalised to `end`/`start`, but write the canonical form.)
- **Padding** is `n`, `[vertical, horizontal]`, or `[top, right, bottom, left]`. There are no
  `paddingTop`-style properties.

## Chunking

This is a skill convention, not a server limit, but it keeps the canvas legible while you work:

- **≤8 ops per call for visual work**, so each call advances the canvas by an amount the user can take
  in with one screenshot.
- Non-visual sweeps (renames, `context` backfills, metadata) can be larger, but stay focused per call.

For a big screen, plan the order:

1. **Skeleton call:** page frame + main columns + sidebar + footer.
2. **Verify structure** with `snapshot_layout({ parentId: "<page>", maxDepth: 2 })`, the geometry numbers
   tell you whether the skeleton landed without paying for a screenshot.
3. **Region calls:** one per substantial region (hero, form, list).
4. **Polish call:** final tweaks once the structure is solid.

## Smoke test: the minimum first call

After a Pencil version update, or when a call rolls back with a confusing message, run this two-op probe
to confirm the basics before the real skeleton:

```
page = Insert(document, { type: "frame", name: "SmokeTest", layout: "vertical", padding: 16, gap: 8, width: 1440, height: 900, placeholder: true })
hello = Insert(page, { type: "text", name: "Hello", content: "Hello", fontSize: 24, fill: "#0F172A" })
```

It confirms the `document` binding works as an insert parent, `layout: "vertical"` is accepted (catches
`"flex"`/`"row"` typos), scalar `padding` is accepted, `text` uses `content`, `placeholder: true` is
accepted, and a raw-hex text `fill` renders. Delete with `Delete("<pageId>")` once verified.

## Common errors and their fixes

| Server error | Cause | Fix |
|--------------|-------|-----|
| `invalid id: contains '/'` | You set `id: "section/title"` | Pick an id with no slash. `/` is only meaningful in `descendants`/instance paths. |
| `parent not found: <name>` | Referenced a binding before declaring it, or one never created | Reorder so the binding is assigned first. Check the name matches exactly. |
| `/stroke/type expected one of: "color", "gradient", "image", "shader", "mesh_gradient"` | Used the old `stroke: { color, thickness }` form | `stroke: "$border", strokeWidth: 1`. Thickness is the separate `strokeWidth`. |
| `width expected ... number, "$variable", sizing behavior` | Used `width: "100%"` or an object form | Use `width: "fill_container"` / `"fit_content"`, with fallback `"fill_container(320)"`. |
| `unknown type: button` | Used a UI-framework word as a node type | No `button` type. A button is a `frame` (optionally `reusable`) or a `ref` to one. |
| `unexpected property: paddingTop` | Used CSS individual-padding shorthands | Use `padding: [t, r, b, l]` or `[v, h]`. For top-only: `padding: [8, 0, 0, 0]`. |
| `slot frame must be empty in origin` | Put children inside a slot frame in the component origin | Slots are filled at the instance level. Keep the origin slot empty. |

## Commonly built patterns: exact anatomy

These override the generic "bar chart" mental model the Web App guidelines tend to install.

### KPI sparkline (mini trend inside a metric card)

A sparkline is **not** a bar chart. Its bars are 3-4 px wide, never `fill_container` (which would make
each bar fill the parent and read as a loading skeleton). Bars grow upward from the baseline.

```
sparkline = Insert(kpiCard, {
  type: "frame", name: "Sparkline",
  context: "Mini trend, last 12 days. Each bar height encodes relative volume.",
  layout: "horizontal", alignItems: "end", gap: 2, width: 60, height: 32
})
heights = [8, 12, 10, 20, 16, 24, 18, 28, 22, 32]
for (h of heights) Insert(sparkline, { type: "frame", name: "Bar", width: 3, height: h, fill: "$accent", cornerRadius: 1 })
```

- Parent: `layout: "horizontal"`, `alignItems: "end"`, `gap: 2`, explicit px `width`/`height`.
- Each bar: explicit `width: 3` (never `fill_container`), px height for relative magnitude,
  `fill: "$accent"` (no gradients unless the direction calls for them), `cornerRadius: 1`.
- Vary the heights. Equal heights read as a loading bar.

### KPI metric card

```
kpiCard = Insert(statsRow, {
  type: "frame", name: "KPICard_TotalCalls",
  context: "Total API calls over selected period. From /v1/stats/summary. Click navigates to Requests.",
  layout: "vertical", gap: 8, padding: [16, 16, 12, 16],
  width: "fill_container", height: "fit_content",
  fill: "$surface", stroke: "$border", strokeWidth: 1, cornerRadius: 8
})
Insert(kpiCard, { type: "text", name: "MetricLabel", content: "Total API calls", fontSize: "$textSm", fill: "$textMuted" })
valueRow = Insert(kpiCard, { type: "frame", name: "ValueRow", layout: "horizontal", alignItems: "center", justifyContent: "space_between", width: "fill_container" })
Insert(valueRow, { type: "text", name: "MetricValue", content: "24.7M", fontSize: "$text2xl", fontWeight: "600", fill: "$textPrimary", fontFamily: "Geist Mono" })
Insert(valueRow, { type: "text", name: "DeltaBadge", content: "+18%", fontSize: "$textXs", fill: "$success" })
```

For data-dense surfaces: no shadow. The hairline `stroke: "$border", strokeWidth: 1` is the elevation
signal; a shadow claims hierarchy a data card doesn't need.

## A complete small example

A login form, one call:

```
page = Insert(document, { type: "frame", name: "LoginPage", layout: "vertical", justifyContent: "center", alignItems: "center", padding: "$space-8", width: 1440, height: 900, clip: true, placeholder: true })
form = Insert(page, { type: "frame", name: "Form", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: "$surface", stroke: "$border", strokeWidth: 1 })
Insert(form, { type: "text", name: "Title", content: "Sign in", fontSize: "$text2xl", fontWeight: "700", fill: "$textPrimary" })
Insert(form, { type: "text", name: "Subtitle", content: "Welcome back", fontSize: "$textBase", fill: "$textMuted" })
Insert(form, { type: "ref", ref: "Input", name: "EmailField", descendants: { Label: { content: "Email" }, Input: { content: "you@example.com" } } })
Insert(form, { type: "ref", ref: "Input", name: "PasswordField", descendants: { Label: { content: "Password" } } })
Insert(form, { type: "ref", ref: "ButtonPrimary", name: "SubmitButton", descendants: { Label: { content: "Sign in" } } })
Insert(form, { type: "text", name: "ForgotLink", content: "Forgot password?", fontSize: "$textSm", href: "#", textGrowth: "fixed-width", width: "fill_container", textAlign: "center", fill: "$textMuted" })
Update(page, { placeholder: false })
```

After the call, verify structurally with `snapshot_layout({ parentId: "<form id>", maxDepth: 2 })`.
Screenshot once as the final sign-off. Iterate with `Update` ops on the offending nodes.

## See also

- [`pen-schema.md`](pen-schema.md), every node type and property in the live `.pen` schema (v2.14).
- [`advanced-canvas.md`](advanced-canvas.md), shader fills, mesh gradients, `script` nodes, ellipse
  arcs/donuts, `prompt`/`context` nodes.
- [`mcp-tools.md`](mcp-tools.md), the nine MCP tools and when to reach for each.
