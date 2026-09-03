"""Provider-agnostic adapter protocol. No network clients ship here."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from socialbuddy.context import ContextRecord


@dataclass(frozen=True)
class IngestRequest:
    source_class: str
    payload: dict[str, Any]
    operator_id: str
    allow_network: bool = False
    mock: bool = True


@dataclass(frozen=True)
class AdapterHealth:
    status: str
    detail: str
    live: bool = False


class ContextAdapter(Protocol):
    provider: str | None
    status: str
    capabilities: tuple[str, ...]

    def ingest(self, request: IngestRequest) -> list[ContextRecord]:
        ...

    def health(self) -> AdapterHealth:
        ...


@dataclass
class InterfaceAdapter:
    """Default adapter: documents the class, never hits the network."""

    source_class: str
    capabilities: tuple[str, ...] = ()
    provider: str | None = None
    status: str = "interface"

    def ingest(self, request: IngestRequest) -> list[ContextRecord]:
        if request.allow_network:
            raise RuntimeError(
                f"{self.source_class} adapter is interface-only; "
                "no live client is available (A-002)."
            )
        return []

    def health(self) -> AdapterHealth:
        return AdapterHealth(
            status="interface",
            detail="No live credentials or client. Use operator paste or implement a vendor wrapper.",
            live=False,
        )


INTERFACE_ADAPTERS: dict[str, InterfaceAdapter] = {
    name: InterfaceAdapter(source_class=name, capabilities=caps)
    for name, caps in {
        "linkedin": ("profile_read", "posts_read", "featured_read"),
        "github": ("repo_meta", "commit_or_pr", "readme_docs"),
        "web": ("page_extract",),
        "document": ("file_chunk",),
        "crm": ("account_read", "opportunity_read", "contact_read"),
        "email": ("thread_extract",),
        "calendar": ("event_read",),
    }.items()
}


def get_adapter(source_class: str) -> InterfaceAdapter:
    try:
        return INTERFACE_ADAPTERS[source_class]
    except KeyError as exc:
        raise KeyError(f"Unknown source class: {source_class}") from exc
