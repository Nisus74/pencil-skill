# Style catalogue

A library of named UI styles the agent picks from when starting greenfield. Most AI-generated designs default to an inoffensive neutral SaaS look because nothing told the agent to commit to a direction. This file is the menu. Pick one style, lean into it, and the design has an opinion.

**What this file owns:** 30+ named UI styles with mood, when-to-use guidance, anti-pattern, sample component cues, and real-world exemplars. The styles are organised loosely by family (modernist, expressive, technical, retro) for navigation; the agent can pick from any family per project.

**What this file does NOT own:** the project's *committed* style. That lives in `assets/design-system/visual-style.md` (when the project has chosen one). The visual tokens (colours, type scale, spacing) lift to `assets/design-system/tokens.md`. Component anatomy is in [`composition-patterns.md`](composition-patterns.md).

## When to load this file

- The agent is starting a greenfield design and the project has no `assets/design-system/visual-style.md` yet.
- The user says 'make it feel like Linear' or 'I want a brutalist look' or names any aesthetic direction.
- The design feels generic and the agent needs to commit harder to one style (per [`iteration-patterns.md`](iteration-patterns.md) § Failure mode: too generic).
- The user is exploring directions and wants to see options before committing.

## How to use the catalogue

1. The agent reads the user's brief and any reference images.
2. The agent picks one style from the catalogue that fits the brief. If no fit is obvious, the agent surfaces 2 to 3 candidate styles and asks the user to pick.
3. The chosen style's mood, anti-pattern, and sample-component cues become the constraints on the design.
4. When the design ships, the chosen style gets recorded in `assets/design-system/visual-style.md` so future agents (and future iterations) stay coherent.
5. The MCP `set_variables` call populates the project's tokens to match the style. See [`example-style-selection.md`](../assets/examples/example-style-selection.md) (Phase 4) for the worked flow.

Each entry below carries: a short description, the *mood* it lands in, *when to use it*, *anti-pattern* (the most common way the style ships wrong), *sample components* (what a button or card looks like in this style), and *exemplars* (real products that ship the style well).

## Modernist family

Restrained, geometric, type-led. The dominant family for B2B SaaS in 2025/2026.

### Swiss / International

- **Mood:** rational, calm, confident, type-forward.
- **When to use:** information-dense products where clarity wins (analytics, finance, technical docs, project management).
- **Anti-pattern:** so restrained it reads as cold. Counter with one warm accent or a single hand-drawn touch.
- **Sample components:** flat backgrounds, single-line dividers, sans-serif type (Inter, Helvetica, Söhne, Geist), tight letter-spacing on headings, generous whitespace.
- **Exemplars:** Linear (linear.app), Vercel (vercel.com), Stripe (stripe.com), Apple's developer documentation.

### Editorial

- **Mood:** considered, premium, magazine-quality.
- **When to use:** content-led products (publishing platforms, long-form reading, knowledge bases, premium SaaS marketing pages).
- **Anti-pattern:** the body type fights the headline; the page reads as cluttered. The serif/sans pairing has to feel intentional, not random.
- **Sample components:** serif display headings (Fraunces, Recoleta, GT Sectra, Source Serif), sans-serif body, drop caps on long-form, grid-based layouts, subtle dividers, asymmetric photography.
- **Exemplars:** The Pudding (pudding.cool), Stripe Press, Notion's marketing pages, Pitch (pitch.com).

### Bento

- **Mood:** modern, structured, slightly playful, dense.
- **When to use:** marketing pages with multiple value props, dashboards with mixed-density tiles, product feature showcases.
- **Anti-pattern:** every tile the same size and weight, which collapses the bento back into a grid. The asymmetry must be deliberate.
- **Sample components:** asymmetric tile grid (one big tile, several small), rounded corners (12-16px), subtle gradients or photography in each tile, headline-per-tile.
- **Exemplars:** Apple iPhone 16 product page, CleanShot X (cleanshot.com), Linear feature pages, Raycast (raycast.com).

### Minimal

- **Mood:** quiet, confident, slow.
- **When to use:** consumer apps where the product itself is the focus (writing apps, calendar apps, single-purpose utilities).
- **Anti-pattern:** so minimal the user can't find anything. Affordances must remain obvious; minimalism applies to chrome, not to wayfinding.
- **Sample components:** monochromatic palette with one accent, tight type scale (3-4 sizes total), no decorative shadows or borders, generous padding on every component.
- **Exemplars:** Things 3 (culturedcode.com), Cron (now Notion Calendar), iA Writer (ia.net), Bear (bear.app).

