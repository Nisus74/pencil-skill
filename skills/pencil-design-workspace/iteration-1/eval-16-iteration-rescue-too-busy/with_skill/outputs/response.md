# Rescue protocol: "feels too busy and I can't tell where to look"

The user has handed me two diagnoses bundled into one sentence:

1. **Too busy** — the canonical iteration-one failure mode in `references/iteration-patterns.md`.
2. **Hierarchy unclear** — a separate, related failure mode in the same reference, where the eye can't pick a primary.

Both are addressed below. I will NOT add anything to fix this. The most common second-iteration failure (per iteration-patterns.md) is adding a hierarchy element to "fix" busyness — that makes it worse. The rescue is subtractive, full stop.

## References I consulted and why

- `SKILL.md` — confirmed the host-detection step, the verification ladder, the discipline rules, and the routing line that points "design feels off: too busy" straight at `references/iteration-patterns.md`.
- `references/iteration-patterns.md` — owns the diagnosis vocabulary and the rescue recipes for "too busy" and "hierarchy unclear", plus the three-iteration limit and the four-question self-critique gate.
- `references/visual-hierarchy.md` — owns the six levers (size, weight, colour, position, spacing, motion) and the primary/secondary/tertiary discipline. The hierarchy-unclear rescues operate on these.

I did not load `layout-patterns.md`, `microcopy.md`, `style-catalogue.md`, or any greenfield-bootstrap references — this is an existing design needing rescue, not a fresh build.

## Step 1 — Detect the host

```
get_editor_state({ include_schema: false })
```

Expected response shape: `{ documentPath, selection, schemaVersion, imports, viewport, ... }`.

What I'm checking for:

- Did the call succeed at all? If it errors with `transport not connected to app: desktop`, I stop and tell the user to open the Pencil desktop app or IDE extension. No silent CLI fallback.
- Which `.pen` file is currently open and what's the path. I need this to know where the design lives and whether a `.lib.pen` is imported.
- Is anything selected? If the user has a specific frame selected, that's almost certainly the thing they're calling busy. I scope the rescue to that subtree, not the whole document.
- What schema version. Affects which op grammar is valid in `batch_design`.

## Step 2 — Locate the busy frame and inventory components

If nothing is selected, I need to find the "currently open" design surface. From `get_editor_state` I get the top-level frames; if there are multiple (Cover, SourceOfTruth, BuildReady, etc., per `file-architecture.md`) I ask the user which frame they mean before touching anything. "The design" is ambiguous on a populated canvas.

Then:

```
batch_get({ nodeIds: ["<targetFrameId>"], readDepth: 4 })
```

Expected shape: nested JSON with each child's `id`, `type`, `name`, `fill`, `stroke`, `padding`, `gap`, `font`, `text`, plus any `ref`/`reusable` markers and `context` strings.

This is the actual diagnosis call. With the tree in front of me I'm counting six specific things — the rescue depends on which of these are inflated:

| What I count | "Too busy" threshold |
|---|---|
| Distinct accent hues (non-neutral fills) | More than 1 competing accent → drop to one |
| Distinct typefaces in use | More than 2 (heading + body, optionally + mono) → drop one |
| Distinct neutral stops bound | A 5-stop ramp → collapse to 3 |
| Shadow layers per elevation | 4-layer drops → collapse to 2 |
| Decorative borders / dividers / badges | Each one without semantic load is a removal candidate |
| Section padding values | Note the smallest gap; the rescue may bump it one step in the spacing scale |

I also note which elements *should* be primary vs. secondary vs. tertiary (per `visual-hierarchy.md`). If two elements share the same fill saturation, same size, and same prominence, I have my "hierarchy unclear" culprits.

If the document has imports, I do a quick component pass too:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Why: any hand-built primitive that should have been a library `ref` is a hidden source of busyness — it carries arbitrary visual treatment that drifts from the system. Spotting these lets me convert them as part of the rescue.

## Step 3 — Read the design's actual look

```
get_screenshot({ nodeId: "<targetFrameId>" })
```

