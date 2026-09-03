# Provenance and freshness

## Provenance

A record without provenance is a rumor. Adapters must set:

1. **source_class** — one of the adapter classes, `operator`, or `derived`.
2. **adapter** — module or document name that produced the record.
3. **provider** — optional vendor (e.g. `salesforce`, `hubspot`). Omit rather than guess.
4. **locator** — enough for a human to find the source again.
5. **observed_at** — timestamp *in the source* when possible (commit date, email date, profile “last updated” if the API provides it).
6. **ingested_at** — clock at ingest.
7. **author** — who asserted it in the source (may differ from the subject).

Derived records (`source_class: derived`) must list `related_ids` of parents. Synthesis may lower `epistemic_status` but must not erase parents.

## Freshness

| `as_of` | Meaning |
| --- | --- |
| Same as `observed_at` when known | Prefer |
| `ingested_at` if the source is undated | Allowed; confidence method should not be `direct_export` if the source is undated |

`ttl_hours` is a **policy hint**, not physics:

| Kind | Default TTL hint | `stale_action` |
| --- | --- | --- |
| `profile_fact` (title, employer) | 720 (30d) | `revalidate` |
| `metric` | 168 (7d) unless the window is historical | `withhold` if used in public copy |
| `excerpt` of a versioned doc | until version changes | `revalidate` |
| `event` (meeting) | 0 after end time | `label_stale` |
| `preference` | 2160 (90d) | `revalidate` |

Public LinkedIn copy may only use `verified` or `operator_asserted` facts that are **not** past TTL unless the sentence is explicitly historical (“In 2022…”).

Do not backdate `observed_at` to make a fact look fresh.
