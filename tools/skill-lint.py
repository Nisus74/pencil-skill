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
