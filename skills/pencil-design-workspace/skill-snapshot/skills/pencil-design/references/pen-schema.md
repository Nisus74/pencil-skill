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

## Entity (every node extends this)

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Unique string. **MUST NOT contain `/`**. The server rejects it. |
| `type` | yes | One of the node types below. |
| `name` | no | Display name in the layers panel. |
| `context` | no | Free-form context string. |
| `reusable` | no | `true` makes this node a component (instantiable via `ref`). |
| `theme` | no | Theme-axis activation: `{ axisName: "value" }`. |
| `enabled`, `opacity`, `flipX`, `flipY` | no | Visibility / transform basics. |
| `layoutPosition` | no | Override how this child positions inside an auto-layout parent. |
| `metadata` | no | Free-form key-value map. |

Position uses `x`, `y` for the top-left corner. **Children are positioned relative to their parent's top-left.**

## Node types

### Shape & container

| Type | Notes |
|------|-------|
| `rectangle` | Position + size. Most common building block. |
| `ellipse` | `innerRadius`, `startAngle`, `sweepAngle` for rings/arcs. |
| `line` | Defined by its bounding rect. |
| `polygon` | `polygonCount` (sides), `cornerRadius`. |
| `path` | SVG path geometry. `fillRule: "nonzero" \| "evenodd"`. |
| `frame` | Rectangle that holds children. The auto-layout container. |
| `group` | Container with effects AND layout (supports `layout`, `gap`, `padding`, `justifyContent`, `alignItems`). Has `width`/`height` as `SizingBehavior` only. |

### Content

| Type | Notes |
|------|-------|
| `text` | Rich text. `textGrowth`: `"auto"`, `"fixed-width"`, `"fixed-width-height"`. |
| `icon_font` | Icon from a font set (Lucide / Material / Phosphor / Feather). Prefer this over imported SVG icons. |
| `note`, `prompt`, `context` | Annotation types — non-rendering; for collaboration / agent context. |

### Component & code

| Type | Notes |
|------|-------|
| `ref` | Instance of a `reusable: true` node. Has `ref: "<componentId>"` and optional `descendants` overrides. |
| `script` | Code on Canvas — points at a `.js` file whose output renders as nested layers. Sandboxed; `@input` declarations become controls. |

## Sizing

`width` and `height` accept these shapes:

```jsonc
"width": 240                       // explicit number
"width": "$buttonWidth"            // variable reference
"width": "fill_container"          // bare string — grow to fill parent's auto-layout
"width": "fit_content"             // bare string — shrink to children
"width": "fill_container(320)"     // with fallback (function-call form, baked into the string)
"width": "fit_content(100)"        // with fallback
```

**Verified live (2026-05):** the schema accepts the bare-string and function-call forms above. It rejects the older `{ "sizing": "fill_container" }` object form with the error `expected one of: number, "$variable", sizing behavior (fit_content or fill_container, with optional fallback size like fit_content(100))`. Use the bare string.

## Layout (flexbox-style)

On a `frame`:

```jsonc
{
  "layout": "vertical",          // "none" | "vertical" | "horizontal"
  "gap": "$space-4",             // between children
  "padding": [16, 24],           // number (all sides) | [horiz, vert] | [top, right, bottom, left]
  "justifyContent": "start",     // start | center | end | space_between | space_around
  "alignItems": "center"         // start | center | end   ← NO stretch or baseline
}
```

`layout: "none"` (the default) means children are positioned absolutely via their `x`/`y`.

## Graphics

- **`fill`:** bare `ColorOrVariable` string (most common: `"$primary"`, `"#1F6FEB"`), a single fill object, or an array of fill objects painted bottom-to-top. Structured types: `{ type: "color", color: ColorOrVariable }`, `{ type: "gradient", gradientType: "linear"|"radial"|"angular", ... }`, `{ type: "image", url: "...", mode: "fill"|"fit"|"stretch" }`, `{ type: "mesh_gradient", ... }`. **There is no `solid_color` type** — use the bare string or `type: "color"`.
- **`stroke`:** single stroke object. Properties: `fill` (ColorOrVariable or fill object), `thickness` (NumberOrVariable or `{top, right, bottom, left}` object), `align` (`"inside" | "center" | "outside"`), `join` (`"miter" | "bevel" | "round"`), `cap` (`"none" | "round" | "square"`), `dashPattern` (number[]), `miterAngle`. **Verified live (2026-05):** use singular `fill` (not `fills`); `align` is valid (not `alignment`). Example: `"stroke": { "thickness": 1, "fill": "$border", "align": "inside" }`.
- **`effect`:** array of effects. Order matters. Types: `blur`, `background_blur`, `shadow`.
- **`blendMode`:** 15 modes (`multiply`, `screen`, `overlay`, etc.).
- **`clip`:** boolean — visually clip overflow.
- **`rotation`:** counter-clockwise, in degrees.
- **`cornerRadius`:** single number or `[tl, tr, br, bl]`.

