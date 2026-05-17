# Marketing landing page

Before any ops, a few pickups so the page reads intentional rather than templated.

## What I read first

- `SKILL.md` for the default workflow, the Aesthetic defaults block (especially the "name the atmosphere before you plan" rule and the AI-tells list), and the Failure-modes table.
- `references/layout-patterns.md` because the brief names five marketing archetypes (hero, features, pricing, testimonials, footer). The load-bearing rule is in the Feature sections section: the three-equal-card grid is "the most over-used layout pattern in SaaS marketing. It's a tell." That single sentence reframes the whole brief.
- `assets/examples/example-marketing-page.md` because it is a near-identical brief — same five blocks, same "don't look like every other SaaS" instruction. I am not copying it verbatim (its product is a CI tool, ours is unspecified), but its picks teach the discipline: asymmetric hero, bento features, two-treatment pricing, static testimonials, single-architecture footer.
- `assets/examples/example-pricing-table.md` for the highlighted-tier discipline: pick two of {coloured border, badge, shadow, scale-up}, never four.
- `references/microcopy.md` for verb-led headlines and action-specific CTAs (no "Continue", no "Get started" as a first-party action).
- `references/iteration-patterns.md` for the four-question self-critique gate I will run before reporting done.
- `references/industry-patterns.md` § SaaS for the family-level conventions, plus § Website pressure test because a marketing landing page is a website surface, not a product surface — different completeness checklist.

## Step 1: detect host

```
mcp__pencil__get_editor_state({ include_schema: false })
```

Expected response shape: a JSON object naming the active document (filePath, documentId, schema version), the current selection, and the document's themes/imports. If it errors with `transport not connected to app: desktop`, I stop and tell you to open the Pencil desktop app or the IDE extension. I do not silently fall back to the CLI.

If no document is open, I would ask whether to `open_document('new')` for a fresh `.pen` or open an existing path.

## Step 2: locate context

From the `get_editor_state` response, three things matter:

- Whether a `.pen` is open and what it currently holds (any existing top-level frames I would have to avoid colliding with).
- The document's `imports` field — is there a `.lib.pen` already attached? If so, its components are mine to use.
- Whether the project has a `design-system/` folder. I would `ls` the project root for it.

Three branches at this point:

- **No `design-system/` and the brief is real product work.** I offer once to scaffold the 12 core templates plus `brand.md` and `imagery.md` (both relevant to a marketing surface). On no, I proceed without and do not ask again this session.
- **`design-system/` exists.** I read `README.md`, then `design-system.md` (for the `.lib.pen` path, tech stack, icon library), `tokens.md`, `voice.md` (marketing copy lives or dies on voice), `patterns.md` if the project has documented its preferred marketing layouts, and `brand.md` if present.
- **`design-system/` exists but is a code module** (`.tsx`, `package.json` inside). I do not overwrite. I ask where the docs go instead.

Without knowing your answer I will assume a populated `design-system/` and reference its tokens by name in the plan below. If the project is greenfield I would also load `references/style-catalogue.md`, `references/colour-palettes.md`, and `references/font-pairings.md` to commit to a visual direction before drawing.

## Step 3: load guidelines + inventory components

```
mcp__pencil__get_guidelines({})
```

Expected: a list of categories the server reports for this document. For a marketing landing page I read the `Landing Page` category if present, plus `Web App` for general web conventions and `Tailwind` if the project's stack is Tailwind (check `design-system.md`).

Then the components-first inventory — both halves of the check:

