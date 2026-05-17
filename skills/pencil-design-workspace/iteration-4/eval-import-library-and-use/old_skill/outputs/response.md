# Response: Add a sign-up form using design/system.lib.pen

Here is exactly what I'd do, in order, including every tool call, its parameters, and why each one is chosen.

---

## Step 1: Detect host

```
get_editor_state({ include_schema: false })
```

**Why:** This is the mandatory first call on every Pencil task. Without it I don't know if the MCP server is reachable. If it fails with `transport not connected to app: desktop` I stop immediately and tell you to open the Pencil desktop app. If it succeeds I learn: which `.pen` file is open, what the document root id is, and — critically — what's in the `imports` field. That last part determines whether step 4 is needed at all.

---

## Step 2: Check whether the library file exists

I'd run a directory listing of `design/` in the project filesystem (not an MCP call) to confirm `system.lib.pen` is actually there.

**Why:** If the file is missing, adding an `imports` entry for a non-existent path will produce a silent failure later when I try to resolve components. Better to catch it here and ask you whether the path is stale or the library needs to be created.

---

## Step 3: Inventory the library's components

```
batch_get({
  filePath: "./design/system.lib.pen",
  patterns: [{ reusable: true }],
  readDepth: 2
})
```

**Why:** I need the exact ids and names of Button and Input as they exist in your library — not what I might guess them to be. Component ids are case-sensitive (`Button` vs `button` vs `ButtonPrimary`) and a wrong id produces a ref that silently fails to resolve. Reading the library first also surfaces sibling components (e.g. `ButtonSecondary`, `InputPassword`, `InputError`) that I should know about before planning — I may want to use `InputPassword` for the password field rather than a plain `Input` with a descendant override.

I also scan the open document's existing components at the same time:

```
batch_get({
  patterns: [{ reusable: true }],
  readDepth: 2
})
```

**Why:** In case there's already a `SignUpForm` component, a page-level frame I should add into, or a form group component that would be a better parent than a raw frame.

---

## Step 4: Check the document's imports — add if missing

From the `get_editor_state` result in step 1, I look at the `imports` field.

**If the library is already imported** (e.g. `{ "ds": "./design/system.lib.pen" }`): nothing to do; the components are already in scope.

**If it isn't imported**, I add it:

```
batch_design(`
  U("doc", { imports: { "ds": "./design/system.lib.pen" } })
`)
```

**Why:** Until `imports` is set, any `ref` node pointing at a component from that library is a dangling reference — it won't render and `batch_get` will return an unresolved placeholder. The import must exist before I create `ref` instances. If the document already has other imports I need to merge rather than overwrite, so I'd read the existing `imports` object via `batch_get({ nodeIds: ["doc"] })` first and combine.

---

## Step 5: Check the canvas for empty space

```
find_empty_space_on_canvas()
```

**Why:** If you already have frames on this canvas, dropping a new top-level frame at (0, 0) would overlap existing content — which looks like a rendering failure but is actually a placement collision. `find_empty_space_on_canvas` returns a coordinate region guaranteed to be clear, which I'll use as the `x`/`y` of the outer `SignUpForm` frame. If the canvas is empty, the call still works (returns a sane default origin).

---

## Step 6: Plan — state it before touching the canvas

Before any `batch_design` call I'd tell you:

> "I'll create a 390px-wide `SignUpForm` frame (mobile breakpoint) positioned at the empty space the canvas returned. Inside it: a heading `SignUpHeading`, an email field via a `ref` to your `Input` component, a password field via a second `ref`, a confirm-password field via a third `ref`, and a submit button via a `ref` to your `Button` component. All colors will come from variables; I'll use `$surface` for the card background so it resolves in both light and dark mode. Let me know if you want desktop width or anything different before I proceed."

**Why:** Cheap to catch a bad assumption here; expensive to undo after 15 ops.

---

## Step 7: Build the form

