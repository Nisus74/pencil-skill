# modern-pro-tool

Refined-dense B2B software for people who live inside it. Chrome disappears; the work surface leads. Linear set the visual language for this archetype in the mid-2020s and it has become the canonical reference.

**Surface category:** saas-apps/b2b
**Exemplars:** Linear (primary), Notion business workspaces (document-leaning variant)
**Confidence:** high; confirmed against Linear devtools measurements (May 2026)

Read this alongside `references/chart-anatomy.md` and `references/batch-design-grammar.md`. This file covers archetype-specific rules. When `chart-anatomy.md` and this file conflict, this file wins for this archetype.

---

## When to use this archetype

Pick this when the brief is "modern pro software" without a strong pull toward analytics, enterprise, or workflow collaboration. If the brief is primarily charts and KPIs, use `analytics-dashboard`. If it leans heavily on status-colour-rich workflow boards, use `workflow-platform`. If the user has supplied direction, follow it and use this file only for the parts they didn't specify.

**Key distinction from `analytics-dashboard`:** active sidebar item uses a filled background ($surfaceActive), not a 2px accent border. The accent is reserved for actions, not navigation state. If you mix these up, the designs look like each other.

---

## Design token reference

| Token | Light value | Dark value | Role |
|-------|-------------|------------|------|
| `$bg` | `#FAFAFA` | `#0E0E10` | Page background. Light is canonical for this archetype. |
| `$surface` | `#FFFFFF` | `#17171A` | Main content area, card backgrounds. |
| `$surfaceMuted` | `#F4F4F5` | `#1F1F23` | Sidebar background, table headers, code blocks. |
| `$surfaceActive` | `#EBEBED` | `#2A2A2E` | Active sidebar item fill. Slightly darker than sidebar. |
| `$surfaceHover` | `#EFEFEF` | `#252528` | Sidebar item hover. Between default and active. |
| `$border` | `#E7E5E4` | `#2E2A2E` | 1px hairlines on cards, panels, rows. |
| `$borderMuted` | `#F0EEEC` | `#252428` | Internal dividers, subtle separators. |
| `$textPrimary` | `#111110` | `#EEEEEC` | Issue titles, page titles, active nav labels. |
| `$textSecondary` | `#6B6A6B` | `#A8A29E` | Supporting copy, default nav labels, property values. |
| `$textMuted` | `#A1A0A0` | `#57534E` | Counts, timestamps, keyboard shortcut chips, inactive metadata. |
| `$accent` | Saturated indigo or brand hue, saturation 70–85%. | | Primary CTA fill, link affordances, focus outlines, priority icons where warranted. |
| `$fontUI` | `Inter Display` | | All UI text. This archetype overrides the default `Geist`; `Inter Display` is the exemplar font. |
| `$fontMono` | `Geist Mono` or `Berkeley Mono` | | Counts, estimates, keyboard shortcut chips, version strings. |
| `$positive` | `#16A34A` | `#22C55E` | Done/completed status. |
| `$warning` | `#D97706` | `#F59E0B` | In-progress/started status. |
| `$negative` | `#DC2626` | `#F87171` | Urgent/blocked status. |

---

## Page shell

```
DashboardPage (frame, 1440 x 900, layout: horizontal,
               fill: "$bg")
├── Sidebar (frame, 232 x fill_container, layout: vertical,
│            fill: "$surfaceMuted",
│            stroke: { color: "$border", thickness: 1 })
│   // 232px — Linear's measured sidebar width. Range: 220–248.
│   // No drop_shadow. The 1px border handles separation.
└── MainContent (frame, fill_container x fill_container, layout: vertical,
                 fill: "$surface")
```

---

## Sidebar

### Anatomy

