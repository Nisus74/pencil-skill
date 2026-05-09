# Response: Add a sign-up form using Button and Input from a design library

## What I'd do and why — tool by tool

---

### Step 1 — Detect host

**Tool:** `get_editor_state({ include_schema: false })`

**Why:** Every Pencil task starts here. Without a live MCP connection, every subsequent call fails. This call costs nothing and tells me three things at once: whether the server is reachable, which `.pen` file is open, and what the document's current `imports` field contains. If it errors with `transport not connected to app: desktop`, I stop immediately and tell you to open the Pencil desktop app or IDE extension — I don't silently fall back to anything else.

From the response I note:
- The active document path (the open `.pen` file)
- The current `imports` object — specifically, whether `./design/system.lib.pen` is already present

---

### Step 2 — Verify the library file exists

**Tool:** filesystem directory listing (not an MCP tool — a regular `ls` on the project)

**Why:** Before I attempt to import the library, I confirm the file at `design/system.lib.pen` actually exists at the path you named. If it doesn't, I stop and tell you the path is stale rather than letting `batch_design` produce a confusing runtime error. This is a one-second check that prevents a hard-to-diagnose failure.

---

### Step 3 — Inventory the library's components

**Tool:** `batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })`

**Why:** The skill's "components first" rule requires that I know what's actually in the library before I plan anything. I never guess at component names — `ButtonPrimary` vs `Button` vs `btn-primary` is a real distinction and the server rejects a mismatched `ref`. This call returns every `reusable: true` node in the library with enough depth to see their inner structure (labels, inputs, slots). I build a mental inventory from the result: the exact node IDs for Button and Input, what child override keys they expose (e.g. `label`, `input`, `placeholder`), and what other components exist that I might reach for.

Expected result: something like `ButtonPrimary` (id: `btn-primary`), `ButtonSecondary` (id: `btn-secondary`), `InputField` (id: `input-field`). I use those exact IDs in the `ref` ops later.

---

### Step 4 — Add the import (if missing)

**Tool:** `batch_design` with a `U("doc", { imports: { "ds": "./design/system.lib.pen" } })` op

**Why:** If `get_editor_state` showed the library is not yet in the document's `imports`, I add it now, before any component instantiation. A `ref` to a library component is resolved at import time — if the import is absent, the `ref` silently fails to resolve. I merge with any existing imports (read the current `imports` object from `get_editor_state` and combine, never clobber).

If the library was already imported, I skip this step entirely.

---

### Step 5 — Check for variables and existing tokens

**Tool:** `get_variables()`

**Why:** The sign-up form needs colors for its surface, field backgrounds, and the button fill. Before I reference any `$variable` name, I confirm what variables the document exposes (including those inherited from the library after import). I never assume the document is blank. If `$surface`, `$colorPrimary`, or similar tokens are already declared, I use them. If the document is truly empty of variables, I note that and use the library's own token names (which I learned from the `batch_get` in step 3).

---

### Step 6 — Check canvas for empty space

**Tool:** `find_empty_space_on_canvas()`

**Why:** Your `.pen` file is already open with existing content. Placing a new top-level frame at coordinates `(0, 0)` risks overlapping whatever is already on the canvas, which looks like a rendering failure and is annoying to untangle. `find_empty_space_on_canvas` returns a safe coordinate region. I pass those `x`/`y` values as the position of the outermost `SignUpForm` frame.

---

### Step 7 — Load relevant guidelines

**Tool:** `get_guidelines()` (no arguments first, then load the matching category)

**Why:** The result tells me which guideline categories this document has declared (e.g. `Web App`, `Mobile App`). For a sign-up form I load the `Web App` category at minimum. Guidelines may carry spacing rhythm, corner radius scale, or breakpoint conventions that override the skill's defaults — I follow the document's declared guidelines, not my own assumptions.

---

### Step 8 — Plan (stated to you before any design ops)

Before touching `batch_design` I commit to a plan out loud. For this task it would be something like:

