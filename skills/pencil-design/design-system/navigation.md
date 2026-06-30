# Navigation

The project's primary navigation pattern. The agent reads this file when designing chrome, picking nav structure, or auditing navigation. It complements `references/layout-patterns.md` § Dashboard layouts and § Settings pages.

## Primary navigation

The project commits to: `<top nav | left sidebar | right sidebar (rare) | bottom tab bar (mobile-first) | hamburger drawer (mobile only) | command-driven (⌘+K is the primary nav)>`.

Decision drivers (per `references/layout-patterns.md` § Dashboard layouts):
- **Sidebar + main**: multi-section product, default for B2B SaaS (Linear, GitHub, Stripe Dashboard).
- **Top nav + content**: single primary task per page; nav stays light (Vercel dashboard, Notion).
- **Three-column (nav / list / detail)**: email, messaging, asset browsers (Apple Mail, Things, Linear).
- **Command-driven**: power-user products where keyboard navigation dominates (Linear, Raycast, Arc).

For mobile, the project commits separately: `<bottom tab bar (≤ 5 tabs) | hamburger drawer | persistent top nav>`.

## Sidebar nav structure

If the project ships a sidebar:

- **Width**: `<240px | 280px | collapsible 80px → 240px>`.
- **Sections** (in order): the project's specific sections. E.g. Inbox, My work, Projects, Teams, Settings.
- **Collapsed state**: icons only, labels appear on hover or via tooltip.
- **Workspace switcher**: at the top (above sections) for multi-workspace products.
- **User menu**: at the bottom (avatar + name; click opens settings, profile, logout).
- **Search entry**: at the top, sticky (search is a primary entry point per `search.md`).

## Top nav structure

If the project ships a top nav:

- **Height**: `<48px | 56px | 64px>`.
- **Logo / product mark**: top-left, links to home / dashboard.
- **Primary nav items**: 3-7 items max. Beyond 7, sidebar wins.
- **Search**: centre or right-of-centre.
- **Notifications, account, help**: top-right cluster.

## Breadcrumbs

`<used | not used>`.

If used: live below the top nav (or above the page title for sidebar layouts). Format: `Workspace > Section > Page > Subpage`. Each segment links to the parent. Click on the current page's segment opens a search-this-section affordance (optional).

## Search placement

`<header search bar | command palette (⌘+K) | search modal triggered from a search icon | search-driven settings page (when settings > 30 sections)>`.

Cross-link to `search.md` for the project's full search pattern.

## Notifications

`<icon in header with count badge | dedicated notifications page | both (icon opens a panel)>`.

Notification panel anatomy:
- Group by type (mentions, system, comments).
- Mark as read on view, optional mark-all-as-read action.
- Empty state: see `empty-states.md`.

## Workspace switcher (multi-tenant)

If the project supports multiple workspaces:
- Workspace name + avatar visible in the chrome (top of sidebar or header).
- Click opens workspace switcher: list of workspaces the user belongs to, plus 'Create workspace' and 'Join workspace' actions.
- Switching workspace `<routes to the workspace's home | preserves the current page when possible>`.

## Mobile navigation

Per `references/mobile-patterns.md` § Tab bars:

- Bottom tab bar: `<3 | 4 | 5>` items max.
- Order matters: most-used left, less-used right.
- Active tab: filled icon + label colour change; inactive: outlined icon + muted label.
- Always show labels (don't hide them at default text size).

Mobile nav items: `<item 1, item 2, item 3, item 4, item 5>`.

## Hamburger drawer (mobile fallback)

If the project uses a hamburger drawer instead of bottom tabs:
- Trigger: hamburger icon top-left.
- Slides in from the left.
- Contains the full nav hierarchy.
- Backdrop dismisses on tap.

## Sticky vs scrolling

`<sticky top nav | sticky sidebar (default) | both | neither>`.

Sticky nav stays visible during scroll; the user always sees the chrome. Non-sticky nav reclaims space; the user scrolls to top to reach it.

## Active state

Per `tokens.md` and `motion.md`:
- Active nav item: `<filled background using $accent | left border using $accent | text colour change to $accent>`.
- Hover state: subtle `$surfaceMuted` background; never compete with active.
- Focus ring on nav items via keyboard navigation: `$focusRing`, 2px outline.

## Keyboard navigation

Per `accessibility.md`:
- Tab moves through nav items in DOM order.
- Arrow keys move between sibling nav items in the sidebar.
- Enter / Space activates.
- Skip link at the top of the page lands on `<main>` content, bypassing nav.
- Command palette (⌘+K) is an alternative navigation entry; covers every nav destination.

## Persistent vs ephemeral nav

- **Persistent**: always visible (sidebar, top nav). Default for productivity products.
- **Ephemeral**: appears on demand (drawer, command palette). Default for content-led or canvas-led products.

The project commits one or the other as the *primary*; the other can supplement.

## URL state

Every nav item maps to a URL. The active nav state derives from the URL. Refresh restores the same view. Back / forward browser navigation works. Per `references/flows.md` § Deep links & shareable URLs.

## Notifications and badges

Count badges on nav items (e.g. inbox shows unread count):
- Number for ≤ 99; '99+' for higher counts.
- Colour: `$danger` for urgent (mentions); `$accent` for general (unread).
- Badge appears in the same position consistently (top-right of the nav item icon).

## Verification checklist

Before declaring nav done:

1. Click every nav item. Each routes to the correct page.
2. URL reflects the active nav state.
3. Refresh restores the active state.
4. Browser back / forward works through nav history.
5. Keyboard tab through nav. Focus visible. Order matches visual.
6. Command palette (if used) covers every nav destination.
7. Mobile: bottom tab bar respects safe area (per `mobile.md` § Safe areas).
8. Notification badges update in real time as new items arrive.

## See also

- `references/layout-patterns.md` (in the pencil-design skill): § Dashboard layouts, § Settings pages, § List-detail layouts.
- `references/mobile-patterns.md` (in the pencil-design skill): § Tab bars, § Native conventions per platform.
- `references/flows.md` (in the pencil-design skill): § Back-stack & navigation model, § Deep links & shareable URLs.
- `search.md`: project's search pattern (often a primary nav entry).
- `accessibility.md`: keyboard nav, focus management, skip links.
- `tokens.md`: nav-related colour and spacing tokens.
- `motion.md`: nav transition timing.
- `mobile.md`: bottom tab bar specs, safe area handling.
