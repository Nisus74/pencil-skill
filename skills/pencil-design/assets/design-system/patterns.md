# Patterns

Page-level templates. The agent reads this when laying out a whole page, not just a component. Without these, AI invents a novel page structure on every task, which is why dashboards drift, settings pages all look different, and marketing landing pages cycle through three random hero recipes.

The patterns below are starting structures, not rigid grids. Adapt rhythms; don't reinvent. Each pattern carries an *Archetype variants* subsection showing how the same shape reshapes under different archetypes (see `assets/archetypes/` in the skill for the full bundles), and a *What generic looks like* anti-example showing what the AI defaults to when the agent skips aesthetic commitment.

**What this file does NOT own:** transitions *between* screens (modal-vs-page choice, validation timing, back-stack, multi-step flows, optimistic UI). Those are flow concerns, not layout concerns. When the auth or onboarding lockups below cross multiple steps, this file covers the *page* shape; the step-to-step behaviour lives in the agent skill's `flows` reference.

## Marketing landing page

A linear, scroll-down structure. **Don't** invent four-column feature grids or scroll-jacked sections by default.

```
Page
├── Nav (sticky, $elevation0 until scrolled, $elevation1 once scrolled)
├── Hero
│   ├── Headline (1 line, ≤ 9 words, $text4xl)
│   ├── Subhead (1–2 lines, $textLg, $textMuted)
│   ├── CTA primary + secondary (one of each)
│   └── Visual (product shot OR illustration, not both)
├── Social proof strip (logos OR a single quote, not both)
├── Features (2–4 sections, alternating left/right text+image)
├── Secondary CTA banner
└── Footer
```

**Rules:**

- **One Hero.** Don't stack two hero-sized sections at the top.
- **Three-column equal-card "features" grids are an AI tell.** Use 2 columns or alternating side-by-side instead.
- Vertical rhythm: section padding `$space-12` top/bottom on desktop, `$space-8` on mobile.
- Max content width `$maxContent` (1200) on desktop; full-bleed only for hero backgrounds and image strips.
- No fabricated metrics ("trusted by 10,000+ teams"). Only real numbers, or omit the section.

### Archetype variants

- **`marketing-websites/conversion-focused-saas`** (Linear / Stripe): dark-mode default, numbered systematic sections (1.0 Intake / 2.0 Plan / 3.0 Build), product screenshots as content (not illustrations), monumental headlines like *"Issue tracking is dead"*, quantified customer metrics over flowing testimonials, dense 5-column footer.
- **`marketing-websites/editorial-storytelling`** (Linear Method / Apple): generous space (200px+ vertical hero padding), single point per section, numbered chapters in the manifesto flavour, alternating dark/light section transitions in the cinematic flavour, no pricing tables, no comparison grids.

### What generic looks like (don't ship this)

Centred hero with a violet-gradient CTA, three-column feature cards with a Lucide icon over a bolded title and one-line description, smiling stock photography, "Trusted by leading teams worldwide" with no actual logos, three-tier pricing table, generic FAQ accordion, footer with social icons.

## Pricing page

```
Page
├── Headline + intro
├── Toggle (monthly/annual, if applicable) ← centre, single control
├── Plans (2–4 cards, side by side; one marked "popular" or "recommended")
│   ├── Plan name
│   ├── Price (largest text on the card, $text3xl)
│   ├── Per-period unit (smaller, $textMuted)
│   ├── CTA (primary on the recommended plan, secondary on the rest)
│   └── Feature list (checkmark icons + brief text, max ~10 rows)
└── FAQ (if needed)
```

**Rules:**

- One plan is the recommended default, visually emphasized but not by 30% bigger; subtler (border accent, "popular" tag, primary CTA).
- Feature lists in plans should differ by a meaningful axis (limits, support tier), not by checking-vs-omitting trivial features.
- Don't put the highest-tier ("Enterprise / Contact us") plan visually largest. Right-most or smaller-on-the-end is the convention.

### Archetype variants

- **`marketing-websites/conversion-focused-saas`**: 4 tiers (Free / Basic / Business / Enterprise), annual-only billing presented as the model with no monthly toggle, "All Free features +" pattern for the inheritance copy, comparison table beneath the cards, single trust-signal line ("Trusted by more than 25,000 teams"), prices in proportional currency notation (not monospace).

### What generic looks like (don't ship this)

Three centred tier cards with the middle one visually 30% bigger, monthly/annual toggle even though billing is annual-only, prices in monospace tabular figures, "Most popular" sticker on the middle card, identical feature lists with checkmarks vs missing-mark differentiation, generic FAQ accordion, decorative gradient sweep on the highest tier.

## Settings page

