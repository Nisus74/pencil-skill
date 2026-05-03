# Patterns

Page-level templates. The agent reads this when laying out a whole page, not just a component. Without these, AI invents a novel page structure on every task — which is why dashboards drift, settings pages all look different, and marketing landing pages cycle through three random hero recipes.

The patterns below are starting structures, not rigid grids. Adapt rhythms; don't reinvent.

## Marketing landing page

A linear, scroll-down structure. **Don't** invent four-column feature grids or scroll-jacked sections by default.

```
Page
├── Nav (sticky, $elevation0 until scrolled, $elevation1 once scrolled)
├── Hero
│   ├── Headline (1 line, ≤ 9 words, $text4xl)
│   ├── Subhead (1–2 lines, $textLg, $textMuted)
│   ├── CTA primary + secondary (one of each)
│   └── Visual (product shot OR illustration — not both)
├── Social proof strip (logos OR a single quote — not both)
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

## Pricing page

```
Page
├── Headline + intro
├── Toggle (monthly/annual, if applicable) ← center, single control
├── Plans (2–4 cards, side by side; one marked "popular" or "recommended")
│   ├── Plan name
│   ├── Price (largest text on the card, $text3xl)
│   ├── Per-period unit (smaller, $textMuted)
│   ├── CTA (primary on the recommended plan, secondary on the rest)
│   └── Feature list (checkmark icons + brief text, max ~10 rows)
└── FAQ (if needed)
```

**Rules:**

- One plan is the recommended default — visually emphasized, but not by 30% bigger; subtler (border accent, "popular" tag, primary CTA).
- Feature lists in plans should differ by a meaningful axis (limits, support tier), not by checking-vs-omitting trivial features.
- Don't put the highest-tier ("Enterprise / Contact us") plan visually largest. Right-most or smaller-on-the-end is the convention.

## Settings page

The most-broken page in most products. Default structure:

```
Page (max-width 720, centered)
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

- **Single column, max ~720px wide.** Multi-column settings pages are always a regret — fields don't align with section headings, controls land in awkward places.
- **Label left, control right** for short controls (toggle, select, short input). Stack vertically (label above) for long inputs and multi-line fields.
- **One save action per page** (not per row), unless a setting has immediate side-effects (a toggle that flips a feature on right now).
- **Sticky save bar appears only when dirty.** Don't reserve vertical space for it always.

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

- Pick **either** TopNav as primary navigation **or** SideNav as primary — not both equally weighted. The other is a thin chrome.
- TopNav holds: brand, breadcrumb (or page title), search, notifications, account. Not primary nav links unless the app is small.
- SideNav holds primary nav. ≤ 7 top-level items; group beyond that.
- Right rail is optional and contextual. Don't reserve space for it on pages that don't use it.

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
- Selected list item: not just `$primaryMuted` background — also a 3px left accent bar in `$primary` for clarity. Subtle hover ≠ selected; they should be unmistakable.
- Detail column gets a back arrow on mobile, no back arrow on desktop (the persistent list does that job).

## Auth flow (sign in / sign up / recovery / verify)

A **centered single-column card** on a calm background. Same template across all four screens; copy and fields differ.

```
Page (centered, vertical + horizontal)
└── AuthCard (max-width 400)
    ├── Logo (small, $iconLg)
    ├── Title ($text2xl) — "Sign in" / "Create your account" / "Reset your password"
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

## Onboarding flow

A **2–4 step wizard**. More than 4 steps means it's a settings page, not onboarding.

```
Page
├── Progress indicator (stepper or progress bar at top)
├── Step content (centered card or full-bleed)
│   ├── Step title ($text2xl)
│   ├── Helper text
│   └── Form / choices for this step
└── Footer (Back left, Continue right)
```

**Rules:**

- A user can always **skip** non-essential steps. Force only what genuinely blocks first use (account name, primary workspace).
- Don't ask for things you don't need yet — every onboarding question is a friction tax.
- Show progress (e.g. "Step 2 of 3") so the end is visible.

## Empty state

Not a page pattern but a recurring lockup. See `voice.md` for copy rules; the visual lockup:

```
EmptyState (centered in the empty container)
├── Illustration or icon ($iconXl, $textMuted color, simple)
├── Title (1 line, $textXl, max 8 words)
├── Description (1–2 lines, $textMuted)
└── Primary CTA
```

Don't fill empty states with multiple CTAs ("import", "create", "explore demo") — pick the one most users actually want.

## When the right pattern doesn't exist here

Three options, in order:

1. **Pick the closest pattern and adapt.** Most "new" pages are variations on one of the above.
2. **Compose two patterns side by side** (e.g. a dashboard shell whose main area contains a list+detail).
3. **Surface the missing pattern.** *"This screen doesn't fit the patterns we have. Want to add a `<name>` pattern, or describe what you have in mind?"* The user decides.
