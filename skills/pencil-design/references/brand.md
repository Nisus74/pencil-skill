# Brand register

Brand work is design where the design *is* the product: marketing pages, landing pages, campaign sites, conference microsites, portfolios, manifesto pages, launch pages. The page exists to make the user feel something specific about the brand. Everything else is in service of that feeling.

This reference is the depth behind the brand entry in SKILL.md's register section. If you're working on app surfaces, dashboards, or admin tools, you want [product.md](product.md) instead.

## The anti-reference move

Before naming what the brand IS, name what it explicitly is NOT. This is the single highest-leverage move in brand work and the one the model defaults to skipping.

The reason: training data has aesthetic gravity. AI products default to violet-on-cream. Fintech defaults to navy and gold. Conference microsites default to pastel plus asymmetric grids plus heavyweight serif. Healthcare defaults to white and teal with smooth illustrations. If you start with *"what should this brand look like,"* you get pulled into the category default before you've thought about it. If you start with *"this brand is explicitly NOT X, Y, or Z,"* you've cut off the gravity wells before they pull.

Ask the user (or extract from their brief) at least one of:

- A brand or product in their category they don't want to look like
- An aesthetic family they want to escape (*"SaaS cream"*, *"developer-tool dark mono"*)
- A specific reference that isn't in the obvious lane (a band's site, a magazine, museum signage)

If none is available, name your own anti-reference. *"This is a fintech site that explicitly isn't navy and gold; the direction is editorial-typographic with a single saturated accent."* Then design against it.

## Reflex-reject aesthetic lanes (current as of 2026)

These aesthetic families are over-represented in current AI training data. They read as machine-generated the moment they appear, regardless of execution quality. Refuse them as defaults; require explicit brand direction to override.

| Lane | Tells | Why it reads AI |
|---|---|---|
| **Cabinet Grotesk + Fraunces editorial** | The two fonts as default display + body pair, large hero, restrained palette | Used in many AI-tool launch pages from 2024 onward |
| **Conference microsite pastel** | Pastel background, sans-serif display, asymmetric grid, geometric shapes | Saturated by AI conference and developer-event sites |
| **AI-product cream-on-warm** | Off-white background (`#FAFAF7` adjacent), warm grey text, single saturated accent (often violet or orange), Inter | The default OpenAI/Anthropic/Cursor-adjacent aesthetic |
| **Developer-tool dark mono** | Pure-black or near-black background, monospace everywhere, single neon accent, hairline borders | Linear-inspired SaaS, exhausted by 2025 |
| **Crypto neon-on-black** | Glowing accents, gradient text, futurist sans on black | Web3 saturation, reads dated |
| **SaaS purple gradient** | Violet-to-indigo gradient hero, white card grid below, soft drop shadows | Common across B2B SaaS landings 2020–2024 |
| **Bento-grid product showcase** | 4–6 cards in a bento layout, mixed sizes, dark mode | Apple-inspired saturation, reflex-reject as a default product page |

If the user's direction explicitly names one of these (they want the SaaS purple gradient because that's their actual brand), follow them. These lanes are reflex-defaults to refuse without intent, not absolute prohibitions.

## Colour strategy

Pick one of four commitment levels before picking specific colours. The level matches the aesthetic intent; cycling through levels mid-design is what makes brand work feel scattered.

### Restrained
Tinted neutrals plus one accent used at ≤10% of the surface area. The brand's identity carries through type, layout, and rhythm rather than colour. Fits brand work that wants to feel mature, editorial, or technical without being austere.

Moves: an off-white background tinted toward the brand hue, a charcoal body, a single saturated accent on CTAs and emphatic moments.

### Committed
One saturated colour carries 30–60% of the surface. The colour IS the brand for the duration of the page. Fits identity-driven brands where the colour is the most recognisable asset.

Moves: a hero in the brand colour at full saturation, supporting sections in tinted variants of the same hue, body type in a high-contrast neutral.

### Full palette
3–4 named roles, each used deliberately. Each role gets its own surface treatment. Fits brand campaigns and editorial work where the palette tells a story across sections.

Moves: red sections for one mood, green for another, blue for a third, neutral chapters between.

### Drenched
The surface IS the colour. No off-canvas, no neutral relief. The colour goes wall to wall. Fits brand heroes, campaign launch pages, manifesto pages, anywhere the colour itself is the message.

Moves: a full-bleed coloured viewport, type sitting directly on the colour, photography or illustration in a tonally-related palette.

Default to restrained unless the brand's identity demands more. The "one accent ≤10%" rule from SKILL.md is restrained only; committed, full palette, and drenched exceed it on purpose. Don't collapse every design to restrained by reflex. For OKLCH theory and palette construction, see [color-and-contrast.md](color-and-contrast.md).

## Typography

Type does more brand work than any other axis. Pick a pairing with intent.

### What's exhausted by reflex
- **Cabinet Grotesk + Fraunces** as the default display + body pair. Both are good fonts; the *pair* is the AI-tool launch reflex. Don't reach for it unless the brand specifically wants editorial-warm.
- **Inter as the default body**. Inter is the strongest AI tell after pure black on pure white. Reach for Söhne, Geist, Satoshi, SF Pro, or an editorial serif body before falling back to Inter.
- **Generic serifs as display** (Garamond, Georgia, Times). These read as *"I didn't pick a font."* Use a deliberate serif (Fraunces, Editorial New, Instrument Serif, Tiempos, GT Sectra) or skip serif entirely.

### Pairings that work for brand

