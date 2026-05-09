# Forms

Forms are where the most discipline pays off. The user is *interacting* with what you designed; every key, click, and tap goes through it. A polished form is invisible; a sloppy one teaches the user to dread your product.

**What this file owns:** submit behaviour, label patterns, validation timing, error display, input attributes, submit-state choreography, mobile input quirks, hit-zone discipline, multi-step-form mechanics, unsaved-changes warnings, placeholder conventions.

**What this file does NOT own:** the screen-level orchestration of a multi-step flow (page vs modal, back-stack model). That's [`flows.md`](flows.md). The visual design of inputs (border treatment, focus ring) lives in [`assets/design-system/components.md`](../assets/design-system/components.md). State transitions (loading, error, success at the field level) are in [`states.md`](states.md). Microcopy for errors / empty / success is in `microcopy.md` (when present in your project).

## When to load this file

- The design includes any input the user types, picks, or toggles: sign-up, sign-in, settings, search, filters, comments, comment editors, multi-step wizards, billing pages.
- The user names *form*, *signup*, *login*, *validation*, *autofill*, *autocomplete*, *password manager*, *paste*, *unsaved changes*, *error message*, *fieldset*, *autosave*.
- You're auditing an existing form for hidden friction (a 3% drop in conversion that nobody can locate).
- You're building a reusable input component for the project's `.lib.pen`.

## Submit behaviour

The single most disrespected rule in form design: **Enter submits.** Users press Enter; the browser fires a submit event. If you've broken that, you've made the form hostile to keyboard users, screen-reader users, and most muscle-memory users.

Rules:

- **Single-field forms:** Enter on the focused field submits. Always.
- **Multi-field forms:** Enter on any focused single-line input submits the form. The default browser behaviour. Don't intercept it.
- **Forms with a textarea:** Enter inside the textarea inserts a newline (the textarea behaviour). `⌘+Enter` (or `Ctrl+Enter` on Windows) submits. Document this in the design's `context` and surface the keyboard hint in the UI (a small *"⌘ + Enter to send"* near the submit button).
- **Multi-button forms:** the default submit button is the *first* `type="submit"` in source order. Place the primary action first in the DOM (DOM-first, regardless of visual position). If your design positions Cancel left and Submit right, the DOM order should still be Submit first, Cancel second; visual order is set by flex / grid.
- **No-submit-button forms:** even forms designed without a visible submit button (a search bar, a single-toggle setting) need an Enter handler. Don't ship a form that swallows Enter silently.

In Pencil, name the submit-on-Enter expectation in the form's `context`: *"Single-field form. Enter on the input submits and triggers the search."* The engineer reads it and knows not to intercept.

## Labels

Every interactive control has an accessible label. Either:

- **A `<label>` with a `for` attribute** matching the control's `id`. Click the label, focus moves to the control. The most accessible pattern.
- **A wrapping `<label>`** containing both the control and the label text. Same accessibility, less ceremony, but harder to style consistently.
- **An `aria-label` or `aria-labelledby`** when a visible label isn't possible (an icon-only search input). Less ideal; sighted users want the visible label too.

Rules:

- **Visible labels are the default.** Floating labels and placeholder-as-label patterns ship as accessibility regressions. The label disappears when the user starts typing, and they have no way to recover the field's purpose mid-input. Reserve floating labels for surfaces with extreme density constraints, and even then, pair with a permanent above-the-input label that's visually subtle.
- **Required indicator next to the label,** not the input. A `*` after the label, or *"(required)"* in muted type. When most fields are required, mark the *optional* fields instead. This flips the cognitive load to the rarer case.
- **Click-target the label.** Native `<label>` does this for free. When using `aria-labelledby` or a custom layout, manually wire the label's click handler to focus the input.

In Pencil:

```
{
  "type": "frame",
  "name": "EmailField",
  "context": "Email input field with associated label. Click on label focuses input. Required field.",
  "children": [
    { "type": "text", "name": "EmailLabel", "text": "Email address" },
    { "type": "frame", "name": "EmailInput", "context": "Type: email. Inputmode: email. Autocomplete: email. Autocapitalize: off. Spellcheck: off." }
  ]
}
```

Name the label and the input as siblings under a parent frame named for the field (e.g. `EmailField`). The hierarchical name communicates the binding.

## Validation timing

When you validate determines whether the form feels like a partner or a hall monitor.

- **Don't validate on every keystroke.** A red border that appears as the user types the second character of their email is hostile. The user is mid-thought.
- **Validate on blur** (when the user leaves the field) for individual-field constraints (email format, password strength, required). The user has finished thinking; now you can react.
- **Validate on submit** for cross-field constraints ("password and confirm-password must match"; "you can't book a return flight before the outbound") and for any constraint that requires a server round-trip.
- **Don't block typing.** If a field has constraints (numeric only, max 50 characters), accept anything the user types and surface validation feedback after. Don't silently swallow keystrokes. Browsers used to do this with `<input type="number">`, and users hated it. Modern apps use `inputmode` (which sets the keyboard) and validate after.
- **Allow submitting an incomplete form** to surface all errors at once. Disabling the submit button until every field is valid hides the "what's missing?" question; the user can't see the full list of requirements until they've satisfied them. Better: leave submit enabled, on click validate everything, scroll to the first error, and announce the error count.

A form that lets the user see the whole shape of what's required and lets them iterate is calmer than one that gates each step.

## Error display

When validation fails, the user needs to see where the error is, why it happened, and how to fix it.

- **Inline errors next to the field.** Not in a banner at the top, not in a tooltip on hover. Below the input (or to the right on wider layouts), in the error colour paired with an alert icon, with the message itself written as guidance: *"Use a valid email address, like name@domain.com"*, not *"Invalid email"*.
- **On submit, focus the first error.** Move focus programmatically to the first invalid field and announce the error count via an `aria-live="polite"` region: *"3 fields need attention."* Keyboard users get to the error directly; screen-reader users hear that something happened.
- **Pair `aria-describedby` with the field** so screen readers read the error message alongside the field's label when the user lands on it.
- **Don't clear the error eagerly.** Wait until the user has actually changed the field to something valid before removing the error message. Clearing on first keystroke (when the value is now invalid in a *different* way) creates a flash that hides what's happening.
- **Server errors look the same as client errors.** A "this email is already in use" comes from the server but lands in the same inline location with the same visual treatment. Don't surface server errors in toasts when the cause is a specific field.

Anti-patterns:

- A red banner at the top of the form that says *"Please fix the errors below"* with no indication of which fields. Useless without scrolling.
- Tooltips that appear on hover and disappear when the user mouses to the field to fix it. The error message is no longer visible by the time it's relevant.
- Error messages that blame the user (*"You entered an invalid email"*) instead of guiding them (*"Use a valid email address"*).
- Removing the user's input on submit when validation fails. Devastating for long forms; treat as a critical bug.

## Input attributes

The browser knows what an email looks like, what a phone number is, what a credit card needs. Tell it.

- **`type`** for the high-level kind: `email`, `tel`, `url`, `password`, `number` (rarely; see below), `date`, `time`, `search`, `color`. Each triggers different keyboard, validation, and rendering on mobile.
- **`inputmode`** for the mobile keyboard layout when `type` doesn't fully describe it: `numeric` (no decimal, no minus, suitable for OTP codes, ZIP codes, PIN entry), `decimal` (numeric keyboard with decimal, suitable for currency, weight), `tel` (phone-style keypad), `email` (lowercase + @), `url` (lowercase + .com shortcut), `search` (search-shaped Enter key).
- **`autocomplete`** with the right value: `email`, `username`, `current-password`, `new-password`, `one-time-code` (critical for SMS-OTP autofill on iOS), `name`, `given-name`, `family-name`, `street-address`, `postal-code`, `country`, `cc-number`, `cc-name`, `cc-exp`, `cc-csc`. Without these, password managers and autofill silently fail.
- **`name`** with a meaningful semantic value (`email`, `password`, `firstName`) so password managers and form-fill engines recognise the field. Don't ship `name="field-1"`.
- **`pattern`** for client-side regex validation (sparingly; usually `inputmode` + on-blur validation is better).
- **`autocapitalize`** for control over the iOS autocapitalize behaviour: `none` for emails, `none` for usernames, `words` for names, `sentences` for free-text inputs.
- **`spellcheck="false"`** for inputs where spellcheck is hostile: emails, usernames, codes, passwords. Spellcheck on an OTP code shows red squiggles under every code that isn't a dictionary word. Useless.

