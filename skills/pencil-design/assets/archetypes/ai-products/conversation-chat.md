# conversation-chat

Chrome-light, prose-led surfaces where an AI is a participant in the conversation. The thread is the product; every design decision either serves legibility of the AI's output or gets out of the way.

**Surface category:** ai-products
**Exemplars:** Claude.ai, ChatGPT, Perplexity
**Confidence:** high; confirmed against Claude.ai and ChatGPT devtools (May 2026)

Read this alongside `references/batch-design-grammar.md`. The critical anti-cue: AI messages are NOT bubbles. Do not reach for the SMS/messaging-app pattern.

---

## When to use this archetype

Pick this for dedicated AI assistant surfaces, chatbot UIs, and any product where the primary interaction is: user types query, AI responds with prose (including code, lists, and structured text). Skip it when the AI is embedded inside an existing workspace or when the primary content is the AI doing autonomous tasks; use `ai-augmented-workspace` or `agent-execution` instead.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#FAFAF9` | Main thread area background. Near-white, warm. |
| `$bgSidebar` | `#F5F4F2` | Sidebar background. One step darker than `$bg`. |
| `$surface` | `#EFEEEC` | User message bubble fill. Warm neutral, not white. |
| `$surfaceHover` | `#ECEAE8` | Sidebar row hover. |
| `$surfaceActive` | `#E5E3E0` | Sidebar active conversation row. |
| `$textPrimary` | `#111110` | Message text, headings inside AI response. |
| `$textSecondary` | `#6B6A6B` | Timestamps, model label, placeholder text. |
| `$textMuted` | `#A1A0A0` | Code block language label, metadata. |
| `$accent` | Saturation 55–65%. | Submit button active state, link colour inside AI responses. |
| `$border` | `#E7E5E4` | Composer border, code block optional border. |
| `$fontBody` | `Inter` or `system-ui` | All message text. |
| `$fontMono` | `Geist Mono` | Code blocks inside AI messages. |
| `$codeBlockBg` | `#F0F0EE` (light), `#1C1C1E` (dark) | Code block fill. |

---

## Page shell

```
AppShell (frame, fill_container x fill_container, layout: horizontal,
           fill: "$bg")
├── Sidebar (frame, 260 x fill_container, layout: vertical,
│             fill: "$bgSidebar")
│   // 260px. Confirmed against ChatGPT and Claude.ai devtools.
│   // Contains: new chat button, conversation history list.
└── ThreadPanel (frame, fill_container x fill_container, layout: vertical,
                  fill: "$bg")
    // Contains: thread area (scrollable) + composer (bottom-fixed).
```

### What generic looks like

```
// WRONG: sidebar width 200px or 320px+
Sidebar=I(shell, { width: 200 })
// 200px clips conversation titles. 320px+ is a content panel, not a nav rail.
// 260px is calibrated to show ~35 characters of conversation title.

// WRONG: sidebar fill: "$bg" (same as main area)
Sidebar=I(shell, { fill: "$bg" })
// Identical fills read as one continuous surface. The sidebar needs to
// visually recede from the thread content. One step of value separation ($bgSidebar)
// is enough; shadows, borders, or hard contrasts are too much.
```

---

## Sidebar: conversation history

```
Sidebar (frame, 260 x fill_container, layout: vertical, gap: 0,
          padding: [12, 8, 12, 8], fill: "$bgSidebar")
├── NewChatButton (frame, fill_container x 36, layout: horizontal,
│                  alignItems: center, padding: [0, 12], gap: 8,
│                  cornerRadius: 8,
│                  stroke: { color: "$border", thickness: 1 })
│   ├── PlusIcon (24×24, $textSecondary)
│   └── NewChatLabel (text, 14px, fontWeight: 500, $textPrimary,
│                      content: "New chat")
├── SectionLabel (text, 12px, $textMuted, $fontBody,
│                 content: "Today", padding: [12, 12, 4, 12])
│   // Section labels group conversations. 12px, all-caps not required.
└── ConversationList (frame, fill_container x fit_content, layout: vertical,
                       gap: 2)
    └── ConversationRow × N
        // Row: 36px height, fill_container width, cornerRadius: 6
        // Active state: fill: "$surfaceActive"
        // Hover state: fill: "$surfaceHover"
        // Resting state: fill: transparent
        // Title: 14px, $textPrimary, single line, truncated at fill_container
```

### Active state

