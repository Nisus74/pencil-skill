# cross-platform-modern

Mobile-first apps built with React Native, Expo, or Flutter that work across iOS and Android. The design language is deliberately cross-platform: it doesn't pretend to be fully native, but it doesn't look like a web app either. Custom components, brand typography, and a recognisable visual character.

**Surface category:** mobile
**Exemplars:** Linear mobile (React Native), Notion mobile, Figma mobile, Vercel mobile
**Confidence:** high; Linear mobile confirmed from direct use (May 2026); Figma mobile from direct use

Read this alongside `references/batch-design-grammar.md`. Mobile canvas: 390×844 (iPhone 15 standard). Cross-platform apps use custom fonts, not SF Pro. They use platform primitives but not system-native styles. The result looks polished and modern rather than natively integrated.

---

## When to use this archetype

Pick this for React Native, Expo, or Flutter apps where the brief is "great mobile experience" rather than "native iOS." Skip it when the product specifically targets iOS and must feel fully native; use `ios-native-utility` instead. Skip it for mobile web apps; this archetype is for compiled cross-platform apps.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#0D0D0F` (dark preferred) or `#FAFAF9` (light) | Background. Cross-platform modern apps trend dark. |
| `$bgPanel` | `#161618` (dark) or `#F3F3F5` (light) | Elevated surface. Cards, modals, sheets. |
| `$bgRow` | `#1E1E22` (dark) or `#EEEEF0` (light) | List row hover/selected state. |
| `$textPrimary` | `#F0EEEC` (dark) or `#111110` (light) | Primary content. |
| `$textSecondary` | `#A8A29E` (dark) or `#6B6A6B` (light) | Metadata, labels. |
| `$textMuted` | `#57534E` (dark) or `#A1A0A0` (light) | Placeholder, timestamps. |
| `$border` | `#2A2A2E` (dark) or `#E7E5E4` (light) | Dividers, card borders. |
| `$accent` | Saturation 55–65%. | CTAs, active states, links. |
| `$fontBody` | `Inter` | Body text. Not SF Pro; this is a deliberate cross-platform font choice. |
| `$fontDisplay` | `Inter Display` or brand display font. | Headings. |
| `$fontMono` | `Geist Mono` | Code, IDs, technical data. |

---

## Page shell

```
MobileScreen (frame, 390 x 844, layout: vertical, fill: "$bg")
├── StatusBar (frame, 390 x 44, layout: horizontal,
│               fill: transparent)
│   // Status bar area: time left, indicators right.
│   // In dark mode: white text. In light mode: black text.
│   // Always fill the 44pt status bar area — don't let content bleed into it.
├── ContentArea (frame, 390 x fit_content, layout: vertical,
│                fill: "$bg", overflow: "vertical_scroll")
│   // Scrollable main content.
│   // Bottom safe area: 34pt for home indicator.
└── BottomBar (frame, 390 x 83, layout: horizontal,
               fill: "$bg",
               stroke: { top: { color: "$border", thickness: 0.5 } })
    // Tab bar or bottom toolbar. 49pt content + 34pt safe area.
```

---

## Top navigation bar

Cross-platform apps typically use custom navigation headers, not system UIKit bars.

```
NavBar (frame, 390 x 52, layout: horizontal,
         alignItems: center, justifyContent: space_between,
         padding: [0, 16], fill: "$bg")
│   // 52pt. Custom height (not UIKit's default 44pt).
│   // No translucent blur by default — the custom nav bar has a solid fill.
├── BackButton? (frame, 44 x 44, layout: none, alignItems: center)
│   // 44pt touch target even if the visual is just a 20pt chevron.
│   // Chevron-left icon, $textSecondary. No "Back" label.
├── NavTitle (text, 17pt, fontWeight: 600, $textPrimary, $fontDisplay,
│             textAlign: "center", fill_container)
└── TrailingAction (frame, 44 x 44, layout: none, alignItems: center)
    // Icon button. 44pt touch target.
```

---

## List row