```
Sidebar (frame, 232 x fill_container, layout: vertical,
         fill: "$surfaceMuted",
         stroke: { color: "$border", thickness: 1 })
├── SidebarTop (frame, fill_container x 48, layout: horizontal,
│               alignItems: center, padding: [0, 8], gap: 4)
│   ├── WorkspaceIcon (frame, 20 x 20, cornerRadius: 4, fill: "$accent")
│   ├── WorkspaceName (text, $textSm, fontWeight: 600, $textPrimary,
│   │                  content: "Workspace", width: "fill_container")
│   ├── ChevronIcon (icon_font, 12 x 12, iconFontFamily: "lucide",
│   │               iconFontName: "chevron-down", fill: "$textMuted")
│   └── TopIcons (frame, fit_content x fit_content, layout: horizontal, gap: 2)
│       ├── SearchIcon (icon_font, 16 x 16, iconFontFamily: "lucide",
│       │              iconFontName: "search", fill: "$textSecondary")
│       └── ComposeIcon (icon_font, 16 x 16, iconFontFamily: "lucide",
│                        iconFontName: "edit-3", fill: "$textSecondary")
├── SidebarNav (frame, fill_container x fill_container,
│               layout: vertical, gap: 1, padding: [4, 6])
│   ├── NavItem_Active (frame, fill_container x 28, layout: horizontal,
│   │                    alignItems: center, gap: 6, padding: [0, 8],
│   │                    cornerRadius: 6, fill: "$surfaceActive")
│   │   // Active item: filled background. NO border accent.
│   │   // This is the primary visual distinction from analytics-dashboard.
│   │   ├── NavIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
│   │   │           iconFontName: "inbox", fill: "$accent")
│   │   ├── NavLabel (text, $textSm, fontWeight: 500, $textPrimary,
│   │   │             content: "Inbox", width: "fill_container")
│   │   └── CountBadge (text, 11px, $fontMono, $textMuted, content: "3")
│   ├── NavItem_Default (frame, fill_container x 28, layout: horizontal,
│   │                     alignItems: center, gap: 6, padding: [0, 8],
│   │                     cornerRadius: 6)
│   │   // No fill. Hover state (not shown in static design): fill $surfaceHover.
│   │   ├── NavIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
│   │   │           iconFontName: "circle-dot", fill: "$textSecondary")
│   │   └── NavLabel (text, $textSm, $textSecondary, content: "My issues",
│   │                  width: "fill_container")
│   ├── SectionHeader (frame, fill_container x 24, layout: horizontal,
│   │                   alignItems: center, gap: 4, padding: [0, 8])
│   │   ├── SectionLabel (text, $textSm, fontWeight: 500, $textSecondary,
│   │   │                  content: "Workspace")
│   │   │   // Sentence-case lowercase. NOT "WORKSPACE". NOT "workspace ▼" in title case.
│   │   └── SectionChevron (icon_font, 10 x 10, iconFontFamily: "lucide",
│   │                        iconFontName: "chevron-down", fill: "$textMuted")
│   └── NestedNavItem (frame, fill_container x 28, layout: horizontal,
│                       alignItems: center, gap: 6,
│                       padding: [0, 8, 0, 20],  // 20px left = 8 base + 12 indent
│                       cornerRadius: 6)
│       ├── TeamIcon (frame, 14 x 14, cornerRadius: 2, fill: "$warning")
│       │   // Each team gets a distinct colour swatch, not a generic icon
│       └── TeamName (text, $textSm, $textSecondary, content: "Product")
└── SidebarFooter (frame, fill_container x 40, layout: horizontal,
                    alignItems: center, padding: [0, 12], gap: 8)
    ├── UserAvatar (frame, 22 x 22, cornerRadius: 11, fill: "$surfaceActive")
    └── HelpIcon (icon_font, 16 x 16, iconFontFamily: "lucide",
                  iconFontName: "help-circle", fill: "$textMuted")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Sidebar width | 232px | Range: 220–248. Slightly wider than analytics-dashboard to accommodate team names. |
| Item height | 28px | 4px tighter than analytics-dashboard. This archetype is denser. |
| Item corner radius | 6px | Same as analytics-dashboard. |
| Active item fill | `$surfaceActive` | NOT an accent border. The background IS the active state signal. |
| Section header height | 24px | Shorter than nav items. Hierarchically subordinate. |
| Section label case | Sentence-case lowercase | "Workspace", not "WORKSPACE" or "workspace". |
| Indent per nesting level | 12px additional left padding | Applied via padding array: `[0, 8, 0, base+12]`. |
| Count badge | 11px `$fontMono` `$textMuted` | Right-aligned, no background pill. Plain text. |

### Worked ops (sidebar skeleton)

```
sidebarTop=I(sidebar, {
  type: "frame", name: "SidebarTop",
  layout: "horizontal", alignItems: "center",
  width: "fill_container", height: 48,
  gap: 4, padding: [0, 8]
})
wsIcon=I(sidebarTop, {
  type: "frame", name: "WorkspaceIcon",
  width: 20, height: 20, cornerRadius: 4, fill: "$accent"
})
wsName=I(sidebarTop, {
  type: "text", name: "WorkspaceName",
  content: "Workspace", fontFamily: "$fontUI",
  fontSize: "$textSm", fontWeight: 600, fill: "$textPrimary",
  width: "fill_container"
})
wsChevron=I(sidebarTop, {
  type: "icon_font", name: "WorkspaceChevron",
  iconFontFamily: "lucide", iconFontName: "chevron-down",
  width: 12, height: 12, fill: "$textMuted"
})
nav=I(sidebar, {
  type: "frame", name: "SidebarNav",
  layout: "vertical", gap: 1, padding: [4, 6],
  width: "fill_container", height: "fill_container"
})
activeItem=I(nav, {
  type: "frame", name: "NavItem_Inbox",
  layout: "horizontal", alignItems: "center",
  width: "fill_container", height: 28,
  gap: 6, padding: [0, 8], cornerRadius: 6,
  fill: "$surfaceActive"
})
activeIcon=I(activeItem, {
  type: "icon_font", name: "InboxIcon",
  iconFontFamily: "lucide", iconFontName: "inbox",
  width: 14, height: 14, fill: "$accent"
})
activeLabel=I(activeItem, {
  type: "text", name: "NavLabel",
  content: "Inbox", fontFamily: "$fontUI",
  fontSize: "$textSm", fontWeight: 500, fill: "$textPrimary",
  width: "fill_container"
})
activeCount=I(activeItem, {
  type: "text", name: "CountBadge",
  content: "3", fontFamily: "$fontMono",
  fontSize: 11, fill: "$textMuted"
})
```

### What generic looks like

```
// WRONG: active item as a coloured pill or accent border
activeItem=I(nav, {
  fill: [{ type: "color", color: "$accent", opacity: 0.12 }]
})
// Use $surfaceActive (neutral grey background), not accent tint.
// An accent tint on every active nav item makes the sidebar compete with the content.

