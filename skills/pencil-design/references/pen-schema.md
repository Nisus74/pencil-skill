# `.pen` schema reference

Cheat-sheet for the `.pen` JSON format (schema **2.14**). The authoritative copy is the payload of
`get_editor_state({ include_schema: true })`; call that once per session and trust it over this file if
they ever disagree. Public docs: <https://docs.pencil.dev/for-developers/the-pen-format>.

All reads and writes go through the Pencil MCP tools, never a file editor. Tokens, nodes, and structure
are mutated inside a `batch_design` JavaScript snippet (see
[`batch-design-grammar.md`](batch-design-grammar.md)); this file describes the data those calls produce.

## Document

```jsonc
{
  "version": "2.14",
  "themes": { /* optional, axis -> values */ },
  "imports": { /* optional, alias -> relative .pen path */ },
  "variables": { /* optional, design tokens */ },
  "children": [ /* required, array of nodes */ ]
}
```

- **Tokens** (`variables`) and **themes**: set via `SetVariables(...)` inside `batch_design`. Themed
  values like `{ value: "#FAFAFA", theme: { mode: "light" } }` auto-register the matching theme axis, so
  there is no separate axis-declaration step.
- **Imports**: visible in `get_editor_state`. There is no `batch_design` function for them; attach a
  library through the editor's import UI. Read an imported file's contents by passing its path as
  `filePath` to `batch_get` / `get_variables`.
- `document` is the predefined root-node id, usable only as a parent for top-level `Insert`s. There is no
  `Update(document, ...)`.

## Entity (every node extends this)

| Field | Required | Notes |
|-------|----------|-------|
| `id` | auto | Unique string, **MUST NOT contain `/`**. Never set it yourself; the server assigns one. `/` is only meaningful inside `descendants` keys and instance slash-paths (`instanceId/childId`). |
| `type` | yes | One of the node types below. |
| `name` | no | Display name in the layers panel. Always set a meaningful one. |
| `context` | no | Free-form context string for agent / collaborator notes. |
| `reusable` | no | `true` makes this node a component (instantiable via `ref`). |
| `theme` | no | Theme-axis activation on this node: `{ axisName: "value" }`. |
| `enabled` | no | Boolean or variable. Hides the node when false. |
| `opacity` | no | 0-1. |
| `flipX`, `flipY` | no | Boolean. |
| `layoutPosition` | no | `"auto"` (default, joins parent flex) or `"absolute"` (positioned by `x`/`y` inside a flex parent, out of flow). |
| `metadata` | no | Object with a required `type: string` field plus any extra keys. |
| `rotation` | no | Degrees counter-clockwise around the node's top-left corner. |

Position uses `x`, `y` for the top-left corner, relative to the parent. **`x`/`y` are ignored when the
parent uses `layout: "vertical"` or `"horizontal"`** — use flex properties there.

## Node types

`Child` union (the creatable types): `frame`, `group`, `rectangle`, `ellipse`, `polygon`, `path`,
`text`, `note`, `prompt`, `context`, `icon`, `script`, `ref`.

### Shape & container

| Type | Notes |
|------|-------|
| `rectangle` | Position + size + graphics. Most common primitive. `cornerRadius` single number or `[tl, tr, br, bl]`. |
| `ellipse` | `innerRadius` (0=solid, 1=hollow; donut at e.g. `0.6`), `startAngle` (degrees CCW from right, default 0), `sweepAngle` (positive=CCW, negative=CW, range -360..360, default 360). 90° clockwise arc from 12 o'clock: `startAngle: 90, sweepAngle: -90`. |
| `polygon` | `polygonCount` (number of sides), `cornerRadius`. |
| `path` | SVG path. `geometry` (the `d` string), `viewBox: [x, y, w, h]` (set it explicitly), `fillRule: "nonzero" \| "evenodd"`. |
| `frame` | Rectangle that holds children. The auto-layout container. Also `clip`, `placeholder`, `slot`. |
| `group` | Container with children + effects but **no own layout/size**; sizes to its children. Use a `frame` when you need layout, padding, or a background fill. |

> There is **no `line` node** and **no `image` node** in the creatable set. Draw a hairline as a thin
> `rectangle` or a `path`; show an image as an image `fill` on a `frame`/`rectangle` (see Graphics).
> `batch_get`'s search-pattern enum still lists legacy `line`, `connection`, and `icon_font` strings, but
> those are search-only and do not match v2.14 nodes by type.

