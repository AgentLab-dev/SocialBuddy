# Adapters

Adapters turn an external **source class** into `ContextRecord`s. They are **provider-agnostic**: a CRM adapter is not “Salesforce” until a live implementation sets `provider`.

## Status values

| Status | Meaning |
| --- | --- |
| `interface` | Document + protocol only (this revision) |
| `mock` | Emits labeled synthetic records |
| `live` | Authenticated dry-run has succeeded — **not claimed here** |

## Protocol

See [interface.md](interface.md) and `socialbuddy.adapters.ContextAdapter`.

Common rules for every adapter:

1. `ingest` is read-only with respect to the remote system.
2. Emit records that pass `context-record.schema.json`.
3. Run redaction before return.
4. Set `mock: true` on synthetic data.
5. Health checks never print secrets.
6. Writes belong on a separate outbound port with approval — not on the adapter.

## Inventory

| Class | Doc | Typical records |
| --- | --- | --- |
| LinkedIn | [linkedin.md](linkedin.md) | `profile_fact`, `excerpt`, `engagement_signal` |
| GitHub | [github.md](github.md) | `skill_signal`, `document_chunk`, `event` |
| Web | [web.md](web.md) | `excerpt`, `claim` |
| Documents | [documents.md](documents.md) | `document_chunk` |
| CRM | [crm.md](crm.md) | `opportunity`, `relationship` |
| Email | [email.md](email.md) | `excerpt`, `relationship` |
| Calendar | [calendar.md](calendar.md) | `event` |
