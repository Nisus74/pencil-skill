---
name: README rewrite, CONTRIBUTING clarity, and platform reduction
description: Full redesign of README.md, rewrite of CONTRIBUTING.md for clarity, and removal of Gemini CLI and GitHub Copilot CLI from all project surfaces
type: project
---

# Design: README Rewrite, CONTRIBUTING Clarity, and Platform Reduction

**Date:** 2026-05-09
**Branch:** docs/workflows-and-testing

---

## Scope

Three changes ship together because they are tightly coupled — the platform reduction shrinks every table and code block in the README and CONTRIBUTING.md, and the README rewrite is the right moment to restructure both.

1. **Platform reduction** — Remove Gemini CLI and GitHub Copilot CLI from every surface in the repo
2. **README full rewrite** — Replace the current flat, dry README with a structured, energetic one
3. **CONTRIBUTING.md clarity rewrite** — Keep all rules; lead with action, not policy

GitHub workflows have no Gemini/Copilot references and need no changes beyond what the platform reduction touches in other files.

---

## 1. Platform Reduction

### Files to delete
- `skills/pencil-design/references/gemini-tools.md`
- `skills/pencil-design/references/copilot-tools.md`
- `gemini-extension.json`

### Files to update
| File | Change |
|------|--------|
| `README.md` | Full rewrite (see section 2) — remove all Gemini/Copilot rows and blocks |
| `AGENTS.md` | Remove Gemini CLI and Copilot CLI rows from the Platform Support table; remove their install paths from the folder-copy table; remove `gemini-extension.json` and `copilot-tools.md` from the repository structure block |
| `docs/CONTRIBUTING.md` | Full clarity rewrite (see section 3) — remove Gemini/Copilot install examples |
| `.github/PULL_REQUEST_TEMPLATE.md` | Audit for Gemini/Copilot references; remove if present |
| `.github/ISSUE_TEMPLATE/` | Audit for Gemini/Copilot references; remove if present |

### Supported platforms after reduction
| Platform | Plugin install | Folder-copy target |
|----------|--------------|-------------------|
| Claude Code | `/plugin install github:Nisus74/pencil-skill` | `~/.claude/skills/` or `.claude/skills/` |
| Cursor (2.5+) | `/add-plugin` → `github.com/Nisus74/pencil-skill` | `.cursor/skills/` |
| OpenAI Codex | (no plugin installer) | `~/.codex/skills/` |

Folder copy works as the universal fallback for all three.

---

## 2. README Full Rewrite

### Structure (top to bottom)

**Hero block**
- Repo name as H1
- One-line hook: "Teach your AI coding tool to design in pencil.dev."
- Supported tools named inline: Claude Code, Cursor, and Codex
- Badges row: version · license (shield.io style, static)
- Star ask: one sentence, friendly, links to the repo
- Buy Me a Coffee button (image button, the `orange_img.png` version) — removes the duplicate plain-text link

**What it does** (H2)
- 4–5 bullet points, benefit-first
- No "this project", no "it is", no passive voice
- Covers: seven-step design workflow, 13 MCP tools with recipes, 2026 design depth, 12 scaffold templates, 5 worked examples

**Quick install** (H2)
- Three named subsections: Claude Code, Cursor, Codex
- Each gets exactly what it needs: one command or one config block
- Folder copy as a separate subsection with a three-row table: Claude Code, Cursor, Codex (each with their target path)
- Fork + install as a final subsection for users who want edit access + automatic updates

**Usage** (H2)
- Short intro sentence
- Bullet list of 5 example trigger phrases

**Customising** (H2)
- Two paragraphs: design-system files (safe to edit with plugin install) vs. skill content (requires folder copy or fork)

**Contributing** (H2)
- Two sentences + link to `docs/CONTRIBUTING.md`

**License** (H2)
- One line

### Tone rules
- Direct and confident. No filler phrases ("please note that", "it is important to", "feel free to").
- Active voice throughout.
- Short sentences. One idea per sentence.
- No marketing superlatives. Let the tool speak for itself.

---

## 3. CONTRIBUTING.md Clarity Rewrite

### Structure

**Quick start** (H2)
A fenced shell block with the complete contributor command sequence:

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

**What belongs here** (H2)
Short paragraph. Contributions that benefit any pencil.dev user. Project-specific changes belong in a fork.

**Reporting bugs** (H2)
One paragraph + link to bug report template.

**Suggesting improvements** (H2)
One paragraph + link to feature request template.

**Submitting a pull request** (H2)
Numbered steps — explicit, no assumed knowledge:
1. Fork the repo on GitHub
2. Clone your fork and create a branch from `main`
3. Make your change (edit the right file)
4. Run pre-commit checks (exact commands)
5. Push and open a PR (include before/after evidence)

**Skill authoring tips** (H2)
Keep the five bullet points (description field, file size, MCP routing, tool sequencing, platform-agnostic verbs). Remove the introductory paragraph above them — the bullets are self-explanatory.

**Security checks (OWASP AST)** (H2)
Keep the suppression/allowlist instructions and the AST risk table link. Remove the `pip install pre-commit && pre-commit install && pre-commit run --all-files` block — it is now covered by Quick start.

**Versioning** (H2)
Keep existing table. Trim prose to one sentence per row.

### Tone rules
Same as README: direct, active, no policy-speak. Lead with what the contributor *does*, not with what the project *requires*.

---

## Out of Scope

- Changes to `tools/skill-lint.py` or `tools/test_skill_lint.py`
- Changes to `skills/pencil-design/SKILL.md` or any reference files (except deleting `gemini-tools.md` and `copilot-tools.md`)
- GitHub workflow changes (neither workflow references Gemini or Copilot)
- Version bump (content changes to docs do not warrant a semver bump)
