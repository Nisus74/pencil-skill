# Tokens

The variables your designs use. The agent reads this file when it needs to pick a colour, a spacing value, or a type size, so the entries should be **decisions** ("use X when Y"), not just a list.

Each major section carries an *Archetype-keyed bundles* subsection at the end showing how the token choices reshape under different archetypes. See `assets/archetypes/` in the skill for the full archetype definitions; the bundles below are illustrative starting points you'd plug into the table above.

## Colour

Every colour variable carries BOTH a `light` and a `dark` value. No exceptions. The Pencil document declares `themes: { mode: ["light", "dark"] }` at the top level.

| Variable | Light | Dark | Use for |
|----------|-------|------|---------|
| `$primary` | `<#hex>` | `<#hex>` | Primary CTAs, focused states, brand accents. |
| `$primaryMuted` | `<#hex>` | `<#hex>` | Hover/pressed primary backgrounds, primary-tinted surfaces. |
| `$accent` | `<#hex>` | `<#hex>` | Highlights, badges, secondary accents. Use sparingly. |
| `$surface` | `<#hex>` | `<#hex>` | Default page/canvas background. |
| `$surfaceMuted` | `<#hex>` | `<#hex>` | Card backgrounds, raised surfaces, secondary panels. |
| `$border` | `<#hex>` | `<#hex>` | Hairlines, input borders, divider lines. |
| `$textPrimary` | `<#hex>` | `<#hex>` | Body text, headings, default text colour. |
| `$textMuted` | `<#hex>` | `<#hex>` | Helper text, captions, placeholder labels. |
| `$danger` | `<#hex>` | `<#hex>` | Error states, destructive actions, validation failures. |
| `$warning` | `<#hex>` | `<#hex>` | Cautions, non-blocking alerts. |
| `$success` | `<#hex>` | `<#hex>` | Confirmation, completion. |
| `$focusRing` | `<#hex>` | `<#hex>` | Keyboard focus outline. Always declared, always 2px. |

**Rule:** every colour in a new design uses one of these variables. Never `#hex` directly. If you need a colour that doesn't exist here, add it (with both light and dark values) before you reference it.

**Defaults (override per project):**

- One accent only (`$primary`); pick `$accent` only when a second hue genuinely earns its keep. Keep saturation under ~80%.
- Pick neutrals from one family, Zinc *or* Slate *or* Stone, and don't mix warm and cool grays.
- `$surface` (light) should be off-white (e.g. `#FAFAFA`), not `#FFFFFF`. `$surface` (dark) should be off-black (e.g. Zinc-950 `#09090B`), not `#000000`. Pure black on pure white reads as an AI default.
- No neon glows, no purple/blue gradient text on headings. If the brand calls for a gradient, declare it explicitly here and scope where it's used.

**Contrast:** every (text colour, background) pair must hit WCAG AA, body text ≥ 4.5:1, large text and UI components ≥ 3:1. Check it in BOTH modes; a pair that passes in light often fails in dark and vice versa. If a pair fails, change the value, don't ship the design.

**Theming syntax** (Pencil schema):

```jsonc
"surface": {
  "type": "color",
  "value": [
    { "value": "#FFFFFF", "theme": { "mode": "light" } },
    { "value": "#0B1117", "theme": { "mode": "dark" } }
  ]
}
```

The last matching theme wins. Activate dark mode on a node with `theme: { mode: "dark" }`.

### Archetype-keyed bundles

Illustrative starting bundles for projects that match a shipped archetype. Plug these values into the table above and adjust per brand.

- **`saas-apps/b2b/analytics-dashboard`** (light canonical):
  - `$primary` = deep ink `#1F2937` or a saturated brand variant (NOT violet by default), saturation 60–70%.
  - `$bg` = `#FAFAF9`, `$surface` = `#FFFFFF`, `$surfaceMuted` = `#F5F5F4`.
  - `$border` = Zinc-200 `#E7E5E4` (light), Zinc-800 `#27272A` (dark). Hairline only.
- **`saas-apps/b2b/modern-pro-tool`** (light canonical, Linear-style):
  - `$primary` = saturated indigo `#5E6AD2` or chosen brand hue at 70–85% saturation.
  - `$bg` = `#FAFAFA` (light) / `#0E0E10` (dark).
  - `$surfaceMuted` = `#F4F4F5` (used for sidebar background AND active-item background).
  - `$border` = `#E7E5E4` (light) / `#2A2A2E` (dark).
