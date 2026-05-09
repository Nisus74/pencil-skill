#!/usr/bin/env python3
"""OWASP Agentic Skills Top 10 lint for the pencil-dev-skill repo.

Runs against SKILL.md files, the Claude Code / Gemini CLI / Cursor manifests,
and all GitHub Actions workflows. Exits 0 if no error-severity findings, 1
otherwise. Warning-severity findings are printed but do not fail the run.
"""
from __future__ import annotations

import json
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


_DANGEROUS_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("eval-shell", re.compile(r"\beval\s+[\"$`]")),
    ("curl-pipe-shell", re.compile(r"curl[^\n]*\|\s*(sh|bash|zsh)\b")),
    ("wget-pipe-shell", re.compile(r"wget[^\n]*\|\s*(sh|bash|zsh)\b")),
    ("base64-pipe-shell", re.compile(r"base64\s+-d[^\n]*\|\s*(sh|bash|zsh)\b")),
    ("write-MEMORY.md", re.compile(r"\bMEMORY\.md\b")),
    ("write-SOUL.md", re.compile(r"\bSOUL\.md\b")),
    # Narrowed: AGENTS.md / CLAUDE.md are commonly referenced in skill prose,
    # so require a write-intent verb on the same line to avoid false positives.
    ("write-AGENTS.md", re.compile(r"\b(write|append|modify|update|edit|overwrite|inject|patch)\b[^\n]*\bAGENTS\.md\b", re.IGNORECASE)),
    ("write-CLAUDE.md", re.compile(r"\b(write|append|modify|update|edit|overwrite|inject|patch)\b[^\n]*\bCLAUDE\.md\b", re.IGNORECASE)),
    ("dotenv-path", re.compile(r"(^|[\s/])\.env(\b|$)")),
    ("ssh-keys", re.compile(r"~/\.ssh\b")),
)

_FENCE_OPEN_RE = re.compile(r"^```([^\n]*)$")


def _split_fenced_blocks(body: str) -> list[tuple[str, str]]:
    """Yield (kind, text) where kind in {'prose', 'fence', 'fence-allowed'}.

    A fenced block is 'fence-allowed' iff its info string contains
    'skill-lint:AST01 allow' followed by a non-empty reason after dash/em-dash.
    """
    out: list[tuple[str, str]] = []
    lines = body.splitlines(keepends=True)
    i = 0
    buf: list[str] = []
    while i < len(lines):
        m = _FENCE_OPEN_RE.match(lines[i].rstrip("\n"))
        if m:
            if buf:
                out.append(("prose", "".join(buf)))
                buf = []
            info = m.group(1)
            allowed = bool(re.search(r"skill-lint:AST01 allow\s*[—-]\s*\S", info))
            i += 1
            block: list[str] = []
            while i < len(lines) and not lines[i].rstrip("\n").startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            out.append(("fence-allowed" if allowed else "fence", "".join(block)))
        else:
            buf.append(lines[i])
            i += 1
    if buf:
        out.append(("prose", "".join(buf)))
    return out


