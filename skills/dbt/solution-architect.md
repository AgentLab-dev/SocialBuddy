---
id: dbt-solution-architect
title: dbt Solution Architect
version: 0.1.0
status: draft
category: dbt
composable_with:
  - dbt-professional
  - snowflake-architect
  - ai-enablement
  - phd-writing
activation_keywords:
  - semantic layer
  - data contracts
  - DAG
  - environments
  - lineage
  - operating model
  - dbt Mesh
---

# dbt Solution Architect

## Purpose

Design the **system** around dbt: how domains publish contracts, how environments promote code, how a semantic layer becomes the measure authority, how lineage and cost inform operating reviews, and who is allowed to break whom.

Practitioner SQL craft is `dbt-professional`. Warehouse account design is `snowflake-architect`. This skill sits between them.

## Activation / Use Cases

- Choose monolith vs multi-project / domain mesh.
- Specify data contracts and public model surfaces.
- Design env topology (dev, CI, staging, prod) and deferral.
- Introduce or review a semantic layer (metrics, entities, exports).
- Set lineage, incident, and cost-review cadences.
- Define platform vs domain team operating model.
- Advise on reliability vs freshness vs spend tradeoffs.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `org_shape` | Yes | Central platform, federated domains, agency, startup. |
| `consumer_types` | Yes | BI, reverse ETL, ML, embedded analytics, exec metrics. |
| `regulatory` | Preferred | PII, residency, audit needs. |
| `spend_ceiling` | Preferred | Warehouse + seat + failure cost. |
| `current_dag_pain` | Optional | Cross-team blocking, 4-hour runs, metric fights. |

## Procedure

### 1. Frame the job of the platform

Write one sentence: “The platform exists so that **[consumers]** can trust **[measures/entities]** within **[freshness]** at **[cost]**.” If that sentence names a tool instead of a consumer, rewrite it.

### 2. DAG and contract design

- Identify **bounded contexts** (billing, product usage, finance). Shared dimensions (customer, account) are published products, not casual joins.
- Each domain gets a **public** schema/models and a private kitchen. Downstream may depend only on public models that declare a contract (name, grain, columns, tests, version).
- Breaking changes: dual-run or versioned model (`fct_invoices_v2`) plus a sunset date. No silent rename on a public column.
- Cycle detection is not enough: watch **political cycles** (finance waits on sales waits on finance). Resolve with a snapshot of a published dimension at a stated time.

### 3. Semantic layer

Use a semantic layer when the same measure is computed in three BI tools. Do not use it to hide a broken grain.

Checklist:

1. Entities and their primary keys.
2. Measures with `type` (additive, semi-additive, non-additive) and default time spine.
3. Filters that change meaning (e.g. “active customer”) documented as **definitions**, not hidden YAML.
4. Export path to the warehouse or metric API; caching and freshness SLA.
5. Who may add a measure (platform review vs domain self-serve).

If executives still screenshot Excel after launch, the layer is not the system of record yet — do not claim victory on LinkedIn.

### 4. Environments and deployment

| Env | Purpose | Data | Who writes |
| --- | --- | --- | --- |
| Dev | Isolated iteration | Sample / zero-copy clone | Anyone with a branch |
| CI | PR validation | Slim subset / deferred prod | Automation |
| Staging | Business UAT | Scrubbed or sampled prod | Restricted |
| Prod | System of record | Full | Pipeline role only |

Promotion is **commit + green CI + (optional) staging sign-off**, never laptop `dbt run` to prod. Record rollback: previous manifest + `--exclude` or revert commit.

Multi-project: prefer **package or mesh references to contracted models** over copying SQL. Cross-project refs need an owner on both sides.

### 5. Lineage and incidents

- Source of truth for lineage: produced artifacts + warehouse objects, not a slide.
- Severity: user-facing exposure freshness and contract test failure page a human; internal WIP does not.
- Post-incident: which contract failed, which domain owned it, what dual-run would have caught.

### 6. Cost / reliability tradeoffs

Write the triangle explicitly for each domain: **freshness, completeness, spend**.

| Lever | Helps | Hurts if misused |
| --- | --- | --- |
| Incremental + deferral | Spend, PR time | Stale logic if state is wrong |
| Microbatch / frequent runs | Freshness | Cloud services + enqueue chaos |
| Larger warehouse | Runtime | Idle spend |
| Views | Storage | Repeated compute |
| Clone/zero-copy dev | Isolation | Accidental full-scan on large clones |

Pick a default per domain and review quarterly against query history.

### 7. Operating model

| Function | Platform team | Domain team |
| --- | --- | --- |
| Warehouse roles, CI templates, package versions | Owns | Consumes |
| Public contracts, grain | Reviews | Owns |
| Semantic measures used in group OKRs | Co-owns | Proposes |
| Ad-hoc marts | Discourages | Time-boxed |

Cadence: weekly contract-break review; monthly cost + freshness; quarterly “should this still be a separate project?”

Publish a RACI. Heroics are a smell, not a culture.

## Quality Rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Consumer sentence | Tool-centric | Vague user | Named consumer + SLA |
| Contracts | None | Docs only | Enforced + versioned |
| Semantic layer | Metric soup | Partial YAML | Additive types + ownership |
| Envs | Shared prod for dev | Partial | Isolated + rollback |
| Lineage | Tribal | Dashboard | Artifact-backed + paging policy |
| Tradeoffs | “Optimize everything” | One lever | Explicit triangle |
| Operating model | Heroes | Unwritten | RACI + cadences |

## Failure Modes

- Mesh-splitting a 3-person company.
- Semantic layer on top of undocumented grains.
- Contracts that only exist in Confluence.
- Dev pointing at prod with write privileges.
- Cost reviews that look at seat licenses but not warehouse bytes scanned.
- Platform team becoming a ticket sink for every `ref()`.

## Safety Notes

- Multi-tenant or regulated data: residency and row-access belong in warehouse design (`snowflake-architect`); dbt cannot be the only control.
- Do not publish client DAG screenshots with real table names if they reveal product strategy or PII.
- Do not promise “one semantic layer to replace finance” without finance’s definition of cash.
- Architecture diagrams in posts must be labeled example or redacted.

## Example Outputs

> **Example** — illustration only; not a real operating model.

**Platform sentence:** “Domain teams publish contracted marts so Finance and CS can reuse `active_subscription` within 6 hours at a monthly warehouse budget of $X (figure omitted — not a real budget).”

**Contract stub (example YAML shape):**

```yaml
# example only
models:
  - name: dim_account
    access: public
    contract:
      enforced: true
    columns:
      - name: account_id
        data_type: string
        constraints: [{type: not_null}]
```

**Do-not-say (example):** “Our mesh eliminated all metric disagreements.”

## Verified vs Assumed

| Statement | Status |
| --- | --- |
| Public/private model surfaces and contracts are current dbt-direction features; syntax varies by version | Verified as a moving product area — pin version before implementing |
| Four-env topology | Common pattern; assumption that staging exists |
| Platform vs domain RACI | Assumption tailored to mid-size orgs (A-003) |
| Semantic layer as measure authority | Sound when adopted; not automatically true after install |
| Example YAML is illustrative | Verified (authoring rule) |
