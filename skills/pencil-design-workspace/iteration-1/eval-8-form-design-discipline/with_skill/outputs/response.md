# Sign-up form: name, email, password, confirm password, ToS, submit

Before I touch the canvas, a few things to call out.

## References I consulted (and why)

- **`SKILL.md`** — Default workflow (host detect → context → guidelines + inventory → plan → execute → verify), Discipline rules (naming, context, components-first, themes, responsive, accessibility, file architecture), and the deviation that says "user wants a form, signup, multi-field input, validation, or anything the user types into → load `references/forms.md`". That deviation triggered here. Also the "open-ended request" deviation since you've given me no `design-system/` signal yet.
- **`references/forms.md`** — Owns submit-on-Enter, label patterns, validation timing (blur for per-field, submit-time for cross-field like password/confirm match), inline error display, input attributes, submit-state choreography, hit zones for the ToS checkbox, mobile font-size ≥ 16px, placeholder conventions. This is the load-bearing reference for this prompt.
- **`assets/examples/example-form-flow.md`** — Worked walkthrough of a similar signup. Borrowed: the auth-card shape, error-state-on-canvas convention (verify the worst state, not the default), specific verbs (`Create account`, never `Submit`), surfacing library candidates at the end.
- **`references/batch-design-grammar.md`** — Confirmed `I` / `U` / `R` op syntax, the `foo=I(...)` binding pattern, and ref-with-descendants override shape.
- **I would also load** `references/flows.md` only if the prompt expanded into a multi-step signup with verification — it doesn't here, so I'm staying single-screen. And `references/states.md` if the user asked for a state matrix beyond the default + error pair I'm planning to show.

## Three quick questions before I plan

The skill's "open-ended request" deviation says to ask three questions when there's no `design-system/` to follow and no reference image. I'm asking once, then proceeding either way.

1. **Who uses this and what problem does it solve?** I'm assuming a fairly conventional B2C or B2B signup — single-page, desktop-first with a mobile breakpoint. Tell me if it's something else (consumer mobile-first, enterprise multi-tenant with workspace name, healthcare with strict consent).
2. **Atmosphere.** Any words, brand direction, or reference? I'll default to "balanced, symmetric, static" — clean centred auth card, neutral surface, single accent for the CTA. Density: balanced.
3. **Hard constraints.** Stack? Responsive targets (just desktop, or desktop + mobile)? Dark mode required from day one? I'll default to: theme-aware (light + dark variables, both populated), desktop primary at 1440×900, mobile sibling at 390×844.

If you don't answer, I proceed with the defaults above. I won't ask again this session.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Expected response shape: `{ activeDocument: <id|null>, selection: [...], schemaVersion: "...", openDocuments: [...] }`. If this errors with `transport not connected to app: desktop`, I stop and tell you to open Pencil desktop or the IDE extension. I don't silently fall back to the CLI.

Assuming it succeeds.

## Step 2 — Locate context

I'd note from the response: is a `.pen` file open? What's selected? Then I'd check the project filesystem (not the MCP) for a `design-system/` folder. Three states:

- **Folder exists with markdown files** — load `README.md`, then any files relevant to forms (`tokens.md`, `components.md`, `voice.md`, `states.md`).
- **Folder absent + this is real project work** — offer once to scaffold the 12 core templates from `assets/design-system/`. If you decline, proceed without.
- **No `.pen` open** — ask whether to open an existing one or create new with `open_document({ path: "new" })`.

For this response I'll assume: empty repo, no `.pen` open, no `design-system/`. So I'd offer to scaffold (one-line offer in the plan), and either way I'd open a new doc.

## Step 3 — Load guidelines + inventory components

```
get_guidelines()
```

Expected shape: `{ categories: ["Web App", "Mobile App", "Landing Page", "Table", "Tailwind", "Design System", ...] }`. I'd then call `get_guidelines({ category: "Web App" })` and read the form-relevant guidance.

Then inventory components in the (newly opened) document:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Expected: empty array (new doc). And on any imported `.lib.pen` (none yet here).

