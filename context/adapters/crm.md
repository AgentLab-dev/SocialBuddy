# CRM adapter (interface)

**Status:** `interface`. Provider-agnostic (Salesforce, HubSpot, Attio, etc. are examples, not integrations).

## Capabilities (read)

| Capability | Records |
| --- | --- |
| `account_read` | `relationship` |
| `opportunity_read` | `opportunity` |
| `contact_read` | `relationship` (redact personal email by default) |

## Mapping rules

- Stage and amount are usually `confidential`. Public posts: **never** include amount or customer name unless `sensitivity: public` and legal/comms approved.
- Closed-lost reasons can be internally useful; they are not LinkedIn anecdotes without approval and anonymization.
- Deduplicate contacts by CRM id, not by name.

## Writes

CRM updates (log activity, create lead) are outbound and need approval plus a live client — not in this revision.
