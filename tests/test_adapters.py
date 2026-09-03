"""Interface adapters must not claim live access."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialbuddy.adapters import IngestRequest, get_adapter  # noqa: E402


class AdapterTests(unittest.TestCase):
    def test_known_classes(self) -> None:
        for name in ("linkedin", "github", "web", "document", "crm", "email", "calendar"):
            adapter = get_adapter(name)
            self.assertEqual(adapter.status, "interface")
            health = adapter.health()
            self.assertFalse(health.live)
            self.assertEqual(health.status, "interface")

    def test_network_ingest_refused(self) -> None:
        adapter = get_adapter("linkedin")
        with self.assertRaises(RuntimeError):
            adapter.ingest(
                IngestRequest(
                    source_class="linkedin",
                    payload={},
                    operator_id="op",
                    allow_network=True,
                )
            )

    def test_offline_ingest_is_empty(self) -> None:
        adapter = get_adapter("github")
        records = adapter.ingest(
            IngestRequest(source_class="github", payload={}, operator_id="op")
        )
        self.assertEqual(records, [])

    def test_unknown_class(self) -> None:
        with self.assertRaises(KeyError):
            get_adapter("not-a-source")


if __name__ == "__main__":
    unittest.main()
