This repo doesn't have a `design-system/` folder yet. I have 12 core templates I can drop in — they teach me your tokens, components, voice, motion, patterns, and tech stack. I can also include optional ones for mobile (`mobile.md`), charts (`data-viz.md`), brand identity (`brand.md`), or imagery treatment (`imagery.md`). Want me to scaffold the core, plus any optional ones that fit your project?

---

*Assuming the user says yes (or says "scaffold everything" / "just do it"):*

---

Before copying files I'll scan the repo root for a few signals that tell me which optional files belong:

- `package.json` — does it list `react-native`, `expo`, `flutter`, or similar? That triggers `mobile.md`.
- Any `marketing/`, `www/`, or `landing/` directory, or multiple `landing.tsx` / `app.tsx` files? That triggers `brand.md` (and `imagery.md` alongside it, since they pair).
- Does the project clearly render charts — a `recharts`, `d3`, `chart.js`, or `victory` dependency? That triggers `data-viz.md`.

For a fresh repo with no signals in any of those places, I include the 4 optional files anyway with a "delete this file if your project doesn't ship this surface" note at the top of each — a user can delete a file in two seconds; reconstructing one they didn't know existed is harder.

## Files I create

All 16 files land at `./design-system/` in the project root. I copy them directly from the skill's bundled `assets/design-system/` templates. No content is generated from scratch — these are pre-authored templates the user fills in.

### Core (always scaffolded — 12 files)

| File | What it contains |
|------|-----------------|
| `design-system/README.md` | Entry point. Tells agents which file to read when, and explains the progressive-loading model. |
| `design-system/design-system.md` | Placeholder for the `.lib.pen` library path, tech stack (framework, component library, styling, build target), icon library choice, brand quick-reference, project constraints, theme axes. |
| `design-system/tokens.md` | Full token table: color variables with light + dark placeholders, spacing scale (`$space-0` through `$space-12`), type ramp (`$textXs` through `$text4xl`), font family slots (`$fontHeading`, `$fontBody`, `$fontMono`), border-radius scale. Rules inline (e.g. "every color uses a variable, never raw hex"). |
| `design-system/components.md` | Catalog template: when to reach for which component, what variants exist, when to build from primitives instead. Starts empty for the user to fill in from their `.lib.pen`. |
| `design-system/layout.md` | Auto-layout rules, sizing behavior (`fill_container` vs `fit_content`), page grid, canonical breakpoints (390/768/1440), content max-width, gutter and column-gap values. |
| `design-system/motion.md` | Duration scale, easing choices, what to animate and what not to (the "no parallax everywhere" rule lives here). |
| `design-system/elevation.md` | Shadow scale, how shadows degrade in dark mode (border fallback, glow fallback), which surface depth gets which shadow level. |
| `design-system/iconography.md` | Stroke weight, icon sizes per context (inline-with-label vs standalone vs hero), icon-only accessibility rule (44×44 hit target even at 16px icon), when to use `icon_font` vs import a custom SVG. |
| `design-system/patterns.md` | Page-level layout templates: marketing landing, settings page, dashboard shell, list+detail, auth, onboarding. Decisions only — not tutorials. |
| `design-system/states.md` | Per-component state coverage (default / hover / focus / pressed / disabled / loading / error / success / skeleton / empty / partial-failure) and screen-level fault states (404 / 403 / 500 / 503 / 408 / 429 / offline / partial-failure), plus the empty-state taxonomy (first-use / no-results / no-permission / post-action). |
| `design-system/voice.md` | Microcopy tone, error and empty-state copy templates, CTA patterns. Anti-patterns like "Elevate", "Seamless", "Revolutionize" are called out as banned defaults. |
| `design-system/code-export.md` | How Pencil concepts map to the chosen code stack — component naming conventions, how token variables translate to CSS custom properties or Tailwind config, how `icon_font` nodes map to the icon library import. |

### Optional (scaffolded based on project signals or user opt-in — 4 files)

| File | Triggered by |
|------|-------------|
| `design-system/mobile.md` | `react-native`, `expo`, `flutter` in `package.json`; iOS / Android folder; `Podfile` / `.xcodeproj`; or user says "mobile". Covers tab bar, sheets, safe areas, gestures, haptics. |
| `design-system/data-viz.md` | User opts in, or charting library detected in `package.json`. Covers chart palette, default chart types, dashboard tile shape. |
| `design-system/brand.md` | User opts in, or marketing surface detected (`marketing/`, `www/`, `landing/` folder; `next.config.js` with public routes). Covers logo lockups, clear space, OG / social imagery. |
| `design-system/imagery.md` | User opts in, or `brand.md` is being included, or the project is content-heavy. Covers photo / illustration style, aspect ratios, AI-imagery rules, avatar fallbacks. |

## What I tell the user after scaffolding

Once the files are written, I give a short orientation:

> Done. `design-system/` now has 12 core files (plus any optional ones you opted into). Everything is placeholder text — **the files are useful immediately for teaching me structure, but they won't shape my design choices until you fill in the angle-bracketed values.**
>
> The three most important files to fill in first:
>
> 1. **`design-system.md`** — add your `.lib.pen` path and tech stack. Without this I can't import your library or know what framework to target when generating code.
> 2. **`tokens.md`** — add your actual hex values and font choices. Until then I'll fall back to the skill's aesthetic defaults (Geist, Zinc neutrals, one low-saturation accent).
> 3. **`components.md`** — add entries for any components already in your `.lib.pen`. Until then I won't know what exists and may build from primitives instead of instantiating a component.
>
> Everything else (`voice.md`, `states.md`, `patterns.md`, etc.) can be filled in incrementally as you work. I re-read on every task, so changes take effect immediately — no cache to clear.
>
> If your project ends up not needing one of the optional files, just delete it.

## What I do NOT do

- I do not generate token values, color palettes, or font choices on the user's behalf during scaffolding. The templates ship with clear placeholders. Inventing values without the project's brand input would mean I'm immediately out of sync with the real design.
- I do not touch any existing files. If the folder already has source code (`.tsx`, `package.json`, etc.) I stop and ask where to put the docs instead.
- I do not ask twice in the same session if the user declines the scaffold offer.
- I do not create a `.lib.pen` file as part of scaffolding. That's a separate step the user takes in Pencil, or asks me to help with once the app structure is known.
