# editorial-storytelling

Long-form narrative surfaces where chrome disappears and the content carries the reader through a single arc. Two distinct flavours live under this archetype: the editorial manifesto (type-led, philosophical) and the cinematic product narrative (full-bleed imagery, scroll-driven).

**Surface category:** marketing-websites
**Exemplars:** Linear Method page (manifesto flavour), Apple product pages (cinematic flavour)
**Confidence:** high; confirmed against Linear Method page devtools (May 2026), Apple from public knowledge

Read this alongside `references/batch-design-grammar.md`. Charts and component grids are anti-cues here; when data appears, it's a single large statistic, not a table.

---

## When to use this archetype

Pick this for single product launches, methodology pages, or deep-dive feature stories where the goal is that the reader stays for the whole arc. Skip it when the brief needs pricing tiers, feature matrices, and structured CTAs; use `conversion-focused-saas` instead.

Pick `conversion-focused-saas` when you need conversions. Pick this archetype when the page IS the message.

---

## Two flavours

**Manifesto (Linear Method style):** type-only or near-type-only. Numbered sections in decimal notation. Prescriptive philosophical claims. No product screenshots. The writing is the product.

**Cinematic (Apple product page style):** full-bleed product photography or rendered imagery. One product. Alternating dark/light sections, each with a single claim. Short copy. The visual is the product.

These two flavours share the same spacing scale, typography register, and anti-cues. They differ in what fills the visual moments.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | Near-white (`#FAFAF9`) for manifesto; near-black (`#0A0A0B`) for cinematic dark sections. | Page background. |
| `$bgDark` | `#0A0A0B` | Cinematic dark sections. Alternates with `$bg`. |
| `$surface` | Same as `$bg`; there are no cards. | This archetype has no card metaphor. |
| `$textPrimary` | `#111110` (light sections), `#F0EEEC` (dark sections) | Headlines, body copy. |
| `$textSecondary` | `#6B6A6B` (light), `#A8A29E` (dark) | Subheadings, supporting copy, section labels. |
| `$textMuted` | `#A1A0A0` (light), `#57534E` (dark) | Decimal labels, legal text. |
| `$accent` | Restrained. Saturation 50–70%. Used for link colour and one-off moments. | Appears 1–3 times on the entire page. |
| `$border` | Hairline only. `#E7E5E4` (light), `#2A2A2E` (dark) | Full-width rule between sections. Never on cards; this archetype has no card metaphor. |
| `$fontDisplay` | `Söhne`, `Inter Display`, or a deliberate serif (`Fraunces`, `Instrument Serif`) when brand permits. | Headlines. Serif is valid for the manifesto flavour. |
| `$fontBody` | Same family as display, regular weight. | 18–22px for reading. |
| `$fontMono` | `Geist Mono` | Decimal section labels (1.1, 2.1), code blocks, the occasional statistic. |
| `$proseMaxWidth` | 680–760px | Body text width. Approximately 65 characters per line at 18–20px. |

---

## Hero: manifesto flavour

### Anatomy

```
ManifestoHero (frame, fill_container x fit_content, layout: vertical,
                alignItems: center, padding: [180, 40, 120, 40],
                fill: "$bg")
│   // 180px top padding. The hero is enormous and slow.
│   // The headline should fill 60–70% of the viewport height.
├── PageTitle (text, 96px, fontWeight: 600, $textPrimary,
│              fontFamily: "$fontDisplay",
│              content: "The Linear Method",
│              textAlign: "center", width: 720, lineHeight: 1.05)
│   // Font size: 96px. Range: 80–120px depending on title length.
│   // Line-height: 1.05. Tighter than body — this is monumental type.
│   // Width: 720px keeps short titles from stretching too wide.
└── HeroSubhead (text, 22px, $textSecondary, fontFamily: "$fontBody",
                 content: "Opinionated principles for building quality software.",
                 textAlign: "center", width: 560, lineHeight: 1.55)
    // Subhead is 2 lines maximum. No CTA. The section just ends.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Hero top padding | 180px | Minimum. Creates the monumental register. Below 120px it reads as a section, not a hero. |
| Hero bottom padding | 120px | Gives space before the first prose section. |
| Headline font size | 96px (manifesto) | Range: 80–120px. Never below 72 for this archetype. |
| Headline line-height | 1.05 | Not body line-height (1.6). Display type at 96px needs tight leading. |
| Headline width | 720px | Short titles: 480–560px. Long titles: up to 840px. |
| No CTA | required | The manifesto hero has no CTA. The read IS the conversion. |

### What generic looks like

```
// WRONG: CTA button in the manifesto hero
CTAButton=I(hero, {
  type: "frame", fill: "$accent", ...
  content: "Read the Method"
})
// The manifesto hero does not have a CTA. The reader is already here.
// Adding a CTA says "we don't trust this page to hold your attention."

