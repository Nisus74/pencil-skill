# Signature moments

One concrete, measurable signature element per archetype. These are the elements that make a design recognisably its archetype at a glance, before any detail work is done.

A signature moment is not a vibe or an aesthetic direction. It is a specific, buildable thing: a node with exact properties that any designer at the exemplar company would recognise as belonging to their product family.

Read this alongside `assets/archetypes/README.md`. If your skeleton doesn't include the signature moment for its archetype, build it first.

---

## analytics-dashboard

**Signature moment:** A KPI card with a hairline border, no shadow, and a monospace value.

```
kpiCard=I(parent, { type: "frame", name: "KPICard",
  layout: "vertical", gap: 8, padding: [16, 16, 16, 16],
  cornerRadius: 8,
  fill: "$surface",
  stroke: { color: "$border", thickness: 1 }
  // No effect property. The absence of shadow is the signal.
})
kpiValue=I(kpiCard, { type: "text", content: "24,831",
  fontSize: 28, fontFamily: "$fontMono", fontWeight: 600,
  fill: "$textPrimary"
  // $fontMono locks column alignment across multiple KPI cards.
})
```

**What to look for in the screenshot:** the card surface and the page background are distinct without any shadow separating them. The value is visibly monospaced (characters take equal horizontal space). No card in this archetype has a shadow.

---

## workflow-platform

**Signature moment:** A task row with a status badge that uses a tinted fill (12–15% opacity), not a full-opacity colour.

```
statusBadge=I(row, { type: "frame", name: "StatusBadge",
  layout: "horizontal", alignItems: "center",
  paddingLeft: 8, paddingRight: 8, height: 22,
  cornerRadius: 4,
  fill: { color: "$statusInProgress", opacity: 0.12 }
  // 12% opacity tinted fill. Full opacity reads as a pill; tinted reads as state.
})
badgeLabel=I(statusBadge, { type: "text",
  content: "In progress",
  fontSize: 12, fontWeight: 500,
  fill: "$statusInProgress"
})
```

**What to look for:** the badge background is visibly tinted (you can see the row background through it). No full-saturation badge fills. Status colours appear in both the label and the faint background.

---

## enterprise-corporate

**Signature moment:** A grey page background, not white.

```
page=I(doc, { type: "frame", name: "Page",
  fill: "$bg"
  // $bg is #F3F4F6, not #FFFFFF. Grey page background is the single most
  // visible institutional signal in this archetype.
})
```

**What to look for:** the page reads as grey, not white. Every panel, card, and form sits on a grey field. If the page looks white, this is not the enterprise-corporate archetype.

Secondary signal: the navigation bar at the top is filled with `$accent`, not transparent. Accent-filled top nav is the institutional marker.

---

## modern-pro-tool

**Signature moment:** A sidebar with extremely tight spacing and no visible dividers.

```
sidebarItem=I(sidebar, { type: "frame", name: "SidebarItem",
  layout: "horizontal", alignItems: "center",
  height: 28, paddingLeft: 8, paddingRight: 8, gap: 6,
  fill: "transparent"
  // 28px height is power-tool density. Looser rows read as consumer apps.
  // No separator lines between items; colour separation only.
})
```

**What to look for:** the sidebar is dense. Items are packed tightly. Active state is a 2px left border accent, not a filled pill background.

---

## developer-platform

**Signature moment:** Monospace font on every technical identifier (API keys, endpoint paths, HTTP methods, IDs, status codes, timestamps).

```
apiKeyField=I(card, { type: "frame", name: "APIKeyField",
  layout: "horizontal", alignItems: "center",
  padding: [8, 12, 8, 12], cornerRadius: 6,
  fill: "$bgCode"
  // $bgCode is slightly darker than $bgPanel — code container surface.
})
apiKeyText=I(apiKeyField, { type: "text",
  content: "sk-••••••••••••••••••••3f8a",
  fontFamily: "$fontMono", fontSize: 13,
  fill: "$textSecondary"
  // Monospace. Masked. Last 4 chars only.
})
```

**What to look for:** any technical string (key, path, code, ID) is in a monospace font. The moment a developer-platform design has an API key in a proportional font, it reads as a marketing page, not a console.

---

## conversion-focused-saas

**Signature moment:** A hero section where the headline is the tallest element on the page and the CTA is the only accent-coloured element.

```
heroHeadline=I(hero, { type: "text", name: "Headline",
  content: "Ship faster, break nothing",
  fontSize: 64, fontWeight: 700, lineHeight: 1.1,
  fill: "$textPrimary"
  // 64px minimum. Smaller reads as a content page, not a conversion page.
})
heroCta=I(hero, { type: "frame", name: "HeroCta",
  layout: "horizontal", alignItems: "center",
  padding: [16, 32, 16, 32], cornerRadius: 8,
  fill: "$accent"
  // Accent fill on the CTA only. No other element on the page uses $accent fill.
})
```

**What to look for:** the headline dominates. One button has the accent fill. Everything else is neutral.

---

## editorial-storytelling

**Signature moment:** A serif display font on the headline with a line height of at least 1.15.

```
articleTitle=I(hero, { type: "text", name: "Title",
  content: "The last decade of design tools",
  fontFamily: "$fontSerif", fontSize: 56, fontWeight: 700,
  lineHeight: 1.15, fill: "$ink"
  // Serif font. Not Inter. Not system UI. The font is the archetype signal.
  // 1.15 line height minimum; tighter reads as display advertising, not editorial.
})
```

**What to look for:** the headline font is visibly different from a sans-serif system font. If you can't tell in one glance that this is a serif font, it's not prominent enough.

