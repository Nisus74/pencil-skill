# Three-tier pricing card section (Free / Pro / Team)

This is the design plan I would execute against the open `.pen` document. Below I describe the references I consulted, the tools I would call, the arguments, the response shape I would expect, and what I would verify.

---

## References consulted

- `SKILL.md` — discipline rules (naming, context, components-first, themes, responsive, accessibility, file architecture) and aesthetic defaults (two-role colour, layered shadows, typography, optical precision, anti-patterns, self-critique gate). Required for every task.
- `assets/examples/example-pricing-table.md` — directly addresses this brief (Free/Pro/Team with Pro highlighted). Owns the canonical highlighted-tier treatment (coloured border + badge), the per-tier microcopy, mobile stack order, and dual-mode verification.
- `references/layout-patterns.md` § Pricing tables — confirms three-tier with highlighted middle is the right pattern for SaaS Free/Pro/Team and pins the rule "coloured border + badge, never all four treatments combined".
- `references/colour-palettes.md` § Two-role architecture refresher — neutral family + one accent only; the highlight uses the existing `$accent`, never a second hue introduced for the badge.
- `references/batch-design-grammar.md` — op syntax, the `foo=I(...)` binding form, the `≤25 ops per call` rule, the `padding: [t, r, b, l]` array (no `paddingTop`), bare-string sizing (`"fill_container"` / `"fit_content"`), and the placeholder-frame lifecycle for top-level frames.
- `references/microcopy.md` (skim, via the example) — action-specific CTAs ("Start free" / "Start Pro trial" / "Contact sales"), not "Get started" / "Continue".

I did *not* load `mobile-patterns.md`, `forms.md`, `data-viz.md`, or `flows.md`. None of those carries the pricing-card section the user asked for; loading them would burn context for nothing.

---

## Step 1 — Detect host and locate context

```js
get_editor_state({ include_schema: false })
```

Expected response shape:

```json
{
  "documentId": "doc_xxx",
  "filePath": "/Users/.../marketing.pen",
  "selection": [],
  "imports": { "ds": "./design/system.lib.pen" },   // or empty
  "themes": { "mode": ["light", "dark"] },          // or absent on a fresh doc
  "schemaVersion": "..."
}
```

What I check: is a `.pen` open at all? If `transport not connected to app: desktop` comes back, I stop and ask the user to open the desktop app or IDE extension — no silent CLI fallback (Failure mode 1). If no document is open, I ask whether to open an existing one or create new (Failure mode 2). If a document is open, I note the imports list and the themes.

In parallel, I check the project filesystem (directory listing — not via MCP) for `./design-system/`. If present, I read `README.md`, then `design-system.md` and `tokens.md` for the project's `.lib.pen` path, icon library, and token names. If absent and this is real project work, I offer the scaffold once (Failure mode 3) — but for an isolated pricing section I'd proceed without if the user just wants the design.

## Step 2 — Load guidelines and inventory components

```js
get_guidelines({})
```

Returns the categories available for this document (e.g. `Web App`, `Landing Page`, `Tailwind`, `Design System`). I'd read the `Landing Page` and `Design System` categories — pricing sits in the marketing surface and the highlighted card needs to honour the project's token / component conventions.

Then the components-first inventory — both passes:

```js
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

What I'm looking for in the response:

- Existing pricing components — `Card_Pricing`, `Card_Pricing_Highlighted`, `PricingTier`, `PricingCard`, anything close.
- Generic primitives I'll need either way — `Button` (Primary / Secondary variants), `Badge`, `Icon` (the project's icon library, e.g. Lucide for `check`).
- Token names — `$accent`, `$surface`, `$surfaceMuted`, `$border`, `$textPrimary`, `$textMuted`, `$radiusLg`, `$shadowAmbient`, `$shadowDirect` (or the project's equivalents).

If `Card_Pricing` and `Card_Pricing_Highlighted` already exist, I instantiate them with `ref` nodes and three `descendants` overrides (the Free/Pro/Team example file walks this exact path). If only a generic `Card` exists, I build the pricing-card structure inline and surface it: *"This pricing card pattern looks reusable — should I add `Card_Pricing` and `Card_Pricing_Highlighted` to your `.lib.pen`?"* If nothing exists, I build from primitives and offer the same.

I'd also confirm `$accent` exists in the document with both light and dark theme values:

```js
get_variables({})
```

Why: the highlighted treatment binds the border colour to `$accent`. If the document has tokens but no `$accent`, the project may name it `$brand`, `$primary`, or similar — I use whatever the existing token name is. I never re-declare a variable (`set_variables` with the same key silently overwrites existing values, per the SKILL token-clobber failure mode).

## Step 3 — Find canvas space (if the canvas is populated)

```js
find_empty_space_on_canvas({ width: 1440, height: 760 })
```

Returns `{ x, y }` for an open coordinate. If the canvas is empty, I default to `(0, 0)` adjacent to the Cover frame in the SourceOfTruth section. Skipping this on a populated canvas creates invisible overlaps that look like rendering bugs.

## Step 4 — Plan (state out loud before any `batch_design` call)

> "Building a `Pricing` section frame at the desktop breakpoint (1440 wide, ~760 tall). One row, three equal cards (`PricingRow` with `gap: 24`). Free and Team use a plain card treatment; Pro uses the highlighted treatment — coloured border in `$accent` (2px) plus a 'Most popular' badge anchored top-right. One layered shadow (ambient + direct, two layers) on Pro only. Two-role colour: `$surface` for the cards, `$accent` for the highlight. Atmosphere: balanced / symmetric / static — pricing reads best in calm symmetry, not chaos."

This commits the vibe in one line per the SKILL aesthetic defaults, names the components I'll instantiate, and pre-empts the four most common AI tells: pure black/white surfaces, a second competing accent for the badge, three identical cards with no highlight, and an unlayered single-drop shadow.

## Step 5 — Execute (split across two `batch_design` calls)

### Call A — section skeleton (≤10 ops)

```
section=I(document, { type: "frame", name: "Pricing", placeholder: true, x: <free>, y: <free>, width: 1440, height: "fit_content", layout: "vertical", padding: [96, 120, 96, 120], gap: 48, alignItems: "center", fill: "$surfaceMuted", context: "Three-tier pricing section (Free / Pro / Team). Pro is the highlighted recommended tier: coloured border using $accent + 'Most popular' badge. Two-role colour ($surface + $accent only). Layered shadow (ambient + direct) on Pro only. Mobile stack: cards stack vertically, Pro stays second so highlight remains in the visual flow." })
header=I(section, { type: "frame", name: "PricingHeader", layout: "vertical", gap: 12, alignItems: "center", width: "fill_container", maxWidth: 720 })
title=I(header, { type: "text", name: "PricingTitle", content: "Pick the plan that fits your team", fontFamily: "$fontDisplay", fontSize: "$text4xl", fontWeight: "$fontWeightBold", fill: "$textPrimary", textAlign: "center" })
sub=I(header, { type: "text", name: "PricingSubtitle", content: "Start free. Upgrade when you outgrow it. All plans include unlimited projects.", fontSize: "$textLg", fill: "$textMuted", textAlign: "center" })
row=I(section, { type: "frame", name: "PricingRow", layout: "horizontal", gap: 24, alignItems: "stretch", width: "fill_container", maxWidth: "$maxContent" })
```

Why this shape:

- `placeholder: true` on the section frame because it's a top-level frame (per the batch-design-grammar placeholder rule). I'll flip it to `false` after Call B.
- `padding: [96, 120, 96, 120]` is a 4-value array, not `paddingTop` — that property doesn't exist (common error in the grammar reference).
- `width: "fill_container"` on the row only works because the parent (section) has flex layout; the parent has `layout: "vertical"`, so this is valid.
- `maxWidth: "$maxContent"` so the row caps at the project's content width (default 1200).
- The header copy is action-grounded and avoids "Elevate", "Seamless", "Unleash" (anti-patterns list).
- `context` documents intent — what the highlighted treatment is, why two-role colour, mobile behaviour. Not visual specs the schema already captures.
- `text-wrap: balance` is implicit in headlines per the typography defaults; if the project's text node supports it as a property I'd add `textWrap: "balance"` on the title.

### Call B — three pricing cards (≤21 ops if components exist, ≤45 if hand-built)

**Path 1 — `Card_Pricing` and `Card_Pricing_Highlighted` exist in the library:**

```
free=C("Card_Pricing", row, { descendants: { tier: { content: "Free" }, price: { content: "$0" }, period: { content: "forever" }, description: { content: "For trying things out." }, ctaLabel: { content: "Start free" }, ctaVariant: "Secondary", "features/0": { content: "Up to 3 projects" }, "features/1": { content: "Unlimited members" }, "features/2": { content: "Community support" }, "features/3": { content: "1 GB storage" } } })
pro=C("Card_Pricing_Highlighted", row, { descendants: { tier: { content: "Pro" }, price: { content: "$12" }, period: { content: "per user / month" }, description: { content: "For growing teams." }, badge: { content: "Most popular" }, ctaLabel: { content: "Start Pro trial" }, ctaVariant: "Primary", "features/0": { content: "Everything in Free" }, "features/1": { content: "Unlimited projects" }, "features/2": { content: "Priority support" }, "features/3": { content: "100 GB storage" }, "features/4": { content: "Custom roles & permissions" }, "features/5": { content: "Audit log" } } })
team=C("Card_Pricing", row, { descendants: { tier: { content: "Team" }, price: { content: "$24" }, period: { content: "per user / month" }, description: { content: "For teams that need scale." }, ctaLabel: { content: "Contact sales" }, ctaVariant: "Secondary", "features/0": { content: "Everything in Pro" }, "features/1": { content: "SSO + SCIM" }, "features/2": { content: "SLA 99.9%" }, "features/3": { content: "Dedicated CSM" }, "features/4": { content: "Custom contract" }, "features/5": { content: "1 TB storage" } } })
U(section, { placeholder: false })
```

Why `C` not `I` with `type: "ref"`: `C` (copy) of a `reusable: true` component creates a live ref instance — same effect, lighter syntax for descendants overrides. Either works; I'd use `C` for brevity here.

The `"features/0"` syntax is the descendants path form — see `references/component-anatomy.md`. If the highlighted component uses a single repeating slot, I'd use that slot name instead.

**Path 2 — only a generic `Card` exists; build pricing-card content inline.** I'd build one card from primitives, instance it three times via `C`, then customise each. Roughly:

```
freeCard=I(row, { type: "frame", name: "PricingCard_Free", layout: "vertical", gap: 24, padding: [32, 28, 32, 28], width: "fill_container", fill: "$surface", border: { width: 1, fill: "$border" }, cornerRadius: 16, context: "Free tier card. Plain treatment (no highlight). Action-specific CTA: 'Start free'." })
freeHeader=I(freeCard, { type: "frame", name: "Header", layout: "vertical", gap: 8 })
freeTier=I(freeHeader, { type: "text", name: "Tier", content: "Free", fontSize: "$textLg", fontWeight: "$fontWeightSemibold", fill: "$textPrimary" })
freePriceRow=I(freeHeader, { type: "frame", name: "PriceRow", layout: "horizontal", gap: 6, alignItems: "baseline" })
freePrice=I(freePriceRow, { type: "text", name: "Price", content: "$0", fontFamily: "$fontDisplay", fontSize: "$text5xl", fontWeight: "$fontWeightBold", fill: "$textPrimary", textVariantNumeric: "tabular-nums" })
freePeriod=I(freePriceRow, { type: "text", name: "Period", content: "forever", fontSize: "$textSm", fill: "$textMuted" })
freeDesc=I(freeCard, { type: "text", name: "Description", content: "For trying things out.", fontSize: "$textSm", fill: "$textMuted" })
freeDivider=I(freeCard, { type: "rectangle", name: "Divider", height: 1, width: "fill_container", fill: "$border" })
freeFeatures=I(freeCard, { type: "frame", name: "Features", layout: "vertical", gap: 12 })
// ...four feature rows (icon "check" + text)
freeCTA=I(freeCard, { type: "ref", ref: "Button", descendants: { label: { content: "Start free" } }, variant: "Secondary", width: "fill_container" })
```

Then `proCard=C(freeCard, row, { ...overrides for the highlighted treatment })`, and `teamCard=C(freeCard, row, { ...overrides for Team })`. The Pro overrides:

```
proCard=C(freeCard, row, { name: "PricingCard_Pro", border: { width: 2, fill: "$accent" }, shadow: [{ x: 0, y: 1, blur: 2, fill: "rgba(0,0,0,0.06)" }, { x: 0, y: 8, blur: 24, fill: "rgba(0,0,0,0.10)" }], context: "Pro tier — recommended. Highlighted treatment: 2px $accent border + 'Most popular' badge anchored top-right. Two layered shadows (ambient + direct, per SKILL.md § Shadows). No scale-up; the border + badge pair is plenty (per layout-patterns.md § Pricing tables — never all four treatments)." })
proBadge=I(proCard, { type: "frame", name: "Badge", layout: "horizontal", padding: [4, 10, 4, 10], cornerRadius: 999, fill: "$accent", x: <calc>, y: -12 })
proBadgeText=I(proBadge, { type: "text", content: "Most popular", fontSize: "$textXs", fontWeight: "$fontWeightSemibold", fill: "$accentForeground" })
```

(The badge sits absolutely positioned relative to the card. If the project's card component has a dedicated `badge` slot, I use that instead of absolute positioning.)

Two important constraints I'm honouring:

- **Two-role colour.** Cards are `$surface`, the highlight is `$accent` — both the border *and* the badge fill use the same `$accent`. Adding a green badge to an `$accent`-bordered card would read as two competing hues.
- **Layered shadow on Pro only.** Two layers (ambient `0 1px 2px rgba(0,0,0,0.06)` + direct `0 8px 24px rgba(0,0,0,0.10)`). A single 40%-opacity drop is the AI default (anti-pattern). Free and Team get the 1px `$border` and no shadow — restraint is the contrast that makes the highlight read.
- **Nested radius.** Card is `cornerRadius: 16`; the badge is `cornerRadius: 999` (pill); the inner button (a ref) inherits its own radius from the library, which should already be ≤ 16 minus padding. I'd verify with a snapshot if I built buttons inline.
- **Tabular numerics.** Prices use `textVariantNumeric: "tabular-nums"` so `$0`, `$12`, `$24` align by digit width — three cards of different prices look ragged otherwise.
- **Dark mode.** Because every colour is a `$variable` with both `light` and `dark` values, dark mode is automatic. I do not need a second screenshot to confirm — the variable system guarantees it (per the SKILL dual-mode rule).

After Call B I flip the placeholder: `U(section, { placeholder: false })`.

## Step 6 — Verify (structural-first ladder)

I climb the verification ladder, stopping at the cheapest rung that answers each question.

**Rung 1 — `batch_design` response.** Confirms each op landed and surfaces any schema errors. Free.

**Rung 2 — `snapshot_layout`:**

```js
snapshot_layout({ parentId: "<row id>", maxDepth: 2 })
```

What I check in the returned numbers:

- All three cards have equal width (the `width: "fill_container"` resolved correctly under the row's `gap: 24`).
- Pro card's border width is `2`; Free and Team are `1`.
- Pro card's height equals the others (the highlighted treatment shouldn't grow the card — only one card scaling up looks accidental, per layout-patterns).
- The 24px gap is honoured.
- Badge positioned at the top-right of Pro (negative `y` offset of ~12px so it overlaps the border).

**Rung 3 — `batch_get`:**

```js
batch_get({ nodeIds: ["<pro card id>", "<pro badge id>", "<pro CTA id>"], readDepth: 2 })
```

What I check:

- `border.fill` resolves to `$accent` (not a raw hex). If it's a raw hex, the dark-mode variant won't follow.
- `shadow` is an array of two entries, not one.
- Badge `fill` is `$accent` (same token as the border — two-role rule).
- CTA `variant` is `Primary` on Pro; `Secondary` on Free and Team.
- CTA labels read "Start free" / "Start Pro trial" / "Contact sales" — none are "Get started" or "Continue".

**Rung 4 — `get_screenshot` (one shot, scoped to the section):**

```js
get_screenshot({ nodeId: "<section id>" })
```

This is the final visual sign-off. Scoped to the section, not the page — pricing has its own visual rhythm separate from the rest of marketing. I scan the rendered image in the order from the verification ladder:

1. **Layout integrity** — three cards visible, equal-width, no overflow.
2. **Spacing rhythm** — 24px between cards, 96px section padding top/bottom, 12px gap inside the header.
3. **Type rhythm** — `$5xl` price > `$lg` tier name > `$sm` description, in that order.
4. **Contrast** — body text passes 4.5:1 against `$surface`; the badge text passes against `$accent`; muted period text passes 4.5:1 against `$surface` (period is `$textSm` so still body, not large text).
5. **Component fidelity** — buttons are refs to the library `Button`, not hand-built lookalikes drifting from the system.

I do **not** screenshot dark mode. The cards are built entirely from variables with both light and dark values, so the theme system guarantees the result. The dual-mode rule says: re-screenshot only if I have reason to suspect a raw hex slipped in.

If something's off, I issue targeted `U` ops against the offending node, re-snapshot (rung 2 or 3), and only re-screenshot for the very last sign-off if a visual issue specifically remains.

## Step 7 — Self-critique gate (60 seconds before declaring done)

Before reporting back to the user, I run the four-question gate from the SKILL aesthetic defaults:

1. **Could a non-designer recognise the brand voice or industry?** If the project has a `voice.md` and a strong palette, the pricing section should read as that brand. If everything reads generic, I revisit the headline copy and the accent choice.
2. **Where does the eye go first / second / third?** The Pro card should land first (border + badge), the price tier names second, the CTAs third. Trace the path. If the badge competes with the headline, the badge is too loud — soften it (or move it inside the card body).
3. **What's decorative-only?** Stripe-y backgrounds, gradient text on the price, glow shadows — all anti-patterns. Strip if present.
4. **What single change would make this feel less AI-generated?** Common fixes: vary the card heights subtly (Pro 4–8px taller via padding, not scale), use a custom check icon instead of the default Lucide check, anchor the badge to overlap the top edge rather than sitting flush inside.

Fix what surfaces; do not note as a TODO.

## Step 8 — Report

Once verification is clean, I summarise back to the user in one paragraph:

> "Pricing section landed at `<x, y>` on the canvas: three-tier (Free / Pro / Team) with Pro highlighted via a 2px `$accent` border and a 'Most popular' badge anchored top-right. Layered shadow (ambient + direct) on Pro only. CTAs are action-specific: 'Start free' / 'Start Pro trial' / 'Contact sales'. Two-role colour throughout (`$surface` + `$accent`). Theme-aware via variables — dark mode follows automatically. Mobile stack will need a separate frame at the 390 breakpoint with cards in a vertical column, Pro positioned second so the highlight stays in the visual middle. Want me to build the mobile and tablet frames as siblings now?"

---

## Failure modes I'd watch for

- **MCP not connected.** `get_editor_state` errors with `transport not connected`. Stop, ask the user to open the Pencil app or IDE extension. No silent CLI fallback.
- **Token clobber.** If the document already has `$accent` defined, calling `set_variables({ accent: ... })` overwrites it. I always call `get_variables()` first and only set absent keys.
- **`paddingTop` schema error.** The schema rejects `paddingTop` / `paddingLeft` / etc. I always use the 4-value `padding: [t, r, b, l]` array.
- **`width: "100%"` schema error.** The schema accepts only bare-string `"fill_container"` / `"fit_content"` (or numbers). Not `"100%"`, not `{ sizing: "fill_container" }` (the older object form is rejected by the live server).
- **`/` in node id.** Slashes are forbidden in `id` (allowed in descendants paths and frame `name` only).
- **Badge using a second hue.** The most common AI tell on this exact pattern. The badge fill must be the same `$accent` as the card border.

---

## Output artifact

Saved to `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-7-shadow-and-color-architecture/with_skill/outputs/response.md`.