// WRONG: section headers all-caps or small-caps
sectionLabel=I(sectionHeader, {
  content: "WORKSPACE",
  // or: content: "WORKSPACE", textTransform: "uppercase"
})
// Use sentence-case lowercase: "Workspace". Linear is deliberate about this.
// All-caps section headers read as archetype mismatch.

// WRONG: count badge as a filled pill
CountBadge=I(activeItem, {
  type: "frame", cornerRadius: 8, fill: "$accent",
  padding: [0, 4], ...
})
// Plain text. 11px mono. No background. No border. Just the number.

// WRONG: sidebar 280px wide (common default)
sidebar=I(page, { width: 280, ... })
// 280px is too wide. 232px.
```

**Detect:**
- Active item shows any colour fill or border (not a neutral grey background): fix to `fill: "$surfaceActive"`.
- Section headers are uppercase or small-caps: fix to sentence-case lowercase.
- Count badge has a background pill: remove the frame, use a plain text node.

---

## Breadcrumb top bar

In this archetype the topbar is minimal: a thin breadcrumb line, not a full 56px bar. It's structurally part of the main content column, not a separate panel.

### Anatomy

```
Topbar (frame, fill_container x 40, layout: horizontal, alignItems: center,
         justifyContent: space_between, padding: [0, 20],
         fill: "$surface",
         stroke: { color: "$border", thickness: 1 })
         // Height: 40px. Compact — this archetype doesn't need a tall topbar.
