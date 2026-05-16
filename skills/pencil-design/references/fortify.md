# Fortify

Fortify is the production-readiness pass. The happy path is done; this work makes the design survive contact with reality. Long copy, missing images, slow networks, error responses, screen sizes the model didn't think of, languages where words run twice as long, users who turned reduced-motion on. Skipping fortify is the single biggest gap in AI-generated design and the most common reason a Pencil comp falls apart in engineering.

Use this reference once the design's direction is settled and the primary surfaces are built. Don't fortify a design that's still being shaped; the work compounds against changes upstream.

## Register

On brand surfaces, fortifying means the page survives at 320px, when images fail to load, when a user has reduced-motion or high-contrast set, when copy gets translated, when content gets longer than the comp assumed. The argument the page makes shouldn't depend on any of these conditions to land.

On product surfaces, fortifying means the full state matrix per component (default, hover, focus, pressed, disabled, loading, error, selected, read-only) and the screen-level fault states (404, 403, 500, 503, 408, 429, offline, partial-failure). It also means realistic content: long names, no names, missing avatars, rows with zero data, rows with extreme data. *"Plausible content"* is the bar; Lorem Ipsum doesn't clear it.

For the full state taxonomy and fault-state catalogue, see [states.md](states.md). For the cross-screen behaviour (modals vs pages, validation timing, back-stack), see [flows.md](flows.md). This reference is the *pass* that runs both checklists; those references are the catalogues.

## Assess current state

For each interactive node, ask: *"which states does this ship today?"* Most AI-generated designs ship default-only on every interactive node; that's the first gap.

For each surface, ask: *"which screen-level fault states apply?"* A logged-in surface needs at minimum 500 and offline; a public surface needs 404 and 500; an action-driven surface needs error and confirmation states for the action.

For each text block, ask: *"what happens at 2x length and 0.5x length?"* The German translation of a six-word English headline often runs to twelve words; truncation and reflow both have to be handled.

For each image, ask: *"what shows if this fails to load?"* The hero image without a fallback is a blank section; the avatar without an initial is an empty circle.

For each motion sequence, ask: *"what does `prefers-reduced-motion` render?"* A page-load orchestration that requires motion to land its message fails for the user who turned motion off.

Output of assessment is a gap inventory. *"Buttons ship default and hover only; cards ship default only; no error state on the form; no 404 frame; the hero copy at 2x length wraps awkwardly; the avatar shows a blank circle on missing image; the entrance sequence has no reduced-motion fallback."*

## Plan

Prioritise the gaps. Some are higher-leverage than others.

1. **State matrix on interactive components.** A button without a disabled state, a form without an error state, a card without a loading skeleton: these are the highest-impact gaps. Most are 30–60 minutes of work each and prevent the most common shipping failures.
2. **Screen-level fault states.** 404 and 500 at minimum. Offline if the product needs it. Empty-state per the taxonomy in [states.md](states.md) (first-use vs no-results vs no-permission vs post-action).
3. **Overflow handling.** Long copy, long names, content stretching outside the comp's assumed bounds.
4. **i18n.** Realistic non-English content; RTL flip for at least one screenshot.
5. **`prefers-*` media queries.** Reduced-motion fallback; high-contrast support; reduced-transparency fallback (no glassmorphism shortcuts).
6. **Realistic content.** No Lorem Ipsum; no *"User Name"* placeholders; plausible long and short instances of every text field.

Decide which gaps ship now and which get deferred with a written justification. *"Deferred"* without justification reads as forgotten.

## Apply

### Component states

For every interactive node, build the states it ships. The two structural options in Pencil:

- **Sibling frames inside a `reusable` component.** One frame per state, named clearly (*"default"*, *"hover"*, *"pressed"*, *"disabled"*, *"loading"*, *"error"*).
- **State theme axis.** Declare `state` as a theme axis via `set_variables` and render the same component frame under different `state` values. Useful when many components share the same state tokens.

Both approaches are documented in [states.md](states.md); pick one per component family and stay in it.

Build, at minimum, every state named in the user's brief plus the defaults from [interaction-design.md](interaction-design.md):

- Buttons: default, hover, focus-visible, pressed, disabled, loading
- Inputs: default, hover, focus, filled, error, disabled, read-only
- Cards as targets: default, hover, focus, pressed, selected, disabled
- Toggles: default, focus, on, off, disabled, loading
- Links: default, hover, focus-visible, visited (if shown), active

### Screen-level fault states

Build the frames the user will land on when things break. The catalogue lives in [states.md](states.md) § Screen-level fault states.

- **404 / not-found.** *"This page isn't here. The link might have moved. [Back to dashboard]"*. Plus the navigation chrome so the user can recover.
- **500 / internal-error.** *"Something broke on our end. We've logged it; you don't need to do anything. [Refresh]"*. Plus a status-page link if the product has one.
- **503 / unavailable.** *"We're working on it. Try again in a few minutes."* Plus expected duration if known.
- **Offline.** *"You're offline. Your changes are saved locally; we'll sync when you reconnect."*. Plus the offline-actions available.
- **Partial-failure.** *"Loaded 24 of 30 jobs. The other 6 hit a timeout; retry?"*. Plus a retry-only-failed affordance.
- **No-permission / 403.** *"This is locked to workspace owners. Ask Aiko for access."*. Plus the path to escalate.
- **Rate-limited / 429.** *"You've hit the request limit. Try again in 47 seconds."*. Plus the time remaining, dynamic.

