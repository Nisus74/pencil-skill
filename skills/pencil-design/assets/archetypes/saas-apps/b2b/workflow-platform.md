# workflow-platform

Project and task management surfaces where work moves through stages and the status of everything is the primary visual information. Status colour is structural, not decorative.

**Surface category:** saas-apps/b2b
**Exemplars:** Asana (project boards), Linear Projects view, Jira board view, Monday.com
**Confidence:** high; Linear and Asana confirmed against devtools and direct use (May 2026)

Read this alongside `references/batch-design-grammar.md`. The critical differentiator from `analytics-dashboard`: analytics shows what happened; workflow shows what is happening and what is assigned. Status badges and swimlane columns are the primary components.

---

## When to use this archetype

Pick this when the primary UI shows tasks or work items moving through stages (Backlog → In Progress → Done, or similar). Pick it when assignment, due dates, and status are more prominent than metrics and charts. Skip it when the data is read-only analytical; use `analytics-dashboard` instead. Skip it when individual items are the primary focus; use `modern-pro-tool` instead.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#FFFFFF` | Page background. Workflow platforms trend whiter than analytics. |
| `$bgSidebar` | `#F7F7F8` | Sidebar background. |
| `$surface` | `#F5F5F7` | Card surface on kanban boards. Hover and drag state: `#EDEDF0`. |
| `$textPrimary` | `#1A1A1C` | Task names, column headers. |
| `$textSecondary` | `#6B6B70` | Assignee name, date label, meta text. |
| `$textMuted` | `#A0A0A8` | Empty state labels, placeholder. |
| `$border` | `#E5E5EA` | Card borders, column dividers, row separators. |
| `$accent` | Saturation 50–60%. | Primary CTA, selection state, focus ring. |
| `$statusTodo` | `#8E8E98` | Not started / to-do status. Neutral muted. |
| `$statusInProgress` | `#F59E0B` | In progress. Amber: universal "working on it" signal. |
| `$statusDone` | `#22C55E` | Done / closed. Green: universal "complete" signal. |
| `$statusBlocked` | `#EF4444` | Blocked / needs attention. Red: universal "problem" signal. |
| `$statusReview` | `#8B5CF6` | In review / waiting. Purple: intermediate state between progress and done. |
| `$fontBody` | `Inter` or `system-ui` | All UI text. |
| `$fontMono` | `Geist Mono` | Issue IDs, ticket numbers (LIN-1234, PROJ-0042). |

### Status colour system

The five status colours above form a complete set. Every status in the system maps to one of them. Using more than 5 distinct status colours produces a legend nobody reads.

| Colour | Signal | Status examples |
|--------|--------|-----------------|
| `$statusTodo` | Not started | Backlog, To-do, Unstarted |
| `$statusInProgress` | Active work | In Progress, Doing, Started |
| `$statusDone` | Finished | Done, Closed, Shipped |
| `$statusBlocked` | Problem | Blocked, Needs input, Rejected |
| `$statusReview` | Intermediate | In Review, Waiting, Pending approval |

---

## Page shell

```
AppShell (frame, fill_container x fill_container, layout: horizontal,
           fill: "$bg")
├── Sidebar (frame, 240 x fill_container, layout: vertical,
│             fill: "$bgSidebar",
│             stroke: { right: { color: "$border", thickness: 1 } })
│   // 240px. Project nav, workspace nav, workspace switcher.
└── MainContent (frame, fill_container x fill_container, layout: vertical,
                  fill: "$bg")
    ├── ProjectHeader (frame, fill_container x 52, layout: horizontal)
    │   // Project name, view switcher (Board / List / Timeline), + New task
    └── ViewArea (frame, fill_container x fill_container)
        // Either BoardView or ListView depending on active tab
```

---

## Sidebar

```
Sidebar (frame, 240 x fill_container, layout: vertical, gap: 0,
          padding: [8, 8], fill: "$bgSidebar")
├── WorkspaceSwitcher (frame, fill_container x 40, layout: horizontal,
│                       alignItems: center, gap: 8, padding: [0, 8],
│                       cornerRadius: 6)
│   ├── WorkspaceIcon (28 x 28, cornerRadius: 6, fill: "$accent")
│   ├── WorkspaceName (text, 14px, fontWeight: 600, $textPrimary)
│   └── ChevronIcon (16×16, $textSecondary)
├── SectionLabel (text, 11px, fontWeight: 600, $textMuted,
│                 content: "PROJECTS",
│                 padding: [12, 8, 4, 8], letterSpacing: "0.08em")
└── ProjectList (frame, fill_container x fit_content, layout: vertical, gap: 2)
    └── ProjectRow × N
        // Row: 32px height, cornerRadius: 5, padding: [0, 8]
        // Active: fill: "$surface"
        // Hover: fill: "$surface"
        // Resting: fill: transparent
        ├── ProjectColourDot (6 x 6, cornerRadius: 3, fill: project colour)
        │   // Each project has a distinct colour dot, NOT the status system colour
        └── ProjectName (text, 14px, $textPrimary, single-line truncated)
```

