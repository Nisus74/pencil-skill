# Example: design a three-tier pricing table with highlighted recommended tier

User says:

> *"Build the pricing page. Free, Pro, Team tiers. Highlight Pro as recommended. Layered shadows, two-role colour."*

This example shows the agent designing a three-tier pricing table with the highlighted-tier treatment, layered shadows, and a feature comparison.

---

## Step 1: Read context

```js
get_editor_state();
```

The agent reads `assets/design-system/visual-style.md`, `tokens.md`, and `voice.md` (for pricing copy tone). Loads `references/layout-patterns.md` § Pricing tables and `SKILL.md` § Aesthetic defaults: Shadows.

## Step 2: Pick the pricing pattern

Per `references/layout-patterns.md` § Pricing tables, four shapes:

- **Three-tier (Free / Pro / Team)**: SaaS with a clear progression. Default for B2B SaaS.
- **Single-tier with feature comparison**: single product, single price.
- **Usage-based**: pricing scales with consumption.
- **Enterprise contact**: top tier is 'Contact us'.

The user named three tiers (Free / Pro / Team). Use three-tier with Pro highlighted.

## Step 3: Plan the layout

Three pricing cards in a row, equal width. Pro tier in the middle, highlighted. Each card:

- Header: tier name + monthly price + 'per user / month' or 'flat rate'.
- Primary action button.
- Feature list (4-8 items per tier; checkmark + feature name).
- Optional secondary CTA below the feature list.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<canvas-root-id>",
      node: {
        type: "frame",
        name: "Marketing_Pricing",
        context: "Three-tier pricing (Free / Pro / Team). Pro is the highlighted recommended tier: coloured border using $accent, layered shadow (ambient + direct), 'Most popular' badge. Don't combine all four treatments; coloured border + badge is the chosen pair.",
        layout: { direction: "column", padding: 64, gap: 48, align: "center" },
        children: [
          { type: "text", text: "Pricing", fontFamily: "$fontDisplay", fontWeight: "$fontWeightBold" },
          { type: "text", text: "Pick the plan that fits your team. All plans include unlimited projects.", color: "$textSecondary" },
          { type: "frame", name: "PricingRow", layout: { direction: "row", gap: 24, align: "stretch" }, children: [] },
        ],
      },
    },
  ],
});
```

## Step 4: Build the Free tier

Plain card, no highlight. Use `Card_Pricing` with default treatment.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<pricing-row-id>",
      node: {
        type: "ref",
        componentId: "Card_Pricing",
        descendants: {
          tier: "Free",
          price: "$0",
          period: "forever",
          description: "For trying things out.",
          ctaLabel: "Start free",
          ctaVariant: "Secondary",
          features: [
            "Up to 3 projects",
            "Unlimited members",
            "Community support",
            "1 GB storage",
          ],
        },
      },
    },
  ],
});
```

## Step 5: Build the Pro tier (highlighted)

Per `references/layout-patterns.md` § Pricing tables: the highlighted tier carries a coloured border (one accent), a layered shadow, a slight scale-up, and either a badge. Don't combine all four. Coloured border + badge is the canonical pair (per the user's brief).

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<pricing-row-id>",
      node: {
        type: "ref",
        componentId: "Card_Pricing_Highlighted",
        descendants: {
          tier: "Pro",
          price: "$12",
          period: "per user / month",
          description: "For growing teams.",
          badge: "Most popular",
          ctaLabel: "Start Pro trial",
          ctaVariant: "Primary",
          features: [
            "Everything in Free",
            "Unlimited projects",
            "Priority support",
            "100 GB storage",
            "Custom roles & permissions",
            "Audit log",
          ],
        },
      },
    },
  ],
});
```

The `Card_Pricing_Highlighted` component (defined in `design-system.lib.pen`):

```js
{
  name: "Card_Pricing_Highlighted",
  reusable: true,
  context: "Highlighted pricing card. Coloured border ($accent, 2px). Layered shadow (ambient + direct, two layers minimum per SKILL.md § Shadows). 'Most popular' badge anchored to the top-right of the card. Hover: subtle lift via translateY(-2px); shadow deepens. Status: ready.",
  fill: "$surface",
  border: { width: 2, colour: "$accent" },
  shadow: [
    { x: 0, y: 1, blur: 2, colour: "rgba(0,0,0,0.04)" },
    { x: 0, y: 8, blur: 24, colour: "rgba(0,0,0,0.08)" },
  ],
  cornerRadius: 12,
  // ... slots for tier name, price, badge, features, CTA
}
```

Two-role colour per `SKILL.md` § Aesthetic defaults: Colour (and `references/colour-palettes.md` § Two-role architecture refresher): the card uses `$surface` (neutral) for the base + `$accent` (one hue) for the border. Don't add a second accent for the badge; the badge uses the same `$accent`.

## Step 6: Build the Team tier

Plain card, similar to Free but with more features.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<pricing-row-id>",
      node: {
        type: "ref",
        componentId: "Card_Pricing",
        descendants: {
          tier: "Team",
          price: "$24",
          period: "per user / month",
          description: "For teams that need scale.",
          ctaLabel: "Contact sales",
          ctaVariant: "Secondary",
          features: [
            "Everything in Pro",
            "SSO + SCIM",
            "SLA 99.9%",
            "Dedicated CSM",
            "Custom contract",
            "1 TB storage",
          ],
        },
      },
    },
  ],
});
```

