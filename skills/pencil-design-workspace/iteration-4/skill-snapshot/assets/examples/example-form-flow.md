# Example: design a multi-step signup with email verification

A worked walkthrough of the seven-step workflow for the prompt:

> *"Design a signup flow with email + password, then email verification, then a welcome confirmation page."*

Assume: Pencil desktop running, no `.pen` open, repo has a `design-system/` folder with `tokens.md`, `voice.md`, `patterns.md`, `states.md`, and a `design/system.lib.pen` library that includes `Input`, `ButtonPrimary`, `LinkText`.

This example exercises:

- Three sibling top-level frames at desktop breakpoint (1440×900), one per step.
- Validation states via `descendants` overrides on the `Input` ref (the focused-with-error edge case).
- `find_empty_space_on_canvas` to place the three frames neatly side-by-side.
- A confirmation step with a different lockup than steps 1–2.
- Cross-references: [`references/flows.md`](../../references/flows.md) for back-stack, validation timing, and confirmation anatomy; [`assets/design-system/patterns.md`](../design-system/patterns.md) § Auth flow / § Onboarding flow for the layout shapes; [`assets/design-system/voice.md`](../design-system/voice.md) for copy.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Result: succeeds. No active document.

## Step 2 — Locate context

- No `.pen` open.
- No selection.
- `design-system/` exists with the relevant files.

## Step 3 — Load guidelines + inventory components

Read `design-system/README.md`, then:

- `design-system/patterns.md` — § Auth flow gives the centered-card shape; § Onboarding flow gives the wizard shape with progress indicator (the welcome step rhymes with the onboarding-confirmation page).
- `design-system/voice.md` — § Error messages (the *what happened. what to do.* shape) and § Buttons & CTAs (specific verbs).
- `design-system/states.md` — confirms `Input` requires error and loading variants.

The skill's [`references/flows.md`](../../references/flows.md) is the playbook for validation timing, back-stack across the three screens, and confirmation-step anatomy. [`references/states.md`](../../references/states.md) covers the focus-with-error edge case I'll need on the password field.

Call `get_guidelines()` to confirm the live category list, then load `Web App`.

Inventory the library:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Library contains `Input`, `ButtonPrimary`, `ButtonSecondary`, `LinkText`. The `Input` component declares `default`, `hover`, `focus`, `error`, and `success` variants — confirmed by inspecting its `descendants`.

## Step 4 — Plan (told to user)

> *"I'll create three sibling top-level frames at desktop breakpoint (1440×900): `Signup_Step1_Email`, `Signup_Step2_Verify`, and `Signup_Step3_Welcome`. Step 1 is the auth-card shape from your patterns — email + password + ToS checkbox + Continue button, with a stepper showing 1-of-3 at the top. I'll show the email field's error state on the canvas (focused with a 'looks already taken' message) so the design covers validation. Step 2 is a slimmer card with a 6-digit verification code input (six narrow boxes), the user's email, and a Resend link. Step 3 is a different lockup — closer to your onboarding confirmation pattern: large checkmark icon, *'You're in.'* headline, *'Go to dashboard'* CTA. All three pages share a stepper at the top. Components: `Input` (instances of the email and password from your library), `ButtonPrimary`, `LinkText` for *'Resend'* and *'Already have an account?'*. Theme-aware via your existing variables."*

## Step 4.5 — Open the document

Since no `.pen` is open:

```
open_document({ path: "new" })
```

Note the document root id — call it `doc`. Declare the `mode` theme axis up front, then add the library import:

```
U("doc", { themes: { mode: ["light", "dark"] } })
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
```

## Step 4.7 — Place the three frames

Three frames side-by-side need ~3 × 1440 + gaps = 4400+ pixels of horizontal canvas. Pick anchors:

```
find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })
```

Returns `(x1, y1)`. The other two frames will be at `(x1 + 1520, y1)` and `(x1 + 3040, y1)` — 1440 wide each plus a 80px gutter between, since the frames represent sequential steps the engineer can scrub.

