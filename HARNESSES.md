# Harness Skills Capabilities Reference

Source of truth for what each AI coding harness supports in terms of agent skills. Used to inform platform-specific manifests and to scope which platforms `pencil-dev-skill` can practically support.

**Currently supported:** Claude Code, Cursor (2.5+), Codex CLI.
**Future-supported (folder-copy install today, plugin manifest when warranted):** Gemini CLI, OpenCode, Pi, Kiro, Qoder, Trae, Rovo Dev.

Last verified: 2026-05-16. Note that platform documentation and tool capabilities evolve frequently; this file represents a point-in-time snapshot and should be re-verified before any major platform updates.

## Official documentation

| Harness | Docs URL |
|---------|----------|
| Claude Code | https://code.claude.com/docs/en/skills |
| Cursor | https://cursor.com/docs/context/skills |
| Gemini CLI | https://geminicli.com/docs/cli/skills/ |
| Codex CLI | https://developers.openai.com/codex/skills |
| GitHub Copilot (Agents) | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| Kiro | https://kiro.dev/docs/skills/ |
| OpenCode | https://opencode.ai/docs/skills/ |
| Pi | https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md |
| Qoder | https://docs.qoder.com/extensions/skills |
| Rovo Dev | https://support.atlassian.com/rovo/docs/extend-rovo-dev-cli-with-agent-skills |

## Spec compliance

All harnesses follow the [Agent Skills specification](https://agentskills.io/specification) to varying degrees. The spec defines these frontmatter fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`.

Provider-specific extensions beyond the spec include: `user-invocable`, `argument-hint`, `disable-model-invocation`, `allowed-tools` (extended syntax), `model`, `effort`, `context`, `agent`, `hooks`, `subtask`, `mcp`.

## Frontmatter support

Fields marked with `*` are spec-standard; the rest are provider extensions.

| Field | Claude Code | Cursor | Gemini | Codex | Copilot | Kiro | OpenCode | Pi | Qoder | Rovo Dev |
|-------|:-----------:|:------:|:------:|:-----:|:-------:|:----:|:--------:|:--:|:-----:|:--------:|
| `name`* | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| `description`* | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| `license`* | Yes | Yes | Ignored | No | Yes | Yes | Yes | Yes | Yes | Yes |
| `compatibility`* | Yes | Yes | Ignored | No | Yes | Yes | Yes | Yes | Yes | Yes |
| `metadata`* | Yes | Yes | Ignored | No | Yes | Yes | Yes | Yes | Yes | Yes |
| `allowed-tools`* | Yes | No | Ignored | No | No | No | Yes | Yes | Yes | Yes |
| `user-invocable` | Yes | No | No | No | Yes | No | Yes | No | Yes | Yes |
| `argument-hint` | Yes | No | No | No | Yes | No | Yes | No | Yes | Yes |
| `disable-model-invocation` | Yes | Yes | No | No | Yes | No | Yes | Yes | TBD | TBD |
| `paths` (Pencil-specific) | Yes | Yes | No | No | TBD | No | No | No | No | No |

Notes:
- Gemini CLI validates only `name` and `description`; other spec fields are parsed but ignored.
- Codex CLI uses a separate `agents/openai.yaml` sidecar for skill metadata (icons, branding, MCP tools, invocation control).
- Unknown fields are silently ignored by all harnesses.
- `paths` is a Pencil convention surfaced in the SKILL.md frontmatter for path-based skill activation. Claude Code and Cursor honour it; other platforms ignore it without erroring.

## Skill directory structure

| Harness | Native directory | Also reads |
|---------|-----------------|------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` (user-level) |
| Cursor | `.cursor/skills/` | `.agents/skills/`, `.claude/skills/` |
| Gemini CLI | `.gemini/skills/` | `.agents/skills/` |
| Codex CLI | `.agents/skills/` (primary) | `~/.codex/skills/` (user-level) |
| GitHub Copilot | `.github/skills/` | `.agents/skills/`, `.claude/skills/` |
| Kiro | `.kiro/skills/` | (none) |
| OpenCode | `.opencode/skills/` | `.agents/skills/`, `.claude/skills/` |
| Pi | `.pi/skills/` | `.agents/skills/` |
| Qoder | `.qoder/skills/` | `~/.qoder/skills/` (user-level) |
| Trae International | `.trae/skills/` | TBD |
| Trae China | `.trae-cn/skills/` | TBD |
| Rovo Dev | `.rovodev/skills/` | `~/.rovodev/skills/` (user-level) |

All harnesses support the `{skill-name}/SKILL.md` directory structure with optional `references/`, `scripts/`, and `assets/` subdirectories. `pencil-dev-skill` uses `skills/pencil-design/` at the repo root, which platforms that read `.agents/skills/` will not automatically discover; for those platforms a folder copy or manifest install is required.

## Variable substitution

Claude Code supports runtime variable substitution directly in SKILL.md bodies: `$ARGUMENTS`, `$0`–`$N`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}`. No other harness supports substitution in skills.

Some harnesses have separate custom-commands systems (distinct from skills) with their own substitution:

| Harness | Command system | Substitution syntax |
|---------|---------------|-------------------|
| Gemini CLI | `.gemini/commands/` (TOML) | `{{args}}`, `!{shell}`, `@{file}` |
| Codex CLI | `.codex/prompts/` | `$ARGNAME` |
| OpenCode | `.opencode/commands/` | `$ARGUMENTS`, `$1`–`$N`, `` !`shell` `` |

`pencil-dev-skill` does not currently use substitution in its SKILL.md; the skill activates on natural-language signals rather than slash-command invocation.

## Platform-specific behaviour worth knowing

- **Claude Code.** Plugin manifest at `.claude-plugin/plugin.json`; marketplace listing at `.claude-plugin/marketplace.json` (the file that lets users run `/plugin marketplace add <repo>`).
- **Cursor (2.5+).** Plugin manifest at `.cursor-plugin/plugin.json`. Cursor's plugin schema doesn't document a `permissions` field but accepts (and ignores) it, which is useful for cross-platform lint enforcement.
- **Codex CLI.** Plugin manifest at `.codex-plugin/plugin.json`. The `interface` block in the manifest carries display metadata (long description, default prompts) that Codex surfaces in its skill picker; other platforms ignore it.
- **Gemini CLI.** Validates only `name` and `description` in frontmatter; other fields parsed and discarded. Folder-copy install only for now.
- **Kiro / Qoder / Rovo Dev.** Folder-copy install only; no public plugin marketplace at time of writing. User-level skill directories (`~/.qoder/skills/`, `~/.rovodev/skills/`) make multi-project installs ergonomic.

## When to add a new platform manifest

A platform earns a dedicated plugin manifest (e.g. `.gemini-plugin/plugin.json`) when:

1. The platform ships an official plugin marketplace with `/plugin install` parity to Claude Code or Cursor, AND
2. The platform's adoption by Pencil users is meaningful enough to justify the maintenance overhead of a fourth (or fifth) manifest, AND
3. The platform's frontmatter requirements differ enough from existing manifests that copying `.claude-plugin/plugin.json` isn't sufficient.

Until those three conditions hold, favour the folder-copy install path documented in the README.
