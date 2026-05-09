# Setting up the customer portal redesign `.pen`

A multi-flow customer portal is exactly the kind of project that gets hard to navigate fast if the file architecture is wrong from day one. Auth, dashboard, billing, and settings all have their own happy paths, error states, and breakpoints; without a clear convention you end up with 60+ frames in arbitrary canvas positions and no answer to "which is canonical?". So this is worth getting right upfront.

## References I consulted

Before doing anything I loaded:

- **`pencil-design/SKILL.md`** — for the default workflow, the discipline rules (especially § File architecture, § Naming, § Themes), and the failure-mode table.
- **`references/file-architecture.md`** — this is the canonical reference for Cover frames, the section-region layout, hierarchical naming, the single-`.pen` vs multi-`.pen` decision tree, and the SaaS pressure test. SKILL.md § "Design intelligence: when to deviate" tells me to load it whenever organising a `.pen` with many flows.
- **`assets/examples/example-file-cover-and-sections.md`** — the worked example for almost exactly this task (a customer-portal redesign with multi-flow naming).

I did not load `forms.md`, `flows.md`, `states.md`, `data-viz.md`, etc. yet — they'll come in when we actually design specific screens. The current task is structural setup, not screen design.

## Step 1 — Detect host and locate context

```
get_editor_state({ include_schema: false })
```

What I'm looking for in the response:

- That the MCP host is connected (no `transport not connected to app: desktop` error). If it errors, I stop and ask you to open the Pencil desktop app or IDE extension — per Failure mode #1, no silent CLI fallback.
- Whether a `.pen` is already open. For a fresh customer portal redesign, I expect no document, or the wrong one — in which case I'd call `open_document("new")` to create the file (Failure mode #2).
- Whether there's an existing `imports` list — relevant if the project already has a `design-system.lib.pen`.

In parallel I'd check the project filesystem (regular shell, not MCP) for:

- `./design-system/` — does the project have its scaffolded markdown? If yes, I read `README.md` then `design-system.md` (which would name any `.lib.pen` to import) and `tokens.md`.
- Existing `.pen` and `.lib.pen` files in the repo so I know what's already there.

If `design-system/` is missing and you confirm this is real project work (not a sketch), I'd offer the one-time scaffold per Failure mode #3 — 12 core templates plus optional `mobile.md` / `data-viz.md` / `brand.md` / `imagery.md`. I'd ask once and not ask again this session.

## Step 2 — Decide the file set

Per `file-architecture.md` § "Single .pen vs multi-.pen", **start with one `.pen` per project** and split only when a real signal fires. For a four-flow customer portal at the start of work, the right shape is:

```
customer-portal.pen        ← all four flows: auth, dashboard, billing, settings
design-system.lib.pen      ← shared components and variables (create only if it doesn't exist)
```

I would not split per flow yet (one designer, one product, no load-time issue, no concurrent contributors). If down the track billing grows its own engineering team or the dashboard becomes a separate tech surface, we split then. Premature splitting creates overhead with zero payoff.

I'd surface this decision to you explicitly before creating anything: *"Going with one `customer-portal.pen` plus a shared `design-system.lib.pen` library. Push back if you want them split per flow from day one."*

## Step 3 — Create the file and the Cover frame

Assuming the doc doesn't exist, I'd call:

```
open_document("new", { fileName: "customer-portal.pen" })
```

Expected response: a `documentId` and a root canvas node id. From there, the very first thing on the canvas is the **Cover frame** at origin `(0, 0)` — per the SKILL.md discipline rule and `file-architecture.md` § "The Cover frame".

Before any token work I'd call `get_variables()` (per the Themes rule, never clobber existing variables). For a brand new doc this returns empty, so I bootstrap themes and the minimal token set:

```
U("doc", { themes: { mode: ["light", "dark"] } })
set_variables({ variables: {
  surface:        { type: "color", value: [{ value: "#FAFAFA", theme: { mode: "light" } }, { value: "#0B1117", theme: { mode: "dark" } }] },
  surfaceMuted:   { type: "color", value: [...] },
  textPrimary:    { type: "color", value: [...] },
  textSecondary:  { type: "color", value: [...] },
  border:         { type: "color", value: [...] },
  // accent set deferred until we know the brand direction
  fontDisplay:    { type: "font", value: "Geist" },
  fontBody:       { type: "font", value: "Geist" },
  fontMono:       { type: "font", value: "Geist Mono" },
  fontWeightBold: { type: "number", value: 700 },
  fontWeightSemiBold: { type: "number", value: 600 },
}, replace: false })
```

If `design-system/tokens.md` exists, those values come from there instead of the defaults; I would not invent token values when the project has them.

Then the Cover, in one `batch_design` call (≤25 ops, well under):

