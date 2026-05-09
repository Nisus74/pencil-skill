# Getting started on a Pencil design

Happy to help, but "design something for our app" is open-ended enough that if I just start placing frames I'll likely build the wrong thing. Before I plan anything, I want to do two cheap checks against the editor and the repo, then ask you three quick questions.

## Step 1 — host detection (first call I always make)

I'll ping the Pencil MCP host before doing anything else:

- **Tool:** `get_editor_state`
- **Args:** `{ include_schema: false }`
- **What I'm checking:** does the call succeed at all (i.e. is a Pencil host actually running — desktop app, IDE extension, or `pencil interactive`), and if so, which `.pen` file is open and what's selected?
- **What I'd do with the response shape:**
  - If it errors with anything like `transport not connected to app: desktop`: I stop and tell you to open the Pencil desktop app or the Pencil IDE extension. I will not silently fall back to the CLI; that's a deliberate policy in the skill so you always see what I'm doing.
  - If it succeeds with no active document: I'll ask whether to open an existing `.pen` (give me the path) or create one with `open_document({ path: "new" })`.
  - If it succeeds with a document open: I note the path, the schema version it declares, and what node is currently selected — selection often tells me what part of the design you're focused on.

## Step 2 — locate context (project filesystem, not MCP)

While I'm at it, I'll look at the project root for a `design-system/` folder using a plain directory listing (filesystem, not MCP — the skill is explicit about this):

- **Looking for:** `./design-system/README.md` plus the 11 other core docs (`design-system.md`, `tokens.md`, `components.md`, `layout.md`, `motion.md`, `elevation.md`, `iconography.md`, `patterns.md`, `states.md`, `voice.md`, `code-export.md`).
- **Three branches:**
  - **Folder exists and has those files:** I'll read `README.md` first, then `design-system.md` and `tokens.md`. Those answer most of the "what does this product look like" questions for me, and I won't need to ask you about palette, fonts, or stack.
  - **Folder exists but contains code (e.g. `.tsx`, `package.json`):** I won't overwrite. I'll ask you where to put the docs instead (`design-system/docs/`, `docs/design-system/`, `.pencil/design-system/`, or a custom path).
  - **Folder absent:** if this is real project work (not a one-off sketch), I'll offer once to scaffold it. The skill ships 12 core templates plus 4 optional ones (`mobile.md`, `data-viz.md`, `brand.md`, `imagery.md`) that get included based on signals like a `react-native`/`expo` dependency, a `marketing/` directory, or your stated build target. I won't ask twice in the same session.

I'll also check the open document (if any) for an `imports` field that points at a `.lib.pen` library — if your project already has one, I want to instantiate components from it via `ref` nodes rather than hand-build buttons and inputs from primitives.

## Step 3 — three questions for you (because the prompt is open-ended)

The skill is explicit on this case: when a request has no reference image, no description of who uses it, and no `design-system/` to follow, I ask three quick questions before planning. Skipping this is how I end up shipping a generic "balanced / symmetric / fluid" design that could belong to any product.

So — three quick ones:

1. **Who uses this and what problem does it solve?** A name for the surface helps too: settings page, onboarding flow, dashboard home, pricing page, error screen, signup form, mobile compose sheet, etc. The archetype shapes which `get_guidelines` category I load (`Web App`, `Mobile App`, `Landing Page`, `Table`) and which reference file I pull (`forms.md`, `flows.md`, `layout-patterns.md`, `mobile-patterns.md`).
2. **Atmosphere — any words, references, brand direction, or competitor sites you'd point at?** Even one adjective per axis is enough: density (airy / balanced / dense), variance (symmetric / offset / chaotic), motion (static / fluid / cinematic). If you have a reference image or a screenshot of a product whose voice you like, drop it in.
3. **Hard constraints?** Things like: tech stack (React + Tailwind, SwiftUI, Flutter), responsive targets (mobile-first, desktop-only, all three breakpoints), dark-mode-only or light + dark, accessibility level (WCAG AA is my default), and whether there's an existing `.lib.pen` I should be importing from.

If any of those have obvious answers from a `design-system/` folder I find in step 2, I'll skip them — your existing docs already speak for you.

## Once you answer

Here's what happens next so you know what you're agreeing to:

1. **Load guidelines + inventory components.** I call `get_guidelines()` once with no args to get the live category list, then load the categories that match the surface (`Web App`, `Landing Page`, `Mobile App`, etc., plus `Tailwind` if your stack matches and `Design System` for component-heavy work). Then I inventory what already exists: `batch_get({ patterns: [{ reusable: true }], readDepth: 2 })` against the open doc, and the same call with `filePath` set against each `.lib.pen` in the document's imports. I want to know which buttons, inputs, cards, and badges already exist before I build anything new.
2. **Plan in 2–3 sentences before any write.** I'll name the top-level frames I'll create, the existing components I'll instantiate (by id), the breakpoint(s) I'm targeting, and the one-line atmosphere ("dense dashboard, symmetric, static" — committed before I draw, so the rest of the design has to honour it). This is the cheapest moment to catch a wrong assumption.
3. **Execute via `batch_design`.** One or more calls, ≤25 ops each, using `foo=I("parent", {...})` bindings so later ops can reference what I just made. Every node gets a meaningful PascalCase `name` (no `Frame 1`, no `Group 2`); every non-trivial node gets a one-sentence `context` that documents intent and behaviour, not visual specs; colours come from variables that have light AND dark values; sizing uses bare-string `"fill_container"` / `"fit_content"` (not `"100%"` and not the older `{ sizing: ... }` object form — the live server rejects both).
4. **Verify structurally first, screenshot last.** I walk the verification ladder and stop at the cheapest rung that answers the question: (a) `batch_design` response, (b) `snapshot_layout(parentId, maxDepth: 2)` for positions / sizes / gaps, (c) `batch_get({ nodeIds: [...] })` for property-level confirmation (variable bindings, text, refs), (d) `get_screenshot(nodeId)` only when the question is genuinely visual or as final sign-off — and always scoped to the smallest meaningful subtree, never the whole canvas. A typical end-to-end design needs one or two screenshots total. The reflex from older versions of this skill ("screenshot after every chunk") burns tokens to confirm things the structural snapshot already proved.
5. **Self-critique gate before declaring done.** Four questions: could a non-designer recognise this as the brand's voice or industry; where does the eye go first / second / third; what's decorative-only that doesn't communicate meaning; what single change would make this feel less AI-generated. Fix what surfaces, don't note it as a TODO.

## What I consulted

- `skills/pencil-design/SKILL.md` — the canonical workflow, the discipline rules, the open-ended-request branch, the failure-modes table, the verification ladder.
- `skills/pencil-design/references/mcp-tools.md` — confirmed the exact `get_editor_state` invocation and the live `get_guidelines` category list.
- I'd load these on demand once you answer the questions: `references/file-architecture.md` (Cover frame + section regions for any new `.pen`), `references/layout-patterns.md` or `references/forms.md` or `references/mobile-patterns.md` depending on the surface, and `references/style-catalogue.md` + `references/colour-palettes.md` + `references/font-pairings.md` if there's no `design-system/` and we're picking direction from scratch.

Tell me about the surface, the vibe, and any constraints — and confirm Pencil is open on your end — and I'll pick it up from there.
