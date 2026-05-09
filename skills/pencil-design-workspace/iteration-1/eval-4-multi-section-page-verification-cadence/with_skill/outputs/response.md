# Marketing landing page — incremental build with per-region verification

## Skill references I consulted (and why)

Before any MCP calls, I loaded:

1. **`SKILL.md`** — the discipline rules (Naming, Context, Components first, Themes, Responsive, Accessibility, File architecture), the verification ladder, and the "Verification cadence" guidance ("a typical end-to-end design task should need one or two screenshots total").
2. **`references/layout-patterns.md`** — for the marketing archetype, especially the Hero, Feature, and Footer sub-menus. This file flags the three-equal-card grid as "the most over-used SaaS marketing pattern" and a layout AI tell. The user explicitly asked for three columns, so I will honour the brief but lean on optical-precision and typography rules to keep it from reading templated.
3. **`references/mcp-tools.md`** — the per-tool cookbook and the cost cheatsheet. Most useful section: the **Greenfield document bootstrap** recipe, which is exactly the right shape for a new `.pen` at 1440×900.
4. **`references/batch-design-grammar.md`** — the op grammar (`I` / `C` / `R` / `U` / `G`), the `placeholder: true` rule for top-level frames, the `width: "fill_container"` bare-string rule, the `padding: [t,r,b,l]` array form, and the ≤25-ops chunking discipline.
5. **`assets/examples/example-marketing-page.md`** — a worked marketing build I scanned for section-naming conventions (`Marketing_*` prefix), restraint patterns (no kitchen-sink footer), and the per-section verification cadence at the end (the example screenshots once per section; for *this* simpler three-region brief, I can do less and stay within the cadence rule).

I did **not** load `references/forms.md`, `references/mobile-patterns.md`, `references/data-viz.md`, or `references/style-catalogue.md` — none apply. I did not load `references/states.md` either; the brief is for a single happy-path landing page, not a fault state, and the user did not ask for component state coverage.

---

## Step 1 — Detect host

```
get_editor_state({ include_schema: false })
```

**Expected response shape:** `{ activeDocumentPath, selectedNodeIds, schemaVersion, … }` or an error of the form `transport not connected to app: desktop`.

**What I would check:** that the call succeeded (host is reachable) and what document, if any, is open. The brief says "in a new `.pen` document", so even if a document is open I will create a new one rather than write into the user's current canvas.

If the call errored, I would stop and tell the user *"Pencil's MCP server isn't reachable. Open the Pencil desktop app or the Pencil IDE extension, then ask me again."* per Failure mode §1. I would not silently fall back to the CLI.

## Step 2 — Open a new document

```
open_document({ path: "new" })
```

**Expected response:** the document root id, plus the document's initial empty state. The next `get_editor_state` would reflect the new document as active.

I would note the document root id (it is always addressable as the predefined `document` binding inside `batch_design` calls, but I want the explicit id for `snapshot_layout` and `batch_get` calls that take `parentId`).

## Step 3 — Load guidelines + bootstrap tokens

### 3a. Guidelines

```
get_guidelines()
get_guidelines({ category: "Landing Page" })
get_guidelines({ category: "Design System" })
```

**Why these two categories:** `mcp-tools.md` § `get_guidelines` decision shortcuts says *"Pricing or marketing page → `Landing Page`, `Design System`."* I would not load `Web App` or `Tailwind` here — `Web App` is for product UI and `Tailwind` only applies if the project ships Tailwind v4, which I have no signal for.

**What I would check in the response:** any rules from `Landing Page` about hero composition, conversion-CTA hierarchy, and footer architecture; any rules from `Design System` about token taxonomy that affect what I bootstrap in step 3c.

### 3b. Project context

I would also list the project filesystem for a `design-system/` folder. The brief reads as a one-off sketch ("placeholder copy", "aim for clean spacing rhythm"), so if no `design-system/` exists I would proceed without offering to scaffold — Failure mode §3 says *"do not ask twice in the same session"* and the offer only fires for "real project work". A throwaway landing-page mock does not qualify.

### 3c. Bootstrap variables

The document is brand new, so `get_variables()` will return an empty (or near-empty) set, but I would still call it before any `set_variables` — the rule from SKILL.md § Themes is mandatory:

```
get_variables()
```

Then declare the theme axis and seed the token suite. Two `batch_design`/`set_variables` calls:

```
batch_design({
  operations: `U(document, { themes: { mode: ["light", "dark"] } })`
})

set_variables({
  variables: {
    surface:        { type: "color", value: [
      { value: "#FAFAFA", theme: { mode: "light" } },
      { value: "#0B1117", theme: { mode: "dark"  } }
    ] },
    surfaceMuted:   { type: "color", value: [
      { value: "#F4F4F5", theme: { mode: "light" } },
      { value: "#18181B", theme: { mode: "dark"  } }
    ] },
    border:         { type: "color", value: [
      { value: "#E4E4E7", theme: { mode: "light" } },
      { value: "#27272A", theme: { mode: "dark"  } }
    ] },
    textPrimary:    { type: "color", value: [
      { value: "#0B1117", theme: { mode: "light" } },
      { value: "#FAFAFA", theme: { mode: "dark"  } }
    ] },
    textMuted:      { type: "color", value: [
      { value: "#52525B", theme: { mode: "light" } },
      { value: "#A1A1AA", theme: { mode: "dark"  } }
    ] },
    accent:         { type: "color", value: [
      { value: "#1F6FEB", theme: { mode: "light" } },
      { value: "#3B82F6", theme: { mode: "dark"  } }
    ] },
    accentText:     { type: "color", value: [
      { value: "#FFFFFF", theme: { mode: "light" } },
      { value: "#0B1117", theme: { mode: "dark"  } }
    ] },
    focusRing:      { type: "color", value: [
      { value: "#1F6FEB", theme: { mode: "light" } },
      { value: "#3B82F6", theme: { mode: "dark"  } }
    ] },

    "space-1": { type: "number", value: 4   },
    "space-2": { type: "number", value: 8   },
    "space-3": { type: "number", value: 12  },
    "space-4": { type: "number", value: 16  },
    "space-5": { type: "number", value: 24  },
    "space-6": { type: "number", value: 32  },
    "space-8": { type: "number", value: 48  },
    "space-10": { type: "number", value: 64 },
    "space-12": { type: "number", value: 96 },

    textSm:    { type: "number", value: 14 },
    textBase:  { type: "number", value: 16 },
    textLg:    { type: "number", value: 18 },
    textXl:    { type: "number", value: 20 },
    text2xl:   { type: "number", value: 28 },
    text4xl:   { type: "number", value: 56 },

    radiusSm:  { type: "number", value: 6  },
    radiusMd:  { type: "number", value: 10 },
    radiusLg:  { type: "number", value: 16 },

    maxContent:{ type: "number", value: 1200 }
  },
  replace: false
})
```

**Notes on the tokens.** Off-black `#0B1117` and off-white `#FAFAFA` rather than pure `#000000` / `#FFFFFF` per the SKILL anti-patterns list. Neutrals from one family (Zinc) per the Aesthetic defaults. One accent (blue) at moderate saturation. Spacing on a 4px base. Type scale jumps tightly at body sizes (14/16/18/20) and opens up at display (28/56) so the hero headline carries weight without crowding the surrounding scale.

I will **not** declare `$fontDisplay` / `$fontBody` font-family variables here — the brief asked for "consistent typography" but did not name a stack. I will rely on Pencil's default rendering and document a `context` recommending `Geist` (per the Aesthetic-defaults Typography rule for software UIs) so an engineer picks it up at handoff.

## Step 4 — Plan

I commit the atmosphere out loud, per `Aesthetic defaults` § Name the atmosphere: **Balanced, symmetric, static.** The brief is a baseline marketing page; nothing in the request asks for editorial flourish or motion-led storytelling, and overcommitting to "asymmetric / cinematic" would fight the user's "clean spacing rhythm" instruction.

I will create one top-level frame (`Marketing_LandingPage`) at `1440×900` with three sibling content regions inside it, in column flex layout. Each region gets a meaningful `name` and a `context` describing intent, per the discipline rules. Three regions:

1. **`Hero`** — full-width, centred copy: eyebrow / H1 / subhead / primary CTA. Auto-layout column, `align: center`. The "centred" hero is the SaaS default and a slight AI tell, but it is the right pick for a single-CTA conversion brief and the user did ask for "a centered headline".
2. **`Features`** — three-column grid. Each column has an icon-tile, a heading, and a paragraph. Equal columns inside an auto-layout row, gap from `$space-6`, contained inside a `$maxContent` (1200) wrapper.
3. **`Footer`** — divider + horizontal row with copyright on the left and three text links on the right. Pulls the "Minimal" footer architecture from `layout-patterns.md` § Footer architectures (right pick for "single-product sites where the footer isn't where the user navigates").