```
// Active conversation row: filled background, no left border
ConversationRow=U(row, {
  fill: "$surfaceActive",
  cornerRadius: 6
})

// WRONG: 2px left border as active indicator
ConversationRow=U(row, {
  stroke: { left: { color: "$accent", width: 2 } }
})
// Left-border active states belong to analytics-dashboard sidebar nav.
// Conversation lists are file-selector hierarchies, not navigation menus.
// The filled background row reads as "selected" without claiming column ownership.
```

---

## Thread area

```
ThreadScrollContainer (frame, fill_container x fill_container,
                         overflow: "vertical_scroll",
                         layout: vertical, alignItems: center,
                         padding: [24, 0, 120, 0])
│   // Bottom padding 120px: clearance above the composer.
│   // alignItems: center — this is how the 720px max-width content
│   // stays centred within a wider panel.
└── ThreadContent (frame, 720 x fit_content, layout: vertical,
                    gap: 24)
    // 720px max-width. Confirmed against Claude.ai devtools (720px).
    // 24px gap between message groups.
    └── MessageGroup × N
        // Either UserMessage or AIMessage — not mixed in one group.
```

---

## User message

```
UserMessage (frame, fill_container x fit_content, layout: horizontal,
              justifyContent: flex_end)
│   // Right-aligned in the thread. The frame is fill_container;
│   // the bubble inside constrains the width.
└── UserBubble (frame, fit_content x fit_content,
                 maxWidth: 504,
                 layout: vertical,
                 padding: [10, 14],
                 cornerRadius: 12,
                 fill: "$surface")
    └── UserText (text, 15px, $textPrimary, $fontBody,
                   lineHeight: 1.6, width: "fill_container")
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Bubble max-width | 504px | ~70% of 720px thread width. Short queries look compact; long ones have headroom. |
| Bubble fill | `$surface` (#EFEEEC) | Warm neutral. Not white (invisible), not `$accent` (WhatsApp pattern). |
| Corner radius | 12px | Consistent with composer. Not pill (24px+), not square (0). |
| Font size | 15px | Not 14px (too dense) or 16px (too loose). |
| Alignment | Right | User content on the right. This is the only asymmetry. |
| No avatar | required | User messages have no avatar. |

### What generic looks like

```
// WRONG: user message bubble filled with $accent
UserBubble=I(thread, {
  fill: "$accent",
  ...
})
// $accent-filled bubbles are iMessage/WhatsApp. AI chat surfaces use warm neutrals
// because the brand personality is more like a document tool than a messaging app.
// A blue user bubble also creates visual competition with the AI's accent-coloured links.

// WRONG: user message left-aligned (same side as AI)
UserMessage=I(thread, {
  justifyContent: "flex_start"
})
// Without right-alignment, user and AI messages are visually indistinguishable at a glance.
// The positional asymmetry is the primary signal that encodes "who said what."
```

---

## AI message

```
AIMessage (frame, fill_container x fit_content, layout: horizontal,
            gap: 12, alignItems: flex_start)
│   // Left-aligned. Full thread width. No fill, no border.
├── AIAvatar (frame, 28 x 28, cornerRadius: 14,
│             fill: "$accent" or brand-specific fill)
│   // 28px circular. Contains model icon or monogram.
│   // Acts as a fixed visual anchor for the left column.
└── AIContent (frame, fill_container x fit_content, layout: vertical,
                gap: 16)
    ├── AIText (text, 15px, $textPrimary, $fontBody,
    │           lineHeight: 1.65, width: "fill_container")
    │   // 1.65 line-height: reading copy, not app density.
    │   // This is the most important single value in this archetype.
    ├── CodeBlock? (see Code block section)
    └── MessageActions (frame, fit_content x fit_content, layout: horizontal,
                         gap: 8, padding: [4, 0, 0, 0])
        // Copy, thumbs-up, thumbs-down icons. 16×16, $textMuted.
        // Appears on hover, not always visible.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Avatar size | 28px | Anchors the left column. Smaller (20px) reads as a dot; larger (36px) competes with content. |
| Gap between avatar and content | 12px | Tight enough to read as connected; loose enough to breathe. |
| AI message fill | none | No card, no border, no background. The AI speaks in prose on the page. |
| Body line-height | 1.65 | Same as editorial-storytelling. The AI's output is reading copy. |
| Font size | 15px | Matches user message. Consistent type scale across both speakers. |

### What generic looks like

```
// WRONG: AI message in a card frame with border
AIMessage=I(thread, {
  type: "frame",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 12, padding: [16, 16],
  fill: "$surface"
})
// A card says "this content is enclosed." AI messages are not enclosed —
// they're contributions to the thread. Cards create a visual back-and-forth
// rhythm that looks like a widget, not a conversation.

// WRONG: AI message body line-height 1.4
AIText=I(message, { lineHeight: 1.4 })
// 1.4 is app UI density (labels, form fields, nav items).
// AI responses contain paragraphs, lists, and explanations. At 1.4,
// a three-paragraph response becomes a wall. 1.65 gives the prose room to breathe.
```

