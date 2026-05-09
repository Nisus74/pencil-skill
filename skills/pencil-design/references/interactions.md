# Interactions

The patterns that make a design *feel* like a real app rather than a screenshot. Most of them are invisible when right and obvious when wrong.

**What this file owns:** keyboard support, focus management, hit-target sizing, loading state choreography, ellipsis conventions, destructive-action discipline, URL-as-state, optimistic UI, tooltips and popovers, toast positioning, modal mechanics, selection patterns, native context menus.

**What this file does NOT own:** form-specific input mechanics, covered in [`forms.md`](forms.md). Animation timing and curves, covered in `modern-patterns.md` § Animation & motion. Component states (default/hover/focus/disabled/loading), covered in [`states.md`](states.md). Mobile gestures and native conventions, covered in `mobile-patterns.md` (when scaffolded).

## When to load this file

- Designing anything the user clicks, taps, types into, drags, or navigates with the keyboard.
- The user names *keyboard*, *focus*, *hit target*, *destructive*, *undo*, *URL state*, *optimistic*, *loading*, *spinner*, *modal*, *toast*, *tooltip*, *selection*, *right-click*.
- You're auditing a design for the dozens of small interactions that separate a polished product from a sketchy one.

## Keyboard everywhere

Every interactive element in your design must be reachable, operable, and dismissable from the keyboard alone. Pencil designs are visual; the keyboard contract is documented in `name` and `context`, then shipped by the engineer.

The WAI-ARIA Authoring Practices Guide (APG) describes keyboard patterns per component type. Defaults you'll use most often:

| Component | Keys |
|-----------|------|
| Button | `Enter` or `Space` activates |
| Link | `Enter` activates |
| Checkbox | `Space` toggles |
| Radio group | `Tab` enters group; `↑`/`↓` (or `←`/`→`) moves; `Space` selects |
| Select / dropdown | `Space` or `↓` opens; `↑`/`↓` moves; `Enter` selects; `Esc` closes |
| Combobox / autocomplete | Same as select; typing filters; `Enter` accepts |
| Tabs | `Tab` enters tab list; `←`/`→` moves between tabs; `Enter`/`Space` activates |
| Modal / dialog | `Esc` closes; focus trapped inside until close |
| Tooltip | Appears on focus; dismissable with `Esc` |
| Menu | `Enter`/`Space`/`↓` opens; `↑`/`↓` moves; `Enter` activates; `Esc` closes |

Don't invent your own keyboard semantics. Users know these defaults; deviating breaks the muscle memory that makes the keyboard fast.

**Hover-only affordances are keyboard-hostile.** A button that only appears when the user hovers over a card is invisible to keyboard users. Either always show, or also surface on `:focus-within` of the card. Same for action menus that only open on right-click: provide a visible trigger (a `⋯` icon button) so keyboard users have a way in.

**Don't intercept native shortcuts.** `⌘+Tab`, `⌘+W`, `⌘+T`, `⌘+L`, `⌘+R`, `⌘+P` belong to the OS or browser. A custom `⌘+S` handler that disables the browser's "Save Page As" without saving anything in your app is hostile.

In Pencil, document keyboard expectations on interactive components:

```
{
  "type": "frame",
  "name": "DropdownMenu_FilterBy",
  "context": "Combobox. Space or ArrowDown opens; ArrowUp/Down moves; Enter selects; Esc closes. Search filters list as the user types.",
  "reusable": true
}
```

## Focus management

Focus is the cursor of the keyboard world. When something interactive is focused, the user can act on it; when nothing is focused (or focus is in the wrong place), the keyboard is blind.

