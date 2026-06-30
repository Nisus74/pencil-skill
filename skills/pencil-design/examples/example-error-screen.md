# Example: design a 404 + offline pair

A worked walkthrough of the seven-step workflow for the prompt:

> *"Design a 404 page and an offline screen for our web app."*

Assume: Pencil desktop running, a `.pen` already open with a populated canvas, and a `design/system.lib.pen` library that includes `ButtonPrimary` and `LinkText` but no dedicated `ErrorBlock` component yet.

---

## Step 1: Detect host

```
get_editor_state({ include_schema: false })
```

Result: succeeds. Active document is `./design/screens.pen`. No selection. The canvas already has `LoginPage` and `DashboardPage` as top-level frames.

## Step 2: Understand aesthetic direction

Existing screens (`LoginPage`, `DashboardPage`) already on the canvas. The error pages belong to the same product shell. Load `references/states.md` — it owns the screen-level fault state taxonomy and the empty-state taxonomy, which 404 and offline both need.

Announced direction: *"match the existing product shell — plain `$surface` background, muted grey icon (not danger red), de-emphasised error code, calm copy."*

## Step 3: Load guidelines + inventory components

Call `get_guidelines()`, then load `Web App`. The skill's own [`references/states.md`](../references/states.md) is the playbook for screen-level fault states.

Call `get_guidelines()` to confirm the live category list, then load `Web App`.

Inventory components:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Library contains `ButtonPrimary`, `ButtonSecondary`, `LinkText`, `Input`, `Card`. No `ErrorBlock` yet. Build it as a regular frame for now and flag it at the end. Promotion to library is a user-owned decision.

## Step 4: Plan

> *"I'll add two sibling frames at 1440×900: `Page_404` and `Page_Offline`. Both use the same centred lockup: icon, title, description, CTA, and a small de-emphasised error code. I'll add a `$illustration` colour token if it isn't declared. Direction: error icons in muted grey, not danger red — these are navigational dead ends, not emergencies."*

## Step 4.5: Verify the token suite

The plan mentions `$illustration`. Confirm before binding:

```
get_variables()
```

Returns the doc's variables. `$textMuted`, `$danger`, `$primary` are present. `$illustration` is **not** declared. Add it:

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

The icon colour is now theme-aware and centrally controllable.

## Step 4.7: Place the new frames in empty canvas

Existing frames occupy part of the canvas. To avoid overlap:

```
find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })
```

Returns coordinates `(x404, y404)`. Place `Page_404` there. Find space for `Page_Offline` immediately to the right or below.

## Step 5: First batch_design (404 page + shared lockup)

```
page404=I("doc", { type: "frame", name: "Page_404", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x404>, y: <y404>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "color", color: "$surface" }] })
block=I(page404, { type: "frame", name: "ErrorBlock", layout: "vertical", justifyContent: "center", alignItems: "center", gap: "$space-5", padding: "$space-8", width: 480 })
icon=I(block, { type: "icon_font", name: "ErrorIcon", iconFontName: "circle-alert", iconFontFamily: "lucide", width: 64, height: 64, fill: [{ type: "color", color: "$illustration" }] })
title=I(block, { type: "text", name: "Title", content: "This page doesn't exist.", fontSize: "$text2xl", fontWeight: 700, textAlign: "center", fill: [{ type: "color", color: "$textPrimary" }] })
desc=I(block, { type: "text", name: "Description", content: "The link may be broken, or the page may have moved. Head back to the dashboard.", fontSize: "$textBase", textAlign: "center", fill: [{ type: "color", color: "$textMuted" }] })
cta=I(block, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Go to dashboard" } } })
code=I(block, { type: "text", name: "ErrorCode", content: "404", fontSize: "$textXs", textAlign: "center", fill: [{ type: "color", color: "$textMuted" }] })
```

7 ops.

## Step 6a: Screenshot and verify structure (404)

```
snapshot_layout({ parentId: "page404", maxDepth: 2 })
get_screenshot({ nodeId: "page404" })
```

Narrate:

> *"404 page on canvas. Direction match: centred block with muted grey icon, plain `$surface` background — calm, not alarming. Two non-obvious decisions. First: the icon is `$illustration` (muted grey), not `$danger` (red). Error pages in `$danger` look like alerts requiring immediate action. This page is a navigational dead end, not an emergency. `$illustration` says 'contextual' not 'urgent'. The generic default puts the icon in `$primary` or `$danger`; both are wrong. Second: the HTTP code '404' is `$textXs` at the bottom, not a large headline. The code is developer metadata. Users don't know what 404 means; what they need is the copy. Showing '404' prominently makes the error number the headline, not the resolution instruction. Drift signal: no shadow on the block. Good."*

