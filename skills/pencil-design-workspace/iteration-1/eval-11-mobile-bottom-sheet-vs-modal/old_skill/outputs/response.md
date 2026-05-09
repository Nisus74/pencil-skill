# Designing the iOS compose flow in Pencil

You've asked for three connected surfaces inside an iOS app's compose flow: a filter selection sheet, an attachments picker, and a destructive "discard draft" confirmation. They're three different overlay shapes, and the choice of shape carries most of the design intent. Before I open `batch_design`, I want to walk through how I'd approach this in your `.pen`, what I'd verify, and the tradeoffs I'm making.

## Skill references I consulted, and why

- **`SKILL.md`**: the discipline rules (naming, context, components-first, themes, responsive, accessibility) and the default workflow. Mobile is one of the canonical breakpoints (390 × 844). The "user asks for a multi-step form, wizard, signup, onboarding, or any flow that crosses screens" branch sends me to flows.md, and the destructive-action signal also sends me there.
- **`references/flows.md`**: owns modal vs page vs sheet vs popover, validation timing, hard vs soft confirmation, optimistic UI, plausible content. Compose-flow design lives squarely here.
- **`assets/design-system/mobile.md`**: owns the iOS-specific bits like tab bar, sheets with drag handles, safe-area insets, gestures (including iOS edge-swipe back), keyboard handling, haptics, action sheets, alerts with destructive actions. This is the file the design will hinge on.
- **`references/states.md`**: owns the per-component state matrix and the soft-vs-hard confirmation distinction at the component level. The "discard draft" alert needs default, pressed, and disabled at minimum, plus the destructive variant treatment.
- **`references/component-anatomy.md`**: needed before I instantiate any existing sheet or alert components from your `.lib.pen`. I'll be reading components, not rebuilding them.
- **`assets/design-system/voice.md`** § Confirmations & destructive actions: copy template for the discard alert (name what's destroyed; specific verb on the destructive button).

I'm not loading `references/modern-patterns.md`, the `references/accessibility.md` deep dive, or the platform-specific tool-name files. They aren't on the critical path for this task.

## Pre-work I'd do before any design op

### 1. Detect host

```
get_editor_state({ include_schema: false })
```

If it errors with `transport not connected`, I stop and tell you to open the Pencil desktop app or IDE extension. If it succeeds, I note which `.pen` is open, what's selected, and whether the document already has imports.

### 2. Locate context

I'd check the project filesystem for `design-system/` (a directory listing, not via MCP). Three things I'm hoping to find:

- `design-system/design-system.md`: points to the project's `.lib.pen` and names the icon library.
- `design-system/mobile.md`: confirms the project actually ships mobile (otherwise the `mobile.md` template wouldn't be scaffolded). If it's missing and the project shows mobile signals (`react-native`, `expo`, `Podfile`, an iOS folder), I'd offer to scaffold it once.
- `design-system/voice.md`: confirms the destructive-confirmation copy template the project uses.

If `design-system/` doesn't exist and this is real project work, I'd offer to scaffold the core 12 templates plus the optional `mobile.md` based on project signals. One offer per session.

### 3. Load guidelines and inventory components

```
get_guidelines({ category: "Mobile App" })
```

That's the relevant category for an iOS surface. If the project also targets a web counterpart, I'd not load Web App now; I can pick it up later if needed.

Then the components inventory, which is the most important pre-work for this task:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

…against the open document, then again with `filePath` set against each `.lib.pen` listed in `imports`.

I'm specifically looking for:

- A `Sheet` or `BottomSheet` component (with a drag handle, safe-area-aware bottom padding, and ideally a header slot).
- A `FilterRow` / `SelectionRow` / `Checkbox` / `Radio` component for the filter list.
- An `Attachment` or `AttachmentTile` component for the picker grid.
- An `Alert` or `Dialog` component with a destructive button variant.
- A `Button` component with at least default, pressed, disabled, and loading states, and a `destructive` variant.
- An `Icon` ref that resolves against the project's icon font (Lucide, SF Symbols, Phosphor, whatever `design-system.md` declares).

If any of these exist, I instantiate via `ref` rather than rebuild. If a `Sheet` exists but doesn't have a destructive variant, I read the component using `component-anatomy.md`'s pattern:

```
batch_get({ nodeIds: ["Sheet"], readDepth: 4 })
```

…then look for slot frames, named children, and the `theme` axes (specifically a `state` axis I might activate via `theme: { state: "destructive" }`). I build from primitives only when nothing matches and the gap is real, not a naming preference.

### 4. Check existing canvas

If there are already top-level frames on the canvas (likely; an existing iOS project will have other screens), I'd call:

```
find_empty_space_on_canvas({ width: 1300, height: 900 })
```

…to find clear space for the three new sibling frames. Width 1300 leaves room for three 390-wide frames laid horizontally with gaps. I pass the returned `x`/`y` on the outermost frame in the first `batch_design` call.

### 5. Get variables

```
get_variables()
```

Per the discipline rule, I never re-declare existing tokens. If the project already has a `surface` / `surfaceMuted` / `danger` / `textPrimary` / `textInverse` set, I use them as-is. If specific tokens are missing (e.g. no `dangerMuted` for the destructive button's pressed state), I'd add only those via `set_variables({ replace: false })`.

## Design plan

A one-line atmosphere first, per SKILL.md: **balanced, symmetric, static.** This is utility UI inside a productivity app; flashy motion would feel wrong, but airy reads thin on a 390-wide phone. Balanced gives me comfortable padding without empty space.

Three sibling top-level frames, each 390 × 844, lined up horizontally so reviewers can read the flow left to right. Names follow the existing convention from your `.lib.pen` if it has one; otherwise:

```
Compose_FilterSheet
Compose_AttachmentsPicker
Compose_DiscardAlert
```

Each frame includes:

- A 47pt `SafeAreaTop` and 34pt `SafeAreaBottom` (per `mobile.md`). Status bar content shown for reviewer context, not as decoration.
- A dimmed scrim layer behind the surface (the parent compose screen showing through at low opacity), because all three are interruptive overlays. Scrim uses a `$scrim` token (semi-transparent black) that I'd add if missing.

### Frame 1: `Compose_FilterSheet`

This is a **bottom sheet**, not a modal. The reasoning:

> From `flows.md`'s decision table: *"Sheet: drilldown that retains context. Filters, share, secondary edit. Mobile by default."* And from `mobile.md`: *"Sheet: focused subtask, optionally dismissible by drag. Use for filters."*

A modal centered overlay would be wrong here. The user is composing; the filter is a contextual choice, not an interruption. The user's existing draft must remain visible above the sheet line.

Anatomy:

```
Compose_FilterSheet (390 × 844)
├── Scrim (full bleed, 50% opacity black)
├── ParentScreenPeek (top portion, draft visible behind scrim)
├── SheetSurface (anchored bottom, fills horizontal, ~520 tall)
│   ├── DragHandle (36 × 5, $textMuted at low opacity, centered top)
│   ├── SheetHeader
│   │   ├── Title ("Filter")
│   │   └── DoneButton (right-aligned, primary style)
│   ├── FilterList (vertical stack)
│   │   ├── FilterRow × ~6 (each: label + selected check)
│   │   └── ...
│   └── SafeAreaBottomPad (34, inside the sheet so the home indicator doesn't sit on a row)
```

Notes I'd encode in `context` strings during the `batch_design` call:

- The sheet root: *"Bottom sheet. Dismissible by drag-down or tapping scrim. iOS edge-swipe-back returns to compose without losing draft. Sheet height is content-driven up to ~70% viewport; clamps with internal scroll if filter list grows."*
- `DoneButton`: *"Commits the selection and dismisses. Selection is single-pick by default; if multi-pick, swap to a 'Apply' verb and surface a count."*
- Each `FilterRow`: *"Row tap toggles selection. Selected state shows a check icon, NOT just a colour change (color-not-only-signal rule)."* Plus haptic note: light selection-rigid haptic per `mobile.md`'s haptics table.

Plausible filter labels from `flows.md`'s plausible-content guidance: not "Filter 1, Filter 2". Use shapes that match the host product (if it's an inbox: Unread, Starred, From people, From channels, Has attachments, Last 7 days). I'd ask if the product domain isn't obvious from the codebase rather than invent.

Touch targets: each row is 44pt minimum. Tap area extends the full sheet width with the visible content centred in the safe gutters.

### Frame 2: `Compose_AttachmentsPicker`

Also a **bottom sheet**, taller than the filter sheet. This is the iOS share-sheet idiom.

Anatomy:

```
Compose_AttachmentsPicker (390 × 844)
├── Scrim
├── SheetSurface (~660 tall, taller for the grid)
│   ├── DragHandle
│   ├── SheetHeader
│   │   ├── Title ("Add to draft")
│   │   └── CloseIconButton (X top-left per iOS convention, or top-right Done; mobile.md says pick one and stay consistent with the rest of the app)
│   ├── SourceSegmentedControl (Photos / Files / Camera / Link)
│   ├── ContentRegion (varies per source)
│   │   └── For Photos: 3-column grid of thumbnails, each 110 × 110, gap 4
│   │       Recent photos render with G(node, "ai", "<prompt>") rather than gray rectangles
│   ├── PermissionsPrompt (conditional, only when user has photo access set to "Selected Photos")
│   │   └── Banner: "Showing 12 selected photos. [Manage] in Settings."
│   ├── SelectionFooter (sticky bottom, only visible when ≥1 selected)
│   │   ├── "{N} selected" label
│   │   └── AddButton (primary, "Add 3 photos")
│   └── SafeAreaBottomPad
```

Several state notes:

- I'd design at least three states for this picker as sibling variants OR via a state axis on the main surface:
  - **Default** (no selection; `SelectionFooter` hidden, `AddButton` would render disabled if shown).
  - **With selection** (footer visible, count and verb dynamic).
  - **Empty source** (e.g. user picks Files, no recent files; per `states.md`'s in-component empty taxonomy, a single muted line *"No recent files."* with a CTA to browse).
  - **Permissions denied** (per `states.md`'s no-permission empty: *"Photos isn't allowed for this app. Open Settings to allow access."* with a path forward).

- **Async loading**: when the user taps a photo, an optimistic check appears immediately. From `flows.md` § Optimistic UI: this is high-confidence (selection is local, no server). The selection is reversible by tapping again. So optimistic without rollback indicators.

- **Source segmented control** uses the project's `Segment` component if it exists. If not, this is the kind of pattern I'd surface to you: *"This looks reusable across other pickers. Should I add `Segment` to your `.lib.pen`?"*

Plausible content for Photos: I'd use `G(thumbnail, "ai", "casual phone photo, slightly imperfect framing, varied subjects")` or `G(thumbnail, "unsplash", "everyday objects")` depending on the project's `imagery.md`. Twelve thumbnails in three rows of four; I avoid identical-aspect stock that all looks like the same photographer.

### Frame 3: `Compose_DiscardAlert`

This is a **modal alert**, not a sheet. The reasoning:

> From `flows.md`: *"Modal: small, focused, hard interruption. Confirmation, single-form-edit. The user must complete or dismiss it before continuing."*

Discarding a draft is exactly that: a finite-outcome interruption with two paths (Discard, Keep). It also matches `mobile.md`'s "alert with destructive action" row: red text on the confirm button on iOS.

Anatomy follows the iOS native action-sheet idiom (UIAlertController with `.alert` style), not a generic web modal:

```
Compose_DiscardAlert (390 × 844)
├── Scrim (heavier than the sheets, ~60% opacity, since this is a hard interruption)
├── ParentScreenBlurred (the compose screen behind, blurred per iOS convention)
├── AlertCard (centered, ~270 wide, content-driven height)
│   ├── AlertHeader
│   │   ├── Title (text-bold-17, centered): "Discard draft?"
│   │   └── Body (text-regular-13, centered, $textMuted): "You have unsaved changes. This can't be undone."
│   └── AlertActions (vertical or horizontal stack; see below)
│       ├── DiscardButton (destructive variant: text in $danger, NOT a filled red button on iOS. iOS alerts use coloured text, not coloured fill.)
│       └── KeepButton (default variant: text in $primary, "Keep editing")
```

Critical iOS-specific notes I'd capture in context:

- **Button order on iOS alerts**: destructive on top OR on the right of a horizontal pair, depending on count. For two actions, horizontal with Cancel-equivalent (Keep editing) on the LEFT, destructive on the RIGHT, separated by a 0.5pt divider. From `mobile.md`: *"Modal dismiss: 'Cancel' left, 'Done'/primary right."* The destructive treatment overrides the "Done = primary" colour, but not the position.
- **Why text-coloured, not filled**: iOS HIG. A filled red button reads as Material/Android. The Pencil convention should match the design's platform.
- **Hard confirmation rationale**, per `flows.md`: discarding work is "irreversible data loss" by definition. No undo toast pattern works here, because the moment the user hits Discard, the draft text is gone. So hard confirmation is correct.
- **Verb on the destructive button**: "Discard draft", not "Discard" alone. From `voice.md` and `flows.md`: *"A specific verb tied to the outcome."*
- **Haptic per `mobile.md`**: medium impact when the user confirms the destructive action.

I'd consider but reject **typed confirmation** (the "type 'discard' to confirm" pattern). That's reserved for org-deletion-tier actions; a single draft doesn't warrant the friction.

### What I'm NOT designing

- The compose screen itself (the editor where the user is typing). The brief is the three overlay surfaces. If you want the parent screen too, I'd want to know whether you've already designed it.
- The success state after discard (the user lands back on… what? Inbox? Drafts list?). That's a navigation decision I'd ask about rather than guess.
- Tablet or desktop variants. iOS-only per the brief.

## Execution plan: one or two `batch_design` calls

I'd batch all three frames into a single call if the op count stays at or below 25. Rough op count:

- 3 outermost frames + 3 scrims + 3 sheet/alert surfaces = 9 ops.
- Sheet header + drag handle for each sheet = ~4 ops.
- ~6 filter rows (if I use `C` to copy a base row and `U` only the label and selected state, that's ~7 ops). Better: instantiate via existing `FilterRow` component if it exists in your `.lib.pen`, which collapses each row to one ref op.
- Attachments grid: 12 thumbnail refs.
- Alert card + 2 buttons.

Ballpark: 30 to 35 ops if I rebuild rows from primitives, 18 to 22 if I instantiate from existing components. Either way I'd split into two calls. **Call 1** is the three top-level frames with their scaffolds (safe areas, scrims, surfaces, headers). **Call 2** fills the content (rows, grid items, alert buttons). Splitting at that boundary means I can `snapshot_layout` between them and fix structural issues cheaply before content goes in.

Each `I` op gets a `name` (PascalCase, role-bearing) and a `context` (one sentence per the rule). I prefer the `foo=I("parent", {...})` binding pattern so call 2 can reference what call 1 created.

For colours: every fill comes from a `$variable` so light/dark mode resolve correctly. I'd never bind raw `#000000` to the alert text or `#FF3B30` to the destructive button. If the project's `tokens.md` doesn't declare `$danger`, I'd add it (with both light and dark values) before the destructive frame goes in.

## Verification ladder I'd walk

Per SKILL.md, screenshots are expensive. The ladder for this task:

1. **`batch_design` response** — confirms ops landed.
2. **`snapshot_layout(parentId, maxDepth: 3)`** on each of the three top-level frames after call 1. I'm checking that:
   - The sheet anchors to the bottom (y position close to 844 minus sheet height).
   - The alert card is centred (x offset = (390 - 270) / 2 = 60).
   - The scrim covers the full 390 × 844.
   - Drag handles are 36 × 5 and centred horizontally.
   - Touch targets on filter rows are ≥ 44pt.
3. **`batch_get`** on the destructive button after call 2 to verify:
   - `fill` resolves to a transparent or surface-coloured background.
   - The label `color` resolves to `$danger`, NOT a raw hex.
   - The button's parent has the iOS-style 0.5pt divider above it.
4. **`get_screenshot`** on the most specific node — once, scoped to the alert card, not the whole compose flow. The alert is the most visually risky element (destructive treatment, type contrast, the iOS-specific "text not fill" treatment). For the two sheets, the structural snapshot plus a `batch_get` on a couple of filter rows should be enough; I'd skip a screenshot unless something on the snapshot looks off.

If the project has both light and dark tokens correctly bound, I do **not** screenshot dark mode. The variable system guarantees parity. I'd only re-screenshot if I see a raw hex anywhere in the `batch_get` results.

Total expected screenshots: **1**. The pre-skill reflex would have produced 4 (one per frame, one final), all of which would have wasted tokens proving things the structural snapshot already proved.

## What I'd flag before declaring done

The state-coverage and accessibility checks from SKILL.md's discipline rules:

- **Filter sheet states**: default, with-selection, scrolled (long list), in-component empty (rare for filters but worth a thought), focus state on the row (an iOS focus ring is unusual but VoiceOver focus is real and the design needs to handle it).
- **Attachments picker states**: default, no-selection-yet, selection-active, empty source (no recent files), permissions-denied, loading (initial photo grid load — skeleton tiles per `states.md`).
- **Discard alert states**: default, pressed (light dim on the row tapped), and the brief moment between tap-and-dismiss (no explicit loading; alerts dismiss immediately on tap).
- **Contrast**: alert title and body against the alert card surface ≥ 4.5:1 in both modes. Destructive button text against the alert card ≥ 3:1 (it's a UI component per WCAG, not body text).
- **Hit targets**: filter rows ≥ 44, attachment thumbnails ≥ 44 (110 × 110 is fine), alert buttons ≥ 44pt tall.
- **Color is never the only signal**: filter selection has a check icon, not just a colour change. Destructive button is paired with the explicit verb "Discard draft", not just red colour.
- **Names map to roles**: `DiscardButton`, `KeepButton`, `FilterRow_Selected`, `AttachmentTile`. Not `Button1`, `RedButton`.
- **Keyboard / VoiceOver focus**: documented in `context` even if not visually styled, since iOS handles the visual ring system-side. The order is: drag handle (skip), header title, list rows top-to-bottom, Done button.

If any of those fail, I fix them in a follow-up `U` op call before reporting done — not as a TODO list back to you.

## Two open questions before I'd start

1. **What goes inside the filter list?** Six labels appropriate to the host product. If this is an email client, an SMS app, a photo manager, or a notes app changes the answer. I can guess from the codebase, but I'd rather ask once.
2. **Single-select or multi-select filters?** Changes the row affordance (radio vs checkbox), the verb on the Done button ("Done" vs "Apply (3)"), and whether the sheet auto-dismisses on tap.

Tell me the product domain and the select-mode, and I'll run the workflow above. I'd expect to land all three frames in two `batch_design` calls and one screenshot, total.
