# conversion-focused-saas

Marketing surfaces that earn the buy through confident, craft-led design. The marketing site is product-calibre: it reads as a careful software artefact, not a sales page.

**Surface category:** marketing-websites
**Exemplars:** Linear (primary, fully reviewed), Stripe (secondary), Vercel (secondary)
**Confidence:** high; values confirmed against Linear.app devtools (May 2026)

Read this alongside `references/batch-design-grammar.md`. Charts appear rarely on marketing surfaces; when they do, they pull product screenshots from the actual app, not constructed diagrams.

---

## When to use this archetype

Pick this when the brief is "marketing site for a modern SaaS, dev-tool, or AI product." This suits products that compete on craft as much as feature set: the marketing site is the strongest proof point. Skip it when the product is consumer-led (use `playful-brand-led`), heavily editorial (use `editorial-storytelling`), or enterprise-formal. If the user supplied direction, follow it and use this file for the parts they didn't specify.

**Key visual contract:** dark mode canonical for marketing, light mode for the app. This is intentional; these archetypes deliberately diverge. A dark marketing page makes product screenshots glow. A light marketing page makes them muddy.

---

## Design token reference

| Token | Light | Dark (canonical) | Role |
|-------|-------|------------------|------|
| `$bg` | `#FAFAFA` | `#0E0E10` | Page background. Dark is canonical for this archetype. |
| `$surface` | `#FFFFFF` | `#17171A` | Cards, screenshot frames, code blocks. |
| `$surfaceMuted` | `#F4F4F5` | `#1F1F23` | Footer, secondary background sections. |
| `$border` | `#E7E5E4` | `#2A2A2E` | 1px hairlines, card edges. Low-contrast in dark mode. |
| `$textPrimary` | `#111110` | `#F0EEEC` | Headlines, body copy. |
| `$textSecondary` | `#6B6A6B` | `#A8A29E` | Nav links, subheadings, feature copy. |
| `$textMuted` | `#A1A0A0` | `#57534E` | Section labels, legal text, small print. |
| `$accent` | Cyan, turquoise, or brand hue at 60–80% saturation. | | Primary CTAs, link hover, badges, subtle gradient sweeps. |
| `$accentSupport` | Purple/lavender at reduced saturation. | | Category badges; Linear pairs cyan + purple/lavender. |
| `$fontDisplay` | `Inter Display` or `Söhne` | | Headlines 48px and above. |
| `$fontBody` | Same family as display, regular weight. | | Body copy, nav, feature descriptions. |
| `$fontMono` | `Geist Mono` or `JetBrains Mono` | | Decimal section labels, metric callouts, code blocks. |

---

## Top nav

### Anatomy

```
TopNav (frame, fill_container x 56, layout: horizontal, alignItems: center,
         padding: [0, 40], justifyContent: space_between,
         fill: "$bg",
         stroke: { color: "$border", thickness: 1 })
         // stroke is bottom only in practice — use a 1px frame divider below the nav
├── NavLeft (frame, fit_content x fill_container, layout: horizontal,
│            alignItems: center, gap: 36)
│   ├── Logo (frame, 24 x 24, cornerRadius: 4, fill: "$accent")
│   └── NavLinks (frame, fit_content x fill_container, layout: horizontal,
│                  alignItems: center, gap: 24)
│       └── NavLink × N (text, $textSm, $textSecondary, content: "Product")
│           // Nav items: sentence-case. Never title case.
└── NavRight (frame, fit_content x fill_container, layout: horizontal,
               alignItems: center, gap: 8)
    ├── SignInLink (text, $textSm, $textSecondary, content: "Log in")
    └── CTAButton (frame, fit_content x 32, layout: horizontal,
                   alignItems: center, padding: [0, 14], cornerRadius: 8,
                   fill: "$accent")
        └── CTAText (text, $textSm, fontWeight: 600, fill: "$bg",
                     content: "Get started")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Nav height | 56px | Same as app topbar for visual continuity when transitioning. |
| Nav padding | `[0, 40]` | 40px horizontal. More generous than app surfaces. |
| NavLink gap | 24px | Generous. Marketing nav has fewer items than app nav. |
| CTA height | 32px | Compact in nav; the hero CTA is larger (44px). |
| CTA corner radius | 8px | Range: 6–10. Never fully rounded pill. |

### What generic looks like

```
// WRONG: gradient fill on the CTA button in the nav
CTAButton=I(navRight, {
  fill: [{ type: "gradient", ... }]
  // The CTA gradient is the single strongest AI-slop signal in marketing design.
  // Flat accent fill only.
})