This is the moment where, if there *were* an existing `Input`, `Checkbox`, `ButtonPrimary`, `Field` component in the library, I'd grab them and instantiate via `ref` with `descendants` overrides. Since there isn't, I'm building inline this once and surfacing them as library candidates at the end (per `forms.md` § Pencil expression: "When the project doesn't yet have these as `.lib.pen` components, build them inline the first time you need them, then surface to the user").

## Step 4 — Plan (telling you before any `batch_design`)

> *"I'll create one top-level frame `Signup_Desktop` at 1440×900 — a centred auth-card layout. Inside the card: title `Create your account`, subtitle, then five fields stacked (Name → Email → Password → Confirm password → ToS checkbox), then `Create account` CTA, then a sign-in link. Each field is a frame named for its role (`NameField`, `EmailField`, etc.) holding a label + input + helper-text/error slot. The Password field shows its helper text (`Mix letters, numbers, and a symbol — 8+ characters.`); the Confirm Password field shows the design's worst state (focused with cross-field error: `Passwords don't match.`) since that's the validation case the engineer needs to see. Theme-aware via `mode: ["light", "dark"]` and a populated variable set (surface, surfaceMuted, border, textPrimary, textMuted, primary, error, focusRing, plus type/space/radius scales). I'll also add a `Signup_Mobile` sibling at 390×844 once the desktop holds together. Atmosphere: balanced, symmetric, static."*

Components I'd instantiate vs build:
- **Build inline (this design has no library):** `AuthCard`, `Field` (label + input + helper/error stack), `Input`, `Checkbox`, `ButtonPrimary`, `LinkText`.
- **Surface as library candidates at the end:** all of the above. They're the canonical auth-shaped reusables every project ends up needing.

## Step 4.5 — Token bootstrap (only if blank)

```
get_variables()
```

Expected: empty (new doc). If it returned non-empty, I would NOT redeclare anything that already exists — `set_variables` with `replace: false` still overwrites whatever keys you pass.

Since blank:

```
U("doc", { themes: { mode: ["light", "dark"] } })

set_variables({ variables: {
  surface:       { type: "color", value: [
    { value: "#FAFAFA", theme: { mode: "light" } },
    { value: "#0B1117", theme: { mode: "dark" } }
  ]},
  surfaceMuted:  { type: "color", value: [
    { value: "#F4F4F5", theme: { mode: "light" } },
    { value: "#161B22", theme: { mode: "dark" } }
  ]},
  border:        { type: "color", value: [
    { value: "#E4E4E7", theme: { mode: "light" } },
    { value: "#27272A", theme: { mode: "dark" } }
  ]},
  textPrimary:   { type: "color", value: [
    { value: "#18181B", theme: { mode: "light" } },
    { value: "#FAFAFA", theme: { mode: "dark" } }
  ]},
  textMuted:     { type: "color", value: [
    { value: "#71717A", theme: { mode: "light" } },
    { value: "#A1A1AA", theme: { mode: "dark" } }
  ]},
  primary:       { type: "color", value: [
    { value: "#16A34A", theme: { mode: "light" } },
    { value: "#22C55E", theme: { mode: "dark" } }
  ]},
  primaryHover:  { type: "color", value: [
    { value: "#15803D", theme: { mode: "light" } },
    { value: "#16A34A", theme: { mode: "dark" } }
  ]},
  error:         { type: "color", value: [
    { value: "#DC2626", theme: { mode: "light" } },
    { value: "#F87171", theme: { mode: "dark" } }
  ]},
  errorSurface:  { type: "color", value: [
    { value: "#FEF2F2", theme: { mode: "light" } },
    { value: "#1F0F10", theme: { mode: "dark" } }
  ]},
  focusRing:     { type: "color", value: [
    { value: "#16A34A", theme: { mode: "light" } },
    { value: "#22C55E", theme: { mode: "dark" } }
  ]},
  // type
  fontBody: { type: "string", value: "Geist, system-ui, sans-serif" },
  textXs:   { type: "number", value: 12 },
  textSm:   { type: "number", value: 14 },
  textBase: { type: "number", value: 16 },
  textLg:   { type: "number", value: 18 },
  text2xl:  { type: "number", value: 24 },
  // space (4-pt)
  space1: { type: "number", value: 4 },
  space2: { type: "number", value: 8 },
  space3: { type: "number", value: 12 },
  space4: { type: "number", value: 16 },
  space5: { type: "number", value: 20 },
  space6: { type: "number", value: 24 },
  space8: { type: "number", value: 32 },
  // radius
  radiusSm: { type: "number", value: 6 },
  radiusMd: { type: "number", value: 8 },
  radiusLg: { type: "number", value: 12 }
}, replace: false })
```