### Card-based

- **Mood:** organised, scannable, modular.
- **When to use:** browsable catalogues (e-commerce, app stores, project lists, asset browsers).
- **Anti-pattern:** every screen becomes a card grid. The card pattern owes the eye some variation; mix card layouts with list views or hero sections.
- **Sample components:** elevated cards (subtle shadow + rounded corners), consistent card width, hover lift, image-led card top, metadata-led card bottom.
- **Exemplars:** Apple App Store, Notion (page browser), Pinterest, Behance (behance.net).

## Expressive family

Personality-led, brand-forward, unafraid of taking up space.

### Brutalist

- **Mood:** bold, raw, anti-corporate.
- **When to use:** creative tools, agency portfolios, niche developer tools, independent media. Not for fintech or healthcare.
- **Anti-pattern:** brutalism done as 'ugly type plus chaos' rather than as compositional confidence. The grid still matters; brutalism breaks it deliberately, not accidentally.
- **Sample components:** monospace or display type set huge, hard edges (no border-radius), high-contrast colour blocks (often black + one neon), system fonts (Helvetica, Times) used unironically, asymmetric layouts.
- **Exemplars:** Are.na (are.na), Bloomberg Businessweek (digital), Read The Docs original theme, many Awwwards winners 2024/2025.

### Neobrutalist

- **Mood:** playful brutalism, colourful, slightly ironic.
- **When to use:** indie SaaS, design tools targeting creatives, products with personality budget.
- **Anti-pattern:** uniform 4px black borders on everything, which becomes its own kind of templated. Vary the offset shadow direction and depth.
- **Sample components:** thick black borders (2-4px), offset hard shadows (no blur), bright primary colours (yellow, cyan, magenta), playful typography.
- **Exemplars:** Gumroad (gumroad.com), Tally Forms (tally.so), several open-source UI kits in 2025.

### Maximalist

- **Mood:** abundant, layered, unapologetic.
- **When to use:** brand-led marketing pages, creative portfolios, products with strong personality.
- **Anti-pattern:** maximalism without hierarchy reads as chaos. The layers must compete in service of one focal point per screen.
- **Sample components:** layered photography, multiple typefaces, gradients, textures, animated backgrounds, generous use of colour.
- **Exemplars:** Spotify Wrapped microsites, Stripe Sessions event sites, Beats by Dre product pages.

### Anti-design

- **Mood:** deliberately rule-breaking, post-modern, ironic.
- **When to use:** rare. Cultural products, art platforms, fashion sites where the rejection of 'good design' is the point.
- **Anti-pattern:** confused with 'we don't know how to design'. The rules must be visibly broken on purpose.
- **Sample components:** clashing colour palettes, broken grids, intentional 'mistakes' (overlapping text, off-baseline alignment), system-default fonts.
- **Exemplars:** Balenciaga (balenciaga.com at various points), Crack Magazine, SSENSE editorial pages.

### Memphis revival

- **Mood:** playful, retro 1980s, geometric.
- **When to use:** kids' products, education, creative tools targeting younger audiences.
- **Anti-pattern:** dated stock-illustration look. The geometric shapes need to feel custom, not pulled from a free vector pack.
- **Sample components:** bold geometric shapes (squiggles, circles, triangles), saturated 80s palette (peach, teal, lemon, magenta), playful sans serif (Recoleta, DM Sans), pattern fills.
- **Exemplars:** Slack's 2019-era marketing pages, Mailchimp historical branding, Duolingo product pages.

## Technical family

Built for power users; density is a feature.

### Terminal / Hacker

- **Mood:** technical, dense, no-nonsense.
- **When to use:** developer tools, CLIs with web UIs, infrastructure dashboards, security products.
- **Anti-pattern:** 'developer aesthetic' applied to a non-technical product. The user has to actually be a developer for this to land.
- **Sample components:** monospace type throughout (JetBrains Mono, IBM Plex Mono, Geist Mono), dark background by default, syntax-highlighted code blocks, command-palette-driven nav, keyboard-shortcut hints visible.
- **Exemplars:** Vercel (vercel.com), GitHub (in dark mode), Linear's command palette, Cursor (cursor.sh), Warp (warp.dev).

