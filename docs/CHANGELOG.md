# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `.cursor-plugin/plugin.json`. Cursor 2.5 (released 2026-02-17) shipped a real plugin marketplace and manifest format, so Cursor users now get one-line install parity with Claude Code and Gemini CLI. The manifest mirrors the Claude one: same `name`, `version`, and `permissions` block.
- Cursor manifest enforcement in `tools/skill-lint.py`. The cross-manifest consistency check (AST10) now validates `.cursor-plugin/plugin.json` when present. Three new unit tests in `tools/test_skill_lint.py` cover matching, divergent, and missing-permissions cases.
- Three install paths in the `README.md`: plugin install (the one-liner), folder copy, and fork-and-install. Per-tool target directories listed for each. A new Customising section explains which path supports which kind of edit.
- `AGENTS.md` Platform Support table now shows plugin install and folder-copy targets per platform, with a short Deployment and customisation section underneath.

### Changed

- Cursor's plugin schema doesn't document a `permissions` field. The manifest carries one anyway so `tools/skill-lint.py` can enforce consistency across all three platforms; Cursor ignores the unknown field.

## [1.11.0] - 2026-05-09

### Added

Phase 5 of the world-class overhaul. The eval suite expands from 6 to 20 evals covering the skill's full surface. Plus an in-app review requirement for evaluation, and an explicit Pencil CLI deviation pointer in SKILL.md so the agent loads the CLI reference when the context is headless.

- **Fourteen new evals** appended to `evals/evals.json` (IDs 6 through 19):
  - `clarify-intent-before-designing` (id 6): open-ended request triggers three clarifying questions before any batch_design.
  - `shadow-and-color-architecture` (id 7): pricing card with two-role colour, layered shadow, hover increases contrast, nested radius child ≤ parent.
  - `form-design-discipline` (id 8): multi-field signup form with visible labels, on-blur validation, autocomplete attrs, mobile font-size ≥ 16px.
  - `compound-component-design` (id 9): Composer.Provider / Frame / Header / Input / Footer slot pattern; explicit variants over boolean props.
  - `marketing-page-archetypes` (id 10): marketing page that avoids the three-card grid; uses alternating image-text or bento; static testimonials.
  - `mobile-bottom-sheet-vs-modal` (id 11): correct sheet vs modal per use case; safe areas; tab bar ≤ 5 items; haptics.
  - `data-viz-dashboard` (id 12): chart picked per data shape; Okabe-Ito + Viridis; never pie > 5, 3D, or dual y-axes; sparklines inline.
  - `microcopy-quality` (id 13): error / empty / success / loading copy that guides the exit; action-specific button labels.
  - `reference-image-translation` (id 14): names layout pattern, extracts palette and type pairing, preserves vs deliberately changes, recreates with project tokens.
  - `industry-aware-saas` (id 15): developer-tools dashboard uses developer conventions; not fintech, healthcare, or e-commerce voice.
  - `iteration-rescue-too-busy` (id 16): diagnoses busyness; subtracts (not adds) to fix; the most common second-iteration failure.
  - `command-palette-pattern` (id 17): proper command-palette UI (search, grouped results, keyboard nav indicators, recent commands).
  - `file-architecture-cover-and-sections` (id 18): Cover frame at origin, section regions, hierarchical naming for multi-screen flows.
  - `saas-completeness-pressure-test` (id 19): full state coverage (empty / loading / error / no-permission / plan-restricted) plus admin surface.
- **`evals/README.md`** documenting the eval workflow and the in-app review requirement: programmatic grading catches structural patterns; design quality demands opening every `.pen` artifact in the Pencil app and checking visual hierarchy, token rendering in both modes, layered shadows, spacing rhythm, microcopy, component states, mobile safe areas, and accessibility patterns. Without the in-app review, an eval can pass programmatic assertions while shipping a visually broken design.
- **SKILL.md updates**:
  - New deviation pointer in `Design intelligence: when to deviate` for headless / CI / batch / scripted contexts: load `references/pencil-cli.md` when the user mentions `pencil` command, `@pencil.dev/cli`, headless workflows, or asks for design without opening the editor. Default policy stays no-auto-fall-back: when MCP isn't connected, stop and ask the user; only invoke the CLI when explicitly directed or the context is unambiguously headless.
  - `compatibility` field broadened to acknowledge headless workflows via `@pencil.dev/cli` alongside the MCP server, with a pointer to the When CLI vs MCP decision table.

### Changed

- Plugin and skill versions bumped to `1.11.0` (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `SKILL.md` frontmatter).

### Quality gates

- Em-dash count: 0 across all added lines.
- Australian English throughout new prose.
- No third-party AI skill citations anywhere in the repo.
- Eval `expected_output` strings cite the relevant references (forms.md, layout-patterns.md, microcopy.md, mobile-patterns.md, data-viz.md, industry-patterns.md, iteration-patterns.md, file-architecture.md, composition-patterns.md, modern-patterns.md, etc.) so a grader can trace each requirement to its canonical source.

## [1.10.0] - 2026-05-09

### Added

Phase 4 of the world-class overhaul. Eight new design-system templates (project-level commitments the user populates per project) and nine new worked examples. The templates round out the conditionally scaffolded Tier 2 set; the examples teach the agent the catalogue → MCP → tokens → designs flow across the most common surfaces.

