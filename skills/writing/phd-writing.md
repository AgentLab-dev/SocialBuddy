---
id: phd-writing
title: PhD-Level Writing
version: 0.1.0
status: draft
category: writing
composable_with:
  - phd-reading
  - dbt-professional
  - dbt-solution-architect
  - snowflake-architect
  - ai-enablement
  - ai-architect
activation_keywords:
  - argument
  - literature synthesis
  - technical writing
  - editing
  - citation
  - audience
  - LinkedIn post
  - article
---

# PhD-Level Writing

## Purpose

Produce prose that can survive informed challenge: a precise claim, warrants that connect evidence to the claim, visible limits, and a revision path. Adapt the same argument to academic, executive, and LinkedIn-native forms without changing the underlying facts.

“PhD-level” here means **method**, not a credential. Do not imply the operator holds a doctorate unless a verified profile fact says so.

## Activation / Use Cases

Activate when the operator needs any of:

- A **thesis-driven argument** (opinion with burden of proof).
- **Literature or vendor-doc synthesis** (multiple sources → one position).
- **Technical writing** (design notes, runbooks, architecture posts).
- **Editing** of an existing draft against a rubric.
- **Citation discipline** (what must be sourced; how to refuse fake references).
- **Audience adaptation** (peer, hiring manager, executive, practitioner feed).
- **LinkedIn-native writing** (post, carousel outline, article, comment).

Do not activate for factual Q&A that only needs a short accurate answer, or for legal/compliance filings.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `claim` or draft text | Yes | One sentence preferred. If missing, extract then confirm. |
| `audience` | Yes | Role, prior knowledge, what they must *do* after reading. |
| `channel` | Yes | `linkedin-post`, `linkedin-article`, `comment`, `longform`, `internal-memo`. |
| `evidence_pack` | Preferred | Context records, quotes with locators, metrics with provenance. |
| `constraints` | Optional | Length, banned claims, house voice, must-cite list. |
| `counterarguments` | Optional | If absent, generate candidates and mark them as hypothesized. |

Refuse to treat unverified metrics or unnamed “customers” as evidence.

## Procedure

### 1. Lock the claim

Rewrite the claim until a skeptical reader can say what would **disprove** it. Split stacked claims. If the operator wants “thought leadership” without a disprovable claim, stop and ask for a decision, a tradeoff, or a failed experiment.

### 2. Map claim → warrant → evidence

For each sub-claim:

1. State the warrant (why this evidence matters).
2. Attach the strongest source from the evidence pack.
3. Mark status: `verified`, `operator-asserted`, `inferred`, `unknown`.

Drop or hedge anything `unknown`.

### 3. Literature / source synthesis (when multiple sources)

Build a synthesis matrix (source × claim × method × limit). Prefer **disagreement** as the interesting result. Do not average incompatible methods into a false consensus. Attribute methods, not just conclusions.

### 4. Technical writing pass

- Define terms once; reuse them.
- Prefer interfaces, invariants, and failure modes over product adjectives.
- Put the decision and the rejected alternatives near the top (BLUF for execs; delayed reveal is allowed on LinkedIn only if the claim still appears in the first screen).

### 5. Citation discipline

- Every non-obvious empirical claim needs a locator (URL, doc section, commit, date).
- Secondary summaries are not substitutes for the primary method section when the method is the point.
- If you cannot retrieve a source, write “source not available” — never invent a DOI, paper title, or quote.
- Public LinkedIn copy: prefer 1–3 high-signal citations over a bibliography dump.

### 6. Audience adaptation

| Audience | Default moves |
| --- | --- |
| Peers | Method, limits, what you would replicate. |
| Hiring / talent | Scope you owned, constraints, outcome with provenance. |
| Executives | Decision, risk, cost, what you need from them. |
| Feed (LinkedIn) | One claim, one concrete scene or number, one limit, one question. |

Change **emphasis and order**, not the facts.

### 7. LinkedIn-native form