## Step 5a — First batch_design (Step 1: Email + Password)

```
page1=I("doc", { type: "frame", name: "Signup_Step1_Email", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x1>, y: <y1>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "solid_color", color: "$surface" }] })
stepper=I(page1, { type: "frame", name: "Stepper", layout: "horizontal", gap: "$space-2", padding: "$space-4", alignItems: "center" })
step1Dot=I(stepper, { type: "ellipse", name: "Step1Dot", width: 8, height: 8, fill: [{ type: "solid_color", color: "$primary" }] })
step1Bar=I(stepper, { type: "rectangle", name: "Step1Bar", width: 32, height: 2, fill: [{ type: "solid_color", color: "$primary" }] })
step2Dot=I(stepper, { type: "ellipse", name: "Step2Dot", width: 8, height: 8, fill: [{ type: "solid_color", color: "$border" }] })
step2Bar=I(stepper, { type: "rectangle", name: "Step2Bar", width: 32, height: 2, fill: [{ type: "solid_color", color: "$border" }] })
step3Dot=I(stepper, { type: "ellipse", name: "Step3Dot", width: 8, height: 8, fill: [{ type: "solid_color", color: "$border" }] })
card=I(page1, { type: "frame", name: "AuthCard", layout: "vertical", gap: "$space-4", padding: "$space-8", width: 400, cornerRadius: "$radiusLg", fill: [{ type: "solid_color", color: "$surfaceMuted" }], stroke: { thickness: 1, fill: "$border" } })
title=I(card, { type: "text", name: "Title", text: "Create your account", fontSize: "$text2xl", fontWeight: 700 })
sub=I(card, { type: "text", name: "Subtitle", text: "Step 1 of 3 — your details.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
email=I(card, { type: "ref", ref: "Input", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com", value: "alex@startup.io" }, error: { text: "That email is already registered. Try signing in instead." } }, theme: { state: "error" } })
pwd=I(card, { type: "ref", ref: "Input", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "8+ characters" }, helperText: { text: "Mix letters, numbers, and a symbol." } } })
tos=I(card, { type: "frame", name: "ToS", layout: "horizontal", gap: "$space-2", alignItems: "start" })
tosCheckbox=I(tos, { type: "ref", ref: "Checkbox", descendants: { label: { text: "I agree to the Terms and Privacy Policy." } } })
continue=I(card, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Continue" } } })
signinLink=I(card, { type: "ref", ref: "LinkText", descendants: { label: { text: "Already have an account? Sign in" } } })
```

15 ops. Note:

- The `email` field is shown in its **error state** — the SKILL.md aesthetic-defaults discipline (and `references/states.md`'s "screenshot the worst state" guidance) says the error-paired-with-focus is what the design needs to verify, not a clean default.
- The error message uses the `voice.md` two-part template (*what happened. what to do.*).
- The `Continue` button's verb is specific (`Continue`, not `Submit`).
- The TOS checkbox text starts with *"I agree"* — clear consent language.

## Step 6a — Verify structure (Step 1)

```
snapshot_layout({ parentId: "page1", maxDepth: 3 })
```

Check: stepper is centered above the card. Card width 400, internal gap 16. Email field's error state has the inline message visible (not collapsed). Password field has helper text. Total card height fits within 900-pixel viewport with vertical centering.

If the stepper is off-center (often: it's left-anchored because the parent's `justifyContent` only applies on the main axis), fix structurally:

```
U("stepper", { width: "fit_content" })   // stepper hugs its content; parent's alignItems: center now centers it horizontally
```

## Step 5b — Second batch_design (Step 2: Verify code)

```
page2=I("doc", { type: "frame", name: "Signup_Step2_Verify", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x1 + 1520>, y: <y1>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "solid_color", color: "$surface" }] })
stepper2=I(page2, { type: "frame", name: "Stepper", layout: "horizontal", gap: "$space-2", padding: "$space-4", alignItems: "center", width: "fit_content" })
s2dot1=I(stepper2, { type: "ellipse", name: "Step1Dot", width: 8, height: 8, fill: [{ type: "solid_color", color: "$primary" }] })
s2bar1=I(stepper2, { type: "rectangle", name: "Step1Bar", width: 32, height: 2, fill: [{ type: "solid_color", color: "$primary" }] })
s2dot2=I(stepper2, { type: "ellipse", name: "Step2Dot", width: 8, height: 8, fill: [{ type: "solid_color", color: "$primary" }] })
s2bar2=I(stepper2, { type: "rectangle", name: "Step2Bar", width: 32, height: 2, fill: [{ type: "solid_color", color: "$border" }] })
s2dot3=I(stepper2, { type: "ellipse", name: "Step3Dot", width: 8, height: 8, fill: [{ type: "solid_color", color: "$border" }] })
card2=I(page2, { type: "frame", name: "AuthCard", layout: "vertical", gap: "$space-4", padding: "$space-8", width: 400, cornerRadius: "$radiusLg", fill: [{ type: "solid_color", color: "$surfaceMuted" }], stroke: { thickness: 1, fill: "$border" } })
title2=I(card2, { type: "text", name: "Title", text: "Check your email", fontSize: "$text2xl", fontWeight: 700 })
sub2=I(card2, { type: "text", name: "Subtitle", text: "We sent a 6-digit code to alex@startup.io.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
codeRow=I(card2, { type: "frame", name: "CodeRow", layout: "horizontal", gap: "$space-2", justifyContent: "center" })
d1=I(codeRow, { type: "frame", name: "Digit1", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d2=I(codeRow, { type: "frame", name: "Digit2", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d3=I(codeRow, { type: "frame", name: "Digit3", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d4=I(codeRow, { type: "frame", name: "Digit4", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d5=I(codeRow, { type: "frame", name: "Digit5", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d6=I(codeRow, { type: "frame", name: "Digit6", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
verify=I(card2, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Verify email" } } })
resend=I(card2, { type: "ref", ref: "LinkText", descendants: { label: { text: "Resend code" } } })
```

19 ops. The 6-digit code input is custom — six small frames in a horizontal row. The component library doesn't have a `CodeInput` yet; this is a candidate to surface for the library at the end of the task.

## Step 6b — Verify structure (Step 2)

```
snapshot_layout({ parentId: "page2", maxDepth: 3 })
```

Check: code row is centered, six 48×56 cells with 8px gaps total ~56px height + 5×8px = 328px wide. Card holds together at 400px width.

## Step 5c — Third batch_design (Step 3: Welcome)

The confirmation page is structurally different. Larger icon, no stepper indicator (or a fully-completed stepper for visual closure), single primary action.

```
page3=I("doc", { type: "frame", name: "Signup_Step3_Welcome", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x1 + 3040>, y: <y1>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "solid_color", color: "$surface" }] })
welcomeBlock=I(page3, { type: "frame", name: "WelcomeBlock", layout: "vertical", justifyContent: "center", alignItems: "center", gap: "$space-5", padding: "$space-8", width: 480 })
checkIcon=I(welcomeBlock, { type: "icon_font", name: "CheckIcon", iconName: "check-circle", iconLibrary: "lucide", fontSize: 64, fill: [{ type: "solid_color", color: "$success" }] })
welcomeTitle=I(welcomeBlock, { type: "text", name: "Title", text: "You're in.", fontSize: "$text3xl", fontWeight: 700, textAlign: "center" })
welcomeSub=I(welcomeBlock, { type: "text", name: "Subtitle", text: "We've set up your workspace. Head over and create your first project.", fontSize: "$textBase", textAlign: "center", fill: [{ type: "solid_color", color: "$textMuted" }] })
goCta=I(welcomeBlock, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Go to dashboard" } } })
```

6 ops. Confirmation copy is concise — *"You're in."* is the lead, the subtitle is one sentence, the CTA is a specific verb (*"Go to dashboard"*). No filler hero copy, no fabricated metrics, no AI clichés.

## Step 6c — Verify structure (Step 3)

```
snapshot_layout({ parentId: "page3", maxDepth: 2 })
```

Check: welcome block centered, icon-title-subtitle-CTA in vertical rhythm with `$space-5` (24px) gaps. CTA width matches its content (the `ButtonPrimary` component's default sizing).

## Step 7 — Final visual sign-off

Three pages, three screenshots. Each scoped to its page, never the doc root:

```
get_screenshot({ nodeId: "page1" })
get_screenshot({ nodeId: "page2" })
get_screenshot({ nodeId: "page3" })
```

Verify per page:

- **Page 1.** Stepper renders (1-of-3 highlighted). Email field shows error-state styling — red border, alert-circle icon, the error message *"That email is already registered. Try signing in instead."* below the input. Password field renders cleanly with helper text. Continue button uses `$primary`. ToS checkbox legible. Sign-in link at bottom.
- **Page 2.** Stepper shows 2-of-3. Email reference (*"alex@startup.io"*) is visible in the subtitle. Six code-input cells render with consistent borders. Verify button uses `$primary`. Resend link is present.
- **Page 3.** Different lockup — larger icon (`check-circle` in `$success`), `$text3xl` headline, single subtitle, single primary CTA. Reads as completion, not as another form step.

Three screenshots total — one per page.

## Step 8 — Surface candidates and notes

Two notes for the user:

1. **`CodeInput` is a candidate library component.** The six-digit code row in Step 2 is six manual frames — fine for a one-off, but a real product uses this on email verify, 2FA, and probably a few other flows. Surface it: *"The 6-digit code input on Step 2 is currently composed from primitives. Want me to promote it to your `.lib.pen` as `CodeInput` so other auth flows can use it?"*
2. **Validation timing decisions belong in `flows.md`.** Document the intended timing in the email field's `context`: *"Async unique-email check fires on blur with 400ms debounce. Error decays when user re-edits the field. Submit-time also catches server-side conflicts."* The engineer reads this and ships matching behavior.

## Final report to user

> *"Done. Three sibling pages — `Signup_Step1_Email`, `Signup_Step2_Verify`, `Signup_Step3_Welcome` — placed side-by-side in empty canvas at desktop dimensions. Step 1 shows an auth-card with email (error state visible — *'already registered'*) and password fields, ToS checkbox, Continue CTA, and a stepper at top showing 1-of-3 progress. Step 2 is a slimmer verification card with 6 code-input cells, Verify CTA, and a Resend link. Step 3 is the welcome confirmation — larger check icon, *'You're in.'* headline, single CTA. All bound to your existing `tokens.md` variables and `mode` theme axis. Verified structurally with `snapshot_layout` per page, then one screenshot per page for sign-off. Two notes: the 6-digit `CodeInput` is a library candidate, and the email field's async-validation timing is documented in its `context` for the engineer."*

## What this example demonstrates

- **Three sibling top-level frames** placed side-by-side with `find_empty_space_on_canvas` — the canonical pattern for visualizing a multi-step flow.
- **Showing error state on the canvas**, not the default state — per `references/states.md` "screenshot the worst state" rule.
- **Specific verbs everywhere** (*Continue*, *Verify email*, *Resend code*, *Go to dashboard*) — never generic *Submit* / *OK* / *Confirm*.
- **A confirmation step with a different lockup** than the form steps — the welcome page rhymes with the onboarding-confirmation in `patterns.md`, not the auth-card.
- **Surfacing library candidates** without promoting unilaterally.
- **Cross-referencing the right files**: `flows.md` for validation timing and back-stack, `patterns.md` for the auth-card and confirmation lockups, `voice.md` for copy, `states.md` for the error-with-focus edge case. Don't restate them; link.

For the back-stack model across the three steps, see [`references/flows.md`](../../references/flows.md) § Back-stack & navigation model. For the auth-card layout shape, see [`assets/design-system/patterns.md`](../design-system/patterns.md) § Auth flow. For the worst-state-screenshot guidance, see [`references/states.md`](../../references/states.md) § Verification.
