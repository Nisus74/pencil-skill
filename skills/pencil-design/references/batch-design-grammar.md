# `batch_design` op grammar

`batch_design` takes a single `input` string. Each line is one op. The server runs them top-to-bottom in order; later ops can reference ids bound earlier in the same call.

## The five ops

### `I`, Insert

Create a child of an existing parent.

```
foo=I("parent", { type: "frame", name: "Container", layout: "vertical", gap: "$space-4" })
```

- `parent` is an existing node id (from `get_editor_state` / `batch_get`, or bound earlier in this call). Use the predefined `document` binding to insert top-level frames: `foo=I(document, { type: "frame", ... })`.
- The `{ ... }` object is the new node's properties (no `id`, the server assigns one and returns it via the `foo=` binding).
- `foo` is the binding name. Use it in subsequent ops as the parent id of children.
- `layout` accepts only `"none"`, `"vertical"`, or `"horizontal"`. Default for frames is `"horizontal"`; default for groups is `"none"`. CSS flexbox words (`"flex"`, `"row"`, `"column"`, `"grid"`) are rejected and roll the call back.
- **Placeholder discipline:** every new, copied, or modified frame must carry `placeholder: true` for the entire duration of work on it. Remove the flag per-frame with `U(id, { placeholder: false })` as each frame is complete (not at the end of the whole task). Multi-screen work: set placeholders on every frame up-front before any content goes in.
- For `descendants` overrides inside a `ref` instance, the keys are slash-separated id paths, e.g. `descendants: { "button/icon": { iconFontName: "log-in" } }`. A descendant entry that includes `type` fully replaces that subtree; without `type`, it merges properties.

### `C`, Copy

Duplicate an existing node into a parent, with optional overrides.

```
btn2=C("PrimaryButton", "form", { x: 0, y: 80, descendants: { label: { content: "Sign up" } } })
```

- First arg: source node id (typically a `reusable` component or another node already on the canvas).
- Second arg: target parent id.
- Third arg: overrides applied to the copy.

### `R`, Replace

Full property replacement on an existing node.

```
R("heroTitle", { type: "text", content: "Welcome back", fontSize: "$text2xl", fontWeight: 700 })
```

- Wipes all current properties and applies the new object. Use sparingly, `U` is usually safer.

### `U`, Update

Partial property merge on an existing node.

```
U("heroTitle", { fontSize: "$text3xl" })
```

- Only the named properties change. Everything else stays.
- **Updating instance descendants:** once an instance is created, override its descendants via slash-path: `U(card+"/title", { content: "Account Details" })`. The same pattern works for `R` (full replacement of the descendant). Do **not** Update the descendants of a node you just **Copied** (`C`), copy generates fresh ids for the descendants; the old paths are stale and the update fails to find them. Use the new bindings returned by the C call instead.

### `G`, Generate (image)

Fill an existing image-bearing node with an AI-generated or stock image.

```
G("heroBg", "ai", "soft morning light through a kitchen window, photorealistic")
G("userAvatar", "unsplash", "smiling barista")
```

- Mode `"ai"` calls the model image pipeline. `"unsplash"` pulls a stock photo by query.
- Target node must already exist and accept an image fill (frame or rectangle).
- The node id must not contain `/`. Use actual node ids or bindings, not descendant paths.

## Two more ops you'll occasionally need

### `D`, Delete

```
D("legacyBanner")
```

Removes the node and its descendants.

### `M`, Move

```
M("loginButton", "form", 2)
```

Reparents `loginButton` under `form` at index `2`. Preserves the node's properties.

## Bindings: chain ops in one call

The `foo=I(...)` form is essential when a later op needs a parent you just created:

```
form=I("page", { type: "frame", name: "LoginForm", layout: "vertical", gap: "$space-4", padding: "$space-6" })
title=I(form, { type: "text", content: "Sign in", fontSize: "$text2xl" })
emailInput=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Email" } } })
passwordInput=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Password" } } })
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Sign in" } } })
```

- Bindings are scoped to the current `batch_design` call only. They don't persist.
- Don't reference a binding before it's been declared. Server reads top to bottom.
- A returned binding's id can also be used after the call completes, the server reports the assigned id back in the response.

## Chunking: ≤8 ops visual, ≤25 ops non-visual

Visual work caps at **≤8 ops per `batch_design` call** so each call advances visible state by an amount the user can take in with one screenshot. Non-visual sweeps (renames, `context` backfills, metadata-only updates) may go up to ≤25 ops, no further. Why:

- Larger calls have higher tail-latency.
- Ordering bugs are harder to spot in a 60-line block.
- Per-op error reporting is more useful when each call's blast radius is smaller.

