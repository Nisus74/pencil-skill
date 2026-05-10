# conversion-focused-saas

> Marketing surfaces that earn the buy through monumental confident design; the marketing IS product-caliber and reads as a careful software artefact.

**Surface category:** marketing-websites
**Confidence:** confirmed via direct review of linear.app (May 2026); Stripe and Vercel cited from public knowledge.
**Exemplars:** Linear (primary, fully reviewed), Stripe (secondary), Vercel (secondary)

## When to choose this archetype

Pick this when the user is silent on aesthetics and the brief is "marketing site for a modern SaaS / dev-tool / AI product." This archetype suits products that compete on craft as much as feature set: the marketing site itself functions as the strongest proof point. Avoid when the product is consumer-led (`playful-brand-led` fits better), highly editorial (`editorial-storytelling`), or aggressively brutal (`brutalist-statement`). If the user supplied direction or named a brand, follow that and use this file as scaffolding.

## Typography

- **Display headlines:** large, geometric, modern sans. Linear uses `Inter Display`-grade typography; Stripe uses their custom `Sohne`-derived stack. Treat as the same family of choice. Sized 48–80px on hero, 32–48px on section heads.
- **Body:** same family as display, regular weight. 16–18px for marketing copy (larger than app surfaces). Generous line-height (1.5–1.65) for legibility.
- **Numerals:** monospace inside data and code blocks. Pricing displays use proportional figures with currency notation, not monospace.
- **Numbered section labels:** decimal pattern (`1.0`, `2.0`, `2.1`) is signature for this archetype, it reads as a deliberate system. Linear's homepage uses `1.0 Intake / 2.0 Plan / 3.0 Build / 4.0 Diffs / 5.0 Monitor`. Render the decimal in a smaller mono or display weight beside the section heading.
- **The Inter family is allowed** here when used as `Inter Display` deliberately, the same override as `modern-pro-tool`. Avoid generic Inter on body.

## Density

- Hero is generous: 120px+ vertical padding, large headline, restrained subhead, single primary CTA.
- Feature sections breathe but not as much as editorial archetypes, section padding 80–120 vertical, content max-width 1200.
- Pricing tiers and comparison tables are tighter (card padding 24–32) so cards read as a comparable set.
- Footer is dense, multi-column (Linear uses 5 columns: Product / Features / Company / Resources / Connect). Each column 6–10 short links.

## Accent strategy

- One primary accent. Linear uses cyan/turquoise on certain interactive elements with purple/lavender for badges. Stripe uses their indigo. The accent appears in: primary CTA, link affordances, badges/labels, occasional gradient sweeps on hero backgrounds.
- Saturation 60–80%. This is not the screaming-gradient era of the late 2010s; restrained but unmistakable.
- Status / category tags appear as small filled badges with the accent or muted siblings of it.
- Gradients allowed but used as ambient backgrounds (radial sweeps behind a hero) or signature edges on cards. Not as button fills.

## Surface treatment

- **Dark mode default for marketing.** This is the late-2020s convention for confident SaaS. Light mode often available as a toggle, but the canonical design lives in dark. (Note: the *app* surface for the same products is often light by default, see `modern-pro-tool`, and the archetypes intentionally diverge.)
- Sharp corner geometry: card radius 12–16, button radius 8–12. No fully-rounded pills outside small chips.
- Surface hierarchy: `$bg` (page, near-black or warm dark) > `$surface` (cards, slightly lighter) > `$surfaceMuted` (footer, secondary blocks). Three levels.
- Borders are present but subtle (1px, low contrast). Soft shadows on cards in dark mode show up as faint glows around the upper edge.

## Data display

- Marketing pages use product screenshots as the primary visual treatment, not stock photography or illustration. The actual UI of the product appears in feature sections (Linear shows their issue detail view, Kanban backlog, timeline chart, code diff, analytics dashboard, weekly summary audio player).
- Carousels of UI variants per feature section (Linear uses 8–9 image variants per feature, suggesting rotating screenshots).
- Inline charts (when shown) use the product's actual chart style. They're proof, not decoration.
- Code blocks use monospace, dark surface, syntax highlighting that respects the page's accent.

## Microcopy and voice

- Confident, almost prescriptive. Hero headlines make claims and let them stand.
- Verbatim Linear examples to anchor tone: *"The product development system for teams and agents"*, *"Purpose-built for planning and building products. Designed for the AI era."*, *"Issue tracking is dead"*, *"A new species of product tool."*, *"Built for purpose"*, *"Plan the present. Build the future."*, *"Built for the future. Available today."*
- Section copy is one-line confident, not feature lists: *"Make product operations self-driving"*, *"Define the product direction"*, *"Move work forward across teams and agents"*, *"Review PRs and agent output"*.
- The `Method` / philosophy page is a signature move: an editorial manifesto positioning the company as thought leader, not vendor. Linear's Method opens with *"There is a lost art of building true quality software."* and prescribes principles like *"Write issues not user stories"*, *"Build in public"*, *"Launch and keep launching"*.
- Customer testimonials prefer quantified metrics over flowing quotes: *"2.0x increase in filed issues"*, *"3.3x faster issue resolution"*, *"28% issues authored by agents"*, *"compressed bug resolution time by 52%"*. Logos of recognisable enterprises (OpenAI, Vercel, Cursor, Coinbase, Ramp, Mercury, Brex) build the credibility floor.
- Pricing copy uses the *"All [Previous tier] features +"* pattern (Linear) with annual-only billing presented as the assumption, not a toggle.