Scoped to the busy frame, not the whole canvas — the verification ladder rule about always passing the most specific node id applies just as much for diagnosis as for verification. I need pixels here because "busy" is a perception problem, not a structural one. `snapshot_layout` would tell me numbers, but the user's complaint is about visual noise, which is what the screenshot answers.

What I scan for, in this order:

1. **First-glance focal point.** Squint at it (per the four-question gate, question 2). Where does my eye land first? If it lands on a decorative element, a coloured badge, or "everywhere at once" — that confirms the hierarchy diagnosis.
2. **Hue census.** Count the saturated colours. More than one competing accent confirms the busy diagnosis.
3. **Type census.** Count the typefaces and weights. A serif heading + sans body + mono code is the ceiling; anything beyond is overage.
4. **Decorative load.** Borders, shadows, dividers, gradients, glows. Each one I can't justify by "this carries information or marks a state" is a candidate.
5. **Whitespace.** Are sections cramped? Macro whitespace 24–40px on a marketing page is starvation per `visual-hierarchy.md`.

This is the only screenshot I take during diagnosis. I do not screenshot light vs. dark separately — variables guarantee theme behaviour, and I'm not changing tokens, only removing visual load.

## Step 4 — State the rescue plan to the user

Before any `batch_design` call, I tell the user what I'm cutting and why, in 2–3 sentences. Per the skill's plan-before-execute rule. Something like:

> *"You've got three competing accents (the blue button, the purple badge, the teal status pill) plus three typefaces and a 4-layer shadow on every card. I'm going to drop the purple badge to a neutral pill, mute the teal pill to a single-letter dot, collapse the shadow to the standard 2-layer pair, and bump section padding from $space-8 to $space-12. The Sign in CTA stays as the only saturated element on the screen, so the eye has somewhere obvious to land. No new elements; pure subtraction."*

This catches bad assumptions cheaply. If the user says "actually the purple badge is brand-critical", I pivot before burning a `batch_design` call.

## Step 5 — Execute the rescue (subtractive only)

The rescues in iteration-patterns.md "too busy" are ordered by effect. I apply them in that order, stopping when the design calms:

| Rescue | Op shape |
|---|---|
| Drop competing accents | `U("<badgeNodeId>", { fill: "$surfaceMuted" })`, `U("<linkNodeId>", { color: "$textPrimary" })` — collapse non-primary saturated fills onto neutrals. Leave the one primary CTA at full accent. |
| Remove a typeface | `U("<displayHeadingId>", { font: "$fontBody" })` — if a third display font snuck in beside heading + body, demote it. |
| Add macro whitespace | `U("<sectionId>", { padding: [<currentTop+step>, <right>, <currentBottom+step>, <left>], gap: <currentGap+step> })` — increase by one step in the spacing scale, not arbitrary px. Read current padding via `batch_get` first so I preserve the side I'm not changing. Note: there is no `paddingTop` property; it's the `[top, right, bottom, left]` array. |
| Collapse the neutral ramp | If the design uses 5 neutrals, retire the two unused middle stops by replacing references via `replace_all_matching_properties` — but only if I'm confident they're truly unused. Otherwise leave them; this rescue is for verified noise, not theoretical noise. |
| Simplify shadows | `U("<cardNodeId>", { shadow: [{ ...ambientLayer }, { ...directLayer }] })` — the standard 2-layer pair, not the 4-layer pile. |
| Mute decorative borders | `U("<dividerId>", { stroke: { fill: "$borderSubtle" } })` or delete the divider entirely with a `D` op if it's not separating two semantically different regions. Singular `stroke.fill`, not `stroke.fills`. |

For the **hierarchy-unclear** half of the diagnosis (in the same `batch_design` call when possible):