```
mcp__pencil__batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Expected response: an array of component-shaped nodes from the open `.pen`, each with `id`, `name`, `reusable: true`, and a shallow shape. I am scanning for: `Button_Primary`, `Button_Secondary`, `Link_Text`, `Card`, `Badge`, `LogoMark`, anything pricing-shaped (`Card_Pricing`, `Card_Pricing_Highlighted`), anything testimonial-shaped (`TestimonialCard`, `Avatar`), and footer atoms (`FooterColumn`, `FooterLink`).

Then for each `.lib.pen` listed in the document's `imports`:

```
mcp__pencil__batch_get({
  filePath: "./design/system.lib.pen",
  patterns: [{ reusable: true }],
  readDepth: 2
})
```

Same scan, library scope. If I find a `Card_Pricing_Highlighted` here I use it; I do not rebuild a highlighted tier from primitives.

For any unfamiliar component I plan to use, I deep-read first per `references/component-anatomy.md`:

```
mcp__pencil__batch_get({ nodeIds: ["Card_Pricing_Highlighted"], readDepth: 4 })
```

I look for slot frames (the content holes I fill via `descendants`), the named-child paths (so I can address `header/title` not just `title`), and any component states I will need (default / hover / focus). If a child sits at path `a → b → c`, the `descendants` key is `"a/b/c"`.

If the inventory is empty (greenfield `.pen` with no library), I would surface that to you and offer to either build minimum atoms inline or scaffold a `.lib.pen` first. I would not silently rebuild the same Button five times across five sections.

## Step 4: name the atmosphere, then plan

Per the Aesthetic defaults rule, I commit to one line before any `batch_design` call. Without a brand brief from you I will pick a defensible default for SaaS marketing that does not read templated:

> **Airy, offset, fluid.** One accent on a near-neutral page. Asymmetric hero. Bento features. Pricing restraint. Static testimonials. Sitemap footer.

If your brand voice is louder (consumer SaaS, dev tools with personality), I would shift to **Dense, offset, fluid** or **Balanced, offset, cinematic** and document the choice on the Cover frame. If it is more conservative (fintech, healthcare-adjacent), **Airy, symmetric, static** is safer.

### Page structure (six sibling top-level frames)

Per `references/file-architecture.md` § Section frames as canvas regions, each section is its own top-level frame in the `SourceOfTruth` region of the canvas:

1. `Marketing_Hero` — asymmetric, off-centre title left, illustration or product surface right.
2. `Marketing_Features` — **bento grid**, not a three-card grid. One headline tile + supporting tiles in asymmetric sizing.
3. `Marketing_Pricing` — three-tier (Free / Pro / Team), Pro highlighted with **two** treatments only: coloured border + "Most popular" badge.
4. `Marketing_Testimonials` — **static** avatar grid (4 quotes in a 2×2 layout). Not a carousel.
5. `Marketing_CTA_Closing` — restated offer with different copy from the hero.
6. `Marketing_Footer` — 4-column sitemap (Product / Company / Resources / Legal). Not a kitchen-sink footer.

Before placing the first frame on a populated canvas, I would call `mcp__pencil__find_empty_space_on_canvas({ width: 1440, height: 5000 })` to get a coordinate that does not overlap existing top-level frames. The expected response is `{ x, y }` in canvas units; I pass that as the `x`/`y` on `Marketing_Hero` and stack the rest below it.

### Theme handling

```
mcp__pencil__get_variables({})
```

Expected: the existing token map. I do not call `set_variables` until I know what is already declared. If the document has `$bg`, `$surface`, `$surfaceElevated`, `$textPrimary`, `$textSecondary`, `$textMuted`, `$border`, `$accent`, `$fontDisplay`, `$fontBody`, `$fontMono`, `$fontWeightBold`, `$fontWeightMedium`, `$maxContent`, I bind to those. If the `mode` axis is not declared (`get_editor_state` shows no `themes`), I add it with one `U("doc", { themes: { mode: ["light","dark"] } })` op before the first colour binding. I do **not** redeclare any variable that already exists — that silently clobbers your tokens (Failure mode #7 in the skill).

## Step 5: execute

A marketing page at this density is roughly 70–90 ops total. I split into four `batch_design` calls so each stays under 25 ops and ordering bugs stay local:

- **Call A:** create the six top-level frames as siblings, set their `name`, `context`, fill, padding, and stacking gaps. This anchors structure first.
- **Call B:** populate Hero + Features (the visually load-bearing half).
- **Call C:** populate Pricing + Testimonials.
- **Call D:** populate Closing CTA + Footer.

Per the Discipline rules, every op carries `name` and (for non-trivial nodes) `context`. Colours come from `$variables`, never raw hex. Sizing uses bare strings: `width: "fill_container"`, `width: "fit_content"`, `width: 1440`. No `"100%"`, no `{ sizing: ... }` object form (the live server rejects it). IDs contain no `/`.

### Call A: section scaffolding

Conceptually:

```
hero=I("doc", { type: "frame", name: "Marketing_Hero",
  context: "Above-the-fold value prop. Asymmetric: title block sits left of optical centre, product surface right. Primary CTA is the only filled button on the page until the closing CTA.",
  size: { width: 1440, height: 720, padding: { x: 120, y: 96 } },
  layout: { direction: "row", justify: "between", align: "center", gap: 80 },
  fill: "$bg",
  x: <find_empty_space.x>, y: <find_empty_space.y>
})
features=I("doc", { type: "frame", name: "Marketing_Features", ... })
pricing=I("doc", { type: "frame", name: "Marketing_Pricing", ... fill: "$surface" })
testimonials=I("doc", { type: "frame", name: "Marketing_Testimonials", ... })
closingCta=I("doc", { type: "frame", name: "Marketing_CTA_Closing", ... fill: "$surfaceElevated" })
footer=I("doc", { type: "frame", name: "Marketing_Footer", ... })
```

Alternating fills (`$bg` → `$bg` → `$surface` → `$bg` → `$surfaceElevated` → `$bg`) give the page a quiet rhythm without competing colour. The eye gets a horizon line at every section change without me reaching for an accent.

### Call B: Hero + Features

**Hero.** The asymmetric move is the 560-pixel copy column sitting in a 1440-pixel frame with `justify: between` — the copy anchors left of optical centre, the visual sits right, and there is intentional negative space around both. That asymmetry is the entire point; a centred 800-pixel hero in the same frame would read as a 2018 SaaS template.

```
copy=I(hero, { type: "frame", name: "HeroCopy", layout: { direction: "column", gap: 24 }, size: { width: 560 } })
I(copy, { type: "text", name: "Eyebrow", text: "<one-line audience cue>",
  fontFamily: "$fontMono", fontSize: 14, color: "$accent",
  context: "Audience signal — names who this is for. Mono type signals product/dev focus." })
