# consumer-productivity

Light, personal task and focus apps where the user relationship is individual rather than organisational. Chrome recedes, content breathes, and the product has a defined personality that makes daily use feel pleasant rather than obligatory.

**Surface category:** saas-apps/b2c
**Exemplars:** Todoist, Things 3, Bear, Craft, Notion (personal tier)
**Confidence:** high; Todoist and Things 3 confirmed from direct use (May 2026)

Read this alongside `references/batch-design-grammar.md`. The critical differentiator from `workflow-platform`: workflow-platform is for teams tracking shared work; consumer-productivity is for individuals managing their own life. Density is lower, personality is higher, and the completion animation is not an afterthought.

---

## When to use this archetype

Pick this for personal task managers, note-taking apps, journaling tools, habit trackers, and focus timers where the primary user is an individual, not a team. Skip it for team collaboration tools; use `workflow-platform` instead. Skip it for professional SaaS; use `modern-pro-tool` instead.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#FFFFFF` | Page background. White is correct here; the product should feel like a personal document. |
| `$bgAlt` | `#F9F9FB` | Alternate section background, hover states. |
| `$surface` | `#F3F3F5` | Sidebar background, input fill. |
| `$textPrimary` | `#1A1A1C` | Task names, note titles. |
| `$textSecondary` | `#6B6B6E` | Due dates, list labels, metadata. |
| `$textMuted` | `#AEAEB2` | Placeholder, empty state copy. |
| `$border` | `#E8E8EC` | Subtle separators. Used sparingly. |
| `$accent` | Saturation 60–75%. Typically a distinct brand hue: Todoist red (`#DB4035`), Things blue (`#007AFF`). | Priority indicator, CTA, completion flash. |
| `$accentSubtle` | `$accent` at 10% opacity. | Selected item background. |
| `$priority1` | `#DB4035` | Urgent / priority 1. Red. |
| `$priority2` | `#FF8C00` | High / priority 2. Orange. |
| `$priority3` | `#4073FF` | Medium / priority 3. Blue. |
| `$priority4` | `$textMuted` | No priority. Muted. |
| `$fontDisplay` | `SF Pro Display` (Apple) or `Inter` | Headings, section labels. |
| `$fontBody` | `SF Pro Text` (Apple) or `Inter` | Task names, body copy. |
| `$fontMono` | `SF Mono` (Apple) or `Geist Mono` | Code blocks in notes; never for task names. |

---

## Page shell

```
AppShell (frame, fill_container x fill_container, layout: horizontal,
           fill: "$bg")
├── Sidebar (frame, 220 x fill_container, layout: vertical,
│             fill: "$surface")
│   // 220px. Personal app sidebars are narrower than B2B apps.
│   // Contains: project list, inbox, filters (Today, Upcoming, etc.)
│   // No visible border between sidebar and main: negative space is the separator.
└── MainPanel (frame, fill_container x fill_container, layout: vertical,
                fill: "$bg")
    ├── ViewHeader (frame, fill_container x 52, layout: horizontal)
    │   // Section title, optional filter, add task button
    └── TaskList (frame, fill_container x fill_content, overflow: "vertical_scroll")
```

### No separator between sidebar and main

```
// Correct: no border between sidebar and main content
Sidebar=I(shell, { fill: "$surface" })
// No stroke property on Sidebar.
// The background colour difference (surface vs bg) is the visual separator.
// A 1px $border between sidebar and main is a B2B signal.
// Consumer productivity apps prefer softer separation.
```

---

## Task item

```
TaskItem (frame, fill_container x 44, layout: horizontal,
           alignItems: center, gap: 10, padding: [0, 16],
           cornerRadius: 0)
│   // 44px height. One full touch target on mobile; comfortable click target on desktop.
│   // Hover: fill: "$bgAlt"
│   // No border between rows — rely on spacing and hover state only.
├── CheckCircle (frame, 18 x 18, cornerRadius: 9,
│                stroke: { color: "$border", thickness: 1.5 })
│   // Resting: hollow circle with $border stroke
│   // Hover: stroke colour transitions to $accent (transition signal)
│   // Done: fill: "$accent", white checkmark 10px inside
│   // Done animation: brief scale + colour flash, then task fades/removes
├── TaskName (text, 15px, $textPrimary, $fontBody,
│              lineHeight: 1.4, width: "fill_container")
│   // Done state: fill: "$textMuted", NO strikethrough
│   // Same font size as normal — shrinking "done" text is condescending
├── PriorityFlag (frame, 14 x 14)
│   // Visible only when priority is set.
│   // Priority 1: red flag icon, $priority1
│   // Priority 2: orange flag icon, $priority2
│   // Priority 3: blue flag icon, $priority3
│   // Priority 4 (none): hidden
└── DueDate (text, 12px, $textSecondary)
    // "Today", "Tomorrow", "May 15", "5 days overdue"
    // Overdue: fill: $priority1 (red)
```

### Completion state

