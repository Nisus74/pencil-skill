# Cmd+K command palette — visual design and keyboard interactions

Before any ops, here's how I'd approach this in Pencil and what the design needs to cover. I'll structure this the way the `pencil-design` skill's default workflow expects: detect host, locate context, load guidelines + inventory components, plan, then execute.

## References I consulted (and why)

- **`SKILL.md`** — for the default workflow, discipline rules (naming, context, components-first, themes, responsive, accessibility), the verification ladder, and the aesthetic anti-patterns to avoid (no Inter, no neon, no pure `#000` / `#FFF`).
- **`references/component-anatomy.md`** — a command palette is composed of nested parts (input, results list, item, footer hints). I want to model it as one reusable component with descendants I can override and a `state` theme axis for hover/selected/loading/empty results.
- **`references/states.md`** — palettes have many states: default empty input, typing, async loading, no-results, error, keyboard-focused row, item hover. The matrix and the empty-state taxonomy (specifically *no-results* vs *first-use*) shape the design.
- **`references/accessibility.md`** — keyboard navigation is the entire point of a Cmd+K palette. ARIA roles (combobox / listbox / option), focus trap inside the overlay, focus-ring rules, hit-target sizes, RTL flip considerations.
- **`references/flows.md`** — modal-vs-page-vs-sheet decision, browser history handling for an overlay (use `replaceState` so Back closes the palette, doesn't navigate away), validation/async timing for search input.
- **`references/modern-patterns.md`** — perceived-performance patterns (skeleton rows, prefetch on hover/keyboard-arrow, debounced async search), and the dated defaults to avoid (no glassmorphism overdose).

I did not load `references/batch-design-grammar.md` or `references/mcp-tools.md` for this response since I'm describing the design rather than executing ops, but I'd load both before any `batch_design` call.

## Step 1 — Detect host (would do, can't here)

I'd call:

```
get_editor_state({ include_schema: false })
```

Expected response shape: a JSON envelope with the open document path, the current selection, the schema version, and the document's `imports`. If it errors with `transport not connected to app: desktop`, I'd stop and tell the user to open the Pencil app or IDE extension. I'm assuming for this response that it succeeds and the user has an app `.pen` open.

## Step 2 — Locate context

Three things I'd capture from the editor state:

1. Which `.pen` file is open (likely an `app.pen` or similar).
2. What's selected (probably nothing relevant; the palette is a new top-level overlay).
3. Whether `design-system/` exists in the project root, and whether the document has an imported `.lib.pen`.

I'd check the filesystem for `./design-system/` (directory listing, not MCP). If `design-system/design-system.md` exists, I'd read it for the icon library, the `.lib.pen` path, and any palette-specific guidance. If the doc imports a library, I'd note its path.

## Step 3 — Load guidelines + inventory components

Two parallel calls:

```
get_guidelines()                         # see which categories exist for this doc
get_variables()                          # token inventory before I touch any colors
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })       # in-doc components
batch_get({ filePath: "<lib path>", patterns: [{ reusable: true }], readDepth: 2 })  # lib components
```

What I'd look for in the inventory:

- An existing `CommandPalette`, `Combobox`, `Modal`, or `SearchInput` component. If any of these exist, I instantiate them with `ref` rather than building from primitives.
- An `Input` or `TextField` I can reuse as the palette's search input.
- A `KeyHint` / `Kbd` / `Keycap` component for the inline shortcut hints (`↑` `↓` `↵` `esc`). These are the bits authors most often hand-roll badly; reuse if it exists.
- An `Icon` or `IconButton` component (and which icon library — Lucide / Phosphor / Material Symbols).
- An `Overlay` / `Backdrop` / `Modal` component for the scrim and focus trap. If we have `Modal`, the palette is "a Modal with a search input and result list inside".

Also `get_guidelines("Web App")` for the web-app conventions (and `Tailwind` if the project uses it for code export). The skill calls these out by category in `references/mcp-tools.md`.

## Step 4 — Plan

**Vibe (per `SKILL.md` § Name the atmosphere):** Dense, symmetric, fluid. Command palettes live or die on density and snappy motion; they're symmetric by nature (centered overlay), and every interaction should feel responsive.

**Surface decision (from `flows.md`):** This is a *modal* overlay, not a page or a sheet. Reasons:

- Hard interruption — when the palette is open, nothing else is interactable.
- Not deep-linkable; it shouldn't be in browser history (use `replaceState`).
- Closes on `Esc` or click-outside.
- Opens via global `Cmd+K` (macOS) / `Ctrl+K` (Windows/Linux). Note the OS in `context`.

**Component model.** One reusable `CommandPalette` component, structured like this:

```
CommandPalette (reusable: true, theme: { state: "default" })
├── Backdrop                   (semi-opaque scrim; rgba surface, NOT pure black)
└── PaletteCard                (centered, max-width 640, top-anchored ~120px from top)
    ├── SearchRow              (horizontal layout)
    │   ├── SearchIcon         (lucide "search", 20px, $textMuted)
    │   ├── SearchInput        (placeholder: "Type a command or search…")
    │   └── CloseHint          (Kbd "esc", subtle, hides on mobile)
    ├── Divider                (1px $border)
    ├── ResultsRegion          (slot — fills with one of: ResultsList / EmptyState / LoadingSkeleton / ErrorBlock)
    └── FooterRow              (horizontal layout, $textXs $textMuted)
        ├── KeyHintGroup_Navigate ("↑ ↓ to navigate")
        ├── KeyHintGroup_Select  ("↵ to select")
        └── KeyHintGroup_Close   ("esc to close")
```

`ResultsList` is itself composed of:

```
ResultsList
├── Group (optional, repeatable)
│   ├── GroupHeader (e.g. "Suggestions", "Pages", "Actions", "Recent")
│   └── ResultItem (repeatable, theme: { state: "default" | "selected" | "hover" | "disabled" })
│       ├── LeadingIcon       (lucide icon, 16px, $textMuted)
│       ├── Label             (1 line, $textBase, $textPrimary, truncate)
│       ├── Subtitle          (optional, 1 line, $textSm, $textMuted)
│       ├── Spacer
│       └── Trailing          (slot — Kbd shortcut OR badge OR submenu chevron)
```

I'd encode interactive states with the `state` theme axis (default / hover / selected / disabled) so the design can show the keyboard-selected row distinctly from a hover row — the two look different in a good palette and a screenshot needs both visible.

**Top-level frames I'd add to the canvas** (per `find_empty_space_on_canvas` first if the canvas is crowded):

1. `CommandPalette_Default` — empty input, recent/suggested actions visible.
2. `CommandPalette_Typing` — input has text, results filtered, top result highlighted.
3. `CommandPalette_NoResults` — input has text, no matches.
4. `CommandPalette_Loading` — async results pending, skeleton rows.
5. `CommandPalette_Disabled` — one item disabled (greyed, with reason).
6. (Optional) `CommandPalette_Mobile` — full-screen takeover variant, since a 640px modal doesn't fit on a 390px viewport.

These ship as siblings. Each is the same `CommandPalette` ref with different `descendants` and `theme: { state: ... }` overrides.

## Step 5 — Execute (what I'd send)

I'd send this as one or two `batch_design` calls (≤ 25 ops each).

**Call 1 — token bootstrap (only if `get_variables()` came back empty for these names):**

```
U("doc", { themes: { mode: ["light","dark"], state: ["default","hover","selected","disabled","loading"] } })
set_variables({ variables: {
  paletteSurface:     { type: "color", value: [
    { value: "#FFFFFFE6", theme: { mode: "light" } },   // ~90% opaque off-white
    { value: "#0F141AE6", theme: { mode: "dark"  } }    // ~90% opaque near-black
  ]},
  paletteBorder:      { type: "color", value: [
    { value: "#E4E4E7", theme: { mode: "light" } },
    { value: "#27272A", theme: { mode: "dark"  } }
  ]},
  paletteRowSelected: { type: "color", value: [
    { value: "#F4F4F5", theme: { mode: "light" } },
    { value: "#1F242B", theme: { mode: "dark"  } }
  ]},
  scrim:              { type: "color", value: [
    { value: "#0B11178C", theme: { mode: "light" } },   // ~55% opacity
    { value: "#0008",    theme: { mode: "dark"  } }
  ]},
  // Reuse $textPrimary, $textMuted, $border, $focusRing, $accent if they already exist.
}, replace: false })
```

I'd skip any variable that `get_variables()` reports already exists. The `replace: false` merge default still overwrites *keys you pass*, so passing none of the existing keys is the only safe bootstrap.

**Call 2 — build the component and the variant frames:**

Roughly: `palette = I("doc", { type: "frame", name: "CommandPalette", reusable: true, ... })`, then a chain of `I(palette, ...)` ops binding each child. Then `I("doc", { type: "ref", ref: palette, name: "CommandPalette_Default", x, y, ... })` for each variant frame, with `descendants` driving their differences and `theme: { state: ... }` selecting the row state.

For the "selected" row in the typing variant:

```
{
  type: "ref", ref: "CommandPalette",
  theme: { state: "default" },
  descendants: {
    "PaletteCard/ResultsRegion": {
      children: [ /* ResultsList instance with one item set to state: "selected" */ ]
    },
    "PaletteCard/SearchRow/SearchInput": { content: "open settings" }
  }
}
```

`x, y` come from `find_empty_space_on_canvas` if the canvas already has frames.

## Visual design — the specifics

These are the defaults; a project's `tokens.md` overrides any of them.

### Surface and overlay

- **Scrim (`$scrim`).** Semi-opaque dark layer covering the whole viewport. About 55% opacity over the page in light mode, ~50% in dark. **Not pure black** — that's an AI tell from `SKILL.md` § Anti-patterns. Use a token resolving to a deep zinc.
- **Palette card.** Max width 640px on desktop, 90vw on tablet, full-screen on mobile. Anchored ~15% from the top of the viewport (so the user looks down at it, not up — feels less intrusive than centered). Corner radius 12px. Border 1px `$paletteBorder`. Shadow: a real elevation token (`$shadow-xl` from `elevation.md`), not a neon glow. In dark mode the shadow is replaced/augmented by a 1px subtle inner border per `elevation.md` conventions.
- **Background blur.** *Optional* — one place for glassmorphism is fine if `tokens.md` allows. If used: `backdrop-filter: blur(20px)` on the palette card, and ship a `prefers-reduced-transparency` opaque fallback (per `accessibility.md`). Don't blur both the scrim and the card.

### Search row

- Height 52px. The search icon sits 16px from the left, the input fills the remainder, and a small `esc` Kbd hint sits 16px from the right (hidden under 480px viewport).
- Input has no border and no fill — it inherits the card surface. Placeholder uses `$textMuted`.
- Font: the project's UI font from `tokens.md` (default `Geist` per `SKILL.md`'s typography defaults; never `Inter`). Body size — `$textBase` (16px), so the input doesn't feel small.
- The search icon swaps to a small spinner when async results are in flight (loading state).