// WRONG: nav background with a backdrop blur or glass effect
TopNav=I(page, {
  fill: [{ type: "color", color: "$bg", opacity: 0.85 }],
  // backdropFilter: "blur(12px)"  (not a valid Pencil property)
  // Just "$bg" solid fill.
})

// WRONG: title-case nav links ("Get Started", "Sign Up")
// Sentence-case only: "Get started", "Sign up". Matching the app tone.
```

---

## Hero section

### Anatomy

```
HeroSection (frame, fill_container x 720, layout: vertical,
              alignItems: center, justifyContent: center,
              padding: [120, 40, 80, 40],
              fill: "$bg")
│   // 720px tall. Fills the viewport on a 1440×900 canvas after the 56px nav.
├── HeroEyebrow (frame, fit_content x 24, layout: horizontal, alignItems: center,
│                gap: 6, padding: [0, 10], cornerRadius: 12,
│                stroke: { color: "$border", thickness: 1 })
│   // Optional category badge above the headline.
│   ├── EyebrowDot (frame, 6 x 6, cornerRadius: 3, fill: "$accent")
│   └── EyebrowText (text, 12px, $textSecondary, content: "Now in beta")
├── HeroHeadline (text, 64px, fontWeight: 700, $textPrimary,
│                 content: "Code review for teams and agents",
│                 textAlign: "center", width: 840, lineHeight: 1.1,
│                 fontFamily: "$fontDisplay")
│   // Font size 64px. Range: 56–80px depending on headline length.
│   // Width: 840px for 1440 layout. Narrower for shorter headlines.
│   // Line-height 1.1 for display headlines. Never 1.5 — too much gap.
├── HeroSubhead (text, 18px, $textSecondary, fontFamily: "$fontBody",
│               content: "Designed for the AI era. Pull requests review themselves.",
│               textAlign: "center", width: 560, lineHeight: 1.55)
├── HeroCTARow (frame, fit_content x fit_content, layout: horizontal,
│               alignItems: center, gap: 12)
│   ├── PrimaryCTA (frame, fit_content x 44, layout: horizontal, alignItems: center,
│   │               padding: [0, 20], cornerRadius: 10, fill: "$accent")
│   │   └── CTAText (text, 16px, fontWeight: 600, fill: "$bg",
│   │               content: "Try the new model")
│   │   // CTA height: 44px. Larger than app CTAs (32px) — needs to catch the eye.
│   │   // CTA copy: confident, specific. "Try the new model" not "Get started".
│   └── SecondaryCTA (frame, fit_content x 44, layout: horizontal, alignItems: center,
│                     padding: [0, 20], cornerRadius: 10,
│                     stroke: { color: "$border", thickness: 1 })
│       └── CTAText (text, 16px, $textSecondary, content: "Watch demo")
└── HeroSubcopy (text, 13px, $textMuted, fontFamily: "$fontBody",
                 content: "No credit card required",
                 textAlign: "center")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Hero height | 720px | Fills the viewport at 1440×900 minus nav. |
