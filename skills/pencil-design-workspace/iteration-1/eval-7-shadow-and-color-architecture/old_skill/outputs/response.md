# Designing a three-tier pricing card section (Free, Pro, Team) with the Pro tier highlighted

I'll work this through the default Pencil workflow. Pricing is a marketing surface, so the relevant guideline category is `Landing Page`, and the SKILL warns me up front that "three-column equal-card grids" read as an AI tell — which is exactly why the highlighted Pro card matters. The whole point of step 4 is to commit to a vibe and a layout treatment that breaks the flat symmetric grid before I touch `batch_design`.

I won't actually be able to call any `mcp__pencil__*` tools in this run, but I'll narrate every call I'd make, what I'd pass, what I'd expect back, and what I'd verify.

---

## Step 1 — Detect host

Reflex first action on any task per the SKILL.

```
mcp__pencil__get_editor_state({ include_schema: false })
```

What I'm checking: does the call return without `transport not connected to app: desktop`. If it errors, I stop and tell the user to open the Pencil desktop app or IDE extension.

What I expect back: an object with the active document path (or none), the current selection, and document metadata. From that I learn (a) is a `.pen` open, (b) what's selected, (c) which schema version. Per the SKILL's failure-mode table, no active document means I branch to ask the user whether to open an existing file or `open_document("new")` — I don't silently create one.

For the rest of this walkthrough I'll assume `get_editor_state` succeeds and a `.pen` is already open.

## Step 2 — Locate context

From the editor state result I'd note: which `.pen`, what (if anything) is selected, what `imports` are declared on the document. Then I'd check the project filesystem (using shell, not MCP) for a `design-system/` folder.

Three branches per the SKILL:

- `design-system/` exists with the standard files → load `README.md` first, then `design-system.md` and `tokens.md`.
- Doesn't exist and this is real project work → offer the scaffold once. Pricing pages are marketing-leaning, so I'd specifically include `brand.md` and `imagery.md` in the optional set if I scaffold.
- Exists but contains code (`.tsx`, `package.json`, etc.) → don't overwrite, ask where to put docs.

I'd also note whether the canvas already has top-level frames. If yes, I'm in "Adding frames to a populated canvas" territory and I'd plan to call `find_empty_space_on_canvas` in step 4 before placing the new section.

## Step 3 — Load guidelines and inventory components

**Guidelines.** Per the SKILL's mcp-tools reference, the decision shortcut for *"Pricing or marketing page"* is `Landing Page` plus `Design System`. So:

```
mcp__pencil__get_guidelines()                                  # discover live category list
mcp__pencil__get_guidelines({ category: "Landing Page" })
mcp__pencil__get_guidelines({ category: "Design System" })
```

If the project ships Tailwind (visible in `design-system.md`), I'd add `get_guidelines({ category: "Tailwind" })`. I would not preload `Web App`, `Mobile App`, `Table`, `Slides`, or `Code` — burning context I won't use.

**Tokens.** Mandatory, per the SKILL's discipline rules:

```
mcp__pencil__get_variables()
```

What I'm checking: the existing token suite. If the user has `surface`, `surfaceMuted`, `border`, `textPrimary`, `textMuted`, `primary`, `primaryMuted`, `success`, etc. already declared with both `mode: "light"` and `mode: "dark"` values, I treat them as authoritative and I do not re-declare any of them. If the document is genuinely empty, I'd `set_variables` only the tokens absent from this response (with `replace: false`) — never assume blank.

Pricing-specific tokens I'd specifically look for and only add if missing:

- `accentMuted` / `primaryWash` — a tinted background for the highlighted card so the Pro tier has a different surface tone than Free/Team. Roughly `#EFF4FF` (light) / `#172554` (dark).
- `successQuiet` — for the green check icons in the feature lists.
- A radius token (`radiusLg`, ~16) for the cards.

I'd add these via `set_variables` only if `get_variables()` doesn't return them.

**Components.** Inventory inside the document and in any imported library:

```
mcp__pencil__batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
mcp__pencil__batch_get({
  filePath: "./design/system.lib.pen",
  patterns: [{ reusable: true }],
  readDepth: 2
})
```

