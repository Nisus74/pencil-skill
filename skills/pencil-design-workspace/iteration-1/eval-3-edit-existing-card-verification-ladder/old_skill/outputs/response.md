# Building the LoginCard, then verifying the edit

I'll walk this in two phases: first create the scratch doc and the LoginCard, then perform the requested edit and walk the verification ladder. The verification narrative at the end is where most of the detail lives — that's the part you asked about.

A note up front: there's no `paddingTop` property in the `.pen` schema. Padding is a 4-value array `[top, right, bottom, left]`. So adding "8px of paddingTop" to the link container becomes `padding: [8, 0, 0, 0]` (or, if the container already has padding on other sides, `[8, R, B, L]` — I'll read first to know).

---

## Phase 1 — Create the scratch doc and LoginCard

### Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

I expect this to come back with `transport not connected` if Pencil isn't open, or with `{ activeDocument: null, selection: null }` if it is. Assuming it succeeds with no active doc, I move on.

### Step 2 — Open a fresh scratch document

```
open_document({ path: "new" })
```

Server returns the new doc's root id. I'll keep referring to it as `doc` in the bindings below; the real returned id is what I'd use in the actual call.

### Step 3 — Bootstrap minimal tokens (light + dark)

Even for a scratch doc, the discipline rule says: every new document declares a `mode` theme axis with `light` and `dark` values, and never binds raw `#000000` / `#FFFFFF`. Before declaring tokens, the rule is also: **always call `get_variables()` first** so I don't clobber anything pre-existing.

```
get_variables()
```

For a brand-new scratch doc this returns an empty (or near-empty) variable set. I declare the theme axis, then a small token suite covering only what this card needs:

```
batch_design ops:
  U("doc", { themes: { mode: ["light", "dark"] } })
```

```
set_variables({
  variables: {
    surface:        { type: "color", value: [
      { value: "#FAFAFA", theme: { mode: "light" } },
      { value: "#0B1117", theme: { mode: "dark"  } } ] },
    surfaceMuted:   { type: "color", value: [
      { value: "#FFFFFF", theme: { mode: "light" } },
      { value: "#111827", theme: { mode: "dark"  } } ] },
    border:         { type: "color", value: [
      { value: "#E4E4E7", theme: { mode: "light" } },
      { value: "#27272A", theme: { mode: "dark"  } } ] },
    textPrimary:    { type: "color", value: [
      { value: "#0B1117", theme: { mode: "light" } },
      { value: "#FAFAFA", theme: { mode: "dark"  } } ] },
    textMuted:      { type: "color", value: [
      { value: "#52525B", theme: { mode: "light" } },
      { value: "#A1A1AA", theme: { mode: "dark"  } } ] },
    primary:        { type: "color", value: [
      { value: "#1F6FEB", theme: { mode: "light" } },
      { value: "#3B82F6", theme: { mode: "dark"  } } ] },
    onPrimary:      { type: "color", value: [
      { value: "#FFFFFF", theme: { mode: "light" } },
      { value: "#FFFFFF", theme: { mode: "dark"  } } ] },
    link:           { type: "color", value: [
      { value: "#1F6FEB", theme: { mode: "light" } },
      { value: "#60A5FA", theme: { mode: "dark"  } } ] },
    "space-2": { type: "number", value: 8 },
    "space-3": { type: "number", value: 12 },
    "space-4": { type: "number", value: 16 },
    "space-5": { type: "number", value: 24 },
    "space-6": { type: "number", value: 32 },
    textSm:    { type: "number", value: 14 },
    textBase:  { type: "number", value: 16 },
    text2xl:   { type: "number", value: 24 }
  },
  replace: false
})
```

I'm also adding a `brandGreen` placeholder now so I won't be re-declaring tokens in the middle of the edit:

(It's deliberately not declared yet — the user's request is to change the button's fill *to* a brand green. I'll add `brandGreen` as a new token at edit time, since it doesn't exist yet, and then bind the button's `fill` to `$brandGreen`. That keeps the token system intact.)

### Step 4 — Plan (told to user)

> *"I'll create a single LoginCard frame at sensible defaults: vertical layout, 24px gap, 32px padding, 360px wide, on a transparent canvas. Inside: a 'Sign in' heading, an Email input (label + input), a Password input (label + input), a primary 'Sign in' button (blue fill), and a 'Forgot password?' link container. Components don't exist in this scratch doc, so I'm building from primitives — that's the right call here per the Components-first rule (nothing to instantiate)."*

### Step 5 — Build the card

One `batch_design` call, well under 25 ops:

