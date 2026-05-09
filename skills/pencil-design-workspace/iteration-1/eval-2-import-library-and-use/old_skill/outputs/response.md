# Sign-up form using your `design/system.lib.pen` Button and Input

Here's the plan, the tools I'd call, and why — walking the skill's default workflow with the deviations that fit "use my design library."

## References I consulted

- **`SKILL.md`** — for the seven-step default workflow, the Components-first discipline rule, the verification ladder, and the *"Use my design library / library is imported"* deviation.
- **`assets/examples/example-import-library.md`** — direct match for "library at a path, instantiate Button + Input." Gives the exact `imports` op and the `ref` pattern.
- **`assets/examples/example-form-flow.md`** — sign-up specifics: stepper, error-state-on-canvas, ToS checkbox, specific verbs, surfacing library candidates. I'm building a single-page sign-up here, not a multi-step flow, so I'll borrow the page-1 shape and skip the wizard scaffolding.
- **`references/component-anatomy.md`** — for reading `Button` and `Input` deeply enough to know what `descendants` keys are valid (label paths, slot frames, the `state` theme axis).
- **`references/batch-design-grammar.md`** — for the `I` / `U` / `ref` syntax, the `placeholder: true` rule on top-level frames, the bare-string `width: "fill_container"` form, and the `padding: [t,r,b,l]` array (no `paddingTop`).
- **`references/flows.md`** § Form validation timing — for the on-blur vs on-submit decisions I'd document in the email field's `context` so the engineer ships matching behavior.

I would *not* load `references/states.md` or `references/modern-patterns.md` for this task — single sign-up form, no states-heavy or container-query work mentioned.

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

What I'd check in the response:
- Did it succeed at all? If it returns `transport not connected to app: desktop`, I stop and tell you to open the Pencil desktop app or the Pencil IDE extension. I don't fall back to the CLI silently.
- The active document id (call it `doc`) and which `.pen` file path it points to.
- The current `imports` field — does it already include `./design/system.lib.pen`?
- Any current selection (informs where to drop the form, though the canvas-position deviation also matters).
- Whether the `mode` theme axis is already declared in `themes`.

## Step 2 — Locate context

I'd verify two things outside the MCP:

- **Library file exists.** A directory listing on `design/` to confirm `system.lib.pen` is there at the path you named.
- **`design-system/` folder.** A directory listing on the project root. If the folder exists, I read `design-system/README.md` and follow its pointers (likely `design-system.md` for stack/icon-library and `tokens.md` for which token to use when). If it doesn't exist, I'd offer to scaffold it once — but for this single-form task I wouldn't insist; if you decline, I proceed and don't ask again this session.

## Step 3 — Load guidelines + inventory components

Two parallel reads.

**Guidelines.** I'd call `get_guidelines()` with no arguments first to see which categories the server reports for this document, then load `Web App` (the relevant one for an app sign-up surface).

**Library inventory** (the Components-first rule made concrete):

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Why: I need the exact component ids before I can `ref` them. `Button` could be `Button`, `ButtonPrimary`, `PrimaryButton` — case matters, and the import-library example flags this as the #1 pitfall.

**Open-document inventory too.** Per the discipline rule I also run the same inventory against the open `.pen` itself:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Reason: if you've already defined something like a `FormField` wrapper or a sign-up-specific composition in the open doc, I should reuse that and not duplicate it from primitives.

**Then I'd read each of the two library components deeply** before I touch them:

```
batch_get({ filePath: "./design/system.lib.pen", nodeIds: ["Button", "Input"], readDepth: 4 })
```

What I'd scan in the response (per `component-anatomy.md`):

- `Button`'s top-level `children` — is the text node id `label`, `text`, `caption`? That id becomes my `descendants` key.
- Does `Button` have an icon child (`iconWrap/icon` or similar) in case I want a leading icon?
- Does `Button` have a `theme` axis with `state` values? I'd want at least `default`, `disabled`, `loading` available so the engineer can wire submit-time states.
- `Input`'s children: `label`, `input`, `helperText`, `error`, possibly `leadingIcon` or `trailingIcon` slot frames.
- Whether `Input.input` accepts `type: "password"` or whether there's a separate `PasswordInput` component.
- Whether there's already a `Checkbox` component (for the ToS row) — if not, I'd surface that gap rather than build a fake.
- Whether `Button` ships in multiple flavors (`Button` vs `ButtonSecondary`) so the cancel-or-secondary action matches your library.

## Step 4 — Plan, told to you before any write

I'd say something like:

> *"Library will be imported as `ds`. I'll add a single sign-up card frame to the open document at desktop sizing — 440px wide, vertical layout, $space-4 gaps. Inside: title (`Create your account`), subtitle, three `Input` instances (Email, Password, Confirm password), a ToS row, and a `Button` instance for `Create account`. Below the card, a secondary text line — `Already have an account? Sign in`. All colors via your library's variables, both light and dark. Atmosphere: balanced density, symmetric, static. I'm placing this in empty canvas space rather than over your existing content."*

This is the moment to catch wrong assumptions cheaply — wrong breakpoint, wrong component name, you wanted social-auth buttons, etc.

**Empty space check** (deviation: "Adding frames to a populated canvas"). Before the build call I'd run:

```
find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })
```

So the new sign-up frame doesn't overlap existing top-level frames. I'd use the returned `(x, y)` on my outermost frame.

## Step 5 — Execute (two `batch_design` calls)

### Call A — Import the library + bootstrap (3 ops)

```
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
U("doc", { themes: { mode: ["light", "dark"] } })   // only if not already declared per Step 1
```

Notes:

- If the doc already has `imports` for other libraries, I'd merge — read existing imports via `batch_get(["doc"])` first and combine, never overwrite.
- I'd skip the themes line if `get_editor_state` showed `mode` is already declared.
- I would *not* call `set_variables` in a library-using workflow — the library carries its own variables, and per the discipline rule I'd call `get_variables()` before touching tokens to avoid clobbering anything user-customized.

### Call B — Build the sign-up form (~14 ops)

```
page=I(document, { type: "frame", name: "SignUpPage", layout: "vertical", justifyContent: "center", alignItems: "center", x: <ex>, y: <ey>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "solid_color", color: "$surface" }], placeholder: true, context: "Standalone sign-up page. Single-step form; for multi-step or email-verification variants see flows.md." })
card=I(page, { type: "frame", name: "SignUpCard", layout: "vertical", gap: "$space-4", padding: "$space-8", width: 440, cornerRadius: "$radiusLg", fill: [{ type: "solid_color", color: "$surfaceMuted" }], stroke: { thickness: 1, fill: "$border" }, context: "Sign-up card. Centered on the page; renders identically across breakpoints, max width 440." })
title=I(card, { type: "text", name: "Title", text: "Create your account", fontSize: "$text2xl", fontWeight: 700, fill: [{ type: "solid_color", color: "$text" }] })
sub=I(card, { type: "text", name: "Subtitle", text: "Takes about a minute.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
email=I(card, { type: "ref", ref: "Input", descendants: { label: { text: "Email" }, input: { placeholder: "you@company.com" } }, context: "Async unique-email check fires on blur with 400ms debounce. Submit-time also catches server-side conflicts." })
pwd=I(card, { type: "ref", ref: "Input", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "8+ characters" }, helperText: { text: "Mix letters, numbers, and a symbol." } }, context: "Sync strength validation on blur. Submit-time validation only after non-empty." })
confirm=I(card, { type: "ref", ref: "Input", descendants: { label: { text: "Confirm password" }, input: { type: "password" } }, context: "Cross-field check at submit time only — don't shame the user mid-keystroke." })
tos=I(card, { type: "frame", name: "ToS", layout: "horizontal", gap: "$space-2", alignItems: "start" })
tosCheckbox=I(tos, { type: "ref", ref: "Checkbox", descendants: { label: { text: "I agree to the Terms and Privacy Policy." } } })
submit=I(card, { type: "ref", ref: "Button", descendants: { label: { text: "Create account" } }, context: "Primary CTA. Disabled until email + password + confirm + ToS are all valid; loading state during async submit." })
signinRow=I(card, { type: "frame", name: "SignInRow", layout: "horizontal", gap: "$space-1", justifyContent: "center" })
signinLead=I(signinRow, { type: "text", name: "Lead", text: "Already have an account?", fontSize: "$textSm", fill: [{ type: "solid_color", color: "$textMuted" }] })
signinLink=I(signinRow, { type: "text", name: "SignInLink", text: "Sign in", fontSize: "$textSm", fontWeight: 600, fill: [{ type: "solid_color", color: "$primary" }], href: "/signin" })
U(page, { placeholder: false })
```

14 ops, comfortably under 25. Things worth flagging in this op set:

- **`document` binding** for the top-level frame, never my own binding named `document` (would overwrite the predefined one).
- **`placeholder: true`** on the page frame the moment it's created, cleared by the final `U` op once the frame is finished.
- **Specific verb on the CTA** — *"Create account"*, not *"Submit"* or *"Sign up"*.
- **`context` on every non-trivial node** — title and subtitle are pure visual primitives so I leave them; the form fields, the page, the card, and the CTA all carry context the engineer reads first.
- **PascalCase semantic names** throughout — `SignUpCard`, `SignInRow`, `SignInLink`, not `Frame 1` or `wrapper`.
- **Component refs use the ids I read in Step 3** (`Button`, `Input`, `Checkbox`) — if any of those ids are different in your actual library, I update the call. If `Checkbox` doesn't exist, I'd ask you whether to (a) add one to the library, (b) build it from primitives once with a *"library candidate"* note, or (c) drop the ToS row.
- **No raw colors** except via variable references like `"$primary"` or `"$surface"`. The fills go through the library's tokens.
- **No `paddingTop` shorthand** — none of the ops need per-side padding here, but if I needed top-only I'd use the `padding: [8, 0, 0, 0]` array form.
- **No `Inter`, no `#000000` / `#FFFFFF`, no neon glow, no three-column equal grid, no fabricated metrics, no AI clichés** like *"Elevate"* or *"Seamless"* in the copy.

## Step 6 — Verify (structural-first, screenshot last)

I walk the verification ladder, stopping at the cheapest rung that answers the question.

**Rung 1 — `batch_design` response.** Did each op succeed? If `email`, `pwd`, `confirm`, or `submit` reports a ref-resolution failure (component id not found, library not loaded), the import is wrong or the id is misspelled. I fix and retry before going further.

**Rung 2 — `snapshot_layout`.**

```
snapshot_layout({ parentId: "page", maxDepth: 3 })
```

What I'd check: card centered on the page, card width 440, gap 16 between fields, padding 32 around the card content, ToS row aligned at start. If the card is left-anchored (often: vertical layout's `alignItems: "center"` has been forgotten), I fix structurally with a single `U` op.

**Rung 3 — `batch_get`.**

```
batch_get({ nodeIds: ["email", "pwd", "confirm", "submit"] })
```

This confirms the refs fully resolved into instances of the library components — I see the inherited children (label, input, helperText), the bound theme, and the descendants overrides applied on top. If any ref shows as a placeholder rather than a resolved tree, the import path or component id is wrong.

**Rung 4 — `get_screenshot`, exactly once, scoped to the card.**

```
get_screenshot({ nodeId: "card" })
```

Why scoped to `card` and not `page`: the card is what changed. The skill is explicit that screenshots are the most expensive thing this skill does — one screenshot, on the smallest meaningful subtree, at the end.

In the rendered image I'd scan in this order:

1. **Layout integrity** — card holds together, nothing off-canvas.
2. **Spacing rhythm** — gaps match `tokens.md`.
3. **Type rhythm** — title is the largest, subtitle smaller, helper text smallest.
4. **Contrast** — body text vs `$surfaceMuted` ≥ 4.5:1; the *"Sign in"* link in `$primary` vs `$surfaceMuted` is the most likely contrast failure to catch here.
5. **Component fidelity** — the inputs and button look exactly like other instances of those library components, not like hand-built lookalikes.

**Dual-mode rule.** I would *not* take a second screenshot for dark mode. The whole design uses variables that have both light and dark values declared in your library — the variable system guarantees the dark mode renders correctly. I'd only re-screenshot if the variable resolution showed something suspicious in Rung 3 (e.g. a fill resolved to a raw hex instead of a variable).

## Step 7 — Iterate or report

If verification surfaced one issue, I'd fix it with a targeted `U` op against the offending node, re-snapshot or re-screenshot scoped to just the changed area, then stop.

Otherwise, I'd report back something like:

> *"Done. Library imported as `ds`. Sign-up card on a new `SignUpPage` frame in empty canvas. Email, Password, Confirm password using your library's `Input`; Create-account CTA using `Button`; ToS checkbox using `Checkbox` (or — if it didn't exist — flagged as a library candidate). Validation timing documented in each field's `context` so the engineer ships matching behavior. Verified structurally with `snapshot_layout`, then one screenshot scoped to the card. Theme-aware via your library variables — both modes rest on the variable system, no second screenshot needed."*

## Things I would not do

- Build a Button from a frame + text (Components-first rule — and you explicitly named the library, so the answer is unambiguous).
- Re-declare any variables your library already defines (`get_variables()` first; `replace: false` still overwrites individual keys).
- Hand-edit the `.pen` file with file tools — every read and write goes through the MCP for schema validation, editor sync, and live screenshots.
- Take more than one screenshot, or screenshot the page when the card subtree is what changed.
- Add a "scroll to explore" hero, three-column feature grid, or fabricated metrics block to *"complete"* the page — sign-up is a single-card screen.

## Confirmation

Output written to `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-2-import-library-and-use/old_skill/outputs/response.md`.