| Rescue | Op shape |
|---|---|
| Pick one primary | If two CTAs both look primary, demote one. `U("<secondaryCtaId>", { variant: "ghost" })` if it's a library button with variants; otherwise `U("<secondaryCtaId>", { fill: "transparent", color: "$textPrimary" })`. |
| Increase one size step on the primary | `U("<primaryHeadingId>", { font: "$text3xl" })` — the headline gets one step bigger. The rest stay put. |
| Spatial separation around the primary | `U("<primaryCtaContainerId>", { padding: [<more>, <more>, <more>, <more>] })` — negative space around the primary is the cheapest hierarchy lever. |

All ops in one `batch_design` call if it stays under 25; split otherwise. Each `U` op preserves only the keys I name, so I won't accidentally clobber unrelated properties.

## Step 6 — Verify (structural before visual)

Walk the ladder, cheapest rung that answers the question:

1. **`batch_design` response.** Did every op land? Free check.
2. **`snapshot_layout({ nodeId: "<targetFrameId>", maxDepth: 3 })`.** Confirm the new padding/gap values landed and nothing shifted unexpectedly. Returns numbers, no image cost.
3. **`batch_get({ nodeIds: [<changedNodeIds>] })`.** Confirm the fill changed to `$surfaceMuted`, the shadow array now has 2 entries not 4, the heading binds `$text3xl`. Property-level check.
4. **`get_screenshot({ nodeId: "<targetFrameId>" })`.** One screenshot, scoped to the rescued frame. The diagnostic question is visual ("is the eye now landing on the primary?"), so this is the correct rung. Total screenshots for the whole rescue: 2 (one diagnostic in step 3, one verification here).

When I look at the verification screenshot I run the four-question self-critique gate from iteration-patterns.md:

1. Could a non-designer recognise the brand/industry? (Was it generic before? Still generic? Iteration 2 should commit harder.)
2. Where does the eye go first? Squint test — does the primary CTA / heading survive? If something decorative still wins, demote it further.
3. Anything decorative-only without meaning? Each surviving border, badge, shadow tier — does it carry information? If not, cut.
4. What single change would make it less AI-generated? If the answer is obvious (a typeface swap, a custom illustration, an asymmetric layout), name it for the user as a follow-up — but don't ship it without their consent on this rescue. The user asked for "less busy", not "more opinionated".

## Step 7 — Report back, honour the three-iteration limit

If the verification screenshot looks calm and the eye lands on the primary, I report what I cut in one paragraph and stop. The skill's verification cadence rule is explicit: don't keep polishing past the user's stated requirements.

If the user pushes back ("still busy"), iteration 2 picks a *different* lever — not a smaller version of iteration 1. Iteration 3 picks a third. After three iterations the skill says to stop and surface the open-ended-request question:

> *"I've tried three directions and we're not landing. Could you point me at a reference image, name a brand whose feel we're after, or describe the atmosphere in three words?"*

Iterating with shrinking adjustments past three is the explicit anti-pattern in iteration-patterns.md.

## What I will NOT do

- Add anything to "balance out" the busy areas. Subtraction only.
- Touch `set_variables` or `replace_all_matching_properties` on global tokens. Token clobber is failure mode #7 in SKILL.md; the rescue is local to the busy frame, not project-wide.
- Screenshot before/after every micro-change. Two screenshots total: one for diagnosis, one for verification.
- Move the design between section regions of the canvas. Iterations live in the existing frame's region; if the user wants to keep the original for comparison, I'd duplicate to the Exploration region first and rescue the copy. I'd ask before doing that.
- Rewrite copy unless the user asks. "Busy" means visual; microcopy is a separate diagnosis.
- Change typefaces if there are only two in play. "Remove a typeface" only fires when there are three or more.

## Summary

The rescue is mostly listening before cutting. Once I can see the design (`get_editor_state` → `batch_get` → one scoped `get_screenshot`), the diagnosis vocabulary from iteration-patterns.md tells me which of six specific things to subtract. I state the cut list to the user before any `batch_design`, execute it in one or two op chunks, verify structurally first and visually once, and stop. Three iterations max before I stop iterating and ask for a reference.

Output file written to: `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-16-iteration-rescue-too-busy/with_skill/outputs/response.md`.
