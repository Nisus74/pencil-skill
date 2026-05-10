# `.pen` schema reference

Cheat-sheet for the `.pen` JSON format. Source of truth: <https://docs.pencil.dev/for-developers/the-pen-format>.

All properties on this page are **verified live against the MCP server (2026-05)** unless noted otherwise.

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

**Updating document-level properties:** `U("document", ...)` is not supported in `batch_design` — the `document` binding is insert-only. Use `set_variables` to write tokens. For `themes` and `imports`, use `U` with the actual document root node ID returned by `open_document`.

## Entity (every node extends this)

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Unique string. **MUST NOT contain `/`**. The server rejects it. |
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

Position uses `x`, `y` for the top-left corner. **Children are positioned relative to their parent's top-left. x/y are completely ignored when the parent uses flexbox layout (`layout: "vertical"` or `"horizontal"`) — use flex properties instead.**

## Node types

### Shape & container

| Type | Notes |
|------|-------|
| `rectangle` | Position + size + graphics. Most common primitive. |
| `ellipse` | `innerRadius` (0=solid, 1=hollow), `startAngle`, `sweepAngle` for rings/arcs. |
| `line` | Defined by its bounding rect. Use `stroke: { align: "center", ... }` on unconnected lines. |
| `polygon` | `polygonCount` (sides), `cornerRadius`. |
| `path` | SVG path geometry. `fillRule: "nonzero" \| "evenodd"`. Always set `viewBox: [x, y, w, h]`. |
| `frame` | Rectangle that holds children. The auto-layout container. See Frame section below. |
| `group` | Container with effects, no layout. Children are absolutely positioned. |

### Content

| Type | Notes |
|------|-------|
| `text` | Rich text. Content field is **`content`** (not `text` or `value`). |
| `icon_font` | Icon from a font set. Properties: `iconFontName` (icon name), `iconFontFamily` (library), `weight`, `fill`. Size via `width`/`height`. |
| `note`, `prompt`, `context` | Annotation types — non-rendering; for collaboration / agent notes. |

### Component & code

| Type | Notes |
|------|-------|
| `ref` | Instance of a `reusable: true` node. Has `ref: "<componentId>"` and optional `descendants` overrides. |
| `script` | Code on Canvas — points at a `.js` file whose output renders as nested layers. |

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
- A parent sized `fit_content` cannot have all direct children sized `fill_container` — circular dependency.
- Don't use `"100%"` or the old `{ "sizing": "fill_container" }` object form. Both are rejected.

## Layout (flexbox-style)

On a `frame`:

```jsonc
{
  "layout": "vertical",       // "none" | "vertical" | "horizontal". Frames default to "horizontal".
  "gap": 16,                  // between children. Number or variable.
  "padding": 16,              // number | [horizontal, vertical] | [top, right, bottom, left]. NO object form, NO individual paddingTop/paddingLeft etc.
  "justifyContent": "start",  // "start" | "center" | "end" | "space_between" | "space_around"  — underscores, not hyphens
  "alignItems": "center"      // "start" | "center" | "end"
}
```

**Key rules:**
- `layout: "none"` (the default for groups; frames default to `"horizontal"`) means children are positioned absolutely via their `x`/`y`.
- When a parent uses `layout: "vertical"` or `"horizontal"`, **child `x`/`y` are completely ignored**. Use flex properties (`gap`, `justifyContent`, `alignItems`, `padding`) to position children.
- `padding` rejects the object form `{ top: N, left: N, ... }` and individual `paddingTop` / `paddingLeft` etc. Use only: a single number, `[horizontal, vertical]`, or `[top, right, bottom, left]`.
- `justifyContent` and `space_around` use underscores — `"space_between"` not `"space-between"`.

## Graphics

- **`fill`:** a color string, a variable string, or an array of fill objects painted bottom-to-top. **Plain color string `"#RRGGBBAA"` or `"$variable"` is accepted as shorthand and preferred.** Fill object types: `"color"` (**not** `"solid_color"`), `"gradient"`, `"image"`, `"mesh_gradient"`.
- **`stroke`:** single stroke object. Properties: `fill` (color or fill object, singular — not `fills`), `thickness`, `align` (`"inside" | "center" | "outside"`), `join`, `cap`, `dashPattern`. Example: `{ thickness: 1, fill: "#E5E7EB", align: "inside" }`.
- **`effect`:** array of effect objects. Types: `"blur"` (`radius`), `"background_blur"` (`radius`), `"shadow"` (`shadowType`, `offset`, `spread`, `blur`, `color`).
- **`blendMode`:** `"normal"` | `"darken"` | `"multiply"` | `"linearBurn"` | `"colorBurn"` | `"light"` | `"screen"` | `"linearDodge"` | `"colorDodge"` | `"overlay"` | `"softLight"` | `"hardLight"` | `"difference"` | `"exclusion"` | `"hue"` | `"saturation"` | `"color"` | `"luminosity"`
- **`clip`:** boolean — visually clip overflow.
- **`rotation`:** counter-clockwise, in degrees.
- **`cornerRadius`:** single number or `[tl, tr, br, bl]`.

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

