# Extract

The extraction workflow: spotting repeated patterns in a working design and pulling them out into reusable components, tokens, or library entries. The design starts as one-offs (a button built from a frame and a text node; a colour value `#3E9D55` written into three different fills); extraction is how it becomes a system over time.

This reference is the *how-to-promote* depth that complements the *components-first* discipline rule in SKILL.md. Use it when the user asks to *"clean this up"*, *"extract a component"*, *"add this to the design system"*, or whenever you notice you're rebuilding the same thing twice in the same `.pen` file.

## When to extract
- A node, group, or shape has been built more than once in the same `.pen` file (or across files in the same project).
- A colour, font, spacing value, or radius is repeated in three or more places.
- A pattern (a card with an icon and a title; an empty state with copy and a CTA) is emerging across surfaces.
- A `.lib.pen` exists for the project and the current `.pen` is building something that should live in it.

## When NOT to extract
- One-off designs (a quick sketch, a throwaway mock); extraction is overhead the surface won't pay back.
- The pattern has been built once and might not repeat; let it appear twice before extracting.
- The user explicitly said *"don't worry about reuse"* or *"just sketch it"*.
- The extracted component would have so many variants that it's an over-system; sometimes two purpose-built components are clearer than one component with twelve variants.

## What to extract

### Tokens
The lowest-cost extraction. A colour, a font family, a spacing value, a radius. Tokens live as variables (`SetVariables` inside `batch_design` per [color-and-contrast.md](color-and-contrast.md), [typography.md](typography.md)) and are referenced via `$variableName` from every node that needs them.

Token candidates:
- **Colours.** Any colour used in two or more places. Anything that should flip between light and dark modes.
- **Font families.** Display, body, mono. Each gets a token even if there's only one of each.
- **Font sizes.** A type scale (12, 14, 16, 20, 24, 32) is just a set of named tokens (`$textXs`, `$textSm`, etc.) referenced from text nodes.
- **Spacing.** The 4/8 multiples from [layout.md](layout.md), as `$spacingSm`, `$spacingMd`, etc.
- **Radii.** A small set (`$radiusSm`, `$radiusMd`, `$radiusFull`) referenced consistently.
- **Motion durations.** Per [motion-design.md](motion-design.md), `$durationFast`, `$durationMedium`.

### Components
Higher-cost extraction; pays back more. A reusable component lives in the document (or in an imported `.lib.pen`) and instantiates via `ref` nodes.

Component candidates:
- Anything built twice. Build #1 was a one-off; build #2 is signalling a pattern.
- Anything with clear states (hover, focus, disabled, error). Authoring those states once and reusing them is much cheaper than rebuilding them per instance.
- Anything that needs to update in lockstep across the design (a header, a sidebar, a card shell).

### Patterns
The largest unit; not always extracted into the design system but worth documenting. A pattern is a composition of components in a particular arrangement: a settings page anatomy, a confirmation modal shape, an empty state template.

Patterns often live in design-system docs (e.g. `design-system/patterns.md` if the project has it) rather than as `.pen` library entries. Code-side, they may map to layout components or templates.

## The extraction workflow

### 1. Identify the candidate
Read what you're about to build or what you just built. Is it a repeat? Does it have clear states? Is its design specific enough to commit to a name?

A pattern reveals itself as a candidate when:
- You catch yourself about to copy-paste from elsewhere in the file.
- Two existing nodes have nearly identical shape, varying only in content.
- You realise you've used the same hex value three times.

### 2. Name the candidate
Naming forces the role-clarification. Per the SKILL.md naming discipline rule:

- **Components are named after their role**, not their treatment: `PrimaryButton`, not `BlueButton`. `EmptyState`, not `CenteredCardWithIcon`.
- **Tokens are named semantically**: `$accent`, not `$green`. `$bg`, not `$zinc50`.

If the candidate doesn't have a clean role-bearing name, it isn't the right extraction yet. Either find the name or leave the pattern as primitives until it earns one.

### 3. Pick the extraction target
Tokens always extract to the document's `variables` (via `SetVariables` inside `batch_design`).

Components extract to one of:
- **The current `.pen` document.** A `reusable: true` node lives in the document; instances inside the same file can `ref` it. Good for components specific to this `.pen`.
- **An imported `.lib.pen`.** The component lives in a library file used across multiple `.pen` files. Good for project-wide components.

If a `.lib.pen` is already imported and the candidate is project-wide, extract there. If no library exists yet and the component is project-wide, this is the moment to create the library (see [SKILL.md](../SKILL.md) `.lib.pen libraries` section).

### 4. Author the canonical version
Build the extracted version with care; this is the version that will propagate. Specifically:

- **All variants** (states, sizes, options) are defined in the canonical version, not in instance overrides. If a button has primary, secondary, and tertiary, build all three as variants of the same component.
- **All states** are defined per [interaction-design.md](interaction-design.md): default, hover, focus, pressed, disabled, loading, error.
- **Every property** binds to a token where possible. Raw hex on a `reusable: true` component is doubly wrong; you've extracted the shape but not the system.
- **The `context` string** documents the component's role, expected usage, and any non-obvious behaviour.

### 5. Replace existing instances
Walk the existing nodes that built the pattern by hand. Replace each with a `ref` instance of the new component. Use `descendants: { ... }` overrides for per-instance content.

