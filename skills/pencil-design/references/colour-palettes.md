# Colour palettes

A library of starting palette *recipes* the agent picks from when starting greenfield. Each entry names a neutral family and an accent scale from an established source system (Tailwind, Radix Colors, IBM Carbon, Material 3, Apple HIG). The agent looks up the actual hex values from the source, then commits them to the project's `assets/design-system/tokens.md` and the `.pen` file's `variables` via `set_variables` MCP calls. After commitment, every design references the project's tokens (`$bg`, `$accent`), never literal hex from this catalogue.

**What this file owns:** 40+ named palette recipes tagged by industry and mood. Each entry: name, mood, accent scale (named, with source), neutral pairing, when to use.

**What this file does NOT own:** the project's actual hex values. Those live in `assets/design-system/tokens.md` (project-owned, version-controlled) and in the `.pen` file's `variables` section (live in the design). This file does not define the project's palette; it lists the menu of starting picks the agent surfaces.

Colour theory and the two-role-architecture rule are in `SKILL.md` § Aesthetic defaults: Colour. Colour-blind-safe palettes specifically for charts are in [`data-viz.md`](data-viz.md). The chosen style (which constrains the palette) is in [`style-catalogue.md`](style-catalogue.md).

## When to load this file

- The agent is starting a greenfield design and the project has no `assets/design-system/tokens.md` populated yet.
- The user names an industry or mood ('fintech', 'calming', 'warm', 'serious') and the agent needs a starting palette to anchor the design.
- The agent is following [`example-style-selection.md`](../assets/examples/example-style-selection.md) (Phase 4) and needs to pick the palette half of the style + palette + font triple.
- The user wants to see palette options before committing.

## How this catalogue works (architecture)

Three layers; the catalogue sits at the top.

