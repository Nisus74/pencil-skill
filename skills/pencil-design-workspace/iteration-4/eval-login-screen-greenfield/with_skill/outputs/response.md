Before touching any tools, here is the complete sequence I'd follow — and why.

---

## Step 1: Detect the host

The first call is always:

```
get_editor_state({ include_schema: false })
```

This pings the Pencil MCP server. If it errors with `transport not connected to app: desktop` or any connection-refused message, I stop entirely and tell you: *"Pencil's MCP server isn't reachable. Open the Pencil desktop app or the Pencil IDE extension, then ask me again."* I don't silently fall back to anything else.

If it succeeds, I note: is a `.pen` file already open? Which file? What's selected? What schema version is the document on? This shapes everything that follows.

---

## Step 2: Locate context

From `get_editor_state`'s result I determine three things:

1. **Is a `.pen` file open?** If not, I'll need to open one (either an existing path you give me, or `open_document("new")`).
2. **What's currently selected?** If you've pre-selected a canvas area, I'll respect that as a placement hint.
3. **Does this repo have a `design-system/` folder?** I check the project filesystem (not a Pencil tool — just a directory listing). Three outcomes:
   - Exists with files → I read `README.md` first, then the specific files it points to.
   - Doesn't exist and this looks like real project work (not a one-off sketch) → I offer once to scaffold 12 core templates. On yes, I copy them in. On no, I proceed and don't ask again this session.
   - Exists but contains code (`.tsx`, `package.json`, etc.) → I don't overwrite. I ask where to put the docs instead.

---

## Step 3: Load guidelines and inventory components

**Guidelines first.** I call `get_guidelines()` with no arguments — the server reports which categories exist for this document. For a login screen, the relevant ones are likely `Web App` (or `Mobile App` if targeting mobile) and any auth-specific patterns. I read those before planning anything.

If `design-system/README.md` exists, I read it next, then the specific files it points to — usually `design-system.md` (which library path is in use, what icon library) and `tokens.md` (which color, spacing, and type token to reach for when).

**Component inventory.** This is non-negotiable before planning. I run:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

against the open document to find any components already defined in the file. Then I check `get_editor_state`'s `imports` field — if there's a `.lib.pen` attached, I repeat the same scan against it:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

The login screen needs three things: an email input, a password input, a primary submit button, and a link for "Forgot password?". Before building any of those from primitives, I need to know if components named `Input`, `ButtonPrimary`, `LinkText`, `TextInput`, or similar already exist. If they do, I instantiate them with `ref` nodes and override per-instance text. Building a button from a frame + text when a `ButtonPrimary` component exists in the library is a maintenance bug — it ships UI that won't update when the library does.

---

## Step 4: Plan (stated to you before any `batch_design` call)

Before writing a single op, I commit to a vibe. Auth screens are not dashboards — they don't need density. My default stance for a login screen: **airy / symmetric / static**. That means generous white space, a single centered card, no distracting motion.

Then I state the plan out loud, roughly like:

> *"I'll create a desktop frame at 1440×900 (`LoginPage_Desktop`) with a vertically and horizontally centered 360px-wide card (`LoginCard`). Inside the card: a heading ('Sign in'), a short subtitle, an email input, a password input, a primary submit button spanning the card width, and a 'Forgot password?' link centered below the button. All inputs, the button, and the link will be instances of your library's `Input`, `ButtonPrimary`, and `LinkText` components if they exist; otherwise I'll build them from primitives and flag that a reusable component would be worth adding. Colors come from `$surface`, `$surfaceMuted`, `$textDefault`, `$textMuted`, and `$border` variables — I'll check `get_variables()` first to confirm the token names already in use before writing any."*

This is the moment to catch bad assumptions cheaply — before any tool call.

**On the theme/tokens check:** Before any `batch_design` call I also call `get_variables()` to see what token names already exist. I never assume the document is empty and I never re-declare a variable that already exists. If the document has a complete token set, I use those names throughout; if it's genuinely empty, I bootstrap a minimal set with `set_variables`, declaring both `light` and `dark` values for every color variable. No "we'll add dark mode later."

---

## Step 5: Execute

Once the plan is stated and you haven't pushed back, I execute. One or more `batch_design` calls, each ≤25 ops. The rough shape for a login screen from scratch:

**Call 1: Document setup + skeleton**

