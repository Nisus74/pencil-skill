# agent-execution

Surfaces where an AI agent is actively doing autonomous work and the human is watching, intervening, and reviewing. The primary content is a live task tree: what the agent queued, what it's doing now, what it completed, and what failed.

**Surface category:** ai-products
**Exemplars:** Devin (cognition.ai), GitHub Actions run view, Claude Code terminal output, Linear automation logs
**Confidence:** medium-high; Devin confirmed from published screenshots and demos (May 2026); GitHub Actions from devtools

Read this alongside `references/batch-design-grammar.md`. The critical differentiator from `conversation-chat`: there are no message bubbles. The agent is not responding to queries; it is executing a plan.

---

## When to use this archetype

Pick this when the primary UI is a live task list of the agent doing something: running commands, editing files, calling APIs, navigating, writing code. Skip it when the user is the primary actor; use `modern-pro-tool` or `conversation-chat` instead. If the AI is embedded as a panel inside an existing workspace, use `ai-augmented-workspace`.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#0D0D0F` | Dark primary background. Agent execution feels like a terminal; dark is canonical. |
| `$bgPanel` | `#161618` | Slightly lighter surface for content panels. |
| `$bgRow` | `#1C1C1F` | Task row hover / focus state. |
| `$textPrimary` | `#F0EEEC` | Main task descriptions, agent output prose. |
| `$textSecondary` | `#A8A29E` | Subtask labels, timestamps, step counts. |
| `$textMuted` | `#57534E` | Pending tasks, metadata. |
| `$accent` | Saturation 55–65% | Active task indicator, links, primary actions. |
| `$statusDone` | `#22C55E` (green-500) | Completed task icon, success output. |
| `$statusError` | `#EF4444` (red-500) | Failed task, error output, error count badge. |
| `$statusActive` | Same as `$accent` | In-progress spinner and left-border indicator. |
| `$statusPending` | `#57534E` | Queued/pending task icon (muted). |
| `$statusNeedsInput` | `#F59E0B` (amber-500) | Waiting-for-human indicator. |
| `$border` | `#2A2A2E` | Panel borders, task row dividers. |
| `$fontBody` | `Inter` or `system-ui` | Task descriptions, prose output. |
| `$fontMono` | `Geist Mono` | Terminal output, file paths, commands, code. |
| `$logOutput` | `#D4D0CB` | Terminal output text (slightly dimmer than $textPrimary). |

---

## Page shell

```
AppShell (frame, fill_container x fill_container, layout: horizontal,
           fill: "$bg")
├── SessionSidebar (frame, 240 x fill_container, layout: vertical,
│                   fill: "$bgPanel",
│                   stroke: { right: { color: "$border", thickness: 1 } })
│   // Optional — some agent surfaces omit the sidebar entirely.
│   // Contains: session history list, new session button.
└── MainPanel (frame, fill_container x fill_container, layout: vertical,
                fill: "$bg")
    ├── AgentHeader (frame, fill_container x 56, layout: horizontal)
    │   // Contains: task headline, status badge, abort button.
    ├── TaskTree (frame, fill_container x fill_container,
    │             overflow: "vertical_scroll")
    │   // The primary content: nested task rows.
    └── OutputPanel (frame, fill_container x 280, layout: vertical,
                      fill: "$bgPanel",
                      stroke: { top: { color: "$border", thickness: 1 } })
        // Live terminal / log output. Fixed height, resizable in real product.
```

---

## Agent header