I will instantiate from primitives because the Components-first inventory step found nothing — this is a new `.pen` with no imported `.lib.pen`. After the page is built, I will surface the *"these patterns look reusable — should I add a `Button`, `FeatureCard`, and `FooterLink` to a `.lib.pen`?"* prompt to the user per Components-first.

I will not call `find_empty_space_on_canvas` — the canvas is empty (new document), so the page goes at origin `(0, 0)`.

---

## Region 1 — Hero

### Build

One `batch_design` call, ~12 ops, well under the 25-op ceiling. The `placeholder: true` flag goes on the page frame.

```
page=I(document, {
  type: "frame",
  name: "Marketing_LandingPage",
  width: 1440,
  height: 900,
  layout: "vertical",
  alignItems: "stretch",
  fill: "$surface",
  placeholder: true,
  context: "Desktop marketing landing page (1440x900). Three sibling regions: Hero, Features, Footer. Atmosphere: balanced, symmetric, static. Tokens: zinc neutrals, single blue accent."
})

hero=I(page, {
  type: "frame",
  name: "Hero",
  width: "fill_container",
  layout: "vertical",
  alignItems: "center",
  justifyContent: "center",
  gap: "$space-5",
  padding: ["$space-12", "$space-12", "$space-12", "$space-12"],
  fill: "$surface",
  context: "Top hero region. Centred copy column. Eyebrow + H1 + subhead + primary CTA. Conversion intent: trial signup."
})

heroCopy=I(hero, {
  type: "frame",
  name: "HeroCopy",
  width: 720,
  layout: "vertical",
  alignItems: "center",
  gap: "$space-4"
})

eyebrow=I(heroCopy, {
  type: "text",
  name: "HeroEyebrow",
  content: "For modern product teams",
  fontSize: "$textSm",
  fontWeight: "500",
  letterSpacing: 0.04,
  fill: "$accent",
  textAlign: "center"
})

headline=I(heroCopy, {
  type: "text",
  name: "HeroHeadline",
  content: "Ship better product, faster.",
  fontSize: "$text4xl",
  fontWeight: "700",
  lineHeight: 1.05,
  letterSpacing: -0.02,
  fill: "$textPrimary",
  textAlign: "center",
  context: "H1. Action-led, benefit-focused. Render with text-wrap: balance to avoid orphan last word."
})

subhead=I(heroCopy, {
  type: "text",
  name: "HeroSubhead",
  content: "An opinionated workspace that helps your team plan, build, and release without the meeting that should have been an issue.",
  fontSize: "$textLg",
  fontWeight: "400",
  lineHeight: 1.5,
  fill: "$textMuted",
  textAlign: "center",
  width: 560
})

ctaWrap=I(hero, {
  type: "frame",
  name: "HeroCtaWrap",
  layout: "horizontal",
  gap: "$space-3",
  alignItems: "center"
})

cta=I(ctaWrap, {
  type: "frame",
  name: "PrimaryCta",
  layout: "horizontal",
  alignItems: "center",
  justifyContent: "center",
  padding: ["$space-3", "$space-5", "$space-3", "$space-5"],
  fill: "$accent",
  cornerRadius: "$radiusMd",
  reusable: false,
  context: "Primary CTA on the hero. Tap target >= 44px high. Hover/focus/disabled states deferred to .lib.pen extraction."
})

ctaLabel=I(cta, {
  type: "text",
  name: "PrimaryCtaLabel",
  content: "Start free trial",
  fontSize: "$textBase",
  fontWeight: "600",
  fill: "$accentText"
})
```

### Verification — region 1

After the call returns I would walk the ladder, stopping at the cheapest rung that answers the question.

1. **Rung 1 — `batch_design` response.** The server returns `{ ok: true, bindings: { page, hero, heroCopy, eyebrow, headline, subhead, ctaWrap, cta, ctaLabel } }` with the assigned ids. **What I would check:** every op succeeded; the binding map is complete (any missing binding means an op failed silently). If any op errored, the error message would name the property — I would cross-reference `batch-design-grammar.md` § Common errors.