I(copy, { type: "text", name: "Title", text: "<verb-led benefit headline>",
  fontFamily: "$fontDisplay", fontSize: 64, fontWeight: "$fontWeightBold",
  letterSpacing: -0.02, color: "$textPrimary",
  context: "Hero headline. Verb-led, benefit-focused, specific. text-wrap: balance to avoid orphan words." })
I(copy, { type: "text", name: "Sub", text: "<one-sentence supporting paragraph>",
  fontSize: 18, color: "$textSecondary" })
actions=I(copy, { type: "frame", name: "HeroActions", layout: { direction: "row", gap: 16, align: "center" } })
I(actions, { type: "ref", ref: "Button_Primary",
  descendants: { "label": { text: "<action-specific verb + noun>" } },
  context: "Primary above-the-fold CTA. Filled accent. Only filled button on this section." })
I(actions, { type: "ref", ref: "Link_Text",
  descendants: { "label": { text: "See how it works" } } })
visual=I(hero, { type: "frame", name: "HeroVisual",
  size: { width: 600, height: 480 }, fill: "$surfaceElevated", cornerRadius: 16,
  context: "Product surface or illustration. Real screenshot when available; AI-generated otherwise." })
G(visual, "ai", "<context-appropriate prompt grounded in your product>")
```

I do not name a fake company or fabricate a metric. The placeholders above (`<verb-led benefit headline>`, `<one-line audience cue>`) get filled with real copy if you give me product context; otherwise I would surface that as a question before declaring done, not invent it. The skill bans placeholder names like `Acme`, `Nexus`, `Lorem Ipsum` in shipped designs.

**Features as bento, not three-card grid.** This is the load-bearing rejection of the templated default. One large headline tile (780×420) carries the headline feature. Four smaller tiles fan around it: two compact (396×198) and two medium (588×240). Sizes are deliberately uneven; a six-tile grid where every tile is the same size is just a three-card grid in disguise.

```
I(features, { type: "text", name: "FeaturesTitle", text: "<verb-led section headline>",
  fontFamily: "$fontDisplay", fontSize: 48, fontWeight: "$fontWeightBold",
  color: "$textPrimary" })
bento=I(features, { type: "frame", name: "BentoGrid",
  layout: { direction: "row", wrap: true, gap: 24 }, size: { width: 1200 } })
I(bento, { type: "frame", name: "Tile_Headline",
  size: { width: 780, height: 420, padding: 40 },
  fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" },
  context: "Headline feature tile. Largest in the grid. Holds the most important capability + a product visual or screenshot." })