```
AgentHeader (frame, fill_container x 56, layout: horizontal,
              alignItems: center, justifyContent: space_between,
              padding: [0, 20], fill: "$bg",
              stroke: { bottom: { color: "$border", thickness: 1 } })
├── HeaderLeft (frame, fit_content x fit_content, layout: horizontal,
│               alignItems: center, gap: 12)
│   ├── StatusIndicator (frame, 8 x 8, cornerRadius: 4)
│   │   // fill: "$statusActive" when running, "$statusDone" when complete,
│   │   // "$statusError" when failed.
│   │   // When active: animated pulse — rendered as two concentric circles,
│   │   // outer at 50% opacity.
│   ├── TaskHeadline (text, 15px, fontWeight: 600, $textPrimary,
│   │                 content: "Implementing the OAuth flow")
│   └── StepCount (text, 13px, $textSecondary,
│                   content: "Step 3 of 7")
└── AbortButton (frame, fit_content x 32, layout: horizontal,
                  alignItems: center, gap: 6, padding: [0, 12],
                  cornerRadius: 6,
                  stroke: { color: "$statusError", thickness: 1 })
    ├── StopIcon (12×12, fill: "$statusError")
    └── AbortLabel (text, 13px, fontWeight: 500, fill: "$statusError",
                     content: "Stop")
```

### What generic looks like

```
// WRONG: abort button styled as a primary CTA
AbortButton=I(header, {
  type: "frame",
  fill: "$statusError",
  cornerRadius: 6, padding: [0, 16]
  // Red-filled button
})
// A filled red stop button reads as an alarm — visually dominates the header.
// The abort is an escape hatch, not a primary action. Ghost style (red border,
// red text, transparent fill) communicates "available if needed" rather than
// "click this." A big red button implies the agent is dangerous; a ghost button
// implies you're in control.
```

---

## Task tree

The task tree is the core component. Every task has a status, description, and optional subtasks.

```
TaskTree (frame, fill_container x fit_content, layout: vertical,
           gap: 0, padding: [16, 16])

TaskRow (frame, fill_container x 40, layout: horizontal,
          alignItems: center, gap: 10,
          padding: [0, 8],
          cornerRadius: 6)
│   // Active task row: fill: "$bgRow", left border 2px $statusActive
│   // Done task row: fill: transparent
│   // Pending task row: fill: transparent, opacity: 0.6
├── StatusIcon (frame, 20 x 20, layout: none)
│   // Pending:    hollow circle, stroke 1.5px $statusPending
│   // Active:     animated ring (SVG spinner in real; rendered as ring + inner dot)
│   // Done:       checkmark icon, fill: "$statusDone"
│   // Failed:     × icon, fill: "$statusError"
│   // NeedsInput: ? icon, fill: "$statusNeedsInput"
├── TaskLabel (text, 14px, $textPrimary, $fontBody, lineHeight: 1.4,
│              width: "fill_container")
│   // Done tasks: fill: "$textSecondary" (dimmed, but not strikethrough)
│   // Active task: fill: "$textPrimary", fontWeight: 500
└── TaskMeta (frame, fit_content x fit_content, layout: horizontal,
               alignItems: center, gap: 8)
    ├── Duration (text, 12px, $textMuted,
    │             content: "2s" or "14s" — elapsed time on completed tasks)
    └── ExpandIcon (12×12, $textMuted)
        // Shown when the task has subtasks. Rotates on expand.
```

### Subtask nesting

```
SubtaskRow (TaskRow with indent: 28)
│   // 28px left indent per nesting level.
│   // Maximum visible nesting: 3 levels. Beyond that, collapse.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Task row height | 40px | 36px is the minimum (text + breathing room). 40px for primary tasks. |
| Status icon size | 20px | Larger than inline text icons (16px). The status column needs visual presence. |
| Left indent per level | 28px | Enough to read as a tree; less than 24px collapses the hierarchy. |
| Active left border | 2px, `$statusActive` | The running task gets the only persistent left border on this surface. |
| Done task opacity | `$textSecondary` fill | Dimmed but not strikethrough. Strikethrough implies "rejected," not "completed." |

### What generic looks like

```
// WRONG: strikethrough on completed tasks
DoneTask=I(tree, {
  type: "frame",
  // task label inside:
  textDecoration: "line-through"
})
// Strikethrough means "rejected" or "invalid." Completed tasks are achievements.
// Dimming to $textSecondary says "done, no longer active" without implying error.