```
// Done task — styled, not removed immediately
TaskItem (with completedState)
│   // fill: transparent (no hover state)
├── CheckCircle (fill: "$accent", ✓ white icon)
└── TaskName (fill: "$textMuted")
    // Light strikethrough is acceptable in Things 3 style; Todoist uses no strikethrough.
    // Pick one and stay consistent. If strikethrough: text-decoration-color: $textMuted,
    // NOT $textPrimary (the strike should be as light as the text).
```

### What generic looks like

```
// WRONG: task row height 32px
TaskItem=I(list, { height: 32 })
// 32px is B2B density. Consumer productivity apps are daily-use tools
// where individual tasks need enough space to be comfortably tapped and read.
// 44px is the Apple HIG minimum tap target and the correct register for this archetype.

// WRONG: heavy status badge on each task
StatusBadge=I(taskItem, {
  type: "frame",
  fill: "$priority1",  // WRONG: solid red badge for priority
  cornerRadius: 4, padding: [0, 6]
})
// Status badges belong to workflow-platform and enterprise-corporate.
// Consumer productivity apps use a small priority flag icon, not a badge.
// A badge says "category"; a flag says "I marked this".
```

---

## Sidebar nav

```
Sidebar (frame, 220 x fill_container, layout: vertical,
          padding: [16, 8, 8, 8], fill: "$surface", gap: 4)
├── SidebarSection × N
│   ├── SectionLabel (text, 11px, fontWeight: 600, $textMuted,
│   │                  letterSpacing: "0.08em",
│   │                  padding: [8, 8, 4, 8],
│   │                  content: "PROJECTS")
│   └── NavItem × N

NavItem (frame, fill_container x 32, layout: horizontal,
          alignItems: center, gap: 8, padding: [0, 8],
          cornerRadius: 6)
│   // Active: fill: "$accentSubtle"
│   // Hover: fill: "$bgAlt" (outside $surface area; hover is very light)
├── ProjectColour (frame, 8 x 8, cornerRadius: 4, fill: project colour)
│   // Each project gets a user-set colour. These are personal colour choices,
│   // not the status system colours from workflow-platform.
├── ProjectName (text, 14px, $textPrimary, single-line truncated)
└── TaskCount (text, 12px, $textMuted)
    // Number of pending tasks in this project. Optional.
```

### Special inbox / today items

```
// "Today" and "Inbox" get $accent-coloured icons, not project colour dots.
// These are system views, not user projects.
TodayItem (NavItem with)
├── TodayIcon (frame, 18 x 18, $accent)
└── TodayLabel (text, 14px, fontWeight: 500, $textPrimary, content: "Today")
```

---

## Empty state

Personal productivity empty states should feel encouraging, not administrative.

```
EmptyState (frame, fill_container x fill_content, layout: vertical,
             alignItems: center, justifyContent: center,
             gap: 12, padding: [48, 40])
├── EmptyIllustration (frame, 64 x 64, layout: none)
│   // Simple, friendly illustration or icon.
│   // Single colour ($accent or $textMuted). Not a stock icon.
├── EmptyHeadline (text, 18px, fontWeight: 600, $textPrimary,
│                   textAlign: "center",
│                   content: "All caught up")
│   // Past tense, positive framing. Not "Nothing here" or "No tasks."
└── EmptySubtext (text, 14px, $textSecondary, textAlign: "center",
                   lineHeight: 1.5,
                   content: "Add a task to get started, or enjoy the quiet moment.")
    // One sentence. Warm but not precious. Never sarcastic.
```

### What generic looks like

```
// WRONG: Empty state matching enterprise register
EmptyHeadline=I(emptyState, {
  type: "text", content: "No tasks found",  // WRONG: cold, admin language
  fontSize: 16, fill: "$textMuted"
})
EmptySubtext=I(emptyState, {
  type: "text", content: "Create a task to get started.",  // WRONG: imperative instruction
  fontSize: 13, fill: "$textMuted"
})
// "No tasks found" sounds like a database query result.
// Consumer apps have personality. The empty state is an opportunity to
// reinforce the brand voice, not to report the absence of data.
```

---

## Microcopy library

### Section/view names

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Inbox (with count badge) | Inbox |
| All Tasks | All |
| My Projects | Projects |
| Completed Items | Completed |
| Archived | Archive |

### Task input placeholder

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Enter task name | Task name |
| Add a new task | Add task |
| What would you like to do? | What do you need to do? |

### Empty state copy

| View | Headline | Subtext |
|------|---------|---------|
| Today (no tasks) | "Your day is clear" | "Add tasks to Today or assign due dates." |
| Inbox (empty) | "All caught up" | "Great work. New tasks land here." |
| Project (empty) | "Nothing here yet" | "Add the first task to get started." |

### Priority labels

| Level | Label | Icon colour |
|-------|-------|-------------|
| 1 | Priority 1 | `$priority1` (red) |
| 2 | Priority 2 | `$priority2` (orange) |
| 3 | Priority 3 | `$priority3` (blue) |
| 4 | No priority | (hidden / muted) |

