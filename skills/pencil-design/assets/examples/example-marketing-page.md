# Example: design a marketing page that doesn't look like every other SaaS

User says:

> *"Build a marketing page for our SaaS. Hero, features, pricing, testimonials, footer. Don't make it look like every other SaaS."*

The brief carries a constraint inside the request: avoid the SaaS defaults. The agent reaching for a centred hero with a three-card feature grid underneath would fail the brief on first contact. This walkthrough shows the picks that get there instead.

---

## Step 1: read context

The agent loads `assets/design-system/visual-style.md`, `assets/design-system/tokens.md`, and `references/layout-patterns.md`. The rule from `layout-patterns.md` § Feature sections is the load-bearing one for this brief: *the three-card feature grid is the most over-used SaaS marketing pattern; reach for alternating image-text rows or a bento grid first*. The agent commits to that rule before placing anything.

It also opens four headings inside `layout-patterns.md`: Hero variations for the top of the page, Pricing tables for the middle, plus Testimonial layouts and Footer architectures lower down. Each section of the page will pick deliberately from those menus.

**In Pencil:** no MCP calls yet; this is reading project markdown and the layout reference.

## Step 2: pick the hero variant

`references/layout-patterns.md` § Hero variations lists the options. Centred-text-and-CTA is the SaaS default and reads as generic. Two stronger picks for this brief:

- **Asymmetric (off-centre title).** Title left, illustration right, intentional negative space. Carries personality without showing off.
- **Bento.** Multiple value props share the hero. Good if the product has 4+ equally weighted hooks.

Pick **Asymmetric** for the example. The product has one clear pitch; bento would dilute it.

## Step 3: plan the page structure

Per `references/file-architecture.md` § Section frames as canvas regions, each section is a sibling top-level frame in the Source of Truth section. Names:

- `Marketing_Hero`
- `Marketing_Features`
- `Marketing_Pricing`
- `Marketing_Testimonials`
- `Marketing_CTA_Closing`
- `Marketing_Footer`

Six frames stacked vertically at the canvas origin. The agent will use `find_empty_space_on_canvas` once for the hero anchor, then offset each subsequent section by its predecessor's height plus a 120-pixel gutter.

## Step 4: build the hero (asymmetric)

Title sits left of centre, supporting paragraph below. Primary CTA *'Start your free trial'* paired with a secondary text link *'See how it works'*. The illustration sits right, deliberately off the vertical centre line so the composition reads as designed rather than templated.

```js
batch_design({
  documentId: "doc",
  ops: [
    { op: "C", parent: "doc", node: { type: "frame", name: "Marketing_Hero", layout: { direction: "row", justify: "between", align: "center", gap: 80 }, size: { width: 1440, height: 720, padding: { x: 120, y: 96 } }, fill: "$bg" } },
    { op: "C", parent: "Marketing_Hero", node: { type: "frame", name: "HeroCopy", layout: { direction: "column", gap: 24 }, size: { width: 560 } } },
    { op: "C", parent: "HeroCopy", node: { type: "text", name: "Eyebrow", text: "For engineering teams", fontFamily: "$fontMono", fontSize: 14, color: "$accent" } },
    { op: "C", parent: "HeroCopy", node: { type: "text", name: "Title", text: "Cut your build time by 40%.", fontFamily: "$fontDisplay", fontSize: 64, fontWeight: "$fontWeightBold", letterSpacing: -0.02, color: "$textPrimary" } },
    { op: "C", parent: "HeroCopy", node: { type: "text", name: "Sub", text: "We cache every step, parallelise across machines, and never rebuild what hasn't changed.", fontSize: 18, color: "$textSecondary" } },
    { op: "C", parent: "HeroCopy", node: { type: "frame", name: "HeroActions", layout: { direction: "row", gap: 16, align: "center" } } },
    { op: "C", parent: "HeroActions", node: { type: "ref", ref: "Button_Primary", descendants: { label: { text: "Start your free trial" } } } },
    { op: "C", parent: "HeroActions", node: { type: "ref", ref: "Link_Text", descendants: { label: { text: "See how it works" } } } },
    { op: "C", parent: "Marketing_Hero", node: { type: "frame", name: "HeroIllustration", size: { width: 560, height: 480 }, fill: "$surfaceElevated", cornerRadius: 16 } },
  ],
});
```

**In Pencil:** the hero is one flex row, copy left, illustration right. The off-centre feel comes from the 560-pixel copy column not being centred in the 1440-pixel frame; it sits left of the optical midline, which reads as intentional.