- **Eight new design-system templates** (Tier 2, conditionally scaffolded):
  - `assets/design-system/forms.md` (112 lines): the project's form conventions. Validation timing (on-blur sync + on-submit cross-field/async; never on keystroke). Error display (inline, focus first error on submit, aria-describedby). Submit-state choreography (idempotency key, spinner-plus-label, preserve form values on failure). Save patterns by surface (autosave default; explicit save for billing/security). Mobile inputs (16px font-size to defeat iOS zoom, autocomplete, inputmode). Hit zones, multi-step forms, unsaved-changes warning, placeholder conventions, verification checklist.
  - `assets/design-system/accessibility.md` (108 lines): the project's a11y standards. WCAG 2.2 AA / APCA Lc 75 hybrid baseline. Focus ring spec, skip links, focus traps. Project-specific keyboard shortcuts table. Screen reader patterns (`role="status"` vs `role="alert"`, `aria-describedby` on form errors). `prefers-reduced-motion` honoured. Dynamic type and RTL commitments. Per-component accessibility table. Six-step verification checklist.
  - `assets/design-system/micro-interactions.md` (102 lines): per-interaction motion specs. Table of every common interaction with duration, easing, properties, and notes (button press, button hover, card hover, modal open/close, sheet drag-to-dismiss, toast in/out, page transition, tab switch, tooltip, skeleton shimmer, progress bar, focus ring, form field error, optimistic UI commit/rollback). Reduced-motion contract. Animation library commitment. GPU-only properties (transform + opacity). Don't-animate list.
  - `assets/design-system/empty-states.md` (92 lines): per-surface empty state catalogue. Visual lockup (illustration / title / description / CTA). Tables for each primary surface (Projects list, Inbox, Search, Settings) with all four empty kinds (first-use / no-results / no-permission / post-action). Copy rules. Illustration approach commitment.
  - `assets/design-system/onboarding.md` (142 lines): first-run experience pattern. Onboarding shape (sign-up to first action, or sign-up to guided onboarding to first action). With sample data vs blank slate routing. Step sequence. Welcome modal vs full-takeover. Coach marks usage. Loaded-with-suggestions. Sample-data realism rules. Skip and exit affordances. Save-progress-on-exit. Re-onboarding for changes. Mobile considerations. Accessibility. Verification checklist.
  - `assets/design-system/navigation.md` (147 lines): the project's primary navigation. Sidebar / top nav / hamburger / command-driven decision per surface and per breakpoint. Sidebar / top nav structure specs. Breadcrumbs, search placement, notifications, workspace switcher (multi-tenant). Mobile navigation (≤ 5 tabs). Hamburger drawer fallback. Sticky vs scrolling. Active-state visual treatment. Keyboard navigation. URL state. Notification badges. Verification checklist.
  - `assets/design-system/search.md` (125 lines): search shape (instant / submit / hybrid). Entry point (header search, command palette, dedicated page). Instant search debounce, minimum query length, results panel placement. Submit-driven search URL state. Suggestions vs results. Suggestion categories. Filters. Keyboard shortcuts. URL state. Empty results pattern. Performance. Accessibility.
  - `assets/design-system/file-architecture.md` (170 lines): the project's chosen `.pen` file structure. File set table (which `.pen` files exist, ownership per file, status). Naming convention. Hierarchical naming for flows (`[Area] / [Flow] / [Step] / [Screen] / [State] / [Breakpoint]`). Section regions per `.pen` (Cover, Source of Truth, Build Ready, UX States, Responsive, Exploration, Archive). Cover frame template. Status taxonomies (file-level + component-level). Source-of-truth designation. Library imports. What NOT to put in a `.pen`. Multi-`.pen` governance. AI-readiness as meta-principle. Completeness checklists by project type.
- **Nine new worked examples**:
  - `assets/examples/example-settings-page.md` (200 lines): settings page with sidebar nav, autosave defaults, explicit-save for Billing, validation, dirty state.
  - `assets/examples/example-dashboard.md` (199 lines): dashboard with KPI cards (top row), chart tile (middle), recent-activity table (bottom). KPI delta colour pairs with arrow shape per colour-blind safety.
  - `assets/examples/example-marketing-page.md` (226 lines): marketing page avoiding the three-card grid. Asymmetric hero, alternating image-text rows or bento features, three-tier pricing with highlighted Pro tier, avatar-grid testimonials, sitemap footer.
  - `assets/examples/example-mobile-app.md` (226 lines): mobile app home screen + Compose flow. Bottom tab bar with 4 tabs respecting safe areas. Full sheet for Compose with half/full detents. Keyboard avoidance, haptic feedback.
  - `assets/examples/example-data-visualization.md` (227 lines): multi-chart dashboard. Chart picked per data shape (line for revenue trend, horizontal bar for conversion by channel, heatmap for cohort, table for top customers). Okabe-Ito for categorical, Viridis for heatmaps. State coding pairs colour with shape.
  - `assets/examples/example-onboarding-flow.md` (242 lines): three-step onboarding (workspace name, role, sample-data choice). Stepper progress, skip on every step, persist progress on exit. Welcome screen optional.
  - `assets/examples/example-component-variants.md` (233 lines): complete Button family in `design-system.lib.pen`. Five variants (Primary / Secondary / Destructive / Ghost / IconOnly) × seven states each (Default / Hover / Focus / Pressed / Disabled / Loading / Error). Theme-axis state authoring. Loading-state choreography preserves width. Icon-only `aria-label` documented.
  - `assets/examples/example-pricing-table.md` (250 lines): three-tier pricing (Free / Pro / Team) with Pro highlighted. Coloured border + badge (the chosen pair; not all four treatments combined). Two-role colour. Layered shadow. Mobile stack puts Pro second.
  - `assets/examples/example-file-cover-and-sections.md` (312 lines): fresh `.pen` setup with Cover frame at canvas origin, section region anchors (Source of Truth / Build Ready / UX States / Exploration / Archive), hierarchical naming for multi-screen flows (`Customer / Billing / 02 / EnterPayment / Default / Desktop`).