// WRONG: hero font size 48–56px
PageTitle=I(hero, { fontSize: 48, ... })
// 48px at 180px padding reads as a section header, not a hero title.
// This archetype is monumental. 80px is the floor.

// WRONG: hero padding 40–60px vertical
ManifestoHero=I(page, { padding: [40, 40], ... })
// 40px of padding is an app surface density.
// Editorial heroes need 160–200px top padding to breathe.
```

---

## Hero: cinematic flavour

### Anatomy

```
CinematicHero (frame, fill_container x 900, layout: none,
                fill: "$bgDark")
│   // 900px tall — fills most of a 1440×900 viewport.
│   // layout: none because the background image fills the frame.
├── HeroBackground (frame, fill_container x fill_container,
│                   // Fill with a generated or product image:
│                   // G("heroBg", "ai", "black product render on dark background")
│                   )
└── HeroContent (frame, fill_container x fit_content, layout: vertical,
                  alignItems: center, justifyContent: center",
                  padding: [0, 40],
                  // Centred vertically via absolute position — y: (900 - contentHeight) / 2
                  )
    ├── Eyebrow (text, 14px, $textMuted, $fontMono,
    │           content: "M4 Pro", textAlign: "center",
    │           letterSpacing: "0.1em")
    │   // Optional. Small model/product identifier above headline.
    ├── HeroHeadline (text, 120px, fontWeight: 700, fill: "$textPrimary",
    │                 fontFamily: "$fontDisplay",
    │                 content: "MacBook Pro.",
    │                 textAlign: "center", lineHeight: 1.0)
    │   // 120px. Apple product pages measure at this scale or larger.
    │   // Line-height: 1.0. Single-word headlines need zero gap between lines.
    └── HeroSubclaim (text, 24px, $textSecondary, fontFamily: "$fontBody",
                       content: "The most powerful chip we've ever made.",
                       textAlign: "center", width: 560, lineHeight: 1.4)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Hero height | 900px | Full viewport. Cinematic heroes fill the screen. |
| Headline font size | 120px | Range: 96–144px for product names and single-claim headlines. |
| Headline line-height | 1.0 | Product names on a dark background. Zero line gap for single-line titles. |
| Eyebrow tracking | `"0.1em"` | Wide tracking on the product category label. Not the headline. |
| Subclaim width | 560px | Narrower than headline for visual tapering. |
| Background content | AI render or product photography | Never stock photography of people. |

---

## Numbered subsection: manifesto

### Anatomy

```
NumberedSubsection (frame, $proseMaxWidth x fit_content, layout: vertical,
                     gap: 20, alignSelf: center)
│   // Width matches $proseMaxWidth (680–760px). Centred on the page.
├── SubsectionLabel (frame, fit_content x fit_content, layout: horizontal,
│                    alignItems: baseline, gap: 10)
│   ├── DecimalLabel (text, $textSm, $fontMono, $textMuted, content: "1.1")
│   └── SubsectionTitle (text, 28px, fontWeight: 600, $textPrimary,
│                         fontFamily: "$fontDisplay",
│                         content: "Write issues not user stories")
│   // Title is a directive, not a noun: "Write issues" not "Issue Writing".
├── SubsectionBody (text, 18px, $textSecondary, fontFamily: "$fontBody",
│                   content: "User stories are a holdover from an era when...",
│                   lineHeight: 1.65, width: "fill_container")
│   // 18px, 1.65 line-height. This is reading copy, not scanning copy.
└── SubsectionSpacer — (implicit in the parent's gap, not a separate node)
    // Gap between subsections in the parent: 96–120px.
    // Within a subsection (between label and body): 20px.
```

### Section container

