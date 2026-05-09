# Forms

The project's form conventions. The agent reads this file before designing any input, validation, or submit pattern. It complements `references/forms.md` (the canonical form-design reference); this file holds the project's specific commitments.

## Validation timing

The project commits to: `<on-blur for sync checks + on-submit for cross-field and async checks | on-submit only | on-keystroke (rare; only for live previews)>`.

Default rule (per `references/forms.md` § Validation timing): never validate on every keystroke. The user is mid-thought.

## Error display

Where errors appear:
- **Inline next to the field**, below the input. `<colour: $danger>`. Icon paired with the message (`alert-circle`).
- On submit with validation errors: focus moves to the first error; an `aria-live="polite"` region announces the count.
- `aria-describedby` on the input pointing to the error message id.

Server errors land in the same inline location as client errors (don't surface server errors in toasts when the cause is a specific field).

## Submit-state choreography

- **Submit stays enabled** until the user actually presses it. Disabling submit-while-invalid hides the form's shape.
- **On press**: disable submit, replace label with spinner-plus-label (`[spinner] Saving...`), keep the original button width to prevent layout shift.
- **Idempotency key** sent with every submit so the server can dedupe double-clicks. Document the key shape in the project's API conventions.
- **On success**: `<navigate to natural next page | inline success state with checkmark | toast confirmation>`. Per surface; default committed here.
- **On failure**: re-enable submit, surface inline errors, focus the first error, preserve form values (never blow them away).

## Save patterns by surface

The project commits one save pattern per surface type:

| Surface type | Save pattern | Notes |
|---|---|---|
| Settings (most) | Autosave per field, ambient indicator | Per `flows.md` § Settings flows |
| Settings (high-stakes: billing, security) | Explicit Save button, dirty-state warning on navigation | |
| Forms (signup, contact, onboarding) | Explicit Submit button | Single submission point |
| Inline editors (cells, fields) | Autosave on blur or Enter | Optimistic UI per `flows.md` § Optimistic UI |
| Long-form (documents, notes) | Continuous autosave with 'Saved 2 minutes ago' indicator | Like Notion, Google Docs |

## Mobile inputs

- **Font-size minimum 16px** on all inputs targeting mobile web (prevents iOS Safari from zooming on focus).
- **`inputmode`** set per input type (`numeric` for OTP / ZIP; `decimal` for currency; `tel` for phone; `email` for email).
- **`autocomplete`** set per field (`email`, `current-password`, `new-password`, `one-time-code`, `name`, `street-address`, `cc-number`, etc.) so password managers and autofill work.
- **`autocapitalize`** set per field (`none` for emails and usernames; `words` for names; `sentences` for free text).
- **`spellcheck="false"`** on emails, usernames, codes, passwords (otherwise red squiggles appear under valid input).

## Hit zones

- Checkbox / radio: label and control share one hit target via wrapping `<label>`.
- Padding extends the hit area at least 8-12px beyond the visible label text.
- Spacing between adjacent options ≥ 8px.

## Multi-step forms

When a form spans multiple screens:

- **Progress indicator visible** (stepper for 2-5 steps; progress bar for 6+; step counter for simple flows).
- **Back navigation preserved** without losing entered values.
- **Validate per step** on Next; don't wait until final submit to surface errors from earlier steps.
- **Auto-save partial progress** server-side (or local-storage as fallback). The user closing the tab shouldn't lose work.

See `references/flows.md` § Multi-step forms / wizards for the full anatomy.

## Unsaved-changes warning

- `beforeunload` listener fires when leaving with unsaved changes.
- Track dirty state: a form is dirty when any field has changed from its initial value.
- Don't fire the warning during the submit handler itself (the user is intentionally leaving).
- Surface the dirty state in the UI: subtle 'Unsaved changes' indicator near the submit button.

## Placeholder conventions

- Placeholders end with `...` (an ellipsis indicates a partial example): `name@domain.com...`, `1234 5678 9012 3456...`.
- Placeholders show an example pattern, never the field's purpose. The label carries the field's purpose.
- Never replace the label with a placeholder. Floating labels and placeholder-as-label patterns ship as accessibility regressions.

## Component library mapping

The project's `Form`, `Field`, `Input`, `Submit` components live in `<.lib.pen path>` (or `<package>`). Variant per input type (`Input_Text`, `Input_Email`, `Input_Search`, `Input_Password`, `Input_OTP`, `Textarea`).

Each component's `context` documents:
- The HTML attributes it ships (`type`, `inputmode`, `autocomplete`, `autocapitalize`, `spellcheck`).
- Validation behaviour (when, how errors render).
- Loading state choreography.

## Verification checklist

Before declaring a form done (per `references/forms.md` § Verification checklist):

1. Tab to the first input, type, press Enter. Form submits.
2. Textarea: Enter inserts a newline; ⌘+Enter submits. Visible in the UI.
3. Validate on blur, not on keystroke. No red borders mid-typing.
4. Submit-with-errors: all errors surface; focus moves to first; live region announces count.
5. Loading state: button shows spinner + keeps label; submit disabled until response.
6. Success state: clear confirmation, not a silent reload.
7. Failure state: submit re-enables, errors appear, form values preserved.
8. Mobile font-size ≥ 16px so iOS doesn't zoom.
9. Autocomplete attributes present; password manager triggers correctly.
10. Hit zones for checkbox/radio: label click toggles control.
11. Unsaved-changes warning fires on navigation away.
12. Required indicator present per the project's chosen convention.

## See also

- `references/forms.md` (in the pencil-design skill): the canonical form-design reference.
- `references/flows.md` (in the pencil-design skill): § Multi-step forms / wizards, § Settings flows for save-pattern decisions.
- `references/microcopy.md` (in the pencil-design skill): error message anatomy, button label patterns.
- `tokens.md`: `$danger`, `$focusRing`, input-related tokens.
- `components.md`: the project's `Form`, `Field`, `Input`, `Submit` component definitions.
- `voice.md`: error message tone.
- `accessibility.md`: ARIA patterns, focus management, keyboard shortcuts.
