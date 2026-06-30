# Layout

Layout is the substrate of every design. Done with intent, it disappears: the user finds what they need, the eye moves through the surface in the order the design wants, the rhythm matches the content. Done by reflex, it produces the same balanced-card grid on every screen and reads as machine-generated regardless of how the rest of the design is treated.

This reference is the depth behind the responsive breakpoint table in SKILL.md and the density guidance in [product.md](product.md). Use it when the design feels *"templated"*, *"flat"*, *"all the same"*, or *"missing something"*; those are layout-rhythm signals.

## Grids and what they're for

A grid is a coordination tool. Its job is to make decisions you'd otherwise have to re-make on every screen. *"Page padding is 64px."* *"Body content max-width is 1200."* *"Column gutter is 24."* These constants free attention for the work that actually requires it.

### When grids help
- Pages with content from multiple sources (cards, blocks, columns) where alignment matters across boundaries.
- Multi-column layouts where the column gutter should match the page padding rhythm.
- Surfaces a team will extend over time; the grid gives the next contributor a defaults to work against.

### When grids hurt
- Forcing every element into a 12-column structure when the content doesn't want that shape.
- Treating the grid as a layout truth rather than a defaults framework. The grid is the starting point; not every element has to honour it.
- Hand-tuning to fit a strict 8px or 4px scale on every value (font sizes, line heights, icon sizes); the surface ends up over-systematic and stiff.

### The 4pt / 8pt baseline
Most design systems sit on a 4pt or 8pt base. Spacing values are multiples (4, 8, 12, 16, 24, 32, 48, 64, 96). The base unit creates rhythm; outliers (a 22px gap, a 7px padding) read as accidental unless they're deliberate.

The discipline is in *picking* a base and *staying* in it. Mixing 4pt and 8pt across the same surface is the most common subtle layout error.

### Semantic spacing tokens
Name spacing tokens by their relationship, not their literal value. `$spaceSm`, `$spaceMd`, `$spaceLg` survive a scale change; `$spacing8`, `$spacing16`, `$spacing24` lock the values in and require renames when the system shifts. The same logic applies to font sizes (`$textSm` over `$text14`), radii (`$radiusMd` over `$radius8`), and elevation (`$shadowLg` over `$shadow24`).

For sibling spacing, prefer `gap` on the parent's auto-layout over per-child `margin`. Pencil's `gap` eliminates the margin-collapse and double-spacing failures that surface when adjacent elements both claim their own margins.

## Spatial rhythm

Spacing is half of layout. The same components arranged with different spacing read as different designs.

### Vary spacing deliberately
The fastest layout failure: same padding everywhere. 16px between every element produces a wall of even rhythm that reads as monotonous. A surface that breathes asymmetrically (40px before a section heading, 12px between cards inside the section, 24px between cards across sections) reads as composed.

Pick a rhythm strategy per surface:

- **Tight-then-airy:** sections pack their content; the gap between sections is large.
- **Crescendo:** vertical spacing grows down the page (tight at the top, expansive at the bottom).
- **Asymmetric:** some sections breathe, others compress, decided by content weight.
- **Pulse:** alternate dense and airy sections deliberately.

Decide a rhythm in step 2 (aesthetic direction) and apply it; don't let *"reasonable defaults"* converge every surface to balanced-everywhere.

### The squint test
Squint at the layout. The eye should land on a deliberate first focal point, then move through the surface in a clear order. If squinting reveals an even field of grey rectangles with no obvious entry point, the layout has no hierarchy.

If the squint test fails, the fix is rarely *"more colour"* or *"a bigger heading."* It's usually *"more spacing variance"* and *"more weight contrast."* See [typography.md](typography.md) on weight contrast and [cognitive-load.md](cognitive-load.md) on hierarchy as a cognitive scaffolding move.

### Hierarchy through multiple dimensions

When the squint test fails, the fix is usually layered. Strong hierarchy combines two or three of these dimensions on the same element; weak hierarchy relies on one of them alone.

| Dimension | Strong hierarchy | Weak hierarchy |
|---|---|---|
| Size | 3:1 ratio or more | Less than 2:1 ratio |
| Weight | Bold versus Regular (900 paired with 300) | Medium versus Regular (500 paired with 400) |
| Colour | High-contrast accent against neutrals | Two similar tones |
| Position | Top-left or geometric focal point | Bottom-right or buried mid-page |
| Space | Generous whitespace around the element | Tight padding everywhere |

A heading that's larger, bolder, AND has more space above it carries unambiguous hierarchy. A heading that's only larger reads as *"the design got the type ratio right"*, which isn't the same as *"this is the thing to look at first."* Pick two or three dimensions per focal point; the others stay quiet.

## Register-specific spatial strategy

### Brand
Brand layouts tolerate wide whitespace and dramatic spacing decisions. The vertical rhythm IS part of the brand expression.

- **Long-form vertical scroll** as default; columns are an editorial choice, not a default.
- **Hero gets disproportionate space** (often 60–80% of the first viewport).
- **Section padding 96–192px** between major sections (yes, that much).
- **Edge-bleed content** at hero, image, or atmospheric moments. Not everything respects the container.
- **Asymmetric grids** are fine. Brand can use 60/40 splits, off-centre arrangements, content sitting in the bottom-right of a screen.

