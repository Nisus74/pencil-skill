# Eval Response: Edit Verification on a LoginCard

---

## Part 1: Creating the LoginCard document

### Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

This confirms the Pencil MCP server is reachable. If it errors with `transport not connected to app: desktop`, I stop and tell you to open the Pencil desktop app. Assuming it succeeds and reports no active document, I proceed to open a new one.

### Step 2 — Open a new scratch document

```
open_document("new")
```

This creates a fresh `.pen` file. I note the returned document id (call it `doc`).

### Step 3 — Load guidelines and check for existing components/variables

```
get_guidelines()
get_variables()
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Since this is a brand-new document, `get_variables()` returns empty and `batch_get` returns no reusable components. No existing tokens to protect; no library components to prefer over primitives.

### Step 4 — Bootstrap tokens and theme axis

The document is empty, so I declare a `mode` theme axis and a minimal token set — including a `brandGreen` variable — before touching the canvas. I also declare `surface`, `onSurface`, `inputBorder`, and `primaryBlue` (for the initial button state, before the edit).

```
U("doc", { themes: { mode: ["light", "dark"] } })

set_variables({ variables: {
  surface:      { type: "color", value: [
    { value: "#FAFAFA", theme: { mode: "light" } },
    { value: "#0B1117", theme: { mode: "dark" } }
  ]},
  surfaceCard:  { type: "color", value: [
    { value: "#FFFFFF", theme: { mode: "light" } },
    { value: "#161B22", theme: { mode: "dark" } }
  ]},
  onSurface:    { type: "color", value: [
    { value: "#111318", theme: { mode: "light" } },
    { value: "#E6EDF3", theme: { mode: "dark" } }
  ]},
  onSurfaceMuted: { type: "color", value: [
    { value: "#5A6170", theme: { mode: "light" } },
    { value: "#7D8590", theme: { mode: "dark" } }
  ]},
  inputBorder:  { type: "color", value: [
    { value: "#D0D7DE", theme: { mode: "light" } },
    { value: "#30363D", theme: { mode: "dark" } }
  ]},
  primaryBlue:  { type: "color", value: [
    { value: "#0969DA", theme: { mode: "light" } },
    { value: "#1F6FEB", theme: { mode: "dark" } }
  ]},
  brandGreen:   { type: "color", value: [
    { value: "#1A7F37", theme: { mode: "light" } },
    { value: "#238636", theme: { mode: "dark" } }
  ]},
  onPrimary:    { type: "color", value: [
    { value: "#FFFFFF", theme: { mode: "light" } },
    { value: "#FFFFFF", theme: { mode: "dark" } }
  ]}
}, replace: false })
```

Note: `brandGreen` gets both light and dark values right now, even though I only need it for the edit in Part 2. Declaring it here means the edit later just references `$brandGreen` — no raw hex, full theme-axis behavior.

### Step 5 — Plan

Atmosphere: **airy / symmetric / static** — a centered auth card on a neutral surface.

I'll build one top-level frame (`LoginCard`) at 390 × auto, centered in a 390 × 844 page frame (`LoginPage_Mobile`). Inside `LoginCard`: a `SignInHeading` text, an `EmailField` group (label + input), a `PasswordField` group (label + input), a `SignInButton` frame (blue fill, white label), and a `ForgotPasswordLink` text below the button. All colors from variables.

Font: Geist (software UI default per skill aesthetic rules).

### Step 6 — Execute (build the card)

One `batch_design` call covering the full card:

```
batch_design(`
  page=I("doc", { type: "frame", name: "LoginPage_Mobile",
    width: 390, height: 844, fill: "$surface",
    context: "Mobile auth page wrapper. Centers LoginCard vertically and horizontally.",
    layoutMode: "horizontal", primaryAxisAlignment: "center", counterAxisAlignment: "center"
  })

  card=I("page", { type: "frame", name: "LoginCard",
    width: 358, fill: "$surfaceCard",
    layoutMode: "vertical", gap: 20, paddingTop: 40, paddingBottom: 40,
    paddingLeft: 32, paddingRight: 32, cornerRadius: 12,
    context: "Auth card. Contains heading, email/password fields, primary CTA, and forgot-password link."
  })

  heading=I("card", { type: "text", name: "SignInHeading",
    content: "Sign in",
    fontSize: 24, fontWeight: 700, fontFamily: "Geist",
    fill: "$onSurface",
    context: "Page-level heading for the sign-in screen."
  })

  emailField=I("card", { type: "frame", name: "EmailField",
    width: "fill_container",
    layoutMode: "vertical", gap: 6,
    context: "Email label + input pair."
  })
  I("emailField", { type: "text", name: "EmailLabel",
    content: "Email address", fontSize: 14, fontWeight: 500,
    fontFamily: "Geist", fill: "$onSurface"
  })
  emailInput=I("emailField", { type: "frame", name: "EmailInput",
    width: "fill_container", height: 44,
    layoutMode: "horizontal", paddingLeft: 12, paddingRight: 12,
    counterAxisAlignment: "center",
    stroke: { fill: "$inputBorder", width: 1, align: "inside" },
    cornerRadius: 6, fill: "$surfaceCard",
    context: "Email text input. Placeholder: 'you@example.com'."
  })
  I("emailInput", { type: "text", name: "EmailPlaceholder",
    content: "you@example.com", fontSize: 14, fontFamily: "Geist",
    fill: "$onSurfaceMuted"
  })

  passwordField=I("card", { type: "frame", name: "PasswordField",
    width: "fill_container",
    layoutMode: "vertical", gap: 6,
    context: "Password label + input pair."
  })
  I("passwordField", { type: "text", name: "PasswordLabel",
    content: "Password", fontSize: 14, fontWeight: 500,
    fontFamily: "Geist", fill: "$onSurface"
  })
  passwordInput=I("passwordField", { type: "frame", name: "PasswordInput",
    width: "fill_container", height: 44,
    layoutMode: "horizontal", paddingLeft: 12, paddingRight: 12,
    counterAxisAlignment: "center",
    stroke: { fill: "$inputBorder", width: 1, align: "inside" },
    cornerRadius: 6, fill: "$surfaceCard",
    context: "Password text input. Placeholder: 'Password'."
  })
  I("passwordInput", { type: "text", name: "PasswordPlaceholder",
    content: "Password", fontSize: 14, fontFamily: "Geist",
    fill: "$onSurfaceMuted"
  })

  btn=I("card", { type: "frame", name: "SignInButton",
    width: "fill_container", height: 44,
    layoutMode: "horizontal", primaryAxisAlignment: "center",
    counterAxisAlignment: "center",
    fill: "$primaryBlue", cornerRadius: 6,
    context: "Primary CTA. Renders disabled while submitting; spinner replaces label on submit."
  })
  I("btn", { type: "text", name: "SignInButtonLabel",
    content: "Sign in", fontSize: 15, fontWeight: 600,
    fontFamily: "Geist", fill: "$onPrimary"
  })

  linkContainer=I("card", { type: "frame", name: "ForgotPasswordContainer",
    width: "fill_container",
    layoutMode: "horizontal", primaryAxisAlignment: "center",
    context: "Wrapper for the forgot-password link. paddingTop provides breathing room below the button."
  })
  I("linkContainer", { type: "text", name: "ForgotPasswordLink",
    content: "Forgot password?", fontSize: 14, fontFamily: "Geist",
    fill: "$primaryBlue",
    context: "Navigation link to the password-reset flow."
  })
`)
```

The server returns success for all ops and echoes back node ids. I capture the real ids for `card`, `btn`, and `linkContainer` from the response bindings — I'll need them for the edit and for every verification call.

Let's say the server assigned:
- `card` → `lc_01`
- `btn` → `lc_btn_01`
- `linkContainer` → `lc_link_01`

---

## Part 2: The edit

### Execute the edit

```
batch_design(`
  U("lc_btn_01",  { fill: "$brandGreen" })
  U("lc_link_01", { paddingTop: 8 })
`)
```

Two ops. Server confirms both succeed. That's **Rung 1** of the verification ladder — free, no image cost.

---

## Part 3: Verification — step-by-step, tool by tool

Here is exactly what I do next, in order, and why.

---

### Rung 1 — `batch_design` response (already done, free)

The server's response to the two-op `batch_design` call above confirms both ops applied without schema errors. This tells me the node ids were valid and the property names were accepted. It does NOT tell me whether `$brandGreen` resolved correctly or whether `paddingTop: 8` is in the right place in the layout — that's what the next rungs are for.

---

### Rung 2 — `snapshot_layout` on the LoginCard

**Tool:** `snapshot_layout`
**nodeId passed:** `lc_01` (the `LoginCard` frame — the parent that contains both changed nodes)
**maxDepth:** `2`

```
snapshot_layout({ nodeId: "lc_01", maxDepth: 2 })
```

**Why this nodeId, not a wider or narrower one:**
- Wider (the page frame) would return layout data for the whole screen including chrome I don't care about — noise, not signal.
- Narrower (just `lc_btn_01` or `lc_link_01`) would miss the relationship *between* them — specifically, whether the `paddingTop: 8` on `lc_link_01` actually created the gap I intended and whether it pushed anything else out of place.
- `lc_01` (the card) covers both changed nodes as siblings (or near-siblings) and returns their positions, sizes, and computed gaps in one cheap JSON read.

**What I'm confirming:**
- `lc_link_01`'s `paddingTop` reads as `8` in the layout snapshot.
- Nothing else in the card shifted unexpectedly (the heading, field stack, and button should be at the same computed offsets they were before — only the link container's top padding changed).
- The button height is still 44 (the `fill` change shouldn't have touched sizing, but I confirm).

If the snapshot shows the link container's top offset increased by 8px relative to the button, the structural edit landed correctly.

---

### Rung 3 — `batch_get` on the button node

**Tool:** `batch_get`
**nodeIds passed:** `["lc_btn_01"]`

```
batch_get({ nodeIds: ["lc_btn_01"] })
```

**Why this nodeId and not the card or the link:**
- This is a property-level check, not a structural one. The specific question is: did `fill` land as `"$brandGreen"` (a variable reference) rather than a raw hex value?
- If the `batch_design` op had silently coerced `"$brandGreen"` to its resolved hex value `"#1A7F37"`, the design would *look* green in light mode but lose all dark-mode theme-axis behavior. `batch_get` on the button node shows the stored `fill` value — if it says `"$brandGreen"`, the variable binding is live. If it says `"#1A7F37"`, I need to re-issue the op.
- I don't need to `batch_get` the link container here — the padding is a numeric value, not a variable reference, and the layout snapshot already confirmed it. No reason to make a second JSON call for something Rung 2 already answered.

---

### Rung 4 — `get_screenshot` on the LoginCard (one call, final sign-off)

**Tool:** `get_screenshot`
**nodeId passed:** `lc_01` (the `LoginCard` frame, not the page)

```
get_screenshot({ nodeId: "lc_01" })
```

**Why `lc_01` and not the page frame:**
The skill's ladder rule is explicit: *"always pass the most specific `nodeId` that contains the change — never the page frame when a card subtree would do."* Both changed nodes (`lc_btn_01` and `lc_link_01`) live inside `lc_01`. Screenshotting the card gives me full fidelity on the green fill and the spacing below the button without capturing 500px of empty page background.

**What I'm visually confirming:**
1. The button renders green — and specifically a brand green that reads as intentional rather than garish. I'm checking that `$brandGreen` (#1A7F37 in light mode) has sufficient contrast against the white card background.
2. The gap between the button and the "Forgot password?" link reads as 8px of breathing room — visible as a small but meaningful separation. This is a spacing-rhythm question that pixel rendering answers better than a layout number (the number said 8; the image confirms it *reads* right at this scale).
3. No other element in the card shifted — heading, fields, and button are in the same relative positions as before the edit.

**Total `get_screenshot` calls: 1.**

---

### Dark mode — do I re-screenshot?

No.

The skill's dual-mode rule states: *"Re-screenshot the alternate mode only if the design uses mode-conditional colors and you have reason to suspect they were set wrong (e.g. raw hex used instead of a variable). Routine theme-aware designs — those built entirely from variables with both light/dark values — do not need a second screenshot."*

Both the `$brandGreen` fill on the button and the existing card tokens are variable bindings with explicit `light` and `dark` values. I already confirmed in Rung 3 that `fill` is stored as `"$brandGreen"` (not a raw hex). That means:
- In light mode: resolves to `#1A7F37`
- In dark mode: resolves to `#238636`