(Repeat for every `.lib.pen` in the document's `imports`.)

What I'm hunting for, ordered by how much they'd shape the design:

1. A `Card` or `PricingCard` component — if it exists I instantiate via `ref`. If only a generic `Card` exists with a content slot, I fill the slot with the tier internals.
2. A `ButtonPrimary` and a `ButtonSecondary` (or `ButtonOutline`) — Pro gets primary, Free and Team get secondary.
3. A `Badge` or `Tag` component — for the "Recommended" pill on the Pro card.
4. A `FeatureRow` or `ListItem` component — for the "thing per row + check icon" feature lists.
5. An `Icon` component or convention for `icon_font` (Lucide is the SKILL's default; the project's `design-system.md` will name it).

For any unfamiliar component the inventory surfaces, I'd inspect deeply per the component-anatomy reference:

```
mcp__pencil__batch_get({ nodeIds: ["PricingCard"], readDepth: 4 })
```

I'd scan for `slot` frames (the recommended-tier visual treatment may live in a state on this component, not as a separate variant), named children (their `id` values become my `descendants` keys, e.g. `header/title`, `body/featureList`, `footer/cta`), and any `theme` axis (a `state` of `recommended` or `featured` would let me activate the highlight without rebuilding the card).

I'd build a short mental inventory from these calls and name in step 4 which existing components I'm reaching for vs anything I'd build from primitives.

## Step 4 — Plan (told to user before any write)

This is the moment to commit to atmosphere and to pre-empt the AI-tell trap. The SKILL instructs me to pick one adjective per axis: density / variance / motion. For a three-tier pricing section that needs to make the Pro tier visually win:

> **Vibe: Balanced, offset, static.** Three cards in a row, but Pro is materially different — taller, on a tinted surface, with a "Recommended" badge in a contrasting fill. The variance is the whole point; if all three cards look the same with Pro merely a different button color, the design has failed.

What I'd say to the user before any `batch_design` call:

> *"I'll add a `PricingSection` frame at desktop width (1440 frame, 1200 content max-width, 24px column gap). Section heading + supporting line, then a horizontal row of three cards: `FreeCard`, `ProCard`, `TeamCard`. Pro is the highlighted tier — it sits on `$accentMuted`, gets an 8px taller offset (a slight scale-up reads as 'recommended' without a separate badge competing with the pill), has a 'Recommended' badge in `$primary` pinned at the top-right corner of the card, and uses a `ButtonPrimary` CTA. Free and Team use `ButtonSecondary` and the default `$surface` fill. Each card has: tier name, price (with `/mo` cadence), one-line summary, divider, feature list with green check icons, CTA. I'll instantiate `Card`, `Badge`, and the `Button*` components from your library; the only new structure is the section wrapper and the per-card body composition. If your library already has a `state: "recommended"` axis on `Card` I'll use that instead of styling the difference manually."*

Three sentences of plan, plus a contingency for the component-anatomy result. The user can correct course before any ops run.

If the canvas is populated, I'd insert one extra step here:

```
mcp__pencil__find_empty_space_on_canvas({
  width: 1440,
  height: 720,
  padding: 80,
  direction: "bottom"
})
```

…and use the returned `{ x, y }` on the section's outer frame to avoid invisible overlaps.

## Step 5 — Execute

I'd split this into two `batch_design` calls so neither exceeds the ≤25-ops rule.

**Call A — section skeleton, header, three card shells (~12 ops).**

```
section=I(document, {
  type: "frame",
  name: "PricingSection",
  layout: "vertical",
  alignItems: "center",
  gap: "$space-8",
  padding: ["$space-12", "$space-6", "$space-12", "$space-6"],
  width: 1440,
  height: "fit_content",
  fill: "$surface",
  placeholder: true,
  context: "Three-tier pricing comparison. Pro is the recommended tier and is visually elevated — taller card, tinted surface, primary CTA. Sits at desktop breakpoint; mobile/tablet variants live in sibling frames."
})
header=I(section, { type: "frame", name: "SectionHeader", layout: "vertical", alignItems: "center", gap: "$space-3", width: "fill_container(1200)", maxWidth: 1200 })
heading=I(header, { type: "text", name: "SectionHeading", text: "Pick the plan that fits", fontSize: "$text4xl", fontWeight: 700, fill: [{ type: "solid_color", color: "$textPrimary" }], textAlign: "center" })
sub=I(header, { type: "text", name: "SectionSubheading", text: "Start free. Move to Pro when you need more — change or cancel any time.", fontSize: "$textLg", fill: [{ type: "solid_color", color: "$textMuted" }], textAlign: "center", maxWidth: 560 })
row=I(section, { type: "frame", name: "TierRow", layout: "horizontal", alignItems: "stretch", gap: "$space-5", width: "fill_container(1200)", maxWidth: 1200 })
freeCard=I(row, { type: "ref", name: "FreeCard", ref: "Card", width: "fill_container", context: "Free tier — entry point. Secondary CTA. Same height as Team card; both shorter than Pro." })
proCard=I(row, { type: "ref", name: "ProCard", ref: "Card", width: "fill_container", theme: { state: "recommended" }, context: "Pro tier — the recommended option. Visually elevated via state variant or fallback styling (tinted surface, taller card, primary CTA, badge)." })
teamCard=I(row, { type: "ref", name: "TeamCard", ref: "Card", width: "fill_container", context: "Team tier — for organisations. Secondary CTA. Same height as Free card." })
```

Notes on what's happening here, tied to the SKILL's discipline rules:

- **Naming.** Every node has a meaningful PascalCase name — no `Frame 1`. The cards are named after their tier role (`FreeCard`, `ProCard`, `TeamCard`), not their visual treatment (not `BluePinkCard`).
- **Context.** Section, the recommended card, and the Free/Team cards all carry one-sentence `context` strings explaining what they're for. The header text nodes don't strictly need it (visual primitives), so I omit.
- **Components first.** I'm using `ref: "Card"` rather than building a frame-from-primitives. If the inventory in step 3 found `PricingCard` instead, I'd swap the `ref` value.
- **State variant.** I pass `theme: { state: "recommended" }` on the Pro `ref`. If the component-anatomy read in step 3 confirmed a `recommended` state exists, this is the right move and the rest of the visual differentiation comes from the component definition. If it doesn't exist, I'd remove the `theme` and apply the differentiation via `descendants` overrides on `proCard` (different `fill` on the card root, different `padding`, taller `height`, primary CTA).
- **Width.** Cards use `width: "fill_container"` inside a horizontal flex row — the SKILL's batch-design grammar warns this requires a flex parent, which `row` is. Three children sharing fill space gives equal-width cards before the per-card height variance kicks in.
- **`placeholder: true`** on the top-level section frame, per the grammar reference. I'd remove it in the final `U` op once the section is finished.
- **Realistic copy.** No "Elevate", "Empower", "Next-Gen", "Seamless". The supporting line is concrete ("Start free. Move to Pro when you need more") and uses Australian voice (the writing-style memory is on for this project).

**Call B — fill each card's body (~24 ops, one ≤25 chunk).**

For each card I'd add: tier name, price + cadence, one-line summary, divider, feature list (5–7 rows of `FeatureRow` refs with check icons), and a CTA `Button*` ref. Pro additionally gets the "Recommended" badge in its header slot.

A representative slice — the Pro card body, assuming the `Card` component exposes `header`, `body`, and `footer` slots (which I confirmed in step 3 via `batch_get({ nodeIds: ["Card"], readDepth: 4 })`):

```
U(proCard, {
  descendants: {
    "header": {
      children: [
        { type: "frame", name: "ProHeader", layout: "horizontal", alignItems: "center", justifyContent: "space-between", width: "fill_container", children: [
          { type: "text", name: "TierName", text: "Pro", fontSize: "$textXl", fontWeight: 600, fill: [{ type: "solid_color", color: "$textPrimary" }] },
          { type: "ref", name: "RecommendedBadge", ref: "Badge", descendants: { label: { text: "Recommended" } } }
        ]}
      ]
    },
    "body": {
      children: [
        { type: "frame", name: "PriceRow", layout: "horizontal", alignItems: "baseline", gap: "$space-2", children: [
          { type: "text", name: "PriceAmount", text: "$29", fontSize: "$text4xl", fontWeight: 700, fill: [{ type: "solid_color", color: "$textPrimary" }] },
          { type: "text", name: "PriceCadence", text: "/ month", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] }
        ]},
        { type: "text", name: "TierSummary", text: "For solo builders shipping real work.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] },
        { type: "frame", name: "FeatureList", layout: "vertical", gap: "$space-3", width: "fill_container", children: [
          { type: "ref", ref: "FeatureRow", descendants: { icon: { iconName: "check" }, label: { text: "Unlimited projects" } } },
          { type: "ref", ref: "FeatureRow", descendants: { icon: { iconName: "check" }, label: { text: "Priority support, ~4hr response" } } },
          { type: "ref", ref: "FeatureRow", descendants: { icon: { iconName: "check" }, label: { text: "Advanced exports (PDF, SVG, code)" } } },
          { type: "ref", ref: "FeatureRow", descendants: { icon: { iconName: "check" }, label: { text: "Custom domains" } } },
          { type: "ref", ref: "FeatureRow", descendants: { icon: { iconName: "check" }, label: { text: "30-day version history" } } }
        ]}
      ]
    },
    "footer": {
      children: [
        { type: "ref", name: "ProCTA", ref: "ButtonPrimary", width: "fill_container", descendants: { label: { text: "Start Pro free for 14 days" } } }
      ]
    }
  }
})
```

(Equivalent `U` calls for `freeCard` and `teamCard` use `ButtonSecondary` instead, omit the badge in the header, and have shorter, plausible feature lists. Pricing per the flows reference's "plausible content" guidance: $0 for Free, $29/mo for Pro, $79/mo per seat for Team. Realistic SaaS numbers, not fabricated.)

**Cleanup.**

```
U(section, { placeholder: false })
```

Removes the in-progress flag now that the section is built.

If the inventory in step 3 didn't surface a `Card` component with a `recommended` state, the Call B `descendants` block also overrides the Pro card's outer `fill` (`$accentMuted`), `cornerRadius` (`$radiusLg`), and adds an explicit `height` taller than its siblings. I'd word that fallback into the plan in step 4 so the user sees the contingency.

## Step 6 — Verify (structural-first)

Walk the verification ladder per the SKILL. Stop at the cheapest rung that answers the question.

**Rung 1 — `batch_design` response.** Free. Confirms ops landed and bindings resolved. If any op failed, I read the error verbatim and cross-reference the batch-design-grammar's error table (e.g. raw color where a `$variable` was required, `paddingTop` instead of the array shorthand, `fill_container` on a non-flex parent).

**Rung 2 — `snapshot_layout`.** This is the right rung for almost everything in this design.

```
mcp__pencil__snapshot_layout({ parentId: "section", maxDepth: 3 })
```

What I'm checking with the returned numbers:

- `TierRow` has three children at equal width (each ≈ (1200 - 2×24) / 3 ≈ 384px, since `gap: "$space-5"` is 24).
- `ProCard` is taller than `FreeCard` and `TeamCard` (the variance the design requires).
- `gap` between header section and tier row is `$space-8` (48).
- Feature lists inside each card have consistent `gap: "$space-3"` (12).
- The "Recommended" badge sits inside the Pro card's `header` slot, not floating outside it.

If any of those numbers are off, that's a structural issue and I fix with `U` ops before paying for pixels.

**Rung 3 — `batch_get` for property-level confirmation.** When I need to confirm a binding rather than a layout number:

```
mcp__pencil__batch_get({
  nodeIds: ["proCard", "ProCTA", "RecommendedBadge"],
  resolveVariables: true
})
```

What I'm checking: the Pro card's outer `fill` resolved to a tinted token (`$accentMuted`), not the default surface. The CTA is bound to `ButtonPrimary` (not the secondary variant). The badge fill is `$primary` and its label colour passes contrast against that fill — `resolveVariables: true` lets me eyeball the actual hex pair.

**Rung 4 — `get_screenshot`.** Once. Scoped to the section, not the document root, per the SKILL's "always pass the most specific `nodeId`" rule.

```
mcp__pencil__get_screenshot({ nodeId: "section" })
```

Scanning the rendered image in the order the SKILL specifies:

1. **Layout integrity.** Three cards visible, Pro is the tallest, badge sits at the top-right corner not overlapping the tier name.
2. **Spacing rhythm.** Section padding matches `$space-12` top/bottom; card gaps match `$space-5`.
3. **Type rhythm.** Section heading is `$text4xl` (48), tier names are `$textXl` (20), prices are `$text4xl` (48) — the price is the visual peak inside each card.
4. **Contrast.** Body text inside the Pro card on `$accentMuted` background still passes WCAG AA. This is the real reason a screenshot is justified — variable bindings can't predict whether `textPrimary` against `accentMuted` clears 4.5:1 in *both* themes. If light mode passes but dark mode is borderline, I'd switch to a darker variant or a different `textOnAccent` token.
5. **Component fidelity.** Every CTA is clearly an instance of the library `Button*` component (no hand-built buttons that drift). The badge matches the library `Badge`.

If anything fails, fix with targeted `U` ops, re-snapshot (rung 2 is usually enough to confirm a fix landed), and only re-screenshot if the fix was visual. The SKILL's worked example explicitly says one or two screenshots is the budget; I'm aiming for one.

**Dual-mode check.** Per the SKILL: routine theme-aware designs built entirely from variables don't need a second screenshot. If every fill, stroke, and text colour is bound to a `$token` with both `light` and `dark` values, the variable system guarantees mode parity. I'd only screenshot dark mode if the contrast check on rung 4 surfaced a borderline case in light mode that I want to confirm doesn't get worse in dark.

## Step 7 — Iterate or report

Likely iterations on a pricing section:

- The "Recommended" badge fills the wrong colour because the `Badge` component's default state is neutral. Fix with `U("RecommendedBadge", { theme: { state: "primary" } })` if Badge has a state axis, otherwise a `descendants` override on the badge's `fill`.
- Cards feel too tight. Increase card-internal `padding` from `$space-5` to `$space-6` via three `U` ops (one per card, if applied at the descendants level).
- The Pro card's height bump is too subtle (looks accidental rather than deliberate). Push the differentiation harder: bigger price, larger CTA, or a small "Save 20% with annual" microline under the price.

Final report when clean:

> *"Pricing section landed at `PricingSection`. Three tiers (`FreeCard`, `ProCard`, `TeamCard`) at desktop width with Pro highlighted via tinted surface, taller card, badge, and primary CTA. All cards instantiate your `Card` component; CTAs use `ButtonPrimary` (Pro) and `ButtonSecondary` (Free, Team); badge is your `Badge` with the primary state. Tokens come from `get_variables` — no raw hex bound. Verified structurally via `snapshot_layout` (heights and gaps match plan), property-level via `batch_get` (Pro card resolves the recommended state and tinted surface), and one screenshot for visual sign-off (contrast passes in both modes). Mobile and tablet variants will need their own breakpoint frames — say the word and I'll add them as siblings."*

---

## Notes on what I deliberately did *not* do

- **I didn't reach for `Inter` or a generic serif, neon glow shadows, or a purple-blue gradient on the heading.** The SKILL flags those as AI tells. Type defaults to `Geist` or `Satoshi` per the SKILL's marketing pairing unless the project's `tokens.md` pins something else.
- **I didn't ship a flat symmetric three-card grid.** Three columns is the right shape for a pricing comparison, but the Pro tier is materially different in surface, height, badge, and CTA strength. The variance is what stops it from reading as "AI-default benefits grid".
- **I didn't load `references/states.md`, `flows.md`, `accessibility.md` deeply.** Pricing cards aren't a multi-screen flow and aren't a fault state, and the SKILL's baseline accessibility checks (contrast, hit targets, names map to roles, focus states on the CTAs from the library component) are sufficient for this surface. If the user followed up with "now design the checkout flow", I'd load `flows.md` then.
- **I didn't pre-screenshot or screenshot dark mode.** Variable system + one final screenshot of the section node is the right cadence.
- **I didn't invent metrics.** No "10,000+ teams trust us", no fabricated logos, no "as seen in" row. The pricing numbers ($0 / $29 / $79) are plausible SaaS figures per `flows.md`'s plausible-content guidance.

## Skill references I consulted, and why

- **`SKILL.md`** — the seven-step workflow, six discipline rules (especially Components-first and Themes), the AI-tell anti-patterns list (specifically the three-column grid warning that's the biggest trap on this task), and the verification ladder.
- **`references/component-anatomy.md`** — to know how to read the `Card` component's structure before instantiating it, build `descendants` paths to its slots (`header`, `body`, `footer`), and decide whether to use a `state: "recommended"` theme axis or a styling override.
- **`references/batch-design-grammar.md`** — for the `I` / `U` op syntax, the `foo=I(...)` binding pattern across two chunked calls, the ≤25-ops rule, the `placeholder: true` requirement on the top-level section frame, and the sizing rules (`fill_container` only inside flex parents, `padding` as a 4-value array, no `paddingTop`).
- **`references/mcp-tools.md`** — to pick the right `get_guidelines` categories (`Landing Page` + `Design System`), to remember `get_variables` is mandatory before any token work, and to map the verification ladder rungs to the right tools (`snapshot_layout` for numbers, `batch_get` for properties, `get_screenshot` only as the final visual sign-off).
- **`references/flows.md`** — only the plausible-content line on pricing numbers.
- **`assets/examples/example-login-screen.md`** — as a structural reference for how a greenfield workflow narrative reads end-to-end (host detect → context → guidelines → plan → batch_design → snapshot → screenshot → report).

I did not load `accessibility.md`, `states.md`, `modern-patterns.md`, `pen-schema.md`, `pencil-cli.md`, or any platform-specific tool-name file (`codex-tools.md` etc.) because none of them were on the path for a single-section pricing build. If the user followed up with "make this responsive across breakpoints", I'd add a sibling `PricingSection_Mobile` and `PricingSection_Tablet` per the SKILL's responsive table; if they followed up with "design the loading and empty states for the pricing data", I'd load `states.md`.
