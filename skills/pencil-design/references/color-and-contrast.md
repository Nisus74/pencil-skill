# Colour and contrast

This reference is the depth behind the colour guidance in SKILL.md's Aesthetic foundation: the "never raw `#000` or `#FFF`" rule, the "one accent, low saturation" default, and the "every colour through a variable" discipline. It covers OKLCH theory, the four palette strategies, semantic role construction, light + dark mode parity, and the reflex-reject palette defaults to refuse.

For accessibility-specific contrast verification (WCAG AA, AAA, the colour-is-never-the-only-signal rule), see [accessibility.md](accessibility.md).

## Why OKLCH (and not HSL or HEX-by-eye)

HSL is broken for design work. The same saturation value reads as wildly different across hues; the same lightness value reads as different perceived brightness across hues. *"50% lightness yellow"* and *"50% lightness blue"* look nothing alike to the human eye. Designing in HSL means hand-correcting every value for what it should be perceptually.

OKLCH (lightness, chroma, hue) is perceptually uniform. The lightness axis matches human perception of brightness across all hues. The chroma axis is consistent across hues at the same intensity. The hue axis behaves predictably. Pick a lightness curve and apply it across hues; the result looks coherent without per-colour tuning.

HEX is fine as the wire format (most exports still target hex) but should never be the *thinking* format. Define palettes in OKLCH, convert at the variable boundary.

A few key OKLCH properties to internalise:

- **Lightness scale: 0 (black) to 1 (white).** A neutral at L=0.3 reads as the same darkness as a saturated accent at L=0.3.
- **Chroma: 0 (perfectly neutral) to roughly 0.4 (the most saturated possible at that hue and lightness).** Most UI work lives at chroma 0.05 to 0.2.
- **Hue: 0 to 360 degrees.** Red around 30, orange around 60, yellow around 90, green around 145, cyan around 180, blue around 230, purple around 290, pink around 350.
- **Chroma collapses near lightness extremes.** As L approaches 0 or 1, the maximum possible chroma drops sharply. Saturated near-blacks and near-whites don't exist; high chroma at extremes looks garish.

The practical rule: reduce chroma as lightness approaches 0 or 1. A near-black accent at chroma 0.15 looks muddy; the same hue at chroma 0.05 looks intentional.

## The four palette strategies

Pick one commitment level per design before picking specific colours. Cycling between strategies mid-design reads as scattered. This catalogue duplicates the per-register guidance in [brand.md](brand.md) and [product.md](product.md); use this reference for the methodology, those references for register-specific picks.

### Restrained
Tinted neutrals plus one accent used at ≤10% of the surface area. The identity carries through type, layout, and rhythm rather than colour. Product default; brand default for minimalist or editorial work.

### Committed
One saturated colour carries 30–60% of the surface. The colour IS the brand for the duration of the page. Brand default for identity-driven pages; rare in product.

**The 60% rule.** When committing to a dominant colour, the visible-surface share matters as much as the choice. 30% reads as accent-shy (the surface still wants to be neutral). 80% reads as suffocating (the eye has nowhere to rest). 60% lands in the middle: dominant enough to read as committed, restrained enough to keep the secondary content legible. The other 40% is neutrals plus one supporting role.

Restrained committal (40%) suits product surfaces that need a strong brand presence without losing function. Maximal committal (70–80%) suits brand heroes and campaign launch pages where atmosphere wins over content density.

### Full palette
3–4 named roles, each used deliberately. Each role gets its own surface treatment. Brand campaigns; product data visualisation (categorical encoding).

### Drenched
The surface IS the colour. No off-canvas, no neutral relief. Brand heroes, campaign launch pages, manifesto pages.

Default to restrained for product work; brand work selects intentionally per page. The "one accent ≤10%" rule from SKILL.md is restrained only; the other three exceed it on purpose.

## Tinted neutrals

The single biggest improvement to most palettes: tint every neutral toward the brand hue.

Pure `#000000` and `#FFFFFF` (banned in SKILL.md) read as soulless because they belong to no system. A neutral at chroma 0 in an otherwise warm-hue brand reads as cold; the same neutral tinted slightly toward the warm brand hue reads as part of the system.

The tint amount is small. Chroma 0.005 to 0.01 is the sweet spot. Higher and the neutrals stop reading as neutrals; lower and the effect is invisible.

A worked example for a brand whose accent is OKLCH(0.6 0.2 145) (a saturated green):

| Role | OKLCH | Approx HEX |
|---|---|---|
| `bg` (page background, light mode) | `oklch(0.985 0.005 145)` | `#FAFAF8` |
| `bgSurface` (raised surface, light) | `oklch(0.97 0.007 145)` | `#F4F5F2` |
| `border` (low-contrast separator, light) | `oklch(0.92 0.01 145)` | `#E5E7E1` |
| `text` (body, light mode) | `oklch(0.22 0.005 145)` | `#262825` |
| `textMuted` (body secondary, light) | `oklch(0.5 0.008 145)` | `#74766F` |
| `accent` (CTA, links, emphasis) | `oklch(0.6 0.2 145)` | `#3E9D55` |