### Content

| Type | Notes |
|------|-------|
| `text` | Content field is **`content`** (not `text`/`value`). No colour by default, always set `fill`. `textGrowth` controls wrapping (below). |
| `icon` | Icon from a library. `library` + `icon` + optional `weight`. Sized by `width`/`height`, needs `fill`. (See Icon nodes.) |
| `note` | Annotation. `content` + TextStyle only (Entity + Size + TextStyle), **no `fill`/`stroke`/`effect`**. Travels with the file for humans/agents; truly never renders in a screenshot. |
| `prompt` | AI prompt. `content`, optional `model` (target LLM), + TextStyle (no graphics props). Shows on canvas as a collapsible "Prompt ⌄" chip (so it *does* appear in screenshots), but carries no visual styling. |
| `context` | Region-level context note. `content` + TextStyle (no graphics props). Shows as a "Context ⌄" chip. A standalone analogue of the Entity `context` field. |

### Component & code

| Type | Notes |
|------|-------|
| `ref` | Instance of a `reusable: true` node. Has `ref: "<componentId>"` and optional `descendants` overrides (keyed by child id, unique name, or slash-path). A descendant entry with `type` replaces that subtree; without `type` it merges properties. |
| `script` | Code on canvas: points at a `.js` file whose returned nodes render as children. See Script nodes and [`advanced-canvas.md`](advanced-canvas.md). |

## Sizing

`width` / `height` accept:

```jsonc
240                       // explicit number
"$buttonWidth"            // variable reference
"fill_container"          // grow to fill parent's auto-layout axis
"fit_content"             // shrink to children
"fill_container(320)"     // fill with fallback
"fit_content(100)"        // fit with fallback
```

- `fill_container` requires the parent to have `layout: "vertical"` or `"horizontal"`.
- `fit_content` is only meaningful on a node that itself uses flex layout.
- A `fit_content` parent whose direct children are *all* `fill_container` is a circular dependency; give
  at least one child a fixed or `fit_content` size.
- `"100%"` and the old `{ sizing: "fill_container" }` object form are rejected.

## Layout (flexbox-style, on `frame`)

```jsonc
{
  "layout": "vertical",          // "none" | "vertical" | "horizontal"
  "gap": "$space-4",
  "padding": [16, 24],           // number | [vertical, horizontal] | [top, right, bottom, left]
  "justifyContent": "start",     // start | center | end | space_between | space_around
  "alignItems": "center"         // start | center | end   ← NO stretch / baseline
}
```

- `layout` is exactly `"none"` / `"vertical"` / `"horizontal"`. Frames default to `"horizontal"`, groups
  have no layout. CSS words (`"flex"`, `"row"`, `"column"`, `"grid"`) hard-error.
- `layout: "none"` positions children by their `x`/`y`. With flex layout, child `x`/`y` are ignored.
- `padding` rejects `{ top, left, ... }` and `paddingTop`-style keys. Use a number, `[v, h]`, or `[t, r, b, l]`.
- `justifyContent`/`alignItems` use the canonical values above. `flex_start`/`flex_end` are tolerated and
  normalised to `start`/`end`, but write the canonical form. **`stretch` is rejected** — to make children
  span the cross axis, set `fill_container` on the relevant axis of each child.

## Graphics

- **`fill`:** a bare `ColorOrVariable` string (`"$primary"`, `"#1F6FEB"`), a single fill object, or an
  array of fill objects painted bottom-to-top. Object types: `color`, `gradient`
  (`gradientType: "linear" | "radial" | "angular"`, `colors: [{ color, position }]`, `rotation`,
  `center`, `size`), `image` (`url`, `mode: "stretch" | "fill" | "fit"`), `shader`, `mesh_gradient`.
  There is no `solid_color` type. Shader and mesh-gradient recipes live in
  [`advanced-canvas.md`](advanced-canvas.md).
- **`stroke` + `strokeWidth` (two separate properties).** `stroke` is a `Fills` value (bare colour,
  `$variable`, or fill object/array). `strokeWidth` is the thickness: a number, or a per-side
  `{ top, right, bottom, left }`. Optional: `strokeLinecap` (`butt`/`round`/`square`), `strokeLinejoin`
  (`miter`/`bevel`/`round`), `strokeAlignment` (`inner`/`center`/`outer`). **The old
  `stroke: { color, thickness }` / `stroke: { fill, thickness, align }` object forms are rejected** with
  `/stroke/type expected one of: "color", "gradient", "image", "shader", "mesh_gradient"`.

  ```jsonc
  { "fill": "$surface", "stroke": "$border", "strokeWidth": 1, "cornerRadius": 8 }
  { "stroke": "$border", "strokeWidth": { "top": 2, "right": 0, "bottom": 0, "left": 0 } }
  ```

