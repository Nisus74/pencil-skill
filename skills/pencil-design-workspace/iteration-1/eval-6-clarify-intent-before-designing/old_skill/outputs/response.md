# Designing in Pencil — let's get oriented before I start drawing

Happy to help. Before I open the editor and start putting frames down, your prompt is intentionally broad ("design something for our app"), and the Pencil skill's workflow really wants a couple of facts pinned down so the first `batch_design` call lands in the right place. Rather than guess, here's what I'm doing and what I need from you.

---

## What I've already done (or would do, on a real run)

### 1. Pinged the host

First reflex on any Pencil task is to confirm the MCP server can reach the editor — without a host, every tool fails with `transport not connected to app: desktop`.

```
get_editor_state({ include_schema: false })
```

**Expected response shape:** a JSON object describing the active document (id, file path, schema version), the current selection (node ids, if any), and the imports declared on the document root.

**What I'd check:**
- Did the call succeed? If it errored with a transport message, I'd stop here and tell you to open the Pencil desktop app or the IDE extension before we go further (Failure mode #1 in the skill).
- Is a `.pen` file open? If yes, what's its path and is anything selected? If no, that's a branch point — I'd need to either open one you specify or call `open_document("new")` (Failure mode #2).

### 2. Located project context

Two parallel checks, both cheap:

- **Filesystem:** does `./design-system/` exist at your repo root? That folder is the source of truth for tokens, components, voice, motion, patterns, and tech stack. I'd use a directory listing (not the MCP) to find it.
- **Library imports:** from the `get_editor_state` result above, I'd note any `.lib.pen` files declared in the document's `imports`. Those hold your reusable components.

**Three states are possible, each with a different next step:**
- `design-system/` exists with the standard files → I'd read `README.md` first, then `design-system.md` and `tokens.md`.
- `design-system/` is missing and this is real project work → I'd offer once to scaffold the 12 core templates (plus optional `mobile.md`, `data-viz.md`, `brand.md`, `imagery.md` based on signals in your repo).
- `design-system/` exists but holds source code (a `.tsx` module, etc.) → I'd ask where to put docs instead rather than overwrite.

### 3. Loaded guidelines and inventoried components

```
get_guidelines()
```

**Expected response shape:** a list of available categories for the open document (e.g. `Web App`, `Mobile App`, `Landing Page`, `Table`, `Tailwind`, `Design System`). I'd call it again with the categories that match your task.

Then the components-first scan — before building anything from primitives, look for what already exists:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

And again with `filePath` set against each `.lib.pen` in the document's `imports`. **What I'd check:** which components exist (Button, Input, Card, etc.), what they're named, and what slots/descendants they expose. If you ask for "a sign-in button" and a `ButtonPrimary` already exists, I instantiate that as a `ref` rather than build a button from a frame plus text.

---

## What I need from you before step 4 (Plan)

The skill's discipline says: state a 2–3 sentence plan to you *before* any `batch_design` call. I can't write that plan without four pieces of information. Quick answers, in any order:

### a. What are you designing?

"Design something" can mean any of:
- A specific screen (e.g. a settings page, a dashboard, an onboarding step, a 404 / error state)
- A specific component (e.g. a card, a notification toast, an empty state, a comment thread)
- A flow that crosses multiple screens (e.g. signup, checkout, a multi-step wizard)
- A page-level template (e.g. a marketing landing page, a pricing page)
- A quick sketch or throwaway mock to explore an idea

If you're not sure yet, give me one or two sentences about what your app *does* and what feature you're working on right now — I can suggest a first surface to design.

### b. Which `.pen` file?

- Is one already open in the Pencil editor? If so, I'll work with that.
- If not — should I open an existing one (give me the path) or create a new one (`open_document("new")`)?
- If this is going into a `.lib.pen` library rather than a regular `.pen`, say so — that changes how I structure the file (every top-level frame is a reusable component candidate, not a screen).

### c. What surface and breakpoint?

The skill targets canonical breakpoints: Mobile 390x844, Tablet 768x1024, Desktop 1440x900. Tell me:
- Web app, native mobile, or marketing site?
- One breakpoint or a per-breakpoint set (sibling frames named `Foo_Desktop`, `Foo_Tablet`, `Foo_Mobile`)?

### d. Atmosphere — one adjective from each axis

Per the skill's aesthetic defaults, before any `batch_design` call I commit to a one-line vibe:
- **Density:** airy / balanced / dense
- **Variance:** symmetric / offset / chaotic
- **Motion:** static / fluid / cinematic

If you don't have a preference, I'll pick based on what the surface implies (dashboards lean dense+symmetric+static; marketing pages lean balanced+offset+fluid) and your `design-system/` if you have one. But if you do have a preference — say a "dense, symmetric, static" Linear-style admin panel vs. an "airy, offset, fluid" consumer app — saying so up front saves a re-do later.

---

## What I won't do

A few things the skill is explicit about, that I want to be upfront on:

- I won't read or write the `.pen` file directly with file tools, even though the format is documented JSON. All reads and writes go through the Pencil MCP so schema validation, live screenshots, and editor sync work correctly.
- I won't silently fall back to the `pencil interactive` CLI if the MCP host isn't reachable — you should see what I'm doing.
- I won't scaffold a `design-system/` folder without asking, and if I ask once and you say no, I won't ask again this session.
- I won't redeclare existing variables. If your document already has tokens, `set_variables` with defaults would silently clobber them, so I always call `get_variables()` first and only set what's missing.
- I won't ship Inter as the UI font, pure `#000000` / `#FFFFFF` for surfaces, neon glow shadows, three-column equal-card grids, or fabricated metrics. Those are AI tells the skill explicitly bans.

---

## Skill references I consulted (and why)

- **`SKILL.md`** — main entry point. Gave me the discipline rules (Naming, Context, Components-first, Themes, Responsive, Accessibility, Design completeness), the default 7-step workflow, the failure mode taxonomy, the verification ladder, and the aesthetic defaults including the "name the atmosphere" requirement.
- **`assets/examples/example-login-screen.md`** — read the first 80 lines to ground my response in a worked example. Confirmed how the workflow plays out end-to-end (host detection → context → guidelines → plan stated to user → open doc if needed → first `batch_design` with library import + component refs → structural verify → screenshot scoped to the smallest meaningful subtree).

I deliberately did *not* preload `references/states.md`, `references/flows.md`, `references/modern-patterns.md`, `references/component-anatomy.md`, or any of the other on-demand references — those are workflow branches that only apply once I know what you're designing. Loading them now would burn context for no benefit. Once you tell me the surface, I'll load whichever fit (e.g. `flows.md` for a multi-step form, `states.md` for an error screen, `mcp-tools.md` if I need a tool I haven't touched recently).

---

**Bottom line:** answer (a) and (b) at minimum, and I'll come back with a concrete plan, open or create the right `.pen`, and start the first `batch_design` call. (c) and (d) are nice-to-have — I'll infer them if you're in a hurry.
