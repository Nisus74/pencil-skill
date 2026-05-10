# Design System: <Project name>

> Replace the angle-bracketed placeholders with your project's real values, then keep this file short. Each section is a decision, not a tutorial.

## Library file

- **Path:** `<path/to/library.lib.pen>`
- **Imported in `.pen` files as:** `imports: { "ds": "<path/to/library.lib.pen>" }`
- **Status:** `<draft | stable>`, when stable, the agent should always reach for an existing component before inventing one.

If you don't have a `.lib.pen` yet: leave the path as-is and tell the agent so on first use. The skill can help you create one.

## Tech stack

Where designs are implemented in code. The agent uses this to know what idioms to use when generating code from a `.pen`.

- **Framework:** `<React | Vue | SwiftUI | Flutter | Solid | Other>`
- **Component library:** `<shadcn/ui | MUI | Radix | custom | none>`
- **Styling:** `<Tailwind | CSS Modules | styled-components | vanilla-extract | other>`
- **Build target:** `<web | iOS | Android | Electron | mobile-web>`

## Icon library

Pencil's `icon_font` node renders icons from one of these sources. Pick one and stick to it.

- **Source:** `<Lucide | Material Symbols | Phosphor | Feather | custom set>`
- **Pencil node type:** `icon_font` (always, don't import individual SVGs unless naming a custom asset)

## Brand quick-reference

The two or three things the agent should never get wrong:

- **Primary color:** `$primary`, `<#hex or short description>`
- **Surface (default background):** `$surface`, `<#hex>`
- **Body font:** `$fontBody`, `<font name>`
- **Heading font:** `$fontHeading`, `<font name, or "same as body">`
- **Default corner radius:** `<8 | 12 | 16>` px

## Chosen archetype

If your project has committed to a shipped archetype from the pencil-design skill, name it here so the agent loads the right archetype file before any work. Examples:

- **Archetype:** `saas-apps/b2b/modern-pro-tool` (Linear-style refined-dense)
- **Archetype:** `saas-apps/b2b/analytics-dashboard` (data-led overview)
- **Archetype:** `marketing-websites/conversion-focused-saas` (monumental confident marketing)

If unsure, leave this blank, the agent will pick the closest archetype based on the brief, name it out loud, and let you correct course. See `assets/archetypes/README.md` in the skill for the full index.

## Project constraints

A few absolute rules. If something belongs here, the agent should refuse to violate it.

- **Colors:** all colors come from variables. No raw `#hex` in any new design.
- **Spacing:** all spacing comes from `$space-N`. No raw px values for margins/gaps.
- **Components:** new reusable patterns belong in the `.lib.pen`, not as one-offs in screen files.
- **Add your own:** `<e.g. "no gradients on text", "buttons must always have a visible focus state">`

## Theme axes

If you support light/dark or other themes:

- **`mode`:** `["light", "dark"]`, default `"light"`
- **`<other axis>`:** `<values>`

If you don't, delete this section.

## Code-side library locations

Where generated components land in the code repo:

- **Components:** `<src/components/>`
- **Tokens (CSS vars):** `<src/styles/tokens.css>` or `<tailwind.config.ts>`
- **Icons:** imported per-component from the icon library above

This lets the agent know where to write code that pairs with a `.pen` design.
