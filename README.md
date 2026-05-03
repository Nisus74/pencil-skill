# pencil-dev-skill

A platform-agnostic AI coding skill plugin that teaches AI coding tools how to work with
[pencil.dev](https://pencil.dev) design files (`.pen` format) via the Pencil MCP server.

Works with Claude Code, OpenAI Codex, Google Gemini CLI, GitHub Copilot CLI, and Cursor.

---

## What This Skill Does

- Guides the AI through a seven-step design workflow — detect host, orient, load guidelines, plan, execute, verify, report
- Teaches all 13 Pencil MCP tools with worked invocations, cost cheatsheet, and composite recipes
- Provides 2026 design depth: user flows, component + screen states, full accessibility coverage, and modern patterns (container queries, fluid type, AI-UI affordances)
- Includes 12 design-system scaffold templates users copy into their project (`tokens.md`, `components.md`, `layout.md`, `states.md`, …)
- Ships 5 worked examples showing real MCP tool sequences from scratch
- Includes per-platform tool-name mappings so the same skill works everywhere

> **Status:** `v1.4.0` — production-ready.

---

## Prerequisites

1. An AI coding tool — any of:
   - [Claude Code](https://claude.ai/code)
   - [OpenAI Codex CLI](https://openai.com/codex)
   - [Google Gemini CLI](https://github.com/google-gemini/gemini-cli)
   - [GitHub Copilot CLI](https://github.com/github/gh-copilot)
   - [Cursor](https://cursor.com)
2. Pencil MCP server configured in that tool
3. A pencil.dev project with `.pen` files

---

## Installation

### Claude Code

```bash
/plugin install github:Nisus74/pencil-skill
```

### Google Gemini CLI

Add to your Gemini configuration:

```json
{
  "extensions": [
    { "source": "github", "repo": "Nisus74/pencil-skill" }
  ]
}
```

### OpenAI Codex / GitHub Copilot CLI

Both auto-discover skills from a `skills/` directory. Clone or symlink this repo
into your tool's skills path (consult your tool's docs for the exact location).

### Cursor

Cursor uses the Pencil MCP server natively — no plugin install needed. Once the
Pencil MCP server is configured in Cursor, the skill content in this repo can be
referenced as project context (Cursor reads `AGENTS.md` automatically when opened
as a workspace).

---

## Usage

Once installed, the skill activates automatically when you describe a pencil.dev task.
Example trigger phrases:

- *"Design a login screen in pencil"*
- *"Open my .pen file and show me the layout"*
- *"Generate a dashboard UI in pencil.dev"*
- *"Use the pencil MCP to update the button color"*
- *"Edit the pencil design and change the header"*

---

## Skills Included

| Skill | Trigger domain | Description |
|-------|---------------|-------------|
| `pencil-design` | pencil.dev / `.pen` files / Pencil MCP | Core workflow for `.pen` file design work |

---

## Repository Layout

The substance of this project is platform-agnostic. Platform-specific files exist
only as install adapters:

```
skills/pencil-design/
  SKILL.md                          # Core skill — YAML frontmatter + instructions
  references/
    mcp-tools.md                    # Cookbook for all 13 MCP tools
    states.md                       # Component states + screen fault states
    flows.md                        # Transitions between screens (modal, validation, back-stack)
    accessibility.md                # ARIA, focus, RTL, prefers-*, dynamic type
    modern-patterns.md              # Container queries, fluid type, AI-UI, perceived perf
    pencil-cli.md                   # Full Pencil CLI reference + When CLI vs MCP table
    pen-schema.md                   # .pen file schema reference
    batch-design-grammar.md         # batch_design op syntax reference
    (platform tool mappings)        # codex-tools.md, gemini-tools.md, copilot-tools.md
  assets/
    design-system/                  # 12 scaffold templates to copy into any project
      README.md, tokens.md, components.md, layout.md, patterns.md,
      voice.md, code-export.md, states.md, …
    examples/                       # 5 worked examples with real MCP sequences
      example-login-screen.md
      example-import-library.md
      example-scaffold-system.md
      example-error-screen.md
      example-form-flow.md

AGENTS.md                           # Canonical project context (cross-platform)
.claude-plugin/plugin.json          # Required by Claude Code's installer
gemini-extension.json               # Required by Gemini CLI's installer
```

See [AGENTS.md](./AGENTS.md) for the full developer guide.

---

## Contributing

Contributions are welcome — bug reports, workflow improvements, and new trigger phrases all help.

Please read [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) before opening a PR.

Security issues: see [docs/SECURITY.md](./docs/SECURITY.md).

---

## License

MIT — see [LICENSE](./LICENSE)
