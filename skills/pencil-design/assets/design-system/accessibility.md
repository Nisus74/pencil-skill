# Accessibility

The project's accessibility commitments. The agent reads this file at session start to know which compliance level the project ships against and what every component owes the keyboard and the screen reader. Without it, the agent guesses, and the bar drifts down session by session.

## Compliance level

The project commits to: `<WCAG 2.2 AA | WCAG 2.2 AAA | APCA Lc 75 body / Lc 60 large | hybrid (WCAG 2.2 AA + APCA Lc 75)>`.

The hybrid commitment is the modern recommendation. WCAG 2.2 AA covers the legal floor that auditors and procurement teams check against. APCA covers what actually reads well on modern displays for users of every age and acuity, and it'll catch contrast failures that AA quietly passes (mid-grey text on a slightly lighter background, for instance).

## Contrast verification

How the project verifies contrast: `<Stark plugin | APCA contrast checker at https://www.myndex.com/APCA/ | Chrome DevTools accessibility audit | axe DevTools>`.

Every text and background pair gets verified in both light and dark modes before the design ships. A pair that passes in one mode often fails in the other. The verification runs on the *rendered* colour (after opacity, after blending against the parent surface), since that's what the user actually sees.

## Keyboard navigation

- Tab order matches DOM order. If a visual reorder is needed (e.g. a card grid), the DOM gets reordered to match.
- Focus ring: `<colour token, e.g. $focusRing>`, `<width, e.g. 2px>`, `<offset, e.g. 2px>`. Always visible. Don't ship `outline: none` without an alternative ring.
- Skip link: `<present | absent>`. Lands on `<main content area, e.g. #main>`.
- Focus traps: modals, sheets, and command palettes use focus traps. Focus restores to the trigger element on dismissal.

## Keyboard shortcuts

The project's specific shortcuts (fill in for your app):

- `⌘+K`: open command palette.
- `⌘+/`: toggle keyboard shortcut reference.
- `⌘+,`: settings.
- `Esc`: close modal, sheet, or popover.
- `<your shortcut>`: `<what it does>`.

Discoverable via the `?` key, which opens the shortcut reference. Shortcuts shouldn't conflict with browser or OS reserved combinations (e.g. `⌘+W`, `⌘+T`, `⌘+Q`). When there's a conflict, the project's shortcut yields.

## Screen reader patterns

- ARIA live regions: `role="status"` for non-urgent updates (saved, copied to clipboard); `role="alert"` for urgent ones (validation errors, network failures).
- Form errors: every input gets `aria-describedby` pointing at its error message. On invalid submit, an error count gets announced via a live region and focus moves to the first invalid input.
- Dynamic content updates announce via live regions. A search results count, a notification, a toast: each gets announced.
- Decorative icons: `aria-hidden="true"`. Meaningful icons: `aria-label` or a visible adjacent label. Icon-only buttons always carry an accessible name.

## Motion accessibility

`prefers-reduced-motion` is honoured throughout. When the user has it set: parallax disables, auto-playing video disables, and animation durations drop to 0ms or near-instant. See `motion.md` for the project's motion timing tokens; the reduced-motion path overrides them.

Vestibular triggers (large parallax shifts, fast spinning, repeated zooms) are gated behind the reduced-motion check even when they're aesthetically central to a page.

## Dynamic type

`<supports dynamic type | does not support>`.

iOS and Android: respect platform Dynamic Type settings. Web: honour the user's font-size preference. Don't lock body text to a fixed pixel size; use `rem` units so the user's browser default scales the layout. Test the layout at 200% zoom: text reflows, nothing gets clipped, no horizontal scrollbar appears on a 1280px viewport.

## Internationalisation and RTL

`<supports RTL | does not yet support>`.

Logical CSS properties (`margin-inline-start`, `padding-inline-end`, `border-inline-end`) replace left and right where supported. Layouts mirror in RTL: navigation, icon orientation, progress direction, all of it. Numbers and dates respect locale formatting. Translatable strings get pulled out of the JSX into the locale catalogue so the layout doesn't break when German doubles the string length.

## Tested with

The assistive-tech matrix the project tests against:

- macOS Safari + VoiceOver: `<every release | spot-checked>`.
- iOS Safari + VoiceOver: `<every release | spot-checked>`.
- Windows Chrome + NVDA: `<every release | spot-checked>`.
- Windows Edge + Narrator: `<every release | spot-checked>`.
- Android Chrome + TalkBack: `<every release | spot-checked>`.

Untested combinations get flagged in the release notes so users on those stacks know what hasn't been verified.

## Per-component accessibility commitments

A starter table. Extend it as the component library grows.

| Component | Accessibility requirements |
|---|---|
| Buttons | Visible focus ring. Accessible label even on icon-only buttons. Disabled state communicates why via `aria-describedby`. |
| Forms | Every input has a visible label. Error feedback inline. Focus moves to the first error on invalid submit. Required fields marked with both `*` and `aria-required="true"`. |
| Modals | Focus trap active. Focus returns to the trigger on dismiss. Esc closes. Backdrop click closes only if the modal carries no unsaved state. |
| Tabs | Arrow keys move between tabs, Enter or Space activates. `aria-selected` reflects the active tab. Tab key leaves the tab strip. |
| Menus | Arrow keys navigate items, Esc closes, Tab leaves the menu. Submenus open on `ArrowRight`, close on `ArrowLeft`. |
| Tooltips | Trigger on focus *and* hover. Don't carry information that isn't available elsewhere. |
| Toasts | Auto-dismiss timer pauses on hover and focus. Dismissable manually. Announced via `role="status"` or `role="alert"` based on urgency. |

(Fill in the table for the project's components.)

## Verification checklist

Before declaring a design done:

1. Tab through every interactive element. Focus stays visible. Order matches the visual order.
2. Run axe DevTools or the equivalent. Zero violations.
3. Test with a screen reader (VoiceOver on macOS, NVDA on Windows). Every action announces.
4. Verify colour contrast for every text and background pair using APCA Lc 75 (or WCAG 4.5:1 for AA).
5. Set `prefers-reduced-motion` and verify animations respect it.
6. Test the keyboard-only flow for every primary task. There aren't any mouse-only affordances.
7. Zoom to 200% in the browser. Layout reflows. No horizontal scroll, no clipped controls.
8. Run the screen at 50% brightness in a sunlit window. Anything that disappears flags a contrast problem the verifier missed.

## See also

- `references/accessibility.md` (in the pencil-design skill): the full accessibility reference covering ARIA, focus, screen readers, APCA, and WCAG 2.2.
- `tokens.md`: the focus ring token and the colour contrast tokens.
- `motion.md`: the project's motion timing tokens and the reduced-motion path.
- WCAG 2.2 standard: https://www.w3.org/TR/WCAG22/
- APCA contrast checker: https://www.myndex.com/APCA/