| Direction | Display | Body |
|---|---|---|
| Editorial | Tiempos, Instrument Serif | Söhne, Inter (sparingly) |
| Brutalist-editorial | GT America Mono | Söhne |
| Warm-confident | Recoleta | Söhne |
| Expressive display | Clash Display, Editorial New | A quiet sans |
| Technical-mono | JetBrains Mono, Berkeley Mono | Same monospace (rare and committed) |
| All-serif | Tiempos for everything | Same family (calm, magazine-like) |
| All-grotesque with personality | PP Neue Montreal, Söhne | Same family, hierarchy through weight |

### Scale and hierarchy
- Display sizes for brand can go larger than product (96–160px hero type is fine; 24–36px section headings).
- Body line length 60–75ch.
- Weight contrast between display and body matters more than size alone. A heavy display (700–900) paired with a regular body (400) carries emphasis without inflating scale.

For per-character moves (small caps, all-caps tracking, italic restraint, OpenType stylistic sets), see [typography.md](typography.md).

## Density, rhythm, hero anatomy

Brand work tolerates much more whitespace than product work. Rhythm is intentional pauses, not packed information.

### Hero anatomy beyond the SaaS template
The hero-metric template is banned in SKILL.md anti-patterns. Brand heroes have richer options:

- **One sentence plus one image.** The sentence does the brand work; the image carries the feeling.
- **One huge sentence.** The sentence at 120–160px IS the hero. No supporting copy.
- **Editorial open.** Date or kicker, headline, one-paragraph deck, then content. Reads as long-form rather than landing.
- **Quote hero.** A single user quote at scale, attribution underneath.
- **Atmospheric.** A video or animation behind a minimal headline.
- **Cold open.** The page starts with the content itself, no hero. Confident.

### Rhythm
Vary spacing deliberately between sections. The same vertical padding everywhere reads as templated. Pick one shape per page:

- **Asymmetric:** some sections breathe, others pack in tight.
- **Crescendo:** tight at the top, expansive at the bottom.
- **Pulse:** alternate dense and airy sections through the page.

### Don't wrap everything in a container
Most things don't need one. Edge-bleed text, full-bleed images, sections that don't respect a max-width can all add brand confidence. Use the container only where the content actively benefits from one.

## Motion

Brand can be choreographed in a way product cannot. The page-load sequence is part of the brand.

- **Page-load sequence.** Hero copy appears in steps (kicker, headline, deck, CTA) over 600–1200ms. Each step eases out with an exponential curve (ease-out-quart or ease-out-expo).
- **Scroll-anchored reveals.** Sections fade and translate in as they enter the viewport. Keep the translate small (8–16px) and the ease quick (200–300ms). Reveal once; don't replay on scroll-back.
- **Expressive hover affordances on CTAs.** A CTA can grow, shift, reveal a secondary element. More expression here is fine; product motion is much tighter.

Avoid:
- Bouncing or elastic ease curves (read as overdone in 2026)
- Parallax on long pages (exhausted)
- Scroll-jacking (the user owns the scroll)
- Continuous background animations that compete with content

## Brand-specific anti-patterns

In addition to the bans in SKILL.md, brand work has its own:

- **Scroll-to-explore copy and animated chevrons.** The user knows how to scroll.
- **AI-elevate copy register.** *"Elevate your workflow"*, *"Unleash the power of"*, *"Seamless integration"*, *"Empowering teams"*. Strike all of these. See [ux-writing.md](ux-writing.md) for the full list and the replacement vocabulary.
- **The trust strip of 8 grayscale customer logos.** Templated; reads as *"any B2B SaaS."* If you must include social proof, pick 3–4 logos and treat them with brand intent.
- **The feature grid of 3–6 identical cards.** Equal-size cards with icon, heading, paragraph. Reach for differentiated section anatomy where each section earns its shape.
- **The pricing comparison table with three columns and a recommended-tier highlight.** Saturated. Reach for a different pricing anatomy whenever the user hasn't specifically asked for the columns.
- **The testimonial carousel.** Static, well-typeset quotes outperform a carousel almost every time. The carousel hides quotes the user might have read.
- **The big-number stats section.** *"10M users. 99.9% uptime. $50B processed."* Reads as filler. Use one specific story over five generic numbers.

## Pencil-specific

### Setting the brand mode
For brand pages designed dark, set the theme mode on the page frame:

```
Update("<pageFrameId>", { theme: { mode: "dark" } })
```

### Variable strategy by colour strategy
The four colour strategies map to different variable shapes:

- **Restrained:** `$bg`, `$bgSurface`, `$text`, `$textMuted`, `$accent`. One accent variable, light + dark values per.
- **Committed:** `$brand`, `$brandSurface`, `$brandSurfaceMuted`, `$onBrand`. The brand colour gets surface and on-colour treatments.
- **Full palette:** `$mood1`, `$mood2`, `$mood3` plus on-colour text per mood. Document which mood maps to which section in the `context` strings.
- **Drenched:** a single `$surface` the whole page sits on, plus `$onSurface` for text.

Declare these via `SetVariables` (inside `batch_design`) before placing any frames so every colour resolves to a token, never raw hex.

### Per-section frames vs single fluid frame
Brand pages with dramatic section-level layout shifts (dense hero, wide editorial body, narrow CTA) suit per-breakpoint frames with explicit layout per breakpoint. Single fluid frames work for brand pages with simpler architecture where the same auto-layout holds together across sizes.

### Image strategy
Use `Generate(nodeId, "ai", "<prompt>")` for hero imagery early in the design loop so the page has something concrete to compose against. Make the prompt specific (camera, lens, lighting, subject); generic prompts produce generic imagery. Replace AI placeholders with real assets before declaring the design done.

### Composition aids
For long-form editorial brand pages, build a single canvas frame per breakpoint and use `snapshot_layout` periodically to verify rhythm. The screenshot loop will surface visual issues; `snapshot_layout` surfaces the numbers behind them (gaps, padding, section heights) when something looks off and you can't read the pixels.
