---
id: ai-enablement
title: AI Enablement
version: 0.1.0
status: draft
category: ai
composable_with:
  - ai-architect
  - phd-writing
  - phd-reading
  - dbt-professional
activation_keywords:
  - use case discovery
  - change management
  - evaluation
  - prompt engineering
  - context engineering
  - RAG
  - responsible AI
  - adoption
---

# AI Enablement

## Purpose

Move an organization from **tool curiosity** to **measured, responsible use**: find use cases that change a real workflow, design adoption, evaluate quality, engineer prompts and context, use RAG only when it earns its keep, and report outcomes without theater.

This is the operator/change/measurement skill. System architecture lives in `ai-architect`.

## Activation / Use Cases

- Use-case discovery workshops and kill criteria.
- Adoption and change plans (roles, incentives, shadow workflows).
- Offline/online evaluation design for assistants and automations.
- Prompt and context engineering standards.
- RAG basics: when to retrieve, what to refuse.
- Responsible AI: privacy, human gates, disclosure.
- Measurement: leading/lagging indicators that finance will accept.

Do not activate to pick a foundation-model vendor in isolation — compose with `ai-architect`.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `workflow` | Yes | Who does what today, how often, cost of error. |
| `data_classes` | Yes | What the model would see. |
| `buyer_and_user` | Yes | Often different people. |
| `risk_appetite` | Preferred | Internal draft vs external customer text. |
| `success_metric_draft` | Preferred | If missing, inventing “engagement” is forbidden. |

## Procedure

### 1. Use-case discovery

Score each candidate on four axes (0–2):

| Axis | 2 looks like |
| --- | --- |
| Frequency | Daily or high-volume weekly |
| Structured-ness | Clear inputs/outputs, examples exist |
| Error cost | Reversible or human-gated |
| Data readiness | Allowed, retrievable, not secretly toxic |

Kill if error cost is high **and** there is no human gate. Kill if the only value is “we should use AI.” Prefer **assists** (draft, extract, classify) over **silent writes**.

Write the use case as: *actor + artifact + definition of done + fallback to human*.

### 2. Adoption / change

- Name the **old** habit you are replacing (searching Confluence, writing the first email, tagging tickets).
- Put the assistant **in the path of work** (ticket tool, IDE, CRM), not a novelty tab.
- Train with real failed examples, not a slide of principles.
- Incentives: time saved must not be punished as “lower utilization.”
- Champions per team; office hours; a kill switch if quality regresses.
- Disclosure: when must a human say content was model-assisted (customer-facing, regulated).

### 3. Evaluation

Before prompt tweaking:

1. **Task spec** and 20–50 golden items (more later).
2. Split: capability vs regression vs safety.
3. Graders: exact match where possible; rubric + second human for prose; model-as-judge only with spot checks.
4. Report: pass rate, calibrated error types, **not** a single “quality %” without a definition.
5. Online: thumbs are weak; instrument *downstream* (ticket reopened, edit distance, time-to-merge).

No production write path without an eval slice for the failure that would embarrass you.

### 4. Prompt and context engineering

Order of leverage:

1. **Right context** (tools, retrieved docs, structured state) with provenance.
2. **Task decomposition** and output schema.
3. **Examples** that include hard negatives.
4. Wording polish.

Rules:

- Instructions must state **refuse conditions** (missing source, user asks to invent citations, PII outbound).
- Context windows are a budget: rank, cap, and cite. Do not paste a warehouse.
- Version prompts like code; A/B one change at a time.

### 5. RAG basics

Use RAG when the answer must track **changing private or long** knowledge. Skip RAG for stable public facts the model already knows **if** you can tolerate stale training data — otherwise retrieve.

Minimum RAG checklist:

- Chunk by **semantic unit** (see context policies), not fixed 512 tokens only.
- Attach source IDs; the user-visible answer must cite or refuse.
- Measure retrieval (recall@k on gold) separately from generation.
- Freshness and ACL: do not retrieve docs the user cannot see.
- “Chat with PDF” demos are not a permission model.

### 6. Responsible AI

- Inventory: data in, data out, retention, subprocessors.
- Human approval for external sends (this repo’s LinkedIn gate is a special case).
- Bias/harm: test with cases that would injure a person or a customer relationship.
- Security: no secrets in prompts logged to a shared store; redact.
- Users can appeal an automated classification that affects them.

### 7. Measurement

| Layer | Example indicators (illustrative classes) |
| --- | --- |
| Adoption | Weekly active users in the target workflow, not logins to a toy |
| Quality | Eval pass rate, human edit rate |
| Outcome | Cycle time, deflection, win-rate — only with a baseline |
| Risk | Policy violations, leaked PII incidents, rollback count |
| Cost | $ per successful task, not $ per token in isolation |

Present a baseline and a window. Do not report “10x productivity” without an operational definition.

## Quality Rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Use-case fit | Demo-led | Partial score | Scored + kill criteria |
| Change plan | Email launch | Training only | In-path + incentive + kill switch |
| Evals | Vibes | A few happy prompts | Gold set + error types |
| Context/prompts | Essay prompt | Some structure | Versioned + refuse rules |
| RAG | Default on | Naive chunk | ACL + retrieval metrics |
| Responsibility | Afterthought | Policy PDF | Gates + inventory |
| Measurement | Vanity | Activity | Baseline + outcome + risk |

## Failure Modes

- Copilot bolted onto a process nobody wanted.
- RAG over a junk Confluence with no owners.
- Eval = “the CEO liked the demo.”
- Prompt files growing into undocumented policy.
- Shadow IT models on customer PII.
- LinkedIn posts that generalize one pilot as a transformation.

## Safety Notes

- Do not put real customer tickets, health data, or unpublished financials into a public model or a public post.
- Disclose AI assistance where the operator’s policy or the channel requires it.
- Enablement success is not permission to auto-send outreach.
- Do not claim regulatory compliance (GDPR, HIPAA, SOC2) from a checklist in this skill alone.

## Example Outputs

> **Example** — illustration only; not a real program.

**Use-case card:**

```
Actor: solutions engineer
Artifact: first draft of an RFP technical response
Done: all answers cite an approved capability record or say "unknown"
Fallback: SE edits; cannot send without manager approval
Kill: if citation fabrication > 0 on gold set
```

**Public-safe sentence (example):** “We will not send an AI draft to a customer unless every technical claim maps to an approved capability record.”

## Verified vs Assumed

| Statement | Status |
| --- | --- |
| Evals should precede prompt fiddling | Verified as current engineering consensus |
| 20–50 gold items as a starting set | Assumption (minimum viable, not a law) |
| In-path beats novelty tabs for adoption | Strong practitioner pattern; not a theorem |
| RAG always required | False; this skill treats RAG as conditional |
| Example RFP workflow is fictional | Verified (authoring rule) |
