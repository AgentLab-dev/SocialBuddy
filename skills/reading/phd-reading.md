---
id: phd-reading
title: PhD-Level Reading
version: 0.1.0
status: draft
category: reading
composable_with:
  - phd-writing
  - dbt-professional
  - dbt-solution-architect
  - snowflake-architect
  - ai-enablement
  - ai-architect
activation_keywords:
  - close reading
  - evidence extraction
  - source critique
  - synthesis
  - contradiction
  - executive summary
  - white paper
---

# PhD-Level Reading

## Purpose

Turn a text (paper, vendor doc, blog, transcript, thread) into **usable structure**: what is claimed, what is shown, what is assumed, what contradicts other sources, and what an operator can safely say in public.

The output is an evidence pack and a critique, not a vibe summary.

## Activation / Use Cases

- **Close reading** of a method, contract, or architecture note before you endorse it.
- **Evidence extraction** into a table that downstream writing can cite.
- **Source critique** (authority, method, incentives, recency, scope).
- **Multi-source synthesis** before a post or design review.
- **Contradiction detection** across docs, code, and marketing.
- **Executive summaries** with BLUF and explicit unknowns.

Activate before `phd-writing` when the operator is reacting to someone else’s work.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `source` | Yes | URL, file, or pasted text plus locator. |
| `source_metadata` | Preferred | Author, date, version, venue, incentive (vendor, academic, operator). |
| `question` | Preferred | What decision this reading must inform. |
| `prior_context` | Optional | Existing context records to test against. |
| `public_safe` | Yes | Whether excerpts may enter LinkedIn drafts. |

If the source cannot be retrieved, stop. Do not hallucinate the contents.

## Procedure

### 1. Bibliographic frame

Record: title, authors/org, date, version, URL, access date, genre (peer-reviewed, vendor, blog, transcript). If date or version is missing, mark `unknown` — do not invent.

### 2. Close reading (one pass, slow)

- Highlight **definitions** and whether they stay stable.
- Mark **normative** sentences (“should,” “best”) vs **empirical** ones.
- Note scope limits, sample, time window, and what was *not* measured.
- Quote sparingly; prefer paraphrase + locator (section, page, heading).

### 3. Evidence extraction

Emit rows, not paragraphs:

| claim_id | quote_or_paraphrase | locator | claim_type | strength | notes |
| --- | --- | --- | --- | --- | --- |

`claim_type`: `empirical`, `method`, `definition`, `normative`, `anecdote`.  
`strength`: `direct-measure`, `indirect`, `assertion`, `marketing`.

Each row can become a context record (`claim` or `excerpt`).

### 4. Source critique (score 0–2)

| Lens | Ask |
| --- | --- |
| Authority | Did the authors do the work, or summarize others? |
| Method | Can a peer replicate the setup from the text? |
| Incentive | What does the publisher sell if you agree? |
| Recency | Is the version current for the product you run? |
| Scope | Who is excluded from the sample or architecture? |
| Internal consistency | Do figures, appendices, and prose agree? |

A vendor architecture guide can still be useful; it cannot be treated as an independent eval.

### 5. Synthesis

When n>1 sources: build source × claim matrix. Outcomes:

- **Agree** (same operational meaning, not just same slogan).
- **Complement** (different scope).
- **Contradict** (cannot both be true in the same conditions).
- **Incommensurable** (different definitions).

Do not “average” contradictions. State the condition under which each is true.

### 6. Contradiction detection

Compare new claims to:

- Other sources in the pack.
- Context records (profile, repo, warehouse standards).
- The operator’s intended public sentence.

On contradiction: record both locators, propose a resolving question, and **block** any public sentence that picks a side without disclosure.

### 7. Executive summary

Fixed shape:

1. **BLUF** (one paragraph: decision + confidence).
2. **What is shown** (method-quality evidence only).
3. **What is asserted**.
4. **Contradictions / unknowns**.
5. **Safe public sentence** (or “none yet”).
6. **Do not say** (list).

Length: 150–400 words unless the operator asked for a longer brief.

## Quality Rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Fidelity | Misstates the source | Omits a limit | Claim and locator match |
| Separation | Mixes fact and spin | Partial | Types labeled |
| Critique | Ad hominem or fan | One lens | Incentive + method + scope |
| Synthesis | Concatenation | Thematic list | Tensions explicit |
| Contradiction | Ignored | Noted vaguely | Dual locators + blocker |
| Exec usability | Recap dump | Long brief | BLUF + do-not-say |
| Public safety | Leaks private or overclaims | Hedged leak | Safe sentence or refusal |

## Failure Modes

- **Abstract-only reading** of a paper.
- **Vendor-voice absorption** (repeating “seamless,” “unified,” “AI-powered”).
- **False balance** (treating a measured result and a slogan as equal).
- **Quote mining** to fit a pre-decided LinkedIn take.
- **Stale version** treated as current product behavior.
- **Hallucinated pages** when the PDF was not available.

## Safety Notes

- Do not reconstruct paywalled or private text as if quoted from memory.
- Do not publish excerpts that violate copyright or NDA. Summarize at a high level or refuse.
- Do not attribute a claim to a person who was only quoted second-hand without saying so.
- PII in transcripts: redact before the evidence pack is reusable.
- Reading a competitor’s post does not grant the right to scrape their network.

## Example Outputs

> **Example** — illustration only; not a real paper, vendor, or excerpt.

**Bibliographic frame:** “Acme Cloud, *Dynamic Tables Primer*, doc version 2024-11, vendor guide, accessed 2026-04-01 (example URL omitted).”

**Extracted row:**

| claim_id | paraphrase | locator | type | strength |
| --- | --- | --- | --- | --- |
| DT-01 | Dynamic tables refresh on a lag target, not a fixed cron, when upstream changes | §“Refresh” (example) | method | assertion (vendor doc) |

**BLUF (example):** “The primer is a product description, not an eval. Safe public sentence: ‘Vendor docs describe lag-targeted refresh; we have not measured cost vs tasks in our account.’ Do not say: ‘Dynamic tables cut cost 40%.’”

## Verified vs Assumed

| Statement | Status |
| --- | --- |
| Close reading should separate empirical claims from normative ones | Verified practice |
| Evidence tables beat unstructured highlights for downstream writing | Assumption (this repo’s working method) |
| BLUF-first exec summaries improve decision quality | Generally accepted comms practice; not a law |
| Vendor docs are assertions until independently measured | Verified methodological stance |
| Example rows in this file are fictional | Verified (authoring rule) |
