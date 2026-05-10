# modern-pro-tool

> Refined-dense B2B software designed by people who use it daily; chrome disappears, the work surface leads.

**Surface category:** saas-apps/b2b
**Confidence:** confirmed via Linear screenshots (May 2026)
**Exemplars:** Linear (primary), Notion business workspaces (secondary, document-leaning)

## When to choose this archetype

Pick this when the user is silent on aesthetics and the brief is "modern pro software" without strong domain pull toward analytics, enterprise, or workflow collaboration. Linear's aesthetic shifted what B2B SaaS looks like in the late 2020s: tight spacing, hairline borders, restrained colour, one strong accent used sparingly, the chrome disappearing so the work shows. The product feels designed by engineers and PMs for engineers and PMs. If the brief leans heavily toward charts and KPIs, prefer `analytics-dashboard`. If it leans heavy on collaboration cards and status colour, prefer `workflow-platform`. If the user has supplied direction, follow it.

## Typography

- **Body and UI:** `Inter Display` is the canonical choice for this archetype. Linear uses it deliberately and well. This archetype explicitly overrides the SKILL.md default ban on the Inter family because the exemplar earns it. Alternatives if `Inter Display` isn't licensed: `Söhne` (Linear's fallback in some contexts), `Geist`, `Satoshi`. Sized at 13–14px for body.
- **Headings:** same family, heavier weight. Page-title H1 22–24/600. Section heads inline at the top of content, not as separate strips.
- **Sidebar section headers:** sentence-case lowercase with a small `▼` chevron when collapsible. *"Workspace"*, *"Your teams"*, *"Try"*. Not small caps, not all caps.
- **Numerals:** monospace inside data-heavy contexts (issue counts, time estimates, version strings). Tabular figures even in proportional fonts where the font supports it.
- **Keyboard shortcuts:** rendered inline as small monospace chips with a slightly darker background tint. Pattern: `G then S`, `O then W`, `⌥⇧Q`. They appear inside button labels (next to "Create new issue") and beside menu items.
- **Tracking:** slightly negative on body (-0.005em).

## Density

- Spacing scale: 4 / 8 / 12 / 16 / 20 / 24. The `20` step matters; it's where most card padding lives.
- Sidebar items: 6–8px vertical padding. Tight enough to fit 12+ items without scrolling.
- Row padding in lists: 6–10 vertical.
- Card padding (settings sections, milestone rows): 16–20.
- Line-height: 1.4 for body, 1.2 for headings, 1.0 for monospace.

## Accent strategy

- One accent. Used in: primary CTA fill, link affordances, focus outlines, certain icons (favourited star), status indicators that warrant attention.
- Linear's signature accent is a saturated indigo / violet; treat it as the canonical example but pick something distinct per project. Saturation 70–85%, this archetype permits more saturation than `analytics-dashboard` because the accent does less work overall.
- Status colours (`$positive`, `$negative`, `$warning`) appear as small filled circles or short text labels. Status pills (Planned, Current, Completed) carry their own muted hues.
- The active sidebar item uses a **light grey filled background** (`$surfaceMuted`), not the accent colour. The accent is reserved for actions and affordances, not navigation state.

## Surface treatment

- **Light mode is canonical.** Dark mode is supported and excellent, but the design optimises for light first. Pencil's usual "dark mode default" guidance doesn't apply here.
- Hairline borders, no shadows on the work surfaces. 1px borders at `$borderSubtle` separate cards, panels, and sections. The only places shadows appear: floating menus, command palettes, dropdowns, and tooltips. Even there, soft and restrained (4–8px blur, low opacity).
- Card corner radius: 6–10. Buttons rounded rectangles at 6–8. Tabs and segmented controls fully rounded pills. Avatars circular.
- Background hierarchy: `$bg` (page, very pale warm grey, near-white) > `$surface` (cards and panels, slightly different warmth) > `$surfaceMuted` (sidebar background, table headers, active sidebar item, code blocks). Three levels.

## Data display

- Tables and lists dominate. Always `frame → cell frame → cell content`. Row separators are 1px borders, not zebra stripes.
- Inline status pills: a small filled circle of status colour, plus short text. Compact, never with a card background.
- Counts and metadata sit at the right edge of rows, monospace, lighter weight.
- **Inline mini-charts are allowed** in specific contexts: cycle burndown, project progress, milestone completion. They use subtle gradient fills (very low opacity), dashed lines for projections, solid lines for actuals. Two-colour palette max (e.g., yellow for started + blue for completed). Render them small and embedded in their data context, never as page-dominating visualisations. For dashboards proper, pick `analytics-dashboard` instead.
- **Properties panels** on the right side of project / issue views: vertical list of `label · icon · value` rows. Subtle hover state, click-to-edit. Each row roughly 32–36px tall.

## Microcopy and voice

- Direct, sentence-case, present-tense. *"3 issues completed today"* beats *"You have completed 3 issues today!"*.
- Empty states: short, helpful, with the next action as a button or link. *"No active issues. Create new issue C"*. Often paired with a small abstract icon cluster (Linear uses 4 abstract shapes in a 2x2 grid before the heading), these are decorative-but-restrained, not illustrated mascots.
- Loading states: skeleton rows matching final shape. Never spinners on list views.
- Error states: terse, actionable. *"Couldn't load. Retry"*. No apology, no exclamation marks.
- Command palette copy is part of the voice: action verbs in present tense (*"Create issue"*, *"Move to project"*, *"Assign to me"*).

## Motion personality

