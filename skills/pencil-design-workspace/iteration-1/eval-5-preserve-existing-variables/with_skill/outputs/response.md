# Adding a login screen without clobbering your tokens

Short version: I will not call `set_variables` or run any `batch_design` op that touches `variables` until I have read your current token set with `get_variables()` and worked out exactly which keys are absent. Anything you have already configured stays untouched. Here is the full plan.

## Why this matters before you see any of my ops

The trap with `set_variables` is that `replace: false` (the merge default) sounds protective but isn't. It merges *keys*, not *values*. If I pass `{ primary: { value: "#1F6FEB", ... } }` and your document already has `primary` set to `#E63946`, your red gets silently overwritten with my blue. The same applies to a `U("doc", { variables: { ... } })` op inside `batch_design`. The skill calls this out as failure mode #7 (Token clobber) for exactly this reason, and the `set_variables` cookbook entry repeats it: *"`replace: false` does not protect existing variable values."*

So the correctness rule is: only pass variables that are absent from `get_variables()`. Never re-declare something that already exists, even with the same nominal value, because I can't be sure my "default" matches what you have customised.

## What I would do, in order

### 1. Ping the host and confirm the file is open

```
get_editor_state({ include_schema: false })
```

I expect a successful response naming your `.pen` as the active document and telling me the current selection (probably none for this task). If this errors with `transport not connected`, I stop and ask you to open the Pencil app or extension. I will not silently fall back to the CLI.

### 2. Read your current variables

```
get_variables()
```

I expect a JSON object keyed by variable name, each entry shaped like `{ type, value }`. Theme-aware ones return `value` as an array of `{ value, theme }` entries. So your `primary` should come back roughly as:

```
primary: { type: "color", value: [
  { value: "#E63946", theme: { mode: "light" } },
  { value: "#<your dark>", theme: { mode: "dark" } }
] }
```

What I check on this response:
- Confirm `primary` resolves to `#E63946` and `surface` to `#F8F9FA` for the light mode entry. If they don't, I read back what they actually are and confirm with you before going further. I'd rather pause than overwrite.
- Note whether `primary` and `surface` carry both `light` and `dark` theme entries, or only `light`. If only `light`, I'll flag it: a login screen wants both modes, and adding a dark variant without your input means inventing brand decisions I shouldn't invent.
- Inventory the rest: do you have `surfaceMuted`, `border`, `textPrimary`, `textMuted`, a focus ring, spacing scale, type scale? I keep a mental list of which token names are present and which are not. The absent ones are the only ones I will pass to `set_variables` later.

### 3. Check the theme axis is declared

I look at the `themes` field on the document root via `get_editor_state` (or by inspecting the doc node in `batch_get`). If `mode: ["light", "dark"]` already exists, I skip declaring it. If it doesn't exist but your variables already carry theme entries, something is off and I stop to ask. If neither exists and you only have light values, I surface the choice rather than silently add dark.

### 4. Inventory the components in the file and any imported library

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

And, for each `.lib.pen` listed in your document's `imports`:

```
batch_get({ filePath: "<lib path>", patterns: [{ reusable: true }], readDepth: 2 })
```

I'm looking for `Input`, `Button` / `ButtonPrimary`, `LinkText`, anything labelled like a form field. Components-first means I instantiate yours via `ref` nodes rather than re-build a button from a frame and text. If nothing matches, I'd say so before building primitives.

### 5. Show you the plan before any write

I'd hand you something like: *"Centred 1440 by 900 LoginPage with a 360px form card. Title, subtitle, email and password instances of your `Input` component, a `ButtonPrimary` for Sign in, and a `LinkText` for Forgot password? Card surface uses `$surface`, primary action uses `$primary`. I will only call `set_variables` if I find missing supporting tokens (focus ring, body type sizes, spacing scale), and only with the keys absent from `get_variables()`. Your `$primary` and `$surface` will not be passed in any token call."*

This is the cheap moment to catch a wrong assumption. I would not move on until you confirm.

### 6. Bootstrap *only* the absent tokens, if any

If `get_variables()` already returned a complete suite, I skip this step entirely. If it returned only `primary` and `surface`, I call `set_variables` with everything else I need for a login screen and nothing more. Concretely, if `textPrimary`, `textMuted`, `border`, `focusRing`, the spacing scale, and the type scale are missing, the call looks like:

```
set_variables({
  variables: {
    textPrimary: { type: "color", value: [
      { value: "#0B1117", theme: { mode: "light" } },
      { value: "#FAFAFA", theme: { mode: "dark" } }
    ] },
    textMuted: { type: "color", value: [ ... ] },
    border:    { type: "color", value: [ ... ] },
    focusRing: { type: "color", value: [ ... ] },
    "space-2": { type: "number", value: 8 },
    "space-4": { type: "number", value: 16 },
    "space-6": { type: "number", value: 24 },
    textBase: { type: "number", value: 16 },
    text2xl:  { type: "number", value: 24 }
    // primary and surface deliberately not passed
  },
  replace: false
})
```

Two things to notice in that shape:
- `replace: false` is set for safety even though, given I'm only passing absent keys, `replace: true` would also be safe in this narrow case. Belt and braces.
- `primary` and `surface` are nowhere in the payload. They cannot be clobbered by something I don't pass.

After the call I'd re-run `get_variables()` to confirm the new keys landed and the existing ones still resolve to your values. That catches any silent surprise.

### 7. Run `batch_design` for the login screen, binding to your tokens by name

When I write the screen, your custom values flow through automatically because the design references variables by name, not hex. Card surface as `$surface`, primary button fill as `$primary`, body text as `$textPrimary`, and so on. I will never bind a raw hex on a node that has a token equivalent.

I would also avoid the `U("doc", { variables: { ... } })` shape for this work. Token mutations belong in `set_variables` calls that I have explicitly checked against `get_variables()`. Mixing them into a `batch_design` body invites the same clobber risk by accident.

## The short list of guarantees this gives you

- I never call `set_variables` before `get_variables()` has come back and I have read it.
- I never pass a key into `set_variables` that already exists in your document.
- I never use `replace: true`.
- I never put a `variables` block inside a `U("doc", ...)` op.
- I never bind a raw hex like `#E63946` on a node when `$primary` is what I should be using.

If `get_variables()` shows your file is already token-complete for what a login screen needs, the whole token step disappears and I go straight to the import check, the component inventory, the plan, and the screen.

## References I leaned on

- `SKILL.md` — the **Themes** subsection of the Discipline rules (the *"call `get_variables()` first; `replace: false` still overwrites"* rule), and **Failure modes** #7 (Token clobber). These are the load-bearing safety statements.
- `references/mcp-tools.md` — the `get_variables` and `set_variables` cookbook entries. The `set_variables` Pitfalls list is explicit that `replace: false` does not protect existing values, and it documents the response shape for theme-aware variables I need to validate against.
- `assets/examples/example-login-screen.md` — the worked seven-step walkthrough I'm following structurally, adjusted for the fact that your file is already open and already has tokens (so I drop the new-document open and the full bootstrap).

Want me to go ahead and run `get_editor_state` and `get_variables` so we can see exactly what's in the file before I commit to a token diff?