---

## Code block

Code blocks appear inside `AIContent` as distinct visual regions.

```
CodeBlock (frame, fill_container x fit_content, layout: vertical,
            gap: 0, cornerRadius: 8,
            fill: "$codeBlockBg")
├── CodeHeader (frame, fill_container x 32, layout: horizontal,
│               alignItems: center, justifyContent: space_between,
│               padding: [0, 12],
│               fill: transparent)
│   ├── LanguageLabel (text, 12px, $textMuted, $fontMono,
│   │                   content: "python")
│   └── CopyButton (frame, fit_content x 24, layout: horizontal,
│                    alignItems: center, gap: 4, padding: [0, 8])
│       ├── CopyIcon (14×14, $textMuted)
│       └── CopyLabel (text, 12px, $textMuted, content: "Copy code")
└── CodeBody (text, 13px, $textPrimary, $fontMono,
               lineHeight: 1.5, padding: [12, 16],
               width: "fill_container")
```

### What generic looks like

```
// WRONG: code block with accent-colour header bar
CodeHeader=I(codeBlock, {
  fill: "$accent"
})
// The header is metadata (language label + copy button). It should read as
// chrome, not as content. An accent header bar makes the code block look
// like a "card" component from a design system library.

// WRONG: code font size matching body (15px)
CodeBody=I(codeBlock, { fontSize: 15 })
// Monospace at 15px is wide. Code blocks at 13px preserve more characters
// per line and reduce wrapping in typical code snippets (70–90 chars).
```

---

## Composer

The composer is bottom-docked inside `ThreadPanel`, not overlaying the thread. It scrolls away with the thread and snaps to the bottom of the visible panel.

```
ComposerArea (frame, fill_container x fit_content, layout: vertical,
               alignItems: center, padding: [12, 0, 24, 0],
               fill: "$bg")
└── Composer (frame, 720 x fit_content,
               layout: vertical, gap: 0,
               cornerRadius: 12,
               stroke: { color: "$border", thickness: 1 },
               fill: "$bg",
               minHeight: 52, maxHeight: 200)
    ├── ComposerInput (text-input, fill_container x fit_content,
    │                   padding: [14, 48, 14, 16],
    │                   fontSize: 15, $textPrimary, lineHeight: 1.6,
    │                   placeholder: "Message Claude")
    │   // placeholder: 15px, $textSecondary
    │   // Right-padding 48px leaves space for the submit button.
    └── ComposerControls (frame, fill_container x fit_content, layout: horizontal,
                           justifyContent: space_between, padding: [8, 8, 8, 8],
                           alignItems: center)
        ├── AttachButton (frame, 32 x 32, cornerRadius: 8, fill: transparent)
        │   └── AttachIcon (16×16, $textSecondary)
        └── SubmitButton (frame, 32 x 32, cornerRadius: 8,
                           fill: "$accent" when active, "$surface" when empty)
            └── SendIcon (16×16, fill: white when active, $textMuted when empty)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Composer width | 720px | Matches thread content width. The alignment is intentional: input and output share the same column. |
| Composer min-height | 52px | One-line input comfortable height. Grows with content. |
| Composer corner radius | 12px | Same as user bubble. Visual language consistency. |
| Composer border | 1px `$border` | Not a filled background (blends into page) and not a thick stroke (too heavy). |
| Submit button size | 32px | Not 24px (too small a tap target) and not 40px (overweights the control). |
| Submit button state | `$accent` when text present, `$surface` when empty | Empty state communicates "nothing to send." Never disable by opacity alone; change fill instead. |

### What generic looks like

```
// WRONG: composer full-width across the panel (not centred, not width-constrained)
Composer=I(threadPanel, {
  width: "fill_container"
})
// A full-width composer on a 1200px screen is an 1200px input field.
// The composer shares the 720px thread column to maintain visual coherence:
// input goes in, response comes out at the same width.

// WRONG: submit button always same fill regardless of input state
SubmitButton=I(composer, { fill: "$accent" })
// An always-active button communicates "send empty message." The $surface
// fill on empty state is a readability cue, not just aesthetic preference.
```

---

## Streaming state

During streaming, the AI message renders incrementally. The composer shows a stop button.

```
// Streaming cursor — appears at the end of the in-progress AI text
StreamingCursor=I(aiMessage, {
  type: "text", content: "▊",
  fontSize: 15, fill: "$textPrimary",
  // Animate: opacity oscillates 1→0→1 at ~700ms period
})

