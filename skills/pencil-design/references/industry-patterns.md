# Industry patterns

How design defaults shift by industry. A fintech product calibrates differently to a creative tool. A B2B SaaS for healthcare clinicians follows different conventions than the patient-facing app for the same hospital. This file gives the agent a per-industry rule sheet so the defaults match the audience.

**What this file owns:** 8 industry families (SaaS, fintech, healthcare, e-commerce, creative tools, social, education, communication) with 15-20 rules per family covering layout, palette mood, typography personality, density, animations, anti-patterns, completeness must-haves, and recommended catalogue picks. Plus the brutal-honesty completeness pressure tests for SaaS, Website, and Mobile projects.

**What this file does NOT own:** the project's *committed* style or palette. Those live in `assets/design-system/visual-style.md` and `assets/design-system/tokens.md`. The catalogues this file recommends from are [`style-catalogue.md`](style-catalogue.md), [`colour-palettes.md`](colour-palettes.md), and [`font-pairings.md`](font-pairings.md). The fault-state taxonomy is in [`states.md`](states.md). The flow patterns are in [`flows.md`](flows.md).

## When to load this file

- The agent is starting a greenfield design and needs to know the industry's default conventions before picking style, palette, or fonts.
- The user names an industry ('design a fintech onboarding', 'a healthcare dashboard for clinicians').
- The agent is auditing an existing design and wants to check whether it covers the must-have screens for its industry (the completeness pressure tests).
- The agent needs to know the anti-patterns that signal 'wrong industry voice' (a brutalist healthcare app, a playful trading platform).

## How to use the catalogue

1. Identify the industry from the brief, or ask. If the product spans two industries (a fintech for healthcare providers), check both sections and merge.
2. Read the matching industry block. Note: layout default, palette recommendation, typography recommendation, density expectation, anti-patterns, completeness must-haves, exemplars.
3. Cross-check the catalogue picks against the chosen style ([`style-catalogue.md`](style-catalogue.md)) and palette ([`colour-palettes.md`](colour-palettes.md)).
4. Run the completeness pressure test for the project type at the end of the design pass. If the must-have screens aren't covered, the design isn't comprehensive.

## SaaS

The dominant family. Calm by default. Density varies wildly by sub-category.

**Sub-categories:**

- **Productivity (Notion, Cron, Things).** Calm, focused, sparse chrome. The product is the content; the chrome stays out of the way. Default style: Swiss / International or Minimal. Default palette recipe: Indigo Calm or Iris Premium. Default fonts: Inter + JetBrains Mono. Density: airy.
- **Developer tools (Linear, Vercel, GitHub).** Dense, monospace-friendly, terminal-aesthetic OK. Keyboard-first. Default style: Swiss / International + Terminal/Hacker. Default palette: Cursor Dark or Linear Dark. Default fonts: Inter + JetBrains Mono or Geist + Geist Mono. Density: dense.
- **Analytics (Stripe Sigma, Linear Insights, Mixpanel).** Data-dense, chart-forward. Number-first. Default style: Swiss / International + Bento for marketing. Default palette: Indigo Calm. Default fonts: Inter + JetBrains Mono. Density: very dense.
- **Collaboration (Slack, Discord, Figma).** Presence cues, real-time emphasis, social affordances. Default style: Swiss / International. Default palette: varies (Slack uses purple; Discord indigo; Figma neutral). Default fonts: Inter + Inter or DM Sans + DM Sans. Density: medium.

**Per-industry rules (SaaS):**

- One primary action per view.
- Sidebar navigation > 6 sections; tabs ≤ 6 sections (per [`layout-patterns.md`](layout-patterns.md) § Settings pages).
- Settings autosave by default; explicit save reserved for high-stakes changes (billing, security).
- Empty states must show what's possible, not what's missing (per [`microcopy.md`](microcopy.md) § Empty state copy).
- Loading states must use skeleton for known-shape content; spinner only for unknown-duration < 1s.
- Error messages guide the exit; never just 'Something went wrong'.
- Keyboard shortcuts for power users; ⌘+K command palette is table-stakes for B2B SaaS in 2025/2026.
- Dark mode shipped by default; users expect it, especially in developer tools.
- Onboarding offers sample data option (per [`flows.md`](flows.md) § Onboarding flows).
- Plan-restricted, trial-expired, no-permission states designed (not just the happy path).

