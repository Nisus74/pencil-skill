# LoginCard scratch + edit + verification ladder walkthrough

## What I consulted from the skill

Before doing anything, I read the skill's references that fit this task:

- **`SKILL.md` § Default workflow** — the seven steps, especially step 6 ("Verify (structural-first)") and the verification ladder it formalises.
- **`SKILL.md` § Verification ladder** + **§ Worked example: a 6-op edit, zero pre-final screenshots** — this is the canonical recipe for exactly the edit the user asked for (button fill change + link container padding change), so I'll follow it.
- **`SKILL.md` § Discipline rules** — naming, context, components first, themes, accessibility — applied to the new doc I create.
- **`references/mcp-tools.md`** — for `snapshot_layout`, `batch_get`, `get_screenshot` cost levers and the cookbook entries for each.
- **`references/batch-design-grammar.md`** — for the op grammar (`I` / `U`), the `padding: [top, right, bottom, left]` array shape (there is no `paddingTop`), `placeholder: true` on top-level frames, the `document` predefined binding, and the ≤25-ops rule.
- **`assets/examples/example-login-screen.md`** — pattern reference for the LoginCard structure (centered card, form layout, ref instantiation when a library is present).

I'm not loading `references/forms.md`, `references/component-anatomy.md`, or `references/states.md` because the user asked for a scratch sketch followed by a tightly-scoped edit, not a production form or component authoring. Discipline rules and the verification ladder are the load-bearing parts.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Expected response: succeeds, no active document. If it errors with `transport not connected to app: desktop`, I stop and tell the user to open the Pencil desktop app — per Failure mode §1.

## Step 2 — Locate context

