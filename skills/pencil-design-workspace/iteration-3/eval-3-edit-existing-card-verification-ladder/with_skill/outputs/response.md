# Eval 3 — Edit existing card, verification ladder

## What I built (setup phase)

A fresh `pencil-new.pen` scratch document containing one top-level frame `LoginCard` (`Akbiu`) with:

- `HeadingText` (`urXGi`) — "Sign in", 24px / weight 600, `$textPrimary`
- `EmailField` (`RyVVk`) — vertical stack: `EmailLabel` + `EmailInput` (`dACKe`) holding `EmailPlaceholder` "you@example.com"
- `PasswordField` (`eKMV4`) — vertical stack: `PasswordLabel` + `PasswordInput` (`OxS4R`) holding masked placeholder
- `SignInButton` (`EWMK8`) — primary CTA, fill `$primary` (blue), 44px tall, center-aligned label
- `ForgotPasswordRow` (`iFIRR`) — row with centered `ForgotPasswordLink` (`v4Ad8M`)

All colors come from theme-aware variables (`mode: light/dark`) including a pre-declared `$brandGreen`. Every node has a meaningful PascalCase name and every non-trivial node has a `context`.

## The edit

Two property updates in a single `batch_design` call:

```
U("EWMK8", { fill: "$brandGreen" })          // button: blue → brand green
U("iFIRR", { padding: [8, 0, 0, 0] })        // link container: +8px paddingTop
```

(Note: the `.pen` schema's 4-tuple padding is `[top, right, bottom, left]`, so `paddingTop: 8` is `[8, 0, 0, 0]`. I initially typed `[0, 0, 0, 8]` and corrected it on the next call.)

## Edit-phase verification report

I walked the verification ladder from the skill (cheapest rung first, stopping when each rung's question was answered). I scoped every call to the smallest meaningful node id rather than the document/canvas.

### Rung 1 — `batch_design` response (free)

**Tool:** `batch_design` itself.
**What it told me:** "Successfully executed all operations." Both `U` ops were accepted server-side, so the file *has* been mutated. This rung confirms the write reached the editor; it does not confirm the *new* values are what I intended (e.g. it would still report success if I'd typo'd `$brnadGreen` and the server had silently accepted it as a literal string — though in practice the server validates variable refs, this rung doesn't *prove* the value resolved).

### Rung 2 — `snapshot_layout` (structural, cheap)

**Tool:** `mcp__pencil__snapshot_layout`
**Args:** `parentId: "Akbiu"` (the LoginCard, the smallest subtree containing both changed nodes), `maxDepth: 2`.
**Why this nodeId:** The button and the link container are both direct children of `Akbiu`. Passing the LoginCard means I see the row positions of all five children plus one level of grandchildren — exactly enough to confirm the link's top padding is real without dragging the rest of the canvas through the response.
**What it told me:**
- `iFIRR` is at `y=317`, `height=24`, and the link text `v4Ad8M` inside it sits at local `y=8`. That `y=8` is the visible signature of an 8px top padding — if I hadn't applied it, the text would sit at `y=0`.
- `EWMK8` is at `y=253`, `height=44`. Nothing else shifted unexpectedly: the `EmailField` and `PasswordField` are still at `y=81` and `y=167`, the button still 44px tall. So the only structural change is the one I intended.

This rung answers "did the structural change land?" yes. It does **not** answer the color change — colors aren't structure. So I went to rung 3 for that.

### Rung 3 — `batch_get` (property, cheap)

**Tool:** `mcp__pencil__batch_get`
**Args:** `nodeIds: ["EWMK8", "iFIRR"]` — the two changed nodes only.
**Why these nodeIds:** Property checks should be as targeted as possible. I do not need the children's properties (the label inside the button, the link text inside the row) — those didn't change. Passing only the two parents I touched keeps the JSON small and answers the exact question.
**What it told me:**
- `EWMK8.fill` = `"$brandGreen"` — string-equal to the variable I intended. The server accepted the variable reference (not a raw hex), so the theme axis still works.
- `iFIRR.padding` = `[8, 0, 0, 0]` — matches the corrected value.

Together with rung 2's positional evidence, the structural and property intent are both confirmed. At this point I could have stopped — the change is provably correct. The skill recommends rung 4 only when the question is genuinely visual.

### Rung 4 — `get_screenshot` (visual, expensive — used once for sign-off)

**Tool:** `mcp__pencil__get_screenshot`
**Args:** `nodeId: "Akbiu"` (the LoginCard, **not** the document or any larger frame).
**Why this nodeId:** The change is visual in nature — the user asked for a *brand green* fill and *breathing room*. Rungs 2 and 3 prove the values landed; only a render proves "brand green" actually reads as green against the card background and that 8px reads as breathing room and not a visual hiccup. The smallest subtree containing both changes is the LoginCard itself. Screenshotting the document or a wrapping page frame would burn tokens on whitespace.
**What it told me:** Button now renders as a clean green; "Forgot password?" sits with visible separation under it; nothing else shifted. Passes contrast against the white card.

### Why I did *not* re-screenshot dark mode

The skill's dual-mode rule: re-screenshot the alternate mode only if the design uses mode-conditional colors *and* there's reason to suspect they were set wrong. `$brandGreen` was declared with both light (`#16A34A`) and dark (`#22C55E`) values up front, and the button binds to the variable, not a raw hex. The variable system guarantees the dark value will be used when the mode flips — no second screenshot needed.

### Tool-call order summary

1. `batch_get(["EWMK8", "iFIRR"])` — *pre-edit* locate, to confirm current state and that I had the right ids.
2. `batch_design(U EWMK8, U iFIRR)` — the edit. (Followed by a one-op corrective `batch_design` to fix the padding tuple order.)
3. `snapshot_layout(parentId: "Akbiu", maxDepth: 2)` — rung 2, structural.
4. `batch_get(["EWMK8", "iFIRR"])` — rung 3, property.
5. `get_screenshot(nodeId: "Akbiu")` — rung 4, visual sign-off.

Total screenshots: **1**, scoped to the smallest meaningful subtree (the LoginCard, id `Akbiu`).