**The text content field is `content`** — not `text`, not `value`. Both are rejected with `unexpected property`.

**Text has no colour by default and will be invisible. Always set `fill`.**

```jsonc
{
  "type": "text",
  "content": "Hello world",
  "fontFamily": "Geist",
  "fontSize": 16,
  "fontWeight": 500,           // StringOrVariable — accepts numbers (400, 700) or strings ("bold")
  "letterSpacing": 0,
  "fontStyle": "normal",       // "normal" | "italic"
  "underline": false,
  "lineHeight": 1.5,           // ratio relative to fontSize: 1.0 = 100%, 1.5 = 150%
  "textAlign": "left",         // "left" | "center" | "right" | "justify"
  "textAlignVertical": "top",  // "top" | "middle" | "bottom"
  "strikethrough": false,
  "href": null,
  "textGrowth": "auto",        // "auto" | "fixed-width" | "fixed-width-height"
  "fill": "#0F172A"            // required — text is invisible without fill
}
```

**`textGrowth` rules:**
- `"auto"` (default): single line, width+height calculated from content. Never set `width`/`height` — they are ignored.
- `"fixed-width"`: `width` must be set; height grows to fit wrapped content. Use `width: "fill_container"` inside a flex parent.
- `"fixed-width-height"`: both `width` and `height` must be set; content may overflow.

## Icon font nodes

```jsonc
{
  "type": "icon_font",
  "iconFontName": "circle-check",          // the icon name — Lucide uses shape-as-prefix: "circle-check", "circle-alert", "circle-x", "circle-plus"
  "iconFontFamily": "lucide",              // "lucide" | "feather" | "Material Symbols Outlined" | "Material Symbols Rounded" | "Material Symbols Sharp" | "phosphor"
  "weight": 400,                           // variable font weight — only for variable-weight fonts
  "width": 24,                             // required — size the icon with width/height, not fontSize
  "height": 24,
  "fill": "$primary"
}
```

**Do not use `fontSize` or `iconName` or `iconLibrary` — those properties don't exist on `icon_font`.**

**Lucide icon naming:** Pencil bundles a recent Lucide build. Geometric shapes moved to prefixes: `circle-check` (not `check-circle`), `circle-alert` (not `alert-circle`), `circle-x` (not `x-circle`), `circle-plus` (not `plus-circle`). Some icons were also renamed: `home` → `house`, `bar-chart-2` → `chart-bar`. If the server reports "Icon X was not found", check the current Lucide icon list. Valid tested names: `circle-check`, `circle-alert`, `circle-x`, `cloud-off`, `arrow-right`, `chevron-right`, `log-in`, `eye`, `eye-off`, `search`, `settings`, `user`, `users`, `bell`, `trending-up`, `chart-bar`, `chart-column`, `layout-dashboard`, `house`, `plus`, `x`, `zap`, `external-link`.

## Color

- 8-digit RGBA hex: `#AABBCCDD`
- 6-digit RGB hex: `#AABBCC`
- 3-digit RGB hex: `#ABC`
- Variable reference: `"$primary"` (preferred — preserves theme behavior)

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

## Themes (axes)

```jsonc
"themes": {
  "mode": ["light", "dark"],
  "brand": ["acme", "globex"]
}
```

Multiple axes layer independently.

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

## Common gotchas

- IDs with `/` are rejected — use `/` only in `descendants` path keys.
- Don't use `width: "100%"` — use `width: "fill_container"`.
- Don't use padding object form `{ top: N }` — use array `[top, right, bottom, left]`.
- Don't use `text:` or `value:` on text nodes — use `content:`.
- Don't use `solid_color` in fill objects — use `"color"`.
- Don't use `justifyContent: "space-between"` — use `"space_between"` (underscore).
- Don't set `x`/`y` on a child when the parent uses flexbox layout — they are ignored.
- `fill_container` only works when the parent has a flexbox layout.
- `fit_content` only works on nodes that themselves use flexbox layout.
- A parent sized `fit_content` with all children sized `fill_container` is a circular dependency.
- `U("document", ...)` in `batch_design` is not supported — `document` is an insert-only binding.
- A `ref` cannot itself be `reusable`. No meta-components.
- Don't bind `#000000` or `#FFFFFF` directly to surfaces — use variables resolving to near-black / near-white.
