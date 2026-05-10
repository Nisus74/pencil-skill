# Code export

How designs in `.pen` files map to code in this project. The agent reads this when translating a Pencil design into source files (or when writing new code that should match an existing design).

## Stack reminders

(These mirror `design-system.md`, kept here for self-contained reading when the agent only loads this file.)

- **Framework:** `<React | Vue | SwiftUI | Flutter | Other>`
- **Styling:** `<Tailwind | CSS Modules | styled-components | other>`
- **Component library:** `<shadcn/ui | MUI | custom | none>`

## Pencil → code mapping

| Pencil concept | Code translation |
|----------------|------------------|
| `frame` with `layout: "vertical"` | A flex column container. (`<div className="flex flex-col gap-4">` in Tailwind, `VStack` in SwiftUI, `Column` in Flutter.) |
| `frame` with `layout: "horizontal"` | A flex row container. |
| `frame` with `layout: "none"` | An absolutely-positioned container, but check first; absolute layout in code is usually a sign the design should have used auto-layout. |
| `text` with `$textBase` | A semantic element appropriate to context (`<p>`, `<span>`, `<label>`, `<h2>`). The variable picks size; the surrounding role picks the tag. |
| `icon_font` | Import from the configured icon library, e.g. `import { LogIn } from 'lucide-react'`. |
| `ref` to a `reusable` component | An import of the matching code-side component, e.g. `<Button variant="primary">`. The component's name matches the library's `id`. |
| Variables (`$primary`, `$space-4`) | CSS custom properties (`var(--primary)`) or theme tokens (`theme.colors.primary`). |
| Theme axes (`mode: "dark"`) | Whatever theming the framework uses (`data-theme="dark"`, `useColorScheme()`, etc.). |

## Component file location

When generating a new component file from a design, use:

- **Path:** `<src/components/{ComponentName}.tsx>` (or framework equivalent)
- **One component per file.** Don't bundle multiple unrelated components.
- **Co-locate styles** if the framework uses them (CSS Modules: `{ComponentName}.module.css` in the same dir).
- **Tests** at `<src/components/{ComponentName}.test.tsx>`.

## Round-tripping

When a design changes:

1. **Re-export the affected component** from the updated `.pen`. Don't hand-edit the generated file in lockstep.
2. **Preserve hand-written extensions** (event handlers, business logic, props the design doesn't know about). The export should regenerate structure and styles, not the logic.
3. **Diff before committing.** If the regenerated code drifts wildly from the previous version, double-check that the design change was intentional.

## What not to generate from a design

The agent should *not* invent these from a `.pen`:

- API calls / data fetching logic (the design only shows shape).
- Form validation rules beyond what's visually implied (a "required" asterisk, an inline error treatment).
- Routing.
- Authentication state.

These belong in code that *uses* the generated component, not in the component itself.

## When the design and code disagree

The design is the source of truth for **structure, spacing, type, color, and component composition**. The code is the source of truth for **behavior, state, and integration**. When they conflict on visual style, change the design first; on behavior, the design defers.
