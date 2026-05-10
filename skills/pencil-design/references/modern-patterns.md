# Modern patterns

Patterns the model under-uses by default. SKILL.md's discipline rules cover the perennials (themes, responsive, accessibility, naming). This file covers what's *currently* table stakes for shipping product UI in 2026 — patterns the model wouldn't reach for unprompted.

**What this file owns:** container queries (vs media queries), fluid type with `clamp()`, AI-UI affordances, perceived performance (skeleton, optimistic UI, LQIP, staggered reveal), modern dark-mode controls, defaults the model reaches for that are already dated.

**What this file does NOT own:** any of the topics it links into other references for tactical detail. It's the *index* for "what's missing from the AI default" — not a re-implementation of motion, flows, accessibility, or imagery.

## When to load this file

- The user names *modern*, *contemporary*, *2026-style*, *fluid*, *container queries*, *AI UI*, *optimistic*, *real-time*, or *presence*.
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
