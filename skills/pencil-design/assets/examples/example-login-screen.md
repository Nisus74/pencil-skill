# Example: design a login screen

A worked walkthrough for the prompt:

> *"Design a login screen in pencil"*

Assume: Pencil desktop app is running, no `.pen` open, repo has a `design-system/` folder and a `design/system.lib.pen` library with `Input`, `ButtonPrimary`, and `LinkText` components.

This example shows the chunked build-screenshot-react loop the SKILL.md `Screenshot loop` section calls for: small ops, a screenshot and narration after each, iteration in response to what the screenshot reveals.

---

## Step 1: Detect host

```
get_editor_state({ include_schema: false })
```

Succeeds. No active document.

## Step 2: Locate context

- No `.pen` open.
- No selection.
- `design-system/` exists, with `README.md` and `design-system.md`.

## Step 3: Load guidelines and inventory

Read `design-system/README.md`. Read `design-system/design-system.md`: confirms library at `./design/system.lib.pen`, stack is React + Tailwind, icon library is Lucide. Read `design-system/tokens.md` for spacing and type tokens.

Call `get_guidelines()`. Server reports categories `colors`, `typography`, `spacing`. Read `colors` and `typography`.

Inventory components from the library:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Component list: `Input`, `ButtonPrimary`, `LinkText`.

Token list (from `tokens.md`): `$surface`, `$surfaceMuted`, `$text`, `$textMuted`, `$border`, `$primary`, `$space-2` through `$space-8`, `$radiusLg`, `$text2xl`, `$textBase`.

Both lists are populated. Step 4 will reference them by id.

## Step 4: Plan

> *"I'll build `LoginPage` at 1440x900: a 360px form card centred on the page with a title, subtitle, email and password inputs (instances of your `Input` component), `ButtonPrimary` for the submit, `LinkText` for 'Forgot password?'. Atmosphere: airy, symmetric, static. Layout shape: centred card on a surface."*

The plan covers all four required parts: top-level frame (`LoginPage`); component ids from the inventory (`Input`, `ButtonPrimary`, `LinkText`); atmosphere stance (airy, symmetric, static); layout shape (centred card on a surface).

## Step 4.5: Open document, declare mode axis and imports

```
open_document({ path: "new" })
```

The server returns the document root id; call it `doc`. First chunk declares the mode axis and the library import before any frames land:

```
U(doc, { themes: { mode: ["light", "dark"] } })
U(doc, { imports: { "ds": "./design/system.lib.pen" } })
```

2 ops, no rendered change yet, no screenshot needed.

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

> *"The 1440x900 page is on the canvas with the 360px form card. The card is sitting too high; the page's `justifyContent: center` cannot take effect because the page is being constrained by the doc root. I'll fix the page height next."*

## Step 5b: Fix the page sizing

```
U(page, { height: "fill_container(900)" })
```

1 op. Screenshot. Narrate:

> *"Page is now 900 tall and the form is centred."*

## Step 5c: Add the title block

```
title=I(form, { type: "text", content: "Sign in", fontSize: "$text2xl", fontWeight: 700, fill: "$text" })
sub=I(form, { type: "text", content: "Welcome back. Enter your details below.", fontSize: "$textBase", fill: "$textMuted" })
```

2 ops. Screenshot the form. Narrate:

> *"Title and subtitle landed; gap reads right at $space-4 (16px). Both colours resolved through variables, no raw hex."*

## Step 5d: Add the inputs

```
email=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { content: "Password" }, input: { type: "password", placeholder: "••••••••" } } })
```

2 ops. Screenshot the form. Narrate:

> *"Both inputs are instances of your `Input` component; labels and placeholders look right, focus states inherited from the library."*

## Step 5e: Add the submit and forgot-password link

```
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Sign in" } } })
forgot=I(form, { type: "ref", ref: "LinkText", descendants: { label: { content: "Forgot password?" } } })
```

2 ops. Screenshot the form. Narrate:

> *"Submit button uses your `$primary` from the library. The 'Forgot password?' link is left-aligned by default, which reads off-centre against the rest of the centred form. I'll centre it next."*

## Step 5f: Adjust the link alignment

```
U(forgot, { textAlign: "center" })
```

1 op. Screenshot. Narrate:

> *"Link is centred now; the form reads as a coherent stack."*

## Step 6: Final pass

Five accessibility checks:

- **Contrast.** `$text` on `$surfaceMuted` passes 4.5:1 in light mode. Switch to dark mode and screenshot:

  ```
  U(page, { theme: { mode: "dark" } })
  get_screenshot({ nodeId: page })
  ```

  Narrate: *"Dark mode rendering: title and subtitle remain legible, form card surface picks up the `$surfaceMuted` dark value, primary button keeps its hue, focus styles from the library hold up."*
- **Hit targets.** Submit button is 44x44 minimum (the library component declares it).
- **Colour-not-only signal.** No error or success states present yet, nothing to verify.
- **Semantic names.** `LoginPage`, `Form`, `Title`, `Subtitle` are correct; `email`, `pwd`, `submit`, `forgot` are bindings, not display names. Verify with `batch_get` if any default `Frame` survived.
- **Focus states.** Inherited from `Input` and `ButtonPrimary`.

Pass. Switch back to light mode for handoff: `U(page, { theme: { mode: "light" } })`.

## Final report to user

> *"Done. `LoginPage` at 1440x900, 360px form card centred with `Input` instances for email and password, `ButtonPrimary` for submit, `LinkText` for the forgot-password link. Atmosphere came through as airy and symmetric. Six visual-build chunks with a screenshot and narration after each, plus one dark-mode screenshot at the final pass. Mode axis declared up-front; every colour resolves through your tokens. Accessibility passes under both modes."*

---

## What this example demonstrates

- **Mode axis declared first.** Before any frame placement, `themes: { mode: ["light", "dark"] }` and the library import go on the doc root. Every colour reference downstream resolves through a variable.
- **Small chunks (1-2 ops each), screenshot after each.** Six visual chunks, six screenshots, plus one in dark mode at the final pass.
- **Narration after each screenshot.** Plain language, specific about what landed and what needs adjusting. The narration is what the user reads to know what the agent is seeing.
- **Components, not primitives.** `Input`, `ButtonPrimary`, and `LinkText` came from the library; nothing was rebuilt from a frame and a text node.
- **Tokens everywhere.** Every `fill` and text colour resolves through a `$variableName` from `tokens.md`. No raw hex appears anywhere in the design.