## Text node

Text nodes use `content` (not `text`) for their string value. **Text has no default color — always set `fill` or the node will be invisible.**

`textGrowth` controls sizing:
- `"auto"` (default) — grows to fit; `width`/`height` are ignored; never wraps.
- `"fixed-width"` — `width` **must** be set; `height` grows to fit wrapped content.
- `"fixed-width-height"` — both `width` and `height` **must** be set; may overflow.

When the parent has flexbox layout, set `width: "fill_container"` + `textGrowth: "fixed-width"` for wrapping text that fills its container.

## Text styling

```jsonc
{
  "fontFamily": "$fontBody",
  "fontSize": "$textBase",
  "fontWeight": "700",
  "letterSpacing": 0,
  "fontStyle": "normal",        // "normal" | "italic"
  "underline": false,
  "lineHeight": 1.5,
  "textAlign": "left",          // "left" | "center" | "right" | "justify"
  "textAlignVertical": "top",
  "strikethrough": false,
  "href": null                  // link target
}
```

## Color

- 8-digit RGBA hex: `#AABBCCDD`
- 6-digit RGB hex: `#AABBCC`
- 3-digit RGB hex: `#ABC`
- Variable reference: `"$primary"` (preferred — preserves theme behavior)

## Variables (design tokens)

Defined at document level:

```jsonc
"variables": {
  "primary": {
    "type": "color",                    // "color" | "number" | "boolean" | "string"
    "value": "#1F6FEB"
  },
  "spaceMd": {
    "type": "number",
    "value": 16
  },
  "fontBody": {
    "type": "string",
    "value": "Inter"
  }
}
```

Reference from anywhere via `"$variableName"`. Theme-aware variants:

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

Declare theme axes at document level:

```jsonc
"themes": {
  "mode": ["light", "dark"],
  "brand": ["acme", "globex"]
}
```

Multiple axes layer independently. A node can activate values from any combination.

## Components (reusable + ref)

Mark a node `reusable: true` to make it a component:

```jsonc
{ "type": "frame", "id": "ButtonPrimary", "reusable": true, /* ... */ }
```

Instantiate elsewhere:

```jsonc
{
  "type": "ref",
  "id": "loginCta",
  "ref": "ButtonPrimary",
  "descendants": {
    "label": { "content": "Sign in" },
    "iconWrap/icon": { "iconName": "log-in" }
  }
}
```

`descendants` keys can be a child id, or a slash-separated path for nested overrides. A descendant entry can:

- override properties (most common)
- replace the child entirely (include `type` in the override)
- replace its children (`children: [...]`)

## Slots

A slot is an empty `frame` inside a `reusable` component, marked with the `slot` property:

```jsonc
{
  "type": "frame",
  "id": "cardBody",
  "slot": ["TextBlock", "Image", "Form"]
}
```

The string array is the list of suggested-component ids that fit this slot. The editor (and you) display them as one-click options. Slot frames must be empty in the origin.

## Imports

```jsonc
"imports": {
  "ds": "./design/system.lib.pen"
}
```

Brings in the imported file's `variables` and `reusable` components. Reference imported components by their bare id (Pencil resolves the alias). The path is relative to the importing `.pen`.

## Common gotchas

- IDs with `/` are rejected — the server uses `/` as a path separator in `descendants` keys.
- Don't pass `width: "100%"` — use `width: "fill_container"` (bare string).
- Don't insert into a parent created earlier in the *same* `batch_design` call without binding it (`foo=I(...)`); the server can't resolve a forward-reference.
- Mixing `layout: "none"` with auto-layout `gap` does nothing — the layout has to be `"vertical"` or `"horizontal"` for `gap` and `alignItems` to apply.
- A `ref` cannot itself be `reusable`. Don't try to make a meta-component.
- **`x`/`y` are ignored in flex children.** Only set them when the parent has `layout: "none"`.
- **`fill_container` requires a flex parent.** Setting it on a child of a `layout: "none"` parent has no effect.
- **Circular dependency:** a `fit_content` frame whose every direct child is `fill_container` produces unpredictable sizing. At least one child must have a fixed size or `fit_content`.
- **No `image` node type.** Images are fill objects (`fill: { type: "image", url: "..." }`) on `frame` or `rectangle` nodes. Use `G(nodeId, "ai", "prompt")` to generate AI images into an existing node.
- **Text needs `fill`** — text nodes have no default color. An unfilled text node renders invisible with no error.
