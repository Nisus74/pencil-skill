# pencil-dev-skill: Project Context

This is the canonical project-context file. All AI coding tools (Claude Code, OpenAI Codex,
Cursor, etc.) should read this file for project context. Platform-specific files (`CLAUDE.md`)
are thin pointers to this file.

---

## Project Purpose

This repository is a standalone, **platform-agnostic** AI coding skill plugin that teaches
AI coding tools how to work with [pencil.dev](https://pencil.dev) design files (`.pen` format)
via the Pencil MCP server.

**Core artifact:** `skills/pencil-design/SKILL.md`, the platform-agnostic skill content.
**Platform adapters:** `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and
`.codex-plugin/plugin.json` are the minimum files required by each platform's installer;
they exist only so users on those platforms can run a one-line install command. They are
not the substance of the project.

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
  SKILL.md                         # The skill — YAML frontmatter + instructions
  references/                      # On-demand references loaded by the skill
    mcp-tools.md                   # Cookbook for all 13 MCP tools + composite recipes
    states.md                      # Component states + screen-level fault states
    flows.md                       # Transitions between screens (modal, validation, back-stack)
    accessibility.md               # ARIA, focus order, RTL, prefers-*, dynamic type
    modern-patterns.md             # Container queries, fluid type, AI-UI, perceived perf
    pencil-cli.md                  # Full Pencil CLI reference + When CLI vs MCP table
    pen-schema.md                  # .pen file JSON schema reference
    batch-design-grammar.md        # batch_design op syntax (I/C/R/U/G/D/M)
    brand.md                       # Brand-register depth: anti-references, aesthetic lanes, palette strategies
    product.md                     # Product-register depth: density, surface, semantic colour, data typography
    typography.md                  # Reflex-reject fonts, pairing rules, scale, readability, OpenType moves
    color-and-contrast.md          # OKLCH theory, palette strategies, tinted neutrals, light + dark parity
    ux-writing.md                  # Buttons, errors, empty states, microcopy, AI cliché list to refuse
    layout.md                      # Grid systems, spatial rhythm strategies, register-specific spacing, the squint test
    motion-design.md               # Easing curves, durations, register-specific motion, reduced-motion
    interaction-design.md          # State design philosophy, register-specific state recipes, focus management depth
    cognitive-load.md              # Three load types, attention budget per surface, density-vs-familiarity
    heuristics-scoring.md          # Ten heuristics + 1–5 scoring rubric + composite-score interpretation
    delight.md                     # Signature moments, personality in functional moments, polish discipline
    onboard.md                     # Activation moment, three onboarding shapes, empty-states by user-state
    extract.md                     # Tokens/components/patterns extraction workflow, library lifecycle
    codex-tools.md                 # OpenAI Codex tool name mappings
  assets/
    design-system/                 # 12 scaffold templates — copy into any project
      README.md                    # Index + how to use
      design-system.md             # Top-level design system doc
      tokens.md                    # Color, spacing, type tokens
      components.md                # Component catalogue + state table
      layout.md                    # Grid, breakpoints, spacing
      patterns.md                  # Page-level templates (landing, dashboard, auth, …)
      voice.md                     # Copy tone + empty/error copy rules
      code-export.md               # Token export to CSS/Tailwind
      states.md                    # Per-component state matrix + screen fault coverage
    examples/                      # 4 worked examples with real MCP tool sequences
      example-login-screen.md      # Greenfield auth screen
      example-import-library.md    # Import .lib.pen library + instantiate components
      example-error-screen.md      # 404 + offline page pair
      example-form-flow.md         # Multi-step signup with email verification

# Platform install adapters (required by each platform's installer)
.claude-plugin/plugin.json         # Claude Code plugin manifest
.claude-plugin/marketplace.json    # Claude Code marketplace listing (single-plugin marketplace)
.cursor-plugin/plugin.json         # Cursor plugin manifest (Cursor 2.5+)
.codex-plugin/plugin.json          # Codex plugin manifest

# Project context files
AGENTS.md                          # This file — canonical, platform-agnostic
CLAUDE.md                          # Thin pointer to AGENTS.md (for Claude Code)
HARNESSES.md                       # Cross-platform skill capability matrix (frontmatter, directories, substitution)

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
  test_skill_lint.py               # 40 unit tests for skill-lint
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
| Cursor (2.5+) | `/add-plugin` pointing at `github.com/Nisus74/pencil-skill` (manifest at `.cursor-plugin/plugin.json`) | `.cursor/skills/` |
| OpenAI Codex | (public plugin directory coming soon — use folder copy for now) | `~/.codex/skills/` |

---

## Deployment and customisation

The full per-platform install instructions live in [README.md](./README.md#install). At a glance:

- **Plugin install** is the right default. Users editing only the design-system scaffolds are unaffected by `/plugin update`, because the skill copies those scaffolds out into the user's project (e.g. `docs/design/`).
- **Folder copy** suits users who want to own the skill files from day one. They edit anything, fetch updates by re-downloading and merging by hand.
- **Fork + install** suits users who want both: full edit access and an automatic update path. Install your fork as a plugin; rebase against upstream when you want changes.

Don't edit files inside a plugin install directory (e.g. `~/.claude/plugins/.../skills/pencil-design/`); the next `/plugin update` will overwrite them.

---

## Plugin System Rules

- The Claude Code plugin manifest MUST live at `.claude-plugin/plugin.json`
- The Claude Code marketplace listing MUST live at `.claude-plugin/marketplace.json`. This makes the repo installable via `/plugin marketplace add github:Nisus74/pencil-skill` followed by `/plugin install pencil-dev-skill`
- The Cursor plugin manifest MUST live at `.cursor-plugin/plugin.json` (Cursor 2.5+)
- The Codex plugin manifest MUST live at `.codex-plugin/plugin.json`
- All three plugin manifests MUST carry matching `name` and `version` fields (enforced by `tools/skill-lint.py`). The marketplace.json plugin entry should match these too
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

The plugin is currently pre-release and **holds at version `0.8.0`** across all four manifests. Don't bump the version without explicit owner approval. All in-flight work accumulates under `[Unreleased]` in `docs/CHANGELOG.md` until the owner decides to cut a release.

When a release is authorised, bump the `version` field in four places, keeping them in sync: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (inside the `plugins[]` entry), `.cursor-plugin/plugin.json`, and `.codex-plugin/plugin.json`. Follow semantic versioning:

- **PATCH** (`0.x.y`): Content fixes, typos, clarifications
- **MINOR** (`0.y.0`): New capability documented, new trigger phrases added
- **MAJOR** (`x.0.0`): Breaking restructuring of the skill workflow

After bumping, replace the `[Unreleased]` heading in `docs/CHANGELOG.md` with the new version and date.

---

## Testing the Skill Locally

**Claude Code:**
```bash
# From repo root
/plugin install .
# Then describe a pencil task; verify pencil-design skill triggers
```

**Codex:**
```bash
# Skills are auto-discovered from skills/ — no install step needed
```

---

## Links

- GitHub repo: https://github.com/Nisus74/pencil-skill
- pencil.dev: https://pencil.dev
- [HARNESSES.md](./HARNESSES.md): cross-platform skill capability matrix (frontmatter support, directory conventions, substitution syntax) — consult when adding a new platform manifest or auditing existing ones