```
ManifestoSection (frame, fill_container x fit_content, layout: vertical,
                   alignItems: center, gap: 96,
                   padding: [80, 40, 120, 40],
                   fill: "$bg")
│   // Gap between subsections: 96px. This is the "air" that makes editorial feel deliberate.
├── SectionOpenHeadline (text, 40px, fontWeight: 600, $textPrimary,
│                         fontFamily: "$fontDisplay",
│                         content: "Direction",
│                         textAlign: "center", width: $proseMaxWidth)
│   // Each section gets a single-word or short-phrase overhead label.
│   // Not "1.0 Direction" — the section label is just "Direction".
│   // The decimal numbers live inside each subsection.
└── NumberedSubsection × N
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Subsection title size | 28px | Range: 24–36px. Not as large as section headline. |
| Body font size | 18px | Minimum for editorial reading. 20px for more generous layouts. |
| Body line-height | 1.65 | Reading copy. This is not marketing copy; the reader will spend time here. |
| Prose max-width | 680–760px | ~65 characters per line. Above 760px lines become uncomfortable to read. |
| Gap between subsections | 96px | This is what makes editorial feel deliberate, not cramped. Never below 64px. |

### What generic looks like

```
// WRONG: subsection title as a noun phrase
SubsectionTitle=I(label, {
  content: "Issue Writing Principles"  // WRONG: nominal phrase
  // Should be: "Write issues not user stories"  — directive, not label
})

// WRONG: subsection body as bullet list
SubsectionBody=I(subsection, {
  type: "text",
  content: "• User stories are legacy\n• Issues are clearer\n• Engineers prefer them"
  // Bullets fragment the reading experience. Write prose.
})

// WRONG: gap between subsections 24–40px
ManifestoSection=I(page, { gap: 24, ... })
// 24px gap turns editorial into a tight list. The 96px gap is not decorative padding —
// it is how the reader understands that each subsection is a separate thought.

// WRONG: body line-height 1.4 (marketing copy line-height)
SubsectionBody=I(subsection, { lineHeight: 1.4, ... })
// 1.4 at 18px is readable but fast. Editorial copy needs 1.65 — the reader slows down.
```

---

## Pull quote

### Anatomy

```
PullQuote (frame, 860 x fit_content, layout: vertical,
            gap: 12, padding: [48, 0],
            alignSelf: center)
│   // 860px breaks out of the prose column ($proseMaxWidth 680–760px).
│   // No card background. No border. The type IS the container.
├── QuoteRule (frame, 40 x 2, fill: "$accent")
│   // Small horizontal accent rule above the quote. Optional.
│   // Width: 40px. Not full-width — it's an accent, not a divider.
└── QuoteText (text, 40px, $textPrimary, fontFamily: "$fontDisplay",
               fontStyle: "italic",
               content: "There is a lost art of building true quality software.",
               lineHeight: 1.2, width: 860)
    // 40px italic. Range: 32–48px.
    // Width: 860px — wider than the prose column, this is intentional.
    // One pull quote per section maximum.
```

### Critical rules

- No background fill. No card border. Pull quotes sit naked on the page.
- Width: 860px, intentionally wider than the 680–760px prose column. The typographic rupture IS the point.
- One per section. Two pull quotes in the same section cancel each other's effect.
- Not a testimonial. Pull quotes are the page's own most confident sentences.
- Accent rule above (40×2px) is optional. Some manifesto pages use it; some don't. Decide per project and stay consistent.

### What generic looks like

```
// WRONG: pull quote inside a card frame with border
PullQuote=I(section, {
  type: "frame",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 12, padding: [24, 24],
  ...
})
// Cards are an anti-cue in this archetype. Pull quotes have no container.

// WRONG: attribution below the quote ("— Karri Saarinen, Linear")
// The Method page pull quotes are the page's own voice, not attributed.
// If attribution is needed (genuine testimonial), use an entirely different component.

// WRONG: pull quote width matching the prose column (680px)
PullQuote=I(section, { width: 680, ... })
// The breakout to 860px IS the pull quote's typographic function.
// Matching prose width turns it into a slightly-larger paragraph.
```

---

## Full-bleed section: cinematic

### Anatomy

```
FullBleedSection (frame, fill_container x 720, layout: none,
                   fill: "$bgDark")
