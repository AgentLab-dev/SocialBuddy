# Workflow: approval before posting (and all outreach)

## Purpose

Ensure **no outbound LinkedIn (or CRM/email) write** occurs unless a human approved the exact payload.

## What counts as outbound

| Action | Approval required |
| --- | --- |
| Create/update a public post or article | Yes |
| Comment | Yes |
| Reaction used as coordinated campaign behavior | Yes |
| Invitation / follow | Yes |
| InMail / DM | Yes |
| CRM activity that contacts a human | Yes |
| Save draft locally | No |
| Validate skills / ingest paste | No |

## Approval artifact

Fields (see `socialbuddy.approval.ApprovalDecision`):

- `action` — enum of outbound types
- `payload_hash` — SHA-256 of canonical payload bytes
- `payload_preview` — text the human saw
- `decided_by` — operator id
- `decision` — `approved` | `rejected`
- `decided_at` — timestamp
- `expires_at` — default 24h (assumption); after expiry, re-approve
- `scope` — must **not** be “all future posts”

## Procedure

1. Canonicalize the payload (UTF-8, stable JSON keys if structured).
2. Hash. If the operator edits a comma, hash changes → old approval is invalid.
3. Show preview + intended recipients + channel + context record ids used.
4. Human decides. Record the artifact.
5. `require_approval(action, payload, decision)` returns the decision or raises `ApprovalRequired`.
6. Live clients (future) call this immediately before the HTTP write.

## Rules

- No implicit approval from a previous post.
- No approval of a *template* that later fills names.
- Batch campaigns: one campaign approval **plus** per-recipient payload hashes.
- Mock/demo modes still record artifacts; they still must not call a live API.

## Example

> **Example** — illustration only.

Payload: the incremental-models post text from `phd-writing`. Hash `e3b0c4…` (example). Decision `approved` by `operator:mock` at `2026-04-01T15:00:00Z`, expires 24h later. A follow-up edit of the last line invalidates it.
