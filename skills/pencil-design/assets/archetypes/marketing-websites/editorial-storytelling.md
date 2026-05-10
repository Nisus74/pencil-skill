# editorial-storytelling

> Long-form narrative surfaces where the chrome disappears and the content carries the reader through a single arc.

**Surface category:** marketing-websites
**Confidence:** confirmed via Linear Method page (May 2026); Apple product pages and Tesla cited from public knowledge.
**Exemplars:** Linear Method page (philosophical-manifesto flavour), Apple product pages (cinematic-narrative flavour), Tesla's older marketing (cinematic flavour)

## When to choose this archetype

Pick this when the brief is a single product launch, a manifesto / methodology page, or a deep-dive feature story, anywhere the goal is *the reader stays for the whole arc* rather than *the reader scans and converts*. Two distinct flavours live under this one archetype:

- **Cinematic product narrative** (Apple-style): full-bleed product imagery, scroll-driven reveals, one product highlighted.
- **Editorial manifesto** (Linear-Method-style): type-only, numbered sections, prescriptive philosophical claims.

Pick `conversion-focused-saas` when you need pricing tiers, feature matrices, and structured CTAs. Pick this archetype when the page IS the message.

## Typography

- **Display headlines:** large editorial. 64–120px on hero. Modern sans (Söhne, Inter Display, Geist) or a deliberate serif (Fraunces, Editorial New, Instrument Serif) when the brand permits, serifs make sense in the manifesto flavour, less so in cinematic-product.
- **Body:** longer-form than `conversion-focused-saas`. 18–22px body type with line-height 1.5–1.7. Reading is the activity.
- **Section labels:** numbered chapters in the manifesto flavour (`1.1`, `1.2`, `2.1`...). The Linear Method uses `1.1 Set the product direction`, `2.1 Write issues not user stories`. Decimal labels render in muted display weight beside or above the heading.
- **Pull quotes:** large standalone editorial moments, 32–48px, often in italic or a contrasting weight. One per section maximum. Pull quotes break the body's rhythm intentionally.
- **Inline emphasis:** bold sparingly; italics for terminology or quoted phrases. The tone is editorial, not technical.

## Density

- Hero is enormous: 200px+ vertical padding, headline takes 60–80% of viewport height alone.
- Section padding 160–240 vertical. Long sections, single point each.
- Content max-width tight for prose: 680–760px (matches the SKILL.md rule of ~65 characters per line for prose).
- Visual moments (full-bleed images, large pull quotes) break out of the text column to fill the viewport.

## Accent strategy

- Restrained accent. Used sparingly, link colour, the rare CTA, sometimes a section-marker rule.
- The page leans on contrast and scale rather than colour to create hierarchy.
- For the cinematic-product flavour, the *product itself* often carries the brand colour; the page chrome is intentionally neutral so the product reads cleanly.
- For the manifesto flavour, the page may be near-monochrome with one accent appearing once or twice across the entire scroll.

## Surface treatment

- Light or dark, often with a **deliberate mode shift between sections**, Apple product pages famously alternate dark sections with light to create rhythm. One section dark, next section light, next dark.
- No card metaphor. Content sits directly on the page background, separated by whitespace and section transitions, not by container chrome.
- Borders almost absent. When a divider appears, it's a hairline rule across the full content width.
- Edges and corners barely matter, there are few rectangles to round.

## Data display

- Data is rare. When it appears (a single statistic, a benchmark), it's rendered editorially: a large numeric paired with one line of context. *"3x faster than the previous generation."*
- No charts, no tables, no comparison matrices. Those break the narrative; if the brief needs them, use `conversion-focused-saas` for that section instead and link to it.
- Code blocks (in technical editorial pieces) are styled as quoted material, large, breathing, treated as part of the narrative, not as a sidebar.

## Microcopy and voice

- Prescriptive and confident in the manifesto flavour. Linear's Method opens with *"There is a lost art of building true quality software."* and follows with declarative principles: *"Write issues not user stories"*, *"Build in public"*, *"Launch and keep launching"*. Each principle is a thesis, not a feature description.
- Cinematic in the product flavour. Apple-style: *"The most powerful chip we've ever made"*, *"Designed for the next decade of computing"*. Confident, monumental, single claim per section.
- Body copy reads as essay, not marketing. Full sentences, paragraphs, deliberate rhythm. *"For 30 years, software development teams have used issue trackers..."*
- No bullet lists where prose can do the same work. Bullets fragment the reading experience.
- Headings are statements, not labels. *"A new way to think about issues"*, not *"Issues"*.

## Motion personality