```
ListRow (frame, 390 x 52, layout: horizontal,
          alignItems: center, padding: [0, 16], gap: 12,
          fill: transparent)
│   // 52pt. Cross-platform modern rows are slightly taller than iOS native (44pt)
│   // because the typography is Inter (slightly more generous than SF Pro).
│   // Active/pressed: fill: "$bgRow". No persistent separators between rows.
│   // Separator rule: either ALL rows have hairlines, or NONE do. Not mixed.
├── RowIcon? (frame, 32 x 32, cornerRadius: 8, fill: "$bgPanel")
│   // Custom branded icon. NOT a system SF Symbol.
│   // 32pt with 8pt corner radius is the cross-platform convention.
├── RowContent (frame, fill_container x fit_content, layout: vertical, gap: 2)
│   ├── RowTitle (text, 15pt, $fontBody, fontWeight: 500, $textPrimary)
│   └── RowSubtitle? (text, 13pt, $fontBody, $textSecondary)
└── RowMeta (frame, fit_content x fit_content, layout: horizontal,
              alignItems: center, gap: 6)
    ├── MetaLabel? (text, 12pt, $textMuted)
    └── ChevronRight? (frame, 16 x 16, fill: "$textMuted")
```

### What generic looks like

```
// WRONG: row height 44pt (iOS system height, not cross-platform Inter height)
ListRow=I(list, { height: 44 })
// 44pt is correct for iOS native with SF Pro.
// Inter at 15pt needs 52pt to breathe at the same visual density.
// 44pt with Inter looks compressed compared to the system baseline.

// WRONG: SF Symbol icons in a cross-platform app
RowIcon=I(row, {
  // Using SF Symbols (apple.logo, list.bullet, etc.)
})
// SF Symbols are iOS-only. Cross-platform apps use custom icon sets or
// lucide-react / phosphor-icons equivalents. SF Symbols in a React Native
// design read as "iOS native mockup" not "cross-platform app."
```

---

## Bottom tab bar

```
TabBar (frame, 390 x 83, layout: horizontal,
         alignItems: flex_start, justifyContent: space_around,
         fill: "$bg",
         stroke: { top: { color: "$border", thickness: 0.5 } },
         padding: [8, 0, 0, 0])
│   // 83pt total: 49pt button area + 34pt home indicator safe area.
│   // $bg fill, NOT translucent. Cross-platform apps typically use solid fills.
└── TabItem × 3–5

TabItem (frame, fit_content x 49, layout: vertical,
          alignItems: center, gap: 3, padding: [8, 12, 0, 12])
├── TabIcon (frame, 24 x 24)
│   // Custom icon. 24pt. Fill: $accent when active, $textMuted when inactive.
└── TabLabel (text, 11pt, fontWeight: 500,
               fill: "$accent" when active, fill: "$textMuted" when inactive)
```

---

## Modal / bottom sheet

Cross-platform sheets follow a simplified version of iOS's sheet idiom, without system materials.

```
BottomSheet (frame, 390 x fit_content, layout: vertical,
              fill: "$bgPanel",
              cornerRadius: [16, 16, 0, 0])
│   // cornerRadius on top corners only. 16pt (slightly rounder than iOS native 13pt).
├── DragHandle (frame, 36 x 4, cornerRadius: 2,
│               fill: "$border", alignSelf: center,
│               margin: [10, 0, 10, 0])
│   // 4pt height (vs iOS native 5pt). Slightly flatter for cross-platform look.
├── SheetHeader (frame, fill_container x 48, layout: horizontal,
│                 alignItems: center, justifyContent: space_between,
│                 padding: [0, 16])
│   ├── SheetTitle (text, 16pt, fontWeight: 600, $textPrimary, $fontDisplay)
│   └── CloseButton (frame, 32 x 32, cornerRadius: 16, fill: "$bgRow")
│       └── CloseIcon (16×16, $textSecondary)
│       // Cross-platform apps use an × icon button, not a "Done" text link.
└── SheetContent (frame, fill_container x fit_content,
                   padding: [0, 0, 34, 0])
```

---

## Microcopy library

### Navigation

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Go back | ← (chevron only) |
| Close dialog | × (icon button) |
| OK | Done |
| Cancel and return | Cancel |

### Tab labels

Keep tab labels to one word. If a concept requires two words, reconsider the information organisation.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Home Screen | Home |
| My Activity | Activity |
| Settings & Preferences | Settings |
| All Projects | Projects |

### Action buttons

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Submit form | Save |
| Create new item | + New [noun] |
| Apply changes | Apply |
| Confirm delete | Delete |

---

## Verification checklist

### Touch targets

- [ ] **All interactive elements have a 44×44pt touch target, even if visually smaller.**
  WHY: Apple HIG and Android Material require 44pt / 48dp minimums for accessible targets. Cross-platform apps must respect both. A 24pt icon button with only a 24pt touch target will fail taps on a moving device. Wrap small icons in a 44×44pt transparent frame.

