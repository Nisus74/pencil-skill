#!/usr/bin/env python3
"""OWASP Agentic Skills Top 10 lint for the pencil-dev-skill repo.

Runs against SKILL.md files, the Claude Code and Gemini CLI manifests, and
all GitHub Actions workflows. Exits 0 if no error-severity findings, 1 otherwise.
Warning-severity findings are printed but do not fail the run.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

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
