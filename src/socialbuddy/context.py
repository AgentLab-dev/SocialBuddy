"""Context records and a small stdlib JSON Schema checker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

from socialbuddy.skills import repo_root

__all__ = [
    "ContextRecord",
    "SchemaError",
    "load_bundle",
    "load_bundle_schema",
    "load_record_schema",
    "records_from_bundle",
    "repo_root",
    "validate_against",
    "validate_bundle",
]


@dataclass(frozen=True)
class ContextRecord:
    id: str
    kind: str
    statement: str
    epistemic_status: str
    mock: bool
    sensitivity: str
    raw: dict[str, Any]

    def public_eligible(self) -> bool:
        return (
            self.epistemic_status in {"verified", "operator_asserted"}
            and self.sensitivity == "public"
            and not self.mock
            and self.raw.get("redaction", {}).get("status") == "clear"
        )


def load_bundle(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_record_schema(root: Path | None = None) -> dict[str, Any]:
    base = root or repo_root()
    return json.loads(
        (base / "context" / "schema" / "context-record.schema.json").read_text(
            encoding="utf-8"
        )
    )


def load_bundle_schema(root: Path | None = None) -> dict[str, Any]:
    base = root or repo_root()
    return json.loads(
        (base / "context" / "schema" / "context-bundle.schema.json").read_text(
            encoding="utf-8"
        )
    )


class SchemaError(ValueError):
    pass


def _check_type(value: Any, expected: str) -> bool:
    mapping = {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "boolean": lambda v: isinstance(v, bool),
    }
    return mapping[expected](value)


def validate_against(schema: dict[str, Any], instance: Any, path: str = "$") -> None:
    """Validate a subset of JSON Schema (draft 2020-ish) without dependencies."""
    if "type" in schema and not _check_type(instance, schema["type"]):
        raise SchemaError(f"{path}: expected type {schema['type']}")

    if schema.get("type") == "object" and isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                raise SchemaError(f"{path}: missing required property {key}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(instance) - set(props)
            if extra:
                raise SchemaError(f"{path}: additional properties not allowed: {sorted(extra)}")
        for key, value in instance.items():
            if key in props:
                validate_against(props[key], value, f"{path}.{key}")

    if schema.get("type") == "array" and isinstance(instance, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict) and "$ref" not in item_schema:
            for i, item in enumerate(instance):
                validate_against(item_schema, item, f"{path}[{i}]")

    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaError(f"{path}: {instance!r} not in enum")

    if "minimum" in schema and isinstance(instance, (int, float)) and instance < schema["minimum"]:
        raise SchemaError(f"{path}: {instance} < minimum {schema['minimum']}")
    if "maximum" in schema and isinstance(instance, (int, float)) and instance > schema["maximum"]:
        raise SchemaError(f"{path}: {instance} > maximum {schema['maximum']}")
    if "minLength" in schema and isinstance(instance, str) and len(instance) < schema["minLength"]:
        raise SchemaError(f"{path}: string shorter than {schema['minLength']}")
    if "pattern" in schema and isinstance(instance, str):
        import re

        if not re.search(schema["pattern"], instance):
            raise SchemaError(f"{path}: does not match pattern")


def validate_bundle(bundle: dict[str, Any], root: Path | None = None) -> None:
    bundle_schema = load_bundle_schema(root)
    record_schema = load_record_schema(root)
    # Validate bundle envelope without resolving $ref on records.
    envelope = {
        k: v
        for k, v in bundle_schema.items()
        if k != "properties"
    }
    props = dict(bundle_schema.get("properties", {}))
    props["records"] = {"type": "array"}
    envelope["properties"] = props
    validate_against(envelope, bundle)
    if not isinstance(bundle.get("records"), list):
        raise SchemaError("$.records must be an array")
    for i, record in enumerate(bundle["records"]):
        validate_against(record_schema, record, f"$.records[{i}]")


def records_from_bundle(bundle: dict[str, Any]) -> list[ContextRecord]:
    out: list[ContextRecord] = []
    for raw in bundle["records"]:
        out.append(
            ContextRecord(
                id=raw["id"],
                kind=raw["kind"],
                statement=raw["statement"],
                epistemic_status=raw["epistemic_status"],
                mock=raw["mock"],
                sensitivity=raw["sensitivity"],
                raw=raw,
            )
        )
    return out