For big screens, plan the order:

1. **Skeleton call:** page frame + main columns + sidebar + footer. Maybe 5-8 ops.
2. **Verify structurally** with `snapshot_layout(parentId: "<page>", maxDepth: 2)`, the geometry numbers tell you whether the skeleton landed without paying for a screenshot.
3. **Region calls:** one per substantial region (hero, form, list). Each ≤8 ops if visual, up to ≤25 ops for a non-visual sweep.
4. **Polish call:** final tweaks, after the main structure is solid.

## Hello world: the minimum first-chunk call

When you start work against the Pencil MCP for the first time in a session, or after a Pencil version update, or when a `batch_design` call rolls back with a confusing message and you want to confirm the basics are still working, run this two-op probe first:

```
page=I(document, { type: "frame", name: "SmokeTest", layout: "vertical", padding: 16, gap: 8, width: 1440, height: 900, placeholder: true })
hello=I(page, { type: "text", content: "Hello", fontSize: 24, fill: "#0F172A" })
```

In two ops it confirms: the `document` predefined binding works as a parent for inserts; `layout: "vertical"` is accepted (catches `"flex"` / `"row"` typos); `padding: 16` scalar form is accepted (catches `{ top: 16 }` object form); `text` nodes use `content` (catches `text:` / `value:` typos); `placeholder: true` is accepted on a new frame; raw hex `fill` is accepted on a text node (catches the "text has no colour by default" gotcha). If this call rolls back, the rest of the workflow will too; if it succeeds, the shape choices that matter most are confirmed before the real skeleton call. Delete with `D("<pageId>")` once you've verified.

## Common errors and their fixes

The **Fail mode** column reads `hard` (server returns an error and rolls back the whole call) or `silent` (the op succeeds, but the result is wrong, no error to read).

