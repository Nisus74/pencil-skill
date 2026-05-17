# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] (0.8.0)

### Added

- **Core skill:** Seven-step design workflow (detect host, orient, load guidelines, plan, execute, verify, report)
- **MCP tool coverage:** All 13 Pencil MCP tools with worked invocations and composite recipes
- **Design depth:** User flows, component and screen states, full accessibility coverage, modern patterns (container queries, fluid type, AI-UI affordances)
- **15 worked examples:** Real MCP tool sequences covering login screens, imports, forms, dashboards, marketing pages, mobile apps, and data visualisation
- **Cross-platform support:** Platform tool-name mappings for Claude Code, Cursor, Codex CLI, Gemini CLI, Copilot CLI

### Platform Manifests

- `.claude-plugin/plugin.json` – Claude Code plugin manifest
- `.claude-plugin/marketplace.json` – Claude Code marketplace listing
- `.cursor-plugin/plugin.json` – Cursor 2.5 plugin manifest
- `.codex-plugin/plugin.json` – OpenAI Codex plugin manifest
- `gemini-extension.json` – Google Gemini CLI extension manifest

### Design References

- **Core references:** MCP tools, states, flows, accessibility, modern patterns, Pencil CLI, .pen schema, batch_design grammar
- **Aesthetic references:** Brand, product, typography, colour and contrast, UX writing
- **Structural references:** Layout, motion design, interaction design, component anatomy, composition patterns, file architecture, forms, interactions, visual hierarchy
- **Advanced references:** Cognitive load, heuristics scoring, delight, onboarding, extraction, industry patterns, data visualisation, style catalogue, colour palettes, font pairings, performance design, iteration patterns, iconography, microcopy, mobile patterns
- **Platform mappings:** Codex tools, Copilot CLI tools, Gemini CLI tools

### Design System Templates

- **Optional reference templates:** `accessibility.md`, `empty-states.md`, `file-architecture.md`, `forms.md`, `micro-interactions.md`, `navigation.md`, `onboarding.md`, `search.md`, `visual-style.md`

### Documentation

- `AGENTS.md` – Cross-platform canonical project context
- `HARNESSES.md` – Platform capability matrix and support comparison
- `CONTRIBUTING.md` – Contribution guidelines and skill authoring tips
- `SECURITY.md` – Security policy and OWASP AST compliance
- `CODE_OF_CONDUCT.md` – Contributor Covenant v2.0

### Quality Assurance

- `tools/skill-lint.py` – OWASP Agentic Skills Top 10 lint with 40+ unit tests
- Pre-commit hooks – Secret scanning (gitleaks), linting, formatting
- GitHub Actions – Automated CI for skill-lint and secret scanning
- `.pre-commit-config.yaml` – Local pre-commit gate configuration
