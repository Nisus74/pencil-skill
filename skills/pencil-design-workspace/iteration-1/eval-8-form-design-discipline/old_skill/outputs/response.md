# Sign-up form — design plan

A single-screen sign-up form: name, email, password, confirm password, ToS checkbox, submit. I'll treat this as one auth-card screen (not a multi-step wizard — it's all one form), and follow the skill's default workflow.

## References I'm working from

Before planning, I read:

- `skills/pencil-design/SKILL.md` — for the discipline rules (Naming / Context / Components-first / Themes / Responsive / Accessibility / Completeness) and the default workflow.
- `references/flows.md` — because the user's prompt mentions a form. Specifically I needed it for **validation timing** (don't validate as the user types; on-blur for shape checks; on-submit for cross-field like password match) and the **submit verb** rule (a sign-up CTA reads "Create account", never "Submit").
- `assets/examples/example-form-flow.md` — the multi-step variant of this. I'm not building three frames, but the per-field `Input` ref pattern with `descendants` overrides and the auth-card lockup transfer directly.
- `references/component-anatomy.md` — to remind myself how `descendants` paths work (`label`, `input`, `helperText`, `error` keys, nested children joined with `/`) before I plan ref overrides I haven't read the actual library to confirm.
- `assets/design-system/patterns.md` § Auth flow — for the centred-card lockup itself: Logo → Title → (Subtitle) → Form fields → Primary button → Footer link.

I did **not** load `references/states.md`, `accessibility.md` (beyond the SKILL baseline), or `modern-patterns.md` for this task — a single sign-up form is squarely covered by the SKILL discipline + flows + the form-flow example. I'd reach for those only if the user asked for the error/loading/disabled states explicitly, an onboarding sequence, or container-query / fluid-type behaviour.

## Step 1 — Detect host

I'd call:

```
get_editor_state({ include_schema: false })
```

Expected response shape: `{ document: {...} | null, selection: [...], schemaVersion: "..." }`. If it errors with `transport not connected to app: desktop`, I stop and tell the user *"Pencil's MCP server isn't reachable. Open the Pencil desktop app or the Pencil IDE extension, then ask me again."* No CLI fallback.

What I'm looking for in a successful response: is a `.pen` open, what's selected, what schema version. The answer changes everything below.

## Step 2 — Locate context

From the `get_editor_state` result, I'd determine:

- Is a `.pen` file open? (If no, I'd ask: open existing, or `open_document({ path: "new" })`?)
- Anything selected? (If a frame is selected, I'd put the form inside it; if nothing, top-level on the canvas.)
- Does the project have a `design-system/` folder? I'd `ls ./design-system/` (filesystem, not MCP) and check for `README.md`, `tokens.md`, `design-system.md`, `voice.md`, `patterns.md`, `states.md`.

I'd also check whether the canvas already has top-level frames. If it does, I'd queue a `find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })` call before placing the new frame, so it doesn't overlap existing work.

## Step 3 — Load guidelines + inventory components

Two things in parallel.

**Guidelines.** Call `get_guidelines()` with no args first to see which categories the server reports for this document. For a sign-up screen, I'd then read `Web App` (and `Mobile App` if the project signals mobile in `design-system/design-system.md`). The auth-card pattern itself is a `patterns.md` thing, not a guideline thing.

**`design-system/` markdown.** If the folder exists I'd read `README.md`, then `design-system.md` (to learn the `.lib.pen` path, tech stack, icon library), `tokens.md` (colour / spacing / type variable names — so I bind `$primary`, `$surface`, `$border` correctly rather than inventing names), `voice.md` (button verbs, error message shape — important for the "Create account" CTA copy), `patterns.md` § Auth flow (the lockup), `states.md` (so I know the project's expected coverage for the `Input` component).

**Component inventory** — both halves of the components-first check:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

then, for each `.lib.pen` listed in the document's `imports` field:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

What I'm hoping to find: `Input`, `ButtonPrimary`, `Checkbox`, `LinkText`. What I'd also accept: equivalents under different names — `TextField`, `PrimaryButton`, `CheckboxField`. I will **not** rebuild a button from a frame + text if a `ButtonPrimary` (or `PrimaryButton`, or even `Button` with a primary variant) exists.

If the inventory surfaces an `Input` I haven't used before, I'd inspect it deeply per `references/component-anatomy.md`:

```
batch_get({ nodeIds: ["Input"], readDepth: 4 })
```

and scan for: `label`, `input`, `helperText`, `error` child ids (those become my `descendants` keys); the `theme.state` axis (default / hover / focus / error / disabled / success); and any nested `iconWrap/icon` paths if the Input supports leading or trailing icons.

If no library exists yet — I'd note it to the user and either (a) build from primitives for this one-off, or (b) suggest scaffolding `design-system/` and a starter `.lib.pen`. I would not silently fork.

## Step 4 — Plan (told to user before any `batch_design` call)

> *"I'll add one top-level frame `SignupPage` at desktop breakpoint (1440×900), centred on a `$surface` background, with one `SignupCard` (max-width 440) inside it. The card holds: a small logo at top, a `Create your account` title, a one-line subtitle, then a vertical stack of five fields — Full name, Email, Password (with helper text *'8+ characters, mix letters and numbers'*), Confirm password, and a Terms-of-Service checkbox with a clickable Terms / Privacy link. Below: a full-width `Create account` primary button, then a *'Already have an account? Sign in'* footer link. All fields are `Input` refs from your `.lib.pen` with `descendants` overrides for label and placeholder; the button is a `ButtonPrimary` ref; the checkbox is a `Checkbox` ref; the footer is a `LinkText` ref. Theme-aware via your existing variables. Atmosphere: airy, symmetric, static — auth screens shouldn't feel busy."*

The atmosphere line is deliberate per the skill's "Name the atmosphere before you plan" rule. Without it, the model defaults to balanced/symmetric/fluid for everything and the result reads generic.

## Step 4.5 — Open the document (only if needed)

If `get_editor_state` reported no active document:

```
open_document({ path: "new" })
```

Then declare the theme axis if the doc is genuinely empty (skip if the existing doc already has it — check `get_editor_state` output for `themes.mode`):

```
batch_design ops:
U("doc", { themes: { mode: ["light", "dark"] } })
```

Before any token work I'd call `get_variables()` first to see which colour / spacing / type variables already exist. If the document already has `$surface`, `$primary`, `$border`, `$text`, `$textMuted`, `$space-*`, `$text*`, `$radius*` — I use them as-is and don't re-declare. The skill is explicit about this: `set_variables` with `replace: false` still overwrites individual keys, so passing a "default suite" silently clobbers user-tuned tokens.

Only if `get_variables()` returns empty would I call `set_variables` with the minimum needed — and only for the variables I'm about to use (surface, primary, border, text, textMuted, space-2/3/4/5/6/8, textBase/Sm/Lg/2xl, radiusMd/Lg).

## Step 5 — Execute (one `batch_design` call, ~22 ops)

Call shape: `batch_design({ operations: "<lines>" })` — one op per line, ≤25 ops, using `foo=I(...)` bindings so later ops can refer to nodes I just created.

Sketch of the ops (assuming a library with `Input`, `ButtonPrimary`, `Checkbox`, `LinkText` is imported as `ds`):

```
page=I(document, { type: "frame", name: "SignupPage", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x>, y: <y>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "solid_color", color: "$surface" }], placeholder: true, context: "Sign-up screen. Single-step form. On submit, validates password match client-side, then POSTs to /signup; success redirects to /onboarding." })
card=I(page, { type: "frame", name: "SignupCard", layout: "vertical", gap: "$space-5", padding: "$space-8", width: 440, cornerRadius: "$radiusLg", fill: [{ type: "solid_color", color: "$surfaceMuted" }], stroke: { thickness: 1, fill: "$border" }, context: "Auth card. Centred on the page; max-width 440 keeps line length comfortable." })
logo=I(card, { type: "icon_font", name: "Logo", iconName: "hexagon", iconLibrary: "lucide", fontSize: 32, fill: [{ type: "solid_color", color: "$primary" }] })
title=I(card, { type: "text", name: "Title", text: "Create your account", fontSize: "$text2xl", fontWeight: 700 })
sub=I(card, { type: "text", name: "Subtitle", text: "Takes about 30 seconds.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
fields=I(card, { type: "frame", name: "FieldStack", layout: "vertical", gap: "$space-4", width: "fill_container", context: "Vertical stack of all five inputs." })
nameField=I(fields, { type: "ref", ref: "Input", name: "NameField", descendants: { label: { text: "Full name" }, input: { placeholder: "Alex Lee" } }, context: "Required. Free-form text. No validation beyond non-empty." })
emailField=I(fields, { type: "ref", ref: "Input", name: "EmailField", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com", type: "email" } }, context: "Required. On blur: format check. On submit: server-side uniqueness check; conflict surfaces inline as 'That email is already registered. Sign in instead.'" })
pwdField=I(fields, { type: "ref", ref: "Input", name: "PasswordField", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "8+ characters" }, helperText: { text: "Mix letters, numbers, and a symbol." } }, context: "Required. Min 8 chars; strength is shown via the helper line. Reveal-password toggle handled by the Input component if it supports it." })
confirmField=I(fields, { type: "ref", ref: "Input", name: "ConfirmPasswordField", descendants: { label: { text: "Confirm password" }, input: { type: "password", placeholder: "Re-enter your password" } }, context: "Required. On submit: cross-field check against PasswordField; mismatch surfaces inline as 'Passwords don\\'t match.'" })
tosRow=I(card, { type: "frame", name: "TermsRow", layout: "horizontal", gap: "$space-2", alignItems: "start", width: "fill_container" })
tosCheckbox=I(tosRow, { type: "ref", ref: "Checkbox", name: "TermsCheckbox", descendants: { label: { text: "I agree to the Terms and Privacy Policy." } }, context: "Required to enable the Create account button. Terms / Privacy substrings link out to /terms and /privacy." })
submit=I(card, { type: "ref", ref: "ButtonPrimary", name: "SubmitButton", descendants: { label: { text: "Create account" } }, context: "Primary CTA. Disabled until all five fields are non-empty AND the Terms checkbox is checked. Renders loading state during the POST; the label is replaced with a spinner; the button width is preserved so the card doesn't reflow." })
divider=I(card, { type: "rectangle", name: "Divider", width: "fill_container", height: 1, fill: [{ type: "solid_color", color: "$border" }] })
signinRow=I(card, { type: "frame", name: "SignInRow", layout: "horizontal", gap: "$space-1", justifyContent: "center", width: "fill_container" })
signinPrompt=I(signinRow, { type: "text", name: "SignInPrompt", text: "Already have an account?", fontSize: "$textSm", fill: [{ type: "solid_color", color: "$textMuted" }] })
signinLink=I(signinRow, { type: "ref", ref: "LinkText", name: "SignInLink", descendants: { label: { text: "Sign in" } } })
U("page", { placeholder: false })
```

19 ops. Things I'm doing deliberately:

- **Every node has a meaningful PascalCase name.** No `Frame 1`, no `wrapper`. Even the inner stack (`FieldStack`) and the row (`TermsRow`, `SignInRow`) earn their names because they have a role.
- **Every non-trivial node has a `context`.** The page frame, the card, every form field, the submit button, the checkbox row. The atomic logo and divider don't need one — they're pure visual primitives.
- **The submit verb is "Create account", not "Submit".** Per `flows.md` and `voice.md`: confirmation CTAs use a specific verb tied to the outcome.
- **Validation timing is documented in field `context`s, not visible on the canvas.** The default canvas state is the resting form. The engineer reads the context to learn that email checks on blur, passwords cross-check on submit, etc.
- **The submit button's loading behaviour is documented**: label replaced with spinner, width preserved, no reflow. Per `flows.md` anti-patterns.
- **`width: "fill_container"`** (bare string) for the field stack and the submit button — never `"100%"`, never the older `{ sizing: ... }` object, never `"auto"`.
- **All colours are variables** — `$surface`, `$surfaceMuted`, `$border`, `$primary`, `$textMuted`. No raw `#000` / `#FFF`. The `mode` theme axis already maps these to light/dark values.
- **Helper text is on the password field**, not the email or name fields. Helper text where there's no rule is just visual noise.
- **The ToS checkbox uses "I agree to" language** — clear consent, not a passive *"Accepts terms"*.
- **The placeholder for email is `you@example.com`**, the name placeholder is `Alex Lee`. Per the Plausible content rules in `flows.md`: not `John Doe`, not `john@example.com` (too generic). Real-shape names with texture.

Things I'm deliberately NOT doing:

- **No social-login buttons** ("Continue with Google", "Continue with GitHub"). The user didn't ask for them, and `patterns.md` is explicit that one primary is enough — adding "or continue with" introduces a second primary affordance.
- **No password-strength meter visualisation.** The helper text covers the rule; a meter is a follow-up if the user asks for it.
- **No live error states on the canvas.** The user asked for the form, not its error states. If I were also asked to cover validation visually, I'd add a sibling frame `SignupPage_Errors` showing the email-already-taken and password-mismatch states (per `references/states.md`'s "screenshot the worst state" rule), but that's a separate task.
- **No filler hero copy.** No *"Join thousands of teams"*, no fabricated metrics, no *"Elevate your workflow"*. The subtitle is *"Takes about 30 seconds."* — useful, honest, short.
- **No mobile or tablet variant frames** unless the project's `design-system/` declares per-breakpoint frames as the convention. If it does, I'd add `SignupPage_Mobile` (390×844) and `SignupPage_Tablet` (768×1024) as siblings, with the card filling the viewport on mobile and gaining its margins back on tablet. I'd surface this choice to the user before making the second / third frame.

