# States

The states this product ships. The agent reads this when deciding what variants a component needs and what fault states a screen needs to handle.

This is the project's *contract* for state coverage. The agent's playbook for *how to design* states lives in the pencil-design skill (`references/states.md`). Don't duplicate the playbook here — record decisions and project-specific overrides.

## Per-component state coverage

This expands [`components.md`](components.md) § Required state coverage with project-specific notes. Every reusable component must cover the columns marked ✅ before shipping into the library.

| Component | Default | Hover | Focus | Pressed | Disabled | Loading | Error | Success | Skeleton | Notes |
|-----------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|-------|
| `ButtonPrimary` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | Loading state replaces label with spinner; preserves width. |
| `ButtonSecondary` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | |
| `ButtonGhost` | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | — | No loading state — use ghost for low-stakes actions. |
| `ButtonDestructive` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | Confirmation modal handles its own loading; button keeps default. |
| `IconButton` | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | — | |
| `LinkText` | ✅ | ✅ | ✅ | — | ✅ | — | — | — | — | |
| `Input` | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | — | Loading is for async-validated inputs. Filled is shown above as the default-with-content variant. |
| `Textarea` | ✅ | — | ✅ | — | ✅ | — | ✅ | — | — | |
| `Select` | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | — | — | Loading covers async-fetched options. |
| `Checkbox` | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | — | |
| `RadioGroup` | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | — | — | |
| `Toggle` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | Loading reflects in-flight side-effect. |
| `Slider` | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | — | |
| `Card` | ✅ | — | — | — | — | — | — | — | ✅ | Skeleton matches card dimensions; pulse 1.4s. |
| `Modal` | ✅ | — | — | — | — | — | — | — | — | First-focus child documented in modal's `context`. |
| `Toast` | ✅ | — | — | — | — | — | — | — | — | Live region; announces on appear. |
| `EmptyState` | ✅ | — | — | — | — | — | — | — | — | See empty-state taxonomy below. |
| `Skeleton` | ✅ | — | — | — | — | — | — | — | — | Is the loading variant for any component without a built-in loading state. |

Add a row for every new component as you add it. When a column is `—`, the project has explicitly decided that state isn't applicable; document why in the notes column.

## Visual recipes — the project's defaults

Project-specific renderings of the states whose visual language differs from the skill's reference defaults. Where this file is silent, the skill's defaults apply.

| State | Project recipe |
|-------|----------------|
| **Focus** | 2px outline `$focusRing` with 2px offset. *(Override if the brand specifies a thicker / colored ring.)* |
| **Hover** | Shift fill toward `$primaryMuted`; no `translateY`. We don't lift on hover anywhere. |
| **Pressed** | Instant `transform: scale(0.98)`; release on `$durationFast`. |
| **Disabled** | `opacity: 0.5`, `cursor: not-allowed`. Foreground stays readable (≥ 3:1). |
| **Error** | Border `$danger` (2px when paired with `:focus`), `circle-alert` icon (16px) at the end of the field, helper text in `$danger` below. |
| **Success** | Border `$success`, `circle-check` icon, helper text in `$success`. Decay to default after 2s for transient confirmation. |
| **Loading (button)** | Replace label with a 16px spinner in the button's foreground color. Preserve width. |
| **Skeleton** | `$surfaceMuted` fill, 1.4s shimmer per `motion.md`. Match loaded-content dimensions. |

Add overrides here if the brand or product calls for something specific (e.g. brand orange for focus, instead of `$focusRing`).

## Screen-level state coverage by archetype

Which fault and life-cycle states each page archetype must handle. Not every product needs every row; mark rows that apply with ✅ and delete the rest.

| Page archetype | Empty | First-use | No-results | Error (500) | Permission (403) | Offline | Loading | Notes |
|----------------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|-------|
| Auth (sign in, sign up) | — | — | — | ✅ | ✅ | ✅ | ✅ | Inline error under field is preferred over banner. |
| Dashboard | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | First-use shows skeleton tiles + "Connect a data source" CTA. |
| List + detail (e.g. inbox, projects list) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Each pane has its own empty/error states; partial-failure handled per-row. |
| Settings | — | — | — | ✅ | ✅ | ✅ | ✅ | Save errors are inline with the dirty section, not a top-page banner. |
| Detail page (single item) | — | — | — | ✅ | ✅ | ✅ | ✅ | 404 for "item doesn't exist"; 403 for "exists but you can't see it". |
| Marketing landing | — | — | — | ✅ (404 only) | — | — | — | 404 is the only fault state marketing pages handle. |
| Onboarding flow | — | — | — | ✅ | — | ✅ | ✅ | Offline state preserves draft answers and resumes when online. |

## Empty-state copy variants

The four empty-state taxonomies with the product's voice applied. Adapt these as the project's `voice.md` evolves; keep them parallel.

| Kind | Title | Description | CTA |
|------|-------|-------------|-----|
| **First-use** | Create your first `<thing>`. | `<One-sentence hook tied to the user's job.>` | New `<thing>` |
| **No-results** | No `<things>` match `<query/filter>`. | Try a different filter or search term. | Clear filters |
| **No-permission** | You don't have access to this `<scope>`. | Ask the workspace owner to invite you. | Request access |
| **Post-action** | You've handled everything. | `<Optional acknowledgment, ≤ 8 words.>` | (omit, or a low-priority secondary action) |

See [`voice.md`](voice.md) § Empty states for the full copy template, length rules, and the *lead with the next action, not the absence* principle.

## Project-level overrides

Place project-specific state decisions here. Examples (delete what doesn't apply):

- *"All async submission errors render as inline banners under the form, never as toasts."*
- *"We never use spinner-only loading on full pages — every page uses skeletons."*
- *"Destructive confirmations use a typed-confirmation pattern, not a checkbox."*
- *"Form errors persist until the user re-edits the field; they don't decay."*
- *"In our domain, 'archived' is a third state distinct from 'no results' and 'empty'."*

## Where this came from

Scaffolded by the [pencil-design skill](https://github.com/Nisus74/pencil-skill). Edit freely — the agent re-reads on each task.

## Not covered here

- Visual recipes for states beyond the project's defaults — see `references/states.md` in the skill.
- Motion timing for state transitions — see `motion.md`.
- Empty-state copy length rules and forbidden words — see `voice.md`.
- Component focus order and ARIA semantics — see `references/accessibility.md` in the skill.
