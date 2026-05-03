# pencil-dev-skill

A platform-agnostic AI coding skill plugin that teaches AI coding tools how to work with
[pencil.dev](https://pencil.dev) design files (`.pen` format) via the Pencil MCP server.

Works with Claude Code, OpenAI Codex, Google Gemini CLI, GitHub Copilot CLI, and Cursor.

---

## What This Skill Does

- Guides the AI through reading and interpreting `.pen` design files safely
  (`.pen` files are encrypted — file tools cannot open them directly)
- Documents the Pencil MCP server tools and when to use each one
- Provides workflow patterns for generating and editing UI designs in pencil.dev
- Includes per-platform tool-name mappings so the same skill works everywhere

> **Status:** `v0.1.0` — placeholder skill. Full workflow content is being written.
> Watch [the repo](https://github.com/Nisus74/pencil-skill) to be notified when v1.0 ships.

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
skills/pencil-design/        # Platform-agnostic skill content (the real work)
AGENTS.md                    # Canonical project context (cross-platform)

.claude-plugin/plugin.json   # Required by Claude Code's installer
gemini-extension.json        # Required by Gemini CLI's installer
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
