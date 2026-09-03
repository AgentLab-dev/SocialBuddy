# Workflow: profile validation

## Purpose

Decide which profile statements are **safe to use** in public copy and which must be fixed, withheld, or marked disputed.

## Inputs

- Context bundle (operator paste and/or future official read).
- Target audience (hiring, buyers, peers).
- Optional: GitHub / web corroboration records.

## Procedure

1. **Inventory** every `profile_fact` (headline, about, each experience, education, cert, metric).
2. **Status gate:**
   - `verified` or `operator_asserted` + not stale + `sensitivity: public` → eligible.
   - `inferred` → convert to a question, not a headline.
   - `disputed` → show both records; block public use.
   - `unknown` dates → do not print “present” or exact years.
3. **Contradiction pass** (conflict-resolution policy): overlapping exclusive jobs, impossible dates, metric vs narrative.
4. **Inflation check:** “led,” “owned,” “increased X%” require a metric or operator assertion with a window. Otherwise rewrite to scope-only language.
5. **About section:** one claim the evidence pack can support; no novel employers.
6. **Output:** table of fields → `keep` / `edit` / `withhold` / `ask_operator`, plus suggested edits that do not add facts.

## Stop

Do not apply edits to LinkedIn. Hand the table to the operator. Publishing is a later, approved write.

## Failure modes

- Treating mock bundle as the operator.
- Filling gaps with “typical” titles for the industry.
- Using GitHub org membership as employer.
