# Flows — transitions, validation, state across screens

How users move between screens and how state behaves across that movement. AI-generated UIs are typically static page snapshots; this file fills in everything that happens in between.

**What this file owns:** modal-vs-page-vs-sheet decisions, form validation timing, multi-step flows and wizards, the back-stack model, confirmations and undo, optimistic UI, real-time/presence flows, deep links, and "plausible content" — what real-shape data looks like in mocks.

**What this file does NOT own:** the *layout* of any single page (auth flow, onboarding, settings, dashboard, list+detail). The *motion* of a transition (durations, easings). The *copy* in error/confirmation states. The *mobile-specific* sheet/back-gesture conventions.

This file covers what happens *between* steps — the transitions, validation events, and state changes. Layout, motion, and copy are handled in project-level documentation or the project's own design guidelines.

## When to load this file

- The user asks for a multi-step form, wizard, signup, onboarding, or "flow" that crosses screens.
- The design has validation timing decisions to make (sync, async, on-blur, on-submit).
- The design uses modals, sheets, popovers, or any overlay — and you need to pick which.
- Real-time or presence affordances are involved (live cursors, typing indicators, conflict resolution).
- The design has destructive or confirmable actions.
- You're filling in plausible content for a list / table / dashboard mock.

## Modal vs page vs sheet vs popover

The four overlay/navigation choices and when to pick each.

