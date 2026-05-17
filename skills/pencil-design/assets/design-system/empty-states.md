# Empty states

Per-surface empty-state catalogue. The agent reads this when designing any surface that can render with no data, no matches, no permission, or after the user's cleared everything out.

This file extends [`states.md`](states.md) § Empty-state copy variants and [`voice.md`](voice.md) § Empty states. The pencil-design skill's `references/states.md` § Empty state taxonomy distinguishes four kinds: first-use, no-results, no-permission, post-action. This file maps each kind to specific copy and visual treatment for every primary surface in the project.

The catalogue here is the project's commitment. The taxonomy itself lives in the skill, so don't restate it; record the surface-specific copy here.

## Visual lockup

Per `references/states.md`, the visual lockup stays consistent across all empty kinds:

```
EmptyState (centred in the empty container)
├── Illustration or icon  ($iconXl, $textMuted)
├── Title (1 line, $textXl, ≤ 8 words)
├── Description (1-2 lines, $textMuted)
└── Primary CTA (omit on post-action)
```

Spacing is fixed by the `EmptyState` component in [`components.md`](components.md). Don't override the internal padding per surface; the centred container already handles it.

Illustration approach for this project: `<custom illustration per surface | system icon $iconXl in $textMuted | small illustration in muted brand colour>`.

## Per-surface empty states

Fill in for each primary surface in the project. Replace the `<placeholders>`. The rows below cover common SaaS surfaces; add or remove per project.

### Projects list (or main collection)

| Kind | Trigger | Title | Description | CTA | Illustration |
|---|---|---|---|---|---|
| First-use | New workspace, no projects | `Create your first project` | `Projects organise your work and let you collaborate with your team.` | `New project` (primary) | `<icon: folder-plus, or custom>` |
| No-results | Filter applied, no matches | `No projects match '<filter>'` | `Try a different filter or clear all filters.` | `Clear filters` (secondary) | `<icon: search>` |
| No-permission | User lacks access | `You don't have access to this workspace's projects.` | `Ask the workspace admin for access, or switch to a workspace you're in.` | `Request access` or `Switch workspace` | `<icon: lock>` |
| Post-action | All projects archived | `You've archived all projects.` | `Restore one from the archive or create a new project.` | `View archive` (secondary) | `<icon: archive>` |

### Inbox / messages

| Kind | Trigger | Title | Description | CTA |
|---|---|---|---|---|
| First-use | No messages ever | `Your inbox is ready.` | `Notifications, mentions, and messages will appear here.` | `Notification settings` (secondary) |
| No-results | Filter applied | `No messages match '<filter>'` | `Try a broader filter or change the time range.` | `Clear filter` |
| Post-action | All read or archived | `You're all caught up.` | `<optional: time saved estimate>` | (none) |

### Search results

| Kind | Trigger | Title | Description | CTA |
|---|---|---|---|---|
| No-results | Search returned nothing | `No results for '<query>'` | `Try a broader search, check spelling, or browse all <items>.` | `Browse all` (secondary) |
| Pre-search | Empty search input | `What are you looking for?` | `Search across <projects, files, people, ...>` | (none) |

### Settings (per section)

| Kind | Trigger | Title | Description | CTA |
|---|---|---|---|---|
| First-use | No integrations connected | `Connect your first integration.` | `Integrations let you bring data from other tools into <product>.` | `Browse integrations` |
| No-permission | User isn't admin | `Only workspace admins can change billing settings.` | `Contact your workspace admin to make changes.` | (none) |

### Add more surfaces here

Each primary surface in the product gets its own table. Surfaces that need empty states: project lists, item lists, file browsers, members lists, audit logs, anything the user might land on with nothing yet.

If a surface has more than one route into it (e.g. an inbox you can also reach via a notification deep-link), the empty state stays the same. The trigger column in the table is what differs, the copy doesn't.

## Copy rules

- **Title leads with the action,** not the absence. `Create your first project.` beats `No projects yet.`
- **Description guides,** doesn't restate. The description tells the user what'll happen if they take the action.
- **CTA repeats the action verb** from the title. `Create your first project.` → CTA: `New project`.
- **One CTA per empty state.** Three competing actions paralyse the user. Pick the one most users do first.
- **Filtered-empty differs from first-use empty.** Name the filter. Offer a way to clear it.
- **Post-action empties acknowledge,** they don't push another task. `You're all caught up.` is a full thought.

## Illustration approach

The project commits to: `<custom per surface | one library across all surfaces | icon-only for compactness | photographic for marketing-adjacent surfaces>`.

If custom: each surface's illustration matches the brand voice. Illustrations live at `<asset path>`.

If icon-only: use `$iconXl` from `tokens.md`, in `$textMuted`. The icon family is in `iconography.md`.

Whichever route you pick, stay consistent across surfaces. Mixing custom illustration with stock icons signals an unfinished design system.

## See also

- [`states.md`](states.md): the empty-state taxonomy this file extends (first-use, no-results, no-permission, post-action).
- [`voice.md`](voice.md): the copy tone and length rules.
- [`tokens.md`](tokens.md): `$iconXl`, `$textMuted`, `$textXl` values.
- [`iconography.md`](iconography.md): the icon family choice.
- `references/states.md` (in the pencil-design skill): the canonical empty-state taxonomy.
- `references/microcopy.md` (in the pencil-design skill): § Empty state copy patterns.