```
cover = I("<canvas-root-id>", {
  type: "frame",
  name: "Cover",
  context: "File operating manual: owner, status, version, scope, links. Read first to determine if this file is safe to build from and what's in or out of scope.",
  position: { x: 0, y: 0 },
  size: { width: 800, height: 600 },
  fill: "$surface",
  layout: { direction: "column", padding: 48, gap: 24 },
})
I(cover, { type: "text", name: "FileTitle",   text: "Customer portal redesign", fontFamily: "$fontDisplay", fontSize: 48, fontWeight: "$fontWeightBold", color: "$textPrimary" })
meta = I(cover, { type: "frame", name: "Meta", layout: { direction: "row", gap: 32 } })
I(meta, { type: "frame", name: "MetaItem_Owner",   children: [
  { type: "text", name: "OwnerLabel",   text: "Owner",          color: "$textSecondary" },
  { type: "text", name: "OwnerValue",   text: "<your name>",    color: "$textPrimary"   },
]})
I(meta, { type: "frame", name: "MetaItem_Status", children: [
  { type: "text", text: "Status", color: "$textSecondary" },
  { type: "text", text: "Discovery", color: "$textPrimary" },   // file just started; will move to "In design" then "Design review" then "Ready for build"
]})
I(meta, { type: "frame", name: "MetaItem_Version", children: [
  { type: "text", text: "Version", color: "$textSecondary" },
  { type: "text", text: "0.1",     color: "$textPrimary"  },
]})
I(meta, { type: "frame", name: "MetaItem_Updated", children: [
  { type: "text", text: "Last updated", color: "$textSecondary" },
  { type: "text", text: "2026-05-09",   color: "$textPrimary"  },
]})
I(cover, { type: "frame", name: "Scope",  children: [
  { type: "text", text: "In scope", color: "$textSecondary" },
  { type: "text", text: "Customer-facing portal: auth (sign in / sign up / password reset / MFA), dashboard, billing (plan selection / payment / invoice history), settings (profile / notifications / security / team).", color: "$textPrimary" },
  { type: "text", text: "Out of scope", color: "$textSecondary" },
  { type: "text", text: "Internal admin console (separate file), enterprise SSO admin config (separate file), marketing pages.", color: "$textPrimary" },
]})
I(cover, { type: "frame", name: "Links", children: [
  { type: "text", text: "Links", color: "$textSecondary" },
  { type: "text", text: "Brief: <link>. Linear: <link>. Prototype: <link>. Design system: ./design-system.lib.pen.", color: "$textPrimary" },
]})
```

The exact field set comes from `file-architecture.md` § Cover frame: Owner, Status, Version, Last updated, Scope (in), Scope (out), Links. Status starts at `Discovery` (just kicked off) and will progress through the taxonomy as work matures. Width capped at 800px so the whole Cover reads at a glance. Note the explicit two-column out-of-scope list — calling out admin console and SSO upfront prevents scope creep into this `.pen`.

**Verification (cheap rungs).** The `batch_design` response confirms ops succeeded (rung 1). I'd then `snapshot_layout(cover, maxDepth: 2)` to confirm the column layout, padding, and gap landed correctly (rung 2). No screenshot needed yet — the Cover is structural text, the variable system handles theming.

## Step 4 — Lay down section region anchors

Per `file-architecture.md` § "Section frames as canvas regions", top-level frames live in named regions. The agent and the next teammate identify which region a frame is in by its canvas position plus a visible header. I'd place anchor headers (large text nodes, not containing frames) at the top of each region. Layout going down the canvas:

| Region | Position | Why here |
|---|---|---|
| Cover | (0, 0) | Anchor; always at origin |
| Source of Truth | (0, 760) | Right below Cover; primary read order |
| Build Ready | (0, 2800) | Below SourceOfTruth, room for several rows |
| UX States | (0, 4800) | Below BuildReady |
| Responsive | (0, 6800) | Below UX States; may also extend right |
| Exploration | (8000, 0) | Far right, deliberately separated |
| Archive | (0, 10000) | Bottom; inactive |

Vertical gaps are generous (1500–2000px) so each region fits a few rows of full-width desktop frames (1440px) without bleeding into the next region. Horizontal placement of Exploration far right is deliberate — physical distance reinforces "this is not canonical".

In one `batch_design` call:

```
I("<canvas-root-id>", { type: "text", name: "_RegionHeader_SourceOfTruth", text: "── SOURCE OF TRUTH ──", position: { x: 0,    y: 720  }, fontSize: 32, fontFamily: "$fontDisplay", color: "$textSecondary" })
I("<canvas-root-id>", { type: "text", name: "_RegionHeader_BuildReady",    text: "── BUILD READY ──",    position: { x: 0,    y: 2760 }, fontSize: 32, fontFamily: "$fontDisplay", color: "$textSecondary" })
I("<canvas-root-id>", { type: "text", name: "_RegionHeader_UXStates",      text: "── UX STATES ──",      position: { x: 0,    y: 4760 }, fontSize: 32, fontFamily: "$fontDisplay", color: "$textSecondary" })
I("<canvas-root-id>", { type: "text", name: "_RegionHeader_Responsive",    text: "── RESPONSIVE ──",     position: { x: 0,    y: 6760 }, fontSize: 32, fontFamily: "$fontDisplay", color: "$textSecondary" })
I("<canvas-root-id>", { type: "text", name: "_RegionHeader_Exploration",   text: "── EXPLORATION ──",    position: { x: 8000, y: 0    }, fontSize: 32, fontFamily: "$fontDisplay", color: "$textSecondary" })
I("<canvas-root-id>", { type: "text", name: "_RegionHeader_Archive",       text: "── ARCHIVE ──",        position: { x: 0,    y: 9960 }, fontSize: 32, fontFamily: "$fontDisplay", color: "$textSecondary" })
```