// WRONG: status indicator as a coloured dot only (no icon)
StatusDot=I(row, {
  type: "frame", width: 8, height: 8, cornerRadius: 4,
  fill: "$statusActive"   // or $statusDone, etc.
})
// An 8px dot is invisible for users scanning a long task list. The status icon
// at 20px with a distinct shape (circle, check, x, ?) allows rapid visual scanning.
// Colour alone is also not accessible to colour-blind users.
```

---

## Needs-input state

When the agent requires human input to proceed, execution pauses. The specific task enters the needs-input state.

```
NeedsInputRow (TaskRow with fill: "$bgRow" and left border 2px $statusNeedsInput)
├── StatusIcon (? icon, fill: "$statusNeedsInput")
├── TaskLabel (text, 14px, $textPrimary)
│   content: "Which database should I use for the session store?"
└── InputPrompt (frame, fill_container x fit_content, layout: vertical,
                  gap: 8, padding: [8, 0, 0, 30])
    // 30px left padding = icon width + gap, aligns with task label column
    ├── InputField (frame, fill_container x 36, cornerRadius: 6,
    │               stroke: { color: "$statusNeedsInput", thickness: 1 })
    │   // Amber border to signal "your input required here."
    └── SubmitRow (frame, fit_content x fit_content, layout: horizontal, gap: 8)
        ├── SubmitButton (frame, fit_content x 28, cornerRadius: 5,
        │                  fill: "$accent", padding: [0, 12])
        │   └── SubmitLabel (text, 13px, fontWeight: 500, fill: white,
        │                     content: "Continue")
        └── SkipButton (frame, fit_content x 28, cornerRadius: 5,
                         stroke: { color: "$border", thickness: 1 })
            └── SkipLabel (text, 13px, $textSecondary, content: "Skip")
```

---

## Output panel

The output panel shows live terminal output: commands executed, file changes, API calls, errors.

```
OutputPanel (frame, fill_container x 280, layout: vertical,
              fill: "$bgPanel",
              stroke: { top: { color: "$border", thickness: 1 } })
├── OutputHeader (frame, fill_container x 36, layout: horizontal,
│                  alignItems: center, justifyContent: space_between,
│                  padding: [0, 16],
│                  stroke: { bottom: { color: "$border", thickness: 1 } })
│   ├── OutputTitle (text, 12px, fontWeight: 500, $textSecondary,
│   │                 content: "Terminal output")
│   └── OutputControls (frame, fit_content, layout: horizontal, gap: 8)
│       // Copy button, clear button: 24×24, fill: transparent, $textMuted icons
└── OutputScroll (frame, fill_container x fill_container,
                   overflow: "vertical_scroll",
                   padding: [8, 16])
    └── OutputLine × N
        // Command lines:   "$ npm install" — $fontMono, 13px, $logOutput
        // Output lines:    "added 148 packages" — $fontMono, 13px, $textSecondary
        // Error lines:     "Error: ENOENT" — $fontMono, 13px, $statusError
        // Step separator:  1px hairline $border, full-width, 4px vertical gap
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Output panel height | 280px (fixed baseline) | Tall enough to show ~15 lines at 13px line-height 1.6. |
| Terminal font | `$fontMono`, 13px | Same as code blocks in conversation-chat. Commands must read as code. |
| Line height in output | 1.6 | Dense enough to pack lines, legible enough to scan quickly. |
| Error line colour | `$statusError` | Errors must be visually distinct without reading. |

### What generic looks like

```
// WRONG: terminal output in proportional font
OutputLine=I(output, {
  fontFamily: "$fontBody",   // Inter, system-ui
  fontSize: 13
})
// Proportional font makes terminal output look like a chat message.
// Monospace is load-bearing: it signals "this is machine output" and
// aligns multicolumn output (file names, sizes, status columns).

// WRONG: output panel full height (no header, no task tree visible above)
OutputPanel=I(mainPanel, {
  height: "fill_container"
})
// Full-height output is a terminal emulator. The task tree is what makes this
// an agent interface. The split: ~60% task tree, ~40% output.
```

---

## Artifact display

When the agent produces a file or artefact the user can review, it surfaces inline in the task tree.