| Server error | Cause | Fix | Fail mode |
|--------------|-------|-----|-----------|
| `Can't find parent node with id '<x/y>'` (when referencing a previously-inserted node whose id contains `/`) | The server accepted the `/`-containing id on insert but cannot resolve it as a parent reference downstream | Don't include `/` in ids; let the server auto-generate. The `/` separator is meaningful only inside `descendants` path keys and inside `U(instance+"/childId", ...)` overrides. The insert succeeds silently; the downstream parent reference hard-errors. | silent → hard |
| `parent not found: <name>` | Referenced a binding before declaring it, or a parent that was never created | Reorder ops. Verify the binding name matches exactly. | hard |
| `/width expected one of: number, "$variable", sizing behavior (fit_content or fill_container, with optional fallback)` | Used `width: "100%"` or the old `{ sizing: "fill_container" }` object form | Use the bare-string form: `width: "fill_container"` or `width: "fit_content"`. With fallback: `"fill_container(320)"`. | hard |
| `unknown type: button` | Used a UI-framework word as a node type | There is no `button` node type. A button is a `frame` with `reusable: true`, or a `ref` to one. | hard |
| `expected variable, got string` | Passed `"#1F6FEB"` where the document declares a variable for that role | Use `"$primary"` (or whatever the variable is). Raw colours are accepted, but if the schema for that property requires a variable, the server enforces it. | hard |
| `slot frame must be empty in origin` | Tried to put children directly inside a slot frame in the component origin | Slots are filled at the instance level, not the origin. Move the contents out of the origin's slot frame. | hard |
| `/text unexpected property` | Used `text:` on a `text` node | The text content field is `content`, not `text`. Use `{ type: "text", content: "Hello" }`. | hard |
| `/padding expected number, [horizontal, vertical], or [top, right, bottom, left]` | Used `padding: { top: N, left: N, ... }` object form | Padding takes a number, a 2-element array `[horizontal, vertical]`, or a 4-element array `[top, right, bottom, left]`. Object form is rejected. | hard |
| `/paddingTop unexpected property` (or Left/Right/Bottom) | Used individual `paddingTop` / `paddingLeft` etc. | No individual padding properties. Only the combined `padding` array. | hard |
| `Node 'document' not found` on `U("document", ...)` | Tried to update document-level `themes`, `variables`, or `imports` via `U("document", ...)` | `U` on `document` is not supported. Tokens go through `set_variables` (themes auto-register from variable values). Imports currently have no documented MCP path, edit the `.pen` JSON directly. | hard |
| `/themes unexpected property` or `/imports unexpected property` on a frame `U` | Tried `U(<frameId>, { themes: ... })` or `U(<frameId>, { imports: ... })` | `themes` and `imports` are document-level only. They cannot be set via `U` on any frame. Use `set_variables` for themes; edit JSON for imports. | hard |
| `/fill[0].type expected one of: "color", "gradient", "image", "mesh_gradient"` | Used `type: "solid_color"` in a fill object | The correct type string is `"color"`, not `"solid_color"`. Use `{ type: "color", color: "$surface" }`. | hard |
| `/effect[0]/type expected one of: "blur", "background_blur", "shadow"` | Used `type: "drop_shadow"` in an effect | Type is `"shadow"`, with `shadowType: "inner"` or `"outer"`. Example: `{ type: "shadow", shadowType: "outer", offset: { x: 0, y: 4 }, blur: 8, color: "#00000033" }`. | hard |
| `/layout expected one of: "none", "vertical", "horizontal"` | Used CSS flexbox vocab (`"flex"`, `"row"`, `"column"`, `"grid"`) | Map `row → horizontal`, `column → vertical`. There is no `"flex"` or `"grid"` layout. | hard |
| `/alignItems expected one of: "start", "center", "end"` | Used `"stretch"` (the standard CSS flexbox value for "make children fill the cross axis") | Pencil rejects `"stretch"`. To make children span the cross axis, set `width: "fill_container"` (vertical parent) or `height: "fill_container"` (horizontal parent) on each child. The flex-prefixed aliases `"flex_start"` and `"flex_end"` are accepted; `"stretch"` is not. | hard |
| `/fill unexpected property` on a `note`, `prompt`, or `context` node | Annotation nodes accept TextStyle properties only, not graphics. Same applies to `stroke` and `effect`. | Remove the graphics property. Annotation nodes are non-rendering anyway; colour them with text-style properties (`fontFamily`, `fontSize`, `fontStyle`, `lineHeight`) only. If you need a coloured rendering, use a `text` node inside a regular `frame` (which does accept fills). | hard |
| Child appears at wrong position / x+y ignored | Set `x`/`y` on a child inside a flex parent | x/y are completely ignored when the parent has `layout: "vertical"` or `"horizontal"`. Remove x/y; use `gap`, `justifyContent`, `alignItems`, and `padding` on the parent instead. | silent |
| `/iconName unexpected property` or `/iconLibrary unexpected property` | Used `iconName`/`iconLibrary` on an `icon_font` node | Correct properties are `iconFontName` (icon name) and `iconFontFamily` (library: `"lucide"`, `"feather"`, etc.). Size the icon with `width`/`height`, not `fontSize`. | hard |
| Text node renders nothing visible | Set `width`/`height` on a `text` node with `textGrowth: "auto"` (the default) | `textGrowth: "auto"` always sizes the text node to its content and ignores any width/height you set. To wrap text, use `textGrowth: "fixed-width"` plus an explicit `width` (number, variable, or `"fill_container"` inside a flex parent). | silent |
| `Variable '<x>' does not have a valid definition` | Called `set_variables` with a bare value like `{ accent: "#FF0000" }` instead of `{ accent: { type: "color", value: "#FF0000" } }` | Wrap every variable value: `{ type: "color" \| "number" \| "string" \| "boolean", value: ... }`. Themed values use `value: [{ value, theme }, ...]`. | hard |

## Order-of-operations cheats

When a call mixes inserts and updates, put inserts first, then updates, so binding-resolution is unambiguous:

```
hero=I("page", { type: "frame", layout: "vertical", padding: "$space-8" })
title=I(hero, { type: "text", content: "Welcome", fontSize: "$text3xl" })
U(hero, { gap: "$space-4" })          // safe, `hero` is bound already
```

When you need to copy then tweak, do both, copy reads source props as of the start of the call:

```
copy=C("ButtonPrimary", "form")
U(copy, { backgroundColor: "$accent" })
```

When deleting and re-creating, delete first:

```
D("oldHero")
hero=I("page", { ...new shape... })
```

## Commonly built patterns: exact anatomy

Some frequently-built components are commonly built wrong, especially when the agent has absorbed a generic "bar chart" mental model from the Web App guidelines. These worked shapes override the generic defaults.

### KPI sparkline (mini trend line inside a metric card)

A sparkline is **not** a bar chart. Its bars are 3–4 px wide, not `fill_container`. A 60 px wide sparkline area with 12 bars at 3 px + 2 px gap uses the full width and reads as a trend indicator. A sparkline built with `fill_container` on the bars will make each bar 40–60 px wide (filling the parent) and look like a loading skeleton.

