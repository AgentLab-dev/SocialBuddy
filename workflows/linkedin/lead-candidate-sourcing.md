# Workflow: lead and candidate sourcing

## Purpose

Help an operator **search and shortlist** using allowed sources, then draft *human* outreach. This is not an automated sequencer and not a scrape.

## Inputs

- Role or ICP definition (must-have skills, location policy, exclusions).
- Allowed sources: operator-supplied lists, official Recruiter/Sales products **if** the operator has them later, CRM read adapter, referrals.
- Domain skills for evaluating public work (GitHub interface, writing samples).

## Procedure

1. **Define the scorecard** before looking at people (skills, evidence types, knock-outs). Reduces motivated browsing.
2. **Ingest** only from allowed adapters. Web adapter is for *public pages the operator provided*, not for crawling LinkedIn SERP HTML.
3. **Evidence:** public repos, talks, posts the operator saved. `skill_signal` at `inferred` cannot be a knock-in.
4. **Shortlist table:** name (if public), evidence locators, gaps, suggested conversation. Sensitivity `internal`.
5. **Outreach drafts** (optional): personalized from evidence; no fake compliments. Each draft → approval-gate. Default channel is whatever official product the operator uses — SocialBuddy does not send.
6. **CRM write-back** (future): still an outbound approval.

## Hard stops

- No scraping LinkedIn search, no buying email dumps, no “email then invite” automation.
- No fabricating a candidate’s current employer.
- No processing of special-category data to filter people.
- Comply with applicable employment and anti-spam law; this spec is not legal advice.

## Example

> **Example** — illustration only.

Scorecard: “Has shipped incremental dbt models with uniqueness tests — evidence = public PR or operator-referred write-up.” A GitHub star count is not evidence.
