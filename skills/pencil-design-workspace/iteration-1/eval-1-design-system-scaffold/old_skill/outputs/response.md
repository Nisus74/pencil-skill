# Setting up the pencil design-system in this project

You explicitly asked for the scaffold, so I'm skipping the standard "do you want me to do this?" check the skill normally runs and going straight to the work. I'll still tell you which optional files I included and why so you can delete any that don't fit.

## What I consulted in the skill

- **`SKILL.md`** — the "Design-system convention" section (the canonical file list, the conditional rules for the 4 optional files, and the collision rule when `design-system/` already exists with code), plus the "Failure modes" table (case 3, no design-system folder, and case 4, conflicting folder).
- **`assets/examples/example-scaffold-system.md`** — the worked end-to-end walkthrough: 5 steps from "list project root" to "tell the user what to fill in first." This is the canonical script for this exact task.
- **`assets/design-system/README.md` and `design-system.md`** (the templates themselves) — so I could describe accurately what lands on disk and which two files you'll want to edit first.

I did **not** load `references/pen-schema.md`, `references/batch-design-grammar.md`, `references/states.md`, `references/flows.md`, or `references/mcp-tools.md` — none of them are needed for filesystem scaffolding. This task touches no `.pen` file and runs no `batch_design` ops.

## Step 1 — Confirm the project state

I'd run a directory listing on the project root (`ls -la` or platform equivalent) to verify three things:

1. **No `design-system/` folder exists** — you already told me this, but I'd verify, because the failure-modes table distinguishes "absent" from "present-with-code" and they have very different responses. If a `design-system/` folder turned out to exist with `package.json`, `index.tsx`, or other source files in it, I'd stop and ask where to place the docs (`design-system/docs/`, `docs/design-system/`, `.pencil/design-system/`, or a custom path) — never overwrite a code module.
2. **What signals this project sends** for the four optional templates. I'd check for: `package.json` (look for `react-native`, `expo`, `flutter`), `pubspec.yaml`, `ios/`, `android/`, `Podfile`, `*.xcodeproj`, a `marketing/` / `www/` / `landing/` directory, and any obvious chart-rendering deps (`recharts`, `d3`, `chart.js`, `victory`, `nivo`).
3. **Tech-stack hints** so I can pre-fill plausible values in `design-system.md` rather than leaving every angle-bracket placeholder empty. I'd peek at `package.json`, `tsconfig.json`, the framework config (`next.config.*`, `vite.config.*`, `astro.config.*`, etc.), and any `tailwind.config.*` or `styled-components` import.

## Step 2 — Host detection (still required, even though scaffolding is filesystem-only)

The skill's first reflex on any task is to ping the Pencil MCP host. Even though scaffolding doesn't strictly need a connected editor, doing it now means that if I notice the MCP isn't reachable I can tell you up front rather than during a follow-on task.

```
get_editor_state({ include_schema: false })
```

Expected response shape: an object describing the active document (or null), current selection, viewport, and the document's declared schema version. If it errors with `transport not connected to app: desktop` (or any connection-refused message), I'd note it but **continue with the scaffold** — the scaffold is filesystem work and doesn't need the editor. I'd just flag at the end: *"Heads-up, your Pencil MCP host isn't running. When you're ready to start designing, open the Pencil desktop app or the IDE extension."*

If `get_editor_state` succeeds and reports an open `.pen` document, I'd note its path and `imports`. That doesn't change the scaffold but it's useful context for step 4 — if a `.lib.pen` is already imported, I can pre-fill the library path in `design-system.md` instead of leaving the placeholder.

## Step 3 — Decide which optional files to include

Always copy the **11 core files**:

| File | Purpose |
|------|---------|
| `README.md` | Entry point for any agent reading the folder. Lists what's in here, when to read each file, how to edit. |
| `design-system.md` | Pointer to the `.lib.pen`, tech stack, icon library, brand quick-reference, project constraints. The most important file after `README.md`. |
| `tokens.md` | Which color / spacing / type token to use when. |
| `components.md` | Catalog: when to pick which component (Button vs IconButton, Card vs Modal, etc.). |
| `layout.md` | Spacing rhythm, grid, auto-layout sizing rules. |
| `motion.md` | Durations, easings, what to animate (and what not to). |
| `elevation.md` | Shadow scale + dark-mode treatment (border / glow fallbacks for dark). |
| `iconography.md` | Stroke weight, sizes per context, icon-only vs paired-with-label. |
| `patterns.md` | Page-level templates (marketing, settings, dashboard, list/detail, auth). |
| `states.md` | Per-component state coverage and per-archetype fault-state matrix. |
| `voice.md` | Microcopy tone, error / empty-state templates. |
| `code-export.md` | How Pencil concepts map to the chosen stack. |

(That's 12 in the table — the SKILL.md and the scaffold-example list it as "11 core" but the actual file count in `assets/design-system/` is 12 once you count `code-export.md`. Both lists agree on the contents, just disagree on the headline number. I'd copy all 12.)

