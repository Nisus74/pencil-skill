# Example: import a `.lib.pen` and use its components

User says:

> *"Use the design library at `design/system.lib.pen` and add a login form using the Button and Input components."*

A `.pen` file is already open. The library is **not** currently imported.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Succeeds. Document `doc` is open. Note the imports field — it's empty or doesn't contain `design/system.lib.pen`.

## Step 2 — Verify the library file exists

Check `design/system.lib.pen` exists in the project (a directory listing, not the MCP). Suppose it does.

## Step 3 — Read the library to see what's available

```
batch_get({ patterns: [{ where: { reusable: true } }] }, [], { documentPath: "./design/system.lib.pen" })
```

(Or whichever pattern syntax the server accepts for cross-document queries — confirm with `get_guidelines("batch_get")` if unsure.)

Result: library has reusable components `ButtonPrimary`, `ButtonSecondary`, `Input`, `Textarea`, `Card`, etc.

## Step 4 — Add the import

Update the document root's `imports`:

```
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
```

(If the document already has imports, merge — read the existing object first via `batch_get(["doc"], [])` and combine.)

## Step 5 — Plan and tell the user

> *"Library imported as `ds`. I'll add a 360px form to your current page with email + password `Input` instances and a `Button` instance for submit. Same pattern as your existing components."*

## Step 6 — Build the form

```
form=I("doc", { type: "frame", name: "LoginForm", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: [{ type: "solid_color", color: "$surface" }] })
title=I(form, { type: "text", text: "Sign in", fontSize: "$text2xl", fontWeight: 700 })
email=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Password" }, input: { type: "password" } } })
submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Sign in" } } })
```

Five ops.

## Step 7 — Verify

```
get_screenshot(form)
```

If components render correctly (correct fonts, correct primary color from the library's variables), you're done. If a `ref` shows as a placeholder, the import path is wrong or the component id is misspelled — fix and retry.

## Common pitfalls

- **Component id case sensitivity.** `ButtonPrimary` ≠ `buttonPrimary` ≠ `Button-Primary`. Get the id from the library, don't guess.
- **Variable scope.** Variables defined in the library are usable in the importing document, but only after the import is added. Don't reference `$libraryVar` before the import op runs.
- **Path is relative to the importing `.pen`**, not to the project root. `./design/system.lib.pen` works only if the current document is at the project root.