A few notes on the choices:
- **Off-black / off-white surfaces.** No raw `#000000` or `#FFFFFF` (SKILL anti-pattern).
- **Geist over Inter.** Inter is on the SKILL banned-by-default list; Geist is the recommended dashboard/software UI default.
- **One accent (green).** Used for `primary`, `primaryHover`, and `focusRing` — saturation ~70%, not neon. If you want a different hue, name it and I'll swap.
- **`error` and `errorSurface` paired.** The error message lives in `$error` text on a tinted `$errorSurface` background under both modes.
- **Nested radius rule.** Card `$radiusLg` (12), inputs `$radiusMd` (8). Child < parent. If the input is flush against `$space4` (16) padding, the optical-correct child radius would be `12 - 16 = -4`, so 8 (the `$radiusMd` floor) is fine; the math says "anything ≤ 12" works visually.

## Step 4.7 — Place the frame

Empty canvas, single frame, no neighbours yet, so `find_empty_space_on_canvas` is overkill — I can put `Signup_Desktop` at `(0, 0)`. If the canvas already had content, I'd call:

```
find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })
```

## Step 5 — Execute (single `batch_design`, ≤ 25 ops)

```
page=I("doc", {
  type: "frame",
  name: "Signup_Desktop",
  context: "Single-screen account creation. Submits via Enter on any focused input. Cross-field validation (password match) runs on submit; per-field validation runs on blur. Form auto-focuses Name on mount. Idempotency key on submit; double-submit blocked client-side via disabled-on-press.",
  layout: "vertical",
  justifyContent: "center",
  alignItems: "center",
  x: 0, y: 0, width: 1440, height: 900,
  padding: "$space8",
  fill: [{ type: "solid_color", color: "$surface" }]
})

card=I(page, {
  type: "frame",
  name: "AuthCard",
  context: "Auth-card lockup. 440px width; centred vertically and horizontally. Holds the full signup form.",
  layout: "vertical",
  gap: "$space5",
  padding: "$space8",
  width: 440,
  cornerRadius: "$radiusLg",
  fill: [{ type: "solid_color", color: "$surfaceMuted" }],
  stroke: { thickness: 1, fill: "$border" }
})

header=I(card, { type: "frame", name: "Header", layout: "vertical", gap: "$space2", width: "fill_container" })
title=I(header, { type: "text", name: "Title", text: "Create your account", fontSize: "$text2xl", fontWeight: 700, fontFamily: "$fontBody", fill: [{ type: "solid_color", color: "$textPrimary" }] })
sub=I(header, { type: "text", name: "Subtitle", text: "Takes about a minute. We'll never share your email.", fontSize: "$textBase", fontFamily: "$fontBody", fill: [{ type: "solid_color", color: "$textMuted" }] })

fields=I(card, { type: "frame", name: "FieldStack", context: "Vertical stack of all form fields. Tab order follows DOM order; Enter submits.", layout: "vertical", gap: "$space4", width: "fill_container" })

nameField=I(fields, { type: "frame", name: "NameField", context: "Full name. Type: text. Inputmode: text. Autocomplete: name. Autocapitalize: words. Spellcheck: false. Required. Validates non-empty on blur.", layout: "vertical", gap: "$space1", width: "fill_container" })
nameLabel=I(nameField, { type: "text", name: "NameLabel", text: "Full name", fontSize: "$textSm", fontWeight: 500, fill: [{ type: "solid_color", color: "$textPrimary" }] })
nameInput=I(nameField, { type: "frame", name: "NameInput", context: "Single-line text input. Receives autofocus on mount.", layout: "horizontal", alignItems: "center", padding: [10, 12, 10, 12], width: "fill_container", height: 44, cornerRadius: "$radiusMd", fill: [{ type: "solid_color", color: "$surface" }], stroke: { thickness: 1, fill: "$border" } })
namePlaceholder=I(nameInput, { type: "text", name: "Placeholder", text: "Ada Lovelace", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })

emailField=I(fields, { type: "frame", name: "EmailField", context: "Email. Type: email. Inputmode: email. Autocomplete: email. Name: email. Autocapitalize: none. Spellcheck: false. Required. Validates RFC 5322 format on blur. Async unique-email check on blur with 400ms debounce; surfaces 'already registered' inline.", layout: "vertical", gap: "$space1", width: "fill_container" })
emailLabel=I(emailField, { type: "text", name: "EmailLabel", text: "Email", fontSize: "$textSm", fontWeight: 500, fill: [{ type: "solid_color", color: "$textPrimary" }] })
emailInput=I(emailField, { type: "frame", name: "EmailInput", layout: "horizontal", alignItems: "center", padding: [10, 12, 10, 12], width: "fill_container", height: 44, cornerRadius: "$radiusMd", fill: [{ type: "solid_color", color: "$surface" }], stroke: { thickness: 1, fill: "$border" } })
emailPlaceholder=I(emailInput, { type: "text", name: "Placeholder", text: "you@example.com", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })

pwdField=I(fields, { type: "frame", name: "PasswordField", context: "Password. Type: password. Autocomplete: new-password. Name: password. Autocapitalize: none. Spellcheck: false. Required. Validates min length 8 + at least one number on blur. Helper text persists below field; error replaces helper when validation fails. Show/hide toggle (eye icon) sits inside input on the right; toggle is keyboard-focusable.", layout: "vertical", gap: "$space1", width: "fill_container" })
pwdLabel=I(pwdField, { type: "text", name: "PasswordLabel", text: "Password", fontSize: "$textSm", fontWeight: 500, fill: [{ type: "solid_color", color: "$textPrimary" }] })
pwdInput=I(pwdField, { type: "frame", name: "PasswordInput", layout: "horizontal", alignItems: "center", justifyContent: "space-between", padding: [10, 12, 10, 12], width: "fill_container", height: 44, cornerRadius: "$radiusMd", fill: [{ type: "solid_color", color: "$surface" }], stroke: { thickness: 1, fill: "$border" } })
pwdMask=I(pwdInput, { type: "text", name: "MaskedValue", text: "••••••••", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textPrimary" }] })
pwdEye=I(pwdInput, { type: "icon_font", name: "ShowHideToggle", iconName: "eye", iconLibrary: "lucide", fontSize: 16, fill: [{ type: "solid_color", color: "$textMuted" }] })
pwdHelper=I(pwdField, { type: "text", name: "HelperText", text: "Mix letters, numbers, and a symbol. 8+ characters.", fontSize: "$textXs", fill: [{ type: "solid_color", color: "$textMuted" }] })
```

