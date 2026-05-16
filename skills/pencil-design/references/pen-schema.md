# `.pen` schema reference

Cheat-sheet for the `.pen` JSON format. Source of truth: <https://docs.pencil.dev/for-developers/the-pen-format>.

## Document

```jsonc
{
  "version": "2.11",
  "themes": { /* optional */ },
  "imports": { /* optional */ },
  "variables": { /* optional */ },
  "children": [ /* required, array of nodes */ ]
}
```

**Updating document-level properties.**

- **Tokens** (`variables`): go through `set_variables`. Themed values like `{ value: "#FAFAFA", theme: { mode: "light" } }` auto-register the matching theme axis, no separate axis declaration is needed.
- **Themes** (`themes`): managed automatically by `set_variables`. There is no other documented path; `U("document", { themes })` errors with `Node 'document' not found`, and `U(<frameId>, { themes })` errors with `/themes unexpected property`.
- **Imports** (`imports`): currently no documented MCP path. `U("document", { imports })` and `U(<frameId>, { imports })` both error. Add or edit `imports` in the `.pen` JSON directly until the server exposes an import-management API.

`U("document", ...)` in `batch_design` is not supported in general, the `document` binding is insert-only. Use it as a parent for top-level frame inserts: `foo=I(document, { type: "frame", ... })`.

## Entity (every node extends this)

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Unique string. **MUST NOT contain `/`**. The server accepts a `/`-containing id on insert, but downstream references to that id as a parent (`I("section/title", ...)`) hard-error with `Can't find parent node`. Treat the rule as absolute, don't include `/` in your own ids. The slash separator is only meaningful inside `descendants` path keys and `U(instance+"/childId", ...)` overrides. |
| `type` | yes | One of the node types below. |
| `name` | no | Display name in the layers panel. |
| `context` | no | Free-form context string for agent / collaborator notes. |
| `reusable` | no | `true` makes this node a component (instantiable via `ref`). |
| `theme` | no | Theme-axis activation: `{ axisName: "value" }`. |
| `enabled` | no | Boolean or variable. Hides node when false. |
| `opacity` | no | 0–1. |
| `flipX`, `flipY` | no | Boolean. |
| `layoutPosition` | no | `"auto"` (default, participates in parent flex) or `"absolute"` (absolutely positioned within a flex parent, ignores flow). |
| `metadata` | no | Object with a required `type: string` field plus any extra keys: `{ type: "myTool", ... }`. |
| `rotation` | no | Degrees counter-clockwise around the node's top-left corner. |

Position uses `x`, `y` for the top-left corner. **Children are positioned relative to their parent's top-left. x/y are completely ignored when the parent uses flexbox layout (`layout: "vertical"` or `"horizontal"`), use flex properties instead.**

## Node types

### Shape & container

| Type | Notes |
|------|-------|
| `rectangle` | Position + size + graphics. Most common primitive. |
| `ellipse` | `innerRadius` (0=solid, 1=hollow), `startAngle` (degrees CCW from right), `sweepAngle` (positive=CCW, negative=CW, range -360..360). Donut: `innerRadius: 0.6`. 90° arc clockwise from 12 o'clock: `startAngle: 90, sweepAngle: -90`. |
| `line` | Defined by its bounding rect. Use `stroke: { align: "center", ... }` on unconnected lines. |
| `polygon` | `polygonCount` (sides), `cornerRadius`. |
| `path` | SVG path geometry. `fillRule: "nonzero" \| "evenodd"`. Always set `viewBox: [x, y, w, h]`. |
| `frame` | Rectangle that holds children. The auto-layout container. See Frame section below. |
| `group` | Container with effects, no layout. Children are absolutely positioned. |

### Content