- First 140–200 characters must stand alone (mobile truncation).
- One idea per post. Articles may carry a short argument chain.
- Line breaks for scanability; no fake “carousel page 1” padding.
- Comments: add evidence or a precise disagreement; do not drop a link-only reply.
- Hashtags: 0–3, specific. Emojis: optional, never a substitute for structure.
- CTA: invite a *falsifiable* reply (“What incremental strategy did you reject and why?”), not “Agree?”.

### 8. Editing passes (in order)

1. **Truth:** any fabricated or unsourced fact?
2. **Logic:** does each paragraph earn the next?
3. **Load:** cut throat-clearing and doubled hedges.
4. **Voice:** consistent person and tense; no unearned “we.”
5. **Channel:** length and first-line test.

### 9. Stop conditions

Hand back the draft plus a rubric score. If the channel is outbound social, attach an approval request (see workflows). Do not post.

## Quality Rubric

Score 0–2 each. Ship only if no dimension is 0 and **Truth** is 2.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Truth | Invented fact or citation | Hedged but still misleading | All public facts sourced or marked unknown |
| Claim precision | Slogan / stacked claims | One claim, fuzzy scope | Disprovable claim, scoped |
| Warrant | Evidence dumped | Implied link | Explicit why-this-counts |
| Counterargument | Ignored | Straw man | Strongest objection addressed |
| Synthesis | Single-source recap | List of takes | Tension resolved or left explicit |
| Audience fit | Wrong altitude | Mixed | Decision-relevant for named audience |
| Channel craft | Wall of text / clickbait | Readable | First line + structure match channel |
| Citation discipline | Fake or missing required cites | Inconsistent | Honest locators; no theater |

## Failure Modes

- **Citation theater:** namedropping papers the writer did not read.
- **Overclaiming causality** from a single deployment story.
- **Jargon as status:** terms that do not change the decision.
- **Engagement bait:** manufactured outrage, fake urgency, “comment ‘YES’.”
- **Voice theft:** imitating a specific person’s cadence as if it were the operator.
- **Scope creep:** turning a post into a textbook.
- **Hedging collapse:** “might possibly” used to smuggle an unsourced metric.

## Safety Notes

- Do not invent employers, titles, dates, customer names, or performance numbers.
- Do not paste private context (pipeline, unpublished revenue, unreleased security issues) into public copy.
- Do not present AI-generated citations as real. Verify or omit.
- Do not claim “research shows” without a retrievable source.
- Copyright: paraphrase and cite; do not reproduce substantial copyrighted text.
- LinkedIn: this skill drafts only. Posting requires the approval gate.

## Example Outputs

> **Example** — illustration only; not a verified fact about a real person, company, or dataset.

**Claim (locked):** “For append-only click events, incremental `merge` with a unique event id is easier to operate than a nightly full refresh, at the cost of stricter uniqueness tests.”

**LinkedIn post draft:**

```
Most “incremental vs full refresh” arguments skip the failure mode.

If your clicks are append-only and you can enforce a unique event_id,
merge incrementals usually win on warehouse time. The bill you pay is
operational: late-arriving keys and a uniqueness test that must page you.

We still full-refresh a 40M-row dim nightly because the business key is
messy. That is a data-quality choice, not a badge.

What uniqueness test actually pages you on-call?

(Example only. The 40M-row figure is invented for the illustration.)
```

**Editing note (example):** First line states the neglected object (“failure mode”). The number is labeled invented so it cannot leak into a real profile as a metric.

## Verified vs Assumed

| Statement | Status |
| --- | --- |
| Scholarly argument typically needs claim, warrant, evidence, and limits | Verified practice (standard argumentation pedagogy) |
| LinkedIn mobile truncation makes the first ~140–200 characters critical | Assumed range; UI changes — verify against current composer |
| Three hashtags is a reasonable default | Assumption (A-004 / channel convention), not a platform rule |
| “PhD-level” must not imply a credential | Product rule (A-005) |
| All numeric examples in this file are fictional | Verified (authoring rule for this module) |