1. **This file (`references/colour-palettes.md`)** is a *menu of starting recipes*. Each recipe names a neutral family and an accent scale from an established source system. The recipes don't hold the project's palette; they're the starting point.
2. **The source systems** hold the actual hex values. The agent looks up the values at the source URLs (Tailwind: https://tailwindcss.com/docs/colors. Radix: https://radix-ui.com/colors. IBM Carbon: https://carbondesignsystem.com/elements/colour. Material 3: https://m3.material.io/styles/color. Apple HIG: https://developer.apple.com/design/human-interface-guidelines/color).
3. **`assets/design-system/tokens.md`** records the project's *committed* palette. The agent copies the chosen scale's hex values into this file as semantic tokens (`$bg`, `$surface`, `$border`, `$textPrimary`, `$accent`, etc.). This file is project-owned; the user can edit it.
4. **The `.pen` file's `variables` section** is the live design's palette. The agent calls `set_variables` MCP to populate the variables from the project's `tokens.md`. Designs reference `$tokenName`, never literal hex.

The rule: **the agent reads this catalogue once at the start of a project, then never again.** Subsequent designs reference the project's variables. If the user wants to change the palette, they edit `tokens.md` and the `.pen` variables; this catalogue stays untouched.

## Workflow (greenfield)

1. Identify the project's industry from the brief, or ask the user.
2. Pick a neutral family from the Neutrals section below.
3. Pick an accent palette from the matching industry section. Cross-check the mood with the chosen style from [`style-catalogue.md`](style-catalogue.md).
4. Look up the full hex scale from the source system cited in the recipe.
5. Populate `assets/design-system/tokens.md` with the chosen scale as semantic tokens (`$accent`, `$bg`, etc.).
6. Call `set_variables` MCP to mirror the tokens into the `.pen` file's `variables` section.
7. Record the chosen palette recipe name in `assets/design-system/visual-style.md`.
8. From this point onward, design with `$tokens`. Never with literal hex.

See [`example-style-selection.md`](../assets/examples/example-style-selection.md) (Phase 4) for the full worked sequence including the `set_variables` invocation.

## Two-role architecture refresher

Per `SKILL.md` § Aesthetic defaults: Colour, every palette has two roles: a neutral family (4 to 6 shades for backgrounds, surfaces, borders, text) and 1 to 3 accent hues (for primary actions, highlights, brand). The catalogue below splits these so the agent picks one neutral and pairs it with one accent.

## Neutral families (pick one as the base)

The neutral family is the foundation. It carries the backgrounds, surfaces, borders, and text. The accent rides on top.

| Name | Hue cast | Source scale | When to use |
|---|---|---|---|
| **Pure Slate** | Cool blue-grey | Tailwind Slate (50 → 950) | Default for B2B SaaS, developer tools, technical products |
| **Cool Gray** | Pure neutral | Tailwind Gray (50 → 950) | Most flexible; pairs with any accent |
| **Zinc** | Slightly warm grey | Tailwind Zinc (50 → 950) | When pure grey reads as cold |
| **Stone** | Warm beige-grey | Tailwind Stone (50 → 950) | Editorial, lifestyle, warm consumer |
| **Mauve** | Slight purple cast | Radix Mauve (1 → 12) | Modern, slightly elevated; pairs with purple/violet/pink accents |
| **Sage** | Slight green cast | Radix Sage (1 → 12) | Calm, organic; pairs with green/teal accents |
| **Olive** | Slight yellow-green cast | Radix Olive (1 → 12) | Editorial, food, lifestyle |
| **Sand** | Warm beige | Radix Sand (1 → 12) | Warm consumer, hospitality, fashion |
| **Carbon Gray** | Cool, slightly bluish | IBM Carbon Gray (10 → 100) | IBM-style enterprise products |
| **Apple Gray** | iOS native | Apple systemGray + systemGray2-6 | Native iOS / iPadOS apps; Apple ecosystem products |

Each scale has 10 to 12 steps with semantic meaning (steps 1-2 = app backgrounds; 3-5 = component backgrounds; 6-8 = borders; 9-10 = solid surfaces; 11-12 = text, in the Radix model). The agent looks up the steps at the source URL and maps them to the project's semantic tokens.

## B2B SaaS palettes (10)

Calm, professional, accent-led. Most B2B SaaS lives in the indigo/blue/violet range with a calm neutral base.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **Indigo Calm** | Calm, focused | Tailwind Indigo | Pure Slate or Cool Gray | Default modern SaaS; productivity tools; project management |
| **Iris Premium** | Premium, modern | Radix Iris | Mauve | Premium SaaS that wants more depth than Indigo |
| **Sky Open** | Open, friendly | Tailwind Sky | Cool Gray | Communication, collaboration, social SaaS |
| **Blue Trust** | Stable, trustworthy | Tailwind Blue | Pure Slate | Conservative SaaS; B2B with trust requirements (HR, contracts, legal-adjacent) |
| **Violet Creative** | Creative, modern | Tailwind Violet | Mauve | Design tools, creative SaaS, prosumer products |
| **Emerald Growth** | Growth, energy | Tailwind Emerald | Pure Slate | Analytics, growth tools, sales-led SaaS |
| **Teal Calm-Energy** | Balanced energy | Tailwind Teal | Sage | Modern SaaS that wants warmth without going warm |
| **Cyan Tech** | Technical, fresh | Tailwind Cyan | Pure Slate | Developer tools, infrastructure, monitoring |
| **Rose Personal** | Personal, modern | Tailwind Rose | Stone | Consumer-leaning SaaS; HR products that want warmth |
| **Amber Bold** | Bold, energetic | Tailwind Amber | Stone | Marketing tools, sales-led products |

## Fintech palettes (6)

Trust comes from restraint. Most fintech leans cool and conservative; consumer fintech can lean warmer.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **Banking Navy** | Conservative, established | Tailwind Blue (deeper steps, 700-900) | Pure Slate | Traditional banking, wealth management, established institutions |
| **Modern Fintech Indigo** | Modern, trustworthy | Tailwind Indigo (700) | Pure Slate | Modern challenger banks (Monzo, Revolut, Wise patterns) |
| **Trading Green-Red** | Active, real-time | Tailwind Green + Red paired (state-coded) | Cool Gray (often dark-default) | Trading platforms, crypto exchanges, market data. Pair with shape coding per [`data-viz.md`](data-viz.md) for colour-blind safety. |
| **Payments Quiet Blue** | Calm, friction-reduced | Tailwind Sky | Cool Gray | Payment processors, checkout flows |
| **Crypto Vibrant** | Energetic, on-chain | Tailwind Violet + Cyan accent | Pure Slate (often dark-default) | Web3, DeFi, crypto wallets |
| **Investment Conservative** | Premium, considered | Tailwind Emerald (deep steps, 700-900) | Stone | Investment platforms, wealth advisory, financial planning |

## Healthcare palettes (5)

Patient-facing leans warm and calming; clinician-facing leans cooler and more technical. Avoid alarming reds without context.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **Patient Warm Teal** | Calm, reassuring, warm | Tailwind Teal | Sand | Patient-facing apps, telehealth, mental health, wellness |
| **Clinical Blue** | Clinical, professional, fast-scan | Tailwind Blue | Cool Gray | Clinician-facing, EHRs, hospital ops, medical research |
| **Wellness Sage** | Organic, calming, slow | Radix Sage (steps 9-11) | Sage | Meditation, mindfulness, wellness apps |
| **Pharmacy Green** | Trusted, established | Tailwind Emerald | Cool Gray | Pharmacy, pharmaceutical reference, prescription management |
| **Pediatric Friendly** | Friendly, approachable, slightly playful | Tailwind Sky + Amber secondary | Stone | Children's healthcare, pediatric apps |

## E-commerce palettes (6)

Varies wildly by sub-type: DTC fashion (editorial), marketplace (information-dense), B2B (catalog-style).

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **DTC Editorial** | Premium, photographic | One brand accent (e.g. Tailwind Rose) on Stone deep ground | Stone | DTC fashion, beauty, lifestyle e-commerce (Aēsop, Glossier patterns) |
| **Marketplace Vibrant** | Active, comparison-friendly | Tailwind Orange | Cool Gray | General marketplaces (Etsy, eBay patterns) |
| **B2B Catalog** | Spec-heavy, scannable | Tailwind Blue | Cool Gray | B2B parts catalogues, distributor sites, industrial supply |
| **Luxury Mono** | Premium, restrained | Black + white only; one accent reserved for brand moments | Stone | Luxury fashion, jewellery, premium goods |
| **Food Warm** | Appetising, warm | Tailwind Amber | Sand | Food delivery, recipe sites, restaurant marketing |
| **Sustainable Earth** | Honest, organic, considered | Tailwind Lime (deeper steps) | Sage | Sustainability-led brands, organic goods |

## Creative tools palettes (5)

Often dark-default. The chrome stays out of the way; the canvas is the brand.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **Design Tool Dark** | Focused, premium, dark-default | Radix Iris (dark steps 9-11) | Mauve dark | Design tools, illustration apps, prototyping (Figma, Linear-design patterns) |
| **Code Editor Dark** | Technical, syntax-friendly | Tailwind Cyan | Pure Slate dark | Code editors, IDEs, developer tools |
| **Photo Editor Neutral** | Quiet, reveals colour | Pure neutral with one cool accent (Tailwind Sky 500) | Cool Gray (often dark-default) | Photo editors, video editors (the chrome must not influence colour perception) |
| **Music Studio Warm** | Tactile, instrument-like | Tailwind Amber | Stone dark | DAWs, music production tools |
| **3D Tool Vibrant** | Spatial, vibrant | Tailwind Violet + Cyan + Lime (state-coded) | Pure Slate dark | 3D modelling, animation, VR tools |

## Education palettes (4)

Clarity over personality. Age matters: pediatric leans bright; higher ed leans restrained.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **K-12 Friendly** | Bright, friendly, approachable | Tailwind Sky + Amber secondary | Stone | Primary and secondary education products |
| **Higher Ed Conservative** | Considered, academic | Tailwind Indigo (deeper steps) | Cool Gray | University LMS, academic research tools |
| **Language Learning Vibrant** | Energetic, motivating | Tailwind Green + Yellow highlight | Stone | Duolingo-style language and skill-building apps |
| **Course Platform Calm** | Focused, low-distraction | Tailwind Teal | Sage | Online course platforms, MOOC-style products |

## Media / publishing palettes (4)

Type leads. Colour supports the type; it doesn't compete.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **Editorial Mono** | Authoritative, type-led | Black + white with one Tailwind Red 700 accent for emphasis | Stone | Newspapers, long-form publications, premium blogs |
| **Magazine Vibrant** | Considered, photographic | One bold accent per issue (Tailwind Rose, Amber, Violet) | Stone | Lifestyle magazines, fashion editorial, food publications |
| **Documentation Quiet** | Quiet, scannable, reference-friendly | Tailwind Sky | Cool Gray | Technical documentation, knowledge bases, API references |
| **Blog Personal** | Warm, individual, considered | One personality accent per project | Stone | Personal blogs, indie publications |

## Consumer / lifestyle palettes (5)

Warm, approachable, personality-led. The brand often is the palette.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **Hospitality Warm** | Inviting, warm, premium | Tailwind Amber (deeper steps) | Sand | Hotels, restaurants, travel, hospitality |
| **Fitness Energy** | Motivating, energetic | Tailwind Lime or Orange | Stone | Fitness apps, sport tracking, athletic products |
| **Beauty Soft** | Soft, premium, considered | Tailwind Pink (lighter steps) | Stone | Beauty, skincare, premium personal care |
| **Travel Wanderlust** | Adventurous, optimistic | Tailwind Sky + Amber secondary | Stone | Travel booking, holiday planning, destination guides |
| **Pet / Family Warm** | Friendly, soft, approachable | Tailwind Orange (lighter steps) | Stone | Pet care, family products, kids-and-parents |

## Dark-mode-first variations (6)

When the product ships dark mode as primary and light mode as a less-common alternative. The accent often desaturates compared to its light-default variant.

| Palette | Mood | Accent scale | Neutral pairing | When to use |
|---|---|---|---|---|
| **Linear Dark** | Premium, focused, dark | Tailwind Indigo (lighter steps for dark mode) | Pure Slate dark | Productivity tools used for hours; Linear pattern |
| **Cursor Dark** | Technical, terminal-adjacent | Tailwind Cyan | Pure Slate dark | Developer tools, IDEs, terminal-style products |
| **Spotify Dark** | Brand-led dark | Tailwind Green | Custom near-black ground (the project commits the exact value in tokens) | Media products with strong brand colour |
| **Discord Dark** | Community, casual | Tailwind Indigo | Custom dark-grey ground | Community products, chat, gaming |
| **Arc Browser Dark** | Modern, calm, dark | Per-space accent (the project commits) | Mauve dark | Browsers, single-window-focused products |
| **Vision Pro Glass** | Translucent, layered | Per-app accent over translucent base | Custom (uses backdrop-filter blur) | visionOS apps, glassmorphic interfaces |

## Pairing recommendations by industry

When in doubt, the agent picks one of these tested pairings:

| Industry | Recommended palette recipe |
|---|---|
| Modern SaaS (default) | Pure Slate + Indigo Calm |
| Developer tool | Pure Slate dark + Cursor Dark |
| Fintech (consumer) | Pure Slate + Modern Fintech Indigo |
| Fintech (trading) | Pure Slate dark + Trading Green-Red (with shape coding for accessibility) |
| Healthcare (patient) | Sand + Patient Warm Teal |
| Healthcare (clinical) | Cool Gray + Clinical Blue |
| Marketing site (any SaaS) | Stone + project's brand accent (one colour from the SaaS table) |
| DTC fashion | Stone + DTC Editorial |
| Code editor | Pure Slate dark + Code Editor Dark |
| Long-form publishing | Stone + Editorial Mono |
| Hospitality | Sand + Hospitality Warm |
| Fitness | Stone + Fitness Energy |

## Contrast and accessibility

Every recipe in this catalogue is built from source systems that meet WCAG 2.2 AA at typical body-text sizes (4.5:1 contrast for normal text, 3:1 for large text and UI components) when the recommended neutral and accent pair on standard backgrounds. APCA equivalents (Lc 75 for body, Lc 60 for large text) are met in light mode for all primary accents.

When the agent commits a palette into `tokens.md`:

1. Verify the accent on the chosen surface meets contrast. APCA contrast checker: https://www.myndex.com/APCA/.
2. Verify the dark-mode accent on the dark surface meets contrast independently. Light-mode accents rarely transfer cleanly to dark mode; the agent picks a 1-2 shade lighter step.
3. Check colour-blind safety using a simulator (Stark, Sim Daltonism, Chrome DevTools Vision Deficiencies). Red and green together fail for ~8% of male users; pair with shape, position, or text labels per [`data-viz.md`](data-viz.md).

The Radix Colors system encodes accessibility into the scale itself: each step is contrast-tested against the others. When the agent picks a Radix recipe, the scale's own documentation indicates which step pairs with which.

## Pencil expression

A chosen palette recipe maps to the project's `tokens.md` and the `.pen` file's `variables`. Example sequence:

1. Agent picks 'Indigo Calm' (Tailwind Indigo + Pure Slate).
2. Agent looks up the Tailwind Indigo scale (50, 100, 200, ..., 900, 950) and the Tailwind Slate scale at https://tailwindcss.com/docs/colors.
3. Agent populates `assets/design-system/tokens.md` with semantic tokens:
   - `$bg` = Slate 50 (light) / Slate 950 (dark)
   - `$surface` = Slate 100 / Slate 900
   - `$border` = Slate 200 / Slate 800
   - `$textPrimary` = Slate 900 / Slate 100
   - `$textSecondary` = Slate 600 / Slate 400
   - `$accent` = Indigo 600 / Indigo 400
   - `$accentHover` = Indigo 700 / Indigo 300
   - `$success` = Emerald 600 / Emerald 400
   - `$warning` = Amber 500 / Amber 400
   - `$danger` = Red 600 / Red 400
4. Agent calls `set_variables` MCP to mirror these into the `.pen` file's `variables` section.
5. Agent records the palette recipe name in `assets/design-system/visual-style.md`: *'Palette: Indigo Calm. Source: Tailwind v4 (Indigo and Slate scales). APCA Lc 75+ verified across both modes.'*
6. Subsequent designs reference `$accent`, `$bg`, `$textPrimary`, etc. via `batch_design`. The agent never types literal hex into `batch_design` for surfaces, accents, or text.

For the worked example, see [`example-style-selection.md`](../assets/examples/example-style-selection.md) (Phase 4).

## Anti-patterns

- **Hard-coding hex from this catalogue into `batch_design`.** This file is a menu of recipes, not a source of values. Hex codes belong in `assets/design-system/tokens.md` and the `.pen` file's `variables`. Designs reference tokens.
- **Inventing hex codes.** Lifting random hex codes from a Dribbble shot rarely produces a coherent system. Pick a recipe from the catalogue, then look up the scale at the source.
- **Mixing neutral families.** A Slate background with a Stone surface clashes. Pick one neutral family and stick to it.
- **Light-mode accent transferred to dark mode unchanged.** The accent that pops on white often disappears on near-black. The agent picks a lighter step (1-2 shades up) for dark mode and verifies contrast.
- **Five colours competing.** Two-role architecture exists for a reason. One neutral + one accent + state colours (success/warning/danger) is plenty.
- **Red-green only state coding.** Fails for colour-blind users. Pair with shape, position, or text per [`data-viz.md`](data-viz.md).
- **Custom recipe when a sourced one would do.** A bespoke palette is a maintenance burden. Pick from the catalogue first; deviate only when the brand requires it, and record the deviation in `visual-style.md`.

## Sources

- **Tailwind v4 colour system**: https://tailwindcss.com/docs/colors. The 22 default colour scales (Slate, Gray, Zinc, Neutral, Stone, Red, Orange, Amber, Yellow, Lime, Green, Emerald, Teal, Cyan, Sky, Blue, Indigo, Violet, Purple, Fuchsia, Pink, Rose) used throughout this catalogue.
- **Radix Colors**: https://radix-ui.com/colors. Semantic 12-step scales with built-in accessibility (steps 9-10 for solid backgrounds, 11-12 for text). Mauve, Sage, Olive, Sand neutrals and Iris, Jade, Bronze accents referenced.
- **IBM Carbon design system v11**: https://carbondesignsystem.com/elements/colour. Carbon Gray scale and semantic interactive token model.
- **Material 3 dynamic colour (Google)**: https://m3.material.io/styles/color. The Material Colour Utilities and Material You dynamic colour generation.
- **Apple system colours**: documented in Apple HIG (https://developer.apple.com/design/human-interface-guidelines/color). systemBlue, systemGreen, systemIndigo, systemOrange, systemPink, systemPurple, systemRed, systemTeal, systemYellow plus systemGray scale.
- **WCAG 2.2 (ISO/IEC 40500:2025)**: 4.5:1 normal text and 3:1 large text contrast ratios applied throughout.
- **APCA (Advanced Perceptual Contrast Algorithm)**: https://www.myndex.com/APCA/. Lc 75 for body text, Lc 60 for large text.
- **Real-product palette references (accessed 2025/2026)**: Linear, Cursor, Spotify, Discord, Arc Browser, Vision Pro UI, Aēsop, Glossier, Monzo, Revolut, Wise, Stripe, Notion, Vercel.
- **Colour-blind safety guidance**: derived from Okabe-Ito 2002 (cited in [`data-viz.md`](data-viz.md)) and current Web Content Accessibility Guidelines 2.2.

## See also

- [`style-catalogue.md`](style-catalogue.md): the named UI styles that constrain palette choice.
- [`font-pairings.md`](font-pairings.md): typography pairings to pair with the chosen palette.
- [`industry-patterns.md`](industry-patterns.md): per-industry pattern density and which palettes belong where.
- [`data-viz.md`](data-viz.md): colour-blind-safe palettes for charts and dashboards.
- [`accessibility.md`](accessibility.md): contrast verification, APCA, WCAG 2.2 baseline.
- [`assets/design-system/tokens.md`](../assets/design-system/tokens.md): where the chosen palette gets recorded as project tokens (the destination, not this file).
- [`example-style-selection.md`](../assets/examples/example-style-selection.md): worked sequence of catalogue → MCP variable population → starter components (Phase 4).