## Step 5: build the features section (bento)

Two candidate shapes per `layout-patterns.md` § Feature sections:

- **Alternating image-text rows.** Image-left + text-right for feature 1, mirrored for feature 2, mirrored again for feature 3. Each row is its own sub-frame inside `Marketing_Features`. Reads editorial.
- **Bento grid.** One large tile (the headline feature) plus 4-6 smaller tiles in asymmetric layout. Reads modern and product-led without being precious about it.

Pick **Bento** for visual impact. The headline feature gets the largest tile; supporting features fan out asymmetrically.

```js
batch_design({
  documentId: "doc",
  ops: [
    { op: "C", parent: "doc", node: { type: "frame", name: "Marketing_Features", layout: { direction: "column", gap: 48 }, size: { width: 1440, padding: { x: 120, y: 120 } }, fill: "$bg" } },
    { op: "C", parent: "Marketing_Features", node: { type: "text", name: "SectionTitle", text: "Everything your CI lacks.", fontSize: 48, fontWeight: "$fontWeightBold", color: "$textPrimary" } },
    { op: "C", parent: "Marketing_Features", node: { type: "frame", name: "BentoGrid", layout: { direction: "row", wrap: true, gap: 24 }, size: { width: 1200 } } },
    { op: "C", parent: "BentoGrid", node: { type: "frame", name: "Tile_Headline", size: { width: 780, height: 420, padding: 40 }, fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "BentoGrid", node: { type: "frame", name: "Tile_Cache", size: { width: 396, height: 198, padding: 32 }, fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "BentoGrid", node: { type: "frame", name: "Tile_Parallel", size: { width: 396, height: 198, padding: 32 }, fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "BentoGrid", node: { type: "frame", name: "Tile_Insights", size: { width: 588, height: 240, padding: 32 }, fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "BentoGrid", node: { type: "frame", name: "Tile_Selfhost", size: { width: 588, height: 240, padding: 32 }, fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } } },
  ],
});
```

**In Pencil:** the bento grid is asymmetric on purpose. The large tile anchors the eye; smaller tiles compose around it. Apple's iPhone product pages popularised the pattern, and Linear's feature pages adopted it.

## Step 6: build the pricing section

Three-tier (Free / Pro / Team) with **Pro** highlighted, per `references/layout-patterns.md` § Pricing tables. The catch most agents miss: highlighting a tier with five competing treatments (coloured border + shadow + scale-up + badge + different background) is louder than the rest of the page combined. Pick two: a coloured border using `$accent` plus a 'Most popular' badge. That's plenty.

```js
batch_design({
  documentId: "doc",
  ops: [
    { op: "C", parent: "doc", node: { type: "frame", name: "Marketing_Pricing", layout: { direction: "column", align: "center", gap: 48 }, size: { width: 1440, padding: { x: 120, y: 120 } }, fill: "$surface" } },
    { op: "C", parent: "Marketing_Pricing", node: { type: "text", name: "SectionTitle", text: "Pricing that scales with your team.", fontSize: 48, fontWeight: "$fontWeightBold", color: "$textPrimary" } },
    { op: "C", parent: "Marketing_Pricing", node: { type: "frame", name: "PricingRow", layout: { direction: "row", gap: 24, align: "stretch" } } },
    { op: "C", parent: "PricingRow", node: { type: "frame", name: "Tier_Free", size: { width: 360, padding: 32 }, fill: "$bg", cornerRadius: 16, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "PricingRow", node: { type: "frame", name: "Tier_Pro", size: { width: 360, padding: 32 }, fill: "$bg", cornerRadius: 16, stroke: { thickness: 2, color: "$accent" }, context: "Highlighted tier. Coloured accent border + 'Most popular' badge. No scale-up, no extra shadow; the border + badge is enough." } },
    { op: "C", parent: "Tier_Pro", node: { type: "frame", name: "PopularBadge", layout: { direction: "row", align: "center" }, size: { padding: { x: 12, y: 4 } }, fill: "$accent", cornerRadius: 999 } },
    { op: "C", parent: "PopularBadge", node: { type: "text", text: "Most popular", fontSize: 12, fontWeight: "$fontWeightMedium", color: "$bg" } },
    { op: "C", parent: "PricingRow", node: { type: "frame", name: "Tier_Team", size: { width: 360, padding: 32 }, fill: "$bg", cornerRadius: 16, stroke: { thickness: 1, color: "$border" } } },
  ],
});
```