> "Library is imported as `ds`. I found `ButtonPrimary` (id: `btn-primary`) and `InputField` (id: `input-field`) in the library. I'll create a `SignUpForm` frame at the empty canvas region, desktop-width (360px), with a vertical auto-layout stack: heading, email `InputField` instance, password `InputField` instance, a submit `ButtonPrimary` instance. I'm using the library's `$surface` and `$colorPrimary` variables for the card background and button fill. Atmosphere: balanced / symmetric / static."

This is the moment to catch wrong assumptions cheaply — before a single op runs.

---

### Step 9 — Execute: build the sign-up form

**Tool:** `batch_design` (single call, ~10 ops)

**Why this sequence of ops:**

```
form=I("page", {
  type: "frame",
  name: "SignUpForm",
  context: "Top-level container for the sign-up flow. Mobile-width card, centers on wider viewports.",
  layout: "vertical",
  gap: 16,
  padding: 24,
  width: 360,
  cornerRadius: 12,
  fill: [{ type: "solid_color", color: "$surface" }],
  x: <x from find_empty_space_on_canvas>,
  y: <y from find_empty_space_on_canvas>
})

heading=I(form, {
  type: "text",
  name: "SignUpHeading",
  context: "Page-level heading. Renders above the field stack.",
  text: "Create your account",
  fontSize: "$textXl",
  fontWeight: 700,
  color: "$textPrimary"
})

emailField=I(form, {
  type: "ref",
  name: "EmailField",
  context: "Email address input. Validates format on blur; shows inline error on submit if blank or malformed.",
  ref: "input-field",
  descendants: {
    "input-field-label": { text: "Email address" },
    "input-field-input": { placeholder: "you@example.com" }
  }
})

passwordField=I(form, {
  type: "ref",
  name: "PasswordField",
  context: "Password input. Masked by default; show/hide toggle on the trailing icon.",
  ref: "input-field",
  descendants: {
    "input-field-label": { text: "Password" },
    "input-field-input": { placeholder: "Create a password", type: "password" }
  }
})

submitButton=I(form, {
  type: "ref",
  name: "SubmitButton",
  context: "Primary CTA. Renders disabled while the form submits; label changes to a loading state.",
  ref: "btn-primary",
  descendants: {
    "btn-primary-label": { text: "Create account" }
  }
})

signInLink=I(form, {
  type: "text",
  name: "SignInLink",
  context: "Navigation link back to the sign-in screen for users who already have an account.",
  text: "Already have an account? Sign in",
  fontSize: "$textSm",
  color: "$colorPrimary"
})
```

Key decisions in these ops:
- Every node has a meaningful `name` (PascalCase, role-bearing). No `Frame`, `Group`, or `Text 1`.
- Every non-trivial node has a `context` — one sentence explaining its role and implied behavior.
- Components are instantiated as `ref` nodes, not rebuilt from primitives. The `Button` and `Input` components from your library update automatically when the library changes; hand-built lookalikes don't.
- `descendants` overrides target child IDs from the library component's actual tree (learned in step 3). I don't guess these names.
- Colors reference `$variable` names, not raw hex. This preserves light/dark theme behavior.
- The outermost frame is positioned at the coordinates from `find_empty_space_on_canvas`.

---

### Step 10 — Verify (structural-first, verification ladder)

I walk the ladder in order, stopping at the cheapest rung that answers each question.

**Rung 1 — batch_design response (free)**

Did the call succeed? The server response confirms each op either succeeded or errored. If any op errored (e.g. mismatched `ref` ID, invalid property), I read the error verbatim, cross-reference the grammar, and fix before proceeding.

**Rung 2 — snapshot_layout (cheap, structural)**

**Tool:** `snapshot_layout(parentId: "<form-id>", maxDepth: 3)`

**Why:** This returns the positions, sizes, gaps, and child order for the entire form subtree as numbers. I confirm: the form is at the expected canvas coordinates, the vertical stack has the expected gap (16px), the button is 44px tall minimum (accessibility hit target), the form width is 360px. This answers every structural question without the cost of an image.

