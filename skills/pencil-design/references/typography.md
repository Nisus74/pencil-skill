# Typography

Typography is the fastest move out of AI-default territory. Colour, layout, and motion can all reach for safe defaults that look competent and read as machine-generated. A deliberate typographic choice signals intent more loudly than any other axis. Get this one right and most of the design follows.

This reference is the depth behind SKILL.md's typography defaults (the negative-space rules in the Aesthetic foundation and the "Inter as UI font" anti-pattern). It covers font selection, pairing, scale, readability, numerals, and special moves. For register-specific pairings, see [brand.md](brand.md) and [product.md](product.md).

## Why typography signals intent

A page can use a great colour palette, a sensible grid, and respectful spacing, and still read as generated because the type pairing is the category default. A page can use a stricter colour palette, a denser grid, and tighter spacing, and read as deliberately designed because the typeface choice carries an opinion.

The opinion comes through in two moves:

1. **Selecting fonts that aren't the category reflex.** Inter is fine; it's also the default UI font in nearly every AI-tool launch from 2023 onward. Picking Söhne, Geist, or SF Pro for the same role costs nothing and instantly differentiates.
2. **Using OpenType features that proportional typefaces support but most designs don't activate.** Small caps, stylistic sets, tabular figures, contextual alternates. The font's already capable; the design declines to use it by reflex.

Typography is where 30 minutes of consideration outperforms 30 hours of decoration.

## Reflex-reject font list

These fonts (or font pairings) are over-represented in current AI training data and design output. Refuse them as defaults; require explicit reason to use them.

### Display fonts to avoid by default
- **Inter as headline display.** Inter is a UI font; using it for hero type is the strongest AI tell.
- **Generic serifs as display** (Garamond, Times, Georgia, default web serifs). These read as *"I didn't pick a font."* If a serif fits the brand, pick a deliberate one (see below).
- **Default Fraunces / Fraunces Soft** as a hero serif. Fraunces is a strong font; it's also the AI-tool reflex serif of 2024–2025.
- **Default Playfair Display.** The 2018-era SaaS serif. Reads dated.

### Body fonts to avoid by default
- **Inter.** As above; safe and saturated. Pick another grotesque before falling back to Inter.
- **System sans (-apple-system, etc.) without a fallback strategy.** Reads as "I didn't pick a body font."
- **Default Roboto.** Material-design reflex; ages poorly outside Android UIs.

### Pairings to avoid by default
- **Cabinet Grotesk + Fraunces.** The AI-tool launch reflex pair. Both fonts are good individually; the *pair* is what reads generated.
- **Fraunces + Inter.** A common variation on the above.
- **Helvetica or Helvetica Neue + Inter.** Two grotesques fighting; neither wins.

### Fonts worth reaching for instead

| Need | Reach for |
|---|---|
| Modern grotesque body | Söhne, Geist, SF Pro, GT America, PP Neue Montreal, Suisse Int'l |
| Editorial serif | Tiempos, Instrument Serif, Editorial New, GT Sectra, Sentinel |
| Expressive display | Clash Display, GT Super, Editorial New, ABC Diatype, Migra |
| Warm display | Recoleta, Bagoss Standard, Söhne Breit |
| Mono / data | JetBrains Mono, Berkeley Mono, IBM Plex Mono, Geist Mono, GT America Mono |
| Brutalist | GT America Mono, Pangaia Grotesk, Standard Book |
| Quiet utility sans | Söhne, Inter (genuinely sometimes the right choice), SF Pro Text |

These aren't a recommended-fonts shortlist; they're alternatives the model under-reaches for. The right font for any design comes from the brand's direction, not from a list.

## Pairing rules

A type system is two to three fonts maximum: a display, a body, and optionally a mono. Most strong type systems are two fonts; many great ones are one.

### Two-font pairing combinations that work