## Step 6 — Verify (structural-first ladder)

After the `batch_design` call returns:

1. **Rung 1.** Read the response. If any op failed, fix and retry. Most likely failure modes: `descendants` key doesn't match the library's actual child ids (I'd `batch_get` the `Input` component to read its real structure and adjust); or I tried `width: "100%"` instead of `"fill_container"`.

2. **Rung 2.** `snapshot_layout({ parentId: "<page id>", maxDepth: 4 })`. What I'd check:
   - Card is centred horizontally and vertically inside the 1440×900 page (page's `justifyContent: center` + `alignItems: center` should land it dead-centre).
   - Card width is 440. If it's wider, the field stack pushed past the padding — fix the field widths.
   - `FieldStack` has 16px (`$space-4`) gap between siblings; outer card has 24px (`$space-5`) gap between blocks.
   - The submit button's height is ≥ 44px (hit target rule from SKILL accessibility checks). If the `ButtonPrimary` component's default is shorter, that's a library issue I'd surface.
   - The checkbox row uses `alignItems: start` so the checkbox aligns with the first line of long-wrapping label text, not the centre.

3. **Rung 3.** `batch_get({ nodeIds: ["<submit id>", "<emailField id>", "<pwdField id>"] })`. What I'd check:
   - Submit button's `fill` resolves to `$primary` (variable name, not a raw hex).
   - Email field's `descendants.input.type` is `"email"` (so the engineer wires the right input mode).
   - Password field's `descendants.input.type` is `"password"`.
   - Helper text on the password field has the correct content.
   - Each field's `context` is populated as I wrote it.

4. **Rung 4.** `get_screenshot({ nodeId: "<page id> or <card id>" })` — scoped to the smallest meaningful subtree. **One screenshot, not two.** I'd scope it to the card if I just want to verify the form lockup; to the page if I want to confirm the card sits centred on the surface. I would not screenshot in dark mode unless I'd specifically used mode-conditional raw colours (I didn't — everything is variables, so the variable system guarantees both modes hold up).

   Scan order for the screenshot:
   1. Layout integrity — card on canvas, no overflow.
   2. Spacing rhythm — the 16/24/32 gap stack reads.
   3. Type rhythm — title is clearly larger than labels; helper text is smaller and muted.
   4. Contrast — title and labels pass against `$surfaceMuted`; the primary button label passes against `$primary`. (If `$primary` is a low-saturation brand colour, I'd verify white text on it specifically.)
   5. Component fidelity — every field is a `ref`, the button is a `ref`, no hand-built lookalikes.

If the structural snapshot already showed everything I needed and the design-system tokens guarantee theme correctness, I'd skip the screenshot entirely on the cheap-side and only screenshot at final sign-off.

## Step 7 — Verify discipline before declaring done

Quick pass against the SKILL non-negotiables:

- **Naming** — every node has a PascalCase semantic name. ✓
- **Context** — every non-trivial node has a one-sentence `context`. ✓
- **Components first** — five `ref`s into the library for the five inputs + button + checkbox + sign-in link. Only the page, card, field stack, terms row, sign-in row, divider, logo, title, subtitle are primitives — and each of those is genuinely structural. ✓
- **Themes** — all colours bound to variables that have light/dark values. ✓
- **Responsive** — desktop frame at 1440×900. If the project convention is per-breakpoint frames I'd add mobile + tablet as siblings; if it's single-fluid I'd verify the card holds together when the parent resizes. I'd surface this to the user as part of the report, not assume.
- **Accessibility** — submit button height ≥ 44px (verified at rung 2); colour is never the only signal (every form field will use the library's error-state combo of red border + alert icon when needed); names map to roles (`SubmitButton`, `EmailField`, `TermsCheckbox`); the `Input` component owns its focus state via `theme.state: focus` — if I look at `batch_get` and the library doesn't have a focus state, that's a library bug to surface, not something to ship around.

## Step 8 — Report to the user

> *"Done. Single `SignupPage` (desktop, 1440×900) on `$surface`, with a centred `SignupCard` (440 wide). The card holds a small logo, *'Create your account'* title, a one-sentence subtitle (*'Takes about 30 seconds.'*), then a vertical stack of five fields — Full name, Email, Password (with helper text on character mix), Confirm password, and a Terms checkbox with *'I agree to'* language. The CTA is a full-width `ButtonPrimary` reading *'Create account'*; below it, a footer row with *'Already have an account?'* + a Sign-in link. Every field is a `ref` to your `Input` library component with `descendants` overrides for label and placeholder; submit is a `ButtonPrimary` ref; checkbox is a `Checkbox` ref. Validation timing is documented in each field's `context`: email shape on blur + uniqueness on submit; passwords cross-check on submit; submit button stays disabled until all fields are non-empty AND the Terms box is checked. Verified structurally with `snapshot_layout` and one final screenshot scoped to the card. Two notes: (1) I haven't added the error-state visualisation to the canvas — happy to add a sibling `SignupPage_Errors` frame showing the *'email already taken'* and *'passwords don't match'* states if you want them on the design itself rather than just in the field contexts. (2) This is a desktop frame only; tell me if you want me to add tablet (768) and mobile (390) siblings."*

That's the artifact for this prompt: one frame, one card, all components from the library, theme-aware, verified structurally first, with explicit follow-up offers rather than silently expanding the scope.

## File written

`/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-8-form-design-discipline/old_skill/outputs/response.md` ✓
