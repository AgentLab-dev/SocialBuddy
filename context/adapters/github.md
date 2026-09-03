# GitHub adapter (interface)

**Status:** `interface`. Provider example: GitHub.com or GHES — not implemented.

## Capabilities (read)

| Capability | Records |
| --- | --- |
| `repo_meta` | `skill_signal` (languages, topics) |
| `commit_or_pr` | `event`, `document_chunk` |
| `readme_docs` | `document_chunk` |

## Mapping rules

- Stars and contrib graphs are **weak** skill evidence (`single_secondary` at best). Prefer owned commits and review comments you can locate.
- Do not infer employer from a company GitHub org unless the operator confirms (many people are outside collaborators).
- Private repo content: `sensitivity: confidential` or higher; never public LinkedIn without redaction + operator mark.
- LICENSE and vendored code are not “your stack.”

## Writes

Issues/PRs are out of scope for SocialBuddy’s LinkedIn workflows. If added later, they are still not LinkedIn writes.