**Anti-patterns:**

- Three-card feature grid on the marketing page (use alternating image-text rows or bento per [`layout-patterns.md`](layout-patterns.md)).
- Auto-rotating testimonial carousel (accessibility tax; use static avatar grid).
- Inoffensive default look that could belong to any other SaaS.
- Settings without autosave; explicit Save buttons everywhere.
- Empty states that say 'Nothing here yet' without a CTA.

**Recommended catalogue picks (SaaS):**

- Style: Swiss / International (default), Bento (marketing), Editorial (premium SaaS), Terminal / Hacker (developer tools).
- Palette: Indigo Calm, Iris Premium, Sky Open, Blue Trust.
- Fonts: Inter + JetBrains Mono (default), Geist + Geist Mono (developer tools), Söhne + Söhne Mono (premium with budget).

**Exemplars:** Linear (linear.app), Vercel (vercel.com), Stripe (stripe.com), Notion (notion.so), Things (culturedcode.com), Cron (cron.com), Raycast (raycast.com), GitHub (github.com), Cursor (cursor.sh).

## Fintech

Trust comes from restraint. The category splits by audience: consumer banking (warm, friction-reduced) vs trading (dense, real-time) vs crypto (newer aesthetics OK; trust still required).

**Sub-categories:**

- **Consumer banking (Monzo, Revolut, Wise).** Warm, calm, conservative palette. Default style: Swiss / International. Default palette: Modern Fintech Indigo or Banking Navy. Default fonts: Inter + Inter. Density: medium-low.
- **Trading platforms (Bloomberg, Robinhood, IBKR).** Dense, real-time, colour-coded states. Default style: Grid-heavy / data-dense + Dark-mode-first. Default palette: Trading Green-Red. Default fonts: Inter + JetBrains Mono. Density: extreme.
- **Crypto / Web3 (Coinbase, MetaMask, Phantom).** Newer aesthetics (vibrant, dark-default, futurist) but trust required. Default style: Cyberpunk / Synthwave or Swiss / International. Default palette: Crypto Vibrant. Default fonts: Inter + JetBrains Mono. Density: medium.
- **Payments (Stripe, Square, PayPal).** Friction-reduced, security-cued. Default style: Swiss / International. Default palette: Payments Quiet Blue. Default fonts: Söhne + Söhne Mono (Stripe) or Inter + JetBrains Mono. Density: low (checkout) to medium (dashboard).

**Per-industry rules (fintech):**

- Numbers right-aligned in tables; tabular numerics (`font-variant-numeric: tabular-nums`) for all monetary values.
- Currency formatted with locale (£1,234.56 for UK; $1,234.56 for US; €1.234,56 for German). Document the locale in the project's `tokens.md`.
- Negative balances always have an explicit minus sign and colour treatment (red, but paired with shape per [`data-viz.md`](data-viz.md) for colour-blind safety).
- Confirmations for irreversible transactions are explicit modals, not toasts (per [`flows.md`](flows.md) § Confirmations & undo).
- Two-factor authentication is a designed flow, not an afterthought.
- Session expiry warnings appear before forced logout, not after.
- Statements and transactions support export to CSV/PDF.
- Calendar views for scheduled payments use real dates (not 'in 3 days'); ambiguity costs trust.
- Compliance footnotes (FDIC, FCA, ASIC) are visible on auth screens and account opening.
- Trading platforms: order book updates are interruptible (the user can cancel mid-transaction).

**Anti-patterns:**

- Playful microcopy on payment confirmations ('Yay! Money sent! 🎉').
- Generic profile illustrations instead of real account information.
- Loading spinners on transaction commits (the user has no idea if the money moved).
- Red-only state coding for losses without shape or position cue.
- Trading platforms with light mode by default (the audience uses dark mode for sessions of 8+ hours).
- Banking apps that hide the balance until the user signs in (privacy is good; total invisibility is hostile).

**Recommended catalogue picks (fintech):**

