# States — components and screens

How to design every state a real product needs. Most AI-generated UIs ship the default state of every component and the happy path of every screen — and nothing else. This file fixes that.

**What this file owns:** the *vocabulary* and *visual recipes* for component-level interaction states (hover, focus, pressed, disabled, loading, error, empty, skeleton, success) and screen-level fault states (404, 403, 500, 503, 408, 429, offline, partial-failure). Plus the empty-state taxonomy.

**What this file does NOT own:** the page *layout* that contains the state (e.g. the Settings page shell). The *copy* that fills it — follow the project's voice guidelines or the copy patterns in this file's empty-state section. The *motion timing* of state transitions — define durations in your token suite (`$durationFast`, `$durationBase`, etc.).

## When to load this file

- The user asks for a 404, 500, offline, empty, error, or "edge case" screen.
- You're authoring a reusable component and need to confirm its required states.
- You're auditing an existing design that ships only default states.
- You're planning verification and want to know which state is the worst-case to screenshot.

If you're laying out a new dashboard or marketing page from scratch, you don't need this file yet — load it once you reach the state-coverage step of step 6 verification.

## Component states — the matrix

Every reusable component must declare these states before it's library-ready. This file covers the full matrix, with particular depth on the three states most commonly omitted: skeleton, in-component empty, and partial-failure.

| State | Required for | Visual recipe (defaults; let `tokens.md` override) |
|-------|--------------|----------------------------------------------------|
| **Default** | Everything | Resting fill / stroke / text per `tokens.md`. |
| **Hover** | Pointer-aware targets (buttons, links, cards-as-targets) | Color shift toward `$primaryMuted` *or* slight `transform: translateY(-1px)`. `$durationFast`. Gated behind `@media (hover: hover)`. |
| **Focus** | Every interactive element. Skipping this fails WCAG. | 2px outline using `$focusRing`, offset 2px. Visible against any surface in both modes. |
| **Active / Pressed** | Buttons, toggles, anything that registers a tap/click | `transform: scale(0.98)` *or* darker fill (one shade past `$primary`). Instant on press; release with `$durationFast`. |
| **Disabled** | Anything that can be inert | `opacity: 0.5`, `cursor: not-allowed`. Foreground stays legible (≥ 3:1 contrast) — don't drop opacity below 0.4 or labels become unreadable. |
| **Loading** | Buttons that submit, async controls, search inputs | Replace label with spinner; **keep the original width** so layout doesn't jump. Spinner uses `$textPrimary` on the component's surface. |
| **Error / Invalid** | Form inputs, validation-bearing controls | Border `$danger`, icon paired with the value (`circle-alert` or `circle-x` from the icon library), helper text in `$danger` below. Never red alone. |
| **Success** | Form inputs after async confirmation, toggle confirmation | Border `$success`, icon (`circle-check`), helper text in `$success`. Decay to default after ~2s for transient confirmations; persistent for committed state. |
| **Skeleton** | Anything that fetches before render | Muted-fill placeholder shape (`$surfaceMuted`), 1.4s shimmer per `motion.md`. Match the dimensions of the loaded content. |
| **In-component empty** | Lists / pickers / dropdowns inside a component (e.g. an autocomplete with no matches) | Single line of muted text inside the component bounds. *Different* from a screen-level empty — see § Empty state taxonomy below. |
| **Partial-failure** | Compound components rendering N items where some failed | The successful items render normally; the failed ones render a small inline error affordance (icon + retry) in their slot. |

For inputs specifically, also draw the **filled** state (with placeholder content replaced by user input) and the **focused-with-error** edge case (focus ring + error border simultaneously — the focus ring wins; error border thickens to 2px).

### State authoring in Pencil

Two conventions, pick one per project and stay consistent:

**Variant siblings inside a `reusable` component.** Each state is a sibling frame named with a suffix:

```
ButtonPrimary (reusable: true)
├── Button_Default
├── Button_Hover
├── Button_Focus
├── Button_Pressed
├── Button_Disabled
├── Button_Loading
└── Button_Error
```

The instance picks a sibling by `descendants` override or by `theme: { state: "hover" }` if you've added a `state` axis.

