"""Approval gate: no outbound action without an exact-payload decision."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialbuddy.approval import (  # noqa: E402
    ApprovalDecision,
    ApprovalRequired,
    OutboundAction,
    payload_hash,
    require_approval,
)


def _decision(text: str, **overrides: object) -> ApprovalDecision:
    data = {
        "action": OutboundAction.POST,
        "payload_hash": payload_hash(text),
        "payload_preview": text,
        "decided_by": "operator:test",
        "decision": "approved",
        "decided_at": "2026-04-01T15:00:00+00:00",
        "expires_at": "2026-04-02T15:00:00+00:00",
        "scope": "single_payload",
    }
    data.update(overrides)
    return ApprovalDecision(**data)  # type: ignore[arg-type]


class ApprovalTests(unittest.TestCase):
    def test_missing_decision_blocks(self) -> None:
        with self.assertRaises(ApprovalRequired):
            require_approval(OutboundAction.POST, "hello", None)

    def test_matching_approval_passes(self) -> None:
        text = "Example post body"
        now = datetime(2026, 4, 1, 16, 0, tzinfo=timezone.utc)
        decision = _decision(text)
        out = require_approval(OutboundAction.POST, text, decision, now=now)
        self.assertTrue(out.is_approved())

    def test_edit_invalidates_approval(self) -> None:
        decision = _decision("Example post body")
        now = datetime(2026, 4, 1, 16, 0, tzinfo=timezone.utc)
        with self.assertRaises(ApprovalRequired):
            require_approval(OutboundAction.POST, "Example post body.", decision, now=now)

    def test_wrong_action_blocked(self) -> None:
        text = "hi"
        decision = _decision(text, action=OutboundAction.POST)
        now = datetime(2026, 4, 1, 16, 0, tzinfo=timezone.utc)
        with self.assertRaises(ApprovalRequired):
            require_approval(OutboundAction.INVITE, text, decision, now=now)

    def test_expired_blocked(self) -> None:
        text = "hi"
        decision = _decision(text)
        now = datetime(2026, 4, 3, tzinfo=timezone.utc)
        with self.assertRaises(ApprovalRequired):
            require_approval(OutboundAction.POST, text, decision, now=now)

    def test_rejected_blocked(self) -> None:
        text = "hi"
        decision = _decision(text, decision="rejected")
        now = datetime(2026, 4, 1, 16, 0, tzinfo=timezone.utc)
        with self.assertRaises(ApprovalRequired):
            require_approval(OutboundAction.POST, text, decision, now=now)

    def test_blanket_scope_blocked(self) -> None:
        text = "hi"
        decision = _decision(text, scope="all_future")
        now = datetime(2026, 4, 1, 16, 0, tzinfo=timezone.utc)
        with self.assertRaises(ApprovalRequired):
            require_approval(OutboundAction.POST, text, decision, now=now)


if __name__ == "__main__":
    unittest.main()
