# Advanced canvas (schema 2.14)

The v2.14 `.pen` schema adds canvas capabilities beyond the primitive shapes: shader and mesh-gradient
fills, `script` nodes that generate children from JavaScript, ellipse arcs and donuts, and the
non-rendering `prompt`/`context` node types. This reference shows each with a worked `batch_design`
snippet. The op API itself is in [`batch-design-grammar.md`](batch-design-grammar.md); the full property
list is in [`pen-schema.md`](pen-schema.md).

Use these when the design genuinely calls for them. Most product UI is still primitives plus components,
reach for a shader or a script when a gradient mesh, a generative texture, or a parameterised layout is
the actual requirement, not as decoration. A shader background on a settings page is the new
glassmorphism.

## Mesh gradient fills

A `mesh_gradient` is a bezier-interpolated grid of colours, richer and softer than a linear/radial
gradient. Set it as a `fill`. Both `colors` and `points` are listed row-major (`columns × rows`).
Verified live.

```
hero = Insert(page, { type: "rectangle", name: "MeshHero", width: "fill_container", height: 360, cornerRadius: 16 })
Update(hero, { fill: { type: "mesh_gradient", columns: 2, rows: 2,
  colors: ["$brand1", "$brand2", "$brand2", "$brand3"],
  points: [[0, 0], [1, 0], [0, 1], [1, 1]] } })
```

- `columns × rows` must equal the length of both `colors` and `points`. A 2×2 is the simplest useful mesh.
- **`points` is required.** Each is a `[x, y]` vertex in `[0,1]` space, row-major. Omitting it makes the
  server **silently drop the whole fill** (the call still succeeds, but the node ends up with no fill and
  renders blank, verified live). Keep the edge vertices at the corners (`0`/`1`); for `columns`/`rows`
  greater than 2 the interior vertices sit between, e.g. a 3×3 centre at `[0.5, 0.5]`. A vertex may also
  be an object with bezier handles (`{ position, leftHandle, rightHandle, topHandle, bottomHandle }`) for
  a warped mesh; plain `[x, y]` pairs are enough for an even grid.
- Colours accept hex or `$variable` references, so a mesh can be theme-aware.
- Optional `opacity` and `blendMode` like any fill.

When to use: a soft branded hero or section background, an auth-screen backdrop, an empty-state canvas.
When not to: behind text-dense UI (it fights legibility) or on data surfaces.

## Shader fills

A `shader` fill runs a WebGL 1.0 fragment shader (`#version 100`) stored in a `.glsl` file referenced by
URL, relative to the `.pen`. Uniforms are described by `@directive` annotations inside block comments in
the shader source; user-set values go in the fill's `uniforms` map.

```glsl
/** @resolution */
uniform vec2 u_resolution;

/** @label Cell Size @range 8, 64 @default 32 */
uniform float u_size;

/** @label Primary @color @default #6366F1 */
uniform vec3 u_color1;

/** @label Secondary @color @default #0EA5E9 */
uniform vec3 u_color2;

void main() {
  vec2 cell = floor(gl_FragCoord.xy / u_size);
  float check = mod(cell.x + cell.y, 2.0);
  gl_FragColor = vec4(mix(u_color1, u_color2, check), 1.0);
}
```

```
panel = Insert(page, { type: "rectangle", name: "ShaderPanel", width: "fill_container", height: 320 })
Update(panel, { fill: { type: "shader", url: "./shaders/checker.glsl", uniforms: { u_size: 24, u_color1: "#6366F1", u_color2: "#0EA5E9" } } })
```

Uniform support and annotations:

- **Types:** `float`/`int` as numbers; `vec2/3/4`, `ivec2/3/4` as number arrays or `"#RRGGBB"` colour
  strings; `sampler2D` as an image-URL string. A numeric uniform may bind a `$number` variable; a colour
  uniform may bind a `$color` variable.
- **`@resolution`** auto-binds a `vec2` to the fill size in pixels. **`@time`** auto-binds elapsed seconds
  (animation). **`@mouse`** binds the pointer in `gl_FragCoord` space. Uniforms annotated `@resolution`
  or `@time` must **not** appear in the `uniforms` map, the runtime supplies them.
- **`@sdf`** binds a `sampler2D` to a signed-distance texture of the node's shape (`r` = signed distance
  in `@resolution` units, positive inside; `gb` = gradient direction). Use `gb` rather than numerically
  differentiating `r`.
- **`@color`** shows a colour picker for a `vec3`/`vec4`. **`@default`** sets the default. **`@min`/`@max`**
  or **`@range <min>, <max>`** bound a numeric uniform (range shows a slider). **`@label <text>`** sets the
  UI name, always set it.
- `textureSize(sampler, lod)` is available (the one addition over stock WebGL 1.0) for aspect-correct
  texturing.

The shader file must exist on disk at the referenced path before the fill renders. When you author a
shader, write the `.glsl` alongside the `.pen` and point `url` at it.

