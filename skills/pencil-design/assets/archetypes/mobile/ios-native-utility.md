# ios-native-utility

Native iOS utility apps that feel like they belong in the OS: SF Pro throughout, 44pt touch targets, standard iOS navigation patterns, and system materials. The goal is invisible craft. The app should feel like Apple shipped it.

**Surface category:** mobile
**Exemplars:** Apple Reminders, Apple Notes, Dark Sky (pre-acquisition), Things 3, Fantastical
**Confidence:** high; Apple HIG confirmed from documentation (May 2026); Things 3 and Fantastical from direct use

Read this alongside `references/batch-design-grammar.md`. Mobile canvas: design at 390×844 (iPhone 15 standard screen). All values in points (pt); Pencil's canvas represents 1pt = 1px at 1× density.

---

## When to use this archetype

Pick this for utilities, productivity apps, and tools that target iOS as the primary platform and aim for a native, system-integrated feel. Skip it if the app is primarily web-based or cross-platform; use `cross-platform-modern` instead. Skip it for games, media apps, or highly branded consumer experiences.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#FFFFFF` (light), `#000000` (dark) | Primary background. System background colour. |
| `$bgSecondary` | `#F2F2F7` (light), `#1C1C1E` (dark) | Grouped table background, inset list fill. |
| `$bgTertiary` | `#FFFFFF` (light), `#2C2C2E` (dark) | Inset cell fill. |
| `$label` | `#000000` (light), `#FFFFFF` (dark) | Primary label. System label colour. |
| `$labelSecondary` | `rgba(60,60,67,0.6)` (light), `rgba(235,235,245,0.6)` (dark) | Secondary label. |
| `$labelTertiary` | `rgba(60,60,67,0.3)` (light), `rgba(235,235,245,0.3)` (dark) | Tertiary label. Placeholders. |
| `$separator` | `rgba(60,60,67,0.29)` (light), `rgba(84,84,88,0.65)` (dark) | Row separators, dividers. |
| `$accent` | `#007AFF` (iOS blue) unless brand overrides. | Tint colour: interactive elements, links, CTAs. |
| `$fillPrimary` | `rgba(120,120,128,0.2)` (light), `rgba(120,120,128,0.36)` (dark) | Search bar fill, secondary button fill. |
| `$fontDisplay` | `SF Pro Display`, weight 700 | Large display titles (34pt+). |
| `$fontText` | `SF Pro Text`, weight 400 | Body text (17pt standard). |
| `$fontRounded` | `SF Pro Rounded` | Numeric displays in utility apps. Optional. |

These match UIKit's system semantic colours exactly. Using named tokens from this list produces designs that adapt correctly to light/dark mode.

---

## Navigation structure

iOS utility apps use one of two navigation patterns:

**Tab bar navigation (bottom):** 3–5 tabs. Each tab is a distinct section. No hamburger menu.

**Navigation controller (stack):** Primary list → Detail view. Back button in top-left of nav bar.

```
TabBar (frame, 390 x 83, layout: horizontal,
         alignItems: flex_start, justifyContent: space_around,
         fill: translucent ($bg at 80% opacity, blurred),
         stroke: { top: { color: "$separator", thickness: 0.5 } },
         padding: [8, 0, 0, 0])
│   // 83pt total: 49pt button area + 34pt home indicator area.
│   // Only show home indicator area on iPhone X+ (safe area).
└── TabItem × 3–5

TabItem (frame, fit_content x 49, layout: vertical,
          alignItems: center, gap: 3, padding: [8, 12, 0, 12])
├── TabIcon (frame, 25 x 25)
│   // SF Symbol, 25pt. Fill: $accent when active, $labelSecondary when inactive.
└── TabLabel (text, 10pt, $fontText, fontWeight: 500,
               fill: $accent when active, $labelSecondary when inactive,
               content: "Today")
```

---

## Navigation bar

```
NavigationBar (frame, 390 x 96, layout: vertical, fill: transparent)
│   // 96pt total: 44pt status bar area + 52pt nav bar.
│   // Background: adaptive — system material (translucent blur on scroll).
│   // On iOS 15+, large title bar collapses on scroll to standard title.
├── StatusBar (frame, 390 x 44, layout: horizontal,
│               alignItems: center, justifyContent: space_between,
│               padding: [0, 16])
│   // Contains: time, indicators (signal, wifi, battery). System-rendered.
│   // Represent with three placeholders: time (left), indicators (right).
└── NavBarContent (frame, 390 x 52, layout: horizontal,
                    alignItems: center, justifyContent: space_between,
                    padding: [0, 16])
    ├── BackButton? (frame, fit_content x 44, layout: horizontal,
    │                alignItems: center, gap: 4)
    │   ├── ChevronLeft (16 x 16, fill: "$accent")
    │   └── BackLabel (text, 17pt, fill: "$accent", content: "Back" or section name)
    ├── LargeTitle (text, 34pt, fontWeight: 700, $fontDisplay,
    │               fill: "$label",
    │               content: "Reminders")
    │   // Large title: appears when scrolled to top.
    │   // Standard title (17pt, fontWeight: 600) appears on scroll.
    └── TrailingButton (frame, 44 x 44, layout: none)
        // "+" button, "Edit" text, SF Symbol icon. 44×44 touch target.
        └── ButtonContent (text or icon, fill: "$accent")
```

