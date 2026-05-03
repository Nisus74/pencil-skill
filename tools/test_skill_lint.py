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


class FrontmatterRequiredFieldsTest(unittest.TestCase):
    def _skill(self, tmp: Path, frontmatter: str, dirname: str = "myskill") -> Path:
        d = tmp / dirname
        d.mkdir()
        p = d / "SKILL.md"
        p.write_text(f"---\n{frontmatter}\n---\nbody\n")
        return p

    def test_all_required_fields_present(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = self._skill(Path(tmp), (
                "name: myskill\n"
                "description: A long enough description for the substantive check to pass.\n"
                "license: MIT\n"
                "metadata:\n  version: '1.0.0'\n"
            ))
            self.assertEqual(skill_lint.check_frontmatter_required_fields(p), [])

    def test_missing_name_is_error(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = self._skill(Path(tmp), "description: x\nlicense: MIT\nmetadata:\n  version: '1'\n")
            findings = skill_lint.check_frontmatter_required_fields(p)
            self.assertTrue(any(f.code == "AST04" and "name" in f.message for f in findings))

    def test_top_level_version_also_accepted(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = self._skill(Path(tmp), (
                "name: myskill\n"
                "description: A long enough description for the substantive check to pass.\n"
                "license: MIT\n"
                "version: '1.0.0'\n"
            ))
            self.assertEqual(skill_lint.check_frontmatter_required_fields(p), [])


class NameMatchesDirectoryTest(unittest.TestCase):
    def test_match(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "pencil-design"
            d.mkdir()
            p = d / "SKILL.md"
            p.write_text("---\nname: pencil-design\n---\n")
            self.assertEqual(skill_lint.check_name_matches_directory(p), [])

    def test_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "pencil-design"
            d.mkdir()
            p = d / "SKILL.md"
            p.write_text("---\nname: other-name\n---\n")
            findings = skill_lint.check_name_matches_directory(p)
            self.assertEqual(findings[0].code, "AST04")
            self.assertEqual(findings[0].severity, "error")


class DescriptionSubstantiveTest(unittest.TestCase):
    def test_long_description_ok(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "SKILL.md"
            p.write_text("---\ndescription: " + ("x" * 60) + "\n---\n")
            self.assertEqual(skill_lint.check_description_substantive(p), [])

    def test_short_description_warns(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "SKILL.md"
            p.write_text("---\ndescription: short\n---\n")
            findings = skill_lint.check_description_substantive(p)
            self.assertEqual(findings[0].code, "AST04")
            self.assertEqual(findings[0].severity, "warn")


if __name__ == "__main__":
    unittest.main()