| Type | Notes |
|------|-------|
| `text` | Rich text. Content field is **`content`** (not `text` or `value`). Has no colour by default, always set `fill`. |
| `icon_font` | Icon from a font set. Properties: `iconFontName` (icon name), `iconFontFamily` (library), `weight` (for variable-weight fonts only, 100–700), `fill`. Size via `width`/`height`. |
| `note` | Non-rendering annotation. Has `content` plus TextStyle (`fontFamily`, `fontSize`, `lineHeight`, `textAlign`, etc.). **Does not accept `fill`, `stroke`, or `effect`**; annotation nodes inherit Entity + Size + TextStyle only, not CanHaveGraphics. For collaboration / agent notes that travel with the file but never render. |
| `prompt` | Non-rendering AI prompt. Has `content`, optional `model` (which LLM the prompt targets), plus TextStyle. Same graphics-property restriction as `note`. Used when a design captures an LLM operation by name. |
| `context` | Non-rendering context note. Has `content` plus TextStyle. Same graphics-property restriction as `note`. Used for agent-readable scene context, analogous to the Entity-level `context` field, but as a standalone node when the context applies to a region rather than a specific node. |

### Component & code

| Type | Notes |
|------|-------|
| `ref` | Instance of a `reusable: true` node. Has `ref: "<componentId>"` and optional `descendants` overrides (keyed by id, or by slash-separated path for nested overrides). |
| `script` | Code on Canvas, points at a `.js` file whose output renders as nested layers. See the Script nodes section below for the full schema-tag + inputs convention. |

**Note:** `batch_get`'s pattern filter accepts two additional type strings that aren't in the `Child` union, `"connection"` (canvas connection lines between nodes, surfaced when reading a board-style document) and `"image"` (matches nodes whose `fill` is an image; there is no standalone image node type, images are fills on `frame` or `rectangle`).

## Sizing

`width` and `height` accept these shapes:

```jsonc
"width": 240                       // explicit number
"width": "$buttonWidth"            // variable reference
"width": "fill_container"          // grow to fill parent's auto-layout axis
"width": "fit_content"             // shrink to children
"width": "fill_container(320)"     // fill with fallback minimum
"width": "fit_content(100)"        // fit with fallback minimum
```

**Constraints:**
- `fill_container` is only valid when the parent has `layout: "vertical"` or `"horizontal"`. On an absolutely-positioned parent it has no effect.
- `fit_content` is only valid on a node that itself uses flexbox layout.
- A parent sized `fit_content` cannot have all direct children sized `fill_container`, circular dependency.
- Don't use `"100%"` or the old `{ "sizing": "fill_container" }` object form. Both are rejected.

## Layout (flexbox-style)

On a `frame`:

```jsonc
{
  "layout": "vertical",       // "none" | "vertical" | "horizontal". Frames default to "horizontal".
  "gap": 16,                  // between children. Number or variable.
  "padding": 16,              // number | [horizontal, vertical] | [top, right, bottom, left]. NO object form, NO individual paddingTop/paddingLeft etc.
  "justifyContent": "start",  // "start" | "center" | "end" | "space_between" | "space_around" , underscores, not hyphens
  "alignItems": "center"      // "start" | "center" | "end"
}
```

**Key rules:**
- `layout` accepts exactly `"none"`, `"vertical"`, or `"horizontal"`. Frames default to `"horizontal"`, groups default to `"none"`. CSS flexbox words (`"flex"`, `"row"`, `"column"`, `"grid"`) hard-error.
- `layout: "none"` means children are positioned absolutely via their `x`/`y`.
- When a parent uses `layout: "vertical"` or `"horizontal"`, **child `x`/`y` are completely ignored**. Use flex properties (`gap`, `justifyContent`, `alignItems`, `padding`) to position children.
- `padding` rejects the object form `{ top: N, left: N, ... }` and individual `paddingTop` / `paddingLeft` etc. Use only: a single number, `[horizontal, vertical]`, or `[top, right, bottom, left]`.
- `justifyContent` canonical values use **underscores**, `"space_between"`, `"space_around"`. The hyphenated `"space-between"` and `"space-around"` aliases are also accepted by the server, but prefer the underscore form in new code.
- `alignItems` canonical values are `"start"`, `"center"`, `"end"`. The CSS aliases `"flex_start"` and `"flex_end"` are also accepted. **`"stretch"` is NOT accepted**; it's the most reached-for CSS alignItems value but Pencil rejects it. The right pattern to make children span the cross axis: set `width: "fill_container"` (for a vertical-layout parent) or `height: "fill_container"` (for a horizontal-layout parent) on each child. Prefer canonical for new code.