- **Display sans + body sans** (one family).  Söhne everywhere, hierarchy through weight. Calm, modern, restrained.
- **Display sans + body serif.** Söhne display, Tiempos body. Tech-meets-editorial; works for brand-product hybrids.
- **Display serif + body sans.** Editorial New display, Söhne body. The most common editorial pairing; goes generic if both fonts are over-saturated.
- **Display serif + body serif** (one family). Tiempos for everything. Magazine-like; reads confident on long-form.
- **Mono everywhere.** JetBrains Mono for both display and body. Rare and committed; suits developer tools and brutalist brand work.

### Rules for pairings

1. **Contrast the personalities.** A neutral display with a quiet body (Söhne + Söhne) is fine but reads safe. A confident display with a quiet body (Clash + Söhne) reads as deliberate. Two confident fonts compete.
2. **Stay within two visual genres maximum.** Display serif + display sans + body sans = three voices arguing.
3. **Mono is a third font, not a free addition.** Adding a mono just to render code blocks counts as a system decision; pick one that lives well with the body.
4. **One font is often the answer.** Pages built in a single typeface with hierarchy through weight contrast and size feel more cohesive than two-font systems for product work especially.

### Avoid

- Pairing two grotesques (they fight)
- Pairing two serifs from different visual eras (Tiempos + Garamond)
- Using script or hand-drawn fonts as either display or body (a 2010s wedding-invitation reflex)
- Stacking three weights in headlines (e.g. *Bold quick* **Black brown** *Light fox*) for "expressive" effect; reads as designed-with-no-discipline

### Condensed and extended widths
Modern variable fonts often ship multiple widths along the same family. Söhne ships Breit (extended) and Schmal (condensed); GT America ships Condensed and Extended; Geist's width axis runs from Compressed to Expanded. The width axis is the most under-used differentiation move in current AI design output.

A condensed display next to a regular-width body reads as designed; the eye picks up the width contrast without having to ask why. The reverse (extended display, regular body) reads as confident on brand pages with plenty of horizontal space.

Discipline:

- **One width contrast per surface, not three.** If the display is condensed, the body stays regular. Mixing condensed display with extended body with regular kicker reads as the family being misused.
- **Stay inside the family.** Mixing Söhne Schmal with a different family's condensed produces two fonts arguing; stay in the Söhne family or in another single family.
- **Tune the tracking.** Condensed widths need slightly more positive tracking than regular widths at the same size; extended widths often want slightly negative tracking to keep the letterforms from drifting apart.

## Scale and hierarchy

### Modular scale
Pick a ratio and stick to it. 1.25 (major third) is the safest default; 1.2 (minor third) is tighter and works for product UIs; 1.333 (perfect fourth) is more expressive and suits brand.

A 1.25 scale starting at 16px body: 12.8, 16, 20, 25, 31, 39, 49, 61, 76, 95. Round these to readable values (12, 16, 20, 24, 32, 40, 48, 64, 80, 96).

### Weight contrast over size contrast
A common AI default: inflate the heading sizes to create hierarchy. *"Make the headline bigger."* The result is a giant headline above tiny body, no middle ground.

Better: contrast weight first, size second. A 24px semibold heading above 16px regular body reads as more hierarchy than a 36px regular heading above 16px regular body. Reserve size jumps for top-level hierarchy (page title, hero), use weight contrast for everything below.

### Extreme weight pairing
Most type systems sit in the middle of the weight axis. Body at 400, headings at 600, occasional emphasis at 700. That range produces competent designs and rarely produces memorable ones.

When the brand or the surface earns it, pair extremes. A 900 display weight next to a 200 (or 300) body reads as committed; a 600 display next to 400 body reads as default. The visible difference is large; the reader notices the type system is doing work.

Modern variable fonts (Geist, Inter, Söhne, GT America) ship the full weight axis. Activating it costs nothing on the design side; the only constraint is what the production font subset includes for runtime weight delivery. Document the weights actually used per family in `context` so engineering knows what to load.

