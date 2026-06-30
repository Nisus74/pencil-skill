# Design eye: first-screenshot diagnostic

Five questions to ask after every first screenshot. Run these before adding any detail ops. A wrong skeleton under 60 ops is nearly unrecoverable; a right skeleton is worth 60 ops of refinement.

These questions are not aesthetic judgements. Each one is answerable with a yes or a no, and each no has a specific fix.

---

## Question 1: Does this match the stated direction?

Re-read the aesthetic direction stated in step 2. Then look at the screenshot.

The direction should answer: what makes this design recognisably itself and not a generic SaaS page? Typography pairing, density register, accent strategy, surface treatment — at least one of these should be visible in the skeleton.

**Pass:** The screenshot is describable with the words from your step 2 direction. A designer reading the direction and then seeing the screenshot would say "yes, that's what was described."

**Fail:** The screenshot could belong to any generic SaaS product. Nothing in it is specific to the stated direction.

**Fix:** Identify which part of the stated direction is absent from the skeleton. Build that first. If the direction said "hairline border, no shadow" and the card has a shadow, remove the shadow now.

---

## Question 2: Can you name one element that reads as a deliberate choice?

One element. Not the overall feel. One specific thing where you can say: "I chose this because [reason from the user's direction or the negative-space defaults]."

Examples of elements that are deliberate vs. defaulted:

| Deliberate | Defaulted |
|---|---|
| `stroke: "$border", strokeWidth: 1` — separates card without claiming elevation | `effect: [{ type: "shadow", shadowType: "outer" }]` — default shadow from any component kit |
| Status badge with 12% opacity tinted fill | Pill badge with `cornerRadius: 999` and full-saturation fill |
| Page background in a grey variable, not `#FFFFFF` | `fill: "#FFFFFF"` — pure white |
| Monospace font on numeric figures | Proportional font on all text including financial values |
| Compact row height (28–40px) on a dense table | Row height at 48–52px on a data table that doesn't need touch targets |

**Pass:** You can name the element and point to it in the screenshot, and explain why it isn't the default.

**Fail:** Every element in the screenshot could have been generated without reading any direction. The design looks like a generic Figma component library dropped onto a white page.

**Fix:** Find the single most distinctive element implied by the direction. Build it first, even if other things are incomplete.

---

## Question 3: Is there a shadow somewhere it shouldn't be?

Shadows are the most common AI-default drift. The correct use cases are narrow: elements that genuinely float above the document surface (tooltips, floating toolbars, popovers, modals, dropdowns) and hero images where depth is intentional.

Everything else — cards, panels, containers, form fields, data tables — should use surface-colour differentiation or hairline strokes, not shadows.

**Pass:** No visible shadows except on elements that genuinely float.

**Fail:** A card, panel, or container has a drop shadow.

**Fix:**

```
Update(nodeId, { effect: [] })
```

One op. Do it before any other work.

---

## Question 4: Is there anything that reads as a generic default?

Common generic defaults that survive into first screenshots:

- **White cards on a white page.** If the page background and the card fill are both `#FFFFFF`, the card is invisible. Surface hierarchy should create visible separation without a shadow. Use a `$surfaceMuted` or `$bg` variable that resolves to a slightly offset tone.
- **Blue primary colour.** The default blue `#0066FF` or `#3B82F6` is in every generic design. If you haven't derived the colour from the user's direction, you've defaulted. Check before binding.
- **16pt/400 body text.** Generic component kits default to 16px regular. Data-dense products typically use 13–14px; consumer apps use 15–16px; editorial uses 17–18px. If the body text looks like "any web app," check what the direction calls for and set it explicitly.
- **Rounded pill badges.** `cornerRadius: 999` on a badge produces a pill. Institutional products use `cornerRadius: 4`; modern SaaS uses `cornerRadius: 6`; consumer apps may use pills intentionally. If you haven't checked the direction, you've defaulted to the pill.
- **Full-width dividers.** A divider that spans the full container width is a web default. Consider whether the design calls for no dividers (most app UIs), inset dividers, or colour-only row separation. Full-width hairlines are often the wrong choice.

**Pass:** You can account for every property in the skeleton and explain why it is what it is.

**Fail:** You see a property in the screenshot and your explanation is "that's the default."

**Fix:** Identify the specific property and override it before adding detail.

---

## Question 5: Does the spacing feel deliberate or just "padded"?

Generic padding is `padding: 16` everywhere. Deliberate spacing varies: more gap between sections, less between related elements.

The test: look at the densest section of the design and the most spacious section. If they look the same, the spacing is not deliberate.

**Pass:** There is visible hierarchy in the spacing. The most important content has the most breathing room. Related elements are tighter to each other than they are to unrelated elements.

**Fail:** Everything has the same padding. The design feels padded rather than structured.

**Fix:** Identify the content hierarchy and apply spacing tokens accordingly. High-density surfaces (data tables, sidebar items) need smaller gaps than page-level sections. Content that is related (label + value) should sit closer than content that is categorically separate (card group A vs card group B).

---

## How to use this diagnostic

Run questions 1–5 after the first screenshot (step 5). Write the answers in your narration:

> *"Direction match: yes — hairline border on card, no shadow. Q3: no shadows anywhere. Q4: body text is at 14px matching the data-dense direction, not the 16px default. Q5: card padding 20px, table rows 40px, visible density hierarchy. Proceeding."*

If any question fails, fix the issue before continuing. The cost of fixing a skeleton is 1–3 ops. The cost of fixing a wrong skeleton after 40 detail ops is starting over.