| Vertical padding | 120px top, 80px bottom | Generous. This is the archetype's "monumental" register. |
| Headline font size | 64px | Range: 56–80. Adjust for headline length. Never below 48. |
| Headline width | 840px | Tighter than the full page width. Long lines are harder to read in display type. |
| Headline line-height | 1.1 | Display type. Not body line-height (1.5). |
| Subhead font size | 18px | Larger than app body (14px). Marketing copy needs more breathing room. |
| Subhead width | 560px | Narrower than headline; creates a visual funnel. |
| Primary CTA height | 44px | 12px taller than app CTAs. Marketing CTAs need visual weight. |

### What generic looks like

```
// WRONG: generic CTA copy
PrimaryCTA=I(heroCTARow, { ..., content: "Get Started" })
// "Get Started" is the most generic CTA in SaaS history.
// Write copy that names the specific action: "Try the new model", "Start building",
// "Ship your first review". The CTA should only work for this product.

// WRONG: hero on a white background with a light colour scheme
HeroSection=I(page, { fill: "#FFFFFF", ... })
// Dark mode is canonical for this archetype.
// A white marketing page makes the product screenshots hard to read.

// WRONG: large illustrated hero scene (mascot, abstract 3D shapes)
// Use a product screenshot or a code block. The product IS the visual.
// An illustration says "we couldn't show you the product because it doesn't look good."

// WRONG: animated "scroll to explore" chevron below the hero
// There is no chevron. The section ends and the next section begins.

// WRONG: headline line-height 1.5 (body line-height)
HeroHeadline=I(hero, { ..., lineHeight: 1.5 })
// Display headlines use 1.0–1.15. A 64px headline at 1.5 line-height
// leaves 32px gaps between lines — it reads as a loading skeleton.
```

**Detect:**
- CTA fills are gradients: replace with flat `$accent` fill.
- Hero background is white or light grey: this archetype is dark.
- CTA copy is "Get Started" or "Learn More": rewrite to something product-specific.
- Headline line-height feels too open: check that it's ≤ 1.15 for display sizes.

---

## Numbered feature section

### Anatomy

```
FeatureSection (frame, fill_container x fit_content, layout: vertical,
                 alignItems: center, gap: 48,
                 padding: [80, 40],
                 fill: "$bg")
├── SectionMeta (frame, fit_content x fit_content, layout: horizontal,
│                alignItems: baseline, gap: 12)
│   ├── DecimalLabel (text, $textSm, $fontMono, $textMuted,
│   │                content: "1.0")
│   │   // Decimal label: monospace, muted. The section number, not a marketing label.
│   └── SectionTitle (text, 36px, fontWeight: 600, $textPrimary,
│                     fontFamily: "$fontDisplay", content: "Intake")
├── SectionSubcopy (text, 18px, $textSecondary, fontFamily: "$fontBody",
│                   content: "Make product operations self-driving.",
│                   textAlign: "center", width: 600, lineHeight: 1.5)
└── ScreenshotFrame (frame, 960 x 540, cornerRadius: 12,
                      fill: "$surface",
                      stroke: { color: "$border", thickness: 1 })
    // Product screenshot. 16:9 aspect ratio. 960px wide (two-thirds of 1440).
    // Use G("screenshotId", "unsplash", "software UI dashboard") as placeholder.
    // In production: actual product screenshots, not stock photography.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Section padding | 80px vertical | Range: 64–120px. More generous than app surfaces. |
| Section title size | 36px | Range: 32–48px. Decimal label stays small (13px) regardless. |
| Decimal label font | `$fontMono` | Non-negotiable. It reads as "engineering precision", not "design flair." |
| Screenshot width | 960px | Two-thirds of 1440. Full-width (1440×auto) for premium hero moments. |
| Screenshot aspect | 16:9 (960×540) | Standard. 4:3 (960×720) for portrait-heavy UIs. |
| Screenshot corner radius | 12px | Rounded, not pill. Matches card radius in this archetype. |

### What generic looks like

```
// WRONG: no decimal label (plain "Intake" as heading with no number)
// The numbered sections are the archetype's signature.
// Without them, the page reads as a standard three-column feature grid.

