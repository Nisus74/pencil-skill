# Tool Name Mapping: Google Gemini CLI

When following this skill on **Google Gemini CLI**, replace Claude Code tool names as follows:

| Claude Code | Gemini CLI equivalent |
|-------------|----------------------|
| `Skill` (invoke a skill) | `activate_skill` |
| `Task` (dispatch subagent) | Not supported — execute steps inline |
| `TodoWrite` | `write_todos` |
| `Read` | `read_file` |
| `Edit` / `Write` | `write_file` |
| `Bash` | `run_shell_command` |
| `WebSearch` | `google_search` |

All Pencil MCP tool names (`get_editor_state`, `batch_design`, etc.) are the same across platforms — only the Claude Code wrapper tool names differ.
