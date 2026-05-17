# Accessibility — beyond the 5-point checklist

SKILL.md § Accessibility names five non-negotiable checks (contrast, hit targets, color-as-only-signal, names-map-to-roles, focus states). This file extends them — the topics that matter for shipping accessible products in 2026 but don't fit in a one-page rule list.

**Standards baseline.** Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/), the current W3C recommendation, also published as [ISO/IEC 40500:2025](https://www.w3.org/WAI/news/2025-10-21/wcag22-iso/). 2.2 adds nine new success criteria over 2.1; the ones most relevant for design are target size minimum (2.5.8), focus appearance (2.4.11 / 2.4.12), focus not obscured (2.4.13), dragging movements (2.5.7), consistent help (3.2.6), redundant entry (3.3.7), and accessible authentication (3.3.8 / 3.3.9). Where a project has no stated standard, default to 2.2 AA. WCAG 2.1 is acceptable for projects under existing certification; older versions (2.0) are not.

**What this file owns:** ARIA semantics, focus order, keyboard navigation, app-level keyboard shortcuts, screen-reader content, ARIA live regions, the deeper-cut contrast cases (gradients, text on photos, APCA as alternative), the `prefers-*` media queries, dynamic type, RTL & internationalisation, colour-blindness, motor accessibility.

**What this file does NOT own:** the SKILL.md baseline (already enforced). Reduced-motion timing (define durations in your token suite). Token-level contrast values (document in your project's tokens). Hit-target sizes for native (document per platform guidelines). Color-blind chart palettes (document in your project's data-viz guidelines).

## When to load this file

- Designing forms, modals, navigation, or anything keyboard-driven.
- The user names *accessibility*, *a11y*, *WCAG*, *screen reader*, *RTL*, *internationalization*, *dynamic type*, *high contrast*, or *focus*.
- You're auditing an existing design for accessibility gaps before handoff.
- You're building a component library and need to encode a11y semantics into the components themselves.

## ARIA roles, names, descriptions

Pencil's `name` and `context` map directly to downstream a11y semantics. The code generator (or the engineer reading the design) uses these to choose ARIA roles and accessible labels.

**Naming for roles.** Use the component's role, not its appearance:

- ✅ `PrimaryAction`, `DestructiveAction`, `IconButton`, `FormError`, `SectionHeading`, `Breadcrumb`, `Tabs`, `TabPanel`.
- ❌ `BlueButton`, `BigButton`, `ErrorRedText`, `BoldHeading`.

These names propagate. If you call a component `IconButton`, the code generator will likely pick `<button>` with an `aria-label`. If you call it `BigCircle`, no semantic information survives the export.

**`context` as a description.** When a node's role isn't obvious from its name (a `frame` that's actually a "button-like card"), populate `context` with the intended role and any non-visual behavior:

```
{
  "type": "frame",
  "name": "JobCard",
  "context": "Acts as a clickable card linking to the job detail page. Renders a focus ring when keyboard-focused; activates on Enter and Space.",
  "reusable": true
}
```

The downstream engineer reads this and knows to ship a `<button role="link">` or an `<a>` with appropriate keyboard handling — not a `<div>` with an onClick.

**Decorative elements.** Anything purely visual (a divider rectangle, a corner accent) doesn't need a `context`, and downstream should mark it `aria-hidden`. Pencil's `name` defaulting to `Frame` or `Group` is the signal — fix the name *or* leave it bland and the code generator will skip it.

## Focus order

Focus order is the order keyboard users tab through interactive elements. Default behavior in code: visual order matches the DOM order. **Your job in design: make sure the visual order someone would expect is the same as the order children are nested in the layer tree.**

Practically, in Pencil:

- **Top-to-bottom, left-to-right.** A vertical-layout `frame` produces this naturally. A horizontal-layout `frame` produces left-to-right tab order, which usually matches user expectation.
- **`layout: "none"` is a focus-order trap.** When children are absolutely positioned, the visual order can diverge from the children-array order. The code generator follows the array, not the eyeballs. Either: lay out with auto-layout, or explicitly state focus order in `context` for downstream to honor.
- **Skip links.** For pages with substantial chrome (top nav, side nav), include a `SkipToContent` link as the first focusable element, hidden visually until focused, that jumps to `<main>`. Express it in Pencil as a small frame at the top of the page tree with `name: "SkipToContent"` and a `context` saying *"Visually hidden until keyboard-focused; jumps to main content area."*

**Modal focus traps.** When a modal opens, focus moves into it and stays trapped until the modal closes. In Pencil, name your modal's first focusable child clearly (`Modal_FirstFocus`) and document the trap in the modal's `context`. The engineer ships the trap; you make sure the design tells them where focus should land first.

## Keyboard navigation

Every interactive design has to be usable without a pointer. Common patterns:

| Action | Default keys |
|--------|--------------|
| Activate a button | `Enter` or `Space` |
| Open a link | `Enter` |
| Close a modal / popover | `Escape` |
| Move within a menu / listbox | `↑` / `↓` |
| Move within a tab list | `←` / `→` (or `↑` / `↓` for vertical tabs) |
| Confirm in a dialog | `Enter` |
| Cancel in a dialog | `Escape` |
| Submit a form | `Enter` (when focus is in a single-line input) |
| Multi-line input newline | `Enter` (textareas only) |

Design implications:

- **Don't design controls that depend on hover.** If a button only appears on hover with no keyboard alternative, the keyboard user can't reach it. Either always show, or surface on focus too.
- **Tab to discover dropdowns.** Dropdown menus that open only on click but are styled identically to ones that open on hover are confusing. Pick one, and make focus open the menu in the same way.
- **Don't intercept native shortcuts.** Browsers reserve certain shortcuts (Cmd+Tab, Cmd+W, etc.). A custom `Cmd+W` handler is hostile.

**Visible focus outline.** Mentioned in SKILL.md and `components.md`; restating: every interactive element gets a 2px `$focusRing` outline with 2px offset on `:focus-visible`. Visible against any surface in both modes. Don't ship `outline: none` without a replacement — that's a keyboard accessibility regression.

### App-level keyboard shortcuts

Beyond per-component keyboard semantics, modern apps ship app-wide shortcuts. The discipline:

- **Discoverable.** Every app shortcut needs a way to find it without reading the source. Common pattern: a `?` keyboard shortcut opens a "Keyboard shortcuts" overlay listing every shortcut grouped by area. Linear, GitHub, Notion, Slack, and Vercel all use this pattern.
- **Documented in UI.** Where a control has a keyboard shortcut, surface it in the UI: a tooltip on hover, a hint next to a menu item, or a `⌘+K` chip inside a search input. Never make the user guess.
- **Don't conflict with browser / OS shortcuts.** `⌘+W`, `⌘+T`, `⌘+R`, `⌘+L`, `⌘+P`, `⌘+S`, `⌘+Q`, `⌘+H`, `⌘+M` belong to the browser or OS. Custom handlers for these break user expectations and accessibility (a custom `⌘+S` that doesn't actually save anything in your app is hostile).
- **Use `⌘` on Mac, `Ctrl` on Windows / Linux.** Display the right key per platform: `⌘+K` on Mac, `Ctrl+K` on Windows / Linux. The browser exposes the OS via `navigator.platform`; the engineer ships the conditional. Document the expectation in component `context`.
- **Modifier stacking.** Combine modifiers in a consistent order: `Ctrl` → `Alt` → `Shift` → key. Display: `⌘+Shift+K`, not `Shift+⌘+K`.
- **Don't shadow `Esc`.** Esc closes overlays, dismisses tooltips, and cancels selections. Don't intercept Esc for a custom action that prevents the user from dismissing what's currently open.

**Common app-wide shortcuts** (with conventions established by widely-used apps; adopt where you can):

| Shortcut | Common action |
|----------|---------------|
| `⌘+K` / `Ctrl+K` | Open command palette |
| `⌘+/` / `Ctrl+/` | Toggle help / show shortcuts |
| `?` | Show keyboard-shortcuts overlay |
| `⌘+,` / `Ctrl+,` | Open settings / preferences |
| `⌘+Enter` | Submit forms with multi-line inputs |
| `Esc` | Close current overlay / dismiss / cancel |
| `g` then `letter` | Navigate (`g h` for home, `g s` for settings; see GitHub, Linear) |

In Pencil, design the keyboard-shortcuts overlay as a component (likely a modal-style panel) with grouped sections, and document each shortcut in the relevant component's `context`: *"Keyboard shortcut: ⌘+K (Mac), Ctrl+K (Windows/Linux). Opens command palette."*

## Screen reader content

Pencil designs are visual; screen readers consume code. The bridge is what the engineer ships, but design choices push them toward good or bad output.

**Alt text on `image` fills.** Every image needs an alt text *or* a clear "this is decorative" signal. In Pencil, set `context` on image nodes:

- For meaningful images: `context: "Photo of the team at the 2026 offsite. Used as a hero on the careers page."`
- For decorative images: `context: "Decorative — no alt text needed."`

The code generator picks up the latter and emits `alt=""` on the `<img>`.

**Icon buttons.** A button that's only an icon (search, close, menu) needs an accessible name. In Pencil, the icon button's `name` *is* that name: `IconButton_Search`, `IconButton_Close`. The code generator emits `aria-label="Search"` on the button.

**Live regions for toasts and async announcements.** A toast that appears asynchronously (form saved, error returned) needs to be announced to screen readers. Mark the toast component's `context`: *"Live region. Announces its content when it appears. Polite (not interrupting)."* The engineer ships `aria-live="polite"` on the toast container.

ARIA live regions come in two main flavours. Pick the right one per use case:

| Pattern | When to use | ARIA |
|---------|-------------|------|
| `role="status"` / `aria-live="polite"` | Non-urgent updates the user benefits from knowing about: "Saved 2 minutes ago", form-submit success, search-results-updated, "12 new items loaded". The screen reader announces *after* the user finishes their current speech. | `aria-live="polite"` (or `role="status"` which implies polite) |
| `role="alert"` / `aria-live="assertive"` | Urgent updates that demand immediate attention: form-validation errors on submit, session-about-to-expire warnings, critical system errors. The screen reader interrupts the current speech. Use sparingly; assertive overuse is the screen-reader equivalent of alert fatigue. | `aria-live="assertive"` (or `role="alert"` which implies assertive) |
| `aria-live="off"` (default) | Anything that doesn't need announcement. The default for most content. | (none; default) |

**Other live-region patterns:**

- **Form error count on submit.** When a user submits a form with validation errors, focus moves to the first invalid field *and* a live region near the form announces the count: *"3 fields need attention."* Polite (the user is now reviewing the errors). See [`forms.md`](forms.md) § Error display.
- **Loading state with announcement.** Long-running operations (export, generation) announce their state changes: *"Export started"*, *"Export 50% complete"*, *"Export complete"*. Polite. Don't announce on every percentage tick; chunk to milestones.
- **Search results updated.** A search input that filters a list as the user types announces the new result count: *"Showing 12 of 89 results"*. Polite, debounced (announce after typing stops, not on every keystroke).
- **Real-time presence updates.** When a teammate joins or leaves a collaborative surface, announce: *"Sarah joined the document"*. Polite. Critical for screen-reader users in collaborative tools who otherwise have no way to know.

In Pencil, document the live-region pattern in the component's `context`:

```
"context": "Live region. Announces error count on submit (e.g. '3 fields need attention'). aria-live='polite'. Announce only on submit, not on field-level validation."
```

**Headings.** Heading hierarchy matters for screen-reader navigation. In Pencil, you don't author HTML heading levels directly — you author text styles (`$text2xl`, `$text3xl`, etc.). The relationship between visual size and heading level should be consistent and obvious to the engineer:

- Page title → `<h1>` (typically `$text3xl` or `$text4xl`)
- Section title → `<h2>` (typically `$text2xl`)
- Subsection title → `<h3>` (typically `$textXl`)
- Component-level title → `<h4>` or `<h5>` (typically `$textLg`)

Don't skip levels visually (a `<h1>` followed by an `<h4>` is a screen-reader jump). Don't use heading sizes for non-heading text — visual emphasis without structural meaning is confusing.

**Lists.** When you draw N items vertically with similar shapes, the engineer probably ships a `<ul>` or `<ol>`. Make the list-ness obvious in the design (consistent vertical rhythm, parallel structure). For standalone groupings that aren't lists (a sidebar with three unrelated cards), make that obvious too — different vertical rhythms, different titles per card.

## Contrast — the deeper cut

The SKILL.md baseline (4.5:1 body, 3:1 large/UI components) and `tokens.md`'s per-pair check cover the common case. Three cases need extra care:

**Gradient backgrounds.** A button with a gradient fill must hit contrast against its *darkest* point — not the average. Test by sampling the gradient's darkest visible region under the label position. This is why neon gradients with white text often fail: the bright gradient stops are fine, but white on the dark stop fails.

**Text on photos.** Always pair with a scrim — a `linear_gradient` overlay from `rgba(0,0,0,0.6)` at the text edge to `transparent` at the opposite edge — or a fully opaque backdrop behind the text region. Translucency over a photo is unpredictable: the text's contrast depends on the photo content, which is variable.

**Disabled states.** Disabled controls relax to ≥ 3:1 because they're not interactive. But don't drop below 3:1 — disabled labels at 1.5:1 are unreadable. The 50% opacity recipe in [`states.md`](states.md) hits ≥ 3:1 against most surfaces; verify in both modes.

**UI components against surfaces.** A button against a card against a page — three layers. Each pair needs to clear 3:1. The most-missed case: a card border (`$border`) against the card surface (`$surfaceMuted`) against the page surface (`$surface`). All three contrasts matter; the page-to-card border is what makes the card visible at all.

**APCA as an alternative metric.** WCAG 2 contrast ratios are based on relative luminance and have known perceptual blind spots: they can flag perceptually-fine combinations as failing (dark grey on medium grey) and pass perceptually-poor ones (certain saturated hue pairings). The [Accessible Perceptual Contrast Algorithm (APCA)](https://apca.info), a candidate metric for WCAG 3, is more perceptually accurate. For projects under existing certification (WCAG 2.1 / 2.2 AA), keep using the 4.5:1 / 3:1 thresholds for compliance. For new projects without a certification requirement, APCA is the better measurement tool: a score of `Lc 75` or above is broadly comparable to AA for body text, `Lc 60` for large text and UI components. When you reach for an APCA score, document the choice in the project's `tokens.md` so the contract is explicit.

## `prefers-*` media queries

Modern operating systems expose user preferences to the browser. Designs that respect them are accessible to a much wider audience.

**`prefers-reduced-motion`.** When the user prefers reduced motion, transitions > 200ms become instant; loops (except skeleton shimmer) disable; micro-interactions ≤ 120ms stay.

**`prefers-contrast`.** Two values matter: `more` (boost contrast) and `less` (rare; reduce contrast). When `more` is set:

- Boost token saturation toward maximum contrast. `$textPrimary` against `$surface` should hit 7:1, not just 4.5:1.
- Thicken strokes — 1px borders become 2px.
- Increase focus-ring weight from 2px to 3px.
- Surfaces gain a 1px border even when they didn't have one before, so adjacent regions are distinguishable.

In Pencil, the `contrast` theme axis registers automatically once you declare contrast-conditional variable values. You don't declare the axis explicitly — `set_variables` reads the `theme: {...}` entries in your values and creates the axis. Variables carry contrast-conditional values:

```
border: { type: "color", value: [
  { value: "#E4E4E7", theme: { mode: "light", contrast: "normal" } },
  { value: "#A1A1AA", theme: { mode: "light", contrast: "more"   } },
  { value: "#27272A", theme: { mode: "dark",  contrast: "normal" } },
  { value: "#71717A", theme: { mode: "dark",  contrast: "more"   } }
] }
```

**`prefers-reduced-transparency`.** When set, the user wants opaque surfaces. Designs that lean on translucency (frosted-glass modal backdrops, blurred sticky headers, sheets with semi-transparent fills) need an opaque fallback:

- `backdrop-filter: blur(...)` → solid `$surfaceMuted` instead.
- 80% opacity sheets → 100% opacity with a stroke instead.
- Ghost buttons that rely on translucent fill on hover → solid `$primaryMuted` fill.

Express in Pencil as conditional fills (or as a separate `*_Opaque` variant of components that lean on translucency).

**`forced-colors` (Windows High Contrast Mode).** A separate accessibility mode where the OS overrides colors entirely — backgrounds, text, links, buttons all become system-defined high-contrast colors. Custom focus rings disappear. Custom button styling collapses. Designs that rely on filled rectangles for borders rather than `border` properties become invisible.

Design implications:

- Use real `stroke` properties for borders, not 1px filled rectangles.
- Don't rely on background color alone to convey state — pair with text or icon.
- Test if the project ships to Windows users who enable HCM. Most products skip this; for accessibility-critical products (gov, edu, healthcare) it's a hard requirement.

**`color-scheme`.** Declared in code via `<meta name="color-scheme" content="light dark">`. Tells the browser to render system widgets (form inputs, scrollbars) in the matching mode. Design implication: when you ship a dark-mode app, the engineer should set `color-scheme: dark`; otherwise the user's text inputs render in light-mode chrome inside your dark page. Note this in the design's handoff if you're shipping dark-only or auto-switching designs.

## Dynamic type & text scaling

Users can scale text — by zooming the browser (typically 100–200%), by setting larger system font sizes (iOS Dynamic Type, Android Font Size), or via Reader Mode. Designs that hard-code pixel heights on text containers break.

Rules:

- **Never lock text container heights.** A heading frame with `height: 64` truncates when the user zooms to 200%. Use `height: "fit_content"` so the frame grows.
- **Don't use single-line containers for content that's not single-line in every locale.** A button with 8px vertical padding around a label fits "Sign in" comfortably but breaks "Bei eindeutigem Bedarf abmelden" — the German equivalent — at 200% zoom.
- **Test at 200% zoom.** A web design that holds together at 200% zoom is robust. One that breaks needs more flexible layout.
- **Mobile dynamic type.** iOS users with the largest Dynamic Type setting see text 200% larger than default. Designs should accommodate this — bottom-anchored CTAs that disappear behind the keyboard at 200% Dynamic Type are a real bug.

In Pencil:

- Default to `"fit_content"` for text containers' constrained dimension. Pin only when the design genuinely requires a fixed dimension (e.g. a sticky header bar — even then, the text inside should overflow gracefully).
- For mobile components, sketch a "200% type" variant (literally 200% of the base font sizes) and verify the layout holds.

## RTL & internationalization

Right-to-left languages (Arabic, Hebrew, Persian, Urdu) flip the reading axis. Designs that hard-code "left" and "right" break when localized.

**Flip these:**

- Layout direction (rows reverse).
- Text alignment defaults (`left` becomes `right`).
- Directional icons (back arrow, next, chevrons in navigation, drawer-open from-left).
- Padding shorthand (logical inline-start / inline-end, not physical left / right).

**Don't flip these:**

- Time-based icons (clock, history, date pickers — clocks go the same direction in every culture).
- Numeric data (numbers stay left-to-right inside RTL contexts).
- Logos and brand marks.
- Media controls (play/pause/stop are universal).
- Charts when the data axis is canonical (e.g. a financial chart's time axis goes left-to-right because that's how the data reads).

**Expansion buffer.** Translated copy is rarely the same length:

- German is ~30% longer than English on average.
- French is ~20% longer.
- Chinese / Japanese / Korean are ~30–50% shorter.
- Russian and Arabic vary widely by phrase.

Design buttons, labels, and section headers with **30% extra width** beyond the English text — or use `"fit_content"` and let the layout adapt. Hard-coded button widths break in localization.

**Locale-specific formatting.** Numbers, dates, currency, plurals all change. Don't hard-code formatting in mockups — use placeholder shapes (`1,234` → `{N} users`, `$1,234 USD` → `{currency}{amount}`) and let the engineer apply the localization library.

**Pseudo-localization.** A test pass where the engineer replaces every translatable string with an inflated placeholder (`Hello` → `[Ḣéĺĺöö Ŵõŕĺď ţéšţ ťéśţ]`). Reveals every string that's not actually localizable, every layout that breaks under 30% expansion. Worth requesting for any product that ships internationally.

## Color-blindness — beyond the basics

SKILL.md says "color is never the only signal." Restated for state design:

- **Errors:** red border + alert icon + helper-text message.
- **Success:** green check + "Saved" text.
- **Warnings:** amber + alert-triangle icon.
- **Status pills:** color + text label, never color + nothing.

For chart palettes specifically (sequential, diverging, categorical):

- **Categorical palettes** must work for the most common color-blindness types (deuteranopia, protanopia). Avoid red/green-only distinctions; pair with shape or pattern.
- **Sequential palettes** are color-blind-safe by default if they vary lightness, not just hue (a viridis-style ramp).
- **Diverging palettes** need a clearly different anchor at each end. Red → blue (with white midpoint) is widely robust; red → green is the classic mistake.

## Touch & motor accessibility

For web:

- **Hit targets ≥ 44×44.** Already in SKILL.md. Restate for web: even on desktop, a 24×24 close-button is hostile to users with motor impairment.
- **Spacing between adjacent targets ≥ 8.** Two buttons one pixel apart force precise targeting. Always pad.
- **Drag interactions need keyboard alternatives.** Drag-to-reorder needs `↑`/`↓` keyboard shortcuts. Drag-to-resize needs `←`/`→`. Drag-only is a motor-accessibility regression.
- **Hover-only context** (a tooltip that appears on hover and disappears as soon as you mouse away) is hostile to users with tremor. Tooltips should be dismissible only by `Escape` or click-outside, not by mouse-movement.

## Verification checklist

Before declaring an accessible design done, run:

1. **Tab-through.** Trace the focus order from the page's first focusable element to last. Does the order match what a sighted user would read? Is every interactive element reachable? Does focus get trapped where it should (modals) and not where it shouldn't (page chrome)?
2. **Focus-ring visibility.** Pick the most contrasting element on the page (a primary CTA on a colored background). Is the focus ring visible? Repeat in the alternate mode.
3. **Disabled-state contrast.** Sample the disabled label color against the disabled button surface. Hits ≥ 3:1?
4. **Error state without color.** Imagine the page in grayscale. Are errors still distinguishable from non-errors? (If not, you're relying on color alone.)
5. **Hit-target sizes.** Does every interactive element clear 44×44 (or 48×48 for Android)? Including icon-only buttons, close ✕ icons, and inline-toolbar controls?
6. **Heading hierarchy.** Read the page title-by-title. Do they form a coherent outline (h1 → h2 → h3, no skipped levels)?
7. **200% zoom.** Mentally (or actually) zoom the design. Does anything overflow, truncate, or break? Are sticky regions still functional?
8. **RTL flip.** If the project ships to RTL locales, mentally mirror the layout. Do directional icons, navigation chevrons, and inline-start/end paddings flip correctly? Does numeric or chart content stay LTR?
9. **HCM / forced-colors.** If the product targets Windows users who use HCM, mentally apply the override: backgrounds become system colors, custom borders go away. Does the layout still work? (Skip if not in scope.)
10. **Live-region announcements.** For toasts, async errors, and inline confirmations: is the live-region behavior documented in `context`?

Fix what fails before reporting done. Don't note a11y failures as "TODOs" — they ship as bugs.

## See also

- SKILL.md § Accessibility — the 5-point baseline (always-on).
- [`states.md`](states.md) — focus-with-error edge case, disabled contrast, error-not-color-alone.