// WRONG: stock photography in the screenshot frame
ScreenshotFrame=I(featureSection, {
  type: "frame", ...
})
G("screenshotId", "unsplash", "team meeting laptop")
// People at laptops is the single most common anti-cue in this archetype.
// The screenshot should show the actual product UI.

// WRONG: section copy as a bullet list
// "• Faster review cycles\n• AI-powered suggestions\n• Real-time feedback"
// One confident sentence. Not bullets. "Make product operations self-driving."

// WRONG: three feature sections all at the same height and layout
// Vary the screenshot placement and section height subtly.
// Monotony breaks the sense of authorship.
```

---

## Customer metric callout

### Anatomy

```
MetricCallout (frame, fit_content x fit_content, layout: vertical,
                gap: 6, padding: [0, 0])
├── MetricValue (text, 48px, fontWeight: 700, $textPrimary,
│               fontFamily: "$fontMono", content: "2.4×")
│   // Monospace for metric values — signals precision, not assertion.
│   // Unit included in the value: "2.4×", "52%", "28%". Not a separate text node.
└── MetricDescription (text, $textSm, $textSecondary,
                        fontFamily: "$fontBody",
                        content: "faster review cycles",
                        width: 140, lineHeight: 1.4)
```

### MetricsRow layout

```
MetricsRow (frame, fill_container x fit_content, layout: horizontal,
             justifyContent: center, gap: 64, padding: [48, 40])
└── MetricCallout × 3
// Typical: 3–4 metrics. Beyond 4, the row becomes too wide at 1440.
```

### WHY monospace for metrics, proportional for pricing

Metric callouts ("2.4×", "52%") are data claims; they benefit from the precision signal of monospace. Pricing figures ("$49") are emotional communication: the offer. Monospace on pricing makes "$49" look like a database cell. Proportional figures for pricing, monospace for measured performance metrics.

### What generic looks like

```
// WRONG: metrics in proportional font
MetricValue=I(callout, { fontFamily: "$fontBody", ... })
// Loses the precision signal. Reads as an assertion, not a measurement.

// WRONG: long descriptive copy under each metric
// "Our customers report completing feature work 2.4 times faster than they did before
//  adopting our platform, according to a study conducted in Q3."
// Keep it terse: "2.4× faster review cycles". The brevity IS the claim.

// WRONG: metric value separated from unit ("2.4" in one node, "×" in another)
// The value and unit read as a single visual token. Keep them in one text node.
```

---

## Pricing tier card

### Anatomy

```
PricingTier (frame, 280 x fit_content, layout: vertical,
              gap: 20, padding: [24, 24, 28, 24],
              fill: "$surface",
              stroke: { color: "$border", thickness: 1 },
              cornerRadius: 12)
├── TierHeader (frame, fill_container x fit_content, layout: vertical, gap: 4)
│   ├── TierName (text, $textBase, fontWeight: 600, $textPrimary,
│   │             content: "Business")
│   └── TierDescription (text, $textSm, $textSecondary,
│                         content: "For growing teams building complex products.",
│                         lineHeight: 1.5)
├── PriceBlock (frame, fill_container x fit_content, layout: horizontal,
│               alignItems: baseline, gap: 2)
│   ├── CurrencySymbol (text, 18px, $textSecondary,
│   │                   fontFamily: "$fontBody", content: "$")
│   ├── PriceAmount (text, 40px, fontWeight: 700, $textPrimary,
│   │               fontFamily: "$fontBody", content: "49")
│   │   // Proportional font for pricing figures. NOT monospace.
│   └── PricePeriod (text, $textSm, $textMuted,
│                    fontFamily: "$fontBody",
│                    content: "/mo per seat, billed annually")
├── CTAButton (frame, fill_container x 40, layout: horizontal,
│              alignItems: center, justifyContent: center",
│              cornerRadius: 8, fill: "$accent")
│   └── CTAText (text, $textSm, fontWeight: 600, fill: "$bg",
│               content: "Start free trial")
└── FeatureList (frame, fill_container x fit_content, layout: vertical, gap: 10)
    └── FeatureItem × N (frame, fill_container x fit_content, layout: horizontal,
                          alignItems: flex_start, gap: 8)
        ├── CheckIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
        │             iconFontName: "check", fill: "$positive")
        └── FeatureText (text, $textSm, $textSecondary,
                          content: "All Free features +")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Card width | 280px | Four cards at 280px with 16px gaps = 1168px, centred on 1440. |