```
ArtifactCard (frame, fill_container x fit_content, layout: horizontal,
               gap: 10, padding: [10, 12],
               cornerRadius: 8,
               stroke: { color: "$border", thickness: 1 },
               fill: "$bgPanel",
               margin: [4, 0, 0, 30])
│   // 30px left margin aligns with task label column.
├── FileIcon (16×16, $textSecondary)
├── ArtifactMeta (frame, fill_container x fit_content, layout: vertical, gap: 2)
│   ├── FileName (text, 13px, fontWeight: 500, $textPrimary,
│   │             content: "src/auth/oauth.ts")
│   └── FileDetail (text, 12px, $textSecondary,
│                    content: "+142 lines")
└── ViewButton (frame, fit_content x 24, cornerRadius: 4,
                 stroke: { color: "$border", thickness: 1 },
                 padding: [0, 8])
    └── ViewLabel (text, 12px, $textSecondary, content: "View diff")
```

The artefact card is an exception to this archetype's "no cards" rule. Files are discrete, reviewable objects; a card border is appropriate to signal "this is a thing you can open."

---

## Microcopy library

### Header states

| State | Headline pattern | Step label |
|-------|-----------------|------------|
| Running | "Implementing the OAuth flow" | "Step 3 of 7" |
| Complete | "OAuth flow implemented" | "7 of 7 complete" |
| Failed | "Stopped at step 4" | "4 of 7 complete" |
| Needs input | "Waiting for your input" | "Paused at step 3" |

### Task labels

Imperative past tense for done, imperative present for active, imperative future for pending.

| State | Example label |
|-------|---------------|
| Pending | "Analyse the existing auth middleware" |
| Active | "Writing the token refresh handler" |
| Done | "Created `src/auth/tokens.ts`" |
| Failed | "Could not connect to the test database" |
| Needs input | "Which environment should I target?" |

### Abort / stop controls

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Cancel | Stop |
| Terminate | Interrupt |
| Kill process | Stop generating |
| Abort | Stop (keep work so far) |

The label "Stop (keep work so far)" is worth using when partial work persists; it reduces hesitation to abort.

---

## Verification checklist

### Status system

- [ ] **Five distinct status states are implemented: pending, active, done, failed, needs-input.**
  WHY: A task list with only "done" and "not done" loses the ability to show live progress. The active spinner tells the user work is happening right now. The needs-input amber marker is the most important state: missing it means the agent silently stalls with no signal to the user.

- [ ] **Status icons are 20px with distinct shapes, not coloured dots.**
  WHY: Coloured dots at 8px are invisible in a long task list. Distinct shapes (ring, check, x, question mark) allow status scanning without colour dependency. This also serves colour-blind users.

- [ ] **Completed tasks are dimmed to `$textSecondary`, not struck through.**
  WHY: Strikethrough means "rejected." Dimming means "done, no longer active." The distinction matters: a long list of strikethrough items looks like a to-do list of failures.

### Terminal output

- [ ] **Output panel uses `$fontMono` at 13px.**
  WHY: Proportional font on terminal output looks like a chat transcript. Monospace is the visual code for "machine output." It also preserves column alignment in structured logs (file paths, status flags, timestamps in columns).

- [ ] **Error lines are `$statusError` colour.**
  WHY: In a fast-scrolling log, errors must be visible without reading. A red line in a grey stream registers instantly. Without colour differentiation, the user has to read every line to catch a failure.

### Layout

- [ ] **Task tree and output panel are both visible (not one or the other).**
  WHY: Hiding the task tree produces a terminal emulator. Hiding the output panel produces a todo list. The split view is what makes this an agent-execution surface: you see what the agent planned AND what it did.

- [ ] **Abort/stop control is ghost style (stroke, not fill), red colour.**
  WHY: A red-filled abort button dominates the header and reads as an alarm. Ghost style (red border, red label, transparent fill) is available and legible without visually screaming. The agent interface should read as calm and in-control, not dangerous.

