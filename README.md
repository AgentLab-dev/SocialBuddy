# SocialBuddy

A **skills-first foundation** for a LinkedIn manager: expert writing and reading procedures, professional capabilities for dbt / Snowflake / AI, a provider-agnostic context layer, and LinkedIn workflows that **never post or outreach without explicit approval**.

This repository is usable today as a library of procedures, schemas, and validation. It is **not** a live LinkedIn, GitHub, CRM, or email integration. No credentials are included. Adapter documents describe interfaces; samples are labeled mock data.

## Scope

| In scope (this revision) | Out of scope |
| --- | --- |
| Expert skill modules with a fixed contract | Live OAuth, webhooks, or scrapers |
| Canonical context schema + ingestion policies | A production database or vector store |
| Provider-agnostic adapter *interfaces* | Claiming a working vendor connector |
| LinkedIn workflow specifications + approval gate | Automated posting, InMail, or invites |
| Stdlib validation and unit tests | A web UI or hosted agent |

Intended use: an operator (or a future agent) loads skills, grounds them in context records, drafts LinkedIn work, and stops at a human approval gate.

## Principles

1. **Evidence over persona.** Public copy may only state profile facts that are verified or explicitly owned by the operator.
2. **Skills are procedures, not vibes.** Each skill has purpose, activation, inputs, steps, a rubric, failure modes, and safety notes.
3. **Facts, inferences, and recommendations are labeled.** Examples are labeled as examples.
4. **Adapters ingest; they do not send.** Outbound social/CRM actions require `ApprovalDecision`.
5. **Provider-agnostic context.** LinkedIn, GitHub, web, documents, CRM, email, and calendar are *source classes*. Vendor SDKs are later, optional implementations.
6. **Minimal dependencies.** Validation runs on Python 3.11+ with the standard library.

See [docs/assumptions.md](docs/assumptions.md) for decisions made so this repo could ship without blocking questions.

## Repository map

```
skills/                     Expert modules (Markdown + catalog)
context/                    Schema, policies, adapter interfaces, mock samples
workflows/linkedin/         Profile, content, audience, network, sourcing, approval
src/socialbuddy/            Loaders, context types, adapter protocol, approval gate
scripts/validate.py         Skill + catalog + sample checks
tests/                      Unittest suite (stdlib)
docs/                       Architecture, safety, integration path
```

## Skills library

| ID | Module | What it is for |
| --- | --- | --- |
| `phd-writing` | [skills/writing/phd-writing.md](skills/writing/phd-writing.md) | Argument, synthesis, technical prose, editing, citation, audience, LinkedIn-native writing |
| `phd-reading` | [skills/reading/phd-reading.md](skills/reading/phd-reading.md) | Close reading, evidence extraction, critique, synthesis, contradiction, exec summaries |
| `dbt-professional` | [skills/dbt/professional.md](skills/dbt/professional.md) | Project structure, models, tests, docs, macros, incrementals, snapshots, exposures, CI/CD, observability, governance |
| `dbt-solution-architect` | [skills/dbt/solution-architect.md](skills/dbt/solution-architect.md) | Semantic layer, DAG/contracts, environments, deployment, lineage, cost/reliability, operating model |
| `snowflake-architect` | [skills/snowflake/architect.md](skills/snowflake/architect.md) | Account/DB/schema, warehouses, RBAC, sharing, streams/tasks/dynamic tables, performance, cost, governance, DR |
| `ai-enablement` | [skills/ai/enablement.md](skills/ai/enablement.md) | Use-case discovery, adoption, evals, prompt/context engineering, RAG basics, responsible AI, measurement |
| `ai-architect` | [skills/ai/architect.md](skills/ai/architect.md) | Reference architectures, agents/tools, models, retrieval, memory, orchestration, security, reliability, evals, FinOps |

Compose skills rather than merging them. A typical LinkedIn article on incremental models uses `phd-writing` + `dbt-professional` + `workflows/linkedin/content-planning.md`, grounded in context records.

## Context generation

Context is how SocialBuddy avoids inventing a career or a customer story.

- Canonical record: [context/schema/context-record.schema.json](context/schema/context-record.schema.json)
- Policies: provenance, freshness, confidence, chunking/synthesis, redaction/PII, conflict resolution under [context/policies/](context/policies/)
- Adapters (interfaces only): LinkedIn, GitHub, web pages, documents, CRM, email, calendar — [context/adapters/](context/adapters/)
- Mock bundle (synthetic): [context/samples/](context/samples/) — **not real people or companies**

## LinkedIn workflows

Specifications live in [workflows/linkedin/](workflows/linkedin/). Every outbound path ends at [approval-gate.md](workflows/linkedin/approval-gate.md). The executable check is `socialbuddy.approval.require_approval`.

How to add a real LinkedIn API later: [docs/adding-linkedin-integrations.md](docs/adding-linkedin-integrations.md).

## Safety boundaries

Read [docs/safety-boundaries.md](docs/safety-boundaries.md). Short version:

- Do not automate posting or outreach without a recorded approval of the **exact** payload.
- Do not fabricate profile facts, citations, or customer names.
- Do not scrape LinkedIn or store secrets in git.
- Do not present mock samples as real data.

## Setup

Requires Python 3.11 or newer. No third-party packages.

```bash
git clone https://github.com/AgentLab-dev/SocialBuddy.git
cd SocialBuddy
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Optional: add `src` to `PYTHONPATH` when importing the package from another tool:

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -c "from socialbuddy import __version__; print(__version__)"
```

## Using skills from an agent or editor

1. Load `skills/catalog.json` to choose modules.
2. Open the matching Markdown and follow **Procedure**.
3. Ground claims in context records (or operator input). If a fact is missing, write `unknown` — do not fill the gap.
4. Score the draft against the skill’s **Quality Rubric**.
5. For anything that would leave the machine (post, comment, invite, InMail), create an approval request and stop.

## Adding future LinkedIn integrations

See [docs/adding-linkedin-integrations.md](docs/adding-linkedin-integrations.md). The supported increment is: operator paste → official read API (if you have access) → drafts → approved writes. Unofficial automation is not an integration path.

## License

MIT. See [LICENSE](LICENSE).
