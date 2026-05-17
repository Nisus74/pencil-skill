# Motion design

Motion is a design surface. Done with intent, it confirms what just happened, maintains spatial continuity, expresses brand personality. Done by reflex, it irritates, distracts, or signals AI default. Most generated motion lands in the second bucket because the model defaults to *"add some animation"* without naming what each animation is doing.

This reference is the depth behind the motion bullets in [brand.md](brand.md), [product.md](product.md), and SKILL.md's negative-space defaults. Use it when planning motion on any surface and when auditing an existing design's motion choices.

## What motion is for

Three legitimate jobs. Every animation in a design should be doing one of these. If you can't name which, cut it.

1. **Spatial continuity.** A panel that slides in from the right rather than appearing instantly tells the user *"this is the same surface, just expanded."* The motion preserves the user's mental model of where things are.
2. **State confirmation.** A button that briefly inverts colour on press tells the user *"the click registered."* The motion confirms what just happened.
3. **Expressive personality.** A brand-page sequence that orchestrates copy in over 1200ms tells the user *"this brand cares about craft."* The motion carries personality.

Failure modes from each:
- **Spatial continuity overdone:** every state change is animated, even ones the user didn't initiate; the surface feels never-still.
- **State confirmation overdone:** every micro-interaction has a flourish; the surface feels twitchy.
- **Expressive personality applied to product:** a brand-style page-load sequence on an admin tool; the user is trying to work and the design is performing.

## Easing fundamentals

Easing curves shape how a motion feels. The same 200ms transition reads as snappy, mechanical, bouncy, or sluggish depending on the curve.

### Five curves, five characters

| Curve | Character | Use for |
|---|---|---|
| Linear | Mechanical, unnatural | Almost never (one exception: continuous progress like a spinner) |
| Ease-out (quadratic, cubic) | Settled, decisive | Default for most UI transitions |
| Ease-out (quart, quint, expo) | Crisp, modern | Snappier UI; brand-page reveals |
| Ease-in-out | Symmetric, hand-off | Layout transitions, cross-fades |
| Spring / overshoot | Playful, organic | Sparingly; brand contexts only |

The default for product UI: ease-out with a moderate exponent (cubic or quart). It feels *"settled"*: fast at the start, decelerates into place. The eye reads it as confident.

### Curves to refuse by default

- **Linear easing on transitions.** Mechanical; reads as broken.
- **Bouncy / elastic / spring on UI controls.** A button that overshoots and settles back reads as overdone in 2026. Reserve for genuinely playful brand contexts.
- **Ease-in (no ease-out).** Starts slow, ends fast. Reads as accelerating into a wall.
- **Cubic-bezier curves copied from CSS galleries.** Pick from the table above; resist the *"smooth springy easing"* you found on a Codepen.

## Duration

Match duration to what's happening on screen.

| What | Duration | Notes |
|---|---|---|
| Press confirmation (button, tap) | ≤16ms (one frame) | Any later reads as broken |
| Hover state transition | 100–150ms | Quick enough to feel responsive |
| Focus ring appearance | 0ms (instant) | Focus rings should never animate in |
| Toggle, checkbox, switch | 150–250ms | Long enough to register |
| Panel open / accordion | 200–300ms | Spatial continuity needs time to read |
| Modal in | 200–250ms | Quick; modal already disrupts attention |
| Modal out | 150–200ms | Faster than in; the user committed to dismissing |
| Page route transition | 200–400ms | If used at all; many products skip these |
| Brand hero reveal sequence | 600–1200ms | Each step in the sequence, not the total |

The default failure: 500ms transitions on everything. Slow enough to notice; not slow enough to be a feature. Tighten product UI motion toward 150–250ms; expand brand motion when the choreography earns the time.

## Register-specific motion

### Brand motion
Brand can be choreographed. The page-load sequence is part of the brand expression.

- **Sequence the hero.** Kicker fades in, then headline, then deck, then CTA. Each step 200–300ms with 100–150ms stagger between steps.
- **Scroll-anchored reveals.** Sections fade in with a small upward translate (8–16px). Reveal once; don't replay on scroll-back.
- **Atmospheric loops.** A background video or subtle continuous motion in the hero. Keep it slow enough not to compete with content.
- **Expressive hover affordances on CTAs.** A CTA can grow, shift, reveal a secondary element. The hover state has more room to express than in product.

### Scroll-anchored staggering
When a section reveals on scroll-into-view, the children inside the section can stagger their entrance for a layered effect. Each child gets 200–300ms with 50–100ms stagger between steps; the eye reads the cascade as composition without it feeling choreographed.

Discipline:

- **Three to five steps is the working ceiling.** Beyond that, the reveal reads as performance rather than as content arriving.
- **One reveal per session.** The intersection observer fires once; scrolling back doesn't replay. Replays read as restless.
- **Stagger by visual order, not DOM order.** The headline arrives before the supporting copy regardless of which sits first in the source.
- **Pair with ease-out-quart.** The crisp deceleration matches the choreographed entrance better than ease-out-cubic or ease-in-out.
- **Cap the translate distance.** 8–16px reveal translate; larger distances read as marketing flourish, which is fine on a hero and noisy on a third-fold section.

### Product motion
Product motion is functional, not expressive. Every animation is doing one of the three jobs above; nothing is for show.

