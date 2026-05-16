# Soften

Quiet design is harder than loud design. Subtlety needs precision. When a surface is too aggressive, too saturated, too busy, the path through it is to reduce intensity without slipping into generic. Soften badly and the design loses its POV; soften well and the design reads as confident enough to whisper.

Use this reference when the surface is overwhelming, when the user is meant to live inside it for hours, when the brand wants to signal craft through restraint, when a competitor's loud aesthetic needs answering with composure rather than volume.

Soften isn't the opposite of [amplify.md](amplify.md); both are about clarity. Amplifying makes the focal point unmissable; softening makes everything except the focal point recede. They're complementary tools on the same axis.

## Register

On brand surfaces, softening means a more restrained palette, more whitespace, more typographic air. Drama is reduced, not eliminated. The page still has a POV; it just doesn't shout it. Editorial brands and luxury brands live here by default; tech and startup brands often arrive here after they've grown up.

On product surfaces, softening means reducing visual noise. Fewer background accents, flatter cards, less colour, less motion. The tool disappears more completely into the task. A softened product UI is what *"production-grade"* and *"mature"* tend to look like; the loud version was the v1.

For the per-register depth, see [brand.md](brand.md) and [product.md](product.md).

## Assess current state

Run `get_screenshot` and identify which intensity sources are pulling the design toward *"too much"*:

- **Saturation everywhere.** Multiple high-chroma colours competing for the eye. Two accents at the same intensity. Backgrounds that aren't backing down.
- **High contrast where it doesn't matter.** Borders the same weight as the focal element; text the same darkness as headings; every element fighting for the same hierarchy level.
- **Competing visual weight.** Five bold elements on one surface. Three cards at the same elevation; six icons at the same scale; eight buttons at primary weight.
- **Animation excess.** Every element on entrance animates; every hover does something; every state transition has a flourish. The page never settles.
- **Decorative complexity.** Gradients on backgrounds, shadows under cards, patterns behind heroes, illustrations between sections. Each one might be fine alone; together they read as decorated.
- **Scale uniformity at high volume.** Everything is large and loud with no clear hierarchy; the surface presents as a wall.

The diagnostic question: *"if I squint, does the eye know where to land?"* If the answer is *"everywhere at once"*, softening is the right tool. If the answer is *"nowhere"*, the design has a hierarchy problem and softening alone won't fix it (it'll just produce a quieter wall).

## Plan

Decide which approach the softening takes; running all of them at once produces a flat, generic result.

- **Colour approach.** Desaturate the palette, restrict the colour count, or shift the dominant proportion. Pick one.
- **Hierarchy approach.** Decide which elements stay bold (very few; one or two per surface) and which recede. Use weight, size, and space to carry hierarchy instead of colour and chrome.
- **Simplification approach.** Decide what can be removed entirely. Decorative gradients, redundant borders, secondary shadows, illustration that doesn't serve. Cut, don't quiet.
- **Sophistication approach.** Decide how the design signals quality through restraint: typographic discipline, generous whitespace, considered detail, refined motion. Restraint without intent collapses to bland.

The discipline: subtlety requires precision. Quiet without intent reads as unfinished, not as designed.

## Apply across dimensions

### Colour

Reducing colour is where most softening lives.

- Reduce saturation. Shift from full-chroma colours (0.18–0.25) toward 70–85% of full intensity (0.12–0.17). The brand identity holds; the volume drops.
- Soften the palette. Replace bright colours with muted versions of themselves. A bright red at OKLCH(0.6 0.22 25) softens to OKLCH(0.58 0.14 25).
- Reduce colour count. Five named accents collapse to two. The remaining two earn more presence; the cut ones weren't doing work anyway.
- Let neutrals do more work. The 10% accent rule from [color-and-contrast.md](color-and-contrast.md) lives here: accent ≤10% of surface area; neutrals carry the rest.
- Use tinted neutrals, not pure greys. A warm-grey background reads as part of the system; a `#888888` background reads as cold and unattached.
- **Never gray on colour.** If text sits on a coloured background, use a darker or lighter shade of that same hue, or use the text colour at reduced opacity. Gray text on a coloured surface reads as accidental.

### Weight

Visual weight is the second softening axis.

