# Motion

How things animate. The agent reads this when adding hover transitions, page transitions, modal entrances, or any micro-interaction. Most AI-generated UIs default to either **dead-static** or **bouncy spring everywhere**, both feel wrong. The decisions below pick a middle path.

The *Motion personality by archetype* section near the end maps each shipped archetype to its motion strategy.

## The rule of thumb

Motion communicates **change** (this thing just appeared / disappeared / moved / responded to you). When it communicates anything else (delight, brand personality, "this is a modern app"), it's probably wrong.

If you can remove an animation and the interface still works, remove it.

## Durations

| Variable | ms | Use for |
|----------|----|---------|
| `$durationFast` | 120 | Hover, focus, colour shifts, tooltip appear/disappear. |
| `$durationBase` | 200 | Slide-in, fade-in, sheet/popover open, accordion expand. |
| `$durationSlow` | 300 | Modal, full-page transition, drawer. |
| `$durationDeliberate` | 500 | Marketing-only, hero reveal, scroll-triggered moment. Never inside a SaaS app. |

**Rule:** the larger the surface that's moving, the slower the animation. A button hover is 120ms; a full-screen modal is 300ms. A 300ms button hover feels broken; a 120ms modal feels jarring.

## Easings

| Variable | Curve | Use for |
|----------|-------|---------|
| `$easeOut` | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Things entering the screen (modal opens, toast appears). Default. |
| `$easeIn` | `cubic-bezier(0.4, 0.0, 1, 1)` | Things leaving the screen (modal dismisses, toast hides). |
| `$easeInOut` | `cubic-bezier(0.4, 0.0, 0.2, 1)` | Movement *within* the screen (a card sliding to a new position). Rare; usually `$easeOut` is better. |

**Avoid by default:** spring/bounce easings (the `cubic-bezier` overshooting curves). They read as App-Store-demo-video and age fast. Use them only for one specific moment per app, typically a celebratory confirmation, declared explicitly here.

## What to animate

Safe to animate (cheap on the GPU, doesn't trigger layout):

- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (sparingly)
- `background-color` and `color` for small surfaces

Avoid animating:

- `width`, `height`, `top`, `left`, these trigger layout, jank on lower-end devices.
- Background colour of large surfaces (whole-page background fades read as "AI loading shimmer," not as intentional motion).
- Anything in a long list (animating 50 cards entering at once = stuttery).

## What *not* to animate at all

- **Text content swaps.** When a label changes (e.g. "Save" to "Saving…"), don't fade the swap. Just swap.
- **Numbers ticking up.** A counter animating from 0 to 1,234 is a marketing-page pattern; in a SaaS dashboard it's noise.
- **Layout reflows on first paint.** If the page lays itself out visibly during load, the skeleton is wrong, not the missing animation.
- **Hover effects on touch devices.** Use `@media (hover: hover)` so taps don't get sticky :hover state.

## Looping animations

The only looping animation that ships by default is **skeleton shimmer** (a soft gradient cycling across loading placeholders, ~1.4s per cycle). Everything else loops only when explicitly opted in (e.g. a brand-page background motif).

Loading spinners: prefer a single 1s rotation over an indeterminate progress bar; both are fine.

## `prefers-reduced-motion`

Respect it. When the user has reduced-motion preference enabled:

- Replace transitions > 200ms with instant changes.
- Disable looping animations except the skeleton shimmer (replace shimmer with a static muted fill).
- Keep micro-interactions ≤ 120ms (these don't trigger reduced-motion sensitivities).

In code:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Common applications

| Interaction | Recipe |
|------------|--------|
| Button hover | `$durationFast`, `$easeOut`, animate `background-color` and `transform: translateY(-1px)`. |
| Button press | Instant on press (no transition); `$durationFast` on release. |
| Modal open | Backdrop fade `$durationBase`, modal `transform: scale(0.96 to 1)` + opacity, `$easeOut`. |
| Modal close | Reverse, with `$easeIn`. |
| Toast appear | `transform: translateY(8px to 0)` + opacity, `$durationBase`, `$easeOut`. |
| Accordion expand | Animate height? **No.** Use `grid-template-rows: 0fr to 1fr` trick or just snap. Snapping is acceptable. |
| Page transition (SPA) | Cross-fade content area only, `$durationBase`. Do not animate the chrome (nav, sidebar). |
| Skeleton shimmer | 1.4s linear loop, gradient sweep across `$surfaceMuted`. |

## Motion personality by archetype

Different archetypes call for different motion characters. Pick the row that matches your chosen archetype; the table above gives you the *building blocks*, this table gives you the *strategy*.

| Archetype | Motion personality | Specifics |
|---|---|---|
| `saas-apps/b2b/analytics-dashboard` | **Instant.** No animations on data updates. | Numbers just change. Charts redraw without count-up animation that delays comprehension. Allowed: 120–160ms ease-out on hover, dropdown opens, tooltip reveals. Anti-cue: count-up KPI animations, chart line tracing on entry, sparkline pulse. |
| `saas-apps/b2b/modern-pro-tool` (Linear) | **Fast, snappy, confident.** | Sidebar item hover: 80–120ms ease-out background fade. Page transitions: 150ms slide. Modal opens: 180ms scale-up from 0.96 with overlay fade. Optimistic updates everywhere; the UI commits before the server confirms. Anti-cue: bouncy springs, long fade-ins, ambient continuous animation, parallax. |
| `marketing-websites/conversion-focused-saas` | **Purposeful.** | Hero headline reveals on scroll (subtle slide + opacity 200–300ms). Section transitions use staggered fades. Product screenshot carousels rotate every 4–6 seconds. Avoid: parallax backgrounds, continuous particle motion, infinite-scrolling logos that strobe. Hover affordances quick (120–160ms). |
| `marketing-websites/editorial-storytelling` (cinematic flavour) | **Cinematic, slow, deliberate.** | Long fade-in reveals (400–600ms ease-out), parallax background shifts, product imagery scaling up as the user scrolls into it. Earns slow because the content rewards patience. |
| `marketing-websites/editorial-storytelling` (manifesto flavour) | **Restrained.** | Short fade-ups on scroll (200–300ms), nothing flashy. The text does the work. |

**What generic looks like (don't ship this):** spring-bounce on every hover, count-up animations on KPI values when the page loads, ambient parallax background shapes, "shake" animation on errors, success confetti everywhere, every transition at 300ms regardless of context.

## Brand exceptions

If a marketing page or brand moment uses a deliberately expressive animation, a hero reveal, a scroll-triggered illustration, declare it here, scoped to where it appears. Outside that scope, the defaults above apply.