## Graphics

- **`fill`:** a colour string (or variable reference), a single fill object, or an array of fill objects painted bottom-to-top. **Plain colour string `"#RRGGBBAA"` or `"$variable"` is accepted as shorthand and preferred for the single-fill case.** Fill object types: `"color"` (**not** `"solid_color"`), `"gradient"`, `"image"`, `"mesh_gradient"`.
- **`stroke`:** single stroke object. Properties: `thickness`, `align` (`"inside" | "center" | "outside"`), `join`, `cap`, `dashPattern`, plus one of `color` (colour string or variable) **or** `fill` (full `Fills` shape, colour, gradient, or image). Both `{ color, thickness }` and `{ fill, thickness }` shapes are accepted; use `color` for the common solid case and `fill` when you need a gradient or image stroke. Dashed example: `{ thickness: 1, color: "$border", align: "inside", dashPattern: [4, 2] }` (4 px dash, 2 px gap).
- **`effect`:** array of effect objects. Types: `"blur"` (`radius`), `"background_blur"` (`radius`), `"shadow"` (`shadowType: "inner" | "outer"`, `offset`, `spread`, `blur`, `color`). There is no `"drop_shadow"` type, use `"shadow"` with `shadowType: "outer"`.
- **`blendMode`:** `"normal"` | `"darken"` | `"multiply"` | `"linearBurn"` | `"colorBurn"` | `"light"` | `"screen"` | `"linearDodge"` | `"colorDodge"` | `"overlay"` | `"softLight"` | `"hardLight"` | `"difference"` | `"exclusion"` | `"hue"` | `"saturation"` | `"color"` | `"luminosity"`.
- **`clip`:** boolean, visually clip overflow.
- **`rotation`:** counter-clockwise, in degrees.
- **`cornerRadius`:** single number or `[tl, tr, br, bl]` array, order starts top-left and goes clockwise.

## Frame

Extends Entity + Size + Layout + Graphics.

```jsonc
{
  "type": "frame",
  "clip": false,          // clip overflow. Default false.
  "placeholder": true,    // marks frame as in-progress during generation. Remove when done.
  "slot": false           // false | string[] of recommended reusable child component ids
}
```

**Defaults:** frames default to `layout: "horizontal"` and `fit_content` sizing when no size is specified.

Use `placeholder: true` on every new top-level frame at the start of generation. Remove it (`U(id, { placeholder: false })`) as soon as the frame is complete.

## Text nodes

**The text content field is `content`**, not `text`, not `value`. Both are rejected with `unexpected property`.

**Text has no colour by default and will be invisible. Always set `fill`.**

```jsonc
{
  "type": "text",
  "content": "Hello world",
  "fontFamily": "Geist",
  "fontSize": 16,
  "fontWeight": 500,           // StringOrVariable, accepts numbers (400, 700) or strings ("bold")
  "letterSpacing": 0,
  "fontStyle": "normal",       // "normal" | "italic"
  "underline": false,
  "lineHeight": 1.5,           // ratio relative to fontSize: 1.0 = 100%, 1.5 = 150%
  "textAlign": "left",         // "left" | "center" | "right" | "justify"
  "textAlignVertical": "top",  // "top" | "middle" | "bottom"
  "strikethrough": false,
  "href": null,
  "textGrowth": "auto",        // "auto" | "fixed-width" | "fixed-width-height"
  "fill": "#0F172A"            // required, text is invisible without fill
}
```