// Stop button — replaces submit during streaming
StopButton=U(submitButton, {
  fill: "$surface",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 8
  // Contains: 10×10 stop square icon, $textPrimary
})
// Tooltip / label: "Stop generating" on hover
```

### What generic looks like

```
// WRONG: "thinking..." placeholder while AI generates
ThinkingLabel=I(aiMessage, {
  type: "text", content: "Thinking...",
  fill: "$textMuted"
})
// Modern chat interfaces show partial streaming content, not a waiting label.
// "Thinking..." is a 2021 chatbot pattern. Show the cursor with partial text.
```

---

## Empty state

Shown when no conversation is active. Centres prompt suggestions in the thread area.

```
EmptyState (frame, fill_container x fill_container, layout: vertical,
             alignItems: center, justifyContent: center, gap: 32)
├── EmptyHeadline (text, 28px, fontWeight: 600, $textPrimary,
│                   content: "How can I help you today?",
│                   textAlign: "center")
│   // One short phrase. Not a description of the product.
└── SuggestionGrid (frame, fit_content x fit_content, layout: grid,
                     columns: 2, gap: 12)
    └── SuggestionCard × 4
        // Each card: 200 x fit_content, cornerRadius: 10,
        // stroke: { color: "$border", thickness: 1 },
        // padding: [12, 14], fill: "$bg"
        ├── SuggestionTitle (text, 14px, fontWeight: 500, $textPrimary,
        │                     lineHeight: 1.5)
        │   // e.g. "Summarise a document"
        └── SuggestionSubtext (text, 13px, $textSecondary)
            // e.g. "Upload a PDF or paste text"
