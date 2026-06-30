# Example: design a login screen

A worked walkthrough for the prompt:

> *"Design a login screen in pencil"*

Assume: Pencil desktop app is running, no `.pen` open, the project has a `design/system.lib.pen` library with `Input`, `ButtonPrimary`, and `LinkText` components.

---

## Step 1: Detect host

```
get_editor_state({ include_schema: false })
```

Succeeds. No active document.

## Step 2: Understand aesthetic direction

The user hasn't given a screenshot or brand reference. Infer from context: this is a B2B data product's auth gate. The design should feel like the product itself — utility-first, no marketing register.

Announced direction: *"utility login for a data product: compact title scale, centred form card with hairline border and no shadow, no hero language."*

## Step 3: Load guidelines and inventory

Call `get_guidelines()`. Load `Web App`.

Inventory components from the library:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Components: `Input`, `ButtonPrimary`, `LinkText`. Token list includes: `$surface`, `$surfaceMuted`, `$text`, `$textMuted`, `$border`, `$primary`, `$space-2` through `$space-8`, `$radiusLg`, `$text2xl`, `$textBase`.

## Step 4: Plan

> *"I'll build `LoginPage` at 1440×900: a 360px form card centred on the page with a title, subtitle, email and password `Input` instances, `ButtonPrimary` for submit, `LinkText` for 'Forgot password?'. Direction: utility scale — hairline border on the card, no shadow, `$text2xl` title, not a hero heading."*

## Step 4.5: Open document, declare mode axis and imports

```
open_document({ path: "new" })
```

The server returns the document root id; call it `doc`. Declare the mode axis and library import before any frames land:

```
U(doc, { themes: { mode: ["light", "dark"] } })
U(doc, { imports: { "ds": "./design/system.lib.pen" } })
```

2 ops. No rendered change; no screenshot needed.

## Step 5a: Place the page and the form card

```
page=I(doc, { type: "frame", name: "LoginPage", layout: "vertical", justifyContent: "center", alignItems: "center", padding: "$space-8", width: 1440, height: 900, fill: "$surface" })
form=I(page, { type: "frame", name: "Form", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: "$surfaceMuted", stroke: { thickness: 1, fill: "$border" } })
```

2 ops. Screenshot:

```
get_screenshot({ nodeId: page })
```

Narrate:

> *"The 1440×900 page is on canvas with the 360px form card centred. Direction match: hairline border visible, no shadow — the card separates from the background without claiming elevation. No AI-default drift to fix: the generic trap here is adding `effect: [{ type: 'drop_shadow', blur: 8, opacity: 0.1 }]` to the card, which I have not done."*

If the card sits off-centre, the page height constraint is the culprit:

```
U(page, { height: "fill_container(900)" })
```

## Step 5c: Add the title block

```
title=I(form, { type: "text", content: "Sign in", fontSize: "$text2xl", fontWeight: 700, fill: "$text" })
sub=I(form, { type: "text", content: "Welcome back. Enter your details below.", fontSize: "$textBase", fill: "$textMuted" })
```

2 ops. Screenshot the form. Narrate:

> *"Title and subtitle landed. Non-obvious decision: `$text2xl` / 700, not a display or hero scale. At `$text3xl`, the heading would outweigh the form fields and make the page read as a marketing surface. `$text2xl` is compact enough to feel functional. `$space-4` gap reads right at 16px."*

## Step 5d: Add the inputs

```
email=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Password" }, input: { type: "password", placeholder: "••••••••" } } })
```

2 ops. Screenshot the form. Narrate:

> *"Both inputs are library `Input` instances. Non-obvious decision: component refs, not raw frames. The generic default is a frame + text label pair, which bypasses your component's error variant. When the engineer adds email-taken validation, the raw primitive requires a rebuild; the `Input` ref just needs a descendants override on its error child."*

## Step 5e: Add the submit and forgot-password link

```
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Sign in" } } })
forgot=I(form, { type: "ref", ref: "LinkText", descendants: { label: { content: "Forgot password?" } } })
```

2 ops. Screenshot the form. Narrate:

> *"Submit and link are placed. The link is left-aligned by default, creating a left-pull against the centred card. Fixing before moving on."*

## Step 5f: Adjust the link alignment

```
U(forgot, { textAlign: "center" })
```

1 op. Screenshot. Narrate:

> *"Link centred. Non-obvious decision: `textAlign: 'center'` on the text node rather than a wrapper frame. The link lives in a vertical-layout form; centring the text property aligns it within its available width without introducing a new layout element."*

## Step 6: Final pass

Five accessibility checks:

- **Contrast.** `$text` on `$surfaceMuted` passes 4.5:1 in light mode. Switch to dark mode and screenshot:

  ```
  U(page, { theme: { mode: "dark" } })
  get_screenshot({ nodeId: page })
  ```

  Narrate: *"Dark mode: title and subtitle legible, card surface picks up `$surfaceMuted` dark value, button keeps its hue, focus styles from the library hold. The mode axis declared in step 4.5 means no raw-hex values need updating."*

- **Hit targets.** `ButtonPrimary` declares 44×44 minimum in the library.
- **Colour-not-only signal.** No error or success states present yet.
- **Semantic names.** `LoginPage`, `Form` correct; `email`, `pwd`, `submit`, `forgot` are bindings. Verify no default `Frame` names survived.
- **Focus states.** Inherited from `Input` and `ButtonPrimary`.

Pass. Switch back to light mode: `U(page, { theme: { mode: "light" } })`.

## Final report to user

> *"Done. `LoginPage` at 1440×900, 360px form card centred with `Input` instances for email and password, `ButtonPrimary` for submit, `LinkText` for the forgot-password link. Hairline border, no shadow, `$text2xl` title scale. Six build chunks with a screenshot after each, plus a dark-mode screenshot at the final pass. Mode axis and library import declared up-front; every colour resolves through your tokens."*

---

## What this example demonstrates

- **Direction drives the card spec.** The card has a 1px `$border` stroke and no shadow because the stated direction was utility-first, no elevation chrome. A drop shadow shifts the card into the marketing-page register. One absent property, `effect`, is the difference between the two registers.

- **Form card width is not arbitrary.** 360px is the compact utility width for a login form. 400px and wider reads as a landing-page card. The difference is subtle: at 360px, the form reads as a tool; at 480px, it reads as a feature.

- **Title scale signals intent.** `$text2xl` / 700 for a utility screen, not display or hero scale. At `$text3xl`, the heading competes with the form fields and makes the login page read as a marketing surface.

- **Component refs preserve future states.** Using `Input` and `ButtonPrimary` library refs means error states, loading states, and focus rings are already specified at the component level. Raw primitives require rebuilding for every state variant.

- **Mode axis declared first.** Before any frame placement, `themes: { mode: ["light", "dark"] }` and the library import go on the doc root. No raw hex in the design; every colour resolves through a variable.
