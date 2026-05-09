# Iconography

How icons look and where they go. The agent reads this when picking an icon, sizing one, or pairing one with text. The icon library itself is named in `design-system.md`; this file covers the rules around using it.

## The library

Single source — pick one in `design-system.md` and stay there. Default for new projects: **Lucide** (1.5px stroke, geometric, mode-agnostic). Mixing icon libraries inside one product is the strongest "AI-assembled UI" signal short of mixing three competing fonts.

## Stroke weight

- **Body / UI icons:** 1.5px (Lucide default). Holds at all sizes ≥ 12.
- **Display icons** (hero illustrations, marketing): 1.75–2px optionally, declared explicitly.
- **Filled (solid) icons:** use only for *active* states in tab bars or highlighted statuses — never as the resting variant in the same set as line icons.

**Rule:** in any single row or group, icons share a stroke weight. A row with one 2px icon and three 1.5px icons reads as broken.

## Sizes per context

| Context | Size (px) | Variable |
|---------|-----------|----------|
| Inside a chip / tag | 12 | `$iconXs` |
| Inside a button (paired with label) | 16 | `$iconSm` |
| Inline with body text | 16 | `$iconSm` |
| Standalone in a row (icon button, list-item leading icon) | 20 | `$iconMd` |
| Top nav, sidebar nav | 20 | `$iconMd` |
| Empty-state and feature illustration | 24–32 | `$iconLg` / `$iconXl` |
| Marketing / hero | 40–64 | n/a — declare per use |

The icon size variables are independent of the `$textN` ramp — don't reuse `$textBase` for icon size, even when both happen to be 16.

## Color rules

- **Inherit by default.** An icon next to a label takes the label's `color`. This means a button with `color: $textPrimary` paints its icon `$textPrimary` automatically. No separate fill prop unless you mean to diverge.
- **Status icons get `$danger`, `$warning`, `$success` directly.** Pair with a matching text label — icon-only status is invisible to colorblind users.
- **Icon-on-color buttons** (e.g. a primary CTA) take the button's text color, not a "muted" version. Don't shave 20% off opacity for "subtlety" — it's a design tell.
- **Dark mode:** the inherit rule handles most cases. Where an icon sits on a colored surface, verify contrast at the rendered color, not the variable name. `$primary` → `$onPrimary` should pass 3:1 in both modes.

## When to use an icon

Default to **icon + text label**. Reach for **icon-only** sparingly:

- Universal symbols where the meaning is unambiguous: ✕ (close), 🔍 (search), ⚙ (settings), trash (delete), pencil (edit), 3-dots (more).
- Icon buttons in dense toolbars where labels would crowd everything else.
- The user has demonstrably learned the icon (e.g. an app the user uses daily).

When in doubt, pair with a label. Icon-only nav with no text is an AI tell — and an accessibility regression: every icon-only control needs an `aria-label`.

## When *not* to use an icon

- **Decorative-only icons next to every form field label.** `User icon` next to "Name" adds nothing. Strip them.
- **Three icons in a row that all mean roughly the same thing.** If you can't tell them apart at a glance, the user can't either.
- **An icon to "balance" a layout.** If the layout needs balancing, fix the layout.
- **Brand logos as decorative bullet points.** Use proper marks at proper sizes, or none.

## Icon + text spacing

| Pairing | Gap |
|---------|-----|
| Icon (16) + body text | `$space-2` (8) |
| Icon (12) inside a chip + label | `$space-1` (4) |
| Icon (20) leading a list item + title | `$space-3` (12) |

The icon goes **before** the label (left in LTR) by default. Trailing icons (right) only when they indicate state (chevron for expand, external-link arrow for outbound).

## Icon-only buttons (special rules)

- Touch target ≥ 44 × 44 even when the icon is 16 × 16. Pad the button.
- Always carry an `aria-label` (in code) and a Pencil `context` describing the action.
- Default to a tooltip on hover/focus that names the action — without a label, the tooltip is the only chance a user has to learn the meaning.
- Don't put more than ~5 icon-only buttons in a single row before grouping or labeling them.

## Custom illustrations

When the icon library doesn't have what's needed:

1. **First, check whether you actually need a custom one.** "Spaceship icon for our space-themed product" is rarely worth the maintenance.
2. If yes, draw it at 24px and 16px sizes and verify both render — tiny custom icons usually need different drawings, not a scaled-down version of the large one.
3. Match the existing library's stroke weight, joins, and overall visual rhythm. A 2px hand-drawn icon next to a row of 1.5px Lucide icons is jarring.
4. Add it to the `.lib.pen` so it survives.

## Brand mark / logo

The product's logo is **not** part of the icon set. Treat it as a `brand.md` concern — clear space, sizing, and color rules differ from generic icons.
