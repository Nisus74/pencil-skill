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

> *"This repo doesn't have a `design-system/` folder yet. I have seven template files I can drop in — they teach me your tokens, components, voice, and tech stack so designs stay consistent across sessions. Want me to scaffold them at `design-system/`?"*

On yes, continue. On no, drop it; don't ask again this session.

## Step 3 — Copy the templates

The seven templates ship with this skill at `assets/design-system/`. Copy each into the user's project:

| Source (this skill) | Destination (user project) |
|---------------------|----------------------------|
| `assets/design-system/README.md` | `design-system/README.md` |
| `assets/design-system/design-system.md` | `design-system/design-system.md` |
| `assets/design-system/tokens.md` | `design-system/tokens.md` |
| `assets/design-system/components.md` | `design-system/components.md` |
| `assets/design-system/layout.md` | `design-system/layout.md` |
| `assets/design-system/voice.md` | `design-system/voice.md` |
| `assets/design-system/code-export.md` | `design-system/code-export.md` |

Use platform-appropriate file ops (Bash `cp`, the `Write` tool reading from skill assets, etc.). The skill assets path is resolvable via the platform's skill-directory variable (e.g. `${CLAUDE_SKILL_DIR}` in Claude Code).

## Step 4 — Tell the user what's there and what to fill in

> *"Scaffolded `design-system/` with seven templates. The two you'll want to edit first are:*
> - *`design-system.md` — replace the `<path/to/library.lib.pen>` placeholder with your actual library path, and confirm the tech stack section.*
> - *`tokens.md` — review the color/spacing/type variables; rename or replace the placeholders with your real token names."*
>
> *"The others (`components.md`, `layout.md`, `voice.md`, `code-export.md`) have sensible defaults you can leave for now. Edit them as you go — they're plain markdown, designed to be human-edited."*

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