├── BreadcrumbRow (frame, fit_content x fill_container, layout: horizontal,
│                  alignItems: center, gap: 4)
│   ├── BreadcrumbParent (text, $textSm, $textMuted,
│   │                     content: "Product")
│   ├── BreadcrumbSeparator (text, $textSm, $textMuted, content: "›")
│   ├── BreadcrumbCurrent (text, $textSm, fontWeight: 500, $textPrimary,
│   │                      content: "Product Strategy & Specs")
│   └── StarIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
│                 iconFontName: "star", fill: "$textMuted")
└── TopbarActions (frame, fit_content x fill_container, layout: horizontal,
                    alignItems: center, gap: 4)
    ├── FilterIcon (icon_font, 16 x 16, iconFontFamily: "lucide",
    │              iconFontName: "sliders-horizontal", fill: "$textSecondary")
    └── MoreIcon (icon_font, 16 x 16, iconFontFamily: "lucide",
                  iconFontName: "more-horizontal", fill: "$textSecondary")
```

### Critical rules

- Height: 40px. Not 56px. The topbar is a positioning aid, not a content area.
- No filled buttons in the topbar. Actions are icon-only at $textSecondary.
- Breadcrumb separator is `›` (single angle quote), not `/` or `>`.

---

## Issue row

The workhorse component. Every list view is rows of these.

### Anatomy

```
IssueRow (frame, fill_container x 32, layout: horizontal,
           alignItems: center, padding: [0, 16], gap: 8)
           // Row height: 32px. Dense. 36px for touch-primary contexts.
├── StatusIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
│               iconFontName: "circle", fill: "$textMuted")
│   // Status indicator: changes icon and fill per status:
│   // Backlog: circle outline, $textMuted
│   // In progress: circle with half fill, $warning
│   // Done: circle-check, $positive
│   // Cancelled: x-circle, $textMuted opacity 0.5
├── PriorityIcon (icon_font, 12 x 12, iconFontFamily: "lucide",
│                iconFontName: "bar-chart-2", fill: "$negative")
│   // Priority: bar-chart-2 ($negative = Urgent), minus ($textMuted = No priority)
│   // Position: left of title, very small, subtle
├── IssueID (text, $textXs, $fontMono, $textMuted,
│            content: "PRO-124", width: 48)
│   // Issue identifier. Monospace. Muted. Fixed width so title column is stable.
├── IssueTitle (text, $textSm, $textPrimary,
│               content: "Fix authentication timeout",
│               width: "fill_container")
├── LabelChips (frame, fit_content x fit_content, layout: horizontal, gap: 4)
│   └── LabelChip (frame, fit_content x 18, layout: horizontal,
│                   alignItems: center, padding: [0, 6], cornerRadius: 3,
│                   fill: "$surfaceMuted")
│       └── ChipText (text, 11px, $textSecondary, content: "Bug")
├── AssigneeAvatar (frame, 18 x 18, cornerRadius: 9, fill: "$surfaceActive")
└── DateLabel (text, $textXs, $fontMono, $textMuted,
               content: "Mar 14", width: 36, textAlign: "right")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Row height | 32px | Never below 28px. 36px acceptable if touch targets matter. |
| Row padding | `[0, 16]` | Generous horizontal. Zero vertical (let height handle it). |
| Status icon | 14 × 14px | Do not enlarge. It is a status indicator, not a primary element. |
| Issue ID | 48px fixed width | Monospace. Right-aligned or left-aligned is fine; consistent width is mandatory. |
| Label chip height | 18px | Compact. Corner radius 3px (very slight, almost square). |
| Avatar | 18 × 18px | Circular. Very small at row scale. |

