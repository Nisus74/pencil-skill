Happy to set this up. Before I start writing files, a quick clarification on what "Pencil design system" means here, because Pencil (pencil.dev) is a design tool that stores designs in encrypted `.pen` files — those are not plain-text artifacts you scaffold by hand. So there are really two layers I can put in place for you:

1. A `design-system/` folder containing the `.pen` files that Pencil itself reads/writes (created via the Pencil MCP, not via plain file writes).
2. A code-side scaffold (tokens, components, docs) that mirrors what's in the `.pen` files so engineers have something to import.

Here is what I'd create. Tell me to proceed and I'll do it; I've made reasonable defaults so you can also just say "go."

## Proposed folder layout

```
design-system/
  README.md
  pen/
    foundations.pen        # colors, typography, spacing, radii, shadows
    components.pen         # buttons, inputs, cards, nav, etc.
    patterns.pen           # composed patterns (forms, empty states, headers)
    screens.pen            # example screens that consume the above
  tokens/
    tokens.json            # exported design tokens (Style Dictionary-compatible)
    colors.css             # CSS custom properties
    typography.css
    spacing.css
  components/
    .gitkeep               # populated as components are extracted from Pencil
  docs/
    contributing.md        # how to edit .pen files via Pencil + MCP
    conventions.md         # naming, variants, token usage
```

## What goes in each file

**`design-system/README.md`**
- One-paragraph explanation that the source of truth lives in the `.pen` files under `design-system/pen/`.
- A note that `.pen` files are encrypted and must be opened with Pencil (or read/written via the Pencil MCP `batch_get` / `batch_design` tools — never `cat`/`Read`).
- Quickstart: install Pencil, open `design-system/pen/foundations.pen`, run the token export.

**`design-system/pen/foundations.pen`** (created via Pencil MCP `open_document` + `batch_design`)
- Variables collection: `color/*`, `font/*`, `space/*`, `radius/*`, `shadow/*`.
- A "Foundations" page with swatches and type ramp so designers can see tokens visually.
- Sensible starter values — neutral grayscale (50–950), a primary brand ramp, semantic aliases (`bg.surface`, `text.default`, `text.muted`, `border.subtle`, `accent.default`), an 8pt spacing scale, four radii, three elevations, an Inter-based type ramp (display/h1–h4/body/caption).

**`design-system/pen/components.pen`**
- Component frames bound to the variables above: Button (primary/secondary/ghost x sm/md/lg x default/hover/disabled), Input, Textarea, Checkbox, Radio, Select, Card, Badge, Avatar, Tabs, NavBar, Sidebar item, Toast.
- Each component uses Pencil variants/properties so engineers see the prop API reflected in the design.

**`design-system/pen/patterns.pen`**
- Composed pieces: form layout, list row, empty state, header with breadcrumb, modal shell.

**`design-system/pen/screens.pen`**
- 2–3 example screens (dashboard, settings, sign-in) so the system is exercised end-to-end.

**`design-system/tokens/tokens.json`**
- Mirrors the variables in `foundations.pen`, in W3C-ish design-token shape:
  ```json
  {
    "color": { "brand": { "500": { "$value": "#5B5BD6", "$type": "color" } } },
    "space": { "4": { "$value": "16px", "$type": "dimension" } }
  }
  ```
- This is the file the codebase imports from; it should be regenerated whenever `foundations.pen` changes (I'd suggest a `pnpm tokens:export` script later).

**`design-system/tokens/colors.css` / `typography.css` / `spacing.css`**
- Plain CSS custom properties derived from `tokens.json`, e.g. `--color-brand-500: #5B5BD6;`. Safe to import from any framework.

**`design-system/docs/contributing.md`**
- Rules I'd write in: edit foundations only via the variables panel in Pencil; never hardcode hex values in components; new components must consume existing variables; after changes, re-export tokens and open a PR with both the `.pen` change and the regenerated `tokens.json`.

**`design-system/docs/conventions.md`**
- Naming (`Component/Variant/State`), variant property names (`size`, `tone`, `state`), when to make something a component vs. a pattern, accessibility expectations.

## How I'd actually create the `.pen` files

I would not write `.pen` files with the `Write` tool — they're encrypted. The flow is:
1. `mcp__pencil__open_document` with `"new"` to create each `.pen` file, then save it to the target path.
2. `mcp__pencil__get_guidelines` to load Pencil's authoring guides for variables and components so the structure follows their conventions.
3. `mcp__pencil__batch_design` calls to insert the variables collection, foundation page, and component frames.
4. `mcp__pencil__batch_get` to read back the variable IDs and generate `tokens/tokens.json` and the CSS files from them.

The plain-text files (`README.md`, `tokens.json`, the CSS files, the docs) I'll create directly with `Write`.

## Defaults I'm assuming (say the word to change any)

- Brand color: a neutral indigo (`#5B5BD6`) as a placeholder until you give me a real one.
- Type: Inter, system fallback.
- Spacing scale: 0, 2, 4, 8, 12, 16, 24, 32, 48, 64.
- Radii: 4 / 8 / 12 / 999.
- Light theme first; I'll wire dark-mode aliases but leave the dark palette as a TODO.
- No framework-specific component code yet (no React/Vue/Svelte) — just tokens + CSS variables. I'll add a framework layer once you tell me which one.

Want me to go ahead and create the folder, scaffold the four `.pen` files via the Pencil MCP, and write the token/doc files? If yes, I'll start with `foundations.pen` so the variables exist before anything references them.
