# Adding future LinkedIn integrations

This repository does **not** ship a live LinkedIn integration. Use this page when you are ready to add one.

## Legal and product gates (do these first)

1. Read current [LinkedIn API Terms](https://www.linkedin.com/legal/l/api-terms) and the relevant product docs. Product names and scopes change; do not copy stale scope lists from blogs.
2. Decide the **official path**: Marketing / Community Management APIs, Recruiter System Connect, Sales Navigator Application Platform, or **operator-supplied exports** (copy-paste, data download). Unofficial scraping is out of scope forever.
3. Register an application only in an environment you control. Do not commit client secrets.
4. Map every intended action to **read** vs **write**. Writes require the approval gate.

## Recommended adapter shape

Implement `socialbuddy.adapters.ContextAdapter` in a new module, for example `src/socialbuddy/adapters/linkedin.py`, and keep it import-optional so validation stays dependency-free.

```
class LinkedInExportAdapter:
    provider = "linkedin"
    status = "interface"   # then "mock", then "live"
    capabilities = ("profile_read", "posts_read")  # add writes only with approval hook

    def ingest(self, request) -> list[ContextRecord]:
        ...

    def health(self) -> AdapterHealth:
        ...
```

Writes (create post, comment, invite, InMail) must **not** live on `ingest`. Put them on a separate `OutboundChannel` that accepts only an `ApprovalDecision` plus the exact payload hash.

## Suggested increment order

| Step | Capability | Context types produced | Write? |
| --- | --- | --- | --- |
| 1 | Operator paste of About / Experience / Featured | `profile_fact`, `claim` | No |
| 2 | Official profile read (when API access exists) | `profile_fact` with provenance URL | No |
| 3 | Draft posts in-repo | none (workflow artifact) | No |
| 4 | Official post create | none | **Yes — approval required** |
| 5 | Comment / react | `engagement_signal` | **Yes — approval required** |
| 6 | Invitation / InMail | `outreach_draft` | **Yes — approval required** |

Skip steps whose official product you do not have. A paste-only adapter is a complete, honest v1.

## Auth and secrets

- Store tokens in the operator’s secret manager, not in git.
- Rotate on leak. Treat any token that ever touched a chat log as burned.
- Health checks should report `unauthorized` without printing the token.

## Testing a new adapter

1. Add a **mock** fixture under `context/samples/` labeled `mock: true`.
2. Unit-test mapping from vendor payload → `ContextRecord` (no network).
3. Add a dry-run test that the outbound path raises if `approval` is missing.
4. Only then run one authenticated read in a personal test account.

## What not to do

- Do not embed cookies, `li_at`, or browser automation as an “integration.”
- Do not mark `status: live` because a design doc exists.
- Do not auto-approve writes because a previous post was approved.
- Do not invent engagement metrics to fill empty dashboards.