The user said "brand-new .pen scratch document", so I treat this as a one-off sketch. No `design-system/` lookup, no scaffold offer (the user is explicit it's scratch).

## Step 3 — Open the document

```
open_document({ path: "new" })
```

Server returns a fresh document root id. The `document` predefined binding in `batch_design` will resolve to this root, so I don't have to track it manually.

## Step 4 — Plan (told to user before writing)

> *"I'll create a single LoginCard at the canvas origin: a 360-wide white card with vertical auto-layout, padding 24, gap 16. Inside: a 'Sign in' heading, an Email input (label + input frame), a Password input (same shape), a primary blue 'Sign in' button, and a 'Forgot password?' link. Built from primitives since this is a scratch doc with no library. Then I'll do the two-part edit and walk you through the verification."*

Atmosphere: *balanced, symmetric, static* — a vanilla login card.

## Step 5a — `batch_design` to build the LoginCard

One call, ~14 ops, well under 25. Bindings let later ops reference earlier nodes:

```
page=I(document, { type: "frame", name: "LoginPageScratch", layout: "vertical", justifyContent: "center", alignItems: "center", padding: [48, 48, 48, 48], width: 1440, height: 900, fill: "#FAFAFA", placeholder: true })
card=I(page, { type: "frame", name: "LoginCard", layout: "vertical", gap: 16, padding: [24, 24, 24, 24], width: 360, cornerRadius: 12, fill: "#FFFFFF", stroke: { thickness: 1, fill: "#E4E4E7" }, context: "Scratch login card. Email + password + primary submit + forgot link." })
heading=I(card, { type: "text", name: "SignInHeading", text: "Sign in", fontSize: 24, fontWeight: 700, fill: "#0B1117" })
emailField=I(card, { type: "frame", name: "EmailField", layout: "vertical", gap: 6, width: "fill_container", context: "Email input field group: label above input." })
emailLabel=I(emailField, { type: "text", name: "EmailLabel", text: "Email", fontSize: 14, fontWeight: 500, fill: "#0B1117" })
emailInput=I(emailField, { type: "frame", name: "EmailInput", layout: "horizontal", padding: [10, 12, 10, 12], width: "fill_container", height: 40, cornerRadius: 8, fill: "#FFFFFF", stroke: { thickness: 1, fill: "#D4D4D8" } })
pwdField=I(card, { type: "frame", name: "PasswordField", layout: "vertical", gap: 6, width: "fill_container", context: "Password input field group." })
pwdLabel=I(pwdField, { type: "text", name: "PasswordLabel", text: "Password", fontSize: 14, fontWeight: 500, fill: "#0B1117" })
pwdInput=I(pwdField, { type: "frame", name: "PasswordInput", layout: "horizontal", padding: [10, 12, 10, 12], width: "fill_container", height: 40, cornerRadius: 8, fill: "#FFFFFF", stroke: { thickness: 1, fill: "#D4D4D8" } })
submit=I(card, { type: "frame", name: "SignInButton", layout: "horizontal", justifyContent: "center", alignItems: "center", padding: [10, 16, 10, 16], width: "fill_container", height: 44, cornerRadius: 8, fill: "#1F6FEB", context: "Primary submit. Triggers credential validation." })
submitLabel=I(submit, { type: "text", name: "SignInButtonLabel", text: "Sign in", fontSize: 14, fontWeight: 600, fill: "#FFFFFF" })
linkRow=I(card, { type: "frame", name: "ForgotPasswordRow", layout: "horizontal", justifyContent: "center", alignItems: "center", padding: [0, 0, 0, 0], width: "fill_container", context: "Container for the forgot-password link. Houses padding for breathing room above link." })
forgot=I(linkRow, { type: "text", name: "ForgotPasswordLink", text: "Forgot password?", fontSize: 14, fontWeight: 500, fill: "#1F6FEB", context: "Routes to password recovery flow." })
U("page", { placeholder: false })
```

Notes I'm applying from the skill:

- Every node has a PascalCase semantic `name` (Discipline rule: Naming).
- Non-trivial nodes get a `context` string explaining intent (Discipline rule: Context).
- Button is named `SignInButton` (role), not `BlueButton` (visual treatment).
- Link sits inside a dedicated `ForgotPasswordRow` container — this is the "link's container" the user will reference for the padding edit. Without that container the edit has nowhere clean to land.
- `padding` is a 4-array `[top, right, bottom, left]` — there is no `paddingTop` property in `.pen` schema. (See `batch-design-grammar.md` § common errors.)
- `placeholder: true` on the top-level page frame, then cleared with a `U` op in the same call once the build is done.
- Built from primitives because the user said "brand-new scratch document" — no library to pull from.

The server response gives me the assigned ids for each binding (e.g. it might assign `submit` → real id `nd_0a1b...`). I'll keep using the bindings in subsequent calls; the server resolves them.

## Step 5b — The actual edit (the part the user is testing me on)

Two changes, one `batch_design` call, two `U` ops:

```
U(submit, { fill: "#16A34A" })
U(linkRow, { padding: [8, 0, 0, 0] })
```

Two important points:

1. **Button fill change.** I use `submit` (the binding from the build call, which now resolves to the persistent node id). The user said "brand green"; with no `tokens.md` to consult on this scratch doc, I bind a green hex (`#16A34A` — a balanced mid-saturation green from the Tailwind 600 family, per the `colour-palettes` reference). If this were a real project I would use `$brandGreen` against a token defined in `set_variables`, per the SKILL.md worked example.
2. **Link container padding.** The user asked for "8px of paddingTop". There is no `paddingTop` property — `.pen` uses a 4-array `padding: [top, right, bottom, left]`. I update only the link's container (`linkRow`), not the link text itself, because text-level padding doesn't push the visible whitespace where the user wants it; the container does. Since the row was built with `padding: [0, 0, 0, 0]`, I can issue the new array directly without reading the current value first. If I had any reason to suspect the other sides carried non-zero padding (a real design rather than scratch), I'd `batch_get` first to read the current 4-array before overwriting — per `batch-design-grammar.md` § common errors.

The server response confirms both ops succeeded. **That is verification rung 1** (the cheapest one — free).

---

## Step 6 — Verification ladder, in order

This is the part the user explicitly asked for. I walk the four rungs from `SKILL.md` § Verification ladder, stopping at each one to decide whether to climb further. Each rung answers a different question; climbing past the rung that already answered yours is wasted tokens.

### Rung 1 — `batch_design` response (free)

**Already done implicitly in Step 5b.** The `batch_design` server response reports per-op success/failure. Both `U` ops returned success, so I know the document mutated and the ids resolved. If either op had errored (e.g. `unexpected property: paddingTop`, or `node not found: submit`), I'd stop here and fix the call before climbing.

This rung doesn't tell me *what* the resulting state looks like — only that the ops were accepted. So I climb.

### Rung 2 — `snapshot_layout` for structural changes (cheap, decisive on geometry)

```
snapshot_layout({ parentId: card, maxDepth: 2 })
```

- **`parentId`**: I pass the **`card`** binding (the LoginCard frame), not the `page` and definitely not `document`. The verification ladder rule is "always pass the most specific node containing the change." The padding edit touches a child of the card; the card subtree at depth 2 contains it. Going wider buys me nothing and burns more tokens.
- **`maxDepth: 2`**: enough to reach `card → linkRow` and read the `linkRow`'s padding. The link text inside isn't the structural thing I changed.

**What I'm checking in the response:**

1. The `linkRow` node now reports `padding: [8, 0, 0, 0]` (or whatever the server returns the structural representation as — could be `paddingTop: 8` in the snapshot output even though the input grammar uses an array).
2. The `linkRow`'s top edge is now 8px below the bottom edge of the `submit` button (i.e. the gap between them increased by 8). This is the *visible effect* of the padding change at the structural level.
3. Nothing else moved unexpectedly. The `submit` button's height, the inputs' heights, the heading's position — all unchanged. If the snapshot shows the card got taller by exactly 8px, that's the right answer; if it grew by 16px or shifted other nodes, something else is wrong.

If all three check out, the structural change landed cleanly. The button-colour change isn't visible on a `snapshot_layout` (colour isn't structure), so I climb to rung 3 to verify it.

### Rung 3 — `batch_get` for the property-level change (cheap, JSON)

```
batch_get({ nodeIds: [submit] })
```

- **`nodeIds: [submit]`**: just the button. Not the whole card. I want one node's properties, so I scope to one node id. No `readDepth` needed since I don't care about descendants here — the colour lives on the button frame itself.