- **SKILL.md additions**:
  - 9 new examples added to the Reference index.
  - `assets/design-system/` template count updated (12 core + 13 optional).

### Changed

- Plugin and skill versions bumped to `1.10.0` (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `SKILL.md` frontmatter).
- AGENTS.md structure listing updated to reflect the 8 new design-system templates and 9 new worked examples (16 total examples now).

### Quality gates

- Em-dash count: 0 across all new files.
- Australian English throughout new content.
- No third-party AI skill citations anywhere in the repo.
- Source-validation policy: examples cite only authoritative 2025/2026 references and real product exemplars; templates point to existing references in the pencil-design skill rather than inventing new claims.

## [1.9.0] - 2026-05-09

### Added

Phase 3 of the world-class overhaul. Eight new reference files (five principle-led, three catalogue-shaped) plus one new design-system template and one new worked example to complete the catalogue architecture end-to-end. Every rule cited to authoritative 2025/2026 sources per the source-validation policy.

- **Three new principle-led reference files**:
  - `references/mobile-patterns.md` (262 lines): safe areas with `env(safe-area-inset-*)` and `viewport-fit=cover`, bottom sheets vs modals decision criteria, sheet detents (peek / half / full / custom), pull-to-refresh expectations, swipe gestures (edge swipe vs row swipe), haptic feedback (success / selection / error / impact), tab bars (≤ 5 items, semantic order, Dynamic Type), iOS vs Android native conventions, FAB usage criteria, keyboard avoidance with accessory bar.
  - `references/iconography.md` (155 lines): stroke weight per context (1.5 / 2 / 1px), size relative to text (cap-height matching, 16 / 20 / 24 / 32px), icon-only vs paired patterns, semantic icon conventions (warning, error, success, info, lock, time, delete, edit, settings, favourite), decorative-vs-meaningful (`aria-hidden` vs accessible name), family consistency (Phosphor / Lucide / Material Symbols / Heroicons / Tabler / SF Symbols), custom icons matching optical weight at 24px base, Pencil's `icon_font` and `icon_image` node types.
  - `references/performance-design.md` (141 lines): network budgets (POST/PATCH/DELETE < 500ms; GET < 200ms above-fold), Core Web Vitals 2025 baseline (LCP < 2.5s; CLS < 0.1; INP < 200ms; INP replaced FID in March 2024), virtualisation for lists > 50 items, image optimisation (explicit width/height for CLS, AVIF / WebP / lazy-load, LQIP/blur-up, responsive `srcset`), font loading (preload critical, `font-display: swap`, subset to actual character range, self-host where possible), `<meta name="theme-color">` matching per mode, skeleton vs spinner choices, perceived performance patterns.
- **Three new catalogue-shaped reference files** (recipe menus, not value definitions):
  - `references/style-catalogue.md` (307 lines): 30+ named UI styles organised by family (Modernist, Expressive, Technical, Retro / Revival, Atmospheric, Hand-crafted). Each entry: mood, when to use, anti-pattern, sample component cues, real-world exemplars (Linear, Vercel, Stripe, Notion, Apple, Things, Cron, Raycast, Arc, Pitch, Cursor, Spotify, Discord, Aēsop, Glossier, Mailchimp, etc.). Includes picking shortcuts by industry.
  - `references/colour-palettes.md` (263 lines): 40+ palette *recipes* tagged by industry and mood. Each recipe names a neutral family + accent scale from established source systems (Tailwind v4, Radix Colors, IBM Carbon v11, Material 3, Apple HIG). The agent commits picks to `assets/design-system/tokens.md` and the `.pen` file's `variables` via `set_variables` MCP; designs reference `$tokens`, never literal hex.
  - `references/font-pairings.md` (217 lines): 30+ typography pairings across families (Sans + Mono, Sans + Sans, Serif + Sans, Display + Sans, Modern grotesque, Serif + Serif, Casual). Each entry: weights, mood, industry fit, anti-pattern, real-world exemplar, source (mostly Google Fonts; some Vercel Geist, GitHub Mona Sans, or commercial foundries with free alternatives).
- **Two expanded reference files**:
  - `references/industry-patterns.md` (416 lines): 8 industry families (SaaS, fintech, healthcare, e-commerce, creative tools, social, education, communication) with 15-20 rules per family. Each family: sub-categories, per-industry rules, anti-patterns, recommended catalogue picks (style + palette + fonts), exemplars. Plus the brutal-honesty completeness pressure tests for SaaS / Website / Mobile projects.
  - `references/data-viz.md` (229 lines): 25-chart selection matrix (sparkline, big-number, bar/horizontal/stacked/grouped/100% stacked, line, area / stacked area, scatter, bubble, heatmap, treemap, sankey, funnel, radar, gauge, progress, candlestick, boxplot, histogram, chord, ridgeline, network, choropleth) with data shape, ideal use case, failure mode, alternative for each. Colour-blind-safe palette recommendations (Okabe-Ito, ColorBrewer, Viridis). Dashboard tile shapes (KPI / chart / table). Default chart styling rules. Chart anti-patterns (3D, pie > 5 slices, dual y-axes, red-green only).
