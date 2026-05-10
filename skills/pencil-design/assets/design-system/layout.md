# Layout

Spacing rhythm, sizing behavior, and grid rules. The agent reads this when laying out a frame, a list, or a page.

## Auto-layout (the default)

Use Pencil frames with `layout: "vertical"` or `layout: "horizontal"` for almost everything. Reach for `layout: "none"` (absolute positioning) only when there's a specific reason, overlays, decorative backgrounds, illustration art.

**Default vertical stack:**

```jsonc
{ "layout": "vertical", "gap": "$space-4", "alignItems": "stretch" }
```

**Default horizontal row:**

```jsonc
{ "layout": "horizontal", "gap": "$space-3", "alignItems": "center" }
```

**Centered content (form on a page):**

```jsonc
{ "layout": "vertical", "justifyContent": "center", "alignItems": "center" }
```

## Sizing

For every node, decide explicitly: should it grow, shrink, or stay fixed?

- **Growing children** → `width: { sizing: "fill_container" }` (or `height`).
  - Use for: primary content area in a page, inputs in a form, list items in a vertical stack.
- **Shrinking children** → `width: { sizing: "fit_content" }`.
  - Use for: buttons, chips, badges, anything whose width should follow its label.
- **Fixed children** → `width: 240` (a number).
  - Use for: cards with intentional width, sidebars with intentional width, hero artwork.

**Rule of thumb:** in a vertical stack, most children are `fill_container` width and `fit_content` height. In a horizontal row, the reverse is rare, children are usually `fit_content` width with one or two growing to fill remaining space.

## Padding

Containers get padding, children don't get margin. Pencil has no margin concept; use the parent's `gap` and `padding` to control space.

| Container type | Default padding |
|----------------|-----------------|
| Page (top-level frame) | `$space-8` (mobile: `$space-4`) |
| Card | `$space-6` |
| Modal | `$space-6` |
| Section inside a page | `$space-6` vertical, `$space-4` horizontal |
| Button | `$space-3` horizontal, `$space-2` vertical |
| Input | `$space-3` horizontal, `$space-2` vertical |

## Responsive: breakpoints

Every project supports the three canonical breakpoints. Two patterns work, pick one and stay consistent across the project:

| Breakpoint | Frame size | Columns | Gutter | Max content width |
|------------|-----------|---------|--------|-------------------|
| Mobile | 390 × 844 | 4 | `$space-4` | full width |
| Tablet | 768 × 1024 | 8 | `$space-5` | full width |
| Desktop | 1440 × 900 | 12 | `$space-6` | `$maxContent` (1200) |

**Pattern A, per-breakpoint frames (recommended for marketing pages, dashboards, landing screens):** one frame per breakpoint, sibling to each other, sharing the same components and variables. Name them with a suffix: `LoginPage_Desktop`, `LoginPage_Tablet`, `LoginPage_Mobile`. Build the desktop frame first, then derive the smaller ones, usually the differences are stack direction (horizontal → vertical), padding, font scale.

**Pattern B, single fluid frame (recommended for app surfaces with predictable scaling):** one frame using `width: "fill_container"` and well-tuned auto-layout. Test by resizing the canvas frame and confirming the layout holds at each breakpoint.

For a page-level container, use `width: "fill_container"` on the outer frame and a fixed `width: 1200` (or `$maxContent`) on an inner content frame. Center it with `justifyContent: "center"` and `alignItems: "center"` on the outer.

## Vertical rhythm

Section-to-section gaps follow this scale: `$space-6` (tight), `$space-8` (default), `$space-12` (marketing-page hero).

Within a section, descend by one step: section padding `$space-8` → child gap `$space-6` → grandchild gap `$space-4`. Skipping steps creates visible cliffs.

## Archetype variants

Layout density is one of the strongest archetype signals. The defaults above lean balanced; archetypes tighten or open them up:

- **`saas-apps/b2b/analytics-dashboard`**: medium-dense. Card padding `$space-4` to `$space-5`. Table row padding `$space-2` to `$space-3` vertical. Skip `$space-7` and above unless separating page regions.
- **`saas-apps/b2b/modern-pro-tool`** (Linear-style): dense. Sidebar items `$space-1` to `$space-2` vertical padding. List rows 6–10 vertical. The `$space-5` step matters most. Skip `$space-12` entirely on app surfaces.
- **`marketing-websites/conversion-focused-saas`**: open. Hero padding `$space-12`+ vertical. Section padding `$space-10` to `$space-12`. Card-internal padding `$space-5` to `$space-6`.
- **`marketing-websites/editorial-storytelling`**: most generous. Hero padding 200+ vertical (often custom values above `$space-12`). Content max-width tight at 680–760 for prose.

See `assets/archetypes/<category>/<archetype>.md` for the full bundles.

## When to break the rules

The rules are defaults. Break them when:

- Designing for a specific brand mood (e.g. an editorial layout that needs uneven gutters).
- Following a reference image the user provided.
- The user explicitly asks for a non-rhythm spacing.
- The chosen archetype calls for it (per the variants above).

In those cases, do it intentionally, and tell the user that's what you're doing, so the choice is visible.