I(bento, { type: "frame", name: "Tile_FeatureA",
  size: { width: 396, height: 198, padding: 32 },
  fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } })
I(bento, { type: "frame", name: "Tile_FeatureB",
  size: { width: 396, height: 198, padding: 32 },
  fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } })
I(bento, { type: "frame", name: "Tile_FeatureC",
  size: { width: 588, height: 240, padding: 32 },
  fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } })
I(bento, { type: "frame", name: "Tile_FeatureD",
  size: { width: 588, height: 240, padding: 32 },
  fill: "$surface", cornerRadius: 20, stroke: { thickness: 1, color: "$border" } })
```

Each tile gets its own headline (~24px), one-sentence description (~16px, `$textSecondary`), and an inline visual cue (icon at the top-left, or a small product surface at the bottom). The tile content sits inside a column auto-layout with `gap: 16`. Note the brief said "three feature blocks" — the bento composes around a headline tile + four supporting tiles which gives me five total. I would either consolidate to one headline + three supporting tiles (still bento, still asymmetric, technically three "blocks" in the visual count) **or** confirm with you whether five tiles is fine. I would not silently ship five when you asked for three; I would surface the trade-off in the report.

The corner-radius rule from `SKILL.md` § Shadows & elevation applies inside the tiles: any inner card or input gets a smaller radius than its tile parent (`r - p` where `p` is the padding). With 20px tiles and 32px padding the inner content is unbounded; with a 12px nested card inside a 20px tile, the inner needs `≤ 8px` to read intentional.

### Call C: Pricing + Testimonials

**Pricing.** Three tiers, Pro highlighted with **two** treatments — coloured border using `$accent` (2px) plus a "Most popular" badge. I do not also add scale-up, layered shadow, and a different background. The example walkthrough makes this explicit: piling on five treatments screams louder than the rest of the page combined.

If the library has `Card_Pricing` and `Card_Pricing_Highlighted`, I instantiate via `ref` and override per-instance via `descendants`:

```
row=I(pricing, { type: "frame", name: "PricingRow",
  layout: { direction: "row", gap: 24, align: "stretch" } })
I(row, { type: "ref", ref: "Card_Pricing",
  descendants: {
    "tier": { text: "Free" },
    "price": { text: "$0" },
    "period": { text: "forever" },
    "description": { text: "For trying things out." },
    "ctaLabel": { text: "Start free" }
  }})
I(row, { type: "ref", ref: "Card_Pricing_Highlighted",
  descendants: {
    "tier": { text: "Pro" },
    "price": { text: "$<X>" },
    "period": { text: "per user / month" },
    "badge": { text: "Most popular" },
    "ctaLabel": { text: "Start Pro trial" }
  },
  context: "Highlighted tier. Border + badge only — not also scale-up + layered shadow + different fill." })
I(row, { type: "ref", ref: "Card_Pricing",
  descendants: {
    "tier": { text: "Team" },
    "price": { text: "Custom" },
    "period": { text: "" },
    "description": { text: "For teams that need scale." },
    "ctaLabel": { text: "Contact sales" }
  }})
```

Numbers use `font-variant-numeric: tabular-nums` so prices align by column — noted in the component's `context` so the engineer ships the CSS. CTA labels are action-specific per `references/microcopy.md` § Buttons / CTAs: `Start free`, `Start Pro trial`, `Contact sales`. None of `Get started`, `Continue`, `Submit`.

If the library does **not** have pricing components, I build them inline as one-off frames in this `.pen` and surface the gap in my report: *"Pricing cards built inline; this pattern is reusable — should I extract `Card_Pricing` and `Card_Pricing_Highlighted` to your `.lib.pen`?"*

**Testimonials as static avatar grid, not carousel.** Per `references/layout-patterns.md` § Testimonials, the auto-rotating carousel is an accessibility tax: it hides 80% of the content behind a timer the user did not ask for, and breaks for keyboard users. Four quotes in a 2×2 grid; every quote visible at once.

```
I(testimonials, { type: "text", name: "TestimonialsTitle",
  text: "<benefit-led headline naming who ships with us>",
  fontFamily: "$fontDisplay", fontSize: 48, fontWeight: "$fontWeightBold" })