- Style: Swiss / International (consumer), Grid-heavy / data-dense (trading), Cyberpunk / Synthwave (crypto with audience match).
- Palette: Modern Fintech Indigo, Banking Navy, Trading Green-Red, Crypto Vibrant.
- Fonts: Inter + JetBrains Mono (default), IBM Plex Sans + IBM Plex Mono (institutional).

**Exemplars:** Monzo (monzo.com), Revolut (revolut.com), Wise (wise.com), Stripe (stripe.com), Coinbase (coinbase.com), Bloomberg Terminal (web equivalent), Robinhood (robinhood.com).

## Healthcare

Two audiences. Patient-facing leans warm, calming, plain language, large type. Clinician-facing leans dense, abbreviation-heavy, fast-scan. Never use alarming reds without context.

**Sub-categories:**

- **Patient-facing (telehealth, mental health, wellness).** Warm, calming, large type. Default style: Minimal or Editorial. Default palette: Patient Warm Teal or Wellness Sage. Default fonts: DM Sans + DM Sans or Manrope + Manrope. Density: low.
- **Clinician-facing (EHRs, hospital ops).** Dense, abbreviation-heavy, fast-scan. Default style: Grid-heavy / data-dense. Default palette: Clinical Blue. Default fonts: Inter + JetBrains Mono or IBM Plex Sans + IBM Plex Mono. Density: very dense.
- **Pharmacy / pharmaceutical reference.** Trusted, established, reference-like. Default style: Swiss / International + Documentation Quiet. Default palette: Pharmacy Green. Default fonts: Source Serif + Source Sans. Density: medium.

**Per-industry rules (healthcare):**

- Patient-facing: minimum body type 16px (better: 17-18px) for accessibility and audience age.
- Patient-facing: plain language; no medical jargon without an in-line explanation (or a 'What does this mean?' link).
- Clinician-facing: abbreviations are the language; spell-out tooltips on hover for newer staff.
- All: dates show absolute time, never just 'in 2 hours' (clinicians need to coordinate with shift schedules).
- Dosage and units always include the unit (mg, ml, IU); never bare numbers.
- Allergy and contraindication warnings are persistent banners at the top of patient records, not modals (modals get dismissed and forgotten).
- Patient identifiers (name, DOB, MRN) appear in the screen header on every clinical view.
- Print views are first-class designs (clinicians print prescriptions, lab orders, discharge summaries).
- Audit trail visible per record (who changed what, when).
- Data entry forms: tab order matches the clinician's keyboard workflow (chief complaint → history → exam → assessment → plan).

**Anti-patterns:**