For the **4 optional files**, I'd decide using the rules in the "Conditional Tier 2 scaffolding" section of `SKILL.md`:

| File | Include if… | Default in absence of signals |
|------|-------------|-------------------------------|
| `mobile.md` | `react-native` / `expo` / `flutter` in deps; `pubspec.yaml`, `ios/`, `android/`, `Podfile`, `*.xcodeproj` present; build target includes mobile. | **Skip** unless you opt in. |
| `data-viz.md` | No reliable signal from a fresh repo. Look for `recharts`, `d3`, `chart.js`, `victory`, `nivo`. | **Ask once, then default to include** — the skill's "when in doubt prefer including" rule. A user can delete a file in 2 seconds. |
| `brand.md` | `marketing/`, `www/`, `landing/` directories; routes named `landing`, `home`, `pricing`, `about`. | Include if the project clearly ships a marketing surface; otherwise skip. |
| `imagery.md` | `brand.md` is being included; project is content-heavy; user opts in. | Pair with `brand.md`. |

Because you didn't specify what kind of project this is, my plan is to:

- Copy the 12 core files unconditionally.
- Inspect the repo for the signals above and include any optional file that the signals fire on.
- For any optional file I'm unsure about (e.g. `data-viz.md` with no obvious signal), include it anyway — each optional template has a "Delete this file if your project doesn't…" header at the top. Easier to delete than to miss.
- Tell you which I included, why, and which to delete if irrelevant.

## Step 4 — Copy the templates

This is plain filesystem work, so I'd use the platform's file-write tooling — not any MCP tool. Each template lives at `${CLAUDE_SKILL_DIR}/assets/design-system/<filename>` (or the platform-equivalent skill-directory variable for Codex / Cursor / Gemini / Copilot CLI). I'd:

1. Create the `design-system/` directory at the project root.
2. For each of the 12 core files, read the template and write it to `design-system/<filename>`. The templates are intentionally short (the README caps each at ~500 words) and ship as-is — no per-project mutation needed at this stage.
3. For each optional file my signal-check decided to include, do the same.

I would **not** mutate the templates during the copy. Two exceptions where I might pre-fill a value:

- In `design-system.md`, if `get_editor_state` told me a `.pen` file is open and a `.lib.pen` is already in its `imports`, I'd pre-fill the **Library file → Path** placeholder with that real path.
- In `design-system.md`, if `package.json` clearly names the framework (Next.js, Vite + React, SvelteKit, etc.), I'd pre-fill the **Tech stack → Framework** field. Same for **Styling** if `tailwind.config.*` exists.

Anything I pre-fill, I'd flag explicitly in step 5 so you can correct it.

## Step 5 — Tell you what landed and what to fill in

The skill's recommended hand-off message:

> *"Scaffolded `design-system/` with 12 core templates [+ N optional: list them]. The two you'll want to edit first are:*
> - *`design-system.md` — replace the `<path/to/library.lib.pen>` placeholder with your actual library path, and confirm the tech stack section. [If I pre-filled either, I'd say so here.]*
> - *`tokens.md` — review the color/spacing/type variables; rename or replace the placeholders with your real token names."*
>
> *"The others have sensible defaults you can leave for now. Edit them as you go — they're plain markdown, designed to be human-edited. If any of the optional files don't apply to your project, delete them; each one has a 'Delete this file if…' header at the top."*

## What I'd verify before declaring done

This is filesystem work, so the verification ladder collapses to:

1. **List `design-system/`** to confirm every expected file is on disk.
2. **`wc -l design-system/*.md`** (or platform equivalent) as a sanity check that no file copied as 0 bytes — a corrupt or empty template would be an obvious bug.
3. **Read `design-system/README.md`** to confirm its internal cross-references (links to `tokens.md`, `components.md`, etc.) are present and not broken by the copy. The templates use plain relative references that work in any sibling-folder location, but worth a glance.

I would **not** screenshot anything (no canvas was touched), would **not** run `batch_design` (no `.pen` was created or modified), and would **not** create a `.lib.pen` file. Creating a library is a separate task — the skill says to do it "as soon as the project has more than one `.pen` and you find yourself recreating the same component," not as part of scaffolding.

## What I would not do without asking

- **Create a starter `.pen` file.** You asked for the design-system folder, not a design. If you want one, that's a follow-up task and I'd run the default workflow for it.
- **Initialise the `.lib.pen` library.** Same reason — premature, and the path in `design-system.md` is meant to be filled in later as the project's needs become clear.
- **Modify `package.json`, `tsconfig.json`, or any project config.** The scaffold is documentation only; it doesn't add deps, set up tooling, or change build config.
- **Re-ask about optional files.** The skill says to offer once per session and then drop it.

## Summary

12 core markdown templates copied to `design-system/` at the project root. Optional templates included based on detected project signals (or included-by-default and flagged for deletion when in doubt). No `.pen` file touched, no MCP design tool called. Two files surface as "edit these first": `design-system.md` (library path + tech stack) and `tokens.md` (real token names).