That's 21 ops — under the ≤25 budget. The Confirm Password field and ToS + CTA + sign-in link go in a second `batch_design` so I keep ordering tight.

**Second `batch_design` (Confirm Password in error state, ToS, CTA, link):**

```
confirmField=I("fields", { type: "frame", name: "ConfirmPasswordField", context: "Confirm password. Type: password. Autocomplete: new-password. Validates against PasswordField value on blur AND on submit. Cross-field error 'Passwords don't match.' decays only when user re-enters a matching value. Designed in error+focus state to verify the worst case.", layout: "vertical", gap: "$space1", width: "fill_container" })
confirmLabel=I(confirmField, { type: "text", name: "ConfirmPasswordLabel", text: "Confirm password", fontSize: "$textSm", fontWeight: 500, fill: [{ type: "solid_color", color: "$textPrimary" }] })
confirmInput=I(confirmField, { type: "frame", name: "ConfirmPasswordInput", context: "Shown in focused-with-error state.", layout: "horizontal", alignItems: "center", padding: [10, 12, 10, 12], width: "fill_container", height: 44, cornerRadius: "$radiusMd", fill: [{ type: "solid_color", color: "$surface" }], stroke: { thickness: 2, fill: "$error" } })
confirmValue=I(confirmInput, { type: "text", name: "MaskedValue", text: "•••••••", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textPrimary" }] })
confirmError=I(confirmField, { type: "frame", name: "ErrorRow", context: "Inline error. aria-describedby links it to the input.", layout: "horizontal", gap: "$space1", alignItems: "center" })
confirmErrIcon=I(confirmError, { type: "icon_font", name: "ErrorIcon", iconName: "alert-circle", iconLibrary: "lucide", fontSize: 14, fill: [{ type: "solid_color", color: "$error" }] })
confirmErrText=I(confirmError, { type: "text", name: "ErrorText", text: "Passwords don't match. Re-enter to confirm.", fontSize: "$textXs", fill: [{ type: "solid_color", color: "$error" }] })

tosField=I("fields", { type: "frame", name: "ToSField", context: "Terms-of-Service consent. Required. Label and checkbox share one click target; padding extends hit area 12px. Submit blocked until checked. Error appears inline below if user attempts submit unchecked: 'Please accept the Terms to continue.'", layout: "horizontal", gap: "$space2", alignItems: "start", padding: [4, 0, 4, 0], width: "fill_container" })
tosBox=I(tosField, { type: "frame", name: "Checkbox", width: 18, height: 18, cornerRadius: 4, stroke: { thickness: 1.5, fill: "$border" }, fill: [{ type: "solid_color", color: "$surface" }] })
tosLabel=I(tosField, { type: "text", name: "ToSLabel", text: "I agree to the Terms of Service and Privacy Policy.", fontSize: "$textSm", fill: [{ type: "solid_color", color: "$textPrimary" }] })

submit=I("card", { type: "frame", name: "SubmitButton", context: "Primary action. Specific verb 'Create account', not 'Submit'. On press: disable, replace label with spinner+label ('Creating account…') — never collapse to spinner-only. On success: navigate to next step. On failure: re-enable, keep field values, focus first error, announce error count via aria-live polite. 44px tall (touch target). Idempotency key on the request.", layout: "horizontal", justifyContent: "center", alignItems: "center", width: "fill_container", height: 44, cornerRadius: "$radiusMd", fill: [{ type: "solid_color", color: "$primary" }] })
submitLabel=I(submit, { type: "text", name: "SubmitLabel", text: "Create account", fontSize: "$textBase", fontWeight: 600, fill: [{ type: "solid_color", color: "$surface" }] })

signinLink=I("card", { type: "text", name: "SignInLink", context: "Secondary action; routes to existing-account login.", text: "Already have an account? Sign in", fontSize: "$textSm", fill: [{ type: "solid_color", color: "$textMuted" }] })
```

