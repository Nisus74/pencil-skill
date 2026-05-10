# ai-augmented-workspace

Workspace surfaces where the user's primary activity is editing (code, documents, notes) and the AI surfaces contextually inline. The workspace comes first; the AI is a layer that appears on demand and retreats without friction.

**Surface category:** ai-products
**Exemplars:** Cursor (AI + code editor), Notion AI (document editor), Granola (AI note-taking), GitHub Copilot (inline suggestions)
**Confidence:** high; Cursor and Notion AI confirmed from direct use (May 2026)

Read this alongside `references/batch-design-grammar.md`. The critical differentiator from `conversation-chat` and `agent-execution`: there is no thread and no task tree. The AI interacts with the document the user is already editing. It cannot claim permanent screen space.

---

## When to use this archetype

Pick this when the product is primarily an editor (text, code, data, visuals) and the AI is a contextual affordance: suggesting completions, rewriting selections, answering inline questions, or summarising context. Skip it when the AI is the primary surface; use `conversation-chat` instead. Skip it when the AI is executing autonomous tasks; use `agent-execution` instead.

---

## The fundamental constraint

The AI must never permanently consume more than 30% of the workspace width without explicit user action. The workspace is the product. The AI is an enhancement. Any layout where the AI panel is equally prominent as the editor is a regression to a split-window design, not an augmented workspace.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | Matches host workspace. `#FAFAF9` (light), `#1B1B1D` (dark). | Page background. |
| `$ghostText` | `#C0BEBC` (light), `#4A4A50` (dark) | Inline AI suggestion text. Not `$textMuted`; it must be distinguishable from real muted text. |
| `$aiSurface` | `#F0EEF5` (light), `#252530` (dark) | AI-generated content region. Very slight tint, not a strong card colour. |
| `$aiSurfaceBorder` | `#DCD9F0` (light), `#3A3A4E` (dark) | Border of AI content regions. Matches `$aiSurface` tint family. |
| `$textPrimary` | Matches host workspace. | User's own content. |
| `$textSecondary` | Matches host workspace. | Labels, metadata. |
| `$accent` | Saturation 55–65%. | AI indicator icon, accept button, primary AI action. |
| `$border` | Matches host workspace. | General borders and dividers. |
| `$fontBody` | Matches host workspace. | Document text. |
| `$fontMono` | `Geist Mono` | Code completions, code context panel. |

The AI layer inherits the workspace's design language. Its distinguishing visual signals are `$ghostText`, `$aiSurface`, and the accent indicator. It does not use a different typeface or colour scheme.

---

## Ghost text (inline completion)

Ghost text is the least intrusive AI affordance: a suggestion continues the cursor without interrupting the editing flow.

```
// Ghost text appears inline after the user's text cursor
InlineCompletion (text, same font/size as surrounding text,
                   fill: "$ghostText",
                   content: " and returns a promise that resolves with the result")
│   // Same font family, same font size, same line-height as body text.
│   // Colour is the only differentiator: $ghostText, not $textPrimary.
│   // Dismissed on any keystroke except Tab (accept) or Right Arrow (accept word).
│
│   // NOT a separate text node stacked below.
│   // NOT a tooltip or popover.
│   // NOT italic or underlined.
```

### Acceptance indicator

```
AcceptHint (frame, fit_content x 20, layout: horizontal,
             alignItems: center, gap: 4,
             padding: [0, 8], cornerRadius: 4,
             fill: "$aiSurface",
             stroke: { color: "$aiSurfaceBorder", thickness: 1 })
│   // Appears at the end of the ghost text, not in the gutter.
├── HintIcon (12×12, $textMuted)  // typically a Tab key icon
└── HintLabel (text, 11px, $textMuted, $fontMono, content: "Tab")
```

### What generic looks like

```
// WRONG: ghost text in accent colour
InlineCompletion=I(editor, {
  fill: "$accent",   // bright blue/purple suggestion
  fontSize: 14
})
// Accent-coloured ghost text reads as a link or an error highlight.
// Ghost text must recede. The signal that it is AI content is its
// grey/muted colour, not a brand colour. Accent says "important"; ghost
// says "available if you want it."

// WRONG: ghost text in italic to distinguish it from user content
InlineCompletion=I(editor, {
  fontStyle: "italic",
  fill: "$ghostText"
})
// Italic at 14px in a monospace editor looks like an error state
// or a language comment. Use fill only; don't alter font style.
```