| Card padding | `[24, 24, 28, 24]` | Extra 4px bottom gives the feature list breathing room. |
| Price font size | 40px | Proportional (not monospace). Clear hierarchy over the tier name (16px). |
| CTA height | 40px | Slightly shorter than hero CTA (44px). Proportionate to the card scale. |
| Feature check icon | 14 × 14px | Lucide `check`. `$positive` colour. Always include; don't omit for the free tier. |

### What generic looks like

```
// WRONG: monospace pricing figures
PriceAmount=I(priceBlock, {
  fontFamily: "$fontMono", content: "49"
})
// Monospace pricing reads as a data cell. Pricing is an emotional offer; use proportional.

// WRONG: monthly/annual toggle when the model is annual-only
// Just show the annual price with "/mo per seat, billed annually" as the period label.
// A toggle implies the user can choose monthly. If they can't, don't show a toggle.

// WRONG: highlighted "popular" tier with a shadow and badge
// Use a subtle $accent stroke on the recommended tier instead of a card that floats
// on a drop shadow. Shadows on cards are an anti-cue in this archetype.

// WRONG: feature list with 12+ line items
// Cap at 6–8 items. Use "All [Tier] features +" as the first item.
// A 12-item checklist reads as feature dumping, not positioning.
```

---

## Method section (editorial manifesto)

The Method page is a signature move: type-led, no screenshots, philosophical.

### Anatomy

```
MethodSection (frame, fill_container x fit_content, layout: vertical,
                alignItems: center, gap: 64,
                padding: [80, 40],
                fill: "$bg")
├── MethodHeadline (text, 48px, fontWeight: 700, $textPrimary,
│                   content: "There is a lost art of building true quality software.",
│                   textAlign: "center", width: 720, lineHeight: 1.15,
│                   fontFamily: "$fontDisplay")
├── MethodIntro (text, 18px, $textSecondary, fontFamily: "$fontBody",
│               content: "We believe software is a craft.",
│               textAlign: "center", width: 560, lineHeight: 1.6)
└── PrinciplesList (frame, fill_container x fit_content, layout: vertical, gap: 40,
                     width: 720)
    └── PrincipleItem (frame, fill_container x fit_content, layout: horizontal,
                        gap: 24, alignItems: flex_start)
        ├── PrincipleNumber (text, $textSm, $fontMono, $textMuted,
        │                    content: "1.1", width: 32)
        └── PrincipleText (frame, fill_container x fit_content, layout: vertical, gap: 8)
            ├── PrincipleTitle (text, $textBase, fontWeight: 600, $textPrimary,
            │                   content: "Write issues not user stories")
            └── PrincipleBody (text, $textSm, $textSecondary,
                                content: "User stories are a way of pretending you know what users want.",
                                lineHeight: 1.6)
```

### Critical rules

- No screenshots in the Method section. It is type-only.
- Principle numbers use decimal notation (1.1, 1.2, 2.1), same register as the numbered sections.
- The opening headline is a claim, not a description. "There is a lost art..." is a claim. "Our approach to software" is a description.
- Principle titles are directives: "Write issues not user stories", "Build in public", "Launch and keep launching". Not "Issue Writing" or "Transparency".

---

## Microcopy library

### Hero headlines (exemplar register)

The headline is a claim. It should only work for this specific product, not any competitor.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| The all-in-one platform for teams | Issue tracking is dead |
| Work better together | A new species of product tool |
| Build faster with AI | Code review for teams and agents |
| Your productivity suite | Purpose-built for planning and building products |
| The future of work | Plan the present. Build the future. |

