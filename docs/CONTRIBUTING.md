# Contributing to pencil-dev-skill

Thank you for your interest in improving this skill. Contributions of all kinds are welcome:
bug reports, workflow improvements, new trigger phrases, and platform-specific fixes.

---

## Before You Start

- Search [open and closed issues](https://github.com/Nisus74/pencil-skill/issues?q=is%3Aissue)
  to avoid duplicates.
- For questions or discussion, use [GitHub Discussions](https://github.com/Nisus74/pencil-skill/discussions)
  rather than opening an issue.
- Please read and follow the [Code of Conduct](./CODE_OF_CONDUCT.md).
- **Never commit secrets.** API keys, tokens, passwords, and credentials must never appear
  in any file. Every PR is automatically scanned by [gitleaks](https://github.com/gitleaks/gitleaks)
  and will be blocked if secrets are detected.

---

## Reporting Bugs

Open a [bug report](https://github.com/Nisus74/pencil-skill/issues/new?template=bug_report.md).
Include the exact prompt that triggered the issue and evidence of the incorrect behaviour
(transcript or screenshot).

---

## Suggesting Improvements

Open a [feature request](https://github.com/Nisus74/pencil-skill/issues/new?template=feature_request.md).
Describe the specific scenario where the skill falls short and what you'd want it to do instead.

---

## Submitting a Pull Request

1. **Fork** the repository and create a branch from `main`.

2. **Edit** `skills/pencil-design/SKILL.md` (or the relevant reference file).

3. **Test** your change with at least 3 different prompts that should trigger the skill:
   - Install the plugin locally on the AI coding tool of your choice
     (Claude Code: `/plugin install .` from the repo root)
   - Try your trigger phrases and verify the skill activates and behaves correctly
   - Test at least one edge case

4. **Open a PR** using the pull request template and fill in all sections.
   "It works" isn't sufficient evidence; include specific before/after examples.

---

## What Belongs Here

This is a **general-purpose** pencil.dev skill. A change belongs here if it would benefit
any pencil.dev user, regardless of their project.

If your change is specific to your project's design system, component library, or workflow,
it belongs in a fork, not here.

---

## Skill Authoring Tips

The skill lives in `skills/pencil-design/SKILL.md`. When editing it:

- The `description` frontmatter field controls when the skill activates, so be precise.
  Include the exact phrases users are likely to say.
- Keep the main `SKILL.md` focused on the core workflow. Move detailed edge cases
  or reference content to `skills/pencil-design/references/`.
- Always route `.pen` reads and writes through the Pencil MCP tools. The format is
  JSON and technically readable with file tools, but the MCP path gives you schema
  validation, screenshot feedback, and live-editor sync. It's also the contract the
  skill teaches.
- Document tool sequencing where it matters (e.g., call `get_editor_state` before
  `batch_design`).

If you use Claude Code, the `superpowers:writing-skills` skill provides useful guidance
for authoring high-quality SKILL.md content. It is entirely optional and not a dependency
of this project.

---

## Security Checks (OWASP AST)

Before opening a PR, install the pre-commit hook so the OWASP Agentic Skills
Top 10 checks run on every commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

The `tools/skill-lint.py` script enforces:

- `SKILL.md` frontmatter loads safely under `yaml.safe_load` and contains the
  required fields (`name`, `description`, `license`, `version`/`metadata.version`)
- `name` matches the skill's directory
- A `permissions:` block exists with `shell: none`, `network: none`,
  `filesystem: none|project-only`, and an explicit `mcp` allowlist
- All three platform manifests (`.claude-plugin/plugin.json`,
  `.cursor-plugin/plugin.json`, `gemini-extension.json`) carry a
  `permissions` field equal to the SKILL.md block
- No dangerous patterns in skill bodies (`curl | bash`, writes to
  `MEMORY.md` / `SOUL.md` / `AGENTS.md` / `CLAUDE.md` / `.env` / `~/.ssh`)
- Every `uses:` in `.github/workflows/*.yml` is pinned to a 40-char SHA

If you have a legitimate reason to deviate, suppress the finding with a
non-empty justification:

- For `permissions:`, add an `allowlist-justification: "<reason>"` sibling
  key in the same mapping.
- For workflow `uses:` lines, append `# skill-lint: AST07 allow — <reason>`.
- For dangerous patterns inside an illustrative fenced code block, mark the
  opening fence: ` ```bash skill-lint:AST01 allow — <reason>`.

Empty justifications are themselves errors.

The full mapping of AST risks to controls lives in [SECURITY.md](./SECURITY.md).

---

## Versioning

After any meaningful change, bump the version in:
- `.claude-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `skills/pencil-design/SKILL.md` frontmatter
- Add an entry to `docs/CHANGELOG.md`

(`gemini-extension.json` doesn't declare a version field.)

Follow [Semantic Versioning](https://semver.org/):

| Change type | Version bump |
|-------------|-------------|
| Typo fix, clarification | PATCH (`0.1.x`) |
| New capability or trigger phrases | MINOR (`0.x.0`) |
| Breaking workflow restructure | MAJOR (`x.0.0`) |
