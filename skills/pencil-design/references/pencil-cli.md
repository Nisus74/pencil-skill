# `@pencil.dev/cli` — full reference

A command-line tool for working with `.pen` files outside the desktop app or IDE extension. Useful for headless workflows (CI, batch generation, scripted exports). **This skill does not auto-fall-back to the CLI** — the rationale is at the top of this file. The reference below covers the CLI surface so when CLI *is* the right tool, you have everything you need.

## Why this skill does not auto-fall-back

The default workflow assumes the user has the Pencil desktop app or IDE extension running. When that fails (Failure mode §1 in SKILL.md), the skill **stops and tells the user** rather than launching the CLI. Reasons:

1. **The user's expectation.** When someone asks the agent to design in Pencil, they expect to see changes in the editor they have open. Spawning a headless CLI session is invisible to them.
2. **Auth and config.** The CLI uses a separate session token (`~/.pencil/session-cli.json`) and may require `PENCIL_CLI_KEY` / `ANTHROPIC_API_KEY` env vars. The agent shouldn't manage these silently.
3. **Output divergence.** A CLI run writes to a file path; the user's open document doesn't update. Reconciling later is error-prone.

If a user explicitly asks to use the CLI ("run pencil --in ... --out ..."), follow their instruction — the rule is "don't auto-fall-back," not "never use it." For ambiguous requests where CLI *might* be the right call, see § When CLI vs MCP below.

## When CLI vs MCP

The decision table — load-bearing content; the rest of this file is appendix-style.

| Situation | Use… | Why |
|-----------|------|-----|
| User has Pencil desktop / IDE extension open and is editing live | **MCP** | Live editor sync; user sees changes immediately. |
| User asks to design something and is in an interactive session | **MCP** | Default expectation. The CLI is invisible. |
| Headless CI run (GitHub Actions, build pipeline) | **CLI** | No desktop app available; no need for live sync. |
| Batch process N files (`--tasks` config) | **CLI** | The CLI's `--tasks` flag is purpose-built for this; MCP processes one operation at a time. |
| Bulk export to PNG/PDF as a build artifact | **CLI** | `--export` writes files directly; MCP's `export_nodes` requires a connected editor. |
| User says *"design this without opening the editor"* | **CLI** | Explicit headless intent. |
| User says *"render N variations of this hero"* | **CLI** | The agent-mode `--prompt` is purpose-built for one-shot generation. |
| Quick sketch, exploration, iteration | **MCP** | The CLI's one-shot model is wrong for a back-and-forth task. |
| Scripted recurring task (a cron, a CI hook) | **CLI** | No human in the loop; CLI is the only sane choice. |
| Auditing a file (`batch_get`, then tallying values yourself) | **MCP** | Audit is interactive; the CLI doesn't expose these tools meaningfully. |

**The rule of thumb:** if a human is in the loop, MCP. If no human is in the loop, CLI. If a human is in the loop but explicitly wants headless behavior, ask before launching the CLI.

## Install & runtime

**Requirements:** Node 18 or newer. macOS, Linux, or Windows.

```
npm install -g @pencil.dev/cli
```

Verify installation:

```
pencil --version
pencil status        # confirms auth state
```

**Configuration paths:**

- `~/.pencil/` — root config directory.
- `~/.pencil/session-cli.json` — CLI session token (separate from desktop/IDE auth).
- `~/.pencil/config.json` — optional global config.

**Environment variables:**

- `PENCIL_CLI_KEY` — Pencil API key. Used in CI where browser-based auth isn't available.
- `ANTHROPIC_API_KEY` — required for AI-generation modes (`Generate("ai", ...)` ops, `--prompt`).
- `PENCIL_LOG_LEVEL` — set to `debug` for troubleshooting.

## Modes

The CLI runs in two modes — pick by command shape.

### Agent mode

One-shot AI design generation. Input file in, output file out, prompt drives the change.

```
pencil --in input.pen --out output.pen --prompt "Add a pricing section below the hero"
```

Required: `--in`, `--out`, `--prompt`. Optional: `--model`, `--export`, `--tasks`.

**What happens:** the CLI loads the input, sends the document + prompt to the configured model, applies the model's `batch_design` ops, writes the result to `--out`. Nothing in the editor updates.

### Interactive mode

Opens a shell that exposes the same MCP tools as the desktop app. Useful when an agent (Claude Code, Codex, etc.) needs to drive Pencil headlessly.

```
pencil interactive
```

Inside the shell, the same MCP server runs that the desktop app launches. An agent can connect via the standard MCP protocol and call all 9 tools (`get_editor_state`, `batch_design`, `snapshot_layout`, etc.).

**Use case:** a CI job that needs to generate, audit, or modify designs without a desktop app available. The agent connects to interactive mode and operates as if the editor were open — except the document is a file, not a live canvas.

## Full flag reference

Grouped by purpose. Long form first; short form (where available) in parens.

### Input / output

| Flag | Purpose |
|------|---------|
| `--in / -i <path>` | Input `.pen` path. Required for agent mode. Relative paths resolved against the CWD. |
| `--out / -o <path>` | Output `.pen` path. Required for agent mode. Overwrites if it exists. |
| `--export / -e <format>` | Render to image/PDF (`png`, `jpeg`, `webp`, `pdf`) instead of (or in addition to) writing a `.pen`. |
| `--export-dir <path>` | Destination directory for exports. Defaults to the same directory as `--out`. |
| `--export-scale <n>` | Resolution scale for raster exports (`1`, `2`, `3`). Default `2`. |

### Prompting

| Flag | Purpose |
|------|---------|
| `--prompt / -p <text>` | The instruction to apply to the input. Required for agent mode. |
| `--prompt-file <path>` | Read the prompt from a file instead of the command line. Useful for long prompts. |

