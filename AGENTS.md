# pencil-dev-skill — Developer Guide

## Project Purpose

This repository is a standalone AI coding skill plugin that teaches Claude Code (and other
AI coding tools) how to work with [pencil.dev](https://pencil.dev) design files (`.pen` format)
via the Pencil MCP server.

**Plugin type:** Skill-only plugin (no slash commands, no agents, no hooks)
**Skill name:** `pencil-design`
**Skill trigger domain:** pencil.dev design tasks, `.pen` file manipulation, Pencil MCP usage
**Supported platforms:** Claude Code, Cursor, OpenAI Codex, Google Gemini CLI, GitHub Copilot CLI

---

## Repository Structure

```
.claude-plugin/plugin.json         # Claude Code plugin manifest
.cursor-plugin/plugin.json         # Cursor plugin manifest (identical to Claude Code)
gemini-extension.json              # Gemini CLI extension manifest
skills/pencil-design/SKILL.md      # The skill — YAML frontmatter + instructions
skills/pencil-design/references/   # Platform tool-name mappings
AGENTS.md                          # This file (symlinked for Codex compatibility)
CLAUDE.md                          # This file
GEMINI.md                          # Minimal Gemini wrapper
```

---

## Plugin System Rules

- `plugin.json` must live at `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`
- `skills/` must be at the repo root (not inside `.claude-plugin/`)
- Each skill is a subdirectory under `skills/` with a `SKILL.md` file
- The YAML frontmatter `description` field controls when the skill activates — edit it carefully
- Skills may have a `references/` subdirectory for supplementary docs loaded on demand

---

## The Pencil MCP Server

pencil.dev stores designs in encrypted `.pen` files.
**Never use `Read`, `Grep`, or any file tool on `.pen` files.**
Always use the Pencil MCP tools:

| Tool | Purpose |
|------|---------|
| `get_editor_state` | Get current document state |
| `open_document` | Open a `.pen` file |
| `get_guidelines` | Retrieve design guidelines |
| `batch_get` | Read multiple nodes |
| `batch_design` | Write / modify design nodes |
| `snapshot_layout` | Capture layout state |
| `get_screenshot` | Visual screenshot of the design |
| `get_variables` | Read design tokens / variables |
| `set_variables` | Update design tokens / variables |
| `find_empty_space_on_canvas` | Locate available canvas space |
| `search_all_unique_properties` | Search across design properties |
| `replace_all_matching_properties` | Bulk-replace properties |
| `export_nodes` | Export nodes to external format |

---

## Writing the Skill

When writing or editing `skills/pencil-design/SKILL.md`:

1. The `description` frontmatter field is the trigger mechanism — include exact phrases users say
2. Keep `SKILL.md` under ~5,000 words; move detailed references to `references/`
3. Use progressive disclosure: core workflow in `SKILL.md`, edge cases in `references/`
4. Never instruct AI to use `Read`/`Grep` on `.pen` files — always use MCP tools
5. Document tool sequencing (e.g., call `get_editor_state` before `batch_design`)

If you use Claude Code, the `superpowers:writing-skills` skill provides useful guidance
for authoring high-quality SKILL.md content — but it is not a dependency of this project.

---

## Version Bumping

Follow semantic versioning in `.claude-plugin/plugin.json` (and mirror in `SKILL.md` frontmatter):

- **PATCH** (`0.1.x`): Content fixes, typos, clarifications
- **MINOR** (`0.x.0`): New capability documented, new trigger phrases added
- **MAJOR** (`x.0.0`): Breaking restructuring of the skill workflow

Keep `.cursor-plugin/plugin.json` in sync — it should always match `.claude-plugin/plugin.json`.

---

## Testing the Skill Locally

**Claude Code:**
```bash
# From repo root
/plugin install .
# Then ask: "help me design a login screen in pencil"
# Verify the pencil-design skill triggers
```

**Gemini CLI:**
```bash
# Ensure gemini-extension.json is present
# Then: activate_skill pencil-design
```

**Codex:**
```bash
# Skills are auto-discovered from skills/ — no install step needed
```

---

## Links

- GitHub repo: https://github.com/Nisus74/pencil-skill
- pencil.dev: https://pencil.dev