- **One new design-system template**:
  - `assets/design-system/visual-style.md` (93 lines): the project's chosen style identity. Records the picks from the three catalogues (style + palette recipe + font pairing), deviations from the catalogue defaults, contrast verification, colour-blind safety status. The agent reads this at the start of every greenfield design pass to constrain output to the chosen direction.
- **One new worked example**:
  - `assets/examples/example-style-selection.md` (292 lines): full workflow from user brief ('developer-tools dashboard, feel like Linear') through catalogue pick (Swiss / International + Linear Dark + Inter + JetBrains Mono), `tokens.md` population, `set_variables` MCP invocation, `visual-style.md` commitment, and starter component scaffolding. Demonstrates the catalogue → MCP → tokens → designs flow that the catalogue layer enables.
- **SKILL.md additions**:
  - Eight new deviation pointers in `Design intelligence: when to deviate` for mobile patterns, iconography, performance design, industry patterns, data viz, style catalogue, colour palettes, font pairings.
  - Eight new entries in the Reference index.
  - Reference to the new `example-style-selection.md` worked example.
  - `assets/design-system/` template count updated to mention `visual-style.md` (now 5 optional templates).

### Changed

- Plugin and skill versions bumped to `1.9.0` (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `SKILL.md` frontmatter).
- AGENTS.md structure listing updated to reflect the new references, the new design-system template, and the new worked example.
- Catalogue architecture clarified across `colour-palettes.md` and `font-pairings.md`: each catalogue is a *menu of recipes*, not a value source. Hex codes and font names live in `assets/design-system/tokens.md` (project-owned) and the `.pen` file's `variables` (mirrored via `set_variables`). Designs reference `$tokens`, never literal values from the catalogues.

### Quality gates

