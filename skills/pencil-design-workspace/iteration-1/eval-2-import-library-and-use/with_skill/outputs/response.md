# Adding a sign-up form using your `design/system.lib.pen` library

Here's the plan, the tools I'd call, and what I'd verify at each step. This follows the default workflow in `pencil-design/SKILL.md` with a deviation: because you've named a `.lib.pen`, I'm folding in the *"Use my design library"* branch from the **Design intelligence: when to deviate** section.

References I consulted (and why):

- `SKILL.md` — the default 7-step workflow, the Components-first discipline rule, the `.lib.pen` import section, and the verification ladder.
- `assets/examples/example-import-library.md` — exact ops for adding an `imports` entry and instantiating `ref` nodes.
- `references/component-anatomy.md` — how to read the library's components, build `descendants` paths, and override per-instance properties.
- `references/forms.md` — sign-up forms have their own discipline (Enter submits, autocomplete attributes, validation timing). I want this in mind before I author.
- `references/batch-design-grammar.md` — confirms the `I` / `U` / `C` op syntax and the binding form (`foo=I(...)`).

A note on the MCP server's "files are encrypted" reminder: SKILL.md flags this text as outdated. The `.pen` format is documented JSON. The reason I'm going through MCP isn't encryption; it's schema validation, live screenshots, and editor sync.

---

## Step 1 — Detect the host

```
get_editor_state({ include_schema: false })
```

**What I'd check:** the call succeeds, what `.pen` file is open, what's selected, what's already in the document's `imports` field, and whether the doc declares a `mode` theme axis with `light` and `dark` values. If the call errors with `transport not connected`, I stop and tell you to open the Pencil desktop app or the IDE extension. I do not silently fall back to the CLI.

**Response shape I'd expect:** an object with the active document id (often `"doc"`), a `selection` array, and the document's top-level metadata including `imports`, `themes`, and `variables`.

## Step 2 — Locate context

Two checks in parallel:

1. Confirm `design/system.lib.pen` actually exists on disk (a directory listing — not the MCP, since the path is a filesystem path).
2. Look for a `design-system/` folder at the repo root. If `design-system/design-system.md` exists and names the library path, I'd cross-check that the path you gave matches what's documented. If it doesn't, I'd surface the mismatch before writing anything.

## Step 3 — Inventory the library's components