### Active state

```
// Active project row: filled background. No left border.
// The project nav uses filled rows like a file selector, not a navigation menu.
// See analytics-dashboard for left-border active state (that's a nav menu).
ProjectRow=U(row, { fill: "$surface", cornerRadius: 5 })
```

---

## Board view

The board view is the canonical workflow-platform layout: columns for each status, cards for each task.

```
BoardView (frame, fill_container x fill_container, layout: horizontal,
            gap: 12, padding: [16, 16], overflow: "horizontal_scroll",
            alignItems: flex_start)
└── BoardColumn × N (one per status)

BoardColumn (frame, 280 x fit_content, layout: vertical,
              gap: 8, padding: [8, 8, 8, 8],
              cornerRadius: 8,
              fill: "$surface")
├── ColumnHeader (frame, fill_container x 32, layout: horizontal,
│                  alignItems: center, gap: 8)
│   ├── StatusDot (8 x 8, cornerRadius: 4, fill: status colour)
│   ├── ColumnTitle (text, 13px, fontWeight: 600, $textPrimary,
│   │                content: "In Progress")
│   ├── TaskCount (text, 13px, $textSecondary, content: "5")
│   └── AddTaskButton (frame, 20 x 20, cornerRadius: 4, fill: transparent)
│       └── PlusIcon (12×12, $textMuted)
└── CardStack (frame, fill_container x fit_content, layout: vertical, gap: 6)
    └── TaskCard × N
```

### Task card (board)

```
TaskCard (frame, fill_container x fit_content, layout: vertical,
           gap: 8, padding: [10, 12],
           cornerRadius: 6,
           fill: "$bg",
           stroke: { color: "$border", thickness: 1 })
│   // fill: "$bg" (white), not $surface — cards sit on the column's $surface.
│   // stroke: 1px $border. No shadow.
├── TaskTitle (text, 14px, $textPrimary, $fontBody,
│              lineHeight: 1.4, width: "fill_container")
├── TaskMeta (frame, fill_container x fit_content, layout: horizontal,
│              alignItems: center, justifyContent: space_between)
│   ├── StatusBadge (frame, fit_content x 20, layout: horizontal,
│   │                alignItems: center, gap: 4, padding: [0, 6],
│   │                cornerRadius: 10,
│   │                fill: status_colour at 15% opacity)
│   │   ├── StatusDot (5 x 5, cornerRadius: 3, fill: status_colour)
│   │   └── StatusLabel (text, 11px, fontWeight: 500,
│   │                     fill: status_colour, content: "In Progress")
│   └── AssigneeChip (frame, fit_content x 20, layout: horizontal,
│                      alignItems: center, gap: 4)
│       ├── Avatar (frame, 18 x 18, cornerRadius: 9,
│       │           fill: generated from name hash)
│       │   └── Monogram (text, 9px, fontWeight: 600, fill: white,
│       │                  content: "JD")
│       └── AssigneeName (text, 12px, $textSecondary, content: "Jane D.")
└── DueDate (text, 12px, $textMuted, content: "May 15")
    // Overdue: fill: "$statusBlocked" (red)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Column width | 280px | Standard. 240px is cramped for task titles; 320px pushes fewer columns on screen. |
| Task card title | 14px, 1.4 line-height | Allows up to ~3 lines before the card becomes too tall. |
| Status badge height | 20px | Inline with meta row. Not a full-height tag. |
| Status badge fill | Status colour at 15% opacity, full opacity on dot+label | The tinted background gives colour mass; full opacity on text/dot gives legibility. |
| Avatar size | 18px | Small enough to fit in a meta row. Monogram at 9px fontWeight 600. |

### What generic looks like

```
// WRONG: task card with shadow
TaskCard=I(column, {
  type: "frame",
  effect: [{ type: "drop_shadow", blur: 8, y: 2, opacity: 0.1 }],
  ...
})
// Shadows on every card multiply into visual noise. 32 cards in a project
// with 32 shadows looks like a waterfall. 1px border only.