### Grid-heavy / data-dense

- **Mood:** information-rich, scannable, professional.
- **When to use:** trading platforms, analytics dashboards, project management at scale, BI tools.
- **Anti-pattern:** density without hierarchy. The user can't find the most important number on the screen.
- **Sample components:** tabular layouts, fixed row heights, sortable columns, sparklines inline with numbers, conditional formatting, frozen panes.
- **Exemplars:** Bloomberg Terminal (web equivalent), Linear's issue list, GitHub's pull request list, Stripe's transaction views.

### Material 3

- **Mood:** Android-native, dynamic colour, accessible.
- **When to use:** Android apps, cross-platform products targeting Android-first users.
- **Anti-pattern:** Material 3 components mixed with iOS conventions, which feels confused. Commit to Material on Android, HIG on iOS.
- **Sample components:** Material 3 components (filled buttons, FAB, snackbar, segmented buttons), dynamic colour from the user's wallpaper, expressive type scale.
- **Exemplars:** Google's apps on Android (Gmail, Calendar, Photos), Tasks.org (open-source).

## Retro / revival family

Aesthetic time-travel done with restraint.

### Y2K revival

- **Mood:** nostalgic 2000-2003, glossy, colourful.
- **When to use:** consumer apps targeting Gen Z, music products, fashion, anything intentionally nostalgic.
- **Anti-pattern:** parody. The references must feel like a homage, not a costume.
- **Sample components:** chrome gradients, frosted glass effects, candy-bright accents (electric blue, hot pink, lime green), pixel-bordered icons, blurred bokeh backgrounds.
- **Exemplars:** Frank Ocean's Blonded Radio site, several Bandcamp redesigns, Dazed Digital.

### Cyberpunk / Synthwave

- **Mood:** neon, dark, future-retro.
- **When to use:** gaming products, music, certain crypto/Web3 brands, niche creative tools.
- **Anti-pattern:** neon-on-neon-on-black with no contrast hierarchy. The eye burns out and the design becomes unreadable.
- **Sample components:** dark backgrounds (near-black or deep navy), neon accents (cyan, magenta, yellow), monospace headings, scan-line textures, holographic effects, glowing borders.
- **Exemplars:** Hyperreal (hyperreal.org), several Web3 projects, Cyberpunk 2077 marketing site.

### Newsprint

- **Mood:** authoritative, journalistic, considered.
- **When to use:** publishing platforms, premium editorial brands, long-form blogs, archives.
- **Anti-pattern:** newspaper-as-skin without earning the authority. The content has to live up to the visual claim.
- **Sample components:** high-contrast serif headlines, multi-column body type, classified-ad-style metadata, no rounded corners, restrained colour palette (black + one accent).
- **Exemplars:** The New York Times, Read The Docs (modern theme), Hacker News (in spirit if not aesthetic).

### Magazine

- **Mood:** photographic, layered, cover-quality.
- **When to use:** lifestyle products, fashion, food, travel, premium consumer brands.
- **Anti-pattern:** magazine-style without the photography budget to back it up. The hero photos have to be original or premium-licenced.
- **Sample components:** full-bleed hero photography, large display type overlapping the photo, generous gutters, pull quotes, asymmetric grids.
- **Exemplars:** Apple product pages, Aēsop (aesop.com), Bandcamp's editorial sections.

## Atmospheric family

Mood-led, often borrowing from physical materials.

### Glassmorphism

- **Mood:** translucent, layered, futuristic.
- **When to use:** consumer apps with rich photography behind the chrome, OS-style products, AR/VR interfaces.
- **Anti-pattern:** glass on glass on glass with nothing behind it, which becomes muddy. Glassmorphism needs a colourful background to read.
- **Sample components:** translucent panels (`backdrop-filter: blur(20px)`), subtle borders (`rgba(white, 0.2)`), layered colourful backgrounds, soft shadows.
- **Exemplars:** Apple's iOS lock screen and Control Center, Apple Vision Pro UI, several music apps on iOS.

### Soft UI / Neumorphism

- **Mood:** soft, tactile, restrained.
- **When to use:** rare. Personal projects, meditation apps, products where softness is the brand. Has accessibility cost.
- **Anti-pattern:** soft buttons that look identical regardless of state. Disabled, hover, and pressed states all need clear differentiation.
- **Sample components:** monochromatic palette, subtle dual shadows (light from top-left, dark from bottom-right), no hard borders, low-contrast affordances.
- **Exemplars:** Dribbble showcases circa 2020, Calm (calm.com) in places.

