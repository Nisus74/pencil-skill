# Interaction design

Component states are the second-class citizen of most generated UI. The default state gets the design attention; hover gets a colour shift; focus gets the browser default; disabled gets greyed out; loading gets a spinner; error gets a red border. The result is a competent default state surrounded by stamped-out variants that read as machine-generated the moment a user interacts.

This reference is the *how-to-design-states* depth that sits alongside [states.md](states.md) (which carries the *taxonomy* of states and screen-level fault states). Use [states.md](states.md) to know *which* states a component needs; use this file to know *how to design each one well*.

## State design philosophy

Every interactive component carries a small society of states. The user spends as much time in non-default states (hovering, focusing, mid-action) as in the default. The design of each state is design work, not afterthought.

Three principles:

1. **The state should describe the change, not just signal it.** A hover state that brightens the button tells the user *"yes, you're targeting this."* A hover state that also subtly shifts the cursor-target affordance (a slight scale, a colour bloom toward the edge) tells the user *"this is interactive and ready."* Both work; the second carries more design intent.
2. **State motion confirms causality.** A button that changes state instantly is unclear: did I cause it? A transition over 100–150ms ties the state change to the user's action.
3. **States should compose predictably.** A button that is hovered AND focused AND about to be clicked needs a defined visual; if the design only thought about one state at a time, the composition reads as accidental.

## The state inventory

For interactive components (buttons, inputs, controls, list items, links), expect to design these states:

| State | When it shows | Common failure |
|---|---|---|
| **Default (rest)** | The component, unread | The only state designed; everything else is afterthought |
| **Hover** | Pointer over the component | A 5% darker fill, nothing else; reads as generic CSS reset |
| **Focus (keyboard)** | Keyboard navigation lands here | Default browser outline; ugly and inconsistent |
| **Focus + hover** | Both at once | Not designed; the two states fight |
| **Pressed (active)** | Mid-click, before release | Skipped entirely; the click feels disconnected |
| **Disabled** | Component can't be used | 50% opacity on everything; conveys nothing about *why* |
| **Loading** | Async work in progress | Spinner replacing label; layout shift on completion |
| **Error** | Validation or state failure | Red border, no explanation |
| **Selected** | Component is "on" or chosen | Colour swap; doesn't compose with hover/focus |
| **Read-only** | Visible but not editable | Looks the same as disabled (different meaning) |

States not in this list (skeleton, empty, partial-failure, the screen-level fault states 404/500/etc.) live in [states.md](states.md) under the component-state and screen-state taxonomies.

## Designing each state well

### Hover
- **Targets every visible affordance**, not just the fill. Border colour, icon weight, label brightness, the cursor-target halo. Multiple subtle shifts compound to feel *"alive."*
- **Eases in over 100–150ms** with ease-out. Instant hover changes read as twitchy.
- **Doesn't shift layout.** A hover that scales the button and pushes neighbouring elements is visually noisy.
- **Reverses smoothly.** Hover-out runs the same duration; no jump-cut back to default.

### Focus (keyboard)
- **Always visible.** *Never* `outline: none` without a replacement. Keyboard users navigate by focus indicator; remove it and the surface becomes unusable.
- **Distinct from hover.** Hover and focus are different events; a focused-but-not-hovered button should be visually identifiable. Common approach: hover changes the fill, focus adds a 2–3px ring around the component.
- **Uses `focus-visible` semantics.** Show the keyboard focus ring on keyboard navigation; suppress it on mouse click (where the visual click feedback already confirms target). In Pencil, document this in `context` for the implementer.
- **Composes with hover.** Focus + hover shows both: the ring AND the hover fill change.
- **High-contrast against background.** Focus rings at low contrast (a 1px blue ring on a light background) fail accessibility. Aim for ≥3:1 against the surface the ring sits on (per [accessibility.md](accessibility.md)).

### Pressed (active)
- **Tiny inset or colour-dim.** A 2–4% darker fill or a 1px translateY downward signals the press. Duration is one frame (≤16ms); the state exists only between mousedown and mouseup.
- **Confirms the click even before release.** Without the pressed state, the user can't tell their click registered until the action completes.

### Disabled
- **Communicates *why*, not just *that*.** A disabled CTA next to a tooltip explaining the missing precondition is far better than a greyed-out button alone. *"Add a payment method to publish"* on hover over a disabled Publish.
- **Maintains shape and position.** Don't shrink or hide disabled components; preserve layout integrity.
- **Reduces visual weight, not just opacity.** 50% opacity often looks like a bug. Tint toward the surface colour, drop the border to 1px lighter, mute the icon.
- **Allows focus on touch and keyboard.** A disabled button should still be focusable so screen-reader users can read the tooltip.

### Loading
- **Skeleton over spinner for content load.** Shaped placeholders matching the line-height and shape of the loaded content (per [motion-design.md](motion-design.md)).
- **In-button spinner for action confirmation.** When the user clicks Submit and the action takes >300ms, show a spinner inside the button label position. Preserve label width so the button doesn't reflow.
- **Disable the action while loading.** Concurrent submits create duplicate work.
- **Optimistic for fast-enough actions.** If the action is statistically near-instant (a like, a toggle), show the success state immediately and reconcile if the server disagrees.

### Error
- **State plus message.** A red border alone tells the user *something* is wrong; the message tells them *what* and *how to fix it*. See [ux-writing.md](ux-writing.md) for error-message structure.
- **Inline near the affecting field.** Error messages stacked at the top of a long form force the user to find the field.
- **Persists until corrected, not on every keystroke.** Validating mid-typing produces error states that flicker as the user types.
- **Doesn't only use colour.** Add an icon (per [accessibility.md](accessibility.md) "colour-is-never-the-only-signal" rule).