**`state` theme axis.** The `state` axis registers automatically once you declare state-conditional variable values via `set_variables`. No explicit axis-declaration step is needed. Bind state-conditional values on the component:

```
fill: [
  { value: "$primary",      theme: { state: "default" } },
  { value: "$primaryMuted", theme: { state: "hover"   } },
  { value: "$primaryDark",  theme: { state: "pressed" } }
]
```

Cleaner for products with a small, consistent state set. Heavier for components with many state-specific shapes (where variant siblings stay clearer).

**Naming.** When using variant siblings, suffix with `_StateName` in PascalCase: `Button_Hover`, `Input_Error`, `Card_Loading`. When using a theme axis, no naming change needed — the axis carries the meaning.

## Empty state taxonomy

There isn't one "empty state" — there are four. Each takes different copy, different CTA, different illustration.

| Kind | When it shows | Copy lead | Primary CTA |
|------|---------------|-----------|-------------|
| **First-use** | The user has never created/added the thing. The system is genuinely empty for them. | Imperative: *"Create your first project."* | A creation action: *"New project"*. |
| **No-results** | A filter or search returned nothing, but the underlying collection isn't empty. | Specific: *"No projects match 'archived'."* | A reset or refinement: *"Clear filters"* / *"Try a different search"*. |
| **No-permission** | The user doesn't have rights to see content that exists. | Honest: *"You don't have access to this workspace."* | A path forward: *"Request access"* / *"Contact admin"*. |
| **Post-action** | The user *did* the thing — inbox cleared, task list completed. | Acknowledging: *"You've reviewed all comments."* | Optional secondary action *or* nothing. Don't push for more work. |

Visual lockup (the same structure across all four):

```
EmptyState (centered in the empty container)
├── Illustration or icon  ($iconXl, $textMuted)
├── Title (1 line, $textXl, ≤ 8 words)
├── Description (1–2 lines, $textMuted)
└── Primary CTA (omit on post-action)
```

Don't stack multiple CTAs ("Import", "Create", "Explore demo"). Pick one. The exception: first-use empty states for products with a strong import path can pair `Create` with a secondary `Import` link below.

Copy rule for empty states: present tense, no exclamation marks, named action verb on the CTA. "No projects yet. Create your first one." not "Wow, it's empty here! Click below to get started."

## Loading taxonomy

Four loading shapes. Picking the wrong one is the most common loading mistake.

| Shape | When | Notes |
|-------|------|-------|
| **None** | The action completes in < 100ms. | The right answer surprisingly often. Don't add a spinner that flashes for 80ms — feels broken. |
| **Skeleton** | Initial load of a known-shape area (a list, a dashboard tile, a card). | Best for perceived performance. The placeholder approximates the loaded content's dimensions so layout doesn't jump. See `motion.md` § skeleton shimmer. |
| **Spinner** | Inline action that has no known shape (a submit button, an unknown-length async). | Single 1s rotation in the component's surface color. Don't wrap a skeleton around a spinner. |
| **Progress** | Long operation with measurable progress (upload, install, export). | A bar with a numeric % when known; an indeterminate bar when not. Indeterminate progress and a spinner do the same job — don't ship both. |

**Don't** show a full-page spinner for a partial update — render the rest of the page and let the in-progress region carry its own loading state. Full-page spinners are an AI default that mistakes "I don't know what to do" for "tell the user to wait."

### Loading state timing

The loading shapes above are the visual recipes; the *timing* rules live in [`interactions.md`](interactions.md) § Loading states. The short version: don't show a spinner before 150-300ms, and once shown, keep it visible for at least 300-500ms even if the operation completes. Without the floor, the spinner flashes and reads as broken.

## Onboarding states

The user's first encounter with the product. Onboarding states differ from empty states. Onboarding fires on the user's first encounter with the product. Empty states fire when a page has nothing to show after the product has been used.

