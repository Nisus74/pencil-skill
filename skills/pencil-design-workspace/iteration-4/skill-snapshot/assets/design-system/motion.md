# Motion

How things animate. The agent reads this when adding hover transitions, page transitions, modal entrances, or any micro-interaction. Most AI-generated UIs default to either **dead-static** or **bouncy spring everywhere** — both feel wrong. The decisions below pick a middle path.

## The rule of thumb

Motion communicates **change** (this thing just appeared / disappeared / moved / responded to you). When it communicates anything else (delight, brand personality, "this is a modern app"), it's probably wrong.

If you can remove an animation and the interface still works, remove it.

## Durations

| Variable | ms | Use for |
|----------|----|---------|
| `$durationFast` | 120 | Hover, focus, color shifts, tooltip appear/disappear. |
| `$durationBase` | 200 | Slide-in, fade-in, sheet/popover open, accordion expand. |
| `$durationSlow` | 300 | Modal, full-page transition, drawer. |
| `$durationDeliberate` | 500 | Marketing-only — hero reveal, scroll-triggered moment. Never inside a SaaS app. |

**Rule:** the larger the surface that's moving, the slower the animation. A button hover is 120ms; a full-screen modal is 300ms. A 300ms button hover feels broken; a 120ms modal feels jarring.

## Easings

| Variable | Curve | Use for |
|----------|-------|---------|
| `$easeOut` | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Things entering the screen (modal opens, toast appears). Default. |
| `$easeIn` | `cubic-bezier(0.4, 0.0, 1, 1)` | Things leaving the screen (modal dismisses, toast hides). |
| `$easeInOut` | `cubic-bezier(0.4, 0.0, 0.2, 1)` | Movement *within* the screen (a card sliding to a new position). Rare; usually `$easeOut` is better. |

**Avoid by default:** spring/bounce easings (the `cubic-bezier` overshooting curves). They read as App-Store-demo-video and age fast. Use them only for one specific moment per app — typically a celebratory confirmation — declared explicitly here.

## What to animate

Safe to animate (cheap on the GPU, doesn't trigger layout):

- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (sparingly)
- `background-color` and `color` for small surfaces

Avoid animating:

- `width`, `height`, `top`, `left` — these trigger layout, jank on lower-end devices.
- Background color of large surfaces (whole-page background fades read as "AI loading shimmer," not as intentional motion).
- Anything in a long list (animating 50 cards entering at once = stuttery).

## What *not* to animate at all

- **Text content swaps.** When a label changes (e.g. "Save" → "Saving…"), don't fade the swap. Just swap.
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
| Modal open | Backdrop fade `$durationBase`, modal `transform: scale(0.96 → 1)` + opacity, `$easeOut`. |
| Modal close | Reverse, with `$easeIn`. |
| Toast appear | `transform: translateY(8px → 0)` + opacity, `$durationBase`, `$easeOut`. |
| Accordion expand | Animate height? **No.** Use `grid-template-rows: 0fr → 1fr` trick or just snap. Snapping is acceptable. |
| Page transition (SPA) | Cross-fade content area only, `$durationBase`. Do not animate the chrome (nav, sidebar). |
| Skeleton shimmer | 1.4s linear loop, gradient sweep across `$surfaceMuted`. |

## Brand exceptions

If a marketing page or brand moment uses a deliberately expressive animation — a hero reveal, a scroll-triggered illustration — declare it here, scoped to where it appears. Outside that scope, the defaults above apply.