```
card=I("doc", {
  type: "frame", name: "LoginCard",
  layout: "vertical", gap: "$space-5", padding: [32,32,32,32],
  width: 360, cornerRadius: 12,
  fill: "$surfaceMuted",
  stroke: { thickness: 1, fill: "$border" },
  context: "Login card on the auth screens. Holds heading, email + password inputs, primary submit, and a secondary forgot-password link.",
  placeholder: true
})
heading=I(card, {
  type: "text", name: "HeadingSignIn",
  content: "Sign in",
  fontSize: "$text2xl", fontWeight: 700,
  fill: "$textPrimary",
  context: "H1 of the login card."
})
emailField=I(card, {
  type: "frame", name: "EmailField",
  layout: "vertical", gap: "$space-2", width: "fill_container",
  context: "Email input + label group."
})
emailLabel=I(emailField, {
  type: "text", name: "EmailLabel",
  content: "Email", fontSize: "$textSm", fontWeight: 500, fill: "$textPrimary"
})
emailInput=I(emailField, {
  type: "frame", name: "EmailInput",
  layout: "horizontal", padding: [12,12,12,12], width: "fill_container", height: 44,
  cornerRadius: 8, fill: "$surface",
  stroke: { thickness: 1, fill: "$border" },
  context: "Single-line email input. Renders error state on validation failure."
})
emailPlaceholder=I(emailInput, {
  type: "text", name: "EmailPlaceholder",
  content: "you@example.com", fontSize: "$textBase", fill: "$textMuted"
})
pwdField=I(card, {
  type: "frame", name: "PasswordField",
  layout: "vertical", gap: "$space-2", width: "fill_container",
  context: "Password input + label group."
})
pwdLabel=I(pwdField, {
  type: "text", name: "PasswordLabel",
  content: "Password", fontSize: "$textSm", fontWeight: 500, fill: "$textPrimary"
})
pwdInput=I(pwdField, {
  type: "frame", name: "PasswordInput",
  layout: "horizontal", padding: [12,12,12,12], width: "fill_container", height: 44,
  cornerRadius: 8, fill: "$surface",
  stroke: { thickness: 1, fill: "$border" },
  context: "Masked password input."
})
pwdPlaceholder=I(pwdInput, {
  type: "text", name: "PasswordPlaceholder",
  content: "••••••••", fontSize: "$textBase", fill: "$textMuted"
})
signInButton=I(card, {
  type: "frame", name: "SignInButton",
  layout: "horizontal", justifyContent: "center", alignItems: "center",
  padding: [12,16,12,16], width: "fill_container", height: 44,
  cornerRadius: 8, fill: "$primary",
  context: "Primary CTA on the login card. Blue while idle; renders disabled while submitting."
})
signInLabel=I(signInButton, {
  type: "text", name: "SignInLabel",
  content: "Sign in", fontSize: "$textBase", fontWeight: 600, fill: "$onPrimary"
})
forgotContainer=I(card, {
  type: "frame", name: "ForgotPasswordContainer",
  layout: "horizontal", justifyContent: "center", alignItems: "center",
  padding: [0,0,0,0], width: "fill_container",
  context: "Wrapper around the forgot-password link. Padding is the lever for breathing room above the link."
})
forgotLink=I(forgotContainer, {
  type: "text", name: "ForgotPasswordLink",
  content: "Forgot password?", fontSize: "$textSm", fill: "$link",
  context: "Secondary navigation. Routes to /forgot-password."
})
U(card, { placeholder: false })
```

15 ops. Every node has a meaningful PascalCase name and a `context` where it earns one. Every color goes through a token with both light and dark values. The link container has explicit `padding: [0,0,0,0]` so the upcoming edit has a known starting point.

I'd structurally verify the build with one `snapshot_layout(parentId: card, maxDepth: 2)`, then move on to the edit. (No mid-build screenshot — the structural snapshot is enough.)

---

## Phase 2 — Perform the edit

The edit is two things:
1. Change the SignInButton's fill from `$primary` (blue) to a brand green.
2. Add 8px of top padding to the ForgotPasswordContainer.

### Locate before editing

Even though I just built the card and have the binding ids in hand from the `batch_design` response, the discipline rule for edits is: read the affected nodes first to confirm their current shape. For padding specifically, this matters — I need to know the *other three* sides' current values so I don't blow them away.

```
batch_get({ nodeIds: ["<SignInButton>", "<ForgotPasswordContainer>"] })
```

The response gives me each node's full current properties. For SignInButton I confirm `fill: "$primary"`. For ForgotPasswordContainer I confirm `padding: [0, 0, 0, 0]` — so the new padding becomes `[8, 0, 0, 0]` rather than `[8, ?, ?, ?]`.

