# Adding a login screen without clobbering your custom tokens

Good question to ask before I touch anything. The footgun here is real: `set_variables` defaults to `replace: false`, but that "merge" mode still overwrites any key you pass. So if I send `primary: { value: "#1F6FEB" }` and you've already set `primary` to `#E63946`, your red is gone with no warning. Same trap exists if I do `U("doc", { variables: { ... } })` inside a `batch_design` call.

Here's the exact sequence I'd run before either `set_variables` or `batch_design` touches your tokens.

## Step 1 — Confirm the host is reachable and your file is the active document

```
get_editor_state({ include_schema: false })
```

I'd check the response shows your `.pen` is the active document and note its root id. If the call errors with `transport not connected to app: desktop`, I stop and tell you to open the Pencil desktop app or IDE extension. No silent CLI fallback.

## Step 2 — Read your existing tokens before anything else

This is the mandatory step that protects your `$primary` and `$surface`:

```
get_variables()
```

The response is keyed by variable name with `{ type, value }` per entry. Theme-aware variables like yours return a `value` array of `{ value, theme }` entries. So I'd expect something roughly like:

```
{
  primary: { type: "color", value: [
    { value: "#E63946", theme: { mode: "light" } },
    { value: "#E63946", theme: { mode: "dark"  } }   // or whatever you set for dark
  ] },
  surface: { type: "color", value: [
    { value: "#F8F9FA", theme: { mode: "light" } },
    { value: "...",     theme: { mode: "dark"  } }
  ] },
  // ...any other tokens you've set
}
```

What I'd verify in the response:

- `$primary` resolves to `#E63946` in light mode (matches what you said).
- `$surface` resolves to `#F8F9FA` in light mode (matches what you said).
- Both have a `dark` entry. If they don't, that's a real concern — the skill's discipline rule is that every color carries both light AND dark values, and a missing dark entry will render badly under `theme: { mode: "dark" }`. I'd surface that to you before designing, not silently add a dark value myself, since picking a dark counterpart for your brand red is a brand decision.
- Note every other token name present (text colors, borders, spacing scale, type scale, etc.).

I'd hold that full list in mind. The rule from here on is: **never include a key that already exists in the `get_variables()` response in any subsequent `set_variables` call or `U("doc", { variables: {...} })` op.**

## Step 3 — Check your theme axis already exists

```
get_editor_state({ include_schema: false })
```

(I already have this from step 1; I'd just look at the document's `themes` field in that result.) If `themes.mode` is already `["light", "dark"]`, I do not re-issue `U("doc", { themes: ... })` — re-declaring the axis is unnecessary and risks side effects.

## Step 4 — Inventory your library components

Before I plan a login screen I check what reusable components you already have, because building inputs and buttons from primitives when you have an `Input` and `ButtonPrimary` in your library is the maintenance bug the skill calls out:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Then, for each entry in your document's `imports`:

```
batch_get({ filePath: "<your-library>.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

This doesn't touch tokens, but it's part of the same "read everything authoritative before writing" discipline that protects your work.

## Step 5 — Decide what tokens (if any) the login screen actually needs added

A login screen typically needs: surface, surface muted, border, text primary, text muted, primary, focus ring, danger (for validation errors), plus spacing and type scales. I'd diff that wishlist against the `get_variables()` response from step 2:

- `$primary` — already set to your `#E63946`. **Skip.**
- `$surface` — already set to your `#F8F9FA`. **Skip.**
- Every other token from the wishlist — only add those that are absent from your response.

If your document already has a complete token set, I skip the bootstrap entirely and go straight to `batch_design`.

## Step 6 — If (and only if) some tokens are missing, run a scoped `set_variables`

```
set_variables({
  variables: {
    // ONLY tokens that did NOT appear in get_variables() output.
    // Your $primary and $surface are deliberately omitted.
    border: { type: "color", value: [
      { value: "#E4E4E7", theme: { mode: "light" } },
      { value: "#27272A", theme: { mode: "dark"  } }
    ] },
    textMuted: { type: "color", value: [
      { value: "#52525B", theme: { mode: "light" } },
      { value: "#A1A1AA", theme: { mode: "dark"  } }
    ] },
    // ...etc, only the absent ones
  },
  replace: false
})
```

I'd never pass `replace: true` unless you told me explicitly to reset tokens — that wipes the whole variable set.

## Step 7 — Verify your tokens survived before designing

Belt and braces. After `set_variables`, run `get_variables()` again and confirm `$primary` is still `#E63946` and `$surface` is still `#F8F9FA`. If either changed, I made a mistake and I stop to tell you, not push forward.

## Step 8 — Now plan and run `batch_design`

Once tokens are confirmed safe, I'd plan the screen out loud (form card width, components I'm instantiating from your library, layout) and only then issue the `batch_design` call. The login frame would bind `fill: "$surface"` and the submit button's fill would resolve through your library's `ButtonPrimary` (which presumably uses `$primary`) — meaning your `#E63946` is what shows up, automatically.

## Summary of the protection chain

1. `get_variables()` first, always — read your existing token values before any token-touching write.
2. Compare wishlist against the response; only add what's missing.
3. `set_variables` with `replace: false` and a payload that contains zero existing keys.
4. Re-read with `get_variables()` to confirm `$primary` and `$surface` are untouched.
5. Then `batch_design`.

The single most important line: **`replace: false` doesn't protect existing values; it just merges. The protection is in not passing the key at all.**

## References I consulted

- `SKILL.md` — the Themes discipline rule (the `get_variables()` precondition for any token work) and Failure mode 7 "Token clobber", which spells out the exact bug this question is asking about.
- `references/mcp-tools.md` — the `get_variables` and `set_variables` cookbook entries; the `set_variables` pitfalls section explicitly calls out that `replace: false` overwrites on key collision and tells you to call `get_variables()` first and only pass absent keys.
- `assets/examples/example-login-screen.md` — the canonical workflow shape for this screen type (frame structure, library refs, verification ladder), so the rest of the design after the token-protection step matches the skill's worked example.
