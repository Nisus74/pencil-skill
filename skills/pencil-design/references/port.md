# Port

Port is the cross-context pass. Desktop to mobile, light to dark, default to high-contrast, English to German, mouse to touch. The design holds together across the variation, makes the same argument on a phone that it makes on a 27-inch monitor, stays readable when the user has bumped their contrast preferences up.

Use this reference when the design was built at one size and one mode and now needs to live in the rest of the matrix. Port is distinct from [fortify.md](fortify.md): fortify handles failure states (404, 500, offline, error); port handles successful but varied conditions (mobile, dark, RTL, high-contrast). Often they're done in the same session; they're separate passes because the work is different.

## Register

On brand surfaces, port means the page makes the same argument at 320px, 768px, and 1920px. The hero scales; the rhythm holds; the typography re-tunes to its mobile scale. Brand pages can absorb a near-redesign at mobile (different image, different copy length, different rhythm) because brand performance is allowed.

On product surfaces, port means the surface does the same job on phone, tablet, and desktop. The chrome changes (sidebar collapses to a drawer; toolbars stack; tables become cards) but the job stays consistent. Product surfaces favour reflow over redesign; the same component library serves both.

For per-register depth on responsive behaviour, see [brand.md](brand.md) and [product.md](product.md). For breakpoints and grid systems, see [layout.md](layout.md).

## Assess current state

Before mutating, list the variation matrix the design has to survive.

1. **Breakpoints declared.** Which breakpoints exist? The standard four are 320 (small mobile), 768 (tablet), 1280 (desktop), 1920 (wide). Some products add 1024 (small desktop) and/or 1440. Check `get_variables` for declared breakpoint tokens.
2. **Theme axes declared.** Run `get_variables` to see which theme axes are live. `mode` (light/dark) is usually present; `density` (compact/comfortable/spacious) and `state` (default/hover/focus/etc) may or may not be.
3. **Screenshots at each axis.** Run `get_screenshot` on the top-level frame, once per breakpoint, once per mode. For a design with light + dark and four breakpoints, that's eight screenshots. Inspect each one for failures.
4. **i18n stress.** What does the layout do with realistic German or Hungarian copy? RTL flip behaves?
5. **`prefers-*` adaptation.** Is there a designed fallback for `prefers-reduced-motion`? For `prefers-contrast`? For `prefers-reduced-transparency`?

Output of assessment is a per-axis punch-list. *"Hero copy at 320 wraps awkwardly to four lines; dark mode borders disappear on row dividers; RTL flip leaves the arrow icon pointing the wrong way; reduced-motion fallback isn't designed."*

## Plan

Decide for each surface whether the mobile (or otherwise non-default) version is a *reflow* or a *redesign*.

- **Reflow.** Same components, same content, different arrangement. The sidebar becomes a drawer; the two-column grid stacks; the table rows wrap. Product surfaces usually reflow.
- **Redesign.** Different components or different content per breakpoint. The marketing hero on mobile uses a different image, a shorter headline, a portrait crop; the desktop hero uses a wide image with side copy. Brand surfaces often redesign for mobile.

Mixing reflow and redesign on the same surface is fine; pick per-element. The chrome reflows; the hero redesigns.

The discipline: a *responsive* design that's just a single column with `display: none` on the desktop columns isn't ported; it's hidden. The mobile experience deserves to be designed, not pruned.

## Apply across dimensions

### Breakpoint behaviour

Pencil's responsive model: declare breakpoint tokens via `SetVariables` (inside `batch_design`), then bind frames to those tokens via `width: "fill_container(max-WIDTHpx)"` patterns. The standard four work for most products:

```
SetVariables({
  "bpSm": { mode: { light: "320px", dark: "320px" } },
  "bpMd": { mode: { light: "768px", dark: "768px" } },
  "bpLg": { mode: { light: "1280px", dark: "1280px" } },
  "bpXl": { mode: { light: "1920px", dark: "1920px" } }
})
```

Design at the smallest breakpoint first and expand. Mobile-first sizing avoids the common failure of *"designed at desktop, broken at mobile"*. The reverse is rarer: designs that work at mobile tend to expand cleanly to desktop.

Single-column reflow is the safe default. Multi-column layouts only when the content benefits (a directory of items, a multi-pane editor, a side-by-side comparison).

See [layout.md](layout.md) for the working layout patterns at each breakpoint.

### Touch targets

Touch interactions need a 44x44px minimum target. Mouse interactions can use smaller hit areas. The mobile port is where this rule lands.

Pencil supports the *"visual icon, larger tap target"* pattern via a sibling frame:

```
Update("<iconButton>", { width: 24, height: 24 })
T1 = Insert("iconButton", { type: "frame", x: -10, y: -10, width: 44, height: 44, fill: "transparent", role: "button" })
```

Apply at minimum to:
- Icon-only buttons in toolbars
- Close buttons on modals and toasts
- Chevrons on expandable rows
- Toggle switches and checkboxes (the visual element can stay 16–20px; the tap target expands)

