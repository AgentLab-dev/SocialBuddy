---
id: ai-architect
title: AI Architect
version: 0.1.0
status: draft
category: ai
composable_with:
  - ai-enablement
  - snowflake-architect
  - dbt-solution-architect
  - phd-writing
  - phd-reading
activation_keywords:
  - reference architecture
  - agents
  - tools
  - model selection
  - retrieval
  - memory
  - orchestration
  - evals
  - observability
  - FinOps
---

# AI Architect

## Purpose

Specify **systems** that use models: reference architectures, agent/tool boundaries, model choice, retrieval and memory, orchestration, security/privacy, reliability, evaluation hooks, observability, and cost control.

Enablement (adoption, change, program metrics) is `ai-enablement`. This skill owns runtime invariants.

## Activation / Use Cases

- Draw or review a reference architecture for an assistant, batch pipeline, or agent.
- Decide model routing (quality, latency, cost, residency).
- Design tool/function calling and allow-lists.
- Specify retrieval, chunking, and memory tiers.
- Orchestration: sync request, workflow/queue, human-in-the-loop.
- Security, privacy, and tenant isolation.
- Reliability: timeouts, retries, idempotency, fallbacks.
- Online/offline eval insertion points.
- Observability and FinOps for tokens, tools, and retrieval.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `job_to_be_done` | Yes | User-visible SLA (latency, accuracy class). |
| `trust_boundary` | Yes | Who the user is; what tools can do. |
| `data_plane` | Yes | Where corpora and logs live; residency. |
| `write_actions` | Yes | List every side effect. Each needs a gate. |
| `budget` | Preferred | p95 latency and $ / successful task. |

## Procedure

### 1. Reference architecture (default shapes)

Pick the simplest shape that meets the job:

| Shape | When |
| --- | --- |
| A. Single model + schema | Classification, extraction, short rewrite |
| B. RAG + model | Questions over changing corpora |
| C. Tool-using agent | Needs live systems, but **narrow** tools |
| D. Workflow / graph | Known steps, retries, human gates |
| E. Multi-agent | Only when roles have **different** tools or cadences; default no |

Every diagram must show: client, policy/authz, orchestrator, model provider(s), retrieval, tool sandbox, log/eval store, human approval for writes.

### 2. Agent / tool systems

- Tools are **capability + authz + idempotency key + timeout**. Not natural-language wishes.
- Default deny. Allow-list tools per workflow, not a global “browser + shell + email.”
- Agents may **propose** writes; `OutboundChannel` applies only with `ApprovalDecision` (this repo) or an equivalent durable gate.
- Bound loops: max steps, max tokens, max tool errors. On exceed: return partial + reason.
- Do not give an agent raw credentials; use scoped tokens per tool.

### 3. Model selection

Decision table (fill with current vendor options at implementation time):

| Need | Prefer |
| --- | --- |
| Strict JSON / tools | Models with reliable structured output |
| Long context / many docs | Larger context **or** better retrieval — measure both |
| Sensitive data | Provider + region that meet policy; or local/VPC |
| Latency | Small model + cache; speculative routing |
| Cost | Route easy tasks down; cache prompts and retrieval |

Re-evaluate on a schedule; do not bake a brand name into the architecture doc as destiny. Record `verified_against` date.

### 4. Retrieval

- Index per **ACL partition**. Query-time filter is mandatory.
- Hybrid (lexical + dense) when names, IDs, and jargon matter.
- Rerank when k is large or the corpus is noisy.
- Citations required for user-visible factual answers.
- Separate indexes for code, tickets, and HR — different chunkers and retention.

### 5. Memory

| Tier | Contents | TTL | Write policy |
| --- | --- | --- | --- |
| Working | Current thread, tool results | Session | Automatic |
| Episodic | Summaries of past threads | Days–weeks | Summarize + redact |
| Profile | Durable user/org facts | Until revoked | **Verified context records only** |
| None | Secrets, raw PII, one-time codes | — | Never persist |