### Product
Product layouts are denser and more disciplined. Spacing is functional and consistent within a surface.

- **Predictable grid** (typically 12-column at desktop) with consistent gutters.
- **Section padding 32–64px** between major regions; row padding 4–16px depending on density.
- **Predictable content max-width** so the user's eye knows where to look across the whole product.
- **Strict edges.** Content respects the container; full-bleed is rare in product UI.
- **Symmetric grids** by default; asymmetric only when there's a structural reason (a sidebar vs main content split).

### Mixed surfaces
Marketing-style pages embedded in a product (an onboarding splash, an upgrade prompt) should lean toward the brand spatial register; the product surrounding them keeps its discipline.

## Layout patterns that work

### The single-column long-form
The simplest, most under-used pattern. One column, content stacked, generous whitespace. Works for blog posts, manifesto pages, documentation, settings pages, mobile-first product surfaces.

Why it's under-used: the model defaults to *"add visual interest"* by splitting columns. A single column with strong typography and rhythm often outperforms a clever multi-column.

### The sidebar + main
Standard product chrome. Sidebar for navigation; main for content. The trap: making the sidebar too wide, too dense, or visually competing with the main area.

Sidebar guidance:
- Width 240–280px on desktop; collapsible to icon-only at 56–64px.
- Visually quieter than main content (lower text contrast, no decorative chrome).
- Single-level by default; second-level navigation lives in the main area or in a per-section nav, not stacked inside the sidebar.

### The dashboard grid
A grid of metric-cards, charts, and tables. The trap: making every cell the same size, which compounds into the *"identical card grid"* anti-pattern banned in SKILL.md.

Dashboard guidance:
- Differentiate card sizes by what they hold (a sparkline is 1×1; a chart is 2×2; a primary KPI is 1×2 with the number doing the visual work).
- Reserve the top-left for the most important content; the user's eye starts there.
- Don't fill empty cells with low-value content; let the grid breathe.

### The split-screen
Two columns of roughly equal weight, often used for forms (form on left, value-prop on right) or comparisons.

Split-screen guidance:
- Each side has a clear job (one is action, the other is context).
- Don't compete: if both sides have hero treatments, neither wins.
- Mobile collapses to stacked; the design ships the stacked version on mobile, not a shrunken split.

### The bento grid
Mixed-size cards arranged in a grid (popularised by Apple, now over-saturated). Refuse as the default product page (per [brand.md](brand.md)); use intentionally when the content actually varies in importance and shape.

### Cards as a layout choice
Cards are overused. Spacing, alignment, and typography create visual grouping naturally; reaching for cards every time a group needs to be distinct produces the *"identical card grid"* aesthetic that reads as templated.

Cards earn their place in three situations:

- The content is genuinely distinct and actionable; each card is a tappable target.
- Items need direct visual comparison in a grid; pricing tiers, plan options, dashboard metrics with shared shape.
- The content needs a clear interaction boundary; a drag-and-drop target, a hoverable preview surface.

When none of those apply, render the group as a list with stronger typography or as separated sections with rhythm. Cards-by-reflex is a fast way to make a brand page feel like a generic product page.

**Never nest cards inside cards.** The SKILL.md ban exists because the layout pattern is unsalvageable; if you find yourself reaching for a nested card, the outer card probably shouldn't have been a card to begin with. Use spacing, typography, and subtle dividers for hierarchy within a card instead.

## Working with breakpoints

The SKILL.md responsive table covers the canonical breakpoints (Mobile 390, Tablet 768, Desktop 1440). Layout decisions per breakpoint:

### Mobile (390 wide)
- Single column always; multi-column is almost never right at this size.
- Sticky navigation at the top OR bottom, not both.
- Touch targets ≥44px (per [accessibility.md](accessibility.md)).
- Content margin 16–24px from the viewport edges.

### Tablet (768 wide)
- Two-column is now an option; three is usually too dense.
- Navigation can stay sticky or expand inline.
- Touch targets still ≥44px; the device is touch-primary.
- Content margin 32px from edges; respect a 704 max-width.

### Desktop (1440 wide)
- Multi-column is comfortable; three-to-four columns work for content grids.
- Navigation can expand to a full sidebar.
- Touch targets can drop to 32px for dense desktop UIs (per density call).
- Content margin 120px from edges; respect a 1200 max-width.

### Beyond desktop
For very wide viewports (1920+), the design should NOT keep stretching. Either:
- Cap content at 1200 (or whatever max-width the brand uses) and let the wings breathe.
- Add a third column of supporting content (right-rail navigation, related content).
- Increase font size and line spacing rather than line length; long lines harm reading.

## Touch targets

Mouse pointers have pixel precision; fingers don't. A 24px button works on desktop and reads as broken on mobile. The 44x44px floor from [accessibility.md](accessibility.md) applies wherever touch is plausible.

