# Confidence

`confidence.score` is in `[0, 1]`. It is **not** a probability you can multiply across a career. It is a routing signal:

| Score | Typical `method` | May appear in public copy? |
| --- | --- | --- |
| 0.9–1.0 | `direct_export` or `operator_entry` with `verified` | Yes, if sensitivity is `public` and not stale |
| 0.7–0.89 | `corroborated` (two independent sources) | Yes, with optional “according to A and B” |
| 0.4–0.69 | `single_secondary` | No — internal drafts only unless operator upgrades |
| 0.1–0.39 | `model_inferred` | No. May seed a *question* to the operator |
| 0 | `unknown` | No |

Rules:

- Inference cannot raise `epistemic_status` to `verified`.
- A second copy of the same blog post is not corroboration.
- GitHub + LinkedIn agreeing on an employer is corroboration if dates are compatible.
- Operators may set `operator_asserted` + high confidence; that is their reputation, still not “verified” until an independent source exists.

Always fill `rationale` when score ≥ 0.7 or status is `inferred`.