---

## Inline prompt panel

The inline prompt panel appears below the cursor when the user triggers an AI action (keyboard shortcut or slash command). It replaces the current selection or inserts at cursor.

```
InlinePromptPanel (frame, 480 x fit_content, layout: vertical,
                    gap: 0, cornerRadius: 10,
                    stroke: { color: "$aiSurfaceBorder", thickness: 1 },
                    fill: "$aiSurface",
                    // Positioned: below selection, aligned to left edge of selection
                    // If no room below, appears above.
                    shadow: { y: 4, blur: 12, color: "$border", opacity: 0.15 })
│   // Shadow is permitted here: floating panel, not embedded content.
│   // Shadow is required to separate the panel from the document it overlays.
├── PromptInput (frame, fill_container x 36, layout: horizontal,
│               alignItems: center, padding: [0, 12], gap: 8,
│               stroke: { bottom: { color: "$aiSurfaceBorder", thickness: 1 } })
│   ├── AIIndicator (frame, 16 x 16, cornerRadius: 8, fill: "$accent")
│   │   // Small accent circle: the AI's "handshake" icon.
│   └── PromptText (text-input, fill_container x fill_container,
│                    fontSize: 14, $fontBody, $textPrimary,
│                    placeholder: "Ask AI to write, edit, or explain...")
└── ActionRow (frame, fill_container x 36, layout: horizontal,
                alignItems: center, justifyContent: flex_end,
                padding: [0, 8], gap: 6)
    ├── EscLabel (text, 12px, $textMuted, content: "Esc to dismiss")
    └── SubmitButton (frame, fit_content x 26, cornerRadius: 5,
                       fill: "$accent", padding: [0, 10])
        └── SubmitLabel (text, 12px, fontWeight: 500, fill: white,
                          content: "Generate")
```

### AI result state

When the AI returns a result, it replaces the prompt input:

```
AIResultBlock (frame, fill_container x fit_content, layout: vertical, gap: 0)
├── ResultContent (text, same font/size as surrounding document,
│                   fill: "$textPrimary",
│                   background: "$aiSurface",
│                   padding: [12, 12])
│   // The result text inherits document styling.
│   // Background tint distinguishes it as unconfirmed.
└── ResultActions (frame, fill_container x 36, layout: horizontal,
                    alignItems: center, justifyContent: space_between,
                    padding: [0, 8])
    ├── AcceptButton (frame, fit_content x 26, cornerRadius: 5,
    │                  fill: "$accent", padding: [0, 10])
    │   └── AcceptLabel (text, 12px, fontWeight: 500, fill: white, content: "Accept")
    ├── RetryButton (ghost style, same dimensions)
    └── DismissButton (ghost style, same dimensions)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Panel width | 480px | Wide enough for a short prompt and a meaningful result. Narrow enough to not cover the whole document. |
| Panel position | Below selection, left-aligned | Contextual to where the user triggered it. Shift up if no room below. |
| Corner radius | 10px | Slightly rounder than a card (8px). Signals "floating" rather than "embedded." |
| Shadow | y: 4, blur: 12 | Required for floating panels. One of the few valid shadow uses in this archetype. |

---

## Selection toolbar

The selection toolbar appears above a text selection when the user holds still for 600ms or triggers via keyboard shortcut. It offers 3–5 primary AI actions.

```
SelectionToolbar (frame, fit_content x 36, layout: horizontal,
                   alignItems: center, gap: 2, padding: [0, 4],
                   cornerRadius: 8,
                   stroke: { color: "$border", thickness: 1 },
                   fill: "$bg",
                   shadow: { y: 2, blur: 8, color: "$border", opacity: 0.12 })
│   // Appears above selection, centered horizontally on selection.
│   // Floats with the selection; disappears on deselect.
└── ToolbarAction × 3–5
    // Each action: 28 x 28, cornerRadius: 6, fill: transparent,
    // hover fill: "$aiSurface"
    // Icon: 16×16, $textSecondary
    // Tooltip on hover: text label (not always-visible label)
    // Common actions: Improve, Shorter, Longer, Explain, Translate
