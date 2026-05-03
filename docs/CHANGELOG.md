# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [Unreleased]

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
