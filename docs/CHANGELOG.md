# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
