"""Unit tests for tools/skill-lint.py."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_LINT = _HERE / "skill-lint.py"
_spec = importlib.util.spec_from_file_location("skill_lint", _LINT)
skill_lint = importlib.util.module_from_spec(_spec)
sys.modules["skill_lint"] = skill_lint
assert _spec.loader is not None
_spec.loader.exec_module(skill_lint)


class FindingTest(unittest.TestCase):
    def test_format(self):
        f = skill_lint.Finding(
            code="AST04",
            severity="error",
            location="path/to/file.md",
            message="missing field",
        )
        self.assertEqual(
            f.format(),
            "AST04 [error] path/to/file.md: missing field",
        )


class MainTest(unittest.TestCase):
    def test_lint_paths_empty_returns_empty(self):
        self.assertEqual(skill_lint.lint_paths([]), [])

    def test_main_returns_zero_when_no_findings(self):
        self.assertEqual(skill_lint.main(["skill-lint.py"]), 0)


class FrontmatterLoadsSafelyTest(unittest.TestCase):
    def _write(self, tmp: Path, body: str) -> Path:
        p = tmp / "SKILL.md"
        p.write_text(body)
        return p

    def test_clean_frontmatter_no_findings(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(Path(tmp), "---\nname: x\n---\nbody\n")
            self.assertEqual(skill_lint.check_frontmatter_loads_safely(p), [])

    def test_python_tag_is_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(Path(tmp), "---\n!!python/object/apply:os.system ['id']\n---\n")
            findings = skill_lint.check_frontmatter_loads_safely(p)
            self.assertTrue(findings)
            self.assertEqual(findings[0].code, "AST05")
            self.assertEqual(findings[0].severity, "error")

    def test_missing_frontmatter_block(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(Path(tmp), "no frontmatter at all\n")
            findings = skill_lint.check_frontmatter_loads_safely(p)
            self.assertTrue(findings)
            self.assertEqual(findings[0].code, "AST05")


if __name__ == "__main__":
    unittest.main()
