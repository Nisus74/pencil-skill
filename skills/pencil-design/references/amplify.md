# Amplify

When the brief says *"make it bolder"*, *"give it more impact"*, or *"commit harder"*, the model's reflex stack arrives first: cyan-to-purple gradients, glassmorphism, neon accents on near-black, gradient text on hero metrics. These are the AI category-default for *"bolder"* and they're the opposite of bold. They read as more AI, not as more designed.

Amplifying a design means stronger hierarchy, committed scale, decisive typography, one sharper accent applied with intent. Drama through clarity and POV, not drama through accumulated effects. Reject the reflex first; then increase impact.

Use this reference when the design feels too safe, too templated, too quiet for its job. Use it cautiously on product surfaces; *"more impact"* is rarely the right diagnosis for a tool the user lives in for hours.

## Register

On brand surfaces, amplification is permitted to push: extreme scale (96–200px hero type), an unexpected colour committing to 60% of the surface, typographic risk (display serifs paired with grotesque body, condensed widths, distinct stylistic sets), a committed POV that wouldn't survive on a competing brand. Brand can sacrifice some restraint for memorability; the page is allowed to perform.

On product surfaces, amplification rarely means theatrics. Theatrics on a tool undermines trust and slows the user. Product amplification means stronger hierarchy (3:1 size ratios where there's currently 1.5:1), clearer weight contrast (900 + 200 weights where there's currently 600 + 400), one accent committed to one role, denser data with more disciplined spacing rhythm. The work goes into confidence, not drama.

For the per-register depth on what each lane will tolerate, see [brand.md](brand.md) and [product.md](product.md).

## Assess current state

Identify which weakness sources are dragging the design toward *"safe"*:

- **Generic typeface choices.** Inter as a display font is the loudest tell ([typography.md](typography.md) reflex-reject list). System sans without a fallback strategy is the second.
- **Timid scale.** Every heading lives in the 16–32px range; the hero is 28px when it could be 80px. No size jumps cross the 2:1 threshold.
- **Low weight contrast.** Headings at 600, body at 400, no visible weight difference. Or worse, everything at 500 for *"modern"*.
- **Monotone palette.** Five tinted greys plus a hint of accent at 5% surface. Nothing carries the brand at a glance.
- **Predictable composition.** Three balanced columns, centred hero, symmetric padding everywhere. The page reads as a template even before the content lands.
- **Static.** No motion sequencing on entrance, no scroll-anchored reveals, no hover affordances with personality (or hover affordances at all, on brand work).

Run `get_screenshot` on the top-level frame, squint, and ask: *"where does the eye land first?"* If the answer is *"nowhere obvious"*, the design lacks a focal point. That's the most common amplification gap, and it usually outranks any individual fix below.

## Plan

Pick a personality lane and a focal point. Don't try to amplify across every dimension at once; the surface ends up loud rather than confident.

- **Lane:** maximalist (lots of contrast, layered elements, atmospheric backgrounds), elegant drama (extreme type contrast, restrained palette, generous space), playful energy (warm colour, character-rich type, motion-rich), dark moody (committed darkness, single bright accent, atmospheric lighting). Commit to one.
- **Focal point:** which element wins the page? Hero typography, a custom data visualisation, an image, a brand mark treatment. The chosen element gets the dramatic treatment; everything else supports it.
- **Risk budget:** brand work absorbs more risk; product surfaces less. The same amplification applied to both lands very differently.

A direction without a focal point produces *"everything got louder"*, which scans as the same problem in a different costume.

## Apply across dimensions

### Typography

Typography carries more of *"bolder"* than any other axis. A page with the same colour, layout, and motion reads dramatically different on a Söhne Breit + Tiempos pairing than on Inter + Inter.

- Swap generic display fonts for the reach-for list in [typography.md](typography.md): Söhne Breit, GT Sectra, Editorial New, Clash Display, ABC Diatype, Migra. Pick what suits the lane.
- Increase scale jumps. A hero at 80–160px (brand) or 40–56px (product) where currently 28–40px. The leap to the next-down step should be obvious, not subtle.
- Increase weight contrast. Pair 900 with 200 (or 300), not 600 with 400. A 200-weight body next to a 900-weight headline reads as decisive.
- Activate stylistic sets and contextual alternates. Geist `ss01`, Söhne `ss02`. A single alternate set across the design adds visible character at near-zero cost.
- For variable fonts, use the full width axis. A condensed display headline above a regular-width body reads as designed; ignoring the width axis is the default.

### Colour

Move from restrained to committed. The four palette strategies live in [color-and-contrast.md](color-and-contrast.md); amplifying almost always means picking the next-up strategy.