### Typography

- [ ] **Body text is `$fontBody` (Inter), not SF Pro.**
  WHY: SF Pro is the iOS system font. Using it in a React Native design signals "this is an iOS native mockup." Inter reads as a deliberately cross-platform product. The font choice is the primary indicator of intent.

- [ ] **Body text is 15pt, not 17pt.**
  WHY: 17pt is iOS native standard (SF Pro). Inter at 17pt reads as slightly large for a cross-platform app. 15pt with Inter's generous x-height produces similar reading comfort to 17pt SF Pro. Both Things 3 and Linear mobile use ~15pt for primary list content.

### Layout

- [ ] **List rows are 52pt tall (not 44pt).**
  WHY: Inter is more generous than SF Pro. 44pt rows with 15pt Inter look slightly cramped compared to the same density in SF Pro. 52pt provides the same comfortable density while accommodating Inter's metrics.

- [ ] **Bottom sheet corner radii are 16pt (top corners only).**
  WHY: 16pt is the cross-platform convention; iOS native uses 13pt. The extra 3pt is subtle but distinguishes the cross-platform idiom from the native one. All-four-corner radii make the sheet look like a card, not a sheet.

- [ ] **Status bar area (44pt) is always reserved at the top of every screen.**
  WHY: Cross-platform apps must reserve the status bar area or content bleeds under the time/battery indicators. It is not optional; it is a required safe area.

---

## Contrast examples

### Example 1: List row (correct vs generic)

**Correct:**

```
listRow=I(screen, {
  type: "frame", name: "ListRow",
  layout: "horizontal", alignItems: "center",
  height: 52, width: "fill_container",
  padding: [0, 16], gap: 12,
  fill: "transparent"
})
rowIcon=I(listRow, {
  type: "frame", width: 32, height: 32, cornerRadius: 8,
  fill: "$bgPanel"
  // Custom icon inside, not SF Symbol
})
rowTitle=I(listRow, {
  type: "text", content: "Project Alpha",
  fontSize: 15, fontFamily: "$fontBody",
  fontWeight: 500, fill: "$textPrimary"
})
```

Why this is right: 52pt height for Inter typography. Custom icon in a rounded square. 15pt Inter. Transparent row fill with no separator.

**Generic:**

```
listRow=I(screen, {
  type: "frame", height: 44,   // WRONG: iOS native height for SF Pro
  layout: "horizontal", padding: [0, 16]
})
rowIcon=I(listRow, {
  // SF Symbol: "folder.fill"  WRONG: system icon
})
rowTitle=I(listRow, {
  type: "text", fontSize: 17,   // WRONG: iOS native text size for SF Pro
  fontFamily: "SF Pro Text"   // WRONG: system font in cross-platform design
})
```

Why this is wrong: 44pt / 17pt / SF Pro is the iOS native register. In a React Native app this combination reads as "someone copied an iOS screen, not designed a cross-platform app." The font alone signals platform intent.

---

### Example 2: Bottom sheet (correct vs generic)

**Correct:**

```
sheet=I(screen, {
  type: "frame", name: "BottomSheet",
  layout: "vertical",
  width: 390, cornerRadius: [16, 16, 0, 0],
  fill: "$bgPanel"
})
dragHandle=I(sheet, {
  type: "frame", width: 36, height: 4, cornerRadius: 2,
  fill: "$border", alignSelf: "center"
})
closeButton=I(sheet, {
  type: "frame", width: 32, height: 32, cornerRadius: 16,
  fill: "$bgRow"
  // × icon inside, 16pt, $textSecondary
})
```

Why this is right: top-only corner radii at 16pt. 4pt drag handle. `$bgPanel` fill. Close button is a circular icon button (cross-platform convention), not a text "Done" link (iOS native convention).

**Generic:**

```
sheet=I(screen, {
  type: "frame",
  cornerRadius: 16,   // WRONG: all four corners — looks like a card
  fill: "#FFFFFF"   // WRONG: white in a dark-mode app
})
// No drag handle
doneButton=I(sheet, {
  type: "text", content: "Done",   // WRONG: iOS native text link style
  fill: "$accent"
})
```

Why this is wrong: all-corner radii produce a floating card, not a sheet. No drag handle means users can't tell if it's dismissible. "Done" text link is the iOS native idiom; cross-platform apps use icon close buttons.