**Rung 3 — batch_get on specific nodes (cheap, property-level)**

**Tool:** `batch_get({ nodeIds: ["<emailField-id>", "<passwordField-id>", "<submitButton-id>"] })`

**Why:** Confirms the `ref` links resolved correctly. A `ref` that didn't resolve shows up in `batch_get` as a bare node with no expanded descendants. This is the definitive check that the library import worked and the component IDs were correct. I also verify `fill` on the form frame resolved to `$surface` (not fallen back to a raw hex or undefined).

**Rung 4 — get_screenshot (expensive, visual — used once)**

**Tool:** `get_screenshot(nodeId: "<form-id>")`

**Why at this rung:** The structural snapshot proved the layout numbers are right. The `batch_get` proved the refs resolved. The screenshot answers the one remaining question that only pixels can answer: does the form look right? Specifically I'm checking:
- Component fidelity — the Button and Input instances render identically to the library originals, not as drifted lookalikes
- Type rhythm — heading, label, placeholder, and link text step in readable proportion
- Contrast — body text and labels against the `$surface` background pass WCAG AA (4.5:1)
- Spacing rhythm — the 16px gap between fields and the 24px padding read as intended

Crucially, I scope the screenshot to the `form` node, not the entire page frame. The page may have many other elements; I only need to confirm the sign-up form.

**I do not take a second screenshot for dark mode** unless I used raw hex colors instead of variables. Because all colors in this design were bound to `$variable` names with light/dark values declared in the library, the variable system guarantees both modes hold. A second screenshot would confirm what the variable binding already proved — burning tokens without learning anything new.

---

### What I'd fix if verification found problems

| Problem | Fix |
|---------|-----|
| `ref` node shows no resolved descendants | The component ID in `ref` is wrong. Re-read the library with `batch_get({ filePath: "...", patterns: [{ reusable: true }] })`, get the exact ID, retry with `R` op. |
| Form overlaps existing content | `find_empty_space_on_canvas` result was ignored or stale. `U("<form-id>", { x: <corrected>, y: <corrected> })`. |
| Contrast fails in screenshot | The `$surface` or `$textPrimary` variables resolve to values too close together. Check with `get_variables()`, then `set_variables` to correct the failing token. Re-screenshot scoped to the form. |
| Button is less than 44px tall | `snapshot_layout` surfaced this. `U("<submitButton-id>", { height: 44 })` or check if the library component's minimum height is under-constrained. |
| Wrong label text in a ref instance | `descendants` key was incorrect. `batch_get` the library component to find the real child ID, then `U` the instance. |

---

### Summary of tools called and their order

| # | Tool | Purpose | Cost |
|---|------|---------|------|
| 1 | `get_editor_state` | Host detection, find open doc, read current imports | Free |
| 2 | filesystem `ls` | Confirm library file exists before importing | Free |
| 3 | `batch_get` (on library) | Inventory reusable components, get exact IDs | Cheap |
| 4 | `batch_design` (U op) | Add library to document imports (if missing) | Free |
| 5 | `get_variables` | Know what token names are available before referencing them | Cheap |
| 6 | `find_empty_space_on_canvas` | Safe canvas coordinates for new top-level frame | Cheap |
| 7 | `get_guidelines` | Load Web App guidelines for spacing/breakpoint conventions | Cheap |
| 8 | `batch_design` (~6–8 ops) | Build the form with ref instances | — |
| 9 | `snapshot_layout` | Confirm structure: sizes, gaps, child order | Cheap |
| 10 | `batch_get` (on instances) | Confirm refs resolved, variables bound correctly | Cheap |
| 11 | `get_screenshot` (form node) | Final visual sign-off — one screenshot, scoped | Expensive |

Total screenshots: **1**, scoped to the smallest meaningful subtree. No mid-flight screenshots, no full-canvas screenshots, no redundant dark-mode confirmation for a variable-based design.