When extreme weight is right:
- Brand heroes with a single committed message; the 900 headline carries the page.
- Marketing pages where the visual contrast IS part of the argument.
- Editorial layouts where the display sets a strong typographic voice.

When extreme weight is wrong:
- Dense product UIs where 900 headings shout at every section.
- Surfaces with many similar headings; extreme weight needs quiet around it.
- Brands whose voice is restrained or scholarly; extreme weight reads as too loud.

### Avoid flat scales
Three consecutive type sizes within 2px of each other (14, 16, 18) read as no scale at all. Pick a ratio and skip steps. The 16/20/24 + bold trio of headlines reads flatter than 16/24/40 with weight contrast.

### Tracking discipline
- **Body text:** 0 letter-spacing in most fonts. Some fonts (Söhne, GT America) benefit from -0.005 to -0.01 at body sizes for visual evenness.
- **Display sizes ≥ 48px:** slightly negative tracking (-0.01 to -0.02) tightens the spaced-out feel of large type.
- **All-caps below 14px:** positive tracking (0.04 to 0.08) to keep legibility.
- **Small caps:** positive tracking (0.02 to 0.05) for the same reason.

## Readability

### Measure (line length)
Body copy reads best at 60–75 characters per line. Pencil's SKILL.md uses 65ch as the safe ceiling on long-form prose. Use `width: "fill_container(max-65ch)"` patterns where possible.

Long-form text (blog posts, documentation, manifesto pages) sits at 60–70ch.
Short-form UI text (cards, list items, modals) can go wider, up to 90ch, because the chunks are small.
Very wide lines (>90ch) lose the eye between the end of one line and the start of the next.

### Line height
Body type: 1.5 to 1.625 (24px line height at 16px body).
Display type: 1.0 to 1.15 (tighter for impact).
Long-form prose: 1.625 to 1.75 (more breathing room over many lines).

### Light-on-dark line-height bump
White or light text on a dark background visually compresses. Add 0.05 to the line height of body text on dark backgrounds compared with the same font on a light background. A body that reads at 1.5 line height in light mode wants 1.55 in dark mode.

### Optical alignment
First-letter indent on body text reads as old-fashioned for UI; reserve for genuine long-form prose. Hanging punctuation (quote marks pulled into the margin) is a deliberate move worth using on pull-quotes and editorial layouts.

## Numerals

Numbers stack in product UIs constantly. The default proportional numerals look ragged when stacked vertically:

```
Proportional:    Tabular:
  1,234            1,234
    567              567
12,345           12,345
   89               89
```

Most modern fonts support both via OpenType. Activate tabular figures explicitly on:

- Tables (every column)
- KPI cards (the big number)
- Transaction lists, ledger entries, financial figures
- Sparklines and chart axis labels
- Any vertically-stacked numeric column

For dedicated data surfaces (trading interfaces, log viewers, observability dashboards), reach for a true monospace at least for the numeric content.

For prose contexts (a single number in a sentence), proportional figures read better.

## Special moves

These OpenType features and typographic moves are under-used in machine-generated design. Each is a low-cost differentiation move.

### Small caps
Use for: metadata labels (*"STATUS"*, *"OWNER"*, *"LAST RUN"*), section kickers above headlines, navigation in restrained brand designs.
Quieter than all-caps, more deliberate than sentence-case. Most modern fonts include true small caps; if the font doesn't, faux small caps (CSS `font-variant: small-caps`) read as inferior.

### All-caps with tracking
Use for: labels in dense product UIs, button text in some brand contexts, ribbon copy.
Below 14px, add 4–6% letter-spacing to maintain legibility. All-caps body text above one short phrase reads as shouting; restrict to short strings.

### Italic restraint
Italics for emphasis in long-form prose read fine. Italics on short UI labels, in card titles, on buttons, in form labels read as accidental. The rule: italic for *emphasis within prose*, never for design decoration.

