"""Skill library contract tests."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialbuddy.skills import (  # noqa: E402
    REQUIRED_HEADINGS,
    has_labeled_example,
    load_catalog,
    load_skill,
    repo_root,
)
from socialbuddy.validate import validate_skills  # noqa: E402


class SkillFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = repo_root()
        cls.catalog = load_catalog(cls.root)

    def test_catalog_lists_seven_domain_skills(self) -> None:
        ids = {row["id"] for row in self.catalog["skills"]}
        self.assertEqual(
            ids,
            {
                "phd-writing",
                "phd-reading",
                "dbt-professional",
                "dbt-solution-architect",
                "snowflake-architect",
                "ai-enablement",
                "ai-architect",
            },
        )

    def test_required_headings_match_contract(self) -> None:
        self.assertEqual(tuple(self.catalog["required_headings"]), REQUIRED_HEADINGS)

    def test_each_skill_loads_and_matches_catalog(self) -> None:
        for entry in self.catalog["skills"]:
            skill = load_skill(self.root / entry["path"])
            self.assertEqual(skill.id, entry["id"])
            self.assertEqual(skill.category, entry["category"])
            for heading in REQUIRED_HEADINGS:
                self.assertIn(heading, skill.headings, msg=f"{skill.id} missing {heading}")
            self.assertTrue(
                has_labeled_example(skill.body),
                msg=f"{skill.id} examples are not labeled",
            )

    def test_validate_skills_clean(self) -> None:
        self.assertEqual(validate_skills(self.root), [])

    def test_invalid_fixture_is_rejected(self) -> None:
        path = self.root / "tests" / "fixtures" / "invalid-skill.md"
        skill = load_skill(path)
        missing = [h for h in REQUIRED_HEADINGS if h not in skill.headings]
        self.assertGreaterEqual(len(missing), 6)
        self.assertFalse(has_labeled_example(skill.body))


if __name__ == "__main__":
    unittest.main()
