# Layout patterns

How the agent picks the *shape* of a page. Most AI-generated UIs default to the same handful of layouts: the centred hero, the three-card feature grid, the sidebar + main dashboard. Those defaults are familiar, which means they're invisible. This file gives the agent a richer menu to pick from, with the trade-offs spelled out so the choice can be deliberate.

**What this file owns:** the named layout patterns the agent picks from for marketing pages, dashboards, settings, list-detail screens, and empty pages. For each pattern: when it works, when it doesn't, real-world exemplars that ship it well.

**What this file does NOT own:** the typography, colour, and spacing that fill the layout. That's [`assets/design-system/tokens.md`](../assets/design-system/tokens.md) and the per-project commitments. Component-level state (loading, error, hover) is in [`states.md`](states.md). Visual hierarchy within a chosen layout is in [`visual-hierarchy.md`](visual-hierarchy.md). Microcopy that fills the layout is in [`microcopy.md`](microcopy.md).

## When to load this file

- The user asks for a marketing page, landing page, hero section, pricing page, testimonials block, or footer.
- The user asks for a dashboard, settings page, list-detail screen, or empty/error page.
- The agent is reaching for a familiar default (three-card grid, centred hero) and wants alternatives.
- The design feels generic, and a different layout shape might be the rescue.

## Hero variations

The hero is the screen's first impression. Defaulting to the centred-text-and-CTA hero ships a design that looks like every other SaaS landing page from 2018.

| Pattern | When it works | Real-world exemplar |
|---|---|---|
| **Centred** | Single, clear value prop. No supporting visual needed. | Linear (linear.app), Things (culturedcode.com). |
| **Split (form right, image left)** | Sign-up driven. The form is the action; the visual sets the mood. | Notion sign-up, Stripe Atlas. |
| **Asymmetric (off-centre title)** | Editorial or personality-led brands. Breaks the cadence of corporate symmetry. | Vercel (vercel.com), Apple product pages. |
| **Full-bleed video or animation** | Product demo is the value prop. The visual is the pitch. | Arc browser (arc.net), Loom. |
| **Minimal (typography only)** | Strong type, strong opinion. The brand is the design. | Pitch (pitch.com), Cron (now Notion Calendar). |
| **Bento grid** | Multiple value props need equal weight. Modern alternative to a feature list. | Apple product pages (iPhone 16 page), CleanShot X (cleanshot.com). |

The mistake to watch for: every variant becomes the centred hero with one alteration. If the agent is picking 'split' but the form is centred and the image is decorative, that's still a centred hero. Commit to the asymmetry.

## Feature sections (not three-card grids)

The three-equal-card-grid is the most over-used layout pattern in SaaS marketing. It's a tell.

Better feature-section patterns:

- **Alternating image-text rows.** Image left + text right, then image right + text left. Each feature gets a full row. Used by Linear, Stripe, Vercel.
- **Bento grid.** Tiles of varied sizes laid out asymmetrically. The biggest tile carries the headline feature; smaller tiles support. Apple started the pattern; Linear, Raycast, Arc all use variations.
- **Comparison table.** Three or four columns, one feature per row, checkmarks/dashes for what each tier or competitor offers. Heavy but earns its weight when the value prop is competitive.
- **Icon grid done well.** If you must use a grid, make the icons varied in size, the spacing intentional, and leave one tile empty as breathing room. Six-up symmetric grids of identical-size icons read as a stock template.
- **Single hero feature.** One feature, given the full attention of a section. The follow-up section gets the next feature. Used by Things, Cron, Apple.

When the request is 'a marketing page with three features', the agent's first instinct shouldn't be a three-card grid. Ask: would alternating rows or a bento grid carry the same information with more personality?

## Pricing tables

Three-tier pricing with a highlighted middle tier is the dominant pattern for a reason: it works. Pick the variant deliberately.

| Pattern | When it works | Real-world exemplar |
|---|---|---|
| **Three-tier (Free / Pro / Team)** | SaaS with a clear progression. Highlight the recommended tier with a coloured border, layered shadow, and 'Most popular' badge. | Linear, Notion, Vercel. |
| **Single-tier with feature comparison** | Single product, single price. The page focuses on what's included rather than which tier to pick. | Things 3, Cron, most consumer apps. |
| **Usage-based** | Pricing scales with consumption (API calls, storage, seats). Show the price calculator inline; let the user explore. | Stripe, Vercel, AWS-style products. |
| **Enterprise contact** | Top tier is 'Contact us'. Reserve for genuinely enterprise-only features (SSO, SLAs, dedicated support). Don't gate basic features behind it. | Linear (Enterprise tier), Vercel Enterprise. |

The highlighted tier carries: a coloured border (one accent colour, never multiple), a layered shadow (ambient + direct, per `SKILL.md` § Shadows), a slight scale-up, and either a 'Most popular' or 'Recommended' badge. Don't combine all four. A coloured border plus a badge is plenty. See [`example-pricing-table.md`](../assets/examples/example-pricing-table.md) (Phase 4).

