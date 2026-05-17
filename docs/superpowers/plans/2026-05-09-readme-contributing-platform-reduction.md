# README Rewrite, CONTRIBUTING Clarity, and Platform Reduction — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove Gemini CLI and GitHub Copilot CLI from the entire repo, rewrite README.md from scratch for clarity and impact, and rewrite CONTRIBUTING.md so contributors can act immediately.

**Architecture:** Pure documentation work — file deletions, content rewrites, and targeted edits. No code changes. Three independent streams (platform reduction, README, CONTRIBUTING) executed in order because README and CONTRIBUTING both depend on knowing the final platform list.

**Tech Stack:** Markdown, git, GitHub

---

## File Map

| Action | File |
|--------|------|
| Delete | `gemini-extension.json` |
| Delete | `skills/pencil-design/references/gemini-tools.md` |
| Delete | `skills/pencil-design/references/copilot-tools.md` |
| Rewrite | `README.md` |
| Rewrite | `docs/CONTRIBUTING.md` |
| Edit | `AGENTS.md` — remove Gemini/Copilot rows |
| Edit | `.github/ISSUE_TEMPLATE/bug_report.md` — remove Gemini/Copilot from environment list |

> `.github/PULL_REQUEST_TEMPLATE.md` and `.github/ISSUE_TEMPLATE/feature_request.md` have no Gemini/Copilot references — skip them.

---

## Task 1: Delete Gemini and Copilot files

**Files:**
- Delete: `gemini-extension.json`
- Delete: `skills/pencil-design/references/gemini-tools.md`
- Delete: `skills/pencil-design/references/copilot-tools.md`

- [ ] **Step 1: Delete the three files**

```bash
git rm gemini-extension.json
git rm skills/pencil-design/references/gemini-tools.md
git rm skills/pencil-design/references/copilot-tools.md
```

- [ ] **Step 2: Verify they are gone**

```bash
git status
```

Expected: three deletions staged, no other changes.

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove Gemini CLI and Copilot CLI platform support"
```

---

## Task 2: Update AGENTS.md

**Files:**
- Modify: `AGENTS.md`

Current state (before edit):
- Platform Support table has 5 rows: Claude Code, Gemini CLI, Cursor, Codex, Copilot CLI
- Repository Structure block lists `gemini-extension.json` and `copilot-tools.md`
- Deployment section references Gemini/Copilot install paths

- [ ] **Step 1: Remove Gemini CLI and Copilot CLI rows from the Platform Support table**

Find this block in `AGENTS.md` (around line 120):

```markdown
| Platform | Plugin install | Folder-copy target |
|----------|---------------|-------------------|
| Claude Code | `/plugin install github:Nisus74/pencil-skill` (manifest at `.claude-plugin/plugin.json`) | `~/.claude/skills/` or `.claude/skills/` |
| Google Gemini CLI | `gemini-extension.json` at repo root | `~/.gemini/skills/` or `.gemini/skills/` (alias `.agents/skills/`) |
| Cursor (2.5+) | `/add-plugin` pointing at `github.com/Nisus74/pencil-skill` (manifest at `.cursor-plugin/plugin.json`) | `.cursor/skills/` (Cursor also reads `AGENTS.md` from project root) |
| OpenAI Codex | (no plugin manifest) | `~/.codex/skills/` |
| GitHub Copilot CLI | (no plugin manifest) | `~/.copilot/skills/` (alias `~/.agents/skills/`) or project `.github/skills/` |
```

Replace with:

```markdown
| Platform | Plugin install | Folder-copy target |
|----------|---------------|-------------------|
| Claude Code | `/plugin install github:Nisus74/pencil-skill` (manifest at `.claude-plugin/plugin.json`) | `~/.claude/skills/` or `.claude/skills/` |
| Cursor (2.5+) | `/add-plugin` pointing at `github.com/Nisus74/pencil-skill` (manifest at `.cursor-plugin/plugin.json`) | `.cursor/skills/` |
| OpenAI Codex | (no plugin installer) | `~/.codex/skills/` |
```

- [ ] **Step 2: Remove the final sentence of the Platform Support section**

Find and delete this line (just below the table):

```
All platforms also accept a `SKILL.md` in their respective skills directory; folder copy works universally.
```

- [ ] **Step 3: Remove Gemini/Copilot entries from the Repository Structure block**

In the repository structure code block, find and remove these two lines:

```
gemini-extension.json              # Required by Gemini CLI's installer
```

and

```
    copilot-tools.md               # GitHub Copilot CLI tool name mappings