The variable system guarantees the dark value is live without me rendering it. A dark-mode screenshot would cost another large image payload and tell me nothing I don't already know from the variable binding confirmation. I don't take it.

If Rung 3 had revealed the fill was stored as a raw hex `#1A7F37` instead of `$brandGreen`, I would have: (1) re-issued the `U` op with the correct variable reference, (2) confirmed the binding via `batch_get` again, and (3) then taken a dark-mode screenshot to verify the dark value rendered correctly — because a raw hex has no dark-mode behavior and that's exactly the kind of "reason to suspect they were set wrong" the rule calls out.

---

## Summary table

| Step | Tool | nodeId | Why |
|------|------|--------|-----|
| 1 | `batch_design` response | — (implicit) | Free confirmation both ops were accepted without schema errors |
| 2 | `snapshot_layout` | `lc_01` (LoginCard) | Confirm `paddingTop: 8` landed on `lc_link_01` and no sibling shifted unexpectedly; structural, cheap |
| 3 | `batch_get` | `["lc_btn_01"]` (SignInButton) | Confirm `fill` is stored as `"$brandGreen"` variable reference, not a coerced raw hex; property-level, cheap |
| 4 | `get_screenshot` | `lc_01` (LoginCard) | Final visual sign-off: green renders correctly, spacing reads right, contrast passes; scoped to card not page |

**Total `get_screenshot` calls: 1.**
**Dark-mode re-screenshot: no** — variable bindings confirmed at Rung 3; the variable system guarantees both modes without a second render.
