# Modern patterns

Patterns the model under-uses by default. SKILL.md's discipline rules cover the perennials (themes, responsive, accessibility, naming). This file covers what's *currently* table stakes for shipping product UI in 2026 — patterns the model wouldn't reach for unprompted.

**What this file owns:** container queries (vs media queries), fluid type with `clamp()`, AI-UI affordances, animation & motion timing, modern UI affordances (command palette, slash commands, AI input chips, streaming, attachments), perceived performance (skeleton, optimistic UI, LQIP, staggered reveal), modern dark-mode controls, defaults the model reaches for that already read as dated.

**What this file does NOT own:** any of the topics it links into other references for tactical detail. It's the *index* for "what's missing from the AI default" — not a re-implementation of motion, flows, accessibility, or imagery.

## When to load this file

- The user names *modern*, *contemporary*, *2026-style*, *fluid*, *container queries*, *AI UI*, *optimistic*, *real-time*, *presence*, *command palette*, *cmd+K*, *slash commands*, *streaming*, or *animation timing*.
- A design feels generic and you want to introduce a sharper-than-default pattern.
- Auditing an existing design that reads as "AI default" — glassmorphism, three-card grids, parallax everywhere.

## Container queries (not media queries)

Media queries respond to the viewport. Container queries respond to the parent container. When a component needs to look different in a sidebar at 320px wide vs. a main column at 800px wide, container queries are the right primitive — media queries can't tell the difference.

**When to reach for container queries:**

- Components that are reused at different sizes within the same page.
- Layouts where the same card/widget appears in a sidebar, a grid, and a full-width detail view.
- Responsive components inside a resizable region (a panel the user can drag wider).

**When to stay with media queries:**

- Page-level layout (the page header is a viewport concern).
- Top-level navigation chrome.
- Anything where "the device is small" is the actual signal, not "the container is small."

**Pencil expression.** A `frame` with `width: "fill_container"` plus internal auto-layout that adapts to the actually-measured width is the design-side analog. Encode the responsive variants in the component's `descendants` overrides and let the engineer ship the container-query CSS:

```
ProductCard (reusable: true, layout: "vertical", gap: "$space-4", padding: "$space-5")
├── Image    (height: 160 in default; the engineer scales up via @container)
├── Title    ($textXl in default; @container (min-width: 600px) → $text2xl)
├── Subtitle ($textSm $textMuted)
└── CTA      (size scales with container; the engineer ships the rules)
```

Document in the card's `context`: *"Container-aware. At ≥ 600px container width, the title scales up to `$text2xl` and the image to 240px height."*

## Fluid type with `clamp()`

Discrete type-scale steps work for most design surfaces, but for marketing pages and hero typography, fluid type — `font-size: clamp(2rem, 4vw, 4rem)` — gives smooth scaling between breakpoints without intermediate breakpoints.

**When to reach for fluid type:**

- Hero headlines on marketing pages.
- Landing page section titles.
- Display-only typography (oversized, used for atmosphere).
- Anything that should "scale with viewport" rather than step at breakpoints.

**When to stay with discrete steps:**