```
sparklineArea=I(kpiCard, {
  type: "frame", name: "Sparkline",
  context: "Mini trend, last 12 days. Each bar height encodes relative volume.",
  layout: "horizontal", alignItems: "flex_end", gap: 2,
  width: 60, height: 32
})
// Build each bar with an explicit pixel width, never fill_container.
// Heights vary to show the trend; vary them when building real data.
bar1=I(sparklineArea, { type: "frame", name: "Bar1", width: 3, height: 8,  fill: "$accent", cornerRadius: 1 })
bar2=I(sparklineArea, { type: "frame", name: "Bar2", width: 3, height: 12, fill: "$accent", cornerRadius: 1 })
bar3=I(sparklineArea, { type: "frame", name: "Bar3", width: 3, height: 10, fill: "$accent", cornerRadius: 1 })
bar4=I(sparklineArea, { type: "frame", name: "Bar4", width: 3, height: 20, fill: "$accent", cornerRadius: 1 })
bar5=I(sparklineArea, { type: "frame", name: "Bar5", width: 3, height: 16, fill: "$accent", cornerRadius: 1 })
bar6=I(sparklineArea, { type: "frame", name: "Bar6", width: 3, height: 24, fill: "$accent", cornerRadius: 1 })
bar7=I(sparklineArea, { type: "frame", name: "Bar7", width: 3, height: 18, fill: "$accent", cornerRadius: 1 })
bar8=I(sparklineArea, { type: "frame", name: "Bar8", width: 3, height: 28, fill: "$accent", cornerRadius: 1 })
bar9=I(sparklineArea, { type: "frame", name: "Bar9", width: 3, height: 22, fill: "$accent", cornerRadius: 1 })
bar10=I(sparklineArea, { type: "frame", name: "Bar10", width: 3, height: 32, fill: "$accent", cornerRadius: 1 })
```

Key rules:
- Parent: `layout: "horizontal"`, `alignItems: "flex_end"` (bars grow upward from the bottom), `gap: 2`, explicit `width`/`height` in px.
- Each bar: explicit `width: 3` (never `fill_container`), explicit height in px representing relative magnitude, `fill: "$accent"` (no gradients unless the user's direction explicitly calls for them), `cornerRadius: 1`.
- Vary heights across bars to show trend shape. Do not use equal heights, that's a loading bar.

### KPI metric card

```
kpiCard=I(statsRow, {
  type: "frame", name: "KPICard_TotalCalls",
  context: "Total API calls over selected period. Populated from /v1/stats/summary. Click navigates to Requests view.",
  layout: "vertical", gap: 8, padding: [16, 16, 12, 16],
  width: "fill_container", height: "fit_content",
  fill: "$surface",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 8
})
label=I(kpiCard, { type: "text", name: "MetricLabel", content: "Total API calls", fontSize: "$textSm", fill: "$textMuted" })
valueRow=I(kpiCard, { type: "frame", name: "ValueRow", layout: "horizontal", alignItems: "center", justifyContent: "space_between", width: "fill_container" })
value=I(valueRow, { type: "text", name: "MetricValue", content: "24.7M", fontSize: "$text2xl", fontWeight: 600, fill: "$textPrimary", fontFamily: "Geist Mono" })
delta=I(valueRow, { type: "text", name: "DeltaBadge", content: "+18%", fontSize: "$textXs", fill: "$success" })
// Sparkline goes in kpiCard, not valueRow
spark=I(kpiCard, { type: "frame", name: "Sparkline", layout: "horizontal", alignItems: "flex_end", gap: 2, width: 60, height: 24 })
```

For data-dense product surfaces: no shadow on the card. Use `stroke: { color: "$border", thickness: 1 }`. Remove any `effect: [{ type: "shadow", ... }]` if present (the type is `"shadow"`, not `"drop_shadow"`). The hairline border is the elevation signal; a shadow claims hierarchy the data card doesn't need.

Server-accepted aliases: `alignItems: "flex_end"` works, and `alignItems: "end"` (the canonical schema spec value) works too. Same pattern with `stroke: { color }` and `stroke: { fill }`, both are accepted.
## A complete small example

A login form, ~12 ops, in one call:

```
page=I(document, { type: "frame", name: "LoginPage", layout: "vertical", justifyContent: "center", alignItems: "center", padding: "$space-8", width: "fill_container", height: "fill_container" })
form=I(page, { type: "frame", name: "Form", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: [{ type: "color", color: "$surface" }] })
title=I(form, { type: "text", content: "Sign in", fontSize: "$text2xl", fontWeight: 700 })
sub=I(form, { type: "text", content: "Welcome back", fontSize: "$textBase", fill: [{ type: "color", color: "$textMuted" }] })
email=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Password" }, input: { type: "password" } } })
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Sign in" } } })
forgot=I(form, { type: "text", content: "Forgot password?", fontSize: "$textSm", href: "#", textAlign: "center" })
```

After the call, screenshot. If the form looks right, you're done. If not, iterate with `U` ops on the offending nodes.
