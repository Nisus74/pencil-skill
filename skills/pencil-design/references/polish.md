# Polish

Polish is the final pass before shipping. It isn't personality (that's [delight.md](delight.md)) and it isn't directional refinement (that's [bolder.md](bolder.md), [quieter.md](quieter.md), [distill.md](distill.md)). Polish is the alignment, spacing-consistency, and detail-coherence pass that catches the small things that read as accidental: the orphan 22px gap, the icon that's geometrically centred but optically left-leaning, the one card that has shadow-md when its siblings have shadow-sm, the heading that lost its tabular figures along the way.

Skipping polish is how a competent design ships looking *"close, but"*. The work in this pass is small per item and large in aggregate; the cumulative drift between a design's first build and its shipping state is what polish reels back in.

This reference is the handoff target for the other scaffold refs. Every bolder, quieter, distill, or harden pass ends by suggesting polish. After polish, the design is ready for the SKILL.md step-6 completeness rubric.

## Register

Brand polish leans on rhythm and atmosphere. The headline group has the rhythm it set out to have; the section padding flexes around content weight; the hero image bleeds where it should bleed and respects the container where it shouldn't. Polish on a brand surface is about restoring composition after the design has accumulated edits.

Product polish leans on alignment grids and token-consistency. Every spacing value resolves to the chosen scale; every colour resolves to a variable; every shadow steps on the elevation scale; every text node uses tabular figures where numbers stack. Polish on a product surface is about restoring system-coherence after the design has accumulated overrides.

Both registers share the discipline: polish doesn't add ideas. If a new idea surfaces during polish, write it down and run the appropriate refinement scaffold first.

## Assess current state

Before mutating, build a complete picture of what needs polishing.

1. **Screenshot the surface in both modes.** Run `get_screenshot` on the top-level frame, once with `theme.mode: "light"` and once with `dark`. Many polish issues only show up in one mode (border that disappears in dark, shadow that overpowers in light, accent that glows in dark).
2. **Run the squint test.** Per [layout.md](layout.md), squint at the surface and check whether the first focal point and the second focal point are obvious. If they aren't, polish won't fix it; the design needs hierarchy work upstream.
3. **Sweep for raw literals.** Call `search_all_unique_properties({ property: "fill" })`. Any returned hex string that doesn't start with `$` is a token-discipline failure. Repeat for `fontFamily`, `border`, and shadow tokens.
4. **List orphan spacing values.** Pencil's auto-layout `gap` and `padding` properties surface every spacing value in the design. Anything off the 4pt scale (22, 7, 33, 18) is a candidate to reel in.
5. **Check the state matrix.** For every interactive component, confirm hover, focus, pressed, and disabled all share alignment, share token resolution, and step on the same elevation scale (see [interaction-design.md](interaction-design.md)).

The output of assessment is a punch-list, not an opinion. *"Three orphan spacing values, two raw hex fills, one icon optically off-centre, one shadow inconsistent with its sibling cards, dark mode border on row dividers disappears."*

## Plan the polish

Pick one of three modes per surface and commit to it. Don't run all three at once; the surface gets edited in three competing directions and the result feels rushed.

- **Alignment-and-rhythm polish.** The surface's spacing, alignment, and optical centring are off. The token system might already be clean; the issue is execution.
- **Token-and-consistency polish.** The system is mostly applied but with overrides; one card has a literal hex, one button uses a raw shadow value, one font-family is named instead of variable-bound. Bulk-fix via `replace_all_matching_properties`.
- **Detail-coherence polish.** Borders, shadows, radii, icon weights drift between components that should match. Bring them onto a shared scale.

For most surfaces, one mode is dominant; the others get a single pass after. If all three modes need substantial work, the design isn't ready for polish; it's still in build.

## Apply the polish

### Alignment

Every element snaps to the chosen grid. Pencil's auto-layout handles most of this; the failures are usually in the few elements that escape the layout (absolutely-positioned overlays, floating action buttons, hero typography that pokes out of containers).