2. **Rung 2 — `snapshot_layout(parentId: "<hero>", maxDepth: 2)`.** **What I would check:**
   - The `Hero` frame's computed height is the sum of its children plus padding (so it sits ~around the 720px desktop hero shape).
   - `HeroCopy`'s computed width is 720px and its children stack vertically with `$space-4` (16px) gaps.
   - `HeroCtaWrap` sits below `HeroCopy` with a `$space-5` (24px) gap from the hero's vertical layout.
   - `PrimaryCta` is at least 44px tall (the WCAG hit-target check from SKILL.md § Accessibility). Padding `[12, 24, 12, 24]` plus a 16px-tall label gives 40px — *that fails my own check*, so this is exactly the kind of issue rung 2 catches before a screenshot. I would fix it with `U("<cta>", { padding: ["$space-4", "$space-5", "$space-4", "$space-5"] })` (16px top/bottom = 48px total height) and re-snapshot.

3. **Rung 3 — `batch_get({ nodeIds: ["<headline>", "<cta>", "<ctaLabel>"], resolveVariables: false })`.** **What I would check:** `headline.fill` resolves to `"$textPrimary"` (the variable binding survived), not a raw hex; `cta.fill` resolves to `"$accent"`; `ctaLabel.content` is `"Start free trial"`. Property-level confirmation that the tokens are bound, not raw colours.

4. **Rung 4 — `get_screenshot`.** *Skipped for this region.* The hero is straight typography on a neutral surface bound to variables; rungs 2 and 3 already proved structure and bindings landed. No image content (no AI image), no contrast question I cannot resolve from the variable values, no rhythm question that pixels would settle better than numbers.

**What I verified after region 1, in order:**
- `batch_design` response → ops succeeded, 9 bindings returned.
- `snapshot_layout(parentId: "<hero>", maxDepth: 2)` → structure landed; CTA hit-target check caught a 40px height (4px short of 44 minimum). Fixed via `U` op, re-snapshotted, now 48px.
- `batch_get({ nodeIds: ["<headline>", "<cta>", "<ctaLabel>"] })` → variable bindings intact; CTA label matches the user's "primary CTA button" intent.

**Tools used: 1× `batch_design` (build), 1× `batch_design` (CTA fix), 2× `snapshot_layout`, 1× `batch_get`. No screenshot.**

---

## Region 2 — Features (three-column)

### Build

The user explicitly asked for three columns with icon + heading + paragraph each. The skill notes this is the most over-used SaaS pattern, but the brief is explicit, so I will execute it with the rescues from `layout-patterns.md` § Feature sections: *"varied icons, intentional spacing, leave breathing room"*. I will also bind everything to tokens so the spacing rhythm is consistent with the hero, satisfying the user's "clean spacing rhythm" ask.

One `batch_design` call, ~22 ops — close to the ceiling but still inside it. I would split into two calls if I needed any more.