Use `batch_get` to read the subtree and tally the values yourself to find candidates; for bulk token replacements (e.g. swapping every `#3E9D55` to `$accent`), read the target nodes with `batch_get`, then loop `Update` inside a `batch_design` snippet (e.g. `for (id of ["a", "b"]) Update(id, { fill: "$accent" })`).

### 6. Verify
After extraction:
- Screenshot the affected surfaces. The visual result should be identical to before. If it isn't, the canonical version doesn't quite match the originals.
- Confirm the `.pen` still validates (no orphan references).
- Confirm the extracted component has all the variants its callers needed.

## Common extractions

### The token sweep
A file that pre-dates the discipline rules likely has raw hex everywhere. A one-pass extraction:

1. Read the subtree with `batch_get` and tally every `fill` value yourself.
2. Group the hex values by visual role (backgrounds, text, accents).
3. Declare semantic variables (`$bg`, `$text`, `$accent`) covering the groups.
4. Loop `Update` inside a `batch_design` snippet to swap each hex for its variable (e.g. `for (id of ["a", "b"]) Update(id, { fill: "$bg" })`).
5. Test under both light and dark modes; raw hex doesn't theme, so the swap may reveal mode-bugs the original design hid.

### The button extraction
The most common component extraction. Walk the file, find every button-shaped node (frame + text + interactive intent), confirm the variants needed (primary / secondary / tertiary; small / medium / large; disabled / loading / error), build the canonical version with all variants, replace instances with `ref` nodes.

### The card extraction
Cards appear in many designs in different specific forms. Extract the shell (`Card` component with slots) once; let consumers fill the slots per instance. Don't build `MetricCard`, `FeatureCard`, `PricingCard` as separate components if they share the same shell.

### The empty-state extraction
Empty states across a product follow a pattern: icon or illustration, headline, body copy, primary action. Build `EmptyState` once with slots for each; variants cover the four types (first-use, returning-empty, no-results, no-permission) per [onboard.md](onboard.md) and [product.md](product.md).

### The icon-set extraction
Most projects use one icon library (Lucide, Material Symbols, Phosphor). Use `icon` nodes with the project's chosen library; don't import SVGs for icons that exist in the library. The icon library itself is effectively an extracted set.

## Anti-patterns in extraction

- **Over-extraction.** Building components with twelve props because every possible variation might appear. Components with many variants are hard to read and hard to maintain. Split into two purpose-built components instead.
- **Premature extraction.** Promoting a one-off to a component before it appears twice. The one-off may never repeat; the component now has to be maintained anyway.
- **Naming by treatment.** `BlueCard`, `RoundedButton`, `LargeFrame`. The names lock in the visual; when the visual evolves, the names lie.
- **Extracting and leaving the originals.** Building the canonical version, never replacing the hand-built instances. The library and the working design now diverge.
- **Components without states.** Extracting only the default state; consumers each rebuild hover/focus/disabled. The point of the extraction is to do this once.
- **Raw hex on `reusable: true` components.** The component is reusable; the colour is not theme-aware. The next colour change has to touch every instance.

## Pencil-specific

### `reusable: true` and `ref` mechanics
A node marked `reusable: true` becomes a component. Other nodes can reference it via `ref: "<componentId>"` and override properties via `descendants: { "<childId>": { ...overrides } }`.

```
// Inside batch_design:
btn = Insert("doc", {
  type: "frame",
  name: "PrimaryButton",
  reusable: true,
  // ... full button spec with all states as variants
})

// Then elsewhere, instantiate:
instance = Insert("page", {
  type: "ref",
  ref: btn,
  descendants: { "<btn-label-id>": { content: "Sign in" } }
})
```

### Library lifecycle
A `.lib.pen` is a regular `.pen` file marked as a library. Once marked, it can't be unmarked. To use:

1. Author the library file with `reusable: true` components and shared variables.
2. Add it to the consuming document's `imports`: `Update(docRootId, { imports: { "ds": "./design/system.lib.pen" } })`.
3. Instantiate components in the consumer via `ref` nodes pointing at library node IDs.

### When to create a `.lib.pen`
- The project has more than one `.pen` file AND you're recreating the same component.
- A clear set of shared tokens has emerged across files.
- The team is ready to maintain the library (changes to the library affect every consumer; commitment).

Don't create one for a single-file project. Don't create one for a throwaway prototype.

### Inventory before building
The components-first rule in SKILL.md requires inventorying existing components before building new ones. Extraction is the flip side: if you're building, also notice what *should* exist as a component but doesn't. Often the extraction catches itself: the agent is about to copy a card pattern for the third time, realises the pattern, extracts mid-flow rather than copy-pasting again.

### Track tokens via `get_variables`
To audit what tokens exist in the current document or an imported library:

```
get_variables({ filePath: "./design/system.lib.pen" })
```

The returned set is what consumers can reference via `$variableName`. If the library is missing a semantic role you need, add it via `SetVariables` inside `batch_design` against the library file before the consumer references it.

### Verify after extraction with the screenshot loop
The screenshot loop catches whether the extracted component matches the visual of the originals. Replace instances in small batches (3–5 at a time), screenshot the affected region, confirm the visual is unchanged. Bulk-replacing all instances at once and screenshotting only the final result hides the case where one instance was subtly different and the extraction lost it.
