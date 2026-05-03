# pencil-dev-skill

A standalone AI coding skill plugin that teaches Claude Code, Cursor, OpenAI Codex,
and Google Gemini CLI how to work with [pencil.dev](https://pencil.dev) design files
(`.pen` format) via the Pencil MCP server.

---

## What This Skill Does

- Guides the AI through reading and interpreting `.pen` design files safely (they are encrypted — file tools cannot open them)
- Documents the Pencil MCP server tools and when to use each one
- Provides workflow patterns for generating and editing UI designs in pencil.dev
- Includes platform-specific tool-name mappings for Codex, Gemini CLI, and Copilot CLI

> **Status:** `v0.1.0` — placeholder skill. Full workflow content is being written.
> Follow [the repo](https://github.com/Nisus74/pencil-skill) to be notified when v1.0 ships.

---

## Prerequisites

1. An AI coding tool installed:
   - [Claude Code](https://claude.ai/code)
   - [Cursor](https://cursor.com)
   - OpenAI Codex CLI
   - Google Gemini CLI
2. Pencil MCP server configured in your environment
3. A pencil.dev project with `.pen` files

---

## Installation

### Claude Code

```bash
/plugin install github:Nisus74/pencil-skill
```

Or add to your project's `.claude/settings.json`:

```json
{
  "plugins": [
    { "source": "github", "repo": "Nisus74/pencil-skill" }
  ]
}
```

### Cursor

Same as Claude Code — Cursor reads `.cursor-plugin/plugin.json` from the installed plugin.

### Gemini CLI

Add to your Gemini configuration:

```json
{
  "extensions": [
    { "source": "github", "repo": "Nisus74/pencil-skill" }
  ]
}
```

### OpenAI Codex

Codex natively discovers skills from the `skills/` directory — no extra installation step needed once the plugin is available in your environment.

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

## Contributing

Contributions are welcome — bug reports, workflow improvements, and new trigger phrases all help.

Please read [CONTRIBUTING.md](./docs/CONTRIBUTING.md) before opening a PR.

---

## License

MIT — see [LICENSE](./LICENSE)
