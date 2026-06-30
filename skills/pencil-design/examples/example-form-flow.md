# Example: design a multi-step signup with email verification

A worked walkthrough of the seven-step workflow for the prompt:

> *"Design a signup flow with email + password, then email verification, then a welcome confirmation page."*

Assume: Pencil desktop running, no `.pen` open, the project has a `design/system.lib.pen` library that includes `Input`, `ButtonPrimary`, `LinkText`, `Checkbox`.

---

## Step 1: Detect host

```
get_editor_state({ include_schema: false })
```

Result: succeeds. No active document.

## Step 2: Understand aesthetic direction

No explicit direction given. This is a signup conversion flow, so the design should feel like a utility auth screen, not a marketing page. Load `references/flows.md` before planning — it owns validation timing, back-stack model, and multi-step confirmation anatomy.

Announced direction: *"utility auth card: centred form, hairline border, no shadow, dot stepper (not numbered), specific CTAs. The welcome page breaks the card pattern to signal completion."*

## Step 3: Load guidelines + inventory components

Call `get_guidelines()`, then load `Web App`.

Inventory the library:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Components: `Input`, `ButtonPrimary`, `ButtonSecondary`, `LinkText`, `Checkbox`. The `Input` component declares `default`, `hover`, `focus`, `error`, and `success` variants.

## Step 4: Plan

> *"I'll create three sibling top-level frames at 1440×900: `Signup_Step1_Email`, `Signup_Step2_Verify`, `Signup_Step3_Welcome`. Step 1 is a centred auth card with email + password fields, a dot stepper showing 1-of-3, and the email field in error state on the canvas. Step 2 is a slimmer card with a 6-digit code input. Step 3 breaks the card shape entirely: icon, title, single CTA, no card wrapper. Direction: utility auth register — hairline borders, no shadows, dot steppers not numbered."*

## Step 4.5: Create document

The user creates a new `.pen` in the editor. The predefined root id is `document`. The mode axis auto-registers from the themed values passed to `SetVariables`, so no separate declaration is needed. The library is attached through the editor's import UI; confirm it landed via `get_editor_state`.

## Step 4.7: Place the three frames

Three frames at 1440px need ~4400px of horizontal canvas. Pick anchor coordinates with `FindEmptySpace` as the first line inside the `batch_design` snippet (it returns `{x, y}`):

```
batch_design({ filePath: "", input: `
const slot = FindEmptySpace({ width: 1440, height: 900, padding: 80, direction: "right" })
// slot.x / slot.y anchor Step 1; the other two frames go at slot.x + 1520 and slot.x + 3040.
` })
```

The other two frames go at `(slot.x + 1520, slot.y)` and `(slot.x + 3040, slot.y)`: 1440px each with an 80px gutter between, so the engineer can scrub the sequence left-to-right.

## Step 5a: First batch_design (Step 1: email + password)

