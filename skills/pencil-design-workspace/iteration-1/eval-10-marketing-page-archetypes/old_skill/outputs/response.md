# Marketing landing page — plan and walkthrough

I'll build this in Pencil end-to-end via the MCP, following the skill's seven-step workflow. A landing page is a non-trivial surface (multiple sections, hero typography, pricing tiers, social proof) so I'm going to plan more carefully than I would for a quick sketch, lean hard on the component library if one exists, and explicitly avoid the AI defaults that make landing pages read templated — three equal feature cards, gradient hero text, glass everything, "Elevate / Seamless / Unleash" copy.

Below is exactly what I'd run, what I'd expect back, and what I'd verify at each step.

## References I consulted (and why)

- `SKILL.md` — the seven-step default workflow, discipline rules, aesthetic defaults, anti-patterns. The "name the atmosphere before you plan" rule and the AI-tells list are load-bearing for keeping a landing page from feeling stock.
- `references/mcp-tools.md` — to confirm `get_guidelines` has a `Landing Page` category (it does, as of 2026-05) and to remember `set_variables` rules (must call `get_variables` first; `replace: false` still overwrites by key).
- `references/batch-design-grammar.md` — op syntax (`I` / `C` / `R` / `U` / `G`), the 25-op chunking rule, the `placeholder: true` lifecycle on top-level frames, sizing rules (`fill_container` / `fit_content` bare strings), the `padding: [t,r,b,l]` array form.
- `references/component-anatomy.md` — how to read a `batch_get` result for an existing card/button before instantiating, and how to build `descendants` paths including the `parent/child` join.
- `references/modern-patterns.md` — fluid type with `clamp()` for the hero specifically, plus the dated-defaults list (three-card grids, parallax-everywhere, scroll-jacking, gradient-on-everything) so I don't reach for them.
- `references/states.md` — for the design-completeness check at the end (every authored component needs hover / focus / disabled at minimum; the page itself doesn't have a "fault state" in the marketing case but the CTA buttons do).
- `assets/examples/example-login-screen.md` — as the canonical greenfield walkthrough so my tool sequence matches the skill's expected shape.

I did **not** load `references/flows.md` (no multi-screen flow), `references/accessibility.md` (the SKILL baseline plus what's in modern-patterns is enough for a marketing page), or `references/pen-schema.md` (no schema-edge questions).

## A couple of things I'd ask up front

Before any tool call I'd want to know:

1. **What's the product?** — name, one-line value prop, and category. "SaaS product" is too thin to write good hero copy, plausible feature labels, or pricing tier names. If you don't tell me, I'll pick something concrete (e.g. "Halt — observability for background jobs") and label it clearly as a placeholder you'll swap for your real positioning.
2. **Is there an existing `.pen` file or `design-system/` folder I should respect?** — drives whether I scaffold tokens or read existing ones.
3. **Brand stance** — is there a brand colour, font, or logo you want me to honour? If not I'll pick one accent in low saturation (per the aesthetic defaults) and a non-Inter sans for display + body.

For the rest of this response I'll assume the worst case for the agent: greenfield repo, no `.pen` open, no `design-system/` folder, no brand input. That makes every step explicit.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

Expected response shape: an object with `activeDocument`, `selection`, and `schemaVersion` (when requested). On success with no doc open, `activeDocument` is null/empty.

If this errors with `transport not connected to app: desktop`: stop and tell you to open the Pencil desktop app or IDE extension. No silent CLI fallback.

If it succeeds with a `.pen` already open: I'd ask whether to add the landing page to that file (likely as a sibling top-level frame, using `find_empty_space_on_canvas` for placement) or open a new doc. For this walkthrough I'll assume no doc open.

## Step 2 — Locate context

Two checks:

1. The `get_editor_state` result tells me no `.pen` is open and nothing is selected.
2. A directory listing of the project root looks for `./design-system/`. Assume it's absent.

## Step 3 — Offer to scaffold, then load guidelines, then inventory

Per Failure mode #3, I'd offer once:

> *"This repo doesn't have a `design-system/` folder yet. I have 12 core templates I can drop in — they teach me your tokens, components, voice, motion, patterns, and tech stack. Since this is a marketing surface, I'd also recommend the optional `brand.md` and `imagery.md` (they pair). Want me to scaffold the core plus those two? You can say no and I'll proceed without."*

Assume you say yes (it's worth it for marketing work). I'd copy from `assets/design-system/` into `./design-system/`, including `brand.md` and `imagery.md` because the project ships a marketing surface and the two pair.

Then:

```
get_guidelines()
```

Expected response: a list of available categories. For 2026-05 the live set includes `Landing Page`, `Web App`, `Design System`, `Tailwind`, `Code`, `Mobile App`, `Slides`, `Table`. I'd call:

```
get_guidelines({ category: "Landing Page" })
get_guidelines({ category: "Design System" })
```

`Tailwind` only if `design-system/design-system.md` declares Tailwind as the stack. I'd skip it for the unknown-stack case.

Then **inventory components** per the Components-first rule. Even with no library imported, I'd check the just-opened doc:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

Expected response: empty `nodes` array (fresh doc has no reusables). That tells me I'll need to either build inline primitives for now or, better, declare a minimal in-document `reusable` Button + Pricing-card so the design isn't a one-off splat. I'll choose the latter; it costs ~6 extra ops at the start and means every CTA on the page stays in lockstep.

If you have a `.lib.pen` (e.g. `./design/system.lib.pen` declared in `design-system/design-system.md`), I'd add the import via a `U("doc", { imports: { "ds": "./design/system.lib.pen" } })` op and run the same `batch_get` against `filePath: "./design/system.lib.pen"`.

## Step 4 — Plan, named atmosphere

Per the aesthetic defaults, before any `batch_design` I commit to a one-line vibe. For a SaaS marketing page that wants to feel intentional:

> **Vibe:** *Balanced density, slightly offset, static.* One accent (a desaturated indigo, not the AI-default purple gradient). Display type in a non-Inter sans (Cabinet Grotesk for headlines, Satoshi for body). Pricing emphasises the middle tier with a different elevation, not a different colour. No three-equal-card features grid; instead an asymmetric layout where the first feature is wider and image-led, the next two stack to its right.

Plan I'd state to you before touching the doc:

> *"I'll build a desktop landing page (1440×900) as the primary frame, with `Tablet` (768) and `Mobile` (390) sibling frames once the desktop holds together. The desktop frame contains: a sticky-feeling top nav (logo, 4 nav links, secondary + primary CTA), a hero (eyebrow, headline using fluid `clamp()` type, sub, two CTAs, one supporting image), a logo strip ('used by'), a feature region using the asymmetric 1-large + 2-stacked pattern, a three-tier pricing block (Starter / Pro / Team — Pro elevated), a testimonials region with two quote cards offset (not three equal cards), a closing CTA band, and a four-column footer. I'll declare a `Button` component and `PricingCard` component in this doc as `reusable: true` so every instance stays consistent. Themes will be light + dark from the start; tokens get bootstrapped with `set_variables` only after `get_variables` confirms the doc is empty."*

That plan is cheap to revise; if you tell me "no nav, that goes elsewhere" I haven't spent any ops yet.

## Step 4.5 — Open the document

```
open_document({ path: "new" })
```

Expected response: a fresh document id. The next `get_editor_state` confirms it.

## Step 5 — Execute

Multiple `batch_design` calls because a landing page is well over 30 visible elements. Order:

### Call A — Themes + skeleton (≤10 ops)

First I declare the theme axis, then bootstrap variables. **But** before the variables call I run:

```
get_variables()
```

Expected: empty object on a fresh doc. Confirmed empty → safe to bootstrap. If it had returned anything, I'd skip whichever keys were already present.

```
set_variables({
  variables: {
    surface:        { type: "color", value: [
      { value: "#FAFAFA", theme: { mode: "light" } },
      { value: "#0B1117", theme: { mode: "dark"  } } ] },
    surfaceMuted:   { type: "color", value: [
      { value: "#F4F4F5", theme: { mode: "light" } },
      { value: "#111418", theme: { mode: "dark"  } } ] },
    surfaceElevated:{ type: "color", value: [
      { value: "#FFFFFF", theme: { mode: "light" } },
      { value: "#181B20", theme: { mode: "dark"  } } ] },
    border:         { type: "color", value: [
      { value: "#E4E4E7", theme: { mode: "light" } },
      { value: "#262A30", theme: { mode: "dark"  } } ] },
    textPrimary:    { type: "color", value: [
      { value: "#101216", theme: { mode: "light" } },
      { value: "#F5F5F4", theme: { mode: "dark"  } } ] },
    textMuted:      { type: "color", value: [
      { value: "#52525B", theme: { mode: "light" } },
      { value: "#A1A1AA", theme: { mode: "dark"  } } ] },
    primary:        { type: "color", value: [
      { value: "#3D52B5", theme: { mode: "light" } },
      { value: "#7287D9", theme: { mode: "dark"  } } ] },
    primaryMuted:   { type: "color", value: [
      { value: "#E0E5F7", theme: { mode: "light" } },
      { value: "#1B2247", theme: { mode: "dark"  } } ] },
    focusRing:      { type: "color", value: [
      { value: "#3D52B5", theme: { mode: "light" } },
      { value: "#7287D9", theme: { mode: "dark"  } } ] },
    "space-1": { type: "number", value: 4 },
    "space-2": { type: "number", value: 8 },
    "space-3": { type: "number", value: 12 },
    "space-4": { type: "number", value: 16 },
    "space-5": { type: "number", value: 24 },
    "space-6": { type: "number", value: 32 },
    "space-8": { type: "number", value: 48 },
    "space-10": { type: "number", value: 64 },
    "space-12": { type: "number", value: 96 },
    "space-16": { type: "number", value: 128 },
    textXs:    { type: "number", value: 12 },
    textSm:    { type: "number", value: 14 },
    textBase:  { type: "number", value: 16 },
    textLg:    { type: "number", value: 18 },
    textXl:    { type: "number", value: 20 },
    text2xl:   { type: "number", value: 24 },
    text3xl:   { type: "number", value: 32 },
    text4xl:   { type: "number", value: 48 },
    textHero:  { type: "number", value: 72 },
    radiusSm:  { type: "number", value: 8 },
    radiusMd:  { type: "number", value: 12 },
    radiusLg:  { type: "number", value: 20 },
    maxContent:{ type: "number", value: 1200 }
  },
  replace: false
})
```

Note the choices: indigo `#3D52B5` (desaturated, not the default Tailwind indigo-500) as the only accent; one neutral family (Zinc); off-black `#101216` and off-white `#FAFAFA` instead of pure 0/255; a `textHero` token for the headline; a fluid hero size will be expressed in code via `clamp()` per `references/modern-patterns.md` (in Pencil I bind the discrete `$textHero` and document the clamp intent in the headline node's `context`).

Then the page skeleton in a single `batch_design`:

```
U("doc", { themes: { mode: ["light", "dark"] } })
page=I(document, { type: "frame", name: "MarketingHome_Desktop", layout: "vertical", gap: 0, width: 1440, height: "fit_content", fill: "$surface", placeholder: true, context: "Marketing landing page, desktop. Vertical stack of regions; each region maxes at $maxContent (1200) with $space-12 gutters." })
nav=I(page, { type: "frame", name: "TopNav", layout: "horizontal", justifyContent: "space-between", alignItems: "center", padding: [20, 120, 20, 120], width: "fill_container", fill: "$surface", stroke: { thickness: 1, fill: "$border", side: "bottom" } })
hero=I(page, { type: "frame", name: "Hero", layout: "vertical", gap: "$space-6", padding: [128, 120, 128, 120], width: "fill_container", alignItems: "center" })
logos=I(page, { type: "frame", name: "LogoStrip", layout: "horizontal", justifyContent: "space-between", alignItems: "center", padding: [48, 120, 48, 120], width: "fill_container", fill: "$surfaceMuted" })
features=I(page, { type: "frame", name: "Features", layout: "vertical", gap: "$space-10", padding: [128, 120, 128, 120], width: "fill_container" })
pricing=I(page, { type: "frame", name: "Pricing", layout: "vertical", gap: "$space-8", padding: [128, 120, 128, 120], width: "fill_container", fill: "$surfaceMuted" })
testimonials=I(page, { type: "frame", name: "Testimonials", layout: "vertical", gap: "$space-8", padding: [128, 120, 128, 120], width: "fill_container" })
ctaBand=I(page, { type: "frame", name: "ClosingCTA", layout: "vertical", gap: "$space-5", padding: [96, 120, 96, 120], width: "fill_container", alignItems: "center", fill: "$primaryMuted" })
footer=I(page, { type: "frame", name: "Footer", layout: "vertical", gap: "$space-6", padding: [64, 120, 32, 120], width: "fill_container", fill: "$surface", stroke: { thickness: 1, fill: "$border", side: "top" } })
```

Then verify structurally before going further:

```
snapshot_layout({ parentId: "page", maxDepth: 2 })
```

Expected: 9 children with the right widths (`fill_container` in a 1440 parent → 1440 each), the right paddings, the cumulative height of `page` should be ~2200–2500px. If anything's off here (a region collapsed because I forgot a child sized `fit_content`, a padding wrong) I fix it before filling regions.

### Call B — In-document Button + PricingCard components (~14 ops)

I declare two reusables in the doc itself — they live as off-canvas children of the document root (or in a holding frame).

```
sys=I(document, { type: "frame", name: "_Components", x: 1600, y: 0, layout: "vertical", gap: "$space-8", context: "Off-canvas component definitions for this doc. Do not include in exports." })
btn=I(sys, { type: "frame", name: "Button", reusable: true, layout: "horizontal", gap: "$space-2", alignItems: "center", justifyContent: "center", padding: [12, 20, 12, 20], cornerRadius: "$radiusMd", fill: "$primary", height: 44, context: "Primary CTA. 44px tall to meet hit-target minimum. Hover state should darken fill 8%; focus state adds 2px $focusRing offset 2px." })
btnLabel=I(btn, { type: "text", name: "Label", text: "Get started", fontSize: "$textBase", fontWeight: 600, fill: "$surface" })
card=I(sys, { type: "frame", name: "PricingCard", reusable: true, layout: "vertical", gap: "$space-5", padding: [32, 32, 32, 32], cornerRadius: "$radiusLg", fill: "$surface", stroke: { thickness: 1, fill: "$border" }, width: 360, context: "Pricing tier card. Default elevation is flat with a 1px border. The middle/featured tier overrides fill to $surfaceElevated and adds a stronger shadow, NOT a colour change." })
cardTier=I(card, { type: "text", name: "TierName", text: "Pro", fontSize: "$textSm", fontWeight: 600, fill: "$primary" })
cardPriceRow=I(card, { type: "frame", name: "PriceRow", layout: "horizontal", gap: "$space-2", alignItems: "baseline" })
cardPrice=I(cardPriceRow, { type: "text", name: "Price", text: "$29", fontSize: "$text4xl", fontWeight: 700, fill: "$textPrimary" })
cardPer=I(cardPriceRow, { type: "text", name: "Per", text: "/seat / month", fontSize: "$textSm", fill: "$textMuted" })
cardDesc=I(card, { type: "text", name: "Description", text: "For small teams getting serious.", fontSize: "$textBase", fill: "$textMuted" })
cardFeatures=I(card, { type: "frame", name: "Features", layout: "vertical", gap: "$space-3", padding: [16, 0, 16, 0] })
cardCta=I(card, { type: "ref", ref: btn, name: "CardCTA", descendants: { Label: { text: "Choose Pro" } } })
```

Then I'd add three feature-bullet rows to `cardFeatures` either now or in the pricing-region call.

### Call C — Top nav (≤10 ops)

```
logoMark=I(nav, { type: "frame", name: "Logo", layout: "horizontal", gap: "$space-2", alignItems: "center" })
logoIcon=I(logoMark, { type: "icon", iconName: "circle-dot", width: 24, height: 24, fill: "$primary", context: "Placeholder logo mark — replace with brand mark when supplied." })
logoText=I(logoMark, { type: "text", text: "Halt", fontSize: "$textLg", fontWeight: 700, fill: "$textPrimary" })
navLinks=I(nav, { type: "frame", name: "NavLinks", layout: "horizontal", gap: "$space-6", alignItems: "center" })
link1=I(navLinks, { type: "text", text: "Product", fontSize: "$textSm", fill: "$textMuted" })
link2=I(navLinks, { type: "text", text: "Pricing", fontSize: "$textSm", fill: "$textMuted" })
link3=I(navLinks, { type: "text", text: "Customers", fontSize: "$textSm", fill: "$textMuted" })
link4=I(navLinks, { type: "text", text: "Docs", fontSize: "$textSm", fill: "$textMuted" })
navCtas=I(nav, { type: "frame", name: "NavCtas", layout: "horizontal", gap: "$space-3", alignItems: "center" })
signIn=I(navCtas, { type: "text", text: "Sign in", fontSize: "$textSm", fontWeight: 500, fill: "$textPrimary" })
ctaPrimary=I(navCtas, { type: "ref", ref: btn, descendants: { Label: { text: "Start free" } } })
```

### Call D — Hero (≤14 ops)

The hero is where the page either reads intentional or templated. The choices: a real product name and value prop (placeholder I'd flag), a constrained content width inside the larger padding, an asymmetric arrangement (left-weighted text + a single product visual to the right rather than the centred "scroll to explore" default), no gradient on the headline.

```
heroInner=I(hero, { type: "frame", name: "HeroInner", layout: "horizontal", gap: "$space-12", alignItems: "center", justifyContent: "space-between", width: "fill_container(1200)" })
heroText=I(heroInner, { type: "frame", name: "HeroText", layout: "vertical", gap: "$space-5", width: 560 })
eyebrow=I(heroText, { type: "text", text: "Background jobs, observed", fontSize: "$textSm", fontWeight: 600, fill: "$primary", context: "Eyebrow line — short, sets the category. Replace with the product's real category label." })
headline=I(heroText, { type: "text", text: "Know exactly when a job stops working.", fontSize: "$textHero", fontWeight: 700, fill: "$textPrimary", lineHeight: 1.05, context: "Hero headline. In code, font-size should be clamp(40px, 6vw, 72px). Discrete $textHero here is the desktop baseline." })
sub=I(heroText, { type: "text", text: "Halt watches every cron, queue worker, and scheduled task in your stack. When something stops sending heartbeats, you hear about it before your customers do.", fontSize: "$textLg", fill: "$textMuted", lineHeight: 1.45 })
heroCtas=I(heroText, { type: "frame", name: "HeroCtas", layout: "horizontal", gap: "$space-3", padding: [16, 0, 0, 0] })
heroCtaPrimary=I(heroCtas, { type: "ref", ref: btn, descendants: { Label: { text: "Start watching" } } })
heroCtaSecondary=I(heroCtas, { type: "frame", name: "SecondaryCta", layout: "horizontal", gap: "$space-2", alignItems: "center", padding: [12, 20, 12, 20], cornerRadius: "$radiusMd", stroke: { thickness: 1, fill: "$border" }, height: 44 })
secondaryLabel=I(heroCtaSecondary, { type: "text", text: "See a live demo", fontSize: "$textBase", fontWeight: 500, fill: "$textPrimary" })
secondaryIcon=I(heroCtaSecondary, { type: "icon", iconName: "arrow-right", width: 16, height: 16, fill: "$textPrimary" })
heroVisual=I(heroInner, { type: "frame", name: "HeroVisual", width: 520, height: 380, cornerRadius: "$radiusLg", fill: "$surfaceMuted", stroke: { thickness: 1, fill: "$border" }, context: "Product screenshot or AI-generated product visual. To be filled with G(\"heroVisual\", \"ai\", ...) on the next call." })
```

Then immediately:

```
G("heroVisual", "ai", "minimal product UI screenshot showing a list of background jobs with green and amber heartbeat indicators, neutral light interface, soft shadow on the card, no glow effects")
```

I'd avoid `unsplash` mode for the hero visual — generic stock photos are an AI tell.

### Call E — Logo strip (~6 ops)

Five customer/partner logos rendered as plain text in muted colour (the right pattern when you don't have real logo assets to drop in):

```
logosInner=I(logos, { type: "frame", name: "LogosInner", layout: "horizontal", justifyContent: "space-between", alignItems: "center", width: "fill_container(1000)" })
logoCue=I(logosInner, { type: "text", text: "Used by teams at", fontSize: "$textSm", fill: "$textMuted" })
l1=I(logosInner, { type: "text", text: "Linear", fontSize: "$textXl", fontWeight: 600, fill: "$textMuted" })
l2=I(logosInner, { type: "text", text: "Cursor", fontSize: "$textXl", fontWeight: 600, fill: "$textMuted" })
l3=I(logosInner, { type: "text", text: "Vercel", fontSize: "$textXl", fontWeight: 600, fill: "$textMuted" })
l4=I(logosInner, { type: "text", text: "Resend", fontSize: "$textXl", fontWeight: 600, fill: "$textMuted" })
l5=I(logosInner, { type: "text", text: "Anthropic", fontSize: "$textXl", fontWeight: 600, fill: "$textMuted" })
```

I'd flag these as placeholders — never ship invented customer names. `voice.md` would have an opinion here; in its absence I'd say so.

### Call F — Three feature blocks, asymmetric (≤22 ops)

Per the AI-defaults list, three equal cards in a row is *the* tell for a feature section. I'm instead doing a 1-large + 2-stacked layout:

```
featuresHead=I(features, { type: "frame", name: "FeaturesHead", layout: "vertical", gap: "$space-3", width: "fill_container(800)" })
featuresEyebrow=I(featuresHead, { type: "text", text: "Why teams switch", fontSize: "$textSm", fontWeight: 600, fill: "$primary" })
featuresTitle=I(featuresHead, { type: "text", text: "Built for the alerts you actually want.", fontSize: "$text3xl", fontWeight: 700, fill: "$textPrimary" })
featuresGrid=I(features, { type: "frame", name: "FeaturesGrid", layout: "horizontal", gap: "$space-8", alignItems: "stretch", width: "fill_container(1200)" })
fLarge=I(featuresGrid, { type: "frame", name: "Feature_Heartbeats", layout: "vertical", gap: "$space-5", padding: [32, 32, 32, 32], cornerRadius: "$radiusLg", fill: "$surfaceMuted", width: 720, context: "Lead feature — visual-led, takes 60% of the row." })
fLargeVisual=I(fLarge, { type: "frame", name: "Visual", height: 280, cornerRadius: "$radiusMd", fill: "$surface", stroke: { thickness: 1, fill: "$border" }, context: "AI image: heartbeat timeline UI. Filled via G() after this call." })
fLargeTitle=I(fLarge, { type: "text", text: "Heartbeat-by-heartbeat timelines", fontSize: "$text2xl", fontWeight: 700, fill: "$textPrimary" })
fLargeDesc=I(fLarge, { type: "text", text: "Every job sends a heartbeat. Halt graphs them so you can see drift before it becomes downtime — usually hours before your customers notice anything.", fontSize: "$textBase", fill: "$textMuted", lineHeight: 1.5 })
fStack=I(featuresGrid, { type: "frame", name: "FeaturesStack", layout: "vertical", gap: "$space-5", width: "fill_container", alignItems: "stretch" })
fSmall1=I(fStack, { type: "frame", name: "Feature_Routing", layout: "vertical", gap: "$space-3", padding: [24, 24, 24, 24], cornerRadius: "$radiusLg", fill: "$surfaceMuted" })
fSmall1Icon=I(fSmall1, { type: "icon", iconName: "split", width: 24, height: 24, fill: "$primary" })
fSmall1Title=I(fSmall1, { type: "text", text: "Route alerts to the right human", fontSize: "$textXl", fontWeight: 700, fill: "$textPrimary" })
fSmall1Desc=I(fSmall1, { type: "text", text: "On-call rotations, escalations, working hours per timezone. The page that goes off at 3am is the one that should.", fontSize: "$textBase", fill: "$textMuted" })
fSmall2=I(fStack, { type: "frame", name: "Feature_NoConfig", layout: "vertical", gap: "$space-3", padding: [24, 24, 24, 24], cornerRadius: "$radiusLg", fill: "$surfaceMuted" })
fSmall2Icon=I(fSmall2, { type: "icon", iconName: "wand", width: 24, height: 24, fill: "$primary" })
fSmall2Title=I(fSmall2, { type: "text", text: "No config files to maintain", fontSize: "$textXl", fontWeight: 700, fill: "$textPrimary" })
fSmall2Desc=I(fSmall2, { type: "text", text: "Halt watches what your stack already does. New cron, new queue worker — picked up on the next deploy without a YAML edit.", fontSize: "$textBase", fill: "$textMuted" })
```

Then after the call:

```
G("fLargeVisual", "ai", "abstract data visualization of horizontal timeline lines with green and amber dots representing heartbeats, light neutral interface, very subtle, no glow effects")
```

### Call G — Pricing (≤18 ops)

Three tiers, middle one elevated by treatment, not by colour. Each instance overrides the `PricingCard` component:

```
pricingHead=I(pricing, { type: "frame", name: "PricingHead", layout: "vertical", gap: "$space-3", alignItems: "center", width: "fill_container(800)" })
pricingTitle=I(pricingHead, { type: "text", text: "Simple pricing. Stop paying per host.", fontSize: "$text3xl", fontWeight: 700, fill: "$textPrimary", textAlign: "center" })
pricingSub=I(pricingHead, { type: "text", text: "Every plan includes the full alert engine. You're paying for seats and history, not features.", fontSize: "$textLg", fill: "$textMuted", textAlign: "center" })
pricingGrid=I(pricing, { type: "frame", name: "PricingGrid", layout: "horizontal", gap: "$space-5", justifyContent: "center", alignItems: "stretch", width: "fill_container" })
tStarter=I(pricingGrid, { type: "ref", ref: card, descendants: { TierName: { text: "Starter" }, "PriceRow/Price": { text: "$0" }, "PriceRow/Per": { text: "free forever" }, Description: { text: "For solo developers and side projects." }, "CardCTA/Label": { text: "Start free" } } })
tPro=I(pricingGrid, { type: "ref", ref: card, descendants: { TierName: { text: "Pro" }, "PriceRow/Price": { text: "$29" }, "PriceRow/Per": { text: "/seat / month" }, Description: { text: "For small teams getting serious about uptime." }, "CardCTA/Label": { text: "Choose Pro" } }, fill: "$surfaceElevated", stroke: { thickness: 1, fill: "$primary" }, context: "Featured tier. Differentiation is structural (border + elevation), not colour." })
tTeam=I(pricingGrid, { type: "ref", ref: card, descendants: { TierName: { text: "Team" }, "PriceRow/Price": { text: "$99" }, "PriceRow/Per": { text: "/seat / month" }, Description: { text: "For platforms running thousands of jobs." }, "CardCTA/Label": { text: "Talk to sales" } } })
```

I'd then add three feature-list rows to each card via a follow-up call (one per tier; each row is icon + text using the Lucide `check` icon in `$primary`). That's ~9 ops; still inside one call budget if I batch.

The `descendants` paths — `"PriceRow/Price"`, `"CardCTA/Label"` — use the `parent/child` form documented in `references/component-anatomy.md`. Each id has to actually exist in the component tree as I built it in Call B; I'd verify with a quick `batch_get` if any descendant key errors.

### Call H — Testimonials, two cards offset (≤12 ops)

Per the avoid-three-equal-cards rule, two cards offset slightly:

```
testimonialsHead=I(testimonials, { type: "frame", name: "TestimonialsHead", layout: "vertical", gap: "$space-3", width: "fill_container(800)" })
tEyebrow=I(testimonialsHead, { type: "text", text: "What teams say", fontSize: "$textSm", fontWeight: 600, fill: "$primary" })
tTitle=I(testimonialsHead, { type: "text", text: "Quiet pages. Loud heartbeats.", fontSize: "$text3xl", fontWeight: 700, fill: "$textPrimary" })
tGrid=I(testimonials, { type: "frame", name: "TestimonialsGrid", layout: "horizontal", gap: "$space-8", alignItems: "start", width: "fill_container(1200)" })
quote1=I(tGrid, { type: "frame", name: "Quote_1", layout: "vertical", gap: "$space-5", padding: [32, 32, 32, 32], cornerRadius: "$radiusLg", fill: "$surface", stroke: { thickness: 1, fill: "$border" }, width: 540 })
quote1Body=I(quote1, { type: "text", text: "We caught a queue worker silently crashing on a Thursday afternoon. Without Halt we'd have noticed Monday when the support tickets came in.", fontSize: "$textLg", fill: "$textPrimary", lineHeight: 1.45 })
quote1Author=I(quote1, { type: "frame", name: "Author", layout: "horizontal", gap: "$space-3", alignItems: "center" })
quote1Avatar=I(quote1Author, { type: "frame", width: 40, height: 40, cornerRadius: 20, fill: "$primaryMuted", context: "Avatar — fill via G() with portrait or replace with real photo on handoff." })
quote1Name=I(quote1Author, { type: "frame", layout: "vertical", gap: 0 })
quote1NameText=I(quote1Name, { type: "text", text: "Engineering lead, mid-stage SaaS", fontSize: "$textSm", fontWeight: 600, fill: "$textPrimary", context: "Anonymised role + company shape — replace with real attribution on handoff." })
quote1Role=I(quote1Name, { type: "text", text: "200-engineer team", fontSize: "$textSm", fill: "$textMuted" })
quote2=I(tGrid, { type: "frame", name: "Quote_2", layout: "vertical", gap: "$space-5", padding: [32, 32, 32, 32], cornerRadius: "$radiusLg", fill: "$surface", stroke: { thickness: 1, fill: "$border" }, width: 540, y: 32, context: "Offset 32px lower than the first quote — breaks the equal-row default." })
```

(Similar inner ops for `quote2`, omitted for brevity — same shape as `quote1`.)

The `y: 32` on `quote2` works because `tGrid` uses `alignItems: "start"`. With the row alignment as start, the second card rendering 32px lower gives the offset I want without needing `layout: "none"`.

The avatar frames I'd leave as solid `$primaryMuted` blocks rather than fake photos. If you want headshots, I'd flag that as needing real input — a `G(\"\", \"unsplash\", \"smiling person\")` call here is the AI tell to end all AI tells.

### Call I — Closing CTA band (≤6 ops)

```
closingTitle=I(ctaBand, { type: "text", text: "Stop guessing whether your jobs ran.", fontSize: "$text3xl", fontWeight: 700, fill: "$textPrimary", textAlign: "center" })
closingSub=I(ctaBand, { type: "text", text: "Five minutes to install. Free for one developer, forever.", fontSize: "$textLg", fill: "$textMuted", textAlign: "center" })
closingCtas=I(ctaBand, { type: "frame", name: "ClosingCtas", layout: "horizontal", gap: "$space-3", justifyContent: "center" })
closingPrimary=I(closingCtas, { type: "ref", ref: btn, descendants: { Label: { text: "Start free" } } })
closingSecondary=I(closingCtas, { type: "ref", ref: btn, descendants: { Label: { text: "Talk to sales" } }, fill: "$surface", stroke: { thickness: 1, fill: "$border" }, context: "Secondary CTA — uses the Button component but overrides fill + stroke for outline style. If we end up needing this in many places, extract to a ButtonOutline component." })
```

The `closingSecondary` flag is important: I'm overriding the component for a one-off, but the discipline rules say I should surface that out loud. I'd note to you in the report: *"There are now two outline-style CTAs on the page. If you want this consistent, I'll promote `Button` to a state-axis or sibling-variant component with a `secondary` style."*

### Call J — Footer (≤16 ops)

A four-column footer with brand mark + copy in the first column, then product / company / legal:

```
footerInner=I(footer, { type: "frame", name: "FooterInner", layout: "horizontal", gap: "$space-10", justifyContent: "space-between", alignItems: "start", width: "fill_container(1200)" })
fcBrand=I(footerInner, { type: "frame", name: "Brand", layout: "vertical", gap: "$space-3", width: 280 })
fcLogo=I(fcBrand, { type: "frame", layout: "horizontal", gap: "$space-2", alignItems: "center" })
fcLogoIcon=I(fcLogo, { type: "icon", iconName: "circle-dot", width: 20, height: 20, fill: "$primary" })
fcLogoText=I(fcLogo, { type: "text", text: "Halt", fontSize: "$textBase", fontWeight: 700, fill: "$textPrimary" })
fcCopy=I(fcBrand, { type: "text", text: "Heartbeat monitoring for background work.", fontSize: "$textSm", fill: "$textMuted" })
fcProduct=I(footerInner, { type: "frame", name: "ProductCol", layout: "vertical", gap: "$space-3" })
fcProductTitle=I(fcProduct, { type: "text", text: "Product", fontSize: "$textSm", fontWeight: 600, fill: "$textPrimary" })
fcProduct1=I(fcProduct, { type: "text", text: "Features", fontSize: "$textSm", fill: "$textMuted" })
fcProduct2=I(fcProduct, { type: "text", text: "Pricing", fontSize: "$textSm", fill: "$textMuted" })
fcProduct3=I(fcProduct, { type: "text", text: "Changelog", fontSize: "$textSm", fill: "$textMuted" })
fcProduct4=I(fcProduct, { type: "text", text: "Status", fontSize: "$textSm", fill: "$textMuted" })
```

Plus equivalent `Company` (About / Customers / Careers / Contact) and `Legal` (Terms / Privacy / Security / DPA) columns and a final bottom row with `© Halt 2026`. About 14 ops total in this call.

### Call K — Take down placeholder

Once everything's in place:

```
U("page", { placeholder: false })
```

Per `batch-design-grammar.md` § Placeholder frames, this signals to the editor the frame is finished.

## Step 6 — Verify (structural-first, then one screenshot)

I'd walk the verification ladder, not screenshot per call:

1. **`batch_design` responses** — each call's success/failure was confirmed inline as I went.
2. **`snapshot_layout({ parentId: "page", maxDepth: 3 })`** — final structural sweep. I'm checking: does each section's height look right (~120–180px for nav, ~600–700px for hero, ~700px for features, ~600px for pricing, ~500px for testimonials, ~280px for closing CTA, ~280px for footer; cumulative ~3000–3300px)? Do all `fill_container` widths land at the same 1440? Are gaps between cards in pricing the `$space-5` I asked for?
3. **`batch_get({ nodeIds: ["headline", "tPro", "fLarge"], resolveVariables: true })`** — confirms the headline's font size resolved to the `$textHero` value, the Pro card's fill resolved to `$surfaceElevated`'s correct hex per mode, and the lead feature card's width is 720.
4. **`get_screenshot({ nodeId: "page" })`** — one screenshot, scoped to the page (not document root). I'm scanning for: layout integrity (nothing off-canvas), spacing rhythm (the `$space-12` gutters reading consistent), type rhythm (the hero headline dominating, supporting text stepping down predictably), contrast (the `$textMuted` body copy in dark mode passing AA against `$surface` — the `textMuted` `#A1A1AA` on `surface` `#0B1117` is approx 8.4:1, well past 4.5), component fidelity (every CTA visibly the same Button shape; no drift).

Per the dual-mode rule in SKILL.md: I built every fill from `mode`-aware variables. **I would not screenshot the dark mode separately** — the variable system guarantees mode parity for theme-aware designs. If I had hardcoded a hex anywhere, I'd screenshot dark mode to verify; I didn't, so I won't.

If the screenshot reveals one or two discrete issues (a likely candidate: the closing-CTA band's `$primaryMuted` background reading too pale in light mode against the surrounding `$surface`), I'd fix with targeted `U` ops and re-screenshot once. Three iterations on the same problem → stop and ask you.

## Step 7 — Tablet + Mobile breakpoints

Once the desktop holds together, add the two responsive frames as siblings of `MarketingHome_Desktop`. Each is its own `placeholder: true` frame at 768×~3500 and 390×~4000, structured the same way but with:

- Smaller gutter padding (`[80, 32, 80, 32]` on tablet, `[48, 16, 48, 16]` on mobile).
- Hero text and visual stack vertically (`HeroInner` switches `layout: "vertical"`).
- Feature grid collapses: large card on top, two stacked cards below (vertical).
- Pricing grid stacks vertically; the featured tier comes first on mobile (high-value content on top of the fold).
- Testimonials stack; no offset (`y: 0`).
- Footer collapses to two columns on tablet, single column on mobile.
- Top nav becomes a logo + hamburger on mobile; the hamburger is an icon-only button at the 44×44 hit-target minimum.

These are three more `batch_design` calls of ~15–20 ops each, mostly mirroring the desktop with property differences.

## What I'd flag in the final report

When I hand back, I'd say:

> *"Built `MarketingHome_Desktop`, `_Tablet`, and `_Mobile` as sibling frames. Eight regions per breakpoint, all driven by the in-doc `Button` and `PricingCard` components. Light + dark themes both supported via the `mode` axis and theme-aware variables. Verified structurally at each phase, one final screenshot of the desktop scoped to the page node — no full-page screenshots, no dark-mode screenshot (variables guarantee parity).*
>
> *Three things to flag:*
>
> *1. All product copy ('Halt', the value prop, customer logo names, testimonial attribution) is placeholder content, clearly labelled in node `context` strings. Swap before launch.*
>
> *2. The two outline-style CTAs in the closing band override the `Button` component's fill and stroke. If outline CTAs are a real pattern for you, want me to promote that to a `ButtonSecondary` (sibling component) or a `state` axis on `Button`?*
>
> *3. The hero AI image and the lead feature AI image are placeholders generated via `G()`. They're decent enough for a design review; replace with real product screenshots before shipping. Avatar frames in testimonials are intentionally blank — AI-generated headshots are an AI tell I won't ship without your sign-off."*

That's the full task. The shape of the work — atmosphere named first, components first, structural verification before pixels, one screenshot, AI defaults explicitly avoided — is what makes the difference between a landing page that reads intentional and one that reads templated.