- Cinematic motion in the product flavour: long fade-in reveals (400–600ms ease-out), parallax background shifts, product imagery scaling up as the user scrolls into it.
- Restrained motion in the manifesto flavour: short fade-ups on scroll (200–300ms), nothing flashy. The text does the work.
- Avoid: bouncy springs, character-by-character text reveals, looping ambient particle motion. Editorial archetypes earn slow because the content rewards patience.

## Anti-cues (don't reach for these in this archetype)

- Sticky top nav with 8 items competing with the headline.
- Three-column feature grids (the page has one column of attention).
- Pricing tier cards.
- "Book a demo" CTAs every 600px of scroll.
- Stock photography of meeting rooms.
- Floating chat widgets (they distract from the read).
- Comparison tables vs competitors.
- Animated chevron prompts under the hero.
- Section-internal carousels that interrupt the linear flow.
- Pop-up newsletter modals on first scroll.
- Generic value-prop sub-headers like *"Why choose us"*.

## Worked example: a methodology page like the Linear Method

For a brief like *"build a Method page for our product, articulating our philosophy of how teams should work"*:

- **Hero:** centred page title at 96–120/600, *"The Linear Method"*. Subhead at 22/400, two lines max, restating the page's intent. No CTA at hero; no chevron beneath; the section just ends.
- **Opening editorial paragraph:** 22/400, max-width 680px, opens with a confident philosophical claim. *"There is a lost art of building true quality software."* Followed by 1–2 paragraphs of context.
- **Section 1, Direction:** numbered subsections (`1.1 Set the product direction`, `1.2 Plan in cycles`, `1.3 Choose initiatives wisely`, `1.4 Define the product`). Each subsection: small `1.1` decimal label, larger heading, then 1–3 paragraphs of body. Generous space between subsections (96–120px).
- **Section 2, Building:** 6 numbered subsections in the same shape. Each with prescriptive title and essay body.
- **Pull quote** at one or two strategic points: 40px italic, breaking out of the body column to span ~900px wide.
- **No images**, or one or two restrained editorial photographs. The Method is type-led.
- **Closing** is quiet: a single line in muted weight, optionally a subtle link to read more or download the full method as PDF.

For a cinematic product narrative like an Apple product launch page:

- **Hero:** centred 120px headline, single product hero image full-bleed below.
- **Section 1:** dark background, full-bleed product render, one big claim above (*"The fastest we've ever made"*), short paragraph below.
- **Section 2:** light background (deliberate flip), close-up product detail, single feature highlight.
- **Section 3:** dark, ambient lifestyle imagery, second feature.
- **Continued alternation:** each section a single point, alternating dark/light, with full-bleed visuals and short editorial copy.
- **Final CTA section:** restrained, single primary action.

## Notes for AI implementers

Tokens this archetype implies (illustrative; rename to project's scheme):

| Token | Value |
|---|---|
| `$accent` | Restrained, used sparingly; saturation 50–70%. |
| `$bg` | For manifesto: near-white or near-black, single mode chosen. For cinematic: alternating modes by section. |
| `$surface` | Effectively the same as `$bg`; cards are absent. |
| `$borderSubtle` | Only used for occasional hairline rules, not for cards. |
| `$fontDisplay` | Editorial sans (`Söhne`, `Inter Display`) or modern serif (`Fraunces`, `Editorial New`, `Instrument Serif`) when brand permits. |
| `$fontBody` | Same family as display, regular weight. Sized 18–22px for reading. |
| `$proseMaxWidth` | 680–760px (~65ch for body). |

Components most affected: `EditorialHero`, `NumberedSubsection` (manifesto), `PullQuote` (large, breaks column), `FullBleedSection` (cinematic), `EditorialStatistic` (one large number with one-line context). Each gets a variant inside this archetype.

Common slip-ups:

- Adding pricing tiers or feature comparison tables. They belong in `conversion-focused-saas`; mixing breaks the reading experience.
- Using bullet lists where prose paragraphs would carry the same weight.
- Letting the page max-width follow the marketing-page default of 1200px. Prose blocks need the 680–760px constraint.
- Adding a sticky top nav that competes with the hero. Editorial pages often hide or minimise nav after scroll.
- Reaching for the Inter family generically. If using Inter Display, declare it explicitly per the modern-pro-tool override.
- Sprinkling small images throughout. Editorial visuals are large editorial moments, not decorative spacers.
- Treating the manifesto flavour like a features page (it's not). Treating the cinematic flavour like a manifesto (also not).
- Ending the page with a generic CTA section. Editorial pages often end quietly; the read itself was the conversion.
