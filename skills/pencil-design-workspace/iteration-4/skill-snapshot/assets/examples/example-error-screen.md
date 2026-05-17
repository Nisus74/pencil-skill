# Example: design a 404 + offline pair

A worked walkthrough of the seven-step workflow for the prompt:

> *"Design a 404 page and an offline screen for our web app."*

Assume: Pencil desktop running, a `.pen` already open with a populated canvas, repo has a `design-system/` folder with `tokens.md` and a `design/system.lib.pen` library that includes `ButtonPrimary` and `LinkText` but no dedicated `ErrorBlock` component yet.

This example exercises:

- `get_variables` and `set_variables` to confirm and add a missing token.
- Sibling top-level frames sharing one new `ErrorBlock` reusable.
- `find_empty_space_on_canvas` to place the new frames without overlapping existing work.
- `snapshot_layout` for structural verification, one screenshot per page for final sign-off.
- Cross-references: [`references/states.md`](../../references/states.md) for the screen-level state taxonomy and the lockup; [`assets/design-system/voice.md`](../design-system/voice.md) for copy.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Result: succeeds. Active document is `./design/screens.pen`. No selection. The canvas already has `LoginPage` and `DashboardPage` as top-level frames.

## Step 2 — Locate context

- `screens.pen` is open.
- No selection.
- `design-system/` exists with `README.md`, `tokens.md`, `voice.md`, `components.md`, `patterns.md`, `states.md`.

## Step 3 — Load guidelines + inventory components

Read `design-system/README.md`, then `design-system/states.md` (the project's state coverage contract), `design-system/voice.md` (for empty-state and error copy templates), and `design-system/patterns.md` (which has an Empty state lockup that 404 / offline can adapt). The skill's own [`references/states.md`](../../references/states.md) is the playbook for screen-level fault states.

Call `get_guidelines()` to confirm the live category list, then load `Web App` for product-error patterns.

Inventory components:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Library contains `ButtonPrimary`, `ButtonSecondary`, `LinkText`, `Input`, `Card`. **No `ErrorBlock` yet.** That's the right place to put the shared lockup — but build it as a regular frame for now and flag it. Promotion to library is a user-owned decision (per `components.md` § "When the right component doesn't exist").

## Step 4 — Plan (told to user)

> *"I'll add two sibling top-level frames at desktop breakpoint (1440×900): `Page_404` and `Page_Offline`. Both use the same lockup — a centered icon, title, description, and primary CTA — built as a single frame I'll copy with overrides for each page. The 404 uses `alert-circle`, copy *'This page doesn't exist'* and a CTA back to the dashboard. The offline page uses `cloud-off`, copy *'You're offline'* and a Retry CTA. Both bind colors to your `tokens.md` variables and inherit the `mode` theme axis you already have. I'll add a `$illustration` color token if it isn't already declared so the icon color is centrally controlled."*

## Step 4.5 — Verify the token suite

The plan mentioned `$illustration`. Confirm before binding:

```
get_variables()
```

Returns the doc's variables. `$textMuted`, `$danger`, `$primary`, etc. are present. `$illustration` is **not** declared. Add it:

```
set_variables({
  variables: {
    illustration: { type: "color", value: [
      { value: "#A1A1AA", theme: { mode: "light" } },
      { value: "#52525B", theme: { mode: "dark"  } }
    ] }
  },
  replace: false
})
```

Now the icon color is theme-aware and centrally controllable.

## Step 4.7 — Place the new frames in empty canvas

Existing top-level frames occupy part of the canvas. To avoid overlap:

```
find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })
```

Returns coordinates — call them `(x404, y404)`. Place `Page_404` there. After it lands, find space for `Page_Offline` immediately below or to the right.

## Step 5 — First batch_design (404 page + shared lockup)

```
page404=I("doc", { type: "frame", name: "Page_404", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x404>, y: <y404>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "solid_color", color: "$surface" }] })
block=I(page404, { type: "frame", name: "ErrorBlock", layout: "vertical", justifyContent: "center", alignItems: "center", gap: "$space-5", padding: "$space-8", width: 480 })
icon=I(block, { type: "icon_font", name: "ErrorIcon", iconName: "alert-circle", iconLibrary: "lucide", fontSize: 64, fill: [{ type: "solid_color", color: "$illustration" }] })
title=I(block, { type: "text", name: "Title", text: "This page doesn't exist.", fontSize: "$text2xl", fontWeight: 700, textAlign: "center", fill: [{ type: "solid_color", color: "$textPrimary" }] })
desc=I(block, { type: "text", name: "Description", text: "The link may be broken, or the page may have moved. Head back to the dashboard.", fontSize: "$textBase", textAlign: "center", fill: [{ type: "solid_color", color: "$textMuted" }] })
cta=I(block, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Go to dashboard" } } })
code=I(block, { type: "text", name: "ErrorCode", text: "404", fontSize: "$textXs", textAlign: "center", fill: [{ type: "solid_color", color: "$textMuted" }] })
```

7 ops — well under 25. Note the `name` and `context` discipline: `Page_404`, `ErrorBlock`, `ErrorIcon`, `Title`, `Description`, `ErrorCode`. No `Frame 1` defaults.

## Step 6a — Verify structure (404)

```
snapshot_layout({ parentId: "page404", maxDepth: 2 })
```

Check: `block` is centered (`x` close to `(1440 - 480) / 2 = 480`, `y` close to centered vertical). Gaps between block children match `$space-5` (24px). Title and description render at expected widths. No overflow.

If something's off (often: title or description text grew taller than expected because they're long-strings), it's structural and fixed with a `U` op:

```
U("desc", { width: 480 })   // explicit width forces wrap
```

Don't screenshot to confirm structure — `snapshot_layout` is enough.

## Step 7a — Final visual sign-off (404)

```
get_screenshot({ nodeId: "page404" })
```

One screenshot, scoped to the page (not the doc root). Confirm:

- Icon color reads as `$illustration` against `$surface`.
- Title contrasts against the background (≥ 4.5:1 — verify in both modes if any of the colors had raw hex; since we used variables, mode parity is guaranteed by the variable system).
- The button's primary fill is correct.
- The error code is visible but de-emphasized.

If clean, move to the offline page.

## Step 5b — Second batch_design (Offline page, copying the ErrorBlock)

The lockup is the same. Use `C` (copy) with `descendants` overrides:

```
pageOffline=I("doc", { type: "frame", name: "Page_Offline", layout: "vertical", justifyContent: "center", alignItems: "center", x: <xOffline>, y: <yOffline>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "solid_color", color: "$surface" }] })
blockCopy=C(block, pageOffline, { descendants: {
  ErrorIcon:    { iconName: "cloud-off" },
  Title:        { text: "You're offline." },
  Description:  { text: "We can't reach the server. Check your connection and try again." },
  ErrorCode:    { text: "" },
  /* The CTA stays a ButtonPrimary ref, but we override the label */
} })
```

Wait — the CTA needs to change from *"Go to dashboard"* to *"Try again"*. The label override goes through the nested `ButtonPrimary` ref's `descendants`. The Pencil schema supports nested descendants paths; the cleaner approach is a follow-up `U` op on the copied CTA's id:

```
U(`${blockCopy}/cta`, { descendants: { label: { text: "Try again" } } })
```

(The `${blockCopy}/cta` syntax assumes the copy preserves the original child id `cta`; if the schema reassigns ids on copy, fall back to a `batch_get` to resolve, then `U`.)

Also clear the error-code text since offline isn't an HTTP code:

```
U(`${blockCopy}/code`, { text: "" })
```

Or just suppress visibility:

```
U(`${blockCopy}/code`, { enabled: false })
```

## Step 6b — Verify structure (offline)

```
snapshot_layout({ parentId: "pageOffline", maxDepth: 2 })
```

Confirm the layout matches the 404 page. Same block dimensions, same internal spacing, same centered block. The copy override didn't shift anything structurally.

## Step 7b — Final visual sign-off (offline)

```
get_screenshot({ nodeId: "pageOffline" })
```

Confirm:

- The `cloud-off` icon renders correctly.
- The new copy fits the block width without truncation.
- The CTA label is *"Try again"*.
- Error code area is hidden (no leftover ghost).

Two screenshots total across both pages, each scoped to its page.

## Step 8 — Surface the missing component

The lockup is now used twice. Surface it as a `.lib.pen` candidate:

> *"The two pages share the same lockup — `ErrorBlock` (icon, title, description, CTA, optional error code). It's living inside `Page_404` right now and copied into `Page_Offline`. Want me to promote it to your `design/system.lib.pen` so any future error pages can `ref` it directly?"*

If yes, mark the `block` node `reusable: true` and the user copies it into the library on their next save (or the agent does it via a `batch_design` `U` op on the `block` node, then re-references both pages with `ref` instead of containing the lockup directly). If no, leave as-is — two-instance duplication is a fair cost for not over-engineering the library.

## Final report to user

> *"Done. Two new pages — `Page_404` and `Page_Offline` — at desktop dimensions, placed in empty canvas to the right of your existing screens. Both use a shared `ErrorBlock` lockup (icon, title, description, CTA, optional error code) bound to your `$illustration`, `$textPrimary`, `$textMuted`, and `$surface` tokens — I added `$illustration` since it wasn't declared. Verified structurally with `snapshot_layout`, then one screenshot per page for sign-off. The `ErrorBlock` is currently embedded — let me know if you want it promoted to your `.lib.pen`."*

## What this example demonstrates

- **`get_variables` before binding tokens you're not sure exist;** `set_variables` to add the missing one in a single call.
- **Sibling top-level frames** sharing one lockup, copied with descendants overrides — the canonical pattern for "a family of variants on the same shape" (404, 403, 500, offline all fit the same lockup).
- **`find_empty_space_on_canvas`** before placing on a populated canvas — avoids invisible overlaps with existing work.
- **One screenshot per final page**, scoped to the page node, never the doc root.
- **Surface candidates for the library** but don't promote unilaterally — that's a user-owned decision.
- **Cross-reference the right files**: `references/states.md` for the screen-state taxonomy, `voice.md` for copy, `tokens.md` for the variables. Don't restate them; link.

For the empty-state taxonomy and the full screen-level error matrix this example draws on, see [`references/states.md`](../../references/states.md). For the copy template (the *"what happened. what to do."* shape), see [`voice.md`](../design-system/voice.md) § Error messages.