In Pencil, document the attributes as a flat list in the input's `context`:

```
"context": "Type: email. Inputmode: email. Autocomplete: email. Name: email. Autocapitalize: none. Spellcheck: false."
```

The engineer reads it once and ships them all.

**Avoid `<input type="number">` for most numeric inputs.** It's harder to control than it looks: it strips leading zeros, breaks on locales that use commas as decimal separators, accepts scientific notation, and the up/down spinner is rarely useful. Use `<input type="text" inputmode="numeric" pattern="[0-9]*">` for OTP codes and the like; `<input type="text" inputmode="decimal">` for currency. Reserve `type="number"` for genuine numeric ranges with sliders or steppers.

## Submit-state choreography

The split-second between "user pressed submit" and "user sees the result" is where a lot of forms quietly fail.

- **Keep submit enabled until the user actually presses it.** Disabling submit-while-invalid hides the form's shape; disabling submit-because-already-pressed prevents double-submission, which is the *only* reason to disable submit. Disable on press, not before.
- **On press, disable submit and show a spinner inside the button** (replacing the text or paired with it). The button should NOT collapse to just-spinner; *keep the original label* so the user knows what's happening. Pattern: `[spinner] Saving…` instead of `[spinner]`.
- **Block double-submit on the server too** with an idempotency key. The client-side disable is the friendly version; the server-side dedupe is the actually-safe version. Document the idempotency expectation in the form's `context`.
- **Show the result without making the user wait.** Optimistic UI when the request is high-confidence (toggling a setting, marking complete). Pessimistic when the request can fail in user-visible ways (creating a record, charging a card). For pessimistic submits, the button stays in the loading state until the server responds; for optimistic, the button completes immediately and the API call happens in the background.
- **On success, do something.** Don't leave the user staring at a populated form wondering if it worked. Either: show a success state inline (a checkmark + confirmation text, autosaved fields), navigate to the natural next page, or clear the form for re-entry, whichever the workflow demands.
- **On failure, restore submit and surface the error.** The form's values stay populated (never blow them away). Inline errors appear where they belong. Focus moves to the first error, or to a top-level error region for server-only errors that don't map to a field.

## Mobile inputs

Mobile inputs have their own taxonomy of small mistakes that look like big mistakes.

- **Font-size ≥ 16px on inputs.** iOS Safari zooms into any input with `font-size < 16px` when the user taps it, then zooms out when they blur. The zoom-in/zoom-out shuffle is jarring. Set `font-size: 16px` minimum on all inputs targeting mobile web. Use `clamp(16px, 1rem, 18px)` if you want to keep desktop slightly smaller.
- **Use the right keyboard.** `inputmode` matters more on mobile than desktop. A user entering a phone number with `inputmode="tel"` sees a numeric keypad; without it, they see a full QWERTY and have to find the digits.
- **Trim values.** Users paste into mobile inputs constantly, and pastes from contact apps or QR scanners often include leading/trailing whitespace. Trim on submit (server-side, ideally also client-side) to avoid "Invalid email" errors caused by an invisible space.
- **Numeric autofill.** For OTP codes, set `autocomplete="one-time-code"`. iOS surfaces the SMS code as a keyboard suggestion the user can tap. Without it, the user copies the code from the SMS and pastes it manually.
- **Date pickers vary wildly.** Native mobile date pickers are good; native desktop date pickers are inconsistent across browsers. For desktop, consider a custom date picker; for mobile, lean on native. Document the choice in the field's `context`.
- **Action button on the keyboard.** iOS shows a button on the keyboard's top-right (Go, Send, Search, Done). The label comes from the form's submit button; ship a meaningful submit button label so the keyboard reflects the action.

