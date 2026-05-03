# OWASP Agentic Skills Top 10 Compliance — Design

**Date:** 2026-05-03
**Status:** Approved (pending implementation plan)
**Scope:** `pencil-dev-skill` repository (the public skill plugin), not consuming projects.

---

## Goal

Bring the `pencil-dev-skill` repository into 100% alignment with the
[OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
(AST01–AST10) before the public release, and enforce that alignment automatically
via a pre-commit hook and a CI workflow so the bar cannot regress silently.

## Non-goals

- Hardening the Pencil MCP server itself (out of repo scope).
- Hardening consuming projects that install this skill.
- Building a generic OWASP-AST scanner for arbitrary skills (the lint here is
  tailored to this repo's three manifests and its `SKILL.md`; it can be
  extracted later if useful).
- Release signing (ed25519) and content-hash pinning — deferred until a
  consuming registry exists that verifies them.

## Risk → control mapping

Every AST risk gets either an enforced control or an explicit, documented N/A.

| Code | Risk | Control | Enforcement |
|---|---|---|---|
| AST01 | Malicious skills | Lint scans `SKILL.md` content for shell-eval patterns, exfiltration, and writes to identity/secret paths | `tools/skill-lint.py` + pre-commit + CI |
| AST02 | Supply chain compromise | Pin all GitHub Actions to 40-char commit SHAs (with `# vX.Y.Z` comment); `CODEOWNERS` requires maintainer review on every PR; existing gitleaks | Lint regex + `CODEOWNERS` + branch protection (manual repo setting) |
| AST03 | Over-privileged skills | Declare a `permissions:` block in `SKILL.md` frontmatter (and mirrored in both manifests); lint enforces a strict default-deny allowlist | Lint requires `shell: none`, `network: none`, `filesystem ∈ {none, project-only}` unless an `allowlist-justification` sibling key explains otherwise |
| AST04 | Insecure metadata | Lint validates required frontmatter / manifest fields are present, non-trivial, and consistent across `SKILL.md`, `plugin.json`, `gemini-extension.json` | Lint cross-manifest check |
| AST05 | Unsafe deserialization | Lint loads YAML with `yaml.safe_load` (rejects Python tags); JSON parsed with stdlib `json`; lint fails on parse error | Lint loader choice + try/except → error finding |
| AST06 | Weak isolation | **N/A — docs-only repo, no runtime.** Documented in `SECURITY.md` | Documentation |
| AST07 | Update drift | Same SHA-pinning rule as AST02; `dependabot.yml` opens grouped weekly bumps so pins stay fresh without manual drift | Lint regex + Dependabot |
| AST08 | Poor scanning | The `skill-lint` script + pre-commit + CI **is** the scanning layer. PR template requires the contributor checkbox | Pre-commit + CI workflow |
| AST09 | No governance | `CODEOWNERS`, expanded `SECURITY.md`, existing CHANGELOG/semver, PR template gate | Repo configuration + docs |
| AST10 | Cross-platform reuse | Lint runs against all three manifests (`plugin.json`, `gemini-extension.json`, `SKILL.md` frontmatter) so a divergent compromise on one platform is caught | Cross-manifest consistency check in lint |

## Components

### 1. `tools/skill-lint.py`

A single Python 3 script (~200 lines, stdlib + PyYAML only). Invoked as:

```
python3 tools/skill-lint.py [PATH ...]
```

When called with no paths it lints the canonical set:
`skills/*/SKILL.md`, `.claude-plugin/plugin.json`, `gemini-extension.json`,
and every `.github/workflows/*.yml`.

**Output format** — one finding per line:

```
AST03 [error] skills/pencil-design/SKILL.md: missing 'permissions:' block in frontmatter
AST07 [error] .github/workflows/secret-scan.yml:6: 'actions/checkout@v4' is not pinned to a 40-char SHA
AST04 [warn]  .claude-plugin/plugin.json: 'description' is shorter than 50 characters
```

Exit code: `0` if no errors (warnings allowed), `1` otherwise.

**Check catalog** (each function emits zero or more findings):

| Function | AST | Severity | What it does |
|---|---|---|---|
| `check_frontmatter_loads_safely` | 05 | error | `yaml.safe_load` on `SKILL.md` frontmatter; non-mapping or Python-tag → error |
| `check_frontmatter_required_fields` | 04 | error | `name`, `description`, `license`, `metadata.version` (or top-level `version`) present and non-empty |
| `check_name_matches_directory` | 04 | error | Frontmatter `name` equals parent directory name |
| `check_description_substantive` | 04 | warn | `description` ≥ 50 chars |
| `check_permissions_block_present` | 03 | error | `permissions:` mapping exists with at least `mcp`, `shell`, `filesystem`, `network` keys |
| `check_permissions_minimal` | 03 | error | `shell` ∈ {`none`} unless an `allowlist-justification` sibling key explains; same for `filesystem` (`none` or `project-only`) and `network` (`none`) |
| `check_dangerous_content` | 01 | error | Regex scan of `SKILL.md` body (excluding fenced code blocks marked `# nolint:AST01` on the opening fence) for: `\beval\b`, `curl[^\n]*\|\s*(sh|bash)`, `wget[^\n]*\|\s*(sh|bash)`, `base64\s+-d[^\n]*\|\s*(sh|bash)`, writes to `MEMORY\.md`, `SOUL\.md`, `AGENTS\.md`, `CLAUDE\.md`, `\.env`, `~/\.ssh` |
| `check_cross_manifest_consistency` | 04, 10 | error | `plugin.json.name` (sans org prefix) matches a skill directory name; `description` non-empty in `plugin.json` and `gemini-extension.json`; both manifests must declare a `permissions` field equal to the `SKILL.md` `permissions` block |
| `check_workflow_pin` | 02, 07 | error | Each `uses:` in `.github/workflows/*.yml` matches `^[a-z0-9._/-]+@[a-f0-9]{40}( +#.*)?$` |

**Exemption mechanism** — A finding can be suppressed by adding the inline
comment `# skill-lint: AST0X allow — <reason>` on the same line (for workflow
files) or by adding an `allowlist-justification: "<reason>"` sibling key in
the YAML mapping (for `permissions`). Exemptions without a non-empty reason
are themselves errors.

### 2. `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: <pinned-sha>  # v5.0.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/gitleaks/gitleaks
    rev: <pinned-sha>  # v8.x
    hooks:
      - id: gitleaks

  - repo: local
    hooks:
      - id: skill-lint
        name: OWASP AST skill lint
        entry: python3 tools/skill-lint.py
        language: system
        files: '^(skills/.*/SKILL\.md|\.claude-plugin/plugin\.json|gemini-extension\.json|\.github/workflows/.*\.ya?ml)$'
        pass_filenames: true
```

All third-party hooks are pinned to immutable SHAs (eat our own dog food).

### 3. `.github/workflows/skill-lint.yml`

A new workflow, runs on `push` to `main` and on every `pull_request`:

```yaml
name: Skill Lint
on:
  push:
    branches: [main]
  pull_request:
jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>  # v4.x
      - uses: actions/setup-python@<sha>  # v5.x
        with: { python-version: '3.12' }
      - run: pip install pre-commit
      - run: pre-commit run --all-files --show-diff-on-failure
```

The existing `.github/workflows/secret-scan.yml` is also re-pinned to SHAs as
part of this work (it currently uses `@v4` / `@v2` floating tags).

### 4. Manifest changes

**`SKILL.md` frontmatter** — add the `permissions:` block:

```yaml
permissions:
  mcp:
    - pencil:get_editor_state
    - pencil:open_document
    - pencil:get_guidelines
    - pencil:batch_get
    - pencil:batch_design
    - pencil:snapshot_layout
    - pencil:get_screenshot
    - pencil:get_variables
    - pencil:set_variables
    - pencil:find_empty_space_on_canvas
    - pencil:search_all_unique_properties
    - pencil:replace_all_matching_properties
    - pencil:export_nodes
  shell: none
  filesystem: project-only  # reads ./design-system/ and writes scaffolded templates
  network: none
```

**`.claude-plugin/plugin.json`** — add a `"permissions"` field mirroring the
above (Claude Code's plugin schema does not yet enforce it; this declaration
is forward-looking and is what the lint enforces today).

**`gemini-extension.json`** — same `"permissions"` field.

The lint's `check_cross_manifest_consistency` enforces that the three stay in
agreement.

### 5. Governance bits

- **`CODEOWNERS`** at repo root: `* @Nisus74`. Combined with branch protection
  (a manual GitHub setting, called out in the implementation plan as a manual
  step), every change requires owner review.
- **`docs/SECURITY.md`** — append the full AST risk → control table from
  this spec, plus a new "Reporting a malicious skill update" section that
  explains how a downstream user can report a compromised release.
- **`docs/CONTRIBUTING.md`** — add a "Security checks (OWASP AST)" section:
  what the lint enforces, how to install pre-commit, how to write a
  justified exemption.
- **`docs/CHANGELOG.md`** — entry under a new minor version (`0.2.0`).
  Bump `metadata.version` in `SKILL.md` frontmatter and `version` in both
  manifests to match.
- **`.github/PULL_REQUEST_TEMPLATE.md`** — add a checkbox:
  `- [ ] I ran 'pre-commit run --all-files' and all OWASP AST checks pass.`
- **`.github/dependabot.yml`** — weekly grouped bumps for the
  `github-actions` and `pip` ecosystems so SHA pins stay current.

## Data flow

```
contributor edits a file
  └─ git commit
      └─ pre-commit hook fires
          ├─ check-yaml / check-json / end-of-file-fixer / trailing-whitespace
          ├─ gitleaks (secret scan)
          └─ skill-lint  ──► finds AST violations? exit 1, commit aborted
contributor pushes / opens PR
  └─ GitHub Actions
      ├─ secret-scan.yml (gitleaks, SHA-pinned)
      └─ skill-lint.yml  (pre-commit run --all-files)
          └─ failure blocks the merge (with branch protection)
```

## Testing

The lint script ships with unit tests at `tools/test_skill_lint.py`
(stdlib `unittest`, runnable as `python3 -m unittest tools.test_skill_lint`).
Coverage targets:

- Each `check_*` function: at least one passing fixture, at least one failing
  fixture asserting both the AST code and severity.
- Exemption mechanism: a finding is suppressed by a justified exemption,
  emitted again by an empty-reason exemption.
- `check_workflow_pin`: passes for `actions/checkout@<40-char-sha> # v4.2.2`,
  fails for `@v4`, fails for `@<short-sha>`.

The test suite runs as a separate `pre-commit` local hook *and* as an
additional step in `.github/workflows/skill-lint.yml`.

End-to-end check after implementation: run `pre-commit run --all-files` on a
clean checkout — must exit 0.

## Implementation order

1. Land `tools/skill-lint.py` + tests against the **current** repo (will
   produce a known set of failures — expected and used as fixtures).
2. Add the `permissions` block to `SKILL.md` and both manifests; re-run lint;
   confirm AST03/AST04 findings clear.
3. Re-pin every workflow `uses:` to a 40-char SHA with version comment;
   confirm AST02/AST07 findings clear.
4. Add `.pre-commit-config.yaml` (with pinned SHAs) and `.github/workflows/skill-lint.yml`.
5. Add `CODEOWNERS`, `dependabot.yml`, PR template checkbox.
6. Expand `SECURITY.md` with the AST table; expand `CONTRIBUTING.md` with the
   security-checks section.
7. Bump versions, add CHANGELOG entry.
8. Manual step (called out in the plan, not automated): enable branch
   protection in GitHub repo settings — require status checks `Skill Lint`
   and `Secret Scan` to pass before merging to `main`.

## Open questions for the implementation plan

None blocking. The implementation plan can pick up directly from §
"Implementation order".
