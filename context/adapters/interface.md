# Adapter interface

Executable shape (Python 3.11+):

```python
from socialbuddy.adapters import AdapterHealth, ContextAdapter, IngestRequest
```

## IngestRequest (logical fields)

| Field | Type | Notes |
| --- | --- | --- |
| `source_class` | str | Must match the adapter |
| `payload` | mapping | Provider-neutral: `text`, `uri`, `export`, `items` |
| `operator_id` | str | Who is requesting ingest |
| `allow_network` | bool | Default false in this revision |
| `mock` | bool | Force synthetic path |

If `allow_network` is true and no live client exists, the adapter must return health `unsupported` and **no** guessed records.

## ContextAdapter

- `provider`: `None` or vendor id
- `status`: `interface` | `mock` | `live`
- `capabilities`: tuple of capability tags (`profile_read`, `repo_read`, …)
- `ingest(request) -> list[ContextRecord]`
- `health() -> AdapterHealth`

## OutboundChannel (not an adapter)

Separate protocol for posts/messages. Requires `ApprovalDecision` and `payload_hash`. See `socialbuddy.approval`.

## Adding a vendor

1. Keep this interface.
2. Subclass or wrap with `provider="hubspot"` (example name).
3. Map vendor payloads → records in a pure function (unit-testable).
4. Do not change skills or workflows to mention the vendor.
