# Design eye: first-screenshot diagnostic

Five questions to ask after every first screenshot. Run these before adding any detail ops. A wrong skeleton under 60 ops is nearly unrecoverable; a right skeleton is worth 60 ops of refinement.

These questions are not aesthetic judgements. Each one is answerable with a yes or a no, and each no has a specific fix.

---

## Question 1: Does this match the verifiable brief?

Re-read the brief you wrote in step 4. Then look at the screenshot.

The brief has three parts:
- "What success looks like": a description specific enough to distinguish this design from a generic SaaS page.
- "Signature element": one measurable, concrete detail.
- "Microcopy register": phrases this design says and phrases it would never say.

**Pass:** The screenshot is describable with the words from your brief. A designer reading the brief and then seeing the screenshot would say "yes, that's what the brief described."

**Fail:** The screenshot could belong to any generic SaaS product. Nothing in it is specific to the archetype. The "what success looks like" description could apply to a dozen other designs.

**Fix:** Identify which part of the brief is absent from the skeleton. Build that first. If the brief said "hairline border, no shadow" and the card has a shadow, remove the shadow now. If the brief said "signature element: 10-bar sparkline" and there's no sparkline, that's step 5 work, not step 5a work. But the structural container for it needs to be visible in the skeleton.

---

## Question 2: Can you name one element that reads as this specific archetype?

One element. Not the overall feel. One specific thing.

| Archetype | Example element you should be able to name |
|---|---|
| `analytics-dashboard` | Card with hairline border and no shadow |
| `workflow-platform` | Status badge with tinted fill (not full-opacity) |
| `enterprise-corporate` | Grey page background (not white) |
| `developer-platform` | Monospace font on any technical identifier |
| `conversion-focused-saas` | Auth card width narrower than a content card |
| `editorial-storytelling` | Serif display heading with generous line height |
| `consumer-productivity` | Task rows with no visible separator lines |
| `consumer-finance` | Monospace font on any numeric figure |
| `conversation-chat` | AI message with no card or background fill |
| `agent-execution` | Dark theme with status icon using shape, not just colour |
| `ai-augmented-workspace` | Ghost text matching document font exactly |
| `cross-platform-modern` | 52pt list rows (not iOS native 44pt) |
| `ios-native-utility` | 0.5pt inset hairline separator (not full-width) |

**Pass:** You can name the element and point to it in the screenshot.

**Fail:** Every element in the screenshot could belong to any archetype. The design looks like a generic Figma component library was dropped onto a white page.

**Fix:** Find the single most distinctive element in the archetype spec. Build it first, even if other things are incomplete. A developer-platform design that doesn't have monospace on API keys is not yet a developer-platform design; it's a generic table design with a different label.

---

## Question 3: Is there a shadow somewhere it shouldn't be?

Shadows are the most common AI-default drift. Most archetypes in this skill explicitly reject shadows. The exceptions are narrow:

- `ai-augmented-workspace`: floating panels (inline prompt panel, selection toolbar) use a shadow because they float above the document layer. Cards within the panel do not.
- `conversion-focused-saas` and `editorial-storytelling`: hero sections may use subtle depth on images. Card components do not.

Everything else: no shadows on cards, panels, or containers. If you see a shadow in the screenshot, it was added by a default and needs to be removed.

**Pass:** No visible shadows except in the specific exceptions above.

**Fail:** A card, panel, or container has a drop shadow.

**Fix:**

```
U(nodeId, { effect: [] })
```

One op. Do it before any other work.

---

## Question 4: Is there anything that reads as a generic Figma default?

Common generic defaults that survive into first screenshots:

- **White cards on a white page.** If the page background is `#FFFFFF` and the card fill is `#FFFFFF`, the card is invisible. The archetype's surface hierarchy should create visible separation without a shadow.
- **Blue primary colour.** The default blue `#0066FF` or `#3B82F6` is in every generic design. It may be correct for some archetypes (like `ios-native-utility` with `$accent: #007AFF`), but if you haven't checked the design-system tokens, you've defaulted.
- **16pt/400 body text.** Generic component kits default to 16px regular. Most archetypes have a specific size: 15pt for cross-platform-modern, 17pt for ios-native-utility, 14px for analytics-dashboard data density. If the body text looks like "any web app," it's at the default size.
- **Rounded pill badges.** `cornerRadius: 999` on a badge produces a pill. Most archetypes use `cornerRadius: 4` (institutional) or `cornerRadius: 6` (modern SaaS). Pills on status badges read as consumer app defaults.
- **Full-width dividers.** A divider that spans the full container width is a web default. iOS native uses inset dividers. Most SaaS archetypes use no dividers.

**Pass:** You can account for every property in the skeleton and explain why it is what it is.

**Fail:** You see a property in the screenshot and your explanation is "that's the default."

**Fix:** Identify the specific property and override it before adding detail.

---

## Question 5: Does the spacing feel deliberate or just "padded"?

Generic padding is `padding: 16` everywhere. Deliberate spacing varies: more gap between sections, less between related elements.

The test: look at the densest section of the design and the most spacious section. If they look the same, the spacing is not deliberate.

**Pass:** There is visible hierarchy in the spacing. The most important content has the most breathing room. Related elements are tighter to each other than they are to unrelated elements.

**Fail:** Everything has the same padding. The design feels padded rather than structured.

**Fix:** Identify the content hierarchy and apply spacing tokens accordingly. The analytics-dashboard archetype has specific guidance: KPI card padding `$space-5` (20px), table row height 40px with `$space-3` vertical padding, sidebar gap `$space-2` between items. Use the archetype spec, not a generic `$space-4` everywhere.

---

## How to use this diagnostic

Run questions 1–5 after the first screenshot (step 5a). Write the answers in your narration:

> *"Brief match: yes. Archetype signal: hairline border on card, no shadow. Q3: no shadows. Q4: body text is 14px per analytics-dashboard spec, not the 16px default. Q5: KPI card padding 20px, table rows 40px, visible density hierarchy. Proceeding."*

If any question fails, fix the issue before continuing. The cost of fixing a skeleton is 1–3 ops. The cost of fixing a wrong skeleton after 40 detail ops is starting over.