### Dark-mode-first

- **Mood:** focused, premium, easy on the eyes.
- **When to use:** developer tools, design tools, video/photo editing, creative products, anything used for long sessions.
- **Anti-pattern:** dark mode that's just light-mode-with-inverted-colours. True dark mode adjusts hue saturation, shadow direction, and accent colours independently.
- **Sample components:** near-black backgrounds (#0a0a0a, not #000), elevated surfaces lighter not darker (#1a1a1a, #2a2a2a), reduced-saturation accents, soft shadows from below not from corners.
- **Exemplars:** Linear, Cursor, Arc Browser, Spotify, Discord.

### Skeuomorphic

- **Mood:** literal, tactile, period-1990s-2010s.
- **When to use:** music apps where 'tape', 'vinyl', or 'instrument' metaphors land. Niche creative tools.
- **Anti-pattern:** skeuomorphism applied to non-physical metaphors (a 'paper' invoice doesn't gain anything from looking like paper).
- **Sample components:** textured surfaces (felt, wood, leather), realistic shadows, 3D-rendered controls, photographic icons.
- **Exemplars:** GarageBand (Apple), Korg Gadget, several boutique music apps.

## Hand-crafted family

The opposite of templated.

### Hand-drawn

- **Mood:** warm, human, indie.
- **When to use:** creative tools, education, small-scale consumer products, personal portfolios.
- **Anti-pattern:** hand-drawn elements mixed with crisp UI. The drawings need to inform the whole system, not decorate one corner.
- **Sample components:** hand-drawn icons or illustrations, slightly imperfect strokes, marker or pencil textures, friendly type (Caveat, Patrick Hand, custom hand-lettering).
- **Exemplars:** Dropbox Paper (its early days), Glide (glideapps.com), several Notion templates.

### Illustrated

- **Mood:** narrative, friendly, branded.
- **When to use:** consumer onboarding, education, marketing pages where the brand has invested in custom illustration.
- **Anti-pattern:** stock illustration sets that show up in three other products you've seen this month.
- **Sample components:** custom illustration in heroes and empty states, consistent illustration style across the system, usually flat-with-personality (not photorealistic).
- **Exemplars:** Mailchimp, Headspace, Calm's marketing, Slack's customer story pages.

### Photo-forward

- **Mood:** premium, magazine-quality, brand-led.
- **When to use:** consumer products with hero photography (food, travel, fashion, hardware), premium B2B that wants to feel personal.
- **Anti-pattern:** stock photography. The hero shots have to be commissioned or sourced from a premium library, and consistent in style.
- **Sample components:** full-bleed hero photos, photographic backgrounds in feature sections, headshots in testimonials, high-quality product photography.
- **Exemplars:** Apple, Aēsop, Stripe's customer story pages, Linear's homepage hero in places.

### Type-forward

- **Mood:** typographic, restrained, premium.
- **When to use:** publishing, design tools, premium SaaS where the brand is the typography.
- **Anti-pattern:** type-as-decoration without the underlying structure. Type-forward design needs an opinion on every type-related decision (tracking, leading, weight pairings, optical sizing).
- **Sample components:** large display type (Fraunces, Söhne, GT America, Geist), tight tracking on headlines, restrained palette, minimal imagery, type-as-hero.
- **Exemplars:** Pitch (pitch.com), several creative agency sites, Vercel (typography is the brand).

### Mono-tone

- **Mood:** focused, restrained, confident.
- **When to use:** brand-led products that want to lean entirely on one colour family.
- **Anti-pattern:** mono-tone but every state uses a different shade with no system. The shade scale needs to be deliberate.
- **Sample components:** one hue family (10-12 shades from near-white to near-black), no other colours except possibly one accent for state, type-led hierarchy.
- **Exemplars:** Vercel (mono-tone with one accent), Notion (mono-tone with one product accent), Linear (near mono-tone in its Dark theme).

## Picking a style

A few decision shortcuts for the agent:

- **B2B SaaS, no strong brand direction.** Default to Swiss / International. Add Bento for marketing pages.
- **Developer tool, technical audience.** Terminal / Hacker, often paired with Dark-mode-first.
- **Consumer app, personality-led brand.** Pick from the Expressive family (Brutalist, Neobrutalist, Maximalist) based on the brand's voice.
- **Publishing or content-led.** Editorial or Newsprint depending on register.
- **Fintech or healthcare.** Stay in the Modernist family. Trust signals come from restraint, not personality.
- **Creative tool.** Dark-mode-first, often paired with Type-forward or Maximalist for marketing.
- **Multiple value props on a marketing page.** Bento (instead of three-card grid).

When the agent isn't sure, surface 2 to 3 candidates. *'I think this could be Swiss / International (clean and quiet) or Editorial (more premium, more typography-led). Which feels closer to what you're after?'*

## Pencil expression

A chosen style maps to two layers of the project:

- **`assets/design-system/visual-style.md`** records the chosen style and any deviations: *'Style: Swiss / International with Bento for marketing pages. Deviations: warmer accent colour (#FF6B35) instead of the typical Swiss blue, to land closer to the brand's energy.'*
- **`assets/design-system/tokens.md`** holds the type, colour, and spacing tokens that match the style. The agent populates them via `set_variables` MCP calls. See [`example-style-selection.md`](../assets/examples/example-style-selection.md) (Phase 4) for the worked sequence.

When designing a new screen, the agent reads `visual-style.md` first to recall which style applies, then constrains every choice to that style. A Brutalist project doesn't get glassmorphic modals; a Swiss project doesn't get Memphis-shaped dividers.

## Anti-patterns

- **Inoffensive default.** No style picked, no opinion shown. Reads as templated.
- **Style cocktail.** Three styles in one design (Brutalist hero, Glassmorphic modal, Bento features). Pick one.
- **Style applied to chrome only.** The hero is brutalist; the rest of the product is generic SaaS. Commit across the system.
- **Style without the supporting tokens.** Picking 'Editorial' but using a sans-serif body font with default tracking. The style needs the typography to support it.
- **Style at odds with the audience.** Brutalist healthcare. Cyberpunk for retirement planning. Pick a style the audience can read.

## Sources

- **Real-world product exemplars (accessed 2025/2026):** Linear, Vercel, Stripe, Notion, Apple product pages, Things 3, Cron, Arc Browser, Raycast, Cursor, Pitch, GitHub, Spotify, Mailchimp, Slack, Discord, Tally Forms, Gumroad, CleanShot X, Dropbox Paper, Headspace, Calm, Aēsop, The New York Times, Bandcamp, Bloomberg.
- **Refactoring UI** (Adam Wathan, Steve Schoger): the typography, colour, and shadow principles underlying many of these styles.
- **Apple Human Interface Guidelines (iOS 18 / iPadOS 18 / visionOS 2)**: Glassmorphism patterns (Vision Pro UI), Skeuomorphism in music apps, Photo-forward hero photography conventions.
- **Material 3 (Google)**: Material 3 style entry; dynamic colour and Android-native conventions.
- **WCAG 2.2 (ISO/IEC 40500:2025)**: contrast and accessibility considerations applied to dark-mode-first, glassmorphism, and soft UI styles where accessibility cost is highest.
- **Awwwards, Site Inspire, and design publications (Sidebar, Brand New)**: surveys of brutalist, anti-design, neobrutalist, and Y2K revival exemplars.
- **Style movement history**: Swiss / International (post-WWII Swiss design schools), Memphis Group (1980s Italian design), Y2K (early 2000s consumer software), brutalism (mid-2010s web revival).

## See also

- [`assets/design-system/visual-style.md`](../assets/design-system/visual-style.md): the project's chosen style, lifted from this catalogue (when populated, Phase 4).
- [`colour-palettes.md`](colour-palettes.md): industry-tagged colour palettes to pair with the chosen style.
- [`font-pairings.md`](font-pairings.md): typography pairings to pair with the chosen style.
- [`industry-patterns.md`](industry-patterns.md): which styles pair with which industries.
- [`iteration-patterns.md`](iteration-patterns.md) § Failure mode: too generic: the rescue when the design isn't committing to a style.
- [`layout-patterns.md`](layout-patterns.md): the layouts each style favours (Bento maps to bento; Editorial maps to alternating-rows; etc.).
- [`example-style-selection.md`](../assets/examples/example-style-selection.md): worked example of picking a style + palette + font pairing and populating tokens via `set_variables` (Phase 4).
