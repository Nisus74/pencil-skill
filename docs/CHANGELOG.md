# Changelog

All notable changes to this project will be documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] (0.8.0)

### Changed

- **Aligned the whole skill to the current Pencil MCP server (schema v2.14), verified against the live
  server.** The tool surface dropped from 13 to 9: `set_variables` and `find_empty_space_on_canvas`
  became the `SetVariables` and `FindEmptySpace` JavaScript functions inside `batch_design`;
  `open_document`, `search_all_unique_properties`, and `replace_all_matching_properties` were removed
  (bulk property work is now a `batch_get` + `Update`-loop pattern); `export_html` was added.
- **Rewrote `batch_design` documentation:** the op DSL is now a JavaScript snippet with full-word
  functions (`Insert`/`Copy`/`Update`/`Replace`/`Move`/`Delete`/`SetVariables`/`Generate`/`FindEmptySpace`)
  instead of the old single-letter `I/C/R/U/G/D/M` grammar. Bindings are per-call (no cross-call
  persistence); reference nodes by their returned literal id.
- **Schema corrections (v2.14):** icons are `type: "icon"` with `library`/`icon` (not `icon_font`);
  `stroke` is a fill value plus a separate `strokeWidth` (the old `{ color, thickness }` object is
  rejected); `group` has no own layout/size; the creatable node set excludes `line`/`connection`.
- Swept all references and 15 worked examples to the current API; updated frontmatter permissions to the
  real 9 tools.

### Added

- **New reference `advanced-canvas.md`:** v2.14 canvas capabilities, shader fills (WebGL fragment shaders
  with `@directive` uniforms), mesh-gradient fills (require an explicit `points` array), `script` nodes
  (`@input`-driven JavaScript generators), ellipse arcs/donuts (`innerRadius`/`startAngle`/`sweepAngle`),
  and the `prompt`/`context` node types.
- **Core skill:** Seven-step design workflow (detect host, orient, load guidelines, plan, execute, verify, report)
- **MCP tool coverage:** All 9 Pencil MCP tools with worked invocations and composite recipes
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