```

### What generic looks like

```
// WRONG: selection toolbar as a permanent floating bar always visible
SelectionToolbar=I(editor, {
  position: "fixed",
  bottom: 24, right: 24   // corner-pinned, always visible
})
// A permanent toolbar competes with the editing surface.
// The selection toolbar is contextual — it appears on demand and
// vanishes when done. Corner-pinned toolbars claim permanent territory;
// contextual toolbars don't.

// WRONG: 8+ actions in the toolbar
SelectionToolbar=I(selection, { width: 320, ... })
// Improve, Shorter, Longer, Rephrase, Formal, Casual,
// Translate, Summarise, Explain, Ask follow-up
// More than 5 actions requires reading. 3–4 actions are instantly scannable.
// Overflow to a "More" icon if additional actions are needed.
```

---

## AI side panel

The side panel is optional, user-invoked, and closeable. It shows AI context without requiring the user to leave the editing surface.

```
AISidePanel (frame, 300 x fill_container, layout: vertical,
              fill: "$bg",
              stroke: { left: { color: "$border", thickness: 1 } })
│   // 300px. Never wider than 320px — 1/4 of a 1280px screen.
│   // User-invoked (keyboard shortcut or toolbar button).
│   // Closeable via × button or same keyboard shortcut.
├── PanelHeader (frame, fill_container x 44, layout: horizontal,
│               alignItems: center, justifyContent: space_between,
│               padding: [0, 12],
│               stroke: { bottom: { color: "$border", thickness: 1 } })
│   ├── PanelTitle (text, 13px, fontWeight: 600, $textPrimary,
│   │               content: "AI context")
│   └── CloseButton (frame, 24 x 24, cornerRadius: 4, fill: transparent)
│       └── CloseIcon (14×14, $textSecondary)
└── PanelContent (frame, fill_container x fill_container,
                   overflow: "vertical_scroll", padding: [12, 12])
    // Contains: context summary, suggested actions, chat history (if any)
