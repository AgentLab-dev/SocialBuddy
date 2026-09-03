---
id: dbt-professional
title: dbt Professional
version: 0.1.0
status: draft
category: dbt
composable_with:
  - phd-writing
  - phd-reading
  - dbt-solution-architect
  - snowflake-architect
activation_keywords:
  - dbt
  - models
  - tests
  - macros
  - incremental
  - snapshots
  - exposures
  - Slim CI
  - governance
---

# dbt Professional

## Purpose

Plan, review, and explain **dbt project work** at practitioner standard: layered models, tests that match grain, docs that a stranger can run, incrementals and snapshots with explicit tradeoffs, CI that does not rebuild the world, and lightweight governance.

This skill is about **project craft**. Platform topology and semantic-layer operating models live in `dbt-solution-architect`.

Product surfaces change (dbt Core vs Cloud vs Fusion, etc.). Prefer invariants (DAG, grain, tests, state) over UI labels. When citing a command or feature, record the version you mean.

## Activation / Use Cases

- Design or review `staging` / `intermediate` / `marts` layout.
- Choose materialization and incremental strategy.
- Specify tests, freshness, and documentation for a model.
- Write or review macros without hiding business logic.
- Introduce snapshots or exposures.
- Set up CI/CD (build-on-PR, Slim CI / state comparison concepts).
- Define ownership, naming, and what “done” means for a model.
- Draft a LinkedIn or internal explanation of a dbt decision (compose with `phd-writing`).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `warehouse` | Preferred | Snowflake, BigQuery, Databricks, Redshift, etc. Affects incremental SQL. |
| `dbt_version_family` | Preferred | Core/Cloud and major version if known. |
| `grain` | Yes for model work | Business keys + time. |
| `sources` | Yes for model work | Freshness expectations, late-arriving behavior. |
| `sla` | Optional | Query latency, freshness, rebuild budget. |
| `repo_conventions` | Optional | Existing `dbt_project.yml`, style guide. |

If grain is unknown, stop at a grain workshop — do not pick incremental merge “because scale.”

## Procedure

### 1. Project structure

Default layers (override only with a recorded reason):

| Layer | Holds | May be referenced by |
| --- | --- | --- |
| `sources` | Raw landing, freshness | staging only |
| `staging` | 1:1 with source, renamed, typed, light filters | intermediate, marts |
| `intermediate` | Conformed joins, fan-out/fan-in | marts |
| `marts` | Business entities and facts | BI, reverse ETL, exposures |
| `metrics` / semantic | Measures defined once | downstream consumers |

Rules of thumb:

- No “select star from raw” in marts.
- Staging does not join widely; that is intermediate’s job.
- Marts have a documented grain and owner.

### 2. Models

For each model, write a card before SQL:

1. Grain (one sentence).
2. Unique key.
3. Inputs and join intent (lookup vs fan-out).
4. Materialization: view / table / incremental / ephemeral.
5. Public columns vs helper columns.

Refuse models named `final_final_v2` without a retirement plan.

### 3. Tests

Map tests to risk, not to a coverage vanity number.

| Risk | Typical test |
| --- | --- |
| Duplicate grain | `unique` + `not_null` on the key |
| Broken relation | `relationships` |
| Invalid enum | `accepted_values` |
| Business invariant | Singular test (SQL) |
| Recency | source freshness + downstream assertions |

If an incremental model can emit duplicates, uniqueness is **paging-level**, not optional.

### 4. Documentation

Minimum for a public mart: description, grain, owner, and column descriptions for keys and measures. `codegen` is a start, not done. Docs should say **what a row means**, not restate the column name.

### 5. Macros

Use macros for repeated *mechanics* (surrogate keys, incremental predicates, warehouse-specific date truncation). Do not hide pricing logic or grain changes inside a clever macro. Dispatch / adapter macros belong at the adapter boundary.

### 6. Incremental models

Decision sequence:

1. Is the source insert-only, mutating, or late-arriving?
2. Can you name a monotonic cursor **or** a reliable unique key for merge?
3. What is the lookback window for late data?
4. What test fails if the predicate is wrong?