grid=I(testimonials, { type: "frame", name: "QuoteGrid",
  layout: { direction: "row", wrap: true, gap: 24 }, size: { width: 1200 } })
// Four Quote tiles, each 588×~200, $surface fill, $border stroke, 1px
// Each tile: avatar 48px, name (16px bold), role @ company (14px muted), quote (18px)
```

Each quote uses real-feeling content (names, roles, companies) once I know your customer references. If I do not have real testimonials I name that as a content gap rather than fabricate quotes from `John Doe at Acme` — that is one of the AI tells the skill bans.

### Call D: Closing CTA + Footer

**Closing CTA** restates the offer for users who scrolled past the hero. Different copy from the hero so the page does not feel repetitive: hero says `Start your free trial`, closing says e.g. `Try <product> free for 14 days`. Pair with a secondary `Contact sales` text link for enterprise leads. Background is `$surfaceElevated` so the section reads as a subtle terminus, not a duplicate of the hero.

**Footer.** Per `references/layout-patterns.md` § Footer architectures, I pick **one** shape and stick to it. For a SaaS with a docs/blog/changelog ecosystem, the 4-column sitemap (Product / Company / Resources / Legal) is the right shape. I do **not** also cram a newsletter form, a social rail, and a contact form in. Each column gets 4–6 link text nodes; the columns share a horizontal `justify: between`, the wordmark sits top-left, and a thin divider plus the copyright closes the page.

If your project ships a newsletter and you want it on the marketing page, it should be its own section above the footer (its own top-level frame, `Marketing_Newsletter`), not a sub-region of the footer. I would surface that as an option in the report rather than guess.

## Step 6: verify (structural-first)

Per `SKILL.md` § Verification ladder, I do **not** screenshot every section as I build. The reflex from older versions of this skill is wrong; structural snapshots prove most of what a screenshot would.

1. **Rung 1 (free):** every `batch_design` call returns success. If a call errors with a schema error, I read it verbatim, cross-reference `references/batch-design-grammar.md` and `references/pen-schema.md`, and fix specifically. Common causes I would check first: id contains `/` (forbidden), `width: "100%"` instead of `"fill_container"`, raw hex where a `$variable` was expected, `stroke.fills` plural instead of singular.

2. **Rung 2 (cheap):** after Call A, `mcp__pencil__snapshot_layout({ nodeId: "doc", maxDepth: 1 })` to confirm all six top-level frames landed at non-overlapping coordinates with the expected widths. After Call B, `snapshot_layout({ nodeId: hero, maxDepth: 3 })` to confirm the hero's row split (560 + 600 with 80px gap and 80px residual asymmetry inside a 1440 frame). After Call C, `snapshot_layout({ nodeId: pricing, maxDepth: 2 })` to confirm three columns of equal stretch.

3. **Rung 3 (cheap):** `mcp__pencil__batch_get({ nodeIds: [primaryCtaButtonId, highlightedTierId, headlineTileId], readDepth: 2 })` to confirm property-level intent: the primary CTA's fill resolved to `$accent` (not raw hex), the highlighted tier carries the accent border *and* the badge (not a third treatment), the headline tile has the larger size.

4. **Rung 4 (expensive — once):** one final `mcp__pencil__get_screenshot({ nodeId: "doc" })` scoped to the page subtree (or per-section if the page is too tall to render usefully at one zoom). I am looking for: layout integrity (nothing off-canvas, nothing overlapping), spacing rhythm (gaps match `tokens.md`), type rhythm (heading sizes step in declared order), contrast (body text passes WCAG AA against its background), component fidelity (no hand-built buttons drifting from the library style).

The skill's dual-mode rule applies: I screenshot the primary mode only. I do **not** routinely re-screenshot the dark mode "to confirm both hold up" — the variable system guarantees that if I only used `$variables` for colour. I would re-screenshot dark only if a structural snapshot showed a raw hex slipped in somewhere.

Total expensive verification: **one screenshot.** Not six.

### The four-question self-critique gate (60 seconds before reporting)

Per `references/iteration-patterns.md` § The four-question self-critique gate, run before declaring done:

1. **Could a non-designer recognise this as your brand's voice or industry?** If the page could belong to any SaaS, I have not committed hard enough to the atmosphere I named in step 4. Pick one direction and lean.
2. **Where does the eye go first / second / third?** Squint at the page. The eye should land on the hero headline, then the primary CTA, then the section cadence. If the eye lands on a decorative element first, demote it.
3. **What's decorative-only that doesn't communicate meaning?** Borders that don't carry information, badges that don't mark a state, gradients that don't direct attention. Cut them.
4. **What single change would make this feel less AI-generated?** Honest answers: a custom illustration in the hero instead of a stock product shot; a typography choice with more personality (Geist over Inter, Cabinet Grotesk for display); an asymmetric crop on the hero visual; replacing the placeholder microcopy with one specific real metric.

Fix what surfaces. Do not note the four questions as a TODO.

## What I would deliberately not do

- **Three-equal-card feature grid.** The single most over-used SaaS marketing pattern. Reaching for it would fail the brief on first contact.
- **Centred-text-and-CTA hero.** The default. Asymmetric reads as designed; centred reads as a 2018 template.
- **Auto-rotating testimonial carousel.** Accessibility tax, hides content. Static avatar grid every time.
- **Pile-on highlighted pricing tier** (border + shadow + scale + badge + different fill). Two treatments only.
- **Kitchen-sink footer** with sitemap + newsletter form + social rail + contact form. Pick one architecture.
- **Pure `#000000` / `#FFFFFF`** bound directly. Use `$bg` / `$surface` / `$textPrimary` resolving to off-black and off-white.
- **`Inter` as the display font.** It is the AI signature. For a SaaS I would default to Geist + Geist Mono or Söhne + Söhne Mono; for editorial-leaning brands, Cabinet Grotesk paired with Inter for body is OK because the display work happens elsewhere.
- **Filler hero copy** like "Scroll to explore" or animated chevrons.
- **Fabricated metrics** ("Trusted by 10,000+ teams") or placeholder names (`Acme`, `John Doe`, `Lorem Ipsum`). I would surface the content gap rather than invent.
- **AI copy clichés**: "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize", "Empower". Strike on sight.

