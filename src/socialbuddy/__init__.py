"""SocialBuddy: skills, context records, adapters, and approval gates."""

from socialbuddy.approval import (
    ApprovalDecision,
    ApprovalRequired,
    OutboundAction,
    canonical_payload,
    payload_hash,
    require_approval,
)
from socialbuddy.context import ContextRecord, load_bundle
from socialbuddy.skills import Skill, load_catalog, load_skill

__version__ = "0.1.0"

__all__ = [
    "ApprovalDecision",
    "ApprovalRequired",
    "ContextRecord",
    "OutboundAction",
    "Skill",
    "__version__",
    "canonical_payload",
    "load_bundle",
    "load_catalog",
    "load_skill",
    "payload_hash",
    "require_approval",
]