### What generic looks like

```
// WRONG: row height 44–48px (touch-safe but bloated for desktop pro tools)
IssueRow=I(list, { height: 44, ... })
// Desktop pro tools use 32px. The density is the feature.

// WRONG: status as a text-only badge ("In Progress") with no icon
// Status in this archetype is an icon. The text is secondary or absent at list scale.

// WRONG: alternating row backgrounds (zebra stripes)
// Use a bottom border at $borderMuted. No alternating fills.

// WRONG: label chips with large cornerRadius: 8+ (pill-shaped)
// Use cornerRadius: 3. Pill-shaped chips read as navigation tags, not content labels.

// WRONG: all metadata right-aligned with fill_container widths
// Assign fixed widths: IssueID 48px, DateLabel 36px. Otherwise columns shift as content changes.
```

---

## Keyboard shortcut chip

### Anatomy

A shortcut chip is always embedded in a button or menu item — it never stands alone.

```
// Inside a primary button (Create issue C):
PrimaryButton (frame, fit_content x 32, layout: horizontal,
               alignItems: center, gap: 6, padding: [0, 12], cornerRadius: 6,
               fill: "$accent")
├── ButtonText (text, $textSm, fontWeight: 500, fill: "$surface",
│               content: "Create new issue")
└── ShortcutChip (frame, fit_content x 20, layout: horizontal,
                  alignItems: center, justifyContent: center,
                  padding: [0, 5], cornerRadius: 4,
                  fill: { color: "$textPrimary", opacity: 0.15 })
    └── ShortcutText (text, 11px, $fontMono, fill: "$surface", content: "C")

// Multi-key shortcut (G then S):
ShortcutChips (frame, fit_content x fit_content, layout: horizontal, gap: 2)
├── ChipG (same shape as above, content: "G")
├── ThenLabel (text, $textXs, $textMuted, content: "then")
└── ChipS (same shape as above, content: "S")
```

### Critical rules

- Chip fill: `fill: { color: "$textPrimary", opacity: 0.15 }` inside an accent-filled button. Not a hardcoded colour.
- Chip font: `$fontMono` always. 11px. Never $fontUI for shortcut keys.
- Chip size: height 20px, padding `[0, 5]`. Slightly shorter than full button height.
- Single letters and symbol keys. Multi-key sequences use a "then" label, not a `+`.

### What generic looks like

```
// WRONG: no shortcut chip inside the primary CTA
// In this archetype, the primary action button always shows its keyboard shortcut.
// Missing shortcut = the design doesn't feel like a pro tool.

// WRONG: shortcut chip using $fontUI
ShortcutText=I(chip, { fontFamily: "$fontUI" })
// Use $fontMono. Keyboard characters need monospace.

// WRONG: shortcut chip with white background pill outside the button
// Chips sit inside button fills. A floating white chip reads as a badge, not a shortcut.
```

---

## Empty state

### Anatomy

