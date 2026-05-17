# Security Policy

## Supported Versions

Only the latest published version of `pencil-dev-skill` receives security updates.

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |
| Older   | No        |

## Reporting a Vulnerability

If you discover a security issue, please **do not open a public GitHub issue.**

Instead, report it privately using one of these channels:

1. **GitHub Security Advisories** (preferred):
   [Report a vulnerability](https://github.com/Nisus74/pencil-skill/security/advisories/new)
2. **Email:** tpolland@gmail.com

Please include:
- A description of the vulnerability
- Steps to reproduce
- Affected versions (if known)
- Any suggested mitigations

You can expect an initial response within 7 days. Once the issue is confirmed,
a fix will be prioritized based on severity.

## Scope

Because this repository contains only documentation and skill instructions
(no executable code), the realistic threat model is limited to:

- **Prompt injection** via SKILL.md content that could subvert AI behaviour
- **Malicious links** in documentation
- **Secrets accidentally committed** to the repo (gitleaks runs on every PR)

If you believe any of the above has occurred, please report it via the channels above.

---

## OWASP Agentic Skills Top 10: Compliance Map

This repo's controls against [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/).

| Code | Risk | Control in this repo |
|------|------|----------------------|
| AST01 | Malicious skills | `tools/skill-lint.py` scans `SKILL.md` for shell-eval, exfiltration, and writes to identity/secret paths. Runs in pre-commit and CI. |
| AST02 | Supply chain compromise | All GitHub Actions pinned to 40-char SHAs with version comments. `CODEOWNERS` requires maintainer review on every PR. Branch protection (manual repo setting) requires green Skill Lint and Secret Scan checks. |
| AST03 | Over-privileged skills | `SKILL.md` frontmatter may declare a `permissions:` block for documentation. The lint function `check_permissions_block` enforces a default-deny baseline and requires `allowlist-justification` for elevated access; call it explicitly for skills that opt in to formal permission declarations. |
| AST04 | Insecure metadata | Lint enforces required frontmatter fields, name-matches-directory, and substantive descriptions. All three platform manifests (`.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`) must carry `name` and `description`; lint enforces this. |
| AST05 | Unsafe deserialization | Frontmatter parsed via `yaml.safe_load`; lint rejects Python tags and non-mapping frontmatter. Manifests parsed via stdlib `json`. |
| AST06 | Weak isolation | **N/A.** This repo ships documentation only; there is no runtime under our control. Isolation is the responsibility of the AI host. |
| AST07 | Update drift | Same SHA-pin rule as AST02. Dependabot opens grouped weekly bumps (`github-actions`, `pip`) so pins stay current with reviewable diffs. |
| AST08 | Poor scanning | The lint + pre-commit + CI is the scanning layer. PR template requires the contributor to confirm a green run. |
| AST09 | No governance | `CODEOWNERS`, `SECURITY.md` (this file), `CHANGELOG.md`, semver, PR template gate, and branch protection (manual). |
| AST10 | Cross-platform reuse | Lint runs against all three platform manifests (`.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`). `name` and `version` must be identical across manifests, so a stealth update on one platform is caught before it reaches CI. |

## Reporting a malicious skill update

If you believe a published version of `pencil-dev-skill` is compromised
(unexpected manifest changes, new permissions, dangerous instructions in
`SKILL.md`), report it via the channels above and **uninstall the plugin
locally** until the issue is acknowledged. Include the plugin version
and a diff against the previous known-good version if possible.
