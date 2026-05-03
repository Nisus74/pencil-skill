# `@pencil.dev/cli` — what it is and why this skill doesn't auto-fall-back

A command-line tool for working with `.pen` files outside the desktop app or IDE extension. Installed with `npm install -g @pencil.dev/cli`. Requires Node 18+.

Two modes:

- **Agent mode:** `pencil --in input.pen --out output.pen --prompt "<task>"` — one-shot AI design generation.
- **Interactive mode:** `pencil interactive` — opens a shell that exposes the same MCP tools as the desktop app. Can connect to a running app or run headlessly.

## Why this skill does not use it

The default workflow assumes the user has the Pencil desktop app or IDE extension running. When that fails (Failure mode §1), the skill **stops and tells the user** rather than launching the CLI. Reasons:

1. **The user's expectation.** When someone asks the agent to design in Pencil, they expect to see changes in the editor they have open. Spawning a headless CLI session is invisible to them.
2. **Auth and config.** The CLI uses a separate session token (`~/.pencil/session-cli.json`) and may require `PENCIL_CLI_KEY` / `ANTHROPIC_API_KEY` env vars. The agent shouldn't manage these silently.
3. **Output divergence.** A CLI run writes to a file path; the user's open document doesn't update. Reconciling later is error-prone.

If a user explicitly asks to use the CLI ("run pencil --in ... --out ..."), follow their instruction — the rule is "don't auto-fall-back," not "never use it."

## Reference: useful flags

- `--in / -i` — input `.pen` path.
- `--out / -o` — output `.pen` path (required for agent mode).
- `--prompt / -p` — instruction.
- `--model / -m` — model selection. Defaults to `claude-opus-4-6` at the time of writing.
- `--export / -e` — render to PNG/JPEG/WEBP/PDF instead of (or in addition to) writing a `.pen`.
- `--tasks` — batch processing from a JSON config.
- `pencil status` — check auth.
- `pencil login` — interactive auth.
