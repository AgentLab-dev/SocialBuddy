# Assumptions

This document records decisions made so the repository can ship without blocking on unanswered questions. Treat every item as an **assumption** until a maintainer promotes it to a verified product decision.

| ID | Assumption | Why it was made | How to overturn |
| --- | --- | --- | --- |
| A-001 | SocialBuddy is a **skills, context, and workflow foundation**, not a live LinkedIn client in this revision. | The GitHub repository was empty; no API credentials, app review status, or partner agreements exist in-repo. | Add a real adapter implementation plus a documented auth path. |
| A-002 | No live integrations or credentials are available. Adapter modules are **interfaces + mock samples**. | Prevents accidental claims of working OAuth, scraping, or CRM sync. | Implement an adapter and mark its status `live` only after a successful authenticated dry-run. |
| A-003 | Target operator is a **practitioner** (data/AI professional or their assistant) who wants expert writing, reading, and positioning on LinkedIn. | Matches the requested skill mix (PhD writing/reading, dbt, Snowflake, AI). | Add a persona file and retarget skill activation. |
| A-004 | Primary language is **English**. Locale and market variants come later. | Keeps the first skill library coherent. | Add `locale` to skill frontmatter and context records. |
| A-005 | “PhD-level” means **methodological rigor** (argument, evidence, critique), not that the user holds a doctorate. | Avoids credential inflation in generated copy. | If a user supplies a verified credential, cite it as a profile fact. |
| A-006 | License is **MIT**. | Common default for an empty public foundation repo. | Change `LICENSE` and this row. |
| A-007 | Runtime is **Python 3.11+**, standard library only. | Validation and schemas should run anywhere without a lockfile. | Add a dependency only when an adapter truly needs it. |
| A-008 | LinkedIn posting, InMail, connection requests, and other outreach are **write actions** and require explicit human approval per item. | Platform ToS, spam risk, and reputation risk. | Do not overturn; only refine the approval artifact. |
| A-009 | Profile facts (titles, employers, dates, metrics, credentials) must come from **verified context** or the operator. Fabrication is a defect. | Trust and professional harm. | Do not overturn. |
| A-010 | Context from GitHub, web, documents, CRM, email, and calendar is **provider-agnostic**. Vendor names in adapter docs are examples of a class, not a committed integration. | User asked for “other apps to generate context.” | Bind a vendor in an adapter’s `provider` field when implementing. |
| A-011 | Sample context under `context/samples/` is **synthetic / mock**. Names, companies, and metrics are invented. | Prevents readers from treating fixtures as real people. | Replace with operator-supplied, redacted exports labeled `source_kind: operator`. |
| A-012 | Skill content encodes **generally accepted practitioner standards** (dbt Labs docs patterns, Snowflake well-architected themes, common eval practice). Version-specific product UI can drift. | Skills must stay usable without pinning every vendor release. | Add a `verified_against` date and pin vendor doc versions when a skill is used in production. |
| A-013 | This repository does not scrape LinkedIn or bypass authentication. Future integrations must use **official APIs / approved partner programs** or operator-pasted exports. | ToS and legal risk. | Do not overturn. |

When you write copy, architecture notes, or tests, label new assumptions with the next `A-0xx` ID and add a row here.