│   // Alternates: dark → light → dark. Each section one claim.
│   // Height: 720px typical. 900px for hero-scale moments.
├── SectionImage (frame, fill_container x fill_container)
│   // G("sectionImage", "ai", "product render, dark background, studio lighting")
│   // or a brand product photograph
├── SectionContent (frame, fill_container x fit_content, layout: vertical,
│                   alignItems: center, gap: 20,
│                   padding: [0, 40])
│   // Positioned via y: (section height - content height) / 2 (absolute)
│   ├── SectionClaim (text, 56px, fontWeight: 600, fill: "$textPrimary",
│   │                 fontFamily: "$fontDisplay",
│   │                 content: "The fastest we've ever made.",
│   │                 textAlign: "center", width: 680, lineHeight: 1.1)
│   └── SectionBody (text, 18px, $textSecondary, fontFamily: "$fontBody",
│                     content: "M4 Pro delivers performance no laptop has seen before.",
│                     textAlign: "center", width: 480, lineHeight: 1.5)
```

### Section alternation

Light sections use: `fill: "$bg"`, `$textPrimary` for text.
Dark sections use: `fill: "$bgDark"`, `fill: "$textPrimary"` (which resolves to near-white).

Build this consistently. The alternation is the rhythm; interrupting it destroys the cadence.

```
// Correct sequence:
section1=I(page, { fill: "$bgDark", ... })   // dark
section2=I(page, { fill: "$bg", ... })        // light
section3=I(page, { fill: "$bgDark", ... })   // dark
section4=I(page, { fill: "$bg", ... })        // light
```

### Critical rules

- One claim per section. "The fastest we've ever made." Not "The fastest we've ever made, with up to 64GB of memory."
- Claim font size: 48–72px. Subcopy: 18–20px. The size gap is intentional hierarchy.
- No nav, no sidebar, no sticky controls over the full-bleed image.
- Body copy is 2–3 sentences maximum. These are not feature descriptions.

---

## Editorial statistic

### Anatomy

```
EditorialStatistic (frame, fit_content x fit_content, layout: vertical,
                     gap: 8, alignSelf: center)
├── StatValue (text, 80px, fontWeight: 700, $textPrimary,
│             fontFamily: "$fontMono", content: "3×")
│   // Monospace for measured statistics. Same rule as analytics-dashboard.
│   // 80px. Range: 64–96px. The number should feel like a visual moment.
└── StatDescription (text, 18px, $textSecondary, fontFamily: "$fontBody",
                      content: "faster than the previous generation",
                      lineHeight: 1.4, width: 240)
    // One line of context. Not a paragraph. The number speaks first.
```

### What generic looks like

```
// WRONG: statistic inside a card
StatCard=I(section, {
  type: "frame",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 12, padding: [24, 24], ...
})
// Statistics in this archetype have no container. They float on the page background.

// WRONG: three statistics in a row as a "numbers section"
// A row of three statistics is a conversion-focused-saas pattern.
// In editorial-storytelling, use one statistic per section as a punctuation mark.