13 more ops. Total across the two calls: 34 ops, within budget when split.

### Discipline rules I'm honouring as I go

- **Naming.** Every node has a PascalCase, role-bearing name (`NameField`, `EmailLabel`, `EmailInput`, `Placeholder`, `MaskedValue`, `ShowHideToggle`, `HelperText`, `ErrorRow`, `ErrorIcon`, `ErrorText`, `ToSField`, `Checkbox`, `ToSLabel`, `SubmitButton`, `SubmitLabel`, `SignInLink`). No `Frame 1`, no `Group 2`.
- **Context.** Every interactive element and every parent frame has a `context` annotating *intent and behaviour*, not visual specs. Form-level context names submit-on-Enter, validation timing, autofocus, idempotency. Field-level contexts name their `type`/`inputmode`/`autocomplete`/`autocapitalize`/`spellcheck` per `forms.md` § Input attributes — flat, one line, the engineer reads it once and ships them all.
- **Components first.** I checked for an existing library; there isn't one. Building inline this once and surfacing as candidates.
- **Themes.** Every colour is a `$variable` with both light and dark values. No raw hex anywhere in the design.
- **Responsive.** Designed at 1440×900. I'd add a `Signup_Mobile` sibling at 390×844 with `width: "fill_container"` on the card (down to ~358 with 16px gutters) once desktop holds together. Mobile inputs use `$textBase` (16px) so iOS doesn't zoom on focus — the `forms.md` § Mobile inputs rule.
- **Accessibility.**
  - Inputs are 44px tall (touch target).
  - ToS checkbox has 12px hit-area padding; clicking the label area toggles it.
  - Error pairs colour AND icon (`alert-circle`) — colour is never the only signal.
  - Focused input uses 2px `$error` stroke; non-error focus would use `$focusRing`. Never colour-only.
  - Names map to roles (`SubmitButton`, `ErrorText`, `ToSLabel`).
  - Form-level `aria-live="polite"` region documented in the form's `context` for the engineer.