### Type scale

The modular scale used at desktop is too large on mobile. Drop the top end of the scale, not the bottom.

- Desktop hero: 64–160px. Mobile hero: 32–48px.
- Desktop section heading: 32–48px. Mobile section heading: 24–32px.
- Body, captions, microcopy: stay at the same size or one step smaller; readability ceiling matters more than scale rhythm at body size.

Don't scale linearly; pick a tighter ratio for mobile (1.2 minor third instead of 1.25 major third). The breakpoints carry the scale ratio, not just the hero size.

See [typography.md](typography.md) for the modular-scale guidance.

### Mode adaptation

Every colour variable carries both light and dark values from declaration (SKILL.md discipline rule, depth in [color-and-contrast.md](color-and-contrast.md)).

Port the design under both modes from the same `.pen` file:

- Declare the `mode` theme axis on the document root via `SetVariables` (inside `batch_design`) with themed values.
- For per-frame mode-specific rendering: `Update("<frameId>", { theme: { mode: "dark" } })`. Use this for screenshots and for surfaces that should always render in a specific mode (a dark hero on a brand site that lives inside a light product).
- Inspect both modes for the common dark-mode failures listed in [color-and-contrast.md](color-and-contrast.md): borders that disappear, accents that glow, body text that's too white, missing line-height bump on light-on-dark.

### Density adaptation

If the product has compact / comfortable / spacious modes (Linear's density toggle, Notion's spacing options), declare it as a theme axis:

```
SetVariables({
  "density": { value: "comfortable", themes: { density: ["compact", "comfortable", "spacious"] } },
  "rowPadding": { mode: { density: { compact: 4, comfortable: 8, spacious: 16 } } },
  "rowGap": { mode: { density: { compact: 2, comfortable: 4, spacious: 8 } } }
})
```

Then frames reference `$rowPadding` and `$rowGap`; switching density becomes a single theme update. Most products don't need this; products that do usually need it across the whole surface, not just one component.

### i18n

Test the layout with realistic non-English content. The two stress tests:

- **Length expansion.** German runs 30–50% longer than English. Hungarian, Finnish, and Polish similar. Replace dummy text with a real translation sample for one screenshot per surface; verify the layout absorbs the expansion without breaking.
- **RTL flip.** Hebrew and Arabic flip the entire layout horizontally. Pencil supports this via the `direction` property on frames. Render the surface in RTL for at least one screenshot per major view; check that icons pointing left or right got flipped, controls reversed, alignment held.

Cross-link [accessibility.md](accessibility.md) § i18n and RTL for the deeper coverage.

### `prefers-*` adaptation

Honour the user-level preferences across the port.

- **`prefers-reduced-motion`.** Designed fallbacks replace expressive durations with zero. Track via a `motionPreference` theme axis or via the `prefersReducedMotion` variable in motion tokens. See [motion-design.md](motion-design.md) § Reduced motion.
- **`prefers-contrast`.** Bump body text contrast above WCAG AA (4.5:1) toward AAA (7:1); thicken borders; remove low-contrast decorative elements. A `contrastPreference` theme axis may be worth declaring on contrast-critical surfaces.
- **`prefers-reduced-transparency`.** Replace glassmorphism or backdrop-blur with solid surfaces. If the design uses backdrop-blur (refused elsewhere in this skill), at least design the solid fallback.

## Never

- **Never use desktop typography sizes on mobile.** A 96px hero on a 320px viewport dominates the surface; drop the top of the scale.
- **Never declare a `mode` theme without testing both modes.** Light-only or dark-only designs ship as broken in the other mode; verify before declaring done.
- **Never declare a design responsive without screenshotting 320 and 1920.** *"It looks fine"* on a single viewport doesn't clear the bar.
- **Never use hover-only affordances on mobile.** Touch has no hover state; an interaction that requires hover to discover is invisible on mobile.
- **Never ship a design with `display: none` mobile state.** The content is needed somewhere; hidden content fails accessibility and likely user-need too.
- **Never confuse port with redesign.** Port is one design rendered across conditions; redesign is multiple designs for different conditions. Pick per-element.
- **Never assume the user's device pointer.** Touch and mouse coexist on tablets and 2-in-1s; affordances should work for either.

## Verify

Screenshot the surface across the matrix:

- **Breakpoints.** Screenshots at 320, 768, 1280, 1920 all hold the design's intent.
- **Modes.** Light and dark both pass WCAG AA contrast in every state matrix entry.
- **Touch targets.** Every interactive element on mobile meets 44x44px minimum.
- **i18n.** At least one screenshot with realistic non-English content; RTL has been checked.
- **`prefers-*`.** Reduced-motion fallback exists; high-contrast still meets contrast targets; reduced-transparency has solid equivalents.
- **No hover-only affordances.** Every important interaction has a non-hover path.
- **No `display: none` mobile state.** Every element on desktop has a mobile location, even if the visual treatment differs.

When the result feels right, hand off to [finalise.md](finalise.md) for the alignment, spacing, and token-consistency pass.
