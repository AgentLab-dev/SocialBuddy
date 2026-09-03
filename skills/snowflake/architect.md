---
id: snowflake-architect
title: Snowflake Architect
version: 0.1.0
status: draft
category: snowflake
composable_with:
  - dbt-professional
  - dbt-solution-architect
  - ai-architect
  - phd-writing
activation_keywords:
  - Snowflake
  - warehouse
  - RBAC
  - data sharing
  - dynamic tables
  - streams
  - tasks
  - governance
  - disaster recovery
---

# Snowflake Architect

## Purpose

Design Snowflake **accounts, databases, schemas, compute, access, sharing, pipelines, performance, cost, governance, and recovery** so that dbt and BI sit on a boring, auditable platform.

Features and edition names change. Prefer control objectives (least privilege, blast-radius isolation, measurable spend, recoverable region failure) and verify the current object types in official docs before implementation.

## Activation / Use Cases

- Account and environment layout (prod/non-prod, regions, organizations).
- Database/schema product surfaces vs raw landing.
- Warehouse sizing, isolation, and auto-suspend policy.
- RBAC: functional roles vs access roles.
- Secure data sharing / Marketplace / listings (conceptual).
- Streams, tasks, dynamic tables vs external orchestrators.
- Performance (pruning, clustering, search optimization, spill).
- Cost (compute, storage, cloud services, idle).
- Governance (tags, masking, row access, classification).
- Disaster recovery (replication, failover groups — verify current product).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `edition_and_region` | Preferred | Affects features and DR. |
| `tenancy` | Yes | Internal enterprise, ISV multi-tenant, agency. |
| `data_classes` | Yes | Public, internal, confidential, restricted/PII. |
| `workload_mix` | Yes | ELT, BI, data science, apps, sharing. |
| `rpo_rto` | Preferred | If missing, do not claim DR. |
| `identity_provider` | Preferred | SCIM/SSO assumed where possible. |

## Procedure

### 1. Account / org layout

- Separate **prod** from **non-prod** at the account or database boundary with no routine write role crossing.
- Prefer reader accounts or shares for consumers who should not see raw.
- Record organization-level defaults (parameters, network policies, session policies) as code.

### 2. Database and schema design

| Database | Typical contents |
| --- | --- |
| `RAW` | Ingest landing; limited transform; retain per legal hold |
| `PREP` | dbt staging/intermediate (or equivalent) |
| `PROD` | Published marts + semantic exports |
| `SHARE` | Outbound shareable objects only |
| `SANDBOX` | Time-boxed, quota-capped clones |

Schemas as **products** (`FINANCE`, `PRODUCT_USAGE`), not as team nicknames that outlive the team. Time-travel and fail-safe are not a data model.

### 3. Warehouses

- Isolate **loading**, **transform**, **BI**, and **ad-hoc** so a dashboard cannot starve ELT (and vice versa).
- Auto-suspend in tens of seconds for bursty BI unless a measured cold-start SLA forbids it.
- Scale **up** for single-query CPU/memory; scale **out** (multi-cluster) for concurrency. Do not do both by habit.
- Statement timeouts and resource monitors with hard stops on sandbox and ad-hoc.
- Name warehouses by workload, not by person.

### 4. RBAC

Use a two-layer model:

1. **Access roles** own privileges on objects (`R_PROD_FINANCE_READ`).
2. **Functional roles** (job functions) inherit access roles (`ANALYST_FINANCE`).
3. Users receive functional roles only; never direct object grants to users.
4. Service principals for dbt/orchestrators: least privilege, no UI, key rotation.

Future grants on `PROD` schemas so new tables inherit. Periodic access review from `ACCOUNT_USAGE` / `ORGANIZATION_USAGE` (verify view names for your version).

### 5. Secure data sharing

Sharing is a **product**: contracted schema, no PII unless the listing says so, versioned, revoke-tested. Prefer shares over copying extracts. Reader accounts are for consumers without their own account — still apply network and masking policy. Do not share `RAW`.

### 6. Streams, tasks, dynamic tables

Decision framework (confirm current semantics in docs):

| Tool | Use when | Avoid when |
| --- | --- | --- |
| Stream + task | Procedural, merge-style CDC you must control | You want declarative lag only |
| Dynamic tables | Declarative DAG with lag targets on well-grained SQL | Opaque UDFs, poorly keyed joins, uncontrolled cost |
| External orchestrator (Airflow, etc.) | Cross-system dependencies, human gates | You only needed a cron on one table |