```
U("doc", { themes: { mode: ["light", "dark"] }, imports: { "ds": "./design/system.lib.pen" } })
page=I("doc", { type: "frame", name: "LoginPage_Desktop", width: 1440, height: 900, layout: "vertical", justifyContent: "center", alignItems: "center", fill: [{ type: "solid_color", color: "$surface" }] })
card=I(page, { type: "frame", name: "LoginCard", context: "Auth card. Centered on the page. Contains all login form elements.", layout: "vertical", gap: 20, padding: 32, width: 360, cornerRadius: 12, fill: [{ type: "solid_color", color: "$surfaceMuted" }], stroke: { thickness: 1, fill: "$border" } })
heading=I(card, { type: "text", name: "LoginHeading", text: "Sign in", fontSize: "$text2xl", fontWeight: 700 })
subtitle=I(card, { type: "text", name: "LoginSubtitle", text: "Welcome back.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
email=I(card, { type: "ref", name: "EmailField", ref: "<InputComponentId>", context: "Email address input. Validated on blur; error state shows inline below the field.", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(card, { type: "ref", name: "PasswordField", ref: "<InputComponentId>", context: "Password input. Masked. Error state used when credentials are wrong.", descendants: { label: { text: "Password" }, input: { placeholder: "••••••••" } } })
submit=I(card, { type: "ref", name: "SubmitButton", ref: "<ButtonPrimaryComponentId>", context: "Primary CTA. Renders disabled while request is in-flight; label swaps to spinner.", descendants: { label: { text: "Sign in" } } })
forgot=I(card, { type: "ref", name: "ForgotPasswordLink", ref: "<LinkTextComponentId>", context: "Opens password reset flow. Centered below the submit button.", descendants: { label: { text: "Forgot password?" } } })
```

That's 9 ops — well under 25. If no library components exist and I'm building from primitives, the call grows by ~5–8 ops but stays in range.

**Naming discipline.** Every node gets a meaningful PascalCase name: `LoginPage_Desktop`, `LoginCard`, `EmailField`, `PasswordField`, `SubmitButton`, `ForgotPasswordLink`. Not `Frame 1`, not `wrapper`, not `f4`. The default names the editor falls back to are unacceptable for anything I author.

**Context discipline.** Every non-trivial node gets a `context` string: what role it plays, what data fills it in code, what behavior it implies. The `LoginCard` context explains it's the centered auth container. The `SubmitButton` context calls out the disabled-while-loading state. Future agents picking up this file read those first.

**Accessibility discipline.** The submit button must be ≥44×44px for touch targets even on desktop (responsive export). Body text against the card background needs ≥4.5:1 contrast ratio (WCAG AA). Color is never the sole error signal — if I add an error state to the inputs, it gets an icon *and* red, not just red. I don't leave this as a TODO.

---

## Step 6: Verify (structural-first)

I walk the verification ladder from cheapest to most expensive, stopping at the rung that answers the actual question.

**Rung 1:** Did `batch_design` report success? If not, I read the error verbatim and cross-reference the grammar rules (IDs can't contain `/`; `width: "100%"` is wrong — use bare `"fill_container"`; `stroke.fills` plural is wrong — use `stroke.fill` singular).

**Rung 2:** `snapshot_layout` on the `LoginCard` subtree:

```
snapshot_layout({ parentId: "LoginCard", maxDepth: 2 })
```

This returns positions, sizes, gaps, and child order as numbers. It confirms: is the card 360px wide? Is the gap between form rows what I intended? Is the submit button's computed height ≥44px? Is the forgot-password link the last child? This is cheap and catches most structural bugs before I reach for a screenshot.

**Rung 3:** If a specific property needs confirming (did the color token bind correctly? is the ref resolving to the right component?), I call `batch_get` on the specific node.

**Rung 4 (screenshot):** Only when the question is genuinely visual — rendered contrast, spacing rhythm at scale, or final sign-off. I screenshot the most specific node that contains the change: `get_screenshot(nodeId: "LoginCard")`, not the page frame, not the document root. A typical end-to-end design like this should need **one or two screenshots** total — not one after every chunk.

When scanning the screenshot I check in order: layout integrity (anything off-canvas?), spacing rhythm (gaps match tokens?), type rhythm (heading > body, legible?), contrast (body passes 4.5:1?), component fidelity (refs look like the library style, not hand-built look-alikes?).

---

## Step 7: Iterate or report

If verification surfaces issues, I return to step 5 with targeted `U` (update) or `R` (replace) ops against the specific offending node. If clean, I report in one paragraph: what landed, what components were instantiated, what tokens are in use, any deviations from the plan and why. Then I stop — I don't keep polishing past what you asked for.

---

## What I'd flag before starting

One thing worth confirming before I touch any tools: **is there a `.pen` file already open, or do I need to create one?** If you've already got a file open with a populated canvas, I'd also call `find_empty_space_on_canvas` at step 4 to place the new page frame without overlapping existing content — skipping that on a crowded canvas produces invisible overlaps that look like rendering failures.

If this is a one-off sketch rather than real project work, I'd skip the design-system folder check and the component inventory entirely and go straight to execution — verification still happens.