- **Visible focus indicators always.** Every interactive element gets a 2px `$focusRing` outline with 2px offset on `:focus-visible`. Visible against any surface in light and dark modes. Don't ship `outline: none` without a replacement.
- **`:focus-visible`, not `:focus`.** `:focus-visible` shows the ring only for keyboard navigation. Browsers handle the heuristic; you just style `:focus-visible` and let `:focus` be silent for mouse users.
- **`:focus-within` for grouped controls.** A card with multiple interactive children should subtly indicate when *any* child has focus, via a slight border highlight or a faint background shift. Tells the user where they are at the group level.
- **Restore focus on dismissal.** When a modal closes, focus returns to the element that opened it. When a popover closes, same. Without restoration, the user is dumped at the top of the page and has to re-find their place.
- **Focus traps for modals.** When a modal opens, focus moves into it (typically to the first interactive element, or to a "Cancel" button for destructive modals). Tabbing past the last element wraps back to the first. Esc closes and restores focus.
- **First-focus matters.** A modal that confirms a destructive action should land focus on the *Cancel* button to reduce accidental confirmation. A modal that requires user input lands focus on the input. A modal that just shows information lands focus on the close button.

In Pencil, name modal first-focus children explicitly: `Modal_FirstFocus` (a frame attribute, surfaced in the modal's `context`).

## Hit targets

The minimum interactive size that's comfortable for users:

- **24×24 visual minimum** on desktop pointer surfaces (tight UI density, dense data tables).
- **44×44 hit target on touch surfaces** (mobile, tablet, anything where a finger can land). The hit area can extend beyond the visible target via padding. A 24×24 close icon with 10px padding all around hits 44×44.
- **48×48 on Android** for material-spec compliance.
- **8px minimum spacing between adjacent targets.** Two buttons one pixel apart force precise targeting. Always pad.

Common offenders:

- **Icon-only close buttons** at 16×16 on dense modals. Expand to 24×24 visual + padding to 44×44 hit.
- **Inline actions in tables** where the row's row-height is 32 and the action icon is 12. The icon is unreachable on mobile; use overflow menus or expand row-height.
- **Accordion chevrons** that take only the chevron's pixel area as the click target. Make the entire row clickable.
- **Tab labels** in segment-control patterns where the label has no padding. The text is the hit target, so a 4-character tab is impossible to tap.

**Don't shrink targets below the minimum even on dense layouts.** A dense data table with 24-line-height rows can still have 44×44 hit zones via padding that overlaps the row above and below. The eye sees a 24×24 icon, the finger gets 44×44 of forgiveness. Document this in the component's `context`: *"Visual: 24×24. Hit area: 44×44 via 10px overflow padding."*

## Loading state choreography

The split-second between "user pressed something" and "user sees the result" is where loading-state design earns its keep.

- **Show a spinner on the action that's loading,** not on a global page overlay. The user pressed *that* button; that button should reflect the work.
- **Keep the original label visible.** A button that goes from `Save` to `Saving…` (with a spinner) tells the user what's happening. A button that goes from `Save` to a spinner *only* leaves them wondering.
- **Min show-delay 150–300ms.** Don't show the loading state for requests that complete in 50ms; the flicker is jarring. Wait 150–300ms before rendering the spinner; if the response arrives before then, skip the spinner entirely.
- **Min visible time 300–500ms.** Once the spinner appears, keep it visible for a minimum duration even if the response arrives quickly. A spinner that flashes for 80ms is more confusing than no spinner at all.
- **Skeleton screens for layout-known loads** (cards, lists, tables loading their data). They reserve the space and signal "content arriving here." Pair with a 1.4s shimmer animation per [`assets/design-system/motion.md`](../assets/design-system/motion.md).
- **Spinners only for unknown-duration loads** (a long-running export) or for actions where layout doesn't change (a button submit).
- **Progress indicators when duration is known.** A determinate progress bar (showing `47%`) is more reassuring than a perpetual spinner for any operation taking > 2 seconds.

In Pencil, document loading timing in the loading state's `context`: *"Show after 200ms; minimum visible 400ms. Replaces label with spinner + 'Saving…'."*

## Ellipsis conventions

A small piece of typography carrying outsized meaning. The trailing `…` means *something else is coming*. Use it consistently.

- **`Rename…`** (action that opens a follow-up dialog or input). The user clicks; a name field appears; they finish the rename in that field.
- **`Saving…`** (action in progress). Time-bound, finite, ends when the operation completes.
- **`Loading…`** (data fetch in progress). Same.
- **`Sign in`** (action that completes immediately, with no follow-up). No ellipsis.
- **`Delete`** (action that completes immediately, where deletion happens on click). No ellipsis.
- **`Delete…`** (action that opens a confirmation dialog). Has ellipsis.

The convention disambiguates: `Delete` deletes; `Delete…` opens "are you sure?"

Use the actual ellipsis character (`…` U+2026), not three periods (`...`). The character renders better, takes one character of width, and signals the convention to typography-aware users.

## Destructive actions

Anything that destroys user data, removes access, or otherwise makes their world worse.

Two acceptable patterns. Pick one per action; never both.

**Pattern A: Confirmation.** Use for actions that are catastrophic (delete account, drop database, archive a year of data) or non-undoable. The flow:

1. User clicks `Delete…` (note the ellipsis: it opens a dialog).
2. A confirmation modal appears, focus on **Cancel** to reduce accidental confirmation.
3. The modal labels the consequence: *"This will delete 12 items permanently. They cannot be recovered."*
4. The confirm button labels the action: *"Delete 12 items"*, instead of *"Confirm"*.
5. For especially destructive actions, require typing the resource name before the confirm button enables: *"Type the project name to confirm: my-project"*. GitHub's repo-delete uses this pattern.

**Pattern B: Undo.** Use for everything else: actions that are common, not catastrophic, and reversible. The flow:

1. User clicks `Delete` (no ellipsis; the action happens on click).
2. The thing is removed from the UI immediately.
3. A toast appears: *"Item deleted"* with an `Undo` button visible for 5–8 seconds.
4. If the user clicks Undo, the item returns. If they don't, the action completes server-side.

Undo is the better default for non-catastrophic actions because confirmation creates friction the user pays for *every time*; undo only costs them when they actually need it.

**Don't combine.** A confirm dialog *plus* an undo toast is the worst of both worlds. The user pays for confirmation every time and *still* gets a slow action.

## URL as state

The single most-skipped pattern in modern web design. The URL should reflect the user's current view state so they can refresh, share, and use the back button.

What belongs in the URL:

- **Filters and search queries** (`/customers?status=active&search=acme`).
- **Tabs and tab groups** (`/settings/billing` not `/settings`).
- **Pagination and sort** (`/orders?page=3&sort=date-desc`).
- **Open modal or drawer state** when the modal contains addressable content (`/photos/4567` for the photo viewer, not just `/photos` with state).
- **Selected item in master-detail** (`/inbox/conversation-789`).
- **Expanded panel state** when significant content is hidden behind it (`/dashboard?expand=metrics`).

What stays in component state:

- Hover state, focus state, transient UI state (a tooltip currently visible).
- Form draft values mid-typing (auto-saved server-side or local-storage, not URL).
- Animation in-progress.

Why it matters:

- **Refreshable.** The user refreshes; the page returns to where they were.
- **Shareable.** The user copies the URL and sends it; the recipient lands at the same view.
- **Back-button-able.** The browser's back button does something useful at every step.
- **Deep-linkable.** Notifications, emails, and external links can point at specific app state.

In Pencil, document URL-state expectations in the page's `context`: *"Filters and search persist in URL query params. Selected item appears in path. Modal state in URL hash."* The engineer ships the routing.

## Optimistic UI

For high-confidence writes (toggling a setting, marking a task done, liking a post, adding a tag), update the UI *immediately* and reconcile with the server in the background.

- **Update the local view on click.** The toggle visually flips, the task visually checks off, the like count visually increments. Don't wait for the server.
- **Send the request in the background.**
- **On success, do nothing visible.** The UI was already updated; no toast, no flash, no celebration.
- **On failure, roll back with a non-blocking toast.** *"Couldn't save your change, try again."* The toggle visually unflips. Don't replace the user's view; the toast is enough.

When NOT to use optimistic UI:

- **Server-side validation that's not replicable client-side** (uniqueness checks, complex permission logic). Use pessimistic UI.
- **Actions that have visible follow-on effects** (creating a record that needs a server-assigned ID before the user can interact with it).
- **Charges, billing, irreversible writes.** The user wants to know the action succeeded *for real* before they move on.

Optimistic UI is the single largest factor in perceived speed for action-heavy interfaces. Use it whenever you can.

## Tooltips

Tooltips are a last resort. Reach for them after you've tried inline help, label expansion, and visible affordances.

- **Inline help first.** A short helper text below a field beats a `?` icon with a tooltip. Always-visible, always-accessible, no hover discovery required.
- **Tooltips for icon-only controls.** A button with only an icon (no label) gets a tooltip that says what the icon does. Trigger on hover *and* on focus (keyboard users need it too).
- **Never essential information in a tooltip.** A tooltip that contains the only explanation of a critical feature is broken. Touch users (no hover) and screen-reader users may miss it. Tooltips are *supplementary*.
- **Dismissable with `Esc`.** Tooltips that linger until the user mouses off can trap users with tremor. Esc dismisses; click-outside dismisses.
- **Delay open, no delay close.** Around 500ms before opening on hover so passing the mouse doesn't trigger a cascade; instant close on mouse-out so they don't linger.
- **Position smart.** Tooltips that overflow the viewport should flip to the opposite side. The library handles this; document the expectation in component `context`.

## Toasts

Toasts are non-blocking notifications. They appear, hold briefly, and dismiss.

- **Position bottom-right** on desktop, **bottom-centre** on mobile. Out of the way of the user's task; predictable location.
- **Stack with a limit.** Cap at 3–5 visible toasts; older toasts collapse into a "+N more" affordance or fade out.
- **Auto-dismiss with a progress indicator.** A subtle bar showing time-to-dismiss. Pause-on-hover (the user is reading) and reset-on-action (they clicked Undo).
- **Default 5 seconds for info, 7–8 seconds for actionable** (toasts with an Undo or Retry button need longer).
- **Critical toasts don't auto-dismiss.** A "Your changes failed to save" toast stays until the user dismisses it or takes action.
- **Live-region announcements.** Toast containers ship `aria-live="polite"` (or `aria-live="assertive"` for critical errors). Document in component `context`.

## Modals

Modals interrupt. Use sparingly.

- **When to use:** confirmations, blocking decisions, focused tasks (a multi-step form that benefits from focused context), critical errors that block continuation.
- **When not to use:** secondary information (use a popover or expand-in-place), actions the user will repeat (cap-locked friction), navigation (use routing).
- **Backdrop dismiss vs explicit close.** Most modals: backdrop click dismisses. Destructive-action modals: backdrop click does nothing; require explicit Cancel. Form modals with unsaved changes: backdrop click warns about losing changes.
- **Close affordance always visible.** A `✕` close button in the corner, plus Esc, plus the backdrop in non-destructive cases. Three ways out is the floor.
- **Focus trap.** Tab cycles within the modal; doesn't escape to the page behind. Esc closes.
- **Don't nest modals.** A modal that opens another modal is a sign the flow needs to be a page or a wizard.

## Selection

Patterns for selecting items in a list, grid, or canvas.

- **Single-select** (radio-like): clicking an item selects it; clicking another deselects the first. No modifier keys.
- **Multi-select with toggle**: `⌘+click` (Mac) or `Ctrl+click` (Windows/Linux) toggles each item independently.
- **Multi-select with range**: `Shift+click` selects from the previously-selected anchor to the clicked item. Combined with `⌘`/`Ctrl` for additive range select.
- **Select-all**: a checkbox in the table header (or list header). When some-but-not-all are selected, render the indeterminate state (`-` instead of `✓`).
- **Clear selection**: an explicit affordance when 1+ items are selected, like *"3 selected · Clear"*. Don't make the user click a blank area to deselect.
- **Bulk actions toolbar**: when 1+ items are selected, an action bar appears (sticky to top or bottom) showing what they can do with the selection: Delete, Move to, Tag, Export.

In Pencil, name the selection states explicitly:

```
List_Customers / SelectionState_None
List_Customers / SelectionState_Some / 3-selected
List_Customers / SelectionState_All
```

## Right-click menus

Native context menus belong to the browser. Most apps should leave them alone.

- **Default: don't override.** The user expects to right-click and see Cut/Copy/Paste, Inspect Element, View Source. Overriding without strong reason is hostile.
- **When to override:** in a canvas-driven app (Figma, Pencil itself), in a file browser, in a heavily list/grid app where right-click delivers significant value (rename / duplicate / move to). Even then, fall through to the native menu when the user right-clicks on text or whitespace.
- **Always provide a non-right-click path.** Every action in your custom right-click menu must also be reachable via a visible affordance (a `⋯` icon, a toolbar button). Right-click is not the only way in.
- **Touch users get no right-click.** Long-press is the touch equivalent on iOS / Android. Document the expectation; ship the behaviour on touch surfaces too.

## Pencil expression

The interaction patterns above mostly live in `context` strings. The design's visual surface doesn't show them, but the code generator and the engineer need to know the intent.

Recommended `context` snippets per pattern:

- **Keyboard:** `"Keyboard: Space or ArrowDown opens; arrows move; Enter selects; Esc closes."`
- **Hit zone:** `"Visual: 24×24. Hit area: 44×44 via 10px overflow padding."`
- **Loading:** `"Show spinner after 200ms; min visible 400ms. Replaces label with 'Saving…'."`
- **Destructive:** `"Confirmation pattern. Confirm button labels the action ('Delete 12 items'). Focus lands on Cancel."`
- **URL:** `"Filter state persisted in URL query params (?status=active&search=). Refresh-safe."`
- **Optimistic:** `"Optimistic UI. Local state updates immediately. Toast on failure with Undo."`
- **Toast:** `"Live region. aria-live='polite'. Auto-dismiss 5s. Pause on hover."`
- **Modal:** `"Focus trap. First focus on Cancel. Backdrop click does nothing (destructive)."`

When you build a reusable component for an interaction pattern (e.g. a `ToastNotification` or a `ConfirmDialog`), encode the discipline in the component's `context` so every instance inherits it.

## Verification checklist

Before declaring an interactive design done:

1. **Tab-through.** Trace focus from the first focusable element to the last. Order matches visual reading order. Every interactive element is reachable.
2. **Focus ring visible.** Pick the most contrasting element (a primary CTA on its own surface). Focus ring visible in light *and* dark modes.
3. **Esc closes overlays.** Modal, popover, tooltip: all dismissable with Esc.
4. **Hit targets ≥ 44×44 on touch.** Test mobile-sized icons; padding extends hit area where needed.
5. **Loading state.** Loading actions show a spinner *and* keep their label. No bare spinners.
6. **Destructive paths.** Each destructive action follows confirmation OR undo, never both, never neither.
7. **URL state.** Filters / pagination / tabs / open-item all persist in URL. Refresh works.
8. **Optimistic where appropriate.** High-confidence writes update local state immediately.
9. **Toast position.** Toasts in the right place, with progress indicator, dismissable.
10. **Right-click.** Native context menu preserved by default (unless explicitly overridden with reason).

Fix what fails. Don't note any of these as TODOs; broken interactions ship as user-trust bugs.

## See also

- SKILL.md § Discipline rules: accessibility baseline (focus states, hit targets, colour-as-only-signal).
- [`forms.md`](forms.md): form-specific submit / validation / autofill mechanics.
- [`states.md`](states.md): component states (hover/focus/active/loading/error/success).
- [`flows.md`](flows.md): multi-step flow orchestration, modal-vs-page, optimistic UI patterns.
- [`accessibility.md`](accessibility.md): ARIA roles, focus order, screen-reader content, keyboard discoverability.
- [`modern-patterns.md`](modern-patterns.md): animation timing, command palette, AI-UI affordances.
- [`assets/design-system/motion.md`](../assets/design-system/motion.md): durations, easings, skeleton shimmer.
- [`assets/design-system/components.md`](../assets/design-system/components.md): visual treatment of interactive components.
