# Example: design a multi-step signup with email verification

A worked walkthrough of the seven-step workflow for the prompt:

> *"Design a signup flow with email + password, then email verification, then a welcome confirmation page."*

Assume: Pencil desktop running, no `.pen` open, repo has a `design-system/` folder with `tokens.md`, `voice.md`, `patterns.md`, `states.md`, and a `design/system.lib.pen` library that includes `Input`, `ButtonPrimary`, `LinkText`.

---

## Step 1: Detect host

```
get_editor_state({ include_schema: false })
```

Result: succeeds. No active document.

## Step 2: Locate context

- No `.pen` open.
- No selection.
- `design-system/` exists with the relevant files.

## Step 3: Load guidelines + inventory components

Read `design-system/README.md`, then:

- `design-system/patterns.md`: § Auth flow gives the centred-card shape; § Onboarding flow gives the wizard shape with progress indicator (the welcome step rhymes with the onboarding-confirmation page).
- `design-system/voice.md`: § Error messages (the *what happened. what to do.* shape) and § Buttons & CTAs (specific verbs).
- `design-system/states.md`: confirms `Input` requires error and loading variants.

The skill's [`references/flows.md`](../../references/flows.md) is the playbook for validation timing, back-stack across the three screens, and confirmation-step anatomy. [`references/states.md`](../../references/states.md) covers the focus-with-error edge case on the password field.

Call `get_guidelines()` to confirm the live category list, then load `Web App`.

Inventory the library:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Components: `Input`, `ButtonPrimary`, `ButtonSecondary`, `LinkText`. The `Input` component declares `default`, `hover`, `focus`, `error`, and `success` variants.

## Step 4: Plan

Archetype: `conversion-focused-saas`. This is an onboarding signup funnel; the three-step flow is the product's primary conversion path.

**Verifiable brief:**

- **What success looks like:** three frames side by side. Pages 1 and 2 look like auth cards: centred card with a stepper at the top. Page 3 breaks the card shape completely, showing just a centred vertical block with an oversized icon and a single CTA. The break in structure at page 3 makes the completion moment legible at a glance.
- **Signature element:** `WelcomeBlock` on page 3 has no card frame. It is a bare vertical layout with `fill: "transparent"`, no `stroke`, no `cornerRadius`. Nothing wrapped around the content.
- **Microcopy register:** says "Continue", "Verify email", "You're in.", "Go to dashboard"; would never say "Submit", "OK", "Congratulations! Your account is ready."

> *"I'll create three sibling top-level frames at 1440×900: `Signup_Step1_Email`, `Signup_Step2_Verify`, `Signup_Step3_Welcome`. Step 1 is the auth-card shape from patterns.md with email + password fields, a dot stepper showing 1-of-3, and the email field in error state on the canvas. Step 2 is a slimmer card with a 6-digit code input. Step 3 breaks the card shape: icon, title, single CTA, no card wrapper. Components: `Input`, `ButtonPrimary`, `LinkText`. Archetype: conversion-focused-saas."*

## Step 4.5: Open document

```
open_document({ path: "new" })
```

Note the document root id; call it `doc`. Declare the mode axis and library import:

```
U("doc", { themes: { mode: ["light", "dark"] } })
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
```

## Step 4.7: Place the three frames

Three frames at 1440px need ~4400px of horizontal canvas. Pick anchor coordinates:

```
find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })
```

Returns `(x1, y1)`. The other two frames go at `(x1 + 1520, y1)` and `(x1 + 3040, y1)`: 1440px each with an 80px gutter between, so the engineer can scrub the sequence left-to-right.

## Step 5a: First batch_design (Step 1: email + password)