**`textGrowth` rules:**
- `"auto"` (default): single line, width+height calculated from content. Never set `width`/`height`, they are ignored.
- `"fixed-width"`: `width` must be set; height grows to fit wrapped content. Use `width: "fill_container"` inside a flex parent.
- `"fixed-width-height"`: both `width` and `height` must be set; content may overflow.

## Icon font nodes

```jsonc
{
  "type": "icon_font",
  "iconFontName": "circle-check",          // the icon name, Lucide uses shape-as-prefix: "circle-check", "circle-alert", "circle-x", "circle-plus"
  "iconFontFamily": "lucide",              // "lucide" | "feather" | "Material Symbols Outlined" | "Material Symbols Rounded" | "Material Symbols Sharp" | "phosphor"
  "weight": 400,                           // variable font weight, only for variable-weight fonts
  "width": 24,                             // required, size the icon with width/height, not fontSize
  "height": 24,
  "fill": "$primary"
}
```

**Do not use `fontSize` or `iconName` or `iconLibrary`, those properties don't exist on `icon_font`.**

**Lucide icon naming:** Pencil bundles a recent Lucide build. Geometric shapes moved to prefixes: `circle-check` (not `check-circle`), `circle-alert` (not `alert-circle`), `circle-x` (not `x-circle`), `circle-plus` (not `plus-circle`). Some icons were also renamed: `home` → `house`, `bar-chart-2` → `chart-bar`. If the server reports "Icon X was not found", check the current Lucide icon list. Valid tested names: `circle-check`, `circle-alert`, `circle-x`, `cloud-off`, `arrow-right`, `chevron-right`, `log-in`, `eye`, `eye-off`, `search`, `settings`, `user`, `users`, `bell`, `trending-up`, `chart-bar`, `chart-column`, `layout-dashboard`, `house`, `plus`, `x`, `zap`, `external-link`.

## Color

- 8-digit RGBA hex: `#AABBCCDD`
- 6-digit RGB hex: `#AABBCC`
- 3-digit RGB hex: `#ABC`
- Variable reference: `"$primary"` (preferred, preserves theme behavior)

## Variables (design tokens)

Defined at document level via `set_variables` or in the JSON directly:

```jsonc
"variables": {
  "primary": { "type": "color", "value": "#1F6FEB" },
  "spaceMd":  { "type": "number", "value": 16 },
  "fontBody": { "type": "string", "value": "Geist" }
}
```

Types: `"color"` | `"number"` | `"boolean"` | `"string"`. Reference from anywhere via `"$variableName"`.

Theme-aware variants:

```jsonc
"primary": {
  "type": "color",
  "value": [
    { "value": "#1F6FEB", "theme": { "mode": "light" } },
    { "value": "#3B82F6", "theme": { "mode": "dark" } }
  ]
}
```

When evaluating, **the last matching theme wins.** Activate a theme on a node with `theme: { mode: "dark" }`.

A multi-axis themed variable layers on every axis active at once:

```jsonc
"accentBold": {
  "type": "color",
  "value": [
    { "value": "#FF0000", "theme": { "mode": "light", "brand": "acme" } },
    { "value": "#00FF00", "theme": { "mode": "light", "brand": "globex" } },
    { "value": "#0000FF", "theme": { "mode": "dark",  "brand": "acme" } },
    { "value": "#FF00FF", "theme": { "mode": "dark",  "brand": "globex" } }
  ]
}
```

Activate both at once on a node with `theme: { mode: "dark", brand: "globex" }`.

## Themes (axes)

```jsonc
"themes": {
  "mode": ["light", "dark"],
  "brand": ["acme", "globex"]
}
```

Multiple axes layer independently. **`themes` registers automatically**, `set_variables` reads the `theme: {...}` entries in your variable values and creates the corresponding axis. No separate axis declaration is needed.

## Components (reusable + ref)

Mark a node `reusable: true` to make it a component:

```jsonc
{ "type": "frame", "id": "ButtonPrimary", "reusable": true }
```

Instantiate elsewhere with a `ref` node:

```jsonc
{
  "type": "ref",
  "ref": "ButtonPrimary",
  "descendants": {
    "label": { "content": "Sign in" },
    "iconWrap/icon": { "iconFontName": "log-in" }
  }
}
```

`descendants` keys: a child id, or a slash-separated path for nested overrides. A descendant entry with `type` present fully replaces that subtree; without `type`, it merges properties.

## Slots

A slot is an empty `frame` inside a `reusable` component, marked with the `slot` property:

```jsonc
{ "type": "frame", "id": "cardBody", "slot": ["TextBlock", "Image"] }
```

The array lists suggested-component ids. Slot frames must be empty in the origin component.

## Imports

```jsonc
"imports": { "ds": "./design/system.lib.pen" }
```

Brings in the imported file's `variables` and `reusable` components. Path is relative to the importing `.pen`.

**No documented MCP write path for `imports`**, `U("document", { imports })` and `U(<frameId>, { imports })` both error. Add or edit imports in the `.pen` JSON directly until the server exposes an import-management API.

## Script nodes

A `script` node points to a JavaScript file whose output renders as nested children at canvas time.

```jsonc
{
  "type": "script",
  "scriptUri": "./generators/grid.js",
  "width": 600,
  "height": 400,
  "inputs": { "rows": 3, "color": "#3B82F6" }
}
```

**Script file rules:**

- First line must be `/** @schema 2.10 */`. Missing this tag is an error.
- Scripts receive a `pencil` object: `pencil.width`, `pencil.height`, `pencil.input.<name>`.
- Scripts must return an array of node objects following the `.pen` schema.
- Inputs are declared via `@input name: type [= default]` JSDoc annotations. Types: `number`, `string`, `boolean`, `color`, `ref`, `enum("a","b",...)`.
- `Math.random()` is **deterministic** in scripts, safe for reproducible procedural generation.

Reach for `script` when a layout depends on a runtime input (parameterised hero, configurable grid) or needs procedural content (scatter, generated cells). Avoid for anything you'd otherwise hand-build with primitives, debugging a script is harder than reading flat node properties.

## Common gotchas

- IDs with `/` are accepted on insert but cannot be referenced as a parent downstream, don't include `/` in your own ids. The `/` separator is only meaningful inside `descendants` path keys and `U(instance+"/childId", ...)` overrides.
- Don't use `width: "100%"`, use `width: "fill_container"`.
- Don't use padding object form `{ top: N }`, use a single number or array `[h, v]` / `[t, r, b, l]`.
- Don't use `text:` or `value:` on text nodes, use `content:`.
- Don't use `solid_color` in fill objects, use `"color"`.
- Don't use `drop_shadow` in effects, use `"shadow"` with `shadowType: "outer"`.
- Don't use CSS flexbox layout names, `layout` accepts only `"none"`, `"vertical"`, `"horizontal"`.
- `justifyContent` underscored values are canonical (`"space_between"`); hyphenated CSS aliases also work but prefer canonical.
- `alignItems` canonical values are `"start"`, `"center"`, `"end"`; CSS aliases `"flex_start"` / `"flex_end"` also work.
- Don't set `x`/`y` on a child when the parent uses flexbox layout, they are silently ignored.
- `fill_container` only works when the parent has a flexbox layout.
- `fit_content` only works on nodes that themselves use flexbox layout.
- A parent sized `fit_content` with all children sized `fill_container` is a circular dependency.
- `U("document", ...)` in `batch_design` is not supported, `document` is an insert-only binding. Tokens go through `set_variables` (themes auto-register); imports require direct JSON edit.
- A `ref` cannot itself be `reusable`. No meta-components.
- Text nodes have no colour by default, always set `fill`, or the text renders invisible.
- Setting `width`/`height` on a `text` node with `textGrowth: "auto"` silently does nothing, use `textGrowth: "fixed-width"` plus an explicit width to enable wrapping.
- Variable names must not start with `$`, the `$` prefix is only for reference syntax in node properties.
