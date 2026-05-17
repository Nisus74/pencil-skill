# Design System

This folder is read by AI coding tools (Claude Code, Codex, Gemini CLI, Copilot CLI, Cursor, and any other agent that supports the [agentskills.io](https://agentskills.io) standard) when working on this project's UI — whether designing in pencil.dev or writing the code that ships from those designs.

## How agents use it

When you ask an agent to design or build something, it loads files in this order:

1. **`README.md` (this file)** — to find the entry points
2. **`design-system.md`** — to find the `.lib.pen` library and tech stack
3. **The other files only when the task needs them** — e.g. `tokens.md` when picking a color, `components.md` when choosing what to instantiate, `voice.md` when writing copy

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
| `elevation.md` | Choosing shadows / depth — cards, modals, popovers, dropdowns. |
| `iconography.md` | Picking an icon size, deciding icon-only vs paired-with-label, applying icon color. |
| `patterns.md` | Laying out a whole page — marketing landing, settings, dashboard shell, list+detail, auth, onboarding. |
| `states.md` | Deciding which states a component needs (hover, focus, error, loading, skeleton…) or which fault states a page needs (404, 500, offline, empty). |
| `voice.md` | Writing user-facing copy — labels, error messages, empty states, CTAs. |
| `code-export.md` | Translating a design into code (React component, SwiftUI view, etc.). |

### Optional (present only if your project ships these surfaces)

| File | Read when… | Delete if… |
|------|-----------|-----------|
| `mobile.md` | Designing native-mobile patterns (tab bar, sheets, safe areas, gestures, haptics). | Your project is desktop-only. |
| `data-viz.md` | Designing a chart, sparkline, or dashboard tile. | Your project doesn't render charts. |
| `brand.md` | Placing a logo, designing OG/social-share imagery, applying brand identity. | Your project has no marketing surface and no distinct brand mark. |
| `imagery.md` | Choosing photo style, illustration style, AI-imagery treatment, avatar fallbacks. | Your project is mostly chrome and data. |
| `visual-style.md` | Locking in a specific aesthetic direction — style family, palette recipe, type pairing. | No fixed visual style has been chosen. |
| `micro-interactions.md` | Specifying per-interaction animation values beyond the motion.md defaults. | You have no detailed animation requirements. |
| `empty-states.md` | Designing the lockup and copy for empty lists, dashboards, and post-action states. | The defaults from `states.md` are sufficient. |
| `onboarding.md` | Designing a sign-up or guided first-use flow. | Your product has no onboarding sequence. |
| `navigation.md` | Specifying sidebar, top bar, breadcrumb, or mobile nav patterns. | Your navigation is simple and needs no formal spec. |
| `search.md` | Designing instant search, submit-driven search, suggestions, and empty-results states. | Your product has no search feature. |
| `forms.md` | Specifying validation timing, error display, save patterns, and multi-step behaviour. | You have no forms, or the defaults are fine. |
| `accessibility.md` | Setting compliance targets, keyboard nav requirements, and screen-reader patterns. | No accessibility targets have been set yet. |
| `file-architecture.md` | Organising multiple `.pen` files — naming, section regions, status taxonomy. | Your project has only one design file. |

## Editing this folder

Everything here is plain Markdown. Edit any file by hand — agents re-read on each task.

**Not a developer or designer?** See [CUSTOMISING.md](./CUSTOMISING.md) for a plain-English walkthrough that explains each file and where to start.

Two principles for keeping it useful:

1. **Decisions, not exhaustive documentation.** "Use `$primary` for any interactive accent color" is more useful than "We have these 47 colors." The agent can look up colors; it can't easily learn taste.
2. **Short and decision-shaped.** Most files top out at ~500 words. If a file grows past that, split it or trim ruthlessly. Long files get skipped or skimmed.

## Where this came from

This folder was scaffolded by the [pencil-design skill](https://github.com/Nisus74/pencil-skill). You can keep, edit, rename, or remove any of these files — none of them are required for the skill to work, but they make the agent's output dramatically more consistent.

## Not using pencil.dev?

That's fine — this folder is tool-agnostic markdown. A frontend coding agent benefits just as much from `tokens.md` and `components.md` as a design agent does. Keep the folder; ignore the `.lib.pen` references in `design-system.md`.