### Model

| Flag | Purpose |
|------|---------|
| `--model / -m <id>` | Model selection. Defaults to `claude-opus-4-7` at the time of writing. Available: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`. |
| `--temperature <n>` | Model temperature (0–1). Lower = more deterministic. Default 0.3 for design work. |

### Batch

| Flag | Purpose |
|------|---------|
| `--tasks <path>` | Path to a JSON file describing N tasks to run. Each task entry has `in`, `out`, `prompt`, optionally `model` / `export`. |
| `--parallel <n>` | When using `--tasks`, run up to N tasks concurrently. Default 1. |

**Tasks file shape:**

```json
[
  { "in": "./templates/hero.pen", "out": "./out/hero-v1.pen", "prompt": "Add a green CTA" },
  { "in": "./templates/hero.pen", "out": "./out/hero-v2.pen", "prompt": "Add a blue CTA" }
]
```

### Auth

| Command | Purpose |
|---------|---------|
| `pencil status` | Show auth state, current account, configured model, key presence. |
| `pencil login` | Interactive auth flow (opens a browser). Writes session to `~/.pencil/session-cli.json`. |
| `pencil logout` | Clear local session. |

### Debug

| Flag | Purpose |
|------|---------|
| `--verbose / -v` | More-detailed logs to stderr. |
| `--debug` | Equivalent to `PENCIL_LOG_LEVEL=debug`. |
| `--dry-run` | Parse and validate the inputs but don't make any model calls or write outputs. |

## `pencil status`

Reports:

- Current logged-in account (or *"not logged in"*).
- Session expiry.
- Whether `PENCIL_CLI_KEY` is set.
- Whether `ANTHROPIC_API_KEY` is set (required for AI generation).
- Default model.

When status shows *"not logged in"*: run `pencil login`. If running in CI, set `PENCIL_CLI_KEY` instead.

## `pencil login`

Opens a browser to the Pencil auth flow. The user signs in; Pencil redirects with a token; the CLI writes the token to `~/.pencil/session-cli.json`.

Headless / CI: don't use `pencil login`. Set `PENCIL_CLI_KEY` directly in the environment. The login flow requires a browser.

## Headless / CI workflows

A typical setup for a GitHub Actions job that generates design assets on every PR:

```yaml
name: Generate hero variants
on: pull_request
jobs:
  design:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm install -g @pencil.dev/cli
      - run: pencil --in design/hero-template.pen --out design/out/hero.pen --prompt "Generate a hero for ${{ github.head_ref }}" --export png --export-dir design/exports
        env:
          PENCIL_CLI_KEY: ${{ secrets.PENCIL_CLI_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - uses: actions/upload-artifact@v4
        with: { name: hero-exports, path: design/exports }
```

**Notes:**

- The `PENCIL_CLI_KEY` lives in repo secrets, not in code.
- Both `PENCIL_CLI_KEY` and `ANTHROPIC_API_KEY` are required when the prompt triggers AI image generation; just `PENCIL_CLI_KEY` is enough for prompts that only manipulate existing nodes.
- Exports are uploaded as artifacts so reviewers can preview without running the job locally.

For batch generation, point at a tasks file:

```yaml
- run: pencil --tasks design/variants.json --parallel 3
```

## Auth troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `pencil status` shows *"not logged in"* | Session expired or never created | `pencil login` (interactive) or set `PENCIL_CLI_KEY` (headless) |
| `Error: API key not found` on a `--prompt` run | `ANTHROPIC_API_KEY` not set | Set it in the environment |
| `403 Forbidden` from `pencil` calls | Account lacks access to the model in `--model` | Use a model your account has access to (`pencil status` shows the default) |
| `pencil login` succeeds but `pencil status` still says *"not logged in"* | Multiple Node versions or shells; session written to a different `~/.pencil/` | Confirm `which pencil` matches the install you authed against |
| `Error: input not a valid .pen file` | File is corrupted or schema-incompatible | Open in the desktop app first; the app will offer to migrate |

## What CLI can't do

- **Live editor sync.** A CLI run does not update the desktop app's open document.
- **Screenshots that match what the user sees.** `--export` renders against the file's declared themes / dimensions; the desktop app might be in a different mode or zoom. Use the desktop app for "what does this look like to me right now."
- **Real-time multi-agent edits.** Two CLI runs hitting the same `.pen` race; the second silently overwrites the first.
- **`get_editor_state`, `FindEmptySpace`, `get_screenshot` against a live canvas.** The CLI's interactive mode exposes these against the file, but the file is a static snapshot — there's no canvas to find space on, no live screenshot.
- **Interactive design exploration.** The CLI's agent mode is one-shot. Iteration requires re-running.

## What MCP can't do

- **True headless operation.** MCP requires a host (desktop, IDE extension, or the CLI's interactive mode).
- **Batch tasks from a JSON file.** MCP processes one tool call at a time. The CLI's `--tasks` is the right shape for "process these 50 templates."
- **Fully scripted exports without a UI.** `export_nodes` via MCP works, but it requires a connected host. CI usually doesn't have one — the CLI's `--export` is purpose-built.
- **CI-friendly auth.** MCP's auth lives in the host (desktop/IDE), which doesn't exist in CI. The CLI's `PENCIL_CLI_KEY` env var is built for that.

## See also

- [`mcp-tools.md`](mcp-tools.md) — the full MCP surface this file contrasts with.
- SKILL.md § Failure modes §1 — the no-auto-fallback rule.
- [`batch-design-grammar.md`](batch-design-grammar.md) — the op grammar the CLI's agent mode runs.
- [Pencil docs](https://docs.pencil.dev) — canonical product documentation.