```
page1=I("doc", { type: "frame", name: "Signup_Step1_Email", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x1>, y: <y1>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "color", color: "$surface" }] })
stepper=I(page1, { type: "frame", name: "Stepper", layout: "horizontal", gap: "$space-2", padding: "$space-4", alignItems: "center", width: "fit_content" })
step1Dot=I(stepper, { type: "ellipse", name: "Step1Dot", width: 8, height: 8, fill: [{ type: "color", color: "$primary" }] })
step1Bar=I(stepper, { type: "rectangle", name: "Step1Bar", width: 32, height: 2, fill: [{ type: "color", color: "$primary" }] })
step2Dot=I(stepper, { type: "ellipse", name: "Step2Dot", width: 8, height: 8, fill: [{ type: "color", color: "$border" }] })
step2Bar=I(stepper, { type: "rectangle", name: "Step2Bar", width: 32, height: 2, fill: [{ type: "color", color: "$border" }] })
step3Dot=I(stepper, { type: "ellipse", name: "Step3Dot", width: 8, height: 8, fill: [{ type: "color", color: "$border" }] })
card=I(page1, { type: "frame", name: "AuthCard", layout: "vertical", gap: "$space-4", padding: "$space-8", width: 400, cornerRadius: "$radiusLg", fill: [{ type: "color", color: "$surfaceMuted" }], stroke: { thickness: 1, fill: "$border" } })
title=I(card, { type: "text", name: "Title", content: "Create your account", fontSize: "$text2xl", fontWeight: 700 })
sub=I(card, { type: "text", name: "Subtitle", content: "Step 1 of 3: your details.", fontSize: "$textBase", fill: [{ type: "color", color: "$textMuted" }] })
email=I(card, { type: "ref", ref: "Input", descendants: { label: { content: "Email" }, input: { placeholder: "you@example.com", value: "alex@startup.io" }, error: { content: "That email is already registered. Try signing in instead." } }, theme: { state: "error" } })
pwd=I(card, { type: "ref", ref: "Input", descendants: { label: { content: "Password" }, input: { type: "password", placeholder: "8+ characters" }, helperText: { content: "Mix letters, numbers, and a symbol." } } })
tos=I(card, { type: "frame", name: "ToS", layout: "horizontal", gap: "$space-2", alignItems: "start" })
tosCheckbox=I(tos, { type: "ref", ref: "Checkbox", descendants: { label: { content: "I agree to the Terms and Privacy Policy." } } })
continue=I(card, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Continue" } } })
signinLink=I(card, { type: "ref", ref: "LinkText", descendants: { label: { content: "Already have an account? Sign in" } } })
```

15 ops.

## Step 6a: Screenshot and verify structure (Step 1)

```
snapshot_layout({ parentId: "page1", maxDepth: 3 })
get_screenshot({ nodeId: "page1" })
```

Narrate:

> *"Step 1 is on canvas. Brief match: centred auth card with stepper above. Archetype signal: the dot stepper, not a numbered stepper. Non-obvious decision: dots, not numbers. Numbers suggest a menu the user can jump between; dots read as a one-way tunnel. On a signup flow, users don't navigate backwards by choice. The generic default here is a numbered pill stepper (1, 2, 3 with circles) which reads as a wizard menu. The dot-plus-bar shape reads as progress. Drift check: the email field is showing its error state correctly with the inline message visible. Good. Card uses hairline border, no shadow."*