```

### What generic looks like

```
// WRONG: side panel auto-opens and defaults to 40% of screen width
AISidePanel=I(appShell, {
  width: 480,   // WRONG: ~37% of a 1280px screen
  // opens automatically without user action
})
// A 480px AI panel on a 1280px editor leaves 800px for code or documents.
// That's a split-view workspace, not an AI-augmented workspace.
// 300px at 1280px is 23% — enough for context, not enough to displace the editor.
```

---

## Microcopy library

### Inline prompt placeholder

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Enter your instruction | Ask AI to write, edit, or explain... |
| What would you like the AI to do? | Improve this paragraph |
| AI command | Edit or generate |

Keep the placeholder short and action-first. The user triggered this intentionally; don't over-explain.

### Selection toolbar actions

Keep labels to one word or a very short verb phrase. These appear as icon tooltips, not button labels.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Make it better | Improve |
| Make it shorter / reduce length | Shorter |
| Make it longer / expand | Longer |
| Reword this | Rephrase |
| Explain this to me | Explain |

### Ghost text acceptance

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Press Tab to accept this suggestion | Tab |
| Accept AI suggestion | Tab to accept |
| Click to accept | Tab |

The acceptance hint should be a key symbol (or short key name), not a sentence.

### AI result actions

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Insert this text | Accept |
| Apply changes | Accept |
| Try again | Retry |
| Close / cancel | Dismiss |

---

## Verification checklist

### The workspace-first principle

- [ ] **The editor/document area is at least 70% of the screen width at default state.**
  WHY: An AI panel wider than 30% of the screen produces a split-view workspace. Split-view is a conscious decision the user makes; it should not be the default. The AI is an enhancement, not an equal partner in the layout.

- [ ] **No AI affordance is always visible when the user is editing.**
  WHY: Persistent AI chrome distracts from the editing task. Ghost text appears at cursor position on demand. The selection toolbar appears on selection. The side panel requires user invocation. AI that's always visible is noise; AI that appears when needed is enhancement.

### Ghost text

- [ ] **Ghost text colour is `$ghostText`, not `$accent` and not `$textMuted`.**
  WHY: `$accent` reads as a link or error. `$textMuted` may collide with intentionally muted content in the document (comments, metadata). `$ghostText` is a dedicated value, intentionally between `$textMuted` and `$textSecondary`, chosen to be visible but clearly non-primary.

- [ ] **Ghost text uses the same font family, size, and line-height as the surrounding document text.**
  WHY: Any typographic shift (different font, size, or italic) breaks the visual flow of the text. The suggestion must feel like a possible continuation of the user's sentence, not a foreign element inserted into it.

### Floating panels

- [ ] **Inline prompt panel and selection toolbar have a shadow.**
  WHY: Floating panels over document content require a shadow to separate them from what they overlay. Without a shadow, a panel on top of text reads as text with a background box. It looks broken. This is one of the few valid shadow uses in the AI-product family.

- [ ] **AI side panel is closeable and does not auto-open.**
  WHY: The user is editing. An AI panel opening automatically, even once, interrupts their focus. The panel must be on demand. "Helpful proactive surfacing" that interrupts editing is not helpful; it's an interruption with good intentions.

### Inline result

- [ ] **AI-generated result uses `$aiSurface` tint, not `$accent` fill.**
  WHY: An accent-filled result region looks like a highlighted selection or an error state. `$aiSurface` is a very subtle tint (nearly the same as `$bg`) that signals "this is pending confirmation" without claiming visual dominance.

---

## Contrast examples

### Example 1: Ghost text (correct vs generic)

**Correct:**

```
ghostText=I(editorLine, {
  type: "text",
  content: " returns the filtered array sorted by createdAt",
  fontFamily: "$fontMono",   // same as editor
  fontSize: 14,              // same as editor
  lineHeight: 1.6,           // same as editor
  fill: "$ghostText"         // the ONLY visual differentiator
})
acceptHint=I(editorLine, {
  type: "frame",
  layout: "horizontal", alignItems: "center", gap: 4,
  padding: [0, 6], cornerRadius: 4,
  fill: "$aiSurface",
  stroke: { color: "$aiSurfaceBorder", thickness: 1 }
  // Tab key icon + "Tab" label, 11px $fontMono $textMuted
})
```

Why this is right: same font, same size, same line-height as the editor. The only difference is fill colour. The acceptance hint is a small, muted badge. Nothing shouts; the suggestion is available and easy to confirm or ignore.

**Generic:**

```
ghostText=I(editorLine, {
  type: "text",
  content: " returns the filtered array sorted by createdAt",
  fontFamily: "$fontMono", fontSize: 14,
  fill: "$accent",     // WRONG: bright accent colour
  fontStyle: "italic"  // WRONG: italic to indicate AI origin
})
popover=I(editorLine, {
  type: "frame",
  fill: "$aiSurface",
  cornerRadius: 8, padding: [8, 12],
  // Contains: "Accept suggestion" button and "Dismiss" button
  // WRONG: a popover for a ghost text acceptance is too heavy
})
```

Why this is wrong: accent colour makes the ghost text look like a hyperlink. Italic breaks the typographic continuity; the line no longer feels like a coherent sentence. The accept popover requires mouse movement and a click for a flow that should be Tab-key ergonomics. Heavy affordances for lightweight actions train users to avoid them.

---

### Example 2: Selection toolbar (correct vs generic)

**Correct:**

```
toolbar=I(selection, {
  type: "frame", name: "SelectionToolbar",
  layout: "horizontal", alignItems: "center",
  gap: 2, padding: [0, 4],
  cornerRadius: 8,
  height: 36,
  stroke: { color: "$border", thickness: 1 },
  fill: "$bg",
  shadow: { y: 2, blur: 8, color: "#000000", opacity: 0.12 }
  // 4 action buttons: Improve, Shorter, Longer, Explain
  // Each: 28×28, icon only, tooltip on hover
})
```

Why this is right: 4 actions, icon-only, tooltip on hover. Small (36px tall) and unobtrusive. `$bg` fill blends with the page; the 1px border and shadow give it edge. Appears above the selection; disappears on deselect.

**Generic:**

```
toolbar=I(editor, {
  type: "frame",
  position: "fixed", bottom: 24, right: 24,   // WRONG: always visible, corner-pinned
  width: 280,
  fill: "$accent",   // WRONG: accent fill for chrome
  cornerRadius: 12
  // Contains 8 labelled action buttons
})
```

Why this is wrong: a permanently-visible corner toolbar occupies visual space even when no text is selected. Accent fill turns chrome into content. Eight labelled buttons require reading. This is a feature toolbar masquerading as a contextual tool. The selection toolbar should appear and vanish with the selection; it should feel like it appeared because the user did something, not because the app is always presenting options.
