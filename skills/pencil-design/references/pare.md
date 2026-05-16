# Pare

Pare strips a design to its essentials. It removes what doesn't earn its place and lets the remaining elements have more presence per element. Great design is simple, powerful, clean; paring is the work that takes a competent surface to that bar.

Pare isn't [soften.md](soften.md). Soften reduces *intensity*: lower saturation, lighter weights, less motion. Pare reduces *content*: fewer elements, fewer sections, fewer ideas competing on the same surface. A softened design can still be full; a pared design is sparse on purpose.

Use this reference when the surface is busy without being clear, when *"there's a lot going on"* keeps coming up in critique, when the brief grew and the design grew with it, when a Figma comp got built faithfully and the result feels assembled rather than designed.

## Register

On brand surfaces, paring means the page makes one argument. Everything supporting that argument stays; everything else cuts. A pared brand page has a single thesis and three to five supporting moves, not eleven sections of mixed messages. The hero argument is named in one phrase; the page is the proof of that phrase.

On product surfaces, paring means each surface does one job. The job is named and obvious within three seconds. A pared product UI has a clear primary action per view, a clear primary signal, a clear primary affordance; the secondary moves don't disappear, they just don't compete. Settings pages, dashboards, and admin views are where this work has the highest leverage.

For the per-register depth, see [brand.md](brand.md) and [product.md](product.md).

## Assess current state

Before cutting, name the job.

1. **Name the surface's purpose in one sentence.** *"This page exists so a prospect can decide whether to start a trial."* *"This dashboard exists so the operator can see which jobs are stuck."* If the sentence doesn't fit in one breath, the surface is doing too many jobs.
2. **`get_screenshot` the full surface.** Then list every element on it: every section heading, every card, every metric, every illustration, every icon-text pair, every CTA, every microcopy block.
3. **Rate each element on a four-way scale:**
   - **Essential.** The surface fails its job without this.
   - **Supportive.** Adds material to the essential work; pulling it doesn't break the surface but weakens it.
   - **Decorative.** Doesn't move the user toward the surface's job. May look fine, may even add character, but pulls attention without paying it back.
   - **Inherited.** Got built because *"a page like this usually has one"*. Often a section heading, a *"learn more"* card, a redundant CTA, a metadata strip the user doesn't act on.
4. **Decorative and most inherited elements cut.** Essential always stays. Supportive earns case-by-case review.

The output is a punch-list of cuts and a defended core. *"Cut the testimonial carousel, the press logos band, the secondary metric strip, and the bottom feature grid. Keep the hero, the primary feature, the social proof line, and the CTA."*

## Plan

Decide whether the cuts produce a calmer surface or a more impactful one. Both are valid outcomes of paring; they call for different follow-up moves.

- **Cuts produce calm.** The surface ends up sparser; remaining elements get more whitespace, more breathing room, more typographic discipline. Follow up with [soften.md](soften.md) if it isn't already calm enough.
- **Cuts produce impact.** The surface ends up with fewer but louder elements; remaining elements absorb the attention budget the cuts released. Follow up with [amplify.md](amplify.md) if the surviving elements can carry more presence.

A pared design that doesn't land in either direction has cut too much without redistributing the gain; the remaining elements still feel underweight. Pick a direction and let the cuts feed it.

## Apply

### Content

Cut what doesn't move the user toward the surface's job.

- **Decorative sub-headings** that restate the section's title or pad with category labels. The H2 says *"Pricing"*; the H3 says *"Plans"*. The H3 is for SEO or for instinct; it doesn't earn its place.
- **Redundant CTAs.** The hero has *"Start free trial"*; the features section has *"Start free trial"*; the pricing section has *"Start free trial"*; the footer has *"Start free trial"*. Two is enough on most marketing pages; one is enough on most product surfaces.
- **Metadata the user doesn't act on.** *"Created 2024-03-14 by aiko@example.com"* under every list item when only the timestamp matters; the email is data exhaust.
- **Sections built because *"a homepage usually has one"*.** Testimonial carousels with one slot. Logo bands with three logos. Stat strips with rounded fake numbers. If the content isn't earned, cut the section.
- **Filler copy.** *"In today's fast-paced world..."*, *"Whether you're a startup or enterprise..."*, *"Built for teams that ship."* The user's attention is finite; spend it on specifics.