```
EmptyState (frame, fill_container x fit_content, layout: vertical,
             alignItems: center, gap: 12, padding: [32, 24])
├── IconCluster (frame, 48 x 48, layout: none)
│   // 4 small abstract icons in a 2×2 grid. Each 16×16. Positioned at corners of the 48×48 frame.
│   // Use abstract Lucide shapes — not thematic icons that illustrate the data.
│   ├── Icon1 (icon_font, 16 x 16, iconFontFamily: "lucide",
│   │         iconFontName: "circle", fill: "$accent",
│   │         x: 0, y: 0)
│   ├── Icon2 (icon_font, 16 x 16, iconFontFamily: "lucide",
│   │         iconFontName: "triangle", fill: "$warning",
│   │         x: 20, y: 0, opacity: 0.7)
│   ├── Icon3 (icon_font, 16 x 16, iconFontFamily: "lucide",
│   │         iconFontName: "square", fill: "$textMuted",
│   │         x: 0, y: 20, opacity: 0.5)
│   └── Icon4 (icon_font, 16 x 16, iconFontFamily: "lucide",
│              iconFontName: "zap", fill: "$positive",
│              x: 20, y: 20, opacity: 0.6)
│   // Spacing: icons at 0px and 20px give a slight gap between them.
│   // All four different: different icons, different colours, slightly different opacities.
├── EmptyHeading (text, $textBase, fontWeight: 600, $textPrimary,
│                 content: "Active issues",
│                 textAlign: "center")
├── EmptyBody (text, $textSm, $textSecondary,
│              content: "Issues that are actively being worked on will appear here.",
│              textAlign: "center", width: 260)
├── PrimaryButton (frame, fit_content x 32, layout: horizontal,
│                  alignItems: center, gap: 6, padding: [0, 12], cornerRadius: 6,
│                  fill: "$accent")
│   ├── ButtonText (text, $textSm, fontWeight: 500, fill: "$surface",
│   │               content: "Create new issue")
│   └── ShortcutChip (frame, 20 x 20, layout: horizontal,
│                     alignItems: center, justifyContent: center",
│                     cornerRadius: 4,
│                     fill: { color: "$textPrimary", opacity: 0.15 })
│       └── ShortcutText (text, 11px, $fontMono, fill: "$surface", content: "C")
└── SecondaryButton (frame, fit_content x 32, layout: horizontal,
                     alignItems: center, padding: [0, 12], cornerRadius: 6,
                     stroke: { color: "$border", thickness: 1 })
    └── ButtonText (text, $textSm, $textSecondary, content: "Documentation")
```

### What generic looks like

```
// WRONG: large illustrated mascot or scene
// A person holding an empty box, confetti shapes, "It's quiet here!" heading.
// This archetype uses 4 small abstract icons. Not an illustration. Not a mascot.

// WRONG: single icon (like analytics-dashboard empty state)
// analytics-dashboard uses one muted icon. This archetype uses 4 abstract icons in a cluster.
// The two archetypes have different empty state signatures — don't mix them.

// WRONG: three or more CTAs ("Create / Import / Explore Demo")
// Two buttons: one primary action with keyboard shortcut, one secondary fallback.

// WRONG: heading with an exclamation mark or question ("No issues yet — get started!")
// "Active issues" as a heading. Short, declarative, no exclamation.
```

---

## AI assistant pill

Every modern pro tool in 2026 has an entry point to the AI assistant. This archetype's signature placement is a floating pill in the bottom-right of the main content area.

### Anatomy

```
AskAIPill (frame, fit_content x 32, layout: horizontal,
            alignItems: center, gap: 6, padding: [0, 14], cornerRadius: 16,
            fill: "$surface",
            stroke: { color: "$border", thickness: 1 },
            effect: [{ type: "drop_shadow", blur: 8, y: 2, opacity: 0.08 }])
            // Floating pill: this IS one of the few places a shadow is correct.
            // Floating elements (menus, pills, tooltips) use soft shadows.
            // Fixed card surfaces do not.
├── ChatIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
│             iconFontName: "message-circle", fill: "$textSecondary")
├── PillLabel (text, $textSm, $textSecondary, content: "Ask Linear")
└── HistoryIcon (icon_font, 14 x 14, iconFontFamily: "lucide",
                 iconFontName: "clock", fill: "$textMuted")
```

### Placement

The pill sits in `layout: none` mode at the bottom-right of the main content frame, with x/y positioning:

```
// Inside the main content frame (layout: none for this specific overlay):
AskAIPill positioned:
  x: fill_container minus pill width minus 24
  y: fill_container minus 32 minus 24
// In Pencil: place the pill in a layout: none container that overlays the content area,
// with manual x/y set to bottom-right corner padding.
```

---

## Microcopy library

Write microcopy in this register: direct, sentence-case, present-tense. Actions are verbs. No exclamation marks. Keyboard shortcuts are always visible on primary actions.