| State | When it shows | Visual recipe |
|-------|---------------|---------------|
| **Welcome** | First launch after sign-up. Before any user data exists. | Full-screen takeover or centred modal. Brand voice, single primary action, optional 'skip' link. Don't gate; the user can always come back to onboarding from settings. |
| **Sample data** | The user wants to explore the product without creating their own data first. | A pre-populated workspace, project, or document with realistic content. Clearly marked 'sample' so the user knows it's for exploration. A 'Replace with my own' CTA stays visible. |
| **Coach marks** | Discoverable hints for non-obvious features (keyboard shortcuts, command palette, contextual menus). | Small floating cards anchored to the relevant UI element. Always dismissible. Never auto-show more than one at a time. Stop showing after 2-3 dismissals (the user knows). |
| **Loaded-with-suggestions** | The user has done one action; the product can now suggest the next. | Inline 'next steps' panel or a banner above the main content. Suggestions are specific to what the user just did. Generic 'next steps' don't earn their space. |

The visual lockup matches what empty states use (illustration + title + description + CTA). The trigger is different: onboarding fires on first visit only.

Don't combine all four. A welcome modal + sample data + coach marks + suggestions all firing on the first visit overwhelms the user. Pick the one or two that genuinely help.

## Settings states

Settings have their own state vocabulary distinct from generic forms. The dominant pattern is autosave; explicit-save is the exception.

| State | When it shows | Visual recipe |
|-------|---------------|---------------|
| **Saved** | The default. Values persist on change. | No special indicator. The absence of an 'unsaved' marker is the signal. Optional 'Last saved 2 minutes ago' timestamp for the user's reassurance. |
| **Saving** | In flight, between user change and server confirmation. | Subtle indicator near the field or in the page chrome: small spinner + 'Saving...' text. Don't block the rest of the form. |
| **Saved-just-now** | Transient state after a successful save. | A check-mark icon next to the field for ~2 seconds, then decay to default. Or a non-blocking toast: 'Saved.' Pick one based on how prominent the change was. |
| **Dirty** | For explicit-save forms only. The user has changed values; nothing's been saved yet. | A 'Save' button enables; an 'Unsaved changes' indicator appears in the page chrome. The browser's beforeunload warning fires on navigation. |
| **Validation** | The user entered something invalid. Save is blocked until they fix it. | Inline error next to the offending field (per [`forms.md`](forms.md) § Error display). The Save button stays visible but indicates blocked: tooltip on hover explains why. |
| **Conflict** | Another session (another device, another user) changed the same setting since the user opened this page. | Banner above the form: '<Other user> changed this setting <time> ago. <View their version> or <Save anyway>.' Force a conscious choice; don't silently overwrite. |

The conflict state is rare but critical for collaborative or multi-device products. Without it, the last save wins silently and the user's history quietly disappears. The conflict banner forces a conscious choice.

Per `assets/design-system/patterns.md` § Settings page (when populated), each settings section in the project commits to one save pattern (autosave or explicit). The states above apply to whichever pattern was chosen.

## Screen-level fault states

When something has gone wrong at a system level — not a single component — the page itself becomes the state. Every product should have a coherent answer to each of these.

| Code | What happened | What to render | What NOT to render |
|------|---------------|----------------|---------------------|
| **404** | The URL/route doesn't exist | Friendly title (*"This page doesn't exist."*), suggested action (*"Go home"*, *"Search"*), one illustration | Stack traces, full URLs of broken routes, "the dev team has been notified" filler |
| **403** | The user is authenticated but not authorized | *"You don't have access to this page."*, path forward (*"Request access"*, *"Contact admin"*, *"Sign in as a different user"*) | The thing they can't see (no titles or counts that leak permission-protected info) |
| **500** | Server error, unrecoverable in this request | *"Something went wrong on our end."*, retry button, error code (small, beneath the message — for support, not for the user to read aloud) | The literal exception message, internal stack traces |
| **503** | Service is up but unavailable (maintenance, deploy) | *"We're updating something."*, ETA if known, status-page link | Vague *"please try again later"* with no information |
| **408** | Request timed out | *"That took too long."*, retry, with a "things to try" list (check connection, simpler request) | A generic spinner that re-tries indefinitely |
| **429** | Rate-limited | *"You're going faster than we can keep up."*, when they can try again, plan-upgrade path if applicable | Punitive language (*"You've been blocked"*) for a recoverable state |
| **Offline** | Connection lost | Banner *or* takeover, depending on severity (see § Offline & connectivity below) | A modal that blocks recovery — they can't dismiss it without reconnecting |
| **Partial-failure** | Some panels of a page errored, the page itself works | The successful regions render normally; the failed regions render an inline error block with retry | A page-wide error wall when only one widget broke |

