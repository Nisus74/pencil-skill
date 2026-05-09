# Contributing

Bug reports, workflow improvements, new trigger phrases, and platform fixes are all welcome.

---

## Quick start

```bash
# 1. Fork on GitHub, then clone your fork:
git clone https://github.com/<your-handle>/pencil-skill.git
cd pencil-skill
git checkout -b my-change

# 2. Make your change, then run the pre-commit checks:
pip install pre-commit
pre-commit install
pre-commit run --all-files

# 3. Push and open a PR:
git push -u origin my-change
# Open a PR on GitHub using the pull request template
```

---

## What belongs here

A change belongs here if it benefits any pencil.dev user, regardless of their project. If your change is specific to your design system, component library, or workflow, it belongs in a fork.

---

## Reporting bugs

Open a [bug report](https://github.com/Nisus74/pencil-skill/issues/new?template=bug_report.md). Include the exact prompt that triggered the issue and evidence of the incorrect behaviour: a transcript or screenshot.

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

   Open a PR on GitHub using the pull request template. Fill in every section. Include specific before/after examples. "It works" isn't sufficient evidence.

---

## Skill authoring tips

- The `description` frontmatter field controls when the skill activates. Include exact phrases users are likely to say.
- Keep `SKILL.md` focused on the core workflow. Move detailed edge cases to `skills/pencil-design/references/`.
- Always route `.pen` reads and writes through the Pencil MCP tools. The MCP path gives you schema validation, screenshot feedback, and live-editor sync.
- Document tool sequencing where it matters. For example: call `get_editor_state` before `batch_design`.
- Keep instructions platform-agnostic. Use generic verbs ("read", "write", "search") rather than tool names where possible. When tool names are necessary, default to Claude Code names and rely on tool-mapping reference files for other platforms.

If you use Claude Code, the `superpowers:writing-skills` skill provides guidance for authoring high-quality SKILL.md content. It's optional and not a dependency of this project.

---

## Security checks (OWASP AST)

Every PR runs `tools/skill-lint.py` automatically in CI. The pre-commit hook runs the same checks locally. See Quick start above.

If you have a legitimate reason to deviate from a check, suppress it with a non-empty justification:

- For `permissions:`, add `allowlist-justification: "<reason>"` as a sibling key.
- For workflow `uses:` lines, append `# skill-lint: AST07 allow — <reason>`.
- For dangerous patterns inside an illustrative fenced code block, mark the opening fence: `` ```bash skill-lint:AST01 allow — <reason> ``.

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

**Never commit secrets.** API keys, tokens, passwords, and credentials must never appear in any file. Every PR is automatically scanned by [gitleaks](https://github.com/gitleaks/gitleaks) and blocked if secrets are recognised.