### CTA copy

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Get Started | Try the new model |
| Learn More | Read the Method |
| Sign Up Free | Start building |
| Book a Demo | Watch demo |
| Try It Now | Ship your first review |

Never "Get Started" as a primary CTA. It's the single most generic CTA in SaaS history and communicates nothing about the product.

### Customer metric format

Always: `[number][unit]` in one text node, then `[short description]` below.

- "2.4× faster review cycles"
- "52% reduction in bug resolution time"
- "28% of issues authored by agents"
- "3.3× faster issue resolution"

The number leads. The description is always specific, not "improved performance" but "faster review cycles". Quantified claims over flowing quotes.

### Pricing CTA

| Tier | CTA |
|------|-----|
| Free | Start for free |
| Paid | Start free trial |
| Enterprise | Contact sales |

Never "Get Started" or "Sign Up" on a pricing card. Name the action: "Start free trial" tells the user they get a trial. "Start for free" tells them it's free. "Get Started" tells them nothing.

---

## Verification checklist

### Structure

- [ ] **Page background is dark (`$bg` = `#0E0E10` or similar), not white.**
  WHY: Dark mode is canonical for this archetype. A light marketing page makes product screenshots (typically designed for dark backgrounds) hard to read and undermines the "premium craft tool" positioning.

- [ ] **Content width for centred sections is capped at 840–960px for text, 1040–1200px for screenshots.**
  WHY: A 1440-wide page with full-width body text produces line lengths of 100+ characters. Readability breaks above 75 characters per line. Cap text width and centre it.

### Hero

- [ ] **Hero headline is 56px or larger.**
  WHY: This archetype's visual register is "monumental." A 36px headline on a 1440-wide canvas reads as a product feature section, not a hero. 56–72px sets the scale hierarchy correctly.

- [ ] **Primary CTA is 44px tall with flat `$accent` fill.**
  WHY: Marketing CTAs need more visual weight than app CTAs. 44px gives a clear tap/click target. Gradient fills are the most common AI slop signal in marketing design; flat colour reads as deliberate.

- [ ] **CTA copy is product-specific (not "Get Started", "Learn More", or "Sign Up Free").**
  WHY: Generic CTA copy signals generic thinking. Confident SaaS marketing writes copy that only works for that product. "Get Started" works for any product; "Try the new model" only works for one.

- [ ] **Hero background is dark, not white or light grey.**
  WHY: See page structure note above. Consistency between page background and hero section.

### Feature sections

- [ ] **Section numbers use decimal notation in `$fontMono` (1.0, 2.0, 3.0).**
  WHY: Decimal notation reads as "engineered system." It signals that the product was planned, not assembled. Sans-serif numbered bullets read as a feature list. Monospace decimal labels read as a philosophy.

- [ ] **Screenshots show the actual product UI, not stock photography.**
  WHY: The product UI is the proof. Stock photography says "we had budget for marketing." The actual UI says "the product looks this good."

- [ ] **Section copy is one sentence, not a bullet list.**
  WHY: Bullet lists invite the reader to skim and move on. One confident sentence demands to be read and believed. "Make product operations self-driving" is a claim. Three bullets about the same feature are feature specifications.

### Pricing

- [ ] **Pricing figures use proportional font, not monospace.**
  WHY: Pricing is an emotional offer. "$49" in proportional type reads as a personal proposal. "$49" in monospace reads as a cell in a database table. One framing closes deals; the other undermines them.

- [ ] **No monthly/annual billing toggle if the model is annual-only.**
  WHY: A toggle implies a choice. Showing a toggle for a monthly price that the business doesn't offer creates a misleading affordance. Show the annual price with "billed annually" in the period label.

---

## Contrast examples

### Example 1: Hero headline and CTA (correct vs generic)

**Correct:**