- Alarming red used for non-urgent UI (delete buttons, trash icons). Reserve red for clinical alerts.
- Cute illustrations in clinical contexts (the work is serious).
- Patient apps with developer-tool aesthetic (cold, dense, jargon).
- Clinician apps with consumer aesthetic (large white space, oversized buttons).
- Modal-only critical alerts (clinicians dismiss reflexively; the alert disappears before it's read).

**Recommended catalogue picks (healthcare):**

- Style: Minimal (patient), Grid-heavy / data-dense (clinical), Editorial (educational/wellness).
- Palette: Patient Warm Teal, Clinical Blue, Wellness Sage, Pharmacy Green.
- Fonts: DM Sans + DM Sans (patient), Inter + JetBrains Mono (clinical), Source Serif + Source Sans (educational).

**Exemplars:** Epic (clinician-facing), Cerner (clinician-facing), Doximity (clinician-facing), Headspace (patient/wellness), Calm (patient/wellness), Babylon Health (patient).

## E-commerce

Splits by sub-type more than any other industry: DTC fashion (editorial), marketplace (information-dense, comparison-friendly), B2B (catalog-style, spec-heavy).

**Sub-categories:**

- **DTC fashion / beauty (Aēsop, Glossier, Allbirds).** Editorial, photography-led, generous white space. Default style: Editorial or Magazine. Default palette: DTC Editorial. Default fonts: Cormorant Garamond + Inter or Fraunces + Manrope. Density: very low.
- **Marketplace (Etsy, eBay, StockX).** Information-dense, comparison-friendly, search-driven. Default style: Card-based. Default palette: Marketplace Vibrant. Default fonts: Inter + Inter. Density: high.
- **B2B catalog (Grainger, McMaster-Carr).** Spec-heavy, scannable, reference-like. Default style: Documentation Quiet + Grid-heavy. Default palette: B2B Catalog. Default fonts: IBM Plex Sans + IBM Plex Mono. Density: very high.
- **Food delivery (Uber Eats, DoorDash).** Photo-forward, appetising, fast. Default style: Photo-forward. Default palette: Food Warm. Default fonts: Inter + Inter. Density: medium.

**Per-industry rules (e-commerce):**

- Product price always visible above the fold on PDP (product detail page).
- 'Add to cart' is the primary action; never compete with another button at the same visual weight.
- Stock availability stated explicitly ('In stock', '3 left', 'Out of stock'). Never silent absence.
- Product images: minimum 4 angles + a context shot (lifestyle); zoom on hover for desktop, pinch on mobile.
- Sizing chart accessible from the PDP, not buried in the footer.
- Reviews aggregated in a star rating + count; individual reviews sortable by helpfulness or recency.
- Cart visible from any page (icon in header with count badge).
- Checkout is single-page when possible; multi-step checkout shows progress (per [`flows.md`](flows.md) § Multi-step forms).
- Guest checkout supported; account creation optional (forced account creation kills conversion).
- Currency switcher visible if the site sells internationally.
- Returns policy linked from the cart and PDP.

**Anti-patterns:**

- Stock photography that looks like every other DTC brand.
- Forced account creation before checkout.
- Hidden shipping costs revealed only on the final checkout step.
- Auto-playing product videos with sound.
- Pop-up newsletter signups within the first 5 seconds of page load.
- Generic 'Submit' or 'Continue' buttons in the checkout flow.

**Recommended catalogue picks (e-commerce):**

- Style: Editorial (DTC fashion), Card-based (marketplace), Documentation Quiet (B2B), Photo-forward (food).
- Palette: DTC Editorial, Marketplace Vibrant, B2B Catalog, Food Warm.
- Fonts: Cormorant Garamond + Inter (DTC), Inter + Inter (marketplace), IBM Plex Sans + IBM Plex Mono (B2B).

**Exemplars:** Aēsop (aesop.com), Glossier (glossier.com), Allbirds (allbirds.com), Etsy (etsy.com), StockX (stockx.com), Grainger (grainger.com), McMaster-Carr (mcmaster.com), Uber Eats (ubereats.com).

## Creative tools

Dark by default. Tool-prominent UI. Canvas-first. The chrome must not influence colour perception (especially for photo, video, design tools).

**Sub-categories:**

- **Design / illustration (Figma, Sketch, Linear-design).** Dark-default. Tool palette in the chrome. Canvas takes the full viewport. Default style: Design Tool Dark. Default palette: Design Tool Dark. Default fonts: Inter + JetBrains Mono. Density: high (chrome).
- **Video / photo editors (Premiere, Final Cut, Photoshop).** Pure neutral chrome (the chrome must not bias colour perception). Default style: Photo Editor Neutral. Default palette: Photo Editor Neutral. Default fonts: Inter + Inter. Density: very high.
- **Music production (Logic, Ableton, GarageBand).** Tactile, instrument-like. Often skeuomorphic for hardware metaphors. Default style: Skeuomorphic or Music Studio Warm. Default palette: Music Studio Warm. Default fonts: Inter + Inter. Density: high.
- **3D / animation (Blender, Cinema4D, Unity).** Spatial, vibrant accents (each axis has a colour: X red, Y green, Z blue is convention). Default style: 3D Tool Vibrant. Default palette: 3D Tool Vibrant. Default fonts: Inter + JetBrains Mono. Density: extreme.

**Per-industry rules (creative tools):**

- Dark mode is the default; light mode is the alternative.
- Chrome stays out of the canvas; tools are in the periphery (sidebars, top bar, contextual panels).
- Keyboard shortcuts are first-class. Every tool has a keyboard binding documented in tooltips.
- Right-click menus are common (context-specific actions). Don't override the browser's native menu without strong reason in web apps.
- Undo / redo work with full history (the user expects ⌘Z to walk back hundreds of steps).
- Auto-save is essential; manual save is a backup, not the primary save mechanism.
- File format support is documented (which formats import, export, both).
- Performance matters more than other industries: lag during canvas operations is a deal-breaker.
- Cursor changes communicate state (drag, resize, rotate, paint).
- Selection states are visually clear (handles, marching ants, coloured outlines).

**Anti-patterns:**

- Light mode by default in tools used for hours of focused work.
- Chrome that bleeds colour into the canvas (warm-toned UI in a photo editor).
- Generic save dialogs; creative tools deserve thought-out file management.
- Modals blocking the canvas during work (the user is mid-thought).
- Onboarding tours that take over the full screen on first launch (the user came to make something).

**Recommended catalogue picks (creative tools):**

- Style: Design Tool Dark, Photo Editor Neutral, Music Studio Warm, 3D Tool Vibrant.
- Palette: Design Tool Dark, Photo Editor Neutral, Music Studio Warm, 3D Tool Vibrant.
- Fonts: Inter + JetBrains Mono (default), Geist + Geist Mono (modern dev-adjacent tools).

**Exemplars:** Figma (figma.com), Adobe Photoshop / Premiere, Cinema4D, Blender, Logic Pro, Ableton Live, Linear's design tools (in development).

## Social

Feed-driven. Minimal chrome around content. Engagement affordances clear (like, comment, share, save).

**Per-industry rules (social):**

- Feed is the primary surface; everything else is secondary.
- Engagement actions (like, comment, share, save, repost) are visible on every feed item without hover.
- Profile is reachable from any user mention or avatar.
- Notifications are designed (badge counts, notification feed, in-app deep links).
- Direct messages are first-class (often a separate tab or panel).
- Search supports users, posts, hashtags, and entities.
- Content reporting flow is accessible from every post (overflow menu).
- Creation flow is one tap from anywhere in the app (compose button is global).
- Time stamps relative for recent ('2h ago'); absolute for older ('Mar 14').
- Infinite scroll is the default for feeds; paginated for archives.

**Anti-patterns:**

- Marketing-page feeds (so much chrome that the content is squeezed).
- Engagement buttons that require hover to appear (mobile users are stuck).
- Notification UI that conflates types (a like and a DM look the same).
- Search that returns only one entity type.
- Composition flows that take more than 3 taps to start.

**Recommended catalogue picks (social):**

- Style: Minimal or Card-based.
- Palette: project's brand accent + Pure Slate or Cool Gray neutral.
- Fonts: DM Sans + DM Sans, Inter + Inter.

**Exemplars:** Bluesky (bsky.app), Threads (threads.net), Discord (discord.com), Slack (slack.com).

## Education

Clear progression cues. Achievement markers. Age-appropriate density.

**Per-industry rules (education):**

- Progress visible on every screen ('Lesson 3 of 8', course progress bar).
- Achievements (badges, streaks, certificates) celebrated proportionally to the effort required.
- Skip and back navigation always available; learners shouldn't be locked into a path.
- Quiz feedback explains the right answer when the learner gets it wrong.
- Difficulty scales: K-12 leans bright and friendly; higher ed leans restrained and reference-like.
- Plain language; jargon defined inline when introduced.
- Audio and video controls accessible (transcripts, captions, playback speed).
- Note-taking and bookmarking first-class (learners revisit content).
- Multi-device handoff (start on desktop, continue on mobile).
- Time estimates per lesson ('15 min read', '8 min video').

**Anti-patterns:**

- Quiz feedback that's binary right/wrong with no explanation.
- Progress that resets on accidental navigation.
- Locked content with no preview of what's behind the lock.
- Adult-targeted gamification on K-12 products (XP bars, level-up animations get tiresome).
- Reference-grade dryness on K-12 products.

**Recommended catalogue picks (education):**

- Style: Minimal (higher ed), Card-based (LMS), Illustrated (K-12).
- Palette: Higher Ed Conservative, K-12 Friendly, Course Platform Calm, Language Learning Vibrant.
- Fonts: Inter + Inter (higher ed), DM Sans + DM Sans (K-12), Lora + Inter (long-form learning).

**Exemplars:** Duolingo (duolingo.com), Khan Academy (khanacademy.org), Coursera (coursera.org), Brilliant (brilliant.org), Notion (for university LMS-style use).

## Communication

Presence and read-state critical. Threading patterns. Reply affordances.

**Per-industry rules (communication):**

- Presence indicator (online/idle/offline/typing) is visible per user in conversation lists and message threads.
- Read state visible per message (sent / delivered / read).
- Typing indicator surfaces in real time when another participant is composing.
- Message editing supported with an 'edited' marker (the recipient should know).
- Message deletion supported; deletion leaves a placeholder ('Message deleted by Alex').
- Reactions (emoji, custom, polls) accessible from every message.
- Threading or quoted-replies for longer conversations.
- Search across all conversations from a single entry point.
- Mentions (@user) trigger notifications; replies in threads do too.
- Voice and video calls integrated, not in a separate app.

**Anti-patterns:**

- Read receipts that can't be turned off (privacy violation by design).
- Message edits that silently change history (no 'edited' marker).
- Notification noise (every reaction triggers a push notification).
- Threaded replies hidden behind multiple taps.
- Search limited to current conversation.

**Recommended catalogue picks (communication):**

- Style: Swiss / International or Card-based.
- Palette: project's brand accent + Cool Gray neutral.
- Fonts: Inter + Inter, DM Sans + DM Sans.

**Exemplars:** Slack, Discord, Linear (in-app comments), Loom (async video communication), Cron / Notion Calendar.

## Completeness pressure tests

The brutal-honesty section. If the file doesn't show these screens, it's not comprehensive. It's a sales demo or a brochure.

### SaaS pressure test

> *If the file does not show roles, permissions, empty states, loading states and error recovery, it is not comprehensive. It is a sales demo.*

Required screen set:

- **Auth.** Sign-in, sign-up, password reset, MFA, SSO, session-expired.
- **Workspace.** No-workspace state, create workspace, workspace switcher, workspace settings.
- **Navigation.** Global nav, collapsed nav, breadcrumbs, search, notifications.
- **Core product.** Dashboard, list view, detail view, create flow, edit flow, delete-restore.
- **Admin.** Users, roles, permissions, billing, integrations, audit log.
- **System states.** Empty state per primary surface, loading state per primary surface, error state per primary surface, no-permission state, read-only state, plan-restricted state, trial-expired state, job-running state.

If the design covers only the dashboard and the marketing site, it's not a SaaS design. It's a sales demo.

### Website pressure test

> *If the file does not show mobile navigation, forms, validation, cookie/consent states, SEO heading structure and CMS template behaviour, it is not comprehensive. It is a brochure mock-up.*

Required screen set:

- **Mobile nav.** Hamburger or mega-menu open and closed; bottom-nav for mobile-first.
- **Forms.** Submitting state, success state, error state, validation in-line.
- **Cookie / consent.** Banner, preference modal, accepted state, declined state.
- **Fault states.** 404, 500, offline.
- **CMS templates.** Blog index, article template, author page, category page.
- **SEO.** Meta titles, descriptions, Open Graph cards visible per template.

If the design covers only the homepage and one product page, it's not a website. It's a brochure mock-up.

### Mobile pressure test

> *If the file does not show keyboard states, permissions, offline behaviour, platform navigation and safe-area handling, it is not comprehensive. It is resized desktop design.*

Required screen set:

- **Splash and first launch.** Splash screen, welcome, onboarding (per [`flows.md`](flows.md) § Onboarding flows).
- **Permissions.** Push notifications, camera, microphone, location, contacts (each as designed prompt + denied state).
- **Authentication.** Biometric prompt (Face ID / Touch ID / fingerprint), passcode fallback.
- **Connectivity.** Offline state, sync-failed state, sync-success state.
- **Notifications.** Push notification appearance, in-app notification, notification settings.
- **Keyboard-open.** Form layouts adjusted for the keyboard (input visible, accessory bar present).
- **Safe-area handling.** Notch, home indicator, dynamic island, status bar (per [`mobile-patterns.md`](mobile-patterns.md) § Safe areas).
- **Sheet detents.** Peek, half, full (where used).

If the design covers only the home tab and the create flow, it's not a mobile app. It's a resized desktop design.

## Pencil expression

Industry context lives in two places:

1. **`assets/design-system/visual-style.md`** records the project's industry and the chosen style/palette/font picks. The agent reads this at the start of every design pass.
2. **The `.pen` file's `Cover` frame** (per [`file-architecture.md`](file-architecture.md)) records the project's industry, scope, and links to the brief. The agent reads the Cover at session start.

When the agent designs a new screen, it cross-references the industry's must-have list (above) against the project's existing screens. If the project is a SaaS but lacks a 'no-permission' or 'plan-restricted' state, the agent surfaces that gap to the user: *'I notice the design doesn't cover the no-permission state. Should I add it?'*

## Anti-patterns (cross-industry)

- **Industry-mismatched style.** Brutalist healthcare. Cyberpunk for retirement planning. Editorial for a developer tool. Pick a style the audience can read.
- **Sales-demo SaaS.** Only happy paths designed. No error, empty, no-permission states. The completeness pressure test fails.
- **Brochure-mockup website.** Only the homepage designed. No mobile nav, no forms, no fault states.
- **Resized-desktop mobile.** Desktop designs scaled to mobile widths without rethinking the navigation, the keyboard, or the safe areas.
- **Industry conventions ignored.** Trading platform with light mode default. Healthcare patient app with developer-tool aesthetic. Educational LMS with adult-only gamification.

## Sources

- **Industry exemplars (accessed 2025/2026):** Linear, Vercel, Stripe, Notion, GitHub, Cursor, Things, Cron, Raycast (SaaS); Monzo, Revolut, Wise, Stripe, Coinbase, Bloomberg, Robinhood (fintech); Epic, Cerner, Doximity, Headspace, Calm (healthcare); Aēsop, Glossier, Etsy, McMaster-Carr (e-commerce); Figma, Adobe, Cinema4D, Blender, Logic Pro (creative tools); Bluesky, Threads, Slack, Discord (social/communication); Duolingo, Khan Academy, Coursera (education).
- **Apple Human Interface Guidelines (iOS 18 / iPadOS 18 / visionOS 2)**: per-platform conventions referenced in mobile and creative-tools sections.
- **Material 3 (Google)**: Android conventions referenced in mobile sections.
- **WCAG 2.2 (ISO/IEC 40500:2025)**: minimum body type sizes, contrast, accessible authentication patterns referenced in healthcare and education sections.
- **Refactoring UI** (Adam Wathan, Steve Schoger): density and visual-hierarchy principles applied across industries.
- **Nielsen Norman Group**: research on industry-specific UX patterns (e.g., e-commerce checkout, healthcare clinical workflows, fintech trust signals).
- **Baymard Institute**: research on e-commerce conversion patterns referenced in the e-commerce section.
- **Industry compliance frameworks**: HIPAA (healthcare), PCI-DSS (payments), GDPR (any EU-touching), SOC 2 (B2B SaaS) inform some completeness pressure-test items.

## See also

- [`style-catalogue.md`](style-catalogue.md): the named UI styles each industry section recommends.
- [`colour-palettes.md`](colour-palettes.md): the palette recipes each industry section recommends.
- [`font-pairings.md`](font-pairings.md): the typography pairings each industry section recommends.
- [`states.md`](states.md): the empty/loading/error state vocabulary the completeness pressure tests require.
- [`flows.md`](flows.md): the onboarding, settings, search flows referenced in industry rules.
- [`layout-patterns.md`](layout-patterns.md): the layouts each industry favours (dashboards, settings, list-detail).
- [`microcopy.md`](microcopy.md): the voice patterns that match each industry register.
- [`mobile-patterns.md`](mobile-patterns.md): the mobile-specific patterns required by the Mobile pressure test.
- [`data-viz.md`](data-viz.md): chart-type selection for analytics, fintech, healthcare dashboards.
- [`file-architecture.md`](file-architecture.md): the Cover frame that records the project's industry.
- [`assets/design-system/visual-style.md`](../assets/design-system/visual-style.md): the project's chosen industry-aligned style commitment.
- [`example-style-selection.md`](../assets/examples/example-style-selection.md): worked example of picking style + palette + fonts per industry (Phase 4).
