# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