### Add the brand green token (it doesn't exist yet)

Before binding `$brandGreen` on the button, the token has to exist with both light and dark values. I check first:

```
get_variables()
```

If `brandGreen` is in there, I skip the next call. If not (likely — it wasn't in the bootstrap suite):

```
set_variables({
  variables: {
    brandGreen: { type: "color", value: [
      { value: "#16A34A", theme: { mode: "light" } },
      { value: "#22C55E", theme: { mode: "dark"  } }
    ] }
  },
  replace: false
})
```

`replace: false` is critical — `replace: true` would wipe the entire token suite I just declared.

### Apply the edit

One `batch_design` call, two `U` ops:

```
U("<SignInButton>", { fill: "$brandGreen" })
U("<ForgotPasswordContainer>", { padding: [8, 0, 0, 0] })
```

The server response confirms both ops landed and reports zero errors. **That's verification ladder rung 1.** It tells me the schema accepted the values; it does not tell me the layout actually moved or the color is bound correctly.

---

## Phase 3 — Verify the edit, step by step

This is the part you asked about. I walk the verification ladder, stopping at the cheapest rung that answers each question. The ladder is: (1) `batch_design` response, (2) `snapshot_layout`, (3) `batch_get`, (4) `get_screenshot`. I do not start at (4) and work down.

### Verification call 1 — `snapshot_layout` on the card

**Tool:** `snapshot_layout`
**Args:** `{ parentId: "<LoginCard>", maxDepth: 2 }`
**Why this nodeId:** the LoginCard is the smallest subtree containing both changed nodes (the button is a direct child; the forgot-password container is a direct child). Going to the document root would burn budget for no extra signal; going only to the SignInButton would miss the layout shift caused by the new padding rippling through the card's vertical flex.
**Why this tool first:** of the two changes, only one is structural (the padding). `snapshot_layout` is rung 2 and is the cheapest decisive answer to "did the layout shift the way I asked?".
**Response shape I expect:** a tree of nodes with `position: { x, y }`, `size: { width, height }`, and (when relevant) `padding`, `gap`, and child layout numbers.
**What I check:**

- ForgotPasswordContainer's `padding` is `[8, 0, 0, 0]` (the change landed at the structural level).
- The card's overall computed height grew by ~8px vs the pre-edit snapshot (the change actually shifted geometry, not just metadata).
- The forgot-password container's `position.y` is greater than it was before by ~8px relative to the SignInButton's bottom edge (no other rows shifted unexpectedly).
- The SignInButton's `size` is unchanged — the color edit shouldn't have moved geometry; if it did, I have a layout side-effect to investigate.

If any of those is wrong, I fix it now with another targeted `U` op rather than climbing higher up the ladder. Most failures here are cheap recoveries: padding written `[8]` instead of `[8,0,0,0]`, or written to the wrong sibling.

### Verification call 2 — `batch_get` on the SignInButton

**Tool:** `batch_get`
**Args:** `{ nodeIds: ["<SignInButton>"] }`
**Why this nodeId:** the color change is on this node specifically. There's no benefit to reading the whole card again — `batch_get` here is doing one thing: confirming that the `fill` property resolved to the variable binding I asked for, not to a raw hex.
**Why this tool, not a screenshot:** the question "did `fill` get set to `$brandGreen`?" is a property-level question, not a visual one. `batch_get` answers it in JSON; `get_screenshot` answers it in pixels and is ~5–10× the token cost. The skill explicitly calls this out: rung 3 (`batch_get`) for property-level intent, rung 4 (`get_screenshot`) for visual intent.
**Response shape I expect:** the full JSON for SignInButton, including its `fill` field.
**What I check:**

- `fill` is the literal string `"$brandGreen"` (the variable binding), not `"#16A34A"` (the resolved value). If I see the raw hex, the variable wasn't set up properly upstream and I need to re-issue the edit binding to the variable.
- Other properties on the button (`width`, `height`, `cornerRadius`, `padding`, `layout`) are unchanged from before the edit.

I do **not** also `batch_get` the ForgotPasswordContainer here — I already confirmed its padding via `snapshot_layout`. Re-fetching it would duplicate the signal.

### Verification call 3 (conditional) — `get_screenshot` on the LoginCard

**Tool:** `get_screenshot`
**Args:** `{ nodeId: "<LoginCard>" }`
**Why this nodeId:** the LoginCard subtree contains both edits and nothing else relevant. Screenshotting the document root would 5× the token cost for zero extra information — there's nothing else on the canvas worth re-rendering.
**Why this tool last:** the SKILL's verification ladder is explicit that screenshots are the most expensive step and should be reserved for genuinely visual questions or final sign-off. Two questions here genuinely need pixels:

1. Does the brand green render at acceptable contrast against the card background and `$onPrimary` label? Variables guarantee the color is *bound*; only a render shows whether the contrast holds at this specific pairing.
2. Does the 8px breathing room above the link actually read as breathing room, or is it absorbed by the card's `gap`? `snapshot_layout` proved the number is 8; only the screenshot proves it's *visually* sufficient.

**What I check, in the prescribed scan order:**

1. **Layout integrity** — the card holds together; nothing off-canvas; nothing wildly oversized.
2. **Spacing rhythm** — gaps between heading → email → password → button still match `$space-5`; the new gap above the link container reads as deliberate breathing room, not a misalignment.
3. **Type rhythm** — heading still steps above the body text correctly; nothing has gone tiny or huge.
4. **Contrast** — `$onPrimary` (white) against `$brandGreen` (#16A34A) — eyeball whether it passes WCAG AA (4.5:1 for body, 3:1 for large UI). The button label is `$textBase` 16px weight 600 — that's right at the body/large boundary, so 4.5:1 is the bar. #FFFFFF on #16A34A is roughly 3.5:1 in light mode, which is borderline for body and *fails* AA for body weight. If the screenshot confirms the contrast looks marginal, I'd raise it to the user and either bump the brand green darker (e.g. `#15803D`) or accept the tradeoff explicitly.
5. **Component fidelity** — N/A here, no library refs in this scratch doc.

**Dual-mode rule:** I screenshot the *primary* mode only (light, by default). I do *not* automatically re-screenshot in dark mode, because the design is built entirely from variables that have both light and dark values declared — the variable system guarantees mode parity. The only reason to take a second screenshot in dark mode would be if I had reason to suspect a raw hex slipped in — and I just confirmed via `batch_get` that the button's fill is bound to `$brandGreen`, not to a raw hex.

---

## Why this order, summarised

| Step | Tool | nodeId | Question it answers | Cost |
|------|------|--------|---------------------|------|
| 0 | `batch_design` response | n/a | Did the schema accept both `U` ops? | Free |
| 1 | `snapshot_layout` | `LoginCard` | Did the padding actually shift geometry? Did anything else move that shouldn't? | Cheap |
| 2 | `batch_get` | `SignInButton` | Did `fill` resolve to `$brandGreen`, or did it get a raw hex? | Cheap |
| 3 | `get_screenshot` | `LoginCard` | Does the brand green hold contrast under render? Does the 8px read as breathing room? | Expensive — used once, scoped to the card |

The total verification budget for this edit is **one screenshot, scoped to the smallest subtree containing both changes**. Pre-skill habits would have produced 2–3 screenshots (one mid-flight, one full-canvas final, possibly one in dark mode). Walking the ladder from cheap to expensive, and stopping at the cheapest rung that answers the actual question, keeps the work decisive without burning context.

If the screenshot surfaces an issue (say, contrast is borderline), I fix with one more `U` op and re-screenshot the same `LoginCard` nodeId. Three iterations max — past that, I'd stop and ask the user whether they want a darker brand green or to accept the tradeoff.

---

## Skill references I consulted

- **`SKILL.md`** — primary playbook. The "Edit the X" deviation under § Design intelligence, the verification ladder section (especially the worked 6-op example which mirrors this exact prompt), the discipline rules on Naming + Context + Themes, and Failure mode §7 (token clobber).
- **`references/batch-design-grammar.md`** — confirmed the `U` op syntax for property updates, the padding 4-array (`[top, right, bottom, left]`) — there is *no* `paddingTop` shorthand in this schema, the Common-errors table calls this out specifically — and the ≤25-ops chunking rule.
- **`references/mcp-tools.md`** — the per-tool cookbook for `snapshot_layout`, `batch_get`, `get_screenshot`, and `set_variables`, plus the explicit warning that `replace: false` does *not* protect existing variable values (so `get_variables()` first is mandatory).
- **`assets/examples/example-login-screen.md`** — confirmed the structural pattern for a from-primitives login card without a library. Did not consult `references/component-anatomy.md` because this scratch doc has no library and no `ref` nodes — that reference is for instantiating existing components, which doesn't apply here.

I did not load `references/states.md`, `references/flows.md`, `references/accessibility.md`, or `references/modern-patterns.md` for this task — none of the deviation triggers fired (no error/empty screen, no multi-screen flow, no modern-patterns ask, no a11y deep-dive ask).