## Testimonials

The carousel is an accessibility tax. It auto-rotates, hides content, and breaks for keyboard users. Better patterns:

- **Avatar grid (3 to 6 quotes).** Each tile has the avatar, name, role, company logo, and a short quote. Layered horizontally on desktop; stacked on mobile.
- **Single hero quote.** One testimonial, given the full attention of a section. Pairs with a logo wall below. Used by Linear, Stripe.
- **Logo wall (no quotes).** Just the customer logos, in muted colour, evenly spaced. Lighter weight; works when the brands themselves are the credential. Stripe, Vercel, Linear all do this.
- **Video embed.** When you have a customer willing to record a 60-second testimonial, the video is more credible than any pull quote. Embed inline (don't autoplay, don't loop).

Carousels are acceptable when the user explicitly controls the rotation, but the auto-rotating variant shouldn't ship.

## CTA sections

Three places a CTA earns its weight on a marketing page:

- **Hero CTA.** Primary action, above the fold.
- **Mid-page CTA.** Inline after a value-prop section, when the user is convinced. Uses different copy from the hero CTA ('Start your free trial' instead of 'Get started').
- **Closing CTA.** Full-width section at the page foot, restating the offer. Pairs with a secondary action ('Contact sales', 'Read the docs') for the user who isn't ready.

Sticky footer CTAs (the bar that follows the user as they scroll) work for ecommerce checkout but feel pushy on B2B SaaS marketing. Use sparingly.

## Footer architectures

Footers are where the user goes when they're stuck or curious. Pick the shape based on the site's information density:

- **Minimal.** Logo, copyright, three or four legal links. Right for consumer apps and single-product sites where the footer isn't where the user navigates.
- **Sitemap (4-column).** Product, Company, Resources, Legal columns. Each column has 4 to 8 links. Right for SaaS with documentation, blog, customer stories.
- **Legal-only.** Just the regulatory links (Privacy, Terms, Cookies, GDPR, Accessibility statement). Right for landing pages where the footer is statutory rather than navigational.
- **Social/contact dominant.** Social links and contact info take centre stage. Right for personal brands, agencies, conferences.

Don't mix architectures. A sitemap with a giant 'Subscribe to our newsletter' form crammed in reads as a kitchen-sink footer.

## Dashboard layouts

| Pattern | When it works | Real-world exemplar |
|---|---|---|
| **Sidebar + main** | Multi-section product. The sidebar is the navigation; the main is the work surface. Default for most B2B SaaS. | Linear, GitHub, Stripe Dashboard. |
| **Top nav + content** | Single primary task per page. The nav is light; the content gets the full canvas. | Vercel (vercel.com/dashboard), Notion. |
| **Three-column (nav / list / detail)** | Email, messaging, asset browsers. The user picks an item from the middle column; the right column shows it. | Apple Mail, Things, Linear's issue view. |
| **Command-driven** | Power-user products where ⌘+K is the primary navigation. The chrome stays minimal because the keyboard does the work. | Linear, Raycast, Arc. |

For multi-product platforms, the sidebar may need a workspace switcher or a product switcher at the top. Document the chosen pattern in the project's `assets/design-system/navigation.md` (Phase 4).

## Settings pages

Pick the navigation pattern based on the number of settings sections:

- **Tabs (≤ 6 sections).** Horizontal tabs at the top. Right for small settings surfaces. macOS System Settings (post-Ventura) uses this.
- **Sidebar nav (> 6 sections).** Vertical nav on the left. The default for most SaaS settings pages. Linear, GitHub, Stripe.
- **Search-driven (> 30 sections).** When there are too many settings to navigate by hierarchy. Search becomes the primary entry; the sidebar becomes secondary. Slack settings, GitHub repository settings.

Settings autosave by default. The user changes a value, the value persists, no Save button. The exception: settings that affect billing, security, or other consequential outcomes need explicit Save with confirmation. See [`flows.md`](flows.md) § Settings flows.

## List-detail layouts

Four shapes; pick by context density and screen size:

| Pattern | When it works | Notes |
|---|---|---|
| **Master-detail (split)** | Both list and detail are useful side-by-side. Desktop default for inboxes and asset browsers. | Resizable divider; remember the user's preferred ratio. |
| **Three-column (nav / list / detail)** | Adds a navigation column. Right for products with multiple folders or projects above the list. | Apple Mail, Things, Linear. |
| **Modal detail** | The detail is small enough to fit in a modal; the user wants to keep their place in the list. | Notion's page peek, Linear's issue modal from the inbox. |
| **Full-page detail** | The detail is rich enough to deserve its own URL and back-button behaviour. | GitHub issue pages, Stripe customer pages. |

Mobile collapses all four into a stack: list-then-detail. Don't try to keep the split layout below ~768px wide; it stops being usable.

## Empty page templates

The 404, 500, and offline pages are a brand opportunity. Treat them as designed pages, not as default browser-error stand-ins. See [`states.md`](states.md) § Screen-level fault states for the full taxonomy and copy patterns; this file owns the *layout*:

- **Centred error block** with illustration + title + description + primary CTA. The default. Linear, Stripe, GitHub all use this shape.
- **Helpful 404** with a sitemap or popular links below the error block. Right for content-heavy sites where the user might be looking for something specific.
- **Branded fault states** with a custom illustration that ties to the brand voice. The fault state is one of the rare moments the user sees the brand without the product chrome around it. Worth the design investment.

First-run welcome pages are different from empty states (which live inside a populated product). They're the user's first interaction. Show what the product can do: sample data, a guided tour, or a 60-second video. See [`example-onboarding-flow.md`](../assets/examples/example-onboarding-flow.md) (Phase 4).

## Pencil expression

Layout patterns map to top-level frame structure in `.pen`:

- **Marketing pages.** Each section is its own top-level frame at canvas origin or below: `Hero`, `Features`, `Pricing`, `Testimonials`, `CTA`, `Footer`. Use the section names from this file so the agent (and the next agent) recognises the pattern immediately.
- **Dashboards.** A single top-level frame named for the route (`Dashboard`, `Inbox`, `Settings`). Inside, the layout primitives (`Sidebar`, `Main`, `DetailPanel`) are reusable components imported from the design system.
- **Settings pages.** One frame per settings section, all sharing a `SettingsLayout` reusable that holds the navigation. Each section frame names its scope: `Settings_Profile`, `Settings_Billing`, `Settings_Notifications`.
- **List-detail.** The layout is a `MasterDetail` reusable; the list and detail content are slotted in. Document the resize behaviour and the modal-on-mobile fallback in the layout's `context`.
- **Fault states.** Sibling frames per code (`404Page`, `500Page`, `OfflinePage`), each instantiating a single `ErrorBlock` component with overrides. See [`states.md`](states.md) § Authoring screen errors in Pencil.

## Anti-patterns

These read as layout-blind designs and should be fixed in passing:

- **Three-card feature grid.** The most over-used SaaS marketing pattern. Reach for alternating rows or a bento grid first.
- **Centred-hero default.** When every page leads with the same shape, the brand reads as templated.
- **Auto-rotating testimonial carousel.** Hides content from keyboard users and accessibility tools. Use a static avatar grid or a single hero quote instead.
- **Sidebar nav for ≤ 4 settings sections.** Tabs would be lighter and easier to scan.
- **Master-detail layout below 768px wide.** Stops being usable. Collapse to a stack.
- **Generic 404 page.** The browser's default 404 is more useful than a branded page that says only 'Not found'. If you ship a custom 404, it must help the user.
- **CTA section with three competing buttons.** Pick one primary action. The user can't decide between three.
- **Footer with a sitemap and a newsletter form and a contact form and social links.** Pick a footer architecture and stick to it.

## Sources

- **Marketing patterns**: Refactoring UI (Schoger / Wathan), the marketing pages of Linear, Vercel, Stripe, Notion, Arc, Things, Cron, Raycast, Apple product pages, Pitch, Loom (accessed 2025/2026).
- **Pricing patterns**: Stripe, Linear, Notion, Vercel pricing pages; Patrick Campbell (ProfitWell) research on SaaS pricing-page conversion.
- **Dashboard patterns**: Linear, GitHub, Stripe Dashboard, Vercel Dashboard, Notion; Apple HIG (macOS) on master-detail layout.
- **Settings patterns**: macOS System Settings (Ventura onward), Linear settings, GitHub settings, Slack settings, Apple HIG.
- **Fault states**: Apple HIG, Material 3 (Google), Linear fault pages, Stripe fault pages, GitHub fault pages.
- **Bento grid pattern**: Apple iPhone 16 product page (apple.com), CleanShot X (cleanshot.com), Linear feature pages, Raycast.
- **Carousel anti-pattern**: Nielsen Norman Group research on auto-rotating carousels (multiple studies, 2013 onward, still current).

## See also

- [`visual-hierarchy.md`](visual-hierarchy.md): the six levers (size, weight, colour, position, spacing, motion) that organise content within any chosen layout.
- [`composition-patterns.md`](composition-patterns.md): how to build the components that fill these layouts.
- [`states.md`](states.md): empty, error, and fault state vocabulary for the empty-page templates.
- [`flows.md`](flows.md): how the user moves between pages within these layouts (modal vs page, back-stack, deep links).
- [`microcopy.md`](microcopy.md): the words that fill these layouts.
- [`assets/design-system/patterns.md`](../assets/design-system/patterns.md): the project's chosen layouts, lifted from this menu.
- [`assets/design-system/navigation.md`](../assets/design-system/navigation.md): the project's chosen navigation pattern (Phase 4).
- [`assets/examples/example-marketing-page.md`](../assets/examples/example-marketing-page.md): worked example of a non-three-card-grid marketing page (Phase 4).
- [`assets/examples/example-dashboard.md`](../assets/examples/example-dashboard.md): worked example of a dashboard with proper hierarchy (Phase 4).
