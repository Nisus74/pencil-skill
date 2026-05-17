# Micro-interactions

How each specific interaction animates. The agent reads this file when wiring a button hover, a modal open, a toast, a drag gesture, or any other moment where the UI responds to a user. It extends `motion.md`: that file holds the timing tokens (`$durationFast`, `$durationBase`, `$durationSlow`); this file maps real interactions to those tokens, with easing and state-by-state choreography.

Fill in the values during scaffolding. Each row is a project commitment, so once it's set, the agent uses it everywhere that interaction appears.

## Per-interaction specs

| Interaction | Duration | Easing | Properties | Notes |
|---|---|---|---|---|
| Button press (primary) | `$durationFast` (~120ms) | `ease-out` | `transform: scale(0.98)`, fill slightly darker | Restores instantly on release. |
| Button hover | `$durationBase` (~200ms) | `ease-out` | `fill`, `transform: translateY(-1px)` | Gated behind `@media (hover: hover)` so taps don't stick. |
| Card hover | `$durationBase` (~200ms) | `ease-out` | `transform: translateY(-2px)`, deeper shadow | Don't apply on touch. |
| Modal open | `$durationBase` (~250ms) | `ease-out` | `opacity 0 → 1`, `transform: scale(0.96 → 1)` | Backdrop fades in over the same duration. |
| Modal close | `$durationFast` (~150ms) | `ease-in` | Reverse | Faster on close than open, the user's already moved on. |
| Sheet (mobile) open | `$durationBase` (~300ms) | spring `cubic-bezier(0.32, 0.72, 0, 1)` | `transform: translateY(100% → 0)` | Native iOS sheet feel. |
| Sheet drag-to-dismiss | continuous | none, follows finger | `transform: translateY` | Snap to nearest detent on release. |
| Toast in | `$durationBase` (~250ms) | `ease-out` | `opacity 0 → 1`, `transform: translateY(20px → 0)` | |
| Toast out | `$durationFast` (~200ms) | `ease-in` | Reverse | After dismiss timer (~5s) or click. |
| Page transition | `$durationBase` (~300ms) | `ease-in-out` | `opacity` cross-fade | View Transitions API where supported. |
| Tab switch | `$durationFast` (~150ms) | `ease-out` | `opacity` cross-fade | Avoid layout shift on switch. |
| Tooltip appear | `$durationFast` (~100ms) after `200ms` delay | `ease-out` | `opacity 0 → 1` | Delay prevents flash on accidental hover. |
| Skeleton shimmer | infinite | `linear` | `background-position` | 1.4s loop, per `motion.md`. |
| Progress bar | duration of operation | `linear` | `width: 0 → 100%` | Indeterminate uses a 1s loop. |
| Focus ring appear | `$durationFast` (~100ms) | `ease-out` | `outline-color`, `outline-offset` | Instant feel preferred. |
| Form field error appear | `$durationFast` (~150ms) | `ease-out` | `opacity 0 → 1`, `transform: translateY(-4px → 0)` | Subtle shake on submit-with-errors. |
| Optimistic UI commit | instant | none | UI updates first | Subtle fade if rollback. |
| Optimistic UI rollback | `$durationBase` (~200ms) | `ease-in-out` | Reverse | Toast appears explaining the failure. |

## Reduced-motion contract

When `prefers-reduced-motion: reduce` is set:

- Disable transform-based animations (translate, scale).
- Replace cross-fades with instant changes.
- Keep colour transitions, they've got low motion impact and the affordance still reads.
- Disable parallax, autoplaying video, and infinite loops (skeleton shimmer included; swap for a static muted fill).

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Test with the OS setting toggled on. Don't trust DevTools emulation alone, the real preference can behave differently in some browsers.

## Animation library

The project uses `<library: Framer Motion | React Transition Group | hand-rolled CSS | View Transitions API | none, native CSS only>`. State the choice once. Every interaction in the table above resolves to that library's API, so the rest of the project doesn't drift between approaches.

If a particular interaction needs a different library (say, a complex gesture handled by `react-use-gesture`), document the exception inline in the row's Notes column.

## When the spec doesn't cover an interaction

If you're wiring something the table doesn't list, pick the closest analogue and reuse its timing. A new "popover open" inherits from "tooltip appear". A "drawer slide" inherits from "modal open". Then add a row to the table so the next agent doesn't have to make the same call twice.

Don't invent a new duration. The four tokens in `motion.md` cover every reasonable case, and adding a fifth quietly fragments the system.

## GPU-only properties

Animate only `transform` and `opacity` for performance. Avoid `width`, `height`, `top`, `left`, `margin`, and `padding` in animations because they trigger layout and jank on lower-end devices.

For colour transitions, `background-color` and `color` are fine, they composite cheaply when no other properties change in the same frame.

## Don't animate

Some moments shouldn't animate at all:

- Loading spinners during the show-delay window (under 150ms feels broken, the spinner appears and vanishes before the eye registers it).
- Layout changes that move content the user is reading or interacting with.
- Anything during keyboard input, the user's mid-thought and motion competes with their attention.
- Anything that runs without a user trigger. No autoplay, no idle ambient motion in product surfaces.
- Numbers ticking up or text crossfades on label swaps. Just swap the value.

## Choreography rules

When two interactions overlap, the agent follows these defaults so the page doesn't feel chaotic:

- **One thing moves at a time.** If a modal's opening, the toast waits 100ms before sliding in.
- **Backdrops match their content.** A modal backdrop fades in over the same `$durationBase` as the modal itself, not faster, not slower.
- **Exit is faster than entry.** Closing a modal at `$durationFast` after opening at `$durationBase` feels right because the user's already moved on.
- **Stagger lists, don't burst.** When a list of cards animates in, offset each by ~30ms. Cap the total stagger at 200ms so the last item isn't still arriving when the user starts scanning.

## Testing micro-interactions

Each interaction gets verified in the browser with the actual easing and duration. Don't approve animations from screenshots, the timing is the design. A 200ms ease-out and a 200ms ease-in-out look identical in a still frame and feel completely different in motion.

If you can't decide between two timings, ship the faster one. Users notice slow more than fast.

Record interactions at 60fps when reviewing with a designer; phone screen-recording is fine. Loom and QuickTime both capture transition frames cleanly enough to debug timing.

## See also

- `motion.md`: the timing tokens this file references (`$durationFast`, `$durationBase`, `$durationSlow`) and the easing variables.
- `tokens.md`: durations live as tokens alongside spacing, colour, and type.
- `references/modern-patterns.md` (in the pencil-design skill): § Animation & motion timing tables, plus the GPU-only and never-`transition: all` rules.
- `references/interactions.md` (in the pencil-design skill): § Loading states, the show-delay and min-visible-time windows referenced above.
- `references/accessibility.md` (in the pencil-design skill): `prefers-reduced-motion` patterns.
- View Transitions API spec: https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API