If the title or description text grows beyond the block width, fix with an explicit width:

```
U("desc", { width: 480 })   // forces wrap within the block
```

## Step 5b: Second batch_design (offline page, copying the ErrorBlock)

The lockup is identical. Use `C` (copy) with descendants overrides:

```
pageOffline=I("doc", { type: "frame", name: "Page_Offline", layout: "vertical", justifyContent: "center", alignItems: "center", x: <xOffline>, y: <yOffline>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "color", color: "$surface" }] })
blockCopy=C(block, pageOffline, { descendants: {
  ErrorIcon:    { iconFontName: "cloud-off" },
  Title:        { content: "You're offline." },
  Description:  { content: "We can't reach the server. Check your connection and try again." },
  ErrorCode:    { content: "" }
} })
```

The CTA label needs changing too. If the copy preserves child ids on copy:

```
U(`${blockCopy}/cta`, { descendants: { label: { content: "Try again" } } })
```

If not, resolve via `batch_get` first, then `U`.

## Step 6b: Verify structure (offline)

```
snapshot_layout({ parentId: "pageOffline", maxDepth: 2 })
get_screenshot({ nodeId: "pageOffline" })
```

Narrate:

> *"Offline page on canvas. Same lockup as 404, different icon (`cloud-off`) and copy. Non-obvious decision: copying the lockup rather than building it fresh. Structurally, 404 and offline are the same communication problem: 'we can't show you what you asked for.' The only differences are the icon and the copy. Separate lockups would diverge over time. Shared lockup means any future refinement (spacing, icon size, CTA placement) applies to both pages at once."*

Two screenshots total, each scoped to its page.

## Step 8: Surface the missing component

The lockup is now used on two pages. Surface it:

> *"The two pages share the same lockup: `ErrorBlock` (icon, title, description, CTA, optional error code). It's inside `Page_404` right now and copied into `Page_Offline`. Want me to promote it to your `design/system.lib.pen` so future error pages can reference it directly? A 403, a 500, a maintenance page all use the same shape."*

If yes: mark the `block` node `reusable: true`. If no: leave as-is. Two-instance duplication is a fair cost; the user decides when the overhead of promoting to library is worth it.

## Final report to user

> *"Done. Two new pages (`Page_404` and `Page_Offline`) at desktop dimensions, placed in empty canvas to the right of your existing screens. Both use a shared `ErrorBlock` lockup (icon, title, description, CTA, error code). I added `$illustration` since it wasn't in your token suite: muted grey in light mode, slightly darker in dark. The icon is `$illustration`, not `$danger`; these are navigational dead ends, not alerts. Error code '404' is de-emphasised at `$textXs`. `ErrorBlock` is currently embedded; let me know if you want it promoted to your `.lib.pen`."*

---

## What this example demonstrates

- **`$illustration` for contextual icons, not `$danger`.** Error page icons in danger-red look like alerts requiring immediate action. A 404 page is a navigational dead end, not an emergency. `$illustration` (muted grey) signals "contextual information" rather than "urgent problem." The generic default puts error icons in `$primary` or `$danger`; both import the wrong urgency register into a dead-end page.

- **Error code de-emphasised, copy primary.** The HTTP code is developer metadata. At `$textXs` with `$textMuted` fill, it's present for debugging purposes without claiming visual priority. The user's primary need is the copy; the developer's secondary need is the code. Both are served by the size and colour hierarchy.

- **Shared lockup for structurally identical problems.** 404 and offline are the same design problem: "we can't show you what you asked for." Separate lockups for each would require double maintenance for what is the same pattern. Copy-with-overrides encodes the insight that these are variants of one thing.

- **`get_variables` before adding tokens.** Checking what exists before adding `$illustration` prevents duplicate tokens with different values. The variable system is the source of truth; don't add to it without reading it first.

- **`find_empty_space_on_canvas` on a populated canvas.** Placing new frames at arbitrary coordinates risks invisible overlaps with existing work. The canvas tool returns safe coordinates; use it every time the canvas already has content.

For the screen-state taxonomy and the full fault-state matrix, see [`references/states.md`](../references/states.md).
