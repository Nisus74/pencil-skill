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

## Step 6 — Verify

```
get_screenshot()
```

Look at the result. Assume two issues surface:

1. Form is sitting at the very top of the page — `justifyContent` on `page` was `start` not `center`.
2. The forgot-password link is left-aligned; should be centered to match the form's vertical rhythm.

(Wait — `justifyContent` was set to `"center"` in the op. If the screenshot shows it at the top, the parent `page` height isn't actually 900 — perhaps the document root constrains it. This is the sort of thing the screenshot reveals that the JSON wouldn't.)

## Step 7 — Iterate

```
U("page", { height: "fill_container(900)" })
U(forgot, { textAlign: "center" })
```

Screenshot again. Looks right.

## Final report to user

> *"Done. Login screen at `LoginPage` — 1440×900, centered 360px form card with email/password inputs, primary submit, and a centered forgot-password link. All components are instances of your library (`Input`, `ButtonPrimary`, `LinkText`); colors and spacing reference your tokens. Two iterations after the first screenshot to fix vertical centering and link alignment."*