- Fast, snappy, confident. Sidebar item hover: 80–120ms ease-out background fade. Page transitions: 150ms slide. Modal opens: 180ms scale-up from 0.96 with overlay fade.
- Optimistic updates everywhere. The UI commits to the change before the server confirms; correct silently if the server rejects.
- Anti-cue: bouncy springs, long fade-ins, ambient continuous animation, parallax. This archetype is sober.

## Anti-cues (don't reach for these in this archetype)

- Soft shadows on every card.
- Decorative gradients, especially purple-to-blue, on backgrounds or buttons.
- Three-column feature grids on the dashboard home.
- Glass-morphism, backdrop blur, materially expressive surfaces.
- Avatar groups with overflow counts in headers (use member counts inline instead).
- Marketing-style hero sections inside the app.
- Notification badges with strong colour fills (use a small mono badge with count).
- Big illustrated empty states with mascots or scenes (use 2–4 small abstract icons clustered above the heading instead).
- Onboarding tooltip cascades that block the UI on first run.
- All-caps small-cap section headers in the sidebar (this archetype uses sentence-case lowercase).
- Active sidebar item as a coloured pill or accent border (use `$surfaceMuted` background instead).

## Worked example: a project management tool

Imagine the current `pencil-new.pen` brief reframed as a Linear-style project management view in this archetype:

- **Sidebar** ~232px, pale grey background. Top row: small workspace icon + name "Workspace ▼" with a search and "compose" icon-buttons to its right. Then primary nav items: Inbox (with right-aligned `3` count badge), My issues, Reviews. Then "Workspace ▼" section header (sentence-case lowercase, small chevron) with: Projects, Views, More. Then "Your teams ▼" section header with each team listed as `coloured-team-icon + name ▼`, expandable to Issues / Cycles / Projects / Views. Bottom: "Try ▼" with Invite people, Initiatives, then `?` help icon at the very bottom.
- **Top bar** is barely there: breadcrumb (e.g. *Product › Product Strategy & Specs ⭐*) + a star icon, with action icons (filter, settings, panel-toggle) right-aligned. No separate strip, just a thin top edge of the main column.
- **Main column** with tabs (Overview / Activity / Issues) as a small segmented pill control beneath the breadcrumb. Active tab gets a slightly darker background fill.
- **Page title** uses an emoji (📋) as the icon, then *"Product Strategy & Specs"* at 22–24/600, subtitle below.
- **Properties row** inline beneath the title: small icon + value chips (`Backlog`, `High`, `Lead`, `Mar 14th → May 30th`, `Product`), readable as a status line, not a form.
- **Resources / Customers / Description / Milestones** sections stack vertically, each with a subtle label and content.
- **Right panel** ~280px wide carries Properties (label + icon + value rows), Milestones (diamond icon + name + `0% of 3` + date), and Progress (small inline chart).
- **Bottom-right** floating: a thin pill labelled *"Ask Linear"* with chat + history icons. The AI assistant entry point lives here, not as modal chrome.
- **Empty state** (when an issue list is empty): four abstract small icons in a 2×2 cluster, then bold heading *"Active issues"*, then descriptive paragraph, then two buttons, primary `Create new issue C` (filled accent, with the keyboard shortcut as a darker mono chip on its right edge) and secondary `Documentation` (white with subtle border).

## Notes for AI implementers

Tokens this archetype implies (illustrative; rename to project's scheme):

| Token | Value |
|---|---|
| `$accent` | Saturated indigo or chosen brand hue at 70–85% saturation. |
| `$bg` | `#FAFAFA` (very pale warm grey) light, `#0E0E10` dark. Light is canonical. |
| `$surface` | `#FFFFFF` light, `#17171A` dark. |
| `$surfaceMuted` | `#F4F4F5` light, `#1F1F23` dark. Used for sidebar background and active sidebar item. |
| `$borderSubtle` | `#E7E5E4` light, `#2A2A2E` dark. Hairline, never bolder. |
| `$fontUI` | `Inter Display` (canonical for this archetype, overriding SKILL.md default). Alternatives: `Söhne`, `Geist`, `Satoshi`. |
| `$fontMono` | `Geist Mono`, `JetBrains Mono`, or `Berkeley Mono` for keyboard-shortcut chips and code blocks. |

Components most affected: `Sidebar`, `IssueRow`, `StatusPill`, `KeyboardShortcutChip`, `PropertiesPanel`, `Breadcrumb`, `InlineCount`, `EmptyState`, `AskAIPill`, `MilestoneRow`, `InlineMiniChart`. Each gets a variant inside this archetype.

Common slip-ups:

- Reaching for shadows on cards because "they look unfinished". They aren't. Hairlines do the work.
- Defaulting to dark mode because the archetype is "modern pro tool". Light is canonical here; ship dark too but treat light as the brief.
- Using purple-blue gradients on CTAs. Pick a project-specific accent and apply it as a flat fill; gradients are an anti-cue.
- Building marketing-style hero sections on the dashboard. The dashboard is the work surface; no marketing.
- Adding decorative illustrations to empty states. Use a 2x2 cluster of abstract icons instead, kept small.
- Spacing too generously because "modern UI is airy". Modern *pro* UI is tight.
- Making the active sidebar item a coloured pill or accent border. Use a `$surfaceMuted` background.
- Skipping the AI assistant entry point. In 2026 a floating "Ask <product>" pill in the bottom-right is increasingly the modern-pro-tool default.
- Using all-caps small-caps for sidebar section headers. Use sentence-case lowercase with a small chevron.