## Hit zones

Checkboxes and radio buttons have small visual targets. The label and the control should share one hit zone; clicking the label focuses and toggles the control.

- **Wrap the input and label in a single `<label>`** so the entire region is the hit target. No dead zones between input and text.
- **Add padding to the label** so the hit area extends 8–12px beyond the visible text. Touch users (and tremor users) hit the right control without aiming.
- **Spacing between adjacent options ≥ 8px.** Two checkboxes vertically stacked with no gap creates a target ambiguity; the user may toggle the wrong one.
- **For radio groups, the entire group has one tab-stop.** Tab focuses the first (or selected) radio; arrow keys move between options. Don't tab between every radio in a 5-option group; that's hostile.

In Pencil, name the wrapping frame `Field_<label>` and document the hit-zone expectation: *"Label and control share a single click target. Padding extends hit area 12px beyond visible text."*

## Multi-step forms

When a form spans multiple screens (signup with email-verify, checkout with address-and-payment, onboarding with three steps), the design carries extra obligations.

- **Show progress.** A progress indicator (`Step 2 of 4`, a horizontal stepper) tells the user how much is left. Don't hide it. Don't make it interactive unless the user can actually jump forward.
- **Allow back navigation.** The user must be able to go back without losing what they entered. Either persist values in form state, or use the browser's back button (which means each step is its own URL; see `interactions.md` § URL as state).
- **Validate per step.** Each step validates its own fields on Next; don't wait until final submit to surface errors from step 1. The user has moved on; surfacing errors retroactively is frustrating.
- **Show what's coming.** A breadcrumb or stepper that says *"Account → Profile → Preferences → Done"* sets expectations. The user knows what they're committing to.
- **Save partial progress on long forms.** A 4-step signup that loses everything when the browser tab closes is a conversion killer. Auto-save server-side (with `name` + `email` as a draft key), or local-storage as a fallback.

For full multi-step flow patterns (page vs modal, back-stack, deep links into mid-flow), see [`flows.md`](flows.md).

## Unsaved-changes warnings

When the user has typed into a form and tries to leave the page (close the tab, navigate away, click a link), they should be warned.

- **`beforeunload` listener.** Browsers expose this as a generic prompt: *"You have unsaved changes. Leave anyway?"* The wording is browser-controlled; you don't get to customise it. Use sparingly; every false positive teaches the user to dismiss the warning reflexively.
- **Track dirty state.** A form is "dirty" when any field has changed from its initial value. A form is "clean" when all fields match initial values, or when the form has been successfully saved. Only fire the warning when dirty.
- **Don't fire on submit.** When the user clicks Submit, they're intentionally leaving the form. Don't ask them to confirm. Suppress the warning during the submit handler.
- **Surface the dirty state in the UI.** A subtle indicator near the submit button (*"Unsaved changes"*, or a small dot) tells the user there's work-in-progress without nagging them.

In Pencil, document the dirty-state expectation on the form's outer frame: *"Tracks dirty state. Fires beforeunload warning when leaving with unsaved changes. Suppresses warning during submit."*

## Placeholders

Placeholders are the most-misused convention in form design.