- Body text (don't fluid-scale). Body should be 16px on mobile, 16–18px on desktop. `clamp(14px, 1.2vw, 16px)` is bad — it produces unreadable text at narrow widths.
- UI text (buttons, labels, table cells). Discrete `$textSm` / `$textBase` / `$textLg` is right.
- Headings inside product UI. Step them; don't fluid them.

**Caveats:**

- Don't fluid-scale `$textBase` below 14 or above 19. Body text outside that range is uncomfortable.
- Always set a `min` and `max` clamp; "infinite scale" hero text breaks at 4K resolutions.
- Test at 200% zoom — fluid type can balloon in unexpected ways.

**Token expression.** Fluid sizes belong in `tokens.md` if used:

```
$textHeroFluid: "clamp(2rem, 4vw + 1rem, 4rem)"
```

Use only on display surfaces. Bind the typography of headlines that *should* be fluid; leave product-UI typography on the discrete ramp.

## AI-UI patterns

Patterns specific to interfaces that include AI-generated content or AI-driven actions. Underdone in most products even when the AI is the headline feature.

**Disclosure.**

When AI generated content, mark it. Patterns that work:

- A small badge on the AI-generated element (a sparkle icon + *"AI"* label).
- A footer note when an entire section is AI-generated: *"Summary written by AI."*
- A border treatment (subtle gradient stroke) on AI-generated cards.

The user should never wonder *"did a human or a model produce this?"*. Disclosure is also a regulatory requirement in some jurisdictions for AI-generated media.

**Regenerate.**

Anywhere the AI produced something, the user should be able to ask for a different one. The regenerate affordance is a small icon button (clockwise arrow + sparkle, or just the sparkle in a button frame), placed near the generated content. On click: replace the content with a new generation.

Edge cases:

- **Loading state during regenerate.** Don't blank the prior content; overlay a subtle loading state on the existing content so the user can compare. Decay the prior on success.
- **Regenerate history.** For high-stakes outputs (a generated product description that the user might commit), keep a small history with previous versions accessible. For low-stakes (a draft, a suggestion), no history needed.

**Confidence.**

When the model's output has measurable uncertainty (a classification, a recommendation, a fact retrieval), surface the confidence:

- High-confidence: no special treatment. Just the answer.
- Medium-confidence: a subtle badge or footer note: *"Based on similar items"* or *"Best guess — verify before sharing."*
- Low-confidence: explicit acknowledgment: *"I'm not sure — here's what I found."* + a path to source / verification.

Don't show numeric confidence to non-technical users. *"82%"* is opaque. *"Best guess"* is human.

**Inline citations.**

When AI output is grounded in retrieved sources, link those sources inline. Numbered superscripts (`Citation 1`, `Citation 2`) are the convention; they expand on hover/click into a small popover with the source title and link. Don't bury citations at the end as a wall of links — people don't read those.

**Abort controls.**

Long-running AI tasks (multi-step generation, retrieval over a large corpus) need a stop button. The control:

- Renders during the streaming response (not just before it starts).
- Is unmistakably a stop, not a pause (a hard square or X icon, not a triangle).
- On click, halts the stream and keeps whatever was already generated.

Without an abort, slow-running AI feels broken — users don't know if it's still working or stuck.

**Don't:**

- Animate AI output character-by-character if the response arrives whole. The fake typewriter is an AI tell.
- Hide AI generation behind a *"loading…"* with no signal that it's an AI doing work. The model's brand value is that it's an AI; don't disguise it.
- Wrap AI features in cute personas (*"Hi, I'm Sparky, your AI helper!"*) unless the brand calls for it. Most products are better served by sober AI affordances.

## Animation & motion

Animation is one of the strongest "feels finished" signals in product design and one of the easiest to get wrong. The rules below apply unless the project's [`motion.md`](../assets/design-system/motion.md) overrides them.

**Timing by interaction type.** Different interactions earn different durations:

| Interaction | Duration |
|-------------|----------|
| Micro (button press, checkbox toggle, hover) | 100–150ms |
| State change (modal open, sheet slide-in, panel expand) | 200–300ms |
| Page transition (route change, full-screen swap) | 300–500ms |
| Long-form motion (a hero animation, a guided onboarding step) | 600ms–1.2s, only with strong reason |

Anything longer than its category reads sluggish; anything shorter reads jittery. The boundaries aren't strict, but a 300ms button press feels broken and a 100ms page transition feels disorienting.

**GPU-accelerated properties only.** Animate `transform` (translate / scale / rotate) and `opacity`. Never animate `width`, `height`, `top`, `left`, `padding`, `margin`, or any layout property; these trigger reflow on every frame and tank performance, especially on lower-end devices. When you need a "size change" animation, use `transform: scale()` with `transform-origin` set to the right anchor, *not* `width` / `height` interpolation.

**Never `transition: all`.** Always enumerate the specific properties to transition:

```css
/* Bad: animates every property change, including unintended ones */
transition: all 200ms ease-out;

/* Good: explicit */
transition: opacity 200ms ease-out, transform 200ms ease-out;
```

`transition: all` will animate properties you didn't intend to (a class change shifts a font-weight, the page suddenly animates the weight change), and it forces the browser to track every property for changes. Always list properties explicitly.

**Loading state flicker rule.** When showing a spinner or skeleton, add a `~150–300ms show-delay` and a `~300–500ms minimum-visible-time` so fast responses don't flash a loading state. Pseudocode:

```
when starting an async operation:
  schedule "show loading state" in 200ms

when async operation completes:
  if loading state is visible:
    hide it after at least 400ms total visible time
  else:
    cancel the scheduled show
    don't show loading state at all
```

This is the difference between a UI that feels responsive and one that feels twitchy.

**Interruptible.** Starting a new state transition should cancel the current one in progress, not queue behind it. A user that clicks rapidly should see the current UI snap to where they pointed it, not wait for animations to play out in series. Document the expectation in component `context`: *"Interruptible. New state transition cancels in-progress transition."*

**Never autoplay.** Don't loop animations on idle UI elements. A subtly-shimmering CTA, a perpetually-pulsing icon, or a card that gently floats reads as desperate ("look at me!") and exhausts the user's attention. The exception: skeleton-screen shimmer, which is a load-state signal, not an idle decoration.

**Hover micro-pattern.** A subtle `translateY(-2px) scale(1.01)` on cards and interactive tiles communicates affordance without layout shift:

```css
.card:hover {
  transform: translateY(-2px) scale(1.01);
  transition: transform 150ms ease-out;
}
```

Avoid layout-shifting hover patterns (`translateY(-8px)`, `scale(1.05)`); they look impressive in isolation and create visual jitter when several cards are visible at once.

**Reduced motion.** Respect `prefers-reduced-motion: reduce` (already covered in [`accessibility.md`](accessibility.md)). When set, transitions > 200ms become instant; loops disable; micro-interactions ≤ 120ms stay (they're imperceptible to most users and provide the affordance signal).

For the project's specific durations, easings, and the skeleton shimmer pattern, see [`assets/design-system/motion.md`](../assets/design-system/motion.md).

## Modern UI affordances

The patterns the model under-uses by default but that ship in essentially every modern productivity surface in 2026.

**Command palette / `⌘+K`.** A keyboard-first command interface, summoned with `⌘+K` (or `Ctrl+K`), that lets the user search across actions, navigate to pages, and execute commands without using the mouse. Now standard in Linear, Notion, GitHub, Vercel, Raycast, Slack, Cursor, and most developer-leaning tools.

Anatomy:

- A modal-style overlay summoned by `⌘+K`.
- A search input that filters in real time.
- Grouped results: navigation targets, actions, recent items, search results from your data.
- Keyboard nav (`↑`/`↓` to move, `Enter` to activate, `Esc` to dismiss).
- Each result shows a hint of its keyboard shortcut if it has one (`⌘+P` next to "Open project").

When to design one: any product the user opens daily, any product with > 10 navigation destinations, any product with frequent actions the user repeats. Skip if the product is pure-content (a blog, a marketing site).

In Pencil, build the palette as a reusable `CommandPalette` component with slots for `SearchInput`, `Results`, `EmptyState`. Document the keyboard contract in `context`.

**Slash commands.** A text input where typing `/` opens a context menu of commands the user can run inline. Standard in Notion, Slack, GitHub PR comments, Discord. Two patterns:

- *Editor slash:* `/` in a text editor opens block-type picker (heading, list, image, code).
- *Search slash:* `/` in a search bar opens a filter / scope picker.

Anatomy:

- A `/` keystroke triggers the menu.
- A filter input narrows the menu options.
- Arrow keys move; Enter selects; Esc closes; clicking outside closes.

In Pencil, design the menu as a popover component anchored to the input's caret position. Document the trigger and dismissal contract.

**AI input affordances.** When an input accepts AI prompts, the affordance should make this discoverable:

- A subtle `✦` (sparkle) icon in the input or its trailing edge.
- A placeholder that hints at what's possible: *"Ask anything…"*. Use sparingly; placeholder-as-label is still bad.
- A `/` slash menu showing AI-specific actions (`/summarise`, `/rephrase`, `/expand`).
- An attach affordance for files / images the model can consume; usually a paperclip icon adjacent to the input.

**Streaming response patterns.** When an AI response streams in token by token:

- Show a cursor (a thin vertical bar, blinking ~600ms cycle) at the streaming position.
- The streaming text appears character-by-character as it arrives. *Do not* fake this with a typewriter animation when the response arrives whole; that's an AI tell.
- A subtle "thinking" indicator before the first token appears (a small `…` or pulsing dot near the cursor).
- An abort control (`■` square or `✕` icon) renders during streaming, lets the user halt and keep what's already generated.

**Attachment affordances.** For inputs that accept files (chat composers, AI prompts, support forms):

- Drag-and-drop the file onto the input; the input shows a "drop here" overlay during drag-over.
- A paperclip icon or "attach file" button as a fallback (clicks open the native file picker).
- Once attached, the file appears as a chip near the input with a thumbnail (for images), filename + size (for documents), and a `✕` to remove.
- Allow paste-from-clipboard for images (`⌘+V` of an image pastes the image as an attachment).

These affordances are easy to skip and easy to spot when missing. A 2026 product without them reads as a 2022 product.

## Perceived performance

Several patterns where the perceived speed of an interaction matters more than the actual speed. The model under-uses these by default.

**Skeleton screens.**

Restated from [`states.md`](states.md): a placeholder shape that approximates the loading content's dimensions, with a 1.4s shimmer animation. The pattern is a 2026 default — don't ship a centred spinner for initial-page loads on any product surface that isn't trivially fast.

**Optimistic UI.**

Restated from [`flows.md`](flows.md): for high-confidence writes (toggling a setting, marking a task done, liking a post), update the UI immediately and reconcile with the server in the background. Roll back on failure with a non-blocking toast.

**LQIP / blur-up imagery.**

For images that take a few hundred ms to load, a low-quality preview placeholder shown immediately is much better than blank space. Three patterns:

- **Blurred LQIP.** A tiny base64-encoded blurred preview embedded in the page; replaced with the full image on load. Most React/Next image components do this automatically.
- **Dominant-color placeholder.** A solid color (the average of the image) rendered immediately; the image fades in over it. Cheaper than LQIP for sites that don't pre-process images.
- **SVG silhouette.** For product photography or illustrations with a clear shape, a flat SVG silhouette in `$surfaceMuted` while the image loads.

In Pencil, document the LQIP intent on image nodes: *"Uses LQIP — blurred preview shown until full image loads."* The engineer ships the runtime.

Document imagery treatment decisions in the project's image guidelines or as `context` on image node placeholders in the design.

**Staggered content reveal.**

When a page has multiple regions that load on different schedules (the page chrome arrives instantly, the data takes 800ms, the chart takes 1500ms), animate each region in as it arrives — not the page all at once. The user sees the page assembling, which feels faster than waiting for everything to be ready.

The animation is subtle: a 120ms fade-in plus a tiny `translateY(4px → 0)`. Stagger by ~50ms between regions so the assembly is visible but not distracting.

**Prefetch on hover.**

On the web, hovering a link typically gives the browser ~200ms before the user clicks. Prefetching the destination on hover means the navigation feels instant on click. This is a code-side pattern (the engineer triggers prefetch on `mouseenter`), but designs that *enable* prefetch — small, fast routes; lightweight detail pages — feel snappier.

In Pencil, link nodes can document: *"Prefetched on hover. Detail page is < 50KB; hover-to-click is typically instant."*

## Modern dark mode

Dark mode is a 2024 default; the *quality* of dark mode in 2026 still varies. Patterns that distinguish a competent dark mode from a mechanical one:

**`color-scheme` declaration.**

In code: `<meta name="color-scheme" content="light dark">` (or `dark` for dark-only apps, `light` for light-only). Tells the browser to render system widgets — form inputs, scrollbars, the password manager dropdown — in the matching mode. Without it, the user's text inputs render in light-mode chrome inside your dark page. Document the choice in the design's handoff.

**Manual toggle vs system-driven.**

Three options:

- **System-driven only.** The site/app follows `prefers-color-scheme` automatically. No user toggle. Best for products with a strong opinion on theme handling.
- **Manual toggle, persisted.** A button (sun/moon icon, typically) in the page chrome. The user's choice persists in localStorage. The toggle should also offer a "follow system" option.
- **Manual toggle with system as default.** Initial visit: follow system. After explicit toggle: persist the user's choice and stop following system.

The third option is the modern best-practice — it respects the system signal but lets the user override.

**Avoid pure inversions.**

A dark mode that's literally `invert(100%)` of the light mode reads cheap. Real dark modes:

- Use slightly desaturated colors. Brand colors that pop on white can become harsh on black; soften them by 10–20% saturation.
- Use higher contrast for fine details. Hairline borders that read as 1px in light mode often need to be slightly stronger in dark mode.
- Use slightly warmer surfaces. Pure dark gray is cold; a slight blue or warm undertone (not chosen randomly — chosen per brand) adds depth.

For shadow alternatives in dark mode: substitute a 1px border or a subtle inner glow for what would be a drop shadow in light mode. Shadows are created by light; in a dark-mode surface they don't read.

**Brand color anchors.**

A brand element (logo, accent button) often needs adjustment between modes. The brand isn't necessarily one color — it's a feeling the brand wants to evoke. In dark mode that might require a different hue or saturation than the literal Pantone. Document the dark-mode anchor explicitly in your token suite so future editors don't guess.

## Real-time / presence

Short. The detail lives in [`flows.md`](flows.md) § Real-time / presence flows.

In 2026, multi-user presence is no longer a "collaboration features" thing — it shows up in:

- Active-user avatars in any shared workspace (settings pages where multiple admins might be editing, dashboards where the team is monitoring at once).
- *"Last edited by X 2 minutes ago"* indicators on documents and configurations.
- Live cursors and selections in any genuinely collaborative surface.
- *"Someone else is editing this"* indicators when conflict resolution would otherwise silently overwrite.

The design pattern: even in single-user-feeling features, expose presence cues when relevant. A user who realizes their teammate is also editing the same setting will pause; a user who finds out *after* they overwrote each other's work won't return to the feature.

## Inclusive design

Short. The detail lives in [`accessibility.md`](accessibility.md).

In 2026, the floor for inclusive design has risen:

- `prefers-reduced-motion` — respect it.
- `prefers-contrast: more` — boost contrast on demand.
- `prefers-reduced-transparency` — ship opaque alternatives.
- Dynamic type — never lock pixel heights on text containers.
- RTL — design with logical inline-start/end, not physical left/right.
- High-contrast mode (Windows HCM) — use real `stroke` properties for borders, not 1px filled rectangles.

A design that ignores these signals isn't a 2026 design.

## Dated defaults to avoid

Patterns the model reaches for unprompted that read as already-aged:

- **Glassmorphism overuse.** A blurred-translucent navbar plus blurred-translucent cards plus a blurred-translucent modal is three glass effects too many. Pick one place where the effect adds atmosphere; the rest are solid surfaces.
- **Neumorphism.** The soft-extruded-plastic look from 2020. Reads dated and accessibility-poor (low contrast by design).
- **Three-column equal-card "features" grids** as the default for any "benefits" or "features" section. Already an SKILL.md anti-pattern; restated here.
- **Parallax-on-everything.** Hero parallax is fine sparingly; parallaxing every section is exhausting and 2018.
- **Scroll-jacked storytelling.** Pages that hijack the user's scroll to "tell a story" frequently break native gestures, accessibility, and predictability. Reserve for genuine art-pieces; never for product onboarding.
- **Big floating round-rectangle search bars** centered in heroes. A 2022 SaaS-marketing default. Replace with a clear primary CTA.
- **Animated chevrons saying *"Scroll to explore"*.** Already in SKILL.md anti-patterns; restated for emphasis.
- **AI-typewriter effect on every AI response.** Discussed above; it's an AI tell, not an enhancement.
- **Gradient-on-everything.** Brand gradient on the hero, brand gradient on buttons, brand gradient on borders, brand gradient on text. Pick one place; let the rest be flat.
- **Background-blur-everywhere as "depth".** Real depth comes from proper elevation tokens (see `elevation.md`). Background blur is a *finishing* tool, not a foundational one.

## See also

- [`states.md`](states.md) — skeleton screens, loading taxonomy, optimistic-pending visuals.
- [`flows.md`](flows.md) — full real-time, optimistic UI, validation timing detail.
- [`accessibility.md`](accessibility.md) — `prefers-*`, RTL, dynamic type, HCM.
- [`chart-anatomy.md`](chart-anatomy.md) — chart build anatomy including data-viz colour guidance.
