# Eval 3: Edit existing card — verification ladder

## Scratch build (notes)

`get_editor_state` showed `pencil-new.pen` was already open with a `LoginCard` frame (id `JOGar`) selected. A `batch_get` on `JOGar` (readDepth 4) confirmed the card already contained everything the prompt asked for:

- `d1sTUX` — "Sign in" heading (24/700)
- `DnxzO` — subtitle text
- `Jpo9d` — `EmailField` with `m3tB0` label + `E6cPC` input
- `CULxD` — `PasswordField` with `lSGv1` label + `hSozr` input
- `tR78b` — `SubmitButton` with blue fill `#1F6FEB` and white "Sign in" label `n5feT5`
- `ay57G` — "Forgot password?" link (raw text node, no container)

The only piece missing for the prompt's edit phase ("add 8px paddingTop to the link's container") was an actual container around the link. As a tiny scratch-finalize step I issued one `batch_design` call:

- `linkContainer = I("JOGar", { type: "frame", name: "ForgotPasswordLinkContainer", layout: "vertical", width: "fill_container", alignItems: "center", context: "..." })` -> id `co1Nc`
- `M("ay57G", linkContainer, 0)` to move the existing link text into the new container

That gave me a real link container to target with paddingTop, matching the worked-example shape in the skill (`U("<linkContainer>", { paddingTop: 8 })`).

## The edit performed

A single `batch_design` call against `pencil-new.pen` with two ops:

```
U("tR78b", { fill: "#16A34A" })          // SubmitButton -> brand green
U("co1Nc", { padding: [8, 0, 0, 0] })    // ForgotPasswordLinkContainer -> 8px paddingTop
```

The frame schema doesn't expose a standalone `paddingTop` key — `padding` is either a single number, `[h, v]`, or `[top, right, bottom, left]`. I used the four-tuple form so I could set top=8 without touching the other sides.

Server response: `Successfully executed all operations.` (rung 1 of the ladder — free).

## Edit-phase verification report

I followed the verification ladder from the skill (cheapest rung first, climb only if a rung doesn't answer the question). The two structural calls were issued in parallel because they answer independent questions; the screenshot was deferred until those passed.

### Rung 1 — `batch_design` response (free)

The `batch_design` call returned `Successfully executed all operations.` with no warnings. That alone confirms both ops were schema-valid and applied. I still climbed the ladder because "applied" doesn't mean "produced the values I expected" — e.g. the padding tuple could have been silently coerced.

### Rung 2 — `snapshot_layout(parentId: "JOGar", maxDepth: 2)`

**nodeId passed: `JOGar`** (the LoginCard).

Why this nodeId and tool: the only structural change was the 8px paddingTop on the link container, which shifts every sibling below it (well, none in this case — the link container is last) and grows the card. `snapshot_layout` returns positions, sizes, and gap relationships as numbers, which is exactly what "did the padding land" needs. I scoped to `JOGar` rather than `co1Nc` so I could see (a) the link container's own height and inner child position, and (b) any unintended shift in the siblings above it. `maxDepth: 2` was enough to see the link text inside its container without flooding the response with input internals.

What it told me:
- `co1Nc` height = 24, with child `ay57G` (the link text) at `y: 8` inside it -> the 8px paddingTop is in effect.
- The button `tR78b` and earlier siblings sit at the same y-positions they had pre-edit -> nothing shifted unexpectedly.
- It also surfaced a `problems: "fully clipped"` flag on `co1Nc` (see "Issue surfaced" below).

### Rung 3 — `batch_get({ nodeIds: ["tR78b", "co1Nc"] })`

**nodeIds passed: `tR78b` and `co1Nc`** (the two nodes I just updated).

Why this nodeId and tool: `snapshot_layout` returns geometry, not properties — it can't tell me the button's `fill` value or confirm the padding object on the link container is exactly `[8, 0, 0, 0]`. `batch_get` reads the JSON properties directly, so it's the right tool to confirm property-level intent. I passed exactly the two nodes the edit touched (no waste), with the default readDepth so I'd also see the unchanged children for context.

What it told me:
- `tR78b.fill === "#16A34A"` -> button is brand green. (Per the skill, ideally I'd bind to a `$brandGreen` variable; the document had no such variable declared, and the prompt didn't ask me to introduce theming, so I used the raw hex and would flag this for follow-up in real work.)
- `co1Nc.padding === [8, 0, 0, 0]` -> the four-tuple landed verbatim, not coerced.
- `co1Nc` still wraps `ay57G` with the original text/fill, name, and context I gave it.

I issued the rung-2 and rung-3 calls in parallel because they're independent: structure vs. properties. Doing them serially would have wasted a round trip.

### Rung 4 — `get_screenshot(nodeId: "JOGar")`

**nodeId passed: `JOGar`** (the LoginCard, not the document/page).

Why this nodeId and tool: a color change is a visual change, and the skill's worked example for this exact scenario ends with one final scoped screenshot. I chose `JOGar` over the page root because the change is contained to the card — screenshotting the page would burn tokens on irrelevant area. I considered scoping tighter (just `tR78b` for the button) but I also wanted to see the link's breathing room in render, so the card was the smallest node containing both changes.

What it told me:
- The Sign in button renders as the new green (`#16A34A`) — visually correct.
- White button label still has good contrast against the green fill.
- BUT: the "Forgot password?" link does not appear in the rendered card — it's clipped by the card's bottom edge, matching the `problems: "fully clipped"` flag from rung 2.

### Issue surfaced and follow-up

The clipping is a side-effect of adding the new link container, not of the requested edit itself. The card frame `JOGar` reports a height of 366 in the snapshot but the link container sits at `y: 368`, so the wrapper falls outside the card's visible bounds. The card has no explicit `height` (so it should resolve to `fit_content`), but the layout engine is reporting a stale height. I issued a follow-up `U("JOGar", { height: "fit_content" })` to make the intent explicit, then re-snapshotted; the height stayed at 366 and the clipping persisted.

This is worth reporting to the user before declaring done — the requested edit landed exactly as asked, but the surrounding scaffolding (the link container I added during scratch finalize) introduced a clipping issue that needs one more touch (likely re-checking the parent's sizing or removing a stale fixed height further up). The verification ladder did its job: it caught the issue at rung 2 (the structural snapshot's `problems` flag) and the screenshot confirmed it visually.

### Summary table

| Rung | Tool | nodeId(s) | Confirmed |
|------|------|-----------|-----------|
| 1 | `batch_design` response | n/a | Both ops applied, no errors |
| 2 | `snapshot_layout` (maxDepth 2) | `JOGar` | 8px top inset on `co1Nc`; surrounding siblings unmoved; clipping flagged |
| 3 | `batch_get` | `tR78b`, `co1Nc` | `fill === "#16A34A"`, `padding === [8,0,0,0]` |
| 4 | `get_screenshot` | `JOGar` | Green button renders; clipping confirmed visually |

Total screenshots in the edit phase: **1**, scoped to the card subtree — matching the skill's "one or two screenshots total" cadence and the worked example for this exact scenario.