- **`marketing-websites/conversion-focused-saas`** (dark canonical for marketing):
  - `$primary` = cyan or chosen brand hue at 60–80% saturation.
  - `$accentSupport` = purple/lavender for badges and category labels (Linear pairs cyan + purple). Optional second hue.
  - `$bg` = near-black warm dark (`#0E0E10`) for marketing. Light mode supported but not canonical.
- **`marketing-websites/editorial-storytelling`** (light or dark, often deliberate per-section):
  - `$primary` = restrained, used sparingly; saturation 50–70%.
  - `$bg` and `$surface` are effectively the same value; cards are absent.

**What generic looks like (don't ship this):** `$primary` = `#7C3AED` (violet) by default, `$bg` = `#FFFFFF` pure, `$surface` = `#FFFFFF` (no hierarchy), `$border` invisibly soft, two competing accent colours for "variety".

## Spacing

A modular scale. All gaps, paddings, and margins come from here.

| Variable | px | Use for |
|----------|----|---------|
| `$space-0` | 0 | No spacing (rare; explicit zero). |
| `$space-1` | 4 | Tight inline gaps (icon-to-text inside a chip). |
| `$space-2` | 8 | Inside buttons (icon-to-label). |
| `$space-3` | 12 | Compact list-item gaps. |
| `$space-4` | 16 | Default gap inside a form, list, or vertical stack. |
| `$space-5` | 24 | Padding inside cards; section sub-gaps. |
| `$space-6` | 32 | Card outer padding; medium section gap. |
| `$space-7` | 40 | (rarely used) |
| `$space-8` | 48 | Page-level vertical rhythm; major section gap. |
| `$space-9` | 64 | Top-of-page hero margins. |
| `$space-10` | 80 | (rarely used) |
| `$space-11` | 96 | (rarely used) |
| `$space-12` | 128 | Marketing-page hero spacing. |

**Rule:** every padding and gap is one of these. If you find yourself reaching for an in-between value, it's almost always a sign the surrounding rhythm is off, not that you need a new token.

### Archetype-keyed bundles

The same scale, but density choices differ:

- **`saas-apps/b2b/analytics-dashboard`** (medium-dense): card padding 16–20 (`$space-4` to `$space-5`); table row padding 8–12 vertical (`$space-2` to `$space-3`); skip 32+ unless separating major page regions.
- **`saas-apps/b2b/modern-pro-tool`** (dense, Linear-style): sidebar items 6–8 vertical (`$space-1` to `$space-2`); list rows 6–10 vertical; card padding 16–20 (`$space-4` to `$space-5`); the `$space-5` step matters most. Skip `$space-12` entirely on app surfaces.
- **`marketing-websites/conversion-focused-saas`**: hero padding 120+ vertical (`$space-12`); section padding 80–120 (`$space-10` to `$space-12`); card-internal padding 24–32 (`$space-5` to `$space-6`).
- **`marketing-websites/editorial-storytelling`** (most generous): hero padding 200+ (above `$space-12`, may need a custom value); section padding 160–240 between sections; content max-width tight at 680–760 for prose.

**What generic looks like (don't ship this):** every region uses the same `$space-4` and `$space-6` rhythm; nothing intentionally denser or airier than the default. Cards float on `$space-8` of whitespace whether they belong on a dense dashboard or a marketing hero.

## Typography

A type ramp. All font sizes come from here.

| Variable | px | Use for |
|----------|----|---------|
| `$textXs` | 12 | Captions, footnotes, very fine print. |
| `$textSm` | 14 | Helper text, labels, dense table content. |
| `$textBase` | 16 | Body text. The default. |
| `$textLg` | 18 | Lead paragraphs, prominent body. |
| `$textXl` | 20 | Card titles, list-section headers. |
| `$text2xl` | 24 | Page subtitles, modal titles. |
| `$text3xl` | 32 | Page titles. |
| `$text4xl` | 48 | Marketing hero headings. |

Font families:

- `$fontHeading`, `<Geist | Satoshi | Cabinet Grotesk | other>`
- `$fontBody`, `<Geist | Satoshi | other>`
- `$fontMono`, `<Geist Mono | JetBrains Mono | IBM Plex Mono | other>` (for code/numerics)

**Defaults (override per project):**

- Dashboards / software UIs: `Geist` + `Geist Mono`, or `Satoshi` + `JetBrains Mono`.
- Marketing / editorial: `Cabinet Grotesk` or `Satoshi` for display; pair with a modern serif (`Fraunces`, `Instrument Serif`, `Editorial New`) only if the brand warrants it.
- Avoid by default: `Inter` (overused to the point of being an AI signature) and generic serifs (`Times New Roman`, `Georgia`, `Garamond`, `Palatino`). Use them only if the chosen archetype explicitly opts in.
- Body lines cap at ~65 characters.
- In dense layouts, numerics use `$fontMono` so columns of figures align.

**Rule:** every text node uses a `$textN` variable. Avoid raw font sizes. Body text is `$textBase` unless there's a reason.

### Archetype-keyed bundles

- **`saas-apps/b2b/analytics-dashboard`**:
  - `$fontUI` = `Geist` or `Satoshi`. Body 13–14px (`$textSm`).
  - `$fontMono` = `Geist Mono` or `JetBrains Mono` for ALL numerics (KPI values, table figures, axis labels).
  - 11px small caps with 0.04em tracking for column headers and section labels.
- **`saas-apps/b2b/modern-pro-tool`**:
  - `$fontUI` = `Inter Display` (canonical, archetype overrides the SKILL.md ban), `Söhne`, `Geist`, or `Satoshi`.
  - `$fontMono` = `Geist Mono`, `JetBrains Mono`, or `Berkeley Mono` for keyboard-shortcut chips and code blocks.
  - Body 13–14px with slightly negative tracking (-0.005em).
- **`marketing-websites/conversion-focused-saas`**:
  - `$fontDisplay` = `Inter Display` (canonical override), `Söhne`, or `Geist`.
  - `$fontBody` = same family, regular weight, 16–18px (`$textBase` to `$textLg`) for marketing prose.
  - Hero display 48–80px (`$text4xl` and above).
- **`marketing-websites/editorial-storytelling`**:
  - Display 64–120px on hero (well above `$text4xl`, may need custom value).
  - Body 18–22px with line-height 1.5–1.7. Reading is the activity.
  - Modern serif option (`Fraunces`, `Editorial New`, `Instrument Serif`) becomes acceptable in the manifesto flavour.

**What generic looks like (don't ship this):** Inter throughout (no archetype override declared), no monospace anywhere even on data, all text at one of three sizes (small, body, big), no character to type pairing.

## Border radius

| Variable | px | Use for |
|----------|----|---------|
| `$radiusSm` | 4 | Inputs, chips, small interactive surfaces. |
| `$radiusMd` | 8 | Buttons, badges, default for most interactive elements. |
| `$radiusLg` | 12 | Cards, modals, large containers. |
| `$radiusXl` | 24 | Hero containers, oversized panels. |
| `$radiusFull` | 9999 | Pills, avatars, fully-rounded shapes. |

### Archetype-keyed bundles

- **`saas-apps/b2b/analytics-dashboard`**: cards 6–10 (`$radiusSm` to `$radiusMd`). Buttons 8 (`$radiusMd`). No fully rounded.
- **`saas-apps/b2b/modern-pro-tool`** (Linear): cards 6–8. Buttons rounded rectangles 6–8. Tabs and segmented controls fully rounded pills (`$radiusFull`). Avatars circular.
- **`marketing-websites/conversion-focused-saas`**: card radius 12–16 (`$radiusLg`). Button radius 8–12. No fully rounded outside small chips.
- **`marketing-websites/editorial-storytelling`**: edges and corners barely matter, there are few rectangles to round. Default radius is largely cosmetic.

**What generic looks like (don't ship this):** everything at `$radiusLg` (12px) regardless of context, fully-rounded buttons everywhere, mismatched radii where adjacent elements use different values.

## Adding a token

If you need a value that doesn't fit, add it here first, then reference it. Don't skip the table, the agent uses this file as the source of truth, and one-off values quietly break consistency over time.