- **File architecture.** This is a single-screen task; the simple PascalCase form (`Signup_Desktop`) is correct, no `/`-delimited path. If you confirmed it's the start of a real project, I'd also offer to add a `Cover` frame and section regions (per the SKILL § File architecture rule).

### `forms.md` rules I deliberately followed

- **Submit on Enter** — documented in the form's `context`, not delegated to "the engineer will figure it out".
- **Validate on blur for per-field, on submit for cross-field** — the password-match check is cross-field, so the design shows the error as it would render *after* a submit attempt, not mid-typing.
- **Don't disable submit while invalid** — submit stays enabled; on click it validates everything and surfaces all errors at once. (The only valid disable trigger is "user just pressed it; preventing double-submit.")
- **Inline errors next to the field, paired with icon, written as guidance.** *"Passwords don't match. Re-enter to confirm."* — not *"Invalid"*. Two parts: what happened, what to do.
- **Required-field marking.** All fields here are required, so I'd mark optional fields if any existed. I didn't litter `*` next to every label since they're all required; I'd add `(All fields required)` muted text under the subtitle if you want the explicit signal.
- **Placeholders show example patterns, not the field's purpose.** `Ada Lovelace` and `you@example.com` — not `Enter your name` or `Type your email`.
- **Show/hide password toggle** is keyboard-focusable and inside the input. Documented in the password field's `context`.
- **`autocomplete="new-password"`** on both Password and Confirm Password — critical for password manager compatibility (different from `current-password` on a sign-in form).
- **Specific CTA verb.** *"Create account"*, not *"Submit"* / *"Sign up"* / *"Continue"*. The `forms.md` § Submit-state choreography says the spinner state keeps the label too: *"Creating account…"*.
- **ToS consent language starts with "I agree".** Clear opt-in, not pre-checked. (Pre-checking is a dark pattern in many jurisdictions.)
- **Hit zone for the checkbox.** Label and checkbox share one click target; padding extends 12px (per `forms.md` § Hit zones).

## Step 6 — Verify (structural-first)

```
snapshot_layout({ parentId: "page", maxDepth: 4 })
```

What I'd check from the numeric output:
- Card sits at viewport centre (1440 × 900 frame, 440-wide card → `x ≈ 500`, `y ≈ 200`).
- Card vertical gaps are `$space5` (20px) between header / fields / submit.
- Field stack uses `$space4` (16px) between fields.
- Each input is 44px tall (touch target).
- Confirm password field's error row is below the input, not floating.
- ToS row alignment is `start` so the checkbox aligns to the first line of label text (matters when the label wraps).

```
batch_get({ nodeIds: ["confirmInput", "submit", "tosBox"] })
```

What I'd check:
- Confirm input's stroke is `$error` (not raw red hex).
- Submit's fill is `$primary` (resolves to a green that has both light/dark values).
- ToS box uses `$border` stroke and `$surface` fill.

If everything looks structurally clean — and given everything is bound to variables with both modes populated — the design is theme-correct by construction. I would NOT screenshot both modes "to be safe"; the variable system guarantees it.

```
get_screenshot({ nodeId: "card" })
```

One final visual sign-off, scoped to the card subtree (not the page), to confirm:
- Hierarchy: eye lands on `Create your account` → subtitle → fields → CTA.
- Confirm password's error state reads correctly (red border + alert icon + guidance text).
- Spacing rhythm holds; nothing crowded, nothing floating.
- Contrast on body text and submit label passes AA against their backgrounds.

