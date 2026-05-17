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
R("heroTitle", { type: "text", content: "Welcome back", fontSize: "$text2xl", fontWeight: "700" })
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

### The `document` predefined binding

`document` is a built-in binding that always resolves to the document root. Use it **only** when inserting top-level frames (screens, canvas-level containers):

```
page=I(document, { type: "frame", name: "LoginPage", width: 1440, height: 900 })
```

**Never name your own binding `document`** — it overwrites the predefined one and breaks all subsequent inserts into the root.

## Placeholder frames

**Every new top-level frame (screen) must carry `placeholder: true` for the entire duration you're building it.** The server uses this to signal to the editor that the frame is in-progress. Rules:

- Set `placeholder: true` in the same `I` op that creates the frame.
- You can update layout and size props on the placeholder frame while building its contents.
- Remove it — `U("frameId", { placeholder: false })` — as soon as the frame is finished. Don't wait until all screens are done.
- Do **not** set `placeholder: true` on inner content frames — only on top-level page frames.

```
page=I(document, { type: "frame", name: "LoginPage", width: 1440, height: 900, placeholder: true })
card=I(page, { type: "frame", name: "LoginCard", width: 440, layout: "vertical" })
// ... build contents ...
U("page", { placeholder: false })
```

## Sizing and layout constraints

These cause silent bugs or server errors if you get them wrong:

- **`fill_container` requires a flex parent.** A child set to `width: "fill_container"` does nothing if its parent has `layout: "none"` (absolute positioning). The parent must have `layout: "vertical"` or `"horizontal"`.
- **`fit_content` requires a flex node.** Same constraint — only meaningful on nodes with flex layout.
- **Circular dependency.** A frame sized `fit_content` (shrink to children) whose *all* direct children are `fill_container` (grow to parent) creates a circular dependency. The server resolves it unpredictably. Always have at least one child with a fixed size or `fit_content` sizing when the parent is `fit_content`.
- **`x`/`y` are ignored in flex children.** When a parent has `layout: "vertical"` or `"horizontal"`, child `x`/`y` values are completely ignored — position is determined by the parent's flex rules. Only set `x`/`y` on a child when its parent has `layout: "none"`.
- **Text is invisible without `fill`.** Text nodes have no default color. Always set `fill: "$textColor"` (or a raw hex) explicitly — omitting it produces an invisible node with no error.
- **There is no `image` node type.** Images are fills (`fill: { type: "image", url: "..." }`) applied to `frame` or `rectangle` nodes. To add an AI-generated image, create a frame first, then call `G(nodeId, "ai", "prompt")`.

## Chunking: the ≤25-ops rule

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

| Server error | Cause | Fix |
|--------------|-------|-----|
| `invalid id: contains '/'` | You set `id: "section/title"` | Pick an id with no slash. `descendants` paths are the only place `/` is meaningful. |
| `parent not found: <name>` | Referenced a binding before declaring it, or a parent that was never created | Reorder ops. Verify the binding name matches exactly. |
| `width expected one of: number, "$variable", sizing behavior (fit_content or fill_container...)` | Used `width: "100%"` OR the older `width: { sizing: "fill_container" }` object form | Use the bare-string form: `width: "fill_container"` or `width: "fit_content"`. With fallback, use the function-call form baked into the string: `"fill_container(320)"`. **Verified live (2026-05).** |
| `unknown type: button` | Used a UI-framework word as a node type | There is no `button` node type. A button is a `frame` with `reusable: true`, or a `ref` to one. |
| `expected variable, got string` | Passed `"#1F6FEB"` where the document declares a variable for that role | Use `"$primary"` (or whatever the variable is). Raw colors are accepted, but if the schema for that property requires a variable, the server enforces it. |
| `slot frame must be empty in origin` | Tried to put children directly inside a slot frame in the component origin | Slots are filled at the instance level, not the origin. Move the contents out of the origin's slot frame. |
| `unexpected property: paddingTop` (or `paddingLeft`, `paddingRight`, `paddingBottom`) | Used CSS-style individual padding shorthands | There are no `paddingTop` etc. properties. Use `padding: [top, right, bottom, left]` (4-value array). To add only top padding while keeping others at 0: `padding: [8, 0, 0, 0]`. If other sides already have values, read them first via `batch_get` before overwriting. |

## Order-of-operations cheats

When a call mixes inserts and updates, put inserts first, then updates, so binding-resolution is unambiguous:

```
hero=I("page", { type: "frame", layout: "vertical", padding: "$space-8" })
title=I(hero, { type: "text", content: "Welcome", fontSize: "$text3xl" })
U(hero, { gap: "$space-4" })          // safe — `hero` is bound already
```

When you need to copy then tweak, do both, copy reads source props as of the start of the call:

```
copy=C("ButtonPrimary", "form")
U(copy, { fill: "$accent" })
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
form=I(page, { type: "frame", name: "Form", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: "$surface" })
title=I(form, { type: "text", content: "Sign in", fontSize: "$text2xl", fontWeight: "700" })
sub=I(form, { type: "text", content: "Welcome back", fontSize: "$textBase", fill: "$textMuted" })
email=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Password" }, input: { type: "password" } } })
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Sign in" } } })
forgot=I(form, { type: "text", content: "Forgot password?", fontSize: "$textSm", href: "#", textGrowth: "fixed-width", width: "fill_container", textAlign: "center" })
```

After the call, verify structurally with `snapshot_layout(parentId: form, maxDepth: 2)`. Screenshot once as the final sign-off. If something looks off, iterate with `U` ops on the offending nodes.
