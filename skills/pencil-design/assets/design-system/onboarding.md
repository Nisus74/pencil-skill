# Onboarding

The project's first-run experience pattern. The agent reads this file when designing or auditing the new-user flow. It complements `references/flows.md` § Onboarding flows (the menu of patterns) and `references/states.md` § Onboarding states (the visual recipes).

## Onboarding shape

The project commits to: `<sign-up to first action (no intermediate screens) | sign-up to guided onboarding to first action | hybrid (guided on first sign-up, skippable)>`.

Use case fit:
- **No intermediate screens** suits products where the first action is obvious (a writing app opens a blank document; a chat app drops the user into chat).
- **Guided onboarding** suits products with significant setup (CRMs, project-management tools, analytics platforms).

## With sample data vs blank slate

`<sample data only | blank slate only | both options offered>`.

Recommended: offer both. The sign-up flow asks 'Would you like to start with sample data, or set up your own workspace?' and routes accordingly.

- **Sample data**: pre-populated workspace, project, or document with realistic example content. Clearly marked 'sample' with a 'Replace with my own' CTA visible.
- **Blank slate**: empty workspace with a clear first-action prompt.

## Sequence

The project's specific onboarding sequence (placeholder). E.g.:

1. Sign-up form (email + password, or OAuth).
2. Email verification (if required by compliance).
3. Workspace name.
4. Role selection (`<roles list>`).
5. Sample data offer (yes / no).
6. First-action prompt: `<create your first project | invite your team | connect an integration | etc.>`.

Each step has a Skip option except the strictly required (auth, terms acceptance).

## Welcome modal vs full-takeover

Per `references/states.md` § Onboarding states: Welcome state is `<full-screen takeover | centred modal | inline banner>`. Brand voice; single primary action; optional 'skip' link.

The user can return to onboarding from `<settings | help menu | empty state>`.

## Coach marks

`<used | not used>`.

If used: small floating cards anchored to the relevant UI element. Always dismissible. Never auto-show more than one at a time. Stop showing after 2-3 dismissals (the user knows the feature exists).

Coach marks live for: `<feature 1, feature 2, ...>`. Each one earns its place by surfacing a non-obvious feature (keyboard shortcut, command palette, contextual menu).

## Loaded-with-suggestions

After the user's first action, the product surfaces 'next steps':

- Inline 'next steps' panel or a banner above the main content.
- Suggestions are specific to what the user just did. Generic 'getting started' lists don't earn their space.

Example: user creates first project. 'Next steps' panel suggests:
- Invite a teammate
- Add a board
- Connect Slack

## Sample data details

If the project ships sample data:

- **Realism**: names, dates, and content match the product's domain. Not 'John Doe' / 'Project Apollo' / 'Lorem ipsum'.
- **Clearly marked**: every sample item has a 'Sample' tag or muted styling so the user knows it's not theirs.
- **Replaceable**: a 'Replace with my own' CTA visible in the workspace; clears sample data and prompts for real input.
- **Self-contained**: deleting sample data shouldn't break references or leave orphans.

## Empty-with-CTA fallback

If the user skips onboarding (or onboarding is the no-intermediate-screens type), the empty state of every primary surface acts as inline onboarding. See `empty-states.md` for per-surface copy.

## Skip and exit affordances

- Skip per step is `<text link 'Skip' bottom-right | secondary button next to primary>`.
- Skip-all (from any step) returns to a sensible default (usually empty state of the primary surface).
- Exit confirmation `<required | not required>`. Required when the user has entered data they'd lose.

## Progress indication

Per `references/flows.md` § Multi-step forms § Step indicator: `<stepper for ≤ 5 steps | progress bar for 6+ steps | step counter for simple flows>`.

Mark current, completed, and upcoming steps visually distinct.

## Time expectation

The product tells the user how long onboarding takes. Examples:
- 'Set up takes about 2 minutes.'
- 'You can finish this in under 60 seconds.'

Honesty matters; the user adjusts their patience accordingly.

## Save-progress on exit

If the user exits mid-onboarding, the project commits to: `<silently persist progress and resume | clear and restart on next launch | offer 'Save and finish later' explicitly>`.

Default: silently persist. Asking 'Save your progress?' on exit feels like a chore; restoring on return feels like care.

## Re-onboarding for changes

Major product changes: surface re-onboarding via `<release notes modal | first-launch banner after upgrade | dismissible coach marks per changed feature>`.

Don't force re-onboarding on every login.

## Mobile considerations

If the product ships on mobile:
- Onboarding screens use full-screen takeovers (modals don't fit well at smaller widths).
- Permission prompts (notifications, camera, location) appear in onboarding context, not just-in-time during the first relevant action. The project commits one or the other.
- Biometric setup (Face ID, Touch ID, fingerprint) offered after primary auth, not before.

## Accessibility

- Every onboarding step is keyboard-reachable.
- Focus moves to the next step's primary input on Next.
- Screen reader announces step changes via `aria-live="polite"`.
- Skip links present on every step.
- Coach marks dismissible by Esc key.

## Verification checklist

Before declaring onboarding done:

1. Walk through the full sequence as a new user. Note any friction.
2. Try Skip on every step. Ensure the user lands somewhere usable.
3. Try Back on every step. Ensure values preserved.
4. Refresh mid-onboarding. Ensure progress restored.
5. Walk through with sample data. Ensure realism and clear 'Sample' marking.
6. Walk through blank slate. Ensure empty states guide the user.
7. Test keyboard-only flow. Every step reachable; focus moves correctly.
8. Test screen reader. Step changes announced.

## See also

- `references/flows.md` (in the pencil-design skill): § Onboarding flows (sign-up patterns, sample data vs blank).
- `references/states.md` (in the pencil-design skill): § Onboarding states (welcome, sample data, coach marks, loaded-with-suggestions).
- `references/microcopy.md` (in the pencil-design skill): empty state copy patterns also apply to first-action prompts.
- `empty-states.md`: per-surface empty states the user lands on after skipping or finishing onboarding.
- `voice.md`: tone for welcome, encouragement, skip copy.
- `patterns.md`: the page layouts onboarding screens use.
- `accessibility.md`: keyboard, focus, screen reader patterns for stepped flows.