- **Instant feedback on input.** Anything ≤16ms reads as instant; anything 30ms+ reads as laggy.
- **Tight state transitions.** Hover, focus, selection all in the 150–250ms range with ease-out.
- **Spatial transitions for layout shifts.** Panel expansion, accordion open, sidebar collapse. 200–300ms ease-out. The motion confirms *"this surface just rearranged itself; here's where things went."*
- **Skeleton loading over spinners.** For content that takes >300ms to load, show shaped placeholders (text-line skeletons matching the line height of the loaded content). Reserve spinners for indeterminate post-action waits.
- **No idle motion.** A product surface at rest doesn't animate. Continuous background motion on idle product UIs reads as restless.

## Motion in dark mode

Dark mode amplifies motion. A bright element appearing on a dark surface is more visually loud than the same element on a light surface. Two adjustments:

- **Shorter durations for state confirmations.** A hover transition that reads as crisp in light mode reads as flashing in dark mode. Trim 25–50ms from product UI durations under dark mode; the eye's contrast-sensitivity behaviour compresses perceived duration on dark surfaces.
- **Reduce opacity flashes.** A modal that fades in from 0 to 1 opacity is fine in light mode; in dark mode it briefly creates a bright flash. Fade from 0 to 0.95 or use the dark-surface tint as the start state.

## Reduced motion

A meaningful percentage of users have motion sensitivity (vestibular disorders, attention regulation). They've enabled `prefers-reduced-motion`. The design honours this:

- Replace translate-based reveals with simple fades or with no transition at all.
- Disable parallax entirely.
- Shorten or eliminate page-route transitions.
- Keep state confirmations (button press, focus appearance); these are functional, not expressive, and removing them harms feedback.

Pencil tokens can carry motion preferences as variables (`$transitionFast`, `$transitionMedium`, `$transitionExpressive`); the `prefers-reduced-motion` branch sets all expressive durations to zero while leaving functional ones intact.

## Motion intensity reduction

When toning a design's motion down (often during a [soften.md](soften.md) pass), apply these recipes consistently across the surface. Half-reductions read as inconsistent; commit to the full pass.

- **Cut translate distances by half.** 40px reveals soften to 20px; 20px reveals soften to 10px. The motion still confirms; it stops performing.
- **Shift easing toward ease-out-quart.** Less character than ease-out-expo or ease-out-quint; reads as understated. Refuse ease-in-out, bounce, and elastic across the board.
- **Reduce durations by 25–40%.** A 300ms transition softens to 200ms; a 200ms transition softens to 150ms. The motion is shorter and lands sooner.
- **Remove decorative motion entirely.** Hover affordances that grow elements, bouncy CTAs, idle loops, scroll parallax. Keep functional motion (state transitions, panel reveals); cut everything else.
- **Document the original intent in `context` strings.** When engineering reads the design, the `context` should still say what the un-softened motion would have done so they can dial it back up if the soften pass overcorrects.

The softened motion still earns the three jobs above (continuity, confirmation, personality); it just runs quieter.

## Anti-patterns

In addition to the bans in SKILL.md, motion has its own:

- **Animated everything.** Cards that slide in on page load, buttons that pulse on hover, icons that rotate when you click them. The page never settles; the user can't focus.
- **Parallax on long pages.** A 2010s holdover. Mostly distracting; rarely earns the spatial complexity it adds.
- **Scroll-jacking.** Hijacking the user's scroll to drive a forced narrative. The user owns the scroll.
- **Loading spinners on near-instant operations.** A spinner that flashes for 80ms reads as broken. Either skip the loading state or commit to skeletons that hold for the full duration.
- **Bouncy/elastic curves on UI controls.** Overdone in 2026; reads dated.
- **Hover effects that change layout.** A card that scales up on hover and pushes its neighbours; a button that grows and shifts the line below. Layout that moves on hover is visually noisy.
- **Continuous loops everywhere.** Looped animations should be rare. One subtle background motion in the hero is fine; ten elements all looping at different rhythms is a video game cabinet.

## Pencil-specific

### Pencil's motion vocabulary
Pencil designs are static representations of UI; the design file doesn't author the actual animation runtime, but the choices you record influence how the design hands off.

Use the `interaction` property on nodes to document expected state transitions (hover, focus, pressed). Use named `context` strings on motion-bearing nodes (*"Section reveals with 200ms ease-out fade plus 8px translate on viewport intersection"*) so the engineer implementing the design knows what was intended.

For prototyping motion in Pencil, build the start and end states as sibling frames with a `transition` annotation in the parent's `context`. Don't try to fake the motion itself in the design file.

### Motion tokens via `set_variables`
Declare motion tokens once so duration and easing apply globally:

```
set_variables({
  "durationFast": { mode: { light: "150ms", dark: "120ms" } },
  "durationMedium": { mode: { light: "250ms", dark: "200ms" } },
  "easeOut": { mode: { light: "cubic-bezier(0.16, 1, 0.3, 1)" } }
})
```

Note the dark-mode durations are slightly shorter per the dark-mode motion rule above. Components and state transitions then reference these tokens rather than literal values.

### When motion design enters the loop
For most Pencil design tasks, motion is recorded in `context` strings and handed off to engineering. Two cases call for explicit motion design:

1. **Brand hero sequences.** Build each step of the sequence as a separate frame so the choreography is visible.
2. **Loading and skeleton states.** Build the loading frame as a sibling of the loaded frame. The transition between them is the motion design.

For most product UIs, the motion design is a one-sentence intent in `context` plus the tokens. The engineer implements; the design records.

### Verify motion choices against the registered intent
At step 6 of the SKILL.md workflow, when running the distinctiveness checklist, also ask: *does the motion direction match what was stated in step 2?* A direction that called for *"crisp, technical, no flourish"* and produced a design with bouncy hovers contradicts itself. Fix the motion intent in `context` strings to match the direction.
