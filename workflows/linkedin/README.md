# LinkedIn workflow layer

Specifications for operator jobs. Nothing here posts to LinkedIn.

## Jobs

| Job | Spec | Skills typically composed |
| --- | --- | --- |
| Profile validation | [profile-validation.md](profile-validation.md) | `phd-reading` |
| Content planning | [content-planning.md](content-planning.md) | `phd-writing` + domain skills |
| Audience / persona | [audience-persona.md](audience-persona.md) | `phd-reading` |
| Networking | [networking.md](networking.md) | writing (comments), reading |
| Lead / candidate sourcing | [lead-candidate-sourcing.md](lead-candidate-sourcing.md) | reading + domain |
| Approval before posting | [approval-gate.md](approval-gate.md) | all outbound |

## Invariants

1. Fabricated profile facts are defects, not style issues.
2. Every outbound action (post, comment, react if treated as outreach, invite, InMail) needs a fresh `ApprovalDecision` on the **payload hash**.
3. Mock context cannot be used as if it were the operator’s biography.
4. No live LinkedIn client is assumed.

Executable check: `socialbuddy.approval.require_approval`.