---

## consumer-productivity

**Signature moment:** A task row with a hollow circle checkbox on the left and no separator line between rows.

```
taskRow=I(list, { type: "frame", name: "TaskRow",
  layout: "horizontal", alignItems: "center",
  height: 44, paddingLeft: 16, paddingRight: 16, gap: 12,
  fill: "transparent"
  // No separator. Row separation is white space, not a line.
  // 44px height matches Apple HIG touch target.
})
checkbox=I(taskRow, { type: "ellipse", name: "Checkbox",
  width: 20, height: 20,
  stroke: { color: "$border", thickness: 1.5 }
  // Hollow circle, not a square checkbox. Personal task apps use circles.
  // No fill until the task is complete.
})
```

**What to look for:** a list of tasks with circles, not squares, on the left. No horizontal lines between rows. The list breathes.

---

## consumer-finance

**Signature moment:** A balance figure in a large monospace font on a dark surface.

```
balanceCard=I(parent, { type: "frame", name: "BalanceCard",
  layout: "vertical", gap: 8, padding: [24, 24, 24, 24],
  cornerRadius: 12, fill: "$surfaceDark"
  // Dark fill ($surfaceDark), not $accent. Dark is the trust register in fintech.
})
balanceAmount=I(balanceCard, { type: "text",
  content: "$24,831.50",
  fontSize: 40, fontFamily: "$fontMono", fontWeight: 600,
  fill: "$textOnDark"
  // $fontMono on all financial figures. No exceptions.
  // 40px. Smaller reads as a label, not a balance.
})
```

**What to look for:** the balance is large, monospaced, and on a dark card. If the balance figure is in a proportional font, this is not the consumer-finance archetype.

---

## conversation-chat

**Signature moment:** An AI message with no card, no background, no border. Just text directly on the page surface.

```
aiMessage=I(thread, { type: "frame", name: "AIMessage",
  layout: "horizontal", alignItems: "flex-start",
  padding: [0, 72, 0, 0], gap: 16,
  fill: "transparent"
  // No fill. No stroke. No cornerRadius. AI message floats directly on the thread.
  // A card on the AI message reads as a chatbot widget, not a conversational AI.
})
aiBody=I(aiMessage, { type: "text", name: "AIBody",
  content: "Here's what I found...",
  fontSize: 15, lineHeight: 1.65,
  fill: "$textPrimary"
})
```

**What to look for:** AI messages have no visible container. User messages have a bubble (right-aligned, warm fill). The contrast between the two (bubble vs. floating text) is the signature.

---

## agent-execution

**Signature moment:** A task list where each item has a status icon with a distinct shape (not just a colour-coded dot).

```
taskIcon=I(taskRow, { type: "frame", name: "TaskIcon",
  width: 20, height: 20, cornerRadius: 10
  // Shape encodes status: circle = running (spin animation), check = done,
  // pause = waiting, x = failed, dot = queued.
  // A coloured dot for every status removes the shape signal. Users who are
  // colour-blind cannot distinguish running from failed from a dot alone.
})
```

**What to look for:** the status icons use different shapes (or shape + colour combinations), not just different colours. A list where all items have the same circular dot in different colours is not the agent-execution archetype.

---

## ai-augmented-workspace

**Signature moment:** Ghost text that is visually indistinguishable from the document text in everything except colour.

```
ghostText=I(document, { type: "text", name: "GhostText",
  content: "continued the argument by noting",
  fontSize: 16, fontFamily: "$fontBody", fontWeight: 400,
  lineHeight: 1.6,
  fill: "$ghostText"
  // Same font. Same size. Same weight. Same line height.
  // ONLY the fill colour differs ($ghostText is lighter than $textPrimary).
  // Any other property difference breaks the visual illusion of the AI
  // continuing the user's thought.
})
```

**What to look for:** ghost text looks exactly like the surrounding text except it's lighter. If the ghost text is a different font, size, or weight, the AI intrusion is legible as a foreign object, not a continuation.

---

## cross-platform-modern (React Native / Expo / Flutter)

**Signature moment:** List rows at 52pt height with Inter font at 15pt.

```
listRow=I(screen, { type: "frame", name: "ListRow",
  layout: "horizontal", alignItems: "center",
  height: 52, width: "fill_container",
  padding: [0, 16], gap: 12,
  fill: "transparent"
  // 52pt, not 44pt. 44pt is iOS native (SF Pro). Inter at 15pt needs 52pt to
  // breathe at the same visual density.
})
rowTitle=I(listRow, { type: "text", content: "Project Alpha",
  fontSize: 15, fontFamily: "$fontBody", fontWeight: 500,
  fill: "$textPrimary"
  // 15pt Inter. Not 17pt (iOS native). Not 14pt (too small for a cross-platform
  // app aiming at reading comfort on mobile).
})
```

**What to look for:** rows are taller than 44pt. Text is visibly Inter, not SF Pro or a system font. If the rows look like an iOS Settings app, this is not the cross-platform-modern archetype.

---

## ios-native-utility

**Signature moment:** A list row separator that is inset 16pt from the left edge (not full-width).

```
separator=I(row, { type: "frame", name: "Separator",
  height: 0.5,
  marginLeft: 16,
  fill: "$separator"
  // Inset 16pt. Full-width separators are the web-style signal.
  // 0.5pt height (hairline on @2x screens).
  // $separator is rgba(60,60,67,0.29) in light mode.
})
```

**What to look for:** the separator lines between rows do not extend to the left edge of the screen. There is a 16pt gap on the left (76pt if there's a leading icon). Full-width separators immediately identify a non-native design.