```
features=I(page, {
  type: "frame",
  name: "Features",
  width: "fill_container",
  layout: "vertical",
  alignItems: "center",
  gap: "$space-8",
  padding: ["$space-12", "$space-12", "$space-12", "$space-12"],
  fill: "$surfaceMuted",
  context: "Three-column features section. Icon + heading + paragraph per column. Inner wrapper capped to $maxContent (1200) so the row reads anchored at desktop."
})

featuresInner=I(features, {
  type: "frame",
  name: "FeaturesGrid",
  width: 1200,
  layout: "horizontal",
  alignItems: "stretch",
  justifyContent: "between",
  gap: "$space-6"
})

// Column 1
col1=I(featuresInner, {
  type: "frame",
  name: "FeatureCard_Plan",
  width: "fill_container",
  layout: "vertical",
  gap: "$space-4",
  padding: ["$space-6", "$space-6", "$space-6", "$space-6"],
  fill: "$surface",
  cornerRadius: "$radiusLg",
  stroke: { thickness: 1, fill: "$border" }
})
icon1=I(col1, {
  type: "frame",
  name: "FeatureIcon_Plan",
  width: 40, height: 40,
  layout: "horizontal",
  alignItems: "center", justifyContent: "center",
  fill: "$surfaceMuted",
  cornerRadius: "$radiusSm",
  context: "Icon tile. Replace inner with icon_font (e.g. lucide:calendar) at handoff."
})
h1=I(col1, {
  type: "text",
  name: "FeatureHeading_Plan",
  content: "Plan in plain English",
  fontSize: "$textXl",
  fontWeight: "600",
  lineHeight: 1.3,
  fill: "$textPrimary"
})
b1=I(col1, {
  type: "text",
  name: "FeatureBody_Plan",
  content: "Write what you want. The roadmap updates itself, with dependencies, owners, and rough sizing already filled in.",
  fontSize: "$textBase",
  fontWeight: "400",
  lineHeight: 1.55,
  fill: "$textMuted"
})

// Column 2
col2=I(featuresInner, {
  type: "frame",
  name: "FeatureCard_Build",
  width: "fill_container",
  layout: "vertical",
  gap: "$space-4",
  padding: ["$space-6", "$space-6", "$space-6", "$space-6"],
  fill: "$surface",
  cornerRadius: "$radiusLg",
  stroke: { thickness: 1, fill: "$border" }
})
icon2=I(col2, {
  type: "frame",
  name: "FeatureIcon_Build",
  width: 40, height: 40,
  layout: "horizontal",
  alignItems: "center", justifyContent: "center",
  fill: "$surfaceMuted",
  cornerRadius: "$radiusSm"
})
h2=I(col2, {
  type: "text",
  name: "FeatureHeading_Build",
  content: "Build without the busywork",
  fontSize: "$textXl",
  fontWeight: "600",
  lineHeight: 1.3,
  fill: "$textPrimary"
})
b2=I(col2, {
  type: "text",
  name: "FeatureBody_Build",
  content: "Branch, PR, and ticket all stay in lockstep. Status changes flow from the code, not from a status meeting.",
  fontSize: "$textBase",
  fontWeight: "400",
  lineHeight: 1.55,
  fill: "$textMuted"
})

// Column 3
col3=I(featuresInner, {
  type: "frame",
  name: "FeatureCard_Release",
  width: "fill_container",
  layout: "vertical",
  gap: "$space-4",
  padding: ["$space-6", "$space-6", "$space-6", "$space-6"],
  fill: "$surface",
  cornerRadius: "$radiusLg",
  stroke: { thickness: 1, fill: "$border" }
})
icon3=I(col3, {
  type: "frame",
  name: "FeatureIcon_Release",
  width: 40, height: 40,
  layout: "horizontal",
  alignItems: "center", justifyContent: "center",
  fill: "$surfaceMuted",
  cornerRadius: "$radiusSm"
})
h3=I(col3, {
  type: "text",
  name: "FeatureHeading_Release",
  content: "Release with confidence",
  fontSize: "$textXl",
  fontWeight: "600",
  lineHeight: 1.3,
  fill: "$textPrimary"
})
b3=I(col3, {
  type: "text",
  name: "FeatureBody_Release",
  content: "Roll out gradually, watch the metrics, roll back if anything wobbles. Every release ships with its own escape hatch.",
  fontSize: "$textBase",
  fontWeight: "400",
  lineHeight: 1.55,
  fill: "$textMuted"
})
```

### Verification — region 2

1. **Rung 1 — `batch_design` response.** Confirm 16 bindings returned, all ops succeeded. **What I would check:** no `parent not found` errors (the bindings are sequential within one call, so order is critical).

