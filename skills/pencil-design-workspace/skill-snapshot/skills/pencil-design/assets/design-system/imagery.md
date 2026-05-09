# Imagery

Photos, illustrations, and AI-generated visuals. **Delete this file if your project is mostly chrome and data** (internal SaaS, dashboards) — imagery decisions matter most for marketing surfaces, content products, and content-heavy app states.

The agent reads this when adding a hero image, an empty-state illustration, an avatar fallback, or any visual that isn't a chart or icon.

## Image style

Pick one of these and stay there. Mixing styles in one product is the strongest "asset library cobbled from three Pinterest boards" tell.

| Style | What it looks like | Best for |
|-------|--------------------|----------|
| **Editorial photography** | Real, contextual, slightly imperfect. People in real environments. | Marketing for human-centered products. |
| **Product photography** | Clean, controlled, often on a neutral background. | Hardware, physical-good brands. |
| **Abstract photography** | Macro, textures, gradients in real materials. | Brand-forward, less explicit narrative. |
| **Line illustration** | Single-weight, flat, mode-agnostic. | Empty states, docs, calm SaaS marketing. |
| **Filled illustration** | Shapes + color, brand palette. | Marketing heroes, onboarding, story-driven. |
| **Isometric illustration** | 3D-ish, technical-feeling. | Developer tools, infrastructure products. |
| **3D / render** | Heavy lift, hard to maintain at scale. | Use only if you have a dedicated artist. |

**Rule:** declare your project's primary style here in one sentence and an example URL or path.

## Aspect ratios

Use standard ratios. Variables let consumers swap implementations.

| Variable | Ratio | Use for |
|----------|-------|---------|
| `$ratioHero` | 16:9 | Marketing hero, video thumbnails, blog featured images. |
| `$ratioWide` | 21:9 | Cinematic / immersive marketing moments. |
| `$ratioPortrait` | 4:5 | Social-card images, in-feed photo posts. |
| `$ratioSquare` | 1:1 | Avatars, team-grid tiles, gallery default. |
| `$ratioCard` | 3:2 | Card thumbnails, product listings. |

**Rule:** never crop a photo to a non-standard ratio (e.g. 1.37:1 because that's what made the layout balance). Choose a ratio first, then make the layout balance.

## Treatment

A unified treatment is what separates "a brand" from "a Pinterest board."

- **Corner radius:** `$radiusLg` (12px) by default for in-product imagery; full-bleed for marketing hero.
- **Color overlay:** if you tint images for contrast (text-on-image), use `$surface` (light: white at 40%, dark: black at 50%) as the overlay. Don't use a brand-color overlay — it makes every image look like it's the same image.
- **Drop shadow on images:** by default, **none.** Float images on the page; let surrounding layout carry depth.
- **Borders:** none on photography (corner radius does the framing). 1px `$border` on illustration when it sits directly on a card.
- **Filters / saturation shifts:** none. Apply at the source if needed; don't filter in CSS.

## Accessibility & alt text

- Every meaningful image gets descriptive alt text. *"Two engineers reviewing code at a whiteboard"* > *"team"* > *"image"*.
- **Decorative-only images** (texture under a hero) get `alt=""` (empty), not omitted.
- Alt text describes the image, not its function — the function is the surrounding text. *"A chart showing weekly active users rising 15%"* belongs in a `<figcaption>` or the body, not in `alt`.

## AI-generated imagery

Where AI-generated art is OK in this project:

- ✅ **Empty-state illustrations and icon decorations.** Tight scope, low brand stakes, easy to swap if better art appears later.
- ✅ **Filler / texture / abstract backgrounds** behind brand-led typographic moments.
- ✅ **In-product placeholders** while real assets are being commissioned.

Where it's not:

- ❌ **Hero shots on marketing pages.** They tend to read as generic; the brand needs to feel real.
- ❌ **Photos of people**, especially testimonials, "team" pages, and "real customer" imagery — these read as fraudulent and the cost when discovered is higher than the cost of a stock photo.
- ❌ **Images that imply specific facts** (a screenshot of "your dashboard" — make a real one; a fake city skyline labeled with a city name — find or skip).

In Pencil, prefer `G(node, "ai", "<prompt>")` for AI-generated art and `G(node, "unsplash", "<query>")` for stock photography. Stock photography is rarely the right answer either; better to use real product imagery whenever possible.

## Avatars

- Default size: 32 × 32 in lists, 40 × 40 in headers, 64 × 64 in profile views.
- **Fallback when there's no image:** colored circle with initials. Pick the background color from the user's id hash, not random per-render. Initials on top in `$onPrimary` color (or whatever contrasts).
- Always circular for personal avatars; square (with `$radiusSm` rounding) for organization / brand avatars. The shape language helps users distinguish "person" from "team."
- Don't use `John Doe` placeholder names + a generic silhouette in shipped designs. Use a list of plausible names and varied initials when illustrating.

## Hero imagery

For a marketing hero:

- The image carries roughly 50% of the visual weight; the headline and CTA carry the other 50%. If the image dominates and the text recedes, conversion drops; if the image is incidental, the hero feels empty.
- Prefer **a product shot** over a stock photograph, every time.
- If using illustration: scale it generously. A small illustration in the corner of a hero reads like clip art.
- Don't put text *over* a busy photograph. Either use a layout where text lives in a clear column, or apply a `$surface` overlay (per Treatment above).

## Social / OG imagery

Per-page open-graph imagery extends the brand template in `brand.md`. For pages without a custom OG image (most blog posts, deep app pages), generate one programmatically: brand surface, page title in display type, optional accent shape — not the page's screenshot.

## Where images live in code

- **Public marketing imagery:** `<public/images/>` or your CDN. Use Next.js `<Image>` (or framework equivalent) for responsive sizing.
- **In-product illustrations:** SVG inline via component, or imported from `<src/illustrations/>`.
- **Avatars:** served from your auth provider, with the colored-circle fallback above.

(Mirror this from `code-export.md` if you want one canonical answer.)
