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
Include the exact prompt that triggered the issue and evidence of the incorrect behavior
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
   - Install the plugin locally in Claude Code: `/plugin install .` (from the repo root)
   - Try your trigger phrases and verify the skill activates and behaves correctly
   - Test at least one edge case

4. **Open a PR** using the pull request template and fill in all sections.
   "It works" is not sufficient evidence — include specific before/after examples.

---

## What Belongs Here

This is a **general-purpose** pencil.dev skill. A change belongs here if it would benefit
any pencil.dev user, regardless of their project.

If your change is specific to your project's design system, component library, or workflow,
it belongs in a fork — not here.

---

## Skill Authoring Tips

The skill lives in `skills/pencil-design/SKILL.md`. When editing it:

- The `description` frontmatter field controls when the skill activates — be precise.
  Include the exact phrases users are likely to say.
- Keep the main `SKILL.md` focused on the core workflow. Move detailed edge cases
  or reference content to `skills/pencil-design/references/`.
- Never instruct the AI to use `Read`, `Grep`, or other file tools on `.pen` files —
  they are encrypted and must be accessed via the Pencil MCP tools only.
- Document tool sequencing where it matters (e.g., call `get_editor_state` before
  `batch_design`).

If you use Claude Code, the `superpowers:writing-skills` skill (from the
[superpowers plugin](https://github.com/superpowers)) provides useful guidance for
authoring high-quality SKILL.md content. It is entirely optional and not a dependency
of this project.

---

## Versioning

After any meaningful change, bump the version in:
- `.claude-plugin/plugin.json`
- `.cursor-plugin/plugin.json` (keep in sync)
- `skills/pencil-design/SKILL.md` frontmatter

Follow [Semantic Versioning](https://semver.org/):

| Change type | Version bump |
|-------------|-------------|
| Typo fix, clarification | PATCH (`0.1.x`) |
| New capability or trigger phrases | MINOR (`0.x.0`) |
| Breaking workflow restructure | MAJOR (`x.0.0`) |
