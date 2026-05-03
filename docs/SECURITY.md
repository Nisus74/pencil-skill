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

- **Prompt injection** via SKILL.md content that could subvert AI behavior
- **Malicious links** in documentation
- **Secrets accidentally committed** to the repo (gitleaks runs on every PR)

If you believe any of the above has occurred, please report it via the channels above.
