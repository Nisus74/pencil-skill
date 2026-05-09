# Elevation

How depth is communicated. The agent reads this when adding cards, modals, popovers, dropdowns, or anything that should feel "above" the page. Without rules here, AI defaults to `0 4px 24px rgba(0,0,0,0.15)` everywhere — Bootstrap-era, immediately dated.

## The scale

Five levels. Most surfaces sit at level 0; reach for higher levels only when a surface needs to detach from what's behind it.

| Variable | Level | Light treatment | Dark treatment | Use for |
|----------|-------|----------------|----------------|---------|
| `$elevation0` | Flat | None | None | Page background, inline blocks, list rows. |
| `$elevation1` | Raised | `0 1px 2px rgba(0,0,0,0.06)` | `0 0 0 1px rgba(255,255,255,0.06)` (border, no shadow) | Cards, table headers, sticky chrome. |
| `$elevation2` | Overlay | `0 4px 12px rgba(0,0,0,0.08)` | `0 0 0 1px rgba(255,255,255,0.08)` + subtle inner glow | Popover, tooltip, dropdown, hover-elevated card. |
| `$elevation3` | Floating | `0 8px 24px rgba(0,0,0,0.10)` | Border + `0 8px 24px rgba(0,0,0,0.5)` (true shadow against dark surface, but only because the surface itself is dark) | Modal, dialog, command palette, drawer (mobile). |
| `$elevation4` | Top | `0 16px 48px rgba(0,0,0,0.14)` | Same as level 3, plus `$primaryMuted` border accent | Full-screen takeovers, onboarding modals. Reserve for one surface at a time. |

**Rule:** at most one level-3+ surface visible at any moment. If a modal opens over a dropdown, close the dropdown first.

## Why dark mode is different

Drop shadows mostly fail in dark mode. A 6%-opacity black shadow on a `#0F0F12` background is invisible. Don't paper over this by darkening the shadow further — that creates an opaque "dirt smudge" effect.

Instead, in dark mode, depth comes from **light borders** (a 1px hairline at 6–10% white opacity), **subtle inner glow**, or **lightening the surface itself** (a card on a `#0F0F12` page might be `#16161A`). Reserve actual shadows for level 3+ where the surface contrast is large enough to support them.

This is why the Light/Dark columns in the table above aren't symmetric — they shouldn't be.

## What sits where (defaults)

| Surface | Elevation | Notes |
|---------|-----------|-------|
| Page background | `$elevation0` | Flat. |
| Card | `$elevation1` | Raised hairline. Most cards stay here. |
| Card on hover (clickable card) | `$elevation2` | Lift on hover; transition is the `$durationFast` color/transform recipe. |
| Sticky header / footer | `$elevation1` | Hairline shadow appears only when content scrolls beneath (use `box-shadow` only when `scrollTop > 0`). |
| Sidebar (desktop) | `$elevation0` | Sidebars don't elevate — they sit on the same plane as the page, separated by a 1px `$border`. |
| Dropdown / Select menu | `$elevation2` | |
| Popover | `$elevation2` | |
| Tooltip | `$elevation2` | |
| Modal | `$elevation3` | Backdrop is `rgba(0,0,0,0.5)` (light) / `rgba(0,0,0,0.7)` (dark). |
| Drawer / Sheet | `$elevation3` | |
| Toast | `$elevation2` | |

## Anti-patterns

- **Shadow as the only visual signal.** Pair every elevation > 0 with at least one other affordance (border, lighter surface color, padding). Shadow alone is invisible to color-blind users in some palettes and gone entirely in dark mode.
- **Glow shadows on light mode** (`box-shadow: 0 0 24px rgba(120, 80, 255, 0.4)`). Reads as 2014-era "neon." Reserve glow effects for explicit brand moments declared in this file.
- **Stacked drop shadows.** Two `box-shadow` values to "make it pop." If level 1 isn't enough, you want level 2 — not level 1 + level 1.
- **Animated elevation on first render.** Cards lifting into place when the page loads is loading-shimmer-adjacent and reads AI-generated. Animate elevation only on user interaction (hover, focus, drag).
- **Inset shadows on inputs in dark mode.** Almost always invisible. Use a 1px border instead.

## Borders, the elevation alternative

When you'd reach for a shadow but the surface is too low-contrast for one to read, use a border:

- Light mode: `1px solid $border` (e.g. Zinc-200).
- Dark mode: `1px solid` at ~6–10% white opacity, or `$borderMuted`.

Borders + level-1 shadow is the most common card recipe.

## Rounded corners + elevation

Higher-elevation surfaces use larger radii:

- `$elevation1` (cards) → `$radiusLg` (12px).
- `$elevation2` (popovers) → `$radiusLg` (12px).
- `$elevation3` (modals) → `$radiusXl` (24px).

Sharp corners (`$radiusSm` or 0) on a high-elevation surface read as cheap. Pair `$radiusXl` with at least `$elevation2`.

## Adding new elevation tokens

If you need a depth that doesn't fit, add a new `$elevationN` row here with **both** light and dark treatments before referencing it. Don't ship a one-off `box-shadow` value in a single component — it'll metastasize.
