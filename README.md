# pencil-dev-skill

Teach your AI coding tool to design in [pencil.dev](https://pencil.dev). Works with Claude Code, Cursor, and Codex.

[![version](https://img.shields.io/badge/version-0.8.0_pre--release-orange)](https://github.com/Nisus74/pencil-skill/commits/main) [![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

> **Unofficial community plugin.** This project is not affiliated with or endorsed by the Pencil.dev team. For the Pencil editor, MCP server, and official documentation, visit [pencil.dev](https://pencil.dev). Issues with this skill belong in [this repo](https://github.com/Nisus74/pencil-skill); issues with the Pencil editor or MCP server belong with the Pencil.dev team.

[Star the repo](https://github.com/Nisus74/pencil-skill) if it helps you, or
[buy me a coffee or lunch](https://www.buymeacoffee.com/Nisus74) to support ongoing maintenance.

---

## What it does

- Guides the AI through a seven-step design workflow: detect host, orient, load guidelines, plan, execute, verify, report
- Teaches all 13 Pencil MCP tools with worked invocations, cost cheatsheet, and composite recipes
- Provides 2026 design depth: user flows, component and screen states, full accessibility coverage, and modern patterns (container queries, fluid type, AI-UI affordances)
- Includes 25 scaffold templates (12 core + 13 optional) that users copy into their project: `tokens.md`, `components.md`, `layout.md`, `voice.md`, `navigation.md`, `forms.md`, and more
- Ships 16 worked examples showing real MCP tool sequences from scratch
- Includes per-platform tool-name mappings so the same skill works everywhere

> **Status:** `v1.11.0`, production-ready.

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

**Claude Code:** two install paths, pick either.

Direct install:

```bash
/plugin install github:Nisus74/pencil-skill
```

Or via the marketplace listing (lets you pin and update via marketplace commands):

```bash
/plugin marketplace add github:Nisus74/pencil-skill
/plugin install pencil-dev-skill
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

For Codex and Copilot CLI, use folder copy. The end result is the same; you just don't get an automatic update path.

---

## Customising the skill

Two parts can be customised.

The **design-system files** in [skills/pencil-design/assets/design-system/](skills/pencil-design/assets/design-system/) are starting points. The skill copies them into your project (typically at `docs/design/`), and you edit those copies to match your brand. They live with your code, so plugin updates never touch them; plugin install is fine here. If you're not a developer or designer, [CUSTOMISING.md](skills/pencil-design/assets/design-system/CUSTOMISING.md) walks you through each file in plain English.

The **skill content** (`SKILL.md`, the references, the worked examples) tells the AI how to do its work. To rewrite it for your team's workflow, pick folder copy or fork-and-install. Editing it inside a plugin install will be wiped on the next update.

For example: if you want the AI to use your brand's colour tokens, plugin install is enough. The AI copies `tokens.md` into your project, and you change the values there. To make the AI follow a different design workflow, you're editing `SKILL.md` itself, so pick folder copy or fork-and-install.

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
    design-system/                  # 25 scaffold templates (12 core + 13 optional)
      README.md                     # Agent loading guide
      CUSTOMISING.md                # Plain-English guide for non-technical editors
      tokens.md, components.md, layout.md, patterns.md,
      voice.md, navigation.md, forms.md, code-export.md, states.md, …
    examples/                       # 16 worked examples with real MCP sequences
      example-login-screen.md
      example-dashboard.md
      example-marketing-page.md
      example-form-flow.md
      (and 12 more)

AGENTS.md                           # Canonical project context (cross-platform)
.claude-plugin/plugin.json          # Required by Claude Code's installer
gemini-extension.json               # Required by Gemini CLI's installer
```

See [AGENTS.md](./AGENTS.md) for the full developer guide.

---

## Contributing

Read [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) for the full guide.

Short version: fork, branch from `main`, make your change, run the pre-commit checks, open a PR with before/after examples.

---

## License

MIT. See [LICENSE](./LICENSE).
