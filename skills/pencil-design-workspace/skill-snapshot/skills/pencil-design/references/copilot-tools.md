# Tool Name Mapping: GitHub Copilot CLI

When following this skill on **GitHub Copilot CLI**, replace Claude Code tool names as follows:

| Claude Code | Copilot CLI equivalent |
|-------------|----------------------|
| `Skill` (invoke a skill) | `skill` |
| `Task` (dispatch subagent) | `task` |
| `TodoWrite` | `sql` (for task tracking) |
| `Read` | `view` |
| `Edit` / `Write` | `str_replace_editor` |
| `Bash` | `bash` (supports async sessions — use `session_id` for long-running commands) |
| `WebSearch` | `web_search` |

All Pencil MCP tool names (`get_editor_state`, `batch_design`, etc.) are the same across platforms — only the Claude Code wrapper tool names differ.