- Em-dash count: 0 across all new and extended files.
- Australian English throughout new content.
- No third-party AI skill citations anywhere in the repo.
- Source-validation policy applied: every catalogue entry and rule cited to authoritative 2025/2026 sources (Apple HIG, Material 3, WCAG 2.2, Refactoring UI, Linear, Vercel, Stripe, Tailwind, Radix Colors, IBM Carbon, Nielsen Norman Group, web.dev, Google Fonts, Klim Type Foundry, Pangram Pangram, Grilli Type, Okabe-Ito 2002, ColorBrewer 2.0, Viridis 2015, Tufte's *Visual Display of Quantitative Information*, Microcopy: The Complete Guide, Mailchimp Content Style Guide, Shopify Polaris, Atlassian Design System, Stripe Style Guide, ICU MessageFormat).

## [1.8.0] - 2026-05-09

### Added

Phase 2 of the world-class overhaul. Three new on-demand reference files filling depth gaps in layout selection, design rescue, and microcopy, plus extensions to states.md and flows.md for onboarding, settings, and search patterns. Every rule cited to authoritative 2025/2026 sources per the source-validation policy.

- **Three new on-demand reference files**:
  - `references/layout-patterns.md`: named layout patterns the agent picks from for marketing pages, dashboards, settings, list-detail screens, and empty pages. Hero variations (centred / split / asymmetric / full-bleed / minimal / bento), feature-section alternatives to the three-card grid (alternating image-text, bento, comparison table, single hero feature), pricing tables (three-tier / single-tier / usage-based / enterprise), testimonials (avatar grid / single hero / logo wall / video; never auto-rotating carousel), CTA sections, footer architectures, dashboard layouts (sidebar / top nav / three-column / command-driven), settings patterns (tabs / sidebar / search-driven), list-detail shapes (master-detail / three-column / modal / full-page), and empty-page templates. Real-world exemplars cited throughout (Linear, Stripe, Vercel, Notion, Apple, Things, Cron, Raycast, Arc).
  - `references/iteration-patterns.md`: failure-mode diagnoses and rescue recipes for the six most common iteration failures (too busy, too sparse, too generic / reads as AI, doesn't feel premium, hierarchy unclear, breakpoints don't hold). Each failure mode lists the specific levers to pull, in order of effect. The expanded four-question self-critique gate (with examples and tests for each question), the reference-image translation protocol (six-step process from naming the layout pattern to recreating without copying), and the three-iteration limit before stopping to ask the user.
  - `references/microcopy.md`: the voice and tone framework (formal-casual, serious-playful, calm-energetic axes), action-specific CTA patterns ('Save changes' beats 'Continue'), error message anatomy (state what happened + hint why + tell the user what to do next, never blame the user), empty state copy that frames the empty state as a beginning rather than a deficit, calibrated success copy (don't over-celebrate routine work), confirmation copy that restates the action ('Delete 12 items' not 'Confirm'), specific system status, named loading copy ('Fetching your projects' not 'Loading...'), and localisation considerations (avoid metaphors that don't travel, leave room for German and Russian, don't bake plurals into single strings).
- **`references/states.md` extended** with onboarding states (welcome, sample data, coach marks, loaded-with-suggestions), settings states (saved, saving, saved-just-now, dirty, validation, conflict), and a loading-state-timing cross-link to `interactions.md`.
- **`references/flows.md` extended** with onboarding flows (sign-up → first-action vs sign-up → guided onboarding → first-action; with sample data vs blank slate), settings flows (autosave default vs explicit-save for high-stakes; per-field vs form-level autosave), and search flows (instant vs submit-driven; results vs suggestions; empty results state; URL state).
- **SKILL.md additions**:
  - Three new deviation pointers in `Design intelligence: when to deviate` for layout patterns, iteration rescues, and microcopy.
  - Three new entries in the Reference index for the new files.
- **Source-validation policy applied** to every rule in the new and extended files. Authoritative 2025/2026 sources cited per file in a Sources section: Refactoring UI, Linear, Stripe, Vercel, Apple HIG, Material 3, WCAG 2.2, APCA, Nielsen Norman Group, Mailchimp Content Style Guide, Shopify Polaris, Atlassian Design System, Stripe Style Guide, Microcopy: The Complete Guide (Yifrah), and others.
- **Writing-style sweep** applied to all new content. Em-dash count: 0 across the new and extended files. Australian English throughout.

### Changed

- Plugin and skill versions bumped to `1.8.0` (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `SKILL.md` frontmatter).
- The Phase 1 (`1.7.0`) CHANGELOG entry no longer cites third-party skill repositories by name; references for skill design were inputs to the planning conversation, not material that needs to live in the repo.

## [1.7.0] - 2026-05-09

### Added

Phase 1 of the world-class overhaul. The skill now covers depth across five new domains while keeping `SKILL.md` lean (around 500 lines).

- **Five new on-demand reference files** filling major gaps in design craft:
  - `references/forms.md`: submit behaviour (Enter focused-if-single / last-if-many; ⌘+Enter for textarea), label patterns, validation timing (on-blur vs on-submit; never block keystrokes), error display (inline + focus first error + aria-describedby), input attributes (type / inputmode / autocomplete / name / autocapitalise / spellcheck), submit-state choreography (idempotency, password managers, 2FA paste), mobile inputs (16px to defeat iOS zoom, OTP autofill), hit zones, multi-step forms, unsaved-changes warnings, placeholder conventions.
  - `references/interactions.md`: keyboard everywhere (WAI-ARIA APG patterns by component), focus management (`focus-visible`, `focus-within`, focus traps, restore on dismissal), hit targets (≥24/44/48), loading state choreography (150–300ms show-delay, 300–500ms min-visible-time), ellipsis conventions (`Rename…`, `Saving…`, `Loading…`), destructive actions (confirmation OR undo, never both), URL as state, optimistic UI, tooltips, toasts, modals, selection patterns, native context menus.
  - `references/composition-patterns.md`: compound components vs boolean prop explosion (worked Composer example), generic state/actions/meta interface, explicit variants instead of boolean modes, slot anatomy (named by content not position; default vs required), descendants override discipline, component status workflow (`draft` / `ready` / `stable` / `needs-review` / `deprecated`), when to extract to `.lib.pen`, library-hygiene anti-patterns.
  - `references/visual-hierarchy.md`: the six levers (size, weight, colour, position, spacing, motion) and when to reach for which, primary/secondary/tertiary order, eye-flow patterns (F / Z / Gutenberg / centre-out), reading order = DOM order = focus order, whitespace as a tool (macro / micro / padding scales), composition principles (rule of thirds, golden ratio, optical centre vs geometric centre, visual weight balance, symmetry vs asymmetry, tension and resolution), density calibration per audience.
  - `references/file-architecture.md`: Cover frame template (owner / status / version / scope / links), section-region layout (`SourceOfTruth` / `BuildReady` / `UXStates` / `Responsive` / `Exploration` / `Archive`), hierarchical naming patterns (`[Area] / [Flow] / [Step] / [Screen] / [State] / [Breakpoint]`), file-level status taxonomy (Discovery → In design → Design review → Engineering review → Ready for build → In build → QA → Shipped → Deprecated), single-`.pen` vs multi-`.pen` decision tree, recommended file sets per project size (early / growing / large), what NOT to put in a `.pen` (research transcripts, full PRDs, inspiration boards), per-project-type completeness pressure tests for SaaS / Website / Mobile, AI-readiness as a meta-principle.
- **`references/modern-patterns.md` extended** with two new sections:
  - **Animation & motion.** Timing tables by interaction type (micro 100–150ms, state 200–300ms, page 300–500ms), GPU-accelerated properties only, never `transition: all`, loading-state flicker rule (150–300ms show-delay + 300–500ms min-visible-time), interruptible transitions, never autoplay, hover micro-pattern (`translateY(-2px) scale(1.01)`), reduced-motion contract.
  - **Modern UI affordances.** Command palette / `⌘+K` anatomy, slash commands, AI input affordances (sparkle icons, suggestion chips), streaming response patterns (cursor blink, abort control), attachment affordances (drag-and-drop, paperclip, paste images).
- **`references/accessibility.md` extended** with WCAG 2.2 / ISO/IEC 40500:2025 baseline (2.4.11 focus appearance, 2.5.7 dragging, 2.5.8 target size, 3.3.7 redundant entry, 3.3.8/9 accessible authentication), APCA as alternative contrast metric (`Lc 75 ~ AA` for body), ARIA live region patterns table (`role="status"` polite vs `role="alert"` assertive with use cases), expanded live-region examples (form error count on submit, loading state announcements, search results updated, real-time presence), app-level keyboard shortcuts subsection (discoverable via `?`, documented in UI, don't conflict with browser/OS, `⌘`/`Ctrl` per platform, common shortcut conventions table).
- **SKILL.md additions** (around 85 lines, total around 500):
  - New **File architecture** discipline rule covering Cover frame, section regions, and hierarchical naming.
  - New **annotation discipline** added to Context rule: annotate behaviour, not visual specs.
  - **Colour** expanded: two-role architecture (4–5 neutrals + 1–3 accents), hue tinting on non-neutral surfaces, interactions increase contrast (hover/focus carry *more* contrast than rest, never less), colour-blind safety.
  - **Typography** expanded: tabular numerics for columns, `text-wrap: balance` for headings, non-breaking spaces for unit pairs, optical sizing for variable fonts.
  - New **Shadows & elevation** subsection: layered shadows (ambient + direct, ≥2 layers), nested border-radius rule (child ≤ parent, concentric).
  - New **Optical precision** subsection: ±1–2px adjustments where the eye disagrees with the maths, icon-text contrast balance, optical centre vs geometric centre.
  - New **Content & microcopy** subsection: active voice, second person, title case, action-specific button labels, error messages guide the exit, empty state copy encourages and guides.
  - New **Self-critique gate** subsection: 60-second four-question gate before declaring done.
  - New deviation pointers in `Design intelligence: when to deviate` for: open-ended requests (clarify-intent protocol), forms, interactions, composition, visual hierarchy, file architecture.
- **Reference index in SKILL.md updated** to include all new and extended references.
- **Writing-style sweep** applied to all new content. Em-dash count: 0 across the new and extended files. Australian English throughout. Slop dictionary clean.

### Changed

- Plugin and skill versions bumped to `1.7.0` (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `SKILL.md` frontmatter).

## [1.6.0] - 2026-05-09

### Added

- `references/component-anatomy.md` and `assets/examples/example-component-deep-dive.md`: fills the gap between component discovery and component use. Adds a mandatory inspect-before-use step in SKILL.md, covers structure-reading, slot identification, descendant path syntax (including nested `/` paths), state activation, and the full read→understand→instantiate cycle with three instantiation patterns.

## [1.5.0] - 2026-05-09

### Changed

- Live MCP execution corrections to `batch-design-grammar.md`, `pen-schema.md`, `mcp-tools.md` (text uses `content` not `text`; `fill` required; `document` predefined binding; `placeholder: true` on top-level frames; `padding` array-only; `alignItems` start/centre/end only; `justifyContent` uses underscores; `fontWeight` string; fill types: colour/gradient/image/mesh_gradient; `stroke.align` valid; `stroke.fill` not plural; `group` supports layout; sizing constraints; common gotchas).
- SKILL.md and `mcp-tools.md` mandate `get_variables()` before token work; explain `replace: false` still clobbers values for keys passed; bootstrap only absent tokens.
- Eval coverage expanded to validate live execution discipline.

## [1.4.0] - 2026-05-03

### Added

- **Five new on-demand references** filling the largest gaps in design knowledge and tool-surface coverage:
  - `references/mcp-tools.md` — cookbook for all 13 Pencil MCP tools (including the four previously undocumented ones: `get_variables`, `set_variables`, `search_all_unique_properties`, `replace_all_matching_properties`), the eight `get_guidelines` categories with a "for task X load category Y" decision table, composite recipes (token audit, greenfield bootstrap, library smoke test), and a tool-cost cheatsheet
  - `references/states.md` — component states (default/hover/focus/pressed/disabled/loading/error/success/skeleton/empty/partial-failure) and screen-level fault states (404/403/500/503/408/429/offline/partial-failure), plus the four-kind empty-state taxonomy (first-use / no-results / no-permission / post-action)
  - `references/flows.md` — what happens *between* screens: modal-vs-page-vs-sheet decisions, sync/async/submit-time form validation, multi-step wizards, the back-stack model (web vs mobile), confirmations and undo, optimistic UI, real-time/presence flows, deep links, and "plausible content" guidance
  - `references/accessibility.md` — beyond the SKILL.md 5-point baseline: ARIA semantics, focus order, keyboard navigation, screen-reader content, deeper-cut contrast (gradients, text on photos), `prefers-reduced-motion`, `prefers-contrast`, `prefers-reduced-transparency`, `forced-colors`, dynamic type, RTL & internationalization, motor accessibility, verification checklist
  - `references/modern-patterns.md` — patterns the model under-uses by default: container queries, fluid type with `clamp()`, AI-UI affordances (disclosure, regenerate, confidence, citations, abort), perceived performance (skeleton, optimistic UI, LQIP, staggered reveal), modern dark-mode handling; plus dated AI defaults to avoid (glassmorphism overuse, three-card grids, parallax-everything, scroll-jacked storytelling)
- **`references/pencil-cli.md` expanded** from a 29-line cautionary note to a full reference (~150 lines): install & runtime, agent vs interactive modes, every flag grouped by purpose, `pencil status` / `pencil login` walkthroughs, headless / CI workflows with a GitHub Actions example, auth troubleshooting, a load-bearing "When CLI vs MCP" decision table, and what each surface can/can't do that the other can't. The no-auto-fall-back policy is preserved verbatim
- **One new design-system scaffold:** `assets/design-system/states.md` — project-level state contract (per-component state coverage matrix, visual recipes, screen-level state coverage by archetype, empty-state copy variants). Brings the core scaffold count from 11 to 12 templates
- **Two new worked examples:**
  - `assets/examples/example-error-screen.md` — designing a 404 + offline pair with a shared `ErrorBlock` lockup; exercises `get_variables`/`set_variables`, `find_empty_space_on_canvas`, sibling top-level frames, and library-candidate surfacing
  - `assets/examples/example-form-flow.md` — multi-step signup with email verification across three sibling frames; exercises validation states via `descendants` overrides on `Input`, the focused-with-error edge case, and a confirmation step with a different lockup
- **SKILL.md surgical edits** (~25 lines net add, total stays under 400):
  - New "Design completeness" mini-section under Discipline rules pointing at `states.md` / `flows.md` / `accessibility.md`
  - Three new bullets under "Design intelligence: when to deviate" — error/empty screens load `states.md`; multi-step flows load `flows.md`; container-queries / fluid-type / AI-UI / "modern" patterns load `modern-patterns.md`; less-used MCP tools load `mcp-tools.md`
  - Default workflow step 3 now links to `mcp-tools.md` § `get_guidelines` for the eight-category decision table
  - Accessibility rule footer points to `accessibility.md` for the deeper cut
  - Reference index expanded with all new files; design-system convention block updated to include `states.md` as a 12th core template

### Changed

- Plugin and skill versions bumped to `1.4.0`
- The 8 `get_guidelines` categories (Code, Design System, Landing Page, Mobile App, Slides, Table, Tailwind, Web App) are now enumerated in `mcp-tools.md` with explicit decision shortcuts. The skill instructs agents to call `get_guidelines()` with no args first to discover the live list, treating the documented set as guidance rather than a closed enumeration

## [1.3.0] - 2026-05-03

### Changed

- **Verification reframed as structural-first, visual-last** to reduce screenshot-driven token consumption. Previous guidance defaulted to `get_screenshot` after every chunk and mandated a dual-mode (light + dark) re-screenshot for every design. Both have been replaced with a four-rung **verification ladder**:
  1. `batch_design` response — confirms ops succeeded (free)
  2. `snapshot_layout` — confirms structural intent (numbers; cheap)
  3. `batch_get` — confirms property-level intent (JSON; cheap)
  4. `get_screenshot` — confirms visual intent (image; expensive — reserve for genuinely-visual questions or final sign-off, always scoped to the most specific `nodeId`)
- **Dual-mode screenshotting is now conditional**, not mandatory: only re-screenshot the alternate theme mode when the design uses mode-conditional colors that may have been set with raw hex instead of variables. Designs built entirely from variables get the variable system's correctness guarantee for free.
- **`snapshot_layout` repositioned** as the default verification tool (previously framed as a niche structural debugger)
- **"Edit the X" deviation** updated to prefer `snapshot_layout` / `batch_get` over a screenshot when the change is structural or property-level
- New `### Worked example: a 6-op edit, zero pre-final screenshots` subsection in SKILL.md illustrates the ladder end-to-end on a typical edit
- Plugin and skill versions bumped to `1.3.0`

### Added (evals)

- Eval 0 (`login-screen-greenfield`) and eval 2 (`import-library-and-use`) — assertions extended to require the verification-ladder description and conditional dual-mode screenshotting
- New eval 3 (`edit-existing-card-verification-ladder`) — execution-based eval where the model actually invokes MCP tools to perform a small edit and must explain its verification choices; pass criteria include at most one `get_screenshot` call in the edit phase, scoped to the affected subtree (not the document root)

## [1.2.0] - 2026-05-03

### Added

- **Documented three previously-undocumented MCP tools** that were in the permissions block but missing from the workflow:
  - `snapshot_layout` — explained as the structural complement to `get_screenshot`; guidance on when to use each (pixels vs. numbers), added to the Verification section
  - `find_empty_space_on_canvas` — added to Design Intelligence as the required step before placing frames on a populated canvas, to prevent invisible overlaps
  - `export_nodes` — added to Design Intelligence with guidance on when to use it vs. `get_screenshot`, and what to ask the user before calling

### Changed

- Plugin and skill versions bumped to `1.2.0`

## [1.1.0] - 2026-05-03

### Added

- **OWASP Agentic Skills Top 10 compliance** (AST01–AST10):
  - `tools/skill-lint.py` — Python lint covering AST01 (dangerous patterns), AST03 (permissions), AST04 (metadata), AST05 (safe deserialization), AST10 (cross-manifest consistency); reusable `Finding` type, exit-non-zero on errors only
  - `tools/test_skill_lint.py` — 31 unit tests covering every check function
  - `permissions:` block in `SKILL.md` frontmatter and mirrored in `.claude-plugin/plugin.json` and `gemini-extension.json` (AST03, AST04, AST10)
  - `.pre-commit-config.yaml` running skill-lint + gitleaks + basic hygiene, all repos pinned to immutable SHAs (AST08)
  - `.github/workflows/skill-lint.yml` running pre-commit + unit tests on push and PR (AST08)
  - `.github/CODEOWNERS` requiring owner review on every PR (AST09)
  - `.github/dependabot.yml` opening grouped weekly bumps for `github-actions` and `pip` so SHA pins stay fresh (AST07)
  - `tools/requirements.txt` for Dependabot's pip ecosystem
  - `docs/SECURITY.md` — OWASP AST risk → control table and malicious-update reporting section
  - `docs/CONTRIBUTING.md` — Security Checks section explaining the lint and exemption mechanism

### Changed

- All GitHub Actions `uses:` pinned to 40-char SHAs with `# vX.Y.Z` comments (AST02, AST07)
- PR template requires contributor confirmation that `pre-commit run --all-files` passes
- `AGENTS.md` CI/Hooks section updated to document the new workflow + pre-commit
- `.gitleaks.toml` simplified — empty `[allowlist]` block removed (gitleaks 8.x rejects it)
- Plugin and skill versions bumped to `1.1.0`

## [1.0.0] - 2026-05-03

### Added

- Full `pencil-design` skill content: mental model, default seven-step workflow, design intelligence, design-system convention, .lib.pen library guidance, batch_design grammar essentials, screenshot verification loop, and a six-case failure-mode runbook
- `design-system/` markdown convention for user projects, with seven shippable templates in `skills/pencil-design/assets/design-system/` (`README.md`, `design-system.md`, `tokens.md`, `components.md`, `layout.md`, `voice.md`, `code-export.md`)
- New reference files (flat per agentskills.io spec): `pen-schema.md`, `batch-design-grammar.md`, `pencil-cli.md`, `example-login-screen.md`, `example-import-library.md`, `example-scaffold-system.md`
- Skill frontmatter conformance with the [Agent Skills standard](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata.version`. Description follows `superpowers:writing-skills` style — imperative, intent-focused, ≤200 words, no workflow summary
- Skill validated against the official `skills-ref validate` checker
- Eval workflow run via Anthropic's `skill-creator` plugin: 3 test prompts × with-skill / baseline subagents → graded → benchmark.json with delta. Results: with-skill 100%, baseline 23%, delta +77pp

### Changed

- Corrected `.pen` file format claim: `.pen` is JSON conforming to a published schema, not encrypted. `AGENTS.md`, `README.md`, and the skill body all updated. MCP-first guidance retained for schema validation, screenshot feedback, and live-editor sync
- Plugin description widened to mention design-system docs and `.lib.pen` libraries
- Plugin and skill versions bumped to `1.0.0`

### Fixed (live-test corrections)

- Width/height sizing syntax: bare-string form (`"fill_container"`, `"fit_content"`, `"fill_container(320)"`) — not the older `{ sizing: ... }` object form, which the live server rejects with `expected one of: number, "$variable", sizing behavior...`
- Stroke schema: singular `fill` (not plural `fills`); the live server rejects `fills` and top-level `alignment` as unexpected properties
- All affected references and the SKILL.md failure-mode runbook updated

### Added (discipline rules)

New "Discipline rules (always apply)" section in SKILL.md covering six non-negotiable disciplines, plus matching template updates:

- **Naming:** every node gets a meaningful PascalCase, role-bearing name (no default `Frame` / `Group` / `Text`). The agent also audits and renames default-named layers proactively when reading existing files — issuing a `U` op in the same `batch_design` call where it's already touching that area.
- **Context:** every non-trivial node populates the Entity `context` field with one-sentence design intent — required for components, page-level frames, form fields, interactive elements. The agent also backfills missing context on existing nodes it reads, in passing.
- **Components first:** before building from primitives, the agent scans (1) the open document for `reusable: true` nodes and (2) every imported `.lib.pen` library — using `batch_get({ patterns: [{ reusable: true }] })` in both. When a matching component exists, instantiate via `ref` with optional `descendants` overrides. Building from primitives only when no matching component exists, when the user explicitly asks for a one-off, or when the need is genuinely different — and even then, surfaces the gap to the user.
- **Themes (light + dark):** every new document declares `themes: { mode: ["light", "dark"] }`; every color variable carries both values; verification re-screenshots under `theme: { mode: "dark" }`. `tokens.md` template now has Light/Dark columns plus `$focusRing`.
- **Responsive:** canonical breakpoints (mobile 390×844, tablet 768×1024, desktop 1440×900). Two patterns documented: per-breakpoint frames and fluid auto-layout. `layout.md` template updated with the table and pattern guidance.
- **Accessibility:** five non-negotiable verification checks — contrast ≥ AA in both modes, hit targets ≥ 44×44, color is never the only signal, semantic role-bearing names, every component covers default / hover / focus / active / disabled / loading / error states. `components.md` template updated with the state-coverage table and a11y role naming convention.

Workflow steps 3 (load guidelines + inventory components), 5 (execute), and 6 (verify) updated to reference the discipline rules inline.

## [0.2.0] - 2026-05-03

### Added

- Platform-agnostic project structure with `AGENTS.md` as canonical context
- Platform install adapters: `.claude-plugin/plugin.json` (Claude Code), `gemini-extension.json` (Gemini CLI)
- Placeholder `pencil-design` skill with full Pencil MCP tool reference
- Per-platform tool-name mapping references (Codex, Gemini, Copilot CLI)
- GitHub PR template, issue templates, and Discussions config
- gitleaks secret-scanning workflow on push and PR
- Comprehensive `.gitignore` with secret patterns (`.env`, `*.pem`, `*.key`, etc.)
- `.gitattributes` for cross-platform line-ending normalization
- Community health files in `docs/`: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`

### Changed

- `CLAUDE.md` reduced to a thin pointer to `AGENTS.md` for platform neutrality
- `gemini-extension.json` now points to `AGENTS.md` (eliminated separate `GEMINI.md`)
- Plugin description updated to be platform-neutral

### Removed

- `.cursor-plugin/` directory (was based on a non-existent Cursor format)
- `GEMINI.md` (consolidated into `AGENTS.md`)

## [0.1.0] - 2026-05-03

Initial repository setup. Skill content is a placeholder; the actual workflow
will be written in v0.2.0+.