- [ ] **Active task has a 2px `$statusActive` left border, not a filled row.**
  WHY: Filled rows in task trees look like selection. Active does not mean selected. The left border is the same signal used for the "current" state in other list contexts (code editors use a left indicator for the current line). It communicates "this is where execution is" without implying the user chose it.

---

## Contrast examples

### Example 1: Task row (correct vs generic)

**Correct:**

```
taskRow=I(taskTree, {
  type: "frame", name: "TaskRow",
  layout: "horizontal", alignItems: "center", gap: 10,
  height: 40, width: "fill_container",
  padding: [0, 8], cornerRadius: 6,
  fill: "$bgRow",
  stroke: { left: { color: "$statusActive", width: 2 } }
  // Active row only
})
statusIcon=I(taskRow, {
  type: "frame", name: "StatusIcon",
  width: 20, height: 20, cornerRadius: 10,
  stroke: { color: "$statusActive", thickness: 2 }
  // Animated spinner ring in production
})
taskLabel=I(taskRow, {
  type: "text",
  content: "Writing the token refresh handler",
  fontSize: 14, fontWeight: 500, fill: "$textPrimary",
  lineHeight: 1.4
})
```

Why this is right: 2px active left border signals "execution is here" without implying selection. 20px status icon is visible in a list. Task label at 14px, fontWeight 500 makes the active task distinct from pending (muted) and done (dimmed).

**Generic:**

```
taskRow=I(taskTree, {
  type: "frame", height: 40, layout: "horizontal",
  fill: "$bgRow"   // same fill regardless of state
})
statusDot=I(taskRow, {
  type: "frame", width: 8, height: 8, cornerRadius: 4,
  fill: "$statusActive"   // WRONG: 8px dot, shape carries no meaning
})
taskLabel=I(taskRow, {
  type: "text", fontSize: 14,
  fill: "$textPrimary"   // WRONG: same fill for all states
  // No differentiation between active, pending, done
})
```

Why this is wrong: an 8px coloured dot is invisible at scanning speed. No state differentiation on the label means the user has to read every row to know what's active. Without the left border, the "active" state is a slightly different shade of the same background. The agent could have stopped and the user wouldn't notice for several seconds.

---

### Example 2: Needs-input state (correct vs generic)

**Correct:**

```
needsInputRow=I(taskTree, {
  type: "frame", name: "NeedsInputRow",
  fill: "$bgRow",
  stroke: { left: { color: "$statusNeedsInput", width: 2 } }
  // Amber left border signals: I need you
})
statusIcon=I(needsInputRow, {
  // ? icon, 20px, fill: "$statusNeedsInput"
})
taskLabel=I(needsInputRow, {
  type: "text",
  content: "Which database should I use for the session store?",
  fontSize: 14, fill: "$textPrimary"
})
inputField=I(needsInputRow, {
  type: "frame", height: 36, width: "fill_container",
  cornerRadius: 6,
  stroke: { color: "$statusNeedsInput", thickness: 1 },
  // Amber border matches the row state indicator
  margin: [8, 0, 0, 30]
})
```

Why this is right: amber is distinct from both the green (done) and blue (active) states. The amber border on the input field echoes the row's left border; they're the same signal at two scales. The 30px left margin aligns the input with the task label column.

**Generic:**

```
needsInputRow=I(taskTree, {
  type: "frame",
  fill: "$bgRow"   // WRONG: same fill as the active task — indistinguishable
})
clarificationLabel=I(needsInputRow, {
  type: "text",
  content: "Waiting for input...",   // WRONG: passive, generic
  fill: "$textMuted"   // WRONG: muted label is easy to miss
})
inputField=I(needsInputRow, {
  type: "frame", height: 36, cornerRadius: 4,
  stroke: { color: "$border", thickness: 1 }
  // WRONG: standard border — looks like any other input
})
```

Why this is wrong: "Waiting for input..." is not a question. The agent paused and the user doesn't know what's being asked. The standard `$border` input looks identical to any form field. The muted fill on the label makes the only interaction-required state the hardest to notice. An agent surface that can't clearly communicate "I need you" will appear frozen rather than paused.