**In Pencil:** the highlighted Pro tier reads as the recommended pick without screaming. Stripe and Linear both use the same restraint on their pricing pages; the brief's *'don't look like every other SaaS'* is satisfied by skipping the pile-on.

## Step 7: build the testimonials section

Don't auto-rotate. An auto-rotating carousel hides 80% of the content behind a timer the user didn't ask for, and it's an accessibility headache. Use a static avatar grid (4 quotes); each tile holds an avatar paired with the person's name and short quote, captioned by their role at company.

```js
batch_design({
  documentId: "doc",
  ops: [
    { op: "C", parent: "doc", node: { type: "frame", name: "Marketing_Testimonials", layout: { direction: "column", gap: 48 }, size: { width: 1440, padding: { x: 120, y: 120 } }, fill: "$bg" } },
    { op: "C", parent: "Marketing_Testimonials", node: { type: "text", name: "SectionTitle", text: "Teams that ship faster with us.", fontSize: 48, fontWeight: "$fontWeightBold", color: "$textPrimary" } },
    { op: "C", parent: "Marketing_Testimonials", node: { type: "frame", name: "QuoteGrid", layout: { direction: "row", wrap: true, gap: 24 }, size: { width: 1200 } } },
    { op: "C", parent: "QuoteGrid", node: { type: "frame", name: "Quote_1", size: { width: 588, padding: 32 }, fill: "$surface", cornerRadius: 16, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "QuoteGrid", node: { type: "frame", name: "Quote_2", size: { width: 588, padding: 32 }, fill: "$surface", cornerRadius: 16, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "QuoteGrid", node: { type: "frame", name: "Quote_3", size: { width: 588, padding: 32 }, fill: "$surface", cornerRadius: 16, stroke: { thickness: 1, color: "$border" } } },
    { op: "C", parent: "QuoteGrid", node: { type: "frame", name: "Quote_4", size: { width: 588, padding: 32 }, fill: "$surface", cornerRadius: 16, stroke: { thickness: 1, color: "$border" } } },
  ],
});
```

**In Pencil:** four static tiles in a 2x2 grid. Keyboard-accessible by default, no JavaScript timer, every quote visible at once.

## Step 8: build the closing CTA

A second CTA at the bottom of the page restates the offer for users who scrolled past the hero without converting. Use different copy from the hero so the page doesn't feel repetitive: hero said *'Start your free trial'*; closing says *'Try Forge free for 14 days'*. Pair with a secondary *'Contact sales'* link for enterprise leads.

```js
batch_design({
  documentId: "doc",
  ops: [
    { op: "C", parent: "doc", node: { type: "frame", name: "Marketing_CTA_Closing", layout: { direction: "column", align: "center", gap: 24 }, size: { width: 1440, padding: { x: 120, y: 120 } }, fill: "$surfaceElevated" } },
    { op: "C", parent: "Marketing_CTA_Closing", node: { type: "text", text: "Ready to ship faster?", fontSize: 56, fontWeight: "$fontWeightBold", color: "$textPrimary" } },
    { op: "C", parent: "Marketing_CTA_Closing", node: { type: "frame", name: "ClosingActions", layout: { direction: "row", gap: 16, align: "center" } } },
    { op: "C", parent: "ClosingActions", node: { type: "ref", ref: "Button_Primary", descendants: { label: { text: "Try Forge free for 14 days" } } } },
    { op: "C", parent: "ClosingActions", node: { type: "ref", ref: "Link_Text", descendants: { label: { text: "Contact sales" } } } },
  ],
});
```

## Step 9: build the footer

Per `references/layout-patterns.md` § Footer architectures, pick one shape and stick to it. A 4-column sitemap (Product, Company, Resources, Legal) is the right pick for a SaaS that ships feature pages alongside a blog and a changelog. Don't cram a newsletter signup into the same footer; that's a different architecture.

