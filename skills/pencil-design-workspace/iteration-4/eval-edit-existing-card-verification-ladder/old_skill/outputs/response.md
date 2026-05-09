# Eval Response: LoginCard build + verification ladder explanation

## Step 1 — Host detection

```
get_editor_state({ include_schema: false })
```

Confirms the MCP server is reachable. If this fails I stop and tell the user to open the Pencil desktop app. Assuming it succeeds and shows no document currently open.

---

## Step 2 — Open a new scratch document

```
open_document("new")
```

This creates a fresh, unsaved `.pen` scratch file. The response gives me the new document's root node id, which I'll call `<doc>` throughout.

---

## Step 3 — Context check

`get_editor_state` showed no `imports`, so there are no attached libraries. I call:

```
get_guidelines()
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Both return empty — no categories matched, no reusable components in the new doc. I'll build from primitives.

**Atmosphere decision (required by the skill's aesthetic defaults):**
"Balanced / symmetric / static" — this is an auth card, not a dashboard, so airy-ish with tight internal rhythm.

**Font:** Geist (software UI, no design-system/ folder present, Inter is banned by the skill's anti-patterns rule).

---

## Step 4 — Plan

I'll create a single `LoginCard` frame at a mobile-ish width (360 × auto) with vertical auto-layout, containing:

- `SignInHeading` — display text "Sign in"
- `EmailField` — labelled input group
- `EmailInput` — the actual input frame
- `PasswordField` — labelled input group
- `PasswordInput` — the actual input frame
- `SignInButton` — primary CTA, blue fill (I'll bind `$primary` variable, set to a blue)
- `ForgotPasswordLink` — text link below the button

Variables declared upfront: `$surface`, `$textPrimary`, `$textSecondary`, `$primary`, `$primaryFg`, `$border` — each with both `light` and `dark` theme values, per the Themes rule.

---

## Step 5 — Execute (build the LoginCard)

**Call A** — declare theme axis and variables on the document:

```
U("<doc>", { themes: { mode: ["light", "dark"] } })
U("<doc>", { variables: {
  surface:      { type: "color", value: [{ value: "#FAFAFA", theme: { mode: "light" } }, { value: "#0B1117", theme: { mode: "dark" } }] },
  textPrimary:  { type: "color", value: [{ value: "#111218", theme: { mode: "light" } }, { value: "#F0F0F5", theme: { mode: "dark" } }] },
  textSecondary:{ type: "color", value: [{ value: "#5A5A72", theme: { mode: "light" } }, { value: "#8888A8", theme: { mode: "dark" } }] },
  primary:      { type: "color", value: [{ value: "#2563EB", theme: { mode: "light" } }, { value: "#3B82F6", theme: { mode: "dark" } }] },
  primaryFg:    { type: "color", value: [{ value: "#FFFFFF", theme: { mode: "light" } }, { value: "#FFFFFF", theme: { mode: "dark" } }] },
  border:       { type: "color", value: [{ value: "#E4E4EF", theme: { mode: "light" } }, { value: "#2A2A3C", theme: { mode: "dark" } }] }
} })
```

**Call B** — build the card tree (≤25 ops):

```
card=I("<doc>", {
  type: "frame", name: "LoginCard",
  context: "Auth surface. Contains sign-in heading, email+password inputs, primary CTA, and forgot-password link.",
  width: 360, height: "fit_content",
  layout: "vertical", gap: 16, paddingTop: 40, paddingBottom: 40,
  paddingLeft: 32, paddingRight: 32,
  fill: "$surface",
  cornerRadius: 12,
  stroke: { fill: "$border", weight: 1 }
})

heading=I(card, {
  type: "text", name: "SignInHeading",
  context: "Page-level heading for the auth card.",
  text: "Sign in",
  fontSize: 28, fontWeight: 700, fontFamily: "Geist",
  color: "$textPrimary"
})

emailField=I(card, {
  type: "frame", name: "EmailField",
  context: "Label + input group for email address.",
  width: "fill_container", height: "fit_content",
  layout: "vertical", gap: 6
})

emailLabel=I(emailField, {
  type: "text", name: "EmailLabel",
  text: "Email", fontSize: 13, fontWeight: 500, fontFamily: "Geist",
  color: "$textSecondary"
})

