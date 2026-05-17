# Example: design a login screen

A worked walkthrough of the default seven-step workflow for the prompt:

> *"Design a login screen in pencil"*

Assume: Pencil desktop app is running, no `.pen` open, repo has a `design-system/` folder and a `design/system.lib.pen` library with `Input`, `ButtonPrimary`, and `LinkText` components.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Result: succeeds. No active document.

## Step 2 — Locate context

- No `.pen` open.
- No selection.
- `design-system/` exists, with `README.md` and `design-system.md`.

## Step 3 — Load guidelines

Read `design-system/README.md` (60 lines). Read `design-system/design-system.md` — confirms library at `./design/system.lib.pen`, stack is React + Tailwind, icon library is Lucide. Read `design-system/tokens.md` for spacing and type tokens.

Call `get_guidelines()`. Server reports categories `colors`, `typography`, `spacing`. Read `colors` and `typography`.

## Step 4 — Plan (told to user)

> *"I'll create a centered single-column login screen at 1440×900: a 360px-wide form card with a title, subtitle, email + password inputs (instances of your `Input` component), a primary submit button (instance of `ButtonPrimary`), and a 'Forgot password?' link below. I'll add the `design/system.lib.pen` import so the components resolve."*

## Step 4.5 — Open the document

Since no `.pen` is open:

```
open_document("new")
```

The server returns a fresh document id and reports it back via `get_editor_state`. Note the document root id (let's call it `doc`).

## Step 5 — First batch_design (skeleton + import)

```
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
page=I("doc", { type: "frame", name: "LoginPage", layout: "vertical", justifyContent: "center", alignItems: "center", padding: "$space-8", width: 1440, height: 900, fill: [{ type: "solid_color", color: "$surface" }] })
form=I(page, { type: "frame", name: "Form", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: "$surfaceMuted", stroke: { thickness: 1, fill: "$border" } })
title=I(form, { type: "text", text: "Sign in", fontSize: "$text2xl", fontWeight: 700, textAlign: "left" })
sub=I(form, { type: "text", text: "Welcome back. Enter your details below.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
email=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "••••••••" } } })
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Sign in" } } })
forgot=I(form, { type: "ref", ref: "LinkText", descendants: { label: { text: "Forgot password?" } } })
```

10 ops — well under 25.

## Step 6 — Verify (structural-first)

Walk the verification ladder. Start cheap:

```
snapshot_layout({ parentId: "page", maxDepth: 2 })
```

This tells us positions and sizes — confirms the form card's width, the `page`'s computed height, the `gap` values between rows. Suppose it surfaces one issue: `page`'s computed height is shorter than 900 (the document root is constraining it), so `justifyContent: "center"` has nothing to center within.

That's a structural issue — fix it before reaching for pixels:

```
U("page", { height: "fill_container(900)" })
```

Now the visual sign-off, scoped to the page (not the document root):

```
get_screenshot(nodeId: "page")
```

Suppose one visual issue remains that the snapshot couldn't catch: the forgot-password link is left-aligned and looks off against the centered form. Fix it:

```
U(forgot, { textAlign: "center" })
```

## Step 7 — Final visual sign-off

```
get_screenshot(nodeId: "page")
```

Looks right. Two screenshots total — one after the structural fix, one for final sign-off — both scoped to the `page` node, never the document root.

## Final report to user

> *"Done. Login screen at `LoginPage` — 1440×900, centered 360px form card with email/password inputs, primary submit, and a centered forgot-password link. All components are instances of your library (`Input`, `ButtonPrimary`, `LinkText`); colors and spacing reference your tokens. Verified structurally with `snapshot_layout`, then a screenshot of the page revealed the link was off-center; fixed and re-verified."*
