# pencil-dev-skill

Teach your AI coding tool to design in [pencil.dev](https://pencil.dev). Works with Claude Code, Cursor, and Codex.

[![version](https://img.shields.io/badge/version-0.8.0_pre--release-orange)](https://github.com/Nisus74/pencil-skill/commits/main) [![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

> **Unofficial community plugin.** This project is not affiliated with or endorsed by the Pencil.dev team. For the Pencil editor, MCP server, and official documentation, visit [pencil.dev](https://pencil.dev). Issues with this skill belong in [this repo](https://github.com/Nisus74/pencil-skill); issues with the Pencil editor or MCP server belong with the Pencil.dev team.

[Star the repo](https://github.com/Nisus74/pencil-skill) if it helps you, or
[buy me a coffee or lunch](https://www.buymeacoffee.com/Nisus74) to support ongoing maintenance.

---

## What it does

Pencil.dev is a collaborative design tool for creating web and mobile interfaces via the Pencil MCP server. This skill teaches AI coding tools how to work with `.pen` design files.

- Guides the AI through a seven-step design workflow: detect host, orient, load guidelines, plan, execute, verify, report
- Teaches all 9 Pencil MCP tools with worked invocations, cost cheatsheet, and composite recipes
- Provides 2026 design depth: user flows, component and screen states, full accessibility coverage, and modern patterns (container queries, fluid type, AI-UI affordances)
- Ships 15 worked examples showing real MCP tool sequences from scratch
- Includes per-platform tool-name mappings so the same skill works everywhere

> **Status:** `0.8.0`, pre-release. Nothing is shipped until the owner cuts a release.

---

## What you'll be able to do

After installing this skill:

- **Generate complete UI designs** from natural language ("design a dashboard") without manual tool hunting
- **Speed up design iteration** by delegating pattern work to AI while you focus on unique decisions
- **Maintain design consistency** across components and screens
- **Work cross-platform** with the same skill on Claude Code, Cursor, or Codex
- **Customise the skill** for your team's workflow via folder copy or fork-and-install

---

## Prerequisites

You'll need three things:

1. **An AI coding tool:** [Claude Code](https://claude.ai/code), [Cursor](https://cursor.com), or [OpenAI Codex](https://openai.com/codex)
2. **Pencil MCP server:** Configure it in your tool ([how to set up Pencil](https://pencil.dev/docs/setup))
3. **A Pencil.dev workspace:** Create one free at [pencil.dev](https://pencil.dev) (no credit card required)

> **New to Pencil.dev?** It's a browser-based design tool. You don't install it; you open it in your browser and create `.pen` files there. This skill helps your AI tool work with those files.

---

## Install

**Most people want plugin install.** If you plan to customise the skill's instructions for your team, use folder copy or fork + install instead.

### Plugin install (recommended)

**Claude Code:** add the marketplace, then install the plugin. This lets you pin and update through the marketplace commands.

```bash
/plugin marketplace add Nisus74/pencil-skill
/plugin install pencil-dev-skill@pencil-dev-skill
```

**Cursor 2.5+:** in the editor, run `/add-plugin` and point it at `github.com/Nisus74/pencil-skill`.

**Codex:** add the marketplace, then install the plugin. Codex reads the same `.claude-plugin/marketplace.json` the repo ships.

```bash
codex plugin marketplace add Nisus74/pencil-skill
codex plugin add pencil-dev-skill@pencil-dev-skill
```

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

### Fork + install

Available for Claude Code, Cursor, and Codex.

1. Fork [Nisus74/pencil-skill](https://github.com/Nisus74/pencil-skill) on GitHub.
2. Install your fork as a plugin:
   - Claude Code: `/plugin marketplace add <your-handle>/pencil-skill`, then `/plugin install pencil-dev-skill@pencil-dev-skill`
   - Cursor: `/add-plugin` pointing at `github.com/<your-handle>/pencil-skill`
   - Codex: `codex plugin marketplace add <your-handle>/pencil-skill`, then `codex plugin add pencil-dev-skill@pencil-dev-skill`
3. Edit your fork, commit, and push. The next plugin update pulls your changes.
4. To pull upstream changes, rebase your fork against `Nisus74/pencil-skill`.

For Copilot CLI, use folder copy. The end result is the same; you just don't get an automatic update path.

### Install Methods Comparison

| | One command | Edit freely | Auto-updates |
|---|---|---|---|
| **Plugin install** | yes | no | yes |
| **Folder copy** | yes | yes | manual |
| **Fork + install** | yes (after forking) | yes | yes (after rebasing) |

> **Note:** Don't edit files inside a plugin install directory. The next update overwrites them. To customise the skill itself, use folder copy or fork + install.

---

## Usage

Once installed, the skill activates automatically when you describe a pencil.dev task:

- *"Design a login screen in pencil"*
- *"Open my .pen file and show me the layout"*
- *"Generate a dashboard UI in pencil.dev"*
- *"Use the pencil MCP to update the button colour"*
- *"Edit the pencil design and change the header"*

The AI will handle opening files, reading your design system, generating components, and even taking screenshots to verify the work.

---

## Customising the skill

The skill content (`SKILL.md`, the references, the worked examples) tells the AI how to work. To rewrite it for your team's workflow, use folder copy or fork-and-install. Editing files inside a plugin install directory won't stick — the next update overwrites them.

---

## Getting help

**Questions?** Open a [GitHub issue](https://github.com/Nisus74/pencil-skill/issues/new) or check the [Q&A discussions](https://github.com/Nisus74/pencil-skill/discussions).

**Bug report?** Include the exact prompt you used, what you expected, and what happened instead. Screenshots help.

**Want to contribute?** Read [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) for the full guide. Short version: fork, branch from `main`, make your change, run the pre-commit checks, open a PR with before/after examples.

---

## Repository Layout

The substance of this project is platform-agnostic. Platform-specific files exist only as install adapters:

```
skills/pencil-design/
  SKILL.md                          # Core skill — YAML frontmatter + instructions
  references/                       # 50 reference files loaded on demand
    mcp-tools.md                    # Cookbook for all 9 MCP tools
    batch-design-grammar.md         # batch_design JavaScript API reference
    pen-schema.md                   # .pen file schema reference (v2.14)
    advanced-canvas.md              # Shader fills, mesh gradients, script nodes, arcs/donuts, prompt/context
    pencil-cli.md                   # Full Pencil CLI reference + When CLI vs MCP table
    states.md                       # Component states + screen fault states
    flows.md                        # Screen transitions (modal, validation, back-stack)
    accessibility.md                # ARIA, focus, RTL, prefers-*, dynamic type
    modern-patterns.md              # Container queries, fluid type, AI-UI, perceived perf
    component-anatomy.md            # Reading component structure: slots, descendants, states
    visual-hierarchy.md, layout-patterns.md, typography.md,
    colour-palettes.md, font-pairings.md, data-viz.md, …  # Design-depth references
    style-catalogue.md, industry-patterns.md, …           # Menu-style catalogues
    amplify.md, pare.md, trim.md, soften.md, …            # Sub-command references
    codex-tools.md                  # Codex tool name mappings
  design-system/                    # Optional design-system reference templates (one level deep)
    README.md                       # Agent loading guide
    CUSTOMISING.md                  # Plain-English guide for non-technical editors
    accessibility.md, empty-states.md, file-architecture.md,
    forms.md, micro-interactions.md, navigation.md,
    onboarding.md, search.md, visual-style.md
  examples/                         # 15 worked examples with real MCP sequences (one level deep)
    example-login-screen.md
    example-dashboard.md
    example-marketing-page.md
    example-form-flow.md
    (and 11 more)
  evals/
    evals.json

AGENTS.md                           # Canonical project context (cross-platform)
tools/
  skill-lint.py                     # OWASP agentic skills lint (CI + pre-commit)
  test_skill_lint.py                # Lint unit tests
.claude-plugin/
  plugin.json                       # Claude Code plugin manifest
  marketplace.json                  # Claude Code marketplace listing
.cursor-plugin/plugin.json          # Cursor plugin manifest
.codex-plugin/plugin.json           # Codex plugin manifest
```

See [AGENTS.md](./AGENTS.md) for the full developer guide.

---

## License

MIT. See [LICENSE](./LICENSE).