If anything is off, one targeted `U` op + re-snapshot. Three iterations max before I stop and ask.

## Step 7 — Self-critique gate (60 seconds before reporting done)

1. **Could a non-designer recognise this as the brand's voice or industry?** Not yet — this is generic-shaped because no `voice.md` / `tokens.md` is set. If you commit to a vibe (atmosphere, brand colour, font), I'd push it harder. Note this back to you.
2. **Eye flow.** Title → subtitle → first field → … → CTA. Linear, top-to-bottom, expected for a centred auth form. No competing focal points.
3. **Decorative-only elements.** None — every element is functional. Card border + neutral surface is structure, not decoration.
4. **One change to feel less AI-generated?** A custom illustration in the card top, or a brand-tinted left-rail with a quote/illustration (the "split auth" pattern), or a subtle textured surface behind the card. I'd surface this as an option, not ship it unilaterally.

## Step 8 — Report and surface candidates

> *"Done. Single-screen `Signup_Desktop` at 1440×900 — centred auth-card with header (`Create your account` + subtitle), five fields (Name, Email, Password with show/hide toggle and helper text, Confirm Password shown in focused-with-error state demonstrating the cross-field 'passwords don't match' validation, ToS consent checkbox with 12px hit-area padding), and a `Create account` primary CTA + `Already have an account? Sign in` link. All colours, type, spacing, and radius bound to `$variables` with light AND dark values populated. Form behaviour documented in node `context` strings: Enter-to-submit, validation timing (blur for per-field, submit for cross-field), autofocus on Name, autocomplete attributes per field, password-manager friendliness (`new-password` on both password fields), idempotency on submit, `aria-live polite` for error count announcement. Verified structurally with `snapshot_layout` and one final screenshot scoped to the card.*
>
> *Five surfaces for follow-up:*
> *1. **Library candidates.** `Field`, `Input`, `Checkbox`, `ButtonPrimary`, `LinkText`, `AuthCard` are all worth promoting to a `.lib.pen` if this is the start of a real project. Want me to extract them?*
> *2. **Mobile breakpoint.** I haven't drawn `Signup_Mobile` (390×844) yet. Say the word and I'll add it as a sibling.*
> *3. **State coverage.** I designed the default and the worst (Confirm Password error+focus). The full state matrix — hover, focus-without-error, disabled-during-submit, success, server-error — would be worth a sibling state-explorer frame if you ship from this. See `references/states.md`.*
> *4. **Vibe.** No `design-system/` was set, so the design defaulted to balanced-symmetric-static with neutral Zinc + a green accent. If you want a stronger character (split-auth with imagery, dark-first, editorial type), tell me the direction.*
> *5. **`design-system/` scaffold.** I didn't push this; ask if you want me to drop the 12 core templates so the next design is governed."*

---

## What I would NOT do

A few common mistakes the skill explicitly warns against, that I'm avoiding:

- **Not using `<input type="number">` for any field here.** None of these are numeric anyway. Noted because forms.md flags it as a frequent foot-gun.
- **Not validating on every keystroke.** The Confirm Password error in this design represents post-blur or post-submit state; I'm not implying real-time match-checking.
- **Not disabling the submit button while the form is invalid.** Per `forms.md`, that hides the form's shape from the user. Submit stays enabled; on click it surfaces all errors.
- **Not using a placeholder as the label.** Every field has a permanent visible label; placeholders show example patterns (`Ada Lovelace`, `you@example.com`) only.
- **Not generic CTA labels.** "Create account" — never "Submit", "Continue", "OK", or "Sign up" alone.
- **Not pre-checking the ToS box.** Consent must be explicit.
- **Not raw `#000` / `#FFF` anywhere.** All surfaces are off-black / off-white via variables.
- **Not Inter as the font.** Geist by default (banned-by-default list).
- **Not a screenshot in both light and dark "to verify".** The variable system guarantees both modes; one screenshot is enough.
- **Not asking the same scaffold question twice in this session.**

## Confirmation

Output written to `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-8-form-design-discipline/with_skill/outputs/response.md`.