This is the **Components-first** discipline rule. Before I instantiate anything, I need to know exactly what `Button` and `Input` are called in the library, what their reusable ids are, and what slots / descendants they expose.

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2, filePath: "./design/system.lib.pen" })
```

**What I'd check in the response:** the list of `reusable: true` nodes. I'm looking for the exact ids — `Button`, `ButtonPrimary`, `Input`, etc. Case matters; `ButtonPrimary` is not the same as `buttonPrimary`. I'd also note any sibling components I might want (a `FormField` wrapper, a `Link` for "Already have an account?", a `Divider`).

I'd also call:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

against the open document, in case it already has its own `Button` or `Input` overrides that should win over the library versions.

## Step 4 — Deep-read each component before using it

This is the part agents skip and regret. `readDepth: 2` from inventory shows top-level fields only. I need to see nested children to know which `descendants` keys are valid.

```
batch_get({ nodeIds: ["Button", "Input"], readDepth: 4, filePath: "./design/system.lib.pen" })
```

**What I'd scan in the response, per `component-anatomy.md`:**

- **`children`** — direct children's `id` values become my top-level `descendants` keys. For an `Input`, I'd expect something like `label`, `inputArea`, `helperText`, `errorText`. For a `Button`, typically `label` and maybe `iconLeft` / `iconRight`.
- **Nested children** — if `Input` has `inputArea/placeholder` or `inputArea/value`, those are addressable as `"inputArea/placeholder"` (slash-joined path).
- **`slot`** — any frame with a `slot` array is a content hole I'd fill via `descendants`.
- **`theme`** — tells me which states the component supports (`default`, `hover`, `focus`, `disabled`, `error`). The sign-up form uses `default` for everything, but I want to know the error state exists in case I add a "this email is taken" example state later.
- **`type` of each child** — tells me which properties are valid to override. A `text` child takes `content`; an `icon` child takes `iconName`; a `frame` child takes layout properties.

If I find that the library's `Input` doesn't expose a way to set `type="password"` or `type="email"` per instance, that's something I'd note — the engineer needs that, and if it's missing I'd flag it rather than silently shipping inputs that all look the same.

## Step 5 — Check for existing variables before assuming token names

```
get_variables()
```

**Why:** the Themes discipline rule is explicit — never re-declare a variable that already exists, and `set_variables` with `replace: false` still clobbers any keys you pass. I'd use this call to learn the actual token names available (likely from the library, since they're imported once step 6 lands), so my form's `fill` and `color` references match what's there rather than introducing new ones.

## Step 6 — Add the import (if not already present)

If `get_editor_state` showed `imports` does not contain the library, I'd add it. If imports exist already, I'd merge rather than overwrite.

```
batch_design({ operations: 'U("doc", { imports: { ds: "./design/system.lib.pen" } })' })
```

**Why a `U` and not an `R`:** `U` merges. `R` would wipe any other imports the document might already have. Variables defined in the library become available only after this lands — I won't reference `$libraryVar` until then.

## Step 7 — Plan and tell you, before any structural ops

Per the default workflow's step 4 (Plan), I'd say something like:

> *"Library imported as `ds`. I'll add a 400px-wide `SignUpCard` to your current page in empty canvas space. Inside: a heading, four `Input` instances (Full name, Email, Password, Confirm password), a primary `Button` for submit, and a footer line with a link back to sign-in. Email and password get `type` and `autocomplete` documented in `context` for the engineer. I'm using your `Button` and `Input` — no primitives. Sound right?"*

That one paragraph catches bad assumptions cheaply (wrong width, wrong fields, wanted email-only signup, etc.).

## Step 8 — Find empty canvas space (if the canvas is populated)

If your document already has frames on the canvas, I don't want my `SignUpCard` overlapping them.

```
find_empty_space_on_canvas({ width: 400, height: 600 })
```

**What I'd check:** the returned `x` / `y` coordinates. I'd pass them as the outermost frame's position in the next call. Skipping this on a crowded canvas produces invisible overlaps that look like rendering failures.

## Step 9 — Build the form (one `batch_design` call, ≤ 25 ops)

Following the `example-import-library.md` pattern, plus the discipline rules (every node gets a meaningful PascalCase `name`; non-trivial nodes get a `context`; theme-aware colours come from variables; behaviour annotations live in `context`, not visual specs).

```
card=I("doc", {
  type: "frame",
  name: "SignUpCard",
  context: "Sign-up form. Submit with Enter on any single-line input. On submit, validate all fields and focus first error. Posts to /api/auth/signup.",
  x: <from step 8>, y: <from step 8>,
  width: 400,
  layout: "vertical", gap: "$space-5", padding: "$space-7",
  cornerRadius: "$radius-lg",
  fill: [{ type: "solid_color", color: "$surface" }],
  stroke: { fill: "$border", width: 1 }
})
heading=I(card, { type: "text", name: "SignUpHeading", content: "Create your account", fontSize: "$text2xl", fontWeight: 700, color: "$textPrimary" })
sub=I(card, { type: "text", name: "SignUpSubheading", content: "Start your free trial. No credit card required.", fontSize: "$textSm", color: "$textMuted" })
nameField=I(card, { type: "ref", ref: "Input", name: "FullNameField",
  context: "autocomplete=name; autocapitalize=words; required.",
  descendants: { label: { content: "Full name" }, "inputArea/placeholder": { content: "Jane Cooper" } } })
emailField=I(card, { type: "ref", ref: "Input", name: "EmailField",
  context: "type=email; inputmode=email; autocomplete=email; autocapitalize=none; spellcheck=false; required. Validate format on blur.",
  descendants: { label: { content: "Email address" }, "inputArea/placeholder": { content: "you@company.com" } } })
pwdField=I(card, { type: "ref", ref: "Input", name: "PasswordField",
  context: "type=password; autocomplete=new-password; required. Min 8 chars; show strength indicator on blur.",
  descendants: { label: { content: "Password" }, "inputArea/placeholder": { content: "At least 8 characters" } } })
confirmField=I(card, { type: "ref", ref: "Input", name: "ConfirmPasswordField",
  context: "type=password; autocomplete=new-password. Validate match against PasswordField on blur and on submit.",
  descendants: { label: { content: "Confirm password" } } })
submit=I(card, { type: "ref", ref: "Button", name: "SignUpSubmit",
  context: "Primary submit. Disabled while submitting; spinner replaces label. Calls POST /api/auth/signup.",
  descendants: { label: { content: "Create account" } },
  width: "fill_container" })