- **`effect`:** a single effect object or an array. Types: `blur` (`radius`), `background_blur`
  (`radius`), `shadow` (`shadowType: "inner" | "outer"`, `offset: { x, y }`, `blur`, `spread`, `color`,
  `blendMode`). The shadow type string is `"shadow"`, not `"drop_shadow"`. Clear with `effect: []`.
- **`blendMode`** (on fills/effects): `normal`, `multiply`, `screen`, `overlay`, `darken`, `colorBurn`,
  `colorDodge`, `softLight`, `hardLight`, `difference`, `exclusion`, `hue`, `saturation`, `color`,
  `luminosity`, and more, see the live schema.
- **`clip`** (frame): boolean, clip overflow. **`cornerRadius`:** number or `[tl, tr, br, bl]` clockwise from top-left.

## Text nodes

The content field is **`content`** (not `text`/`value`; both rejected). **Text has no colour by default;
always set `fill` or it renders invisible.**

```jsonc
{
  "type": "text",
  "content": "Hello world",
  "fontFamily": "Geist",
  "fontSize": 16,
  "fontWeight": "500",         // StringOrVariable; "400"/"700"/"bold"
  "letterSpacing": 0,
  "fontStyle": "normal",       // "normal" | "italic"
  "underline": false,
  "lineHeight": 1.5,           // ratio of fontSize: 1.0 = 100%
  "textAlign": "left",         // "left" | "center" | "right" | "justify"
  "textAlignVertical": "top",  // "top" | "middle" | "bottom"
  "strikethrough": false,
  "href": null,                // link target
  "textGrowth": "auto",        // "auto" | "fixed-width" | "fixed-width-height"
  "fill": "#0F172A"
}
```

**`textGrowth` rules:**
- `"auto"` (default): single line; `width`/`height` are ignored; never wraps.
- `"fixed-width"`: `width` **must** be set; height grows to fit wrapped content. Use
  `width: "fill_container"` inside a flex parent for headings/paragraphs.
- `"fixed-width-height"`: both `width` and `height` **must** be set; content may overflow.

## Icon nodes

```jsonc
{
  "type": "icon",
  "icon": "circle-check",                  // icon name within the library
  "library": "lucide",                     // "lucide" | "feather" | "Material Symbols Outlined" | "Material Symbols Rounded" | "Material Symbols Sharp" | "phosphor"
  "weight": 400,                           // variable weight 100-700, only where the library supports it
  "width": 24,                             // size with width/height, not fontSize
  "height": 24,
  "fill": "$primary"
}
```

- Properties are `icon` and `library` (the old `icon_font` type and its `iconFontName`/`iconFontFamily`
  properties no longer exist). The icon scales to fit `width`/`height` and needs a `fill` to be visible.
- **Reading icons back:** the `batch_get` pattern enum has no `icon` type and `type: "icon_font"` does
  **not** match `icon` nodes. Find them by `name` pattern, by `parentId`, or read them by id.
- **Lucide naming:** Pencil bundles a recent Lucide build. Geometric shapes are prefix-first:
  `circle-check` (not `check-circle`), `circle-alert`, `circle-x`, `circle-plus`. Some renames:
  `home` → `house`, `bar-chart-2` → `chart-bar`. If the server reports "Icon X was not found", check the
  current Lucide list. Known-good names: `circle-check`, `circle-alert`, `circle-x`, `cloud-off`,
  `arrow-right`, `chevron-right`, `log-in`, `eye`, `eye-off`, `search`, `settings`, `user`, `users`,
  `bell`, `trending-up`, `chart-bar`, `chart-column`, `layout-dashboard`, `house`, `plus`, `x`, `zap`,
  `external-link`.

## Colour

- 8-digit RGBA `#AABBCCDD`, 6-digit `#AABBCC`, 3-digit `#ABC`, or a variable reference `"$primary"`
  (preferred, preserves theme behaviour). Fill opacity is set through the hex alpha channel.

## Variables (design tokens)