Memory is a source of false confidence. Profile memory must use the context schema (provenance, confidence). Do not “remember” a job title the user joked about.

### 6. Orchestration

- User-facing chat: sync with streaming; tools async with a visible pending state.
- Long jobs: durable workflow (queue + checkpoint). Exactly-once **effects** via idempotency keys.
- Human gate as a first-class state, not a comment in a prompt.
- Idempotent retries on model 5xx; **do not** retry writes without the key.

### 7. Security and privacy

- Authn/z at the orchestrator; the model is untrusted.
- Prompt injection: treat retrieved text and user files as **data**, not instructions. Wrap and delimit. Strip tool names from untrusted text where possible.
- Egress: tools that fetch URLs need allow-lists (SSRF).
- Logs: redact; retain by policy; encrypt.
- Tenants: no shared vector namespace without hard filters tested by a red-team query.
- Training opt-out / no-retain contracts recorded for each provider.

### 8. Reliability

- Timeouts tighter than the client’s patience.
- Fallback: smaller model, retrieve-only, or “unavailable” — never silently invent.
- Circuit-break a tool that errors N times.
- Load tests include token spikes, not just QPS.

### 9. Evals in the architecture

Hooks:

- Offline: replay traces against gold.
- Shadow: new prompt/model on live traffic, no writes.
- Online: sample for human review; gate promotions on regression slices (safety + capability).

Store traces with prompt version, model id, retrieval ids, tool calls, and redaction flag.

### 10. Observability and FinOps

Minimum telemetry: request id, user/tenant, route, model, tokens in/out, retrieval hit count, tool name/latency/error, $ estimate, outcome class.

FinOps:

- Budget per tenant/workflow; hard stop or degrade.
- Cache identical retrieval + prompt prefixes.
- Kill zombie agent loops.
- Weekly: $ / successful task, not only token volume.

## Quality Rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Shape | Agent-by-default | Reasonable | Simplest that works |
| Tools | Open-ended | Some limits | Allow-list + idempotency |
| Authz | In the prompt | Partial | Enforced outside the model |
| Retrieval/memory | Soup | RAG only | ACL + memory tiers |
| Writes | Auto | Sometimes | Durable human gate |
| Evals | None | Demo set | Hooks + promotion gate |
| Observe/cost | Tokens maybe | Dashboards | Budget + $ / success |
| Injection/SSRF | Ignored | Docs | Tested controls |

## Failure Modes

- “Autonomous agent” with email + browser + prod DB.
- Vector DB as a second, ungoverned copy of the warehouse.
- Memory that promotes rumors to profile facts.
- Observability that cannot reconstruct *why* a tool fired.
- FinOps that optimizes tokens while a tool hammers an API.
- Architecture posts that redraw the same hexagons with a new vendor logo.

## Safety Notes

- The model must not be the enforcement point for privacy or payments.
- Do not log raw prompts that contain secrets.
- Do not claim SOC2/ISO/HIPAA from a diagram.
- Public LinkedIn architectures must be generic or labeled example; strip tenant IDs.
- This skill never authorizes outbound LinkedIn actions without the approval workflow.

## Example Outputs

> **Example** — illustration only; not a real vendor design.

**Shape decision:** “RFP assistant = shape D (workflow): retrieve capability records → draft answers with citations → human approve → optional export. Not shape C (free agent).”

**Tool spec (example):**

```
tool: lookup_capability
authz: se_role
idempotency: n/a (read)
timeout: 3s
returns: {id, text, source_uri, as_of}
```

**Do-not-say (example):** “The agent securely handles all compliance automatically.”

## Verified vs Assumed

| Statement | Status |
| --- | --- |
| Least-privilege tools and externalized authz are required | Verified as standard secure design |
| Multi-agent is a last resort | Assumption / bias of this skill — overturn with evidence |
| Hybrid retrieval often helps identifier-heavy corpora | Common IR result; still measure |
| Durable human gate for writes | Product rule (A-008) |
| Example tools and roles are fictional | Verified (authoring rule) |