```
heroHeadline=I(hero, {
  type: "text", name: "HeroHeadline",
  content: "Code review for teams and agents",
  fontFamily: "$fontDisplay", fontSize: 64,
  fontWeight: 700, fill: "$textPrimary",
  textAlign: "center", width: 840, lineHeight: 1.1
})
primaryCTA=I(heroCTARow, {
  type: "frame", name: "PrimaryCTA",
  layout: "horizontal", alignItems: "center",
  padding: [0, 20], cornerRadius: 10,
  height: 44, fill: "$accent"
})
ctaText=I(primaryCTA, {
  type: "text", content: "Try the new model",
  fontFamily: "$fontBody", fontSize: 16,
  fontWeight: 600, fill: "$bg"
})
```

Why this is right: 64px headline at 1.1 line-height reads as monumental, not cramped. Flat accent CTA at 44px has visual weight. "Try the new model" is specific to this product.

**Generic:**

```
heroHeadline=I(hero, {
  type: "text",
  content: "The all-in-one platform for modern teams",  // WRONG: generic
  fontSize: 48,   // WRONG: too small
  lineHeight: 1.5  // WRONG: body line-height on display type
})
primaryCTA=I(hero, {
  type: "frame",
  height: 32,   // WRONG: app-scale, not marketing-scale
  fill: [{ type: "gradient", ... }],  // WRONG: gradient fill
})
ctaText=I(primaryCTA, {
  type: "text", content: "Get Started"  // WRONG: generic
})
```

Why this is wrong: 48px at 1.5 line-height gives a headline that reads as a section title, not a hero. A 32px CTA is invisible at 1440px. "Get Started" with a gradient fill is the most common AI-generated marketing pattern; it appears on every AI-default marketing design regardless of product.

---

### Example 2: Numbered section vs feature grid (correct vs generic)

**Correct:**

```
sectionMeta=I(featureSection, {
  type: "frame", name: "SectionMeta",
  layout: "horizontal", alignItems: "baseline", gap: 12
})
decimalLabel=I(sectionMeta, {
  type: "text", name: "DecimalLabel",
  content: "1.0", fontFamily: "$fontMono",
  fontSize: "$textSm", fill: "$textMuted"
})
sectionTitle=I(sectionMeta, {
  type: "text", name: "SectionTitle",
  content: "Intake",
  fontFamily: "$fontDisplay", fontSize: 36,
  fontWeight: 600, fill: "$textPrimary"
})
sectionCopy=I(featureSection, {
  type: "text",
  content: "Make product operations self-driving.",
  fontSize: 18, fill: "$textSecondary",
  textAlign: "center", width: 560
})
// Then a full-width product screenshot frame.
```

Why this is right: decimal label in monospace muted type reads as precision. One-sentence section copy makes a claim. Product screenshot is the proof.

**Generic:**

```
// A 3-column feature grid:
featureGrid=I(page, {
  type: "frame", layout: "horizontal", gap: 24
})
featureCard=I(featureGrid, {
  type: "frame", layout: "vertical", gap: 12, padding: [24, 24],
  cornerRadius: 12, fill: "$surface",
  effect: [{ type: "drop_shadow", ... }]   // WRONG: shadow
})
featureIcon=I(featureCard, {
  type: "icon_font", iconFontName: "zap",
  width: 32, height: 32, fill: "$accent"   // WRONG: large icon as decoration
})
featureTitle=I(featureCard, {
  type: "text", content: "Fast Workflows",  // WRONG: title-case generic phrase
  fontSize: 18, fontWeight: 600
})
featureBullets=I(featureCard, { ... })
// "• Feature one\n• Feature two\n• Feature three"  // WRONG: bullet list
```

Why this is wrong: a 3-column feature grid with icons, title-case headings, and bullet lists is the standard AI-generated marketing page output. It contains zero information about the product's actual differentiation. The numbered section approach forces the copy to make one specific claim per section, which is harder to write but impossible to confuse with any other product's marketing.