- Check optical centring on icons. Geometric centring of triangles and asymmetric glyphs reads off-centre; a play-triangle shifts right by 1–2px, an arrow shifts toward its direction.
- Check text optical alignment at container edges. Body text at `x: 0` looks indented because of the letterform whitespace on the first character. Apply a negative offset (roughly -0.05em equivalent in pixel space) on display-size text against a container edge.
- Confirm that anything intentionally off-grid has a reason. A 22px gap because *"it looked right"* is drift; a 22px gap because the design uses a 1.1 ratio scale starting at 20 is system.

### Spacing

Replace orphan values with on-scale equivalents. The 4pt scale (4, 8, 12, 16, 24, 32, 48, 64, 96) covers most cases; the 8pt scale (8, 16, 24, 32, 48, 64, 96, 128) is a subset.

For each orphan: was the goal *"slightly more than 16"* (use 20 or 24) or *"slightly less than 32"* (use 28 or 24)? Pick the nearest scale value and commit. The visible difference of 2–4px is rarely worth the system cost.

### Token consistency

The discipline rule from SKILL.md: every colour, font-family, motion duration, and elevation resolves to a variable. Polish is where that rule gets enforced.

- For each raw hex returned by `search_all_unique_properties`, identify the role it's playing (background, border, text, accent) and migrate it to the matching variable. Use `replace_all_matching_properties` for bulk fixes when the same hex maps to one variable.
- For each named font-family, confirm it's bound to `$fontDisplay`, `$fontBody`, or `$fontMono`. Switching fonts later becomes a single variable update; otherwise it's a sweep.
- For each shadow, confirm the value steps on the elevation scale (`$shadowSm`, `$shadowMd`, `$shadowLg`). If two components use different shadows for the same elevation role, pick one and migrate.

### Detail coherence

Walk the surface and ask: *"do these elements feel like they came from the same hand?"*

- Border radii consistent within a component family. Buttons all at `$radiusMd`; cards all at `$radiusLg`; pills all at `$radiusFull`. A button at `$radiusSm` next to one at `$radiusMd` reads as accidental.
- Icon weights consistent. Mixing 1.5px stroke icons with 2px stroke icons within the same toolbar reads as imported-from-two-libraries.
- Type rhythm holds. Body line length under 75ch; light-on-dark text has the line-height bump applied ([typography.md](typography.md)); every numeric column uses tabular figures.
- Motion timings step on the token scale. Hover transitions all at `$durationFast`; panel transitions all at `$durationMedium`; nothing at a literal `180ms`.

## Verify

Screenshot both modes again. The polished surface should pass these:

- Squint test passes (first and second focal points are unambiguous).
- No raw hex, no raw font-family, no raw motion duration remaining.
- All spacing on the chosen scale; no orphan values left.
- Border radii, icon weights, shadows coherent across the component family.
- Light and dark both pass WCAG AA contrast targets ([accessibility.md](accessibility.md)).
- The state matrix is complete and consistent across components ([states.md](states.md)).
- No new ideas got introduced during polish.

If a check fails, fix it before declaring done. *"Mostly polished"* isn't polished.

## Never

- **Never call a design polished without re-screenshotting both modes.** Polish in light without a dark-mode check is the most common false-done.
- **Never polish before the direction is settled.** Polishing a design that's about to be substantially restructured is wasted work; finish the bolder / quieter / distill pass first.
- **Never let token-consistency become an excuse to skip alignment.** A perfectly tokenised design with optical drift still feels accidental.
- **Never introduce new content during polish.** A new section, a new component, a new copy block is a different pass.
- **Never declare polish done without checking the state matrix.** A button's default state is polished; its disabled state still has the raw hex from the early build.
- **Never use polish as a cover for missing work.** If the design needs error states, polish doesn't fix that; it needs [harden.md](harden.md) first.
- **Never run all three polish modes at once.** Pick one; the others follow as a single sweep after.

## Closing

Polish is the universal handoff target for the other scaffold refs. Bolder, quieter, distill, harden, clarify, adapt, and optimize all end with a polish pass. After polish, run the SKILL.md step-6 completeness rubric (Heuristics, States, Flows, Accessibility, Design completeness). Then the design is ready to ship.
