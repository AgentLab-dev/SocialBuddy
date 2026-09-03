# Architecture

SocialBuddy is three layers that compose:

```
┌─────────────────────────────────────────────────────────────┐
│  LinkedIn workflow layer                                    │
│  profile · content · audience · network · sourcing · approve│
└───────────────────────────▲─────────────────────────────────┘
                            │ consumes
┌───────────────────────────┴─────────────────────────────────┐
│  Context layer                                              │
│  schema · provenance · freshness · confidence · redaction   │
│  adapters (interfaces): LinkedIn, GitHub, web, docs, CRM…   │
└───────────────────────────▲─────────────────────────────────┘
                            │ grounds
┌───────────────────────────┴─────────────────────────────────┐
│  Skills library                                             │
│  writing · reading · dbt · Snowflake · AI enablement/arch   │
└─────────────────────────────────────────────────────────────┘
```

## Skills

A **skill** is a reusable expert procedure with a contract: purpose, activation, inputs, procedure, rubric, failure modes, safety, and labeled examples. Skills are Markdown with a small frontmatter block. They are loaded by `socialbuddy.skills` and checked by `scripts/validate.py`.

Skills do not call APIs. They tell an operator or an agent **how to think and what to refuse**.

## Context

A **context record** is the canonical unit of memory. Every record has source provenance, observed-at / ingested-at timestamps, confidence, redaction status, and a claim/evidence split. Adapters implement a single `ContextAdapter` protocol and emit records; they do not write to LinkedIn.

See `context/README.md` and `context/schema/context-record.schema.json`.

## Workflows

A **workflow** sequences skills + context into an operator job (for example: “validate profile, then plan two weeks of posts”). Workflows are specifications first. The only executable policy in this revision is the **approval gate** (`src/socialbuddy/approval.py`).

## Extension points

| Want to add… | Put it here | Contract |
| --- | --- | --- |
| A new expert domain | `skills/<domain>/` | Required sections + catalog entry |
| A new source system | `context/adapters/<name>.md` + a class implementing `ContextAdapter` | Emit `ContextRecord`; no implicit writes |
| A new LinkedIn job | `workflows/linkedin/` | Must call the approval gate for any outbound action |
| A live vendor SDK | New optional extra, never required for validation | Status `live` only after authenticated dry-run |

## What this revision does not include

- OAuth apps, webhooks, or scheduled crawlers
- A production database or vector store
- A web UI
- Guarantees about LinkedIn API product availability (those change; implement against current official docs when you add an adapter)