Every neutral leans toward the brand's green hue at a chroma the eye can't quite read as colour. The result is coherence; the same neutrals against a different brand hue would feel slightly off.

Pick warm or cool tinting per brand; never mix the two in the same design. Mixing warm-grey backgrounds with cool-grey surfaces is the most common subtle palette mistake.

### Never gray on colour
A pure grey text run on a coloured background reads as accidental. The grey belongs to no system; the colour belongs to the brand. Two systems on the same element.

The fix has two shapes:

- **Use a darker or lighter shade of the colour itself.** Text on a green panel resolves to a near-black version of that green (OKLCH lightness around 0.2, chroma slightly reduced); text on a deep blue panel resolves to an off-white tinted toward the same blue. The text and surface are then the same system.
- **Use the original text colour at reduced opacity.** The text inherits the surface's hue through the transparency. Works best for muted secondary text on coloured surfaces.

Either approach reads as system. Gray-on-colour reads as the design system not having been finished.

## Semantic role catalogue

A complete product or brand palette typically defines these roles. Not every design needs all of them; the smaller the palette, the more disciplined the system.

### Surface roles
- **`bg`**: the page background. The lowest-elevation surface.
- **`bgSurface`**: raised content (cards, panels). Slightly different L than `bg`.
- **`bgSurfaceElevated`**: popovers, dropdowns, modals. Higher than `bgSurface`.
- **`bgInverse`**: the inverse surface for emphasis (a dark band in a light design or vice versa).

### Text roles
- **`text`**: primary body text. ≥4.5:1 against the surface it sits on.
- **`textMuted`**: secondary text, captions, metadata. ≥3:1 against the surface.
- **`textOnInverse`**: text on `bgInverse`.
- **`textOnAccent`**: text on the accent colour (often white or off-white).

### Border roles
- **`border`**: low-contrast separators (rows, dividers, card edges). Often L+0.05 above the surface it sits on.
- **`borderEmphasis`**: focused inputs, selected states.

### Accent roles
- **`accent`**: the brand accent. Used on primary CTAs and emphatic moments only.
- **`accentMuted`**: tinted backgrounds derived from the accent (selected row tints, accent-tinted callout backgrounds).
- **`accentEmphasis`**: a darker / more saturated variant for hover or pressed states.

### Semantic roles (product especially)
- **`error`**: destructive actions, validation failures. Red-adjacent.
- **`success`**: completion of significant actions. Green-adjacent.
- **`warning`**: non-blocking attention. Amber-adjacent.
- **`info`**: neutral notifications. Blue-adjacent (distinct from any brand blue).

These four shouldn't double as the brand accent or each other. Reserving them for semantic meaning keeps the signal strong.

### Construction discipline
- Don't define a role you won't use. A palette with `bg`, `text`, `border`, `accent` is fine for a simple product surface.
- Resist defining shade ramps with 50/100/200/.../900 unless you actually need them. Most designs use 3–5 neutrals; a 9-step ramp is overkill that introduces drift.
- Name roles semantically (`bgSurface`), not by colour (`zinc100`). Semantic names survive a palette swap; colour names don't.

## Light + dark mode

Every colour variable in a `.pen` document carries both light and dark values from the first variable declaration (SKILL.md discipline rule). The two modes aren't inverted; they're designed in parallel.

### What changes between modes

- **Lightness flips.** A `bg` at L=0.985 in light mode goes to L=0.15 in dark mode.
- **Chroma changes.** Tinted neutrals on dark backgrounds want slightly higher chroma (0.01 to 0.02) to remain perceptibly tinted; light-mode neutrals at 0.005 chroma read flat in dark mode.
- **The accent often shifts.** A bright accent that reads well on light surfaces may need to lighten slightly in dark mode to maintain contrast.
- **Borders darken less than backgrounds.** A border that's L+0.05 above the surface in light mode wants L+0.08 in dark mode because the eye's contrast sensitivity is non-linear in shadow.

### What stays the same

- **Hue.** The brand hue stays constant across modes.
- **Role semantics.** `text` is text in both modes; `error` is error in both modes.
- **Contrast targets.** WCAG AA targets apply in both modes equally.

### Common dark-mode failures
- **Dark mode is just light mode inverted.** A near-black body text on a near-white background works; pure white body text on pure black is harsh. Use off-white (`oklch(0.95 0.005 hue)`) text on near-black surfaces.
- **Saturated accents stay too saturated.** A vibrant accent on dark backgrounds tends to glow. Reduce chroma slightly (10–20%) or shift lightness up.
- **No line-height bump.** Light text on dark backgrounds visually compresses. Add 0.05 to body line-height in dark mode (covered in [typography.md](typography.md)).
- **Borders disappear.** Light-mode borders at L=0.92 against L=0.985 surface read fine; the same delta in dark mode against an L=0.15 surface is invisible. Widen the delta in dark mode.

### Gentler contrasts where it doesn't matter
High contrast everywhere produces visual noise. Every element fighting for the same attention level reads as the surface having no opinion about which element is primary.

