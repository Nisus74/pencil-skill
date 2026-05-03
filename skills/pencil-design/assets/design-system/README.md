# Design System

This folder is read by AI coding tools (Claude Code, Codex, Gemini CLI, Copilot CLI, Cursor, and any other agent that supports the [agentskills.io](https://agentskills.io) standard) when working on this project's UI — whether designing in pencil.dev or writing the code that ships from those designs.

## How agents use it

When you ask an agent to design or build something, it loads files in this order:

1. **`README.md` (this file)** — to find the entry points
2. **`design-system.md`** — to find the `.lib.pen` library and tech stack
3. **The other files only when the task needs them** — e.g. `tokens.md` when picking a color, `components.md` when choosing what to instantiate, `voice.md` when writing copy

This progressive loading keeps the agent's context small while still giving it the right information at the right time.

## Files

| File | Read when… |
|------|-----------|
| `design-system.md` | Always (after this file). Pointer to the `.lib.pen`, tech stack, icon library, brand quick-reference. |
| `tokens.md` | Picking a color, a spacing value, a font size, or any token-driven property. |
| `components.md` | Deciding which component to use for a job (Button vs IconButton, Card vs Modal, etc.). |
| `layout.md` | Setting auto-layout, choosing sizing behavior (`fill_container` vs `fit_content`), or laying out a page grid. |
| `voice.md` | Writing user-facing copy — labels, error messages, empty states, CTAs. |
| `code-export.md` | Translating a design into code (React component, SwiftUI view, etc.). |

## Editing this folder

Everything here is plain Markdown. Edit any file by hand — agents re-read on each task. Two principles for keeping it useful:

1. **Decisions, not exhaustive documentation.** "Use `$primary` for any interactive accent color" is more useful than "We have these 47 colors." The agent can look up colors; it can't easily learn taste.
2. **Short and decision-shaped.** Most files top out at ~500 words. If a file grows past that, split it or trim ruthlessly. Long files get skipped or skimmed.

## Where this came from

This folder was scaffolded by the [pencil-design skill](https://github.com/Nisus74/pencil-skill). You can keep, edit, rename, or remove any of these files — none of them are required for the skill to work, but they make the agent's output dramatically more consistent.

## Not using pencil.dev?

That's fine — this folder is tool-agnostic markdown. A frontend coding agent benefits just as much from `tokens.md` and `components.md` as a design agent does. Keep the folder; ignore the `.lib.pen` references in `design-system.md`.