2. **Rung 2 — `snapshot_layout(parentId: "<features>", maxDepth: 3)`.** Deeper depth than region 1 because the structure is two levels (`Features → FeaturesGrid → FeatureCard → children`). **What I would check:**
   - `FeaturesGrid` is 1200px wide, sitting centred inside the 1440px `Features` frame because of `alignItems: "center"` on the parent.
   - The three feature cards have **equal** computed widths (`fill_container` inside a row with three siblings → each is one-third). Inequal widths would mean one of the cards has a shrinking child overriding the fill.
   - The gap between cards is 24px (`$space-6`); the gap between an icon and its heading inside a card is 16px (`$space-4`).
   - The card heights are stretched equal because of `alignItems: "stretch"` on the parent. If the body copy lengths differ slightly across columns, this is what keeps the cards aligned.
   - `Features` section's vertical position relative to `Hero` — they sit as siblings inside the page's vertical layout, with no gap between them by default. (The page has no `gap` set on the page-frame layout. *That's a question I want to settle structurally now, not after a screenshot.*) **If they butt directly together, I will add `U("<page>", { gap: "$space-12" })` so the section rhythm matches the within-section spacing.**

3. **Rung 3 — `batch_get`.** Skipped for region 2 — there's nothing here that's not visible from snapshot. No variable rebindings, no `descendants` overrides, no AI image. Climbing to rung 3 here would burn payload for no answer.

4. **Rung 4 — `get_screenshot`.** *Skipped for this region.* Equal-width column layout is exactly the kind of thing snapshot resolves better than pixels (numbers don't lie about width parity, but the eye can be fooled by 1-pixel differences).

**What I verified after region 2, in order:**
- `batch_design` response → 16 bindings returned, no ordering errors.
- `snapshot_layout(parentId: "<features>", maxDepth: 3)` → grid widths equal at 384px each (1200 - 2×24 = 1152, ÷3 = 384), row gap 24px, card padding 32px, icons render at 40×40, vertical gap from hero needs adjustment.
- One follow-up `U("<page>", { gap: "$space-12" })` and a re-snapshot of the page-root layout to confirm the inter-section gap is now 96px.

**Tools used: 1× `batch_design` (build), 1× `batch_design` (page gap fix), 2× `snapshot_layout`. No screenshot, no `batch_get`.**

---

## Region 3 — Footer

### Build

Minimal footer architecture (`layout-patterns.md` § Footer architectures): copyright on the left, three text links on the right, a thin divider above. One `batch_design` call, ~10 ops.

```
footer=I(page, {
  type: "frame",
  name: "Footer",
  width: "fill_container",
  layout: "vertical",
  gap: "$space-4",
  padding: ["$space-6", "$space-12", "$space-6", "$space-12"],
  fill: "$surface",
  context: "Page footer. Minimal architecture: divider + copyright row. No sitemap, no newsletter signup."
})

divider=I(footer, {
  type: "rectangle",
  name: "FooterDivider",
  width: "fill_container",
  height: 1,
  fill: "$border"
})

footerRow=I(footer, {
  type: "frame",
  name: "FooterRow",
  width: "fill_container",
  layout: "horizontal",
  alignItems: "center",
  justifyContent: "between",
  gap: "$space-5"
})

copyright=I(footerRow, {
  type: "text",
  name: "Copyright",
  content: "© 2026 Acme Labs. All rights reserved.",
  fontSize: "$textSm",
  fontWeight: "400",
  fill: "$textMuted"
})

links=I(footerRow, {
  type: "frame",
  name: "FooterLinks",
  layout: "horizontal",
  gap: "$space-5",
  alignItems: "center"
})

link1=I(links, {
  type: "text",
  name: "FooterLink_Privacy",
  content: "Privacy",
  fontSize: "$textSm",
  fontWeight: "500",
  fill: "$textPrimary",
  href: "#",
  context: "Footer link. Hover state defers to .lib.pen extraction. Tap target padded by parent gap."
})

link2=I(links, {
  type: "text",
  name: "FooterLink_Terms",
  content: "Terms",
  fontSize: "$textSm",
  fontWeight: "500",
  fill: "$textPrimary",
  href: "#"
})

link3=I(links, {
  type: "text",
  name: "FooterLink_Contact",
  content: "Contact",
  fontSize: "$textSm",
  fontWeight: "500",
  fill: "$textPrimary",
  href: "#"
})
```

Then I'd remove the placeholder flag from the page since the build is finished:

```
U("<page>", { placeholder: false })
```

### Verification — region 3

1. **Rung 1 — `batch_design` response.** Confirm 8 footer bindings + 1 placeholder-clearing op succeeded.

2. **Rung 2 — `snapshot_layout(parentId: "<footer>", maxDepth: 2)`.** **What I would check:**
   - `FooterRow` is `fill_container`, so it stretches to the inner width (1440 - 2×96 padding = 1248px).
   - `Copyright` sits flush left, `FooterLinks` sits flush right, gap-justified by `justifyContent: "between"`.
   - The three link nodes inside `FooterLinks` have a 24px gap between them.
   - The divider is 1px high and spans the inner width.

3. **Rung 3 — `batch_get({ nodeIds: ["<copyright>", "<link1>", "<link2>", "<link3>"] })`.** **What I would check:** the copyright text matches the `© 2026 Acme Labs…` content I sent (no encoding mangling on the `©`); each link has `href: "#"` set so the engineer knows to wire real URLs; each link's `fill` resolves to `$textPrimary`.

4. **Rung 4 — `get_screenshot`.** *Saved for the page-root final sign-off below.*

**What I verified after region 3, in order:**
- `batch_design` response → 9 ops succeeded (8 footer + 1 placeholder clear).
- `snapshot_layout(parentId: "<footer>", maxDepth: 2)` → row spans inner 1248px, copyright flush left, links flush right, link gap 24px, divider 1px × 1248px.
- `batch_get({ nodeIds: ["<copyright>", "<link1>", "<link2>", "<link3>"] })` → text content matches the brief, all three links carry `href: "#"`, fills bound to `$textPrimary`.

**Tools used: 1× `batch_design` (build + placeholder clear), 1× `snapshot_layout`, 1× `batch_get`. No screenshot.**

---

## Final visual sign-off

One screenshot, scoped to the page frame, as the only screenshot of the build:

```
get_screenshot({ nodeId: "<page>" })
```

**Why one and only one.** The verification cadence rule from SKILL.md says *"a typical end-to-end design task should need one or two screenshots total"*. The dual-mode rule says I do not need a second screenshot in dark mode because every colour I bound is a `$variable` with both `mode: light` and `mode: dark` values declared in step 3c — the variable system guarantees parity, so a second screenshot would just confirm what the token suite already proves.

**What I would scan in the screenshot, in order** (per the verification ladder § Screenshot-scan checklist):

1. **Layout integrity** — page holds together at 1440×900? Hero centred, features aligned, footer pinned at the page foot?
2. **Spacing rhythm** — 96px between sections, 32px card padding, 24px column gap. Each one is bound to the same token scale, so they should read as one rhythm.
3. **Type rhythm** — H1 (56px) → feature heading (20px) → body (16px) → footer body (14px). The 56→20 jump is large by design (display vs supporting) and should not feel choppy because subhead (18px) sits between them in the hero.
4. **Contrast** — `$textPrimary` (zinc-950 / `#0B1117`) on `$surface` (zinc-50 / `#FAFAFA`) is well above 4.5:1; `$textMuted` (`#52525B`) on `$surface` is approximately 7.4:1, also above. `$accent` (`#1F6FEB`) on `$accentText` (`#FFFFFF`) for the CTA is about 4.8:1 — passes AA for normal text. *I would flag this one to the user as "passes AA but not AAA; if you need AAA, deepen the accent to roughly `#1A5CC2`".*
5. **Component fidelity** — N/A for this build (no library imported, nothing to drift from).

If the screenshot surfaced anything off — for instance, the H1 wrapping mid-line into an orphan ("faster.") — I would fix it with a `U` op (`text-wrap: balance` is documented in `context`, but for the static screenshot I might also tighten the headline's `width` to nudge the wrap point) and re-snapshot the affected subtree. I would not re-screenshot unless the change was visual.

---

## Component-extraction prompt to the user

Per the Components-first rule, after the build I would say to the user:

> *"Three patterns in this page repeat enough to warrant extraction: the primary CTA button (which I'd want to give hover/focus/disabled states), the feature card (icon + heading + body, three of them right now), and the footer link. If you want, I can pull these into `./design/system.lib.pen` so any future page on this design system instantiates them as `ref` nodes instead of being hand-built each time. That also lets me give the CTA proper component states. Worth doing?"*

I would not extract them unprompted — premature extraction is its own bug.

---

## Aggregate verification summary

Across the three-region build I would make **eight verification calls** broken down by tool type:

- **`batch_design` response inspection (rung 1):** five calls — one build per region (3), plus the CTA hit-target fix in region 1 and the page-gap fix in region 2. Free; comes back inline with the write.
- **`snapshot_layout` (rung 2):** five calls — one structural confirm per region (3), plus the two re-snapshots after the rung-1 fixes. The default workhorse here, and the reason I avoided most screenshots.
- **`batch_get` (rung 3):** two calls — one in region 1 to confirm hero token bindings (`$textPrimary` / `$accent` / CTA label), one in region 3 to confirm footer text content and link `href`s. Region 2 didn't need rung 3 because it had no overrides or refs to verify.
- **`get_screenshot` (rung 4):** one call, scoped to the page frame, as the final visual sign-off. Skipped per-region screenshots because the structural snapshots and property reads already proved the design landed; skipped a dark-mode screenshot because every colour is bound to a `$variable` with both light and dark values, so the token system guarantees parity. Total screenshot count for the build: **one**, which is in line with the SKILL guidance of "one or two screenshots total" for a typical end-to-end design task.

Including the bootstrap calls (`get_editor_state`, `open_document`, `get_guidelines` ×2 if loaded, `get_variables`, the theme-axis `batch_design`, and `set_variables`), the full session is ~14 MCP calls before counting the writes themselves — most of them small. The expensive call (the screenshot) ran exactly once.
