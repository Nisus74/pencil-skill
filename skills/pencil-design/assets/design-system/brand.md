# Brand

How the brand identity shows up in product. **Delete this file if your project doesn't have a marketing surface or distinct brand mark**, most internal SaaS products don't need it.

The agent reads this when placing a logo, choosing brand colours for a marketing surface, or applying brand voice to a hero. Without rules here, AI defaults to placing the wordmark wherever and stretching marks to fit, both quietly wrong.

## Logo variants

Declare the variants you have. At minimum, most projects ship 3:

| Variant | Asset path | Use for |
|---------|-----------|---------|
| **Full lockup** (mark + wordmark) | `<assets/logo-full.svg>` | Marketing site header, sign-in screen, footer, social-share images. |
| **Mark only** | `<assets/logo-mark.svg>` | App favicons, tight contexts (top of mobile screen, sidebar collapsed state), social avatars. |
| **Wordmark only** | `<assets/logo-wordmark.svg>` | Where the mark would feel redundant (already in chrome) but a brand line still needs to read. |
| **Monochrome variant** | `<assets/logo-mono.svg>` | Newsprint, single-colour reproduction, photo overlays where the brand colour clashes. |
| **Inverse / on-dark** | `<assets/logo-inverse.svg>` | Dark backgrounds where the standard logo's contrast fails. |

If your asset is a single SVG that responds to `currentColor`, you may not need separate inverse/mono files, but document it explicitly so consumers don't recolor by hand.

## Sizing

Logos have a **minimum size** below which they stop reading.

- **Mark:** minimum 16 × 16 (favicon-edge case). Default in app chrome: 24–32.
- **Full lockup:** minimum 80px wide; readable down to ~64px on retina, but only if the wordmark is still legible.
- **Hero / display:** declare a maximum too, a 600px logo on a marketing hero usually reads as overcompensating; 200–320px is typically right.

## Clear space

Reserve clear space around the logo equal to the height of the mark (or the cap-height of the wordmark, whichever is smaller).

```
┌──────────────────────────────────┐
│  ↑                                │
│  c                                │
│  ↓                                │
│ c [LOGO] c                       │
│  ↑                                │
│  c                                │
│  ↓                                │
└──────────────────────────────────┘
```

**Rule:** no other UI element (text, icon, button) intrudes into clear space. This includes nav items in a header, give the logo its own column, with `c` of breathing room.

## Colour

- **Primary brand colour:** `$primary` (defined in `tokens.md`). The logo renders in this colour by default.
- **On dark surfaces:** use the inverse variant.
- **On photographs / video:** use the monochrome variant (white or black) chosen for contrast against the local background, not the brand hue. A blue logo over a busy photo is unreadable.
- **Never** recolor the logo to match a section's accent colour. The logo is constant.

## Don't-do list

- Don't stretch the logo (lock aspect ratio).
- Don't apply effects: no drop shadow, no glow, no gradient overlays, no embossing, no rotating outside the official lockups.
- Don't recolor outside the declared variants.
- Don't crop. The mark is whole.
- Don't pair the logo with another brand's logo in a "lockup" without an established visual partnership pattern.
- Don't animate the logo on every page load. A single hero-moment animation may be acceptable; a logo that wiggles or pulses every navigation is hostile.

## Tagline / wordmark placement

If the brand has a tagline:

- Pair it with the lockup only in dedicated brand moments (footer, marketing hero, app splash), not in nav chrome.
- Tagline typography: `$fontHeading` if it's display-weight, `$fontBody` if it sits in flowing context.
- Keep it shorter than the mark width when stacked beneath.

## OG / social-share imagery

Default OG image (1200 × 630):

- Dark surface (`$surface` dark), centred logo (full lockup, white variant), tagline below.
- Optional: one accent shape or gradient sweep, not multiple.
- Reserve a top-right space (~200 × 100) for context-specific overlay text (page title, blog title) when generating per-page OG images.

Per-page OG images derive from this template; don't redesign per page.

## Favicons

- Use the **mark only**, not the full lockup. The full lockup is illegible at 16 × 16.
- Provide multiple sizes: `16, 32, 48, 180 (apple-touch), 192, 512`.
- Apple touch icon (180 × 180) sits on a coloured background, give it `$primary` (or a brand surface colour) as the background, not transparency, since iOS doesn't render a transparent favicon well on the home screen.

## Brand voice and product voice

`voice.md` covers product copy. The brand voice may differ on marketing surfaces, usually slightly more aspirational. If both apply in your project, name where each lives:

- **Brand / marketing voice:** marketing site (`/`, `/pricing`, `/about`), social posts, sign-up emails.
- **Product voice:** everything inside the authenticated app, including notifications, error messages, settings copy.

Don't let either bleed into the other. Marketing copy inside the app reads as advertising; product copy on marketing reads as cold.

## Archetype variants

How brand shows up changes meaningfully under different archetypes:

- **`marketing-websites/conversion-focused-saas`** (Linear-style): logo full lockup top-left of nav, scaled small (~24px tall). Brand accent appears in primary CTA, link colours, badge fills. Dark mode is the canonical marketing surface so the inverse-on-dark logo variant gets used most. Consider a second support hue for badges and category labels (Linear pairs cyan + purple).
- **`marketing-websites/editorial-storytelling`**: logo gets less screen real estate; the type and content carry the brand. Mark may appear small at the top-left and again subtly in the footer; the page itself is the brand expression.
- **`saas-apps/b2b/modern-pro-tool`**: brand mark in the sidebar workspace switcher (24–32px), often paired with a workspace name. App is light by default; brand colour appears in primary CTA + active sidebar item only.
- **`saas-apps/b2b/analytics-dashboard`**: brand mark identical to modern-pro-tool placement; brand colour appears even more sparingly (delta arrows, primary CTA, link affordance).

**What generic looks like (don't ship this):** logo with a violet-to-blue gradient, animated wiggle on page load, sized at 80px+ in the nav competing with the headline, recoloured to match the active section, used as a decorative background pattern.