// WRONG: status badge as a pill with solid fill
StatusBadge=I(card, {
  type: "frame",
  fill: "$statusInProgress",   // WRONG: full opacity amber fill
  cornerRadius: 10,
  ...
})
// A fully-filled status badge at amber competes with the amber used for
// "In Progress" highlighting. Tinted fill (15% opacity) gives colour signal
// without colour weight. The full-opacity dot and label are sufficient for legibility.
```

---

## List view

The list view shows tasks as rows, grouped by status or project.

```
ListView (frame, fill_container x fit_content, layout: vertical,
           gap: 0, padding: [0, 16])

ListGroup (frame, fill_container x fit_content, layout: vertical, gap: 0)
├── GroupHeader (frame, fill_container x 36, layout: horizontal,
│                alignItems: center, gap: 8, padding: [0, 0],
│                stroke: { bottom: { color: "$border", thickness: 1 } })
│   ├── StatusDot (8 x 8, cornerRadius: 4, fill: status colour)
│   ├── GroupTitle (text, 13px, fontWeight: 600, $textPrimary,
│   │               content: "In Progress")
│   └── TaskCount (text, 13px, $textSecondary, content: "5 tasks")
└── TaskRow × N

TaskRow (frame, fill_container x 40, layout: horizontal,
          alignItems: center, gap: 12, padding: [0, 0],
          stroke: { bottom: { color: "$border", thickness: 1 } })
│   // 40px height. Denser than kanban cards (intentionally).
├── CheckBox (frame, 16 x 16, cornerRadius: 4,
│             stroke: { color: "$border", thickness: 1.5 })
│   // Done state: fill: "$statusDone", checkmark icon white 10px
├── TaskName (text, 14px, $textPrimary, width: fill_container)
├── AssigneeAvatar (frame, 24 x 24, cornerRadius: 12)
│   └── Monogram (text, 11px, fontWeight: 600, fill: white)
├── DueDateChip (frame, fit_content x 22, layout: horizontal,
│                alignItems: center, gap: 4, padding: [0, 6],
│                cornerRadius: 11)
│   // Upcoming: fill: transparent, text: $textSecondary
│   // Due today: fill: "$statusInProgress" at 15% opacity
│   // Overdue: fill: "$statusBlocked" at 15% opacity, text: $statusBlocked
│   └── DateLabel (text, 12px, $textSecondary, content: "May 15")
└── PriorityIcon (frame, 16 x 16)
    // Urgent: up-arrow, $statusBlocked
    // Medium: horizontal bar, $statusInProgress
    // Low: down-arrow, $statusTodo
```

---

## Status badge (standalone)

Used across both board and list views, in headers, and in filters.

```
StatusBadge (frame, fit_content x 22, layout: horizontal,
              alignItems: center, gap: 5, padding: [0, 8],
              cornerRadius: 11)