Each one is a real frame with the page chrome that lets the user act. *"Sorry, something went wrong"* on a blank page doesn't clear the bar.

### Overflow

Test every text block at 2x length and 0.5x length.

- **Headlines:** wrap to two or three lines without breaking layout. If the comp has a fixed-height container, switch to a min-height or auto-height.
- **Body text:** flows naturally; line-clamps where shown explicitly; expandable where critical content might get truncated.
- **Buttons:** wider to fit longer labels (German), or wrap to two lines, or truncate with explicit affordance (*"View full label"*). Avoid hard-coded button widths.
- **List items:** support long names without breaking the row; long descriptions truncate with ellipsis plus tooltip or expand.
- **Numbers:** support 6-figure and 8-figure values without column collapse (and use tabular figures per [typography.md](typography.md)).

### i18n

Replace dummy content with realistic non-English samples for at least one screenshot:

- **German for headline-length stress testing.** *"Einstellungen"* (12 chars for *"Settings"*); *"Geschäftsbedingungen"* (20 chars for *"Terms"*).
- **Finnish or Hungarian for body-length stress.** Often runs 30–50% longer than English equivalents.
- **RTL flip for one screenshot.** Set the document or frame to RTL, render, check for icons pointing the wrong way, controls reversed, alignment broken. Pencil supports this via the `direction` property on frames.
- **Right-to-left text rendering.** Hebrew or Arabic samples for one or two text blocks; verify the layout still holds.

Cross-link [accessibility.md](accessibility.md) § i18n and RTL for the deeper coverage.

### `prefers-*` media queries

Honour the user-level preferences.

- **`prefers-reduced-motion`.** Replace translate-based reveals with simple fades or with no transition; disable parallax entirely; shorten or eliminate page-route transitions; keep functional state transitions (button press, focus appearance). See [motion-design.md](motion-design.md) § Reduced motion.
- **`prefers-contrast`.** Bump body text contrast above the WCAG AA floor (4.5:1) toward AAA (7:1); thicken borders; remove low-contrast decorative elements. Track via a `prefersContrast` theme axis if the design needs distinct frames.
- **`prefers-reduced-transparency`.** Replace glassmorphism or backdrop-blur surfaces with solid equivalents. If the design ships glassmorphism (refused elsewhere in this skill), at least design the solid fallback.

### Error copy

Every error states what went wrong, why, and how to fix.

- *"Invoice 4521 didn't send: Stripe rejected the card. Try a different payment method."* Not *"An error occurred."*
- *"Couldn't load jobs: the connection timed out. Retry, or check status.example.com."* Not *"Network error."*
- *"That email is already in use. Try signing in instead, or use a different email."* Not *"Invalid email."*

See [ux-writing.md](ux-writing.md) for the deeper copy register.

## Never

- **Never declare a design done with default-state-only on interactive components.** Default-plus-hover isn't enough either; disabled and loading are routinely needed.
- **Never skip the 404 / 500 / offline trio on a product surface.** These fail-states happen; the user landing on a blank page erodes trust.
- **Never use Lorem Ipsum or single-character padding to fake content length.** The comp ships against realistic content or it isn't ready.
- **Never claim accessibility without checking keyboard navigation and focus order.** A focus order that jumps around the page is a real accessibility failure that comp screenshots don't catch.
- **Never assume the user's network is fast or available.** Loading states aren't optional; offline behaviour isn't either for surfaces the user works in repeatedly.
- **Never use text-truncation as a substitute for thoughtful overflow handling.** Truncation hides information; the design should plan where information goes when there's too much of it.
- **Never document state-matrix deferrals without a written reason.** *"Skipped the disabled state for the secondary CTA because the secondary CTA doesn't get used in disabled contexts"* is fine; *"Deferred"* alone is forgotten.
- **Never use `prefers-reduced-motion` as a reason to ship no fallback.** The fallback IS what the user with reduced motion sees; it has to be designed.

## Verify

Walk the surface in the conditions that bite:

- **State matrix.** Every interactive node ships the states named in the brief plus the defaults from [interaction-design.md](interaction-design.md).
- **Fault states.** 404, 500, 503, offline, and the relevant taxonomies from [states.md](states.md) are present as frames.
- **Overflow.** Headlines at 2x length, body at 2x length, buttons at 2x length, list items with long names, numbers at 8 figures all render without breaking the layout.
- **i18n.** At least one screenshot shows realistic non-English content; RTL has been checked at least once.
- **`prefers-*`.** Reduced-motion fallback is designed; high-contrast still hits WCAG targets; reduced-transparency has solid equivalents.
- **Error copy.** Every error states what / why / how-to-fix; no *"An error occurred"* generic copy remains.
- **Realistic content.** No Lorem Ipsum; plausible names, dates, numbers throughout.

When the result feels right, hand off to [finalise.md](finalise.md) for the alignment, spacing, and token-consistency pass.
