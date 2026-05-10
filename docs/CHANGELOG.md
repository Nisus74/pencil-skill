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

## [2.1.0] - 2026-05-10

Minor release: **opinionated design-system scaffolds**. The 16 markdown templates that get copied into user projects (`assets/design-system/*.md`) are no longer generic placeholders. Each file now leads with concrete decisions, references the shipped archetype library, and includes "what generic looks like" anti-examples to short-circuit AI defaults.

### Changed

- **`assets/design-system/patterns.md`** restructured. Each page-level pattern (marketing landing, pricing, settings, dashboard, list+detail, auth, onboarding, empty state) gains an *Archetype variants* subsection citing populated archetypes plus a *What generic looks like* anti-example. The rewrite shape was approved before applying it across the rest of the folder.
- **`assets/design-system/voice.md`** rewritten. Each section (tone, case, buttons, errors, empty states, numbers/dates) gains archetype-keyed variants and explicit anti-patterns. The forbidden-words table extended with severity-2 AI clichés (leverage, robust, foster, holistic, transformative, streamline-without-specifics).
- **`assets/design-system/components.md`** rewritten. Adds a "Component variants by archetype" section showing how Button, Card, Sidebar, Empty state, Status pill, Avatar reshape under each populated archetype.
- **`assets/design-system/tokens.md`** rewritten. Each section (colour, spacing, typography, border radius) carries an *Archetype-keyed bundles* subsection with concrete values per archetype, replacing the generic `<#hex>` placeholders for the projects that match a shipped archetype.
- **`assets/design-system/motion.md`** rewritten. Adds a "Motion personality by archetype" table mapping archetypes (analytics-dashboard, modern-pro-tool, conversion-focused-saas, editorial-storytelling) to motion strategies.
- **`assets/design-system/states.md`** rewritten. Adds archetype-keyed visual recipes; notes that Linear-style optimistic updates rarely show loading states; cleans up table cells (the `not-applicable` glyph is now an empty cell rather than an em dash).
- **`assets/design-system/brand.md`** rewritten. Brand voice and product voice section extended with how brand shows up in each archetype.
- **`assets/design-system/data-viz.md`** rewritten. Adds an "Archetype-keyed chart styles" section. analytics-dashboard is the canonical chart archetype; modern-pro-tool keeps charts inline and small; marketing archetypes show data as editorial moments.
- **`assets/design-system/imagery.md`** rewritten. Adds archetype-keyed imagery direction. Linear-style marketing uses product screenshots as the primary visual treatment; analytics-dashboard uses minimal imagery.
- **Tier 3 (`README.md`, `design-system.md`, `layout.md`, `elevation.md`, `iconography.md`, `mobile.md`, `code-export.md`)** received targeted updates: archetype-keyed variant subsections where applicable, cross-references to the archetype library, em-dash sweep applied. `design-system.md` gains a new *Chosen archetype* field for projects that have committed to one. `README.md` gains a *Working with archetypes* section explaining the precedence rule.
- **Plugin manifests bumped to `2.1.0`** across all three platforms.

### Migration notes

- These files are scaffold templates copied into user projects on first scaffold. Existing projects that already have a `design-system/` folder won't see automatic updates; users can re-scaffold individual files or pull the new content selectively.
- The structure of each file is preserved so existing edits remain meaningful. The new content lives in additional sections (*Archetype variants*, *What generic looks like*) rather than replacing existing sections.

## [2.0.0] - 2026-05-10

Major release: **taste-first rework**. The skill no longer outsources aesthetic direction to the user's instinct. It now leads with explicit aesthetic commitment, ships an opinionated archetype library to use as defaults when the user is silent, and runs a single distinctiveness pass after compose to catch generic output before declaring done.

### Added