- Reduce font weights. 900 → 600, 700 → 500, 600 → 400. The hierarchy holds because the size and space contrast carry it.
- Replace heavy borders with hairlines or with whitespace. A 2px border softens to 1px; many borders soften to *"no border, increased gap"*. Pencil's gap-over-border discipline supports this.
- Reduce or remove shadows. Hard drop-shadows soften to subtle elevation; subtle elevations soften to *"no shadow, slight background-tone shift"*.
- Increase whitespace. Generous space around an element gives it presence without requiring weight; this is the *"signal hierarchy through space, not chrome"* move.

### Simplification

What can leave the surface entirely.

- Decorative gradients without purpose. Mesh patterns, two-colour background washes, atmospheric overlays. If they're not signalling something, they're cluttering.
- Redundant borders and dividers. The card already has elevation; it doesn't also need a border. The section is already separated by 96px of space; it doesn't also need a divider.
- Secondary illustrations. Spot illustrations between sections, icon-text label pairs where the icon adds nothing the text didn't. Cut.
- Effect layers. Blur on top of shadow on top of gradient on top of tint. Pick the one that's doing work.
- Repeated reinforcement. The hero has the headline; the section heading repeats it; the CTA says it again. The duplication is for emphasis but reads as repetition. Trust the reader.

### Motion

Motion softens by reducing distance, duration, and concurrency.

- Reduce translate distances. 40px reveals soften to 20px; 20px reveals soften to 10px. The motion still confirms; it stops performing.
- Shorter durations on functional motion. State transitions move from 300ms to 200ms; hovers from 200ms to 150ms.
- Remove decorative motion entirely. Hover affordances that bounce; entrance sequences that stagger; idle motion in the background. Cut.
- Refined easing. Ease-out-quart for understated motion; never bounce, never elastic, never overshoot ([motion-design.md](motion-design.md)).
- Use `prefers-reduced-motion` as the design default for product surfaces. The non-reduced version is the indulgent one; reduced is the calm one.

### Composition

The arrangement softens too.

- Reduce scale jumps. 5:1 size ratios soften to 3:1; 3:1 soften to 2:1. The hierarchy survives; the drama drops.
- Bring rogue elements back to grid. The element that escapes the column to add tension also adds noise; if softening is the direction, the tension is what's leaving.
- Even out spacing rhythm. Extreme variations (12px sometimes, 96px other times) collapse toward a single rhythm with smaller variance.

## Never

- **Never make everything the same size or weight.** Soft design still needs hierarchy. Equal-weight surfaces produce flat, lifeless designs.
- **Never strip all colour.** Quiet isn't grayscale. The brand still wants to be recognisable; tinted neutrals plus one restrained accent does the job.
- **Never eliminate personality.** Refinement keeps the voice; it just turns the volume down. The signature moments from [delight.md](delight.md) earn their place even on quiet surfaces; the discipline cuts everything *else*.
- **Never sacrifice usability for aesthetics.** Buttons still need clear affordances; focus rings still need to be visible; touch targets still need to meet the 44px floor.
- **Never make everything small and light.** Some anchors are needed for the eye to land. A surface with no high-contrast moment anywhere reads as drained, not as quiet.
- **Never use gray text on a coloured background.** Always a darker or lighter shade of the colour itself.
- **Never use softening as an excuse to skip the hierarchy work.** A surface that lacks hierarchy will still lack hierarchy after softening; it'll just be quieter about it.

## Verify

After the softening pass, screenshot the surface again. Run these checks:

- **Still functional.** Tasks complete easily; affordances remain clear; the user can find what they need.
- **Still distinctive.** The brand is recognisable; the surface doesn't read as generic. If a stranger said *"this could be any product"*, the softening cut too far.
- **Better for extended reading.** Text reads comfortably for longer; the eye isn't fatigued; the surface doesn't compete with the content.
- **Restrained, not absent.** The POV survives the cuts. The signature moments still land. The page still has a voice.
- **Accessibility intact.** Reducing contrast can break WCAG AA; verify body text still hits 4.5:1, UI elements still hit 3:1 ([accessibility.md](accessibility.md)).
- **One or two anchors remain.** At least one element on the surface still pulls the eye; complete uniformity isn't the goal.

When the result feels right, hand off to [finalise.md](finalise.md) for the alignment, spacing, and token-consistency pass.