When to use: a deliberate generative/animated background, a noise or gradient texture the gradient types
can't express, an interactive hero. When not to: anything a `mesh_gradient` or plain gradient already
covers, shaders cost GPU and complexity.

## Ellipse arcs, donuts, and gauges

`ellipse` carries three arc properties (all verified live):

- `innerRadius` (0 = solid disc, 1 = hollow ring; a donut sits around `0.6`).
- `startAngle` (degrees counter-clockwise from the 3 o'clock position; default 0).
- `sweepAngle` (arc length; positive = counter-clockwise, negative = clockwise; range -360..360; default 360).

A donut-chart segment, two ops:

```
track = Insert(card, { type: "ellipse", name: "DonutTrack", width: 120, height: 120, innerRadius: 0.7, fill: "$surfaceMuted" })
value = Insert(card, { type: "ellipse", name: "DonutValue", width: 120, height: 120, innerRadius: 0.7, startAngle: 90, sweepAngle: -252, fill: "$accent", layoutPosition: "absolute", x: 0, y: 0 })
```

`-252` is 70% of a full turn clockwise from 12 o'clock (`360 × 0.7 = 252`). For a gauge, sweep a partial
arc (e.g. `startAngle: 180, sweepAngle: -180` for a half-circle) and overlay a value arc the same way.
Stack the value ellipse over the track with `layoutPosition: "absolute"` and matching `x`/`y`.

For multi-segment donuts, this manual angle maths gets fiddly fast, that is a good case for a `script`
node (below) that computes each segment's `startAngle`/`sweepAngle` from a data array.

## Script nodes

A `script` node points at a `.js` file whose returned nodes render as its children, recomputed when its
inputs change. The file declares typed inputs; the node supplies their values.

```js
/**
 * @schema 2.11
 * @input rows: number = 3
 * @input gap: number = 4
 * @input color: color = #6366F1
 */
const rows = Math.max(1, Math.floor(pencil.input.rows));
const cellH = (pencil.height - pencil.input.gap * (rows - 1)) / rows;
const nodes = [];
for (let r = 0; r < rows; r++) {
  nodes.push({
    type: "rectangle",
    name: "Bar " + (r + 1),
    x: 0,
    y: r * (cellH + pencil.input.gap),
    width: pencil.width * (0.4 + 0.6 * Math.random()),
    height: cellH,
    fill: pencil.input.color
  });
}
return nodes;
```

```
chart = Insert(page, { type: "script", name: "GeneratedBars", scriptUri: "./generators/bars.js", width: 600, height: 240, inputs: { rows: 8, gap: 6, color: "#6366F1" } })
```

Rules:

- First line must be `/** @schema 2.11 */` (current version). Missing the tag is an error.
- The script receives a `pencil` object: `pencil.width`, `pencil.height`, `pencil.input.<name>`.
- It must `return` an array of node objects following the `.pen` schema.
- Declare inputs with `@input name: type [= default]`. Types: `number`, `string`, `boolean`, `color`,
  `ref`, `enum("a","b",...)`.
- `Math.random()` is **deterministic** in scripts, so generated output is stable across renders, safe for
  procedural content (scatter, generated cells, varied bar heights).
- The `.js` file must exist on disk at `scriptUri`, relative to the `.pen`.

When to use: a layout parameterised by a runtime input (configurable grid, data-driven chart), or
procedural content you would otherwise hand-place. When not to: anything you would otherwise build with a
handful of primitives, a flat node tree is far easier to read, screenshot, and debug than a generator.

## Prompt and context nodes

Two intent-carrying node types. They carry `content` plus TextStyle and accept **no**
`fill`/`stroke`/`effect`. Unlike a `note` (which never renders), they show on the canvas as small
collapsible labelled chips ("Prompt ⌄", "Context ⌄") that surface their content to editors and agents,
verified live, so they *do* appear in a screenshot, but they carry no visual styling and are part of the
intent layer, not the visual layout.

- **`prompt`** records an AI operation by name, with an optional `model` (the target LLM). Use it where a
  design captures a generative step ("summarise these comments", "draft three headline options") so the
  downstream agent or engineer knows an LLM call belongs there.
- **`context`** is a standalone, region-level context note, the canvas analogue of the Entity `context`
  field, for when the context applies to an area rather than one node.

```
Insert(section, { type: "prompt", name: "HeadlinePrompt", content: "Generate 3 headline options for this hero, <=8 words, active voice.", model: "claude-opus-4-8", width: 280 })
Insert(section, { type: "context", name: "RegionContext", content: "This block renders only for enterprise plans; copy is owned by marketing.", width: 280 })
```

Position them beside the design like `note` annotations. They are part of the deliverable's intent layer,
not its visual layer.

## See also

- [`batch-design-grammar.md`](batch-design-grammar.md), the `batch_design` JavaScript API.
- [`pen-schema.md`](pen-schema.md), full property definitions for fills, ellipse, `script`, `prompt`, `context`.
- [`data-viz.md`](data-viz.md), chart selection and palettes (the donut/gauge belongs to a broader chart system).
