from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_skill import validate_skill  # noqa: E402


class ValidateSkillTests(unittest.TestCase):
    def test_current_skill_passes_structure_validation(self) -> None:
        issues = validate_skill(ROOT)
        errors = [issue for issue in issues if issue[0] == "error"]
        self.assertEqual([], errors, "\n".join(f"{s}: {m}" for s, m in issues))

    def test_rejects_name_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "wrong-folder"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\nname: different-name\ndescription: Use when testing a malformed skill.\n---\n\n# Test\n",
                encoding="utf-8",
            )
            issues = validate_skill(root, deep=False)
            self.assertTrue(any("folder name" in message for severity, message in issues if severity == "error"))


if __name__ == "__main__":
    unittest.main()
