# Walkthrough: designing a login screen in Pencil

Before I touch any tools, here's the plan I'd run. It follows the seven-step default workflow from the pencil-design skill, with the discipline rules layered on top. I'll call out which references I consulted and why.

## References I consulted

- **`SKILL.md`** — the workflow itself, the discipline rules (naming, context, components-first, themes, responsive, accessibility), the aesthetic defaults, the failure-mode table, and the verification ladder.
- **`assets/examples/example-login-screen.md`** — the worked greenfield walkthrough for almost exactly this prompt. It's the closest existing recipe, so I treated it as the spine of my plan.
- **`references/component-anatomy.md`** — because the components-first rule says I must inspect any unfamiliar component (`Input`, `ButtonPrimary`, `LinkText`) before instantiating it. This reference covers `descendants` keys, slot filling, nested paths via `/`, and how to set component states.

I would also read `references/batch-design-grammar.md` and `references/mcp-tools.md` on demand if I needed a refresher on op syntax or a tool I haven't used recently — but I wouldn't preload them.

## Step-by-step plan

### Step 1 — Detect host

Before anything else I'd ping the Pencil MCP host to confirm it's reachable.

**Tool call:** `get_editor_state({ include_schema: false })`

**Expected response shape:** an object describing the active document (or `null` if none), the current selection, and the host context. If the call fails with `transport not connected to app: desktop` or any connection-refused error, I stop immediately and tell you: *"Pencil's MCP server isn't reachable. Open the Pencil desktop app or the Pencil IDE extension, then ask me again."* I do not silently fall back to the CLI.

### Step 2 — Locate context

From the same response I record three facts:

1. Is a `.pen` file open? (drives whether I call `open_document` later)
2. Is anything selected? (a selection might mean you want me to add the login screen as a sibling to existing work)
3. What schema version does the document declare? (I'll defer to it for op shape)

Then I check the project filesystem (a directory listing, not the MCP) for a `design-system/` folder. The state of that folder branches the workflow:

- **Folder exists with markdown.** Load it in step 3.
- **Folder absent + this looks like real project work.** Offer once to scaffold the 12 core templates plus any optional ones (`mobile.md`, `data-viz.md`, `brand.md`, `imagery.md`) that fit your project. If you decline, proceed without and don't ask again this session.
- **Folder exists but holds source code** (`.tsx`, `package.json`, etc.). Don't overwrite. Ask where to put the docs instead.

### Step 3 — Load guidelines and inventory components

This is the step the AI tell skips. I'd do three things in parallel:

**a. Load project guidelines.** If `design-system/README.md` exists, read it. Then read whichever files it points to — typically `design-system.md` (which names the `.lib.pen` path, tech stack, and icon library) and `tokens.md` (which color, spacing, and type tokens to use).

**b. Call `get_guidelines()` with no arguments first.** It reports which categories exist for this document. I'd then read the categories that match the task — almost certainly `colors`, `typography`, `spacing`, and (if present) `Web App` or whichever app archetype matches.

**c. Inventory components.** This is the components-first rule. Two scans:

- **Open document:** `batch_get({ patterns: [{ reusable: true }], readDepth: 2 })` — surfaces components defined inside the current `.pen`.
- **Each attached library:** the document's `imports` field (visible in `get_editor_state`) names them. For each `.lib.pen` listed I'd repeat the scan with `filePath` set: `batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })`.

**What I'm hunting for:** an `Input` (or `TextField`, `FormField`), a primary button (`ButtonPrimary`, `PrimaryButton`, `Button`), and a link text component (`LinkText`, `TextLink`). Names will vary; I use whatever exists. If a component looks close but isn't named exactly what you said, I use the existing one — I don't fork the library because of a naming preference.

**For any unfamiliar component**, I'd read it deeper before instantiating: `batch_get({ nodeIds: ["InputId"], readDepth: 4 })`. In the result I'd scan for `slot` frames (content holes I fill via `descendants`), named children (their `id` values are valid `descendants` keys), and `theme` values (active states like `default` / `error` / `disabled`). A child at path `a → b → c` becomes `"a/b/c"` in `descendants`. This is straight from `references/component-anatomy.md`.

### Step 4 — Plan and name the atmosphere

Two things happen here before I write a single op.

**a. Name the atmosphere.** One adjective from each of three axes — density, variance, motion. For an auth screen my default is *"Airy, symmetric, static."* Login is a low-density landing — generous whitespace, centered geometry, no motion. I'd commit to this stance before planning the tree so the design doesn't drift to the generic "balanced / symmetric / fluid" default the model reaches for if you don't pin it.

**b. State the plan back to you in 2–3 sentences.** Something like:

> *"I'll create a centered single-column login screen at desktop (1440x900). A 360px-wide form card holds a title, a short subtitle, email + password inputs (instances of your `Input` component), a primary submit button (instance of `ButtonPrimary`), and a 'Forgot password?' link below the button. Colors and spacing reference your tokens; the library import is `./design/system.lib.pen`."*

This is the cheap moment to catch bad assumptions. If you want mobile-first, a split-screen with hero imagery, social-login buttons, or a different breakpoint, you tell me before any ops fire. I'd also confirm which breakpoint(s) you want — desktop only, or do you want sibling frames at mobile / tablet / desktop?

### Step 4.5 — Open the document if needed

If `get_editor_state` showed no active document, I'd call `open_document("new")`. The server returns a fresh document id, then I re-read `get_editor_state` to capture the new document root id (call it `doc`). If a `.pen` is already open and you want the login screen added as a sibling on the existing canvas, I'd skip this.

**One extra step on a populated canvas:** if there are already top-level frames on the canvas, I'd call `find_empty_space_on_canvas` and pass the returned `x`/`y` to my outermost frame. Skipping this on a crowded canvas produces invisible overlaps that look like rendering failures.

### Step 4.75 — Themes and variables

Before any color goes into the design I'd call `get_variables()`. Three outcomes:

- **Returns a populated set.** The document already has tokens you may have customised. I treat them as authoritative and never re-declare. I just use them by name (`$surface`, `$textBody`, `$brandPrimary`, etc.) in the ops.
- **Returns empty + the doc is genuinely fresh.** Declare the `mode` theme axis (`U("doc", { themes: { mode: ["light", "dark"] } })`) and call `set_variables` with only the variables I need that are absent. Every color carries both `light` and `dark` values; no exceptions.
- **Returns partial.** Only set the variables that are missing. `replace: false` (the merge default) still overwrites existing values for any key I pass — calling it with a full default suite would silently clobber tokens you'd configured. This is the "token clobber" failure mode in the skill's failure table.

### Step 5 — Execute the design

One `batch_design` call, well under the 25-op cap. Bound nodes via the `foo=I(...)` pattern so later ops can reference them. Roughly:

```
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
page=I("doc", { type: "frame", name: "LoginPage", context: "Auth landing — desktop. Single-column centered form card.", layout: "vertical", justifyContent: "center", alignItems: "center", padding: "$space-8", width: 1440, height: 900, fill: [{ type: "solid_color", color: "$surface" }] })
form=I(page, { type: "frame", name: "LoginCard", context: "Sign-in form. Holds title, subtitle, two inputs, primary CTA, and forgot-password link.", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: "$surfaceMuted", stroke: { thickness: 1, fill: "$border" } })
title=I(form, { type: "text", name: "Heading", text: "Sign in", fontSize: "$text2xl", fontWeight: 700 })
sub=I(form, { type: "text", name: "Subhead", text: "Welcome back. Enter your details below.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
email=I(form, { type: "ref", name: "EmailField", ref: "Input", context: "Email address. Required, validated on blur and on submit.", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", name: "PasswordField", ref: "Input", context: "Password. Required, masked input, show/hide toggle if the Input component supports it.", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "********" } } })
submit=I(form, { type: "ref", name: "SubmitButton", ref: "ButtonPrimary", context: "Primary CTA. Submits the form. Renders disabled while submitting; spinner replaces label.", descendants: { label: { text: "Sign in" } } })
forgot=I(form, { type: "ref", name: "ForgotPasswordLink", ref: "LinkText", context: "Secondary action. Routes to the password-reset flow.", descendants: { label: { text: "Forgot password?" } } })
```

About 10 ops. Discipline rules I'd verify in passing while writing:

- **Names** are PascalCase, semantic, role-bearing — `LoginPage`, `LoginCard`, `EmailField`, `SubmitButton`, `ForgotPasswordLink`. Not `Frame`, `Group`, `wrapper`. Even the inner wrapper `LoginCard` carries its role.
- **Context** strings on every non-trivial node — page-level frame, form card, each form field, the CTA, the link.
- **Refs not primitives** — `Input`, `ButtonPrimary`, `LinkText` are all instances. I don't re-build a button or a text input from a frame plus a text node when components exist.
- **Color via variables** — `$surface`, `$surfaceMuted`, `$border`, `$textMuted` — never raw `#FFFFFF` / `#000000`. The skill names pure black-on-white as one of the strongest AI tells.
- **Spacing via tokens** — `$space-4`, `$space-6`, `$space-8`. Not raw pixels.
- **Hit targets** — the `ButtonPrimary` instance carries the library's height; if the inventory shows it's under 44px I'd raise it via an override. Same for the link's effective tap area.

The exact field overrides on `Input` (`label.text`, `input.placeholder`, `input.type`) are placeholders. The component-anatomy step (4) is what tells me the real `descendants` key names. If the deep-read of `Input` shows the label child is named `fieldLabel`, the path becomes `fieldLabel` not `label`.

### Step 6 — Verify (structural-first)

Walk the verification ladder, stopping at the cheapest rung that answers the question.

**Rung 1 — `batch_design` response.** Did each op succeed? Free.

**Rung 2 — `snapshot_layout({ parentId: "page", maxDepth: 2 })`.** Confirms positions, sizes, gaps, child order in numbers. For this design I'd check:
- `page` computed height equals 900 (if it's shorter, the document root is constraining it — fix with `U("page", { height: "fill_container(900)" })`).
- `form` width is 360.
- Gap between form children matches `$space-4`.
- Each form child appears in the order I authored.

**Rung 3 — `batch_get({ nodeIds: [...] })`.** Confirms property-level intent. I'd verify:
- The two `Input` refs resolved against the library (no orphaned refs).
- Variable bindings landed (`$surface`, `$textMuted`) rather than raw hex slipping in.
- Text content reads as authored.

**Rung 4 — `get_screenshot(nodeId: "page")`.** Only after rungs 1–3 are clean. Scoped to the `page` node, never the document root. I scan in order: layout integrity, spacing rhythm, type rhythm, contrast, component fidelity. The forgot-password link being subtly off-center (left-aligned by default in a centered card) is the kind of pixel-only issue that surfaces here.

**Dual-mode screenshots:** I screenshot the primary mode only. I'd re-screenshot dark mode only if I had reason to suspect mode-conditional colors were set wrong (e.g. a raw hex slipped past me). For a routine theme-aware design built entirely from variables that have both light and dark values, the variable system guarantees both modes hold up — no second screenshot needed.

**Accessibility checks I run before declaring done** (not as TODOs):
1. Body text contrast against the card background passes WCAG AA (4.5:1) under both light and dark themes.
2. The submit button and the forgot-password link are at least 44x44 effective hit targets.
3. Errors (when the `Input` component renders an error state) carry both an icon and a color — never color alone.
4. Names map to roles (`SubmitButton`, `EmailField`, `ForgotPasswordLink`) — code generators downstream consume these.
5. The `Input` and `ButtonPrimary` instances have `focus` states defined in their library definition. If the deep-read in step 3 showed they don't, I'd flag it and offer to add them — shipping a login screen without keyboard focus states ships inaccessible UI.

### Step 7 — Iterate or report

If verification surfaced issues, I'd return to step 5 with targeted `U` (update) ops on the specific offending nodes. If clean, I summarise what landed in one paragraph and stop. I do not keep polishing past your stated requirements.

A typical end-to-end for this design is **one or two screenshots total** — possibly one mid-flight if a structural snapshot revealed something pixel-only could resolve, and one at the end before handing back. The reflex of "screenshot after every chunk" burns tokens to confirm things the structural snapshot already proved.

## Things I'd ask you before starting (if any are unclear)

1. **Breakpoint(s).** Desktop only, or sibling frames at mobile (390x844), tablet (768x1024), and desktop (1440x900)?
2. **Library path.** If `design-system/design-system.md` doesn't already name a `.lib.pen` and the open document has no imports, I'd ask whether to use an existing library (give me the path) or build from primitives this once.
3. **Social login or just email + password.** Your prompt is explicit (email, password, primary submit, forgot-password link) so I'd default to exactly those. I wouldn't add Google/Apple/SSO buttons unless you asked.
4. **Any branding direction** — split-screen with hero imagery, full-bleed background, centered card on a flat surface. The example walkthrough defaults to centered card on a flat surface; that's what I'd reach for unless you say otherwise.

If none of these are blockers, I'd state the plan in one short paragraph (the step-4 plan above), wait a beat for objections, then run the workflow.