- **Archetype library** at `skills/pencil-design/assets/archetypes/`, organised into 7 surface categories (`marketing-websites/`, `saas-apps/{b2b,b2b2b,b2c}/`, `mobile/`, `editors-creative-tools/`, `ai-products/`, `e-commerce-content/`, `docs-onboarding/`). Each archetype is a concrete bundle of moves: typography, density, accent strategy, surface treatment, data display, microcopy, motion personality, anti-cues, worked example, and notes for AI implementers. Top-level `assets/archetypes/README.md` indexes the library and encodes the *defaults-not-prescriptions* principle. Each category folder ships its own README with a "picking between them" decision table.
- **Four shipped archetypes** populated in v2.0.0:
  - `saas-apps/b2b/analytics-dashboard.md`, data-led overview surfaces (Mixpanel / Amplitude / PostHog flavour).
  - `saas-apps/b2b/modern-pro-tool.md`, refined-dense pro software (Linear / Notion business flavour); refined directly from Linear app screenshots.
  - `marketing-websites/conversion-focused-saas.md`, monumental confident marketing where the marketing IS product-caliber (Linear / Stripe / Vercel flavour); drafted from direct review of linear.app marketing pages.
  - `marketing-websites/editorial-storytelling.md`, long-form narrative surfaces; covers both philosophical-manifesto (Linear Method) and cinematic-product-narrative (Apple) flavours.
- **Five stub category READMEs** (`marketing-websites/` partial, `saas-apps/b2b2b/`, `editors-creative-tools/`, `e-commerce-content/`, `docs-onboarding/`) that lock in the folder structure and list planned archetypes for v2.x.
- **`references/distinctiveness-checklist.md`**, the 8-question taste pass that runs once at workflow step 6, with explicit kill-switch rules (skips on *"go fast"*, exits after one revision round). Each question has fail-mode examples and a worked example showing how today's generic SaaS dashboard would score against it.
- **`references/reference-ingestion.md`**, concrete contract for per-session references (screenshots, named brands, URLs, prose, existing design files); explicit precedence rule (per-session always overrides shipped); promotion path for graduating ephemerals into the shipped library.

### Changed