Strategy sketch (warehouse SQL differs; treat as framework):

| Pattern | When | Main failure |
| --- | --- | --- |
| `append` | Immutable events, no updates | Duplicates if rerun without guard |
| `merge` / delete+insert | Mutable facts with a key | Key drift, full-scan merge |
| Full refresh | Small, messy keys, or rebuilding is cheaper | Cost at scale |

Document `--full-refresh` conditions (schema change, poison data).

### 7. Snapshots

Snapshots are for **slowly changing dimensions you must reconstruct**. They are not a backup strategy and not a substitute for a well-grained fact. Record `unique_key`, `strategy` (`timestamp` vs `check`), and what “changed” means. Plan how you will stop snapshotting a retired source.

### 8. Exposures

Declare exposures for dashboards, ML features, and reverse-ETL syncs that executives actually use. An exposure without an owner and a URL is decoration. Use them to prioritize broken upstream tests.

### 9. CI/CD

Minimum pipeline:

1. PR: parse, unit/data tests on **touched** models + downstream (state comparison / Slim CI *concept*).
2. Merge to a staging env: build and test.
3. Prod: build with a recorded manifest; defer to prod for unmodified nodes when using state.
4. On failure: do not “retry until green” without a root-cause note.

Pin adapter and dbt versions. Store artifacts (`manifest.json`, `run_results.json`) for observability.

### 10. Observability

Watch: test fail rate, freshness, run duration, warehouse cost per job, rows produced vs expected. Prefer warehouse query history + dbt artifacts over screenshots. Page on **user-facing** freshness and uniqueness, not on every warning.

### 11. Governance (practitioner scale)

- Model owners in `meta`.
- Naming: `stg_<source>__<entity>`, `int_<entity>_<verb>`, `fct_` / `dim_`.
- PII columns tagged; no PII in public marts without a contract.
- Breaking column changes require a versioned model or a dual-run window.

## Quality Rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Grain | Unstated | Implied | Written + tested |
| Layering | Marts on raw | Partial | Staging/int/marts respected |
| Tests | None / spam | Generic only | Risk-mapped + singular |
| Incremental | Copied recipe | Strategy named | Failure + lookback documented |
| CI | Hope-based | Full rebuild PR | State-aware + artifacts |
| Docs | Empty | Column echo | Row meaning + owner |
| Governance | Hero knowledge | Partial meta | Owner, PII, breaking-change path |

## Failure Modes

- Incremental merge on a non-unique key.
- Snapshotting high-churn facts “for history.”
- Macros that change grain.
- CI that only runs `dbt parse`.
- Tests copied from another project that do not match this grain.
- Exposures that list every Looker tile to look mature.

## Safety Notes

- Do not paste production warehouse results that contain PII into LinkedIn drafts.
- Do not claim “we cut cost X%” without a context record for the measurement window.
- dbt and adapter SQL differ; do not publish dialect-specific code as universal.
- This skill does not grant permission to run `dbt run` against a customer’s prod from an agent.

## Example Outputs

> **Example** — illustration only; not a real project or warehouse.

**Model card:**

```
name: fct_page_views
grain: one row per event_id
unique_key: event_id
materialization: incremental (merge)
lookback: 2 days on event_date
paging tests: unique(event_id), not_null(event_id, occurred_at)
owner: analytics-platform (example)
warehouse: Snowflake (example)
```

**Public-safe sentence (example):** “We only merge incrementals when the unique key is tested; otherwise we full-refresh or fix the grain first.”

## Verified vs Assumed

| Statement | Status |
| --- | --- |
| Layered staging / marts is the dominant dbt Labs–taught shape | Verified as common standard; not the only valid layout |
| Exact Slim CI product behavior depends on dbt Cloud/Core version | Verified (do not hard-code UI steps) |
| Naming `stg_` / `fct_` / `dim_` | Assumption (widely used convention) |
| 2-day lookback in the example | Example only, not a default |
| Uniqueness tests on incremental keys are mandatory in this skill | Local standard (assumption A-012 style) |
