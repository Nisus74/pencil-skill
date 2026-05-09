# Customer portal redesign — file architecture plan

Before I touch the canvas, here's the architecture I want to lock in. A "right from the start" file architecture for a multi-flow product is mostly four decisions: **how many `.pen` files**, **how flows are arranged inside each file**, **where the shared library lives**, and **where the agent-readable docs live**. Get those wrong and the cleanup six weeks in is brutal.

## Skill references I consulted

- **`SKILL.md`** — for the default workflow (steps 1–7), the Discipline rules (naming / themes / responsive / a11y / completeness), the design-system convention, and Failure modes §2 (no `.pen` open) and §3 (no `design-system/` folder).
- **`references/flows.md`** — because this prompt explicitly involves four flows. I needed the modal-vs-page guidance, the back-stack model (different on web vs mobile — relevant for billing and settings sub-screens), and the multi-step wizard anatomy (auth has at least signup → verify → welcome).
- **`assets/examples/example-form-flow.md`** — the worked walkthrough for sibling-frame flow layout (`find_empty_space_on_canvas`, side-by-side frames, per-step naming convention `Auth_Step1_Email`).
- **`references/mcp-tools.md`** — for `open_document({ path: "new" })` semantics, the `get_guidelines` category list (I want `Web App` + `Design System` for a customer portal), and the `get_variables` rule (call before any token work, even on a brand-new doc — paranoia is cheap).
- **`assets/examples/example-scaffold-system.md`** — for the `design-system/` scaffold offer wording and the conditional Tier 2 logic (this is a customer portal, so `mobile.md` is plausible, `data-viz.md` likely if billing has charts, `brand.md` probably no, `imagery.md` no).

I did **not** load `references/states.md`, `accessibility.md`, `modern-patterns.md`, `pen-schema.md`, or `batch-design-grammar.md` yet — those are step-5 references when I start placing nodes. This prompt is architecture, not nodes.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Expected response shape: `{ activeDocument: <path-or-null>, selection: [...], schemaVersion?: ... }`. What I check: did it succeed at all (no `transport not connected to app: desktop` error), is there already a `.pen` open that the user might mean instead of "new", and what schema version the host runs.

If it errors → stop and tell the user to open the Pencil desktop app or the IDE extension. Do not improvise.

## Step 2 — Locate context

Two questions answered without MCP calls:

1. **Project filesystem.** `ls` the repo root. Looking for: existing `design-system/` folder, existing `.pen` files anywhere in the tree (especially `.lib.pen`), `package.json` to read the tech stack and detect mobile signals (`react-native`, `expo`), and any `marketing/` / `landing/` directories.
2. **Existing `.pen` files.** If the repo already has `.pen` files for this product, I want to see their layout before adding more — co-location convention may already be set.

Likely outcomes for a "set up a new .pen for our customer portal redesign" prompt:

- No `.pen` files yet → greenfield, my call on architecture.
- A `design-system/` folder may or may not exist → if missing, scaffold offer (see step 3 below).
- Tech stack visible from `package.json` → informs `design-system.md` defaults later.

---

## The architecture decision (this is the actual answer to your prompt)

### Recommendation: **one `.pen` per flow, plus one `.lib.pen`**

```
design/
  portal.lib.pen           ← shared components, tokens, theme axes
  auth.pen                 ← sign in, sign up, verify, forgot password, reset
  dashboard.pen            ← landing dashboard, widgets, primary nav
  billing.pen              ← plans, invoices, payment methods, receipts
  settings.pen             ← profile, security, notifications, team
design-system/
  README.md
  design-system.md         ← points at design/portal.lib.pen
  tokens.md
  components.md
  ...
```

**Why one file per flow, not one big `portal.pen`:**

- Pencil files are JSON and Git-friendly, but a single file holding 40+ screens makes review diffs unreadable. PRs touching just billing shouldn't show diffs against auth.
- The MCP `batch_get` and `snapshot_layout` calls scope cheaper when the document is bounded to one flow's surface area.
- Different teammates can own different flows without merge conflicts on the same JSON.
- The `imports` field in each flow file points at `portal.lib.pen` — components and tokens stay singular and consistent across all four flows.

**Why not one `.pen` per screen:**

- Sibling top-level frames inside one `.pen` are exactly how Pencil expects you to model a multi-screen flow (see `flows.md` worked example: signup uses three sibling frames in one file). Splitting per screen loses the "you can scrub left-to-right and see the flow" affordance, and balloons file count.

**Why a `.lib.pen` from day one:**