- **`SKILL.md` restructured around taste-first flow.** New 7-step default workflow integrates aesthetic commitment as step 2 (after host detection and context location) and the taste pass as step 6 (combined with accessibility verification). All discipline rules (naming, context, components-first, themes, responsive, accessibility, design completeness) preserved verbatim. The former "Aesthetic defaults" section is now "Aesthetic foundation" with explicit precedence: user direction > project design-system > shipped archetype > negative-space defaults.
- **Anti-patterns list expanded** with the override note explaining when archetypes can opt back into a banned move (e.g., `modern-pro-tool` and `conversion-focused-saas` both opt into the Inter family because Linear uses Inter Display deliberately).
- **Reference index** updated to include the two new reference files and the archetype library.
- **Plugin manifests bumped to `2.0.0`** across all three platforms (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`).

### Migration notes

- Existing users adopting v2.0.0 don't need to change their projects; the new archetype-led flow is additive. The old defaults still fire when the user is silent on aesthetics, the difference is that the agent now *names* the chosen archetype (or synthesises an ephemeral) instead of defaulting silently.
- Projects with a populated `design-system/` folder continue to take precedence over shipped archetypes per the new precedence rule.
- The `assets/design-system/` scaffolds (`brand.md`, `patterns.md`, `tokens.md`, etc.) are scheduled for an opinionated rewrite in a follow-up `2.0.x` release; they remain unchanged in `2.0.0`.

### Coming in v2.0.x and v2.x

- Remaining 12 archetypes across populated categories (`saas-apps/b2b` 2 more, `saas-apps/b2c` 4, `mobile/` 4, `ai-products/` 4, plus 2 more `marketing-websites/` archetypes).
- Stub categories (`saas-apps/b2b2b/`, `editors-creative-tools/`, `e-commerce-content/`, `docs-onboarding/`) populated in v2.x as references accumulate.
- `assets/design-system/` scaffold rewrites, each file rewritten from generic template to opinionated baseline with archetype-keyed variants.

## [1.4.0] - 2026-05-03

### Added

- **Five new on-demand references** filling the largest gaps in design knowledge and tool-surface coverage:
  - `references/mcp-tools.md`, cookbook for all 13 Pencil MCP tools (including the four previously undocumented ones: `get_variables`, `set_variables`, `search_all_unique_properties`, `replace_all_matching_properties`), the eight `get_guidelines` categories with a "for task X load category Y" decision table, composite recipes (token audit, greenfield bootstrap, library smoke test), and a tool-cost cheatsheet
  - `references/states.md`, component states (default/hover/focus/pressed/disabled/loading/error/success/skeleton/empty/partial-failure) and screen-level fault states (404/403/500/503/408/429/offline/partial-failure), plus the four-kind empty-state taxonomy (first-use / no-results / no-permission / post-action)
  - `references/flows.md`, what happens *between* screens: modal-vs-page-vs-sheet decisions, sync/async/submit-time form validation, multi-step wizards, the back-stack model (web vs mobile), confirmations and undo, optimistic UI, real-time/presence flows, deep links, and "plausible content" guidance
  - `references/accessibility.md`, beyond the SKILL.md 5-point baseline: ARIA semantics, focus order, keyboard navigation, screen-reader content, deeper-cut contrast (gradients, text on photos), `prefers-reduced-motion`, `prefers-contrast`, `prefers-reduced-transparency`, `forced-colors`, dynamic type, RTL & internationalization, motor accessibility, verification checklist
  - `references/modern-patterns.md`, patterns the model under-uses by default: container queries, fluid type with `clamp()`, AI-UI affordances (disclosure, regenerate, confidence, citations, abort), perceived performance (skeleton, optimistic UI, LQIP, staggered reveal), modern dark-mode handling; plus dated AI defaults to avoid (glassmorphism overuse, three-card grids, parallax-everything, scroll-jacked storytelling)
- **`references/pencil-cli.md` expanded** from a 29-line cautionary note to a full reference (~150 lines): install & runtime, agent vs interactive modes, every flag grouped by purpose, `pencil status` / `pencil login` walkthroughs, headless / CI workflows with a GitHub Actions example, auth troubleshooting, a load-bearing "When CLI vs MCP" decision table, and what each surface can/can't do that the other can't. The no-auto-fall-back policy is preserved verbatim
- **One new design-system scaffold:** `assets/design-system/states.md`, project-level state contract (per-component state coverage matrix, visual recipes, screen-level state coverage by archetype, empty-state copy variants). Brings the core scaffold count from 11 to 12 templates
- **Two new worked examples:**
  - `assets/examples/example-error-screen.md`, designing a 404 + offline pair with a shared `ErrorBlock` lockup; exercises `get_variables`/`set_variables`, `find_empty_space_on_canvas`, sibling top-level frames, and library-candidate surfacing
  - `assets/examples/example-form-flow.md`, multi-step signup with email verification across three sibling frames; exercises validation states via `descendants` overrides on `Input`, the focused-with-error edge case, and a confirmation step with a different lockup
- **SKILL.md surgical edits** (~25 lines net add, total stays under 400):
  - New "Design completeness" mini-section under Discipline rules pointing at `states.md` / `flows.md` / `accessibility.md`
  - Three new bullets under "Design intelligence: when to deviate", error/empty screens load `states.md`; multi-step flows load `flows.md`; container-queries / fluid-type / AI-UI / "modern" patterns load `modern-patterns.md`; less-used MCP tools load `mcp-tools.md`
  - Default workflow step 3 now links to `mcp-tools.md` § `get_guidelines` for the eight-category decision table
  - Accessibility rule footer points to `accessibility.md` for the deeper cut
  - Reference index expanded with all new files; design-system convention block updated to include `states.md` as a 12th core template

### Changed

- Plugin and skill versions bumped to `1.4.0`
- The 8 `get_guidelines` categories (Code, Design System, Landing Page, Mobile App, Slides, Table, Tailwind, Web App) are now enumerated in `mcp-tools.md` with explicit decision shortcuts. The skill instructs agents to call `get_guidelines()` with no args first to discover the live list, treating the documented set as guidance rather than a closed enumeration

## [1.3.0] - 2026-05-03

### Changed

- **Verification reframed as structural-first, visual-last** to reduce screenshot-driven token consumption. Previous guidance defaulted to `get_screenshot` after every chunk and mandated a dual-mode (light + dark) re-screenshot for every design. Both have been replaced with a four-rung **verification ladder**:
  1. `batch_design` response, confirms ops succeeded (free)
  2. `snapshot_layout`, confirms structural intent (numbers; cheap)
  3. `batch_get`, confirms property-level intent (JSON; cheap)
  4. `get_screenshot`, confirms visual intent (image; expensive, reserve for genuinely-visual questions or final sign-off, always scoped to the most specific `nodeId`)
- **Dual-mode screenshotting is now conditional**, not mandatory: only re-screenshot the alternate theme mode when the design uses mode-conditional colors that may have been set with raw hex instead of variables. Designs built entirely from variables get the variable system's correctness guarantee for free.
- **`snapshot_layout` repositioned** as the default verification tool (previously framed as a niche structural debugger)
- **"Edit the X" deviation** updated to prefer `snapshot_layout` / `batch_get` over a screenshot when the change is structural or property-level
- New `### Worked example: a 6-op edit, zero pre-final screenshots` subsection in SKILL.md illustrates the ladder end-to-end on a typical edit
- Plugin and skill versions bumped to `1.3.0`

### Added (evals)

- Eval 0 (`login-screen-greenfield`) and eval 2 (`import-library-and-use`), assertions extended to require the verification-ladder description and conditional dual-mode screenshotting
- New eval 3 (`edit-existing-card-verification-ladder`), execution-based eval where the model actually invokes MCP tools to perform a small edit and must explain its verification choices; pass criteria include at most one `get_screenshot` call in the edit phase, scoped to the affected subtree (not the document root)

## [1.2.0] - 2026-05-03

### Added

- **Documented three previously-undocumented MCP tools** that were in the permissions block but missing from the workflow:
  - `snapshot_layout`, explained as the structural complement to `get_screenshot`; guidance on when to use each (pixels vs. numbers), added to the Verification section
  - `find_empty_space_on_canvas`, added to Design Intelligence as the required step before placing frames on a populated canvas, to prevent invisible overlaps
  - `export_nodes`, added to Design Intelligence with guidance on when to use it vs. `get_screenshot`, and what to ask the user before calling

### Changed

- Plugin and skill versions bumped to `1.2.0`

## [1.1.0] - 2026-05-03

### Added

- **OWASP Agentic Skills Top 10 compliance** (AST01–AST10):
  - `tools/skill-lint.py`, Python lint covering AST01 (dangerous patterns), AST03 (permissions), AST04 (metadata), AST05 (safe deserialization), AST10 (cross-manifest consistency); reusable `Finding` type, exit-non-zero on errors only
  - `tools/test_skill_lint.py`, 31 unit tests covering every check function
  - `permissions:` block in `SKILL.md` frontmatter and mirrored in `.claude-plugin/plugin.json` and `gemini-extension.json` (AST03, AST04, AST10)
  - `.pre-commit-config.yaml` running skill-lint + gitleaks + basic hygiene, all repos pinned to immutable SHAs (AST08)
  - `.github/workflows/skill-lint.yml` running pre-commit + unit tests on push and PR (AST08)
  - `.github/CODEOWNERS` requiring owner review on every PR (AST09)
  - `.github/dependabot.yml` opening grouped weekly bumps for `github-actions` and `pip` so SHA pins stay fresh (AST07)
  - `tools/requirements.txt` for Dependabot's pip ecosystem
  - `docs/SECURITY.md`, OWASP AST risk → control table and malicious-update reporting section
  - `docs/CONTRIBUTING.md`, Security Checks section explaining the lint and exemption mechanism

### Changed

- All GitHub Actions `uses:` pinned to 40-char SHAs with `# vX.Y.Z` comments (AST02, AST07)
- PR template requires contributor confirmation that `pre-commit run --all-files` passes
- `AGENTS.md` CI/Hooks section updated to document the new workflow + pre-commit
- `.gitleaks.toml` simplified, empty `[allowlist]` block removed (gitleaks 8.x rejects it)
- Plugin and skill versions bumped to `1.1.0`

## [1.0.0] - 2026-05-03

### Added

- Full `pencil-design` skill content: mental model, default seven-step workflow, design intelligence, design-system convention, .lib.pen library guidance, batch_design grammar essentials, screenshot verification loop, and a six-case failure-mode runbook
- `design-system/` markdown convention for user projects, with seven shippable templates in `skills/pencil-design/assets/design-system/` (`README.md`, `design-system.md`, `tokens.md`, `components.md`, `layout.md`, `voice.md`, `code-export.md`)
- New reference files (flat per agentskills.io spec): `pen-schema.md`, `batch-design-grammar.md`, `pencil-cli.md`, `example-login-screen.md`, `example-import-library.md`, `example-scaffold-system.md`
- Skill frontmatter conformance with the [Agent Skills standard](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata.version`. Description follows `superpowers:writing-skills` style, imperative, intent-focused, ≤200 words, no workflow summary
- Skill validated against the official `skills-ref validate` checker
- Eval workflow run via Anthropic's `skill-creator` plugin: 3 test prompts × with-skill / baseline subagents → graded → benchmark.json with delta. Results: with-skill 100%, baseline 23%, delta +77pp

### Changed

- Corrected `.pen` file format claim: `.pen` is JSON conforming to a published schema, not encrypted. `AGENTS.md`, `README.md`, and the skill body all updated. MCP-first guidance retained for schema validation, screenshot feedback, and live-editor sync
- Plugin description widened to mention design-system docs and `.lib.pen` libraries
- Plugin and skill versions bumped to `1.0.0`

### Fixed (live-test corrections)

- Width/height sizing syntax: bare-string form (`"fill_container"`, `"fit_content"`, `"fill_container(320)"`), not the older `{ sizing: ... }` object form, which the live server rejects with `expected one of: number, "$variable", sizing behavior...`
- Stroke schema: singular `fill` (not plural `fills`); the live server rejects `fills` and top-level `alignment` as unexpected properties
- All affected references and the SKILL.md failure-mode runbook updated

### Added (discipline rules)

New "Discipline rules (always apply)" section in SKILL.md covering six non-negotiable disciplines, plus matching template updates:

- **Naming:** every node gets a meaningful PascalCase, role-bearing name (no default `Frame` / `Group` / `Text`). The agent also audits and renames default-named layers proactively when reading existing files, issuing a `U` op in the same `batch_design` call where it's already touching that area.
- **Context:** every non-trivial node populates the Entity `context` field with one-sentence design intent, required for components, page-level frames, form fields, interactive elements. The agent also backfills missing context on existing nodes it reads, in passing.
- **Components first:** before building from primitives, the agent scans (1) the open document for `reusable: true` nodes and (2) every imported `.lib.pen` library, using `batch_get({ patterns: [{ reusable: true }] })` in both. When a matching component exists, instantiate via `ref` with optional `descendants` overrides. Building from primitives only when no matching component exists, when the user explicitly asks for a one-off, or when the need is genuinely different, and even then, surfaces the gap to the user.
- **Themes (light + dark):** every new document declares `themes: { mode: ["light", "dark"] }`; every color variable carries both values; verification re-screenshots under `theme: { mode: "dark" }`. `tokens.md` template now has Light/Dark columns plus `$focusRing`.
- **Responsive:** canonical breakpoints (mobile 390×844, tablet 768×1024, desktop 1440×900). Two patterns documented: per-breakpoint frames and fluid auto-layout. `layout.md` template updated with the table and pattern guidance.
- **Accessibility:** five non-negotiable verification checks, contrast ≥ AA in both modes, hit targets ≥ 44×44, color is never the only signal, semantic role-bearing names, every component covers default / hover / focus / active / disabled / loading / error states. `components.md` template updated with the state-coverage table and a11y role naming convention.

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
