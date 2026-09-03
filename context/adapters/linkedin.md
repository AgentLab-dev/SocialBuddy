# LinkedIn adapter (interface)

**Status:** `interface`. No live API client. Preferred v1: operator paste / official data export.

## Capabilities (read)

| Capability | Payload in | Records out |
| --- | --- | --- |
| `profile_read` | About, experience, education, certifications | `profile_fact` |
| `posts_read` | Operator’s posts or saved drafts | `excerpt`, `engagement_signal` (only if numbers are in the export) |
| `featured_read` | Featured items | `claim` with locators |

## Mapping rules

- One experience row → one `profile_fact` (title, org, start, end).
- Dates missing → `epistemic_status: unknown` on the date portion; do not infer “present” from a blank.
- Engagement counts: only if present in the export; method `direct_export`; TTL short.
- Other people’s profiles: **do not ingest** unless the operator is using an official, permitted product and the use case is sourcing (see workflow). Still no automated invite.

## Writes (not on this adapter)

Create post, comment, react, invite, InMail → `OutboundChannel` + approval. See `docs/adding-linkedin-integrations.md`.

## Forbidden

Scraping, cookie reuse, unofficial automation libraries, inventing connection counts.