- The skill's "Components first" rule (Discipline rules) is impossible to honour without a library — you can't instantiate what doesn't exist. Four flows guarantee shared atoms (Button, Input, Card, Badge, Avatar, Modal, Tabs, Toast). Build them once in `portal.lib.pen`, import into all four flow files via `U("doc", { imports: { "ds": "./portal.lib.pen" } })`.
- Once a `.pen` is marked as a library it can't be unmarked — so I want this decision made deliberately at start, not reverse-engineered later.

### Inside each flow file: sibling top-level frames

Each `.pen` lays out its screens as siblings on the canvas, named by step or screen role:

```
auth.pen
├── Auth_SignIn_Desktop
├── Auth_SignUp_Step1_Email_Desktop
├── Auth_SignUp_Step2_Verify_Desktop
├── Auth_SignUp_Step3_Welcome_Desktop
├── Auth_ForgotPassword_Desktop
└── Auth_ResetPassword_Desktop

dashboard.pen
├── Dashboard_Default_Desktop
├── Dashboard_Empty_Desktop
└── Dashboard_Loading_Desktop

billing.pen
├── Billing_Plans_Desktop
├── Billing_Invoices_Desktop
├── Billing_PaymentMethod_Desktop
├── Billing_PaymentMethod_Edit_Desktop      ← modal-shaped, but a sibling frame so it's diffable
└── Billing_Receipt_Desktop

settings.pen
├── Settings_Profile_Desktop
├── Settings_Profile_Edit_Desktop           ← per flows.md worked example
├── Settings_Security_Desktop
├── Settings_Notifications_Desktop
└── Settings_Team_Desktop
```

**Naming convention** (per the SKILL.md Naming Discipline rule):

- `<Flow>_<Screen>_<Step?>_<Breakpoint>` — PascalCase, semantic, role-bearing.
- Suffix the breakpoint when there's more than one (`_Desktop`, `_Tablet`, `_Mobile`). For app surfaces with predictable scaling, you may use a single fluid frame instead — see Responsive defaults in SKILL.md. My recommendation for a customer portal: per-breakpoint frames for marketing-shaped screens (auth landing pages), single fluid frames for app surfaces (dashboard, settings). Pick one rule per flow file and stay consistent.

**Why sibling frames over separate documents per screen:**

- `find_empty_space_on_canvas` lets me lay them out side-by-side as a visual flow strip. The reviewer scrubs the canvas left-to-right and sees the user's journey.
- Per `flows.md`, multi-step transitions (`SignUp_Step1` → `SignUp_Step2`) are designed to be read as adjacent siblings, not separate files.
- Modal-on-edit screens (e.g. `Settings_Profile_Edit`) are still sibling frames — modals on the canvas are just frames sized like the modal would render. Easier to diff than overlay states stuffed into the parent screen.

---

## Step 3 — Scaffold offer (Failure modes §3)

If `design-system/` doesn't exist (very likely on a new portal redesign), I'll offer once before opening any `.pen`:

> *"This repo doesn't have a `design-system/` folder yet. I have 11 core templates I can drop in — they teach me your tokens, components, voice, motion, patterns, and tech stack so designs stay consistent across all four flows. I can also include 4 optional templates if they fit: `mobile.md` (native-mobile patterns), `data-viz.md` (charts — likely useful for billing usage graphs?), `brand.md` (logo / brand identity), `imagery.md` (photo / illustration treatment). For a customer portal I'd suggest core + `data-viz.md`. Want me to scaffold?"*

I'll signal-detect from `package.json` etc. as the example walkthrough describes, but customer-portal billing usually has at least invoice tables and possibly a usage chart, so I'd lean toward including `data-viz.md`.

## Step 4 — Plan stated to user (the part you'd see before any writes)

> *"Architecture: four flow files (`auth.pen`, `dashboard.pen`, `billing.pen`, `settings.pen`) plus one shared `portal.lib.pen` library, all under `design/`. Each flow file holds its screens as sibling top-level frames named `<Flow>_<Screen>_<Breakpoint>`. The library declares the `mode` theme axis (light + dark) and a baseline component set: Button, Input, Card, Badge, Avatar, Modal, Tabs, Toast, plus tokens for surface, primary, border, text, success, warning, danger, plus spacing and radius scales. I'll build the library first (so the flows have something to import), then create the four flow files with the library imported and one starter screen each so you can see the architecture work end-to-end. Sound right?"*

## Step 4.5 — Bootstrap order

I'd execute in this order, deliberately:

### A. Create the library

```
open_document({ path: "./design/portal.lib.pen" })
```

Then before any token work:

```
get_variables()
```

Expected: empty for a brand-new file. If non-empty (someone pre-seeded it), I respect what's there per the SKILL.md "Token clobber" failure mode.

Then declare the theme axis and bootstrap variables:

```
batch_design ops:
  U("doc", { themes: { mode: ["light", "dark"] } })
```

Followed by `set_variables({ variables: {...}, replace: false })` with the baseline token set — only the variables that didn't come back from `get_variables()`. Each colour gets both light and dark values per the Themes Discipline rule. No raw `#000000` or `#FFFFFF`; `surface` resolves to off-white / Zinc-950.

Then build the components themselves with `batch_design`. Each component gets `reusable: true`, a meaningful PascalCase `name`, and a `context` string explaining its role. Aim ≤25 ops per call; one component per call is usually right when the component has slots and states.

### B. Create the four flow files

For each: `open_document({ path: "./design/<flow>.pen" })`, then immediately:

```
batch_design ops:
  U("doc", { themes: { mode: ["light", "dark"] } })
  U("doc", { imports: { "ds": "./portal.lib.pen" } })
```

Then one starter screen per flow as a sibling frame, sized to desktop (1440×900) per the Responsive defaults table. For positioning, `find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })` so subsequent siblings tile cleanly to the right.

The starter screens, picked because each one anchors that flow's anatomy:

- `auth.pen` → `Auth_SignIn_Desktop` (the simplest of the auth screens, sets the auth-card lockup the rest will share).
- `dashboard.pen` → `Dashboard_Default_Desktop` (establishes the app shell — top nav, side nav, content area — that other dashboard variants will inherit).
- `billing.pen` → `Billing_Plans_Desktop` (the plan-comparison layout is the load-bearing one; invoices/receipts are lighter variants).
- `settings.pen` → `Settings_Profile_Desktop` (per the `flows.md` worked example § settings → edit-profile → save, this is the canonical entry).

### C. Document the architecture in `design-system/design-system.md`

After scaffolding, I'd update the placeholder line in `design-system.md` to point at the library and list the flow files:

```
Library: design/portal.lib.pen
Flows:
  - design/auth.pen
  - design/dashboard.pen
  - design/billing.pen
  - design/settings.pen
```

Future agents (and you, six months on) read this file first and immediately know the file layout.

---

## Step 6 — How I'd verify

For each `.pen` after creation, walking the verification ladder, cheapest rung first:

1. **`batch_design` response** — confirms ops succeeded.
2. **`snapshot_layout({ parentId: <starter screen id>, maxDepth: 2 })`** — confirms the starter frame is at the right size, has the right padding, children are positioned as expected.
3. **`batch_get({ nodeIds: [<doc>] })`** — confirms `imports` includes `portal.lib.pen` and `themes.mode = ["light","dark"]`.
4. **`get_screenshot({ nodeId: <starter screen id> })`** — only on the library file (to confirm components render) and once on the most representative starter (probably `Dashboard_Default_Desktop`) for final sign-off. Five screenshots total across five files would be over-budget; one or two suffices because the architecture is the deliverable, not pixel rhythm.

---

## Things I'd ask you before executing

Three architecture questions where I'd rather get your call than guess:

1. **Path for the design files.** I assumed `design/` at repo root. If you already have a convention (`pencil/`, `figma/`, `docs/design/`), say so — I'll match it.
2. **Library name.** `portal.lib.pen` reads natural for a customer portal. If your org standard is `system.lib.pen`, `<company>.lib.pen`, or matches a npm package name, say so.
3. **Breakpoint coverage.** Customer portal typically means: desktop primary, tablet useful, mobile sometimes. Confirm — *desktop only*, *desktop + mobile*, or *all three*. This determines whether each screen ships as one frame or three siblings, and that's an architecture-shaped choice, not a styling one.

If you say "you decide", my defaults are: `design/` at repo root, `portal.lib.pen` for the library, desktop primary with mobile siblings for surfaces customers will hit on phones (auth definitely, dashboard / billing usually, settings often).

---

## Summary

- **Four `.pen` flow files + one `.lib.pen`** under `design/`, all theme-aware via a shared `mode` axis declared in the library.
- **Sibling top-level frames per screen** inside each flow file, named `<Flow>_<Screen>_<Breakpoint>`, laid out left-to-right via `find_empty_space_on_canvas` so the canvas reads as a flow strip.
- **`design-system/` folder scaffolded first** if missing — 11 core templates plus `data-viz.md` for billing.
- **Library built before the flows**, with tokens bootstrapped after `get_variables()` (never blind).
- **Each flow file imports `portal.lib.pen` immediately on creation** so every node from op zero is built from real components, not primitives that will drift.

Confirm the three open questions above and I'll start with the library bootstrap.

---

*Output written to: `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-18-file-architecture-cover-and-sections/old_skill/outputs/response.md`*