```js
batch_design({
  documentId: "doc",
  ops: [
    { op: "C", parent: "doc", node: { type: "frame", name: "Marketing_Footer", layout: { direction: "column", gap: 48 }, size: { width: 1440, padding: { x: 120, y: 80 } }, fill: "$bg" } },
    { op: "C", parent: "Marketing_Footer", node: { type: "frame", name: "Sitemap", layout: { direction: "row", justify: "between", gap: 64 } } },
    { op: "C", parent: "Sitemap", node: { type: "frame", name: "Col_Product", layout: { direction: "column", gap: 12 } } },
    { op: "C", parent: "Sitemap", node: { type: "frame", name: "Col_Company", layout: { direction: "column", gap: 12 } } },
    { op: "C", parent: "Sitemap", node: { type: "frame", name: "Col_Resources", layout: { direction: "column", gap: 12 } } },
    { op: "C", parent: "Sitemap", node: { type: "frame", name: "Col_Legal", layout: { direction: "column", gap: 12 } } },
    { op: "C", parent: "Marketing_Footer", node: { type: "rectangle", name: "FooterDivider", size: { width: 1200, height: 1 }, fill: "$border" } },
    { op: "C", parent: "Marketing_Footer", node: { type: "text", text: "© 2026 Forge Labs. All rights reserved.", fontSize: 14, color: "$textMuted" } },
  ],
});
```

Each column gets 4-6 links populated through children of `Col_Product`, `Col_Company`, etc. Skipped here for brevity; the pattern is one column heading text node plus link text nodes.

## Step 10: microcopy pass

Per `references/microcopy.md` § Headlines, every section headline should be verb-led and benefit-focused with a specific number wherever the product can back one. Run a real-content pass:

- Hero: *'Cut your build time by 40%.'* beats *'Faster builds.'*
- Features: *'Everything your CI lacks.'* beats *'Our features.'*
- Pricing: *'Pricing that scales with your team.'* beats *'Pricing.'*
- Testimonials: *'Teams that ship faster with us.'* beats *'What our customers say.'*
- Closing CTA: *'Ready to ship faster?'* beats *'Get started today.'*

The CTAs themselves get the same treatment per `references/microcopy.md` § Buttons / CTAs: *'Start your free trial'* and *'Try Forge free for 14 days'* are specific verbs with the offer baked in. *'See how it works'* and *'Contact sales'* describe what happens after the click.

## Step 11: verify

One screenshot per section. Six screenshots total, since each section is its own top-level frame.

```js
get_screenshot({ documentId: "doc", nodeId: "Marketing_Hero" });
get_screenshot({ documentId: "doc", nodeId: "Marketing_Features" });
get_screenshot({ documentId: "doc", nodeId: "Marketing_Pricing" });
get_screenshot({ documentId: "doc", nodeId: "Marketing_Testimonials" });
get_screenshot({ documentId: "doc", nodeId: "Marketing_CTA_Closing" });
get_screenshot({ documentId: "doc", nodeId: "Marketing_Footer" });
```

Confirm:

- Asymmetric hero reads as a deliberate composition. The illustration sits right; the copy column anchors left.
- The features section is a bento grid. No three-card grid anywhere.
- The Pro pricing tier has one accent border plus the badge. No scale-up, no extra shadow.
- Testimonials are static, four tiles in a 2x2 grid, keyboard-accessible.
- The footer is a 4-column sitemap with no newsletter form fighting it.
- Every section headline is verb-led and specific.

If anything's off, fix structurally and re-screenshot only the affected section.

## Final report to user

> *"Done. Marketing page with six sibling sections: asymmetric hero (off-centre title, primary CTA + 'See how it works' link), bento-grid features (one headline tile + four supporting tiles), three-tier pricing (Pro highlighted with accent border + 'Most popular' badge), 2x2 static testimonial grid, closing CTA with restated offer, and a 4-column sitemap footer. No three-card feature grid; no auto-rotating carousel. Microcopy is verb-led: 'Cut your build time by 40%' in the hero, 'Try Forge free for 14 days' in the closing CTA. All bound to your tokens.md variables."*

## What this example demonstrates

- **Defaults rejected on purpose.** The three-card grid and the kitchen-sink footer both got skipped because `references/layout-patterns.md` flagged them as the most over-used SaaS shapes.
- **Each section is its own top-level frame**, named with the `Marketing_` prefix per `references/file-architecture.md` § Section frames as canvas regions.
- **Restraint in highlighted treatments.** The Pro pricing tier uses two cues (accent border + badge); piling on five would scream louder than the rest of the page combined. Stripe and Vercel pricing pages take the same approach.
- **Static over auto-rotating.** Testimonials are visible all at once; no JavaScript timer hiding content.
- **Microcopy pass at the end.** Each section's headline gets a real-content edit so the page doesn't read as scaffolded.

## See also

- `references/layout-patterns.md` § Hero variations, § Feature sections, § Pricing tables, § Footer architectures.
- `references/file-architecture.md` § Section frames as canvas regions.
- `references/microcopy.md` § Headlines, § Buttons / CTAs.
- `assets/examples/example-style-selection.md`: how the tokens this example references got committed in the first place.