### Page-level lockup for a screen-level error

Same general structure across most error pages — copy and code differ:

```
ErrorPage (centered, full viewport)
└── ErrorBlock (max-width 480, centered, padding $space-8)
    ├── Visual (icon $iconXl in $textMuted, OR a small illustration in muted color)
    ├── Title ($text2xl) — concrete, not generic
    ├── Description ($textMuted, 1–2 sentences) — what happened, what they can do
    ├── Primary CTA — Retry / Go home / Sign in
    └── Footer (very small, $textXs $textMuted) — error code, if applicable
```

Build it from the same primitives as the empty-state lockup. Most products do not need a custom illustration per error code — a single muted glyph with code-specific copy reads coherent and ages well.

### Authoring screen errors in Pencil

Sibling top-level frames, one per error kind, sharing one `ErrorBlock` component:

```
404Page    (LoginPage's sibling)
500Page
OfflinePage
```

Each instantiates the same `ErrorBlock` component via `ref` with `descendants` overrides for title / description / icon / CTA. The component lives in your `.lib.pen` once and gets a one-off variant per page. Don't duplicate the lockup.

For a worked example see [`assets/examples/example-error-screen.md`](../assets/examples/example-error-screen.md).

## Offline & connectivity

Three flavors, picked by severity:

- **Banner** (non-blocking) — when the page is still useful read-only, surface a small banner at the top: *"You're offline. Changes will sync when you reconnect."* The banner uses `$warning`, sticks to the top of the viewport, dismisses on reconnect.
- **Inline indicator** — for a single in-progress write that's stuck offline, show a small spinner-with-cloud-slash on the affected control with hover text: *"Will sync when online."* Don't block the rest of the page.
- **Takeover** — when the page can't function offline at all (live collaboration, real-time data), full-screen takeover with a connection-state illustration, a manual retry, and a link to a status page if applicable. The takeover is dismissible — don't trap the user in a blocking modal they can't exit.

**Pending-write reconciliation.** When the user makes changes while offline and the connection returns, show a small, non-blocking indicator near the affected content (*"3 changes synced."*) instead of a celebratory toast. Quiet success is the right tone for connectivity.

## Verification — which state to screenshot

Per the verification ladder in SKILL.md, screenshots are expensive. When you do reach for one to confirm a stateful design, screenshot the **worst** state — typically the error or disabled state — not the default. The default is what the model has been staring at; the failure state is where breaks hide:

- For a form, screenshot the **error** variant (focused-with-error edge case if the design has one).
- For a list, screenshot the **empty** state (first-use lockup, since it has the most surface).
- For an error page, screenshot the **page** itself, not the doc root.
- For a button library, screenshot the **disabled** variant — contrast issues live there.

If a state is built from variables and the design is theme-aware, the variable system guarantees mode parity — don't burn a second screenshot in the alternate mode unless something visibly mode-conditional is present.

## Anti-patterns

These read as state-blind designs and should be fixed in passing whenever you see them:

- **Shipping only the default state.** A button library with only `Default` is unfinished, regardless of how good the default looks.
- **Disabled states with `opacity: 0.3` or lower.** The label becomes unreadable; you've shipped an inaccessible state in the name of "muting" it.
- **Focus rings that disappear on dark backgrounds** (or on light ones, if light is your secondary mode). Always test focus contrast in both modes.
- **Loading states that change layout dimensions.** A button that grows or shrinks when its label becomes a spinner forces a reflow on every async submission.
- **Generic *"An error occurred"* copy.** Says nothing, helps no one. Match the error's specificity in the message.
- **Empty states that lecture.** *"Get started by creating your first item! Items help you organize..."* — cut to the action.
- **Multiple CTAs in an empty state.** Pick one.
- **Page-wide error walls when one widget broke.** Render the working parts, contain the error.
- **Modal-only offline takeovers with no manual retry.** The user is now stuck.

## See also

- [`accessibility.md`](accessibility.md) — focus states, disabled-contrast minimums, error-not-color-alone rule.
- [`assets/examples/example-error-screen.md`](../assets/examples/example-error-screen.md) — worked walkthrough of a 404 + offline pair.