Reserve high contrast for the focal points (primary CTA, primary heading, the one number the user is here to read). Let secondary elements use gentler contrast (3:1 to 4:1) so they read as supporting rather than competing.

- **Body text:** ≥4.5:1 against its surface (WCAG AA floor).
- **Secondary text and labels:** 3:1 to 4.5:1 is fine; below 3:1 starts failing accessibility.
- **Borders and dividers:** 1.5:1 to 3:1 against the surface; high-contrast borders are loud.
- **Decorative icons:** 2:1 to 3:1 is often enough; high-contrast decoration competes with the content it supports.
- **Disabled state:** 2:1 contrast against the surface; disabled text should read as quietly-not-available, not as missing.

The squint test ([layout.md](layout.md)) reveals whether contrast is doing hierarchy work or competing. If everything reads as the same priority when squinting, the contrast is over-applied.

Test under both modes before declaring the design done. The first-screenshot protocol in SKILL.md applies under both modes individually.

## Reflex-reject palette defaults

These colour combinations are over-represented in current AI training data by category. They read as the category default the moment they appear. Refuse them as defaults; use them only when the brand specifically wants the category-default look.

| Category | Reflex palette | Why it reads AI |
|---|---|---|
| AI products | Off-white background, warm grey text, violet or orange accent | The OpenAI/Anthropic/Cursor cluster |
| Observability / monitoring | Dark blue background, cyan or green accents | Datadog / Grafana visual reflex |
| Fintech | Navy and gold, or navy and electric blue | Stripe-era saturated reflex |
| Healthcare | White background, teal accent, soft pastel illustrations | A decade of healthcare-startup default |
| Crypto / Web3 | Neon (often green, magenta, or cyan) on black or near-black | Web3-era saturated reflex; reads dated |
| Developer tools | Pure black or near-black, monospace, single accent (often green) | Linear-era reflex; saturated by 2025 |
| Education | Saturated yellow or orange, rounded shapes, illustration | Duolingo cluster |
| B2B SaaS | Violet-to-indigo gradient, white cards, soft shadows | The 2020–2024 SaaS default |
| Wellness / mindfulness | Soft warm earth tones, sage green, off-white | The wellness-brand default 2021–2024 |
| Travel / hospitality | Saturated warm orange, white, photo-heavy | Airbnb cluster |

If the brand's direction explicitly names one of these, follow it. The rule is "don't reach for these by category reflex", not "refuse them on demand".

## Contrast verification

Run these checks before declaring the design done. The full accessibility protocol lives in [accessibility.md](accessibility.md); the colour-specific checks are:

1. **Body text contrast.** ≥4.5:1 against its surface (WCAG AA). Check under both light and dark modes; a token that passes in one mode often fails in the other.
2. **Large text contrast.** ≥3:1 for text ≥24px (or ≥18.5px bold).
3. **UI component contrast.** ≥3:1 for borders, icons, and other non-text interactive elements against adjacent colours.
4. **Accent on surface.** ≥3:1 for the accent against the surface it sits on (so CTAs remain perceivable).
5. **Text on accent.** ≥4.5:1 for text on accent-coloured backgrounds (so CTA labels stay readable).

If a check fails, fix it before reporting done. Don't note it as a TODO.

## Pencil-specific

### Declaring colour variables
Call `SetVariables` inside `batch_design` to declare the colour palette upfront, before placing any frames. Every colour resolves to a token from then on:

```
SetVariables({
  "bg": { mode: { light: "#FAFAF8", dark: "#1A1B19" } },
  "bgSurface": { mode: { light: "#F4F5F2", dark: "#252622" } },
  "border": { mode: { light: "#E5E7E1", dark: "#3A3B36" } },
  "text": { mode: { light: "#262825", dark: "#F0F1ED" } },
  "textMuted": { mode: { light: "#74766F", dark: "#A3A59E" } },
  "accent": { mode: { light: "#3E9D55", dark: "#5BBA72" } }
})
```

Note the accent shifts slightly in dark mode (lighter, slightly less saturated) per the dark-mode rules above.

### The theme axis
For documents with light + dark variants, declare the `mode` theme axis on the document root before placing frames:

```
Update(docRootId, { themes: { mode: ["light", "dark"] } })
```

Then individual frames can render in a specific mode via:

```
Update("<pageFrameId>", { theme: { mode: "dark" } })
```

This lets you screenshot the same design under both modes from the same `.pen` file.

### Audit existing files
For files that pre-date the discipline rules, read the subtree with `batch_get` and tally the `fill` values yourself to find raw hex still in use. Any hex string (not starting with `$`) is a bug. To bulk-fix where the same hex maps to a known variable, read the target nodes with `batch_get`, then loop `Update` inside a `batch_design` snippet:

```
for (id of ["a", "b"]) Update(id, { fill: "$accent" })
```

### Verifying contrast under both modes
After laying out a surface, screenshot it twice: once with `theme.mode: "light"`, once with `theme.mode: "dark"`. Run the WCAG AA contrast check on both. Tokens often pass one and fail the other; both must pass before the design is done.