### Components

Many surfaces have three components doing roughly the same job.

- **Collapse three similar cards into one repeated row.** When three feature cards have the same shape, the same icon style, the same copy structure, they're a list. Render them as a list with stronger typography; the cards' chrome was adding visual weight without adding meaning.
- **Remove icon-text pairs where the label does the work.** An icon plus the label *"Settings"* is two visual elements doing one job. The icon-only form works in chrome and toolbars; the label-only form works in body content. Don't pair them out of reflex.
- **Cut dividers that the spacing already provides.** Three sections separated by 96px of vertical space don't also need 1px horizontal lines between them.
- **Cut secondary icons.** Each list item has a leading icon, a trailing chevron, and a status dot. Pick one.

### Hierarchy

Fewer elements means hierarchy tightens.

- **Promote the remaining hero.** With the secondary feature grid gone, the primary feature can carry more weight: a larger headline, a richer description, a full-bleed image, a stronger CTA treatment.
- **Demote everything else into supporting rhythm.** The surviving secondary elements step back, in size and in weight, so the hero owns the focal point.
- **Increase whitespace around the kept elements.** The attention budget freed by the cuts gets redistributed as space, not as more chrome.

### Surface treatment

With less content, the surface can also lose some chrome.

- **Card borders earn less.** With fewer cards, the spacing alone groups them; coloured or hairline borders both become redundant.
- **Shadows step down.** Without the visual density that made elevation legible, lighter shadows or none at all read fine.
- **Section dividers cut.** Generous gaps between sections do the structural work; the lines don't.
- **Background treatments cut.** Atmospheric gradients and patterns were filling space; with less to fill, plain surfaces read as confident.

See [color-and-contrast.md](color-and-contrast.md) for tinted-neutrals as a chrome substitute and [layout.md](layout.md) for the spacing rhythm strategies that work on sparser surfaces.

## Never

- **Never pare the brief away.** The surface still has to do its job. If paring removes content needed to clear the bar, the cuts went too far.
- **Never pare personality away.** Signature moments from [delight.md](delight.md) earn their place; the discipline cuts decoration, not character. A pared surface should still feel like the brand.
- **Never confuse paring with strip-mall minimalism.** Less but better, not less and less. Fewer elements need to mean stronger remaining elements; if the kept elements aren't carrying more presence, paring became erosion.
- **Never remove content needed for accessibility.** Skip links, error messages, screen-reader labels, focus indicators. These count as essential regardless of how minimal the surface looks ([accessibility.md](accessibility.md)).
- **Never confuse paring with softening.** Cutting content is different from reducing intensity. Run them as separate passes; pick one direction per session.
- **Never pare a surface before its hierarchy is settled.** Cuts amplify existing hierarchy; if the hierarchy was wrong, paring locks it in.

## Verify

After the cuts, screenshot the surface again. Run these checks:

- **The job is more obvious.** A first-time visitor can name the surface's purpose in one sentence within three seconds.
- **Nothing supports decoration alone.** Every element on the surface is doing essential or supportive work; the decorative and inherited cuts have left.
- **The remaining elements have more presence per element.** Each kept item carries more visual weight than before, or more whitespace around it, or both.
- **The user knows where to look first.** Squint test ([layout.md](layout.md)) passes; the focal point is unambiguous.
- **Accessibility is intact.** Cuts didn't take skip links, error states, or focus indicators with them.
- **The personality survives.** A stranger looking at the surface should still recognise it as the brand; if the cuts erased the voice, restore one or two signature elements before declaring done.

When the result feels right, hand off to [finalise.md](finalise.md) for the alignment, spacing, and token-consistency pass.
