# Skills library

Each skill is a reusable expert module. Load by `id` from `catalog.json`. Do not invent a skill at runtime when a catalog module already covers the job — compose instead.

## Contract

Every skill Markdown file must:

1. Start with frontmatter: `id`, `title`, `version`, `status`, `category`.
2. Include the H2 sections listed in `catalog.json` → `required_headings`.
3. Label every worked example as an **Example** (illustration only).
4. Split **Verified vs Assumed** so operators can see what is standard practice versus a local default.

Schema for frontmatter: `_schema/skill.schema.json`.

## Composition

Skills are not mutually exclusive. Typical stacks:

| Job | Skills |
| --- | --- |
| LinkedIn article on incremental models | `phd-writing` + `dbt-professional` + content-planning workflow |
| Critique a vendor white paper before posting a take | `phd-reading` + domain skill + writing |
| Platform operating model post | `dbt-solution-architect` + `snowflake-architect` + writing |
| Internal AI rollout memo, then a public lesson | `ai-enablement` + reading + writing |
| Reference architecture thread | `ai-architect` + writing |

When skills conflict (for example, academic citation density vs LinkedIn scanability), the **channel skill or workflow wins on form**; the domain skill wins on technical claims.

## Status

All modules ship as `draft`. Promote to `stable` only after an operator has used the rubric on real work and filed gaps.
