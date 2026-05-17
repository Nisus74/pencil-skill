# Response: "Set up a pencil design system in this project"

## What I'd do

### Step 1: Ping the Pencil MCP host

Before touching the filesystem, I ping the host:

```
get_editor_state({ include_schema: false })
```

This task is about scaffolding a `design-system/` folder — a filesystem operation — so even if the MCP server isn't reachable, I can still proceed with the file writes. But I check first because:

1. If a `.pen` file is open, I note its path so I can reference it correctly in `design-system/design-system.md`.
2. If the MCP errors, I tell the user and proceed anyway with the scaffolding, since this task doesn't require MCP writes.

If the MCP is connected and a `.pen` is open (say, `./design/app.pen`), I'll fill in the `.lib.pen` path placeholder in `design-system.md` with the real or likely path (e.g. `./design/system.lib.pen`). If nothing is open, I leave the placeholder and note it.

---

### Step 2: Check what's in the repo

I scan the project root for signals before writing anything:

- Is there already a `design-system/` folder? (The user says no — confirmed.)
- Is there a `design-system/` folder that contains code files (`.tsx`, `package.json`, etc.)? No — so no conflict risk.
- Are there mobile signals? (`react-native`, `expo`, `flutter` in `package.json`; `Podfile`; `*.xcodeproj`; iOS/Android directories.)
- Are there marketing surface signals? (`marketing/`, `www/`, `landing/` directories; `next.config.js` with public routes.)
- Is there content-heavy imagery? (Only relevant if brand.md is included.)

Without knowing the specifics of this repo, I'd inspect `package.json` and the root directory listing before deciding on optional files. I'd tell the user what I found.

---

### Step 3: Offer — exactly once

I present the scaffold offer as the skill specifies:

> "This repo doesn't have a `design-system/` folder yet. I have 12 core templates I can drop in — they teach me your tokens, components, voice, motion, patterns, and tech stack so I produce consistent output each session. I can also include optional templates for:
>
> - **`mobile.md`** — native-mobile patterns (tab bar, sheets, safe areas, gestures, haptics)
> - **`data-viz.md`** — chart palettes, default chart types, dashboard tile shape
> - **`brand.md`** — logo lockups, OG/social imagery, brand identity rules
> - **`imagery.md`** — photo/illustration style, AI-imagery treatment, avatar fallbacks
>
> Want me to scaffold the 12 core files now? And do any of the optional ones apply to your project?"

I wait for the user's answer before writing anything.

---

### Step 4: Write the files (assuming user says yes to core, let's say also opts into `mobile.md`)

I copy the 12 core templates from the skill's bundled assets (`assets/design-system/`) into `./design-system/` in the user's project:

**Core files written (always):**

1. `design-system/README.md` — entry point; how agents load these files
2. `design-system/design-system.md` — `.lib.pen` path, tech stack, icon library, brand quick-reference
3. `design-system/tokens.md` — color, spacing, and type tokens; which to use when
4. `design-system/components.md` — catalog of components; when to pick which one
5. `design-system/layout.md` — spacing rhythm, grid, auto-layout rules
6. `design-system/motion.md` — durations, easings, what to animate (and what not to)
7. `design-system/elevation.md` — shadow scale, dark-mode treatment, border/glow fallbacks
8. `design-system/iconography.md` — stroke weight, sizes per context, icon-only vs paired
9. `design-system/patterns.md` — page-level templates (marketing, settings, dashboard, list/detail, auth)
10. `design-system/states.md` — per-component state coverage and fault-state matrix
11. `design-system/voice.md` — microcopy tone, error/empty-state templates
12. `design-system/code-export.md` — how Pencil concepts map to the chosen code stack

**Optional files written (conditional):**

13. `design-system/mobile.md` — included if user opted in, or if the project has React Native / Expo / Flutter / iOS / Android signals
14. `design-system/data-viz.md` — included only on explicit opt-in (no reliable repo signal for charts)
15. `design-system/brand.md` — included if user opted in or if marketing surface signals are present
16. `design-system/imagery.md` — included if user opted in, or if `brand.md` is being included (they pair)

If I'm uncertain about an optional file, I **include it** with a note at the top: *"Delete this file if your project doesn't ship [mobile/charts/brand/imagery] surfaces."* A user can delete a file in two seconds; discovering they needed it later is harder.

---

### Step 5: Fill in what I know

The templates arrive with placeholder values (e.g. `[YOUR_LIBRARY_PATH]`, `[YOUR_FONT]`, `[YOUR_ICON_LIBRARY]`). I fill in whatever the repo tells me:

- **Tech stack** — from `package.json` (React, Next.js, Tailwind, etc.)
- **`.lib.pen` path** — from the currently open document's `imports`, or a sensible default (`./design/system.lib.pen`) if nothing is open
- **Icon library** — from `package.json` (`lucide-react` → Lucide, `@phosphor-icons/react` → Phosphor, etc.)
- **Font** — from `tailwind.config.js` or CSS custom properties if readable; otherwise I leave the placeholder

I do not invent values I can't ground in the repo. Placeholders are fine — they signal to the human what still needs filling.

---

### Step 6: Report back

After writing, I give a one-paragraph summary:

> "Scaffolded `design-system/` with 13 files: the 12 core templates plus `mobile.md` (included because I found React Native in your `package.json`). I pre-filled the tech stack (`Next.js + Tailwind`), icon library (`Lucide`), and left the `.lib.pen` path as a placeholder — fill that in once you've created or located your design library file. Each file has a short description at the top explaining when agents load it. Start by editing `tokens.md` (colors and spacing) and `design-system.md` (the `.lib.pen` pointer) — those two unlock consistent output across every future design session."

---

### What I would NOT do

- I would not create the folder silently without asking — the offer is part of the workflow.
- I would not ask twice in the same session if the user declines.
- I would not overwrite a `design-system/` folder that contains `.tsx` or `package.json` files — I'd ask for an alternate path instead.
- I would not scaffold `data-viz.md` without an explicit opt-in — there's no reliable repo signal for "this project has charts."
- I would not invent a `.lib.pen` path; I'd leave the placeholder and tell the user to fill it in.
- I would not start a `batch_design` call as part of this task — scaffolding the `design-system/` folder is a filesystem operation, not a Pencil canvas operation.