The most-broken page in most products. Default structure:

```
Page (max-width 720, centred)
├── Page title ($text3xl)
├── (Optional) Tab nav for major sections
├── Section
│   ├── Section title ($textXl)
│   ├── Section description ($textMuted, 1 sentence)
│   └── Setting rows (label left, control right, divider between)
├── Section
│   └── ...
└── Sticky save bar (bottom, only when there are unsaved changes)
```

**Rules:**

- **Single column, max ~720px wide.** Multi-column settings pages are always a regret. Fields don't align with section headings, controls land in awkward places.
- **Label left, control right** for short controls (toggle, select, short input). Stack vertically (label above) for long inputs and multi-line fields.
- **One save action per page** (not per row), unless a setting has immediate side-effects (a toggle that flips a feature on right now).
- **Sticky save bar appears only when dirty.** Don't reserve vertical space for it always.

### Archetype variants

- **`saas-apps/b2b/modern-pro-tool`** (Linear-style settings): different sidebar from the main app (settings-specific categories: General / Members / Billing / Integrations), main content as cards with icon + title + description + chevron right, sections grouped by larger headings, hairline borders only, light mode canonical, keyboard shortcuts visible inline.

### What generic looks like (don't ship this)

Two-column form with labels on the left and inputs on the right squeezed into a narrow gutter, a save button per section, a "Save All" button at the bottom that doesn't tell you which sections are dirty, soft shadows on every section card, blue links with underlines, "Profile / Account / Preferences / Notifications / Billing" tabs across the top with the active tab in primary brand colour.

## Dashboard shell

```
App (full viewport)
├── TopNav (h: 56, sticky)
├── SideNav (w: 240 expanded / 64 collapsed, fixed left)
│   ├── Logo / brand
│   ├── Primary nav (icons + labels)
│   ├── Secondary nav (separator + smaller items)
│   └── User menu (bottom)
├── Main content (fill_container, padding $space-6)
│   ├── Page header (title, breadcrumb, primary action)
│   └── Content
└── (Optional) Right rail (w: 320, fixed right) for context, activity feed, AI assist
```

**Rules:**

- Pick **either** TopNav as primary navigation **or** SideNav as primary, not both equally weighted. The other is a thin chrome.
- TopNav holds: brand, breadcrumb (or page title), search, notifications, account. Not primary nav links unless the app is small.
- SideNav holds primary nav. ≤ 7 top-level items; group beyond that.
- Right rail is optional and contextual. Don't reserve space for it on pages that don't use it.

### Archetype variants

- **`saas-apps/b2b/analytics-dashboard`**: hairline borders separate cards and tables (no shadows), KPI cards at the top with mono numerals + delta chips, one large trend chart, top-events bar list to the right, recent users table at the bottom. Accent appears only on chart bars, deltas, primary CTA, link colour.
- **`saas-apps/b2b/modern-pro-tool`** (Linear-style): pale-grey sidebar background (not white), section headers in the sidebar are sentence-case lowercase with small chevrons (not all caps), active sidebar item is a `$surfaceMuted` filled background (not a coloured pill), dense issue rows replace KPI cards on the home view, floating "Ask <product>" pill in the bottom-right for AI assist, light mode canonical.

### What generic looks like (don't ship this)

Sidebar with a violet gradient logo wordmark, six nav items each with a Lucide icon and an active state that's a soft-violet pill, top bar with breadcrumb + search + notification bell + avatar, four KPI cards with soft shadows showing MAU / DAU / Conversion / Retention with violet sparklines beneath each value, a centred line chart, an "Activity feed" right rail nobody asked for.

## List + detail (master/detail)

```
Page
├── List column (w: 360 fixed on desktop, full-width on mobile)
│   ├── List header (search, filter, sort, "+ New" button)
│   └── List items (selected state shows a strong visual mark)
└── Detail column (fill_container)
    ├── Header (title, status, actions)
    └── Detail body
```

**Rules:**

- On mobile, this collapses to a list view that pushes/transitions to a full-screen detail view (see `mobile.md` if present).
- Selected list item: not just `$primaryMuted` background, also a 3px left accent bar in `$primary` for clarity. Subtle hover ≠ selected; they should be unmistakable.
- Detail column gets a back arrow on mobile, no back arrow on desktop (the persistent list does that job).

### Archetype variants

- **`saas-apps/b2b/modern-pro-tool`** (Linear / Things-style): list items are dense 36px rows with status circle + title + assignee avatar + priority pill + project tag + due-date text, selected item is `$surfaceMuted` background (not accent), detail column carries a Properties panel on its right side with icon + label + value rows.

### What generic looks like (don't ship this)

