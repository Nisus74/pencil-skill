# Cmd+K command palette: visual design and keyboard contract

Before I touch the canvas, a quick note on what I consulted. The skill points cmd+K work straight at `references/modern-patterns.md` (the "Modern UI affordances" section explicitly owns the command palette anatomy), and the keyboard side at `references/interactions.md` (keyboard tables, focus management, modal mechanics). I cross-referenced `iconography.md` rules in passing for the result-row icons, and the SKILL.md discipline rules govern naming, context, themes, and accessibility throughout.

I'd also want to follow my normal workflow: ping `get_editor_state`, check whether your project has a `design-system/` folder, scan the open `.pen` and any imported `.lib.pen` for an existing `CommandPalette` or `Modal` / `Input` / `ListItem` components I should reuse before building from primitives. The plan below assumes a typical app `.pen` with a basic component library available — call out anything different and I'll adjust.

---

## Workflow I'd run

1. `get_editor_state({ include_schema: false })` — confirm the host is connected and a `.pen` is open. If not, stop and ask you to open one.
2. Filesystem check for `./design-system/` — read `README.md`, then `design-system.md` (for tech stack, icon family) and `tokens.md` (for colours, spacing, type, motion, focus ring).
3. `get_guidelines()` with no args, then load `Web App` (and `Tailwind` if your stack is Tailwind).
4. `get_variables()` — note existing tokens. Don't re-declare `surface`, `border`, `textPrimary`, `textMuted`, `focusRing`, `space-*`, `radius-*` if they're already set.
5. Component inventory:
   - `batch_get({ patterns: [{ reusable: true }], readDepth: 2 })` on the open doc.
   - Same against each library in the document's `imports`.
   - I'm specifically hunting for: `Modal` / `Dialog`, `Input` / `SearchInput`, `ListItem` / `MenuRow`, `Kbd` / `Shortcut`, `Icon`, `Badge`. If any exist, the palette is composed of refs, not new primitives.
6. `find_empty_space_on_canvas` if the canvas already has frames — I want the palette frame placed somewhere sensible in the `BuildReady` region.
7. Plan (next section), then `batch_design`.
8. Verify with `snapshot_layout` and `batch_get`. Single end-of-job `get_screenshot` scoped to the palette frame, not the whole page.

---

## The plan (vibe and structure)

