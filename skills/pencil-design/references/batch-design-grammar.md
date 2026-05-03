# `batch_design` op grammar

`batch_design` takes a single `operations` string. Each line is one op. The server runs them top-to-bottom in order; later ops can reference ids bound earlier in the same call.

## The five ops

### `I` — Insert

Create a child of an existing parent.

```
foo=I("parent", { type: "frame", name: "Container", layout: "vertical", gap: "$space-4" })
```

- `parent` is an existing node id (from `get_editor_state` / `batch_get`, or bound earlier in this call).
- The `{ ... }` object is the new node's properties (no `id` — the server assigns one and returns it via the `foo=` binding).
- `foo` is the binding name. Use it in subsequent ops as the parent id of children.

### `C` — Copy

Duplicate an existing node into a parent, with optional overrides.

```
btn2=C("PrimaryButton", "form", { x: 0, y: 80, descendants: { label: { text: "Sign up" } } })
```

- First arg: source node id (typically a `reusable` component or another node already on the canvas).
- Second arg: target parent id.
- Third arg: overrides applied to the copy.

### `R` — Replace

Full property replacement on an existing node.

```
R("heroTitle", { type: "text", text: "Welcome back", fontSize: "$text2xl", fontWeight: 700 })
```

- Wipes all current properties and applies the new object. Use sparingly — `U` is usually safer.

### `U` — Update

Partial property merge on an existing node.

```
U("heroTitle", { fontSize: "$text3xl" })
```

- Only the named properties change. Everything else stays.

### `G` — Generate (image)

Fill an existing image-bearing node with an AI-generated or stock image.

```
G("hero/photo", "ai", "soft morning light through a kitchen window, photorealistic")
G("avatar/photo", "unsplash", "smiling barista")
```

- Mode `"ai"` calls the model image pipeline. `"unsplash"` pulls a stock photo by query.
- Target node should already exist with type that accepts an image fill.

## Two more ops you'll occasionally need

### `D` — Delete

```
D("legacyBanner")
```

Removes the node and its descendants.

### `M` — Move

```
M("loginButton", "form", 2)
```

Reparents `loginButton` under `form` at index `2`. Preserves the node's properties.

## Bindings: chain ops in one call

The `foo=I(...)` form is essential when a later op needs a parent you just created:

```
form=I("page", { type: "frame", name: "LoginForm", layout: "vertical", gap: "$space-4", padding: "$space-6" })
title=I(form, { type: "text", text: "Sign in", fontSize: "$text2xl" })
emailInput=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Email" } } })
passwordInput=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Password" } } })
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Sign in" } } })
```

- Bindings are scoped to the current `batch_design` call only. They don't persist.
- Don't reference a binding before it's been declared. Server reads top to bottom.
- A returned binding's id can also be used after the call completes — the server reports the assigned id back in the response.

## Chunking: the ≤25-ops rule

A single call should stay at or under 25 ops. Why:

- Larger calls have higher tail-latency.
- Ordering bugs are harder to spot in a 60-line block.
- Per-op error reporting is more useful when each call's blast radius is smaller.

For big screens, plan the order:

1. **Skeleton call:** page frame + main columns + sidebar + footer. Maybe 5-10 ops.
2. **Verify** with `get_screenshot()` — page geometry should look right.
3. **Region calls:** one per substantial region (hero, form, list). Each ≤25 ops.
4. **Polish call:** final tweaks, after the main structure is solid.

## Common errors and their fixes

| Server error | Cause | Fix |
|--------------|-------|-----|
| `invalid id: contains '/'` | You set `id: "section/title"` | Pick an id with no slash. `descendants` paths are the only place `/` is meaningful. |
| `parent not found: <name>` | Referenced a binding before declaring it, or a parent that was never created | Reorder ops. Verify the binding name matches exactly. |
| `width expected one of: number, "$variable", sizing behavior (fit_content or fill_container...)` | Used `width: "100%"` OR the older `width: { sizing: "fill_container" }` object form | Use the bare-string form: `width: "fill_container"` or `width: "fit_content"`. With fallback, use the function-call form baked into the string: `"fill_container(320)"`. **Verified live (2026-05).** |
| `unknown type: button` | Used a UI-framework word as a node type | There is no `button` node type. A button is a `frame` with `reusable: true`, or a `ref` to one. |
| `expected variable, got string` | Passed `"#1F6FEB"` where the document declares a variable for that role | Use `"$primary"` (or whatever the variable is). Raw colors are accepted, but if the schema for that property requires a variable, the server enforces it. |
| `slot frame must be empty in origin` | Tried to put children directly inside a slot frame in the component origin | Slots are filled at the instance level, not the origin. Move the contents out of the origin's slot frame. |

## Order-of-operations cheats

When a call mixes inserts and updates, put inserts first, then updates, so binding-resolution is unambiguous:

```
hero=I("page", { type: "frame", layout: "vertical", padding: "$space-8" })
title=I(hero, { type: "text", text: "Welcome", fontSize: "$text3xl" })
U(hero, { gap: "$space-4" })          // safe — `hero` is bound already
```

When you need to copy then tweak, do both — copy reads source props as of the start of the call:

```
copy=C("ButtonPrimary", "form")
U(copy, { backgroundColor: "$accent" })
```

When deleting and re-creating, delete first:

```
D("oldHero")
hero=I("page", { ...new shape... })
```

## A complete small example

A login form, ~12 ops, in one call:

```
page=I("doc", { type: "frame", name: "LoginPage", layout: "vertical", justifyContent: "center", alignItems: "center", padding: "$space-8", width: "fill_container", height: "fill_container" })
form=I(page, { type: "frame", name: "Form", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: [{ type: "solid_color", color: "$surface" }] })
title=I(form, { type: "text", text: "Sign in", fontSize: "$text2xl", fontWeight: 700 })
sub=I(form, { type: "text", text: "Welcome back", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
email=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Password" }, input: { type: "password" } } })
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Sign in" } } })
forgot=I(form, { type: "text", text: "Forgot password?", fontSize: "$textSm", href: "#", textAlign: "center" })
```

After the call, screenshot. If the form looks right, you're done. If not, iterate with `U` ops on the offending nodes.
