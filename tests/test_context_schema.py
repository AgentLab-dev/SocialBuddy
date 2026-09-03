"""Context schema and mock-sample tests."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialbuddy.context import (  # noqa: E402
    SchemaError,
    load_bundle,
    load_record_schema,
    records_from_bundle,
    repo_root,
    validate_against,
    validate_bundle,
)
from socialbuddy.validate import validate_samples  # noqa: E402


class ContextSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = repo_root()
        cls.sample = cls.root / "context" / "samples" / "mock-context-bundle.json"
        cls.bundle = load_bundle(cls.sample)

    def test_sample_validates(self) -> None:
        validate_bundle(self.bundle, root=self.root)

    def test_sample_is_labeled_mock(self) -> None:
        self.assertTrue(self.bundle["mock"])
        self.assertIn("MOCK", self.bundle["notes"].upper())
        for record in self.bundle["records"]:
            self.assertTrue(record["mock"])

    def test_mock_records_are_not_public_eligible(self) -> None:
        for record in records_from_bundle(self.bundle):
            self.assertFalse(record.public_eligible())

    def test_validate_samples_clean(self) -> None:
        self.assertEqual(validate_samples(self.root), [])

    def test_missing_required_field_fails(self) -> None:
        schema = load_record_schema(self.root)
        with self.assertRaises(SchemaError):
            validate_against(schema, {"id": "x"})


if __name__ == "__main__":
    unittest.main()