### Action labels

| Generic | This archetype |
|---------|----------------|
| Create New Issue | Create new issue |
| Submit Form | Save changes |
| Go to Dashboard | Overview |
| View All Items | View all |
| Mark as Complete | Mark done |

Always sentence-case. Never title case for action labels.

### Empty states

| Context | Heading | Body | Primary CTA |
|---------|---------|------|-------------|
| No active issues | Active issues | Issues in progress will appear here. | Create new issue C |
| No projects | Projects | Create a project to organise your work. | New project P |
| No team members | Members | Invite your team to start collaborating. | Invite people |
| No recent activity | Activity | Actions taken in this workspace show up here. | — |

### Status labels

| Status | Label | Icon | Colour |
|--------|-------|------|--------|
| Backlog | Backlog | circle outline | `$textMuted` |
| Todo | Todo | circle | `$textSecondary` |
| In progress | In progress | half-filled circle | `$warning` |
| In review | In review | eye | `$accent` |
| Done | Done | circle-check | `$positive` |
| Cancelled | Cancelled | x-circle | `$textMuted` opacity 0.5 |
| Duplicate | Duplicate | copy | `$textMuted` opacity 0.5 |

All status labels: sentence-case, present-tense, no past-tense ("Completed" → "Done").

---

## Verification checklist

Run this after every build. Each WHY matters for cases the checklist doesn't explicitly cover.

### Structure

- [ ] **Layout: sidebar (232px) left, main content right, horizontal flex.**
  WHY: Same spatial contract as analytics-dashboard. Users who switch between these archetypes share the same mental model.

- [ ] **Main content background is `$surface` (white or near-white), not `$surfaceMuted`.**
  WHY: The contrast between sidebar ($surfaceMuted) and content ($surface) is the primary visual separation. Without it, the two panels merge and the layout becomes ambiguous.

### Sidebar

- [ ] **Active item has a `$surfaceActive` fill, not an accent border or accent tint.**
  WHY: In this archetype, the accent is reserved for actions. A filled neutral background marks position without assigning brand colour to navigation. Mixing in accent colour here makes the sidebar compete with the primary CTAs.

- [ ] **Section headers are sentence-case lowercase with a chevron icon.**
  WHY: "Workspace" reads as structural metadata, not content. All-caps section headers import the analytics-dashboard or enterprise-corporate register into a product that is deliberately informal and engineering-led. Linear's designers were explicit about this choice.

- [ ] **No drop shadow on the sidebar edge.**
  WHY: Same as analytics-dashboard. The 1px border handles separation. No shadow.

- [ ] **Count badges are plain monospace text, no background pill.**
  WHY: A notification badge with a coloured pill fill says "alert, act on this." A plain number says "here is a count, FYI." In a pro tool, the user decides the priority; the UI shouldn't overdramatise counts.

### Issue rows

- [ ] **Row height 32px.**
  WHY: Density is the product's value. A list view that fits 24 issues in the viewport is more useful than one that fits 12. 32px is the minimum for legibility; 44px is appropriate for touch-first mobile apps, not desktop pro tools.

- [ ] **Issue ID column fixed width (48px), monospace.**
  WHY: A variable-width ID column causes titles to shift left/right depending on the ID length. Fixed-width mono keeps the title column stable and scannable.

- [ ] **Status as an icon (not text-only, not a large coloured pill).**
  WHY: At 32px row height, a text badge ("In Progress") takes up 80–100px of a 1140px content column. An icon takes 14px. Status icons don't need a label at list scale once users learn the vocabulary, which happens in the first 30 minutes of use.

### General

- [ ] **Font is `Inter Display`, not `Geist`, `Satoshi`, or system fonts.**
  WHY: This archetype overrides the default font recommendation. The exemplar (Linear) uses Inter Display deliberately and it is part of the archetype's visual identity. Switching to Geist makes the design read as a different archetype.

