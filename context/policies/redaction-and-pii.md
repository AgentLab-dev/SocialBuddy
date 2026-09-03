# Redaction and PII

Nothing enters a bundle used for **generation** until redaction has run.

## Classes to strip or block

| Class | Action | Examples |
| --- | --- | --- |
| Secrets | `blocked` — do not store in statement | API keys, tokens, connection strings, `li_at` |
| Government IDs, health, precise location of a private person | `blocked` or `redacted` | Not for LinkedIn drafts |
| Direct contact | `redacted` unless `sensitivity: public` and operator-owned | Personal email, phone |
| Third-party PII | `redacted` | Candidate home address, a client’s unpublished pipeline |
| Customer confidential | `blocked` for public channels | Deal amounts, unreleased features if marked confidential |

Replacement tokens: `[REDACTED:email]`, `[REDACTED:phone]`, `[REDACTED:secret]`, `[REDACTED:name]`.

## Channel rules

| Channel | Max sensitivity allowed in the artifact |
| --- | --- |
| LinkedIn public post/article | `public` |
| LinkedIn invite / InMail | `internal` at most, and only about the operator or already-public prospect facts |
| Internal memo | `confidential` with need-to-know |
| Model logs | `redacted` always |

If redaction status is `blocked`, adapters must not put the raw payload in `statement`. Drop or store a handle only.

## Operator paste

Pasted text is not “already safe.” Run the same pass. The operator can mark a field `public` **after** seeing the redacted preview.

Policy version string: `redaction-v0.1` for this revision.