**Atmosphere:** dense, symmetric, fluid. A command palette earns density (developers and power users live here), wants symmetry (it's a list), and wants fluid micro-motion (it appears, animates result transitions, and dismisses many times a day).

**Top-level frames I'd add to the canvas (siblings, in `BuildReady`):**

- `CommandPalette / Default / Desktop` — empty input, recents shown.
- `CommandPalette / Typing / Desktop` — query in input, filtered results with one row highlighted.
- `CommandPalette / Empty / Desktop` — no matches state.
- `CommandPalette / Loading / Desktop` — async results pending (only if your palette searches server-side).
- `CommandPalette / Mobile` — full-screen sheet variant, since 390px viewports can't host a centred 640px modal.

The reusable component itself lives in your `.lib.pen` if you have one (or gets promoted there once we're happy). Name: `CommandPalette`. `reusable: true`.

---

## Visual design

### Container

- **Surface:** modal-style overlay. Backdrop is `rgba(0,0,0,0.4)` in light mode and `rgba(0,0,0,0.6)` in dark — bound to a `$backdrop` variable, theme-aware. Subtle 4px backdrop blur if your project's `motion.md` opts in, otherwise solid scrim. Don't reach for glassmorphism on the palette itself; the modern-patterns reference flags glass-on-everything as a dated default.
- **Palette panel:** 640px wide on desktop, capped to `min(640px, calc(100vw - 32px))`. Vertically positioned at ~22% from the top of the viewport, not centred — this is the optical-centre rule (geometric centre on a tall viewport reads as "sinking"). Spotlight, Raycast, Linear all sit higher than centre.
- **Background:** `$surface` (off-white in light, off-black in dark — never raw `#FFF`/`#000`, that's an AI tell).
- **Border-radius:** 12px on the panel. Inner rows round to 8px so the child-radius-≤-parent rule holds.
- **Border:** 1px `$border` for definition, especially in dark mode where the shadow flattens.
- **Elevation:** layered shadow (ambient + direct), per the SKILL.md elevation default:
  ```
  0 1px 2px rgba(0,0,0,0.06),
  0 24px 48px rgba(0,0,0,0.18)
  ```
  In dark mode, swap the heavy drop for a 1px inner highlight (`inset 0 1px 0 rgba(255,255,255,0.04)`) plus a softer outer shadow — `elevation.md` owns this.

### Search input (header row)

- 56px tall. Sits flush at the top of the panel; bottom 1px `$border` separates it from the results.
- Leading 20px search icon (Lucide `search` if your `design-system.md` declares Lucide; whatever family is named otherwise). Icon colour: `$textMuted`. The icon is muted on purpose — pairing icon + text where the text is the active concern (the user's typed query) means the icon steps back. Per `interactions.md` and the SKILL.md aesthetic-defaults rule on icon-vs-text contrast.
- Input itself: 16px `$fontBody`, `$textPrimary`. **Mobile font-size 16px minimum** to defeat iOS auto-zoom (a `forms.md` rule, restated here so the engineer doesn't ship 14px and break it).
- Placeholder: `Search commands, files, or pages…`. Trailing ellipsis is the ellipsis convention from `interactions.md`. Placeholder colour `$textMuted`.
- Trailing region: a compact `Esc` `Kbd` chip showing the dismiss shortcut. Faint, not a button — purely informational.
- No visible border on the input itself; the panel border + the row separator do the framing. Browser `outline` removed and replaced with the `$focusRing` ring on `:focus-visible` (2px, 2px offset).
- `aria-label="Search commands"` documented in `context`.

### Results region

- Scrollable, max-height ~ `60vh`. Scrollbar styled or hidden depending on your project's convention.
- **Grouped sections** with sticky group headers. Typical groups, in this priority order:
  1. **Suggestions** — context-aware top picks (current page actions, the most-likely command based on recency and current selection).
  2. **Recent** — last 5 items the user opened from the palette.
  3. **Pages / Navigation** — addressable destinations.
  4. **Actions** — verbs the user can run (`Create issue`, `Invite teammate`, `Toggle dark mode`).
  5. **Search results** — fuzzy matches over your data (issues, docs, customers). Shows when the query is ≥ 2 characters.
- **Group header:** 12px `$textXs`, `$textMuted`, uppercase, tracked +0.04em. 8px top padding, 4px bottom. Sticky during scroll within its section.

### Result row

- **Height:** 44px. That's a deliberate touch-friendly hit target even though this is a desktop-first surface — keyboard users and touch users both benefit, and a 32px row feels cramped once icons and shortcuts land.
- **Layout (left to right, all in one row, gap 12px):**
  1. **Leading icon** 20×20, `$textMuted` (or category-tinted: blue for navigation, neutral for actions, green for "create" verbs — but keep the palette to one accent dominant per row, not a rainbow).
  2. **Primary label** 14px `$fontBody`, `$textPrimary`, weight 500. Truncate with ellipsis on overflow.
  3. **Optional subtitle / breadcrumb** 13px `$textMuted` — for results that need disambiguation (`Settings → Billing`, or a customer's email under their name).
  4. **Trailing region (right-aligned):**
     - Optional badge (e.g. `New`, `Beta`).
     - Keyboard shortcut hint as `Kbd` chips: `⌘ K`, `⌘ ⇧ P`. Render the shortcut tokens as separate small chips with hairline borders so the eye reads `⌘`+`K` as two keys, not one glued glyph.
- **Highlighted row (the one cursor or arrow keys are on):**
  - Background `$surfaceMuted` (a light tint of surface, not a saturated brand colour — this isn't a click, it's a focus indicator).
  - Add 2px `$accent` left border (or a 3px inset bar) to make the highlight visible to colour-blind users — colour alone isn't enough (SKILL.md a11y rule 3).
  - Trailing `↵` enter chip appears on the highlighted row only, signalling "press enter to run this".
- **Hover** (mouse): same treatment as keyboard-highlighted, but transient. Hover should *also* move the keyboard highlight so they stay in sync (no dual cursors).
- **Match highlighting:** the substring of the label that matched the query renders in `$textPrimary` weight 600; the rest stays at 500. Don't underline or colour-tint matches — weight is enough, and tinting fights the row-highlight colour.

### Footer (status bar)

- 36px tall, top 1px `$border`.
- Left: contextual hints — `↑↓ Navigate`, `↵ Open`, `⌘↵ Open in new tab`, `Esc Close`. Inline `Kbd` chips, 11px text. The shortcuts shown should change with context (when a row is highlighted, surface that row's available verbs).
- Right: a tiny mode badge (e.g. `Pages` / `All`) if your palette supports scoped search. Otherwise leave empty.

### Empty state

- Centred in the results region, 80px tall block.
- Muted icon (search-x or similar, 24px, `$textMuted`).
- Headline: `No results for "<query>"` (16px `$textPrimary`).
- Body: `Try a shorter query, or invite teammates with <code>⌘⇧I</code>` — actionable guidance, not just *"nothing found"*. Per the microcopy default in SKILL.md.

### Loading state

- For palettes with async/server search, show a 1.4s shimmer skeleton row (3 placeholder rows) in the results area after a 200ms show-delay, with a 400ms minimum visible time. This is the loading-flicker rule from `interactions.md` and `modern-patterns.md`. Do not show a centred spinner — the skeleton tells the user where content will land.

### Mobile variant

- Full-screen sheet that slides up from the bottom; not a centred modal at 390px width. Detent: 92% of viewport height.
- Search input pinned at the top with safe-area top padding.
- Footer hints hidden (no keyboard); replaced with a single `Cancel` button at the top-right of the search row.
- Result rows expand to 56px (touch comfort).
- `Esc` chip removed; tap-outside or pull-down-to-dismiss replaces it.

### Theme behaviour

- All colours bind to variables that resolve in both `mode: light` and `mode: dark`. Specifically: `$surface`, `$surfaceMuted`, `$border`, `$textPrimary`, `$textMuted`, `$accent`, `$focusRing`, `$backdrop`. I'd verify with `get_variables()` first; only `set_variables` for ones not already declared.
- Backdrop opacity is the one colour I'd actually want to verify visually under both modes via a single screenshot of the dark variant — light is usually fine; dark backdrop on a near-black surface needs a sanity check.

---

## Keyboard interaction contract

This is the section I'd encode verbatim into the `CommandPalette` component's `context` so it survives into the engineering hand-off.

### Summon and dismiss

- **`⌘ K`** (Mac) / **`Ctrl K`** (Windows / Linux) — open the palette from anywhere in the app. Captured at the document level.
- **`⌘ K`** when already open — close.
- **`Esc`** — close. Always. Even mid-typing, even with results highlighted.
- **Backdrop click** — close (this isn't a destructive action; backdrop dismiss is fine here, per the modal mechanics rule in `interactions.md`).
- **Focus trap** while open: tab cycles within the palette only. On close, focus returns to the element that opened it (the discipline-rule: restore focus on dismissal).
- **First focus on open:** the search input. Caret active, ready to type.

### Don't intercept these

- `⌘ Tab`, `⌘ W`, `⌘ T`, `⌘ R`, `⌘ L` — OS / browser shortcuts. Hands off (`interactions.md` § Keyboard everywhere).
- `⌘ P` — if the project's `Print` matters, leave it. If you intentionally repurpose `⌘ P` for "Quick open file" (Notion / VS Code style), document the override in `voice.md` and provide a settings escape hatch. Don't repurpose silently.

### Within the palette

| Key | Action |
|-----|--------|
| `↓` | Move highlight down one row. Wraps to top at end. |
| `↑` | Move highlight up one row. Wraps to bottom at top. |
| `↵` (Enter) | Run the highlighted row's primary action. |
| `⌘ ↵` | Run in a new tab / window (for navigation rows). |
| `⇧ ↵` | Secondary action, if the row defines one (e.g. "Open in side panel"). |
| `Tab` | If the row supports a sub-action menu, focus that. Otherwise move focus to the next palette region (footer hints) — but most palettes don't need this; arrow keys do all the work. |
| `Esc` | Close palette. If the search has text, first `Esc` clears the query; second `Esc` closes. (Optional behaviour; document the choice.) |
| Letter / number keys | Append to query, filter results in real time. |
| `Backspace` on empty query | No-op (don't close on this; users will pause-delete-and-continue). |
| `⌘ Backspace` | Clear query. |

### Scoped search (slash modifier)

Optional but worth designing in if your data has natural categories:

- Typing **`>`** at the start of the query scopes to actions only (VS Code convention).
- Typing **`/`** at the start scopes to navigation.
- Typing **`@`** scopes to people.
- Typing **`#`** scopes to issues / tags.

When a scope prefix is entered, render a subtle chip in the input replacing the prefix character: `[Actions] do thing`. Backspace at the start of the query removes the chip and returns to all-results mode.

### Mouse and trackpad

- Hover moves the keyboard highlight (single source of truth — never two cursors).
- Click runs the row immediately.
- Scroll within the results region scrolls only the results; doesn't bubble to the page behind.

### Touch

- Tap row to run.
- Pull-down on the search row dismisses the sheet.
- Tap-outside dismisses.
- No long-press behaviour by default.

### Reduced motion

- Respect `prefers-reduced-motion: reduce`. The open/close animation collapses from a 200ms fade+scale to instant. Row-highlight transitions stay (they're under 120ms — imperceptible to most users, and removing them removes the affordance signal).

### Accessibility

- Root element: `role="dialog"`, `aria-modal="true"`, `aria-label="Command palette"`.
- Input: `role="combobox"`, `aria-expanded="true"` while results show, `aria-controls="<results-id>"`, `aria-activedescendant="<highlighted-row-id>"`.
- Result list: `role="listbox"`. Each row: `role="option"`, `aria-selected` matches the keyboard highlight.
- Group headers: not interactive; render with `role="presentation"` and let the listbox semantics do the talking.
- Live region announcement when results count changes: `aria-live="polite"` on a visually-hidden status node — `12 results for "settings"`. Throttle to once per pause in typing so screen readers aren't flooded.
- Focus ring on the input visible against `$surface` in both modes (the SKILL.md a11y check 1 — verify contrast ≥ 3:1 on UI).

---

## How I'd actually build it (batch_design sketch)

I won't run the ops here, but the shape:

```
# Frame: palette wrapper for the BuildReady region
panel = I("doc", { type: "frame", name: "CommandPalette / Default / Desktop",
  width: 640, height: "fit_content",
  fill: "$surface", stroke: { fill: "$border", width: 1 },
  cornerRadius: 12, padding: [0,0,0,0],
  layout: { direction: "vertical" },
  context: "Cmd+K command palette in resting state. Keyboard: ⌘K toggles open/close, Esc dismisses, ↑↓ navigate, ↵ runs highlighted row, ⌘↵ opens nav targets in new tab. ARIA dialog+combobox+listbox. Focus trap; restores focus on close. Mobile variant is a sheet, not a modal." })

inputRow = I(panel, { type: "frame", name: "SearchRow", height: 56, width: "fill_container",
  layout: { direction: "horizontal", gap: 12, padding: [16,16,16,16], align: "center" },
  stroke: { fill: "$border", width: 1, side: "bottom" } })
I(inputRow, { type: "icon_font", name: "SearchIcon", icon: "search", size: 20, fill: "$textMuted" })
I(inputRow, { type: "text", name: "QueryInput", text: "Search commands, files, or pages…",
  font: "$fontBody", size: 16, fill: "$textMuted",
  context: "Combobox input. role=combobox, aria-controls=ResultsList, aria-activedescendant binds to highlighted row. Mobile font-size 16 to defeat iOS auto-zoom." })
I(inputRow, { type: "ref", ref: "Kbd", descendants: { label: { text: "Esc" } } })

results = I(panel, { type: "frame", name: "ResultsList", width: "fill_container",
  layout: { direction: "vertical" },
  context: "role=listbox. Scroll height capped to 60vh. Sticky group headers." })

# ... per-group: GroupHeader frame, then Row refs (or primitives if no Row component yet)
# Highlighted row uses ref with descendants override on the highlight bar + Enter chip slot.

footer = I(panel, { type: "frame", name: "FooterHints", height: 36, width: "fill_container",
  stroke: { fill: "$border", width: 1, side: "top" },
  layout: { direction: "horizontal", gap: 16, padding: [10,16,10,16], align: "center" } })
# ↑↓ Navigate, ↵ Open, ⌘↵ New tab, Esc Close — all rendered with the Kbd component
```

If a `Modal`, `Input`, `Kbd`, or `ListItem` component exists in your library, every line above that uses `I(... type: "frame"...)` for that primitive becomes a `ref` with `descendants` overrides instead. That's the point of the components-first inventory step.

---

## Verification, before I'd say it's done

- `batch_design` response shows all ops succeeded.
- `snapshot_layout(panel, maxDepth: 3)` — confirm panel width 640, input row 56 tall, footer 36 tall, gaps as designed.
- `batch_get` on the panel and a couple of rows — confirm `$surface`, `$border`, `$textPrimary`, `$textMuted`, `$accent`, `$focusRing` are bound as variables, not raw hex.
- `get_screenshot(panel)` — single shot at the end, scoped to the panel, primary mode.
- Re-screenshot in dark mode only if the variable check turned up a raw colour (it shouldn't have).
- Walk the SKILL.md a11y five-check list: contrast (input + body), 44px hit targets on rows and the close affordance, colour-not-only-signal (the highlight has a left border *and* a tint), names map to roles (`SearchRow`, `ResultsList`, `FooterHints`), focus state defined on input.
- Run the four-question self-critique gate: does it look like *your* product or any product? Where does the eye land first (should be the input)? Anything decorative-only? One change to feel less generic (often: the choice of icon family or the way `Kbd` chips render makes the palette feel like it belongs).

---

## Things to confirm with you before I touch the canvas

1. **Library state.** Do you already have a `CommandPalette` (or close cousin) in your `.lib.pen`? If yes, I'd extend rather than rebuild.
2. **Scope.** Does your palette search just navigation and actions, or does it also search project data (issues / files / customers)? That changes whether we need the loading state and the live-region announcement.
3. **Slash scopes.** Want the `>` / `/` / `@` / `#` prefix scoping, or single-flat-list?
4. **Mobile.** Is mobile in scope for this iteration, or desktop-only for now? The sheet variant is a separate frame and a small extra of work; happy to skip if not.
5. **Tech stack.** If you're on a stack with a great existing component (cmdk for React, kbar, Radix Command), I'll match the markup conventions in the `context` strings so the engineer doesn't have to translate.

Tell me which of those bite, and I'll plan the actual `batch_design` calls.