---

## Verification checklist

### Lightness and whitespace

- [ ] **Task row height is 44px.**
  WHY: 44px is the Apple HIG minimum tap target. At this height, a task list with 20 items takes 880px: one scroll. At 32px it takes 640px. The difference is small; the ergonomic improvement is significant. Consumer apps are used every day for years; small ergonomic wins compound.

- [ ] **No border between sidebar and main content area.**
  WHY: A 1px separator between sidebar and content is a B2B visual convention. Consumer productivity apps separate the two surfaces with background colour only (`$surface` vs `$bg`). The absence of a line makes the interface feel lighter.

- [ ] **Task rows have no visible separator (hairlines between rows).**
  WHY: Row dividers are for data tables, not task lists. Consumer task apps rely on vertical spacing and hover states to define rows. Hairline dividers between tasks add visual clutter to a surface users stare at for hours.

### Personality

- [ ] **Empty state has a positive headline (not "No [noun] found").**
  WHY: Consumer apps are daily companions. "No tasks found" is a database result. "All caught up" is human. The empty state copy is the product's voice at its most visible; it appears multiple times per day for a productive user.

- [ ] **Priority is indicated by a flag icon, not a badge.**
  WHY: Status badges belong in workflow and enterprise surfaces where records need categorical classification. A personal task's priority is a personal marking. It should feel like a flag, not a system label. Flags are small, personal, and unobtrusive.

### Typography

- [ ] **Task names are 15px, not 14px.**
  WHY: 15px vs 14px is a small step, but consumer productivity apps are daily reading surfaces. At 14px, a full task list feels slightly compressed. 15px is the observed standard in Todoist and Things 3, confirmed via devtools.

- [ ] **Completed tasks are muted (fill: `$textMuted`), not struck through.**
  WHY: Strikethrough is aggressive. "This thing is wrong." Muted text says "this is done and is no longer relevant." Consumer productivity apps use muted text or gentle animation on completion, not strikethrough. (Exception: if the app's brand deliberately uses strikethrough as a personality choice, it must be consistent throughout.)

---

## Contrast examples

### Example 1: Task row (correct vs generic)

**Correct:**

```
taskItem=I(taskList, {
  type: "frame", name: "TaskItem",
  layout: "horizontal", alignItems: "center",
  gap: 10, padding: [0, 16],
  height: 44, width: "fill_container",
  cornerRadius: 0
  // No fill (transparent). Hover: bgAlt. No border.
})
checkCircle=I(taskItem, {
  type: "frame", width: 18, height: 18, cornerRadius: 9,
  stroke: { color: "$border", thickness: 1.5 }
})
taskName=I(taskItem, {
  type: "text", content: "Finish the quarterly review",
  fontSize: 15, fill: "$textPrimary",
  fontFamily: "$fontBody", lineHeight: 1.4
})
```

Why this is right: 44px height. No separator. Clean hollow circle for completion. 15px task name. Simple and legible.

**Generic:**

```
taskItem=I(taskList, {
  type: "frame", height: 32,   // WRONG: too dense
  layout: "horizontal",
  stroke: { bottom: { color: "$border", thickness: 1 } }  // WRONG: row separator
})
statusBadge=I(taskItem, {
  type: "frame",
  fill: "$accent at 15% opacity",   // WRONG: status badge on personal task
  cornerRadius: 4
})
taskName=I(taskItem, {
  type: "text", fontSize: 14   // WRONG: slightly too small
})
```

Why this is wrong: 32px rows are B2B density. Row separators add noise to a daily-use surface. Status badges on personal tasks look like calendar events, not a personal list. 14px makes the task list feel like metadata.

---

### Example 2: Completed task (correct vs generic)

**Correct:**

```
// After completion animation, task settles to:
taskItem_done=U(taskItem, { fill: "transparent" })
checkCircle_done=U(checkCircle, {
  fill: "$accent",
  stroke: null  // remove border
  // + white checkmark icon 10px inside
})
taskName_done=U(taskName, {
  fill: "$textMuted"  // muted, not struck through
})
```

Why this is right: accent-filled check communicates "done" emphatically. Muted task name says "no longer active" without the aggressive strikethrough. The completed item remains visible briefly, giving the user a moment of satisfaction before it moves to completed view.

**Generic:**

```
taskName_done=U(taskName, {
  textDecoration: "line-through",   // WRONG: strikethrough
  fill: "$textSecondary"   // still slightly too dark
})
checkCircle_done=U(checkCircle, {
  stroke: { color: "$statusDone" }   // WRONG: just coloured border, no fill
})
```

Why this is wrong: strikethrough implies rejection, not completion. "I crossed this out" is different from "I completed this." A green-bordered hollow circle conveys "checkbox", not "celebration." The completion check should feel like a small reward; the generic pattern treats it as a form field state.
