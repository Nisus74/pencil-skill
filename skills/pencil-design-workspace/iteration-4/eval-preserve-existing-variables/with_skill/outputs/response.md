Great — before touching any token or calling `set_variables` or `batch_design`, here is the exact sequence I'd follow to add a login screen without overwriting your existing `$primary` and `$surface` values.

---

## Step 1: Ping the host

```
get_editor_state({ include_schema: false })
```

This confirms the MCP server is connected and the file you described is the active document. I'll also note whether there are existing top-level frames on the canvas (so I know whether to call `find_empty_space_on_canvas` before placing the login frame).

---

## Step 2: Read the existing tokens — `get_variables()` first, non-negotiably

```
get_variables()
```

This is the critical gate. The call returns every document-level variable currently declared, keyed by name with type and value. In your case I'd expect to see at least:

```json
{
  "primary": {
    "type": "color",
    "value": [
      { "value": "#E63946", "theme": { "mode": "light" } },
      { "value": "...",     "theme": { "mode": "dark"  } }
    ]
  },
  "surface": {
    "type": "color",
    "value": [
      { "value": "#F8F9FA", "theme": { "mode": "light" } },
      { "value": "...",     "theme": { "mode": "dark"  } }
    ]
  }
}
```

I record the full list of variable names from this response. That list is my "do not touch" set. Any name that appears in the `get_variables()` result is already configured — it belongs to you, not to me.

---

## Step 3: Diff — only bootstrap what's missing

With the existing token names in hand, I compare them against the standard set a login screen needs:

| Token | Already exists? | Action |
|-------|----------------|--------|
| `primary` | Yes (`#E63946`) | Leave it alone |
| `surface` | Yes (`#F8F9FA`) | Leave it alone |
| `surfaceMuted` | Check the response | Add only if absent |
| `border` | Check the response | Add only if absent |
| `textPrimary` | Check the response | Add only if absent |
| `textMuted` | Check the response | Add only if absent |
| `danger` | Check the response | Add only if absent |
| `focusRing` | Check the response | Add only if absent |
| spacing/type tokens | Check the response | Add only if absent |

The call to `set_variables` — if I make one at all — includes **only the variables absent from the `get_variables()` result**. Your `$primary` and `$surface` are never passed as arguments.

---

## Step 4: Check the theme axis

I check `get_editor_state` output (or the `get_variables()` result) to confirm whether the document already declares a `mode` axis with `light` and `dark` values. If the axis already exists, I skip the `U("doc", { themes: ... })` op entirely. If it's missing — which would be unusual given you have configured tokens — I add it once before the `set_variables` call.

---

## Step 5: Inventory existing components

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Before building the login screen from primitives, I check whether the file already has a `Button`, `InputField`, or similar reusable component I should instantiate via `ref` rather than rebuild.

---

## Step 6: Find space on the canvas

If `get_editor_state` shows existing frames, I call:

```
find_empty_space_on_canvas({ width: 390, height: 844, padding: 80, direction: "right" })
```

This gives me the `x`/`y` coordinates to place the login frame without overlapping what you already have.

---

## Step 7: The `set_variables` call (for absent tokens only)

If the diff in step 3 found missing tokens, I call `set_variables` with exactly and only those:

```
set_variables({
  variables: {
    // Only tokens not present in get_variables() output
    // For example, if surfaceMuted was absent:
    surfaceMuted: { type: "color", value: [
      { value: "#F0F0F1", theme: { mode: "light" } },
      { value: "#18181B", theme: { mode: "dark"  } }
    ] },
    // ...other absent tokens
  },
  replace: false
})
```

Two things I never do here:

- I do **not** pass `primary` or `surface` — they came back from `get_variables()`, so they're yours.
- I do **not** use `replace: true` — that would wipe the entire variable set and reconstruct only what I pass, which would destroy your configured values.

`replace: false` is the merge default, but even `replace: false` overwrites the value of any key you include. The protection comes from the diff step — by not including keys that already exist, I guarantee I never touch them.

---

## Step 8: Build the login screen

With tokens confirmed and space located, I make a `batch_design` call to build the `LoginPage_Mobile` frame (390 × 844) at the coordinates from step 6. Every color reference in this call uses `"$primary"`, `"$surface"`, `"$textPrimary"`, etc. — never a raw hex. That means your `#E63946` and `#F8F9FA` are what the login screen actually renders, inherited through the variables you already own.

---

## Summary of what prevents the overwrite

The guarantee is mechanical, not speculative:

1. `get_variables()` is called before any token work — I see what exists.
2. I build an explicit diff: names present in the response are excluded from the `set_variables` argument list.
3. `replace: true` is never used.
4. The `set_variables` call, if made at all, contains zero keys that appeared in the `get_variables()` response.

Your `$primary (#E63946)` and `$surface (#F8F9FA)` are untouched. The login screen binds `"$primary"` and `"$surface"` by reference, so it inherits your brand values exactly.