- [ ] **Primary CTAs always show keyboard shortcut chips.**
  WHY: A pro tool that hides its shortcuts is not a pro tool. The shortcut chip is both functional (users can glance and learn) and a visual signal that the product respects the user's workflow.

- [ ] **AI assistant pill present in the bottom-right.**
  WHY: By 2026, the floating AI entry point is an expected surface in pro tools. Its absence makes the design read as pre-2024. Its placement is always bottom-right: users' muscle memory for this pattern is already established.

---

## Contrast examples

### Example 1: Sidebar active item (correct vs generic)

**Correct:**

```
activeItem=I(nav, {
  type: "frame", name: "NavItem_Inbox",
  layout: "horizontal", alignItems: "center",
  width: "fill_container", height: 28,
  gap: 6, padding: [0, 8], cornerRadius: 6,
  fill: "$surfaceActive"   // neutral grey background
})
activeIcon=I(activeItem, {
  type: "icon_font", fill: "$accent"   // accent on icon only
})
activeLabel=I(activeItem, {
  type: "text", fill: "$textPrimary", fontWeight: 500
})
```

Why this is right: neutral grey background marks position. Accent appears on the icon only, not the background. The sidebar feels like it belongs to the surface, not competing with it.

**Generic:**

```
activeItem=I(nav, {
  type: "frame",
  ...,
  fill: [{ type: "color", color: "$accent", opacity: 0.12 }]  // WRONG: accent tint
})
activeLabel=I(activeItem, {
  type: "text", fill: "$accent", fontWeight: 600  // WRONG: accent on label too
})
```

Why this is wrong: accent tint on the background plus accent on the label concentrates three accent signals in one 28px row (background, icon, text). The sidebar becomes visually louder than the main content. Every active item shouts; users can no longer locate themselves quietly.

---

### Example 2: Empty state (correct vs generic)

**Correct:**

```
iconCluster=I(emptyState, {
  type: "frame", name: "IconCluster",
  layout: "none", width: 48, height: 48
})
I(iconCluster, { type: "icon_font", iconFontFamily: "lucide", iconFontName: "circle",
  width: 16, height: 16, fill: "$accent", x: 0, y: 0 })
I(iconCluster, { type: "icon_font", iconFontFamily: "lucide", iconFontName: "triangle",
  width: 16, height: 16, fill: "$warning", x: 20, y: 0, opacity: 0.7 })
I(iconCluster, { type: "icon_font", iconFontFamily: "lucide", iconFontName: "square",
  width: 16, height: 16, fill: "$textMuted", x: 0, y: 20, opacity: 0.5 })
I(iconCluster, { type: "icon_font", iconFontFamily: "lucide", iconFontName: "zap",
  width: 16, height: 16, fill: "$positive", x: 20, y: 20, opacity: 0.6 })
heading=I(emptyState, {
  type: "text", content: "Active issues",
  fontFamily: "$fontUI", fontSize: "$textBase",
  fontWeight: 600, fill: "$textPrimary", textAlign: "center"
})
```

Why this is right: 4 small abstract icons in a deliberate 2x2 cluster. Varied colours and opacities create visual interest without an illustration. Heading names what's missing, not a mood.

**Generic:**

```
// A G("heroBg", "ai", "person holding empty box") — WRONG: generated illustration
// or:
emptyIcon=I(emptyState, {
  type: "icon_font", iconFontName: "inbox",
  width: 48, height: 48, fill: "$textMuted"
  // Single large icon — correct for analytics-dashboard, not modern-pro-tool
})
heading=I(emptyState, {
  type: "text", content: "It's quiet here!",  // WRONG: mood, not fact
  ...
})
```

Why this is wrong: a single large icon is the analytics-dashboard empty state pattern. This archetype uses a 2x2 cluster of small abstract icons. The two archetypes have distinct empty state signatures; mixing them makes the design read as archetype-confused. "It's quiet here!" is filler microcopy; it communicates a mood instead of an instruction.
