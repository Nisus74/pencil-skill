# Tokens

The variables your designs use. The agent reads this file when it needs to pick a color, a spacing value, or a type size — so the entries should be **decisions** ("use X when Y"), not just a list.

## Color

Every color variable carries BOTH a `light` and a `dark` value. No exceptions. The Pencil document declares `themes: { mode: ["light", "dark"] }` at the top level.

| Variable | Light | Dark | Use for |
|----------|-------|------|---------|
| `$primary` | `<#hex>` | `<#hex>` | Primary CTAs, focused states, brand accents. |
| `$primaryMuted` | `<#hex>` | `<#hex>` | Hover/pressed primary backgrounds, primary-tinted surfaces. |
| `$accent` | `<#hex>` | `<#hex>` | Highlights, badges, secondary accents. Use sparingly. |
| `$surface` | `<#hex>` | `<#hex>` | Default page/canvas background. |
| `$surfaceMuted` | `<#hex>` | `<#hex>` | Card backgrounds, raised surfaces, secondary panels. |
| `$border` | `<#hex>` | `<#hex>` | Hairlines, input borders, divider lines. |
| `$textPrimary` | `<#hex>` | `<#hex>` | Body text, headings — default text color. |
| `$textMuted` | `<#hex>` | `<#hex>` | Helper text, captions, placeholder labels. |
| `$danger` | `<#hex>` | `<#hex>` | Error states, destructive actions, validation failures. |
| `$warning` | `<#hex>` | `<#hex>` | Cautions, non-blocking alerts. |
| `$success` | `<#hex>` | `<#hex>` | Confirmation, completion. |
| `$focusRing` | `<#hex>` | `<#hex>` | Keyboard focus outline. Always declared, always 2px. |

**Rule:** every color in a new design uses one of these variables. Never `#hex` directly. If you need a color that doesn't exist here, add it (with both light and dark values) before you reference it.

**Contrast:** every (text color, background) pair must hit WCAG AA — body text ≥ 4.5:1, large text and UI components ≥ 3:1. Check it in BOTH modes; a pair that passes in light often fails in dark and vice versa. If a pair fails, change the value, don't ship the design.

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
| `$space-7` | 40 | — |
| `$space-8` | 48 | Page-level vertical rhythm; major section gap. |
| `$space-9` | 64 | Top-of-page hero margins. |
| `$space-10` | 80 | — |
| `$space-11` | 96 | — |
| `$space-12` | 128 | Marketing-page hero spacing. |

**Rule:** every padding and gap is one of these. If you find yourself reaching for an in-between value, it's almost always a sign the surrounding rhythm is off — not that you need a new token.

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

- `$fontHeading` — `<Inter | Geist | Manrope | other>`
- `$fontBody` — `<Inter | Geist | Manrope | other>`
- `$fontMono` — `<JetBrains Mono | IBM Plex Mono | other>` (for code/numerics)

**Rule:** every text node uses a `$textN` variable. Avoid raw font sizes. Body text is `$textBase` unless there's a reason.

## Border radius

| Variable | px | Use for |
|----------|----|---------|
| `$radiusSm` | 4 | Inputs, chips, small interactive surfaces. |
| `$radiusMd` | 8 | Buttons, badges, default for most interactive elements. |
| `$radiusLg` | 12 | Cards, modals, large containers. |
| `$radiusXl` | 24 | Hero containers, oversized panels. |
| `$radiusFull` | 9999 | Pills, avatars, fully-rounded shapes. |

## Adding a token

If you need a value that doesn't fit, add it here first, then reference it. Don't skip the table — the agent uses this file as the source of truth, and one-off values quietly break consistency over time.