## Two things I would surface to you

These are explicit follow-ups, not silent decisions:

1. **Five tiles vs three blocks.** You asked for three feature blocks; the bento layout naturally composes around a headline tile + supporting tiles, which makes five. I would either consolidate to one headline tile + three supporting (technically more than three "blocks" but visually three supporting beats), or confirm five is fine. Do not want to silently re-spec the brief.
2. **Real content needed.** Headlines, customer testimonials, pricing numbers, and the hero visual all need real content to avoid the placeholder/fabricated-metric AI tell. I would either ask you for them or ship the page with `<bracketed placeholders>` and a note in the report so you can paste real copy in. I would not invent.

## What I would report when done

> "Done. Marketing landing page laid out as six sibling top-level frames in the Source of Truth region: asymmetric hero, bento features (one headline tile + four supporting tiles in 780/396/588 widths), three-tier pricing with Pro highlighted by an accent border + 'Most popular' badge (no extra shadow or scale-up), a static 2×2 testimonial grid (no carousel), a closing CTA with restated offer, and a 4-column sitemap footer. Every node carries a `name` and a `context`; every colour binds to a `$variable`; sizing uses bare-string `fill_container` and explicit pixel widths at 1440 desktop. The page passes the four-question self-critique gate. Two follow-ups: bento composes around five tiles rather than three (confirm or I'll consolidate), and the headlines / testimonials / hero visual are placeholders pending your real content. Tablet and mobile breakpoints not built — flag if you want sibling `_Tablet` and `_Mobile` frames, or a single fluid frame instead."

## Out of scope I would name

The Website pressure test in `references/industry-patterns.md` § Completeness pressure tests reads:

> *If the file does not show mobile navigation, forms, validation, cookie/consent states, SEO heading structure and CMS template behaviour, it is not comprehensive. It is a brochure mock-up.*

A landing page in isolation is not the full website. I would not silently expand scope, but I would name the gap so you know what is and is not designed: tablet + mobile breakpoints (hamburger nav, single-column stack), 404 / 500 / offline pages, a cookie/consent banner, the form states for whatever lead-capture lives on this page (signup, contact, demo request), and the wider site templates (blog index, article, author page) if you have them. Each is its own follow-up.