├── StatusDot (6 x 6, cornerRadius: 3, fill: status_colour)
└── StatusLabel (text, 12px, fontWeight: 500, fill: status_colour)
```

Background: `status_colour` at 12–15% opacity. This formula works for all five status colours: the tinted field stays soft, the dot and label stay readable.

```
// Correct implementation across all five states:
// Todo:
{ fill: "$statusTodo at 12%", dot: "$statusTodo", label: "$statusTodo" }
// In Progress:
{ fill: "$statusInProgress at 12%", dot: "$statusInProgress", label: "$statusInProgress" }
// Done:
{ fill: "$statusDone at 12%", dot: "$statusDone", label: "$statusDone" }
// Blocked:
{ fill: "$statusBlocked at 12%", dot: "$statusBlocked", label: "$statusBlocked" }
// In Review:
{ fill: "$statusReview at 12%", dot: "$statusReview", label: "$statusReview" }
```

---

## Microcopy library

### Board column labels

Follow the project's natural stage vocabulary. Do not invent stages that don't map to the workflow.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Status 1 / Status 2 | Backlog / In Progress / Done |
| Not Done | To Do |
| Completed | Done |
| Attention Required | Blocked |

### Empty column state

| Generic (avoid) | This archetype |
|-----------------|----------------|
| No items | No tasks in Backlog |
| Empty | Nothing blocked yet |
| Add tasks here | Drop tasks here or + Add task |

### Task creation CTA

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Create item | + New task |
| Add | + Add task |
| New | + Task |

### Due date labels

| State | Label | Colour |
|-------|-------|--------|
| Future | "May 15" | `$textMuted` |
| Due today | "Today" | `$statusInProgress` (amber) |
| Overdue by 1 day | "Yesterday" | `$statusBlocked` (red) |
| Overdue by N days | "3 days ago" | `$statusBlocked` (red) |

---

## Verification checklist

### Status system

- [ ] **All statuses map to one of the five status colours.**
  WHY: A 6th or 7th status colour requires a legend. The five-colour system is pre-understood: grey = not started, amber = active, green = done, red = problem, purple = intermediate. Adding custom colours breaks the instant-read pattern that makes workflow platforms fast to scan.

- [ ] **Status badge fill is the status colour at 12–15% opacity.**
  WHY: Full-opacity status fills on every card produce a colour-saturated grid that is visually exhausting. A tinted background at 12–15% opacity gives colour signal with low visual weight. The full-opacity dot and label are sufficient for legibility at this scale.

### Task cards (board view)

- [ ] **Task cards have 1px `$border` stroke, no shadow.**
  WHY: A shadow on every task card in a 4-column board multiplies into ~100 shadows on a full project. The visual weight is significant. 1px border cards read as a grid; shadow cards read as a waterfall of floating elements.

- [ ] **Column background is `$surface`, card background is `$bg`.**
  WHY: Column as `$surface`, card as `$bg` (white) creates a two-level depth signal without shadows. The card reads as "on top of" the column. Reversing this (white column, surface card) makes cards disappear into the column.

### List view

- [ ] **List rows are 40px, not 32px or 48px.**
  WHY: 32px is pro-tool density (Linear issues list). Workflow platforms have more meta per row (assignee, due date, priority, status). 40px gives breathing room for the 4-column meta layout. 48px introduces scroll-inducing padding on long task lists.

- [ ] **Overdue dates are `$statusBlocked` (red), not amber or default text.**
  WHY: Due dates are informational until they're overdue. The colour change from muted to red is the "you need to act" signal. Amber ("due today") is a softer warning. Red ("overdue") is the interruption that demands attention. Consistent with the status system's red = problem convention.

### Typography

- [ ] **Issue IDs and ticket numbers use `$fontMono`.**
  WHY: "LIN-1234" and "PROJ-0042" are identifiers, not prose. Monospace keeps them visually distinct from task names. In a list with 30 tasks, a monospace ID column lets the eye separate the identifier from the title without reading both.

---

## Contrast examples

### Example 1: Status badge (correct vs generic)

**Correct:**

```
statusBadge=I(taskCard, {
  type: "frame", name: "StatusBadge",
  layout: "horizontal", alignItems: "center",
  gap: 5, padding: [0, 8], height: 22,
  cornerRadius: 11,
  fill: "$statusInProgress at 12% opacity"
})
statusDot=I(statusBadge, {
  type: "frame", width: 6, height: 6, cornerRadius: 3,
  fill: "$statusInProgress"
})
statusLabel=I(statusBadge, {
  type: "text", content: "In Progress",
  fontSize: 12, fontWeight: 500,
  fill: "$statusInProgress"
})
```

Why this is right: tinted fill gives colour mass without dominance. Full-opacity dot and label are legible at 12px. The result reads as "this is an In Progress item" at a glance without the amber shouting across the board.

**Generic:**

```
statusBadge=I(taskCard, {
  type: "frame",
  fill: "$statusInProgress",   // WRONG: full-opacity amber
  cornerRadius: 10, padding: [0, 8], height: 22
})
statusLabel=I(statusBadge, {
  type: "text", content: "In Progress",
  fontSize: 12, fill: "#FFFFFF"   // WRONG: white text on amber
})
```

Why this is wrong: full-opacity amber on every In Progress card turns the board into a wall of amber blocks. White text on amber fails WCAG AA contrast at 12px. On a board with 20 tasks in progress, this produces 20 solid amber rectangles competing for attention with the actual task names.

---

### Example 2: Task card (correct vs generic)

**Correct:**

```
taskCard=I(column, {
  type: "frame", name: "TaskCard",
  layout: "vertical", gap: 8,
  padding: [10, 12],
  cornerRadius: 6,
  fill: "$bg",
  stroke: { color: "$border", thickness: 1 }
  // No shadow. No effect property.
})
taskTitle=I(taskCard, {
  type: "text",
  content: "Redesign the onboarding flow",
  fontSize: 14, fill: "$textPrimary",
  lineHeight: 1.4, width: "fill_container"
})
```

Why this is right: white card (`$bg`) on grey column (`$surface`) creates depth without shadows. 1px border is enough separation. 10/12px padding gives the title room to breathe across up to 3 lines.

**Generic:**

```
taskCard=I(column, {
  type: "frame",
  fill: "$surface",   // WRONG: same fill as column — card blends into column
  cornerRadius: 8,
  padding: [12, 12],
  effect: [{ type: "drop_shadow", blur: 6, y: 2, opacity: 0.08 }]
  // WRONG: shadow on every card
})
```

Why this is wrong: `$surface` card on `$surface` column produces no depth. The card boundaries disappear; the column reads as a list without visual separation between items. The shadow attempts to compensate, but at 0.08 opacity it's barely visible while still multiplying across 20 cards.