// WRONG: statistic in proportional font
StatValue=I(stat, { fontFamily: "$fontBody", content: "3×" })
// Monospace for measured data. See analytics-dashboard for the same rule.
```

---

## Microcopy library

### Headlines: manifesto register

Statements, not labels. Directive, not descriptive.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Our Approach | There is a lost art of building true quality software. |
| Issue Tracking Features | Issue tracking is dead |
| Team Principles | Write issues not user stories |
| Our Company Values | Build in public |
| Summary | The product that earns the work |

### Headlines: cinematic register

Single claims. Monumental. Product-specific.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Learn More About Our Product | The most powerful chip we've ever made |
| Faster Than Before | Built for the next decade |
| Great Camera Features | Photographs the moment you couldn't plan for |
| Designed Well | Designed to last |

### Body copy register

Editorial prose, not scanning copy. Full sentences. Paragraphs.

**Manifesto body:**
"For 30 years, software development teams have used issue trackers that look the same. The names change. The problem doesn't. We built Linear to do something different."

**Cinematic body:**
"M4 Pro packs more cores into less space than any chip before it. The result: tasks that took minutes finish in seconds."

Both: no bullet points. No exclamation marks. No rhetorical questions.

---

## Verification checklist

### Typography

- [ ] **Headline font size is 80px or larger (manifesto hero) / 96px or larger (cinematic hero).**
  WHY: Below 80px on a 1440-wide page, the headline reads as a section header, not a statement. The scale is how the archetype signals importance. A 48px headline in an editorial layout communicates "we are uncertain about this."

- [ ] **Body font size is 18px or larger, line-height 1.6 or higher.**
  WHY: Body copy in this archetype is reading copy, not scanning copy. 14–16px at 1.4 line-height works for apps; editorial prose requires 18–20px at 1.6–1.65 to feel like an article rather than a UI.

- [ ] **Prose max-width is 680–760px.**
  WHY: Above 760px, lines exceed 75 characters and become physically difficult to read. The narrow column also signals "this is prose"; it triggers reading mode in the user's brain.

### Structure

- [ ] **No card metaphor. Content sits on the page background.**
  WHY: Cards are navigation and organisation structures from app surfaces. In editorial, a card says "this content is separate from me." Editorial content is continuous. Every card frame in an editorial layout is evidence of an app archetype leaking in.

- [ ] **No pricing tiers, feature comparison tables, or "Why choose us" sections.**
  WHY: These are conversion-focused-saas components. Their presence in an editorial page breaks the reading contract. The reader arrived for an argument, not a sales page.

- [ ] **Cinematic sections alternate dark and light.**
  WHY: The alternation creates the page's rhythm. A page of all-dark sections is a product gallery. Alternating dark/light creates the cinematic pacing that makes each section feel like a separate beat.

### Spacing

- [ ] **Gap between numbered subsections is 80px or larger.**
  WHY: 80px is the minimum gap that reads as "deliberate pause." Below 64px, subsections merge into a list. The whitespace is not filler; it's a breathing instruction.

- [ ] **Hero top padding is 120px or larger.**
  WHY: Editorial heroes need air above the headline to create the "arriving into something important" sensation. A 40px padded hero reads as a marketing section, not an opening statement.

---

## Contrast examples

### Example 1: Numbered subsection (correct vs generic)

**Correct:**

```
subsectionLabel=I(subsection, {
  type: "frame", name: "SubsectionLabel",
  layout: "horizontal", alignItems: "baseline", gap: 10
})
decimalLabel=I(subsectionLabel, {
  type: "text", content: "1.1",
  fontFamily: "$fontMono", fontSize: "$textSm", fill: "$textMuted"
})
subsectionTitle=I(subsectionLabel, {
  type: "text", content: "Write issues not user stories",
  fontFamily: "$fontDisplay", fontSize: 28, fontWeight: 600, fill: "$textPrimary"
})
body=I(subsection, {
  type: "text",
  content: "User stories are a holdover from an era when developers weren't in the room. The job title was 'product manager' but the work was translation.",
  fontFamily: "$fontBody", fontSize: 18,
  fill: "$textSecondary", lineHeight: 1.65,
  width: "fill_container"
})
```

Why this is right: directive title reads as a thesis. Monospace decimal label. Prose body at editorial scale.

**Generic:**

```
subsectionTitle=I(section, {
  type: "text", content: "Issue Writing",  // WRONG: noun phrase, not a directive
  fontSize: 24   // WRONG: too small
})
bullets=I(section, {
  type: "text",
  content: "• User stories are outdated\n• Issues are clearer\n• Better for devs"
  // WRONG: bullet list instead of prose
})
```

Why this is wrong: "Issue Writing" is a label that could apply to any product. "Write issues not user stories" is a claim that Linear owns. Bullets shatter the reading experience into discrete fragments; editorial prose carries the reader through an argument.

---

### Example 2: Pull quote (correct vs generic)

**Correct:**

```
pullQuote=I(manifestoSection, {
  type: "frame", name: "PullQuote",
  layout: "vertical", gap: 12, padding: [48, 0],
  width: 860, alignSelf: "center"
  // No fill. No border. No cornerRadius.
})
quoteRule=I(pullQuote, {
  type: "frame", name: "QuoteRule",
  width: 40, height: 2, fill: "$accent"
})
quoteText=I(pullQuote, {
  type: "text",
  content: "There is a lost art of building true quality software.",
  fontFamily: "$fontDisplay", fontSize: 40,
  fontStyle: "italic", fill: "$textPrimary",
  lineHeight: 1.2, width: 860
})
```

Why this is right: no card frame, no border. 860px width breaks out of the 720px prose column; the rupture is intentional. 40px italic is a typographic event, not a larger paragraph.

**Generic:**

```
pullQuoteCard=I(section, {
  type: "frame",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 12, padding: [24, 24],  // WRONG: card with border
  fill: "$surface"  // WRONG: card background
})
quoteText=I(pullQuoteCard, {
  type: "text", content: "There is a lost art of building true quality software.",
  fontSize: 24,   // WRONG: too small — 24px doesn't register as a pull quote moment
  fill: "$textSecondary"  // WRONG: muted colour removes emphasis
})
attribution=I(pullQuoteCard, {
  type: "text", content: "— Company Name"  // WRONG: attribution on a page-voice quote
})
```

Why this is wrong: a card frame turns a pull quote into a callout box. At 24px inside a card, it reads as a "highlighted note," not a typographic event. Muted colour removes the emphasis. Attribution implies it's a testimonial, not the page's own voice.