- **Placeholders end with `…`** by convention (an ellipsis indicates a partial example): `name@domain.com…`, `1234 5678 9012 3456…`.
- **Placeholders show an example pattern, not the field's purpose.** *"name@domain.com"* is right; *"Enter your email"* is wrong (that's the label's job).
- **Never replace the label with a placeholder.** Placeholder-as-label disappears when the user types, leaving them stranded. The label is permanent; the placeholder is temporary guidance.
- **Don't use placeholders for required-field hints** (use the label's required indicator instead) or for validation rules (use a permanent helper text below the field).

A placeholder is a tiny, optional layer of help. If you find yourself relying on it, the field needs more help (a label, a helper text, or a tooltip), not a fancier placeholder.

## Pencil expression

Pencil's component system carries forms naturally; the discipline above maps to slots, descendants, and `context`:

- **`Form` component.** Top-level frame with `name: "Form_<purpose>"` (e.g. `Form_Signup`). Holds field children, submit action, and form-level error region. `context` documents submit behaviour (Enter handling, idempotency, success path).
- **`Field` component.** Reusable, with slots for label, input, helper text, and error message. The `Field` component knows its own focus/error/disabled states (see [`states.md`](states.md)).
- **`Input` primitive.** Variants per type (`Input_Text`, `Input_Email`, `Input_Password`, `Input_Search`); each carries its `type`/`inputmode`/`autocomplete` values in its `context`.
- **`Submit` button.** Distinct from a generic button. `Submit` is a `Button` variant whose default state, loading state, and success state are all designed (see [`states.md`](states.md) § `loading`, § `success`).
- **Form-level error region.** A frame at the top or bottom of the form with `context: "Live region. Announces error count on submit when validation fails. Polite (not interrupting)."*. The engineer ships `aria-live="polite"`.

When the project doesn't yet have these as `.lib.pen` components, build them inline the first time you need them, then surface to the user: *"This form pattern looks reusable. Should I add a `Form` and `Field` component to your library?"*

## Verification checklist

Before declaring a form done:

1. **Submit on Enter.** Tab to the first input, type, press Enter. Form submits.
2. **Textarea submit.** If the form has a textarea, Enter inside it adds a newline; ⌘+Enter submits. Visible in the UI.
3. **Validate on blur, not on keystroke.** No red borders mid-typing. Errors appear when the user moves focus away.
4. **Submit-with-errors.** Click submit on an invalid form. All errors surface; focus moves to the first; an `aria-live` region announces the count.
5. **Loading state.** On submit, the button shows a spinner *and* keeps its label. Submit is disabled until response arrives.
6. **Success state.** On success, the user sees a clear confirmation, not a silent reload.
7. **Failure state.** On failure, submit re-enables, errors appear, form values stay populated.
8. **Mobile font-size.** Inputs are ≥ 16px so iOS doesn't zoom in.
9. **Autocomplete attributes.** Every field has the right `autocomplete` value. Test by triggering the password manager.
10. **Hit zones.** Click the label of every checkbox / radio. The control toggles. No dead zone between label and control.
11. **Unsaved-changes warning.** Type into the form, try to navigate away. Browser asks to confirm.
12. **Required indicator.** Required fields are marked. (Or, if the form is mostly required, optional fields are marked.)

Fix what fails. Don't note any of these as TODOs; broken form mechanics ship as conversion bugs.

## See also

- SKILL.md § Discipline rules; naming, context, components-first all apply to form components.
- [`flows.md`](flows.md): multi-step flow orchestration, back-stack, deep links, optimistic UI.
- [`interactions.md`](interactions.md): keyboard everywhere, focus management, URL-as-state, loading state timing.
- [`states.md`](states.md): field-level states (default/hover/focus/error/disabled/loading/success).
- [`accessibility.md`](accessibility.md): ARIA labels, focus order, screen-reader content, RTL form layout.
- [`composition-patterns.md`](composition-patterns.md): slot design for `Field` and `Input` components.
- [`assets/design-system/components.md`](../assets/design-system/components.md): visual treatment of inputs (border, focus ring, error colour).
- [`assets/design-system/voice.md`](../assets/design-system/voice.md): error message tone, microcopy patterns.
