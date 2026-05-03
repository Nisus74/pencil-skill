Great — I can build that sign-up form into your open `.pen` file using the components from `design/system.lib.pen`. Here is the sequence of Pencil MCP tools I would call, what I would pass, and why each step matters.

## 1. Orient myself in the editor

**Tool:** `get_editor_state({ include_schema: true })`

**Why:** Before touching anything, I need to know which `.pen` file is currently active, what the user has selected (if anything), and the schema/shape of nodes I'll be writing. `include_schema: true` gives me the property formats I need to construct valid `batch_design` operations. This also confirms the active doc is the one you want me to edit (not the library file).

If for some reason no document is open, I would fall back to:

**Tool:** `open_document("new")` — or the explicit path you give me — to ensure there is an active canvas.

## 2. Load the design guidelines

**Tool:** `get_guidelines()` (and likely `get_guidelines("forms")` or similar follow-ups)

**Why:** Pencil ships canonical guidance on layout, spacing, typography, and form patterns. Pulling these first means the sign-up form I generate matches Pencil's expected idioms (label placement, field spacing, button sizing, error-state hooks) instead of me guessing. I'd specifically look for guidance on form composition and component reuse.

## 3. Open / inspect the library file

**Tool:** `open_document("design/system.lib.pen")`

**Why:** `.pen` library files are encrypted on disk — I cannot `Read` them. I have to open them through Pencil to enumerate what's inside. Depending on how Pencil's editor model handles libraries, this either makes the library available to the active document as a linked dependency, or simply gives me a readable handle to copy from. After this I switch focus back to your original document (re-call `get_editor_state` if needed to confirm active file).

## 4. Find the Button and Input components in the library

**Tool:** `batch_get(patterns: ["Button", "Input"])`

**Why:** I need the actual node IDs and prop schemas for the library's `Button` and `Input` so I can instantiate them. Pattern search lets me locate them by name without knowing IDs up front. From the result I'll capture:

- The component master node IDs (to copy/instance from)
- Their variant props (e.g. Button `variant: "primary" | "secondary"`, `size`, `state`; Input `label`, `placeholder`, `type`, `helperText`, `error`)
- Their default sizes so my layout math is correct

If the library exposes a typography/heading component too, I'd grab that in the same call by extending the patterns array (e.g. `["Button", "Input", "Heading", "Text", "Link"]`).

## 5. Find a place to put the form

**Tool:** `find_empty_space_on_canvas()`

**Why:** I don't want to drop the form on top of existing work. This returns a free region on the canvas (x/y/size) that I'll use as the anchor for the new frame.

Optional: `get_screenshot()` to visually confirm the chosen location makes sense relative to what's already on the canvas.

## 6. Build the form with `batch_design`

**Tool:** `batch_design(operations: [...])`

This is the one heavy write call. I'd keep it under ~25 ops. The script roughly looks like:

```
form  = I("<rootFrameId>", { type: "frame", name: "SignUpForm", x: <fromStep5>, y: <fromStep5>, width: 400, layout: "vertical", gap: 16, padding: 24, background: "surface" })
title = I(form, { type: "text", text: "Create your account", style: "heading/lg" })
sub   = I(form, { type: "text", text: "Start your free trial — no credit card required.", style: "body/md", color: "muted" })

email = C("<lib:Input id>", form, { props: { label: "Email",    type: "email",    placeholder: "you@company.com", required: true } })
pass  = C("<lib:Input id>", form, { props: { label: "Password", type: "password", placeholder: "At least 8 characters", required: true, helperText: "Must include a number and a symbol." } })
name  = C("<lib:Input id>", form, { props: { label: "Full name", type: "text",     placeholder: "Ada Lovelace", required: true } })

cta   = C("<lib:Button id>", form, { props: { label: "Create account", variant: "primary", size: "lg", fullWidth: true } })
alt   = C("<lib:Button id>", form, { props: { label: "Sign up with Google", variant: "secondary", size: "lg", fullWidth: true, leadingIcon: "google" } })

footer = I(form, { type: "text", text: "Already have an account? Sign in", style: "body/sm", color: "muted", align: "center" })
```

**Why this shape:**

- **`C` (copy/instance) for Button and Input** — these are library components, so I instance them rather than redrawing them. That keeps your design system intact: future edits to `system.lib.pen` propagate into this form.
- **`I` (insert) for the wrapping frame and plain text nodes** — the frame and copy strings aren't components, just structural content.
- **Vertical auto-layout with consistent gap/padding** — matches typical form patterns from `get_guidelines` and keeps the form responsive.
- **Order: heading → subhead → name → email → password → primary CTA → alt CTA → footer link** — standard sign-up hierarchy; primary action is visually dominant and full-width.

## 7. Verify the result

**Tools:** `batch_get(nodeIds: [<form id>])` then `get_screenshot()`

**Why:** Read back the form node tree to confirm the components instanced correctly (props applied, library link intact), then take a screenshot so I can visually confirm spacing, alignment, and that nothing landed off-canvas. If anything looks off, I'd issue a small follow-up `batch_design` with `U(...)` updates rather than rebuilding.

---

### Summary of why this order

1. `get_editor_state` — know where I am.
2. `get_guidelines` — know the rules.
3. `open_document` on the library + `batch_get` — know the parts I'm allowed to use.
4. `find_empty_space_on_canvas` — know where to put it.
5. `batch_design` — build it in one atomic script using `C` for components and `I` for structure.
6. `batch_get` + `get_screenshot` — verify before declaring done.

If you want, I can go ahead and execute this now against your currently open file — just confirm the active `.pen` is the target (not the library itself) and I'll run steps 1–7.
