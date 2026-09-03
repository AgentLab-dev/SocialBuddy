# Context layer

Context is how SocialBuddy **grounds** skills. A model without context will invent a career; a model with labeled context can still invent — the schema makes that a detectable defect.

This folder is infrastructure and policy. **No live connectors ship here.** Samples are synthetic.

## Canonical unit

A **context record** (`schema/context-record.schema.json`) is one claim or excerpt plus provenance. Records compose into a **bundle** for a job (profile validation, post draft, sourcing list).

Required ideas on every record:

| Field | Role |
| --- | --- |
| `id` | Stable id in the store |
| `kind` | What it is (`profile_fact`, `claim`, `excerpt`, …) |
| `statement` | Operator-facing text |
| `epistemic_status` | `verified` / `operator_asserted` / `inferred` / `unknown` / `disputed` |
| `provenance` | Where it came from and when |
| `confidence` | 0–1 plus method |
| `freshness` | `observed_at`, `as_of`, TTL |
| `redaction` | Whether PII/secrets were stripped |
| `sensitivity` | `public` / `internal` / `confidential` / `restricted` |

## Policies

| Policy | File |
| --- | --- |
| Provenance + freshness | [policies/provenance-and-freshness.md](policies/provenance-and-freshness.md) |
| Confidence | [policies/confidence.md](policies/confidence.md) |
| Chunking and synthesis | [policies/chunking-and-synthesis.md](policies/chunking-and-synthesis.md) |
| Redaction and PII | [policies/redaction-and-pii.md](policies/redaction-and-pii.md) |
| Conflict resolution | [policies/conflict-resolution.md](policies/conflict-resolution.md) |

## Adapters

Adapters implement one ingest interface and emit records. They do not post, email, or mutate SaaS objects. See [adapters/README.md](adapters/README.md).

Classes (provider-agnostic): LinkedIn, GitHub, web, documents, CRM, email, calendar.

## Samples

[samples/](samples/) contains a **mock** bundle. Names and companies are invented. Tests fail if the mock flag is missing.