footer=I(card, { type: "frame", name: "SignInLinkRow", layout: "horizontal", gap: "$space-2", justify: "center" })
footerText=I(footer, { type: "text", content: "Already have an account?", fontSize: "$textSm", color: "$textMuted" })
footerLink=I(footer, { type: "text", name: "SignInLink", context: "Routes to /sign-in.", content: "Sign in", fontSize: "$textSm", color: "$accent", fontWeight: 600 })
```

**Discipline notes baked in:**

- Every node has a PascalCase, role-bearing name (`SignUpCard`, `EmailField`, `SignUpSubmit`) — not `Frame 1` or `wrapper`.
- `context` annotates *behaviour* (validation timing, autocomplete attributes, what the submit posts to), not visual specs (no padding values or font sizes restated in prose — those live in the actual properties).
- I'm using `Input` and `Button` from the library via `ref`, not building from primitives. If your library names them `ButtonPrimary` / `TextInput`, I'd swap the `ref` strings to whatever the inventory call returned.
- `$surface`, `$textPrimary`, `$textMuted`, `$accent`, `$border`, `$space-*`, `$radius-lg`, `$text2xl`, `$textSm` — token bindings, not raw hex. If `get_variables()` shows your library uses different token names, I'd swap to those rather than introducing new ones.
- `width: "fill_container"` on the submit button is the bare-string form the live server accepts — not `"100%"`, not the older `{ sizing: "fill_container" }` object form.
- Bindings (`card=I(...)`) only live for the duration of one `batch_design` call, so subsequent ops can use them as parent ids.
- `autocomplete=new-password` on both password fields is the right value for sign-up (vs `current-password` for sign-in) — password managers need this distinction, per `references/forms.md`.
- 12 ops total, well under the 25-op ceiling.

**One ambiguity I'd resolve before issuing the ops:** the exact `descendants` keys (`"inputArea/placeholder"`, etc.) depend on what step 4 surfaced in the deep-read. If your `Input` exposes the placeholder under a different path, I'd use that path instead. I won't guess; I read first.

## Step 10 — Verify (structural-first, walking the ladder)

The verification ladder in `SKILL.md` says: rung 1 (response success) → rung 2 (`snapshot_layout`) → rung 3 (`batch_get` for property checks) → rung 4 (`get_screenshot`, expensive). I stop at the cheapest rung that answers the question.

```
batch_get({ nodeIds: [emailField, pwdField, submit] })
```

**What I'd check:** each `ref` node resolved to a real instance — the response should show the resolved descendants, not a placeholder. If a ref shows as unresolved (no instance children, original component name missing), the import path or the component id is wrong, and I'd fix that before going visual.

```
snapshot_layout({ nodeId: card, maxDepth: 2 })
```

**What I'd check:** the form rendered as a vertical stack with the gap I asked for, the card is 400px wide, fields stack in the order I issued them, padding numbers match `$space-7`. Numbers, not pixels — fast and cheap.

Then, for final visual sign-off only:

```
get_screenshot({ nodeId: card })
```

**What I'd scan in the rendered image:**

1. Layout integrity — card holds together; nothing off-canvas.
2. Spacing rhythm — gaps match `tokens.md`.
3. Type rhythm — heading > subheading > body > microcopy in legible steps.
4. Contrast — body text passes WCAG AA against `$surface`; submit button passes against its fill. If the library is set up with light + dark variables, dark mode is guaranteed by the variable system; I would not re-screenshot in dark mode unless something looked off in light mode.
5. Component fidelity — the inputs and button look like the library's other instances elsewhere in the project (no drifted styling).

**Total screenshots for this task: one,** scoped to the card subtree, not the whole page.

## Step 11 — Hand back

A one-paragraph summary of what landed: *"Sign-up card added at (`x`, `y`) with four `Input` instances and a primary `Button` from `ds` (your `system.lib.pen`). Email, password, and confirm-password fields document their `autocomplete` and validation expectations in `context` for the engineer. Sign-in link routes to `/sign-in`. Verified structure via `snapshot_layout` and bindings via `batch_get`; one final screenshot confirmed contrast and rhythm."*

---

## Why these tools, in this order

- **`get_editor_state` first** because nothing else works without a host, and I need to know the current `imports` and `themes` before I touch them.
- **`batch_get` against the library before any `batch_design`** because the Components-first rule says: don't build a Button from a frame + text when one already exists. I need the inventory and the deep-read to use the library correctly.
- **`get_variables` before referencing tokens** because re-declaring a variable that already exists silently clobbers user-configured values.
- **`U` op to add the import** rather than re-declaring the whole `imports` object, because the document might already have other imports I'd silently clobber with `R`.
- **`find_empty_space_on_canvas`** because crowded canvases produce invisible overlaps, and I don't know what else is on yours.
- **One `batch_design` call** for the form (12 ops, well under the 25-op ceiling) because it keeps ordering predictable and round-trips minimal.
- **Structural verification before visual** because `snapshot_layout` and `batch_get` answer "did the change land?" cheaply, and screenshots cost real tokens. One screenshot at the end, scoped to the card.

---

**One question before I run any of this:** is the library already imported in your open `.pen`? If yes, I skip step 6 and go straight to inventory + build. If no, I add the import as the first op. Want me to start?
