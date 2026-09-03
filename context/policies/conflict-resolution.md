# Conflict resolution

A **conflict** is two records that cannot both be true for the same subject and time window (example: two current employers with exclusive “full-time” claims and overlapping dates).

## Detect

Compare `kind` + `subject` + normalized predicate (employer, title, metric name). If values differ and intervals overlap, mark both `disputed` and create a derived conflict record listing `related_ids`.

## Resolve (in order)

1. **Operator decision** — recorded as `operator_asserted` with rationale. Wins for *their* profile.
2. **Primary source over secondary** — an official export or commit beats a directory blog.
3. **Fresher `observed_at`** — only if the sources are the same class and neither is inferred.
4. **Narrow the time window** — both can be true sequentially (“employed at A until 2024-03”).
5. **Withhold** — if still unresolved, public copy must not pick a side.

Never resolve by choosing the value that makes a better LinkedIn hook.

## Downstream

Skills and workflows must treat `disputed` as **do not print**. The profile-validation workflow surfaces the pair to the operator.
