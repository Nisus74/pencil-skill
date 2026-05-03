# Example: scaffold a `design-system/` folder

User says:

> *"Set up the pencil design system in this project."*

Or, more commonly, on a different task:

> *"Design a dashboard in pencil"* — and you (the agent) notice during step 2 that there's no `design-system/` folder, so you offer.

---

## Step 1 — Check what exists

List the project root. Three possible states:

- **No `design-system/` at all** → proceed to step 2.
- **`design-system/` exists with markdown files** → already scaffolded; just read it. Don't re-scaffold.
- **`design-system/` exists with code** (`.tsx`, `.ts`, `package.json`, etc.) → see "Collision" below.

## Step 2 — Confirm with the user (skip if they explicitly asked)

> *"This repo doesn't have a `design-system/` folder yet. I have 11 core templates I'll drop in — they teach me your tokens, components, voice, motion, patterns, and tech stack so designs stay consistent across sessions. I can also include 4 optional templates if they fit your project: `mobile.md` (native-mobile patterns), `data-viz.md` (charts), `brand.md` (logo / brand identity), `imagery.md` (photo / illustration treatment). Want me to scaffold the core, plus any optional ones that apply?"*

On yes, continue. On no, drop it; don't ask again this session.

If the user just says "yes" without picking optional files, decide based on signals (see Step 3) and tell them which optional files you included and why — they can delete any that don't apply.

## Step 3 — Copy the templates

The templates ship with this skill at `assets/design-system/`. **Always copy the 11 core files:**

| Source (this skill) | Destination (user project) |
|---------------------|----------------------------|
| `assets/design-system/README.md` | `design-system/README.md` |
| `assets/design-system/design-system.md` | `design-system/design-system.md` |
| `assets/design-system/tokens.md` | `design-system/tokens.md` |
| `assets/design-system/components.md` | `design-system/components.md` |
| `assets/design-system/layout.md` | `design-system/layout.md` |
| `assets/design-system/motion.md` | `design-system/motion.md` |
| `assets/design-system/elevation.md` | `design-system/elevation.md` |
| `assets/design-system/iconography.md` | `design-system/iconography.md` |
| `assets/design-system/patterns.md` | `design-system/patterns.md` |
| `assets/design-system/voice.md` | `design-system/voice.md` |
| `assets/design-system/code-export.md` | `design-system/code-export.md` |

**Optional, copy conditionally** — based on user opt-in OR detectable project signals:

| Source | Destination | Include if… |
|--------|-------------|------------|
| `assets/design-system/mobile.md` | `design-system/mobile.md` | User opts in; OR `package.json` has `react-native` / `expo` / `flutter`; OR `pubspec.yaml` exists; OR `ios/` / `android/` / `Podfile` / `*.xcodeproj` present; OR build target includes iOS, Android, or mobile-web. |
| `assets/design-system/data-viz.md` | `design-system/data-viz.md` | User opts in. (No reliable signal from a fresh repo — ask if it's not obvious.) |
| `assets/design-system/brand.md` | `design-system/brand.md` | User opts in; OR project has `marketing/`, `www/`, `landing/` directories; OR routes named `landing`, `home`, `pricing`, `about`. |
| `assets/design-system/imagery.md` | `design-system/imagery.md` | User opts in; OR `brand.md` is being included; OR project is content-heavy. |

When in doubt, **prefer including** an optional file (its top-of-file header says "Delete this file if your project doesn't…"). A user can delete a file in 2 seconds; reconstructing one they didn't know existed is harder.

Use platform-appropriate file ops (Bash `cp`, the `Write` tool reading from skill assets, etc.). The skill assets path is resolvable via the platform's skill-directory variable (e.g. `${CLAUDE_SKILL_DIR}` in Claude Code).

## Step 4 — Tell the user what's there and what to fill in

> *"Scaffolded `design-system/` with 11 core templates [+ N optional: list them]. The two you'll want to edit first are:*
> - *`design-system.md` — replace the `<path/to/library.lib.pen>` placeholder with your actual library path, and confirm the tech stack section.*
> - *`tokens.md` — review the color/spacing/type variables; rename or replace the placeholders with your real token names."*
>
> *"The others have sensible defaults you can leave for now. Edit them as you go — they're plain markdown, designed to be human-edited. If any of the optional files don't apply to your project, delete them; each one has a 'Delete this file if…' header at the top."*

## Step 5 — Continue with the original task (if applicable)

If you only scaffolded because the original task was "design X" and you noticed the missing folder, return to step 3 of the default workflow (load guidelines), now reading the templates you just placed.

---

## Collision: `design-system/` already exists with code

Don't overwrite. Ask:

> *"Your project has a `design-system/` folder, but it looks like a code module (I see `package.json` and `index.tsx`). I don't want to put markdown docs on top of source code. Where would you like the agent-readable docs?"*
>
> *Options:*
> - *`design-system/docs/` — nested inside the existing folder*
> - *`docs/design-system/` — alongside other documentation*
> - *`.pencil/design-system/` — hidden, signals tooling-only*
> - *Tell me a custom path*

Take the answer, scaffold there. **Edit each template's internal references** so they point at the right relative paths if needed (the README's pointer to `tokens.md`, etc., should remain a relative reference and work in any sibling location).