### Stylistic sets and contextual alternates
Modern fonts often ship multiple stylistic sets: alternate `a` glyphs, single-storey vs double-storey `g`, geometric vs humanist character variants. The Geist `ss01` or Söhne `ss02` can give the same font a different personality.

Check what the brand's chosen font supports and pick one stylistic set explicitly. Activating a single alternate set across a design adds visible character at near-zero cost.

### True small caps and old-style figures together
Editorial layouts (long-form blog, manifesto pages, magazine-style) benefit from combining old-style (text) figures with small caps. Both move the design out of UI-default territory into editorial territory. Avoid mixing in the same surface as tabular figures.

### Monospace as intentional accent
Monospace as a default body font is the developer-tool reflex. Monospace as a deliberate accent (a data column, a code reference, a kicker label, a metadata strip) signals intent; the reader picks up *"this is a different kind of content"* from the type alone.

When mono earns its place:

- **Numeric columns** in tables and dashboards; mono guarantees the alignment that tabular figures get partway to. JetBrains Mono, Berkeley Mono, Geist Mono are the reach-for picks.
- **Code references** inline in prose; a single mono span in a sentence about the API reads as the API, not as decoration.
- **Kicker labels** above editorial headlines; a small mono kicker before a serif display headline reads as a deliberate type system.
- **Metadata strips** in product UIs; *"ID 4521  •  Created 2026-05-16"* in mono reads as system-generated and stays out of the way.

Pair mono with a grotesque body or a serif body, not with another mono. Two monos on the same surface produces *"is this a terminal?"* unless the brand is explicitly developer-tooling.

## Per-register guidance

- **Brand.** Larger scale (96–160px hero type is fine), more dramatic weight contrast, room for expressive display fonts. See [brand.md](brand.md) for pairings by direction.
- **Product.** Tighter scale (24–28px max for most headings), mono numerals on data, small caps on metadata labels, conservative tracking. See [product.md](product.md) for data-typography guidance.

## Pencil-specific

### Setting fonts in `.pen`
Type nodes use `fontFamily`, `fontWeight`, `fontSize`, `lineHeight`, `letterSpacing`, and `textAlign` properties. Example:

```
T1 = Insert("parent", {
  type: "text",
  content: "Pricing",
  fontFamily: "Söhne",
  fontWeight: 600,
  fontSize: 24,
  lineHeight: 1.15,
  letterSpacing: -0.01,
  fill: "$text"
})
```

Text without a `fill` renders invisible. Always set the fill, ideally to a `$variable` so dark mode flips automatically.

### Type tokens via `SetVariables`
Declare type tokens once (call `SetVariables` inside `batch_design`) and reference them everywhere so font changes apply globally:

```
SetVariables({
  "fontDisplay": { mode: { light: "Söhne", dark: "Söhne" } },
  "fontBody": { mode: { light: "Söhne", dark: "Söhne" } },
  "fontMono": { mode: { light: "Berkeley Mono", dark: "Berkeley Mono" } }
})
```

Then text nodes bind to `fontFamily: "$fontDisplay"` instead of literal font names. Switching the brand from Söhne to Geist becomes a single variable update.

### OpenType features
Pencil exposes OpenType features via `fontFeatureSettings` or analogous properties. For tabular figures on a column of numbers:

```
Update("<numberColumn>", { fontFeatureSettings: "tnum" })
```

For stylistic sets:

```
Update("<displayHeading>", { fontFeatureSettings: "ss01" })
```

Check the schema reference (`references/pen-schema.md`) for the current property name if `fontFeatureSettings` doesn't resolve.

### Verification
After laying out type, check:
- Body line length under 75ch
- Heading sizes step on a chosen ratio (no consecutive steps within 2px)
- Tabular figures activated on every numeric column
- Light-on-dark text has the line-height bump applied
- No italic on UI labels (only on prose emphasis)
- The font is named, not the system default
