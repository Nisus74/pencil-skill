# Example: pick a style + palette + font from the catalogues, populate tokens, scaffold a starter

User says:

> *"Start a new pencil project for a developer-tools dashboard. Make it feel like Linear."*

This example shows the full workflow the catalogues enable: read brief → pick style → pick palette recipe → pick font pairing → populate `tokens.md` → call `set_variables` MCP → record commitments in `visual-style.md` → scaffold starter components that match the picks. After this sequence, every subsequent design references `$tokens`, never literal hex.

---

## Step 1: Read the brief and confirm constraints

The user named:

- **Industry:** developer tools.
- **Reference:** 'feel like Linear'.

The agent loads `references/industry-patterns.md` § SaaS § Developer tools and notes the conventions: dense, monospace-friendly, terminal-aesthetic OK, dark mode by default, keyboard-first, ⌘+K command palette is table-stakes.

The agent also loads `references/style-catalogue.md` and finds the entry for Linear directly: Swiss / International (in Linear's day-mode) and Dark-mode-first (Linear's default).

If anything is unclear, the agent asks one quick question:

> *"For the developer-tools dashboard: light mode default, dark mode default, or both shipped equally? Linear ships dark by default and most developers stay there."*

Assume the user picks **dark by default, light as alternative**.

## Step 2: Pick the style

From `references/style-catalogue.md`:

