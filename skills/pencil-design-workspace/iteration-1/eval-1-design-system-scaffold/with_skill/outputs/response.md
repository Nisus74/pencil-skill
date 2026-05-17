# Setting up your Pencil design system

Happy to scaffold this. Before I drop files in, I want to confirm a couple of things and offer a choice on the optional templates.

## What I'm consulting

I read `pencil-design/SKILL.md` end-to-end (it points at the design-system convention, the scaffold offer text, and Failure mode #3 for "no `design-system/` folder"). I also loaded `assets/examples/example-scaffold-system.md` — that's the worked walkthrough for exactly this task. I'm following that script rather than improvising.

## Step 1 — Detect host (precondition, not strictly required for scaffolding)

Scaffolding is filesystem-only — it doesn't touch the Pencil MCP server. So I won't ping `get_editor_state` here. (If the next thing you ask me to do is "now design something in pencil," that's where I'd start the workflow with `get_editor_state({ include_schema: false })` to confirm the host is reachable. A `transport not connected to app: desktop` error there means the desktop app or IDE extension isn't running, and per Failure mode #1 I'd stop and tell you rather than silently fall back to the CLI.)

## Step 2 — Check what exists

I'll list the project root to confirm three things, per the skill's three-state detection logic:

- **No `design-system/` folder already exists** — proceed with the scaffold.
- **`design-system/` exists with markdown files** — already scaffolded; I'd just read it, not re-scaffold.
- **`design-system/` exists with code** (`.tsx`, `.ts`, `package.json`, `index.js`) — name collision; I would not overwrite. I'd ask where to put the docs instead (`design-system/docs/`, `docs/design-system/`, `.pencil/design-system/`, or a custom path).

I'll also scan for project signals that decide which optional templates apply: `package.json` (looking for `react-native`, `expo`, `flutter`), `pubspec.yaml`, `ios/`, `android/`, `Podfile`, `*.xcodeproj`, and any `marketing/`, `www/`, or `landing/` directories.

Tools: a directory listing (Bash `ls -la`) at the project root, and a `Read` on `package.json` if it exists. Given you've told me there's no `design-system/` folder, I expect the listing to confirm that — but I'll still run it. Assumptions about repo contents are exactly the kind of thing that should be checked, not guessed.

## Step 3 — Pick the optional templates

The 11 core templates are non-negotiable: the skill copies them every time. The 4 optional templates are decided by signals or by your call. Default heuristic:

- `mobile.md` — include if any mobile signal is present (RN, Expo, Flutter, an iOS or Android folder, a `Podfile`, a `*.xcodeproj`, or a stated mobile build target). Otherwise skip.
- `data-viz.md` — no reliable signal from a fresh repo. Skip by default unless you tell me the product has charts.
- `brand.md` — include if there's a marketing/landing surface (`marketing/`, `www/`, `landing/` directories, or routes named `landing`, `home`, `pricing`, `about`).
- `imagery.md` — include if `brand.md` is being included (they pair) or if the project is content-heavy.

When in doubt I prefer to **include**. Each optional template has a "Delete this file if your project doesn't…" header at the top — a deletion takes 2 seconds; reconstructing a file you didn't know existed is harder.

I'll tell you which optional files I included and why, so you can delete any that don't fit.

## Step 4 — Copy the templates

Templates ship with this skill at `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design/assets/design-system/`.

**Core (always copy, 11 files):**

| Source | Destination |
|--------|-------------|
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

**Optional (include based on signals or your call, 4 files):**

| Source | Destination | Include if |
|--------|-------------|------------|
| `assets/design-system/mobile.md` | `design-system/mobile.md` | Repo shows RN/Expo/Flutter, iOS/Android folder, `Podfile`, or `*.xcodeproj` |
| `assets/design-system/data-viz.md` | `design-system/data-viz.md` | Product has charts (you opt in) |
| `assets/design-system/brand.md` | `design-system/brand.md` | Project ships a marketing surface |
| `assets/design-system/imagery.md` | `design-system/imagery.md` | `brand.md` included or content-heavy product |

Mechanically: `mkdir -p design-system` then `cp` each source file in. I'd avoid templating contents on first scaffold — the templates have sensible defaults and you'll get more out of editing them in place than out of me guessing your tokens, stack, or voice upfront.

What I'd verify after the copy: a quick `ls design-system/` to confirm the right number of files landed, and a head of `design-system/README.md` to confirm it copied intact (defending against partial writes or wrong-source paths).

## Step 5 — What to edit first

Once the files are in place, I'll tell you (per the skill's standard handover script):

> *"Scaffolded `design-system/` with 11 core templates [+ N optional: list them]. The two you'll want to edit first are:*
> - *`design-system.md` — replace the `<path/to/library.lib.pen>` placeholder with your actual library path, and confirm the tech stack and icon-library sections.*
> - *`tokens.md` — review the colour/spacing/type variables; rename or replace the placeholders with your real token names."*
>
> *"The others have sensible defaults you can leave for now. Edit them as you go — they're plain markdown, designed to be human-edited. If any of the optional files don't apply to your project, delete them; each one has a 'Delete this file if…' header at the top."*

The folder is named `design-system/` (not `pencil/`) deliberately. The contents are tool-agnostic markdown so frontend coding agents — not just the Pencil skill — can read them too.

## What happens next time

Every future Pencil task in this repo will, at step 3 of the workflow:

1. Read `design-system/README.md` first.
2. Branch into `design-system.md` and `tokens.md` for the specifics it needs.
3. Inventory components in the open `.pen` and any imported `.lib.pen` (per the Components-first rule) before drawing anything from primitives.
4. Use those guidelines to keep tokens, components, voice, and stack consistent across sessions and across tools (Claude Code, Codex, Cursor, Gemini CLI all read this same folder).

If the next thing is *"now build a login screen"* or similar, I'd start with `get_editor_state({ include_schema: false })` to confirm the Pencil desktop app (or IDE extension) is running, then `get_guidelines()` to see which categories the document declares, then proceed through plan → `batch_design` → verify (structural-first via `snapshot_layout` and `batch_get`, screenshot only when the question is genuinely visual).

## Edge case I'm watching for

If step 2's listing turns up a `design-system/` containing code, I will not overwrite it. I'll ask where to put the docs instead. The README's relative cross-refs to its sibling files (`tokens.md`, `components.md`, etc.) work in any sibling location, so the templates port cleanly to any nested or hidden path you choose.

---

Want me to go ahead with the core 11, plus optional files based on whatever signals the repo shows? Or would you like to pick the optional set explicitly (any of `mobile.md`, `data-viz.md`, `brand.md`, `imagery.md`)? If you're not sure, I'll just check the repo and decide — you can delete anything that doesn't fit.