---

## List row

The iOS list row is the primary component in utility apps. It must be exactly 44pt tall at minimum.

```
ListRow (frame, fill_container x 44, layout: horizontal,
          alignItems: center, padding: [0, 16], gap: 12,
          fill: "$bgTertiary")
│   // 44pt minimum height. The Apple HIG requirement for touch targets.
│   // Separator: 0.5pt hairline at $separator colour, inset 16pt from left
│   // (not full-width — standard iOS table cell separator inset).
├── LeadingIcon? (frame, 28 x 28, cornerRadius: 6)
│   // Optional. App-specific icon or system SF Symbol.
│   // 28pt is the standard inset icon size.
├── LabelStack (frame, fill_container x fit_content, layout: vertical, gap: 2)
│   ├── PrimaryLabel (text, 17pt, $fontText, fill: "$label",
│   │                  lineHeight: 1.35)
│   └── SecondaryLabel? (text, 15pt, $fontText, fill: "$labelSecondary")
│       // Optional detail text below primary label.
└── TrailingContent (frame, fit_content x fit_content, layout: horizontal,
                      alignItems: center, gap: 6)
    ├── ValueLabel? (text, 17pt, $fontText, fill: "$labelSecondary")
    │   // Optional: "On", "3 items", date.
    └── DisclosureIndicator? (chevron right, 12pt, fill: "$labelTertiary")
        // Shows when the row navigates deeper (navigation controller pattern).
```

### What generic looks like

```
// WRONG: touch target below 44pt
ListRow=I(list, { height: 36 })
// 36pt is below the Apple HIG minimum. It fails tap accuracy for users
// with motor difficulties and feels cramped on a touch interface.
// Always 44pt minimum.

// WRONG: full-width row separator (no inset)
separator=I(row, {
  type: "frame",
  width: "fill_container", height: 0.5,
  fill: "$separator"
})
// iOS table cell separators are inset 16pt from the left edge (or 76pt when
// there's a leading icon). Full-width separators look like web-style dividers,
// not native iOS. The inset is a clear native-vs-web signal.
```

---

## Bottom sheet

Sheets are the iOS idiom for contextual overlays. They slide up from the bottom.

```
BottomSheet (frame, 390 x fit_content, layout: vertical,
              fill: "$bgSecondary",
              cornerRadius: [13, 13, 0, 0])
│   // cornerRadius only on top two corners.
│   // Detents: 300pt (compact), 550pt (half), fill_container (full).
├── GrabHandle (frame, 36 x 5, cornerRadius: 2.5,
│               fill: rgba(60,60,67,0.3),
│               alignSelf: center, margin: [8, 0, 8, 0])
│   // Grab handle appears when the sheet is draggable.
│   // Always present on draggable sheets. 36×5pt.
├── SheetHeader? (frame, fill_container x 44, layout: horizontal,
│                  alignItems: center, justifyContent: space_between,
│                  padding: [0, 16])
│   ├── SheetTitle (text, 17pt, fontWeight: 600, $label,
│   │               content: "Add Reminder")
│   └── DoneButton (text, 17pt, fontWeight: 600, fill: "$accent",
│                    content: "Done")
└── SheetContent (frame, fill_container x fit_content, layout: vertical,
                   padding: [0, 0, 34, 0])
    // 34pt bottom padding for safe area (home indicator).
```

---

## Microcopy library

### Navigation bar buttons

iOS convention: text buttons for contextual actions, icon-only for common actions.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Create New | + (icon) |
| Edit Items | Edit |
| Go Back | Back (or parent section name) |
| Cancel Changes | Cancel |
| Save Changes | Done |
| Delete | (SF Symbol trash icon) |

### Empty state headlines

Match the section name and use positive framing.

| View | Headline | Subtext |
|------|---------|---------|
| Reminders list | "No Reminders" | "Tap + to add a reminder." |
| Notes list | "No Notes" | "Tap the compose button to get started." |
| Search results | "No Results" | "Try a different search." |

Apple's empty states are direct and factual, not conversational. One line headline, one line instruction.

---

## Verification checklist

### Touch targets

- [ ] **All interactive elements are 44×44pt minimum.**
  WHY: Apple HIG requirement. Below 44pt, tap accuracy drops significantly for users with motor difficulties and for anyone tapping while walking. Every row, button, and icon must meet this threshold. Small icons (16–24pt) are visually small but their touch target frame is always 44×44pt.