The `_` prefix on names marks these as scaffolding rather than design content (common file-system convention; survives layer-list scanning). Their `context` (which I'd set on each) reads something like *"Visual region anchor; not a design artifact. Build Ready is current iteration in flight."*

I'd call `find_empty_space_on_canvas` before any future top-level frame placement so we don't accidentally overlap regions as the file grows. For this initial setup the canvas is empty so positions are deterministic; it's worth using it for every subsequent frame.

## Step 5 — Plan the hierarchical naming convention for the four flows

Per `file-architecture.md` § "Hierarchical naming for multi-screen flows", the path is:

```
[Area] / [Flow] / [Step] / [Screen] / [State] / [Breakpoint]
```

For your four flows, the plan I'd commit before designing any screens:

**Auth (multi-step flows).** Hierarchical naming applies; numbered steps because flows cross several screens.

```
Auth / SignIn / 01 / EmailEntry / Default / Desktop
Auth / SignIn / 01 / EmailEntry / ValidationError / Desktop
Auth / SignIn / 02 / Password / Default / Desktop
Auth / SignUp / 01 / AccountDetails / Default / Desktop
Auth / SignUp / 02 / EmailVerify / Sent / Desktop
Auth / SignUp / 02 / EmailVerify / VerifyExpired / Desktop
Auth / SignUp / 03 / Welcome / Default / Desktop
Auth / PasswordReset / 01 / RequestEmail / Default / Desktop
Auth / PasswordReset / 02 / EmailSent / Default / Desktop
Auth / PasswordReset / 03 / SetNewPassword / Default / Desktop
Auth / MFA / 01 / Setup / Default / Desktop
Auth / MFA / 02 / VerifyCode / Default / Desktop
```

**Dashboard (mostly single-surface).** Hierarchical naming still applies — even a single-screen surface benefits from the Area prefix when one `.pen` covers four flows.

```
Dashboard / Home / Default / Desktop
Dashboard / Home / Empty / Desktop          ← first-use empty state
Dashboard / Home / Loading / Desktop
Dashboard / Home / Error / Desktop          ← partial-data fault state
```

**Billing (multi-step purchase flow plus standalone screens).**

```
Billing / Overview / Default / Desktop
Billing / ChangePlan / 01 / SelectPlan / Default / Desktop
Billing / ChangePlan / 02 / EnterPayment / Default / Desktop
Billing / ChangePlan / 03 / Confirm / Default / Desktop
Billing / ChangePlan / 03 / Confirm / ValidationError / Desktop
Billing / Invoices / Default / Desktop
Billing / Invoices / Empty / Desktop
Billing / PaymentMethods / Default / Desktop
```

**Settings (sectioned settings page; the `Step` slot collapses to the section name).**

```
Settings / Profile / Default / Desktop
Settings / Notifications / Default / Desktop
Settings / Security / Default / Desktop
Settings / Security / TwoFactorEnabled / Desktop
Settings / Team / Default / Desktop
Settings / Team / Empty / Desktop           ← no teammates yet
Settings / Team / InviteMember / Default / Desktop
```

Rules I'm enforcing:

- Step numbers are zero-padded to two digits (`01`, `02`) — alphabetical sort matches step order.
- States come from `references/states.md` vocabulary: `Default`, `Empty`, `Loading`, `Error`, `ValidationError`, `Sent`, `VerifyExpired`, `Success`, etc. I'd load `states.md` when actually designing the state variants; for now I'm just naming consistently.
- Breakpoint suffix on every frame. Even desktop-only screens get `/ Desktop` so when we add Mobile and Tablet variants they slot in cleanly.
- Slashes go in `name`, never in `id`. The schema rejects slashes in ids.

I would not create empty placeholder frames for this whole list now — that's overengineering. The naming convention is the commitment; frames get created when we actually design them.

## Step 6 — Initial frames placed in BuildReady

Since you're at the very start, no frame should land in Source of Truth yet (per the workflow: SoT is for approved designs only). The first design lands in **Build Ready**. I'd suggest creating one anchor frame per flow as a starting point so the file structure is concrete rather than abstract:

```
find_empty_space_on_canvas({ width: 1440, height: 900, preferRegion: { x: 0, y: 2820, w: 8000, h: 1800 } })
```

then a `batch_design` placing four sibling frames in Build Ready at row positions:

```
auth      = I("<canvas-root-id>", { type: "frame", name: "Auth / SignIn / 01 / EmailEntry / Default / Desktop", position: { x: 0,    y: 2820 }, size: { width: 1440, height: 900 }, fill: "$surface", context: "Sign-in entry: email step. Validates format on blur; submit is disabled until valid. Routes to Auth / SignIn / 02 / Password on submit." })
dash      = I("<canvas-root-id>", { type: "frame", name: "Dashboard / Home / Default / Desktop",                position: { x: 1500, y: 2820 }, size: { width: 1440, height: 900 }, fill: "$surface", context: "Customer dashboard home. Default state assumes user has at least one active subscription and recent activity." })
bill      = I("<canvas-root-id>", { type: "frame", name: "Billing / Overview / Default / Desktop",              position: { x: 3000, y: 2820 }, size: { width: 1440, height: 900 }, fill: "$surface", context: "Billing landing: current plan, next invoice date, payment method summary, link to invoice history." })
sett      = I("<canvas-root-id>", { type: "frame", name: "Settings / Profile / Default / Desktop",              position: { x: 4500, y: 2820 }, size: { width: 1440, height: 900 }, fill: "$surface", context: "Settings landing: profile section. Sidebar nav for Profile / Notifications / Security / Team." })
```

These are empty frames. I would not start populating them until you tell me which to design first. They exist now to (a) prove the file architecture works end-to-end and (b) anchor the naming convention with concrete examples.

## Step 7 — `.lib.pen` import (if applicable)

If `design-system/design-system.md` exists and names a library path:

- If the file at that path exists and isn't already in the doc's `imports`: add it via `U("doc", { imports: { ds: "./design-system.lib.pen" } })`.
- If `design-system.md` names a path but the file doesn't exist: I'd flag the mismatch (Failure mode #5) and ask whether to create the library or update the path.
- If neither exists: I'd flag that the customer portal will eventually want a `.lib.pen` for shared components (especially for auth forms which repeat across SignIn / SignUp / PasswordReset / MFA), and offer to create an empty one with a Cover.

## Step 8 — Verify the architecture landed

Cheap-rung verification first:

1. `snapshot_layout("<canvas-root-id>", maxDepth: 1)` — confirms top-level frames sit in their intended regions and don't overlap. Returns positions and sizes as numbers; faster and cheaper than a screenshot.
2. `batch_get({ nodeIds: ["<cover-id>"], readDepth: 2 })` — confirms Cover children all have content (no empty text nodes) and `context` strings are populated.
3. `get_variables()` — confirms theme tokens registered correctly with both light and dark values.

Only then, **one screenshot at the end** — `get_screenshot("<canvas-root-id>")` — to confirm the regions read intuitively at a glance: Cover top-left, region headers visible, BuildReady frames in row order. This is the rare case where a full-canvas screenshot is justified, because the deliverable here *is* the canvas-level structure. Per the verification cadence rule, that's one screenshot for the entire setup task.

## What I would surface to you afterwards

A one-paragraph summary covering:

- File created at `customer-portal.pen` with status `Discovery`, version `0.1`.
- Cover at origin with all required fields; I've used `<your name>` as a placeholder for owner — please update.
- Section regions set up with visible headers for Source of Truth / Build Ready / UX States / Responsive / Exploration / Archive.
- Hierarchical naming convention committed; first anchor frame per flow placed in Build Ready.
- Theme axis declared with light + dark; minimum token set bootstrapped (or pulled from `tokens.md` if present).
- Whether a `design-system.lib.pen` was imported, exists but wasn't imported, or needs creating.
- Two open questions for you: *(1) Confirm the in/out scope on the Cover before we start designing; (2) Should we set up Mobile and Tablet Responsive frames now, or wait until Desktop is approved per flow?*

That's the structural setup. Actual screen design starts when you point at the first flow.

---

**Note on tools I did not call.** The instructions said not to attempt `mcp__pencil__*` tools in this run, so the calls above are illustrative of what I would issue, with the arguments and expected response shapes. The discipline rules and file-architecture conventions are exactly what I'd apply in a real session — they don't change based on whether the MCP is reachable.
