# pencil-dev-skill: Project Context

This is the canonical project-context file. All AI coding tools (Claude Code, OpenAI Codex,
Google Gemini CLI, GitHub Copilot CLI, Cursor, etc.) should read this file for project
context. Platform-specific files (`CLAUDE.md`) are thin pointers to this file.

---

## Project Purpose

This repository is a standalone, **platform-agnostic** AI coding skill plugin that teaches
AI coding tools how to work with [pencil.dev](https://pencil.dev) design files (`.pen` format)
via the Pencil MCP server.

**Core artifact:** `skills/pencil-design/SKILL.md`, the platform-agnostic skill content.
**Platform adapters:** `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and
`gemini-extension.json` are the minimum files required by each platform's installer;
they exist only so users on those platforms can run a one-line install command. They
are not the substance of the project.

---

## Naming Conventions

Three names appear in this project, each scoped to a different layer:

| Name | Scope | Where it appears |
|------|-------|-----------------|
| `pencil-skill` | GitHub repo name | Repo URL, clone URL |
| `pencil-dev-skill` | Plugin package name | `plugin.json`, marketplace listings |
| `pencil-design` | Skill name | `SKILL.md` frontmatter, skill activation triggers |

This is intentional: the repo is the deliverable, the plugin is the package, and the
skill is the capability the AI invokes.

---

## Repository Structure

```
skills/pencil-design/              # The platform-agnostic core
  SKILL.md                         # The skill: YAML frontmatter + instructions (v1.10.0)
  references/                      # On-demand references loaded by the skill
    mcp-tools.md                   # Cookbook for all 13 MCP tools + composite recipes
    states.md                      # Component states + screen-level fault states + onboarding/settings states
    flows.md                       # Transitions between screens (modal, validation, back-stack, onboarding, settings, search)
    accessibility.md               # ARIA, focus order, APCA, ARIA live regions, keyboard shortcuts, WCAG 2.2
    modern-patterns.md             # Container queries, fluid type, AI-UI, animation timing, command palette, perceived perf
    pencil-cli.md                  # Full Pencil CLI reference + When CLI vs MCP table
    pen-schema.md                  # .pen file JSON schema reference
    batch-design-grammar.md        # batch_design op syntax (I/C/R/U/G/D/M)
    component-anatomy.md           # Reading component structure: slots, descendants paths, state activation
    composition-patterns.md        # Compound components, slot design, variant naming, status workflow
    file-architecture.md           # Cover frame, section regions, hierarchical naming, multi-.pen layouts
    forms.md                       # Submit behaviour, validation, error display, autofill, mobile inputs
    interactions.md                # Keyboard, focus, hit targets, loading timing, destructive actions, URL-as-state
    visual-hierarchy.md            # Six levers, eye-flow patterns, whitespace, density strategy
    layout-patterns.md             # Hero variations, feature sections beyond three-card grid, pricing, dashboards, settings, list-detail, empty pages (cited 2025/2026 exemplars)
    iteration-patterns.md          # Failure-mode rescues (too busy/sparse/generic/un-premium), self-critique gate, reference-image translation, three-iteration limit
    microcopy.md                   # Voice/tone framework, action-specific CTAs, error message anatomy, empty/success/confirmation copy, loading copy, localisation
    mobile-patterns.md             # Safe areas, sheets vs modals, sheet detents, gestures, haptics, tab bars, native conventions per platform
    iconography.md                 # Stroke weight, sizing, semantic icons, accessibility (aria-hidden vs accessible name), family consistency
    performance-design.md          # Network budgets, Core Web Vitals (LCP/CLS/INP), virtualisation, image and font optimisation, theme-color
    industry-patterns.md           # 8 industry families with 15-20 rules each + completeness pressure tests for SaaS / Website / Mobile
    data-viz.md                    # 25-chart selection matrix, colour-blind palettes (Okabe-Ito, ColorBrewer, Viridis), dashboard tiles, anti-patterns
    style-catalogue.md             # 30+ named UI styles (menu) organised by family with mood, when-to-use, anti-pattern, exemplars
    colour-palettes.md             # 40+ palette recipes (menu) tagged by industry/mood; recipes point to Tailwind/Radix/IBM Carbon/Material 3/Apple HIG
    font-pairings.md               # 30+ typography pairings (menu); recipes point to Google Fonts/Vercel/GitHub/commercial foundries
    codex-tools.md                 # OpenAI Codex tool name mappings
    gemini-tools.md                # Google Gemini CLI tool name mappings
    copilot-tools.md               # GitHub Copilot CLI tool name mappings
  assets/
    design-system/                 # 12 core + 13 optional scaffold templates: copy into any project
      README.md                    # Index + how to use
      design-system.md             # Top-level design system doc
      tokens.md                    # Colour, spacing, type tokens
      components.md                # Component catalogue + state table
      layout.md                    # Grid, breakpoints, spacing
      motion.md                    # Durations, easings, skeleton shimmer
      elevation.md                 # Shadow scale + dark-mode treatment
      iconography.md               # Stroke weight, sizes per context
      patterns.md                  # Page-level templates (landing, dashboard, auth, ...)
      states.md                    # Per-component state matrix + screen fault coverage
      voice.md                     # Copy tone + empty/error copy rules
      code-export.md               # Token export to CSS/Tailwind
      mobile.md                    # Optional: native-mobile patterns
      data-viz.md                  # Optional: chart palettes, default chart types
      brand.md                     # Optional: logo lockups, OG / social imagery
      imagery.md                   # Optional: photo / illustration style, AI-imagery rules
      visual-style.md              # Optional: project's chosen style identity (style + palette + font picks from references catalogues)
      forms.md                     # Optional: project's form conventions (validation timing, error display, save patterns by surface)
      accessibility.md             # Optional: project's a11y standards (WCAG / APCA target, keyboard shortcuts, screen reader patterns)
      micro-interactions.md        # Optional: per-interaction motion specs (button press, card hover, modal entrance, sheet drag, toast)
      empty-states.md              # Optional: per-surface empty state catalogue (first-use / no-results / no-permission / post-action) with copy templates
      onboarding.md                # Optional: first-run experience (sample-data vs blank slate, sequence, coach marks)
      navigation.md                # Optional: primary nav (sidebar / top / hamburger / command-driven), workspace switcher, mobile tab bar
      search.md                    # Optional: search shape (instant / submit / hybrid), suggestions, filters, URL state
      file-architecture.md         # Optional: project's chosen .pen file structure, naming conventions, status taxonomy
    examples/                      # 16 worked examples with real MCP tool sequences
      example-login-screen.md      # Greenfield auth screen
      example-import-library.md    # Import .lib.pen library + instantiate components
      example-scaffold-system.md   # Bootstrap a full design-system scaffold
      example-error-screen.md      # 404 + offline page pair
      example-form-flow.md         # Multi-step signup with email verification
      example-component-deep-dive.md # Full read→understand→instantiate cycle
      example-style-selection.md   # Catalogue (style + palette + fonts) → set_variables MCP → tokens commit → starter components
      example-settings-page.md     # Settings with sidebar nav, autosave + explicit-save for high-stakes
      example-dashboard.md         # KPI cards + chart tile + recent-activity table
      example-marketing-page.md    # Marketing page avoiding three-card grid (asymmetric hero, bento features)
      example-mobile-app.md        # Mobile app with bottom tab bar, sheet detents, safe areas, haptics
      example-data-visualization.md # Multi-chart dashboard with colour-blind-safe palettes
      example-onboarding-flow.md   # Three-step onboarding with progress, skip, sample-data routing
      example-component-variants.md # Complete Button family with all variants and states
      example-pricing-table.md     # Three-tier pricing with highlighted recommended tier
      example-file-cover-and-sections.md # .pen file with Cover frame, section regions, hierarchical naming

# Platform install adapters (required by each platform's installer)
.claude-plugin/plugin.json         # Claude Code plugin manifest
.cursor-plugin/plugin.json         # Cursor plugin manifest (Cursor 2.5+)
gemini-extension.json              # Gemini CLI extension manifest

# Project context files
AGENTS.md                          # This file — canonical, platform-agnostic
CLAUDE.md                          # Thin pointer to AGENTS.md (for Claude Code)

# Public-facing
README.md
LICENSE

# Repo hygiene
.gitignore                         # Includes secret patterns
.gitattributes                     # Cross-platform line-ending normalization
.gitleaks.toml                     # Secret-scanning config

# Quality tooling
tools/
  skill-lint.py                    # OWASP Agentic Skills Top 10 lint (CI + pre-commit)
  test_skill_lint.py               # 36 unit tests for skill-lint
  requirements.txt                 # pip deps for Dependabot

# Documentation
docs/
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  CHANGELOG.md

# GitHub repo configuration
.github/
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
  CODEOWNERS
  dependabot.yml
  workflows/
    secret-scan.yml                # gitleaks on push + PR
    skill-lint.yml                 # skill-lint + unit tests on push + PR
.pre-commit-config.yaml            # Local gate: skill-lint + gitleaks + hygiene
```

---

## Platform Support

| Platform | Plugin install | Folder-copy target |
|----------|---------------|-------------------|
| Claude Code | `/plugin install github:Nisus74/pencil-skill` (manifest at `.claude-plugin/plugin.json`) | `~/.claude/skills/` or `.claude/skills/` |
| Google Gemini CLI | `gemini-extension.json` at repo root | `~/.gemini/skills/` or `.gemini/skills/` (alias `.agents/skills/`) |
| Cursor (2.5+) | `/add-plugin` pointing at `github.com/Nisus74/pencil-skill` (manifest at `.cursor-plugin/plugin.json`) | `.cursor/skills/` (Cursor also reads `AGENTS.md` from project root) |
| OpenAI Codex | (no plugin manifest) | `~/.codex/skills/` |
| GitHub Copilot CLI | (no plugin manifest) | `~/.copilot/skills/` (alias `~/.agents/skills/`) or project `.github/skills/` |

All platforms also accept a `SKILL.md` in their respective skills directory; folder copy works universally.

---

## Deployment and customisation

The full per-platform install instructions live in [README.md](./README.md#installing). At a glance:

- **Plugin install** is the right default. Users editing only the design-system scaffolds are unaffected by `/plugin update`, because the skill copies those scaffolds out into the user's project (e.g. `docs/design/`).
- **Folder copy** suits users who want to own the skill files from day one. They edit anything, fetch updates by re-downloading and merging by hand.
- **Fork and install** suits users who want both: full edit access and an automatic update path. Install your fork as a plugin; rebase against upstream when you want changes.

Don't edit files inside a plugin install directory (e.g. `~/.claude/plugins/.../skills/pencil-design/`); the next `/plugin update` will overwrite them. The README spells this out for each path.

---

## Plugin System Rules

- The Claude Code plugin manifest MUST live at `.claude-plugin/plugin.json`
- The Cursor plugin manifest MUST live at `.cursor-plugin/plugin.json` (Cursor 2.5+)
- `gemini-extension.json` MUST live at the repo root (Gemini CLI requirement)
- All three platform manifests MUST carry a `permissions` block matching SKILL.md (enforced by `tools/skill-lint.py`)
- `skills/` MUST be at the repo root
- Each skill is a subdirectory under `skills/` containing one `SKILL.md`
- The YAML frontmatter `description` field controls when the skill activates, so edit it carefully
- Skills may have a `references/` subdirectory for supplementary docs loaded on demand

---

## The Pencil MCP Server

`.pen` files are JSON conforming to a published schema (`Document` with `version`,
`themes`, `imports`, `variables`, `children`). They are version-controllable like
any code file. While they can technically be read with file tools, **all reading
and writing in this project goes through the Pencil MCP server**. It gives you
schema validation, live screenshots, and stays in sync with the running editor:

| Tool | Purpose |
|------|---------|
| `get_editor_state` | Get current document state |
| `open_document` | Open a `.pen` file |
| `get_guidelines` | Retrieve design guidelines |
| `batch_get` | Read multiple nodes |
| `batch_design` | Write / modify design nodes |
| `snapshot_layout` | Capture layout state |
| `get_screenshot` | Visual screenshot of the design |
| `get_variables` | Read design tokens / variables |
| `set_variables` | Update design tokens / variables |
| `find_empty_space_on_canvas` | Locate available canvas space |
| `search_all_unique_properties` | Search across design properties |
| `replace_all_matching_properties` | Bulk-replace properties |
| `export_nodes` | Export nodes to external format |

---

## Writing the Skill

When writing or editing `skills/pencil-design/SKILL.md`:

1. The `description` frontmatter field is the trigger mechanism, so include exact phrases users say
2. Keep `SKILL.md` under ~5,000 words; move detailed references to `references/`
3. Use progressive disclosure: core workflow in `SKILL.md`, edge cases in `references/`
4. Always route `.pen` reads/writes through the Pencil MCP tools. Schema validation, screenshots, and live-editor sync depend on it
5. Document tool sequencing (e.g., call `get_editor_state` before `batch_design`)
6. Keep instructions **platform-agnostic**. Use generic verbs ("read", "write", "search")
   rather than tool names where possible. When tool names are necessary, default to the
   Claude Code names and rely on `references/<platform>-tools.md` for mappings.

---

## CI / Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `.github/workflows/secret-scan.yml` | push, PR | Runs gitleaks; blocks merge if secrets are detected |
| `.github/workflows/skill-lint.yml` | push, PR | Runs `tools/skill-lint.py` (OWASP Agentic Skills Top 10) and unit tests |
| `.pre-commit-config.yaml` | local `git commit` | Same skill-lint + gitleaks + basic hygiene; install with `pip install pre-commit && pre-commit install` |

The OWASP AST compliance map lives in [docs/SECURITY.md](./docs/SECURITY.md).

---

## Version Bumping

Follow semantic versioning. Bump the `version` field in three places, keeping them in sync: `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and the `skills/pencil-design/SKILL.md` frontmatter. (`gemini-extension.json` does not declare a version field.)

- **PATCH** (`0.1.x`): Content fixes, typos, clarifications
- **MINOR** (`0.x.0`): New capability documented, new trigger phrases added
- **MAJOR** (`x.0.0`): Breaking restructuring of the skill workflow

After bumping, add an entry to `docs/CHANGELOG.md`.

---

## Testing the Skill Locally

**Claude Code:**
```bash
# From repo root
/plugin install .
# Then describe a pencil task; verify pencil-design skill triggers
```

**Gemini CLI:**
```bash
# Install the extension; AGENTS.md loads automatically as project context
# Describe a pencil task; the skill activates via the description trigger
```

**Codex / Copilot CLI:**
```bash
# Skills are auto-discovered from skills/ — no install step needed
```

---

## Links

- GitHub repo: https://github.com/Nisus74/pencil-skill
- pencil.dev: https://pencil.dev
