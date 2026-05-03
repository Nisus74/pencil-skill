#!/usr/bin/env python3
"""OWASP Agentic Skills Top 10 lint for the pencil-dev-skill repo.

Runs against SKILL.md files, the Claude Code and Gemini CLI manifests, and
all GitHub Actions workflows. Exits 0 if no error-severity findings, 1 otherwise.
Warning-severity findings are printed but do not fail the run.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

SEVERITY_ERROR = "error"
SEVERITY_WARN = "warn"


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    location: str
    message: str

    def format(self) -> str:
        return f"{self.code} [{self.severity}] {self.location}: {self.message}"


_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def _read_frontmatter(path: Path) -> tuple[str | None, Finding | None]:
    """Return (raw_frontmatter, error_finding). Exactly one is non-None."""
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None, Finding(
            code="AST05",
            severity=SEVERITY_ERROR,
            location=str(path),
            message="no YAML frontmatter delimited by '---' found",
        )
    return m.group(1), None


def check_frontmatter_loads_safely(path: Path) -> list[Finding]:
    raw, err = _read_frontmatter(path)
    if err:
        return [err]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return [Finding(
            code="AST05",
            severity=SEVERITY_ERROR,
            location=str(path),
            message=f"frontmatter failed yaml.safe_load: {e}",
        )]
    if not isinstance(data, dict):
        return [Finding(
            code="AST05",
            severity=SEVERITY_ERROR,
            location=str(path),
            message="frontmatter is not a YAML mapping",
        )]
    return []


_REQUIRED_FIELDS = ("name", "description", "license")
_MIN_DESCRIPTION_CHARS = 50


def _load_frontmatter(path: Path) -> dict | None:
    raw, err = _read_frontmatter(path)
    if err or raw is None:
        return None
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def check_frontmatter_required_fields(path: Path) -> list[Finding]:
    data = _load_frontmatter(path)
    if data is None:
        return []  # AST05 already reported it
    findings: list[Finding] = []
    for field in _REQUIRED_FIELDS:
        if not data.get(field):
            findings.append(Finding(
                code="AST04",
                severity=SEVERITY_ERROR,
                location=str(path),
                message=f"missing required frontmatter field: {field}",
            ))
    has_top_version = bool(data.get("version"))
    has_meta_version = bool((data.get("metadata") or {}).get("version"))
    if not (has_top_version or has_meta_version):
        findings.append(Finding(
            code="AST04",
            severity=SEVERITY_ERROR,
            location=str(path),
            message="missing version: declare 'version' or 'metadata.version'",
        ))
    return findings


def check_name_matches_directory(path: Path) -> list[Finding]:
    data = _load_frontmatter(path)
    if data is None:
        return []
    name = data.get("name")
    expected = path.parent.name
    if name and name != expected:
        return [Finding(
            code="AST04",
            severity=SEVERITY_ERROR,
            location=str(path),
            message=f"frontmatter name '{name}' does not match directory '{expected}'",
        )]
    return []


def check_description_substantive(path: Path) -> list[Finding]:
    data = _load_frontmatter(path)
    if data is None:
        return []
    desc = (data.get("description") or "").strip()
    if 0 < len(desc) < _MIN_DESCRIPTION_CHARS:
        return [Finding(
            code="AST04",
            severity=SEVERITY_WARN,
            location=str(path),
            message=f"description is {len(desc)} chars (recommend ≥ {_MIN_DESCRIPTION_CHARS})",
        )]
    return []


_REQUIRED_PERMISSION_KEYS = ("mcp", "shell", "filesystem", "network")
_ALLOWED_DEFAULTS = {
    "shell": {"none"},
    "filesystem": {"none", "project-only"},
    "network": {"none"},
}


def check_permissions_block(path: Path) -> list[Finding]:
    data = _load_frontmatter(path)
    if data is None:
        return []
    perms = data.get("permissions")
    if not isinstance(perms, dict):
        return [Finding(
            code="AST03",
            severity=SEVERITY_ERROR,
            location=str(path),
            message="missing 'permissions:' block in frontmatter",
        )]
    findings: list[Finding] = []
    for key in _REQUIRED_PERMISSION_KEYS:
        if key not in perms:
            findings.append(Finding(
                code="AST03",
                severity=SEVERITY_ERROR,
                location=str(path),
                message=f"permissions block missing required key '{key}'",
            ))
    justification = perms.get("allowlist-justification")
    has_justification = isinstance(justification, str) and justification.strip() != ""
    if "allowlist-justification" in perms and not has_justification:
        findings.append(Finding(
            code="AST03",
            severity=SEVERITY_ERROR,
            location=str(path),
            message="allowlist-justification must be a non-empty string",
        ))
    for key, allowed in _ALLOWED_DEFAULTS.items():
        value = perms.get(key)
        if value is not None and value not in allowed and not has_justification:
            findings.append(Finding(
                code="AST03",
                severity=SEVERITY_ERROR,
                location=str(path),
                message=(
                    f"permissions.{key}={value!r} is outside the safe default "
                    f"({sorted(allowed)}); add a non-empty 'allowlist-justification'"
                ),
            ))
    return findings


def lint_paths(paths: list[Path]) -> list[Finding]:
    """Return findings for the given paths. Empty list = clean."""
    findings: list[Finding] = []
    return findings


def collect_canonical_paths() -> list[Path]:
    """Default lint set when no args are given."""
    return [
        *sorted(REPO_ROOT.glob("skills/*/SKILL.md")),
        REPO_ROOT / ".claude-plugin" / "plugin.json",
        REPO_ROOT / "gemini-extension.json",
        *sorted(REPO_ROOT.glob(".github/workflows/*.yml")),
        *sorted(REPO_ROOT.glob(".github/workflows/*.yaml")),
    ]


def main(argv: list[str]) -> int:
    args = argv[1:]
    paths = [Path(a) for a in args] if args else collect_canonical_paths()
    findings = lint_paths(paths)
    for f in findings:
        print(f.format())
    return 1 if any(f.severity == SEVERITY_ERROR for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