The Pencil pattern: keep the visual icon at its natural size and expand the tap target via a sibling frame with `fill: "transparent"`:

```
Update("<iconButton>", { width: 24, height: 24 })
T1 = Insert("iconButton", { type: "frame", x: -10, y: -10, width: 44, height: 44, fill: "transparent", role: "button" })
```

Apply at minimum to:

- Icon-only buttons in toolbars and toasts
- Chevrons on expandable rows
- Toggle switches and small checkboxes
- Close buttons on modals and banners
- Tab targets in dense navigation

The visual element stays small; the tap target gets enough surface area to land. Inconsistent tap targets (some elements 44, some 24) read as bugs on mobile.

Touch-target adherence on desktop is also worth aiming for. Mouse users with low-precision pointing (older users, users with motor difficulties, users on a touchpad) benefit from the extra surface area too.

## Optical adjustments

The pixel grid is precise; the eye isn't. A handful of common adjustments compensate:

- **Icon centring.** Geometric centring of triangles, arrows, and other asymmetric glyphs reads off-centre. A play-triangle shifts right by 1–2px; an arrow shifts toward its direction by 1–2px; a chevron centres on its visual midpoint, not its bounding box.
- **Text optical alignment at container edges.** Body text starting at `x: 0` looks indented because letterform whitespace pushes the visual edge inward. For display-sized text against a container edge, apply a negative offset (roughly -0.05em in pixel terms; for a 64px headline that's about -3px).
- **Vertical text centring in buttons.** Button labels are usually optically centred slightly higher than the geometric centre because of the baseline. If a button looks bottom-heavy, nudge the label up by 1px.
- **Hanging punctuation.** Quote marks, dashes, and similar punctuation pulled into the margin for pull-quotes and editorial layouts. Reserve for editorial; not for product UI.

These adjustments are small per element and visible in aggregate. The surface ends up reading as *"someone cared"* rather than as *"the grid was followed."*

## Layout anti-patterns

In addition to the bans in SKILL.md, layout has its own:

- **Same vertical padding everywhere.** Reads as templated.
- **Cards inside cards.** Banned in SKILL.md; the layout failure that drives it is using cards as the only grouping mechanism.
- **Three-column equal-card grid as the default for "features."** Banned in SKILL.md; the layout failure is reaching for the same grid shape on every page.
- **Sidebar that doubles the main content's chrome.** Bordered, shadowed, with its own header. Sidebar should be calmer than main.
- **Centred-everything in product UIs.** Centred page titles, centred body, centred forms. Reads as marketing-leaked-into-product.
- **Edge-to-edge full-bleed content in product surfaces.** Brand can full-bleed; product surfaces benefit from contained content with predictable margins.
- **A container around every section.** The page becomes a stack of identically-shaped boxes. Most things don't need a container.
- **Aspect-ratio mismatches in image grids.** Images cropped to fit a uniform grid without thought to subject placement. The grid wins; the images suffer.
- **Hidden side-effects of CSS grid.** A 12-column grid auto-fitting elements that end up with awkward 5-of-12 widths because no one decided. Pick spans deliberately.

## Pencil-specific

### Auto-layout vs absolute positioning
Pencil auto-layout (flex direction `row`/`column` on frames) is the right default for most layouts. Use absolute positioning only when content genuinely floats (popovers, overlays, decorative elements).

The discipline: every frame has a deliberate `layoutMode`. *"Auto-layout because the children stack"* is a non-decision; *"horizontal auto-layout with 24px gap because columns"* is a decision.

### Padding and gap discipline
Use the canonical 4/8 multiples (4, 8, 12, 16, 24, 32, 48, 64, 96). When a value doesn't fit (a 7px or 22px gap to make something align), the alignment is fighting the system; usually the fix is upstream.

Padding takes a number, `[h, v]`, or `[t, r, b, l]`. The object form `{ top: N }` is rejected (see [batch-design-grammar.md](batch-design-grammar.md)). Stay consistent with the project's chosen form across the file.

### Constraints and resizing
For per-breakpoint frames, each frame has its own layout; constraints are mostly irrelevant. For single fluid frames, set children to `width: "fill_container"` or `width: "fit_content"` thoughtfully. *"Don't bind both width and height to `fill_container` on a child unless the parent's auto-layout direction supports it."*

### Test under realistic content volume
A grid that looks rhythmic with three cards in design will look different with thirty. A table that looks airy with five rows will look different with five hundred. Build at least one frame with realistic content volume before declaring the layout done. See [cognitive-load.md](cognitive-load.md) on the populated-state verification rule.

### Use `FindEmptySpace` for crowded boards
When the canvas already has multiple top-level frames, call `FindEmptySpace` (a JS function inside `batch_design`, returns `{x, y, parentId?}`) before placing a new one. Skipping this on a crowded canvas produces invisible overlaps that look like rendering failures.

### Snapshot the layout for debugging
When a screenshot reveals that *"something looks off"* but the issue isn't obvious, call `snapshot_layout({ parentId, maxDepth: 2 })` to read positions, sizes, and gaps as numbers. Often the issue is one rogue padding value that fights the rhythm.