```

### What generic looks like

```
// WRONG: empty state as a single large icon with "Start a conversation" label
EmptyState=I(thread, {
  type: "frame", layout: "vertical", alignItems: "center",
  justifyContent: "center"
})
EmptyIcon=I(emptyState, {
  type: "frame", width: 64, height: 64
  // a chat bubble icon
})
EmptyLabel=I(emptyState, {
  type: "text", content: "Start a new conversation",
  fill: "$textMuted"
})
// A single icon + label is the empty state for an inbox, not an AI assistant.
// Prompt suggestion cards communicate what the AI can do. They're functional,
// not decorative. The empty icon pattern abandons the user at the moment
// they most need guidance.
```

---

## Microcopy library

### Composer placeholder

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Type your message here... | Message Claude |
| Enter your query | Ask anything |
| Chat with AI | What are you working on? |
| Send a message | (leave blank; the field affordance is obvious) |

### Sidebar controls

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Create new conversation | New chat |
| Start chatting | + (icon only, or "+ New chat") |
| Clear history | Clear conversations |

### Empty state suggestions

Directorial, short, action-first. Not feature descriptions.

| Generic (avoid) | This archetype |
|-----------------|----------------|
| I can help you with writing | Write a product announcement |
| Code assistance available | Debug my Python script |
| Explore AI capabilities | Summarise this article |
| Chat with our AI | Plan a Q3 roadmap |

### Streaming and status

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Processing... | (show streaming cursor with partial content) |
| Generating response | (streaming cursor is sufficient) |
| Cancel | Stop generating |
| Response complete | (no label; the cursor disappears) |

---

## Verification checklist

### Message rendering

- [ ] **AI message has no background fill, no border, no card frame.**
  WHY: A card around the AI's message says "this content is enclosed and separate." AI messages are contributions to a thread, not widgets. The moment a card appears, the surface reads like a support chatbot widget embedded in a page, not a native assistant interface.

- [ ] **User message fill is `$surface` (#EFEEEC), not `$accent`, not white.**
  WHY: `$accent` (blue or brand colour) is the iMessage/WhatsApp pattern. AI assistant surfaces avoid it because: (1) it creates visual competition with accent-coloured links inside AI responses; (2) it communicates "messaging app" not "thinking tool."

- [ ] **User message is right-aligned; AI message is left-aligned.**
  WHY: The positional asymmetry is the fastest signal for "who said what." Without it, a reader scanning the thread has to read text content to orient. That's a layout failure.

- [ ] **AI message body line-height is 1.65, not 1.4.**
  WHY: 1.4 is UI density for labels and form fields. AI responses contain paragraphs and multi-sentence explanations. At 1.4, three paragraphs becomes a wall of text. 1.65 makes the response feel like a document, not a database dump.

### Typography and scale

- [ ] **Font size is 15px for both message types.**
  WHY: 14px is mobile-app density. Acceptable at small screen sizes, but too compressed for desktop reading of longer AI responses. 16px works but 15px is the observed sweet spot in both ChatGPT and Claude.ai at the time of writing.

- [ ] **Code blocks use `$fontMono` at 13px, not 15px.**
  WHY: Monospace at 15px is wide. Code blocks at 13px preserve ~80 characters per line before wrapping, which covers most code snippets. Code at body font size reads as prose-with-different-font, not as a distinct region.

### Layout and structure

- [ ] **Thread content max-width is 680–720px, centred in the panel.**
  WHY: At 1200px panel width with no max-width constraint, message lines exceed 100 characters. That's physically exhausting to read. 720px keeps AI prose at ~75 characters per line, the comfortable reading maximum.

- [ ] **Composer width matches thread content width (720px), centred.**
  WHY: Input and output should share the same column. A full-width composer on a wide screen is an 1100px input box. The visual coherence of "I type here and the response appears at the same width above" is a deliberate design decision in all exemplar products.

- [ ] **Composer minimum height is 48–56px.**
  WHY: Smaller than 48px produces a cramped single-line input that communicates "short questions only." Multi-line thinking needs a composer that visually invites multi-line input.

### Sidebar

- [ ] **Active conversation row uses filled background (`$surfaceActive`), not left border.**
  WHY: Left-border active states belong to analytics and pro-tool nav menus where the sidebar is a persistent navigation hierarchy. Conversation lists are selection lists: you're picking an item, not navigating to a section. Filled background rows read as "selected" without claiming column ownership.

---

## Contrast examples

### Example 1: AI message (correct vs generic)

**Correct:**

```
aiMessage=I(thread, {
  type: "frame", name: "AIMessage",
  layout: "horizontal", gap: 12,
  alignItems: "flex_start",
  width: "fill_container"
  // No fill, no stroke, no cornerRadius
})
avatar=I(aiMessage, {
  type: "frame", name: "AIAvatar",
  width: 28, height: 28, cornerRadius: 14,
  fill: "$accent"
})
messageBody=I(aiMessage, {
  type: "text", name: "AIText",
  fontSize: 15, fill: "$textPrimary",
  fontFamily: "$fontBody", lineHeight: 1.65,
  width: "fill_container"
})
```

Why this is right: no card frame, no background. The AI's response flows directly on the page background. The 28px avatar anchors the left column without competing with the prose. 1.65 line-height makes the response readable, not dense.

**Generic:**

```
aiMessage=I(thread, {
  type: "frame",
  stroke: { color: "$border", thickness: 1 },
  cornerRadius: 12, padding: [16, 16],
  fill: "$surface",
  width: "fill_container"   // WRONG: card frame around AI response
})
messageBody=I(aiMessage, {
  type: "text",
  fontSize: 15, lineHeight: 1.4,   // WRONG: UI density, not reading density
  width: "fill_container"
})
```

Why this is wrong: the card frame encloses the AI's response in a box. At 15px and 1.4 line-height inside a 1px-bordered card, the result is a support chatbot widget, not a thinking-tool interface. The 1.4 line-height turns a three-paragraph response into a rectangle of compressed text.

---

### Example 2: Composer (correct vs generic)

**Correct:**

```
composerArea=I(threadPanel, {
  type: "frame", name: "ComposerArea",
  layout: "vertical", alignItems: "center",
  padding: [12, 0, 24, 0],
  width: "fill_container",
  fill: "$bg"
})
composer=I(composerArea, {
  type: "frame", name: "Composer",
  width: 720,
  cornerRadius: 12,
  stroke: { color: "$border", thickness: 1 },
  minHeight: 52
})
submitBtn=I(composer, {
  type: "frame", name: "SubmitButton",
  width: 32, height: 32, cornerRadius: 8,
  fill: "$surface"   // empty state fill
})
```

Why this is right: 720px composer matches the thread column. Centred via `alignItems: center` on the parent. 1px `$border` stroke gives definition without weight. Submit button at `$surface` correctly communicates "nothing to send."

**Generic:**

```
composer=I(threadPanel, {
  type: "frame",
  width: "fill_container",   // WRONG: full-width input box
  cornerRadius: 4,           // WRONG: near-square is a form field, not a composer
  stroke: { color: "$border", thickness: 2 },  // WRONG: heavy border
  height: 40   // WRONG: fixed height, won't grow with input
})
```

Why this is wrong: full-width places the composer outside the thread column, destroying the input/output alignment. Near-square corners and a 2px border read as a search field. Fixed height at 40px signals "one-line questions only" and visually disconnects the composer from the chat surface above it.
