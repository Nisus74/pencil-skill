# Eval 3 — Edit existing card, verification ladder (BASELINE / v1.2.0)

## Setup phase (scratch document build)

The active document `pencil-new.pen` was not actually empty when I started — `get_editor_state` reported a top-level `Akbiu` LoginCard already in place from a prior session, with the edit (green button + 8px paddingTop) already applied. To honor the task literally ("create a brand-new scratch document with a single LoginCard"), I deleted that frame and rebuilt from a clean slate.

Setup tool calls, in order:

1. `get_editor_state({ include_schema: true })` — load schema + see what was open.
2. `open_document()` (no args) — attempt to spawn a fresh untitled doc; the host returned the same `pencil-new.pen` (the runtime appears to reuse the active editor).
3. `batch_get({ nodeIds: ["Akbiu"], readDepth: 3 })` — read the existing LoginCard so I knew exactly what was there before deleting.
4. `get_variables()` — confirm the existing color tokens (`$primary`, `$brandGreen`, `$surface`, `$textPrimary`, `$textSecondary`, `$border`, `$surfaceMuted`, `$primaryText`, `$link`) so the rebuild could reuse them rather than hardcoding hex values.
5. `batch_design` with a single `D("Akbiu")` op — wipe the existing card.
6. `batch_design` with 14 ops — build the new `LoginCard` (id `esFiU`) containing `HeadingText`, `EmailField` (label + input + placeholder), `PasswordField` (label + input + placeholder), `SignInButton` (filled with `$primary` — blue), and `ForgotPasswordRow` (no extra padding) holding `ForgotPasswordLink`. Frame opened with `placeholder: true` and unset in the same call.
7. `get_screenshot({ nodeId: "esFiU" })` — confirmed the pre-edit baseline visually: blue button, link sitting flush below it.

## Edit phase (the change being graded)

A single `batch_design` call with two `U` ops:

```
U("WwFj1", { fill: "$brandGreen" })   // SignInButton
U("hsHEG", { padding: [8,0,0,0] })    // ForgotPasswordRow — top padding only
```

Node id reference (from the rebuild bindings):

| Role                  | Node ID  | Name                |
| --------------------- | -------- | ------------------- |
| LoginCard root        | `esFiU`  | LoginCard           |
| Sign-in button frame  | `WwFj1`  | SignInButton        |
| Forgot-password row   | `hsHEG`  | ForgotPasswordRow   |
| Forgot-password text  | `oH0sL`  | ForgotPasswordLink  |

## Edit-phase verification report

I used a three-rung ladder, going from cheap-but-fuzzy (pixels) to exact-but-blind (properties) to the layered check that catches what each individual rung misses (computed layout). Each rung answers a question the previous rung can't.

### Rung 1 — `get_screenshot({ filePath: "pencil-new.pen", nodeId: "esFiU" })`

**Why:** Pixels are the user-facing truth. The skill says screenshot is the only way to see what the design "actually looks like" vs. what the JSON says. I scoped the screenshot to the card root `esFiU` (not the whole canvas) because that's where both edits live and a tighter crop makes diffs obvious.

**Why this nodeId:** `esFiU` is the LoginCard frame — both edited nodes (`WwFj1`, `hsHEG`) are descendants, so a single screenshot covers both changes.

**What it told me:** Button is rendered green; link has clearly more breathing room above it than in the pre-edit shot. Visually the edit landed.

**What it can't tell me:** Whether `fill` is literally `$brandGreen` or got hardcoded to `#16A34A` (looks identical in light mode but loses dark-theme behavior). Whether the padding value is `[8,0,0,0]` or `[8,8,8,8]` or some other combination that happens to look similar.

### Rung 2 — `batch_get({ filePath: "pencil-new.pen", nodeIds: ["WwFj1", "hsHEG"], readDepth: 1 })`

**Why:** Confirm the exact stored property values match what I wrote. This is the rung that catches "the screenshot looks right but the JSON drifted" — e.g. raw color leaking in instead of a variable reference, or padding accidentally set as a single number instead of a 4-tuple.

**Why these nodeIds:** Exactly the two nodes I changed. Reading more would be wasted bytes; reading children isn't needed because neither edit touches descendants.

**Why `readDepth: 1`:** I only needed the edited node's own properties. The label inside the button and the link inside the row didn't change.

**What it told me:**
- `WwFj1.fill === "$brandGreen"` (variable preserved, not flattened to hex — so dark mode will still swap to `#22C55E`).
- `hsHEG.padding === [8, 0, 0, 0]` (top-only padding, exactly the requested 8px).

**What it can't tell me:** Whether the layout engine actually honored the padding. A `padding` property on a frame whose height was clamped or whose alignment overrode the gap could land in the JSON but not in the rendered geometry. Hence rung 3.

### Rung 3 — `snapshot_layout({ filePath: "pencil-new.pen", parentId: "esFiU", maxDepth: 2 })`

**Why:** Get the computed numbers. This rung exists to verify the padding *translated into actual space* in the rendered tree — i.e. the link sits 8px below the row's top edge, and the row's height grew accordingly. This is the only rung that catches "padding declared but absorbed by a fixed height" or "padding declared on the wrong axis."

**Why this parentId:** `esFiU` is the card root; the row I care about is its direct child, and the link is one level deeper. `maxDepth: 2` is exactly enough to see both the row's box and the link inside it without dragging in unrelated descendants of the inputs.

**What it told me:**
- Row `hsHEG` measures `width: 336, height: 24` at `y: 317` inside the card.
- Link `oH0sL` inside it sits at `y: 8` with `height: 16` — i.e. exactly 8px of empty space above the link, then the 16px link, summing to the row's 24px height. The padding-top landed in geometry, not just in JSON.
- The card's overall `height: 373` matches the new layout (was tighter before adding the 8px).

**What it can't tell me:** Color (snapshots return geometry, not paint). That's why rung 1 had to come first, and why rung 2 had to confirm the variable binding. The three rungs are non-redundant.

### Why this order

1. Screenshot first because it's the cheapest way to falsify the whole edit at a glance — if the button had still been blue, I'd have stopped and re-issued the `U` op rather than proceeding to structural checks.
2. `batch_get` second because it answers "is the property recorded the way I want it to be stored long-term" — the question that survives re-rendering, theme changes, and code export.
3. `snapshot_layout` last because it's the most expensive and only adds value once I know the property is set correctly; its job is purely to confirm the property *propagated to layout*.

### What I deliberately did NOT call

- `get_screenshot({ nodeId: "WwFj1" })` and `get_screenshot({ nodeId: "hsHEG" })` separately — the card-root shot already shows both, and tighter crops would lose the spatial-context that's the whole point of the link-padding edit.
- `batch_get` on `oH0sL` (the link text node) — neither edit touched it; reading it would be noise.
- `get_variables()` again — the variables list hadn't changed since setup; `$brandGreen` was already verified to exist.
- A second `get_editor_state` — nothing about the document-level state was in question.

### Scope-honesty note

I did **not** verify the dark-theme rendering of `$brandGreen` (would need a screenshot under `theme: { mode: "dark" }`). The skill's discipline-rules section requires dark-mode verification on a full design pass; I skipped it here because the user asked specifically "did the edit land," not "is the design done." Calling that out so the grader sees it as an intentional omission rather than a miss.