Set via `SetVariables(...)` inside `batch_design`. Read existing tokens with `get_variables` first.

```jsonc
"variables": {
  "primary":  { "type": "color",  "value": "#1F6FEB" },
  "spaceMd":  { "type": "number", "value": 16 },
  "fontBody": { "type": "string", "value": "Geist" },
  "isCompact":{ "type": "boolean","value": false }
}
```

Types: `"color"` | `"number"` | `"string"` | `"boolean"`. Reference anywhere via `"$variableName"`.
Variable keys must **not** start with `$` (that prefix is the reference syntax only).

Theme-aware variants pass an array of `{ value, theme }`; the last matching theme wins:

```jsonc
"primary": { "type": "color", "value": [
  { "value": "#1F6FEB", "theme": { "mode": "light" } },
  { "value": "#3B82F6", "theme": { "mode": "dark" } }
] }
```

Multi-axis values layer independently; activate on a node with `theme: { mode: "dark", brand: "globex" }`.

## Themes (axes)

```jsonc
"themes": { "mode": ["light", "dark"], "brand": ["acme", "globex"] }
```

Axes layer independently and **register automatically**: `SetVariables` reads the `theme: {...}` entries
in your values and creates any missing axis/value. No separate axis declaration is needed.

## Components, instances, slots

Mark a node `reusable: true` to make it a component (its id is server-generated, never settable).
Instantiate it with a `ref`:

```jsonc
{
  "type": "ref",
  "ref": "<componentId>",
  "descendants": {
    "Label": { "content": "Sign in" },
    "IconWrap/Icon": { "icon": "log-in" }
  }
}
```

`descendants` keys: a child id, unique child name, or slash-path for nested overrides. A descendant entry
with `type` replaces that subtree; without `type` it merges. (When *copying* a reusable rather than
inserting a `ref`, key descendants by the origin child **id**, not name — see
[`batch-design-grammar.md`](batch-design-grammar.md) § Copy.)

A **slot** is an empty `frame` inside a component marked with `slot`:

```jsonc
{ "type": "frame", "name": "CardBody", "slot": ["TextBlock", "Image"] }
```

The array lists suggested component ids. Slot frames must be empty in the origin; fill them at the
instance level with `Replace(instanceId + "/CardBody", { ... })`.

## Imports

```jsonc
"imports": { "ds": "./design/system.lib.pen" }
```

Brings in the imported file's `variables` and `reusable` components. Path is relative to the importing
`.pen`. Read an imported library with `batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }] })`.

## Script nodes

A `script` node points to a JavaScript file whose returned nodes render as children at canvas time.

```jsonc
{
  "type": "script",
  "scriptUri": "./generators/grid.js",
  "width": 600,
  "height": 400,
  "inputs": { "rows": 3, "color": "#3B82F6" }
}
```

Script file rules:
- First line must be `/** @schema 2.11 */` (current version). Missing the tag is an error.
- Scripts receive a `pencil` object: `pencil.width`, `pencil.height`, `pencil.input.<name>`.
- Must return an array of node objects following this schema.
- Inputs are declared with `@input name: type [= default]`. Types: `number`, `string`, `boolean`,
  `color`, `ref`, `enum("a","b",...)`.
- `Math.random()` is **deterministic** in scripts, safe for reproducible procedural generation.

Reach for `script` when a layout depends on a runtime input or needs procedural content. Avoid it for
anything you'd otherwise hand-build with primitives; debugging a script is harder than reading flat
node properties. Worked example in [`advanced-canvas.md`](advanced-canvas.md).

## Common gotchas

- IDs with `/` are rejected; `/` is the path separator in `descendants` keys and instance paths.
- `width: "100%"` is rejected; use `width: "fill_container"`.
- Bindings inside a `batch_design` call are per-call. Reference a node from a later call by its literal
  id (from the returned `name → id` map or `batch_get`), never by a previous call's variable name.
- `gap`/`alignItems` do nothing under `layout: "none"`; the layout must be `vertical`/`horizontal`.
- A `ref` cannot itself be `reusable`.
- `x`/`y` are ignored in flex children; `fill_container` needs a flex parent.
- A `fit_content` frame whose every child is `fill_container` is a circular dependency.
- **No `image` node type.** Images are image `fill`s on a `frame`/`rectangle`; generate them with
  `Generate(nodeId, "ai" | "stock", "prompt")` inside `batch_design`.
- **Text needs `fill`**, or it renders invisible with no error.