- **Family:** Modernist (specifically Swiss / International) and Atmospheric (Dark-mode-first).
- **Style commitment:** Swiss / International with Dark-mode-first ground.
- **Sample component cues** (lifted from the catalogue):
  - Flat backgrounds, single-line dividers
  - Sans-serif type with tight letter-spacing on headings
  - Generous whitespace (1.5x to 2x default)
  - Layered shadows (ambient + direct, two layers)
  - Near-black background (#0a0a0a, not #000); elevated surfaces lighter not darker

## Step 3: Pick the palette recipe

From `references/colour-palettes.md`:

- The user's brief points to developer-tools dark, so the agent picks the **Cursor Dark** recipe (Pure Slate dark + Tailwind Cyan accent).
- Alternatively the agent could pick **Linear Dark** (Pure Slate dark + Tailwind Indigo lighter steps for dark) since the user explicitly named Linear.
- Pick **Linear Dark** to match the brief.

The recipe says: Tailwind Slate (dark scale, 50 → 950 inverted) + Tailwind Indigo (lighter steps for dark mode accent).

The agent looks up Tailwind Slate and Tailwind Indigo at https://tailwindcss.com/docs/colors. The full scales are documented there with hex values for each step.

## Step 4: Pick the font pairing

From `references/font-pairings.md`:

- Sub-category Sans + Mono (developer tools).
- Two strong candidates: **Inter + JetBrains Mono** (default modern SaaS) or **Geist + Geist Mono** (modern dev-tool).
- The user said 'feel like Linear'; Linear uses Inter. Pick **Inter + JetBrains Mono**.
- Both fonts are free (Google Fonts for Inter; Google Fonts and JetBrains for JetBrains Mono).

Weights to ship: Inter 400, 500, 600, 700; JetBrains Mono 400, 500.

## Step 5: Open the document and inspect existing variables

Before populating new tokens, the agent reads what already exists in the `.pen` file:

```js
get_editor_state()
get_variables({ documentId: <doc-id> })
```

This returns the current variables (probably empty for a greenfield project) and the document's themes. The agent confirms the document declares `themes.mode: ["light", "dark"]` (or adds it if missing).

## Step 6: Populate `assets/design-system/tokens.md`

The agent edits `tokens.md` to commit the chosen palette and fonts as semantic tokens. The hex values come from the Tailwind scales the agent looked up in step 3.

Updated `tokens.md` sections (showing only the rows the agent populates; the rest of the template stays):

```markdown
## Colour

| Variable | Light | Dark | Use for |
|----------|-------|------|---------|
| `$bg` | `#f8fafc` (Slate 50) | `#020617` (Slate 950) | Page background. |
| `$surface` | `#ffffff` | `#0f172a` (Slate 900) | Card/panel background. Lighter than `$bg` in dark, contrary to the light pattern. |
| `$surfaceElevated` | `#ffffff` | `#1e293b` (Slate 800) | Modals, popovers. Higher elevation than surface. |
| `$border` | `#e2e8f0` (Slate 200) | `#1e293b` (Slate 800) | Hairlines, dividers. |
| `$borderMuted` | `#f1f5f9` (Slate 100) | `#0f172a` (Slate 900) | Quieter hairlines (table row dividers). |
| `$textPrimary` | `#0f172a` (Slate 900) | `#f1f5f9` (Slate 100) | Body text, headings. |
| `$textSecondary` | `#475569` (Slate 600) | `#94a3b8` (Slate 400) | Helper text, captions. |
| `$textMuted` | `#94a3b8` (Slate 400) | `#64748b` (Slate 500) | Placeholder labels, disabled text. |
| `$accent` | `#4f46e5` (Indigo 600) | `#818cf8` (Indigo 400) | Primary CTAs, focus, brand accent. |
| `$accentHover` | `#4338ca` (Indigo 700) | `#a5b4fc` (Indigo 300) | Hover/pressed accent. |
| `$success` | `#059669` (Emerald 600) | `#34d399` (Emerald 400) | Success state. |
| `$warning` | `#d97706` (Amber 600) | `#fbbf24` (Amber 400) | Warning, non-blocking. |
| `$danger` | `#dc2626` (Red 600) | `#f87171` (Red 400) | Error, destructive. |
| `$focusRing` | `#4f46e5` (Indigo 600) | `#818cf8` (Indigo 400) | Keyboard focus, 2px outline, 2px offset. |

## Typography

| Variable | Value | Use for |
|----------|-------|---------|
| `$fontDisplay` | `'Inter', sans-serif` | Display sizes, hero headings. |
| `$fontBody` | `'Inter', sans-serif` | Body text, UI chrome. |
| `$fontMono` | `'JetBrains Mono', monospace` | Code blocks, IDs, keyboard shortcuts, tabular numerics. |
| `$fontWeightRegular` | `400` | Default body weight. |
| `$fontWeightMedium` | `500` | Subheadings, button labels. |
| `$fontWeightSemiBold` | `600` | Headings (h2-h4). |
| `$fontWeightBold` | `700` | Display headings (h1). |
```

Verify contrast: the agent checks each pair against APCA Lc 75 for body text (https://www.myndex.com/APCA/). Slate 900 on Slate 50 in light: passes. Slate 100 on Slate 950 in dark: passes. Indigo 400 on Slate 950: passes. Indigo 600 on Slate 50: passes. Document the result in `visual-style.md`.

## Step 7: Mirror the tokens into the `.pen` file via `set_variables`

```js
set_variables({
  documentId: <doc-id>,
  variables: [
    {
      name: "bg",
      type: "color",
      value: [
        { value: "#f8fafc", theme: { mode: "light" } },
        { value: "#020617", theme: { mode: "dark" } },
      ],
    },
    {
      name: "surface",
      type: "color",
      value: [
        { value: "#ffffff", theme: { mode: "light" } },
        { value: "#0f172a", theme: { mode: "dark" } },
      ],
    },
    {
      name: "accent",
      type: "color",
      value: [
        { value: "#4f46e5", theme: { mode: "light" } },
        { value: "#818cf8", theme: { mode: "dark" } },
      ],
    },
    // ... continue for textPrimary, textSecondary, border, success, warning, danger, focusRing
    {
      name: "fontBody",
      type: "string",
      value: "Inter, sans-serif",
    },
    {
      name: "fontMono",
      type: "string",
      value: "JetBrains Mono, monospace",
    },
  ],
});
```

After this call, the `.pen` file's `variables` section holds the same values as `tokens.md`. The agent has *one source of truth* (tokens.md) and the `.pen` mirrors it.

## Step 8: Record commitments in `visual-style.md`

The agent edits `assets/design-system/visual-style.md`:

```markdown
## Chosen style

**Style:** Swiss / International with Dark-mode-first ground.
**Style family:** Modernist + Atmospheric.
**Why this style:** Developer-tools audience expects calm, dense, type-led chrome that stays out of the canvas. Dark-mode-first because the audience uses the product for hours of focused work.

**Sample component cues:**
- Flat backgrounds, single-line dividers
- Inter at tight letter-spacing on headings (-0.02em)
- Layered shadows (two layers minimum)
- Near-black ground (#020617, Slate 950); elevated surfaces lighter (Slate 900)

**Anti-patterns to avoid:**
- Inoffensive default neutral that could belong to any SaaS. Lean into Linear-adjacent confidence.
- Light mode shipped as primary (audience prefers dark).

## Chosen palette

**Palette recipe:** Linear Dark (Pure Slate + Tailwind Indigo).
**Source:** Tailwind v4 Slate scale + Indigo scale (https://tailwindcss.com/docs/colors).
**Mode coverage:** both (dark default).
**APCA contrast verified:** yes: body text Lc 90+ in both modes; accent on background Lc 75+ in both modes.
**Colour-blind safety:** verified via Stark; state coding pairs colour with shape (success ✓, warning △, danger ✕).

## Chosen typography

**Font pairing recipe:** Inter + JetBrains Mono.
**Source:** Google Fonts (both free).
**Weights to ship:** Inter 400, 500, 600, 700; JetBrains Mono 400, 500.
**Why this pairing:** Default modern SaaS pairing; Linear uses Inter and the brief named Linear as the reference.

## Deviations from the catalogue

No deviations. The catalogue picks fit the brief directly.
```

## Step 9: Scaffold starter components matching the style

With tokens populated, the agent scaffolds the foundational components in a `.lib.pen` (per [`composition-patterns.md`](../../references/composition-patterns.md) § When to extract to .lib.pen). Starter components:

- `Button` (Primary, Secondary, Ghost, Destructive): uses `$accent`, `$accentHover`, `$danger`.
- `Input` (Text, Email, Search, Password): uses `$surface`, `$border`, `$textPrimary`, `$focusRing`.
- `Card`: uses `$surface`, `$surfaceElevated`, `$border`, plus a layered shadow (per the chosen style cues).
- `Badge` (Success, Warning, Danger, Info): uses the corresponding state tokens.

Example `batch_design` for the `Button.Primary`:

```js
batch_design({
  documentId: <doc-id>,
  ops: [
    {
      op: "C",  // Create
      parent: "<library-root-frame-id>",
      node: {
        type: "frame",
        name: "Button_Primary",
        reusable: true,
        context: "Primary CTA button. Uses $accent, $accentHover. 40px height, 16px horizontal padding. Hover increases contrast (lighter accent in dark; darker accent in light). Focus ring uses $focusRing at 2px offset.",
        layout: { direction: "row", align: "center", justify: "center", gap: 8 },
        size: { height: 40, padding: { x: 16, y: 0 } },
        fill: "$accent",
        cornerRadius: 8,
        children: [
          {
            type: "text",
            text: "Button",
            fontFamily: "$fontBody",
            fontWeight: "$fontWeightMedium",
            color: "$bg",  // contrast against $accent
          }
        ],
      },
    },
    // ... Button_Secondary, Button_Ghost, Button_Destructive variants
  ],
});
```

Note: every fill, colour, and font reference is a `$token`, not a literal hex or string.

## Step 10: Verify with one screenshot

Per `SKILL.md` § Verification ladder, take one screenshot of the starter components in both modes. Confirm:

- The chosen style cues are visible (flat surfaces, tight letter-spacing, layered shadows).
- The palette renders correctly in both modes.
- Contrast holds.
- Components don't use any literal hex (the agent did its job).

```js
get_screenshot({ documentId: <doc-id>, nodeId: "<library-root-frame-id>" });
// In dark mode
get_screenshot({ documentId: <doc-id>, nodeId: "<library-root-frame-id>", theme: { mode: "dark" } });
```

If the screenshots match the chosen style, hand back to the user with a one-paragraph summary:

> *'Set up Linear Dark for the developer-tools dashboard. Style: Swiss / International + Dark-mode-first. Palette: Tailwind Slate + Indigo (committed in tokens.md, mirrored to .pen variables). Typography: Inter + JetBrains Mono (Google Fonts). Starter components in the library: Button (Primary / Secondary / Ghost / Destructive), Input (Text / Email / Search / Password), Card, Badge. All components reference $tokens. Ready to design screens against this system.'*

## Why this matters

This sequence is the *only* way to get coherence across multiple sessions. Without `visual-style.md`, the agent picks a different style each session and the product visually drifts. With it, every future agent reads the file at session start and constrains its choices.

The catalogues (style, palettes, fonts) are consulted *once* per project. After this sequence, the agent never reads them again. All future designs reference `$tokens` from the project's `tokens.md` (mirrored in the `.pen` `variables`).

## Common mistakes to avoid

- **Lifting hex codes from `references/colour-palettes.md` into `batch_design` directly.** The references file is a recipe menu, not a value source. Hex values belong in `tokens.md` and the `.pen` `variables`.
- **Hard-coding font names in `batch_design`.** Same reason. Font names belong in `tokens.md` as `$fontBody`, `$fontMono`.
- **Skipping the `set_variables` call.** Without mirroring tokens into the `.pen` variables, the design references resolve to nothing (or to defaults).
- **Skipping `visual-style.md`.** Without it, the next session's agent doesn't know what style was picked. The product loses coherence.
- **Picking from the catalogues every session.** The catalogues are a one-time pick. After commitment, the agent reads `visual-style.md` and `tokens.md`.

## See also

- `references/style-catalogue.md`: the menu of named styles.
- `references/colour-palettes.md`: the menu of palette recipes.
- `references/font-pairings.md`: the menu of font pairings.
- `references/industry-patterns.md`: per-industry recommendations.
- `assets/design-system/visual-style.md`: the project commitment template.
- `assets/design-system/tokens.md`: the project token template.
- `references/composition-patterns.md`: when and how to extract starter components to a `.lib.pen`.
- `references/iteration-patterns.md`: rescues when the chosen style isn't landing.
- `SKILL.md` § Verification ladder: when to screenshot during this flow.