Always define: scheduling identity, failure alerting, idempotency, and how dbt-managed tables interact (do not double-write the same object).

### 7. Performance

Order of investigation:

1. **Result cache / warehouse cache** — do not “tune” a query that never ran cold.
2. **Pruning** — selective predicates on clustered or natural time partitions; avoid `SELECT *` in ETL of wide variants.
3. **Join explosion** — grain errors show up as bytes scanned and as wrong answers.
4. **Spillage** — size up or rewrite; do not hide with a bigger credit budget forever.
5. **Clustering / search optimization / materialized constructs** — add only with a measured query set and an owner who will drop them when unused.

Explain plans are evidence; anecdotes are not.

### 8. Cost

Attribute spend to **workload + owner**. Controls:

- Resource monitors (notify then abort).
- Separate warehouses so idle BI does not look like “ELT is expensive.”
- Storage: time-travel retention by data class; drop transient leftovers.
- Cloud services: chatty metadata patterns, extremely frequent tiny tasks.
- Clones are cheap until someone scans the whole clone in a sandbox warehouse.

Quarterly: top queries by cost, unused tables, warehouses with low active time but high size.

### 9. Governance

- Object **tags** for data class, owner, retention.
- Dynamic masking and row-access policies on restricted columns/rows; test with a denied role.
- Classification jobs as input to tags, not as a substitute for policy.
- `ACCOUNT_USAGE` dashboards for grants, logins, and policy changes.
- Network policy / private connectivity for prod.

dbt `meta` tags should **match** warehouse tags for the same column.

### 10. Disaster recovery

Without `rpo_rto`, write “DR not specified” and stop. If specified:

1. What must fail over (account, databases, shares, users, integrations).
2. Replication / failover group design (verify current objects).
3. How identities and secrets work in the secondary region.
4. Game-day: failover, read test, failback, clock skew, sequence objects.
5. dbt and orchestrators must have a documented target account.

Time-travel is an operational undo, not a regional outage plan.

## Quality Rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Isolation | Shared write-all | Partial | Prod/non-prod + workload WH |
| RBAC | User grants | Roles but messy | Access + functional + reviews |
| Sharing | Uncontracted copy | Ad-hoc share | Productized + revoke test |
| Pipelines | Hidden tasks | Mixed | Chosen tool + identity + alert |
| Performance | Guessing | One knob | Measured plan + owner |
| Cost | Credit surprise | Monitor only | Attribution + hard stops |
| Governance | Hope | Masking only | Tags + policies + tests |
| DR | “It’s the cloud” | Time-travel | Stated RPO/RTO + game day |

## Failure Modes

- One XL warehouse for everything.
- `ACCOUNTADMIN` as a daily role.
- Dynamic tables on an unbounded self-join “to be modern.”
- Sharing `RAW` because a partner asked for speed.
- Clustering every table.
- Claiming multi-region DR because failover was clicked once in a demo.

## Safety Notes

- Never put account locators, private URLs, or customer share names in public posts.
- Do not paste `ACCOUNT_USAGE` rows that contain user emails into Slack/LinkedIn.
- Credit figures in examples are fictional unless a context record says otherwise.
- Confirm edition features before promising them to a client.

## Example Outputs

> **Example** — illustration only; not a real account design.

**Warehouse policy snippet:**

```
WH_ELT_PROD     : M, auto-suspend 60s, monitor abort at 80% daily credits (example)
WH_BI_PROD      : S multi-cluster 1–3, auto-suspend 60s
WH_ADHOC_SANDBOX: XS, abort monitor, 15 min statement timeout
```

**Public-safe sentence (example):** “We isolate ELT and BI warehouses so a dashboard spike cannot starve the load window.”

**Do-not-say (example):** “Auto-suspend 60s always saves 40%.”

## Verified vs Assumed

| Statement | Status |
| --- | --- |
| Separate warehouses by workload is standard Snowflake well-architected advice | Verified as common practice |
| Access-role vs functional-role pattern | Widely taught pattern; assumption it fits most enterprises |
| Exact DR object names (failover groups, etc.) | Must be verified against current docs |
| Auto-suspend 60s in the example | Example only |
| Time-travel ≠ regional DR | Verified control-objective distinction |