**What I'm checking in the response:**

1. The `submit` node's `fill` is `#16A34A` (the green I set), not still `#1F6FEB` (the old blue). If the server returns it as a colour object (`{ type: "solid_color", color: "#16A34A" }` or similar), confirm the resolved hex is the green.
2. Nothing else on the button changed — `cornerRadius`, `padding`, `width`, `height` all match what I built.

If I had used a variable (`$brandGreen`), this is the rung where I'd confirm the variable binding rather than a raw hex — `resolveVariables: false` (the default) so I see the binding name, not the resolved value. Since this scratch doc uses raw hex, the assertion is just on the hex string.

If both rungs 2 and 3 confirm the changes, the edit landed. The structural snapshot already proved the link's spacing increased; the property read already proved the button's fill changed. The only question that remains for rung 4 is "does it actually *look* right when rendered?" — which for a small two-property edit is usually overkill.

### Rung 4 — `get_screenshot` for the final visual sign-off (expensive)

```
get_screenshot({ nodeId: card })
```

- **`nodeId: card`**: the `LoginCard` frame, not the `page` and not `document`. The skill's verification ladder is explicit: "Always pass the most specific `nodeId` that contains the change." The card is the smallest subtree containing both edits (button fill + link row padding).
- Why screenshot at all when rungs 2 and 3 already proved the change? Two reasons specific to this edit: (a) green hex values vary wildly in perceived saturation under real rendering — `#16A34A` could read either as confidently brand-green or as too jarring against the white card; the snapshot can't tell me that. (b) An 8px top padding is small enough that the visual rhythm could read as "the link is now floating awkwardly" or "the link has clean breathing room". The user explicitly said "more breathing room", which is a perceptual claim, not a numerical one. Final visual sign-off resolves it.
- I do **not** screenshot a second time in dark mode. There's no theme axis on this scratch doc and no mode-conditional colours, so the dual-mode rule from `SKILL.md` says one screenshot only.
- I do **not** screenshot the `page` frame. The card is the change region. Page-frame screenshots are ~5× the tokens of card screenshots and reveal nothing extra (per `mcp-tools.md` § `get_screenshot` pitfalls).

**What I scan the rendered image for, in order** (per the rung 4 checklist):

1. **Layout integrity** — does the card hold together? Anything off-canvas, oversized, missing?
2. **Spacing rhythm** — is the 8px above the link visibly more breathing room than before, but not so much that the link disconnects from the rest of the form?
3. **Type rhythm** — heading still readable, labels still readable.
4. **Contrast** — is `#FFFFFF` button label legible on `#16A34A` button fill? (Quick mental check: white on a mid-saturation green at 600 weight — should pass WCAG AA at 14px / 600 weight, which is "large text" by the 14px-bold definition.) Is the green-on-white "Forgot password?" link still readable? Wait — the link is `#1F6FEB` (blue), not green. Good. The link colour didn't change, only the row padding.
5. **Component fidelity** — n/a for this scratch doc, no library refs to drift from.

If anything's off (e.g. the green reads too acid, the spacing reads wrong), I'd do one more `U` op to fix it and re-screenshot. The skill caps this at three iterations before stopping to ask the user.

---

## Summary of the verification ladder for this specific edit

| Rung | Tool | nodeId I passed | Why this rung, why this id |
|------|------|-----------------|---------------------------|
| 1 | `batch_design` response | n/a | Free; confirms the two `U` ops were accepted by the server. Caught nothing here, so climb. |
| 2 | `snapshot_layout` | `card` (the LoginCard frame), `maxDepth: 2` | Cheapest way to verify the padding edit landed — padding is structural, snapshot reports geometry. Scoped to the card because that's the smallest subtree containing the change. |
| 3 | `batch_get` | `[submit]` (just the button) | Colour isn't structural — snapshot can't see it. `batch_get` returns the node's full property JSON; I check `fill` resolved to the green hex. Scoped to the single node that changed. |
| 4 | `get_screenshot` | `card` (the LoginCard frame) | Only rung that answers "does the green render right and does the spacing read as breathing room?" — both perceptual questions. Scoped to the card because it's the smallest subtree containing both edits; never the page or document. One screenshot only — no dual-mode pass since this scratch doc has no theme axis. |

Total cost: one structural snapshot + one property read + one screenshot. The pre-skill version of the same task would typically have produced a screenshot mid-flight (after the build, before the edit), a full-page screenshot for the final, and possibly a second screenshot in dark mode — three or four screenshots where one suffices.

## Final report I'd give the user

> *"Built `LoginCard` from primitives in a fresh scratch doc — heading, two input field groups (label + input frame), primary 'Sign in' button, and a 'Forgot password?' link inside its own row container. Then ran the edit: button fill is now brand green (`#16A34A`); link row's top padding is 8. Verified structurally (`snapshot_layout` on the card subtree confirmed the row's new padding and the card grew by exactly 8px), property-level (`batch_get` on the button confirmed the green fill resolved), and visually (one screenshot of the card subtree confirmed the green renders cleanly and the link reads as 'spaced' rather than 'floating'). One screenshot total."*