```
batch_design({ filePath: "", input: `
const slot = FindEmptySpace({ width: 1440, height: 900, padding: 80, direction: "right" })
page1 = Insert(document, { type: "frame", name: "Signup_Step1_Email", layout: "vertical", justifyContent: "center", alignItems: "center", x: slot.x, y: slot.y, width: 1440, height: 900, padding: "$space-8", fill: "$surface" })
stepper = Insert(page1, { type: "frame", name: "Stepper", layout: "horizontal", gap: "$space-2", padding: "$space-4", alignItems: "center", width: "fit_content" })
step1Dot = Insert(stepper, { type: "ellipse", name: "Step1Dot", width: 8, height: 8, fill: "$primary" })
step1Bar = Insert(stepper, { type: "rectangle", name: "Step1Bar", width: 32, height: 2, fill: "$primary" })
step2Dot = Insert(stepper, { type: "ellipse", name: "Step2Dot", width: 8, height: 8, fill: "$border" })
step2Bar = Insert(stepper, { type: "rectangle", name: "Step2Bar", width: 32, height: 2, fill: "$border" })
step3Dot = Insert(stepper, { type: "ellipse", name: "Step3Dot", width: 8, height: 8, fill: "$border" })
card = Insert(page1, { type: "frame", name: "AuthCard", layout: "vertical", gap: "$space-4", padding: "$space-8", width: 400, cornerRadius: "$radiusLg", fill: "$surfaceMuted", stroke: "$border", strokeWidth: 1 })
title = Insert(card, { type: "text", name: "Title", content: "Create your account", fontSize: "$text2xl", fontWeight: 700 })
sub = Insert(card, { type: "text", name: "Subtitle", content: "Step 1 of 3: your details.", fontSize: "$textBase", fill: "$textMuted" })
email = Insert(card, { type: "ref", ref: "Input", descendants: { label: { content: "Email" }, input: { placeholder: "you@example.com", value: "alex@startup.io" }, error: { content: "That email is already registered. Try signing in instead." } }, theme: { state: "error" } })
pwd = Insert(card, { type: "ref", ref: "Input", descendants: { label: { content: "Password" }, input: { type: "password", placeholder: "8+ characters" }, helperText: { content: "Mix letters, numbers, and a symbol." } } })
tos = Insert(card, { type: "frame", name: "ToS", layout: "horizontal", gap: "$space-2", alignItems: "start" })
tosCheckbox = Insert(tos, { type: "ref", ref: "Checkbox", descendants: { label: { content: "I agree to the Terms and Privacy Policy." } } })
continue = Insert(card, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Continue" } } })
signinLink = Insert(card, { type: "ref", ref: "LinkText", descendants: { label: { content: "Already have an account? Sign in" } } })
` })
```

15 ops.

## Step 6a: Screenshot and verify structure (Step 1)

```
snapshot_layout({ filePath: "", parentId: page1, maxDepth: 3 })
get_screenshot({ filePath: "", nodeId: page1 })
```

Narrate:

> *"Step 1 is on canvas. Direction match: centred auth card with dot stepper above, hairline border visible, no shadow. Non-obvious decision: dots, not numbers. Numbers suggest a menu the user can jump between; dots read as a one-way tunnel. On a signup flow, users don't navigate backwards by choice. The generic default is a numbered pill stepper (1, 2, 3 with circles), which reads as a wizard menu. The dot-plus-bar shape reads as progress. The email field is showing error state correctly with inline message. No AI-default drift to fix."*

If the stepper is off-centre, fix structurally. Pencil layout has no per-child `alignSelf`, so centre it through the parent's cross-axis alignment:

```
batch_design({ filePath: "", input: `Update(page1, { alignItems: "center" })` })
```

## Step 5b: Second batch_design (Step 2: verify code)

```
batch_design({ filePath: "", input: `
page2 = Insert(document, { type: "frame", name: "Signup_Step2_Verify", layout: "vertical", justifyContent: "center", alignItems: "center", x: slot.x + 1520, y: slot.y, width: 1440, height: 900, padding: "$space-8", fill: "$surface" })
stepper2 = Insert(page2, { type: "frame", name: "Stepper", layout: "horizontal", gap: "$space-2", padding: "$space-4", alignItems: "center", width: "fit_content" })
s2dot1 = Insert(stepper2, { type: "ellipse", name: "Step1Dot", width: 8, height: 8, fill: "$primary" })
s2bar1 = Insert(stepper2, { type: "rectangle", name: "Step1Bar", width: 32, height: 2, fill: "$primary" })
s2dot2 = Insert(stepper2, { type: "ellipse", name: "Step2Dot", width: 8, height: 8, fill: "$primary" })
s2bar2 = Insert(stepper2, { type: "rectangle", name: "Step2Bar", width: 32, height: 2, fill: "$border" })
s2dot3 = Insert(stepper2, { type: "ellipse", name: "Step3Dot", width: 8, height: 8, fill: "$border" })
card2 = Insert(page2, { type: "frame", name: "AuthCard", layout: "vertical", gap: "$space-4", padding: "$space-8", width: 400, cornerRadius: "$radiusLg", fill: "$surfaceMuted", stroke: "$border", strokeWidth: 1 })
title2 = Insert(card2, { type: "text", name: "Title", content: "Check your email", fontSize: "$text2xl", fontWeight: 700 })
sub2 = Insert(card2, { type: "text", name: "Subtitle", content: "We sent a 6-digit code to alex@startup.io.", fontSize: "$textBase", fill: "$textMuted" })
codeRow = Insert(card2, { type: "frame", name: "CodeRow", layout: "horizontal", gap: "$space-2", justifyContent: "center" })
d1 = Insert(codeRow, { type: "frame", name: "Digit1", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: "$border", strokeWidth: 1 })
d2 = Insert(codeRow, { type: "frame", name: "Digit2", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: "$border", strokeWidth: 1 })
d3 = Insert(codeRow, { type: "frame", name: "Digit3", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: "$border", strokeWidth: 1 })
d4 = Insert(codeRow, { type: "frame", name: "Digit4", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: "$border", strokeWidth: 1 })
d5 = Insert(codeRow, { type: "frame", name: "Digit5", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: "$border", strokeWidth: 1 })
d6 = Insert(codeRow, { type: "frame", name: "Digit6", width: 48, height: 56, cornerRadius: "$radiusMd", stroke: "$border", strokeWidth: 1 })
verify = Insert(card2, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Verify email" } } })
resend = Insert(card2, { type: "ref", ref: "LinkText", descendants: { label: { content: "Resend code" } } })
` })
```

19 ops. The 6-digit code input is custom: the library doesn't have a `CodeInput` yet. Surface this at the end as a library candidate.

```
get_screenshot({ filePath: "", nodeId: page2 })
```

Narrate:

> *"Step 2 on canvas. The email address ('alex@startup.io') appears in the subtitle, making the verification step concrete and personal. Non-obvious decision: the user's specific email in the subtitle, not the generic 'Check your inbox'. Users who check multiple accounts on the same device need to know which inbox to look at. The code cells are 48×56px, taller than wide, so they read as digit slots not general inputs."*

## Step 5c: Third batch_design (Step 3: welcome)

The confirmation page is structurally different. No card wrapper, larger icon, single action.

```
batch_design({ filePath: "", input: `
page3 = Insert(document, { type: "frame", name: "Signup_Step3_Welcome", layout: "vertical", justifyContent: "center", alignItems: "center", x: slot.x + 3040, y: slot.y, width: 1440, height: 900, padding: "$space-8", fill: "$surface" })
welcomeBlock = Insert(page3, { type: "frame", name: "WelcomeBlock", layout: "vertical", justifyContent: "center", alignItems: "center", gap: "$space-5", padding: "$space-8", width: 480, fill: "transparent" })
checkIcon = Insert(welcomeBlock, { type: "icon", name: "CheckIcon", icon: "circle-check", library: "lucide", width: 64, height: 64, fill: "$success" })
welcomeTitle = Insert(welcomeBlock, { type: "text", name: "Title", content: "You're in.", fontSize: "$text3xl", fontWeight: 700, textAlign: "center" })
welcomeSub = Insert(welcomeBlock, { type: "text", name: "Subtitle", content: "We've set up your workspace. Head over and create your first project.", fontSize: "$textBase", textAlign: "center", fill: "$textMuted" })
goCta = Insert(welcomeBlock, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Go to dashboard" } } })
` })
```

6 ops.

```
get_screenshot({ filePath: "", nodeId: page3 })
```

Narrate:

> *"Step 3 on canvas. Three non-obvious decisions. First: no card wrapper on WelcomeBlock. A card shape would make this read as another form step; the bare vertical layout says the form is over. Second: the icon is `$success` (green), not `$primary` (brand colour). `$primary` is an interactive affordance colour; using it on a static confirmation icon makes it read like a button. `$success` marks achieved state. Third: title is `$text3xl` not `$text2xl`. The welcome moment earns a larger heading — form steps use utility scale, the resolution moment uses slightly more."*

## Step 7: Final visual sign-off

Three pages, three screenshots:

```
get_screenshot({ filePath: "", nodeId: page1 })
get_screenshot({ filePath: "", nodeId: page2 })
get_screenshot({ filePath: "", nodeId: page3 })
```

Verify per page:

- **Page 1.** Dot stepper renders with 1-of-3 highlighted. Email field shows error-state styling with inline message. Password field has helper text. Continue button correct. ToS checkbox legible.
- **Page 2.** Stepper shows 2-of-3 complete. Email address visible in subtitle. Six code cells at 48×56px with consistent borders.
- **Page 3.** No card frame visible. Icon-title-subtitle-CTA centred on plain surface. Check icon in `$success`. Title at `$text3xl`. Single CTA "Go to dashboard".

## Step 8: Surface candidates and notes

Two notes for the user:

1. **`CodeInput` is a library candidate.** The six-digit code row is six manual frames. It will appear again in 2FA and other verification flows. Surface it: *"The 6-digit code input on Step 2 is currently built from primitives. Want me to promote it to your `.lib.pen` as `CodeInput`?"*
2. **Validation timing belongs in context.** Document the email field's intended async behaviour in the node's `context` property: *"Unique-email check fires on blur with 400ms debounce. Error decays when user re-edits the field."* The engineer reads this and ships matching behaviour.

## Final report to user

> *"Done. Three sibling pages at 1440×900 placed side by side. Step 1 is an auth card with email in error state, password, ToS checkbox, Continue CTA, and a dot stepper showing 1-of-3. Step 2 is a verification card with 6 code cells and a Resend link. Step 3 breaks the card pattern: icon, 'You're in.', subtitle, single CTA. No card wrapper on Step 3; that structural break signals completion. All bound to token variables and mode axis. `CodeInput` and validation timing are flagged for follow-up."*

---

## What this example demonstrates

- **The completion page breaks the form card pattern.** Pages 1 and 2 use the auth-card shape. Page 3 does not. The structural break at page 3 signals that the flow is complete. A card on the welcome page would look like another step.

- **Dot stepper, not a numbered stepper.** Numbers suggest a choosable menu; dots read as a one-way sequence. On a signup flow, the user isn't navigating, they're progressing. The dot-plus-bar shape encodes that distinction.

- **Error state on the canvas, not the default state.** Showing the email field's error state on page 1 forces the design to answer: what does error handling look like? A default-only design leaves that question for the engineer. See `references/states.md` for the "screenshot the worst state" rule.

- **Icon colour: `$success` not `$primary`.** On the welcome page, `$primary` is an interactive affordance colour. Using it on a static confirmation icon makes it read as a button. `$success` marks achieved state without claiming interactivity.

- **Specific verbs everywhere.** "Continue", "Verify email", "Resend code", "Go to dashboard"; never "Submit", "OK", "Confirm". Each verb names what happens next.
