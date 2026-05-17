# pencil-dev-skill

A platform-agnostic AI coding skill plugin that teaches AI coding tools how to work with
[pencil.dev](https://pencil.dev) design files (`.pen` format) via the Pencil MCP server.

Works with Claude Code, OpenAI Codex, Google Gemini CLI, GitHub Copilot CLI, and Cursor.

[Star the repo](https://github.com/Nisus74/pencil-skill) if it helps you, or
[buy me a coffee or lunch](https://www.buymeacoffee.com/Nisus74) to support ongoing maintenance.

---

## What This Skill Does

- Guides the AI through a seven-step design workflow: detect host, orient, load guidelines, plan, execute, verify, report
- Teaches all 13 Pencil MCP tools with worked invocations, cost cheatsheet, and composite recipes
- Provides 2026 design depth: user flows, component + screen states, full accessibility coverage, and modern patterns (container queries, fluid type, AI-UI affordances)
- Includes 12 design-system scaffold templates users copy into their project (`tokens.md`, `components.md`, `layout.md`, `states.md`, …)
- Ships 5 worked examples showing real MCP tool sequences from scratch
- Includes per-platform tool-name mappings so the same skill works everywhere

> **Status:** `v1.4.0`, production-ready.

---

## Prerequisites

1. An AI coding tool. Any of these will do:
   - [Claude Code](https://claude.ai/code)
   - [OpenAI Codex CLI](https://openai.com/codex)
   - [Google Gemini CLI](https://github.com/google-gemini/gemini-cli)
   - [GitHub Copilot CLI](https://github.com/github/gh-copilot)
   - [Cursor](https://cursor.com)
2. Pencil MCP server configured in that tool
3. A pencil.dev project with `.pen` files

---

## Installing

This skill is a folder of Markdown files. Your AI coding tool reads them when you ask it to design something in pencil.dev. There are three ways to install it.

| | One command to install | Edit freely | Future updates |
|---|---|---|---|
| **Plugin install** | yes | no | automatic |
| **Folder copy** | one command | yes | manual re-download |
| **Fork and install** | yes, after forking | yes | automatic, after rebasing |

Most people want the plugin install. If you plan to rewrite the skill's instructions for your team, pick folder copy or fork-and-install instead.

> Don't edit files inside the plugin install directory; the next update will overwrite them. To customise the skill itself, use folder copy or fork-and-install.

---

### Plugin install

**Claude Code:**

```bash
/plugin marketplace add Nisus74/pencil-skill
/plugin install pencil-dev-skill@pencil-skill
```

**Google Gemini CLI:** add this to your Gemini config:

```json
{
  "extensions": [
    { "source": "github", "repo": "Nisus74/pencil-skill" }
  ]
}
```

**Cursor 2.5 or newer:** in the editor, run `/add-plugin` and point it at `github.com/Nisus74/pencil-skill`. Cursor reads [.cursor-plugin/plugin.json](.cursor-plugin/plugin.json) at the repo root.

**OpenAI Codex and GitHub Copilot CLI:** no plugin installer. Use the folder copy below.

---

### Folder copy

Download the [skills/pencil-design/](skills/pencil-design/) folder and drop it into the skills directory your AI tool reads.

Quickest method:

```bash
npx degit github:Nisus74/pencil-skill/skills/pencil-design <target>/pencil-design
```

Or with `git`:

```bash
git clone --depth=1 https://github.com/Nisus74/pencil-skill.git /tmp/pencil-skill
cp -r /tmp/pencil-skill/skills/pencil-design <target>/pencil-design
```

Where `<target>` lives, by tool:

| Tool | For all your projects | For one project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Google Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| OpenAI Codex | `~/.codex/skills/` | (use the user-level path) |
| GitHub Copilot CLI | `~/.copilot/skills/` | `.github/skills/` |
| Cursor | (no shared option) | `.cursor/skills/` |

Gemini CLI and Copilot CLI also accept `~/.agents/skills/` and `.agents/skills/` as cross-tool aliases. Cursor reads `AGENTS.md` from a project root, so dropping the skill folder into your project repo also gives Cursor the context.

To update later, re-run the same `degit` or `cp` command. If you've edited the files locally, diff and merge by hand.

---

### Fork and install

Available wherever plugin install is available: Claude Code, Gemini CLI, and Cursor.

1. Fork [Nisus74/pencil-skill](https://github.com/Nisus74/pencil-skill) on GitHub.
2. Install your fork as a plugin:
   - Claude Code: `/plugin marketplace add <your-handle>/pencil-skill` then `/plugin install pencil-dev-skill@pencil-skill`
   - Gemini CLI: change `repo` in your extension config to `<your-handle>/pencil-skill`
   - Cursor: `/add-plugin` and point to `github.com/<your-handle>/pencil-skill`
3. Edit your fork. Commit and push; the next plugin update pulls your changes in.
4. To pull upstream changes later, rebase or merge `Nisus74/pencil-skill` into your fork.

For Codex and Copilot CLI, use folder copy. The end result is the same; you just don't get an automatic update path.

---

## Customising the skill

Two parts can be customised.

The **design-system files** in [skills/pencil-design/assets/design-system/](skills/pencil-design/assets/design-system/) are starting points. The skill copies them into your project (typically at `docs/design/`), and you edit those copies to match your brand. They live with your code, so plugin updates never touch them; plugin install is fine here.

The **skill content** (`SKILL.md`, the references, the worked examples) tells the AI how to do its work. To rewrite it for your team's workflow, pick folder copy or fork-and-install. Editing it inside a plugin install will be wiped on the next update.

For example: if you want the AI to use your brand's colour tokens, plugin install is enough. The AI copies `tokens.md` into your project, and you change the values there. To make the AI follow a different design workflow, you're editing `SKILL.md` itself, so pick folder copy or fork-and-install.

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

Contributions are welcome. Bug reports, workflow improvements, and new trigger phrases all help.

Please read [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) before opening a PR.

Security issues: see [docs/SECURITY.md](./docs/SECURITY.md).

---

## Support

I maintain this project outside of paid work. If it saves you time or helps you
build something useful, you are welcome to buy me a coffee or lunch.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Nisus74)

No pressure. Stars, issues, feedback, and pull requests also help a lot.

---

## License

MIT. See [LICENSE](./LICENSE).
