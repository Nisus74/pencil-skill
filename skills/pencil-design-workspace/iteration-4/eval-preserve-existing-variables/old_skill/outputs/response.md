Good question — protecting existing tokens is the first thing I'd do, before touching variables at all. Here's the exact sequence.

## Step 1: Call get_variables() first — no exceptions

Before I write a single token, I call:

```
get_variables()
```

This returns the full current variable set for the open document. In your case, I'd expect to see something like:

```json
{
  "primary": { "type": "color", "value": [
    { "value": "#E63946", "theme": { "mode": "light" } },
    { "value": "#E63946", "theme": { "mode": "dark" } }
  ]},
  "surface": { "type": "color", "value": [
    { "value": "#F8F9FA", "theme": { "mode": "light" } },
    { "value": "#0B1117", "theme": { "mode": "dark" } }
  ]}
}
```

(Your dark-mode values may differ — I'll see exactly what's there.)

This call is the source of truth. Everything after it flows from what I actually received, not from what I assumed.

## Step 2: Diff against the tokens a login screen needs

A login screen typically needs: `surface`, `textPrimary`, `textMuted`, `border`, `primary`, `danger` (for inline validation errors), `focusRing`, and the spacing/type scale. I hold the `get_variables()` result in mind and compare it against that list.

For each token I'd need:

- **Already present?** I use it as-is, binding `"$primary"` and `"$surface"` in my `batch_design` ops. I do not re-declare it.
- **Missing?** I add only the absent tokens in a targeted `set_variables` call.

In your case `primary` and `surface` are both present, so I won't touch their values at all. I'd only add what's genuinely absent — say, `textPrimary`, `textMuted`, `border`, `danger`, `focusRing`, and the spacing/type scale if those aren't in the document yet.

## Step 3: set_variables — only the gaps, replace: false

I call `set_variables` with exactly the tokens that were missing from `get_variables()`:

```
set_variables({
  variables: {
    textPrimary: { type: "color", value: [
      { value: "#0B1117", theme: { mode: "light" } },
      { value: "#FAFAFA", theme: { mode: "dark"  } }
    ] },
    textMuted: { type: "color", value: [
      { value: "#52525B", theme: { mode: "light" } },
      { value: "#A1A1AA", theme: { mode: "dark"  } }
    ] },
    border: { type: "color", value: [
      { value: "#E4E4E7", theme: { mode: "light" } },
      { value: "#27272A", theme: { mode: "dark"  } }
    ] },
    danger: { type: "color", value: [
      { value: "#DC2626", theme: { mode: "light" } },
      { value: "#F87171", theme: { mode: "dark"  } }
    ] },
    focusRing: { type: "color", value: [
      { value: "#E63946", theme: { mode: "light" } },
      { value: "#E63946", theme: { mode: "dark"  } }
    ] }
    /* ...spacing and type scale tokens similarly, only if absent */
  },
  replace: false
})
```

Two things to note:

- `replace: false` is non-negotiable here. It merges new tokens into the existing set. `replace: true` would wipe your `$primary` and `$surface` and replace them with whatever I passed — that's almost never what you want when the document already has tokens configured.
- I've set `focusRing` to match your `#E63946` brand red, since a login screen's focus ring should echo the brand primary. If your existing tokens already define a focus style differently, I'd defer to whatever `get_variables()` returned.

## Step 4: Then batch_design for the login screen

Only after the token state is confirmed do I start building the layout. Every color property in my `batch_design` ops will reference variables by name — `fill: "$primary"`, `textColor: "$textPrimary"`, `fill: "$surface"`, `stroke: "$border"` — never raw hex. This means your existing `#E63946` and `#F8F9FA` values flow through automatically via the variables you've already configured; I never touch their definitions.

## Why this order matters

If I called `set_variables` with a full default token suite first — before reading what's in the document — I'd risk overwriting `$primary` with a generic blue (`#1F6FEB`) and `$surface` with a plain white (`#FAFAFA`), both of which are the defaults I'd reach for on a blank document. Your brand tokens would be gone. The `get_variables()` call before anything else is the only reliable safeguard against that.

## Summary of the sequence

1. `get_editor_state()` — confirm the host is connected and the file is open
2. `get_variables()` — read every token currently in the document
3. Diff: identify which tokens the login screen needs that are absent
4. `set_variables({ variables: { ...only absent tokens... }, replace: false })` — add gaps only
5. `find_empty_space_on_canvas()` — locate a clear position if there are existing frames on the canvas
6. `batch_design` — build the login screen using `$primary`, `$surface`, and all other tokens by reference

Your `$primary` and `$surface` are never touched.