| Surface | Use when… | Don't use when… |
|---------|----------|----------------|
| **Page (route)** | The task is a primary destination. The user expects deep-linkability. They might bookmark or refresh and return. | The task interrupts a parent flow — pushing to a new page loses context the user wants back. |
| **Modal (centered overlay)** | The task is small, focused, and a hard interruption — confirmation, single-form-edit, image preview. The user must complete or dismiss it before continuing. | The task is multi-step or might be paused (a modal that's closed loses its work). The content has its own URL the user might want to share. |
| **Sheet (edge-anchored)** | The task is a drilldown that retains context — filters, share, secondary edit. Mobile by default. | The desktop counterpart would be a separate page. Mixing modal-on-desktop / sheet-on-mobile for the *same* task is fine; sheets where pages would be better is not. |
| **Popover (small floating)** | A single inline action, hint, or short form (≤ 3 fields). Anchors to an element. | The content needs the user's full attention. Popovers steal focus poorly and dismiss too easily. |

**Decision shortcuts:**

- "Edit this user's profile" → page (deep-linkable, multi-section).
- "Are you sure you want to delete?" → modal (interruption with finite outcomes).
- "Filter this list" → sheet on mobile, popover on desktop.
- "Add a comment" → inline form below the comments list, OR popover from the comment button. Not a modal.
- "Share this document" → sheet/popover (anchor to a Share button).

**Don't combine modal patterns.** A modal that opens another modal is layered focus traps that confuse keyboard users and screen readers. If a modal needs to launch a sub-task, either close the modal first or design the sub-task as inline content within the existing modal.

## Form validation timing

Three validation moments, each with a default behavior:

| When | Default behavior | Use for |
|------|------------------|---------|
| **As the user types** | Don't validate. Don't show errors. | Don't shame the user mid-keystroke. |
| **On blur (the user leaves the field)** | Run sync validation. Show inline error if invalid. | Format checks (email shape, phone shape, password strength). |
| **On submit** | Run any remaining validation, including async/server. Show field-level errors and (only if multi-field) a summary banner. | Cross-field validation, server checks (email already taken, username available). |

Two extra patterns worth knowing:

**Async validation with debounce.** When a check requires a network call (is this username available?), debounce the blur — wait ~400ms after the user stops typing to fire the request. Show a small loading indicator on the field during the in-flight request, then resolve to error / success. Don't block submission while in-flight; if the user submits before the async returns, fall back to on-submit handling.

**Submit-time validation summary.** For long forms (≥ 6 fields), pair field-level errors with a small summary banner at the top: *"Fix 2 errors before continuing."* Each error in the summary links (focuses) to its field. Skip the banner for short forms — one error inline is plenty.

**Errors decay or persist?** Persist until the user edits the offending field. As soon as they re-enter the field and start changing it, clear the error. Don't auto-decay errors on a timer — that hides information the user needs.

For copy, follow the *what happened. what to do.* template: name the problem concisely, then state the resolution action.

## Multi-step forms / wizards

A wizard is a sequence of screens that share state. Every wizard has the same anatomy:

```
Wizard
├── Progress indicator (top)
├── Step content (center)
│   ├── Step title
│   ├── (Optional) Helper text
│   └── Form / choices for this step
└── Footer (Back left, Continue right; final step uses a specific verb e.g. "Create account")
```

Decisions:

**Step indicator.** Three shapes — pick one per product:

- **Stepper (numbered circles, dots, or labels).** Best for 2–5 steps where the user can see the destination. Mark current, completed, and upcoming visually distinct.
- **Progress bar.** Best for 6+ steps or when the count varies per user. Less precise but lighter weight.
- **Step counter** (*"Step 2 of 4"*). Pair with either of the above, or use alone for very simple flows.

**Allow-back, lock-forward.** The default: users can go back to any prior step and edit. Steps that take a while or commit work (a payment confirmation, a server call) can lock forward — once committed, the user can't return to that step. Surface the lock visibly: a "✓ Confirmed" badge instead of a back chevron.

**Save-progress vs reset-on-leave.** Default: save progress so the user can return and pick up. Don't ask the user *"Save your progress?"* on leave — silently persist. The exception: flows with sensitive intermediate data (payment forms, KYC steps) should explicitly clear on leave.

**Confirmation step (final step).** Anatomy differs from form steps — it's a summary, not an input. The structural pattern is: break the card shape used in earlier steps, show a resolution icon (not a form field), and use a single CTA. The confirmation step's CTA uses a specific verb tied to the outcome: *"Create account"*, *"Place order"*, *"Submit application"*. Not *"Submit"*. Not *"Confirm"* alone.

**Skip non-essential steps.** Every step that isn't strictly required should have a Skip option. A flow that forces seven decisions before first use loses users. Be honest with yourself about which steps actually block and which are aspirational.

## Onboarding flows

The user just signed up. Two goals are at play: the user wants to reach the product's core value as quickly as possible, and the product needs to build enough familiarity that the user returns.

Two patterns dominate, picked by the product's complexity:

- **Sign-up → first action.** The user lands directly on the product after sign-up. No intermediate screens. Works for products where the first action is obvious (a chat app drops the user into the chat; a writing app opens a blank document). The product itself is the onboarding.
- **Sign-up → guided onboarding → first action.** Two to four short screens between sign-up and the product. Each screen makes one decision (workspace name, role, integrations). The user lands in the product with the workspace pre-configured. Works for products with significant setup (CRMs, project management tools, analytics).

Either way, design for two paths through onboarding:

- **With sample data.** The user lands in a pre-populated workspace with realistic example content. They can explore without committing. A 'Replace with my own' CTA stays visible. Right for products where the value is hard to see in an empty state (analytics dashboards, project boards, design tools).
- **Blank slate.** The user lands in an empty workspace with a clear first-action prompt. Right for products where the user already knows what they're making (writing apps, single-purpose utilities).

Most products benefit from offering both. The sign-up flow asks 'Would you like to start with sample data, or set up your own workspace?' and routes accordingly. The product doesn't need to commit to one shape.

For onboarding state visual recipes (welcome, sample data, coach marks), see [`states.md`](states.md) § Onboarding states. For onboarding microcopy patterns (encouraging, action-led), see [`microcopy.md`](microcopy.md) § Empty state copy.

## Settings flows

Settings have their own flow patterns distinct from forms. The dominant pattern is autosave; explicit-save is reserved for high-stakes changes.

**Autosave (default).** The user changes a value, the value persists immediately. No Save button. Visual feedback: a brief 'Saved' indicator (per [`states.md`](states.md) § Settings states), then back to ambient. Right for: profile fields, preferences, notification toggles, display options.

**Explicit-save (high-stakes only).** The user changes values; a Save button collects them. Right for: billing, security, anything compliance-sensitive, settings that fan out to other systems (webhook URLs, API keys). The form has a clear dirty state; the browser warns on unsaved navigation.

Per-field vs form-level autosave:

- **Per-field autosave** (the modern default) saves each field independently as the user blurs or toggles. Faster feedback. Risk: partial saves where the user wanted to coordinate multiple changes. Mitigation: optimistic UI with rollback, plus a 'Recent changes' panel for review.
- **Form-level autosave** (the older pattern) saves the whole form on a debounce after any change. Slower feedback but coherent. Risk: the user makes one change and waits 2 seconds for confirmation. Mitigation: shorten the debounce; surface the in-flight state.

Most B2B SaaS uses per-field autosave for routine settings and explicit-save for the high-stakes set.

For the conflict state (another session changed the same setting), see [`states.md`](states.md) § Settings states.

## Search flows

Search is its own flow with its own decisions. The first decision: instant search or submit-driven?

**Instant search.** Results update as the user types (debounced ~150-300ms). The search bar is the entry; results appear inline below or in a panel. Right for: known-item search (the user knows what they're looking for), autocomplete, filtering. Examples: Linear command palette, GitHub repository search, macOS Spotlight.

**Submit-driven search.** The user types a query and presses Enter. Results appear on a results page. Right for: exploratory search (the user is browsing), search that crosses many sources, search that requires server-side processing. Examples: Google, e-commerce product search, Notion's search modal.

Many products combine both: instant suggestions appear as the user types (top 5 matches, plus categories like 'Recent searches', 'Suggested searches'); pressing Enter takes the user to a full results page.

**Results vs suggestions.** Suggestions are the dropdown of what the system predicts the user means. Results are the page of what the system actually found. They can coexist: suggestions appear instantly as the user types, results appear after the user presses Enter.

**Empty results state.** When a search returns nothing, the empty state should: name the query, suggest refinements ('Try a broader search', 'Check spelling'), offer a fallback action ('Browse all', 'Contact support'). Don't just say 'No results' and leave the user stuck. See [`microcopy.md`](microcopy.md) § Empty state copy and [`states.md`](states.md) § Empty state taxonomy.

**URL state.** Search queries belong in the URL. A user who refreshes the page should see the same results. The query is shareable and bookmarkable. See § Deep links & shareable URLs below.

For the search results layout (instant dropdown, results page), see [`layout-patterns.md`](layout-patterns.md) § Settings pages (search-driven variant) and dashboard layouts.

## Back-stack & navigation model

Web and mobile use different mental models — designs that ignore the difference produce navigation that feels broken on one platform.

**Web (browser router).**

- Back button = navigate to previous URL. Forward = next URL. The browser keeps the stack.
- A `pushState` adds to the stack; `replaceState` swaps the current entry. The choice matters for sharing — modals should use `replaceState` (they shouldn't show up in history); page navigations should use `pushState`.
- Refresh restores the current URL's state; anything not encoded in the URL is lost. So: filters, selected tab, sort order *should be* in the URL. Modal-open / dirty-form-state *should not be*.

**Mobile (native nav stack).**

- Back gesture (iOS edge swipe, Android system back) pops the top of the stack. On iOS, this is interruptible mid-swipe.
- Modals stack independently — they don't add to the page nav stack but to a separate modal stack.
- Tab bar tabs each have their own nav stack — switching tabs preserves each tab's state. Don't reset a tab's stack when the user switches away and back.

**Design implications:**

- **Don't intercept the back action.** A custom "Are you sure?" modal on every back press is hostile. Reserve back-confirmation for forms with significant unsaved work, and even then — preserve and restore is usually better than confirm.
- **Modal opens shouldn't break back.** On web, opening a modal should not push history (so back closes the modal, not the page). Use `replaceState` when the modal opens; `replaceState` again when it closes.
- **Wizards use the back button to step backward.** A 4-step wizard has 4 entries in browser history. Browser back goes to the previous step, not all the way out of the wizard.
- **Mobile: preserve scroll position on back.** When the user backs out of a detail page to a list, the list should be scrolled where they left it, with the row they were viewing still in view.

In Pencil, document navigation choices in the document or page-level `context`: *"Routed page. Back returns to projects list with scroll preserved."* The engineer reads this and knows what to ship.

## Confirmations & undo

For destructive or irreversible actions, two patterns:

**Hard confirmation (modal).** A modal that names the thing being destroyed and the consequence:

- *"Delete project 'Acme Marketing'?"*
- *"This will permanently remove all 23 boards and cannot be undone."*
- Buttons: *"Delete project"* (destructive variant) on the right; *"Cancel"* (secondary) on the left.

Use for: account deletion, subscription cancellation, irreversible data loss, anything compliance-sensitive.

**Soft confirmation with undo (toast).** Action commits immediately. A toast appears: *"Comment deleted. [Undo]"* — sticking around for ~5 seconds.

Use for: routine deletions (a comment, a row, an item), anything reversible. Less friction; reduces cumulative UX cost of repeated similar actions.

**Decision rule:** if undoing is *possible* (the system can restore the prior state) and the action is one of many in a session, prefer soft. If undoing is impossible or the action is rare and high-consequence, prefer hard. Don't do both — picking *neither* (commit silently) is also fine for low-stakes, frequent actions like archiving.

**Typed confirmation.** For the most consequential actions (deleting an org, dropping production data), require typing a string: *"Type 'delete acme' to confirm."* Reserve for the top tier.

Copy rule: name the thing being destroyed specifically ("Delete the Acme workspace" not "Delete this item"), use present-tense actionable verbs ("Delete permanently" not "Proceed"), and keep destructive CTAs short.

## Optimistic UI

When to apply optimism:

- The action is high-confidence (it almost always succeeds — toggling a setting, marking a task done, liking a post).
- The user does the action many times per session.
- The cost of being wrong is low (rollback is graceful and the user can re-try).

When NOT:

- The action is high-stakes (payment, data destruction).
- Failure is common (a flaky network is going to roll back often, which feels worse than a brief loading state).
- The action's success affects what other UI shows (e.g. an item appearing in a list — optimistic add looks fine, optimistic move can desynchronize).

**Visual recipe.**

- **Pending state.** The optimistically-updated UI element gets a subtle visual treatment — e.g. a slightly muted opacity, a tiny "syncing" dot. Don't make it ugly; the user shouldn't feel doubt.
- **On success.** The pending visual decays — usually within ≤ 200ms after the server confirms. No celebratory toast for routine actions.
- **On failure.** Roll back the UI to its pre-action state, show a non-blocking error toast: *"Couldn't save your change. Try again."* Don't surprise-modal the user out of context.

In Pencil, document the optimism in the component's `context`: *"Optimistic toggle. Reflects the new state instantly; reverts and shows a toast on failure."* The engineer ships the rollback logic.

## Real-time / presence flows

When multiple users see and edit the same content, the design needs additional affordances:

**Active user presence.**

- Avatar pile (3–5 visible avatars + "+N" overflow) showing who else is here.
- Avatar color outlines on cursors and selections to attribute action to user.
- A small "typing" indicator when relevant (chats, collaborative comments).

Place the avatar pile in the page chrome (top-right by convention), not inline. Live cursors only render in surfaces that genuinely benefit (a shared document, a whiteboard) — don't render them in dashboards or settings.

**Live updates.**

- New items appearing from another user: animate in with a subtle `$durationBase` slide+fade. Don't reflow the user's current scroll position.
- Items being edited by another user: show a subtle highlight (a 1px border in the editor's color) for 2–3 seconds, then decay.
- Items being deleted: animate out *only* if the user can see them; otherwise just remove silently.

**Conflict indicators.** When two users edit the same content simultaneously:

- For text: show a subtle banner *"<Name> is also editing this section."* Don't lock — let the engineering layer pick conflict resolution (CRDT, last-write-wins, etc.).
- For lists: show edits inline as they happen. Mark someone else's selection clearly so the user doesn't accidentally fight over the same row.
- For settings: usually settings shouldn't be co-edited; surface a *"Last saved by <user> a moment ago"* indicator if the user comes back to a stale view.

**Activity timeline.** For products with significant edit history, a "what changed" view is its own page or sidebar — not a notification stream. Group by author, by time, by document section. Don't bombard the user with every keystroke.

Motion rule for presence affordances: join/leave transitions should be fast (150–200ms) and unobtrusive — a fade or a brief slide. Don't animate cursor movements in real-time; sample at 100–200ms intervals or the UI becomes visually noisy.

## Plausible content

Mocks live or die on the believability of their content. AI defaults are tells:

- *"John Doe", "Jane Smith", "Acme Corp", "Lorem Ipsum"* — generic names.
- *"$1,234.56 — Premium Subscription"* — round numbers in suspicious patterns.
- *"99% accuracy", "trusted by 10,000 teams"* — fabricated metrics.
- *"Project Apollo", "Project Phoenix"* — placeholder project names.

What plausible looks like, by surface:

| Surface | Plausible content shape |
|---------|------------------------|
| Inbox / list of messages | Real-shape subjects (5–10 words, varied lengths). Real-shape senders (mix of full names and email-only). Timestamps that vary (mostly recent, a few older). |
| Dashboard tiles (KPIs) | Real-shape numbers — not all multiples of 10. Some increased, some decreased. Sparkline data with believable noise. Dates that anchor in the recent past. |
| Project / document list | Names that match the product's domain (a design tool: "Q4 Brand refresh", "Mobile nav exploration"; a finance tool: "Revenue analysis 2026", "Budget — engineering"). |
| User list (admin) | Real-shape names (mix of cultures, name lengths). Real-shape emails (varied domains, not all `@example.com`). Mix of join dates. |
| Activity feed | Mix of action types. Realistic time clustering (more activity during working hours). Some entries with detail, some terse. |
| Tags / labels | Domain-specific (a CRM: "qualified", "follow-up", "lost"; a project tool: "blocked", "in review"). Not generic ("important", "todo"). |
| Currency / pricing | Match the product's likely audience. SaaS pricing: $29 / $79 / $299. Consumer goods: rough realism per category. |
| Charts | Real-shape distributions — long tail, not perfectly even. Recent dates. Dates aligned to the product's billing cycle if applicable. |

**Anti-pattern reminder:** the SKILL.md aesthetic-defaults section bans fabricated numbers, fake metrics, and placeholder names like John Doe / Acme. This file extends that with positive guidance — plausible content has *texture*: variation in length, in shape, in distribution. AI defaults are smooth; real data is bumpy.

For images, use `Generate(node, "ai", "<prompt>")` or `Generate(node, "stock", "<query>")` — the `Generate` op exists for this. Don't leave gray rectangles labeled "Image".

## Deep links & shareable URLs

A page's URL is a piece of the design. Decide what state belongs in it.

**Belongs in the URL (so refresh restores it):**

- Selected tab.
- Filter / sort / search query parameters.
- Selected item in a list+detail layout.
- Page within a paginated list.
- Open dialog if it has its own meaningful URL (e.g. `/projects/123/edit`).

**Doesn't belong in the URL:**

- Modal-open state (modals are interruption, not destination).
- Form dirty state.
- Hover / popover open state.
- Scroll position (let the browser handle it natively).
- Currently-edited row in an inline-edit table.

**Design implications:** when designing a list with filters, the design implies that those filters survive a refresh. When the engineer asks *"do these filter chips need to deep-link?"*, the answer is in the design's `context`: *"Filters are shareable. Selecting a filter pushes a URL like `/projects?status=active&sort=created`."*

For modals that DO need URLs (a modal that's also accessible directly via link), document explicitly: *"Routed modal. Direct URL `/projects/123/share` opens this modal over the projects list."*

## Worked example: settings → edit-profile → save

A back-stack and validation flow walkthrough. Three screens; user comes from settings root, edits their profile, saves, returns.

**Screens.**

- `Settings_Profile` — list of profile fields with edit buttons next to each.
- `Settings_Profile_Edit` — modal-shaped edit dialog (or full page on mobile) for one field.
- After save: returns to `Settings_Profile`, with the saved field highlighted briefly.

**Flow:**

1. User on `Settings_Profile`, taps "Edit" next to "Display name".
2. `Settings_Profile_Edit` opens. On web: as a modal (URL: `/settings/profile?edit=name`). On mobile: as a full-page route.
3. The edit dialog's first focusable element is the input itself, pre-filled with the current value, text selected.
4. The user types a new name. Input's hover/focus states are visible. No validation runs yet.
5. The user taps Save. Sync validation runs (length check). If invalid, inline error appears below the input; the user fixes and re-taps Save.
6. Async server-side check fires (is the name unique?). Save button shows loading state — label replaced with spinner, width preserved. Other inputs disable.
7. Server returns success. Modal closes (web: URL drops the `?edit=name`; mobile: pop the route). User returns to `Settings_Profile`. The "Display name" row pulses with a subtle `$success` background for ~1s, then decays. A toast confirms: *"Display name updated."*
8. If the server returns failure: the loading state ends, the modal stays open, an inline error appears under the input: *"That name is taken. Try a different one."* Other inputs re-enable.
9. User cancels: modal closes, no toast, no row highlight, no URL change beyond dropping `?edit=name`.

**In Pencil:**

- Three sibling top-level frames: `Settings_Profile`, `Settings_Profile_Edit`, `Settings_Profile_AfterSave` (the third only if the highlighted-row state is materially different from the default).
- Each `Edit` button on `Settings_Profile` has `context`: *"Opens `Settings_Profile_Edit` as a modal on web, full-page on mobile. URL gains `?edit=<field>`."*
- The modal's `context` documents validation timing: *"Sync validation on Save click. Async server check during the loading state. Server failure renders inline error under the input."*

Layout: profile rows in a form-stack layout; each row shows label + current value + Edit button in a horizontal row. Motion: modal open/close at 200ms ease-out; post-save row pulse is a brief background-colour flash (150ms) then back to default. Toast copy: "Changes saved." — no emoji, no exclamation, present tense.

## Anti-patterns

These read as flow-blind designs and should be fixed in passing whenever you see them:

- **Validation that fires on every keystroke.** Shows errors before the user has finished typing. Default to on-blur.
- **Modals that hide multi-step flows.** Modals are for finite, single-purpose interruptions. Multi-step belongs in routed pages or full-page modals.
- **Back buttons that bounce out of a wizard entirely.** The browser back should step the wizard backward, not exit it. Document the expected stack behavior.
- **Toasts as the only confirmation for high-consequence actions.** A 5-second auto-dismiss confirmation is fine for routine actions, hostile for *"Account deleted"*.
- **Loading states that change layout.** A button that grows when its label becomes a spinner forces a reflow on every async submission.
- **Optimism on flaky paths.** Optimistic UI on a known-flaky network produces frequent rollbacks that feel worse than a brief loading state.
- **Hover-only affordances inside flows.** A multi-step form where the next-step button only appears on hover hides the next step from keyboard and touch users.
- **Filters that don't survive refresh.** Mid-edit filter state vanishing on refresh is one of the most common SaaS frustrations.

## See also

- [`states.md`](states.md) — the component states this file's flows transition between (loading, error, success).
- [`accessibility.md`](accessibility.md) — focus management across flows, modal focus traps, keyboard navigation.
- [`mcp-tools.md`](mcp-tools.md) — `FindEmptySpace` for placing the sibling frames a multi-step flow needs.