### Results region

- A scrollable area with `max-height: 400px` (or `60vh` on mobile). Internal scrollbar styled per platform conventions. Auto-layout vertical, no gap between items (rows manage their own padding).
- **Group headers** — uppercase `$textXs`, `$textMuted`, 8px top padding, 12px left padding. Sticky to the top of the scroll area as you scroll past their group.
- **Row anatomy** — 40px tall. 12px horizontal padding. 12px gap between leading icon, label/subtitle, and trailing. Label `$textBase`, subtitle (if present) `$textSm $textMuted` on the same row, comma-separated or right-aligned.
- **Row states (the ones the screenshot must cover):**
  - *Default* — transparent fill.
  - *Hover* — `$paletteRowSelected` fill; cursor pointer. **Not** the same color as keyboard-selected — distinct so a user with a mouse mid-keyboard-nav can tell which one wins.
  - *Selected* (keyboard) — `$paletteRowSelected` fill **plus** a 2px inset focus accent on the leading edge in `$focusRing`. This is the row that activates on `Enter`.
  - *Disabled* — opacity 0.5 (not lower, per `states.md`'s 3:1 contrast rule). Tooltip on hover explains why.
- **Trailing slot** — typically a `Kbd` showing the action's global shortcut (e.g. `⌘K`), a colored badge for "new" / "beta", or a chevron `›` if the item opens a sub-palette.

### Empty / no-results state

Per the empty-state taxonomy in `states.md`, this is *no-results* (the palette has data, just none matching) — **not** *first-use*. Copy lead is specific:

```
EmptyState (centered in ResultsRegion)
├── Icon            (lucide "search-x", 24px, $textMuted)
├── Title           ("No matches for "open settings"" — quote the user's query)
└── Hint            ("Try a different search, or press ↵ to ask AI." if AI fallback exists)
```

Single CTA at most. Don't stack "Create new" + "Browse all" + "Try AI" — pick the most useful one.

### Loading state

Per `states.md` and `modern-patterns.md`: skeleton rows, not a centered spinner. Three rows of placeholder shapes matching the row dimensions, with the 1.4s shimmer per `motion.md`. The search icon also swaps to a spinner so the user knows the input is what's pending.

### Footer

- 36px tall, top divider 1px `$paletteBorder`, horizontal padding 12px. Background uses a subtle `$surfaceMuted` tint so the footer reads as chrome, not content.
- Three groups, separated by 16px: navigate (`↑` `↓`), select (`↵`), close (`esc`). Each group is `<Kbd> <label>`. Hide the footer on mobile (the keys aren't there).

### Aesthetic defaults to honor

- One accent only — `$focusRing` and the leading-edge selected indicator. No multi-hue gradients on rows.
- No emojis in production palette items unless `voice.md` explicitly opts in.
- No neon glow shadows on the card.
- Plausible content in mocks — real action names from the user's app, not "Action 1 / Action 2 / Lorem ipsum". Per `flows.md` § Plausible content.

## Keyboard interactions — the spec

This is the part that matters most. Document every binding in the `CommandPalette` component's `context` so the engineer ships the actual handlers.

### Open / close

| Key | Behavior |
|---|---|
| `Cmd+K` (macOS) / `Ctrl+K` (Win/Linux) | Open the palette. Focus moves to the search input. Toggle behavior: pressing again while open closes it. |
| `Esc` | Close the palette. Focus returns to the element that had focus before opening. |
| Click outside the card | Close (same effect as `Esc`). |
| `Cmd+K` with text selected | Optional: pre-fill the search input with the selection (a useful affordance for "quick lookup" palettes). |

Browser-history rule: use `replaceState`, not `pushState`, so browser Back doesn't surprise the user (per `flows.md` § Back-stack).

### Navigation within the results

| Key | Behavior |
|---|---|
| `↓` | Move selection to the next visible row. Wrap at the bottom to the first row. Skip disabled rows (don't let keyboard land on a disabled item). |
| `↑` | Move selection to the previous visible row. Wrap at the top. |
| `Tab` | **Same as `↓`** in a typical palette — Tab does not exit the palette while it's open (the modal is a focus trap per `accessibility.md`). |
| `Shift+Tab` | Same as `↑`. |
| `PageDown` / `PageUp` | Jump by a viewport's worth of rows (~10 by default). Optional but expected on long lists. |
| `Home` / `End` | Jump to the first / last result. |
| `Enter` (`↵`) | Activate the currently selected row. |
| `Cmd+Enter` | Activate in a "secondary" mode if the action supports one — typically "open in new tab/window" for navigation results. Document on the action; don't surprise the user. |

The selected row must always be scrolled into view as the user moves through the list — `scrollIntoView({ block: "nearest" })` semantics.

### Modes / scoping

If the palette supports scoped modes (e.g. `>` for commands, `#` for tags, `@` for users — the GitHub palette pattern):

| Key | Behavior |
|---|---|
| Type `>` at start of empty input | Switch to "commands" mode. Shows a small mode chip in the input row. |
| Type `#` at start of empty input | Switch to "tags" mode (or whatever the project defines). |
| `Backspace` at the start of input with mode chip | Remove the mode chip, return to default. |
| `Esc` while mode is active and input has text | First press clears the input but keeps the mode; second press closes the palette. (Two-stage escape — a courtesy, not strictly required.) |

Document each mode in `voice.md` so the prefix conventions are project-wide.

### Search input itself

| Key | Behavior |
|---|---|
| Type | Filter results live. Sync filter for in-memory results; debounce 200–400ms for async results. |
| `Cmd+A` | Select all text in the input (don't intercept; let the browser handle). |
| `Cmd+Backspace` | Clear the input. |
| Pasting | Allow. Trim leading/trailing whitespace before filtering. |

### Focus management (accessibility — `accessibility.md` § Modal focus traps)

- Opening the palette moves focus to the search input.
- Tab and Shift+Tab cycle within the palette, never out. The footer hint chips are not focusable (decorative only — they're shortcuts shown for discovery).
- The selected row is communicated to screen readers via `aria-activedescendant` on the input (the input keeps focus; the listbox tracks the active option). This is the standard combobox pattern.
- Closing returns focus to the element that opened it.
- The palette has `role="dialog"` with `aria-modal="true"`. The input has `role="combobox" aria-expanded="true" aria-controls="<results-id>"`. The results region has `role="listbox"`. Each row has `role="option"`.
- I'd note all of this in the `CommandPalette` component's `context` — it's not a visual property, but it tells the engineer exactly what to ship.

### Per-item shortcuts (the global type)

The palette is also the discovery surface for the app's *global* shortcuts. Each result that has a global shortcut (`Cmd+S` to save, `Cmd+,` for settings, etc.) shows it on the row's trailing slot. Two consequences:

- The user can learn the shortcut by hovering the row (no extra interaction needed).
- The shortcut should also work *outside* the palette — pressing `Cmd+,` on the page with no palette open should activate the same action. Don't ship a palette-only shortcut; ship the shortcut everywhere and *display* it in the palette.

### Mobile fallback

`Cmd+K` doesn't exist on mobile. Surface the palette via:

- A search icon in the top-bar nav.
- A floating action / quick-launch button in the corner.
- A pull-down gesture from the top (if the project's mobile pattern uses it).

When opened on mobile, the palette is a full-screen takeover, the system keyboard is summoned automatically, and the footer hint row is hidden (no physical keys to hint at). Cancel returns to the previous screen.

## Step 6 — Verify

The verification ladder I'd walk after the `batch_design` call:

1. **Server response** — confirm all ops succeeded.
2. **`snapshot_layout(parentId: "<CommandPalette>", maxDepth: 3)`** — confirm the card is 640px wide, the search row is 52px tall, the results region scrolls, the footer is 36px. Numbers confirm structure cheaply.
3. **`batch_get({ nodeIds: ["<SearchInput>", "<selected ResultItem>", "<EmptyState/Title>"] })`** — confirm the input's placeholder is the right string, the selected row's `theme: { state: "selected" }` applied, the empty-state title quotes the user's query token (a common bug is forgetting the dynamic interpolation marker).
4. **`get_screenshot(nodeId: "<CommandPalette_NoResults>")`** — *one* screenshot, scoped to the worst-case state per `states.md` § Verification. The no-results frame exposes: contrast of muted text on the palette surface, the focus ring on the disabled state, footer chip legibility, scrim opacity. If this state holds up, the others almost certainly do.

I would **not** screenshot every variant. The skill is explicit about screenshot cost — one targeted screenshot at the end is the right number for routine theme-aware work like this.

## Discipline-rule pass before I declare done

Quick mental run through `SKILL.md`'s six rules:

1. **Naming** — every node has a PascalCase, role-bearing name. No `Frame 1` survives.
2. **Context** — `CommandPalette` itself, every variant frame, the search input, and the result item all carry a `context` line. The component's `context` lists the keyboard bindings and the ARIA roles for the engineer.
3. **Components first** — I built `CommandPalette` as `reusable: true` and reused `Kbd`, `Icon`, `Input` if they exist in the lib. I would *not* hand-roll a button if `IconButton` already exists.
4. **Themes** — every color is a token with light + dark values. `paletteSurface`, `paletteBorder`, `paletteRowSelected`, `scrim` all defined for both modes.
5. **Responsive** — desktop 640px modal; tablet 90vw; mobile full-screen takeover. Encoded as either a separate `CommandPalette_Mobile` variant or a `width: "fill_container"` design that adapts.
6. **Accessibility** — focus ring on the selected row passes 3:1 in both modes; row hit target is 40px tall (under the 44px touch minimum, so on the mobile variant rows go to 48px); icons paired with text, not color-only; keyboard reachability is the entire spec; `Esc` exits and returns focus.

## What I'd report back

A one-paragraph summary: I built a `CommandPalette` reusable with a `state` theme axis covering default / selected / disabled / loading; sibling variant frames cover the typing / no-results / loading states; tokens added for `paletteSurface`, `paletteBorder`, `paletteRowSelected`, `scrim` (both modes); footer documents the `↑ ↓ ↵ esc` chord. Keyboard spec lives in the component's `context` for the engineer. Verified structure via `snapshot_layout`, properties via `batch_get`, and a single sign-off screenshot of the no-results variant.
