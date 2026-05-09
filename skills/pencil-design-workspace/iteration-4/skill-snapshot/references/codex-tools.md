# Tool Name Mapping: OpenAI Codex

When following this skill on **OpenAI Codex**, replace Claude Code tool names as follows:

| Claude Code | Codex equivalent |
|-------------|-----------------|
| `Skill` (invoke a skill) | Native skills — Codex discovers skills automatically from the `skills/` directory |
| `Task` (dispatch subagent) | `spawn_agent` |
| `TodoWrite` | `update_plan` |
| `Read` | Native file tools |
| `Edit` / `Write` | Native file tools |
| `Bash` | Native shell tools |
| `WebSearch` | Native search tools |

All Pencil MCP tool names (`get_editor_state`, `batch_design`, etc.) are the same across platforms — only the Claude Code wrapper tool names differ.
