# Safety boundaries

SocialBuddy is designed to **advise and draft**, not to impersonate, spam, or invent a career.

## Hard rules

1. **No write to LinkedIn (or any social/CRM channel) without an approval artifact.** Drafts may be stored. Sends, posts, comments, reactions that constitute outreach, connection requests, and InMail are blocked until `ApprovalDecision.approved` exists for that exact payload.
2. **Never fabricate profile facts.** Titles, employers, dates, degrees, certifications, headcount, revenue, and performance metrics are either sourced from verified context or marked `unverified` and withheld from public copy.
3. **Never fabricate citations, quotes, or customer names.** If a source is missing, say so.
4. **No scraping, credential stuffing, or unofficial LinkedIn automation.** Future adapters use official APIs, approved partner channels, or operator-supplied exports.
5. **Redact secrets and sensitive PII** before a context record is eligible for generation. See `context/policies/redaction-and-pii.md`.
6. **Do not claim live integrations.** Adapter status is `interface`, `mock`, or (later) `live`. This repo ships only the first two.
7. **Distinguish facts, inferences, and recommendations** in every operator-facing artifact.
8. **No automated mass outreach.** Even with approval, batch sends require a separate campaign approval that lists recipients and copy variants.

## Allowed without extra approval

- Load and validate skills.
- Ingest **operator-pasted** text or files into the context store (still run redaction).
- Produce drafts, critique, plans, and checklists.
- Read mock/sample context labeled as such.
- Run validation scripts and unit tests.

## Disallowed even if the operator asks in-character

- Inventing employment history or “likely” metrics presented as fact.
- Posting, messaging, or connecting as the operator without a recorded approval.
- Using private email/calendar/CRM content in a public post without an explicit “public-safe” classification.
- Impersonating another person.

## Residual risk the operator still owns

- A human can approve a bad post. The approval gate records consent; it does not guarantee quality or legal compliance.
- Vendor documentation (dbt, Snowflake, model providers) changes. Skills can become stale.
- Mock samples can be mistaken for real data if labels are stripped. Do not strip labels.