- [ ] **Tab bar items are 44pt tall (not counting safe area).**
  WHY: Tab bar items are the primary navigation. At 36pt, the tab is reachable with a precise tap but misses the guideline. 44pt is the floor.

### Typography

- [ ] **Body text is 17pt (`$fontText`), not 14pt or 16pt.**
  WHY: iOS system apps use 17pt as the standard text size. 14pt reads as "web density" on iOS; it's clearly not native. 16pt is close but still reads as slightly compressed. 17pt is the size the user's OS was tuned for; native apps should match it.

- [ ] **Large title is 34pt, fontWeight 700, `$fontDisplay`.**
  WHY: iOS's large title navigation bar uses exactly these values. Any other values look like a custom implementation, not a native one. "Invisible craft" means matching the system exactly.

### Navigation patterns

- [ ] **No hamburger menu.**
  WHY: iOS utility apps do not use hamburger menus. Navigation is either a tab bar (bottom) or a navigation controller (back/forward stack). A hamburger menu is a mobile web pattern that native iOS apps have not adopted. Its presence immediately reads as "built by a web developer."

- [ ] **Bottom sheet has a grab handle when draggable, top corner radii only.**
  WHY: The grab handle is the iOS signal for "you can drag this." Without it, users don't know the sheet is interactive. Radii on all four corners look like a floating card, not an iOS sheet. The two-corner radius is the system idiom.

### Separator inset

- [ ] **List row separators are inset 16pt from the left edge (76pt if there's a leading icon).**
  WHY: Full-width separators are the number-one signal that a design is "web-style iOS" rather than native iOS. The inset separator is the visual convention that UIKit uses by default. Without it, even a well-designed list reads as not native.

---

## Contrast examples

### Example 1: List row (correct vs generic)

**Correct:**

```
listRow=I(list, {
  type: "frame", name: "ListRow",
  layout: "horizontal", alignItems: "center",
  height: 44, width: "fill_container",
  padding: [0, 16], gap: 12,
  fill: "$bgTertiary"
})
primaryLabel=I(listRow, {
  type: "text", content: "Buy groceries",
  fontSize: 17, fontFamily: "$fontText",
  fill: "$label", lineHeight: 1.35
})
disclosure=I(listRow, {
  // chevron-right SF Symbol, 12pt, fill: "$labelTertiary"
})
// Separator: 0.5pt inset hairline at left: 16
```

Why this is right: 44pt height. 17pt label. `$label` colour. Inset separator. Disclosure indicator. These four properties together produce a native iOS list row.

**Generic:**

```
listRow=I(list, {
  type: "frame",
  height: 36,   // WRONG: below 44pt minimum
  padding: [0, 16], fill: "$surface"
})
primaryLabel=I(listRow, {
  type: "text", content: "Buy groceries",
  fontSize: 14, fill: "$textPrimary"   // WRONG: 14pt (web density)
})
separator=I(list, {
  type: "frame",
  width: "fill_container", height: 1,   // WRONG: full-width, 1pt (not 0.5pt)
  fill: "$border"
})
```

Why this is wrong: 36pt rows, 14pt text, full-width 1pt separators. Three signals that say "web app in a browser frame." The iOS native register requires 44pt rows, 17pt text, and 0.5pt inset separators.

---

### Example 2: Bottom sheet (correct vs generic)

**Correct:**

```
sheet=I(canvas, {
  type: "frame", name: "BottomSheet",
  layout: "vertical",
  width: 390, cornerRadius: [13, 13, 0, 0],
  fill: "$bgSecondary"
})
grabHandle=I(sheet, {
  type: "frame", name: "GrabHandle",
  width: 36, height: 5, cornerRadius: 2.5,
  fill: "rgba(60,60,67,0.3)",
  alignSelf: "center"
})
sheetTitle=I(sheet, {
  type: "text", content: "Add Reminder",
  fontSize: 17, fontWeight: 600, fill: "$label"
})
```

Why this is right: top-only corner radii, grab handle, `$bgSecondary` fill, 17pt title. Matches UIKit's `UISheetPresentationController` appearance exactly.

**Generic:**

```
sheet=I(canvas, {
  type: "frame",
  cornerRadius: 16,   // WRONG: all four corners
  fill: "$surface",   // WRONG: white instead of bgSecondary
  width: 390
})
sheetTitle=I(sheet, {
  type: "text", content: "Add Reminder",
  fontSize: 18, fontWeight: 700   // WRONG: not native iOS typescale
  // No grab handle
})
```

Why this is wrong: all-corner radii look like a floating card, not an iOS sheet. White fill instead of `$bgSecondary` misses the system layering. Missing grab handle means the user doesn't know it's draggable. 18pt/700 weight diverges from the 17pt/600 iOS standard.