def check_dangerous_content(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    body = _FRONTMATTER_RE.sub("", text, count=1)
    findings: list[Finding] = []
    for kind, chunk in _split_fenced_blocks(body):
        if kind == "fence-allowed":
            continue
        for label, pat in _DANGEROUS_PATTERNS:
            if pat.search(chunk):
                findings.append(Finding(
                    code="AST01",
                    severity=SEVERITY_ERROR,
                    location=str(path),
                    message=f"dangerous pattern '{label}' found in skill body",
                ))
                break  # one finding per chunk per scan is enough
    return findings


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def check_cross_manifest_consistency(paths: list[Path]) -> list[Finding]:
    """Compare SKILL.md ↔ Claude / Cursor manifests.

    Claude (`.claude-plugin/plugin.json`) is required for the consistency
    check to run; Cursor (`.cursor-plugin/plugin.json`) is checked when present.
    """
    skill_paths = [p for p in paths if p.name == "SKILL.md"]
    plugin_path = next(
        (p for p in paths if p.name == "plugin.json" and p.parent.name == ".claude-plugin"),
        None,
    )
    cursor_path = next(
        (p for p in paths if p.name == "plugin.json" and p.parent.name == ".cursor-plugin"),
        None,
    )
    if not (skill_paths and plugin_path):
        return []

    findings: list[Finding] = []
    plugin = _load_json(plugin_path) or {}
    cursor = _load_json(cursor_path) if cursor_path else None

    manifests: list[tuple[Path, dict, str]] = [
        (plugin_path, plugin, ".claude-plugin/plugin.json"),
    ]
    if cursor_path is not None:
        manifests.append((cursor_path, cursor or {}, ".cursor-plugin/plugin.json"))

    for manifest_path, manifest, label in manifests:
        for field in ("name", "description"):
            if not manifest.get(field):
                findings.append(Finding(
                    code="AST04", severity=SEVERITY_ERROR,
                    location=str(manifest_path),
                    message=f"{label} missing or empty '{field}'",
                ))

    skill_dirnames = {p.parent.name for p in skill_paths}
    if plugin.get("name") and plugin["name"] not in skill_dirnames:
        findings.append(Finding(
            code="AST04", severity=SEVERITY_WARN,
            location=str(plugin_path),
            message=(
                f"plugin.json name '{plugin['name']}' is not a skill directory name "
                f"({sorted(skill_dirnames)})"
            ),
        ))

    for skill_md in skill_paths:
        skill_data = _load_frontmatter(skill_md) or {}
        skill_perms = skill_data.get("permissions")
        if skill_perms is None:
            continue
        for manifest_path, manifest, _label in manifests:
            manifest_perms = manifest.get("permissions")
            if manifest_perms is None:
                findings.append(Finding(
                    code="AST10", severity=SEVERITY_ERROR,
                    location=str(manifest_path),
                    message="manifest is missing 'permissions' field declared in SKILL.md",
                ))
                continue
            if manifest_perms != skill_perms:
                findings.append(Finding(
                    code="AST10", severity=SEVERITY_ERROR,
                    location=str(manifest_path),
                    message="permissions diverge from SKILL.md frontmatter",
                ))
    return findings


_USES_RE = re.compile(r"^\s*-\s*uses:\s*([^\s#]+)(.*)$")
_PINNED_RE = re.compile(r"^[A-Za-z0-9._/-]+@[a-fA-F0-9]{40}$")
_INLINE_ALLOW_RE = re.compile(r"#\s*skill-lint:\s*AST(02|07)\s+allow\s*[—-]\s*\S")


def check_workflow_pin(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = _USES_RE.match(line)
        if not m:
            continue
        ref = m.group(1)
        rest = m.group(2)
        if _INLINE_ALLOW_RE.search(rest):
            continue
        if not _PINNED_RE.match(ref):
            findings.append(Finding(
                code="AST07",
                severity=SEVERITY_ERROR,
                location=f"{path}:{lineno}",
                message=(
                    f"'{ref}' is not pinned to a 40-char SHA "
                    "(format: owner/repo@<40-hex>  # vX.Y.Z)"
                ),
            ))
    return findings


def lint_paths(paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for p in paths:
        if not p.exists():
            findings.append(Finding(
                code="AST08", severity=SEVERITY_ERROR,
                location=str(p), message="path does not exist",
            ))
            continue
        if p.name == "SKILL.md":
            findings += check_frontmatter_loads_safely(p)
            findings += check_frontmatter_required_fields(p)
            findings += check_name_matches_directory(p)
            findings += check_description_substantive(p)
            findings += check_permissions_block(p)
            findings += check_dangerous_content(p)
        elif p.suffix in (".yml", ".yaml") and ".github/workflows" in str(p):
            findings += check_workflow_pin(p)
    findings += check_cross_manifest_consistency(paths)
    return findings


def collect_canonical_paths() -> list[Path]:
    """Default lint set when no args are given."""
    paths = [
        *sorted(REPO_ROOT.glob("skills/*/SKILL.md")),
        REPO_ROOT / ".claude-plugin" / "plugin.json",
    ]
    cursor_manifest = REPO_ROOT / ".cursor-plugin" / "plugin.json"
    if cursor_manifest.exists():
        paths.append(cursor_manifest)
    paths.extend(sorted(REPO_ROOT.glob(".github/workflows/*.yml")))
    paths.extend(sorted(REPO_ROOT.glob(".github/workflows/*.yaml")))
    return paths


def main(argv: list[str]) -> int:
    args = argv[1:]
    paths = [Path(a) for a in args] if args else collect_canonical_paths()
    findings = lint_paths(paths)
    for f in findings:
        print(f.format())
    return 1 if any(f.severity == SEVERITY_ERROR for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