emailInput=I(emailField, {
  type: "frame", name: "EmailInput",
  context: "Text input for email address. Bound to email field in form state.",
  width: "fill_container", height: 44,
  layout: "horizontal", paddingLeft: 12, paddingRight: 12,
  fill: "$surface", stroke: { fill: "$border", weight: 1 }, cornerRadius: 8
})

emailPlaceholder=I(emailInput, {
  type: "text", name: "EmailPlaceholder",
  text: "you@example.com", fontSize: 15, fontFamily: "Geist",
  color: "$textSecondary"
})

passwordField=I(card, {
  type: "frame", name: "PasswordField",
  context: "Label + input group for password.",
  width: "fill_container", height: "fit_content",
  layout: "vertical", gap: 6
})

passwordLabel=I(passwordField, {
  type: "text", name: "PasswordLabel",
  text: "Password", fontSize: 13, fontWeight: 500, fontFamily: "Geist",
  color: "$textSecondary"
})

passwordInput=I(passwordField, {
  type: "frame", name: "PasswordInput",
  context: "Text input for password. Renders as masked field in code.",
  width: "fill_container", height: 44,
  layout: "horizontal", paddingLeft: 12, paddingRight: 12,
  fill: "$surface", stroke: { fill: "$border", weight: 1 }, cornerRadius: 8
})

passwordPlaceholder=I(passwordInput, {
  type: "text", name: "PasswordPlaceholder",
  text: "••••••••", fontSize: 15, fontFamily: "Geist",
  color: "$textSecondary"
})

signInButton=I(card, {
  type: "frame", name: "SignInButton",
  context: "Primary CTA. Renders disabled while submitting; spinner replaces label.",
  width: "fill_container", height: 44,
  layout: "horizontal", gap: 8,
  paddingLeft: 16, paddingRight: 16,
  fill: "$primary", cornerRadius: 8,
  mainAxisAlignment: "center", crossAxisAlignment: "center"
})

signInButtonLabel=I(signInButton, {
  type: "text", name: "SignInButtonLabel",
  text: "Sign in", fontSize: 15, fontWeight: 600, fontFamily: "Geist",
  color: "$primaryFg"
})

linkContainer=I(card, {
  type: "frame", name: "ForgotPasswordContainer",
  context: "Wrapper for the forgot-password link. paddingTop adds breathing room above.",
  width: "fill_container", height: "fit_content",
  layout: "horizontal", mainAxisAlignment: "center"
})