## Motion personality

- Marketing motion is purposeful, not ambient. Hero headline reveals on scroll (subtle slide + opacity 200–300ms). Section transitions use staggered fades. Product screenshot carousels rotate every 4–6 seconds.
- Avoid: parallax backgrounds, continuous ambient particle motion, infinite-scrolling logos that strobe attention away from copy.
- Hover affordances are quick (120–160ms), same snappy feel as the app counterpart.

## Anti-cues (don't reach for these in this archetype)

- Stock photography of diverse smiling office workers.
- Three-card "Why choose us" feature grids with bullet lists.
- Gradient-filled CTAs with multi-stop colour ramps.
- "We help businesses do X" generic value props.
- Animated chevrons / "scroll to explore" prompts under the hero.
- Glass-morphism, backdrop blur, or maximalist 3D illustrations on the hero.
- Customer testimonials as decorative cards with five-star ratings.
- Generic AI-buzzword headlines without specific product framing.
- Toggle for monthly/annual when the business model is annual-only, just say so.
- Gigantic illustrated hero scenes that compete with the product screenshot.

## Worked example: a marketing site for a developer-tool SaaS

Imagine a brief like *"build a marketing site for a code-review-with-agents product"* in this archetype:

- **Top nav:** logo left, primary nav (Product / Resources / Customers / Pricing / Method / Contact) centred, Open app + Sign up right-aligned. Thin top border, no backdrop fill.
- **Hero:** centred headline at 64–72/600, *"Code review for teams and agents"*. Subhead at 18/400, *"Designed for the AI era. Pull requests review themselves."*. Primary CTA *"Try the new model"* with a small accent gradient sweep behind the hero. No animated chevron beneath; the section just ends.
- **Feature sections (numbered):** `1.0 Intake → 2.0 Diff → 3.0 Review → 4.0 Merge`. Each section is a bold one-line headline plus a product screenshot carousel showing the actual UI. Decimal label appears in muted display weight to the left of the section title.
- **Method page** at `/method`: editorial manifesto-style, opening with a confident philosophical claim. Numbered sections (1.1 / 1.2 / 2.1...) for principles. No screenshots; type-led only.
- **Customers section:** logo grid of recognisable enterprises, then quantified metrics (*"2.4x faster review cycles"*) above written case studies with thumbnails and *"Read story →"* links. Mix in 2–3 video testimonials.
- **Pricing:** 4 tiers (Free / Basic / Business / Enterprise). Annual-only billing stated as the model. Cards use the *"All Free features +"* pattern. Comparison table below the cards. Single trust-signal line: *"Trusted by more than X teams"*.
- **Footer:** 5 dense columns (Product / Features / Company / Resources / Connect), social icons, legal at the bottom.

## Notes for AI implementers

Tokens this archetype implies (illustrative; rename to project's scheme):

| Token | Value |
|---|---|
| `$accent` | Cyan, turquoise, or chosen brand hue at 60–80% saturation. Linear-canonical: a cool cyan with purple support. |
| `$accentSupport` | Purple/lavender for badges and category labels (Linear pairs cyan + purple). Optional. |
| `$bg` | Near-black warm dark (`#0E0E10` or similar) for marketing. Light mode supported but not canonical. |
| `$surface` | One step lighter than `$bg`. |
| `$surfaceMuted` | Footer, secondary blocks. |
| `$borderSubtle` | Very low-contrast 1px. |
| `$fontDisplay` | `Inter Display` (canonical override of SKILL.md default), `Söhne`, or `Geist`. |
| `$fontBody` | Same family, regular weight. |
| `$fontMono` | `Geist Mono` or `JetBrains Mono` for code blocks and decimal section labels. |

Components most affected: `MarketingHero`, `NumberedSection`, `ProductScreenshotCarousel`, `MethodSection` (editorial manifesto), `CustomerLogoGrid`, `MetricCallout`, `PricingTier`, `ComparisonTable`, `FooterMega` (5-column dense). Each gets a variant inside this archetype.

Common slip-ups:

- Defaulting to light mode because the app is light. Marketing flips: dark canonical, light optional.
- Using stock photography or generic illustrations. Use the actual product's UI as the imagery.
- Writing generic value props (*"Boost your productivity"*) instead of confident specific claims (*"Issue tracking is dead"*).
- Adding a Method page that summarises features (it's a manifesto, not a glossary).
- Skipping the numbered section labels because they feel "extra". They're signature.
- Showing prices in monospace tabular figures. Pricing pages use proportional currency notation; mono is for code and data, not money.
- Adding a monthly/annual toggle when the business model is annual-only.
- Letting customer testimonials sprawl into long quotes. Quantified metrics + logo recognition do more lifting.