```

- [ ] **Step 4: Update the Deployment and customisation section**

Find this paragraph (around line 132):

```markdown
The full per-platform install instructions live in [README.md](./README.md#installing). At a glance:

- **Plugin install** is the right default. Users editing only the design-system scaffolds are unaffected by `/plugin update`, because the skill copies those scaffolds out into the user's project (e.g. `docs/design/`).
- **Folder copy** suits users who want to own the skill files from day one. They edit anything, fetch updates by re-downloading and merging by hand.
- **Fork and install** suits users who want both: full edit access and an automatic update path. Install your fork as a plugin; rebase against upstream when you want changes.

Don't edit files inside a plugin install directory (e.g. `~/.claude/plugins/.../skills/pencil-design/`); the next `/plugin update` will overwrite them. The README spells this out for each path.
```

Replace with:

```markdown
The full per-platform install instructions live in [README.md](./README.md#install). At a glance:

- **Plugin install** is the right default. Users editing only the design-system scaffolds are unaffected by `/plugin update`, because the skill copies those scaffolds out into the user's project (e.g. `docs/design/`).
- **Folder copy** suits users who want to own the skill files from day one. They edit anything, fetch updates by re-downloading and merging by hand.
- **Fork + install** suits users who want both: full edit access and an automatic update path. Install your fork as a plugin; rebase against upstream when you want changes.

Don't edit files inside a plugin install directory (e.g. `~/.claude/plugins/.../skills/pencil-design/`); the next `/plugin update` will overwrite them.
```

- [ ] **Step 5: Update the Plugin System Rules section**

Find this line in Plugin System Rules:

```
- `gemini-extension.json` MUST live at the repo root (Gemini CLI requirement)
```

Delete it entirely.

Find this line:

```
- All three platform manifests (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `gemini-extension.json`) carry a `permissions` block matching SKILL.md (enforced by `tools/skill-lint.py`)
```

Replace with:

```
- Both platform manifests (`.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`) carry a `permissions` block matching SKILL.md (enforced by `tools/skill-lint.py`)
```

- [ ] **Step 6: Update the Testing the Skill Locally section**

Find this block:

```markdown
**Gemini CLI:**
```bash
# Install the extension; AGENTS.md loads automatically as project context
# Describe a pencil task; the skill activates via the description trigger
```

**Codex / Copilot CLI:**
```bash
# Skills are auto-discovered from skills/ — no install step needed
```
```

Replace with:

```markdown
**Codex:**
```bash
# Skills are auto-discovered from skills/ — no install step needed
```
```

- [ ] **Step 7: Verify the file looks right**

```bash
grep -n "Gemini\|Copilot\|gemini\|copilot" AGENTS.md
```

Expected: zero matches (or only matches inside the Pencil MCP server table which is unrelated).

- [ ] **Step 8: Commit**

```bash
git add AGENTS.md
git commit -m "docs: remove Gemini CLI and Copilot CLI from AGENTS.md"
```

---

## Task 3: Update the bug report issue template

**Files:**
- Modify: `.github/ISSUE_TEMPLATE/bug_report.md`

- [ ] **Step 1: Update the environment field**

Find:

```markdown
- **AI coding tool:** <!-- Claude Code / Codex / Gemini CLI / Copilot CLI / Cursor -->
```

Replace with:

```markdown
- **AI coding tool:** <!-- Claude Code / Cursor / Codex -->
```

- [ ] **Step 2: Commit**

```bash
git add .github/ISSUE_TEMPLATE/bug_report.md
git commit -m "docs: remove Gemini CLI and Copilot CLI from bug report template"
```

---

## Task 4: Rewrite README.md

**Files:**
- Rewrite: `README.md`

- [ ] **Step 1: Replace the entire contents of README.md**

Write the following as the complete new file:

````markdown
# pencil-dev-skill

Teach your AI coding tool to design in [pencil.dev](https://pencil.dev).
Works with Claude Code, Cursor, and Codex — via plugin or folder copy.

[![version](https://img.shields.io/badge/version-1.4.0-blue)](https://github.com/Nisus74/pencil-skill/releases)
[![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

⭐ If this saves you time, [star the repo](https://github.com/Nisus74/pencil-skill) — it helps more people find it.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Nisus74)

---

## What it does

- Runs a seven-step design workflow: detect host, orient, load guidelines, plan, execute, verify, report
- Covers all 13 Pencil MCP tools with worked invocations, a cost cheatsheet, and composite recipes
- Ships 2026 design depth: user flows, component and screen states, full accessibility coverage, and modern patterns (container queries, fluid type, AI-UI affordances)
- Includes 12 design-system scaffold templates you copy into your project — tokens, components, layout, states, and more
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

Most people want plugin install. If you plan to rewrite the skill's instructions for your team, use folder copy or fork + install instead.

> Don't edit files inside the plugin install directory — the next update overwrites them. To customise the skill itself, use folder copy or fork + install.

### Plugin install

**Claude Code:**

```bash
/plugin install github:Nisus74/pencil-skill
```

**Cursor 2.5+:** in the editor, run `/add-plugin` and point it at `github.com/Nisus74/pencil-skill`.

**Codex:** no plugin installer — use folder copy below.

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
   - Cursor: `/add-plugin` → `github.com/<your-handle>/pencil-skill`
3. Edit your fork, commit, and push — the next plugin update pulls your changes.
4. To pull upstream changes, rebase your fork against `Nisus74/pencil-skill`.

For Codex, use folder copy. The end result is the same; you just don't get an automatic update path.

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

**Design-system files** live in [skills/pencil-design/assets/design-system/](skills/pencil-design/assets/design-system/). The skill copies them into your project (typically `docs/design/`), and you edit those copies to match your brand. Plugin updates never touch them — plugin install is fine here.

**Skill content** (`SKILL.md`, references, worked examples) controls how the AI does its work. To rewrite it for your team's workflow, use folder copy or fork + install. Editing inside a plugin install directory will be overwritten on the next update.

---

## Contributing

Read [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) for the full guide.

The short version: fork, branch from `main`, make your change, run the pre-commit checks, open a PR with before/after examples.

---

## License

MIT. See [LICENSE](./LICENSE).
````

- [ ] **Step 2: Verify no Gemini or Copilot references remain**

```bash
grep -n "Gemini\|Copilot\|gemini\|copilot" README.md
```

Expected: zero matches.

- [ ] **Step 3: Verify both BMC links are gone from the body and only one button remains at the top**

```bash
grep -n "buymeacoffee\|Buy Me" README.md
```

Expected: exactly two matches — the image URL and the link URL — both in the hero block.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: full README rewrite — hero, platform reduction, clarity"
```

---

## Task 5: Rewrite CONTRIBUTING.md

**Files:**
- Rewrite: `docs/CONTRIBUTING.md`

- [ ] **Step 1: Replace the entire contents of docs/CONTRIBUTING.md**

Write the following as the complete new file:

````markdown
# Contributing

Bug reports, workflow improvements, new trigger phrases, and platform fixes are all welcome.

---

## Quick start

```bash
# 1. Fork on GitHub, then:
git clone https://github.com/<your-handle>/pencil-skill.git
cd pencil-skill
git checkout -b my-change

# 2. Make your change, then install and run the pre-commit checks:
pip install pre-commit
pre-commit install
pre-commit run --all-files

# 3. Push and open a PR:
git push -u origin my-change
# → open a PR on GitHub using the template
```

---

## What belongs here

This is a general-purpose pencil.dev skill. A change belongs here if it benefits any pencil.dev user regardless of their project.

If your change is specific to your project's design system, component library, or workflow, it belongs in a fork — not here.

---

## Reporting bugs

Open a [bug report](https://github.com/Nisus74/pencil-skill/issues/new?template=bug_report.md). Include the exact prompt that triggered the issue and evidence of the incorrect behaviour — a transcript or screenshot.

---

## Suggesting improvements

Open a [feature request](https://github.com/Nisus74/pencil-skill/issues/new?template=feature_request.md). Describe the specific scenario where the skill falls short and what you'd want it to do instead.

---

## Submitting a pull request

1. **Fork** the repository on GitHub.

2. **Clone your fork** and create a branch from `main`:

   ```bash
   git clone https://github.com/<your-handle>/pencil-skill.git
   cd pencil-skill
   git checkout -b my-change
   ```

3. **Make your change.** Most changes touch `skills/pencil-design/SKILL.md` or a file under `skills/pencil-design/references/`.

4. **Run the pre-commit checks:**

   ```bash
   pip install pre-commit
   pre-commit install
   pre-commit run --all-files
   ```

   Fix any failures before pushing.

5. **Push and open a PR:**

   ```bash
   git push -u origin my-change
   ```

   Open a PR on GitHub using the pull request template. Fill in every section. Include specific before/after examples — "it works" is not sufficient evidence.

---

## Skill authoring tips

- The `description` frontmatter field controls when the skill activates. Include exact phrases users are likely to say.
- Keep `SKILL.md` focused on the core workflow. Move detailed edge cases to `skills/pencil-design/references/`.
- Always route `.pen` reads and writes through the Pencil MCP tools. The MCP path gives you schema validation, screenshot feedback, and live-editor sync.
- Document tool sequencing where it matters (for example, call `get_editor_state` before `batch_design`).
- Keep instructions platform-agnostic. Use generic verbs ("read", "write", "search") rather than tool names where possible. When tool names are necessary, default to Claude Code names and rely on tool-mapping reference files for other platforms.

If you use Claude Code, the `superpowers:writing-skills` skill provides guidance for authoring high-quality SKILL.md content. It is optional and not a dependency of this project.

---

## Security checks (OWASP AST)

Every PR runs `tools/skill-lint.py` automatically in CI. The pre-commit hook runs the same checks locally — see Quick start above.

If you have a legitimate reason to deviate from a check, suppress it with a non-empty justification:

- For `permissions:` — add `allowlist-justification: "<reason>"` as a sibling key.
- For workflow `uses:` lines — append `# skill-lint: AST07 allow — <reason>`.
- For dangerous patterns inside an illustrative fenced code block — mark the opening fence: `` ```bash skill-lint:AST01 allow — <reason> ``.

Empty justifications are themselves errors.

The full OWASP AST risk-to-control mapping lives in [SECURITY.md](./SECURITY.md).

---

## Versioning

After any meaningful change, bump the version in three places and add a changelog entry:

| File | Field |
|------|-------|
| `.claude-plugin/plugin.json` | `version` |
| `.cursor-plugin/plugin.json` | `version` |
| `skills/pencil-design/SKILL.md` | `metadata.version` in frontmatter |
| `docs/CHANGELOG.md` | new entry |

Follow [Semantic Versioning](https://semver.org/):

| Change type | Bump |
|-------------|------|
| Typo fix, clarification | PATCH (`0.1.x`) |
| New capability or trigger phrases | MINOR (`0.x.0`) |
| Breaking workflow restructure | MAJOR (`x.0.0`) |

---

## Code of conduct

Please read and follow the [Code of Conduct](./CODE_OF_CONDUCT.md).

**Never commit secrets.** API keys, tokens, passwords, and credentials must never appear in any file. Every PR is automatically scanned by [gitleaks](https://github.com/gitleaks/gitleaks) and blocked if secrets are detected.
````

- [ ] **Step 2: Verify no Gemini or Copilot references remain**

```bash
grep -n "Gemini\|Copilot\|gemini\|copilot" docs/CONTRIBUTING.md
```

Expected: zero matches.

- [ ] **Step 3: Commit**

```bash
git add docs/CONTRIBUTING.md
git commit -m "docs: rewrite CONTRIBUTING.md for clarity — quick start and step-by-step PR guide"
```

---

## Task 6: Final verification

- [ ] **Step 1: Scan the entire repo for remaining Gemini/Copilot references**

```bash
grep -rn "Gemini\|Copilot\|gemini-extension\|copilot-tools\|gemini-tools" \
  --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" \
  --exclude-dir=".git" .
```

Expected: zero matches across all tracked files.

- [ ] **Step 2: Confirm deleted files are gone**

```bash
ls gemini-extension.json 2>/dev/null && echo "STILL EXISTS" || echo "deleted OK"
ls skills/pencil-design/references/gemini-tools.md 2>/dev/null && echo "STILL EXISTS" || echo "deleted OK"
ls skills/pencil-design/references/copilot-tools.md 2>/dev/null && echo "STILL EXISTS" || echo "deleted OK"
```

Expected: all three print `deleted OK`.

- [ ] **Step 3: Run the pre-commit checks to catch any lint regressions**

```bash
pip install pre-commit
pre-commit run --all-files
```

Expected: all checks pass. The skill-lint tool checks that platform manifests (`plugin.json`) carry a `permissions` block — confirm this still passes since we only deleted `gemini-extension.json`, which the linter does not require.

- [ ] **Step 4: Push the branch**

```bash
git push -u origin docs/workflows-and-testing
```