If the stepper is off-centre (common: the parent's `justifyContent` only applies to the main axis), fix structurally:

```
U("stepper", { alignSelf: "center" })
```

## Step 5b: Second batch_design (Step 2: verify code)

```
page2=I("doc", { type: "frame", name: "Signup_Step2_Verify", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x1 + 1520>, y: <y1>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "color", color: "$surface" }] })
stepper2=I(page2, { type: "frame", name: "Stepper", layout: "horizontal", gap: "$space-2", padding: "$space-4", alignItems: "center", width: "fit_content", alignSelf: "center" })
s2dot1=I(stepper2, { type: "ellipse", name: "Step1Dot", width: 8, height: 8, fill: [{ type: "color", color: "$primary" }] })
s2bar1=I(stepper2, { type: "rectangle", name: "Step1Bar", width: 32, height: 2, fill: [{ type: "color", color: "$primary" }] })
s2dot2=I(stepper2, { type: "ellipse", name: "Step2Dot", width: 8, height: 8, fill: [{ type: "color", color: "$primary" }] })
s2bar2=I(stepper2, { type: "rectangle", name: "Step2Bar", width: 32, height: 2, fill: [{ type: "color", color: "$border" }] })
s2dot3=I(stepper2, { type: "ellipse", name: "Step3Dot", width: 8, height: 8, fill: [{ type: "color", color: "$border" }] })
card2=I(page2, { type: "frame", name: "AuthCard", layout: "vertical", gap: "$space-4", padding: "$space-8", width: 400, cornerRadius: "$radiusLg", fill: [{ type: "color", color: "$surfaceMuted" }], stroke: { thickness: 1, fill: "$border" } })
title2=I(card2, { type: "text", name: "Title", content: "Check your email", fontSize: "$text2xl", fontWeight: 700 })
sub2=I(card2, { type: "text", name: "Subtitle", content: "We sent a 6-digit code to alex@startup.io.", fontSize: "$textBase", fill: [{ type: "color", color: "$textMuted" }] })
codeRow=I(card2, { type: "frame", name: "CodeRow", layout: "horizontal", gap: "$space-2", justifyContent: "center" })
d1=I(codeRow, { type: "frame", name: "Digit1", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d2=I(codeRow, { type: "frame", name: "Digit2", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d3=I(codeRow, { type: "frame", name: "Digit3", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d4=I(codeRow, { type: "frame", name: "Digit4", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d5=I(codeRow, { type: "frame", name: "Digit5", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
d6=I(codeRow, { type: "frame", name: "Digit6", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" } })
verify=I(card2, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Verify email" } } })
resend=I(card2, { type: "ref", ref: "LinkText", descendants: { label: { content: "Resend code" } } })
```

19 ops. The 6-digit code input is custom: the library doesn't have a `CodeInput` yet. Surface this at the end as a library candidate.

```
get_screenshot({ nodeId: "page2" })
```

Narrate:

> *"Step 2 on canvas. The email address ('alex@startup.io') appears in the subtitle, making the verification step concrete and personal. Non-obvious decision: including the user's specific email in the subtitle, not the generic 'Check your inbox'. Users who check multiple accounts on the same device need to know which inbox to look at. The code cells are 48×56px, taller than wide, so they read as digit slots not general inputs."*

## Step 5c: Third batch_design (Step 3: welcome)

The confirmation page is structurally different. No card wrapper, larger icon, single action.

```
page3=I("doc", { type: "frame", name: "Signup_Step3_Welcome", layout: "vertical", justifyContent: "center", alignItems: "center", x: <x1 + 3040>, y: <y1>, width: 1440, height: 900, padding: "$space-8", fill: [{ type: "color", color: "$surface" }] })
welcomeBlock=I(page3, { type: "frame", name: "WelcomeBlock", layout: "vertical", justifyContent: "center", alignItems: "center", gap: "$space-5", padding: "$space-8", width: 480, fill: "transparent" })
checkIcon=I(welcomeBlock, { type: "icon_font", name: "CheckIcon", iconFontName: "circle-check", iconFontFamily: "lucide", width: 64, height: 64, fill: [{ type: "color", color: "$success" }] })
welcomeTitle=I(welcomeBlock, { type: "text", name: "Title", content: "You're in.", fontSize: "$text3xl", fontWeight: 700, textAlign: "center" })
welcomeSub=I(welcomeBlock, { type: "text", name: "Subtitle", content: "We've set up your workspace. Head over and create your first project.", fontSize: "$textBase", textAlign: "center", fill: [{ type: "color", color: "$textMuted" }] })
goCta=I(welcomeBlock, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Go to dashboard" } } })
```

6 ops.

```
get_screenshot({ nodeId: "page3" })
```

Narrate:

> *"Step 3 on canvas. Three non-obvious decisions here. First: no card wrapper on the WelcomeBlock. A card shape would make this read as another form step. The bare vertical layout says the form is over; this is resolution, not continuation. Second: the icon is `$success` (green), not `$primary` (brand colour). `$primary` is an interactive affordance colour; using it on a static confirmation icon makes it read like a button. `$success` marks achieved state. Third: the title is `$text3xl` not `$text2xl`. The welcome moment earns a larger heading because this is the completion of a conversion funnel. Form steps use utility scale; the resolution moment uses a slightly larger scale."*

## Step 7: Final visual sign-off

Three pages, three screenshots, each scoped to its page:

```
get_screenshot({ nodeId: "page1" })
get_screenshot({ nodeId: "page2" })
get_screenshot({ nodeId: "page3" })
```

Verify per page:

- **Page 1.** Dot stepper renders with 1-of-3 highlighted. Email field shows error-state styling with the inline message "That email is already registered. Try signing in instead." Password field has helper text. Continue button correct. ToS checkbox legible.
- **Page 2.** Stepper shows 2-of-3 complete. Email address visible in subtitle. Six code cells render with consistent borders at 48×56px.
- **Page 3.** No card frame visible. Just icon-title-subtitle-CTA centred on a plain surface. Check icon in `$success`. Title at `$text3xl`. Single CTA "Go to dashboard".

## Step 8: Surface candidates and notes

Two notes for the user:

1. **`CodeInput` is a library candidate.** The six-digit code row is six manual frames. It is likely to appear again in 2FA and any other verification flows. Surface it: *"The 6-digit code input on Step 2 is currently built from primitives. Want me to promote it to your `.lib.pen` as `CodeInput` so other flows can reference it?"*
2. **Validation timing belongs in `flows.md`.** Document the email field's intended async behaviour in the node's `context` property: *"Unique-email check fires on blur with 400ms debounce. Error decays when user re-edits the field."* The engineer reads this and ships matching behaviour.

## Final report to user

> *"Done. Three sibling pages at 1440×900 placed side by side. Step 1 is an auth card with email in error state, password, ToS checkbox, Continue CTA, and a dot stepper showing 1-of-3. Step 2 is a verification card with 6 code cells and a Resend link. Step 3 breaks the card pattern: icon, 'You're in.', subtitle, single CTA. No card wrapper on Step 3; that break in structure signals completion. All bound to your `tokens.md` variables and mode axis. `CodeInput` and the validation timing are flagged for follow-up."*

---

## What this example demonstrates

- **The completion page breaks the form card pattern.** Pages 1 and 2 use the auth-card shape. Page 3 does not. The structural break at page 3 signals that the flow is complete. A card on the welcome page would look like another step.

- **Dot stepper, not a numbered stepper.** Numbers suggest a choosable menu; dots read as a one-way sequence. On a signup flow, the user isn't navigating, they're progressing. The dot-plus-bar shape encodes that distinction.

- **Error state on the canvas, not the default state.** Showing the email field's error state on page 1 forces the design to answer: what does error handling look like? A default-only design leaves that question for the engineer to answer. See `references/states.md` for the "screenshot the worst state" rule.

- **Icon colour: `$success` not `$primary`.** On the welcome page, `$primary` is an interactive affordance colour. Using it on a static confirmation icon makes it read as a button. `$success` marks achieved state without claiming interactivity.

- **Specific verbs everywhere.** "Continue", "Verify email", "Resend code", "Go to dashboard"; never "Submit", "OK", "Confirm". Each verb names what happens next.

For the back-stack model across the three steps, see [`references/flows.md`](../../references/flows.md) § Back-stack and navigation model. For the auth-card layout shape, see [`assets/design-system/patterns.md`](../design-system/patterns.md) § Auth flow. For copy patterns, see [`assets/design-system/voice.md`](../design-system/voice.md).
