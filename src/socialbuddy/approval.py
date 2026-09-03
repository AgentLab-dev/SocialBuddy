"""Outbound approval gate. No send path exists without a matching decision."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any


class OutboundAction(str, Enum):
    POST = "post"
    ARTICLE = "article"
    COMMENT = "comment"
    REACT = "react"
    INVITE = "connect"
    MESSAGE = "message"
    INMAIL = "inmail"
    CRM_CONTACT = "crm_contact"
    EMAIL_SEND = "email_send"


class ApprovalRequired(RuntimeError):
    """Raised when a write is attempted without a valid approval artifact."""


@dataclass(frozen=True)
class ApprovalDecision:
    action: OutboundAction
    payload_hash: str
    payload_preview: str
    decided_by: str
    decision: str
    decided_at: str
    expires_at: str
    scope: str = "single_payload"

    def is_approved(self) -> bool:
        return self.decision == "approved"


def canonical_payload(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def payload_hash(payload: Any) -> str:
    return hashlib.sha256(canonical_payload(payload)).hexdigest()


def _parse_iso(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def require_approval(
    action: OutboundAction | str,
    payload: Any,
    decision: ApprovalDecision | None,
    *,
    now: datetime | None = None,
) -> ApprovalDecision:
    """Return the decision if it authorizes this exact action+payload; else raise."""
    if isinstance(action, str):
        action = OutboundAction(action)
    if decision is None:
        raise ApprovalRequired(
            f"{action.value} blocked: no approval artifact. Drafts may be stored; sends may not."
        )
    if decision.scope != "single_payload":
        raise ApprovalRequired("Blanket or template approvals are not accepted.")
    if decision.action != action:
        raise ApprovalRequired(
            f"Approval is for {decision.action.value}, not {action.value}."
        )
    expected = payload_hash(payload)
    if decision.payload_hash != expected:
        raise ApprovalRequired(
            "Approval payload_hash does not match the current payload. Re-approve after edits."
        )
    if decision.decision != "approved":
        raise ApprovalRequired(f"Decision is {decision.decision!r}, not approved.")
    clock = now or datetime.now(timezone.utc)
    if clock.tzinfo is None:
        clock = clock.replace(tzinfo=timezone.utc)
    if _parse_iso(decision.expires_at) <= clock:
        raise ApprovalRequired("Approval has expired. Request a new decision.")
    return decision