## Step 7: Microcopy pass

Per `references/microcopy.md` § Buttons / CTAs: action-specific verbs.

- Free CTA: 'Start free' (specific to the action).
- Pro CTA: 'Start Pro trial' (mentions the tier; differentiates from Free).
- Team CTA: 'Contact sales' (the right action for enterprise tier).

Avoid 'Get started' (too generic), 'Continue' (means nothing in pricing context), 'Buy now' (too transactional for SaaS).

Per `references/microcopy.md` § Headlines: descriptions are benefit-focused and specific. 'For growing teams' is fine; 'For better collaboration' is generic.

## Step 8: Feature comparison (optional)

If the user wants a feature-by-feature comparison below the three cards, build a comparison table:

- One row per feature.
- Three columns (Free / Pro / Team) with checkmarks (`✓`) where included.
- Use `$textPrimary` for ✓; `$textMuted` for `–` (not included).

Per `references/data-viz.md` § Pairing colour with shape: don't rely on colour alone. The checkmark shape is the primary signal.

## Step 9: Optional: monthly / yearly toggle

Many SaaS pricing pages include a billing-period toggle. If the project ships one:

- Toggle above the three cards: 'Monthly | Yearly (Save 20%)'.
- Active state: filled background using `$accent`.
- Yearly prices show with monthly equivalent and the savings.
- Toggle state in URL (`?billing=yearly`) per `references/flows.md` § Deep links & shareable URLs.

## Step 10: Mobile layout

The three cards stack vertically on mobile (≤ 768px). The highlighted Pro card stays highlighted; in a vertical stack, position it second so it's still in the middle of the visual flow.

The badge stays in place; the layered shadow renders the same.

## Step 11: Verify with one screenshot

```js
get_screenshot({ documentId, nodeId: "<marketing-pricing-frame-id>" });
get_screenshot({ documentId, nodeId: "<marketing-pricing-frame-id>", theme: { mode: "dark" } });
```

Confirm:
- Pro tier has both the coloured border and the badge (the chosen pair).
- Layered shadow visible (two layers; the depth reads as cared-for).
- Two-role colour: only `$surface` and `$accent` used; no third hue competing.
- CTA copy is action-specific (no 'Get started').
- Mobile stack puts Pro second.
- Dark mode: shadow direction adjusted (per `references/colour-palettes.md` § Dark-mode-first variations: elevated surfaces lighter, not darker).

## See also

- `references/layout-patterns.md` § Pricing tables.
- `references/colour-palettes.md` § Two-role architecture refresher.
- `references/microcopy.md` § Buttons / CTAs, § Headlines.
- `references/data-viz.md` § Pairing colour with shape (for the feature comparison checkmarks).
- `SKILL.md` § Aesthetic defaults: Shadows, Colour.
- `assets/design-system/visual-style.md`: project's chosen style and palette.
- `assets/design-system/components.md`: `Card_Pricing` and `Card_Pricing_Highlighted` definitions.
- `assets/design-system/voice.md`: pricing-related microcopy tone.