List of card-shaped rows with avatars and three lines of preview text, selected item glows with a soft shadow + violet border, detail column has a generic header strip + tabs + body, back arrow on desktop wastes a row of vertical space.

## Auth flow (sign in / sign up / recovery / verify)

A **centred single-column card** on a calm background. Same template across all four screens; copy and fields differ.

```
Page (centred, vertical + horizontal)
└── AuthCard (max-width 400)
    ├── Logo (small, $iconLg)
    ├── Title ($text2xl), "Sign in" / "Create your account" / "Reset your password"
    ├── (Optional) Subtitle, 1 sentence
    ├── Form fields (vertical stack, $space-4 gap)
    ├── Primary button (full width)
    ├── (Optional) Divider + "Continue with [provider]" buttons
    └── Footer link ("Don't have an account? Sign up", or similar)
```

**Rules:**

- One primary button. "Sign in with email" + "Sign in with Google" + "Continue with magic link" is too many primaries.
- The provider buttons (Google, GitHub, etc.) sit *below* the email/password form by convention, not above.
- Errors: inline under the offending field, not a banner at the top.
- "Forgot password?" link sits inside the form, near the password field, not in the footer.

### Archetype variants

- **`marketing-websites/conversion-focused-saas`** (a SaaS sign-in landing): card sits on a near-black background with a subtle radial gradient, primary CTA in the brand accent (not a violet default), "Continue with Google / GitHub" providers below the form, no marketing copy in the card; signup link in the footer points to `/signup` not the same form.

### What generic looks like (don't ship this)

Centred card with a soft shadow on a violet-gradient background, "Welcome back!" headline, three OAuth provider buttons stacked above the email field, "Sign in" button in flat violet, "Forgot password?" link beneath the button, footer link in the same violet.

## Onboarding flow

A **2–4 step wizard**. More than 4 steps means it's a settings page, not onboarding.

```
Page
├── Progress indicator (stepper or progress bar at top)
├── Step content (centred card or full-bleed)
│   ├── Step title ($text2xl)
│   ├── Helper text
│   └── Form / choices for this step
└── Footer (Back left, Continue right)
```

**Rules:**

- A user can always **skip** non-essential steps. Force only what genuinely blocks first use (account name, primary workspace).
- Don't ask for things you don't need yet, every onboarding question is a friction tax.
- Show progress (e.g. "Step 2 of 3") so the end is visible.

### Archetype variants

- **`saas-apps/b2b/modern-pro-tool`** (Linear-style first-run): minimal chrome, single decision per screen, options as full-width selectable rows with optional helper text below each, keyboard shortcut hints visible (e.g. `1 / 2 / 3` for the options), continue button activates only when a choice is made, no animated mascots or celebration confetti.

### What generic looks like (don't ship this)

Four-step wizard with a horizontal progress bar at the top showing dot-line-dot-line-dot, large illustrated mascots on each step, "What brings you here today?" with five role checkboxes, mandatory company size and team-size questions, a "🎉 You're all set!" success screen with a confetti cannon animation, modal that blocks the UI on first run.

## Empty state

Not a page pattern but a recurring lockup. See `voice.md` for copy rules; the visual lockup:

```
EmptyState (centred in the empty container)
├── Illustration or icon ($iconXl, $textMuted color, simple)
├── Title (1 line, $textXl, max 8 words)
├── Description (1–2 lines, $textMuted)
└── Primary CTA
```

Don't fill empty states with multiple CTAs ("import", "create", "explore demo"), pick the one most users actually want.

### Archetype variants

- **`saas-apps/b2b/analytics-dashboard`**: skip the illustration, lead with a single-line confident headline naming what's missing and the next action (*"No events tracked yet. Send your first one →"*), subdued mono numeral if a count would help.
- **`saas-apps/b2b/modern-pro-tool`** (Linear-style): four small abstract icons in a 2×2 cluster above the heading (decorative-but-restrained, not illustrated mascots), bold title, descriptive paragraph, two buttons: filled accent primary with keyboard shortcut chip, white-with-border secondary (e.g. `Documentation`).

### What generic looks like (don't ship this)

Large illustrated mascot scene of someone holding an empty box, title "It's quiet here!", a long description explaining what this section is for, three buttons offering Import / Create / Explore Demo, decorative confetti shapes around the edges.

## When the right pattern doesn't exist here

Three options, in order:

1. **Pick the closest pattern and adapt.** Most "new" pages are variations on one of the above.
2. **Compose two patterns side by side** (e.g. a dashboard shell whose main area contains a list+detail).
3. **Surface the missing pattern.** *"This screen doesn't fit the patterns we have. Want to add a `<name>` pattern, or describe what you have in mind?"* The user decides.
