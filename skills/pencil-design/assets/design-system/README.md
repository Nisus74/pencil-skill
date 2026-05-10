# Design System

This folder is read by AI coding tools (Claude Code, Cursor, Codex, and any other agent that supports the [agentskills.io](https://agentskills.io) standard) when working on this project's UI, whether designing in pencil.dev or writing the code that ships from those designs.

## How agents use it

When you ask an agent to design or build something, it loads files in this order:

1. **`README.md` (this file)**, to find the entry points
2. **`design-system.md`**, to find the `.lib.pen` library and tech stack
3. **The other files only when the task needs them**, e.g. `tokens.md` when picking a color, `components.md` when choosing what to instantiate, `voice.md` when writing copy

This progressive loading keeps the agent's context small while still giving it the right information at the right time.

## Files

### Core (always present)

| File | Read when… |
|------|-----------|
| `design-system.md` | Always (after this file). Pointer to the `.lib.pen`, tech stack, icon library, brand quick-reference. |
| `tokens.md` | Picking a color, a spacing value, a font size, or any token-driven property. |
| `components.md` | Deciding which component to use for a job (Button vs IconButton, Card vs Modal, etc.). |
| `layout.md` | Setting auto-layout, choosing sizing behavior (`fill_container` vs `fit_content`), or laying out a page grid. |
| `motion.md` | Adding any transition, hover effect, modal entrance, or animated state. |
| `elevation.md` | Choosing shadows / depth, cards, modals, popovers, dropdowns. |
| `iconography.md` | Picking an icon size, deciding icon-only vs paired-with-label, applying icon color. |
| `patterns.md` | Laying out a whole page, marketing landing, settings, dashboard shell, list+detail, auth, onboarding. |
| `states.md` | Deciding which states a component needs (hover, focus, error, loading, skeleton…) or which fault states a page needs (404, 500, offline, empty). |
| `voice.md` | Writing user-facing copy, labels, error messages, empty states, CTAs. |
| `code-export.md` | Translating a design into code (React component, SwiftUI view, etc.). |

### Optional (present only if your project ships these surfaces)

| File | Read when… | Delete if… |
|------|-----------|-----------|
| `mobile.md` | Designing native-mobile patterns (tab bar, sheets, safe areas, gestures, haptics). | Your project is desktop-only. |
| `data-viz.md` | Designing a chart, sparkline, or dashboard tile. | Your project doesn't render charts. |
| `brand.md` | Placing a logo, designing OG/social-share imagery, applying brand identity. | Your project has no marketing surface and no distinct brand mark. |
| `imagery.md` | Choosing photo style, illustration style, AI-imagery treatment, avatar fallbacks. | Your project is mostly chrome and data. |

## Editing this folder

Everything here is plain Markdown. Edit any file by hand, agents re-read on each task. Two principles for keeping it useful:

1. **Decisions, not exhaustive documentation.** "Use `$primary` for any interactive accent color" is more useful than "We have these 47 colors." The agent can look up colors; it can't easily learn taste.
2. **Short and decision-shaped.** Most files top out at ~500 words. If a file grows past that, split it or trim ruthlessly. Long files get skipped or skimmed.

## Detecting unfilled templates

When you read files in this folder, check for unfilled placeholder values before using any design-system content. Placeholder values have the form `<placeholder-text>` (angle-bracket delimited). If you find one, stop and tell the user before continuing.

**Common unfilled spots:**

| File | Placeholder | Why it matters |
|------|-------------|----------------|
| `design-system.md` | `<path/to/library.lib.pen>` | The library import path cannot be resolved; all component `ref:` ops will fail silently until this is set. |
| `design-system.md` | `<stack>` or `<framework>` | The agent will not know whether to reference React, Vue, SwiftUI, etc. when suggesting code export. |
| `tokens.md` | `[primary-color]`, `[surface-color]`, etc. | Token names in brackets are templates, not real tokens. Any `fill: "[primary-color]"` op will produce invalid markup. |
| `components.md` | `[ComponentName]` or `<describe>` | The component inventory is incomplete; the agent may build from primitives instead of using a library component that exists. |
| `voice.md` | `[product name]` | Copy generated with literal `[product name]` will appear in the design. |

**Detection rule:** when you read a file from this folder, scan for the pattern `<[^>]+>` or `\[[A-Z][^\]]*\]`. If any match is a template placeholder (not a description in a context that uses brackets intentionally, like code examples), tell the user:

> *"I see unfilled template values in `design-system.md`: the library path is still `<path/to/library.lib.pen>`. I'll need that filled in before I can import your component library. Want to update it now, or should I proceed without the library for this task?"*

Do not silently proceed with placeholder values.

## Working with archetypes

The pencil-design skill ships an opinionated archetype library at `assets/archetypes/<category>/<name>.md` (e.g. `analytics-dashboard`, `modern-pro-tool`, `conversion-focused-saas`). Most files in this design-system folder reference those archetypes in an *Archetype variants* subsection, showing how the same baseline reshapes under different aesthetic directions.

Precedence when the agent is making a decision:

1. The user's direction (a screenshot, a brand name, a description) wins.
2. This `design-system/` folder wins next.
3. The shipped archetype (when no user direction or specific design-system rule covers it).
4. The skill's negative-space defaults.

If your project has committed to a specific archetype, note it in `design-system.md` so the agent loads the right archetype file before any work.

## Where this came from

This folder was scaffolded by the [pencil-design skill](https://github.com/Nisus74/pencil-skill). You can keep, edit, rename, or remove any of these files, none of them are required for the skill to work, but they make the agent's output dramatically more consistent.

## Not using pencil.dev?

That's fine, this folder is tool-agnostic markdown. A frontend coding agent benefits just as much from `tokens.md` and `components.md` as a design agent does. Keep the folder; ignore the `.lib.pen` references in `design-system.md`.