Using the component ids from step 3 (let's call them `cmpInput` and `cmpButton` — the real ids come from that `batch_get` result):

```
batch_design(`
  form=I("doc", {
    type: "frame",
    name: "SignUpForm",
    context: "Sign-up card. Renders on the auth screen; submitted to POST /auth/register. Shows inline validation on blur.",
    layout: "vertical",
    gap: 16,
    paddingTop: 32, paddingBottom: 32, paddingLeft: 24, paddingRight: 24,
    width: 390,
    cornerRadius: 12,
    fill: [{ type: "solid_color", color: "$surface" }],
    x: <x from find_empty_space>,
    y: <y from find_empty_space>
  })
  heading=I(form, {
    type: "text",
    name: "SignUpHeading",
    context: "Page heading for the sign-up screen.",
    text: "Create your account",
    fontSize: "$textXl",
    fontWeight: 700,
    fill: [{ type: "solid_color", color: "$textPrimary" }]
  })
  emailField=I(form, {
    type: "ref",
    name: "EmailField",
    context: "Email address input. Validated on blur; error state on invalid format.",
    ref: "cmpInput",
    descendants: {
      label: { text: "Email address" },
      input: { placeholder: "you@example.com" }
    }
  })
  passwordField=I(form, {
    type: "ref",
    name: "PasswordField",
    context: "Password input. Masked by default; show/hide toggle on the right.",
    ref: "cmpInput",
    descendants: {
      label: { text: "Password" },
      input: { placeholder: "Min 8 characters" }
    }
  })
  confirmField=I(form, {
    type: "ref",
    name: "ConfirmPasswordField",
    context: "Confirm password input. Validates match against PasswordField on blur.",
    ref: "cmpInput",
    descendants: {
      label: { text: "Confirm password" },
      input: { placeholder: "Re-enter password" }
    }
  })
  submitBtn=I(form, {
    type: "ref",
    name: "CreateAccountButton",
    context: "Primary CTA. Disabled while submitting; spinner replaces label text.",
    ref: "cmpButton",
    width: "fill_container",
    descendants: {
      label: { text: "Create account" }
    }
  })
`)
```

**Why each decision:**
- `name` on every node: discipline rule — default names (`Frame`, `Group`) are unacceptable.
- `context` on every non-trivial node: discipline rule — future agents (and future you) read these first.
- `ref` nodes, not hand-built frames: Components-first rule. Your library has Button and Input; recreating them from primitives would produce one-off look-alikes that won't update when the library does.
- `fill: "$surface"`, `fill: "$textPrimary"`: Variables, not raw hex. Variables carry both light and dark values; raw hex breaks dark mode.
- `width: "fill_container"` on the button (bare string): the grammar requires this form; `"100%"` and `{ sizing: "fill_container" }` are both rejected by the server.
- `width: 390` on the form frame: mobile canonical breakpoint (390 × 844). If you need desktop too, I'd add a sibling frame named `SignUpForm_Desktop` at 1440px with the same components.

---

## Step 8: Verify — the ladder, cheapest rung first

**Rung 1 — batch_design response (free)**

The server returns success or a list of failed ops. If any op failed, I read the error verbatim, cross-reference the grammar, and fix before continuing. Common causes: id with a slash, wrong sizing string, referencing a parent binding before it was created. I don't retry blindly.

**Rung 2 — snapshot_layout (cheap, structural)**

```
snapshot_layout({ parentId: "form", maxDepth: 2 })
```

This returns positions, sizes, gap values, and child order as numbers. I'm checking:
- `form` is 390px wide at the expected x/y coordinates.
- Six children in the correct order (heading, emailField, passwordField, confirmField, submitBtn).
- Gap between children is 16px as declared.
- No child reports zero height (which would mean a ref failed to resolve).

If something is wrong here I fix it with a targeted `U` op — I don't jump to screenshots.

**Rung 3 — batch_get on the ref nodes (cheap, property-level)**

```
batch_get({ nodeIds: ["emailField", "passwordField", "confirmField", "submitBtn"] })
```

**Why this rung matters for library refs specifically:** A `ref` node that points at an unresolvable component id doesn't error — it renders as a zero-height placeholder. `snapshot_layout` would catch the zero height, but `batch_get` on the node itself tells me *why*: it'll show the `ref` property still pointing at the original id with no resolved descendants. This is the rung where I confirm the import worked and the component ids are correct.

I'm looking for:
- Each node's `ref` field matches the actual component id (not a guess).
- The `descendants` overrides are present (label text, placeholder text).
- `fill` on `form` resolves to `$surface`, not a raw hex.

**Rung 4 — get_screenshot (expensive, visual — one call)**

```
get_screenshot({ nodeId: "form" })
```

Scoped to the `form` node, not the full page canvas. I scan the rendered image for:
1. Layout integrity — all five elements visible, nothing off-canvas or collapsed.
2. Spacing rhythm — 16px gap looks right at rendered scale; padding inside the card reads as breathing room.
3. Type rhythm — heading visually larger than field labels; body weight appropriate.
4. Contrast — label text against the card surface passes WCAG AA (4.5:1). Button label against button fill passes 3:1.
5. Component fidelity — the rendered Button and Input look like your library's components, not hand-built primitives. If they look wrong (wrong border radius, wrong fill), the ref either didn't resolve or a descendant override clobbered a structural property.

**I do not take a second screenshot for dark mode** unless I used raw hex colors somewhere. The form is built entirely from `$variables` that carry both light and dark values — the variable system guarantees the alternate mode holds up. A second screenshot would only confirm what the variable bindings already prove, at the cost of a large image payload.

---

## What I'd report when done

> "Sign-up form added to your canvas (`SignUpForm`, 390px wide, positioned at [x, y] to avoid existing content). It uses your library's `Input` and `Button` components — three email/password/confirm fields and a full-width 'Create account' button. Colors are bound to `$surface` and `$textPrimary` so the form responds to your theme variables in both modes. Screenshot confirms layout, spacing, and component fidelity. Let me know if you want a desktop-width sibling frame or any changes to the field order or copy."

---

## Pitfalls I watched for

- **Component id case sensitivity.** I got the real ids from `batch_get` on the library (step 3). I didn't guess `Button` or `button`.
- **Import before instantiation.** The `U("doc", { imports: ... })` op runs in its own `batch_design` call before any `ref` nodes are created. Refs to unimported libraries fail silently.
- **Path is relative to the importing `.pen`.** `./design/system.lib.pen` works if your open document is at the project root. If it's nested, the path needs to be adjusted — I'd confirm this from the `get_editor_state` result.
- **Canvas overlap.** `find_empty_space_on_canvas` ensures the new frame doesn't invisibly overlap your existing work.
- **Width string form.** `width: "fill_container"` not `"100%"`, not `{ sizing: "fill_container" }`.
- **No fabricated copy.** Field labels and button text use plausible real content, not "Lorem Ipsum" or AI clichés like "Seamless sign-up experience".