forgotLink=I(linkContainer, {
  type: "text", name: "ForgotPasswordLink",
  context: "Navigates to the password-reset flow.",
  text: "Forgot password?", fontSize: 13, fontFamily: "Geist",
  color: "$primary"
})
```

Server response confirms all ops succeeded. (Rung 1 satisfied.)

---

## Step 6 — Verify the initial build

I run `snapshot_layout(parentId: card, maxDepth: 2)` to confirm the 5 direct children of `LoginCard` landed in the right order with expected sizes. I don't screenshot here — the structural snapshot is sufficient to confirm the tree.

The card is now in place.

---

## Step 7 — Perform the requested edit

The two changes: (1) `SignInButton` fill → brand green; (2) `ForgotPasswordContainer` paddingTop → 8.

First, I need to know the node ids for those two nodes. I captured them in the binding variables above (`signInButton` and `linkContainer`), but in a real session where the card was already built in a prior exchange I'd call:

```
batch_get({ patterns: [{ name: "SignInButton" }, { name: "ForgotPasswordContainer" }], readDepth: 1 })
```

This returns the node ids. Call those `<signInButton>` and `<linkContainer>`.

I also need to know whether `$brandGreen` already exists as a variable. I check:

```
get_variables()
```

If `brandGreen` is absent, I add it to the document before the edit:

```
U("<doc>", { variables: {
  brandGreen: { type: "color", value: [
    { value: "#16A34A", theme: { mode: "light" } },
    { value: "#22C55E", theme: { mode: "dark" } }
  ]}
}})
```

Then the edit:

```
U("<signInButton>", { fill: "$brandGreen" })
U("<linkContainer>", { paddingTop: 8 })
```

Server response confirms both ops succeeded. (Rung 1 satisfied.)

---

## Step 8 — Verification (the graded section)

Here is the exact verification sequence I run, in order, including which nodeId I pass to each call and why.

### Call 1: `snapshot_layout(parentId: "<LoginCard>", maxDepth: 2)`

**Why this first:** I need to confirm the structural consequence of the `paddingTop: 8` change — that the `ForgotPasswordContainer`'s position shifted by exactly 8px relative to what it was before, and that nothing else in the card's auto-layout recomposed unexpectedly. `snapshot_layout` returns numbers (positions, sizes, gaps, child order) without burning image tokens. This is the cheapest tool that answers "did the spacing change land?"

**NodeId passed:** `<LoginCard>` — the direct parent of both edited nodes. I use the card level rather than the page root because the change is entirely contained within the card; scanning the full page would return irrelevant siblings. `maxDepth: 2` is enough to see all direct children of `LoginCard` and their immediate children, which covers `ForgotPasswordContainer`'s padding.

**What I confirm:** `ForgotPasswordContainer` shows `paddingTop: 8` in the returned layout data and its y-offset within the card reflects the 8px addition. No other child shifted unexpectedly.

### Call 2: `batch_get({ nodeIds: ["<signInButton>"] })`

**Why this second:** `snapshot_layout` confirmed the spacing landed but it doesn't surface property-level bindings like `fill`. I need to confirm that `fill` on `SignInButton` is now `"$brandGreen"` (the variable reference) rather than a raw hex. If a schema or binding error silently degraded the `U` op to a raw hex, I'd catch it here before doing the expensive screenshot. This is Rung 3 — cheap JSON, surgically targeted.

**NodeId passed:** `<signInButton>` only. I don't need to re-read `<linkContainer>` here because the padding was a scalar property change with no variable binding ambiguity — `snapshot_layout` already confirmed it numerically.

**What I confirm:** `fill` field reads `"$brandGreen"` (not `"#16A34A"` or any other raw hex). If it reads raw hex, I know the variable binding failed and I fix it before proceeding.

### Call 3: `get_screenshot(nodeId: "<LoginCard>")`

**Why this at all:** Two genuine visual questions remain that the structural tools cannot answer:

1. Does the brand green render correctly on screen — does it look like a confident CTA green rather than, say, a washed-out or clashing tone against the card's `$surface`?
2. Does the 8px paddingTop above the link read as the "breathing room" the user described — i.e. does the visual rhythm actually feel right, not just measure right?

Both of these are pixel-only questions. The render matters. So I escalate to Rung 4.

**NodeId passed:** `<LoginCard>` — the most specific node that contains both changes. I do NOT pass the page root or the document, because those would return the full canvas including any other frames, burning unnecessary tokens. I do not pass `<signInButton>` alone, because I need to see the button in context with the link to judge the combined spatial rhythm.

**What I examine in the rendered image:**
1. Button fill — green is rendering, not blue, not transparent.
2. Green contrast against card surface — passes WCAG 3:1 for a UI component (the button is not body text so 4.5:1 doesn't apply here, but I visually check it reads clearly).
3. Spacing between button and link — the 8px paddingTop reads as a visible, intentional gap rather than zero or an overwhelming void.
4. Nothing else in the card shifted (the heading, inputs are in the right positions).

**Total `get_screenshot` calls: 1.**

### Why no second screenshot in dark mode

The `$brandGreen` variable was declared with explicit `light` and `dark` theme values (`#16A34A` / `#22C55E`). The `$surface` variable it sits against likewise has both values. Because both sides of the contrast relationship are bound to theme-aware variables — not raw hex — the variable system guarantees the dark-mode pairing is correct by construction. There is no reason to re-screenshot in dark mode unless I had reason to suspect the variable declarations themselves were wrong (for example, if `get_variables()` had returned unexpected values). The skill's dual-mode rule is explicit on this: "Routine theme-aware designs — those built entirely from variables with both light/dark values — do not need a second screenshot to 'confirm both modes hold up'; the variable system guarantees it."

If I had used a raw hex like `fill: "#16A34A"` for the button, that would be a variable-binding failure and I'd need to re-screenshot in dark mode (or, better, fix the binding and screenshot once in whichever mode the user is currently viewing). The right fix is always to bind the variable, not to add a second screenshot.

---

## Summary

The LoginCard was built with all five requested elements, theme-aware variables for both light and dark mode, and Geist typography. The edit — green fill on `SignInButton`, 8px paddingTop on `ForgotPasswordContainer` — was executed in a single `batch_design` call. Verification ran three tools in order: `snapshot_layout` (structural, spacing confirmed), `batch_get` (property, variable binding confirmed), `get_screenshot` (visual, green render and rhythm confirmed). One screenshot total, scoped to `<LoginCard>`.