### Selected
- **Compositionally clean.** Selected + hover needs to be readable. Common pattern: selected uses a tinted background plus a 2px leading border; hover adds a 5% surface darken on top of the selected tint.
- **Distinct from focus.** Selected is a persistent state ("this row is the one I'm working with"); focus is transient ("this row received keyboard attention"). They should look different.

### Read-only
- **Looks editable but unresponsive.** A read-only input has no hover, no focus ring, no edit affordances, but reads as full-strength visually. The user knows what value is set; they just can't change it here.
- **Distinct from disabled.** Disabled = "you can't change this right now (and you might be able to under other conditions)." Read-only = "this value is fixed by definition."

## Register-specific state recipes

### Product
Product state design is functional. Each state's job is feedback; ornament is restrained.

- Hover: subtle (`oklch(L-0.03 …)` darken on fill, label brightens 5%, no scale, no shadow).
- Focus: 2px ring in accent colour, 2px offset from the component.
- Pressed: 1px translateY down, fill 5% darker, instant.
- Disabled: fill at 20% accent, label at 40% text, no border.
- Loading: skeleton on content; in-button spinner on actions; both ≥300ms threshold.
- Error: 2px error-coloured border, error message in 13px below, error-tinted background on the field at 5% chroma.
- Selected: surface-accent tint (5% accent over surface), 2px accent leading border.

### Brand
Brand state design has more room to express. The hover of a brand CTA can be choreographed.

- Hover: fill changes, label shifts, secondary affordance appears (an arrow that slides in from the right, a subtle scale, a halo bloom). Easing curve has more character (ease-out-expo or a gentle overshoot).
- Focus: ring in brand colour, possibly with a soft glow that hints at brand expression (used sparingly).
- Pressed: brief scale-down to 0.98 plus opacity dip to 0.9 over 100ms, then back.
- Disabled: rare in brand (CTAs on brand sites are almost never disabled).
- Loading: page-transition shimmer rather than skeleton; brand pages typically don't load partial content the way product surfaces do.
- Error: form errors on a brand page (newsletter signup, contact form) should still follow product error patterns; the brand voice is in the message copy, not the visual chrome.

## Focus management depth

Focus order is part of interaction design that most generated UI gets wrong by default.

### Default focus order
The DOM order. If the design lays out the page so that the natural reading flow matches the DOM, default focus order works. If the design uses CSS to reposition elements (a "Submit" button visually below the form but actually before it in the DOM), focus order betrays the user.

### Focus traps
Modals and overlays should trap focus inside them. Keyboard navigation from the last focusable element in a modal wraps to the first; focus shouldn't escape to the underlying page until the modal closes. Document this in `context` on modal components.

### Skip links
Long pages benefit from a "Skip to main content" link as the first focusable element, hidden visually until focused. The keyboard user lands on it, presses Enter, and skips past the navigation.

### Restoring focus after interaction
When a modal closes, focus should return to the element that opened it (so the keyboard user can continue from where they were). When a list item is deleted, focus should move to the next item (not back to the top of the list).

For deeper a11y coverage of focus and keyboard navigation, see [accessibility.md](accessibility.md).

## State composition

States compose. Hover + focus + selected + disabled is a real possibility that the design needs to handle. Build a small matrix per component:

|  | Default | Hover | Focus | Selected |
|---|:---:|:---:|:---:|:---:|
| **Default** | rest | hover only | focus only | selected only |
| **Hover** | hover only | (self) | hover + focus | hover + selected |
| **Focus** | focus only | hover + focus | (self) | focus + selected |
| **Selected** | selected only | hover + selected | focus + selected | (self) |

Each compound state needs a defined visual. Most designs lazily compose by stacking CSS rules; the result depends on rule order and feels accidental. Decide explicitly: hover + selected should look like *this*; focus + selected should look like *that*.

## Pencil-specific

### Building states as component variants
Reusable components in `.lib.pen` should ship with state variants. The structure:

```
PrimaryButton/
  Default       (the rest state)
  Hover
  Focus
  Pressed
  Disabled
  Loading
```

Build each as a variant of the same reusable component so consumers can switch states without reauthoring. Use `descendants: { ... }` overrides on `ref` instances when a particular surface needs a state variant.

### Document state transitions in `context`
The design file doesn't author the runtime animation, but the `context` string on the component records the intended state behaviour:

*"PrimaryButton: 150ms ease-out hover transition on fill and label brightness. Focus ring 2px in `$accent`, 2px offset. Pressed state instant (≤16ms). Disabled: 20% accent fill, 40% text colour, no border, still focusable."*

When engineers implement, this is the spec.

### Verify state coverage at step 6
The SKILL.md verification checklist includes *"every component you authored has the states it needs."* Walk each interactive component and confirm:

- Hover exists, eases in
- Focus is visible, contrasts ≥3:1 against surface
- Pressed exists, is instant
- Disabled communicates *why* (tooltip or adjacent text)
- Loading skeleton or in-button spinner present where action could take >300ms
- Error state exists with inline message
- Selected (if applicable) composes cleanly with hover and focus

If any state is missing, fix it before declaring done. *"States are a hand-off concern"* is the most common excuse and the most common production bug.

### State design within the screenshot loop
After building the default state of a component, build at least the hover and focus variants in the same `batch_design` call. Screenshot the trio. The composition of default-hover-focus reveals whether the states were designed together (they read as a family) or stamped out (each one looks slightly off-key).
