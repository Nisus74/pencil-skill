# pencil-dev-skill

Teach your AI coding tool to design in [pencil.dev](https://pencil.dev). Works with Claude Code, Cursor, and Codex.

[![version](https://img.shields.io/badge/version-1.4.0-blue)](https://github.com/Nisus74/pencil-skill/releases) [![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

⭐ [Star the repo](https://github.com/Nisus74/pencil-skill) if it saves you time.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Nisus74)

---

## What it does

- Runs a seven-step design workflow: detect host, orient, load guidelines, plan, execute, verify, report
- Covers all 13 Pencil MCP tools with worked invocations, a cost cheatsheet, and composite recipes
- Ships 2026 design depth: user flows, component and screen states, full accessibility coverage, and modern patterns (container queries, fluid type, AI-UI affordances)
- Includes 12 design-system scaffold templates you copy into your project. Tokens, components, layout, states, and more
- Provides 5 worked examples showing real MCP tool sequences from scratch

> **Status:** v1.4.0, production-ready.

---

## Prerequisites

1. One of: [Claude Code](https://claude.ai/code), [Cursor](https://cursor.com), or [OpenAI Codex](https://openai.com/codex)
2. The Pencil MCP server configured in that tool
3. A pencil.dev project with `.pen` files

---

## Install

Three ways to install. Plugin install is the right default.

| | One command | Edit freely | Auto-updates |
|---|---|---|---|
| **Plugin install** | yes | no | yes |
| **Folder copy** | yes | yes | manual |
| **Fork + install** | yes (after forking) | yes | yes (after rebasing) |

Most people want plugin install. If you plan to customise the skill's instructions for your team, use folder copy or fork + install instead.

> Don't edit files inside the plugin install directory. The next update overwrites them. To customise the skill itself, use folder copy or fork + install.

### Plugin install

**Claude Code:**

```bash
/plugin install github:Nisus74/pencil-skill
```

**Cursor 2.5+:** in the editor, run `/add-plugin` and point it at `github.com/Nisus74/pencil-skill`.

**Codex:** use folder copy below. The Codex public plugin directory isn't available yet for third-party plugins.

---

### Folder copy

Download [skills/pencil-design/](skills/pencil-design/) and drop it into the skills directory your tool reads.

Quickest method:

```bash
npx degit github:Nisus74/pencil-skill/skills/pencil-design <target>/pencil-design
```

Or with git:

```bash
git clone --depth=1 https://github.com/Nisus74/pencil-skill.git /tmp/pencil-skill
cp -r /tmp/pencil-skill/skills/pencil-design <target>/pencil-design
```

Where `<target>` lives:

| Tool | Path |
|------|------|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Cursor | `.cursor/skills/` |
| Codex | `~/.codex/skills/` |

To update, re-run the same `degit` or `cp` command. If you've edited the files locally, diff and merge by hand.

---

### Fork + install

Available for Claude Code and Cursor.

1. Fork [Nisus74/pencil-skill](https://github.com/Nisus74/pencil-skill) on GitHub.
2. Install your fork as a plugin:
   - Claude Code: `/plugin install github:<your-handle>/pencil-skill`
   - Cursor: `/add-plugin` pointing at `github.com/<your-handle>/pencil-skill`
3. Edit your fork, commit, and push. The next plugin update pulls your changes.
4. To pull upstream changes, rebase your fork against `Nisus74/pencil-skill`.

For Codex, use folder copy. Fork the repo, edit your fork, and re-run the copy command when you want to pull in your changes.

---

## Usage

Once installed, the skill activates automatically when you describe a pencil.dev task:

- *"Design a login screen in pencil"*
- *"Open my .pen file and show me the layout"*
- *"Generate a dashboard UI in pencil.dev"*
- *"Use the pencil MCP to update the button colour"*
- *"Edit the pencil design and change the header"*

---

## Customising

**Design-system files** live in [skills/pencil-design/assets/design-system/](skills/pencil-design/assets/design-system/). The skill copies them into your project (typically `docs/design/`), and you edit those copies to match your brand. Plugin updates never touch them, so plugin install is fine here.

**Skill content** (`SKILL.md`, references, worked examples) controls how the AI does its work. Rewrite it for your team using folder copy or fork + install. Anything inside the plugin install directory gets overwritten on the next update, so don't edit files there.

---

## Contributing

Read [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) for the full guide.

Short version: fork, branch from `main`, make your change, run the pre-commit checks, open a PR with before/after examples.

---

## License

MIT. See [LICENSE](./LICENSE).
