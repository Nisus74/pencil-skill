# enterprise-corporate

Formal, high-density SaaS surfaces for enterprise buyers where trust, legibility at scale, and compliance-adjacent visual language take priority over elegance or brand personality. Information density is high; visual decoration is low.

**Surface category:** saas-apps/b2b
**Exemplars:** Salesforce Lightning, SAP Fiori, ServiceNow, Workday
**Confidence:** medium-high; SAP Fiori confirmed from public design system docs; Salesforce Lightning from direct use (May 2026)

Read this alongside `references/batch-design-grammar.md`. The critical differentiator from `modern-pro-tool` and `analytics-dashboard`: the user base is large (hundreds or thousands of users per deployment), the data is operational (records, cases, accounts), and the visual language must be institutional rather than crafted.

---

## When to use this archetype

Pick this for HR software, ERP interfaces, CRM back-office views, compliance dashboards, and any B2B product sold primarily to enterprise IT buyers rather than end-users. Skip it when the user base is a small team of power users; use `modern-pro-tool` instead. Skip it when the primary experience is data visualisation; use `analytics-dashboard` instead.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#F3F4F6` | Page background. Deliberately grey, not white. Grey signals "system," not "brand." |
| `$surface` | `#FFFFFF` | Card, table, and panel surface. White content on grey background. |
| `$surfaceHeader` | `#F9FAFB` | Table header row background. One step darker than surface. |
| `$textPrimary` | `#111827` | Record field values, primary data. |
| `$textSecondary` | `#6B7280` | Field labels, column headers. |
| `$textMuted` | `#9CA3AF` | Placeholder, empty state. |
| `$border` | `#E5E7EB` | Table dividers, card borders, input borders. |
| `$borderStrong` | `#D1D5DB` | Section dividers, tab underlines. |
| `$accent` | Saturation 50–60%. Typically blue: `#2563EB`. | Primary CTA, active navigation, selected row. |
| `$accentSubtle` | `$accent` at 8% opacity. | Selected row background, active nav item background. |
| `$statusSuccess` | `#16A34A` | Active, approved, successful record state. |
| `$statusWarning` | `#D97706` | Pending, requires action, under review. |
| `$statusError` | `#DC2626` | Error, rejected, failed. |
| `$statusNeutral` | `#6B7280` | Inactive, closed, archived. |
| `$fontBody` | `Inter` or system-ui. In SAP contexts: `72` (SAP's typeface). | All UI text. |
| `$fontMono` | `Geist Mono` | Record IDs, case numbers, account codes. |

---

## Page shell

```
AppShell (frame, fill_container x fill_container, layout: vertical,
           fill: "$bg")
├── TopNav (frame, fill_container x 48, layout: horizontal,
│            fill: "$accent",
│            alignItems: center, padding: [0, 16])
│   // Enterprise platforms typically use an accent-filled top nav.
│   // This is the exception to the "chrome recedes" rule in other archetypes.
│   // The filled nav is an institutional marker: it signals "you are inside
│   // a system" rather than "you are using a product."
├── SecondaryNav (frame, fill_container x 44, layout: horizontal,
│                  fill: "$surface",
│                  stroke: { bottom: { color: "$border", thickness: 1 } })
│   // Optional: breadcrumbs, module switcher, page tabs.
└── PageContent (frame, fill_container x fill_container, layout: horizontal,
                  fill: "$bg", gap: 16, padding: [16, 16])
    ├── LeftPanel (frame, 280 x fit_content, ...)  // optional sidebar/filter
    └── MainPanel (frame, fill_container x fill_container, ...)
```

### Top nav exception: accent fill

```
// Correct: accent-filled top nav in enterprise-corporate archetype
TopNav=I(shell, {
  fill: "$accent",   // $accent fills the full-width top bar
})
// White text and icons on accent background.

// This IS correct for this archetype. It is wrong for analytics-dashboard
// and modern-pro-tool. Enterprise navigation is an institutional fixture,
// not a content surface. The accent fill signals "header" unambiguously
// without requiring users to infer hierarchy.
```

---

## Record table

The record table is the primary component in enterprise software. Every screen is essentially a list of records with columns.

```
RecordTable (frame, fill_container x fit_content, layout: vertical,
              fill: "$surface",
              stroke: { color: "$border", thickness: 1 },
              cornerRadius: 6)
├── TableHeader (frame, fill_container x 40, layout: horizontal,
│                fill: "$surfaceHeader",
│                stroke: { bottom: { color: "$borderStrong", thickness: 1 } })
│   └── HeaderCell × N
│       // 12px, fontWeight: 600, $textSecondary, ALLCAPS, letterSpacing: 0.06em
│       // padding: [0, 12]
│       // Sortable: chevron icon 12×12 $textMuted after label
└── TableBody (frame, fill_container x fit_content, layout: vertical)
    └── RecordRow × N

RecordRow (frame, fill_container x 48, layout: horizontal,
            alignItems: center,
            stroke: { bottom: { color: "$border", thickness: 1 } })
│   // 48px row height. Not 32px (too tight for enterprise data volume) or
│   // 56px (wastes vertical space — the user might have 200+ records).
│   // Hover: fill: "$accentSubtle"
│   // Selected: fill: "$accentSubtle" + left border 3px $accent
└── DataCell × N
    // padding: [0, 12]
    // Primary data: 14px, $textPrimary
    // Secondary/label: 13px, $textSecondary
```

### Status pill (in table rows)

```
StatusPill (frame, fit_content x 22, layout: horizontal,
             alignItems: center, gap: 4, padding: [0, 8],
             cornerRadius: 4)  // cornerRadius: 4, NOT 11 — enterprise rounds less
├── StatusDot (6 x 6, cornerRadius: 3, fill: status_colour)
└── StatusLabel (text, 12px, fontWeight: 500, fill: status_colour)
// Background: status_colour at 10% opacity
// Note: cornerRadius 4 vs workflow-platform's 11 is intentional.
// Square-ish badges read as institutional; pill-shaped badges read as consumer.
```

### Record ID cell

```
RecordID (text, 13px, $fontMono, $textSecondary,
           content: "CASE-10042" or "ACC-2891")
// Monospace for all record identifiers. Keeps ID columns scannable.
// IDs are always $textSecondary (not primary) — they're references, not content.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Row height | 48px | 40px for dense read-only tables; 48px when rows have actions. |
| Header all-caps | required | `text-transform: uppercase`, `letterSpacing: 0.06em`. Signals "this is a header column", not another data row. |
| Selected row | `$accentSubtle` fill + 3px left border `$accent` | The left border is the primary selection indicator. The fill is secondary reinforcement. |
| Corner radius on table | 6px | Not 0 (too industrial), not 12px (too consumer). 6–8px is the enterprise register. |
| Corner radius on status pill | 4px | Square-ish, not pill-shaped. Consumer patterns use 10–12px radius; enterprise uses 4px. |

### What generic looks like

```
// WRONG: table rows at 32px
RecordRow=I(table, {
  height: 32,
  ...
})
// 32px is a pro-tool row height for expert-user-dense interfaces.
// Enterprise tables often have 5–8 data columns per row. At 32px,
// the text and meta are cramped. 48px gives each row enough breathing room
// to scan quickly across columns without confusion.

// WRONG: header cells in title case, same fill as data cells
HeaderCell=I(header, {
  type: "text",
  fontSize: 14, fill: "$textPrimary",
  fontWeight: 600,
  content: "Account Name"  // WRONG: Title Case
  // fill: "$surface" WRONG: same fill as data rows
})
// Uppercase headers with letter-spacing are the primary signal that
// "this is a category label, not data." Without this, the header row
// reads as the first data row.
```

---

## Form / record detail

Enterprise products spend as much time in record detail views as in list views. The detail view is a structured form.

```
RecordDetail (frame, fill_container x fit_content, layout: vertical,
               gap: 0, fill: "$surface",
               stroke: { color: "$border", thickness: 1 },
               cornerRadius: 6)
├── RecordHeader (frame, fill_container x 56, layout: horizontal,
│                  alignItems: center, justifyContent: space_between,
│                  padding: [0, 16],
│                  stroke: { bottom: { color: "$border", thickness: 1 } })
│   ├── RecordTitle (text, 16px, fontWeight: 600, $textPrimary)
│   └── ActionBar (frame, fit_content, layout: horizontal, gap: 8)
│       // Edit, Save, Cancel, Delete — standard record actions
└── FieldGrid (frame, fill_container x fit_content, layout: grid,
                columns: 2, gap: [16, 20], padding: [16, 16])
    └── FieldPair × N

FieldPair (frame, fill_container x fit_content, layout: vertical, gap: 4)
├── FieldLabel (text, 12px, fontWeight: 500, $textSecondary,
│               letterSpacing: "0.02em",
│               content: "Account Name")
└── FieldValue (text, 14px, $textPrimary, content: "Acme Corp")
    // Edit mode: replace with input frame, 1px $border, cornerRadius: 4, height: 36
```

### What generic looks like

```
// WRONG: full-page form layout (one column, labels above inputs, no grid)
RecordDetail=I(page, {
  layout: "vertical",
  width: 600  // centered, full-width labels and inputs
})
// A single-column form on a 1280px screen wastes 600px on each side.
// Enterprise records have 20–40 fields. A 2-column grid renders them
// in half the vertical space without requiring scrolling past 20 labels.
```

---

## Navigation: left sidebar

The enterprise sidebar is a persistent navigation hierarchy with section labels, item counts, and optional nested navigation.

```
EnterpriseSidebar (frame, 240 x fill_container, layout: vertical,
                    gap: 0, fill: "$surface",
                    stroke: { right: { color: "$border", thickness: 1 } })
├── NavSection × N
│   ├── SectionLabel (text, 11px, fontWeight: 600, $textMuted,
│   │                  letterSpacing: "0.08em",
│   │                  content: "ACCOUNTS",
│   │                  padding: [12, 12, 4, 16])
│   └── NavItem × N

NavItem (frame, fill_container x 36, layout: horizontal,
          alignItems: center, gap: 10, padding: [0, 16],
          cornerRadius: 0)  // flat row, no corner radius
│   // cornerRadius: 0 is correct for enterprise sidebar items.
│   // Rounded nav items read as modern-consumer. Flat rows read as institutional.
│   // Active: background: "$accentSubtle", left border: 3px $accent
│   // Hover: background: "$bg" (one step down from $surface)
├── NavIcon (16×16, $textSecondary when resting, $accent when active)
├── NavLabel (text, 14px, $textPrimary when active, $textSecondary when resting)
└── NavCount (frame, fit_content x 18, cornerRadius: 9,
               fill: "$border", padding: [0, 6])
    └── CountLabel (text, 11px, fontWeight: 600, $textSecondary)
    // Count badge for pending items, open cases, etc.
```

---

## Microcopy library

### CTA labels

Enterprise products use cautious, professional verb phrases. No clever copy.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Let's go | Submit |
| Get started | Create record |
| Add | New account |
| Delete | Remove |
| Save changes | Save |
| Oops, something went wrong | Error saving record. Try again. |

### Status labels

Match the customer's operational vocabulary. These are not UI states; they're business states.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Active | Open (for cases); Active (for accounts) |
| Done | Closed |
| Red / Yellow / Green | Approved / Pending / Rejected |
| On hold | Escalated |

### Empty state

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Nothing here yet! | No records found |
| Wow, such empty | No accounts match your filters |
| You're all caught up | 0 open cases |

No exclamation marks, no friendly humour. The user is doing their job.

---

## Verification checklist

### Institutional register

- [ ] **Page background is `$bg` (#F3F4F6), not white.**
  WHY: White page backgrounds read as consumer web products. Enterprise SaaS uses a grey page background to signal "system." The content surfaces (cards, tables, panels) are white. This two-level treatment is the canonical enterprise visual language.

- [ ] **Top nav is accent-filled.**
  WHY: In analytics-dashboard and modern-pro-tool, the top bar recedes. In enterprise-corporate, it doesn't. The filled header is an institutional marker that communicates "you are logged into a system." This is the one archetype where a filled nav header is correct.

- [ ] **Status pill corner radius is 4px, not 10–12px.**
  WHY: 10–12px corner radius on status badges reads as consumer SaaS. 4px is the institutional register. Small corner radii signal "this is a formal system." It sounds arbitrary, but in context it is immediately legible: Salesforce status pills look different from Linear status badges.

### Tables

- [ ] **Header cells are uppercase with 0.06em letter-spacing.**
  WHY: Column headers that look identical to data cells produce ambiguous tables. All-caps + letter-spacing is the universal "this is a header row, not a data row" signal in enterprise data tables.

- [ ] **Table row height is 44–48px, not 32px.**
  WHY: Enterprise records have 5–8 visible columns. At 32px, the row is too dense to scan across multiple columns without errors. 48px keeps the visual rhythm readable across long sessions.

- [ ] **Record IDs use `$fontMono`.**
  WHY: CASE-10042 and ACC-2891 are references, not prose. Monospace keeps ID columns distinct from content columns, allows faster scanning, and prevents confusion between similar-looking alphanumeric sequences.

### Form layout

- [ ] **Record detail uses a 2-column field grid.**
  WHY: A single-column form on a 1280px screen is 600px wide with 600px of dead space on each side. Enterprise records have 20–40 fields. A 2-column grid cuts scrolling in half and uses the available space professionally.

---

## Contrast examples

### Example 1: Table header (correct vs generic)

**Correct:**

```
tableHeader=I(table, {
  type: "frame", name: "TableHeader",
  height: 40, width: "fill_container",
  layout: "horizontal",
  fill: "$surfaceHeader",
  stroke: { bottom: { color: "$borderStrong", thickness: 1 } }
})
headerCell=I(tableHeader, {
  type: "text",
  content: "ACCOUNT NAME",        // uppercase
  fontSize: 12, fontWeight: 600,
  fill: "$textSecondary",
  letterSpacing: "0.06em",
  padding: [0, 12]
})
```

Why this is right: all-caps, `$surfaceHeader` background, `$borderStrong` divider below. The header is visually unambiguous from the first data row.

**Generic:**

```
tableHeader=I(table, {
  type: "frame",
  height: 40, fill: "$surface"   // WRONG: same fill as data rows
})
headerCell=I(tableHeader, {
  type: "text",
  content: "Account Name",   // WRONG: title case
  fontSize: 14, fontWeight: 600,   // WRONG: same size as data
  fill: "$textPrimary"   // WRONG: same fill as data
})
```

Why this is wrong: same fill, same font size, same colour. The header row is indistinguishable from the first data row. A user glancing at the table sees 10 rows, not 9 rows and a header. They have to read each row to find which one has the column labels.

---

### Example 2: Status pill (correct vs generic)

**Correct:**

```
statusPill=I(tableRow, {
  type: "frame", name: "StatusPill",
  layout: "horizontal", alignItems: "center",
  gap: 4, padding: [0, 8], height: 22,
  cornerRadius: 4,    // square-ish, institutional
  fill: "$statusWarning at 10% opacity"
})
statusDot=I(statusPill, {
  type: "frame", width: 6, height: 6, cornerRadius: 3,
  fill: "$statusWarning"
})
statusLabel=I(statusPill, {
  type: "text", content: "Pending",
  fontSize: 12, fontWeight: 500,
  fill: "$statusWarning"
})
```

Why this is right: cornerRadius 4 is institutional. Tinted background at 10% opacity keeps colour signal without dominance. Full-opacity dot and label are legible.

**Generic:**

```
statusPill=I(tableRow, {
  type: "frame",
  cornerRadius: 12,   // WRONG: pill-shaped, consumer register
  fill: "$statusWarning",   // WRONG: full-opacity amber fill
  padding: [0, 10], height: 24
})
statusLabel=I(statusPill, {
  type: "text", content: "Pending",
  fontSize: 12, fill: "#FFFFFF"   // WRONG: white on amber
})
```

Why this is wrong: pill-shaped with full amber fill and white text is the consumer design system badge pattern (GitHub, Linear, Notion). In enterprise software it reads as a design-forward consumer product impersonating an enterprise tool. The institutional register requires smaller corner radii and tinted backgrounds.