- Pick one dominant colour to own ≥60% of the visible surface. Not 30% (still feels accent-shy), not 80% (too suffocating for most jobs). Commit to 60%.
- Increase saturation toward the brand's full chroma, not toward neon. A green at chroma 0.18 reads as confident; the same green at 0.28 reads as Crypto.
- Harmonise neutrals to the dominant hue. Every grey tinted toward the dominant by chroma 0.005 to 0.01 ([color-and-contrast.md](color-and-contrast.md) tinted-neutrals section).
- Refuse the AI-default gradient set: purple-to-blue, cyan-to-pink, orange-to-magenta. If a gradient is needed, design one with multiple stops in a single hue (a green-to-darker-green or warm-to-cooler within the brand). Most surfaces don't need a gradient.

### Spatial drama

Amplified layouts use space the way restrained layouts use type weight: contrast.

- Hero elements 3x to 5x larger than their supporting elements. A hero KPI rendered at 200px next to a 32px label reads as the page's argument. The same KPI at 80px reads as data.
- Asymmetric layouts on brand surfaces. 70/30 splits, off-centre arrangements, content sitting in the bottom-right of the first viewport. Symmetric balance is the default; asymmetric tension is the choice.
- Generous section gaps. 96–192px between major sections on brand pages. 24–48px gaps that read as fine for product reads as cramped on brand.
- Full-bleed elements where appropriate. The hero image, the atmospheric band, the brand mark moment. Not every element respects the container.
- Intentional overlap. A headline that crosses an image edge; a card that breaches its column gutter. Reads as composed when used once per surface; reads as broken when used five times.

### Effects

Effects support amplification when they're decisive; they undermine it when they're the boldness.

- Dramatic shadows for elevation, but not generic drop-shadows-on-rounded-rectangles. Larger, softer, sometimes coloured (a green shadow under a green CTA rather than `rgba(0,0,0,0.1)`). Use sparingly; one or two elevated surfaces per page, not every card.
- Background treatments that read as deliberate: mesh patterns in the brand palette, noise textures, geometric shapes that echo the brand mark. Avoid glassmorphism (it's the 2023–2024 AI default).
- Borders or frames as decorative elements on brand surfaces. A thick brand-coloured outline on a hero card; a custom-shape frame around a portrait. Product surfaces stay with the system borders.

### Motion

Motion amplifies the design when it's choreographed; it scatters it when every element animates.

- Sequence the hero. Kicker fades in, then headline, then deck, then CTA. Each step 200–300ms with 100–150ms stagger ([motion-design.md](motion-design.md)).
- Scroll-anchored reveals on subsequent sections. Translate of 8–16px plus opacity fade, ease-out-quart, 300–400ms. Reveal once per session; don't replay on scroll-back.
- Hover affordances with personality on brand CTAs. A button that grows by 2–4%, shifts its arrow icon, or reveals secondary copy. Use sparingly; one per page.
- Refuse bouncy and elastic curves on UI controls. Ease-out-quart, ease-out-expo, ease-out-quint carry the modern crispness. Bouncy reads as 2018.

## Never

- **Never reach for cyan-to-purple or purple-to-blue gradients.** They are the AI-default for *"bolder"* and read as more AI within seconds.
- **Never use glassmorphism as the amplification move.** Backdrop-blur surfaces stacked on bright backgrounds read as 2023.
- **Never put gradient fills on metrics.** A KPI number with a gradient fill reads as decoration over confidence; render it in a single committed colour.
- **Never use bouncy or elastic easing on UI controls.** Overshoot motion on buttons and toggles reads as overdone.
- **Never make everything bold at once.** Bold without contrast is no bold. Boldness needs quiet to land against.
- **Never sacrifice body readability.** Display can be loud; body text holds 60–75ch line length, 1.5 line height, real contrast against its surface.
- **Never reach for neon-on-black as a shortcut.** Pure black background with a single neon accent is the Crypto / Web3 cluster ([color-and-contrast.md](color-and-contrast.md) reflex-reject palettes).
- **Never copy a trendy aesthetic blindly.** A bolder Linear, a bolder Vercel, a bolder Stripe is still a derivative. *"More impact"* means distinctive, which means committing to a POV that wouldn't survive being lifted to another brand.

## Verify

After the amplification pass, screenshot the surface again. Run these checks:

- **The AI slop test.** If a stranger looked at the result and said *"AI made this bolder"*, the work is wrong. Amplifying means becoming distinctive, not *"adding more effects"*. Start again if the test fails.
- **The focal point test.** Squint. The first focal point is unmissable. The second is clear. If the eye doesn't know where to land, the amplification scattered.
- **Body legibility.** Body text under 75ch, 1.5 line height, WCAG AA contrast in both light and dark modes.
- **Motion still feels intentional.** Each animation is doing one of the three jobs from [motion-design.md](motion-design.md); none of them are running for personality alone.
- **One dominant colour.** Owns ≥60% of the visible surface; not split across three accents.
- **State matrix intact.** Hover, focus, pressed, disabled states all carry the new boldness; nothing slipped back to the old palette ([states.md](states.md)).

When the result feels right, hand off to [finalise.md](finalise.md) for the alignment, spacing, and token-consistency pass.
